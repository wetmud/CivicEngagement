# Civic Engagement

**Know who represents you. Contact them in under a minute.**

Enter your Canadian address and instantly find every elected official who represents you — city councillor, regional rep, MPP, and MP. See your ward boundary on a map. Draft a real email with AI assistance. No account. No login. Nothing collected.

[![MIT License](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)
[![Live](https://img.shields.io/badge/live-civicengagement.ca-blue)](https://civicengagement.ca)

---

<!-- SCREENSHOT: Add a screenshot of the main UI here (address search + rep cards + ward map) -->
<!-- Suggested: `docs/screenshot.png` — 1200x750px, showing dark mode with a rep result loaded -->

---

## Try It Live

**[civicengagement.ca](https://civicengagement.ca)**

---

## Features

- **Address autocomplete** — Canadian addresses, powered by Geoapify
- **All three levels of government** — municipal councillor, regional rep, MPP, and federal MP in one search
- **Ward boundary map** — your riding or district drawn on an interactive map (Leaflet + GeoJSON)
- **Representative profiles** — photo, contact info, social links, Wikipedia bio, and voting record for federal MPs
- **Nearby public services** — libraries, parks, hospitals, and schools sorted by distance
- **AI email drafting** — pick an issue, describe it, get a polished draft ready to send (uses your own Anthropic API key)
- **Council meeting summaries** — Burlington council minutes scraped, summarized by Claude, and surfaced in-app (Burlington pilot — more cities coming)
- **Light and dark mode** — toggle persists in localStorage
- **Zero data collection** — no cookies, no accounts, no analytics, no backend database. Nothing you do here is stored anywhere

---

## How It Works

1. You type your address — autocomplete narrows it to a valid Canadian location
2. The app calls [OpenNorth's Represent API](https://represent.opennorth.ca) to look up every elected official at that coordinate
3. Ward/riding boundaries are fetched as GeoJSON and drawn on the map
4. You click a rep, read their profile, and optionally draft an email with Claude
5. Everything happens in your browser. When you close the tab, it's gone

The API proxy runs on Cloudflare Workers (`civicconnect-proxy.jason-steltman.workers.dev`) — it holds the Geoapify key server-side and handles CORS for the Represent API, so no secrets are exposed in the frontend.

---

## Tech Stack

| Layer | Tool |
|---|---|
| Frontend | Vanilla HTML / CSS / JavaScript — single file, no framework, no build step |
| Address autocomplete + geocoding | [Geoapify API](https://www.geoapify.com) |
| Representatives + ward boundaries | [Represent API](https://represent.opennorth.ca) by OpenNorth (free, open data) |
| MP voting records | [OpenParliament.ca API](https://api.openparliament.ca) (free, open data) |
| Rep bios | Wikipedia REST API |
| Map | [Leaflet.js](https://leafletjs.com) + CartoDB tiles |
| AI email drafting | Anthropic Claude (user-supplied API key, BYOK) |
| API proxy / CORS | [Cloudflare Workers](https://workers.cloudflare.com) (free tier) |
| Meeting scraper | Python + Playwright + pdfplumber + Claude, runs on GitHub Actions |
| Hosting | GitHub Pages |

---

## Run It Locally

No build step. No dependencies to install.

```bash
git clone https://github.com/wetmud/CivicEngagement.git
cd CivicEngagement
open index.html
```

The app will work for rep lookup and map features out of the box — those go through public APIs. For AI email drafting, you'll be prompted to enter your own [Anthropic API key](https://console.anthropic.com) when you first use that feature. It's stored in `sessionStorage` only and never leaves your browser.

If you want to run the full version with your own proxy (to protect a Geoapify key), deploy the included Cloudflare Worker and update the `PROXY_BASE` constant in `index.html`.

---

## Why I Built This

I live in Burlington, Ontario. I couldn't tell you off the top of my head who my city councillor was, let alone how to reach them. That felt like a real problem — not just for me, but for everyone. Your representatives work for you, but the system makes it harder than it should be to figure out who they even are. I built this because the information exists and the connection should take seconds, not an afternoon of Googling.

---

## Roadmap

- [ ] Fix Burlington meeting scraper date parsing (pipeline is built, first summaries blocked on this)
- [ ] Re-enable Budget tab (built and tested, currently commented out)
- [ ] Re-enable federal representatives tab (code ready in comments)
- [ ] Fix Burlington meeting scraper date parsing
- [ ] Re-enable Budget tab
- [ ] Mobile layout polish
- [ ] Expand council meeting summaries beyond Burlington
- [ ] Share a rep's contact info via URL

Got an idea or found a bug? [Open an issue](https://github.com/wetmud/CivicEngagement/issues) or submit a PR.

---

## Data Sources

| Data | Source | License |
|---|---|---|
| Canadian representatives | [OpenNorth Represent API](https://represent.opennorth.ca) | Open Data |
| Ward / district boundaries | [OpenNorth Represent API](https://represent.opennorth.ca) | Open Data |
| Federal MP voting records | [OpenParliament.ca](https://api.openparliament.ca) | Open Data |
| Address geocoding + nearby places | [Geoapify](https://www.geoapify.com) | Free tier |
| Rep bios | [Wikipedia REST API](https://www.mediawiki.org/wiki/API:REST_API) | CC BY-SA |
| Map tiles | [CartoDB](https://carto.com/basemaps) via Leaflet | Free / attribution required |

---

## License

MIT — free to use, modify, and distribute.

---

*Built in Burlington, Ontario — for Canadians who want to actually use their democracy.*
