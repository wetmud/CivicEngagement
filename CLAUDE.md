# Civic Engagement — CLAUDE.md

Free, open-source civic engagement tool for Canadians. Enter an address → get every elected official who represents you, nearby public services, ward boundaries on a map, a Leaders tab (Premier + PM), and one-click email drafting to representatives.

**Live:** `civicengagement.ca`
**Stack:** Single-file vanilla HTML/CSS/JS — no build step, no framework, no backend.

---

## Architecture

Frontend lives in `index.html`. No build process. Deploy by pushing to GitHub Pages.
Meeting summarizer is a Python scraper + GitHub Actions pipeline that commits static JSON.

```
index.html                          — All frontend (HTML + CSS + JS, ~3900 lines)
├── <head>                          — CSP, meta, Google Fonts, Leaflet CSS/JS CDN
├── <style>                         — All CSS (CSS custom properties for theming)
├── <body>                          — All HTML markup
└── <script>                        — All JavaScript (inline)

data/
└── leaders.json                    — Hard-coded PM + provincial leaders, fetched at runtime

scripts/
└── scrape_burlington.py            — Meeting scraper (Playwright + pdfplumber + Claude)

.github/workflows/
└── burlington-meetings.yml         — Cron: every Tuesday 10 UTC, auto-commits summaries

meetings/burlington/
├── index.json                      — Array of date strings, newest-first (auto-generated)
└── {YYYY-MM-DD}.json               — Individual meeting summary (auto-generated)
```

**Brand palette (current):**
| Token | Dark mode | Light mode |
|-------|-----------|------------|
| `--accent` | `#ffb963` (orange) | `#682FED` (purple) |
| `--accent-dim` | `#e09840` | `#8252f0` |
| `--accent2` | `#682FED` | `#ffb963` |
| `--on-accent` | `#0e0f0c` | `#ffffff` |

**External APIs (all free tier):**
| API | Purpose | Key location |
|-----|---------|-------------|
| Geoapify | Address autocomplete + geocoding + nearby places | Cloudflare Worker proxy |
| Represent (OpenNorth) | Canadian rep data + ward boundaries | No key required |
| Anthropic Claude | Meeting summarization (scraper only — frontend AI disabled) | `ANTHROPIC_API_KEY` GitHub Secret |
| Wikipedia REST API | Rep bio lookup in profile modal | No key required |
| OpenParliament.ca API | Federal MP voting records | No key required |
| Burlington eSCRIBE portal | Council meeting minutes | No key required; SSL verify disabled |

**Claude model in use (scraper):** `claude-sonnet-4-20250514`

---

## Key Code Sections

| Feature | Approx. line | Notes |
|---------|-------------|-------|
| Theme toggle | ~1230 | CSS vars swap; map tiles re-render on toggle |
| Address autocomplete | ~1250 | Debounced 300ms, Canada-only filter; captures `state_code` for province detection |
| Representative fetch | ~1380 | Represent API, 3-level sort (city → regional → provincial) |
| Rep card rendering | ~1790 | `escAttr()`, `buildSocialLinks()`, `renderRepList()` |
| Rep profile modal | ~1850 | `openRepProfile()`, `fetchWikiBio()` — Wikipedia bio + offices |
| Voting record | ~2650 | `fetchVotingRecord()` — federal MPs only, OpenParliament.ca |
| Support modal | ~2050 | Ko-fi tiers ($5/$10/$25/$50), ~$40/yr hosting cost shown |
| Tips modal | ~2036 | `openTips()` — advice on writing better emails, using AI |
| Ward boundary map | ~1430 | Leaflet + GeoJSON; scoring algo picks most-local boundary |
| Nearby services | ~1490 | Geoapify Places, Haversine distance sort |
| Email modal | ~1570 | Manual compose only — AI draft disabled. Has tip nudge. |
| Leaders tab | ~3722 | `initLeadersTab(provinceCode)`, `renderLeaderCard()` — fetches data/leaders.json |
| Budget data (CITY_BUDGETS) | ~3800 | Hard-coded JSON, 8 ON cities, 2025 + 2026 — **tab commented out** |
| Meetings tab + panel | ~1793 | Commented out — scraper being fixed |
| Meeting card rendering | ~2350 | `buildMeetingCard()` — collapsible cards with time bar, items table |

---

## AI Status — DISABLED on Frontend

