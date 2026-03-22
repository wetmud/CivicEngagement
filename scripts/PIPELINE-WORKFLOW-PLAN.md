# Burlington Meeting Pipeline — Workflow Optimization Plan
*Generated 2026-03-20 using Workflow Optimizer + Project Shepherd + Data Engineer agents (msitarzewski/agency-agents)*

---

## 📈 Projected Impact

| Metric | Current | Optimized | Delta |
|--------|---------|-----------|-------|
| Pipeline reliability | ~70% (silent failures) | ~95% | +25pts |
| Debugging time per failure | 30–60 min | 5 min | −85% |
| Manual discovery work | 100% manual | ~0% | −100% |
| Batch resumability | Partial | Full | complete |
| Schema brittleness incidents | Unknown | 0 | eliminated |
| Data auditability | None | Full | new capability |

---

## 🔍 Current State Bottlenecks

**Bottleneck 1 — Silent failure cascade** *(Severity: 5/5)*
`sys.exit()` is used for error signaling across ~6 distinct failure modes (no stream, yt-dlp fail, API key missing, transcription fail, etc.). In `--auto` mode, all failures collapse to the same "skipping" message with no reason. After an overnight batch run you have no idea what went wrong.

**Bottleneck 2 — Fragile discovery layer** *(Severity: 4/5)*
Calendar scraping uses a single regex against unpredictable eSCRIBE link text. Any format variation (e.g. `"Feb. 17, 2026"` vs `"February 17, 2026"`) silently drops meetings from the queue. No warning, no log — they just vanish.

**Bottleneck 3 — No data auditability** *(Severity: 4/5)*
Meeting JSON files have no audit fields — no `ingested_at`, no `source_url`, no `pipeline_version`. You cannot tell when a file was processed, what version of the pipeline produced it, or where the audio came from. `index.json` is a flat array of date strings with no metadata, making it impossible to answer "which meetings need a backfill?" without opening every file.

**Bottleneck 4 — No observability** *(Severity: 3/5)*
No log file, no structured output, no way to audit a batch run after the terminal closes. Overnight runs are blind.

**Bottleneck 5 — Schema drift risk / broken data contract** *(Severity: 3/5)*
Two undeclared schemas already exist (PDF-scraped vs Whisper). A third is planned (voter name arrays). `buildMeetingCard()` is the sole consumer and will silently render broken at some future breakage point. There is no documented contract between pipeline output and frontend consumer.

**Bottleneck 6 — Resource leak under failure** *(Severity: 3/5)*
`check_stream_exists()` registers a Playwright request listener and removes it after — but if `page.goto()` throws, `remove_listener` never runs. Handlers stack across 10-meeting batch runs.

**Bottleneck 7 — No backfill strategy** *(Severity: 2/5)*
When the schema changes (e.g. adding `yes_voters`/`no_voters`), there's no documented process for re-processing old meetings. Old JSON files become second-class citizens silently.

---

## 🎯 Implementation Plan

### Phase 1 — Quick Wins (~10 min, commit after)

| Task | Detail | Effort |
|------|--------|--------|
| **1.1 Playwright try/finally** | Wrap `check_stream_exists()` body so `remove_listener` always runs, even on exception | 2 min |
| **1.2 Rate limiting** | Add `time.sleep(REQUEST_DELAY)` after each stream check — uses existing constant, zero new code | 2 min |
| **1.3 `--max N` flag** | Add optional `--max` arg to `parse_args()`, default 10. Exposes the buried `MAX_QUEUE = 10` constant | 5 min |

---

### Phase 2 — Error Handling Overhaul (~40 min, commit between tasks)

**2.1 — Replace `sys.exit()` with typed exceptions**
Define `PipelineError(reason: str)`. Replace all ~6 `sys.exit(1)` calls inside pipeline steps with `raise PipelineError("stream not found for {date}")` etc. The `--auto` loop catches and logs the full reason string per date. This is the highest-value fix — one bad date currently kills diagnostic info for the entire batch.

**2.2 — Batch log file**
At start of `--auto`, open `/tmp/burlington/batch-{timestamp}.log`. Write each step result: date | status | reason | duration. Print the log path at end of run so it survives terminal close.

**2.3 — Failure summary table**
End of `--auto`: print a clean table — date | status | reason | duration. Replace the current flat list that gives no diagnostic info.

---

### Phase 3 — Discovery Hardening (~60 min)

**3.1 — Date parsing fallback**
If the calendar link text regex fails, fall back to loading the meeting detail page and scraping the date from the page header. Slower per-meeting but never silently drops a meeting from the queue. Current risk: any eSCRIBE format change silently empties the discovery queue.

**3.2 — Discovery dry-run output table**
`--discover` (without `--auto`) prints a structured table: date | title | stream | status (queued / already-processed / no-stream). Makes the queue auditable before committing to a batch run.

