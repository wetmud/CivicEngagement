# PLAN: --discover mode for pipeline.py

## Goal
Add a `--discover` mode to `pipeline.py` that scrapes the eSCRIBE calendar for the last 6 months, checks which meetings have video streams, filters out already-processed dates, and prints a queue of up to 10 unprocessed dates. With `--auto`, runs the full pipeline on each.

## Architecture
Single new code path in `pipeline.py`. No new files.

```
pipeline.py --discover
  └─ 1. Playwright → scrape eSCRIBE calendar pages for last 6 months
  └─ 2. Collect all meeting UUIDs + dates
  └─ 3. For each: lightweight stream check (does lookup_stream resolve?)
  └─ 4. Load index.json → filter out already-processed dates
  └─ 5. Print queue (max 10)

pipeline.py --discover --auto
  └─ Steps 1-5 above, then:
  └─ 6. For each queued date: run full 6-step pipeline (existing main flow)
```

## Tech Stack
- Python 3, argparse, Playwright (already installed), `urllib.request` for HEAD checks
- No new dependencies

## File Structure
Only one file changes: `scripts/pipeline.py`

---

## Tasks

### Task 1: Refactor argparse to support --discover mode

**What:** Make `date` positional arg optional (required only when not using `--discover`). Add `--discover` and `--auto` flags.

**Where:** `parse_args()` function, lines 46-56.

**Code — replace the current `parse_args()` with:**

```python
def parse_args():
    parser = argparse.ArgumentParser(
        description="Burlington council meeting pipeline",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=__doc__,
    )
    parser.add_argument("date", nargs="?", default=None,
                        help="Meeting date in YYYY-MM-DD format (required unless --discover)")
    parser.add_argument("--discover",         action="store_true",
                        help="Scrape eSCRIBE for unprocessed meetings with available streams")
    parser.add_argument("--auto",             action="store_true",
                        help="With --discover: auto-run pipeline on each queued date")
    parser.add_argument("--skip-download",    action="store_true", help="Reuse existing audio")
    parser.add_argument("--skip-transcribe",  action="store_true", help="Reuse existing .vtt")
    parser.add_argument("--output-dir",       help="Temp file directory")

    args = parser.parse_args()

    if args.auto and not args.discover:
        parser.error("--auto requires --discover")
    if not args.discover and not args.date:
        parser.error("date is required unless --discover is used")

    return args
```

**Verify:**
```bash
python3 scripts/pipeline.py --help
# Should show --discover and --auto flags, date as optional

python3 scripts/pipeline.py --auto
# Should error: "--auto requires --discover"

python3 scripts/pipeline.py
# Should error: "date is required unless --discover is used"

python3 scripts/pipeline.py 2026-02-17
# Should still work as before (will prompt about existing summary)
```

---

### Task 2: Add `scrape_calendar_dates()` function

**What:** New function that uses Playwright to visit eSCRIBE calendar pages for each of the last 6 months and collects all meeting UUIDs + dates.

**Where:** Add after `validate_date()` (after line 66), before `discover_stream_url()`.

**Code:**

```python
# ── Discovery helpers ─────────────────────────────────────────────────────────

def scrape_calendar_dates() -> list[dict]:
    """
    Scrape eSCRIBE calendar for the last 6 months.
    Returns list of dicts: [{"date": "YYYY-MM-DD", "uuid": "...", "title": "..."}, ...]
    """
    from datetime import timedelta
    try:
        from playwright.sync_api import sync_playwright
    except ImportError:
        print("Error: playwright not installed.")
        sys.exit(1)

    meeting_url_re = re.compile(
        r"Meeting\.aspx\?Id=([0-9a-f\-]{36})", re.IGNORECASE
    )
    date_re = re.compile(r"(\w+ \d{1,2}, \d{4})")

    # Build list of first-of-month dates for last 6 months
    today = datetime.now()
    months = []
    for i in range(6):
        d = today.replace(day=1) - timedelta(days=30 * i)
        first = d.replace(day=1)
        months.append(first.strftime("%Y-%m-%d"))

    meetings = []
    seen_uuids = set()

    print(f"Scanning eSCRIBE calendar for {len(months)} months...")

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        page.set_extra_http_headers(HEADERS)

        for month_date in months:
            url = f"{ESCRIBE_BASE}/MeetingsCalendarView.aspx?StartDate={month_date}"
            print(f"  Loading: {month_date[:7]}...", end=" ", flush=True)
            try:
                page.goto(url, wait_until="networkidle", timeout=30000)
            except Exception as e:
                print(f"FAILED ({e})")
                continue

            links = page.eval_on_selector_all(
                "a[href]",
                "els => els.map(e => ({ href: e.getAttribute('href'), text: e.innerText }))"
            )

            count = 0
            for link in links:
                href = link.get("href") or ""
                text = (link.get("text") or "").strip()
                m = meeting_url_re.search(href)
                if not m:
                    continue
                uuid = m.group(1)
                if uuid in seen_uuids:
                    continue
                seen_uuids.add(uuid)

                # Try to extract a date from the link text
                # eSCRIBE typically shows "Meeting Type - Month DD, YYYY"
                dm = date_re.search(text)
                if dm:
                    try:
                        parsed = datetime.strptime(dm.group(1), "%B %d, %Y")
                        iso_date = parsed.strftime("%Y-%m-%d")
                    except ValueError:
                        continue
                else:
                    continue

                meetings.append({
                    "date": iso_date,
                    "uuid": uuid,
                    "title": text.split(" - ")[0].strip() if " - " in text else text,
                })
                count += 1

            print(f"{count} meetings found")

        browser.close()

    # Sort by date descending
    meetings.sort(key=lambda m: m["date"], reverse=True)
    print(f"  Total: {len(meetings)} unique meetings across {len(months)} months")
    return meetings
```

