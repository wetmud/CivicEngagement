# Rep Profile Modal, Support Modal, Budget Comment-out & Courtesy Tip

> **For agentic workers:** REQUIRED: Use superpowers:subagent-driven-development (if subagents available) or superpowers:executing-plans to implement this plan. Steps use checkbox syntax for tracking.

**Goal:** Add a rich rep profile modal (Wikipedia bio + office info), Ko-fi support modal, comment out the budget tab, and add a courtesy communication tip below the rep list.

**Architecture:** All changes in `index.html` (single-file vanilla JS). Follow existing modal pattern: backdrop div + `.open` class toggled via JS. Wikipedia API called on modal open, results cached in `wikiCache` object. All external content sanitized via `escAttr()` before insertion into HTML attributes; Wikipedia extract is stripped of HTML tags before display.

**Tech Stack:** Vanilla HTML/CSS/JS, Wikipedia REST API (free, no key, CORS-friendly via `origin=*`), Ko-fi (external link only).

---

## Chunk 1: Budget Comment-out + Courtesy Tip

### Task 1: Comment out Budget tab

**Files:** `index.html` lines ~1329 and ~1338-1355

- [ ] Comment out the Budget tab button (line ~1329):
  Wrap `<button class="tab-btn" onclick="switchTab('budget', this)">City Budget</button>`
  in `<!-- BUDGET TAB: re-enable by removing comment ... -->`

- [ ] Comment out the entire `<div class="tab-panel" id="tab-budget">...</div>` block (lines ~1338-1355)
  in `<!-- BUDGET PANEL: re-enable by removing comment ... -->`

- [ ] Open `index.html` in browser. Verify Budget tab is gone. Local & Provincial tab still works.

- [ ] Commit: `git commit -m "chore: comment out budget tab (re-enable by removing HTML comments)"`

---

### Task 2: Courtesy Tip Bubble

**Files:** `index.html` (CSS block + `renderRepList` JS function)

- [ ] Add CSS after `.rep-actions` responsive block (~line 651):

```css
.courtesy-tip {
  margin-top: 1.5rem;
  padding: 1rem 1.25rem;
  background: var(--profile-bg);
  border-left: 3px solid var(--accent);
  border-radius: 12px;
  display: flex;
  gap: 0.75rem;
  align-items: flex-start;
}
.courtesy-tip-icon { font-size: 1.2rem; flex-shrink: 0; margin-top: 0.05rem; }
.courtesy-tip-heading {
  font-size: 0.65rem; text-transform: uppercase; letter-spacing: 0.12em;
  color: var(--accent); margin-bottom: 0.35rem;
}
.courtesy-tip-body { font-size: 0.75rem; color: var(--text-muted); line-height: 1.65; }
```

- [ ] In `renderRepList`, after the `reps.forEach` loop and before `document.getElementById(elId).innerHTML = html`, append:

```js
html += `
  <div class="courtesy-tip">
    <div class="courtesy-tip-icon">🤝</div>
    <div>
      <div class="courtesy-tip-heading">A note on civic communication</div>
      <div class="courtesy-tip-body">Representatives respond best to respectful, specific, and good-faith messages. Focus on one issue, explain your perspective clearly, and stay courteous — it is significantly more effective than frustration or demands.</div>
    </div>
  </div>`;
```

- [ ] Search a Canadian address in browser. Verify tip appears below rep cards with orange left border.

- [ ] Commit: `git commit -m "feat: add courtesy communication tip below rep list"`

---

## Chunk 2: Support Modal

### Task 3: Support modal HTML, CSS, and JS

**Files:** `index.html`

- [ ] Change header Support button (line ~1275) from `<a href="https://ko-fi.com/wetmud" ...>` to:
```html
<button class="btn-donate" onclick="openSupport()">☕ Support</button>
```

- [ ] Also update Ko-fi link in the About modal body (line ~1420) from `ko-fi.com/wetmud` to `ko-fi.com/jasonsteltman`

- [ ] Add Support modal HTML after the About modal backdrop closing tag (~line 1424):

