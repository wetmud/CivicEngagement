#!/usr/bin/env python3
"""
Burlington Council Meeting Pipeline
------------------------------------
Full pipeline: stream discovery → download → transcribe → summarize → update index.

Usage:
  python3 scripts/pipeline.py <YYYY-MM-DD> [options]

Options:
  --skip-download     Reuse existing audio in output dir (skip yt-dlp)
  --skip-transcribe   Reuse existing .vtt in output dir (skip mlx_whisper)
  --output-dir PATH   Temp file directory (default: /tmp/burlington/{date}/)

Requirements:
  pip3 install anthropic playwright mlx-whisper
  python3 -m playwright install chromium
  brew install ffmpeg yt-dlp

See scripts/CLAUDE.md for full setup and usage instructions.
"""

import argparse
import json
import os
import re
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path

# ── Constants ──────────────────────────────────────────────────────────────────

CLIENT_ID    = "burlington"
ESCRIBE_BASE = "https://burlingtonpublishing.escribemeetings.com"
ISILIVE_VOD  = f"https://cdn1.isilive.ca/vod/_definst_/mp4:{CLIENT_ID}"
MEETINGS_DIR = Path(__file__).parent.parent / "meetings" / "burlington"
INDEX_FILE   = MEETINGS_DIR / "index.json"

HEADERS = {
    "User-Agent": "CivicEngagement/1.0 (civicengagement.ca; open source civic tool)",
}

# ── Argument parsing ──────────────────────────────────────────────────────────

def parse_args():
    parser = argparse.ArgumentParser(
        description="Burlington council meeting pipeline",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=__doc__,
    )
    parser.add_argument("date", help="Meeting date in YYYY-MM-DD format")
    parser.add_argument("--skip-download",    action="store_true", help="Reuse existing audio")
    parser.add_argument("--skip-transcribe",  action="store_true", help="Reuse existing .vtt")
    parser.add_argument("--output-dir",       help="Temp file directory")
    return parser.parse_args()


def validate_date(date_str: str) -> str:
    try:
        datetime.strptime(date_str, "%Y-%m-%d")
        return date_str
    except ValueError:
        print(f"Error: date must be YYYY-MM-DD, got: {date_str}")
        sys.exit(1)


# ── Step 1: Discover stream URL via Playwright ────────────────────────────────

