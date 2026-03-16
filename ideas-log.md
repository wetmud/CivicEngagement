# 💡 Ideas Log
*Captured from our session — Feb 2026*

---

## Built ✅

### CivicConnect
A free civic tool for Canadians. Enter your address, instantly find every elected official who represents you — city councillor, regional rep, MPP — and contact them directly with AI-drafted emails. Includes nearby public services (libraries, parks, hospitals, schools), an interactive ward boundary map, and a profile card showing your address and district. No account. No data collected. Ever.

**Live at:** `wetmud.github.io/CivicConnect`

**Future features already scoped:**
- Federal representatives tab (code already saved in comments, ready to enable)
- Response tracking — log when you sent an email and whether your rep replied. Over time this becomes public accountability data: "your MPP responds to 34% of constituent emails, average 12 days." Requires a small backend database (Supabase). Powerful enough that journalists and political opponents would notice it.
- US version — straightforward swap of the Represent API for Google Civic Information API, covers all 50 states, free tier available, roughly an afternoon of work
- Community issue surfacing — neighbours independently reporting the same pothole shows up as a signal, turning one frustrated person into a pattern a councillor can't ignore
- Organizer tools — bulk coordinated messaging for advocacy groups and local campaigns
- PWA (Progressive Web App) — 20 lines of code converts the site into an installable home screen app on any phone, no app store needed
- QR code sticker campaign — physical stickers placed in context (broken bench, pothole, busted bus shelter) linking directly to CivicConnect. The context does the selling.

**Exit potential:** Municipal governments and civic organizations in Canada actively seek engagement tools they can't build internally. Path: real users → media/grant attention → municipal pilot → licensing or acquisition. OpenNorth (the team behind the Represent API we use) followed a similar trajectory.

---

## Strong Candidates 🔥

### WorkerShield (name TBD)
A civic-style tool for Canadian workers. Input your province and job type, instantly understand your legal rights — minimum wage, break entitlements, overtime rules, termination rights, what your employer can and cannot do. Designed for the moment something has already gone wrong and you need to confirm whether it was legal.

**Why it matters:** Labour law is public information but practically inaccessible. Most workers don't know their rights until they've already been violated. Dangerous job environments (warehouse, gig, construction) make this especially urgent.

**Origin:** Personal — laid off from warehouse work. Built from lived experience, not research.

**The mechanic:** Same DNA as CivicConnect. Simple input → scrape/surface the relevant regulation → take action. "You work in Ontario as a warehouse worker. Here are your rights: X, Y, Z. Here's what to do if your employer does A or B."

**Canada-first reasoning:** Simpler regulatory landscape to start, province-by-province coverage is manageable, and Employment Standards Acts are public and well-structured. US version possible later but labour law varies enormously by state.

**Could include:**
- Incident documentation tool — log a workplace issue with timestamp, description, witness names. Creates a paper trail before you need one.
- Know-your-rights summaries by province, updated when legislation changes
- "Is this legal?" prompt — describe what happened, get a plain-language assessment
- Links to the right reporting body (Ontario Labour Relations Board, ESA claims, etc.)

---

## Parked Ideas 🗂️

### Independent Zine & Art Book Marketplace
A dedicated marketplace for small-run printed work — zines, art books, risograph prints, chapbooks. Etsy is too generic, Instagram is too algorithmic, there's no purpose-built home for this community.

**Why it's interesting:** The publishing and design background here is a genuine insider advantage. You'd understand the community, the pricing norms, the aesthetic, and what sellers actually need.

**Why it's parked:** Cold-start problem — you need supply and demand simultaneously. A community problem as much as a product problem. Better as a second or third project once you have some momentum and maybe a community from CivicConnect.

**Could differentiate with:** Edition tracking, print run documentation, artist provenance, filterable by format/technique/region.

---

### Artist Pricing Tool
A tool to help visual artists price their work with confidence. Aggregates comparable sales data, accounts for materials and time, outputs a defensible price range. Solves one of the most emotionally painful parts of being an artist.

