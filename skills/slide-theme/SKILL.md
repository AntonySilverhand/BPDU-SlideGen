---
name: slide-theme
description: Applies or modifies the BPDU theme (branding, colors, typography) on an existing HTML slide deck.
---

# SlideTheme: BPDU Theme Applicator

Update an existing HTML slide deck to match the BP Debate Union (BPDU) design system.

## Input Context
- **Target File:** The HTML file to be updated.
- **Goal:** Ensure branding (logo, bar, fonts, colors) is consistent with the BPDU style.

## Key BPDU Design Standards
- **Primary Color:** `#F5C230` (Amber).
- **Secondary Colors:** Government (Blue: `#3B82F6`), Opposition (Red: `#EF4444`).
- **Brand Bar:** Must include `BPDU_LOGO.png`, "BP Debate Union", and dynamic slide tag.
- **Typography:** 'Poppins' or similar rounded sans-serif.

## Implementation Steps

### Step 1 — Read and audit the target file

Read the full HTML file. Identify:
- Does `header.brand-bar` exist in the `<body>`?
- Does the `<style>` block contain a `:root { }` rule?
- Does the `<script>` block contain a `go(n)` function (BPDU nav)?
- Do any `<img>` tags use relative `src` paths instead of `data:` URIs?
- Are there hardcoded hex colors outside `:root` that don't match the palette?

### Step 2 — Update CSS tokens

If a `:root` block exists, replace or add the following tokens so they exactly match:
```css
:root {
  --primary: #F5C230; --primary-light: #FFF6D6; --primary-dark: #C49A00;
  --bg: #FFFFFF; --bg-warm: #FFFDF5; --bg-dark: #1A1207;
  --text: #1A1A1A; --muted: #6B6B6B; --border: #EDE9DC;
  --gov: #3B82F6; --gov-light: #EFF6FF; --gov-mid: #BFDBFE;
  --opp: #EF4444; --opp-light: #FFF5F5; --opp-mid: #FCA5A5;
  --radius: 16px; --radius-lg: 28px; --font: 'Poppins', system-ui, sans-serif;
  --bar: 48px;
}
```
If no `:root` block exists, insert one at the top of the `<style>` block. Do **not** replace arbitrary hardcoded colors throughout the file — only update `:root`.

### Step 3 — Brand bar

**If `header.brand-bar` is missing:** Insert the following immediately after the opening `<body>` tag:
```html
<header class="brand-bar">
  <img src="" alt="BPDU" id="brandLogo">
  <span class="brand-bar-name">BP Debate Union</span>
  <span class="brand-bar-dot"></span>
  <span class="brand-bar-slide-tag" id="slideTag"></span>
</header>
```
Then add the brand bar CSS from `CLAUDE.md` to the `<style>` block.

**If it already exists:** Verify it has `position: fixed` in the CSS and that the logo `src` is a `data:` URI (not a relative path).

**Logo URI:** Run `python3 skills/slidegen/scripts/embed-images.py` to get `LOGO_URI` and `THEME_URI`. Paste `LOGO_URI` as the logo `src`. **Do not read the `.b64` files with the Read tool — they are too large and will be truncated.**

### Step 4 — Navigation JS

If no `go(n)` function is present, or navigation is clearly broken (e.g., missing `querySelector('.slide')`), replace the entire `<script>` block with the verbatim snippet from `CLAUDE.md`. Otherwise leave existing JS untouched.

### Step 5 — Post-update checklist

Before writing the output file, verify all of the following:
- [ ] `:root` contains all 14 BPDU tokens listed above
- [ ] `header.brand-bar` exists with `position: fixed` and logo `src` is a `data:` URI
- [ ] Every `.slide` has `padding-top: var(--bar)` (or equivalent)
- [ ] Navigation `go(n)` function is present and references `slides`, `counter`, `slideTag`
- [ ] No `<img>` uses a relative `src` path

## Design Reference
Refer to `skills/slidegen/assets/slide-templates.html` for canonical CSS and HTML markup, and `CLAUDE.md` for the full design system specification.
- CSS variables and `:root` token block
- Transitions (`translateX` for Reference/Case, `scale` for Event Host)
- Stagger animations (`.a` class)
- Three deck types: Reference, Case File, Event Host

## Output
Write the complete updated HTML file. If the user did not explicitly request overwriting, show a summary of changes made (brand bar added/updated, tokens updated, JS replaced) before writing.
