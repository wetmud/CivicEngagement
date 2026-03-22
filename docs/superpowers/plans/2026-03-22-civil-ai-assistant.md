# Civil AI Assistant Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Add Civil — a floating AI chat assistant — to `index.html` that helps users identify the right contact (elected rep or city department) and draft a message to them, using Pollinations as a free, keyless AI backend.

**Architecture:** All code lives in `index.html` (single-file, no build step). Civil adds ~250 lines of HTML/CSS/JS. A `civilHistory[]` array holds the conversation. `civilContext()` builds a session snapshot from existing globals (`selectedCity`, `selectedProvince`, `loadedReps`). Pollinations provides OpenAI-compatible multi-turn chat with no API key. Department data lives in static JSON files under `data/departments/`.

**Tech Stack:** Vanilla HTML/CSS/JS, Pollinations text API (`https://text.pollinations.ai/openai`), static JSON data files.

**Spec:** `docs/superpowers/specs/2026-03-22-civil-ai-assistant-design.md`

---

## File Map

| File | Action | Purpose |
|------|--------|---------|
| `index.html` | Modify | Add Civil globals, DOM, CSS, JS functions |
| `data/departments/index.json` | Create | List of cities with department data |
| `data/departments/burlington.json` | Create | Burlington department contacts |

---

## Task 1: Add `loadedReps` global and populate it in `renderRepList()`

This is the foundational integration point. Civil reads `loadedReps` to know who the user's representatives are.

**Files:**
- Modify: `index.html` (~line 2501 for globals, ~line 3140 for `renderRepList`)

- [ ] **Step 1: Add the global variable**

Find the globals block around line 2500 (near `let currentRepForProfile = null;` and `let currentRep = null;`). Add `loadedReps` on the line after:

```javascript
let currentRepForProfile = null;
let currentRep = null;
let loadedReps = [];   // ← ADD THIS LINE
```

- [ ] **Step 2: Populate it inside `renderRepList()`**

Find `function renderRepList(elId, reps, label)` at ~line 3140. Add one line at the very top of the function body. Guard on `elId === 'results-reps'` to avoid being overwritten by the Leaders tab render:

```javascript
function renderRepList(elId, reps, label) {
  if (elId === 'results-reps') loadedReps = reps;  // ← ADD THIS LINE
  // ... rest of existing function unchanged
```

- [ ] **Step 3: Manually verify**

Open `index.html` in browser. Search an address. Open browser console. Type `loadedReps` and confirm it returns an array of rep objects with `.name`, `.elected_office`, `.email`, `.representative_set_name` fields.

- [ ] **Step 4: Commit**

```bash
git add index.html
git commit -m "Add loadedReps global for Civil context"
```

---

## Task 2: Create department data files

Civil uses these to route city services issues to the right department.

**Files:**
- Create: `data/departments/index.json`
- Create: `data/departments/burlington.json`

- [ ] **Step 1: Create the index file**

Create `data/departments/index.json`:

```json
{
  "cities": [
    { "name": "Burlington", "slug": "burlington", "province": "ON" }
  ]
}
```

- [ ] **Step 2: Create the Burlington departments file**

Create `data/departments/burlington.json`:

```json
{
  "city": "Burlington",
  "slug": "burlington",
  "updated": "2026-03-22",
  "departments": [
    {
      "name": "Public Works — Roads",
      "handles": ["pothole", "road", "sidewalk", "snow removal", "street light", "curb", "pavement"],
      "phone": "905-335-7777",
      "email": "roads@burlington.ca",
      "web": "https://www.burlington.ca/en/services-for-you/roads.aspx"
    },
    {
      "name": "Bylaw Enforcement",
      "handles": ["noise", "parking", "property standards", "bylaw", "property", "fence", "zoning"],
      "phone": "905-335-7731",
      "email": "bylaw@burlington.ca",
      "web": "https://www.burlington.ca/en/services-for-you/bylaw.aspx"
    },
    {
      "name": "Parks & Recreation",
      "handles": ["park", "playground", "tree", "trail", "recreation", "arena", "pool"],
      "phone": "905-335-7738",
      "email": "parks@burlington.ca",
      "web": "https://www.burlington.ca/en/services-for-you/parks-and-open-spaces.aspx"
    },
    {
      "name": "Transit (Burlington Transit)",
      "handles": ["bus", "transit", "route", "schedule", "stop"],
      "phone": "905-639-0550",
      "email": null,
      "web": "https://www.burlington.ca/en/services-for-you/burlington-transit.aspx"
    },
    {
      "name": "Waste Collection",
      "handles": ["garbage", "waste", "recycling", "bin", "pickup", "compost"],
      "phone": "905-335-7777",
      "email": null,
      "web": "https://www.burlington.ca/en/services-for-you/garbage-and-recycling.aspx"
    },
    {
      "name": "311 — General Inquiries",
      "handles": ["general", "unsure", "other", "help"],
      "phone": "311",
      "email": null,
      "web": "https://www.burlington.ca/en/city-hall/311.aspx"
    }
  ]
}
```

