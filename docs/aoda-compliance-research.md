# AODA Compliance Research — Council Meeting Captions
**Date:** 2026-03-19
**Context:** Sent email to Burlington City Clerk (clerks@burlington.ca) on 2026-03-18 asking whether Burlington produces transcripts or captions for council meetings. Received response from Lisa Palermo (Manager, Committee Services/Deputy Clerk) stating they do not produce transcripts and have no plans to offer them.

---

## The Legal Question

Does Burlington have a legal obligation under AODA to provide captions for archived council meeting videos posted on their website?

**Short answer: Yes.**

---

## Governing Law

**Ontario Regulation 191/11** — Integrated Accessibility Standards Regulation (IASR), Section 14: Accessible Websites and Web Content.

All designated public sector organizations (which includes every Ontario municipality) must ensure their websites and web content conform to **WCAG 2.0 Level AA**.

**Deadlines:**
- January 1, 2014 — New websites and new content must meet WCAG 2.0 Level A
- **January 1, 2021 — All websites and all content must meet WCAG 2.0 Level AA** (with two carve-outs)

The 2021 deadline has passed. Burlington is a large municipality — no grace period applies.

---

## The Specific Requirement That Applies

**WCAG 2.0 Success Criterion 1.2.2 — Captions (Prerecorded) — Level A**

> "Captions are provided for all prerecorded audio content in synchronized media."

In plain English: if you post a video with audio to your website, it must have captions.

Burlington posts archived council meeting videos to their website. Those videos are "prerecorded synchronized media." WCAG 1.2.2 requires captions.

**This is a Level A requirement** — it's the baseline, not even the full Level AA bar. It is not one of the two exceptions IASR carved out (those are: live captions [1.2.4] and audio descriptions for prerecorded video [1.2.5]). There is no exception that removes the 1.2.2 obligation.

### The two IASR exceptions — what's NOT required:
| WCAG Criterion | Level | Status under IASR |
|---|---|---|
| 1.2.4 Captions (Live) | AA | **Exempted** — live streams don't need captions |
| 1.2.5 Audio Description (Prerecorded) | AA | **Exempted** — audio descriptions not required |

### What IS required:
| WCAG Criterion | Level | Status |
|---|---|---|
| 1.2.2 Captions (Prerecorded) | **A** | **Required** — no exception |

---

## What Burlington's Response Actually Means

Lisa Palermo's response: *"We do not produce transcripts of any of our standing committee or council meetings. Decisions of Council are captured in the meeting minutes and the meeting discussions can be viewed via archived videos on the city's website."*

She confirmed:
- Burlington posts meeting videos on their website ✓
- They do not provide captions or transcripts ✓

That combination is a WCAG 1.2.2 violation under IASR Section 14. She may not have understood the question as being about AODA compliance — the original email asked about transcripts, not specifically about captioning obligations. She may also be unaware of the legal requirement (this is a clerk, not an accessibility officer).

The response was not a legal position — it was a procedural one.

---

## Precedent: Other Ontario Municipalities

This is a known, widespread problem across Ontario. Multiple municipalities have explicitly grappled with the WCAG 1.2.2 obligation:

**Town of Goderich:** Staff recommended stopping posting videos to the website because of WCAG captioning obligations. Cited cost. The municipality acknowledged the legal obligation was real.

**Municipality of Bluewater:** Council voted unanimously to stop posting recorded meetings online and switch to livestream-only, explicitly to avoid AODA captioning requirements. Clerk cited professional captioning costs of ~$15,000/year. Existing YouTube videos would need to be removed. Livestream is exempt (WCAG 1.2.4 is one of the two IASR exceptions).

**Pattern:** Municipalities know about the obligation. Many are responding by pulling videos offline rather than captioning them — legally defensible, but terrible for transparency and democratic access.

Burlington has not done this — they still post videos uncaptioned — which makes their current situation non-compliant.

---

## Enforcement Reality

Enforcement under AODA is weak:
- Complaints go to the Ontario Accessibility Directorate of Ontario (ADO)
- Since 2017, only ~45 enforcement orders have been issued province-wide
- Maximum $100,000/day penalty has never been applied
- System relies almost entirely on self-reporting

That said: **the legal obligation is clear and unambiguous.** The enforcement gap doesn't change what's required.

Key advocacy: AODA Alliance (David Lepofsky) has publicly documented widespread municipal non-compliance and inadequate enforcement.

File a complaint: https://www.ontario.ca/page/file-accessibility-complaint

