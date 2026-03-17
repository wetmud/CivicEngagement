# Civic Engagement — CLAUDE.md

Free, open-source civic engagement tool for Canadians. Enter an address → get every elected official who represents you, nearby public services, ward boundaries on a map, city budget breakdowns with AI summaries, and one-click AI-drafted emails to representatives.

**Live:** `civicengagement.ca`
**Stack:** Single-file vanilla HTML/CSS/JS — no build step, no framework, no backend.

---

## Architecture

Frontend lives in `index.html`. No build process. Deploy by pushing to GitHub Pages.
Meeting summarizer is a Python scraper + GitHub Actions pipeline that commits static JSON.

```
index.html                          — All frontend (HTML + CSS + JS, ~2600 lines)
├── <head>                          — CSP, meta, Google Fonts, Leaflet CSS/JS CDN
├── <style>                         — All CSS (CSS custom properties for theming)
├── <body>                          — All HTML markup
└── <script>                        — All JavaScript (inline)

scripts/
└── scrape_burlington.py            — Meeting scraper (Playwright + pdfplumber + Claude)

.github/workflows/
└── burlington-meetings.yml         — Cron: every Tuesday 10 UTC, auto-commits summaries

meetings/burlington/
├── index.json                      — Array of date strings, newest-first (auto-generated)
├── {YYYY-MM-DD}.json               — Individual meeting summary (auto-generated)
└── .gitkeep                        — Placeholder (no summaries generated yet — see Known Issues)
```

**Brand palette (current):**
| Token | Dark mode | Light mode |
|-------|-----------|------------|
| `--accent` | `#ffb963` (orange) | `#682FED` (purple) |
| `--accent-dim` | `#e09840` | `#8252f0` |
| `--accent2` | `#682FED` | `#ffb963` |
| `--on-accent` | `#0e0f0c` | `#ffffff` |
Old lime-green palette is commented out directly above the active `:root` block in `<style>`.

**External APIs (all free tier):**
| API | Purpose | Key location |
|-----|---------|-------------|
| Geoapify | Address autocomplete + geocoding + nearby places | `const GEOAPIFY_KEY` (~line 1148) |
| Represent (OpenNorth) | Canadian rep data + ward boundaries | No key required |
| Anthropic Claude | Email drafting + budget summaries + meeting summarization | User-provided via session modal (frontend); `ANTHROPIC_API_KEY` GitHub Secret (scraper) |
| corsproxy.io | CORS proxy for Represent API | Hardcoded URL — replace before production |
| Wikipedia REST API | Rep bio lookup in profile modal | No key required (`origin=*` for CORS) |
| OpenParliament.ca API | Federal MP voting records | No key required — open civic data |
| Burlington eSCRIBE portal | Council meeting minutes (JS-rendered calendar + PDF documents) | No key required; SSL verify disabled in scraper |

**Claude model in use:** `claude-sonnet-4-20250514`

---

## Key Code Sections

| Feature | Approx. line | Notes |
|---------|-------------|-------|
| Theme toggle | ~1230 | CSS vars swap; map tiles re-render on toggle |
| Address autocomplete | ~1250 | Debounced 300ms, Canada-only filter |
| Representative fetch | ~1380 | Represent API, 3-level sort (city → regional → provincial) |
| Rep card rendering | ~1790 | `escAttr()`, `buildSocialLinks()`, `renderRepList()` — photo + social media |
| Rep profile modal | ~1850 | `openRepProfile()`, `fetchWikiBio()`, `renderWikiBio()` — Wikipedia bio + offices |
| Voting record | ~2650 | `fetchVotingRecord()`, `renderVotes()`, `loadMoreVotes()` — federal MPs only, OpenParliament.ca |
| Support modal | ~2050 | `openSupport()` / `closeSupport()` — Ko-fi tiers, Recommend Feature button |
| Ward boundary map | ~1430 | Leaflet + GeoJSON; scoring algo picks most-local boundary |
| Nearby services | ~1490 | Geoapify Places, Haversine distance sort |
| Email drafting modal | ~1570 | Claude call; graceful fallback template |
| Budget data (CITY_BUDGETS) | ~1647 | Hard-coded JSON, 8 ON cities, 2025 + 2026 — **tab commented out** |
| Budget tab init/render | ~2022 | City detection by address string match — **re-enable by un-commenting tab + panel** |
| Budget card AI summary | ~2100 | Claude call; JSON parse; session cache |
| Budget email draft | ~2178 | Claude call; same pattern as rep email |
| Meetings tab + panel | ~1737 | "Council Meetings" tab; `loadMeetings()` fetches static JSON from `meetings/burlington/` |
| Meeting card rendering | ~2286 | `buildMeetingCard()` — collapsible cards with time bar, items table, outcome badges |
| Meeting share on X | ~2431 | `shareMeetingOnX()` — Twitter Web Intent, 280-char pre-filled tweet |
| Meeting CSS | ~788 | `.meeting-card`, `.meeting-outcome` badges, `.meeting-time-bar`, fadeUp animation |

