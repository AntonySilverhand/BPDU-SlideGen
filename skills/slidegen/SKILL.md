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
    4. **Invitation Letter / Email**: Branded HTML email for inviting guests, panelists, judges, or participants to a BPDU event.
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

## Print Poster / Flyer Templates

The following A4 print-ready HTML poster/flyer templates are available as canonical reference for event promotion materials. These are **not** slide decks — they are single-page (or multi-page), self-contained HTML files designed for A4 printing (`794px × 1123px`).

### Bowen Cup flyer design system

- **Dimensions:** A4 portrait, `width: 794px; height: 1123px;`
- **Background:** Warm cream `#FDF8EB`
- **Primary accent:** Amber `#FFC542`
- **Secondary accent:** Teal `#A2D2DF`
- **Typography:** Bilingual — English primary with Chinese secondary (`opacity: 0.85; font-size: 0.68rem;`)
- **Layout:** Card-based with generous rounded corners, subtle shadows, and geometric accent shapes
- **Assets:** All images embedded as base64 data URIs for full self-containment

### Available templates

| File | Path | Description |
|------|------|-------------|
| **Bowen Cup — Full** | `/home/antony/coding/BP Debate Union/Bowen Cup/bowen_cup_flyer.html` | Original version with front page, back page, and sponsors poster (3 pages). Contains full event info, QR codes, schedule, and participation guidelines. |
| **Bowen Cup — Clean** | `/home/antony/coding/BP Debate Union/Bowen Cup/bowen_cup_flyer_clean.html` | Streamlined 2-page version (front + back only, no sponsors page). Use when sponsor information is not needed. |
| **Bowen Cup — SCGK** | `/home/antony/coding/BP Debate Union/Bowen Cup/bowen_cup_flyer_scgk.html` | Front and back variant with "scgk" (仕呈公考) sponsor branding. Use when this specific sponsor is involved. |

When generating new event flyers or posters, read the relevant template file first to copy its CSS tokens, layout patterns, and bilingual text styling verbatim. Do not invent new class names for poster layouts.

## Invitation Letter / Email Templates

Branded HTML emails for inviting panelists, judges, guests, or participants to BPDU events. Designed for maximum compatibility across email clients using **table-based layout with inline CSS**.

### Design system

| Element | Specification |
|---|---|
| **Width** | `600px` centered card inside a full-width outer table |
| **Outer background** | `#f5f0e6` (warm cream) |
| **Card background** | `#ffffff` |
| **Primary accent** | `#ffc62a` (amber) — top bar, divider, signature border |
| **Text primary** | `#061425` (dark navy) |
| **Text secondary** | `#261e40` (muted navy) |
| **Typography** | `'Varela Round'`, system-ui, sans-serif; body `15px`, line-height `1.75` |
| **Card shadow** | `0 2px 16px rgba(6,20,37,0.06)` |

### Canonical structure

Copy this skeleton verbatim and fill in the bracketed placeholders. All CSS must remain inline — never use `<style>` blocks or external stylesheets for email output.

