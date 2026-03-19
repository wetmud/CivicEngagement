#!/usr/bin/env python3
"""
Burlington council meeting summarizer.
Takes a Whisper transcript (.txt) and produces a structured JSON summary via Claude.

Usage:
  python3 summarize_meeting.py <transcript.txt> <meeting_date YYYY-MM-DD>
"""

import sys
import json
import os
import anthropic

CHUNK_CHARS = 80000  # ~20k tokens per chunk, safe for Haiku context
CLAUDE_MODEL = "claude-haiku-4-5-20251001"

CHUNK_PROMPT = """You are summarizing a chunk of Burlington City Council meeting transcript.
Extract key information from this portion. Be concise and factual.

For each chunk, identify:
- Main topics discussed
- Any motions moved, votes taken, or decisions made (with councillor names if mentioned)
- Any notable delegations or public speakers and what they said
- Any bylaws passed or rejected

Transcript chunk:
{chunk}

Respond as JSON:
{{
  "topics": ["topic1", "topic2"],
  "motions": [{{"description": "...", "result": "carried/defeated/tabled", "vote": "X-Y or unanimous"}}],
  "delegations": [{{"speaker": "name or 'public'", "topic": "...", "summary": "..."}}],
  "bylaws": [{{"number": "XX-XXXX", "title": "...", "result": "passed/defeated"}}],
  "notes": "any other notable points"
}}"""

FINAL_PROMPT = """You are writing a public summary of a Burlington City Council meeting for the Civic Engagement app (civicengagement.ca).
Citizens use this to quickly understand what their council discussed and decided.

Meeting date: {date}
Municipality: Burlington, Ontario

Here are summaries from each section of the meeting:
{chunks_json}

Write a structured summary. Be clear, factual, and accessible to regular citizens.

Respond as JSON:
{{
  "date": "{date}",
  "municipality": "Burlington",
  "tldr": "2-3 sentence plain-language summary of the most important things that happened",
  "topics": ["list of main agenda topics discussed"],
  "decisions": [
    {{"item": "what was decided", "result": "what council decided", "vote": "X-Y or unanimous if known"}}
  ],
  "delegations": [
    {{"speaker": "name or description", "topic": "what they spoke about", "summary": "1-2 sentences"}}
  ],
  "bylaws": [
    {{"number": "bylaw number if known", "title": "bylaw title", "result": "passed/defeated"}}
  ],
  "next_meeting": "date if mentioned, else null"
}}"""


def chunk_transcript(text, chunk_size=CHUNK_CHARS):
    chunks = []
    while len(text) > chunk_size:
        # Split at newline near chunk boundary
        split_at = text.rfind('\n', 0, chunk_size)
        if split_at == -1:
            split_at = chunk_size
        chunks.append(text[:split_at])
        text = text[split_at:].lstrip()
    if text.strip():
        chunks.append(text)
    return chunks


def summarize_chunks(client, chunks):
    results = []
    for i, chunk in enumerate(chunks):
        print(f"  Summarizing chunk {i+1}/{len(chunks)} ({len(chunk)} chars)...")
        msg = client.messages.create(
            model=CLAUDE_MODEL,
            max_tokens=1024,
            messages=[{"role": "user", "content": CHUNK_PROMPT.format(chunk=chunk)}]
        )
        text = msg.content[0].text.strip()
        # Strip markdown code fences if present
        if text.startswith("```"):
            text = text.split("```")[1]
            if text.startswith("json"):
                text = text[4:]
        try:
            results.append(json.loads(text))
        except json.JSONDecodeError:
            print(f"  Warning: chunk {i+1} response wasn't valid JSON, storing raw")
            results.append({"raw": text})
    return results


def build_final_summary(client, chunk_summaries, date):
    print("  Building final summary...")
    msg = client.messages.create(
        model=CLAUDE_MODEL,
        max_tokens=2048,
        messages=[{"role": "user", "content": FINAL_PROMPT.format(
            date=date,
            chunks_json=json.dumps(chunk_summaries, indent=2)
        )}]
    )
    text = msg.content[0].text.strip()
    if text.startswith("```"):
        text = text.split("```")[1]
        if text.startswith("json"):
            text = text[4:]
    return json.loads(text)


def main():
    if len(sys.argv) < 3:
        print("Usage: summarize_meeting.py <transcript.txt> <YYYY-MM-DD>")
        sys.exit(1)

    transcript_path = sys.argv[1]
    date = sys.argv[2]

    api_key = os.environ.get("ANTHROPIC_API_KEY")
    if not api_key:
        print("Error: ANTHROPIC_API_KEY not set")
        sys.exit(1)

    print(f"Loading transcript: {transcript_path}")
    with open(transcript_path, "r") as f:
        transcript = f.read()
    print(f"  {len(transcript)} chars, splitting into chunks...")

    chunks = chunk_transcript(transcript)
    print(f"  {len(chunks)} chunks")

    client = anthropic.Anthropic(api_key=api_key)

    print("Summarizing chunks...")
    chunk_summaries = summarize_chunks(client, chunks)

    print("Building final summary...")
    summary = build_final_summary(client, chunk_summaries, date)

    out_path = f"meetings/burlington/{date}.json"
    os.makedirs("meetings/burlington", exist_ok=True)
    with open(out_path, "w") as f:
        json.dump(summary, f, indent=2)
    print(f"\nDone! Written to {out_path}")
    print("\nTLDR:", summary.get("tldr", "N/A"))


if __name__ == "__main__":
    main()
