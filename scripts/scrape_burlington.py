#!/usr/bin/env python3
"""
Burlington City Council Meeting Summarizer
------------------------------------------
Fetches the latest meeting minutes from Burlington's eSCRIBE portal,
extracts text from PDFs, and uses Claude to produce a journalist-style
JSON summary committed to meetings/burlington/.

Requires:
  pip install requests pdfplumber anthropic beautifulsoup4

Environment:
  ANTHROPIC_API_KEY  — Anthropic API key (GitHub Secret in CI)
"""

import json
import os
import re
import sys
import tempfile
from datetime import datetime, timezone
from pathlib import Path

import anthropic
import pdfplumber
import requests
from bs4 import BeautifulSoup

# ── Config ────────────────────────────────────────────────────────────────────

ESCRIBE_BASE    = "https://burlingtonpublishing.escribemeetings.com"
PAST_MEETINGS   = f"{ESCRIBE_BASE}/MeetingsCalendarView.aspx/PastMeetings"
MEETING_PAGE    = f"{ESCRIBE_BASE}/Meeting.aspx"
FILESTREAM      = f"{ESCRIBE_BASE}/filestream.ashx"
OUTPUT_DIR      = Path(__file__).parent.parent / "meetings" / "burlington"
INDEX_FILE      = OUTPUT_DIR / "index.json"
CLAUDE_MODEL    = "claude-sonnet-4-20250514"
REQUEST_TIMEOUT = 30
REQUEST_DELAY   = 2   # seconds between HTTP requests — be polite

HEADERS = {
    "User-Agent": "CivicConnect/1.0 (civic engagement tool; github.com/wetmud/CivicConnect)",
    "Accept": "application/json, text/html, */*",
}

# ── Helpers ───────────────────────────────────────────────────────────────────

import time

def get(url: str, **kwargs) -> requests.Response:
    time.sleep(REQUEST_DELAY)
    r = requests.get(url, headers=HEADERS, timeout=REQUEST_TIMEOUT, **kwargs)
    r.raise_for_status()
    return r

def post_json(url: str, payload: dict) -> dict:
    time.sleep(REQUEST_DELAY)
    r = requests.post(
        url,
        headers={**HEADERS, "Content-Type": "application/json"},
        json=payload,
        timeout=REQUEST_TIMEOUT,
    )
    r.raise_for_status()
    return r.json()

# ── Step 1: Fetch recent meetings ─────────────────────────────────────────────

def fetch_recent_meetings(page_size: int = 10) -> list[dict]:
    """Returns list of dicts with keys: id (UUID), title, date (YYYY-MM-DD)."""
    print("Fetching recent meetings from eSCRIBE...")
    data = post_json(PAST_MEETINGS, {"pageIndex": 0, "pageSize": page_size, "meetingType": ""})
    meetings = []
    # eSCRIBE returns a 'd' wrapper with 'aaData' rows
    rows = data.get("d", {}).get("aaData", []) if isinstance(data.get("d"), dict) else []
    # Fallback: sometimes the response is just a list
    if not rows and isinstance(data.get("d"), list):
        rows = data["d"]
    for row in rows:
        # Each row is typically [id, title, date_str, ...]
        if isinstance(row, list) and len(row) >= 3:
            meeting_id   = row[0]
            meeting_title = row[1] if isinstance(row[1], str) else str(row[1])
            date_raw     = row[2] if isinstance(row[2], str) else str(row[2])
        elif isinstance(row, dict):
            meeting_id    = row.get("Id") or row.get("id") or row.get("MeetingId")
            meeting_title = row.get("Title") or row.get("title") or ""
            date_raw      = row.get("Date") or row.get("MeetingDate") or ""
        else:
            continue
        # Normalise date to YYYY-MM-DD
        date_str = _parse_date(str(date_raw))
        if meeting_id and date_str:
            meetings.append({"id": meeting_id, "title": meeting_title, "date": date_str})
    print(f"  Found {len(meetings)} meetings.")
    return meetings