**Verify:**
```bash
python3 -c "
import sys; sys.path.insert(0, 'scripts')
from pipeline import scrape_calendar_dates
results = scrape_calendar_dates()
for r in results[:5]:
    print(r)
"
# Should print dicts with date, uuid, title for recent Burlington meetings
```

---

### Task 3: Add `check_stream_exists()` function

**What:** Lightweight check whether a meeting UUID has a video stream. Uses Playwright to load the meeting page and intercept the `lookup_stream` request, but does NOT download anything. Returns the stream name if found, `None` otherwise.

**Where:** Add directly after `scrape_calendar_dates()`.

**Design decision:** We need Playwright here (not a simple HTTP request) because the `lookup_stream` URL is triggered by JavaScript on the meeting page. But we can reuse a single browser instance for all checks by accepting a `page` parameter.

**Code:**

```python
def check_stream_exists(uuid: str, page) -> str | None:
    """
    Load a meeting page and check if lookup_stream fires.
    Returns stream_name if found, None otherwise.
    Does NOT download anything.
    """
    captured = {"stream_name": None}

    def handle_request(request):
        if "lookup_stream" in request.url and "stream_name" in request.url:
            m = re.search(r"stream_name=([^&]+)", request.url)
            if m:
                captured["stream_name"] = m.group(1)

    meeting_url = f"{ESCRIBE_BASE}/Meeting.aspx?Id={uuid}&Agenda=Agenda&lang=English"

    page.on("request", handle_request)
    try:
        page.goto(meeting_url, wait_until="networkidle", timeout=20000)
        page.wait_for_timeout(2000)
    except Exception:
        pass
    page.remove_listener("request", handle_request)

    return captured["stream_name"]
```

**Verify:**
```bash
# Use a known meeting UUID from Task 2 output
python3 -c "
from playwright.sync_api import sync_playwright
import sys; sys.path.insert(0, 'scripts')
from pipeline import check_stream_exists, HEADERS
with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    page = browser.new_page()
    page.set_extra_http_headers(HEADERS)
    result = check_stream_exists('PASTE_UUID_HERE', page)
    print(f'Stream: {result}')
    browser.close()
"
# Should print a stream_name string or None
```

---

### Task 4: Add `load_processed_dates()` helper

**What:** Reads `index.json` and returns a set of already-processed date strings.

**Where:** Add after `check_stream_exists()`.

**Code:**

```python
def load_processed_dates() -> set[str]:
    """Load already-processed dates from index.json."""
    if INDEX_FILE.exists():
        return set(json.loads(INDEX_FILE.read_text()))
    return set()
```

**Verify:** Trivial — tested implicitly in Task 5.

---

### Task 5: Add `discover()` function — the main discovery orchestrator

**What:** Ties together scraping, stream checking, filtering, and printing. Returns the queue list.

**Where:** Add after `load_processed_dates()`.

**Code:**