def discover_stream_url(date: str) -> str:
    """
    Navigates Burlington's eSCRIBE meeting page for the given date,
    intercepts the iSiLIVE lookup_stream network request, and returns
    the full HLS m3u8 URL.
    """
    try:
        from playwright.sync_api import sync_playwright
    except ImportError:
        print("Error: playwright not installed.")
        print("  pip3 install playwright && python3 -m playwright install chromium")
        sys.exit(1)

    year, month, _ = date.split("-")
    calendar_url = f"{ESCRIBE_BASE}/MeetingsCalendarView.aspx?StartDate={date}"
    meeting_url_re = re.compile(
        r"Meeting\.aspx\?Id=([0-9a-f\-]{36})",
        re.IGNORECASE,
    )

    print(f"Step 1: Discovering stream URL for {date}...")

    captured_stream_name = None

    def handle_request(request):
        nonlocal captured_stream_name
        if "lookup_stream" in request.url and "stream_name" in request.url:
            m = re.search(r"stream_name=([^&]+)", request.url)
            if m:
                captured_stream_name = m.group(1)
                print(f"  ✓ Captured stream_name: {captured_stream_name}")

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        page.set_extra_http_headers(HEADERS)

        # Find the meeting UUID for the given date from the calendar
        print(f"  Loading calendar: {calendar_url}")
        page.goto(calendar_url, wait_until="networkidle", timeout=30000)

        links = page.eval_on_selector_all(
            "a[href]",
            "els => els.map(e => ({ href: e.getAttribute('href'), text: e.innerText }))"
        )

        # eSCRIBE shows dates as "February 17, 2026" — convert YYYY-MM-DD for matching
        dt = datetime.strptime(date, "%Y-%m-%d")
        date_variants = {
            dt.strftime("%-d, %Y"),        # "17, 2026" — matches "February 17, 2026"
            dt.strftime("%B %-d, %Y"),     # "February 17, 2026"
            dt.strftime("%b %-d, %Y"),     # "Feb 17, 2026"
            date,                          # "2026-02-17" fallback
        }

        meeting_id = None
        for link in links:
            href = link.get("href") or ""
            text = (link.get("text") or "").strip()
            m = meeting_url_re.search(href)
            if m and any(v in text for v in date_variants):
                meeting_id = m.group(1)
                print(f"  ✓ Found meeting UUID: {meeting_id[:8]}... (matched in: {text[:60]})")
                break

        if not meeting_id:
            # Fallback: load each meeting page and check its content for the date
            uuids = [meeting_url_re.search(l.get("href","")).group(1)
                     for l in links if meeting_url_re.search(l.get("href",""))]
            print(f"  Date not found in calendar link text. Checking {min(len(uuids), 10)} meeting pages...")
            for uid in uuids[:10]:
                test_url = f"{ESCRIBE_BASE}/Meeting.aspx?Id={uid}&Agenda=Agenda&lang=English"
                page.goto(test_url, wait_until="networkidle", timeout=20000)
                content = page.inner_text("body")
                if any(v in content for v in date_variants):
                    meeting_id = uid
                    print(f"  ✓ Found meeting UUID via page content: {meeting_id[:8]}...")
                    break

        if not meeting_id:
            print(f"  ✗ No meeting found for {date} in Burlington's eSCRIBE calendar.")
            print("  Check: https://burlingtonpublishing.escribemeetings.com/MeetingsCalendarView.aspx")
            browser.close()
            sys.exit(1)

        # Load the meeting page — this triggers the iSiLIVE lookup_stream request
        meeting_page_url = f"{ESCRIBE_BASE}/Meeting.aspx?Id={meeting_id}&Agenda=Agenda&lang=English"
        print(f"  Loading meeting page to intercept stream request...")
        page.on("request", handle_request)
        page.goto(meeting_page_url, wait_until="networkidle", timeout=30000)

        # Give it a moment in case the video player loads async
        page.wait_for_timeout(3000)
        browser.close()

    if not captured_stream_name:
        print("  ✗ Stream URL not found — meeting may not have a video recording.")
        print("  The lookup_stream request was not intercepted. Try loading the meeting page manually:")
        print(f"  {meeting_page_url}")
        sys.exit(1)

    # URL-encode spaces if needed
    stream_name_encoded = captured_stream_name.replace(" ", "%20")
    hls_url = f"{ISILIVE_VOD}/{stream_name_encoded}/playlist.m3u8"
    print(f"  ✓ HLS URL: {hls_url}")
    return hls_url


# ── Step 2: Download audio ────────────────────────────────────────────────────

def download_audio(hls_url: str, output_dir: Path, skip: bool) -> Path:
    raw_path = output_dir / "raw.mp4"

    if skip and raw_path.exists():
        print(f"Step 2: Skipping download — using existing {raw_path}")
        return raw_path

    print(f"Step 2: Downloading audio...")
    print(f"  This may take a few minutes (~1.2GB for a 5-hour meeting).")

    cmd = [
        "yt-dlp",
        "-x", "--audio-format", "mp3", "--audio-quality", "5",
        hls_url,
        "-o", str(output_dir / "raw.%(ext)s"),
        "--no-playlist",
    ]

    result = subprocess.run(cmd, capture_output=False)
    if result.returncode != 0:
        print("  ✗ yt-dlp failed. Check the HLS URL is still valid.")
        sys.exit(1)

    # yt-dlp sometimes ignores -x on HLS and produces .mp4 — find whatever it made
    for ext in ("mp3", "mp4", "m4a"):
        candidate = output_dir / f"raw.{ext}"
        if candidate.exists():
            print(f"  ✓ Downloaded: {candidate} ({candidate.stat().st_size / 1e9:.2f} GB)")
            return candidate

    print("  ✗ Could not find downloaded file. Check yt-dlp output above.")
    sys.exit(1)


# ── Step 3: Detect and strip pre-roll silence ─────────────────────────────────

