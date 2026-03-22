# Civil — AI Civic Assistant Design Spec
**Date:** 2026-03-22
**Project:** CivicConnect (civicengagement.ca)
**Status:** Approved for implementation

---

## Overview

Civil is a floating chat assistant embedded in `index.html`. It helps users identify who to contact about a civic issue, find the right city department if applicable, and draft a message. It is named Civil, has a distinct personality, and can later be ported to Discord or other platforms.

---

## Personality

**Archetype:** The Knowledgeable Neighbour
**Voice:** Warm, plain-spoken, community-oriented. Knows how government works but never makes users feel dumb for not knowing it. Frames users as capable civic actors, not petitioners.
**Whimsy:** Small celebratory moments when users take action. Light, never sarcastic. Nothing that undercuts credibility.
**Avatar:** ⚖️
**Psychological grounding:** Reduces civic participation anxiety by normalizing the ask and providing concrete next steps. Always frames the user as having power.

---

## Scope (Phase 1)

- Route user's issue to the right contact: elected rep (municipal/provincial/federal) OR city department
- Draft a message to that contact in Civil's voice
- Multi-turn conversation — Civil remembers what was said earlier in the session

**Out of scope (Phase 2):**
- General civic Q&A ("what does a city councillor do?")
- Meeting summary lookup
- Voting record discussion

---

## Architecture

All code lives in `index.html`. No new files, no build step.

### New DOM elements
```
#civil-bubble     — fixed ⚖️ button, bottom-right
#civil-tooltip    — "Need help? Ask Civil ✦" nudge, fades after first open
#civil-panel      — chat window, hidden until opened
  #civil-messages — scrollable message list
  #civil-input    — text input
  #civil-send     — send button
```

### New JS globals (add near top of script block)
```javascript
let civilHistory = [];        // conversation array, cleared on page reload
let civilOpened = false;      // tracks whether opening message has been sent
let civilDepts = null;        // loaded departments JSON for user's city, or null
let loadedReps = [];          // populated inside renderRepList() after Represent API fetch
```

`loadedReps` must be assigned inside the existing `renderRepList()` function:
```javascript
// Add at top of renderRepList(reps):
loadedReps = reps;
```

### New JS functions
```
civilContext()         — builds session snapshot string from loadedReps, selectedCity, selectedProvince, ward
civilOpen()            — opens panel, fetches departments JSON if not loaded, sends opening message if first open
civilClose()           — hides panel
civilSend()            — appends user message to civilHistory[], calls Pollinations, renders response
civilRender(msg, role) — renders a message bubble to #civil-messages
civilLoadDepts()       — fetches data/departments/{citySlug}.json, sets civilDepts; silent fail if 404
civilPrefillEmail(rep) — sets currentRepForProfile or equivalent and opens #email-backdrop pre-filled
```

### Context rebuild
`civilContext()` is called on every `civilSend()` invocation, not just on open. This ensures that if the user searches a new address mid-conversation, subsequent messages reflect the updated reps and city. The system prompt (first message in `civilHistory`) is static per session — only the context injected into each user-turn prompt updates.

---

## API

**Provider:** Pollinations (`https://text.pollinations.ai/openai`)
**Pattern:** OpenAI-compatible chat completions, multi-turn
**Model:** `openai` (Pollinations default)
**Key required:** None
**Fallback:** If the fetch fails or returns a non-200, Civil displays: "I'm having trouble connecting right now — here's your rep's direct contact info" and surfaces name + email/phone from `loadedReps[0]` (most local rep).

---

## System Prompt

Injected once as the first entry in `civilHistory` (role: `system`) when Civil is first opened. Never shown to the user. Session context is injected separately into each user-turn message as a prefix.

```
You are Civil, a friendly civic guide for Canadians built into civicengagement.ca.
You're like a knowledgeable neighbour — warm, plain-spoken, never condescending.
You know how government works but you never make people feel dumb for not knowing it.

Your job:
1. Help users figure out who to contact about their issue (elected rep or city department)
2. Find the right department if it's a city services issue
3. Help them draft a short, effective message

Rules:
- Keep responses short (2-4 sentences max unless drafting a message)
- Never use government jargon without explaining it
- Frame the user as capable — they have a right to be heard
- Celebrate when they take action ("That's it — your voice is on record ✦")
- Never make up contact information — only use what's in the session context
- If you don't know something, say so plainly
```

### Per-turn context prefix

Each user message is prepended (invisibly) with current session state before being added to `civilHistory`:

