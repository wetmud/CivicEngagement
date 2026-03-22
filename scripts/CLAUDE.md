# scripts/ — CLAUDE.md

Tools for downloading, transcribing, and summarizing Burlington city council meetings.

---

## Scripts Overview

| Script | Purpose |
|--------|---------|
| `pipeline.py` | Full pipeline: stream discovery → download → transcribe → summarize → update index |
| `summarize_meeting.py` | Takes a Whisper `.vtt` file → calls Claude → writes `meetings/burlington/{date}.json` |
| `scrape_burlington.py` | PDF-based scraper: fetches posted minutes from eSCRIBE → Claude summary (runs in CI via GitHub Actions) |

---

## How the Pipeline Works

```
pipeline.py
  └─ 1. Playwright → eSCRIBE calendar → intercept lookup_stream request → get HLS URL
  └─ 2. yt-dlp → download audio to /tmp/burlington/{date}/raw.mp4
  └─ 3. ffmpeg silencedetect → trim pre-roll silence → trimmed.mp3
  └─ 4. mlx_whisper → transcribe → .vtt / .txt / .srt / .json
  └─ 5. summarize_meeting.py → Claude Haiku → meetings/burlington/{date}.json
  └─ 6. Update meetings/burlington/index.json
```

Temp files live in `/tmp/burlington/{date}/`. They survive between runs so you can resume after a failure.

The final output is two files committed to the repo:
- `meetings/burlington/{date}.json` — structured meeting summary
- `meetings/burlington/index.json` — updated list of available summaries

---

## Running the Pipeline

### First-time setup

```bash
# Install Python dependencies
pip3 install anthropic playwright mlx-whisper

# Install Playwright's headless Chromium browser
python3 -m playwright install chromium

# Install system tools (if not already installed)
brew install ffmpeg yt-dlp

# Fix Python SSL certs (needed once on macOS for model download)
open "/Applications/Python 3.14/Install Certificates.command"

# Set your API key
export ANTHROPIC_API_KEY=your_key_here
```

### Run for a specific meeting

```bash
cd /Users/macintosh/Documents/GitHub/CivicConnect

# Full pipeline (takes ~1-2hrs — whisper is the slow part)
python3 scripts/pipeline.py 2026-03-19

# Resume after failure — skips steps whose output already exists
python3 scripts/pipeline.py 2026-03-19

# Skip download (reuse existing audio in /tmp)
python3 scripts/pipeline.py 2026-03-19 --skip-download

# Skip transcription (reuse existing .vtt in /tmp)
python3 scripts/pipeline.py 2026-03-19 --skip-transcribe

# Custom temp directory
python3 scripts/pipeline.py 2026-03-19 --output-dir ~/Desktop/meeting-work/
```

### After the pipeline finishes

```bash
# Review the summary
cat meetings/burlington/2026-03-19.json

# Commit and push
git add meetings/burlington/
git commit -m "Add 2026-03-19 council meeting summary"
git push
```

---

## Summarizer (standalone)

If you already have a `.vtt` file from a previous whisper run:

```bash
export ANTHROPIC_API_KEY=your_key_here
python3 scripts/summarize_meeting.py /path/to/transcript.vtt 2026-03-19
```

Falls back to `.txt` if `.vtt` isn't available — but time data will be estimated, not real.

---

## The Two JSON Schemas

Older summaries (scraped from PDFs by `scrape_burlington.py`) use:
```json
{ "items": [{ "title", "outcome", "vote", "estimated_minutes", "notes" }] }
```

Newer summaries (produced by `summarize_meeting.py` from Whisper transcripts) use:
```json
{ "decisions": [...], "delegations": [...], "bylaws": [...], "key_issues": {...} }
```

`buildMeetingCard()` in `index.html` handles both — checks for `decisions[]` first, falls back to `items[]`.

---

## The Welsh Hallucination Fix

**Always pass `--language en` to mlx_whisper.** Without it, Whisper auto-detects the language. If the recording has silence or background noise at the start (Burlington meetings have ~44 seconds of pre-roll silence), Whisper misidentifies it as Welsh/Breton/Maori and hallucinates thousands of lines of Celtic text.

`pipeline.py` handles this automatically: it detects silence with `ffmpeg silencedetect`, trims it, and passes `--language en` to whisper.

---

## Adding a New City

The current pipeline is hardcoded to Burlington (iSiLIVE + eSCRIBE). To add another city:

1. Check if they use eSCRIBE — search `{city}publishing.escribemeetings.com`
2. Check if their iSiLIVE streams are open: `cdn1.isilive.ca/vod/_definst_/mp4:{city}/`
3. Copy `pipeline.py`, replace the `CLIENT_ID` and `ESCRIBE_BASE` constants
4. Test with one meeting before building automation

Cities known to use eSCRIBE + iSiLIVE: Burlington, Oakville, Hamilton, Mississauga (verify before assuming streams are open).

---

## Temp File Layout

```
/tmp/burlington/{date}/
  raw.mp4          — downloaded HLS stream (yt-dlp output)
  trimmed.mp3      — silence-trimmed audio (ffmpeg output)
  trimmed.vtt      — Whisper captions with timestamps ← used by summarizer
  trimmed.txt      — Whisper plain text
  trimmed.srt      — Whisper subtitles
  trimmed.json     — Whisper raw segment data
```