- [ ] **Step 3: Manually verify the JSON is valid**

```bash
python3 -m json.tool data/departments/index.json
python3 -m json.tool data/departments/burlington.json
```

Both should print the JSON without errors.

- [ ] **Step 4: Commit**

```bash
git add data/departments/
git commit -m "Add Burlington department contacts data"
```

---

## Task 3: Add Civil CSS

Civil's visual styles. Add these into the existing `<style>` block in `index.html`, just before the closing `</style>` tag.

**Files:**
- Modify: `index.html` (inside `<style>` block, before `</style>`)

- [ ] **Step 1: Add the CSS**

Find the closing `</style>` tag and insert before it:

```css
/* ── Civil AI Chat ─────────────────────────────────── */
#civil-bubble {
  position: fixed;
  bottom: 24px;
  right: 24px;
  width: 52px;
  height: 52px;
  background: var(--accent2);
  border-radius: 50%;
  border: none;
  cursor: pointer;
  font-size: 1.4em;
  display: flex;
  align-items: center;
  justify-content: center;
  box-shadow: 0 4px 16px rgba(0,0,0,0.3);
  z-index: 9000;
  transition: transform 0.2s ease, box-shadow 0.2s ease;
}
#civil-bubble:hover {
  transform: scale(1.08);
  box-shadow: 0 6px 20px rgba(0,0,0,0.4);
}
#civil-tooltip {
  position: fixed;
  bottom: 84px;
  right: 20px;
  background: var(--accent2);
  color: var(--on-accent);
  padding: 6px 12px;
  border-radius: 12px;
  font-size: 0.78em;
  font-weight: 500;
  white-space: nowrap;
  z-index: 9001;
  pointer-events: none;
  opacity: 1;
  transition: opacity 0.4s ease;
}
#civil-tooltip.hidden { opacity: 0; }
#civil-panel {
  position: fixed;
  bottom: 84px;
  right: 24px;
  width: 320px;
  height: 420px;
  background: var(--bg);
  border: 1px solid var(--border);
  border-radius: 16px;
  display: flex;
  flex-direction: column;
  overflow: hidden;
  box-shadow: 0 8px 32px rgba(0,0,0,0.35);
  z-index: 9000;
  opacity: 0;
  transform: translateY(12px) scale(0.97);
  pointer-events: none;
  transition: opacity 0.2s ease, transform 0.2s ease;
}
#civil-panel.open {
  opacity: 1;
  transform: translateY(0) scale(1);
  pointer-events: all;
}
#civil-header {
  background: var(--accent2);
  color: var(--on-accent);
  padding: 12px 16px;
  display: flex;
  align-items: center;
  justify-content: space-between;
  flex-shrink: 0;
}
.civil-header-info { display: flex; align-items: center; gap: 10px; }
.civil-avatar {
  width: 32px; height: 32px;
  background: rgba(255,255,255,0.2);
  border-radius: 50%;
  display: flex; align-items: center; justify-content: center;
  font-size: 1em;
}
.civil-name { font-weight: 600; font-size: 0.9em; }
.civil-tagline { font-size: 0.7em; opacity: 0.8; }
#civil-close {
  background: none; border: none;
  color: var(--on-accent);
  cursor: pointer; font-size: 1em; opacity: 0.8;
  padding: 4px;
}
#civil-close:hover { opacity: 1; }
#civil-messages {
  flex: 1;
  overflow-y: auto;
  padding: 12px;
  display: flex;
  flex-direction: column;
  gap: 10px;
  background: var(--surface);
}
.civil-msg {
  display: flex;
  gap: 8px;
  align-items: flex-start;
  animation: civilFadeIn 0.2s ease;
}
.civil-msg.user { flex-direction: row-reverse; }
@keyframes civilFadeIn {
  from { opacity: 0; transform: translateY(4px); }
  to   { opacity: 1; transform: translateY(0); }
}
.civil-msg-avatar {
  width: 28px; height: 28px;
  background: var(--accent2);
  border-radius: 50%;
  display: flex; align-items: center; justify-content: center;
  font-size: 0.78em;
  flex-shrink: 0;
}
.civil-msg-bubble {
  background: var(--bg);
  border: 1px solid var(--border);
  border-radius: 0 10px 10px 10px;
  padding: 9px 12px;
  font-size: 0.82em;
  line-height: 1.5;
  color: var(--text);
  max-width: 82%;
  word-break: break-word;
}
.civil-msg.user .civil-msg-bubble {
  background: var(--accent2);
  color: var(--on-accent);
  border: none;
  border-radius: 10px 0 10px 10px;
}
.civil-typing .civil-msg-bubble {
  display: flex; gap: 4px; align-items: center;
  padding: 12px;
}
.civil-dot {
  width: 7px; height: 7px;
  background: var(--text-muted);
  border-radius: 50%;
  animation: civilBounce 1.2s infinite both;
}
.civil-dot:nth-child(2) { animation-delay: 0.2s; }
.civil-dot:nth-child(3) { animation-delay: 0.4s; }
@keyframes civilBounce {
  0%, 80%, 100% { transform: scale(0.7); opacity: 0.4; }
  40%           { transform: scale(1.1); opacity: 1; }
}
#civil-footer {
  padding: 10px;
  border-top: 1px solid var(--border);
  display: flex;
  gap: 8px;
  background: var(--bg);
  flex-shrink: 0;
}
#civil-input {
  flex: 1;
  background: var(--surface);
  border: 1px solid var(--border);
  border-radius: 8px;
  padding: 8px 12px;
  font-size: 0.82em;
  color: var(--text);
  font-family: inherit;
}
#civil-input:focus { outline: none; border-color: var(--accent2); }
#civil-input:disabled { opacity: 0.5; }
#civil-send {
  background: var(--accent2);
  color: var(--on-accent);
  border: none;
  border-radius: 8px;
  padding: 8px 14px;
  font-size: 0.85em;
  cursor: pointer;
  transition: opacity 0.15s;
}
#civil-send:hover { opacity: 0.85; }
#civil-send:disabled { opacity: 0.4; cursor: default; }
@media (max-width: 400px) {
  #civil-panel  { right: 8px; width: calc(100vw - 16px); bottom: 80px; }
  #civil-bubble { right: 16px; bottom: 16px; }
  #civil-tooltip { right: 8px; }
}
```

