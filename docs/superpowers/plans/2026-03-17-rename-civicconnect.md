# Rename CivicConnect → Civic Engagement Implementation Plan

> **For agentic workers:** REQUIRED: Use superpowers:subagent-driven-development (if subagents available) or superpowers:executing-plans to implement this plan.

**Goal:** Rename all user-facing and code references from "CivicConnect" to "Civic Engagement" (and GitHub repo from `CivicConnect` to `CivicEngagement`). The proxy worker URL (`civicconnect-proxy`) is out of scope — it stays as-is.

**Architecture:** Text/config changes only. No logic changes. Single-file app (`index.html`) plus `manifest.json`, `README.md`, `CLAUDE.md`.

**Tech Stack:** Find-and-replace across 4 files + GitHub repo rename + git remote update.

---

## File Map

| File | What changes |
|------|-------------|
| `index.html` | Title, OG tags, Twitter tags, logo text, privacy text, about section, support modal, GitHub URLs, tweet hashtag |
| `manifest.json` | Already correct — `name` is "Civic Engagement", `short_name` is "CivicEngage". **No changes needed.** |
| `README.md` | Title, badge URLs, live URL, clone URL, issue links, body text |
| `CLAUDE.md` | Title line, live URL, scraper User-Agent mention |

---

## Chunk 1: index.html — Head Section (meta tags)

**Files:** `index.html` (lines 1–40)

- [ ] **Step 1: Update `<title>` tag (line 18)**

Find:
```html
<title>CivicConnect — Know Who Represents You</title>
```
Replace:
```html
<title>Civic Engagement — Know Who Represents You</title>
```

- [ ] **Step 2: Update `og:url` (line 31)**

Find:
```html
<meta property="og:url" content="https://civicconnect.jason-steltman.workers.dev/" />
```
Replace:
```html
<meta property="og:url" content="https://civicengagement.ca/" />
```

- [ ] **Step 3: Update `og:title` (line 32)**

Find:
```html
<meta property="og:title" content="CivicConnect — Know Who Represents You" />
```
Replace:
```html
<meta property="og:title" content="Civic Engagement — Know Who Represents You" />
```

- [ ] **Step 4: Update `twitter:title` (line 37)**

Find:
```html
<meta name="twitter:title" content="CivicConnect — Know Who Represents You" />
```
Replace:
```html
<meta name="twitter:title" content="Civic Engagement — Know Who Represents You" />
```

- [ ] **Step 5: Verify — DO NOT touch line 13 (CSP)**

Line 13 references `civicconnect-proxy.jason-steltman.workers.dev` in the CSP `connect-src`. This is the proxy worker URL and must stay as-is.

---

## Chunk 2: index.html — Body (logo, privacy, about, support, footer)

**Files:** `index.html` (lines 1700–2100)

- [ ] **Step 1: Update logo text (line 1730)**

Find:
```html
<span class="logo">CivicConnect</span>
```
Replace:
```html
<span class="logo">Civic Engagement</span>
```

- [ ] **Step 2: Update privacy text (line 1745)**

Find:
```
CivicConnect collects <strong>zero data</strong> about you.
```
Replace:
```
Civic Engagement collects <strong>zero data</strong> about you.
```

- [ ] **Step 3: Update about heading (line 1869)**

Find:
```html
<h2>About <em>CivicConnect</em></h2>
```
Replace:
```html
<h2>About <em>Civic Engagement</em></h2>
```

- [ ] **Step 4: Update about body text (line 1873)**

Find:
```
I built CivicConnect because I got tired of not knowing who actually represents me.
```
Replace:
```
I built Civic Engagement because I got tired of not knowing who actually represents me.
```

- [ ] **Step 5: Update support modal text (line 1909)**

Find:
```
CivicConnect is different — it is free, open-source, and built for everyone.
```
Replace:
```
Civic Engagement is different — it is free, open-source, and built for everyone.
```

---

## Chunk 3: index.html — GitHub URLs

**Files:** `index.html` (lines 1820–3710)

All GitHub URLs change from `wetmud/CivicConnect` to `wetmud/CivicEngagement`. Do a global find-and-replace:

Find: `wetmud/CivicConnect`
Replace: `wetmud/CivicEngagement`

This covers all 6 occurrences:
- [ ] Line 1820: budget footer issue link
- [ ] Line 1886: GitHub repo link in about section
- [ ] Line 1888: bug report link in about section
- [ ] Line 1903: recommend feature link in about section
- [ ] Line 1973: recommend feature link in support modal
- [ ] Line 2033: recommend feature link in footer
- [ ] Line 3707: budget city request issue link

- [ ] **Verify:** After replace, grep `index.html` for `wetmud/CivicConnect` — should return 0 results.

---

## Chunk 4: index.html — Tweet Hashtag

**Files:** `index.html` (line 2489)

- [ ] **Step 1: Update meeting share hashtag**

Find:
```js
'#Burlington #CivicConnect'
```
Replace:
```js
'#Burlington #CivicEngagement'
```

---

## Chunk 5: index.html — DO NOT touch (proxy worker URL)

These references stay as-is — they are functional code pointing to the live proxy:
- Line 13: CSP `connect-src` — `civicconnect-proxy.jason-steltman.workers.dev`
- Line 2112: `const WORKER_URL = 'https://civicconnect-proxy.jason-steltman.workers.dev';`

**No action required.**

---

## Chunk 6: README.md — Full Update

**Files:** `README.md`

