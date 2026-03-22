# CivicConnect — Full Launch Plan
**Assembled:** 2026-03-22
**Process:** Multi-agent roundtable — Growth Hacker 🚀, Paid Social Strategist 📱, Social Media Strategist 📣, SEO Specialist 🔍, facilitated by Agents Orchestrator 🎛️
**Source material:** `pre-launch-research-2026-03.md`, `reddit-launch-2026-03.md`, `social-media-launch-plan-2026-03.md`, `social-strategy-review-2026-03.md`

---

## 🎛️ ORCHESTRATOR: Session Brief

> We have four weeks of quality research sitting in the trend-analysis folder. Social strategy is drafted, post copy exists, timing is mapped. What we don't have is a unified launch plan that accounts for all channels, growth mechanics beyond social, and a longer arc past April 13. Each of you owns your lane. I'll enforce the agenda and surface gaps. Let's start with a synthesis, move to disagreements, then produce a single executable plan. No passengers.

**Agenda:**
1. What the research got right
2. Gaps and disagreements
3. The full plan — phased, cross-channel
4. Agent handoffs and what still needs to be built

---

## ROUND 1: What the Research Got Right

---

### 🚀 GROWTH HACKER

The research correctly identified the North Star moment: **three by-elections on April 13, a toss-up riding (Terrebonne), and a minority government 3 seats from a majority.** That's not just a content hook — it's a **conversion trigger**. People don't just want to read about Terrebonne. They want to feel like they can affect it. CivicConnect is the "do something now" button.

The Google Civic Info API shutdown framing for r/civictech is strong. That's a **narrative of necessity** — not "I built a cool thing" but "a vacuum existed and I filled it." That story travels.

What I'm adding to the record: the research treats traffic as the goal. **Traffic is not the goal.** The goal is a user who enters an address, lands on their rep list, and sends an email. That's the activation event. Every channel should be measured against that funnel completion, not just clicks.

**North Star Metric I'm proposing:** Email drafts initiated (proxy: time-on-page + interaction with email modal). Track via Cloudflare Analytics + any client-side event you can log without a backend.

---

### 📱 PAID SOCIAL STRATEGIST

I want to flag something the existing research doesn't: **zero paid budget is a choice, not a given.** Jason's running this for $40/yr. That's a constraint, not a law. A $50–100 CAD Meta campaign targeting Canadians interested in politics, civic engagement, or "elections" during the April 6-13 window would buy real impressions in Terrebonne-adjacent Quebec ridings.

That said — I agree the organic-first approach is correct *for now.* The r/canada and r/canadianpolitics posts have the potential to spike 5,000+ impressions for free if timed right. Paid amplification makes sense **after** you've identified which organic message converts best.

My read on the paid window: **April 8-12** — three days before the by-elections. Boost the winning Reddit post as a dark Meta ad. Target: Canada, age 25-55, interest in Canadian politics. Objective: traffic. Budget: $50 CAD. That's not nothing. That's a real test.

For LinkedIn: the three differentiated posts (civic tech professionals, academics, municipal staff) are well-scoped. LinkedIn Sponsored Content would amplify the civic tech / academic posts for $30-50 CAD. **Municipal staff targeting by job title is a LinkedIn superpower** — this is where the meeting summaries feature gets its most receptive audience.

---

### 📣 SOCIAL MEDIA STRATEGIST

The research got the tone right: first person, acknowledge limitations, credit OpenNorth. That's the only voice that doesn't get flagged as spam on r/canada. The voice rules in the plan are worth preserving in full.

The sequencing is solid — Civic Tech Toronto first, r/burlington second, escalate to r/canada and r/canadianpolitics the week of April 6. I'd make one change: **post to Mastodon on the same day as r/civictech**, not after. The civic tech Mastodon community is the same audience and they read each other's feeds. Double coverage for zero extra effort.

