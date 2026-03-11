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

import time

import anthropic
import pdfplumber
import requests
import urllib3
from bs4 import BeautifulSoup

# Suppress SSL warnings for the eSCRIBE municipal portal — its intermediate
# cert is not in the GitHub Actions trust store but the site is a known source.
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# ── Config ────────────────────────────────────────────────────────────────────

ESCRIBE_BASE    = "https://burlingtonpublishing.escribemeetings.com"
MEETING_PAGE    = f"{ESCRIBE_BASE}/Meeting.aspx"
FILESTREAM      = f"{ESCRIBE_BASE}/filestream.ashx"
OUTPUT_DIR      = Path(__file__).parent.parent / "meetings" / "burlington"
INDEX_FILE      = OUTPUT_DIR / "index.json"
CLAUDE_MODEL    = "claude-sonnet-4-20250514"
REQUEST_TIMEOUT = 30
REQUEST_DELAY   = 2   # seconds between HTTP requests — be polite
SSL_VERIFY      = False  # eSCRIBE cert chain not trusted by GH Actions runner

CALENDAR_URL = f"{ESCRIBE_BASE}/MeetingsCalendarView.aspx"

HEADERS = {
    "User-Agent": "CivicConnect/1.0 (civic engagement tool; github.com/wetmud/CivicConnect)",
    "Accept": "text/html, */*",
}

# ── Helpers ───────────────────────────────────────────────────────────────────

def get(url: str, **kwargs) -> requests.Response:
    time.sleep(REQUEST_DELAY)
    r = requests.get(url, headers=HEADERS, timeout=REQUEST_TIMEOUT, verify=SSL_VERIFY, **kwargs)
    r.raise_for_status()
    return r

# ── Step 1: Fetch recent meetings by scraping the public HTML calendar ────────
# The eSCRIBE AJAX endpoints require ASP.NET session state that is not reliably
# reproducible in CI. Instead, we scrape Meeting.aspx links directly from the
# public calendar HTML — no session or auth required.

def fetch_recent_meetings(limit: int = 5) -> list[dict]:
    """Returns list of dicts with keys: id (UUID), title, date (YYYY-MM-DD)."""
    print("Fetching meetings from eSCRIBE calendar HTML...")
    resp = get(CALENDAR_URL)
    soup = BeautifulSoup(resp.text, "html.parser")

    seen = set()
    meetings = []

    # Meeting links look like: Meeting.aspx?Id=<UUID>&Agenda=...&lang=English
    uuid_re = re.compile(
        r"Meeting\.aspx\?Id=([0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12})",
        re.IGNORECASE,
    )

    for tag in soup.find_all(["a", "div", "span", "td"], string=True):
        href = tag.get("href", "")
        m = uuid_re.search(href)
        if not m:
            # Also check data attributes and onclick values
            for attr in ("onclick", "data-url", "data-id"):
                val = tag.get(attr, "")
                m = uuid_re.search(val)
                if m:
                    break
        if not m:
            continue
        mid = m.group(1)
        if mid in seen:
            continue
        seen.add(mid)

        # Try to extract a title and date from nearby text
        title = tag.get_text(strip=True) or "Council Meeting"
        date_str = _extract_date_near(tag)
        meetings.append({"id": mid, "title": title, "date": date_str or ""})

    # Also scan raw HTML for UUIDs not in visible links (JS-rendered menus etc.)
    for m in uuid_re.finditer(resp.text):
        mid = m.group(1)
        if mid not in seen:
            seen.add(mid)
            meetings.append({"id": mid, "title": "Council Meeting", "date": ""})

    # For meetings without a parsed date, fetch the meeting page to get it
    filled = []
    for mtg in meetings[:limit * 3]:  # fetch a few extra in case some lack dates
        if not mtg["date"]:
            mtg["date"] = _fetch_meeting_date(mtg["id"]) or ""
        if mtg["date"]:
            filled.append(mtg)
        if len(filled) >= limit:
            break

    # Sort newest-first
    filled.sort(key=lambda x: x["date"], reverse=True)
    result = filled[:limit]
    print(f"  Found {len(result)} meetings.")
    return result

def _extract_date_near(tag) -> str | None:
    """Looks for a date string in the tag's text or its parent's text."""
    for node in [tag, tag.parent, tag.parent.parent if tag.parent else None]:
        if node is None:
            continue
        text = node.get_text(" ", strip=True)
        d = _parse_date(text)
        if d:
            return d
    return None

def _fetch_meeting_date(meeting_id: str) -> str | None:
    """Fetches the meeting page and extracts the date from its title/header."""
    try:
        url = f"{MEETING_PAGE}?Id={meeting_id}&Agenda=Agenda&lang=English"
        resp = get(url)
        soup = BeautifulSoup(resp.text, "html.parser")
        # eSCRIBE typically puts the date in the page <title> or a heading
        candidates = [soup.title, soup.find("h1"), soup.find("h2"),
                      soup.find(class_=re.compile(r"meeting.?title|event.?title", re.I))]
        for el in candidates:
            if el:
                d = _parse_date(el.get_text(" ", strip=True))
                if d:
                    return d
    except Exception:
        pass
    return None

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