Frontend AI (email drafting, budget summaries) is **commented out** pending funding. To re-enable:
1. Un-comment the BYOK block starting `// ── API key (BYOK) — DISABLED` (~line 2090)
2. Un-comment `generateEmail` / `_doGenerateEmail` functions (~line 3280)
3. Un-comment budget AI calls in `toggleBudgetCard` and `draftBudgetEmail`
4. Restore the `✦ AI Draft` button in the email modal HTML
5. Remove the tip nudge or update it to reflect AI is back

The scraper backend still uses Claude via `ANTHROPIC_API_KEY` GitHub Secret — unaffected.

**Monetization path:** Ko-fi donations at ko-fi.com/jasonsteltman. Support modal shows ~$40/yr hosting cost. Featured tier $25.

---

## Leaders Tab

`data/leaders.json` contains hard-coded data for the federal PM and all 13 provincial/territorial premiers. The file has an `_instructions` block at the top with a ready-to-paste Claude prompt for updating when a leader changes.

**To update a leader:** Edit the relevant entry in `data/leaders.json`, bump `verified_at` to today's date, commit. The frontend fetches this file at runtime so it goes live immediately — no redeploy needed.

**Province detection:** Geoapify `state_code` field is captured from both autocomplete selection and fallback geocode. Stored in `selectedProvince`. Passed to `initLeadersTab(provinceCode)`.

---

## What to Know Before Editing

- **Single file.** Keep it that way until the project meaningfully outgrows it.
- **No build step.** Edit `index.html`, refresh browser, done. Deploying = `git push`.
- **CSS custom properties** drive all theming. `--bg`, `--surface`, `--border`, `--accent`, `--text-muted` etc.
- **Budget data is hard-coded.** Adding a new city = add a key to `CITY_BUDGETS`. Intentional — accuracy > automation.
- **Federal rep voting records** use OpenParliament.ca. Slug via `toOpenParliamentSlug()`. Cached in `votingCache`.
- **escHtml() and escAttr()** must be used on all user/API data inserted into HTML. Never bypass.

---

## Known Issues & Technical Debt

| Issue | Severity | Notes |
|-------|---------|-------|
| Meeting scraper date parsing | Medium | Partially fixed 2026-03-18. Awaiting next Tuesday CI run to verify. |
| No rate limiting | Low | Add per-session debounce or Cloudflare rate limiting |
| Budget city detection is naive string match | Low | Only matters when budget tab is re-enabled |

---

## Roadmap

**Next up:**
- [ ] Verify scraper fix after next Tuesday CI run; fix date parsing if still broken
- [ ] Share on Reddit (r/ontario, r/burlington, r/canadianpolitics, r/civictech) and X
- [ ] Reach out to https://www.dougfordclownshow.ca/
- [ ] **Build Civil** — AI chat assistant, fully designed. Spec + plan ready: `docs/superpowers/plans/2026-03-22-civil-ai-assistant.md`
- [ ] City department contacts pipeline — `data/departments/{city}.json` (Burlington first, manual; automate later). Required by Civil.
- [ ] Re-enable AI drafting once funded
- [ ] Leader contacts: cabinet/minister links in leader profile (future)
- [ ] Budget tab: Jason has ideas for non-AI version — revisit

**Longer-term:**
- [ ] US address support (Google Civic Information API)
- [ ] Response tracking (requires backend + DB)
- [ ] Organizer mode (bulk/template messaging)
- [ ] Scale meeting scraper to other cities (Toronto has Open Data API + YouTube)
- [ ] Civil Phase 2: general civic Q&A, "Open in composer" button, French language support
- [ ] Civil Discord bot (same personality/system prompt, different transport)

---

## Deployment

```bash
git add -A && git commit -m "..." && git push
# GitHub Pages serves index.html from main branch root.
```

---

## Dev Notes

- Ward boundary scoring algo at `fetchWardBoundary()` — don't simplify it; the priority logic handles edge cases.
- Rep card photos from `rep.photo_url` — `onerror` handler hides broken images.
- Rep social links from `rep.extra` dict — keys: `twitter`, `facebook`, `instagram`, `youtube`, `linkedin`.
- `--on-accent` controls text on accent-colored buttons. Dark: `#0e0f0c`, Light: `#ffffff`.
- Support modal (`#support-backdrop`): Ko-fi link `ko-fi.com/jasonsteltman`. Tiers $5/$10/$25/$50.
- Budget tab is commented out — search `<!-- BUDGET TAB:` and `<!-- BUDGET PANEL:` to re-enable.
- Leaders JSON is fetched at runtime — cached in `_leadersData` after first load.
- Meeting scraper: `REQUEST_DELAY = 2s`, polite User-Agent. Loads current + previous month calendar. Debug logging prints raw link text for every UUID found.