```html
<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>[Event Name] — [Invitation Type]</title>
</head>
<body style="margin:0; padding:0; background:#f5f0e6; font-family:'Varela Round',system-ui,sans-serif;">
<table role="presentation" width="100%" cellpadding="0" cellspacing="0" style="background:#f5f0e6; padding:40px 0;">
<tr><td align="center">
<table role="presentation" width="600" cellpadding="0" cellspacing="0" style="background:#fff; overflow:hidden; box-shadow:0 2px 16px rgba(6,20,37,0.06);">

  <!-- Amber accent bar -->
  <tr><td style="background:#ffc62a; height:4px; font-size:0; line-height:0;">&nbsp;</td></tr>

  <!-- Header with logo -->
  <tr>
    <td style="background:#fff; padding:28px 40px 20px; text-align:center;">
      <a href="https://bpdebate.club" style="text-decoration:none; display:inline-block;">
        <img src="__LOGO_URI__" alt="BP Debate Union" width="48" height="48" style="display:inline-block; vertical-align:middle; border:0;">
        <span style="display:inline-block; vertical-align:middle; margin-left:12px; font-size:20px; font-weight:700; color:#061425; letter-spacing:0.5px; text-transform:uppercase;">BP DEBATE UNION</span>
      </a>
    </td>
  </tr>

  <!-- Gold divider -->
  <tr><td style="padding:0 40px;"><div style="border-bottom:3px solid #ffc62a; width:60px; margin:0 auto;"></div></td></tr>

  <!-- Event title -->
  <tr>
    <td style="padding:24px 40px 8px; text-align:center;">
      <div style="font-size:26px; font-weight:700; color:#061425; letter-spacing:0.5px;">[Event Name]</div>
      <div style="font-size:13px; color:#261e40; margin-top:6px; letter-spacing:2px; text-transform:uppercase;">[Invitation Type]</div>
    </td>
  </tr>

  <!-- Body -->
  <tr>
    <td style="padding:28px 40px 16px;">
      <p style="margin:0 0 18px; font-size:15px; color:#061425; line-height:1.75;">Dear [Recipient Name],</p>
      <p style="margin:0 0 18px; font-size:15px; color:#061425; line-height:1.75;">[Opening paragraph — context + invitation ask]</p>
      <!-- Optional: schedule table or extra details -->
    </td>
  </tr>

  <!-- Closing -->
  <tr>
    <td style="padding:0 40px 32px;">
      <p style="margin:0 0 18px; font-size:15px; color:#061425; line-height:1.75;">[Closing paragraph — gratitude + next steps]</p>
      <p style="margin:0 0 4px; font-size:15px; color:#061425; line-height:1.75;">Best regards,</p>
    </td>
  </tr>

  <!-- Signature -->
  <tr>
    <td style="padding:0 40px 28px;">
      <table role="presentation" cellpadding="0" cellspacing="0">
        <tr>
          <td style="border-left:3px solid #ffc62a; padding-left:16px;">
            <div style="font-size:16px; font-weight:700; color:#061425;">[Sender Name]</div>
            <div style="font-size:13px; color:#261e40; margin-top:2px;">[Title], BP Debate Union</div>
            <div style="font-size:13px; color:#261e40; margin-top:4px;">
              <a href="mailto:team@bpdebate.club" style="color:#061425; text-decoration:underline;">team@bpdebate.club</a>
            </div>
          </td>
        </tr>
      </table>
    </td>
  </tr>

  <!-- Theme illustration -->
  <tr>
    <td style="padding:0 40px 28px; text-align:center;">
      <img src="__THEME_URI__" alt="BP Debate Union" width="400" style="display:block; margin:0 auto; max-width:100%; height:auto; border-radius:8px;">
    </td>
  </tr>

  <!-- Footer -->
  <tr>
    <td style="background:#061425; padding:20px 40px; text-align:center;">
      <a href="https://bpdebate.club" style="color:#ffc62a; font-size:12px; text-decoration:none; letter-spacing:1px;">bpdebate.club</a>
      <div style="font-size:11px; color:#999; margin-top:6px;">Where logic clashes, minds meet, ideas matter...</div>
    </td>
  </tr>

</table>
</td></tr>
</table>
</body>
</html>
```

### Variable placeholders

| Placeholder | Source / Example |
|---|---|
| `[Event Name]` | e.g. "Bowen Cup II" |
| `[Invitation Type]` | e.g. "Panelist Invitation", "Judge Invitation", "Participant Welcome" |
| `[Recipient Name]` | e.g. "Professor Daniel" |
| `[Opening paragraph]` | Context + specific ask |
| `[Closing paragraph]` | Gratitude, logistics, or call-to-action |
| `[Sender Name]` | e.g. "Antony" |
| `[Title]` | e.g. "President" |

### Schedule table (optional)

When the invitation includes an event schedule, insert this table markup inside the body cell:

```html
<p style="margin:0 0 24px; font-size:15px; color:#061425; line-height:1.75;">The tournament schedule is as follows:</p>
<table role="presentation" width="100%" cellpadding="0" cellspacing="0" style="border-collapse:collapse; border:2px solid #061425;">
  <tr>
    <th style="background:#061425; color:#fff; padding:10px 16px; font-size:13px; text-align:left; font-weight:600;">Time</th>
    <th style="background:#061425; color:#fff; padding:10px 16px; font-size:13px; text-align:left; font-weight:600;">Activity</th>
    <th style="background:#061425; color:#fff; padding:10px 16px; font-size:13px; text-align:left; font-weight:600;">Notes</th>
  </tr>
  <tr>
    <td style="padding:10px 16px; font-size:14px; color:#061425; border-bottom:1px solid #e8e4da;"><strong>09:00 – 11:00</strong></td>
    <td style="padding:10px 16px; font-size:14px; color:#061425; border-bottom:1px solid #e8e4da;">Round 1</td>
    <td style="padding:10px 16px; font-size:14px; color:#061425; border-bottom:1px solid #e8e4da;">Opening round</td>
  </tr>
  <!-- stripe alternate rows with background:#fefbf3 -->
</table>
```

### Image handling for emails

Unlike slide decks, HTML emails **should not rely on base64 data URIs for delivery** — many email clients (Gmail, Outlook) block or strip them. Instead, follow the same placeholder workflow, then replace with hosted URLs before sending:

1. Run the embed script to produce `.logo_uri.txt` and `.theme_uri.txt`.
2. Write the email HTML with `__LOGO_URI__` and `__THEME_URI__` placeholders.
3. After injection, if the email will be sent through an ESP or Mailchimp/SendGrid, **swap the base64 strings for reliable `https://` CDN URLs** (e.g. hosted on `bpdebate.club`).
4. Keep the base64 version for offline drafts or local previews.

> ⚠️ **Never paste multi-megabyte base64 strings directly into the email markup during editing.** Use placeholders and inject only at the final step.

### Output
Save invitation letters to `tmp/` with a descriptive name, e.g. `tmp/invite-[event]-[role].html`.

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

## Phase 0 — Research & Content Brief

**Required for Case File and Reference decks. Skip for Event Host.**

This phase runs entirely in text — no HTML, no templates. Its output is a validated content brief that all slide content must be drawn from. Do not skip or abbreviate it; shallow briefs produce shallow slides.

### Step 0a — Check local knowledge base

Before any web search, check whether the local debate database is available:

```bash
python3 db/query.py stats 2>/dev/null && echo "DB_AVAILABLE" || echo "DB_MISSING"
```

**If `DB_AVAILABLE`:** query it for existing analyses and motions related to the topic before going to the web. Use these commands:

```bash
# Full-text search for related motions
python3 db/query.py search "[topic keyword]"

# Pull existing analyses for any matching motion IDs found above
python3 db/query.py motion [ID]

# Broader analysis search by motion text fragment
python3 db/query.py analysis "[topic keyword]"

# Search speech transcripts for real examples
python3 db/query.py transcripts "[topic keyword]"
```

Record any arguments, framings, or evidence found in the DB. These count as validated debate-community sources — treat them as a first-draft skeleton for the brief. Note which motion IDs they came from.

**If the DB returns no results** for any query: note that the topic has no prior coverage in the knowledge base, then proceed directly to Step 0c web searches. Do not spend more than 2 additional queries trying alternate keywords — absence of DB data is not a problem, just proceed.

**If `DB_MISSING`:** skip this step and proceed directly to Step 0b.

### Step 0b — Decompose the motion

Write out:
- **Motion text** (exact wording)
- **Key terms** — define each contested word; note which definition favours which side
- **Status quo** — what is currently true / what policy currently exists
- **Burden** — what Government must prove; what Opposition must prove
- **Assumed stakeholders** — who is most affected and why they matter

### Step 0c — Web search for evidence

Run at least **6 searches** covering all four team positions. Required search targets:

| Search target | Example query |
|---|---|
| Empirical evidence supporting the motion | `"[topic]" study statistics harm benefit site:scholar OR site:gov OR site:org` |
| Empirical evidence against the motion | `"[topic]" criticism failure unintended consequences research` |
| Real-world jurisdiction or case | `country OR city "[topic]" policy implemented results` |
| Named scholar or critic | `professor researcher "[topic]" argues OR claims OR warns` |
| Quantified impact | `"[topic]" percent OR million OR billion data report` |
| Recent news or development | `"[topic]" 2023 OR 2024 OR 2025` |

For each search result used, record: **source name, date, the specific claim or figure, and URL**.

### Step 0d — Draft the content brief

Write a structured brief covering all four BP teams. For each team write **2–3 arguments**, each argument must have all four parts:

```
CLAIM      — one sentence stating what is true
MECHANISM  — 2–3 sentences explaining the causal chain (how/why, not just that)
EVIDENCE   — a named source + specific statistic, study finding, or real case
             ❌ "studies show..."   ✅ "MIT Media Lab (2023) found that..."
             ❌ "in many countries" ✅ "Germany's 2022 NetzDG law resulted in..."
IMPACT     — what concretely breaks down if this argument is lost; who suffers and how
```

Also write:
- **2–3 key clashes** — the central tensions where the teams' arguments directly collide
- **CG and CO extension angles** — what genuinely new ground each closing bench can add beyond opening

### Step 0e — Adversarial critique

Re-read the brief and challenge every argument with these questions. Rewrite any that fail:

1. **Is the evidence real and named?** If you wrote "research suggests" or "studies show" without a source, find a real one.
2. **Is the mechanism specific?** If the mechanism is just a restatement of the claim ("X causes harm because X is harmful"), rewrite it with an actual causal chain.
3. **Is the impact weighable?** Can you compare this impact against a competing one? If not, add a magnitude or scope qualifier.
4. **Is the extension genuinely new?** If CG/CO arguments are just rephrasing OG/OO, replace them with a distinct framing or stakeholder.