def _parse_date(raw: str) -> str | None:
    """Converts various date formats to YYYY-MM-DD, or None if unparseable."""
    # Handle /Date(1234567890000)/ format
    m = re.search(r"/Date\((\d+)", raw)
    if m:
        ts = int(m.group(1)) / 1000
        return datetime.fromtimestamp(ts, tz=timezone.utc).strftime("%Y-%m-%d")
    for fmt in ("%Y-%m-%d", "%B %d, %Y", "%d/%m/%Y", "%m/%d/%Y"):
        try:
            return datetime.strptime(raw.strip(), fmt).strftime("%Y-%m-%d")
        except ValueError:
            pass
    return None

# ── Step 2: Check if already summarised ──────────────────────────────────────

def already_summarised(date: str) -> bool:
    return (OUTPUT_DIR / f"{date}.json").exists()

# ── Step 3: Find minutes PDF on meeting page ──────────────────────────────────

def find_minutes_pdf(meeting_id: str) -> tuple[str | None, str | None]:
    """Returns (document_id, source_url) for the minutes PDF, or (None, None)."""
    source_url = f"{MEETING_PAGE}?Id={meeting_id}&Agenda=PostMinutes&lang=English"
    print(f"  Fetching meeting page: {source_url}")
    resp = get(source_url)
    soup = BeautifulSoup(resp.text, "html.parser")

    for link in soup.find_all("a", href=True):
        href = link["href"]
        text = link.get_text(strip=True).lower()
        if "filestream.ashx" in href and ("minute" in text or "minutes" in text):
            m = re.search(r"DocumentId=(\d+)", href, re.IGNORECASE)
            if m:
                return m.group(1), source_url

    # Fallback: try the Agenda view for links labelled "Minutes"
    agenda_url = f"{MEETING_PAGE}?Id={meeting_id}&Agenda=Agenda&lang=English"
    resp2 = get(agenda_url)
    soup2 = BeautifulSoup(resp2.text, "html.parser")
    for link in soup2.find_all("a", href=True):
        href = link["href"]
        text = link.get_text(strip=True).lower()
        if "filestream.ashx" in href and "minute" in text:
            m = re.search(r"DocumentId=(\d+)", href, re.IGNORECASE)
            if m:
                return m.group(1), agenda_url

    print("  ⚠️  No minutes PDF found — meeting may not have published minutes yet.")
    return None, None

# ── Step 4: Download PDF and extract text ────────────────────────────────────

def extract_pdf_text(document_id: str) -> str:
    """Downloads PDF and returns extracted plain text."""
    pdf_url = f"{FILESTREAM}?DocumentId={document_id}"
    print(f"  Downloading PDF (DocumentId={document_id})...")
    resp = get(pdf_url)

    with tempfile.NamedTemporaryFile(suffix=".pdf", delete=False) as tmp:
        tmp.write(resp.content)
        tmp_path = tmp.name

    try:
        text_parts = []
        with pdfplumber.open(tmp_path) as pdf:
            for page in pdf.pages:
                text = page.extract_text()
                if text:
                    text_parts.append(text)
        raw = "\n".join(text_parts)
        # Collapse excessive whitespace while preserving paragraph breaks
        cleaned = re.sub(r"\n{3,}", "\n\n", raw).strip()
        print(f"  Extracted {len(cleaned):,} characters from PDF.")
        return cleaned
    finally:
        os.unlink(tmp_path)

# ── Step 5: Summarise with Claude ─────────────────────────────────────────────

SUMMARY_PROMPT = """You are analysing official city council meeting minutes for Burlington, Ontario, Canada.

Your job is to produce a structured JSON summary that reads like a clear, neutral journalistic breakdown — as if you were a reporter who sat through the whole meeting and is filing a story about what actually happened and whether the meeting was productive.

Return ONLY valid JSON matching this schema exactly (no markdown, no commentary):

{
  "tldr": "2-3 sentence plain-English summary of what happened at this meeting",
  "productive_minutes": <integer estimate of time spent on substantive decisions>,
  "procedural_minutes": <integer estimate of time on roll call, procedural motions, recesses, etc.>,
  "items": [
    {
      "title": "short descriptive title of the agenda item",
      "outcome": "Passed|Failed|Deferred|Received|Noted|Withdrawn",
      "vote": "e.g. 6-1, or null if no recorded vote",
      "estimated_minutes": <integer, your best estimate of time spent>,
      "notes": "1-2 sentence plain-English explanation of what this item was and what happened"
    }
  ],
  "deferred": ["list of item titles that were deferred, tabled, or rescheduled"]
}

Guidelines:
- Be precise and neutral. No editorialising.
- If vote counts are in the minutes, use them. If not, set "vote" to null.
- Time estimates: use any timestamps in the minutes if present; otherwise estimate based on item complexity.
- "Received" means an information item with no vote. "Noted" means acknowledged without action.
- Include ALL substantive agenda items — do not skip any.
- Deferred items should also appear in "items" with outcome "Deferred", AND be listed in "deferred".
- productive_minutes + procedural_minutes should roughly equal total meeting duration.

Meeting minutes text:
---
{minutes_text}
---"""