```html
<!-- Support Modal -->
<div class="support-backdrop" id="support-backdrop" onclick="closeSupport(event)">
  <div class="support-box">
    <button class="about-close" onclick="closeSupport()">✕</button>
    <h2>Keep <em>CivicConnect</em> Free</h2>
    <div class="about-byline">Open civic tech for Canadians — no ads, no tracking</div>
    <div class="support-body">
      <p>CivicConnect costs <strong>~$0/month</strong> to run — GitHub Pages is free and AI features use your own API key. Your support helps expand coverage and keeps development going.</p>
      <div class="support-transparency">
        <div class="support-cost-row">
          <span>Hosting (GitHub Pages)</span><span class="support-cost-val">$0 / month</span>
        </div>
        <div class="support-cost-row">
          <span>AI features (BYOK — your own key)</span><span class="support-cost-val">$0 / month</span>
        </div>
        <div class="support-cost-row">
          <span>Developer time &amp; future infra</span><span class="support-cost-val">your support ☕</span>
        </div>
      </div>
      <div class="support-tiers">
        <a class="support-tier" href="https://ko-fi.com/jasonsteltman" target="_blank" rel="noopener">$5</a>
        <a class="support-tier" href="https://ko-fi.com/jasonsteltman" target="_blank" rel="noopener">$10</a>
        <a class="support-tier support-tier-featured" href="https://ko-fi.com/jasonsteltman" target="_blank" rel="noopener">$25</a>
        <a class="support-tier" href="https://ko-fi.com/jasonsteltman" target="_blank" rel="noopener">$50</a>
      </div>
    </div>
    <a class="support-cta" href="https://ko-fi.com/jasonsteltman" target="_blank" rel="noopener">☕ Support on Ko-fi →</a>
    <p style="font-size:0.65rem;color:var(--text-muted);text-align:center;margin-top:0.75rem">All amounts in CAD. Processed securely by Ko-fi.</p>
  </div>
</div>
```

- [ ] Add Support modal CSS (after `.about-links` CSS block ~line 230):

```css
.support-backdrop {
  display: none; position: fixed; inset: 0;
  background: rgba(0,0,0,0.6); backdrop-filter: blur(6px);
  z-index: 200; align-items: center; justify-content: center; padding: 1rem;
}
.support-backdrop.open { display: flex; }
.support-box {
  background: var(--surface); border: 1px solid var(--border);
  border-radius: 20px; padding: 2.5rem 2rem 2rem;
  max-width: 480px; width: 100%; position: relative;
  animation: fadeUp 0.3s ease both;
  box-shadow: 0 20px 60px rgba(0,0,0,0.4);
}
.support-box h2 { font-family: 'DM Serif Display', serif; font-size: 1.6rem; margin-bottom: 0.4rem; }
.support-box h2 em { font-style: italic; color: var(--accent); }
.support-body { margin: 1.25rem 0; }
.support-body p { font-size: 0.78rem; color: var(--text-muted); line-height: 1.7; margin-bottom: 1rem; }
.support-transparency {
  background: var(--profile-bg); border-radius: 10px; padding: 0.85rem 1rem; margin-bottom: 1.25rem;
}
.support-cost-row {
  display: flex; justify-content: space-between;
  font-size: 0.72rem; color: var(--text-muted);
  padding: 0.3rem 0; border-bottom: 1px solid var(--border);
}
.support-cost-row:last-child { border-bottom: none; }
.support-cost-val { color: var(--accent); font-weight: 500; }
.support-tiers { display: flex; gap: 0.5rem; margin-bottom: 1.25rem; justify-content: center; }
.support-tier {
  flex: 1; text-align: center; padding: 0.6rem 0;
  border: 1px solid var(--border); border-radius: 10px;
  font-family: 'DM Mono', monospace; font-size: 0.8rem; color: var(--text);
  text-decoration: none; transition: border-color 0.2s, color 0.2s, background 0.2s;
}
.support-tier:hover { border-color: var(--accent); color: var(--accent); }
.support-tier-featured {
  border-color: var(--accent); color: var(--accent);
  background: rgba(255, 185, 99, 0.08);
}
:root.light .support-tier-featured { background: rgba(104, 47, 237, 0.07); }
.support-cta {
  display: block; width: 100%; text-align: center; padding: 0.85rem;
  background: var(--accent); color: var(--on-accent);
  border-radius: 12px; font-family: 'DM Mono', monospace;
  font-size: 0.8rem; text-transform: uppercase; letter-spacing: 0.1em;
  text-decoration: none; transition: background 0.2s, box-shadow 0.2s; font-weight: 500;
}
.support-cta:hover { background: var(--accent-dim); box-shadow: 0 4px 16px rgba(255,185,99,0.35); }
:root.light .support-cta:hover { box-shadow: 0 4px 16px rgba(104,47,237,0.3); }
```