---

## Claude API Integration

All Claude calls are direct browser → `api.anthropic.com`. **No backend proxy yet.**

**Authentication pattern:** User provides their own Anthropic API key via a session modal (stored in `sessionStorage` only — never persisted). Key is injected into fetch headers at call time.

```js
headers: {
  'Content-Type': 'application/json',
  'x-api-key': getApiKey(),        // from sessionStorage
  'anthropic-version': '2023-06-01'
}
```

If no key is set, the UI prompts the user before any Claude feature is used.

**Three Claude call sites:**
1. `draftEmail()` — representative email drafting
2. `toggleBudgetCard()` — budget category AI summary
3. `draftBudgetEmail()` — budget recommendation email

**Caching:** Budget summaries are cached in `budgetSummaryCache` (in-memory object keyed by `city-year-idx`) to avoid re-querying the same card.

---

## What to Know Before Editing

- **Single file.** Keep it that way until the project meaningfully outgrows it. Avoid premature refactoring into modules.
- **No build step.** Edit `index.html`, refresh browser, done. Deploying = `git push`.
- **CSS custom properties** drive all theming. `--bg`, `--surface`, `--border`, `--accent`, `--text-muted` etc. both light/dark variants live at the top of `<style>`.
- **Budget data is hard-coded.** Adding a new city requires adding a key to `CITY_BUDGETS` with researched data. This is intentional — accuracy > automation.
- **Federal rep voting records** appear in the rep profile modal for MPs/Senators. Uses OpenParliament.ca API — no key required. Slug matching via `toOpenParliamentSlug()` (converts "Jane Smith" → "smith-jane"). Results cached in `votingCache`.
- **corsproxy.io** is a placeholder. Replace with a Cloudflare Worker or Vercel Edge Function before production traffic.

---

## Known Issues & Technical Debt

| Issue | Severity | Fix |
|-------|---------|-----|
| Geoapify key hardcoded in JS | ~~High~~ | ✅ Fixed — Cloudflare Worker proxy (civicconnect-proxy.jason-steltman.workers.dev) |
| corsproxy.io (untrusted third party) | ~~High~~ | ✅ Fixed — same Worker, /proxy?url= route |
| No rate limiting | Medium | Add per-session debounce or Cloudflare rate limiting |
| No ARIA roles on modal | Low | Add `role="dialog"`, `aria-modal`, focus trap |
| OpenParliament slug matching | Low | `toOpenParliamentSlug()` handles accents but may miss unusual names; test edge cases |
| Budget city detection is naive string match | Low | Improve with geocoded city name normalization |
| Meeting scraper date parsing broken | High | eSCRIBE calendar renders 10 UUIDs but `_parse_date_from_text()` resolves 0 dates — format likely changed. Add debug logging, fix parser. |
| eSCRIBE SSL cert not trusted in CI | Medium | `SSL_VERIFY = False` in scraper — works but not ideal |

---

## Roadmap

> Full launch plan with rationale in `LAUNCH_PLAN.txt`.

**LAUNCH BLOCKERS (must do before sharing):**
- [x] Cloudflare Worker proxy for Geoapify key + corsproxy.io replacement (civicconnect-proxy.jason-steltman.workers.dev)
- [x] Social sharing meta tags (`og:*`, `twitter:card`, `meta description`)
- [x] Favicon (🏛️ emoji SVG)

**Post-launch (informed by user feedback):**
- [x] MP voting tracker — OpenParliament.ca, shown in rep profile modal (March 2026)
- [ ] Custom domain — `civicengagement.ca` purchased on GoDaddy; wire up by pointing GoDaddy NS to Cloudflare, then configure Worker route in Cloudflare dashboard
- [ ] Fix meeting scraper → uncomment Meetings tab
- [ ] Re-enable Budget tab (data + UI built, just commented out)
- [ ] Replace `alert()` with toast notifications
- [ ] Mobile layout polish
- [ ] Share representative info via URL
- [ ] Expand budget coverage beyond 8 Ontario cities

**Meeting Summarizer (Burlington pilot → scale):**
- [x] **Phase 1:** GitHub Actions cron → scrape Burlington council minutes via eSCRIBE portal → extract PDF text → Claude summarization → commit JSON to `/meetings/burlington/` (March 2026)
- [x] **Phase 2:** "Council Meetings" tab on site — fetches `index.json` + per-date summary JSONs, renders collapsible cards with time bars, items table, outcome badges (March 2026)
- [x] **Phase 3:** "Share on X" button — Twitter Web Intent pre-filled with 280-char summary + hashtags (March 2026)
- [ ] **Phase 1 bug — scraper date parsing broken:** Playwright finds 10 meeting UUIDs from eSCRIBE calendar but resolves 0 dates. `_parse_date_from_text()` fails on all link text, and `_fetch_meeting_meta()` fallback also fails. Likely the calendar changed its date rendering format. **No summaries have been generated yet.** Next step: add debug logging to print raw link text, then fix date parsing to match current format.
- [ ] **Phase 4:** Scale to other cities — each needs a data-source adapter (Burlington uses in-house video system, not YouTube; Toronto has Open Data API + YouTube)
- Toronto is better-resourced for Phase 4 (Open Data API + YouTube + vote CSV download)

