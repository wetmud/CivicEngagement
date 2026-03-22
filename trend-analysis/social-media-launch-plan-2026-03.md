# CivicConnect — Social Media Launch Plan
**Generated:** March 20, 2026
**Agent:** Social Media Strategist
**Campaign window:** March 20 – April 20, 2026
**Live URL:** civicengagement.ca

---

## 1. Campaign Overview

### Goal
Drive meaningful first-use traffic to civicengagement.ca, establish Jason (wetmud) as a credible solo civic-tech builder, and create a feedback loop before the April 13 by-elections and October 2026 municipal cycle.

### Success Metrics (30 days)

| Metric | Minimum | Good | Great |
|--------|---------|------|-------|
| Unique visitors | 500 | 2,000 | 5,000+ |
| Reddit post upvotes (combined) | 100 | 500 | 1,500+ |
| GitHub stars | 10 | 50 | 150+ |
| Ko-fi supporters | 1 | 5 | 15+ |
| Email drafts generated (self-reported) | any | — | — |
| Civic Tech Toronto engagement | mentioned | demo request | invited to present |

Track via: Cloudflare Analytics, GitHub Traffic tab, Ko-fi dashboard.

### Tone & Voice

**What you are:** A solo Canadian builder who got annoyed that Google killed its civic info API and built the replacement. Not a startup, not an NGO, not a government initiative. A person.

**Voice rules:**
- First person, direct. "I built this" not "we built"
- Lead with the civic moment, not the product
- Acknowledge limitations honestly (data can be stale, Burlington-only meetings for now)
- Never say "check out" — reads as spam
- Credit OpenNorth / Nord Ouvert explicitly and sincerely
- One ask per post maximum. Either GitHub star, Ko-fi, or "let me know what you think" — never all three

---

## 2. Content Calendar

| Date | Platform | Audience | Post | Notes |
|------|----------|----------|------|-------|
| Thu Mar 20 | Civic Tech Toronto Slack | #projects or #general | CT-1 | Post here FIRST — before Reddit |
| Fri Mar 21 | Reddit | r/civictech | POST 4 | Technical audience, safe to lead with |
| Fri Mar 21 | Mastodon | infosec.exchange + social.coop | MAST-1 | Tag @opennorth |
| Sat Mar 22 | Hacker News | Show HN | HN-1 | Weekend is fine for Show HN |
| Mon Mar 24 | Reddit | r/burlington | POST 3 | Local = most forgiving audience |
| Tue Mar 25 | Twitter/X | — | TW-1 | Thread, tag @opennorth |
| Mon Mar 31 | Reddit | r/ontario | ONT-1 | Ford majority / ER closures angle |
| Mon Mar 31 | Reddit | r/onguardforthee | OGF-1 | Elbows Up angle |
| Tue Apr 1 | Reddit | r/NDP | NDP-1 | Leadership race + contact-your-rep |
| Tue Apr 1 | LinkedIn | Civic tech professionals | LI-1 | Architecture + open data framing |
| Wed Apr 2 | LinkedIn | Public policy academics | LI-2 | Research angle |
| Thu Apr 3 | Reddit | r/canadahousing | HOUS-1 | Zoning + dev charges angle |
| Sun Apr 6 | Reddit | r/canada | POST 1 | By-election hook — timing critical |
| Mon Apr 7 | Reddit | r/canadianpolitics | POST 5 | Trade war / elbows up angle |
| Tue Apr 8 | Reddit | r/toronto | TOR-1 | Scarborough SW + Univ-Rosedale |
| Wed Apr 9 | LinkedIn | Municipal staff / planners | LI-3 | Constituent contact framing |
| Mon Apr 14 | Reddit | r/canada or r/canadianpolitics | FU-1 | Post-election follow-up |
| Mon Apr 14 | Twitter/X | — | TW-2 | By-election results thread |

---

## 3. All Post Copy

---

### POST 1 — r/canada
**Title:** April 13 by-elections are in 24 days. Here's a free tool to find and email every politician who represents you.

**Body:**
Three ridings vote on April 13. Carney is three seats short of a majority. Terrebonne was decided by one vote in 2025, the Supreme Court annulled it, and the rematch is on.

Whether or not you're in one of those ridings — your MP, MPP, and city councillor exist right now, and most people have never contacted any of them.

I built civicengagement.ca to fix that. Enter any Canadian address and you get:

- Every elected official at city, provincial, and federal level
- Their emails, phones, offices, social links
- An email drafting tool (you write it, the tool formats it)
- Ward boundary map and nearby public services
- Federal MP voting records via OpenParliament.ca
- Burlington council meeting summaries (expanding to other cities)

No account. No signup. No tracking. ~$40/yr to run, donation-supported.

The tool uses the Represent API from OpenNorth / Nord Ouvert and OpenParliament.ca — both excellent open data projects worth knowing about.

It won't change anyone's mind on its own. But if you've ever meant to contact a rep and didn't because you didn't know who to contact or what to say — this removes that friction.

April 13 is a real moment. Use it if you want.

---

### POST 3 — r/burlington
**Title:** I built a tool that auto-summarizes Burlington city council meetings — here's what happened at the Feb 17 session

**Body:**
Keeping up with Burlington council is a part-time job. The minutes run 40+ pages, the videos are long, and the eSCRIBE portal is not exactly user-friendly.

So I built a scraper that pulls the agenda PDFs, runs them through an AI summarizer, and publishes readable summaries at civicengagement.ca.

[INSERT 3-5 bullet highlights from meetings/burlington/2026-02-17.json before posting]

The tool also does the broader thing: enter any Burlington address and you get your city councillor, regional councillor, MPP, and MP — all with one-click email drafting.

October 2026 municipal election is coming up fast. Ward boundaries, who your councillor is, what they've been voting on — it's all in there.

Free, no account, no tracking. Open source: github.com/wetmud/CivicConnect

Feedback welcome — especially if something is wrong or missing.

**⚠ Note:** Confirm Feb 17 summary renders correctly in the UI before posting.

---

### POST 4 — r/civictech
**Title:** I rebuilt the Google Civic Information API for Canada after Google killed it — open source, single-file, no backend

**Body:**
Google deprecated its Civic Information API last April. For Canadian addresses it was never reliable anyway, but it was the only option a lot of civic tools were wired to. When it died, a bunch of projects quietly broke.

I'd been frustrated with this for a while, so I built a replacement: civicengagement.ca.

**What it does:**

Enter a Canadian address → get every elected official at city, provincial, and federal level, with contact info, social links, ward boundary map, nearby public services, and one-click email drafting. Federal MPs also have voting records pulled from OpenParliament.ca.

**The stack:**

- Vanilla HTML/CSS/JS — single file, no build step, no framework
- Leaflet.js for the ward boundary map (GeoJSON from Represent API)
- Geoapify for address autocomplete and geocoding (key protected via Cloudflare Worker proxy)
- Represent API (OpenNorth / Nord Ouvert) for rep data and ward boundaries — the real foundation
- OpenParliament.ca for federal voting records
- Wikipedia REST API for rep bios
- GitHub Actions + Python + Claude API for Burlington council meeting summaries (auto-scrapes eSCRIBE PDFs on a cron)
- Hosted on GitHub Pages, ~$40/yr total

**Honest limitations:**

The Represent API data can be stale after redistribution cycles — OpenNorth maintains it but it's volunteer-driven. If you find a missing rep or wrong boundary, file an issue with them, not me. I'm just the consumer.

Meeting summaries are Burlington-only for now. Toronto is next because they have an Open Data API and YouTube archives.

**What I'm curious about:**

Anyone else building on the Represent API? What's your experience with data freshness? And is there a solid equivalent for non-OpenNorth municipalities?

Source: github.com/wetmud/CivicConnect

---

### POST 5 — r/canadianpolitics
**Title:** "Elbows up" energy rarely makes it to an MP's inbox. This tool makes that easier.

**Body:**
Since February, there's been more political energy in Canada than I've seen in years. People are angry about the tariffs, about the trade war, about what comes next. That anger is mostly circulating on social media.

The research on this is pretty clear: constituent contact moves politicians — especially in minority governments, especially in marginal ridings. A study by Bergan and Cole (Political Behavior, 2015) found roughly a 12-point shift in legislator support from constituent contact in a randomized field experiment. Westminster party discipline compresses that effect, but in a minority Parliament, in a riding that was decided by a few hundred votes, it's not nothing.

The gap between "I'm furious about this" and "I sent an email to my MP" is mostly logistical. Most people don't know who their MP is. They don't know how to find an email address. They start drafting something and give up.