def trim_silence(audio_path: Path, output_dir: Path) -> Path:
    """
    Uses ffmpeg silencedetect to find where speech actually starts.
    Trims silence from the beginning to prevent Whisper's Welsh hallucination bug.
    Always passes --language en to whisper, but trimming makes detection more reliable.
    """
    trimmed_path = output_dir / "trimmed.mp3"

    if trimmed_path.exists():
        print(f"Step 3: Skipping silence trim — using existing {trimmed_path}")
        return trimmed_path

    print("Step 3: Detecting pre-roll silence...")

    result = subprocess.run(
        ["ffmpeg", "-i", str(audio_path),
         "-af", "silencedetect=noise=-40dB:d=1",
         "-vn", "-f", "null", "-"],
        capture_output=True, text=True
    )

    # Parse silence_end (first time non-silence starts)
    silence_end = 0.0
    for line in result.stderr.splitlines():
        m = re.search(r"silence_end: ([\d.]+)", line)
        if m:
            silence_end = float(m.group(1))
            break

    if silence_end > 5:
        print(f"  Found {silence_end:.1f}s of pre-roll silence — trimming...")
        subprocess.run([
            "ffmpeg", "-ss", str(silence_end),
            "-i", str(audio_path),
            "-vn", str(trimmed_path),
            "-y",
        ], check=True, capture_output=True)
        print(f"  ✓ Trimmed audio saved to {trimmed_path}")
    else:
        print(f"  No significant pre-roll silence ({silence_end:.1f}s) — copying as-is...")
        subprocess.run(["ffmpeg", "-i", str(audio_path), "-vn", str(trimmed_path), "-y"],
                       check=True, capture_output=True)

    return trimmed_path


# ── Step 4: Transcribe with mlx_whisper ──────────────────────────────────────

