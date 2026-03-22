#!/usr/bin/env python3
"""
Burlington council meeting summarizer.
Takes a Whisper .vtt transcript and produces a structured JSON summary via Claude.
The .vtt format has real timestamps per segment — used to calculate actual time-on-topic.

Usage:
  python3 summarize_meeting.py <transcript.vtt> <meeting_date YYYY-MM-DD>

Falls back to plain .txt if a .vtt isn't available (time data will be estimated, not real).
"""

import sys
import json
import os
import re
import anthropic

CHUNK_CHARS = 80000  # ~20k tokens per chunk, safe for Haiku context
CLAUDE_MODEL = "claude-haiku-4-5-20251001"


# ── VTT parsing ───────────────────────────────────────────────────────────────

def parse_vtt(vtt_text: str) -> list[dict]:
    """Parse WebVTT into list of {start_sec, end_sec, text} segments."""
    segments = []
    blocks = re.split(r'\n{2,}', vtt_text.strip())
    time_re = re.compile(
        r'(\d{2}):(\d{2}):(\d{2})[.,](\d{3})\s*-->\s*(\d{2}):(\d{2}):(\d{2})[.,](\d{3})'
    )
    for block in blocks:
        lines = block.strip().splitlines()
        for i, line in enumerate(lines):
            m = time_re.match(line)
            if m:
                h1, m1, s1, ms1, h2, m2, s2, ms2 = map(int, m.groups())
                start = h1*3600 + m1*60 + s1 + ms1/1000
                end   = h2*3600 + m2*60 + s2 + ms2/1000
                text  = ' '.join(lines[i+1:]).strip()
                if text:
                    segments.append({'start_sec': start, 'end_sec': end, 'text': text})
                break
    return segments


