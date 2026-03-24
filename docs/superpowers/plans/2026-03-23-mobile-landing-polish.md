# Mobile Landing Page Polish — Implementation Plan

**Source:** `docs/audits/2026-03-23-mobile-ui-audit.md`
**File:** `index.html` (single file — all CSS + HTML changes)

---

## Task 0: Commit existing unstaged Frontend Developer changes

The previous agent session left clean, tested changes unstaged. Commit them before starting new work.

**What to commit:** search button `btn-long`/`btn-short`, tab `flex-wrap: nowrap` + `data-short`, rep actions `grid 1fr 1fr`.

**Commit message:** `Fix mobile search button, tab wrap, and rep card layout`

---

## Task 1: Hero visual hierarchy — make "Your voice." dominate

**Goal:** "Your address." becomes the setup line; "Your voice." becomes the emotional punch.

### Steps

1. **CSS (~line 718):** Split the `h1` styling so the first line is lighter weight and smaller:

   ```css
   .hero h1 {
     font-family: 'DM Serif Display', serif;
     font-size: clamp(2.2rem, 6vw, 3.8rem);
     line-height: 1.1;
     letter-spacing: -0.03em;
     margin-bottom: 1rem;
     font-weight: 400;           /* lighten the whole h1 */
   }

   .hero h1 em {
     font-style: italic;
     color: var(--accent);
     font-weight: 400;           /* keep italic, keep accent color */
     font-size: 1.15em;          /* bump up ~15% relative to parent */
   }
   ```

   The key move: `h1` gets `font-weight: 400` (DM Serif Display regular is already elegant at 400). The `em` gets `font-size: 1.15em` so "Your voice." is visually larger. The contrast between the two lines creates hierarchy without adding markup.

2. **HTML (~line 2133):** No change needed — `<h1>Your address.<br><em>Your voice.</em></h1>` already has the right structure.

### Verify
- Dark mode: "Your voice." should be larger and accent-colored, "Your address." lighter.
- Light mode: same hierarchy, purple accent on "Your voice."
- Desktop: ensure it still looks balanced at `3.8rem` clamp ceiling.

---

## Task 2: Move hint text into placeholder

**Goal:** The hint "Start typing your Canadian address and select from suggestions." is hidden by the mobile keyboard. Move it into the input placeholder so it's visible when the user focuses.

### Steps

1. **HTML (~line 2140–2143):** Change the `placeholder` attribute:

   ```html
   <input
     id="address-input"
     type="text"
     placeholder="Start typing your Canadian address..."
     autocomplete="off"
   />
   ```

   Shortened from the full sentence — placeholders should be scannable, not paragraphs.

2. **HTML (~line 2150):** Remove the `.hint` paragraph entirely:

   ```html
   <!-- remove this line -->
   <p class="hint">Start typing your Canadian address and select from suggestions.</p>
   ```

3. **CSS (~line 811–815):** Remove the `.hint` rule (now unused):

   ```css
   /* remove */
   .hint {
     margin-top: 0.75rem;
     font-size: 0.68rem;
     color: var(--text-muted);
   }
   ```

### Verify
- Focus the input on mobile — placeholder text visible.
- After typing, placeholder disappears (browser default).
- No orphan `.hint` class left in CSS or HTML.

---

## Task 3: Search bar border contrast (light mode)

**Goal:** The search pill should pop more at rest in light mode. Currently the border is faint against `#faf8f5`.

### Steps

1. **CSS (~line 762–770):** Update `.input-row`:

   ```css
   .input-row {
     display: flex;
     border: 1.5px solid var(--border);     /* was 1px */
     border-radius: 2rem;
     overflow: hidden;
     transition: border-color 0.2s, box-shadow 0.2s;
     background: var(--surface);
     box-shadow: 0 1px 4px rgba(0,0,0,0.06);  /* was 0 2px 12px rgba(0,0,0,0.10) */
   }
   ```

   The change: `1.5px` border (slightly thicker at rest) + lighter resting shadow `0.06` that doesn't compete with the focus state. The focus-within shadow (`0.16`) already provides the "active" emphasis.

### Verify
- Light mode: search bar visually distinct from background at rest.
- Dark mode: still looks clean (dark `--border` is already visible).
- Focus state: still noticeably different from rest state.

---

## Task 4: Subtitle max-width on mobile

**Goal:** The DM Mono subtitle runs too wide on mobile, making it feel dense.

### Steps

1. **CSS (~line 738):** Add `max-width` to the mobile `.hero p` rule:

   ```css
   @media (max-width: 480px) {
     .hero { margin-bottom: 1.5rem; }
     .hero p { font-size: 0.78rem; color: var(--text); max-width: 30ch; margin: 0 auto; }
     .about-body p { font-size: 0.82rem; line-height: 1.6; }
   }
   ```

   `30ch` = ~30 characters wide. With DM Mono (monospace), this gives clean 2–3 line breaks instead of one dense block.

### Verify
- Mobile (≤480px): subtitle wraps at ~30 characters, centered.
- Desktop: no change (the existing `max-width: 420px` on `.hero p` still applies).

---

## Execution Order

0 → 1 → 2 → 3 → 4 (sequential, all in `index.html`)

After all 4 tasks: single commit with message `Polish mobile landing page per UI audit`
