# Civic Engagement — Demo Guide

**Live site:** civicengagement.ca
**Target video length:** 2:30–3:00
**Format:** Screen recording (Playwright-driven) + voiceover recorded separately
**Audience:** Potential users, grant reviewers, journalists, Reddit/social

---

## What We're Showing

Most Canadians don't know who represents them at every level of government — let alone how to actually reach them. Civic Engagement solves that in one address search. The demo shows:

1. The full rep discovery flow (federal + provincial + municipal, one search)
2. The ward map — visual proof of where you live politically
3. Rep profiles — real bios, voting records, contact info
4. Email drafting — one click to write your rep
5. Leaders tab — Premier + PM always visible
6. The "coming soon" tabs — signals where the product is going

---

## The Script

### SECTION 1 — Cold Open (0:00–0:12)

**[Browser opens on civicengagement.ca. Hold on the homepage for 3 seconds. Let the marquee banner scroll. Don't do anything yet.]**

> VOICEOVER: "Most Canadians don't know who all their elected representatives are. Federal, provincial, municipal — it's a lot to keep track of. This is Civic Engagement."

---

### SECTION 2 — The Search (0:12–0:35)

**[Slowly click into the address search bar.]**
**[Type: `414 Locust Street, Burlington`]**
**[Pause 1 second after typing — let the autocomplete dropdown appear.]**
**[Click the first autocomplete result.]**
**[Pause 1 second. Then click the Search button.]**
**[Wait for results to load — ~2 seconds.]**

> VOICEOVER: "Type any Canadian address. We'll show you every elected official who represents that person — at every level of government."

---

### SECTION 3 — The Rep Results (0:35–1:05)

**[Results are now showing. Hold on the full list for 2 seconds before scrolling.]**
**[Scroll slowly down through the rep cards — federal MP at top, then provincial MPP, then city councillor, then mayor.]**
**[Pause briefly on each card so viewers can read the name and role.]**

> VOICEOVER: "Federal MP. Provincial MPP. City councillor. Mayor. All in one place, all sourced live from OpenNorth's Represent API — no manual data entry, no outdated spreadsheets."

**[After scrolling through ~4–5 cards, scroll back up to the ward map.]**
**[Pause on the map for 3 seconds — let it breathe.]**

> VOICEOVER: "The map shows your exact ward boundary — so you always know whose job it is to represent your neighbourhood."

---

### SECTION 4 — Rep Profile (1:05–1:35)

**[Click on the city councillor card — whichever one shows for that address.]**
**[The profile modal opens. Hold for 2 seconds.]**
**[Slowly scroll down inside the modal — show the Wikipedia bio, office info, social links.]**

> VOICEOVER: "Click any rep to see their full profile — bio pulled from Wikipedia, office details, how to reach them."

**[If it's a federal MP: scroll to the voting record section. Hold for 3 seconds.]**

> VOICEOVER (if MP): "For federal MPs, we pull their real voting record — so you can see exactly how they've voted on the issues that matter to you before you write."

**[Click the X to close the modal.]**

---

### SECTION 5 — Write an Email (1:35–1:55)

**[Click the "✉ Write Email" button on any rep card.]**
**[The email modal opens. Hold for 2 seconds — show the compose fields.]**
**[Don't type anything — just let it sit so viewers read the UI.]**

> VOICEOVER: "When you're ready to reach out, one click opens a pre-addressed email template. Fill in your message, send. That's it."

**[Click X to close the modal.]**

---

### SECTION 6 — Leaders Tab (1:55–2:15)

**[Click the "Leaders" tab.]**
**[Two cards appear — Premier and Prime Minister. Hold for 3 seconds.]**
**[Slowly scroll if needed to show both cards fully.]**

> VOICEOVER: "The Leaders tab always shows your Premier and the Prime Minister — with direct contact info. Because sometimes the issue is bigger than your local councillor."

---

### SECTION 7 — What's Coming (2:15–2:35)

**[Click the "Council Meetings" tab.]**
**[The coming-soon panel shows. Hold for 2 seconds.]**

> VOICEOVER: "We're building AI-summarized council meeting minutes — so you can see what your council actually decided without watching five hours of video."

**[Click the "City Budget" tab.]**
**[Hold for 2 seconds.]**

> VOICEOVER: "And a city budget explorer — so when you want to know where your tax dollars go, or who to call about it, you don't have to dig."

---

### SECTION 8 — Close (2:35–2:55)

**[Click back to "Local & Provincial" tab. Scroll up to the top of results — show the full rep list one more time.]**
**[Hold for 3 seconds.]**

> VOICEOVER: "Civic Engagement is free, open source, and built for every Canadian. civicengagement.ca"

**[Hold on screen for 3 more seconds. End recording.]**

---

## Playwright Automation Notes

The Playwright script drives all the clicking. Jason records OBS capturing the browser window, then lays voiceover on top in editing.

**Address used in demo:** `414 Locust Street, Burlington, ON`
(Burlington City Hall — shows federal + provincial + municipal reps cleanly)

**Browser window size:** 1280×800 (fits most screens, clean for social)

**Pacing:** All pauses should feel slightly longer than comfortable — video plays faster than it feels when recording.

---

## Goals

- **Primary:** Get the "one search, every rep" moment to land emotionally
- **Secondary:** Show the product is real and working, not a mockup
- **Grant use:** Demonstrates the full feature set for NLnet, Mozilla MOSS applications
- **Social use:** Cut into 3 clips: (1) the search moment, (2) the profile/email flow, (3) the leaders tab

---

## Clip Cut Points (for social)

| Clip | Seconds | Caption idea |
|------|---------|--------------|
| The search moment | 0:12–0:35 | "Type your address. Know your reps." |
| Profile + email | 1:05–1:55 | "Your MP's voting record + a direct line to their inbox." |
| Leaders tab | 1:55–2:15 | "Your Premier and PM, one click away." |

---

## Process & Architecture (for grant applications)

**How it works:**
- Address → Geoapify geocoding → lat/lon
- lat/lon → OpenNorth Represent API → all Canadian reps at that location
- Ward boundary → Leaflet map with GeoJSON overlay
- Rep profile → Wikipedia REST API (bio) + OpenParliament.ca (voting record)
- Email → mailto compose, pre-addressed
- Leaders data → hand-curated `data/leaders.json`, updated when elections happen

**Stack:** Single-file vanilla HTML/CSS/JS. No framework, no build step. Deploy = git push to GitHub Pages. Served via Cloudflare for HTTPS + edge caching.

**API proxy:** Cloudflare Worker at `civicconnect-proxy.jason-steltman.workers.dev` — keeps Geoapify key server-side, handles CORS.

**Cost to run:** ~$40/year (Cloudflare, GoDaddy domain). No backend, no database, no server costs.

**What makes it different:** Every other "find your rep" tool is either US-only, municipal-only, or requires you to know which level of government to search. This is the only tool that gives you all three levels from one address, with email drafting and voting records, for free.
