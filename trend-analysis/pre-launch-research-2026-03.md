# CivicConnect — Pre-Launch Research
**Generated:** 2026-03-20
**For:** April 6-10 posting push

---

## 1. Constituent Contact Moves Votes — Citations

### Primary Citation (use this one)

**Bergan, D.E. & Cole, R.L. (2015). "Call Your Legislator: A Field Experimental Study of the Impact of a Constituency Mobilization Campaign on Legislative Voting." *Political Behavior*, 37(1).**

- https://link.springer.com/article/10.1007/s11109-014-9277-1
- LSE summary: https://blogs.lse.ac.uk/usappblog/2015/04/29/constituent-contacts-can-influence-how-legislators-vote/

**Design:** Randomized field experiment. Michigan state legislators were assigned to receive constituent phone calls (22, 33, or 65 calls) or none during a campaign to pass anti-bullying legislation (2011).

**Key finding:** Being targeted by constituent calls increased probability of supporting the bill by **~12 percentage points**, independent of party, gender, or district competitiveness.

**Quotable:** "Legislators who received at least one phone call from a constituent asking them to support a certain bill were 11–12 percent more likely to support the legislation."

---

### Supporting Citation (email-specific)

**Bergan, D.E. (2009). "Does Grassroots Lobbying Work? A Field Experimental Test of the Effectiveness of E-mail Lobbying." *American Politics Research*, 37(2).**

- https://journals.sagepub.com/doi/10.1177/1532673X08326967

Randomized 143 New Hampshire state legislators. Found substantial influence on legislative voting behavior from email lobbying campaigns. Establishes email causality specifically.

---

### Canadian-Specific Context

**"Can citizen pressure influence politicians' communication about climate change?" *Climatic Change* (2021)**
- https://pmc.ncbi.nlm.nih.gov/articles/PMC8445256/

Tested constituent influence on Canadian MPs. Key honest caveat: **Westminster party discipline compresses the effect** — a successful campaign may only sway 1–2 of 338 MP votes. This doesn't negate the effect; it means riding-specific contact in marginals matters most.

**Canadian audit study (service responsiveness):**
- https://www.cambridge.org/core/journals/canadian-journal-of-political-science/article/service-responsiveness-to-minority-constituents/57D897D1BEA228E0AA94ED6F71CF9800
Confirms MPs respond differentially to constituent contacts in casework responsiveness.

---

### Practitioner Heuristic

**Congressional Management Foundation (non-partisan):** Legislative staffers report one constituent letter is perceived as representing ~10 constituents who didn't write. Personalized messages consistently outperform form emails.

---

### How to Use This in Posts

Lead with the Bergan & Cole finding — randomized experiment, peer-reviewed, ~12pp effect. Note for Canadian context: party discipline compresses it, but minority governments with tight riding margins are exactly where constituent contact matters most. The April 13 ridings (especially Terrebonne — a genuine toss-up) are the specific case.

---

## 2. April 13, 2026 By-Elections

Called by PM Carney on March 8, 2026. Nominations closed March 23.

Sources: CBC News | Elections Canada (elections.ca)

---

### Scarborough Southwest (Toronto, ON)

**Why vacant:** Liberal MP **Bill Blair** resigned to become Canada's High Commissioner to the UK.

**Liberal candidate:** **Doly Begum** — former Ontario NDP MPP and Deputy Leader. Resigned her provincial seat Feb 3, 2026. Her defection drew NDP criticism ("breeds cynicism in our politics" — Don Davies).

**Other candidates:** Fatima Shaban (NDP), Diana Filipova (CPC — middle school teacher), Pooja Malhotra (Green), Lyall Sanders (Centrist)

**Local issues:** Affordable housing, public transit, community safety.

**Polling (Mainstreet Research, March 2026, n=464):** Liberal 57%, Conservative 22%, NDP 15%. Strong Liberal lead — not competitive.

