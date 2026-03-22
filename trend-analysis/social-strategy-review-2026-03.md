# CivicConnect — Social Strategy Review
**Generated:** 2026-03-20
**Agent:** Social Media Strategist

---

## Post Critiques

### POST 1 — r/canada or r/canadianpolitics
**What works:** By-election hook is timely and concrete. "Emailing your MP actually works" is strong. Feature list is clean.

**What's weak:** Title reads like a product announcement — "Built a" signals self-promotion. No personal "why I built this" context. Feature list buries the lede.

**Verdict:** Rewrite needed. Lead with the civic moment, not the product.

---

### POST 2 — r/ontario
**What works:** Good contextual hooks (Ford majority, ER closures, housing, municipal elections). October election mention is smart.

**What's weak:** "I built something for that" is passive. Ontario scope is undersold. Should explicitly name Ford + ER closures as reasons to act, not just context.

**Verdict:** Minor rewrite. Punch up the frustration hook, name the tool earlier.

---

### POST 3 — r/burlington
**What works:** Most targeted post. Specific local context is the right move. Most authentic.

**What's weak:** Opening buries the best hook — council meeting summaries. If you're local to Burlington, say so.

**Verdict:** Light rewrite. Lead with meeting summaries, add personal local connection if honest.

---

### POST 4 — r/civictech
**What works:** Strongest post. Tech-credible, stack details appropriate, Represent API callout invites discussion. Google API shutdown framing is excellent.

**What's weak:** "Here's what I used instead" undercuts the title. Doesn't invite architectural discussion. Scraper pipeline detail is interesting but under-explained.

**Verdict:** Minor addition. Add one architecture decision note + discussion question.

---

### POST 5 — r/canadianpolitics (alternate)
**What works:** "Elbows Up" hook is clever. Converting civic energy → concrete action is the right angle.

**What's weak:** Two posts jammed together — op-ed seam is visible. "A year into the trade war" is slightly inaccurate for March 2026.

**Verdict:** Rewrite needed. Pick one angle, don't split.

---

## Revised Posts

### POST 1 REVISED — r/canada

**Title:** April 13 by-elections are in 24 days. Here's how to find out who your MP is and email them in under 5 minutes.

**Body:**
Carney is three seats short of a majority. Three by-elections on April 13 — Scarborough Southwest, University-Rosedale, Terrebonne. If you've been following the trade war and wanting to do something that actually reaches Parliament, now is a specific, concrete moment to act.

Emailing your MP works. Not because they read every email personally, but because volume in a minority government gets counted. A few hundred emails from a riding moves staff to brief the MP.

I built civicengagement.ca to make that as frictionless as possible. Enter your address and you get:

- Every rep who covers you: federal MP, provincial MPP, city councillor, regional reps
- One-click email drafting to any of them
- Ward boundary map
- Nearby public services
- PM Carney + your provincial premier in a Leaders tab

Free, no account, no signup, open source. Costs me ~$40/year out of pocket.

Not affiliated with any party. Just wanted this to exist.

---

### POST 3 REVISED — r/burlington

**Title:** You can now read Burlington Council meeting summaries without reading a 200-page PDF — built into a free civic tool

**Body:**
I built a feature into civicengagement.ca that automatically scrapes and summarizes Burlington City Council meeting minutes. If a meeting happened, it shows up as a readable summary — agenda items, decisions, what was passed. No PDF required.

That's the Burlington-specific part. The full tool also lets you enter your address and get your ward councillor, MPP, and MP with one-click email links to all of them.

With the 2026 budget passed, Horizon 2050 planning underway, and municipal elections in October, figured locals might actually want this. Free, no ads, no account. [I live in/near Burlington and] wanted it to exist so I built it.

Source is on GitHub if anyone wants to look at how the scraper works.

*(Note: Only include the bracketed sentence if true.)*

---

### POST 4 REVISED — r/civictech

**Title:** Built an open-source Canadian rep lookup after Google killed its Civic Info API — here's the architecture and what I learned

**Body:**
When Google shut down the Representatives API in April 2025, there was no clean Canadian alternative. So I built one.

civicengagement.ca — enter a Canadian address and get every elected rep (federal, provincial, regional, municipal), ward boundaries on a Leaflet map, nearby public services, and one-click email drafting.

**Stack decisions worth explaining:**

Single-file vanilla HTML/CSS/JS on GitHub Pages — no build step, no framework. The constraint was intentional: I wanted zero infrastructure dependencies and a codebase a non-developer could fork and modify.

The Represent API (OpenNorth) handles all Canadian rep data. It's excellent and almost nobody knows it exists outside of civic tech circles. The GeoJSON for ward boundaries comes from the same API.

The Burlington meeting summarizer is a separate Python pipeline: Playwright scrapes the eSCRIBE portal, pdfplumber pulls text from PDFs, Claude summarizes and structures the output, and a GitHub Actions cron commits static JSON back to the repo. The frontend just fetches JSON. No database, no server.

Geoapify handles geocoding behind a Cloudflare Worker proxy to keep the API key off the client.

Source: github.com/wetmud/CivicConnect. Costs ~$40/yr. No account needed to use.

Would genuinely like to know: has anyone else built on the Represent API? And is there a solid equivalent for non-OpenNorth municipalities (thinking about expanding beyond Burlington for the meeting scraper)?

---

### POST 5 REVISED — r/canadianpolitics

**Title:** The "Elbows Up" energy is real but most of it never reaches an MP's inbox — here's a tool that fixes that

