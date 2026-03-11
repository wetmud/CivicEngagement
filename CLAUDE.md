# CivicConnect — CLAUDE.md

Free, open-source civic engagement tool for Canadians. Enter an address → get every elected official who represents you, nearby public services, ward boundaries on a map, city budget breakdowns with AI summaries, and one-click AI-drafted emails to representatives.

**Live:** `wetmud.github.io/CivicConnect`
**Stack:** Single-file vanilla HTML/CSS/JS — no build step, no framework, no backend.

---

## Architecture

Everything lives in `index.html`. No build process. Deploy by pushing to GitHub Pages.

```
index.html
├── <head>        — CSP, meta, Google Fonts, Leaflet CSS/JS CDN
├── <style>       — All CSS (CSS custom properties for theming)
├── <body>        — All HTML markup
└── <script>      — All JavaScript (inline, ~2200 lines)
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
| Anthropic Claude | Email drafting + budget summaries | User-provided via session modal |
| corsproxy.io | CORS proxy for Represent API | Hardcoded URL — replace before production |
| Wikipedia REST API | Rep bio lookup in profile modal | No key required (`origin=*` for CORS) |

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
| Support modal | ~2050 | `openSupport()` / `closeSupport()` — Ko-fi tiers, Recommend Feature button |
| Ward boundary map | ~1430 | Leaflet + GeoJSON; scoring algo picks most-local boundary |
| Nearby services | ~1490 | Geoapify Places, Haversine distance sort |
| Email drafting modal | ~1570 | Claude call; graceful fallback template |
| Budget data (CITY_BUDGETS) | ~1647 | Hard-coded JSON, 8 ON cities, 2025 + 2026 — **tab commented out** |
| Budget tab init/render | ~2022 | City detection by address string match — **re-enable by un-commenting tab + panel** |
| Budget card AI summary | ~2100 | Claude call; JSON parse; session cache |
| Budget email draft | ~2178 | Claude call; same pattern as rep email |

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
- **Federal reps are disabled** (lines ~1464–1465, commented out). Ready to enable when tested.
- **corsproxy.io** is a placeholder. Replace with a Cloudflare Worker or Vercel Edge Function before production traffic.

---

## Known Issues & Technical Debt

| Issue | Severity | Fix |
|-------|---------|-----|
| Geoapify key hardcoded in JS | High | Move to Cloudflare Worker proxy |
| corsproxy.io (untrusted third party) | High | Self-hosted CORS proxy |
| No rate limiting | Medium | Add per-session debounce or Cloudflare rate limiting |
| No ARIA roles on modal | Low | Add `role="dialog"`, `aria-modal`, focus trap |
| Federal rep code commented out | Low | Test and enable or remove dead code |
| Budget city detection is naive string match | Low | Improve with geocoded city name normalization |

---

## Roadmap

**Immediate (before production):**
- [ ] Cloudflare Worker proxy for Geoapify key
- [ ] Replace corsproxy.io with own proxy
- [ ] Custom domain (civicreach.ca)
- [ ] BYOK modal polish + error states

**Near-term features:**
- [ ] Enable federal representatives (code ready)
- [ ] Mobile layout polish
- [ ] Share representative info via URL
- [ ] Expand budget coverage beyond 8 Ontario cities

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