The biggest miss in the existing plan: **no X/Twitter thread is actually scheduled in the calendar.** It's written (TW-1 is excellent) but the calendar shows "Tue Mar 25" with no follow-through on the 7-tweet thread timing. It needs a hard schedule.

What I'm adding: **a repost cadence**. The research treats each post as single-use. The r/burlington post, the r/civictech post, and the best-performing r/canada post should all get a **second run in September 2026** when Burlington's October municipal election is 30 days out. The by-election angle dies April 14. The municipal election angle is a second life.

---

### 🔍 SEO SPECIALIST

I want to start with what nobody in this folder has addressed: **civicengagement.ca has zero organic search presence right now.** The site is a single HTML file on GitHub Pages. No sitemap, almost certainly no structured data, no `robots.txt`, and the content is all dynamic (rendered via JavaScript) which means Google's indexing of the rep lookups is minimal.

The existing plan is entirely **push marketing** — going to where audiences already are and announcing the product. That's correct for launch. But it ignores the pull opportunity.

**What Canadians search for right now:**
- "Who is my MP [city]" — navigational, high intent
- "How to contact my MPP Ontario" — instructional, conversion-ready
- "Burlington city council meeting minutes" — local, underserved
- "Find my city councillor Canada" — direct product match

These are not high-volume queries (thousands/month, not millions). But the person searching "how do I contact my MP" is already activated. CivicConnect is the answer. The site just isn't showing up.

**My immediate recommendations:**
1. Add a `sitemap.xml` and `robots.txt` to the repo root
2. Add `<title>` and `<meta description>` that include the words "find your MP Canada" and "contact your city councillor"
3. Add structured data (`WebApplication` schema + `FAQPage` for the most common how-to questions) via a `<script type="application/ld+json">` block in the `<head>`
4. After launch push, write 3-5 static informational pages (can be part of the single HTML file as distinct `<section>` elements) targeting the top queries — OR add a simple `/about` static page on GitHub Pages with SEO-optimized copy

The Burlington meeting summaries are a **linkable asset** that nobody is treating as one. A page titled "Burlington City Council Meeting Summaries (2026)" with the actual summaries rendered as readable HTML (not just a JSON fetch) would rank for "Burlington city council 2026" and similar local queries within 60-90 days. That's inbound traffic that doesn't require being awake at the right time to catch a Reddit cycle.

---

## 🎛️ ORCHESTRATOR: Gap Check

> Before we build the plan, I'm surfacing three disagreements:
>
> 1. **Growth Hacker says measure email draft initiations. Current plan measures upvotes and GitHub stars.** We need to pick primary metrics before we execute.
> 2. **Paid Social Strategist is proposing $50-100 in paid spend. The project runs on $40/yr.** Does Jason have budget for a test? We need to flag this as a decision point.
> 3. **SEO Specialist is recommending structural changes to index.html (title, meta, structured data).** This is a product change, not a marketing change. It needs to be scoped separately.
>
> We'll note these as decisions for Jason. The plan proceeds with both paths where needed.

---

## ROUND 2: Disagreements and Resolutions

---

### 🚀 GROWTH HACKER: On metrics

Upvotes and GitHub stars are **vanity metrics** at this stage. They feel good. They don't tell you if the product is working. My proposal: treat the launch as a **growth experiment with a hypothesis**.

**Hypothesis:** CivicConnect gets meaningful first-use traffic by riding the April 13 by-election news cycle on Reddit, with conversion measured by time-on-page and email tool interaction.

**Control:** Cloudflare Analytics for sessions, referrer breakdown, bounce rate. No new tooling required.

**Success definition (revised):**

| Metric | Minimum | Good | Great |
|--------|---------|------|-------|
| Sessions (April 6-14 window) | 500 | 2,000 | 5,000+ |
| Avg. time on page | >2 min | >3 min | >4 min |
| GitHub stars | 10 | 40 | 100+ |
| Ko-fi supporters | 1 | 5 | 15+ |
| Email modal opens (self-reported in comments) | any | 5 | 20+ |
| Civic Tech Toronto response | mentioned | replied | demo invited |