**Body:**
Since the February 2025 tariff escalation, Canadian civic energy has been genuinely different — boycotts, Buy Canadian, high election engagement. But a lot of that energy dissipates into social media instead of landing in the places where it actually changes votes.

In a minority government, constituent contact to MPs is not symbolic. It gets tracked, briefed, and counted when whips are doing headcounts. With three by-elections April 13 and Carney three seats short of a majority, your riding math might be unusual right now.

I built civicengagement.ca for this: enter your address, get every rep who represents you (MP, MPP, councillor, regional reps), and email them directly. Takes about two minutes. Free, no account, open source.

If you've been telling people to "do something," this is a pretty low-friction something.

---

## Research Gaps

### Immediate (before April 6 posts)
- What are the specific issues in each April 13 riding? (Scarborough Southwest, University-Rosedale, Terrebonne) — lets you tailor r/toronto and r/montreal posts
- Has any Canadian MP or party office published data on constituent contact volume? One credible source saying "emails move votes" would strengthen POST 1 and POST 5
- Is there an active r/ontario or r/canada thread about the trade war or by-elections from the last 2 weeks? Timing your post to ride an active thread beats starting cold

### For Burlington
- What specific line items in the 2026 Burlington budget would make locals angry or interested? (Check your own meeting summaries)
- Is there a Burlington community Facebook group or NextDoor with higher engagement than r/burlington?

### For r/civictech
- What happened publicly when Google shut down the Civic Info API? Were there blog posts, complaints, other builders? Linking to that conversation frames your project as a community response
- Who maintains the Represent API now? Is OpenNorth still active? Worth acknowledging as a risk — shows you've thought about it

### Credibility
- Has civicengagement.ca been mentioned anywhere yet — local press, GitHub stars, HN? Social proof helps
- Is there recent Canadian polling on civic participation or political frustration to cite?

---

## Untapped Channels

### Subreddits Not Yet Considered

| Subreddit | Size | Angle |
|-----------|------|-------|
| r/onguardforthee | ~180k | **Highest-upside miss.** Trade war / "elbows up" framing fits perfectly |
| r/toronto | ~400k | Scarborough Southwest by-election, local rep lookup |
| r/canadahousing | ~180k | Hook: find who represents you on zoning/housing decisions |
| r/vancouver | ~280k | Federal election season, housing + transit rep contact |
| r/ottawa | ~180k | Federal politics audience, proximity to Parliament |
| r/NDP | ~15k | NDP leadership race hook |
| r/CanadaPublicServants | ~50k | Civic tech credibility angle |
| r/Edmonton | ~120k | NDP stronghold, politically active |
| r/Winnipeg | ~90k | NDP leadership relevance |

### Communities Outside Reddit
- **Civic Tech Toronto Slack/meetup** — warm audience, post here *before* Reddit, not after
- **Hacker News "Show HN"** — technical framing: "Show HN: I built a Canadian civic rep lookup after Google killed its API"
- **Mastodon** (infosec.exchange, social.coop) — civic tech builders overrepresented here, tag OpenNorth
- **LinkedIn** — three audiences: civic tech professionals, public policy academics, municipal government staff
- **Product Hunt** — low Canadian relevance but good for inbound links and search

### What Not to Bother With
- TikTok / Instagram — wrong audience, wrong format
- Facebook organic — dead for cold posts (Burlington Facebook group is the exception)
- Bluesky — not enough critical mass yet

---

## Timing & Sequencing

### Week of March 24-28 (now — soft launch)
- Post r/burlington (revised) — lowest friction, test the format
- Post r/civictech (revised) — feedback-oriented audience
- Post to Civic Tech Toronto community (Slack/meetup) — warm audience, get early users

### Week of March 31 – April 4 (pre-election buildup)
- Post r/ontario — Ford + ER closures + municipal elections angle
- Post r/onguardforthee — revised POST 5 framing
- Drop comments (not posts) in active r/canada / r/canadianpolitics by-election threads — builds presence before main post

### Week of April 6-10 (by-election window — main push)
- r/canada — revised POST 1. **Tuesday or Wednesday, 7-9pm Eastern** (peak Canadian Reddit traffic)
- r/canadianpolitics — revised POST 5. Same day is fine if content is distinct
- r/toronto — if Scarborough Southwest / University-Rosedale getting local attention, localize the post
- LinkedIn post — civic tech + policy audience
- "Show HN" — Hacker News, technical framing

### After April 13 (post-election)
- If notable outcome: follow-up post — "Tool I built got used during the by-election push — here's what I learned"
- Mastodon post — quieter audience, longer shelf life

---

## Cross-Platform Notes

**Twitter/X:** Tweet thread, 4-5 tweets max. Tag @OpenNorth. Don't expect high organic reach — use mainly for shareable link.

**LinkedIn (3 distinct posts):**
1. Civic tech professionals — Google API shutdown + architecture
2. Public policy academics — civic engagement research angle, cite constituent contact study
3. Municipal government staff — council meeting summary automation angle

**Mastodon:** Adapt r/civictech post, tag OpenNorth.

**Not worth it yet:** TikTok, Instagram, Bluesky (revisit in 6 months).

---

## Summary Priorities

1. Post r/burlington and r/civictech this week — test and iterate
2. Research specific by-election riding issues + find one credible citation on constituent contact effectiveness before April 6-10
3. **Add r/onguardforthee — highest-upside miss in current strategy**
4. Revised POST 4 (r/civictech) is the strongest content — adapt for LinkedIn and HN before by-election window
5. Staged approach is correct — tighten timing per above