def transcribe(audio_path: Path, output_dir: Path, skip: bool) -> Path:
    vtt_path = output_dir / "trimmed.vtt"

    if skip and vtt_path.exists():
        print(f"Step 4: Skipping transcription — using existing {vtt_path}")
        return vtt_path

    print("Step 4: Transcribing with mlx_whisper...")
    print("  This takes ~1-2 hours on M1. Progress log will appear below.")
    print("  (Whisper only writes output when fully done — no mid-run updates)")

    try:
        import mlx_whisper
    except ImportError:
        print("Error: mlx_whisper not installed.")
        print("  pip3 install mlx-whisper")
        sys.exit(1)

    # mlx_whisper.transcribe returns a dict with 'segments'
    # We call it directly rather than via subprocess to stay in-process
    print(f"  Model: mlx-community/whisper-medium-mlx")
    result = mlx_whisper.transcribe(
        str(audio_path),
        path_or_hf_repo="mlx-community/whisper-medium-mlx",
        language="en",
        word_timestamps=False,
    )

    # Write .vtt manually from segments
    segments = result.get("segments", [])
    print(f"  ✓ Transcribed {len(segments)} segments")

    def secs_to_vtt(secs: float) -> str:
        h = int(secs // 3600)
        m = int((secs % 3600) // 60)
        s = secs % 60
        return f"{h:02d}:{m:02d}:{s:06.3f}".replace(".", ",")

    vtt_lines = ["WEBVTT", ""]
    for i, seg in enumerate(segments):
        start = secs_to_vtt(seg["start"])
        end   = secs_to_vtt(seg["end"])
        text  = seg["text"].strip()
        vtt_lines += [f"{i+1}", f"{start} --> {end}", text, ""]

    vtt_path.write_text("\n".join(vtt_lines))

    # Also write plain .txt
    txt_path = output_dir / "trimmed.txt"
    txt_path.write_text("\n".join(seg["text"].strip() for seg in segments))

    print(f"  ✓ VTT written to {vtt_path}")
    return vtt_path


# ── Step 5: Summarize with Claude ─────────────────────────────────────────────

def summarize(vtt_path: Path, date: str, api_key: str):
    print("Step 5: Summarizing with Claude...")

    # Import summarize_meeting from same directory
    sys.path.insert(0, str(Path(__file__).parent))
    from summarize_meeting import parse_vtt, vtt_to_timed_text, total_duration_minutes, chunk_text, summarize_chunks, build_final_summary
    import anthropic

    raw = vtt_path.read_text()
    segments = parse_vtt(raw)
    duration = total_duration_minutes(segments)
    timed_text = vtt_to_timed_text(segments)

    print(f"  {len(segments)} segments, ~{duration} minutes total")
    chunks = chunk_text(timed_text)
    print(f"  {len(chunks)} chunks to summarize")

    client = anthropic.Anthropic(api_key=api_key)
    chunk_summaries = summarize_chunks(client, chunks)
    summary = build_final_summary(client, chunk_summaries, date, duration)

    MEETINGS_DIR.mkdir(parents=True, exist_ok=True)
    out_path = MEETINGS_DIR / f"{date}.json"
    out_path.write_text(json.dumps(summary, indent=2, ensure_ascii=False))
    print(f"  ✓ Summary written to {out_path}")
    return summary


# ── Step 6: Update index.json ─────────────────────────────────────────────────

def update_index(date: str):
    print("Step 6: Updating index.json...")
    existing = []
    if INDEX_FILE.exists():
        existing = json.loads(INDEX_FILE.read_text())
    if date not in existing:
        existing.insert(0, date)
    existing = sorted(set(existing), reverse=True)
    INDEX_FILE.write_text(json.dumps(existing, indent=2))
    print(f"  ✓ index.json updated ({len(existing)} meetings)")


# ── Main ──────────────────────────────────────────────────────────────────────

def main():
    args = parse_args()
    date = validate_date(args.date)

    output_dir = Path(args.output_dir) if args.output_dir else Path(f"/tmp/burlington/{date}")
    output_dir.mkdir(parents=True, exist_ok=True)

    api_key = os.environ.get("ANTHROPIC_API_KEY")
    if not api_key:
        print("Error: ANTHROPIC_API_KEY environment variable not set.")
        print("  export ANTHROPIC_API_KEY=your_key_here")
        sys.exit(1)

    print(f"\n{'='*60}")
    print(f"  Burlington Meeting Pipeline — {date}")
    print(f"  Temp dir: {output_dir}")
    print(f"{'='*60}\n")

    # Check if summary already exists
    summary_path = MEETINGS_DIR / f"{date}.json"
    if summary_path.exists():
        print(f"Note: {summary_path} already exists.")
        answer = input("Re-run and overwrite? [y/N] ").strip().lower()
        if answer != "y":
            print("Aborted.")
            sys.exit(0)

    # Step 1: Discover stream (skip if we're reusing audio or vtt)
    if args.skip_download and (output_dir / "raw.mp4").exists():
        hls_url = None
        raw_audio = output_dir / "raw.mp4"
        print("Step 1: Skipping stream discovery — reusing existing audio")
    elif args.skip_download and (output_dir / "raw.mp3").exists():
        hls_url = None
        raw_audio = output_dir / "raw.mp3"
        print("Step 1: Skipping stream discovery — reusing existing audio")
    elif args.skip_transcribe and (output_dir / "trimmed.vtt").exists():
        hls_url = None
        raw_audio = None
        print("Step 1: Skipping stream discovery — reusing existing VTT")
    else:
        hls_url = discover_stream_url(date)
        raw_audio = None

    # Step 2: Download
    if raw_audio is None and not (args.skip_transcribe and (output_dir / "trimmed.vtt").exists()):
        raw_audio = download_audio(hls_url, output_dir, skip=args.skip_download)

    # Step 3: Trim silence
    if not (args.skip_transcribe and (output_dir / "trimmed.vtt").exists()):
        trimmed_audio = trim_silence(raw_audio, output_dir)
    else:
        trimmed_audio = None
        print("Step 3: Skipping silence trim — reusing existing VTT")

    # Step 4: Transcribe
    vtt_path = transcribe(
        trimmed_audio or output_dir / "trimmed.mp3",
        output_dir,
        skip=args.skip_transcribe,
    )

    # Step 5: Summarize
    summary = summarize(vtt_path, date, api_key)

    # Step 6: Update index
    update_index(date)

    # Done
    print(f"\n{'='*60}")
    print(f"  Done! Meeting summary for {date} is ready.")
    print(f"{'='*60}")
    print(f"\nTLDR: {summary.get('tldr', 'N/A')}")
    print(f"\nTo publish:")
    print(f"  git add meetings/burlington/")
    print(f"  git commit -m \"Add {date} council meeting summary\"")
    print(f"  git push")
    print()


if __name__ == "__main__":
    main()