**Why it's interesting:** Pricing is where most artists undersell themselves, and the problem is universal across mediums.

**Why it's parked:** Data sourcing is hard — comparable sales data isn't centralized anywhere clean. Would need a strategy for where the data comes from before the product makes sense.

---

### Second-Hand Marketplace with Serious Filters
A niche resale platform with genuinely good filter functionality — not Facebook Marketplace's mess, not eBay's outdated UI. A focused vertical (art supplies, cameras, design equipment, music gear) where filters are built around how that community actually shops.

**Why it's interesting:** The filtering problem is real. Every existing platform treats search as an afterthought.

**Why it's parked:** Competitive space, hard logistics, needs a very specific niche to have a shot.

---

## Rejected (with notes) ❌

**Anonymous messaging app** — technically and legally complex. Encryption, infrastructure, compliance. Not a first project.

**Artist social network / Pinterest for artists** — crowded. Behance, Dribbble, ArtStation, Are.na all exist. The exclusive community angle is interesting but the cold-start problem is brutal.

**AI price comparison scraper** — basically Google Shopping now. Hard to differentiate.

**Political social media** — moderation is a nightmare, competing with Reddit/Nextdoor/Facebook Groups. Better as a CivicConnect feature (candidate directory, local positions) than a standalone product.

---

## The Pattern Worth Noticing

The ideas that feel most alive — CivicConnect and WorkerShield — share the same structure:

> *Someone is in a moment of friction or injustice. They need information they're entitled to but can't easily access. The tool surfaces it in under 60 seconds and tells them what to do next.*

That's a product philosophy worth naming. It's not about engagement or growth hacking. It's about reducing the distance between a person and the power they already have.

---

---

## To-Do Notes

### CivicConnect
- [ ] Rewrite the About page in your own voice — make it sound like a person wrote it, not a product description. Should feel genuine and explain why you built it.

### Personal Site
- [ ] **Root/tree visual idea** — explore a scrolling background where you're travelling down through the root system of a tree or plant. As you scroll the page, the roots grow/extend downward. Could be SVG animation or canvas. Distinctive, organic, fits the "growth" metaphor. Revisit this when working on the personal site.
- [ ] **Install algorithmic-art skill** from https://github.com/travisvn/awesome-claude-skills when starting personal site work — useful for the root animation.

### Claude / Workflow Setup
- [ ] **Per-project Claude personas** — add a Tone & Personality section to each repo's CLAUDE.md so Claude behaves differently per project. CivicConnect = civic tech builder voice. Personal site = designer/creative voice. Future projects = whatever fits (marketing, product, etc.). As projects get more complex, could have sub-personas per folder (marketing, HR, dev).
- [ ] **Learn more about Claude agents** — understand how agents work so we can set up smarter multi-agent workflows across projects.

---

---

## Canadian House of the People (CivicConnect Phase 2)

Inspired by houseofthepeople.com — UK direct democracy platform. Build the Canadian equivalent as a natural extension of CivicConnect.

**What maps to Canada:**
- Bills → LEGISinfo API (free, Parliament's official bill tracker) ✅
- MP voting records → OpenParliament.ca (already using) ✅
- MPs directory → Represent API (already using) ✅
- Senate → OpenParliament has Senate data ✅
- Laws → Justice Laws website (no clean API, scraping needed) ⚠️
- Community polls + gap tracker → needs Supabase backend ❌ (Phase 3)

**Strategy:** Build this as CivicConnect Phase 2, not a separate project. The foundation (rep lookup, ward map, email drafting) is already there.

**Action item:** Reach out to House of the People founder before building — @HoTPOfficial on X, LinkedIn. Civic tech people share. He might collaborate, share API knowledge, or at minimum appreciate the heads up. Canada ≠ competition.

---

*Next session: buy civicengagement.ca + wire up custom domain in Cloudflare, or WorkerShield v1 scoping?*
