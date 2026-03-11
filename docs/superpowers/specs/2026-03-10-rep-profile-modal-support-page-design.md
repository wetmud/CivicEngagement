# Design Spec: Rep Profile Modal, Support Modal, Budget Comment-out, Courtesy Tip
**Date:** 2026-03-10
**Project:** CivicConnect (`index.html`, single-file vanilla JS)

---

## 1. Rep Profile Modal

### Trigger
Clicking anywhere on a rep card (not just a button) opens a full-screen modal overlay.

### Layout — Two column on desktop, stacked on mobile
**Left column (~35%):**
- Large photo (120px circle, accent ring + glow shadow) — same `object-position: center 15%`
- Name (DM Serif Display, large)
- Elected office + rep set name
- Party badge (pill, coloured by party if detectable, else accent)
- Social links row (Twitter, Facebook, Instagram, YouTube, LinkedIn from `extra`)
- Office addresses + phone numbers from `extra.offices[]` if present
- Action buttons: "✉ Write Email" (primary), "↗ Official Profile" (outline), "Copy Info" (outline)

**Right column (~65%):**
- Wikipedia bio panel — fetched on modal open via Wikipedia API search
  - Search query: `"[rep.name] [city/role]"`
  - Display intro paragraph if found; hide panel entirely if not found
  - Show loading skeleton while fetching; fail silently
- "Contact Tips" panel — static text: cordial communication advice

### Wikipedia API calls
```
Search:  https://en.wikipedia.org/w/api.php?action=query&list=search&srsearch=QUERY&format=json&origin=*
Extract: https://en.wikipedia.org/w/api.php?action=query&prop=extracts&exintro=true&redirects=1&titles=TITLE&format=json&origin=*
```
- No API key required
- Cache results in `wikiCache` object keyed by rep name (in-memory, session only)
- Timeout: 3s; on failure, hide bio panel silently

### Modal CSS
- Full viewport overlay with `backdrop-filter: blur(6px)` + dark scrim
- Modal container: `max-width: 860px`, `border-radius: 20px`, scrollable
- Close on backdrop click or Escape key
- `fadeUp` animation on open (consistent with existing modals)

---

## 2. Support Modal

### Trigger
"☕ Support" button in header (already exists, currently links to Ko-fi directly) → opens modal instead.

### Content sections
1. **Hero** — "Keep CivicConnect Free" heading + one-sentence mission statement
2. **Why section** — 2–3 sentences: BYOK model, $0/month cost, civic purpose
3. **Transparency panel** — running costs: "$0/month server costs (GitHub Pages), AI costs covered by you via BYOK model"
4. **Donation tiers** — One-time suggestion amounts: $5, $10, $25, $50 CAD — all link to `https://ko-fi.com/jasonsteltman`
5. **CTA button** — "☕ Support on Ko-fi" → `https://ko-fi.com/jasonsteltman` (opens new tab)

### Notes
- No Stripe, no backend — everything goes to Ko-fi
- Max suggested tier: $50 CAD (no custom/open field shown in UI)
- Modal pattern matches existing About modal CSS

---

## 3. Budget Feature — Comment Out

- Comment out the "Budget" tab button in the tab bar (HTML comment)
- Comment out the `#tab-budget` panel (HTML comment)
- Leave all JS and `CITY_BUDGETS` data intact — easy to re-enable
- Note in comment: `<!-- BUDGET: re-enable tab button + panel to restore -->`

---

## 4. Courtesy Tip Bubble

- Rendered below the rep list results, above the footer
- Static HTML, always visible after reps load
- Style: subdued info card — slightly different background (`--profile-bg`), left accent border in `--accent`, `border-radius: 12px`
- Icon: 💬 or 🤝
- Text: **"A note on civic communication"** (small heading) + "Representatives respond best to respectful, specific, and good-faith messages. Focus on a single issue, explain your perspective clearly, and be courteous — it's more effective than anger."

---

## 5. Additional API

| API | Purpose | Key |
|-----|---------|-----|
| Wikipedia REST API | Rep bio lookup | None required |

---

## Out of Scope (Roadmap)
- Voting records (requires openparliament.ca + federal reps re-enabled)
- Brave/Google search API for richer bio data
- Persistent Ko-fi subscriber tracking
