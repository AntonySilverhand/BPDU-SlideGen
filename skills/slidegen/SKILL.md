---
name: slidegen
description: Generates a branded BPDU HTML slide deck based on a topic, motion, or outline.
---

# SlideGen: Branded HTML Slide Generator

Generate a single-file, self-contained HTML slide presentation following the BP Debate Union (BPDU) design system.

## Input Context
- **Topic/Motion:** The subject of the presentation.
- **Deck Type:**
    1. **Reference** (Default): Dense, card-heavy, for reading.
    2. **Case File**: Briefing style, dark accents, focused on a specific motion.
    3. **Event Host**: Projection-ready, massive text, alternating backgrounds, live event features.
- **Outline (Optional):** Specific points or slides requested.

## Design Requirements
- **Color Palette:** Primary: `#F5C842` (Amber), Background: `#FFFFFF` (White) / `#FAFAF8` (Off-white), Text: `#1A1A1A`.
- **Typography:** Rounded sans-serif (e.g., 'Poppins', 'Nunito', 'DM Sans' via Google Fonts).
- **Brand Bar:** `position: fixed` top bar with `BPDU_LOGO.png`, "BP Debate Union", and a dynamic slide tag.
- **Layout:** Use `clamp()` for all sizing. Generous whitespace (max 70% content width).
- **Navigation:** Arrow keys + Spacebar. Touch swipe support. Slide counter (e.g., "3 / 12").
- **Transitions:** `translateX` or `scale` based on deck type.
- **Assets:** Always embed images as base64 data URIs (see workflow below) so the deck is fully self-contained and works on any device.

## Template Library (canonical CSS + HTML source)

`slide-templates.html` at the repo root is the **canonical block library** — 73 live, rendered layout blocks. Always read it for exact CSS and HTML markup before generating a new deck; never invent class names from scratch.

### Available scripts

- **`scripts/catalog.py`** — Parses `slide-templates.html` and prints a compact block catalog (ID, name, background, CSS classes).
- **`scripts/embed-images.py`** — Outputs `LOGO_URI=data:...` and `THEME_URI=data:...` lines for embedding brand images.

### Locating the scripts

The scripts may live in the repo (`skills/slidegen/scripts/`) or in the installed skill directory (`~/.claude/skills/slidegen/scripts/`). Resolve the correct path before running anything:

```bash
# Run once; use $SLIDEGEN the rest of the way
if [ -f "skills/slidegen/scripts/catalog.py" ]; then
  SLIDEGEN="skills/slidegen/scripts"
else
  SLIDEGEN="$HOME/.claude/skills/slidegen/scripts"
fi
echo "Using: $SLIDEGEN"
```

### Step 1 — get the block catalog

```bash
python3 "$SLIDEGEN/catalog.py"
```

Output columns: `ID · Block/Name · Background · CSS classes & notes`. Use this to pick which blocks to combine for the deck.

### Step 2 — read the relevant blocks from the template

Once you know which blocks you need (e.g. A1 title, B1 stats, C3 argument cards), read the matching `<section>` elements from `slide-templates.html` for the exact HTML structure and any inline style overrides. **Copy the markup verbatim and fill in content. The output HTML file must include the exact CSS class names from these blocks — do not hand-write slide layouts.**

### Block groups at a glance

| Group | Slides | What's in it |
|-------|--------|-------------|
| **A — Structure** | s1–s3 | Title light/dark, Accent amber |
| **B — Core content** | s4–s10 | Stats row, Stat boxes dark, Parliament 2×2, Teams grid, Role grid 4-col, Speech pills, Timeline |
| **C — Rich content** | s11–s23 | 2/3-col cards, Argument cards, Clash+VS, Word cards, Philosopher cards, POI bar+grid, POI big number, Criteria row, Extension cards, Frame+Ext box, Pull quote, Big quote+chips |
| **D — Projection** | s24–s26 | Strategy grid dark, Hero text, Dark closing+CTA |
| **E — Creative I** | s27–s36 | Honeycomb, Logic chain, Impact scale, Crumbling SQ, Ripple, T-chart, Spectrum, Spotlight, Venn, Scorecard |
| **F — Creative II** | s37–s46 | Compact honeycomb, Burden pyramid, Glass cards, Radial burden, Clash pillars, Decision tree, Policy slider, Dense grid, Focus center, Nested rings |
| **G — Creative III** | s47–s58 | Honey Pro, 3D stack, Heatmap, Web of tension, Dashboard, Keyhole, Architecture, Pulse, Steps, Table, Glass stakeholder, Final accent |
| **H — Creative IV** | s59–s72 | Bubbles, Progress rings, Glass dash, Lightning, Checkgrid, Shadow cards, Roadmap, Prism, Pendulum, Glass list, Cycle, Split hero, Floating cards, Summary grid |