The email modal metric is soft — we can't track it without a backend. But reading comment threads for "I used it to email my MP" is a signal. Seed the conversation by asking in your Reddit replies: "Did you end up using the email tool?"

---

### 📱 PAID SOCIAL STRATEGIST: On budget

I'll soften the ask. If $50 CAD is not available:

**Free paid-equivalent tactics:**
- Share the winning Reddit post to your own Facebook/Instagram stories. Most Canadian civic tech adjacent people on your list will share it. Small but real.
- If any post crosses 200 upvotes organically, screenshot it and post it on LinkedIn with the caption "apparently this resonated." Social proof compounds.
- After April 13, if Terrebonne has a dramatic outcome (close again, contested), write a tight 200-word post: "The riding that was decided by one vote just voted again. Here's how to contact your rep before the next one." That's a press hook. **Send it to CBC Digital, TVO, The Narwhal.** Small civic tech stories are their beat.

**If $50 CAD is available:** Run the Meta test April 8-12. Target: Canada, "Canadian politics" interest, age 25-54. Creative: screenshot of the site with the copy "Three by-elections. One toss-up riding. Find your MP in 30 seconds." Objective: traffic. $10/day, 5 days, monitor and kill if CPC exceeds $0.50.

---

### 🔍 SEO SPECIALIST: On product changes vs. marketing

I'll scope this to three changes that can be made in under an hour to `index.html` and don't require a separate file:

1. **`<title>` tag:** Change to `CivicConnect — Find Your MP, MPP & City Councillor | civicengagement.ca`
2. **`<meta name="description">`:** `Free Canadian civic tool. Enter your address to find every elected official who represents you — MP, MPP, and city councillor — and email them directly. No signup required.`
3. **Structured data:** Add a `WebApplication` schema block in `<head>` with `name`, `description`, `url`, `applicationCategory: "GovernmentApplication"`, and `offers.price: "0"`.

These three changes are **pure SEO** with no visible impact on the site. They take 15 minutes. The SEO payoff is 60-90 days out — by Burlington's October election, the site will be appearing in "find city councillor Burlington" queries.

The meeting summaries SEO play is a Phase 2 item — requires rendering the Burlington JSON as static HTML. I'll flag it for the roadmap.

---

### 📣 SOCIAL MEDIA STRATEGIST: On the repost cadence

Here's the full two-wave plan I'm proposing:

**Wave 1 (March 20 – April 14): By-election launch**
Execute the existing calendar. By-election angle dies April 14.

**Wave 2 (September 1-15, 2026): Municipal election ramp**
Reposts with rewritten intros for the municipal angle. The r/burlington post becomes: "Burlington's October election is in 6 weeks. Here's a free tool with council meeting summaries from the past year." The r/ontario post becomes about municipal elections, not Ford. Fresh angle, same tool, no rebuilding.

This doubles the campaign's effective life for nearly zero additional work.

---

## 🎛️ ORCHESTRATOR: Assembling the Plan

> Good. We have consensus on: prioritized metrics, a conditional paid test, 3 SEO quick wins, and a two-wave campaign structure. Building the unified plan now.

---

## THE FULL LAUNCH PLAN

---

### PHASE 0: Pre-Launch Checklist (Before any post goes live)

**Owned by:** Jason
**Deadline:** Before March 24

- [ ] `<title>` tag updated: `CivicConnect — Find Your MP, MPP & City Councillor | civicengagement.ca`
- [ ] `<meta name="description">` updated (see SEO rec above)
- [ ] Add `WebApplication` structured data to `<head>` (15 min)
- [ ] Verify civicengagement.ca loads cleanly on mobile (iPhone + Android browser)
- [ ] Confirm Feb 17 Burlington meeting summary renders in the UI (not just JSON)
- [ ] Check `og:image` displays when URL is pasted in Slack or iMessage
- [ ] Confirm GitHub repo is public and README is current
- [ ] Read sidebar rules for r/burlington and r/civictech before posting
- [ ] Have GitHub repo URL and Ko-fi URL ready to paste in comments
- [ ] Add `sitemap.xml` to repo root listing `https://civicengagement.ca/` (single URL is fine for now)
- [ ] Add `robots.txt` to repo root (`User-agent: * / Allow: /`)