- [ ] **Step 2: Manually verify**

Open browser. No Civil elements visible yet (HTML not added). Check browser console — no CSS parse errors.

- [ ] **Step 3: Commit**

```bash
git add index.html
git commit -m "Add Civil chat CSS"
```

---

## Task 4: Add Civil HTML

The chat bubble, tooltip, and panel. Add to `<body>` just before `</body>`.

**Files:**
- Modify: `index.html` (just before `</body>`)

- [ ] **Step 1: Add the HTML**

Find the closing `</body>` tag and insert before it:

```html
<!-- ── Civil AI Chat ──────────────────────────────── -->
<div id="civil-tooltip">Need help? Ask Civil ✦</div>
<button id="civil-bubble" onclick="civilOpen()" aria-label="Open Civil — your civic guide">⚖️</button>

<div id="civil-panel" role="dialog" aria-label="Civil — civic guide chat">
  <div id="civil-header">
    <div class="civil-header-info">
      <div class="civil-avatar">⚖️</div>
      <div>
        <div class="civil-name">Civil</div>
        <div class="civil-tagline">Your civic guide</div>
      </div>
    </div>
    <button id="civil-close" onclick="civilClose()" aria-label="Close Civil">✕</button>
  </div>
  <div id="civil-messages"></div>
  <div id="civil-footer">
    <input
      type="text"
      id="civil-input"
      placeholder="Ask Civil anything…"
      autocomplete="off"
      aria-label="Message Civil"
    />
    <button id="civil-send" onclick="civilSend()" aria-label="Send">→</button>
  </div>
</div>
```