### Step 0f — Lock the brief

After revisions, the brief is locked. All `.arg` card content, pull quotes, clash slides, and stat figures in the HTML **must come directly from this brief**. DB-sourced arguments and web-sourced evidence must both be present where available. Do not invent new content during templating.

---

## Generation Workflow

1. **Locate scripts** — resolve `$SLIDEGEN` using the path-detection block above (repo path first, installed path fallback).
2. **Catalog** — run `python3 "$SLIDEGEN/catalog.py"` to see all 73 blocks.
3. **Plan** — decide which blocks suit the topic and deck type; list them (e.g. A2 → B1 → C3 × 3 → D3). For Case File / Reference decks, map each brief argument to a specific block.
4. **Embed images** — run the embed script to write data URIs to files:
   ```bash
   python3 "$SLIDEGEN/embed-images.py"
   ```
   This writes two files to the **current working directory** (not to stdout):
   - `.logo_uri.txt` — full `data:image/png;base64,...` URI for the logo
   - `.theme_uri.txt` — full `data:image/png;base64,...` URI for the illustration

   > ⚠️ **Never paste the URI contents inline into the HTML.** The logo is 330 KB and the theme image is 2.4 MB of base64 — any attempt to copy-paste them will silently truncate the data and break the images. Use placeholders instead (see step 6).

   > ⚠️ **Never use the Read tool on `.png` files** (`BPDU_LOGO.png`, `BPDU_theme_image.png`). The Read tool sends PNG files to the API as image content blocks, which will cause a fatal "Could not process image" error. All image handling goes through the scripts — never touch the raw PNG files directly.

5. **Copy CSS** — read the relevant `<section>` elements from `slide-templates.html` and copy their CSS classes verbatim into the output file's `<style>` block. Always include the full `:root` token block and all responsive `@media` rules.
6. **Write HTML** — build each `<section class="slide">` using the exact class names from the template. Annotate each slide's `data-tag` with a short label.

   Use these exact placeholder strings as `src` values — **do not substitute real base64 here**:
   - `__LOGO_URI__` for every `<img>` that should show the BPDU logo (brand bar + title/closing slides)
   - `__THEME_URI__` for every `.illo img` and `.closing-illo img`

   > ⚠️ **Mandatory:** the title slide MUST contain a `.illo` div and the closing slide MUST contain a `.closing-illo` div, each with an `<img src="__THEME_URI__">`. If these elements are absent, the theme image will never be injected and the file will be ~360 KB instead of ~2.7 MB — a silent failure. Always verify both are present before saving.

   Required markup (must appear verbatim in the output):
   ```html
   <!-- in brand bar and title/closing slides: -->
   <img src="__LOGO_URI__" alt="BPDU">

   <!-- in title slide inner row: -->
   <div class="illo"><img src="__THEME_URI__" alt=""></div>

   <!-- in closing slide: -->
   <div class="closing-illo"><img src="__THEME_URI__" alt=""></div>
   ```

7. **Wire JS** — use the navigation JS snippet verbatim (see below).
8. **Save** — write the file to the `tmp/` directory with a descriptive name (e.g. `tmp/casefile-[slug].html`). Never save to the repo root.
9. **Inject images** — after saving, run this one-liner to substitute the placeholders with the real URIs:
   ```bash
   python3 - <<'PYEOF'
   import re, pathlib
   logo  = pathlib.Path('.logo_uri.txt').read_text().strip()
   theme = pathlib.Path('.theme_uri.txt').read_text().strip()
   p = pathlib.Path('OUTPUT_FILENAME.html')
   html = p.read_text()
   html = html.replace('__LOGO_URI__', logo).replace('__THEME_URI__', theme)
   p.write_text(html)
   print(f"Done — {len(html)//1024} KB")
   PYEOF
   ```
   Replace `OUTPUT_FILENAME.html` with the actual filename. The file size should jump to ~2.7 MB confirming both images are fully embedded.

   > ⚠️ **If the file stays ~360 KB after injection**, the `.illo` or `.closing-illo` elements were missing from the HTML. Go back, add them to the title and closing slides with `__THEME_URI__` as the src, re-save, and re-run the inject script.

## Output
Produce the complete HTML code for the requested presentation or email as a single file. Save it to `tmp/` with a descriptive filename:
- Case Files: `tmp/casefile-[motion-slug].html`
- Event Host decks: `tmp/event-host-[slug].html`
- Invitation Letters: `tmp/invite-[event]-[role].html`

> ⚠️ **Never run any git commands.** Do not commit, stage, push, or modify git history at any point. Git operations are exclusively the user's responsibility.