---

### PHASE 1: Soft Launch — Community & Credibility (March 24-31)

**Primary channel:** Civic Tech Toronto → r/civictech → r/burlington
**Goal:** Early feedback, bug surface, first 200 visitors

| Date | Platform | Post | Notes |
|------|----------|------|-------|
| Mon Mar 24 | Civic Tech Toronto Slack | CT-1 | Post here FIRST. Read every reply within 2 hours. If someone finds a bug, fix it before Reddit. |
| Mon Mar 24 | Mastodon (infosec.exchange + social.coop) | MAST-1 | Same day as Civic Tech — same audience, different feed |
| Tue Mar 25 | Twitter/X | TW-1 (7-tweet thread) | Post all tweets within 10 minutes. Tag @OpenNorth. |
| Wed Mar 26 | Reddit | r/civictech (POST 4 REVISED) | Technical audience. Lead with Google API shutdown. |
| Mon Mar 31 | Reddit | r/burlington (POST 3 REVISED) | Local angle with council meeting summaries. Confirm Feb 17 renders first. |

**Success gate to advance to Phase 2:**
- No critical bugs reported
- At least one substantive reply on r/civictech
- Civic Tech Toronto response (any form)

---

### PHASE 2: Pre-Election Push (March 31 – April 5)

**Primary channel:** r/ontario, r/onguardforthee, r/NDP, LinkedIn
**Goal:** Audience warming before the by-election window

| Date | Platform | Post | Notes |
|------|----------|------|-------|
| Mon Mar 31 | Reddit | r/ontario (ONT-1) | Ford majority / ER closures angle |
| Mon Mar 31 | Reddit | r/onguardforthee (OGF-1) | Elbows Up angle — highest upside miss per strategy review |
| Tue Apr 1 | Reddit | r/NDP (NDP-1) | Leadership race ends Mar 29 — pivot to post-leadership angle |
| Tue Apr 1 | LinkedIn | LI-1 (civic tech professionals) | Architecture + Google API shutdown |
| Wed Apr 2 | LinkedIn | LI-2 (public policy / academics) | Research angle, Bergan & Cole citation |
| Thu Apr 3 | Reddit | r/canadahousing (HOUS-1) | Zoning / city council angle |
| Thu Apr 3 | LinkedIn | LI-3 (municipal staff) | Meeting summaries + October election |
| Thu Apr 3 | Hacker News | HN-1 (Show HN) | Saturday morning preferred — reschedule to Apr 5 if possible |

**Drop comments (not posts) in active r/canada and r/canadianpolitics by-election threads all week to build karma and presence before the main posts.**

---

### PHASE 3: By-Election Window — Main Push (April 6-14)

**Primary channel:** r/canada, r/canadianpolitics, r/toronto, Meta (conditional)
**Goal:** Peak traffic, email tool activations, mainstream civic awareness

| Date | Platform | Post | Notes |
|------|----------|------|-------|
| Sun Apr 6 | Reddit | r/canada (POST 1 REVISED) | Sunday evening 7-9pm ET — peak Canadian Reddit traffic |
| Mon Apr 7 | Reddit | r/canadianpolitics (POST 5 REVISED) | Trade war / elbows up angle. Same day as r/canada is fine — content is differentiated. |
| Tue Apr 8 | Reddit | r/toronto (TOR-1) | Scarborough Southwest + University-Rosedale angle |
| **Apr 8-12** | **Meta Ads (conditional)** | **$50 CAD test** | Only if budget exists. Boost the best-performing Reddit post. Target: Canada, politics interest, 25-54. Kill if CPC > $0.50. |
| Wed Apr 9 | LinkedIn | Reshare best LI post with by-election context added | Single line added to top: "Three federal ridings vote in 4 days." |
| Fri Apr 11 | Reddit | r/Terrebonne or r/Quebec (if active) | French-language by-election post — "La circonscription décidée par un vote vote à nouveau." Jason writes this or skips if uncomfortable with French. |