- [ ] **Step 1: Update title**

Find:
```
# CivicConnect
```
Replace:
```
# Civic Engagement
```

- [ ] **Step 2: Update badge URLs**

Find:
```
[![Live](https://img.shields.io/badge/live-civicconnect.jason--steltman.workers.dev-blue)](https://civicconnect.jason-steltman.workers.dev)
```
Replace:
```
[![Live](https://img.shields.io/badge/live-civicengagement.ca-blue)](https://civicengagement.ca)
```

- [ ] **Step 3: Update "Try It Live" section**

Find:
```
**[civicconnect.jason-steltman.workers.dev](https://civicconnect.jason-steltman.workers.dev)**

Custom domain coming: `civicengagement.ca`
```
Replace:
```
**[civicengagement.ca](https://civicengagement.ca)**
```

- [ ] **Step 4: Update clone URL**

Find:
```
git clone https://github.com/wetmud/CivicConnect.git
cd CivicConnect
```
Replace:
```
git clone https://github.com/wetmud/CivicEngagement.git
cd CivicEngagement
```

- [ ] **Step 5: Update issue link at bottom**

Find:
```
[Open an issue](https://github.com/wetmud/CivicConnect/issues)
```
Replace:
```
[Open an issue](https://github.com/wetmud/CivicEngagement/issues)
```

- [ ] **Step 6: Leave proxy worker mention in "How It Works" as-is** — it references `civicconnect-proxy` which is a functional URL.

---

## Chunk 7: CLAUDE.md — Project Header and References

**Files:** `CLAUDE.md`

- [ ] **Step 1: Update title line**

Find:
```
# CivicConnect — CLAUDE.md
```
Replace:
```
# Civic Engagement — CLAUDE.md
```

- [ ] **Step 2: Update live URL line**

Find:
```
**Live:** `civicconnect.jason-steltman.workers.dev`
```
Replace:
```
**Live:** `civicengagement.ca`
```

- [ ] **Step 3: Update scraper User-Agent mention (line 205)**

Find:
```
`User-Agent: CivicConnect/1.0`
```
Replace:
```
`User-Agent: CivicEngagement/1.0`
```

- [ ] **Step 4: Leave all `civicconnect-proxy` references as-is** — functional URLs.

---

## Chunk 8: Scraper User-Agent in Python

**Files:** `scripts/scrape_burlington.py`

- [ ] **Step 1: Check for User-Agent string**

Grep `scrape_burlington.py` for `CivicConnect`. If found, update to `CivicEngagement`.

Find:
```python
CivicConnect/1.0
```
Replace:
```python
CivicEngagement/1.0
```

---

## Chunk 9: GitHub Repo Rename + Git Remote

**This chunk must run AFTER all file edits are committed.**

- [ ] **Step 1: Commit all file changes**

```bash
git add index.html README.md CLAUDE.md scripts/scrape_burlington.py
git commit -m "Rename CivicConnect to Civic Engagement"
```

- [ ] **Step 2: Rename the GitHub repo**

Go to `https://github.com/wetmud/CivicConnect/settings` → Repository name → change to `CivicEngagement` → click Rename.

Alternatively via CLI:
```bash
gh repo rename CivicEngagement
```

- [ ] **Step 3: Update local git remote**

```bash
git remote set-url origin https://github.com/wetmud/CivicEngagement.git
```

- [ ] **Step 4: Push**

```bash
git push
```

- [ ] **Step 5: Verify** — visit `https://github.com/wetmud/CivicEngagement` and confirm it loads. Old URL should auto-redirect.

---

## Chunk 10: Root CLAUDE.md (parent directory)

**Files:** `/Users/macintosh/Documents/GitHub/CLAUDE.md`

- [ ] **Step 1: Update project table row**

The active projects table references `CivicConnect` — update the project name column. The `Location` column (`./CivicConnect/`) will change when the local folder is renamed.

- [ ] **Step 2: Update to-do section headers**

Find all `### CivicConnect` headings and update to `### Civic Engagement`.

- [ ] **Step 3: Update any body text** mentioning "CivicConnect" in the to-do items (e.g., "CivicConnect grants" in grant-tracker item). Leave "House of the People" section references to "Civic Engagement" as they already use that term.

---

## Verification Checklist

After all chunks are done:

- [ ] `grep -ri "CivicConnect" index.html` returns only the CSP line (13) and WORKER_URL line (2112) — both are proxy URLs that stay
- [ ] `grep -ri "CivicConnect" README.md` returns only the proxy worker mention in "How It Works"
- [ ] `grep -ri "CivicConnect" CLAUDE.md` returns only proxy-related references
- [ ] `manifest.json` already says "Civic Engagement" — no changes needed, confirm unchanged
- [ ] Open `index.html` in browser: logo says "Civic Engagement", about section reads naturally, all GitHub links point to `wetmud/CivicEngagement`
- [ ] `git remote -v` shows `wetmud/CivicEngagement.git`

---

## Low Priority / Nice-to-Have (NOT part of this plan)

- **Rename proxy worker** from `civicconnect-proxy` to `civicengagement-proxy` on Cloudflare. Requires creating a new Worker, migrating secrets, updating CSP + `WORKER_URL` in index.html, and testing. Do this separately when there's time — the old URL will keep working indefinitely.
- **Rename local folder** from `CivicConnect/` to `CivicEngagement/` — optional, affects all path references in root `CLAUDE.md` and memory files.