- [ ] **Step 2: Manually verify**

Refresh browser. ⚖️ bubble appears bottom-right. Tooltip appears above it. Clicking bubble does nothing yet (JS not added). No console errors.

- [ ] **Step 3: Commit**

```bash
git add index.html
git commit -m "Add Civil chat HTML"
```

---

## Task 5: Add Civil JavaScript

The core logic. Add this entire block to the `<script>` section of `index.html`, just before the closing `</script>` tag.

**Files:**
- Modify: `index.html` (inside `<script>`, before `</script>`)

- [ ] **Step 1: Add globals, context builder, and helper renderers**

```javascript
// ── Civil AI Chat ────────────────────────────────────

let civilHistory   = [];
let civilOpened    = false;
let civilDepts     = null;
let civilLastDraft = '';  // stores last Civil reply — used by civilPrefillEmail()

const CIVIL_POLLINATIONS_URL = 'https://text.pollinations.ai/openai';

function civilContext() {
  const city  = selectedCity     || 'unknown city';
  const prov  = selectedProvince || 'unknown province';
  const ward  = (typeof wardName !== 'undefined' && wardName) ? wardName : 'unknown ward';
  const depts = civilDepts ? 'true' : 'false';
  const repStr = loadedReps.length
    ? loadedReps.map(r => `${r.name} (${r.elected_office}, ${r.representative_set_name})`).join('; ')
    : 'none loaded';
  return `[Session: City=${city}, Province=${prov}, Ward=${ward}, Reps=[${repStr}], Departments loaded=${depts}]`;
}

function civilSystemPrompt() {
  return `You are Civil, a friendly civic guide for Canadians built into civicengagement.ca.
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
- Celebrate when they take action with a small note like "That's it — your voice is on record ✦"
- Never make up contact information — only use what's in the session context
- If you don't know something, say so plainly`;
}

async function civilLoadDepts() {
  const city = selectedCity ? selectedCity.toLowerCase().trim() : '';
  if (!city) return;
  try {
    const idx = await fetch('data/departments/index.json').then(r => r.ok ? r.json() : null);
    if (!idx) return;
    const match = idx.cities.find(c =>
      c.name.toLowerCase() === city || c.slug === city
    );
    if (!match) return;
    const data = await fetch(`data/departments/${match.slug}.json`)
      .then(r => r.ok ? r.json() : null);
    if (data) civilDepts = data;
  } catch (_) { /* silent fail — Civil will use text fallback */ }
}

function civilRender(text, role) {
  const msgs = document.getElementById('civil-messages');
  const wrap = document.createElement('div');
  wrap.className = 'civil-msg' + (role === 'user' ? ' user' : '');

  if (role !== 'user') {
    const av = document.createElement('div');
    av.className = 'civil-msg-avatar';
    av.textContent = '⚖️';
    wrap.appendChild(av);
  }

  const bubble = document.createElement('div');
  bubble.className = 'civil-msg-bubble';
  bubble.textContent = text;  // textContent only — no HTML injection
  wrap.appendChild(bubble);
  msgs.appendChild(wrap);
  msgs.scrollTop = msgs.scrollHeight;
}

function civilShowTyping() {
  const msgs = document.getElementById('civil-messages');
  const wrap = document.createElement('div');
  wrap.className = 'civil-msg civil-typing';
  wrap.id = 'civil-typing-indicator';

  const av = document.createElement('div');
  av.className = 'civil-msg-avatar';
  av.textContent = '⚖️';
  wrap.appendChild(av);

  const bubble = document.createElement('div');
  bubble.className = 'civil-msg-bubble';

  // Build dots via DOM — no innerHTML
  [1, 2, 3].forEach(() => {
    const dot = document.createElement('div');
    dot.className = 'civil-dot';
    bubble.appendChild(dot);
  });

  wrap.appendChild(bubble);
  msgs.appendChild(wrap);
  msgs.scrollTop = msgs.scrollHeight;
}