- [ ] Add JS functions near `openAbout` / `closeAbout`:

```js
function openSupport() {
  document.getElementById('support-backdrop').classList.add('open');
}
function closeSupport(e) {
  if (!e || e.target === document.getElementById('support-backdrop')) {
    document.getElementById('support-backdrop').classList.remove('open');
  }
}
```

- [ ] Find existing `keydown` Escape handler (search for `e.key === 'Escape'`). If found, add `closeSupport();` inside it. If not found, add:
```js
document.addEventListener('keydown', e => {
  if (e.key === 'Escape') { closeModal(); closeAbout(); closeSupport(); }
});
```

- [ ] Test: click Support in header — modal opens with tiers and Ko-fi CTA. Each tier/CTA opens `ko-fi.com/jasonsteltman`. Escape and backdrop click close modal.

- [ ] Commit: `git commit -m "feat: add Ko-fi support modal with cost transparency and donation tiers"`

---

## Chunk 3: Rep Profile Modal

### Task 4: Rep profile modal HTML + CSS

**Files:** `index.html`

- [ ] Add rep profile modal HTML after the Support modal closing tag:

```html
<!-- Rep Profile Modal -->
<div class="rep-profile-backdrop" id="rep-profile-backdrop" onclick="closeRepProfile(event)">
  <div class="rep-profile-box">
    <button class="about-close" onclick="closeRepProfile()">✕</button>
    <div class="rep-profile-layout">
      <div class="rep-profile-left">
        <div class="rep-profile-photo-wrap">
          <img class="rep-profile-photo" id="rpModal-photo" src="" alt="" onerror="this.parentElement.style.display='none'">
        </div>
        <div class="rep-profile-name" id="rpModal-name"></div>
        <div class="rep-profile-role" id="rpModal-role"></div>
        <div class="rep-profile-party" id="rpModal-party"></div>
        <div class="rep-profile-social" id="rpModal-social"></div>
        <div class="rep-profile-actions">
          <button class="btn-primary" id="rpModal-email-btn" onclick="rpModalWriteEmail()">✉ Write Email</button>
          <a class="btn-outline" id="rpModal-profile-link" href="#" target="_blank">↗ Official Profile</a>
        </div>
      </div>
      <div class="rep-profile-right">
        <div class="rep-profile-offices" id="rpModal-offices"></div>
        <div class="rep-profile-wiki" id="rpModal-wiki">
          <div class="rep-profile-section-label">About</div>
          <div class="rep-profile-wiki-body" id="rpModal-wiki-body"></div>
        </div>
      </div>
    </div>
  </div>
</div>
```

- [ ] Add rep profile modal CSS (after support modal CSS):

