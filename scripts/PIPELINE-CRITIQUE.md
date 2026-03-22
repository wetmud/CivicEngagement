# Pipeline Plan — Project Shepherd Critique
*Generated 2026-03-20 using Project Shepherd agent (msitarzewski/agency-agents)*

---

## What Works Well

The plan is unusually well-structured for a solo project. Task ordering is logical, each task has isolated verify steps, risks are named, and the `--auto` batch mode includes resumability through `summary_path.exists()` + index.json filtering. That's a real failure-recovery pattern, not an afterthought.

---

## Issues & Improvements

**1. The date parsing regex is fragile and will silently drop meetings**

`date_re = re.compile(r"(\w+ \d{1,2}, \d{4})")` assumes eSCRIBE link text always looks like `"Council Meeting - February 17, 2026"`. If the format shifts (e.g. `"Feb. 17, 2026"` or `"2026-02-17"`), meetings get silently dropped. Fix: fall back to scraping the meeting detail page for the date rather than parsing the calendar link text.

**2. Playwright listener leaks in `check_stream_exists()`**

`page.on("request", handle_request)` + `page.remove_listener(...)` — if `page.goto()` throws before `remove_listener`, the listener is never cleaned up. Over 10+ meetings in `--auto` mode, handlers stack. Fix: wrap in try/finally.

**3. `run_pipeline_for_date()` catches `SystemExit` but reports nothing useful**

`sys.exit(1)` is called on ~6 failure modes. All collapse into the same "skipping" message. In an overnight batch, you'll have no idea if failures were network, missing stream, or dead API key. Fix: replace `sys.exit()` with raised exceptions that carry a reason string.

**4. No rate limiting between stream checks**

The plan mentions this risk but the code has no delay. 10 Playwright page loads with `networkidle` in a row will hit eSCRIBE hard. Add `time.sleep(REQUEST_DELAY)` between checks (same constant already used in the scraper).

**5. The `MAX_QUEUE = 10` cap is a buried magic constant**

If you have 15 unprocessed meetings, you need to run twice. Add a `--max N` flag — costs nothing.

**6. Two JSON schemas with no migration path**

Old PDF schema vs new Whisper schema. A third schema variation (adding `yes_voters`/`no_voters`) risks silent render failure. Fix: add `"schema": 2` version field to summarizer output and check it in `buildMeetingCard()`.

**7. `--auto` failure summary isn't persisted**

Terminal output is your only record. Write a `batch-{timestamp}.log` to `/tmp/burlington/` at the end of `--auto` runs.

---

## Prioritized Fixes

| Priority | Issue | Effort |
|----------|-------|--------|
| High | Playwright listener try/finally | 2 min |
| High | Replace `sys.exit()` with raised exceptions + better messages | 20 min |
| Medium | Rate limiting between stream checks | 2 min |
| Medium | Schema version field in summarizer output | 10 min |
| Low | `--max N` flag | 5 min |
| Low | Batch log file | 10 min |
| Later | Date parsing fallback to meeting detail page | 1–2 hrs |