def vtt_to_timed_text(segments: list[dict]) -> str:
    """Convert segments to a text format with timestamps Claude can reason about.
    Format: [HH:MM] text — one line per minute boundary crossed."""
    lines = []
    last_minute = -1
    for seg in segments:
        minute = int(seg['start_sec'] // 60)
        if minute != last_minute:
            h = minute // 60
            m = minute % 60
            lines.append(f'\n[{h:02d}:{m:02d}] {seg["text"]}')
            last_minute = minute
        else:
            lines.append(seg['text'])
    return ' '.join(lines)


def total_duration_minutes(segments: list[dict]) -> int:
    if not segments:
        return 0
    return int((segments[-1]['end_sec'] - segments[0]['start_sec']) / 60)


# ── Chunking ──────────────────────────────────────────────────────────────────

def chunk_text(text: str, chunk_size: int = CHUNK_CHARS) -> list[str]:
    chunks = []
    while len(text) > chunk_size:
        split_at = text.rfind('\n', 0, chunk_size)
        if split_at == -1:
            split_at = chunk_size
        chunks.append(text[:split_at])
        text = text[split_at:].lstrip()
    if text.strip():
        chunks.append(text)
    return chunks


# ── Claude prompts ────────────────────────────────────────────────────────────

CHUNK_PROMPT = """You are summarizing a chunk of a Burlington City Council meeting transcript.
Timestamps in [HH:MM] format mark each minute of the recording.

Extract:
- Topics discussed and the approximate time range they occurred [HH:MM]–[HH:MM]
- Motions, votes, and decisions — capture as structured objects (see schema below)
- Public delegations (speaker name, topic, brief summary)
- Bylaws passed or rejected

For each decision/motion, extract as much structure as possible:
- proposed_by: the councillor who moved the motion (first and last name, e.g. "Councillor Singh")
- seconded_by: councillor who seconded, if mentioned
- votes: {{"yes": N, "no": N, "absent": N}} — use null fields if not mentioned
- location: address or area if the decision is place-specific (zoning, development, infrastructure), else null
- tags: 1-3 topic tags from: zoning, development, budget, infrastructure, transit, parks,
        environment, housing, contracts, procedural, bylaws, community, other

Transcript chunk:
{chunk}

Respond as JSON:
{{
  "topics": [{{"name": "topic", "start": "HH:MM", "end": "HH:MM"}}],
  "motions": [{{
    "description": "what was decided",
    "result": "carried/defeated/deferred",
    "proposed_by": "Councillor Name or null",
    "seconded_by": "Councillor Name or null",
    "votes": {{"yes": null, "no": null, "absent": null}},
    "location": "address or area or null",
    "bylaws": ["bylaw numbers referenced, if any"],
    "tags": ["tag1", "tag2"]
  }}],
  "delegations": [{{"speaker": "name", "topic": "...", "summary": "..."}}],
  "bylaws": [{{"number": "XX-XXXX", "title": "...", "result": "passed/defeated"}}]
}}"""


FINAL_PROMPT = """You are writing a public summary of a Burlington City Council meeting for civicengagement.ca.
Citizens use this to understand what council discussed and decided without watching 5 hours of video.

Meeting date: {date}
Total duration: ~{duration} minutes

Section summaries (each has timestamps):
{chunks_json}

Produce a structured summary. Use the timestamps to calculate real time-on-topic.
productive_minutes = time on substantive decisions/debate.
procedural_minutes = roll call, recesses, procedural motions, reading of bylaws, etc.
They should sum to roughly {duration}.

For decisions, preserve all structured fields from the section summaries — do not flatten them to strings.
Merge duplicate motions (same item appearing in multiple chunks) into one decision object.

Respond as JSON (no markdown):
{{
  "date": "{date}",
  "municipality": "Burlington, Ontario",
  "meeting_type": "Regular Meeting of Council",
  "tldr": "2-3 sentence plain-language summary of the most important things that happened",
  "productive_minutes": <integer>,
  "procedural_minutes": <integer>,
  "topics": [{{"name": "topic name", "start": "HH:MM", "end": "HH:MM"}}],
  "decisions": [
    {{
      "item": "what was decided",
      "result": "Passed/Defeated/Deferred",
      "proposed_by": "Councillor Name or null",
      "seconded_by": "Councillor Name or null",
      "votes": {{"yes": null, "no": null, "absent": null}},
      "location": "address or area or null",
      "bylaws": ["bylaw numbers or empty list"],
      "tags": ["tag1", "tag2"]
    }}
  ],
  "delegations": [
    {{"speaker": "name", "topic": "what they spoke about", "summary": "1-2 sentences"}}
  ],
  "bylaws": [
    {{"number": "bylaw number", "title": "title", "result": "passed/defeated", "vote": "X-Y or null"}}
  ],
  "key_issues": {{
    "summary": "1-2 paragraphs on the most contentious or significant issues"
  }},
  "next_meeting": "YYYY-MM-DD if mentioned, else null"
}}"""


# ── Summarization ─────────────────────────────────────────────────────────────

def summarize_chunks(client, chunks: list[str]) -> list[dict]:
    results = []
    for i, chunk in enumerate(chunks):
        print(f'  Summarizing chunk {i+1}/{len(chunks)} ({len(chunk):,} chars)...')
        msg = client.messages.create(
            model=CLAUDE_MODEL,
            max_tokens=2048,
            messages=[{'role': 'user', 'content': CHUNK_PROMPT.format(chunk=chunk)}]
        )
        text = msg.content[0].text.strip()
        if text.startswith('```'):
            text = text.split('```')[1]
            if text.startswith('json'):
                text = text[4:]
        try:
            results.append(json.loads(text))
        except json.JSONDecodeError:
            print(f'  Warning: chunk {i+1} returned invalid JSON — storing raw')
            results.append({'raw': text})
    return results


def build_final_summary(client, chunk_summaries: list[dict], date: str, duration: int) -> dict:
    print('  Building final summary...')
    msg = client.messages.create(
        model=CLAUDE_MODEL,
        max_tokens=6000,
        messages=[{'role': 'user', 'content': FINAL_PROMPT.format(
            date=date,
            duration=duration,
            chunks_json=json.dumps(chunk_summaries, indent=2)
        )}]
    )
    text = msg.content[0].text.strip()
    if text.startswith('```'):
        text = text.split('```')[1]
        if text.startswith('json'):
            text = text[4:]
    return json.loads(text)


# ── Main ──────────────────────────────────────────────────────────────────────

def main():
    if len(sys.argv) < 3:
        print('Usage: summarize_meeting.py <transcript.vtt|.txt> <YYYY-MM-DD>')
        sys.exit(1)

    transcript_path = sys.argv[1]
    date = sys.argv[2]

    api_key = os.environ.get('ANTHROPIC_API_KEY')
    if not api_key:
        print('Error: ANTHROPIC_API_KEY not set')
        sys.exit(1)

    print(f'Loading transcript: {transcript_path}')
    with open(transcript_path, 'r') as f:
        raw = f.read()

    is_vtt = transcript_path.endswith('.vtt')
    if is_vtt:
        print('  Detected VTT format — parsing timestamps...')
        segments = parse_vtt(raw)
        duration = total_duration_minutes(segments)
        print(f'  {len(segments)} segments, ~{duration} minutes total')
        timed_text = vtt_to_timed_text(segments)
    else:
        print('  Plain text format — timestamps will be estimated by Claude')
        timed_text = raw
        duration = 0  # Claude will estimate

    print(f'  {len(timed_text):,} chars, splitting into chunks...')
    chunks = chunk_text(timed_text)
    print(f'  {len(chunks)} chunks')

    client = anthropic.Anthropic(api_key=api_key)

    print('Summarizing chunks...')
    chunk_summaries = summarize_chunks(client, chunks)

    print('Building final summary...')
    summary = build_final_summary(client, chunk_summaries, date, duration)

    out_path = f'meetings/burlington/{date}.json'
    os.makedirs('meetings/burlington', exist_ok=True)
    with open(out_path, 'w') as f:
        json.dump(summary, f, indent=2)

    print(f'\nDone! Written to {out_path}')
    print('TLDR:', summary.get('tldr', 'N/A'))
    print(f'Productive: {summary.get("productive_minutes")}m  Procedural: {summary.get("procedural_minutes")}m')


if __name__ == '__main__':
    main()
