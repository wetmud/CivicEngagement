# Meeting Transcription — Roadmap

Strategy: build publicly, let the data compound. Don't pitch cities yet.
The embarrassment gap between what citizens have and what the city offers
creates inbound interest on its own timeline. Municipal procurement is 12–18
months minimum — the play is to be already-proven when they come looking.

---

## Phase 1 — Prove It Works (now)

- [x] Build `pipeline.py` — full stream discovery → download → transcribe → summarize
- [x] Build `summarize_meeting.py` with real VTT timestamps for time-on-topic data
- [x] Publish first Whisper-transcribed meeting (Feb 17 2026)
- [ ] Install deps and run pipeline on 2–3 more Burlington meetings
- [ ] Re-run Feb 17 with real `.vtt` timestamps (not estimated)
- [ ] Push live to civicengagement.ca — verify meetings tab works on GitHub Pages
- [ ] Share on Reddit (r/ontario, r/burlington, r/civictech) and X

---

## Phase 2 — Add Coverage (1–2 months)

- [ ] Automate: GitHub Action that detects new Burlington council meeting dates and
      runs the pipeline
- [ ] Backfill: run pipeline on ~6 months of past meetings (iSiLIVE VOD archive)
- [ ] Improve summarizer: speaker diarization would be useful (identify councillors
      by name more reliably — could use the agenda PDF to cross-reference)
- [ ] Add second city: Oakville or Hamilton (same eSCRIBE + iSiLIVE stack)
- [ ] Meeting diff view: what changed vs the previous meeting on ongoing issues

---

## Phase 3 — Make It a Product (3–6 months)

- [ ] City selection UI — user picks their municipality, sees their meetings
- [ ] Meeting search — full-text search across all transcripts
- [ ] Email/SMS alerts — notify subscribers when a new summary drops
- [ ] Issue tracking — automatically link recurring topics across meetings
      (e.g. "bike lanes on Appleby" appears in 4 meetings → show the arc)
- [ ] Public API — `GET /api/burlington/meetings` — let journalists/researchers use the data

---

## Phase 4 — Sell the Service (6–18 months, inbound only)

The value prop to cities isn't "meeting transcription" — it's that we've already
built a public record of their meetings that citizens are using and they don't control.

Options when cities come knocking:
- **White-label SaaS**: city pays for their own branded portal + private API
- **Compliance add-on**: auto-generate legally-required accessible minutes from transcript
- **Staff-facing tools**: search your own meeting history, surface relevant past decisions
- **Integration**: push summaries into their existing eSCRIBE / OpenCities CMS

Don't cold-pitch. Build in public, get press, let procurement find you.

---

## Data Moat

Each transcribed meeting is permanently searchable. After 50 meetings:
- Burlington has ~2 years of indexed council history
- A new competitor has to process 50 hours of audio to catch up
- The data compounds: issue tracking, voting patterns, time-on-topic trends
  all become richer with each new meeting

This is the real asset. The transcription pipeline is just the shovel.