I built civicengagement.ca to close that gap.

Enter your address → instant list of everyone who represents you, with email and phone. Draft a message right there, send it. No account, no signup, no data collected.

It covers federal, provincial, and municipal reps. Because the trade war isn't the only thing happening — there are ER closures, housing policy failures, and an Ontario municipal election cycle starting. Those are also worth contacting people about.

Free. Open source. Built by one person. ~$40/yr to run.

Data via OpenNorth / Nord Ouvert's Represent API.

---

### ONT-1 — r/ontario
**Title:** I built a free tool to find your Ontario MPP, city councillor, and MP — with one-click email drafting

**Body:**
Ford just won his third majority. If you're watching hospital closures, housing policy, development charges, or any of the other fights playing out right now — your MPP exists and their email address is public.

Most people have never contacted an elected official. Not because they don't care, but because the friction is high: who do I contact, what's their email, what do I say?

I built civicengagement.ca to remove that friction. Enter any Ontario address:

- Instant list of your city councillor, regional councillor, MPP, and MP
- Contact info for all of them
- Built-in email drafting tool
- Ward boundary map
- Federal voting records for your MP
- Nearby public services (hospitals, clinics, libraries)

No account, no tracking, no ads. Free. Open source.

Burlington residents also get auto-summarized city council meeting notes — expanding to other cities over time.

October 2026 municipal elections are less than 7 months away.

Built on OpenNorth / Nord Ouvert's Represent API. Source at github.com/wetmud/CivicConnect.

---

### OGF-1 — r/onguardforthee
**Title:** If you want to put "elbows up" energy somewhere useful — this tool finds your MP and drafts the email

**Body:**
Since February, this sub has had more energy than I've seen since 2019. That's not nothing.

Most of it stays here. The MPs don't see it.

I'm not saying Reddit posts don't matter — organizing online has real effects. But constituent emails to swing-riding MPs in a minority Parliament are a measurably different kind of pressure. Westminster systems are weird: the PM controls the caucus, but backbenchers in close ridings do respond to constituent volume. The math shifts when a riding was decided by 300 votes.

I built civicengagement.ca for exactly this. Enter your address → your MP, MPP, city councillor, everyone who represents you — with contact info and a built-in email tool.

No account. No signup. Free. Open source. ~$40/yr to run.

If you've been wanting to do something beyond posting — this is one of the low-friction options.

Data via OpenNorth / Nord Ouvert.

---

### NDP-1 — r/NDP
**Title:** NDP leadership race ends March 29. Whoever wins, constituent contact infrastructure matters — here's a free tool.

**Body:**
Leadership votes March 29. New leader inherits a caucus that needs to punch above its seat count in a minority Parliament.

One thing that doesn't get enough attention: constituent contact capacity. Individual MPs respond to constituent pressure — especially in close ridings, especially in a minority. That's where NDP seats tend to be.

I built civicengagement.ca to make it easier for ordinary people to contact any of their elected officials — federal, provincial, municipal. Enter an address, get your reps, draft an email. No account, no signup.

This isn't partisan — the tool works for everyone regardless of which rep you're contacting. But NDP voters have historically been better at organizing than electorally converting that energy. A tool that lowers friction for constituent contact seems relevant.

Free. Open source. Data via OpenNorth / Nord Ouvert.

Anyone working on NDP digital organizing should know about the Represent API — it's what this is built on.

---

### HOUS-1 — r/canadahousing
**Title:** Zoning decisions happen at city council. Here's a free tool to find your councillor and actually contact them.

**Body:**
Federal housing policy gets most of the attention here. But zoning bylaws, development charges, secondary suite rules, and official plan amendments all happen at city council.

Most people in this sub know more about federal housing policy than they know who their city councillor is.

I built civicengagement.ca because that gap bothers me. Enter any Canadian address:

- Instant list of your city councillor, regional councillor, MPP, and MP
- Their email, phone, offices
- Built-in email drafting (you write it, the tool formats and sends)
- Ward boundary map so you know exactly who covers your area
- Burlington residents get council meeting summaries (expanding to other cities)

No account, no signup, no tracking. Free. Open source.

October 2026 Ontario municipal elections are coming up. Now is the time to know who your councillor is and what they've been doing.

Data from OpenNorth / Nord Ouvert's Represent API.

---

### TOR-1 — r/toronto
**Title:** Scarborough Southwest and University—Rosedale vote April 13. Here's a free tool to find your reps and contact them.