### Reusable Slide Layout Types
Use these layout classes to vary the presentation (all CSS is in `slide-templates.html`):
- **Title**: `.inner.row` + `.illo` on right. Always includes logo + illustration.
- **Stats**: `.stats` flex row of `.stat` cards. Quant overview, 3–5 numbers.
- **2×2 Grid**: `.parliament` CSS grid. Comparing 4 items (e.g., the four BP teams).
- **Timeline list**: `.order` flex-column of `.order-item`. Ordered sequences.
- **Bar + card grid**: `.poi-bar` + `.poi-grid` 2-col. Rules with a timeline element.
- **Role grid**: `.roles` 4-col grid of `.role` cards. Summarizing many roles.
- **Accent slide**: Full `background: var(--primary)`. One critical concept.
- **Meet the Teachers**: Public event style. Blends projection-ready hero text with informational cards for guest bios and motion breakdowns.
- **Teacher Card**: `.teacher-card` (flex-row) with `.teacher-img` (left) and `.teacher-info` (right). For guest bios.
- **Motion Anatomy**: `.motion-anatomy` grid of `.term-card` elements. Breaks down motion definitions for the public.

## Deck Types
- **Reference**: Dense, reading-oriented, card-heavy.
- **Case File**: Briefing style, dark accents, argument cards with `.arg::before`.
- **Event Host**: Projection-ready, massive text (`.hero`), alternating backgrounds, live event features.
- **Meet the Teachers**: Public-facing guest event style. Blends theatrical projection with informative biographies and concept breakdowns.

### Mandatory Brand Bar HTML
```html
<!-- src must be the full data URI from: python3 skills/slidegen/scripts/embed-images.py → LOGO_URI — never a relative path -->
<header class="brand-bar">
  <img src="data:image/png;base64,…(paste full contents of assets/BPDU_LOGO.b64 here)…" alt="BPDU">
  <span class="brand-bar-name">BP Debate Union</span>
  <span class="brand-bar-dot"></span>
  <span class="brand-bar-slide-tag" id="slideTag"></span>
</header>
```

### Mandatory CSS Tokens
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

### Navigation JS (use verbatim for Reference/Case File)
```js
const slides = document.querySelectorAll('.slide');
const progress = document.getElementById('progress');
const counter = document.getElementById('counter');
const slideTag = document.getElementById('slideTag');
const total = slides.length;
let cur = 0;

function go(n) {
  slides[cur].classList.remove('active');
  slides[cur].classList.add('exit');
  const prev = cur;
  setTimeout(() => slides[prev].classList.remove('exit'), 520);
  cur = ((n % total) + total) % total;
  slides[cur].classList.add('active');
  progress.style.width = ((cur + 1) / total * 100) + '%';
  counter.textContent = `${cur + 1} / ${total}`;
  slideTag.textContent = slides[cur].dataset.tag || '';
}

document.addEventListener('keydown', e => {
  if (e.key === 'ArrowRight' || e.key === ' ') { e.preventDefault(); go(cur + 1) }
  if (e.key === 'ArrowLeft') { e.preventDefault(); go(cur - 1) }
});

let tx = 0;
document.addEventListener('touchstart', e => { tx = e.touches[0].clientX }, { passive: true });
document.addEventListener('touchend', e => {
  const dx = e.changedTouches[0].clientX - tx;
  if (Math.abs(dx) > 48) go(dx < 0 ? cur + 1 : cur - 1);
});
```

## Generation Workflow

1. **Locate scripts** — resolve `$SLIDEGEN` using the path-detection block above (repo path first, installed path fallback).
2. **Catalog** — run `python3 "$SLIDEGEN/catalog.py"` to see all 73 blocks.
3. **Plan** — decide which blocks suit the topic and deck type; list them (e.g. A2 → B1 → C3 × 3 → D3).
4. **Embed images** — run the embed script to write data URIs to files:
   ```bash
   python3 "$SLIDEGEN/embed-images.py"
   ```
   This writes two files to the **current working directory** (not to stdout):
   - `.logo_uri.txt` — full `data:image/png;base64,...` URI for the logo
   - `.theme_uri.txt` — full `data:image/png;base64,...` URI for the illustration

   Read **`.logo_uri.txt`** with the Read tool and paste its entire contents as the `src` of every `<img alt="BPDU">` (brand bar + title slides). Read **`.theme_uri.txt`** and paste as the `src` of `.illo img` and `.closing-illo img`.
   **Never use relative file paths** — the deck must open on any device without external files.

   > ⚠️ Do NOT pipe the script output through `head`, `tr`, or any other shell filter — the URIs are 330 KB and 2.4 MB respectively; any truncation breaks the images. Use the files, not stdout.
5. **Copy CSS** — read the relevant `<section>` elements from `slide-templates.html` and copy their CSS classes verbatim into the output file's `<style>` block. Always include the full `:root` token block and all responsive `@media` rules.
6. **Write HTML** — build each `<section class="slide">` using the exact class names from the template. Annotate each slide's `data-tag` with a short label.
7. **Wire JS** — use the navigation JS snippet verbatim (see below).
8. **Save** — write the file to the working directory with a descriptive name.

## Output
Produce the complete HTML code for the requested presentation as a single file. Save it with a descriptive filename (e.g., `casefile-[motion-slug].html` for Case Files).
