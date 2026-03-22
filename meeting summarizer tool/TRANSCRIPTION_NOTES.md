# Burlington Council Meeting Transcription — How It Works

## What This Does

Downloads Burlington City Council meeting videos from the iSiLIVE streaming platform and transcribes them locally using Whisper (Apple Silicon optimized). The goal: feed AI-summarized meeting minutes into the Civic Engagement app so residents can actually understand what council discussed.

---

## How Burlington Streams Their Meetings

Burlington uses **eSCRIBE** (escribemeetings.com) to publish agendas and meeting pages. When you load a meeting page, it fires a network request to **iSiLIVE** (isilive.ca) — a Canadian municipal video streaming platform — to load the video player.

iSiLIVE serves open **HLS (m3u8) streams** with no authentication. The URL pattern is:

```
https://cdn1.isilive.ca/vod/_definst_/mp4:burlington/{stream_name}/playlist.m3u8
```

The `stream_name` is discovered by intercepting the network request eSCRIBE fires:
```
https://video.isilive.ca/eSCRIBE/lookup_stream?client_id=burlington&stream_name={filename}
```

Filename pattern: `iSiLIVE Encoder 763_Regular Meeting of Council_YYYY-MM-DD-HH-MM.mp4`

### eSCRIBE's Built-in Caption Infrastructure (Unused by Burlington)
eSCRIBE checks for captions and summaries per meeting at:
- `https://video.isilive.ca/.../meeting_id.vtt` — captions
- `https://video.isilive.ca/.../meeting_id.summary.txt` — summary

Both return 404 for Burlington — the hooks exist but Burlington doesn't populate them. **This is worth asking Burlington about directly** (see email template below).

---

## Tools Required

| Tool | Purpose | Install |
|------|---------|---------|
| `yt-dlp` | Download HLS video stream | `pip3 install yt-dlp` |
| `mlx-whisper` | Transcribe audio on Apple Silicon | `pip3 install mlx-whisper` |
| `ffmpeg` | Audio demuxing (Whisper dependency) | `brew install ffmpeg` |
| `playwright` | Intercept stream_name from eSCRIBE page | `pip3 install playwright` |

---

## One-Time Setup (Hurdles Encountered)

### 1. Python SSL Certificate Error
`openai-whisper` failed to download the model with:
```
URLError: certificate verify failed: self-signed certificate in certificate chain
```
**Fix:** Run the Python certificate installer:
```bash
open "/Applications/Python 3.14/Install Certificates.command"
```

### 2. ffmpeg Not Installed
Whisper requires ffmpeg for audio decoding but doesn't install it automatically.
**Fix:** `brew install ffmpeg`

### 3. CPU-Only Whisper = Too Slow
`openai-whisper` ran in FP32 on CPU only — estimated 10–20 hours for a 5-hour meeting.
**Fix:** Use `mlx-whisper` instead — runs on Apple Silicon Neural Engine via MLX framework.
```bash
pip3 install mlx-whisper
mlx_whisper audio.mp4 --model mlx-community/whisper-medium-mlx --output-dir ./out --output-format all
```
Estimated time on M1: **1–2 hours** for a 5-hour meeting.

### 4. mlx_whisper Shows No Progress
The log freezes at "Fetching 4 files: 100%" while transcribing. This is normal — it only writes output when completely done. Confirm it's running with:
```bash
ps aux | grep mlx_whisper | grep -v grep
```

### 5. Welsh Hallucination (Whisper Language Auto-Detection Bug)
First transcription run produced entirely Welsh output — thousands of lines of "Mae'r cyfle wedi'i ddod yn ystod y cyfle."

**Cause:** The recording has ~44 seconds of silence before the mayor speaks. Whisper's auto-detect misidentifies silence/background noise as Welsh (a known Whisper quirk — hallucinates Breton, Maori, or Welsh on silence).

**Diagnosis:**
```bash
ffmpeg -i recording.mp4 -af "silencedetect=noise=-40dB:d=1" -vn -f null - 2>&1 | grep silence
# silence_start: 0 / silence_end: 43.894771 → first 44 seconds are silent
```

**Fix:** Always pass `--language en` AND strip the pre-roll silence first:
```bash
ffmpeg -ss 44 -i 2026-02-17.mp4 -vn 2026-02-17-trimmed.mp3
mlx_whisper 2026-02-17-trimmed.mp3 --model mlx-community/whisper-medium-mlx --language en --output-dir ./out --output-format all
```

### 6. HF Hub Rate Limit Warning
```
Warning: You are sending unauthenticated requests to the HF Hub.
```
Harmless — model downloads fine without a token. Set `HF_TOKEN` env var for higher rate limits if needed.

---

## Test Run: February 17, 2026 Council Meeting

**Meeting page:** https://burlingtonpublishing.escribemeetings.com/Meeting.aspx?Id=f2f43022-2ed7-4a64-8828-7bf4e7fe3f2d

**Stream URL discovered:**
```
https://cdn1.isilive.ca/vod/_definst_/mp4:burlington/iSiLIVE%20Encoder%20763_Regular%20Meeting%20of%20Council_2026-02-17-08-54.mp4/playlist.m3u8
```

**Download command used:**
```bash
mkdir -p /tmp/burlington_test
yt-dlp -x --audio-format mp3 --audio-quality 5 \
  "https://cdn1.isilive.ca/vod/_definst_/mp4:burlington/iSiLIVE%20Encoder%20763_Regular%20Meeting%20of%20Council_2026-02-17-08-54.mp4/playlist.m3u8" \
  -o "/tmp/burlington_test/2026-02-17.%(ext)s"
```
Note: yt-dlp produced `.mp4` despite `-x` flag on HLS streams. Whisper handles `.mp4` fine.

**Stats:** 1547 HLS fragments, ~1.2GB, ~5 hours long.

**Transcription command:**
```bash
nohup mlx_whisper /tmp/burlington_test/2026-02-17.mp4 \
  --model mlx-community/whisper-medium-mlx \
  --output-dir /tmp/burlington_transcripts \
  --output-format all \
  > /tmp/whisper_progress.log 2>&1 &
```

**Output** (when complete): `.txt`, `.vtt`, `.srt`, `.tsv`, `.json` in `/tmp/burlington_transcripts/`

---

## Next Steps After Transcription

1. **Chunk the transcript** — split by time or token count for Claude API limits
2. **Summarize with Claude Haiku** — structured JSON: `{ tldr, topics[], votes[], decisions[], timestamp }`
3. **Save to `data/meetings.json`** — loaded by Meetings tab in the app
4. **Build `scrape_burlington.py`** — automate the full pipeline for all meetings

---

## Who to Contact at Burlington

The **City Clerk's Office** manages council records and accessibility. They are the right contact to ask about official captions/transcriptions.

**Email:** clerks@burlington.ca

**Draft:**
> Subject: Request for Council Meeting Captions or Transcriptions
>
> Hello,
>
> I'm a Burlington resident building an open-source civic engagement tool (civicengagement.ca) that helps citizens connect with their elected representatives. I'd like to add AI-summarized council meeting minutes so residents can quickly understand what was discussed.
>
> I noticed Burlington's eSCRIBE meeting portal has infrastructure for captions (.vtt) and summaries, but those files aren't currently populated for Burlington's meetings.
>
> Could you let me know:
> 1. Whether Burlington produces official transcriptions or captions for council meetings?
> 2. If so, whether they're available via a public feed or API?
> 3. If not, whether there are plans to offer them?
>
> Happy to share more about what I'm building if useful.
>
> Thank you,
> Jason Steltman — jason.steltman@gmail.com