function civilHideTyping() {
  const el = document.getElementById('civil-typing-indicator');
  if (el) el.remove();
}
```

- [ ] **Step 2: Add `civilOpen()` and `civilClose()`**

```javascript
async function civilOpen() {
  // Dismiss tooltip permanently
  const tip = document.getElementById('civil-tooltip');
  if (tip) {
    tip.classList.add('hidden');
    try { localStorage.setItem('civil-seen', '1'); } catch (_) {}
  }

  document.getElementById('civil-panel').classList.add('open');
  document.getElementById('civil-input').focus();

  if (!civilOpened) {
    civilOpened = true;
    await civilLoadDepts();

    // System prompt injected once as first history entry
    civilHistory = [{ role: 'system', content: civilSystemPrompt() }];

    let greeting;
    if (loadedReps.length === 0) {
      greeting = "Hey! Search an address above and I'll be able to help you reach the right people.";
    } else {
      const city = selectedCity || 'your area';
      greeting = `Hey! I can see you've found your reps for ${city}. What's on your mind — something local, provincial, or federal?`;
    }

    civilRender(greeting, 'civil');
    civilHistory.push({ role: 'assistant', content: greeting });
  }
}

function civilClose() {
  document.getElementById('civil-panel').classList.remove('open');
}

// Fade out tooltip after 5s on page load if not already seen
window.addEventListener('load', () => {
  try {
    if (localStorage.getItem('civil-seen')) {
      const tip = document.getElementById('civil-tooltip');
      if (tip) tip.classList.add('hidden');
    } else {
      setTimeout(() => {
        const tip = document.getElementById('civil-tooltip');
        if (tip) tip.classList.add('hidden');
      }, 4000);
    }
  } catch (_) {}
});
```

- [ ] **Step 3: Add `civilSend()` — the main send/receive loop**

```javascript
async function civilSend() {
  const input   = document.getElementById('civil-input');
  const sendBtn = document.getElementById('civil-send');
  const text    = input.value.trim();
  if (!text) return;

  // Render user bubble
  civilRender(text, 'user');
  input.value = '';
  input.disabled  = true;
  sendBtn.disabled = true;

  // Prepend session context to user message (not shown in UI)
  const contextualText = civilContext() + '\n\nUser message: ' + text;
  civilHistory.push({ role: 'user', content: contextualText });

  civilShowTyping();

  try {
    const res = await fetch(CIVIL_POLLINATIONS_URL, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ model: 'openai', messages: civilHistory })
    });

    civilHideTyping();

    if (!res.ok) throw new Error('non-200');

    const data  = await res.json();
    const reply = (data.choices && data.choices[0] && data.choices[0].message)
      ? data.choices[0].message.content
      : "Sorry, I couldn't get a response right now.";

    civilLastDraft = reply;  // store for civilPrefillEmail()
    civilHistory.push({ role: 'assistant', content: reply });
    civilRender(reply, 'civil');

  } catch (_) {
    civilHideTyping();
    let fallback = "I'm having trouble connecting right now.";
    if (loadedReps.length > 0) {
      const rep = loadedReps[0];
      fallback += ' Here\'s your most local rep\'s contact: ' + rep.name;
      if (rep.email)     fallback += ' — ' + rep.email;
      else if (rep.url)  fallback += ' — ' + rep.url;
    }
    civilRender(fallback, 'civil');
    civilHistory.push({ role: 'assistant', content: fallback });
  }

  input.disabled   = false;
  sendBtn.disabled = false;
  input.focus();
}

// Send on Enter (not Shift+Enter)
document.addEventListener('DOMContentLoaded', () => {
  const inp = document.getElementById('civil-input');
  if (inp) {
    inp.addEventListener('keydown', e => {
      if (e.key === 'Enter' && !e.shiftKey) {
        e.preventDefault();
        civilSend();
      }
    });
  }
});
```

- [ ] **Step 4: Manually test — basic conversation**

Open browser, search a Burlington address, open Civil.
- Greeting references Burlington and asks what's on their mind ✓
- Type "there's a pothole on my street" → Civil routes to Public Works ✓
- Type "noise complaint from my neighbour" → Civil routes to Bylaw ✓
- Type "help me write an email to my MPP about housing" → Civil drafts a message ✓

- [ ] **Step 5: Manually test — edge cases**

- Open Civil before searching an address → "Search an address above" ✓
- Search a Toronto address → Civil names Toronto in fallback message, not Burlington ✓
- Reload page → tooltip gone, conversation resets ✓
- Disconnect network, send a message → fallback with rep contact info appears ✓

- [ ] **Step 6: Commit**

```bash
git add index.html
git commit -m "Add Civil chat JS — Pollinations-backed civic guide"
```

---

## Task 6: Add `civilPrefillEmail()` — bridge to email compose modal

**Files:**
- Modify: `index.html` (~line 3293, after `closeModal()`)

- [ ] **Step 1: Verify the email modal open pattern**

Find `function openModal(rep)` at ~line 3281. Confirm it:
1. Sets `currentRep = rep`
2. Clears `#email-subject` and `#email-body`
3. Adds `.open` to `#modal-backdrop`