---

### Phase 4 — Data Layer (~45 min)

*Informed by Data Engineer review. Adapted for static JSON on GitHub Pages — no Spark, no warehouse needed at this scale. Focus is on auditability, schema contracts, and future-proofing the data as more cities are added.*

**4.1 — Audit fields on meeting JSON output**
Add to every `summarize_meeting.py` output:
```json
{
  "_meta": {
    "schema": 2,
    "ingested_at": "2026-03-20T02:14:00Z",
    "pipeline_version": "1.0.0",
    "source_url": "https://burlington.escribemeetings.com/Meeting.aspx?Id=...",
    "audio_duration_seconds": 7234,
    "whisper_model": "mlx-whisper"
  }
}
```
Zero cost, massive future value. Lets you answer "when was this processed?", "what version produced it?", "where's the source?".

**4.2 — Enrich `index.json` with metadata**
Current: `["2026-02-17", "2026-03-05"]`

Upgrade to:
```json
[
  { "date": "2026-03-05", "schema": 2, "title": "Regular Council", "ingested_at": "2026-03-20T02:14:00Z" },
  { "date": "2026-02-17", "schema": 2, "title": "Regular Council", "ingested_at": "2026-03-18T11:30:00Z" }
]
```
Frontend still works (check `typeof entry === "string"` for backward compat). Enables filtering by schema version for backfills.

**4.3 — Document the data contract**
Add `scripts/SCHEMA.md` — the single source of truth for what the pipeline produces and what the frontend expects. Covers both current schemas (v1 PDF, v2 Whisper), documents every field, notes which fields are optional. When a third schema is added, this file gets updated first.

**4.4 — Guard in `buildMeetingCard()`**
Check `_meta.schema` before render. Unknown/missing → render a labelled fallback card rather than a silently broken one. Handles v1, v2, and any future versions without silent failures.

**4.5 — Backfill strategy (documented, not built yet)**
Add a `--reprocess DATE` flag to `pipeline.py` that re-runs only the summarize step (skipping download + transcribe) on an existing VTT. Lets you upgrade old meetings to a new schema without re-downloading 2hr audio files. Only worth building once the voter name arrays are ready to add.

---

## 🛠 Execution Order

```
Phase 1 — Quick wins (commit as one)
  └─ 1.1  Playwright try/finally          2 min
  └─ 1.2  Rate limiting                   2 min
  └─ 1.3  --max N flag                    5 min

Phase 2 — Error handling (commit between each)
  └─ 2.1  PipelineError exception class  20 min  ← highest priority
  └─ 2.2  Batch log file                 10 min
  └─ 2.3  Failure summary table          10 min

Phase 3 — Discovery hardening
  └─ 3.1  Date parsing fallback          45 min
  └─ 3.2  Dry-run output table           15 min

Phase 4 — Data layer
  └─ 4.1  Audit fields on JSON output    15 min
  └─ 4.2  Enrich index.json             20 min
  └─ 4.3  SCHEMA.md data contract        10 min
  └─ 4.4  buildMeetingCard() guard       15 min
  └─ 4.5  --reprocess flag              (when voter arrays are ready)
```

---

## Priority Reference

| Priority | Task | Effort |
|----------|------|--------|
| 🔴 High | 1.1 Playwright try/finally | 2 min |
| 🔴 High | 2.1 PipelineError + better failure messages | 20 min |
| 🟡 Medium | 1.2 Rate limiting between stream checks | 2 min |
| 🟡 Medium | 4.1 Audit fields on JSON output | 15 min |
| 🟡 Medium | 4.2 Enrich index.json with metadata | 20 min |
| 🟡 Medium | 4.3 SCHEMA.md data contract | 10 min |
| 🟡 Medium | 4.4 buildMeetingCard() schema guard | 15 min |
| 🟢 Low | 1.3 `--max N` flag | 5 min |
| 🟢 Low | 2.2–2.3 Batch log + summary table | 20 min |
| 🔵 Later | 3.1 Date parsing fallback to detail page | 45 min |
| 🔵 Later | 3.2 Discovery dry-run table | 15 min |
| 🔵 Later | 4.5 `--reprocess` flag for backfills | when needed |

---

## On Scaling Beyond Burlington

*Data Engineer note: The current architecture (static JSON on GitHub Pages) is correct for this scale and team size. It's free, fast, and zero-ops. The upgrade path when you add more cities:*

- **Short term:** One `index.json` per city, same schema. `meetings/{city}/index.json`. Frontend filters by city.
- **Medium term:** A `meetings/manifest.json` aggregating all cities — lets the frontend show a cross-city feed without fetching N index files.
- **Long term (if response tracking or user accounts are ever added):** Supabase. The static JSON becomes the Bronze layer, Supabase becomes Silver/Gold. The pipeline writes to both. Don't build this until there's a clear reason to.