```python
def discover() -> list[dict]:
    """
    Discover unprocessed meetings with available video streams.
    Returns up to 10 dicts: [{"date": ..., "uuid": ..., "title": ..., "stream_name": ...}]
    """
    MAX_QUEUE = 10

    # Step 1: Scrape calendar
    all_meetings = scrape_calendar_dates()

    if not all_meetings:
        print("\nNo meetings found on eSCRIBE calendar.")
        return []

    # Step 2: Filter out already-processed dates
    processed = load_processed_dates()
    unprocessed = [m for m in all_meetings if m["date"] not in processed]

    if not unprocessed:
        print(f"\nAll {len(all_meetings)} discovered meetings are already processed.")
        return []

    print(f"\n{len(unprocessed)} unprocessed meetings found. Checking for video streams...")

    # Step 3: Check each for a video stream (stop once we have MAX_QUEUE hits)
    try:
        from playwright.sync_api import sync_playwright
    except ImportError:
        print("Error: playwright not installed.")
        sys.exit(1)

    queue = []

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        page.set_extra_http_headers(HEADERS)

        for m in unprocessed:
            if len(queue) >= MAX_QUEUE:
                break
            print(f"  Checking {m['date']} ({m['title']})...", end=" ", flush=True)
            stream_name = check_stream_exists(m["uuid"], page)
            if stream_name:
                print(f"HAS STREAM")
                m["stream_name"] = stream_name
                queue.append(m)
            else:
                print(f"no stream")

        browser.close()

    # Step 4: Print queue
    print(f"\n{'='*60}")
    print(f"  Discovery Results: {len(queue)} meetings ready to process")
    print(f"{'='*60}")
    for i, m in enumerate(queue, 1):
        print(f"  {i}. {m['date']}  {m['title']}")
    if not queue:
        print("  No unprocessed meetings with video streams found.")
    print()

    return queue
```

**Verify:**
```bash
python3 scripts/pipeline.py --discover
# Should print calendar scraping progress, stream checks, then a numbered list
# of up to 10 unprocessed dates with streams
```

---

### Task 6: Add `run_pipeline_for_date()` — extract existing main logic into a callable function

**What:** Refactor the pipeline execution out of `main()` into a standalone function so `--auto` can call it in a loop. The function takes a date string and the parsed args, runs steps 1-6.

**Where:** Replace the body of `main()`. Add a new function before `main()`.

**Code:**

```python
def run_pipeline_for_date(date: str, args):
    """Run the full 6-step pipeline for a single date."""
    date = validate_date(date)

    output_dir = Path(args.output_dir) if args.output_dir else Path(f"/tmp/burlington/{date}")
    output_dir.mkdir(parents=True, exist_ok=True)

    api_key = os.environ.get("ANTHROPIC_API_KEY")
    if not api_key:
        print("Error: ANTHROPIC_API_KEY environment variable not set.")
        print("  export ANTHROPIC_API_KEY=your_key_here")
        sys.exit(1)

    print(f"\n{'='*60}")
    print(f"  Burlington Meeting Pipeline -- {date}")
    print(f"  Temp dir: {output_dir}")
    print(f"{'='*60}\n")

    # Check if summary already exists
    summary_path = MEETINGS_DIR / f"{date}.json"
    if summary_path.exists():
        print(f"  Skipping {date} -- summary already exists at {summary_path}")
        return

    # Step 1-6 (same as current main body, lines 380-430)
    if args.skip_download and (output_dir / "raw.mp4").exists():
        hls_url = None
        raw_audio = output_dir / "raw.mp4"
        print("Step 1: Skipping stream discovery -- reusing existing audio")
    elif args.skip_download and (output_dir / "raw.mp3").exists():
        hls_url = None
        raw_audio = output_dir / "raw.mp3"
        print("Step 1: Skipping stream discovery -- reusing existing audio")
    elif args.skip_transcribe and (output_dir / "trimmed.vtt").exists():
        hls_url = None
        raw_audio = None
        print("Step 1: Skipping stream discovery -- reusing existing VTT")
    else:
        hls_url = discover_stream_url(date)
        raw_audio = None

    if raw_audio is None and not (args.skip_transcribe and (output_dir / "trimmed.vtt").exists()):
        raw_audio = download_audio(hls_url, output_dir, skip=args.skip_download)

    if not (args.skip_transcribe and (output_dir / "trimmed.vtt").exists()):
        trimmed_audio = trim_silence(raw_audio, output_dir)
    else:
        trimmed_audio = None
        print("Step 3: Skipping silence trim -- reusing existing VTT")

    vtt_path = transcribe(
        trimmed_audio or output_dir / "trimmed.mp3",
        output_dir,
        skip=args.skip_transcribe,
    )

    summary = summarize(vtt_path, date, api_key)
    update_index(date)

    print(f"\n{'='*60}")
    print(f"  Done! Meeting summary for {date} is ready.")
    print(f"{'='*60}")
    print(f"\nTLDR: {summary.get('tldr', 'N/A')}\n")
```

---

### Task 7: Update `main()` to dispatch --discover vs single-date mode

**Where:** Replace the existing `main()` function (lines 353-434).

**Code:**