**Election night (Apr 13):**
- Watch Terrebonne results live
- Draft FU-1 the moment results are called
- If close or contested: post within 30 minutes of result

| Date | Platform | Post | Notes |
|------|----------|------|-------|
| Mon Apr 14 | Reddit | r/canada or r/canadianpolitics (FU-1) | Results + pivot to year-round constituent contact |
| Mon Apr 14 | Twitter/X | TW-2 | By-election results thread — Terrebonne result as hook |

---

### PHASE 4: Post-Election Consolidation (April 14-30)

**Goal:** Convert traffic spike into sustained awareness, set up Wave 2

- **April 14-20:** Reply to all remaining comments across all posts. Personal, specific replies only — no copy-paste.
- **April 15:** Post brief r/civictech update if scraper is stable: "Built a Playwright → pdfplumber → Claude pipeline for Burlington council PDFs — here's what I learned." Technical community appreciates this and it generates backlinks.
- **April 17-20:** Send cold (not spam) emails to two organizations:
  - **Civic Tech Toronto meetup organizers** — offer to present at a May meetup
  - **The Narwhal or TVO** — one-paragraph pitch: "I built the Canadian replacement for Google's deprecated Civic Info API and it got used during the April 13 by-elections. Happy to talk." No deck required.
- **April 21-30:** Begin scoping Toronto meeting summaries feature. Announce on r/civictech that Toronto is next.

---

### PHASE 5: Municipal Election Ramp — Wave 2 (September 1-15, 2026)

**Goal:** Second life for all content ahead of October 2026 Ontario municipal elections

**Repost plan (entirely rewritten intros, same tools, municipal framing):**

| Date | Platform | Original Post | New Angle |
|------|----------|---------------|-----------|
| Tue Sep 1 | Reddit | r/burlington (POST 3) | "Burlington's October election is 7 weeks away. Here's a year of council meeting summaries." |
| Wed Sep 2 | Reddit | r/ontario | Municipal elections across Ontario in October. Find your councillor, see what they've been doing. |
| Mon Sep 7 | LinkedIn | LI-3 revisit | Municipal election angle for community organizations and municipal staff |
| Tue Sep 8 | Reddit | r/canadahousing | Local zoning decisions: your city councillor matters more than your MP right now |
| Mon Sep 14 | Reddit | r/burlington (second post) | "October 27 is in 6 weeks — Burlington council candidates and how to reach your current councillor" |

---

## AGENT HANDOFF MAP

The following additional agents from The Agency should be engaged as phases proceed:

| Phase | Trigger | Agent | Task |
|-------|---------|-------|------|
| Phase 0 | Pre-launch | **Reddit Community Builder** | Review sidebar rules for all target subreddits, identify recent by-election threads to comment in before main posts |
| Phase 1 | After CT-Toronto response | **Content Creator** | Refine the French-language Terrebonne post (r/Quebec) if CT feedback surfaces Quebec audiences |
| Phase 2 | After LI-1 response | **LinkedIn Content Creator** | If civic tech professionals engage, build a longer LinkedIn article from the architecture post |
| Phase 3 | If Meta test is approved | **Paid Social Strategist (active execution)** | Set up and monitor the $50 Meta campaign. Kill decision at 48 hours. |
| Phase 4 | After April 14 results | **Analytics Reporter** | Pull Cloudflare Analytics, GitHub traffic, Ko-fi data — produce a one-page results summary for the next wave |
| Phase 4 | If Civic Tech Toronto invites a demo | **Social Media Strategist** | Prep a 10-minute demo script. The audience is technical and civic-minded. Lead with the architecture, close with the email tool. |
| Phase 5 | August 2026 | **Growth Hacker (second session)** | Revisit North Star metrics from Wave 1. Identify what converted and double down for the municipal election cycle. |