**Notable:** Simultaneous Ontario *provincial* by-election in the same riding (triggered by Begum's own provincial resignation).

Sources: Wikipedia | Beach Metro | Mainstreet Research | CP24

---

### University—Rosedale (Toronto, ON)

**Why vacant:** Liberal MP **Chrystia Freeland** resigned Jan 5, 2026 to become unpaid economic adviser to Ukrainian President Zelenskyy. Conservatives raised ethics concerns.

**Liberal candidate:** **Dr. Danielle Martin** — family physician, chair of Dept of Family and Community Medicine at U of T, former VP at Women's College Hospital. Known nationally for defending Canadian public healthcare before a US Senate committee in 2014.

**Other candidates:** Serena Purdy (NDP — community organizer, Kensington Market), Don Hodgson (CPC), Andrew Massey (Green), Adam Golding (Independent — electoral reform focus)

**Local issues:** Healthcare (Martin's natural terrain), housing affordability, electoral reform.

**Strategic importance:** A Liberal win here brings the party to **172 seats — the minimum for a majority**. This is why Carney is running a high-profile candidate.

Sources: Wikipedia | CBC | TorontoToday | Provincial Times

---

### Terrebonne (Quebec)

**Why vacant:** Court-ordered rematch. In the 2025 federal election, Liberal **Tatiana Auguste** won by **literally one vote** in a judicial recount. Bloc candidate **Nathalie Sinclair-Desgagné** challenged the result — a printing error on a mail-in ballot return envelope caused a validly cast Bloc vote to be returned undelivered. On **Feb 13, 2026, the Supreme Court of Canada annulled the result** and ordered a by-election.

**Candidates:** Tatiana Auguste (Liberal), Nathalie Sinclair-Desgagné (Bloc), Adrienne Charles (CPC), Benjamin Rankin (Green), Maxime Beaudoin (NDP), Maria Cantore (PPC)

**Local issues:**
- High-speed rail routing (Alto HSR) — potential property expropriations
- Cost of living, seniors' support, first-time homebuyers (Bloc platform)
- Federal representation / riding access to government (Auguste platform)

**Drama:** The Longest Ballot Committee is targeting this by-election with protest candidates.

**This is the only genuinely competitive riding.** Liaison Strategies (March 2026): "virtual locks for the Liberals" in both Toronto ridings; Terrebonne is "a genuine toss-up." 338Canada rates it highly competitive.

Sources: Wikipedia | CBC | Globe and Mail | CP24

---

### Riding Summary for Posts

| Riding | Competitive? | Best angle |
|--------|-------------|------------|
| Scarborough Southwest | No (Liberal +35) | Dual federal/provincial election happening simultaneously |
| University—Rosedale | No (safe Liberal) | Liberal majority hinges on this seat |
| Terrebonne | **Yes — toss-up** | Won by 1 vote in 2025, Supreme Court rematch — most dramatic story |

---

## 3. OpenNorth / Represent API Status

### Organization: Active

OpenNorth (opennorth.ca) is a Montreal-based not-for-profit, founded 2011. Website updated August 2025. Still active, recruiting, taking on projects.

- Website: opennorth.ca
- GitHub: github.com/opennorth
- Twitter: @opennorth (exists but **not actively monitored** — use email)
- Email: represent@opennorth.ca
- Bilingual name: **Open North / Nord Ouvert**

### API: Live, but data may be stale

The Represent API at represent.opennorth.ca is **live and returning data**. No deprecation notice found.

**Important caveat:** The `represent-canada-data` GitHub repo shows some boundary files last updated **2017-08-23** — these predate the 2022–2023 federal electoral redistribution that took effect for the 2025 election. **Riding boundaries and MP data may be stale.** Worth running a live postcode query to verify accuracy before relying on it in production or making claims about it in posts.

### GitHub Activity

Repos: `represent-canada`, `represent-canada-data`, `represent-reps`, `represent-postcodes`, `represent-boundaries`

Status: **Stable/low-touch** — maintained but not actively developed. No fork, handoff, or deprecation announcement found.

### How to Reference in r/civictech Post

- Credit as: Open North / Nord Ouvert
- Link: represent.opennorth.ca
- Tag: @opennorth (low engagement expected)
- Be transparent about the data staleness risk — it shows you've done due diligence and will read as credible to a technical audience
- Ask in the post if anyone knows the current maintenance status — good community discussion hook

Sources: opennorth.ca | github.com/opennorth | represent.opennorth.ca | OpenNorth LinkedIn