```python
def main():
    args = parse_args()

    if args.discover:
        queue = discover()

        if not queue:
            sys.exit(0)

        if not args.auto:
            print("Run with --discover --auto to process these automatically.")
            print("Or run individually:")
            for m in queue:
                print(f"  python3 scripts/pipeline.py {m['date']}")
            sys.exit(0)

        # --auto mode: process each queued date
        print(f"Auto-processing {len(queue)} meetings...\n")
        succeeded = []
        failed = []

        for i, m in enumerate(queue, 1):
            print(f"\n{'#'*60}")
            print(f"  [{i}/{len(queue)}] Processing {m['date']} — {m['title']}")
            print(f"{'#'*60}")
            try:
                run_pipeline_for_date(m["date"], args)
                succeeded.append(m["date"])
            except SystemExit:
                print(f"  FAILED: {m['date']} — skipping")
                failed.append(m["date"])
            except Exception as e:
                print(f"  FAILED: {m['date']} — {e}")
                failed.append(m["date"])

        # Summary
        print(f"\n{'='*60}")
        print(f"  Batch Complete")
        print(f"{'='*60}")
        print(f"  Succeeded: {len(succeeded)}")
        for d in succeeded:
            print(f"    {d}")
        if failed:
            print(f"  Failed: {len(failed)}")
            for d in failed:
                print(f"    {d}")
        print(f"\nTo publish:")
        print(f"  git add meetings/burlington/")
        print(f"  git commit -m \"Add {len(succeeded)} council meeting summaries\"")
        print(f"  git push")

    else:
        # Original single-date mode
        run_pipeline_for_date(args.date, args)
        print(f"\nTo publish:")
        print(f"  git add meetings/burlington/")
        print(f"  git commit -m \"Add {args.date} council meeting summary\"")
        print(f"  git push")
        print()
```

**Verify:**
```bash
# Discovery only (no processing)
python3 scripts/pipeline.py --discover
# Should list meetings, then print "Run with --discover --auto..."

# Full auto-batch (the real deal — takes hours)
python3 scripts/pipeline.py --discover --auto
# Should discover, then process each date sequentially

# Single-date mode still works
python3 scripts/pipeline.py 2026-02-17
# Should behave exactly as before
```

---

### Task 8: Handle SystemExit gracefully in --auto mode

**What:** The existing pipeline calls `sys.exit(1)` on failures (no stream found, yt-dlp fails, etc). In `--auto` mode, we catch `SystemExit` so one failed date doesn't kill the whole batch. This is already handled in the Task 7 code above via `except SystemExit`.

**Verify:** Kill a run mid-way (Ctrl+C), then re-run `--discover --auto`. Already-processed dates should be skipped (resumability comes from the `summary_path.exists()` check in `run_pipeline_for_date` + the `index.json` filter in `discover()`).

---

### Task 9: Update docstring and CLAUDE.md

**What:** Update the module docstring at the top of `pipeline.py` and `scripts/CLAUDE.md` to document the new flags.

**Where:**
- `pipeline.py` lines 2-21: add `--discover` and `--auto` to the Usage section
- `scripts/CLAUDE.md`: add a "Discovery Mode" section

**Docstring update:**

```python
"""
Burlington Council Meeting Pipeline
------------------------------------
Full pipeline: stream discovery → download → transcribe → summarize → update index.

Usage:
  python3 scripts/pipeline.py <YYYY-MM-DD> [options]
  python3 scripts/pipeline.py --discover [--auto]

Single-date options:
  --skip-download     Reuse existing audio in output dir (skip yt-dlp)
  --skip-transcribe   Reuse existing .vtt in output dir (skip mlx_whisper)
  --output-dir PATH   Temp file directory (default: /tmp/burlington/{date}/)

Discovery options:
  --discover          Scrape eSCRIBE for unprocessed meetings with video streams
  --auto              With --discover: auto-run pipeline on each (max 10 per run)
"""
```

**Verify:**
```bash
python3 scripts/pipeline.py --help
# Should show all options clearly
```

---

## Implementation Order

1. Task 1 — argparse refactor (unblocks everything)
2. Task 4 — `load_processed_dates()` (trivial, no deps)
3. Task 2 — `scrape_calendar_dates()` (test independently)
4. Task 3 — `check_stream_exists()` (test independently)
5. Task 5 — `discover()` orchestrator (needs 2, 3, 4)
6. Task 6 — `run_pipeline_for_date()` extract (refactor only, doesn't change behavior)
7. Task 7 — `main()` rewrite (needs 5, 6)
8. Task 8 — verify resumability (manual test)
9. Task 9 — docs update

## Estimated Time

- Tasks 1-7 coding: ~45 minutes
- Task 8 testing: ~10 minutes (run --discover, verify output, kill mid-auto, re-run)
- Task 9 docs: ~5 minutes
- Full --auto run: ~hours (depends on number of meetings found)

## Risks

- **eSCRIBE date format varies:** The calendar link text might not always be "Month DD, YYYY". If Task 2 misses dates, add more date parsing patterns.
- **Rate limiting:** Hitting eSCRIBE with 6 calendar pages + N meeting page checks in quick succession. Add a 1-2 second delay between stream checks if they start blocking.
- **Playwright listener cleanup:** `check_stream_exists` must remove its listener after each call to avoid stacking handlers. The code uses `remove_listener` for this.
