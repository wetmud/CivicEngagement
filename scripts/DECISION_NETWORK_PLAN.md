# Decision Network — Build Plan

> **Status:** New idea, not started. Proof-of-concept phase.
> **Context:** Extension of the Burlington meeting pipeline into a structured, queryable network of civic decisions.

> **Vibe:** The Pepe Silvia wall from It's Always Sunny. Charlie connects every piece of mail in the office into a grand unified theory — turns out he's right, there's just a lot of it. That's this. Documents, decisions, people, contracts, places — all connected, all real, just invisible until someone maps it. Except instead of hallucinating a shadow man, Jason is talking to his computer at 2am.

![pepe silvia](../../charlie.jpg)

---

## The Core Shift

Right now the pipeline produces meeting summaries — human-readable TLDRs and topic lists.

The upgrade: extract **structured decision objects** from every meeting, then link them into a network.

Instead of:
> "Council discussed a zoning amendment on Main St."

You get:
```json
{
  "id": "decision-2026-03-04-003",
  "type": "zoning_change",
  "status": "approved",
  "summary": "Zoning amendment approved for 123 Main St — residential to mixed-use",
  "meeting_id": "burlington-2026-03-04",
  "proposed_by": "Councillor Singh",
  "votes": { "yes": 5, "no": 2, "absent": 1 },
  "location": { "address": "123 Main St", "ward": "Ward 3" },
  "bylaws": ["2026-045"],
  "related_documents": [],
  "speakers": ["Singh", "Sharman", "Nisan"],
  "tags": ["zoning", "development", "ward3"]
}
```

Now it's queryable, linkable, and composable into a graph.

---

## The Network Model

Nodes:
- `Meeting` — date, type (council/committee), agenda
- `Decision` — vote, outcome, type, location
- `Person` — councillor, staff, delegate
- `Place` — address, ward, neighbourhood
- `Organization` — developer, vendor, community group
- `Document` — bylaw, contract, report
- `Contract` — vendor, value, department, linked decision

Edges:
- `Meeting → CONTAINS → Decision`
- `Person → VOTED_ON → Decision`
- `Decision → IMPACTS → Place`
- `Decision → PRODUCED → Document`
- `Contract → AWARDED_TO → Organization`
- `Contract → LINKED_TO → Decision`
- `Person → SPOKE_AT → Meeting`

The value emerges from the links — patterns across meetings that are invisible in individual summaries.

---

## Pipeline (Full Build)

### Step 0 — Archive scrape
- Hit eSCRIBE with full date range (estimate: 2018–present, ~200+ meetings)
- Collect every meeting UUID + date + type + video URL
- Save as `archive_queue.json` — ordered newest-first
- Filter: skip meetings with no video or no agenda

### Step 1 — Download + transcribe
- Same yt-dlp / HLS download as current pipeline
- Strip silent pre-roll (44s fix already in place)
- Force `--language en` to prevent Welsh hallucination
- mlx_whisper → raw transcript

### Step 2 — AI structuring (upgrade from current)
Current `summarize_meeting.py` produces: TLDR, topics, decisions (text), delegations, bylaws.

Upgrade Claude prompt to also extract:
- `decisions[]` as structured objects (see schema above)
- `votes{}` per decision where available
- `entities[]` — people, orgs, addresses mentioned
- `speakers[]` — normalized names (see entity resolution below)

### Step 3 — Entity resolution
The hard part. "Councillor Smith", "J. Smith", "John A. Smith" = same person.

Approach:
- Maintain a `entities/people.json` — canonical name → aliases
- Maintain `entities/orgs.json` — canonical org → aliases
- Run a normalization pass after extraction using these lookup files
- Flag unresolved entities for manual review
- Build the lookup files incrementally as archive is processed

### Step 4 — Storage
For the proof of concept: flat JSON files (same pattern as current)
```
meetings/burlington/{date}.json        — full meeting with decisions[]
decisions/burlington/{decision-id}.json — individual decision objects
entities/people.json                   — canonical people lookup
entities/orgs.json                     — canonical org lookup
index/decisions.json                   — flat list for querying
```

Future: Postgres + graph layer (Neo4j or pg_graph) when scale demands it.

### Step 5 — API layer (future)
Clean REST endpoints over the structured data:
- `GET /meetings?city=burlington&date=2026-03-04`
- `GET /decisions?city=burlington&type=zoning`
- `GET /places/{address}` — all decisions that impacted this address
- `GET /representatives/{id}` — voting patterns, decision involvement
- `GET /contracts?vendor=XYZ` — money flows linked to decisions

---

## Compute Reality Check

mlx_whisper runs at ~5x realtime on M1 Neural Engine.
- Short meeting (45min committee) → ~9min to transcribe
- Full council meeting (5hrs) → ~1hr to transcribe
- 200 meetings → potentially 100–200hrs of M1 time

**Strategy:**
- Process in nightly chunks (5–10 meetings/night background job)
- Prioritize recent first (last 2 years most useful)
- Filter by duration — skip anything under 20min (procedural only)
- Track progress in `archive_queue.json` with status field

---

## Proof-of-Concept First

Before automating anything:

1. Pick one archived meeting (ideally one with a known zoning vote)
2. Run the upgraded extraction prompt manually
3. Verify the JSON schema has what the network needs
4. Check entity names are consistent enough to link
5. Confirm decisions have enough structure to be queryable

**If the schema is wrong before automation, 200 files end up in the wrong format.**

Schema sign-off checklist:
- [ ] `decisions[]` are objects not strings
- [ ] `votes{}` are captured where available
- [ ] `location` field present on zoning/place-related decisions
- [ ] `proposed_by` normalized to canonical name
- [ ] `bylaws[]` linked to decision (not just listed at meeting level)
- [ ] `speakers[]` per decision (not just per meeting)

---

## How This Connects to Civic Engagement (Current App)

| Current feature | What it becomes |
|---|---|
| Address search | `GET /places/{address}` — decisions that touched your neighbourhood |
| Leaders/reps tab | Rep profile with voting history + decision graph |
| Budget tab (commented out) | Contracts + money flows linked to decisions |
| Meeting summaries | Entry point to queryable decision network |
| Email drafting | Context-aware — draft about *this specific decision* |

Same address-first UX. Massively more depth underneath.

---

## Open North Relationship

OpenNorth's Represent API gives us:
- Ward boundaries
- Rep contact info + mapping

We use them as an **input layer**, not a competitor. We build meaning, relationships, and timelines on top of what they provide.

---

## What Makes This Defensible

- Dataset is unique — no one else has structured Burlington decisions going back to 2018
- Structure is hard to replicate — entity resolution and linking takes time
- Historical archive compounds — gets more valuable the longer it runs
- Address-based personalization is the hook — "what's happening near me" is a universal question

---

## Notes

- This is a separate project from the current Civic Engagement scraper — don't muddy the existing pipeline until the POC validates the schema
- Burlington is the lab. Get it right here before touching another city.
- The "Request my city" button in the app is the demand signal for expansion priority
- MiroFish (saved in memory) could be relevant here — feeding decision network data as seed material for civic scenario simulation