---

## Burlington's Accessibility Infrastructure

- Burlington has a Multi-Year Accessibility Plan (required under AODA)
- Burlington has an Accessibility Advisory Committee (required for municipalities over 10,000 population)
- Burlington posts to their Accessibility page at burlington.ca
- **Burlington uses eSCRIBE + iSiLIVE for meeting streaming** — iSiLIVE has built-in .vtt caption infrastructure per meeting, but Burlington does not populate those files (both return 404). This means the technical path to compliance is already in place — Burlington just isn't using it.

---

## Technical Note: The Caption Infrastructure Exists

eSCRIBE (Burlington's meeting portal software) already checks for captions at:
```
https://video.isilive.ca/.../meeting_id.vtt
```
That URL returns 404 for Burlington — not because the capability doesn't exist, but because Burlington hasn't populated the files. The system is built for this. Burlington is paying for software that supports captioning and not using that feature.

---

## Recommended Follow-Up Email

See below. Tone: informative, not confrontational. Goal: get the right person (Accessibility Officer, not Clerk) looking at this, and frame our tool as a resource toward compliance.

---

## Draft Follow-Up Email to Burlington

**To:** clerks@burlington.ca (Lisa Palermo / Committee Services)
**CC:** Consider adding Burlington's Accessibility contact if findable
**Subject:** Re: Request for Council Meeting Captions or Transcriptions — AODA Compliance Question

---

Good morning Lisa,

Thank you for the prompt response. I appreciate you clarifying Burlington's current practice.

I want to flag something I don't think was fully addressed in my original email — not to be difficult, but because I think it's worth getting to the right team.

Under Ontario's Integrated Accessibility Standards Regulation (O. Reg. 191/11, Section 14), public sector organizations are required to ensure web content conforms to WCAG 2.0 Level AA. The compliance deadline for large organizations was January 1, 2021.

WCAG 2.0 Success Criterion 1.2.2 (Level A) requires captions for pre-recorded synchronized media — which is the category that archived council meeting videos fall into. This is distinct from the two exceptions IASR carves out (live captions and audio descriptions), neither of which covers archived recordings.

If Burlington's archived council meeting videos are posted on the city website without captions, that would appear to be a WCAG 1.2.2 compliance gap under IASR Section 14.

I'm not raising this as a complaint — I'm raising it because a few other Ontario municipalities (Goderich, Bluewater) have recently dealt with exactly this issue, and I thought Burlington's Accessibility team might want to be aware of it if they aren't already.

A few things I noticed that may be useful for your team:

1. Burlington's meeting portal (eSCRIBE via iSiLIVE) has built-in infrastructure for .vtt caption files — the endpoint exists but currently returns 404 for Burlington's meetings. The technical path may already be partially in place.

2. As part of the civic engagement tool I'm building (civicengagement.ca), I've already transcribed at least one Burlington council meeting using local speech-to-text tools. I'd be happy to share that output or collaborate in any way that helps Burlington move toward compliance.

Could you point me to the right person on Burlington's accessibility team? I want to make sure this lands with whoever is responsible for the Multi-Year Accessibility Plan.

Thank you,
Jason Steltman
civicengagement.ca

---

## Sources

- [O. Reg. 191/11 — IASR full text (CanLII)](https://www.canlii.org/en/on/laws/regu/o-reg-191-11/latest/o-reg-191-11.html)
- [WCAG 2.0 SC 1.2.2 — Captions (Prerecorded)](https://www.w3.org/TR/UNDERSTANDING-WCAG20/media-equiv-captions.html)
- [Bluewater decides against captioning recorded council meetings — AODA.ca](https://aoda.ca/bluewater-decides-against-captioning-recorded-council-meetings/)
- [Goderich — providing closed captioning too costly, suggests town staff — AODA.ca](https://aoda.ca/providing-closed-captioning-on-council-meetings-too-costly-suggests-town-staff/)
- [Burlington — Accessibility Legislation in Ontario](https://www.burlington.ca/en/community-supports/accessibility-legislation-in-ontario.aspx)
- [Burlington — Multi-Year Accessibility Plan](https://www.burlington.ca/en/council-and-city-administration/multi-year-accessibility-plan.aspx)
- [File an AODA accessibility complaint](https://www.ontario.ca/page/file-accessibility-complaint)
- [AODA enforcement overview — CBC (2023)](https://www.cbc.ca/news/canada/toronto/aoda-ontario-accessibility-2025-1.7053136)