**Longer-term:**
- [ ] PWA / offline support
- [ ] US address support (Google Civic Information API)
- [ ] Response tracking (requires backend + DB — significant scope)
- [ ] Organizer mode (bulk/template messaging for advocacy groups)

---

## Deployment

```bash
# No build step. Just push.
git add -A && git commit -m "..." && git push
# GitHub Pages serves index.html from main branch root.
```

---

## Monetization Notes

**Current stance: free and open-source.**

The only real cost is Claude API usage (per-token billing). With the BYOK pattern, users absorb this cost themselves — project runs at ~$0/month.

If a managed version with a shared API key is offered later, cost-per-user is low (Claude Sonnet is cheap per call). Options if scale ever warrants:
- Ko-fi / GitHub Sponsors (voluntary)
- Vercel/Cloudflare free tier for proxy
- Grants (civic tech, journalism, open data orgs)
- **Not recommended:** paywalling core features — contradicts the civic purpose

---

## Dev Notes (add as you learn)

- The ward boundary scoring algorithm is at `fetchWardBoundary()` — don't simplify it; the priority logic exists to handle edge cases where Represent returns provincial boundaries instead of municipal ones.
- Budget city detection fires on address string, not geocoded city field — watch for edge cases with suburbs (e.g. "Etobicoke" → needs to map to "toronto").
- Rep card photos come from `rep.photo_url` (Represent API). Not all reps have photos — the `onerror` handler hides broken images gracefully.
- Rep social links are parsed from `rep.extra` (dict). Keys checked: `twitter`, `twitter_handle`, `facebook`, `instagram`, `youtube`, `linkedin`. Use `escAttr()` for all values inserted into HTML attributes — never bypass this.
- `--on-accent` CSS var controls text color on top of accent-colored buttons. Dark mode: `#0e0f0c` (works on orange). Light mode: `#ffffff` (works on purple).
- **Rep profile modal** (`#rep-profile-backdrop`): opens on any rep card click. Two-column layout — photo/actions left, Wikipedia bio + offices right. `wikiCache` (in-memory, keyed by `rep.name`) prevents redundant API calls. Fails silently if Wikipedia has no article. Uses DOM methods only (no `innerHTML`) for bio text — XSS safe.
- **Support modal** (`#support-backdrop`): triggered by "☕ Support" header button. Ko-fi link: `ko-fi.com/jasonsteltman`. Tiers: $5/$10/$25/$50 CAD. Recommend Feature button links to GitHub issues. No Stripe, no backend.
- **Budget tab is commented out** — search for `<!-- BUDGET TAB:` and `<!-- BUDGET PANEL:` to re-enable. All JS + data is intact.
- **Meeting scraper pipeline** (`scripts/scrape_burlington.py`): Playwright loads JS-rendered eSCRIBE calendar → extracts meeting UUIDs from `Meeting.aspx?Id=` links → parses dates from link text (4 format patterns + `/Date(ms)/` fallback) → fetches meeting page for minutes PDF link → `pdfplumber` extracts text → Claude (`claude-sonnet-4-20250514`) produces journalist-style JSON summary → writes to `meetings/burlington/{date}.json` + updates `index.json`. GitHub Actions runs every Tuesday 10 UTC and auto-commits.
- **Meeting scraper polite rate limiting**: `REQUEST_DELAY = 2` seconds between requests. `User-Agent: CivicConnect/1.0`. eSCRIBE base: `burlingtonpublishing.escribemeetings.com`.
- **Meeting frontend**: `loadMeetings()` fires on first tab switch (cached via `_meetingsLoaded`). Fetches `meetings/burlington/index.json` → parallel-loads all date JSONs → `buildMeetingCard()` renders collapsible cards. Currently shows "Meeting summaries coming soon..." because no JSON files exist yet.
- **Voting record section** in rep profile modal: only visible for federal reps (`isFederal()` check). `toOpenParliamentSlug("Jane Smith")` → `"smith-jane"`. API endpoint: `GET https://api.openparliament.ca/votes/?politician_slug={slug}&format=json&limit=10`. Results paginated via `loadMoreVotes()` (offset increments by 10). Cache in `votingCache` (keyed by slug). Fails silently — hides section if API unreachable or slug not found. Vote descriptions are bilingual objects `{en: "...", fr: "..."}` — always use `.en` field.