```css
.rep-profile-backdrop {
  display: none; position: fixed; inset: 0;
  background: rgba(0,0,0,0.65); backdrop-filter: blur(8px);
  z-index: 200; align-items: center; justify-content: center; padding: 1rem;
}
.rep-profile-backdrop.open { display: flex; }
.rep-profile-box {
  background: var(--surface); border: 1px solid var(--border);
  border-radius: 20px; padding: 2rem; max-width: 820px; width: 100%;
  max-height: 90vh; overflow-y: auto; position: relative;
  animation: fadeUp 0.3s ease both;
  box-shadow: 0 24px 64px rgba(0,0,0,0.45);
}
.rep-profile-layout { display: flex; gap: 2rem; align-items: flex-start; }
.rep-profile-left {
  width: 200px; flex-shrink: 0;
  display: flex; flex-direction: column; align-items: center; text-align: center;
}
.rep-profile-photo-wrap { margin-bottom: 1rem; }
.rep-profile-photo {
  width: 110px; height: 110px; border-radius: 50%;
  object-fit: cover; object-position: center 15%;
  border: 3px solid var(--accent); display: block;
  box-shadow: 0 0 0 5px rgba(255,185,99,0.15), 0 10px 30px rgba(0,0,0,0.4);
}
:root.light .rep-profile-photo {
  box-shadow: 0 0 0 5px rgba(104,47,237,0.12), 0 10px 30px rgba(0,0,0,0.15);
}
.rep-profile-name { font-family: 'DM Serif Display', serif; font-size: 1.25rem; margin-bottom: 0.25rem; line-height: 1.2; }
.rep-profile-role { font-size: 0.72rem; color: var(--text-muted); margin-bottom: 0.5rem; line-height: 1.4; }
.rep-profile-party {
  font-size: 0.65rem; text-transform: uppercase; letter-spacing: 0.1em;
  background: rgba(255,185,99,0.12); border: 1px solid rgba(255,185,99,0.25);
  border-radius: 20px; padding: 0.2rem 0.75rem; color: var(--accent);
  margin-bottom: 0.9rem; display: inline-block;
}
:root.light .rep-profile-party { background: rgba(104,47,237,0.08); border-color: rgba(104,47,237,0.2); }
.rep-profile-social { display: flex; flex-wrap: wrap; justify-content: center; gap: 0.35rem; margin-bottom: 1rem; }
.rep-profile-social a {
  font-size: 0.62rem; color: var(--text-muted); text-decoration: none;
  border: 1px solid var(--border); border-radius: 20px; padding: 0.18rem 0.55rem;
  transition: color 0.2s, border-color 0.2s, background 0.2s;
}
.rep-profile-social a:hover { color: var(--accent); border-color: var(--accent); background: rgba(255,185,99,0.08); }
.rep-profile-actions { display: flex; flex-direction: column; gap: 0.5rem; width: 100%; }
.rep-profile-actions .btn-primary,
.rep-profile-actions .btn-outline { width: 100%; text-align: center; }
.rep-profile-right { flex: 1; min-width: 0; }
.rep-profile-section-label {
  font-size: 0.62rem; text-transform: uppercase; letter-spacing: 0.14em;
  color: var(--text-muted); margin-bottom: 0.65rem;
  padding-bottom: 0.4rem; border-bottom: 1px solid var(--border);
}
.rep-profile-offices { margin-bottom: 1.25rem; }
.rep-profile-office-entry {
  font-size: 0.75rem; color: var(--text-muted); line-height: 1.6;
  padding: 0.75rem 0.9rem; background: var(--profile-bg);
  border-radius: 10px; margin-bottom: 0.5rem;
}
.rep-profile-office-entry strong {
  display: block; color: var(--text); font-size: 0.7rem;
  text-transform: uppercase; letter-spacing: 0.08em; margin-bottom: 0.25rem;
}
.rep-profile-wiki-body { font-size: 0.78rem; color: var(--text-muted); line-height: 1.75; }
.rep-profile-wiki-body p { margin-bottom: 0.75rem; }
@media (max-width: 600px) {
  .rep-profile-layout { flex-direction: column; }
  .rep-profile-left { width: 100%; }
  .rep-profile-box { padding: 1.25rem; }
}
```

- [ ] Open `index.html`. Verify no CSS/console errors.

- [ ] Commit: `git commit -m "feat: add rep profile modal HTML and CSS"`

---

### Task 5: Rep profile modal JavaScript

**Files:** `index.html` JS block

- [ ] Add state variables near top of script block (with other cache/state vars):
```js
const wikiCache = {};
let currentRepForProfile = null;
```

- [ ] Add `openRepProfile(rep)` function:

```js
function openRepProfile(rep) {
  currentRepForProfile = rep;

  // Photo
  const photoEl = document.getElementById('rpModal-photo');
  if (rep.photo_url && /^https?:\/\//.test(rep.photo_url)) {
    photoEl.src = escAttr(rep.photo_url);
    photoEl.alt = escAttr(rep.name);
    photoEl.parentElement.style.display = '';
  } else {
    photoEl.parentElement.style.display = 'none';
  }

  // Text fields — use textContent for plain text (XSS-safe)
  document.getElementById('rpModal-name').textContent = rep.name || '';
  document.getElementById('rpModal-role').textContent =
    (rep.elected_office || '') + (rep.representative_set_name ? ' — ' + rep.representative_set_name : '');

  const partyEl = document.getElementById('rpModal-party');
  if (rep.party_name) {
    partyEl.textContent = rep.party_name;
    partyEl.style.display = '';
  } else {
    partyEl.style.display = 'none';
  }

  // Social links — reuse buildSocialLinks, strip the outer div wrapper
  const socialHtml = buildSocialLinks(rep).replace('<div class="rep-social">', '').replace('</div>', '');
  document.getElementById('rpModal-social').innerHTML = socialHtml;

  // Action buttons
  const emailBtn = document.getElementById('rpModal-email-btn');
  emailBtn.style.display = rep.email ? '' : 'none';
  const profileLink = document.getElementById('rpModal-profile-link');
  if (rep.url && /^https?:\/\//.test(rep.url)) {
    profileLink.href = escAttr(rep.url);
    profileLink.style.display = '';
  } else {
    profileLink.style.display = 'none';
  }

  // Offices — build with textContent assignments to avoid XSS
  const officesEl = document.getElementById('rpModal-offices');
  const offices = (rep.extra && rep.extra.offices) ? rep.extra.offices : [];
  if (offices.length) {
    officesEl.innerHTML = '';
    const label = document.createElement('div');
    label.className = 'rep-profile-section-label';
    label.textContent = 'Contact & Offices';
    officesEl.appendChild(label);
    offices.forEach(o => {
      const entry = document.createElement('div');
      entry.className = 'rep-profile-office-entry';
      if (o.name) {
        const strong = document.createElement('strong');
        strong.textContent = o.name;
        entry.appendChild(strong);
      }
      if (o.postal) { entry.appendChild(document.createTextNode(o.postal)); entry.appendChild(document.createElement('br')); }
      if (o.tel) { entry.appendChild(document.createTextNode('📞 ' + o.tel)); entry.appendChild(document.createElement('br')); }
      if (o.fax) { entry.appendChild(document.createTextNode('Fax: ' + o.fax)); }
      officesEl.appendChild(entry);
    });
    officesEl.style.display = '';
  } else {
    officesEl.innerHTML = '';
    officesEl.style.display = 'none';
  }

  // Open modal
  document.getElementById('rep-profile-backdrop').classList.add('open');

  // Fetch Wikipedia bio
  fetchWikiBio(rep);
}
```

- [ ] Add `fetchWikiBio(rep)` function — strips all HTML from Wikipedia extract using regex before displaying (plain text only, no HTML injection risk):