def summarise_with_claude(minutes_text: str, api_key: str) -> dict:
    """Calls Claude API and returns parsed JSON summary dict."""
    print("  Sending to Claude for summarisation...")
    client = anthropic.Anthropic(api_key=api_key)

    # Truncate if very long (Claude context window is large but be safe)
    if len(minutes_text) > 180_000:
        minutes_text = minutes_text[:180_000] + "\n\n[truncated for length]"

    message = client.messages.create(
        model=CLAUDE_MODEL,
        max_tokens=4096,
        messages=[{
            "role": "user",
            "content": SUMMARY_PROMPT.replace("{minutes_text}", minutes_text),
        }],
    )

    raw = message.content[0].text.strip()

    # Strip markdown code fences if Claude adds them
    raw = re.sub(r"^```(?:json)?\s*", "", raw)
    raw = re.sub(r"\s*```$", "", raw)

    return json.loads(raw)

# ── Step 6: Write output ──────────────────────────────────────────────────────

def write_summary(date: str, meeting_title: str, source_url: str, summary: dict) -> Path:
    out = {
        "date": date,
        "meeting_type": meeting_title,
        "source_url": source_url,
        "generated_at": datetime.now(tz=timezone.utc).isoformat(),
        **summary,
    }
    path = OUTPUT_DIR / f"{date}.json"
    path.write_text(json.dumps(out, indent=2, ensure_ascii=False))
    print(f"  ✅ Wrote {path}")
    return path

def update_index(new_date: str):
    """Maintains index.json listing all available summaries sorted newest-first."""
    existing = []
    if INDEX_FILE.exists():
        existing = json.loads(INDEX_FILE.read_text())
    if new_date not in existing:
        existing.insert(0, new_date)
    existing.sort(reverse=True)
    INDEX_FILE.write_text(json.dumps(existing, indent=2))
    print(f"  ✅ Updated index.json ({len(existing)} entries)")

# ── Main ──────────────────────────────────────────────────────────────────────

def main():
    api_key = os.environ.get("ANTHROPIC_API_KEY")
    if not api_key:
        print("ERROR: ANTHROPIC_API_KEY environment variable not set.", file=sys.stderr)
        sys.exit(1)

    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    meetings = fetch_recent_meetings(page_size=5)
    if not meetings:
        print("No meetings returned — the eSCRIBE API response format may have changed.")
        sys.exit(0)

    new_summaries = 0
    for meeting in meetings:
        date  = meeting["date"]
        title = meeting["title"]
        mid   = meeting["id"]

        print(f"\n{'─'*60}")
        print(f"Meeting: {title} | {date}")

        if already_summarised(date):
            print(f"  ↩️  Already summarised — skipping.")
            continue

        doc_id, source_url = find_minutes_pdf(mid)
        if not doc_id:
            continue

        try:
            text = extract_pdf_text(doc_id)
        except Exception as e:
            print(f"  ❌ PDF extraction failed: {e}")
            continue

        if len(text) < 200:
            print(f"  ⚠️  Extracted text too short ({len(text)} chars) — skipping.")
            continue

        try:
            summary = summarise_with_claude(text, api_key)
        except json.JSONDecodeError as e:
            print(f"  ❌ Claude returned invalid JSON: {e}")
            continue
        except Exception as e:
            print(f"  ❌ Claude API error: {e}")
            continue

        write_summary(date, title, source_url, summary)
        update_index(date)
        new_summaries += 1

    print(f"\n{'='*60}")
    print(f"Done. {new_summaries} new summary/summaries written.")
    # Exit code 0 always — GitHub Actions will only commit if files changed
    sys.exit(0)

if __name__ == "__main__":
    main()
