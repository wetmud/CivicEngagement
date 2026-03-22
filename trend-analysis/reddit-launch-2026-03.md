# CivicConnect — Reddit Launch Research
**Generated:** 2026-03-20

---

## Trend Summary

**The political moment is strong for this tool right now.**

### 1. By-elections on April 13 (Scarborough Southwest, University-Rosedale, Terrebonne)
PM Carney called three by-elections March 8. Liberals are 3 seats short of a majority. These ridings are contested and politically charged — a direct hook for "know who your rep is and contact them."

### 2. Ongoing US-Canada trade war / "Elbows Up" movement
35% US tariffs (escalated August 2025) sparked one of the largest waves of Canadian civic and consumer patriotism in modern memory. Boycotts of US goods, cancelled travel, Buy Canadian campaigns. A full year in, it's baked into the culture now (CBC documented it March 2026). Canadians are already in "do something" mode — CivicConnect gives them a direct channel.

### 3. Ontario under Ford's third majority (elected Feb 27, 2025)
ER closures, housing debates, development charges — Ontario residents have active grievances with both provincial and municipal governments. October 2026 municipal elections (Burlington is already buzzing per Focus Burlington). Perfect time to know who your MPP and city councillor are.

### 4. Burlington: October municipal election on the horizon
Focus Burlington launched a public community engagement initiative around the October 2026 municipal election. Council debated development charges, 2026 budget passed with 4.49% property tax increase, flood protection, Horizon 2050 strategic plan. Locals are engaged.

### 5. Google shut down its Representatives API (April 2025)
Direct competitive gap CivicConnect fills. r/civictech and open source communities may not know a Canadian alternative exists. The Civic Tech Field Guide is a real submission target too.

### 6. NDP leadership race ongoing (March 9–29)
Federal political attention is high right now.

### 7. Civic tech in Canada is having a moment
Canadian Digital Service published a full civic tech report in January 2025 examining partnerships between civic tech groups and government. Civic Tech Toronto still has regular meetups. There's an active, receptive community.

---

## Posting Strategy

| Subreddit | Hook | Timing |
|-----------|------|--------|
| r/burlington | Council meeting summaries, 2026 budget, October election | Anytime — post first |
| r/civictech | Google API shutdown, open-source stack | Anytime |
| r/ontario | Ford third majority, ER closures, October municipal elections | Anytime |
| r/canada | By-elections April 13, minority government | April 6–10 |
| r/canadianpolitics | "Elbows up" → email your MP | April 6–10 |

**Post r/burlington first** — lowest friction, most specific, good message test.
**r/civictech** — small but right audience; could get listed on civictech.guide.
**r/canada / r/canadianpolitics** — post week of April 6–10 to ride the by-election news cycle.