```js
async function fetchWikiBio(rep) {
  const wikiEl = document.getElementById('rpModal-wiki');
  const bodyEl = document.getElementById('rpModal-wiki-body');

  bodyEl.textContent = 'Loading…';
  wikiEl.style.display = '';

  if (wikiCache[rep.name] !== undefined) {
    if (wikiCache[rep.name]) {
      renderWikiBio(bodyEl, wikiCache[rep.name].text, wikiCache[rep.name].title);
    } else {
      wikiEl.style.display = 'none';
    }
    return;
  }

  try {
    const query = encodeURIComponent(rep.name + ' ' + (rep.elected_office || ''));
    const searchRes = await Promise.race([
      fetch('https://en.wikipedia.org/w/api.php?action=query&list=search&srsearch=' + query + '&format=json&origin=*&srlimit=1'),
      new Promise((_, rej) => setTimeout(() => rej(new Error('timeout')), 3000))
    ]);
    const searchData = await searchRes.json();
    const hits = searchData.query && searchData.query.search;
    if (!hits || !hits.length) { wikiCache[rep.name] = null; wikiEl.style.display = 'none'; return; }

    const pageTitle = hits[0].title;
    const extractRes = await Promise.race([
      fetch('https://en.wikipedia.org/w/api.php?action=query&prop=extracts&exintro=true&redirects=1&titles=' + encodeURIComponent(pageTitle) + '&format=json&origin=*'),
      new Promise((_, rej) => setTimeout(() => rej(new Error('timeout')), 3000))
    ]);
    const extractData = await extractRes.json();
    const pages = extractData.query && extractData.query.pages;
    const page = pages && Object.values(pages)[0];
    const extract = page && page.extract;

    if (!extract || extract.includes('may refer to')) { wikiCache[rep.name] = null; wikiEl.style.display = 'none'; return; }

    // Strip all HTML tags — display as plain text only
    const plain = extract.replace(/<[^>]+>/g, ' ').replace(/\s+/g, ' ').trim();
    const limited = plain.length > 600 ? plain.slice(0, 600).replace(/\s+\S*$/, '') + '…' : plain;

    wikiCache[rep.name] = { text: limited, title: pageTitle };
    renderWikiBio(bodyEl, limited, pageTitle);
  } catch (e) {
    wikiCache[rep.name] = null;
    wikiEl.style.display = 'none';
  }
}

function renderWikiBio(el, text, pageTitle) {
  el.innerHTML = '';
  const p = document.createElement('p');
  p.textContent = text;
  el.appendChild(p);
  const link = document.createElement('a');
  link.href = 'https://en.wikipedia.org/wiki/' + encodeURIComponent(pageTitle);
  link.target = '_blank';
  link.rel = 'noopener';
  link.textContent = 'Read more on Wikipedia ↗';
  link.style.cssText = 'font-size:0.68rem;color:var(--accent)';
  el.appendChild(link);
}
```

- [ ] Add close and helper functions:

```js
function closeRepProfile(e) {
  if (!e || e.target === document.getElementById('rep-profile-backdrop')) {
    document.getElementById('rep-profile-backdrop').classList.remove('open');
  }
}

function rpModalWriteEmail() {
  if (currentRepForProfile) {
    closeRepProfile();
    openModal(currentRepForProfile);
  }
}
```

- [ ] Add `closeRepProfile()` and `closeSupport()` to the Escape keydown listener.

- [ ] Test in browser console:
```js
openRepProfile({ name: 'Olivia Chow', elected_office: 'Mayor', party_name: 'Liberal', photo_url: '', email: 'test@toronto.ca', url: 'https://toronto.ca', extra: {} })
```
Confirm: modal opens, name/role/party show, Wikipedia fetch runs (check Network tab), bio appears or wiki panel hides.

- [ ] Commit: `git commit -m "feat: add rep profile modal JS with Wikipedia bio and office info"`

---

### Task 6: Wire rep cards to open profile modal on click

**Files:** `index.html` — `renderRepList` function

- [ ] Make card div clickable — add `cursor:pointer` and `onclick` to card container:

Change:
```js
html += `\n        <div class="rep-card" style="animation-delay:${i * 0.06}s">`;
```
To:
```js
html += `\n        <div class="rep-card" style="animation-delay:${i * 0.06}s;cursor:pointer" onclick='openRepProfile(${JSON.stringify(rep).replace(/'/g, "&#39;")})'>`;
```

- [ ] Add `event.stopPropagation()` to all buttons inside the card to prevent double-firing:

- Write Email button: prepend `event.stopPropagation();` to its onclick
- Profile link: add `onclick="event.stopPropagation()"`
- Copy Info button: prepend `event.stopPropagation();` to its onclick

- [ ] Full browser test — search Canadian address then:
  - Click card body → profile modal opens
  - Click "Write Email" → email modal opens (not profile modal)
  - Click "Profile" → navigates to URL (not profile modal)
  - Click "Copy Info" → clipboard copy (not profile modal)
  - Escape key → closes profile modal
  - Wikipedia bio loads for known politicians (e.g. mayor of Toronto); hides gracefully for unknown councillors

- [ ] Commit: `git commit -m "feat: wire rep cards to open full profile modal on click"`

---

## Post-Implementation

- [ ] Update `CLAUDE.md` External APIs table — add Wikipedia REST API row
- [ ] Update `CLAUDE.md` Key Code Sections table — add rep profile modal and support modal
- [ ] Update `MEMORY.md` — note budget commented out, profile modal added, Ko-fi link updated