```
[Session: City={city}, Province={province}, Ward={ward or "unknown"},
Reps=[{name} ({level}, {party}), {name} ({level}, {party}), ...],
Departments loaded={true/false}]

User message: {actual user text}
```

Rep list serialization example:
```
Reps=[John Taylor (Municipal - City Councillor, Independent),
      Natalie Pierre (Provincial - MPP, Liberal),
      Karina Gould (Federal - MP, Liberal)]
```

---

## Conversation Flow

```
1. User opens Civil
   → civilLoadDepts() fetches data/departments/{citySlug}.json (or fails silently)
   → If no address searched yet: Civil says "Hey! Search an address above and
     I'll be able to help you reach the right people."
   → If reps loaded: Civil says greeting referencing actual city and asks what's on their mind

2. User describes issue
   → Civil classifies: elected rep issue OR city services issue
   → City services + depts loaded: Civil names the right department and its contact
   → City services + no depts: Civil says "I don't have [city]'s full department
     list yet, but I can still help you reach your elected reps. For city services,
     try [city]'s 311 line or website."
   → Elected rep: Civil identifies correct level and names the rep

3. Civil offers to draft
   → Generates draft inline in the chat as a quoted block
   → Long drafts (>200 words) get a "Copy draft" button below them
   → User can iterate: "shorter", "more formal", "friendlier"

4. User approves draft
   → For elected rep: Civil calls civilPrefillEmail(rep) which opens the existing
     #email-backdrop modal with To/Subject pre-filled
   → For city department: Civil displays dept name, phone, email, and web form link
   → Celebration line: "That's it — your voice is on record ✦"
```

---

## Email Modal Integration

`civilPrefillEmail(rep)` bridges Civil to the existing email compose flow:

```javascript
function civilPrefillEmail(rep) {
  // Set the rep as current (same pattern as openRepProfile)
  currentRepForEmail = rep; // use whichever global the email modal reads
  // Pre-fill subject
  document.getElementById('email-subject').value =
    `Re: [Issue] — constituent from ${selectedCity}`;
  // Open modal
  document.getElementById('email-backdrop').classList.remove('hidden');
}
```

The draft text Civil generated should be copied to the email body field if the user confirms they want it there. Civil asks: "Want me to drop that draft into the email composer?" before calling this.

---

## Data: Departments JSON

### `data/departments/{citySlug}.json`
```json
{
  "city": "Burlington",
  "slug": "burlington",
  "updated": "2026-03-22",
  "departments": [
    {
      "name": "Public Works — Roads",
      "handles": ["pothole", "road", "sidewalk", "snow removal", "street light"],
      "phone": "905-335-7777",
      "email": "roads@burlington.ca",
      "web": "https://www.burlington.ca/en/services-for-you/roads.aspx"
    },
    {
      "name": "Bylaw Enforcement",
      "handles": ["noise", "parking", "property standards", "bylaw"],
      "phone": "905-335-7731",
      "email": "bylaw@burlington.ca",
      "web": "https://www.burlington.ca/en/services-for-you/bylaw.aspx"
    },
    {
      "name": "311 — General Inquiries",
      "handles": ["general", "unsure", "other"],
      "phone": "311",
      "email": null,
      "web": "https://www.burlington.ca/en/city-hall/311.aspx"
    }
  ]
}
```

### `data/departments/index.json`
```json
{
  "cities": [
    { "name": "Burlington", "slug": "burlington", "province": "ON" }
  ]
}
```

`civilLoadDepts()` fetches `index.json` first to check if the city is covered, then fetches the city file if found. Network failures at either step set `civilDepts = null` silently.

---

## UI Details

- Panel: 320px wide, 420px tall, fixed bottom-right, `z-index: 9000` (above modals at ~8000, below nothing)
- Accent: `var(--accent2)` — this is `#682FED` in dark mode and `#ffb963` in light mode, matching brand in both themes
- Civil message bubbles: avatar ⚖️ in a small `var(--accent2)` circle, message in `var(--surface)` background
- User message bubbles: `var(--accent2)` background, right-aligned
- Tooltip nudge: shown on first page load, fades after 4s or after panel is opened; `localStorage.setItem('civil-seen', '1')` prevents it showing again
- Send on Enter key (without Shift) + send button
- Input disabled while Civil is responding (show a typing indicator: three bouncing dots)

---

## Future / Phase 2

- Port Civil's system prompt + personality to a Discord bot
- Expand scope to general civic Q&A
- Add automated city department data pipeline (scraper → `data/departments/`)
- French language support (priority: Terrebonne and other Quebec cities)