This is the function Civil will call. Subject and body must be set *after* `openModal()` since it clears them.

- [ ] **Step 2: Add the bridge function after `closeModal()`**

```javascript
function civilPrefillEmail(rep, subject, body) {
  // body defaults to civilLastDraft if not explicitly passed
  const emailBody = body || civilLastDraft || '';
  const emailSubject = subject || ('Re: Constituent concern — ' + (selectedCity || 'your area'));
  openModal(rep);  // opens modal, clears fields
  document.getElementById('email-subject').value = emailSubject;
  if (emailBody) document.getElementById('email-body').value = emailBody;
}
```

- [ ] **Step 3: Verify from browser console**

After searching a Burlington address, run in console:

```javascript
civilPrefillEmail(loadedReps[0], 'Test subject', 'Test body text')
```

Email modal should open with both fields pre-filled.

- [ ] **Step 4: Note Phase 2 enhancement**

Add this comment above the function:

```javascript
// Phase 2: Civil will call civilPrefillEmail() after user confirms a draft.
// Trigger: user types "yes send it" or "open the composer" → Civil
// detects confirmation intent and calls this with the draft content.
```

- [ ] **Step 5: Commit**

```bash
git add index.html
git commit -m "Add civilPrefillEmail bridge to email modal"
```

---

## Task 7: Final QA pass

- [ ] **Step 1: Dark mode**

Toggle dark mode. Civil bubble, panel header, message bubbles use CSS variables correctly. No hardcoded colours visible as inconsistencies.

- [ ] **Step 2: Light mode**

Toggle light mode. `var(--accent2)` renders orange. Panel remains readable.

- [ ] **Step 3: Mobile (375px)**

Resize to 375px. Panel fits viewport without overflow (media query from Task 3 handles this).

- [ ] **Step 4: Keyboard navigation**

Tab to ⚖️ bubble → Enter to open → Tab to input → type message → Enter to send → Tab to close button → Enter to close.

- [ ] **Step 5: Commit any QA fixes**

```bash
git add index.html
git commit -m "Civil QA fixes"
```

---

## Task 8: Push and verify on live site

- [ ] **Step 1: Review commits**

```bash
git log --oneline -8
```

Expected commits (in order):
1. `Add loadedReps global for Civil context`
2. `Add Burlington department contacts data`
3. `Add Civil chat CSS`
4. `Add Civil chat HTML`
5. `Add Civil chat JS — Pollinations-backed civic guide`
6. `Add civilPrefillEmail bridge to email modal`
7. `Civil QA fixes` (if needed)

- [ ] **Step 2: Push**

```bash
git push
```

- [ ] **Step 3: Verify on live site**

Visit `civicengagement.ca` after GitHub Pages deploys (~60 seconds).
- ⚖️ bubble appears bottom-right ✓
- Tooltip shows on first visit, fades after 5s ✓
- Searching Burlington address → Civil greets with city name ✓
- Pollinations API responds (may take 2-5s, typing indicator shows) ✓

---

## Notes for Implementer

- `wardName` may not exist as a global in all code paths — `civilContext()` guards with `typeof wardName !== 'undefined'` already
- `loadedReps` assignment in `renderRepList()` guards on `elId === 'results-reps'` to avoid being overwritten by the Leaders tab
- Pollinations can be slow (2-5s) — the typing indicator is essential UX
- The `handles` array in department JSON is context for Civil's AI reasoning, not a JS keyword-matcher
- When adding more cities to `data/departments/`, add to `index.json` and match the slug to what `selectedCity` contains for that city (check what Geoapify returns)
- All user content in Civil message bubbles uses `textContent` — never `innerHTML` — to prevent XSS