---

## DECISIONS FOR JASON

Three items that need a yes/no before execution begins:

1. **Paid Media test (April 8-12): Yes or No?**
   Budget needed: $50 CAD. If yes, set up a Meta Business account and boosting pixel before April 6.

2. **French-language Terrebonne post: Yes or No?**
   If Jason isn't comfortable writing in French, skip it. Don't post machine-translated copy to a Quebec community.

3. **SEO changes to `index.html`: Proceed immediately?**
   These are three meta-tag changes with no visible user impact. Recommended: do this in Phase 0 this week.

---

## SUCCESS METRICS (REVISED)

### Wave 1 (March 24 – April 14)
| Metric | Min | Good | Great |
|--------|-----|------|-------|
| Unique sessions | 500 | 2,000 | 5,000+ |
| Avg. session duration | >2 min | >3 min | >4 min |
| GitHub stars | 10 | 40 | 100+ |
| Ko-fi supporters | 1 | 5 | 15+ |
| Comment reports of email tool used | 1 | 5 | 15+ |
| Civic Tech Toronto response | mentioned | replied | demo booked |
| Press mentions | 0 | 1 | 2+ |

### Wave 2 (September 2026)
| Metric | Min | Good | Great |
|--------|-----|------|-------|
| Unique sessions (Sep 1-30) | 1,000 | 4,000 | 10,000+ |
| Organic search sessions | 50 | 200 | 500+ |
| Burlington meeting summaries views | 100 | 500 | 1,500+ |
| Toronto meeting summaries live | No | In dev | Live |

---

## WARNING SIGNS

| Sign | Response |
|------|----------|
| Posts removed by mods | Re-read sidebar rules. Reduce link prominence. Move to comment-only strategy in that sub. |
| Zero HN engagement | Expected. HN is high variance. Move on. |
| Data complaints dominate comments | Add UI note linking to Represent API issue tracker. Reply: "Thanks — filing with OpenNorth." |
| API errors reported | Check Cloudflare Worker logs and Geoapify quota. |
| Meta test CPC > $0.50 at 24 hours | Kill the campaign. The organic posts are performing better. |
| No Civic Tech Toronto response after 72 hours | Send one follow-up in-thread. If no response, treat Mastodon as the warm community instead. |

---

## 🎛️ ORCHESTRATOR: Closing Assessment

> The existing research was strong. It identified the right moment, the right voice, the right sequencing for Reddit. What was missing: a growth funnel framing (Growth Hacker added this), a paid test option with clear kill conditions (Paid Social added this), a two-wave repost strategy (Social Media added this), and SEO infrastructure that turns the launch into long-term inbound traffic (SEO added this).
>
> The plan is now executable. Phase 0 checklist takes one afternoon. The rest is calendar execution.
>
> One final note: the strongest distribution move in the entire plan is still the Civic Tech Toronto Slack post. Post there first. If it lands, everything else gets easier. If nobody responds, that's a signal — adjust the voice before Reddit.
>
> Pipeline is ready to execute. Quality gate: complete the Phase 0 checklist before any post goes live.

---

*Agents referenced: [Growth Hacker](https://github.com/msitarzewski/agency-agents/blob/main/marketing/marketing-growth-hacker.md) · [Paid Social Strategist](https://github.com/msitarzewski/agency-agents/blob/main/paid-media/paid-media-paid-social-strategist.md) · [Social Media Strategist](https://github.com/msitarzewski/agency-agents/blob/main/marketing/marketing-social-media-strategist.md) · [SEO Specialist](https://github.com/msitarzewski/agency-agents/blob/main/marketing/marketing-seo-specialist.md) · [Agents Orchestrator](https://github.com/msitarzewski/agency-agents/blob/main/specialized/agents-orchestrator.md)*
