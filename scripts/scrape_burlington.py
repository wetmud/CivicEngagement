#!/usr/bin/env python3
"""
Burlington City Council Meeting Summarizer
------------------------------------------
Fetches the latest meeting minutes from Burlington's eSCRIBE portal,
extracts text from PDFs, and uses Claude to produce a journalist-style
JSON summary committed to meetings/burlington/.

Requires:
  pip install requests pdfplumber anthropic beautifulsoup4 playwright
  playwright install chromium

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

def _calendar_url_for_month(year: int, month: int) -> str:
    """eSCRIBE calendar accepts a StartDate param to load a specific month."""
    return f"{ESCRIBE_BASE}/MeetingsCalendarView.aspx?StartDate={year}-{month:02d}-01"

HEADERS = {
    "User-Agent": "CivicEngagement/1.0 (civic engagement tool; github.com/wetmud/CivicEngagement)",
    "Accept": "text/html, */*",
}

# ── Helpers ───────────────────────────────────────────────────────────────────

def get(url: str, **kwargs) -> requests.Response:
    time.sleep(REQUEST_DELAY)
    r = requests.get(url, headers=HEADERS, timeout=REQUEST_TIMEOUT, verify=SSL_VERIFY, **kwargs)
    r.raise_for_status()
    return r

# ── Step 1: Discover meeting UUIDs via Playwright (JS-rendered calendar) ──────
# The eSCRIBE calendar is fully JavaScript-rendered. We use a headless Chromium
# browser to load the page, wait for meeting links to appear, then extract UUIDs.

UUID_RE = re.compile(
    r"Meeting\.aspx\?Id=([0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12})",
    re.IGNORECASE,
)

def fetch_recent_meetings(limit: int = 5) -> list[dict]:
    """Returns list of dicts with keys: id (UUID), title, date (YYYY-MM-DD)."""
    from playwright.sync_api import sync_playwright

    print("Fetching meetings via headless browser (JS-rendered calendar)...")
    meetings_seen: dict[str, dict] = {}  # uuid → {id, title, date}

    # Load current month + previous month to catch recent meetings regardless of when
    # the scraper runs within the month. eSCRIBE defaults to current month only.
    now = datetime.now(tz=timezone.utc)
    months_to_check = []
    for delta in (0, -1):
        m = now.month + delta
        y = now.year
        if m < 1:
            m += 12
            y -= 1
        months_to_check.append((y, m))

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)

        for year, month in months_to_check:
            url = _calendar_url_for_month(year, month)
            print(f"  Loading calendar: {url}")
            page = browser.new_page()
            page.set_extra_http_headers(HEADERS)
            page.goto(url, wait_until="networkidle", timeout=30000)

            # Extract UUID + visible link text in one JS pass — the calendar renders
            # anchor text like "Regular Meeting of Council\nJanuary 14, 2025"
            link_data = page.eval_on_selector_all(
                "a[href]",
                "els => els.map(e => ({ href: e.getAttribute('href'), text: e.innerText }))"
            )
            print(f"    Raw links found: {len(link_data)}")
            for item in link_data:
                href = item.get("href") or ""
                text = (item.get("text") or "").strip()
                m = UUID_RE.search(href)
                if not m:
                    continue
                uid = m.group(1)
                if uid in meetings_seen:
                    continue
                print(f"    → UUID {uid[:8]}… | raw text: {repr(text[:80])}")
                date_str = _parse_date_from_text(text)
                title = text.split("\n")[0].strip() or "Burlington City Council"
                if date_str:
                    meetings_seen[uid] = {"id": uid, "title": title, "date": date_str}
                    print(f"      ✓ Parsed date: {date_str}")
                else:
                    print(f"      ✗ No date found in text")
                    meetings_seen[uid] = {"id": uid, "title": title, "date": None}

            # Fallback: scan raw HTML for any UUIDs we missed (JS-injected content)
            html = page.content()
            for m in UUID_RE.finditer(html):
                uid = m.group(1)
                if uid not in meetings_seen:
                    meetings_seen[uid] = {"id": uid, "title": "Burlington City Council", "date": None}
            page.close()

        browser.close()

    print(f"  Found {len(meetings_seen)} meeting UUID(s) in calendar.")

    # For any meetings where Playwright text didn't yield a date, fall back to
    # fetching the static meeting page (title tag often has a parseable date)
    dateless = [v for v in meetings_seen.values() if not v["date"]]
    print(f"  {len(meetings_seen) - len(dateless)} with dates from calendar; "
          f"{len(dateless)} need fallback resolution...")

    for entry in dateless:
        date_str, title = _fetch_meeting_meta(entry["id"])
        if date_str:
            entry["date"] = date_str
            entry["title"] = title
            print(f"    ✓ (fallback) {title} | {date_str}")

    # Keep only meetings with resolved dates, sort newest-first
    dated = [v for v in meetings_seen.values() if v["date"]]
    dated.sort(key=lambda x: x["date"], reverse=True)
    result = dated[:limit]
    print(f"  Resolved {len(result)} meetings with dates.")
    return result

# Date patterns that appear in eSCRIBE calendar link text
_DATE_PATTERNS = [
    (re.compile(r"\b(\w+ \d{1,2},\s*\d{4})\b"), "%B %d, %Y"),   # January 14, 2025
    (re.compile(r"\b(\d{4}-\d{2}-\d{2})\b"),      "%Y-%m-%d"),   # 2025-01-14
    (re.compile(r"\b(\d{1,2}/\d{1,2}/\d{4})\b"),  "%m/%d/%Y"),   # 01/14/2025
    (re.compile(r"\b(\d{1,2}-\w{3}-\d{4})\b"),    "%d-%b-%Y"),   # 14-Jan-2025
]

def _parse_date_from_text(text: str) -> str | None:
    """Scan arbitrary text for a recognisable date and return YYYY-MM-DD."""
    # Try /Date(ms)/ first
    m = re.search(r"/Date\((\d+)", text)
    if m:
        ts = int(m.group(1)) / 1000
        return datetime.fromtimestamp(ts, tz=timezone.utc).strftime("%Y-%m-%d")
    for pattern, fmt in _DATE_PATTERNS:
        for raw in pattern.findall(text):
            raw_clean = re.sub(r"\s+", " ", raw).strip()
            try:
                return datetime.strptime(raw_clean, fmt).strftime("%Y-%m-%d")
            except ValueError:
                continue
    return None

def _fetch_meeting_meta(meeting_id: str) -> tuple[str | None, str]:
    """Fetches the meeting page (static HTML) and extracts date + title.
    Used as a fallback when the calendar link text doesn't contain a parseable date."""
    try:
        url = f"{MEETING_PAGE}?Id={meeting_id}&Agenda=PostMinutes&lang=English"
        resp = get(url)
        soup = BeautifulSoup(resp.text, "html.parser")

        # Only look at structured elements — the old approach of scanning 3000 chars
        # of body text was catching copyright years, footers, etc. as false dates.
        candidates: list[str] = []
        for tag in ("title", "h1", "h2", "h3"):
            el = soup.find(tag)
            if el:
                candidates.append(el.get_text(" ", strip=True))
        # One extra pass: look for a <meta> description or OG title which often
        # contains the meeting name and date on eSCRIBE pages.
        for meta in soup.find_all("meta", attrs={"name": ["description", "og:title"]}):
            content = meta.get("content", "").strip()
            if content:
                candidates.append(content)

        date_str: str | None = None
        title = "Burlington City Council"
        for raw in candidates:
            if not date_str:
                date_str = _parse_date_from_text(raw)
            if raw and title == "Burlington City Council":
                candidate_title = raw.split("|")[0].strip()
                if candidate_title:
                    title = candidate_title
            if date_str and title != "Burlington City Council":
                break

        return date_str, title
    except Exception as e:
        print(f"    ⚠️  Could not resolve meta for {meeting_id}: {e}")
        return None, "Burlington City Council"


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

    meetings = fetch_recent_meetings(limit=5)
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