**Body:**
Two Toronto ridings are in the April 13 federal by-elections. University—Rosedale is a Liberal hold that would give Carney his majority. Scarborough Southwest is a +35 Liberal riding.

But your MP, MPP, city councillor, and school board trustee exist right now regardless of by-election timing.

I built civicengagement.ca for exactly this. Enter a Toronto address and you get:

- Everyone who represents you at city, provincial, and federal level
- Contact info for all of them (email, phone, office)
- Ward boundary map
- Federal voting records via OpenParliament.ca
- Built-in email drafting tool

No account. No signup. No data collected. Free and open source.

Toronto is a good test case because the ward structure is complicated — a lot of people don't know if they're in Ward 9 or Ward 10, which councillor covers them, or who their school board trustee is. The tool handles that.

Data from OpenNorth / Nord Ouvert. Feedback welcome — Toronto data is complex and I want to know if anything is wrong.

---

### HN-1 — Hacker News Show HN
**Title:** Show HN: CivicConnect – enter a Canadian address, get every elected rep with contact info and email drafting

**Body:**
civicengagement.ca

Built after Google deprecated its Civic Information API last April and a bunch of civic tools broke. Canada never had great coverage from it anyway, but it was what people were wired to.

Stack: single-file vanilla HTML/CSS/JS, no build step, no framework. Leaflet for maps, Geoapify for geocoding (behind a Cloudflare Worker proxy so the key isn't exposed), Represent API from OpenNorth for rep data and ward boundaries, OpenParliament.ca for federal voting records, Wikipedia REST API for bios.

Meeting summaries are a separate pipeline: GitHub Actions cron, Playwright scraper, pdfplumber, Claude API for summarization. Currently Burlington-only. JSON committed to the repo, fetched at runtime.

The frontend AI (email drafting via Claude) is disabled pending funding. The email tool is manual for now. Backend scraper still uses Claude via GitHub Secret.

Hosted on GitHub Pages. ~$40 USD/yr total.

Obvious limitations: Represent API data can lag after redistribution cycles — it's volunteer-maintained. Meeting scraper is brittle (PDF parsing always is). US support would require a completely different data layer.

Source: github.com/wetmud/CivicConnect

Happy to discuss the architecture or the data layer. The Represent API is genuinely underappreciated for what it is.

---

### MAST-1 — Mastodon

**Post 1:**
Built a free Canadian civic engagement tool: civicengagement.ca

Enter any address → every elected rep at city/provincial/federal level, with contact info and email drafting. Ward boundary map, MP voting records, nearby services.

No account, no tracking, no ads. ~$40/yr, open source.

Built on @opennorth's Represent API — which is excellent and under-credited.

April 13 federal by-elections in 24 days. Good time to know who your MP is.

github.com/wetmud/CivicConnect

#civictech #canada #opendata

**Post 2 (follow-up, 3 days later):**
Burlington friends: civicengagement.ca now auto-summarizes city council meetings. Scraper pulls the eSCRIBE PDFs, Claude summarizes, JSON committed to the repo and rendered on the site.

October 2026 municipal election is coming. Might be worth knowing what's been happening at council.

Still expanding to other cities — Toronto is next.

#burlington #civictech #opendata

---

### TW-1 — Twitter/X Thread

**Tweet 1:** Google killed its Civic Information API last April. A bunch of civic tools broke quietly. I built the Canadian replacement: civicengagement.ca 🧵

**Tweet 2:** Enter any Canadian address → instant list of every elected official. City councillor. Regional councillor. MPP. Federal MP. Emails, phones, offices, social links.

**Tweet 3:** Click any rep → full profile. Wikipedia bio pulled automatically. Office locations. Social links. Federal MPs: voting record pulled from @OpenParliament.

**Tweet 4:** Ward boundary map. Not just "here's who your councillor is" — the actual geographic boundary on a map. Useful when a rezoning is near you and you want to know whose ward it's in.

**Tweet 5:** Burlington residents: council meeting summaries. Auto-scraper pulls eSCRIBE PDFs every Tuesday, Claude summarizes, JSON committed to the repo. Expanding to other cities — Toronto is next.

**Tweet 6:** The stack: Single-file vanilla HTML/CSS/JS. No build step. Leaflet for maps. Geoapify behind a Cloudflare Worker. Represent API from @opennorth — the actual foundation. OpenParliament.ca for voting records. GitHub Pages, ~$40/yr.

**Tweet 7:** No account. No signup. No tracking. No ads. ~$40/yr in hosting. Ko-fi supported. April 13 by-elections in 24 days. Terrebonne is a toss-up. Know who your MP is: civicengagement.ca — source: github.com/wetmud/CivicConnect

---

### LI-1 — LinkedIn (Civic Tech Professionals)
**Headline:** I rebuilt Canada's civic information layer after Google deprecated its API. Here's what I learned.

**Body:**
Last April, Google deprecated its Civic Information API. For Canadian civic tools, it was never the primary source — OpenNorth's Represent API was — but it was the integration point for a lot of projects. When it died, several tools quietly broke with no public replacement.

I spent the last few months building civicengagement.ca as a direct response.

The product: enter any Canadian address and get every elected official at city, provincial, and federal level — with contact info, ward boundary maps, rep profiles with Wikipedia bios, federal voting records, nearby public services, and email drafting tools.

The stack is intentionally minimal: single-file HTML/CSS/JS, no build step, no framework, no backend. The entire civic data layer runs on OpenNorth / Nord Ouvert's Represent API. Federal voting records via OpenParliament.ca.

There's also a meeting summarization pipeline: GitHub Actions cron scrapes Burlington council meeting PDFs weekly, Claude summarizes them, and the JSON gets committed to the repo and fetched at runtime.

A few things I'd flag for anyone building in this space:

1. The Represent API is volunteer-maintained and can lag post-redistribution. Credit them, contribute data if you find gaps.
2. Browser-direct Claude API calls require `anthropic-dangerous-direct-browser-access: true` and a BYOK pattern if you're not running a backend.
3. Single-file architecture is the right constraint for a solo project at this scale. Build steps and frameworks are leverage debt.

The whole thing runs for ~$40 CAD/yr. Hosted on GitHub Pages, Cloudflare for the API proxy.

Source: github.com/wetmud/CivicConnect

Happy to connect with anyone building Canadian civic tech or working in open government data.

---

### LI-2 — LinkedIn (Public Policy / Academic)
**Headline:** Constituent contact tools and political behavior research — what the evidence says and a free tool that tries to act on it

**Body:**
Bergan and Cole (2015, Political Behavior) ran a randomized field experiment on constituent contact and found approximately a 12-percentage-point increase in legislator support. The effect is smaller in Westminster systems with strong party discipline — but minority governments, marginal ridings, and policy areas where backbenchers have room to deviate are real exceptions.

Canada has all three right now: a minority Parliament, a by-election in a riding that was decided by one vote (Terrebonne), and a trade policy crisis that backbenchers in border ridings have independent reason to respond to.

The gap between political intent and constituent contact is largely logistical. Most Canadians can't quickly name their MP, let alone their MPP and city councillor.

civicengagement.ca is a free tool that addresses that gap. Enter a Canadian address, get every elected official at every level, with contact info and built-in email drafting.

I'm not aware of solid Canadian data on email-to-phone ratios for legislative offices, or how volume thresholds affect staffer response protocols at the federal vs. provincial level. If anyone is researching this, I'd genuinely like to know — and would consider making the tool available for field research.

Free, open source, no tracking, no account required. Data via OpenNorth / Nord Ouvert.

---

### LI-3 — LinkedIn (Municipal Staff / City Planners)
**Headline:** A free tool for constituent contact at the city level — with ward boundary maps and council meeting summaries

**Body:**
I work in civic tech and I've been surprised by how difficult it is for ordinary residents to answer three basic questions:

1. Who is my city councillor?
2. What is their email address?
3. What has council been doing lately?

civicengagement.ca answers all three. Enter any Canadian address and get your city councillor, regional councillor, MPP, and MP — with contact info, a ward boundary map, and an email drafting tool.

For Burlington specifically, the tool publishes auto-summarized council meeting notes — scraped from eSCRIBE PDFs, summarized by Claude, and committed to a public GitHub repository. The data is open: github.com/wetmud/CivicConnect/meetings/burlington/

A few things for municipal staff or communications teams:

- Ward boundary data comes from OpenNorth / Nord Ouvert's Represent API. If you notice a boundary error, filing an issue with OpenNorth is the right path.
- Meeting summaries are AI-generated and explicitly labeled as such. They're meant to reduce friction for residents, not replace official minutes.
- The tool is free and open source. If your municipality wants to be added to the meeting summary pipeline, I'd welcome a conversation.

Expanding beyond Burlington in 2026. Toronto is next. October 2026 municipal elections make this timing relevant.

---

### CT-1 — Civic Tech Toronto Slack
**Channel:** #projects or #general

**Message:**
Hey all — I've been building a Canadian civic engagement tool and it's at a point I'm comfortable sharing: civicengagement.ca

Enter any address → every elected rep at city/provincial/federal level, with contact info and email drafting. Ward boundary maps, MP voting records via OpenParliament, Burlington council meeting summaries (GitHub Actions + Claude pipeline).

Stack is single-file vanilla HTML/CSS/JS + Represent API from OpenNorth — no build step, no framework. ~$40/yr to run.

April 13 by-elections are in 24 days, which feels like the right time to share this.

Would genuinely value feedback from people who know this space better than I do — especially on data quality and anything I'm missing about the Ontario/federal context. Happy to present at a meetup if there's interest.

Source: github.com/wetmud/CivicConnect

---

### FU-1 — Post-April 13 Follow-up
**⚠ Draft night of April 13 once results are in. Do not post before results.**

**Title:** April 13 results: Terrebonne watch, majority status, and — a reminder that your MP exists year-round

**Body structure:**
- 1-2 sentences on actual results (Terrebonne outcome, majority/minority status)
- Brief note on what the result means for the next Parliament
- Pivot: by-elections end, Parliament continues, constituent contact doesn't stop being relevant
- Short re-mention of civicengagement.ca — "if you used the tool in the lead-up to April 13, it still works"
- No hard sell. Let the political moment do the work.

**Key:** If Terrebonne flips or is contested again, that's the story. Lead with it.

---

## 4. Platform-Specific Notes

### Reddit — Universal Rules
- Never post a link without substantial body text
- One account, real engagement — vote and comment in subs before posting
- Reply to every comment within the first 2 hours
- Do not cross-post the same copy — every post above is differentiated
- Use "I" not "we"

| Subreddit | Optimal post time |
|-----------|------------------|
| r/burlington | Weekday morning 8-10am ET |
| r/civictech | Weekday morning |
| r/ontario | Monday–Wednesday morning |
| r/onguardforthee | Anytime — very active |
| r/canada | **Sunday evening or weekday morning** |
| r/canadianpolitics | Weekday morning |
| r/toronto | Weekday morning |
| r/NDP | Anytime through Mar 29 |
| r/canadahousing | Any day |

**Before posting anywhere:** Read the sidebar rules. Check if self-promotion requires flair or mod approval.

### Hacker News
- Post Saturday morning (7-9am Pacific) or weekday morning
- Title must start with "Show HN:"
- Make sure GitHub README is updated and repo is clean before posting
- Respond to early comments fast — HN front page half-life is ~4 hours
- Acknowledge limitations, don't be defensive

### LinkedIn
- Post as yourself, not a company page
- Tuesday/Wednesday 8-10am are peak windows
- Use line breaks aggressively — walls of text get scrolled
- Tag OpenNorth / Nord Ouvert if they have a LinkedIn presence

### Twitter/X
- Post all thread tweets within a few minutes of each other
- Tag @OpenNorth (verify current handle first)
- #civictech and #canada — no hashtag stuffing

### Mastodon
- Find OpenNorth's actual Mastodon handle before tagging
- 500-char limit per post
- #civictech #canada #opendata

### Civic Tech Toronto Slack
- **Most valuable single post in the plan**
- Post here FIRST — if there are bugs, you want to know before 500 visitors
- If someone asks you to present at a meetup: say yes

---

## 5. Response Playbook

### "This is spam / self-promotion"
> Fair concern. I'm the person who built it — one dev, ~$40/yr, no company behind it. I posted because [subreddit] is the right audience. Happy to answer any questions about how it works. If it's not useful, downvote it.

### "The data is wrong / my rep isn't listed"
> Thanks for catching that. The rep data comes from OpenNorth / Nord Ouvert's Represent API — they're the authoritative source. Filing an issue with them at github.com/opennorth/represent-canada-data gets it fixed for everyone. I'll note it on my end too.

### "What about [other province / city]?"
> The core tool works everywhere in Canada — address → reps → email is national. Meeting summaries are Burlington-only for now; Toronto is next. If you want to see your city added, drop me a note or open a GitHub issue.

### "Why not use [existing tool]?"
> If there's a better tool for this I genuinely want to know about it. [Engage seriously.] The gap I was solving: Google deprecated its Civic Info API, and most Canadian tools don't cover all three levels in one lookup.

### "The meetings feature doesn't work / is empty"
> Burlington council meeting summaries are live. Other cities aren't in the pipeline yet — the scraper is city-specific and Burlington was first. Toronto is next. Happy to hear which city you'd want added.

### "Is this secure? Are you selling my data?"
> No account, no login, no data stored. The address goes to Geoapify for geocoding (via a Cloudflare Worker proxy) and to the Represent API for rep lookup. Neither stores your address under my account. No analytics script on the page. CSP headers are in the source if you want to verify.

### "Open source? Where's the code?"
> github.com/wetmud/CivicConnect — it's all there. Single HTML file, meeting scraper in /scripts, GitHub Actions in .github/workflows.

### Positive comments / "this is great"
Don't just say thank you. Ask:
- "Which part was most useful for you?"
- "Did anything not work or seem off?"
- "Is there a feature that would make you actually use this regularly?"

### Someone with a large following engages
Respond within 15 minutes. Be direct, not fawning. Offer to answer technical questions or hop on a call if they're building something.

---

## 6. Success Metrics

### What to track
- **Cloudflare Analytics:** Unique visitors/day, top referrers, geographic distribution, mobile vs desktop
- **GitHub Insights > Traffic:** Unique clones, views, stars over time
- **Reddit:** Upvote ratio, comment count, link clicks
- **Ko-fi:** Number of supporters, total raised

### Milestones
- **Week 1 (Mar 20-27):** Civic Tech Toronto engagement, 20+ upvotes on r/civictech, 200+ unique visitors
- **Weeks 2-3 (Mar 28 – Apr 10):** At least one post crosses 100 upvotes, 1,000+ total visitors, 2+ people report using the email tool
- **April 13 window:** 500+ visitors on peak day
- **End of April:** 5,000+ total visitors, 50+ GitHub stars, 3+ Ko-fi supporters, at least one Civic Tech Toronto meetup conversation

### Warning signs
- Multiple posts removed by mods → re-read sidebar rules, reduce link prominence
- Zero HN engagement → not a signal, HN is high variance; move on
- Data complaints dominating → add UI note linking to Represent API issue tracker
- Crash / API errors reported → check Cloudflare Worker logs and Geoapify quota

---

## 7. Post-April 13 Follow-Up Plan

### April 14-15
Post FU-1. Frame as: by-elections over, Parliament continues, constituent contact is year-round.

### April 14-30
- **Burlington October election:** Frame the tool as election-prep infrastructure. Post in r/burlington with council meeting summaries as "here's what your councillors have been doing."
- **Scraper stability:** If 3+ clean weekly runs confirmed, post a brief r/civictech update on the pipeline.
- **Toronto expansion:** Mention it in Burlington/civictech follow-up posts to give people a reason to return.

### May–September 2026 (municipal election ramp)
- Repost in r/ontario and r/burlington with municipal election framing
- LinkedIn post targeting Burlington community organizations
- Reach out to Burlington Public Library or Burlington Community Foundation — both have community outreach channels

### Things to watch for
- **NDP new leader (March 29):** If they run a "contact your MP" campaign, engage publicly and offer the tool as infrastructure
- **Federal budget (spring 2026):** Budget reactions drive constituent contact spikes — have a post ready
- **Terrebonne news after April 13:** If close again or contested, another posting moment

---

## Execution Checklist

Before posting anything:

- [ ] Verify civicengagement.ca loads cleanly on mobile
- [ ] Confirm Feb 17 Burlington meeting summary renders in the UI (not just in JSON)
- [ ] Check og:image displays when URL is pasted in Slack or iMessage
- [ ] Confirm GitHub repo is public and README is current
- [ ] Read sidebar rules for r/burlington and r/civictech
- [ ] **Post to Civic Tech Toronto Slack FIRST — before any Reddit posts**
- [ ] Have GitHub repo URL and Ko-fi URL ready to paste in comments

---

**Total posts: 19** (including follow-up and CT Slack). Every post is written in full. Execute in calendar order.