**Other distribution:**
- [Civic Tech Field Guide](https://civictech.guide/) — submit for directory listing
- Civic Tech Toronto meetups — worth reaching out to demo

---

## Drafted Posts

---

### POST 1 — r/canada or r/canadianpolitics

**Title:** Built a free tool so Canadians can find every rep who represents them and email them — no account, no signup

**Body:**
With by-elections April 13 and the trade war still grinding, I kept seeing people say "I want to do something" but not know where to start. Emailing your MP actually works — especially in a minority government where every vote counts.

So I built this: **civicengagement.ca**

Enter your address and you get:
- Every elected official who represents you (federal MP, provincial MPP, city councillor, regional reps)
- One-click email drafting to any of them
- Ward boundary map
- Nearby public services
- Leaders tab (PM Carney + your provincial premier)

It's free, no account needed, open source, and costs me about $40/year to run out of pocket.

Not affiliated with any party. Just a Canadian who wanted a tool like this to exist.

---

### POST 2 — r/ontario

**Title:** Made a free tool to find your MPP, city councillor, and every other rep by address — with one-click email drafting

**Body:**
Ford just won a third majority, ER closures are still hitting rural Ontario, and housing debates are everywhere. If you've ever wanted to contact your MPP or city councillor but didn't know who they were or what to say, I built something for that.

**civicengagement.ca** — enter your Ontario address and you get every elected rep who covers you: federal, provincial, regional, and municipal. Plus a map of your ward boundaries and one-click access to email any of them.

Free. No account. Open source.

October municipal elections are coming up too — good time to start paying attention to who sits on your local council.

---

### POST 3 — r/burlington

**Title:** Built a civic tool that includes Burlington council meeting summaries — free, no signup

**Body:**
Hey Burlington — I built a free civic engagement tool at **civicengagement.ca** and added Burlington-specific features: it scrapes and summarizes Burlington City Council meeting minutes automatically, so you can catch up on what was decided without reading a 200-page PDF.

Enter your address and you also get your ward councillor, your MPP, your MP — and one-click email links to all of them.

With the 2026 budget passing, the Horizon 2050 plan, and October's municipal election coming up, figured locals might find it useful. No ads, no account, just a tool I built because I wanted it to exist.

---

### POST 4 — r/civictech

**Title:** Built an open-source Canadian rep lookup tool after Google shut down its Civic Info API — here's what I used instead

**Body:**
When Google killed its Representatives API in April 2025, I couldn't find a solid Canadian alternative. So I built one.

**civicengagement.ca** — enter a Canadian address and get:
- Every elected rep (federal, provincial, regional, municipal) via the Represent API (OpenNorth)
- Ward boundary GeoJSON on a Leaflet map
- Nearby public services via Geoapify Places
- Leader profiles (PM + premiers) from a hand-maintained JSON file
- One-click email drafting
- Burlington council meeting summaries via a Playwright scraper + Claude pipeline that auto-commits static JSON to GitHub

**Stack:** Single-file vanilla HTML/CSS/JS, no build step, GitHub Pages. Python scraper runs on GitHub Actions cron. Geoapify behind a Cloudflare Worker proxy. Zero backend.

Source is on GitHub (wetmud/CivicConnect). No account needed to use it. Costs me ~$40/yr.

The Represent API is doing the heavy lifting for Canadian rep data — it's excellent and underused. Would be curious if others have built on it.

---

### POST 5 — r/canadianpolitics (alternate angle)

**Title:** "Elbows up" is a great slogan but emailing your MP is the thing that actually moves votes

**Body:**
A year into the trade war and Canadian civic energy is genuinely high — boycotts, Buy Canadian, record election turnout. But a lot of that energy doesn't make it into the parliamentary inbox where it actually matters.

MPs in a minority government pay attention to constituent contact. It takes 5 minutes.

I built **civicengagement.ca** — enter your address, find every rep who represents you (MP, MPP, city councillor, regional reps), and email them directly. Free, no account, open source.

With April 13 by-elections coming up and Carney 3 seats short of a majority, your riding might matter more than usual right now.

---

## Sources

- [Mark Carney by-elections announcement](https://www.pm.gc.ca/en/news/news-releases/2026/03/08/prime-minister-carney-announces-elections)
- [2025 Canadian federal election - Wikipedia](https://en.wikipedia.org/wiki/2025_Canadian_federal_election)
- [Elbows up: how Canadian boycotts played out - CBC News](https://www.cbc.ca/news/canada/boycotts-buy-canada-2025-9.7026211)
- [One year after Trump's sovereignty threats, Canadians keep 'elbows up' - CNBC](https://www.cnbc.com/2026/03/07/canada-boycott-trump-travel-alcohol-economy.html)
- [Canadian Digital Service: How civic tech can help government service delivery](https://digital.canada.ca/2025/01/23/how-can-civic-tech-help-improve-government-service-delivery/)
- [Google Representatives API shutdown notice](https://groups.google.com/g/google-civicinfo-api/c/9fwFn-dhktA)
- [Burlington March 10, 2026 Council Decision Highlights](https://www.burlington.ca/en/news/march-10-2026-council-decision-highlights-and-updates.aspx)
- [Burlington 2026 Budget](https://www.burlington.ca/en/news/2026-budget-invests-in-the-services-and-infrastructure-residents-rely-on.aspx)
- [Focus Burlington community discussion](https://www.focusburlington.ca/2026communitydiscussion/)
- [Civic Tech Toronto](https://civictech.ca/)
- [Civic Tech Field Guide](https://civictech.guide/)
- [2025–2026 US trade war with Canada - Wikipedia](https://en.wikipedia.org/wiki/2025%E2%80%932026_United_States_trade_war_with_Canada_and_Mexico)
- [NDP leadership election - Wikipedia](https://en.wikipedia.org/wiki/2026_New_Democratic_Party_leadership_election)
