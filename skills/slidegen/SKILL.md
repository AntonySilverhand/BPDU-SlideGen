---
name: slidegen
description: |
  Generates a branded BPDU HTML slide deck, case file, event host deck, experience sharing deck, or invitation email.
  Use when the user asks for slides, a presentation, a case file, an event host deck, an experience sharing deck, or a BPDU-branded email invitation.
  Do NOT use for plain text outlines, PDF generation, or non-BPDU-branded content.
allowed-tools: Bash(python3 *), Read, Write
metadata:
  author: BP Debate Union
  version: "1.0"
---

# SlideGen: Branded HTML Slide Generator

Generate a single-file, self-contained HTML slide presentation following the BP Debate Union (BPDU) design system.

## Input Context
- **Topic/Motion:** The subject of the presentation.
- **Deck Type:**
    1. **Reference** (Default): Dense, card-heavy, for reading.
    2. **Case File**: Briefing style, dark accents, focused on a specific motion.
    3. **Event Host**: Projection-ready, massive text, alternating backgrounds, live event features.
    4. **Experience Sharing**: Elegant, warm, personal-presentation style. Editorial serif headings, cream backgrounds, reveal animations, floating decorative shapes, tip cards, score cards, QR contact slides.
    5. **Simplicity**: Ultra-minimal, dark-background, keyword-chip style. One idea per slide. Handwritten hero title, massive centered text, no cards or grids.
    6. **Invitation Letter / Email**: Branded HTML email for inviting panelists, judges, guests, or participants to BPDU events. Table-based layout with inline CSS for maximum email client compatibility.
- **Outline (Optional):** Specific points or slides requested.

## Input Parsing & Auto-Routing

The user does not need to remember hashtags or keywords. They speak naturally (e.g., "make me a deck about school dropout" or "I need a case file on THW ban social media"). The agent infers everything from the user's language.

### How to infer the workflow

**Step 1 — Detect the output type**

| User says something like... | Inferred workflow |
|---|---|
| "email," "invite," "letter," " invitation" | Invitation Email |
| "experience sharing," "my IELTS journey," "talk about," "workshop on my..." | Experience Sharing |
| "simplicity," "minimal," "keyword chips," "short deck," "quick intro," "icebreaker" | Slide Deck → Simplicity |
| "case file," "briefing on," "motion analysis" | Slide Deck → Case File |
| "event host," "hosting," "live event," "projection" | Slide Deck → Event Host |
| "reference," "rules," "guide," "training" | Slide Deck → Reference |
| Anything else ("slides on X," "deck about Y," "presentation for Z") | Slide Deck → Reference (default) |

**Step 2 — Detect speed mode**

| User signals... | Speed |
|---|---|
| "just give me," "quick," "rush through," "draft," "rough," "something simple," "fast" | FAST — skip Phase 0, generate from model knowledge |
| No urgency cues, or "thorough," "detailed," "comprehensive," "in-depth" | DEEP — run full Phase 0 (default) |

**Step 3 — Detect domain**

| User signals... | Domain |
|---|---|
| "pros and cons," "workshop on," "teaching slides," "general presentation," topic is clearly non-debate | GENERAL — neutral colors, no BP conventions |
| Topic looks like a motion ("THW...", "THB..."), or is clearly debate-related | DEBATE — gov/opp colors, BP structure (default) |
| Ambiguous | DEBATE (default) |

**Summary of defaults:**
- Output type → inferred from language (see Step 1)
- Speed → DEEP unless user signals hurry
- Domain → DEBATE unless user explicitly frames as non-debate

> **The user never needs to type hashtags.** Hashtags (`#quick`, `#general`, etc.) are accepted as explicit overrides for power users, but the agent must never ask the user to use them.

## Debate Strategy Content

When generating training decks, strategy guides, or coaching materials, read `skills/slidegen/assets/debate-strategy.md` for structured BP debate theory from the UChicago Debate Society workshop.

### When to reference strategy content

| User asks for... | Action |
|---|---|
| "BP strategy guide," "how to debate," "debate training" | Read Sections 1, 3 (pillars 1–3), 4, 5, 6, 7. Generate a training deck covering these fundamentals. |
| "How to prep in 15 minutes," "prep strategy" | Read Section 4 only. Generate a focused prep-guide deck or card. |
| "How to write a PM speech," "PM intro tips" | Read Section 5 (Rhetorical Architecture). Generate speech-structure slides. |
| "How to win as CG" / "CO strategy" / "Closing bench tips" | **STOP.** You cannot advise closing bench without knowing the opening half. First generate OG + OO content (or ask the user for it). Only after OG/OO exists may you read Section 2 and Section 3 (pillar 4) to advise on extension and weighing. |
| Case File on a motion | Optionally inject **one** strategy tip card per deck (e.g., a `.tip-card` reminding debaters to check "Did you mechanize this argument?" from Section 7). Do not overload the deck. |

### Critical constraint

**Never use opponent-dependent strategy sections (Section 2, Section 3 pillar 4) without first establishing Opening Government and Opening Opposition content.** If the user asks for closing-bench strategy and no opening half exists, explain that closing strategy requires knowing what OG/OO said, then offer to generate the opening half first.

## Design Requirements
- **Color Palette:** Primary: `#F5C842` (Amber), Background: `#FFFFFF` (White) / `#FAFAF8` (Off-white), Text: `#1A1A1A`.
- **Typography:** Rounded sans-serif (e.g., 'Poppins', 'Nunito', 'DM Sans' via Google Fonts).
- **Brand Bar:** `position: fixed` top bar with `BPDU_LOGO.png`, "BP Debate Union", and a dynamic slide tag.
- **Layout:** Use `clamp()` for all sizing. Generous whitespace (max 70% content width).
- **Navigation:** Arrow keys + Spacebar. Touch swipe support. Slide counter (e.g., "3 / 12").
- **Transitions:** `translateX` or `scale` based on deck type.
- **Assets:** By default, use CDN-hosted URLs for brand images (fast, small files). Use base64 data URI embedding **only** when the user explicitly requests a fully offline/self-contained file.

## Template Library (canonical CSS + HTML source)

`slide-templates.html` in `skills/slidegen/assets/` is the **canonical block library** — 84 live, rendered layout blocks. For agent use, read the smaller **per-group files** in `skills/slidegen/assets/templates/` instead. Each group file is a self-contained HTML preview containing the full CSS plus only that group's blocks. Use the monolithic `slide-templates.html` only as a browser preview or when you need the complete library in one file.

### Available scripts

- **`scripts/catalog.py`** — Parses `slide-templates.html` and prints a compact block catalog (ID, name, background, CSS classes).
- **`scripts/embed-images.py`** — Writes image URIs to `.logo_uri.txt` / `.theme_uri.txt`. Default mode writes CDN URLs (`--url` flag). Base64 mode (`--base64` or no flag) encodes local PNGs as data URIs for fully offline decks.

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

Once you know which blocks you need (e.g. A1 title, B1 stats, C3 argument cards), read the matching group file (`templates/group-a.html` for Group A, `templates/group-i.html` for Group I, etc.) for the exact HTML structure and any inline style overrides. **Copy the markup verbatim and fill in content. The output HTML file must include the exact CSS class names from these blocks — do not hand-write slide layouts.** Each group file contains the full CSS, so you can copy both the CSS tokens and the block markup from one file.

### Block groups at a glance

| Group | Slides | What's in it |
|-------|--------|-------------|
| **A — Structure** | s0–s3 | Index, Title light/dark, Accent amber |
| **B — Core content** | s4–s10 | Stats row, Stat boxes dark, Parliament 2×2, Teams grid, Role grid 4-col, Speech pills, Timeline |
| **C — Rich content** | s11–s23 | 2/3-col cards, Argument cards, Clash+VS, Word cards, Philosopher cards, POI bar+grid, POI big number, Criteria row, Extension cards, Frame+Ext box, Pull quote, Big quote+chips |
| **D — Projection** | s24–s26 | Strategy grid dark, Hero text, Dark closing+CTA |
| **E — Creative I** | s27–s36 | Honeycomb, Logic chain, Impact scale, Crumbling SQ, Ripple, T-chart, Spectrum, Spotlight, Venn, Scorecard |
| **F — Creative II** | s37–s46 | Compact honeycomb, Burden pyramid, Glass cards, Radial burden, Clash pillars, Decision tree, Policy slider, Dense grid, Focus center, Nested rings |
| **G — Creative III** | s47–s58 | Honey Pro, 3D stack, Heatmap, Web of tension, Dashboard, Keyhole, Architecture, Pulse, Steps, Table, Glass stakeholder, Final accent |
| **H — Creative IV** | s59–s72 | Bubbles, Progress rings, Glass dash, Lightning, Checkgrid, Shadow cards, Roadmap, Prism, Pendulum, Glass list, Cycle, Split hero, Floating cards, Summary grid |
| **I — Experience Sharing** | s73–s84 | Title experience, Self-intro, TOC, Tip cards, Big score, Philosophy diagram, Dark pillars, Promo cards, QR contact, Intro greeting, Two-path split, Contact closing |

### Reusable Slide Layout Types
Use these layout classes to vary the presentation (all CSS is in every group file):
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
- **Tip Cards**: `.tip-cards` flex column of `.tip-card` elements (icon + text, left gold border). For advice, suggestions, or step-by-step tips.
- **Big Score**: `.score-slide` with `.big-score` watermark number + `.score-cards-row` of `.score-card` pills. For displaying quantitative results (test scores, metrics).
- **Philosophy Diagram**: `.philosophy-diagram` row of `.thought-box` cards with `.thought-arrow` separators. For contrasting two approaches (right vs wrong way).
- **Dark Feature Pillars**: `.debate-slide` dark background with `.pillars-row` of `.glass-pillar` cards + `.debate-stats-row`. For dramatic feature highlights.
- **Promo Cards**: `.promo-row` grid of `.promo-card` elements with top gradient border and bullet lists. For promoting events, clubs, or opportunities.
- **QR Contact**: `.qr-row` of `.qr-card` elements with embedded QR images + `.contact-links`. For closing slides with WeChat / social contact.
- **Self-Introduction Card**: `.self-card` centered card with `.name`, `.role`, `.self-tags`. For speaker bios.
- **Table of Contents**: `.toc-list` of `.toc-item` with `.toc-num`, `.toc-label`, `.toc-line`. For agenda/overview slides.
- **Intro Greeting**: `.intro-slide` with `.intro-greeting` and `.intro-desc`. For welcoming the audience.
- **Two-Path Split**: Two `.tip-card` elements side-by-side in a flex row, used as path/choice cards.
- **Gold Divider**: `.gold-divider` with `.diamond` center. Elegant horizontal rule for visual separation.
- **Decorative Elements**: `.deco-circle`, `.deco-ring`, `.deco-dot` with `animation: float` / `floatSlow`. Floating ambient shapes for atmosphere.
- **Corner Brackets**: `.corner-tl` + `.corner-br` thin gold L-shapes. Adds editorial framing to title/closing slides.
- **Section Number Watermark**: `.section-number` giant faded numeral. Adds depth to content slides.
- **Reveal Animations**: `.reveal`, `.reveal-left`, `.reveal-right`, `.reveal-scale` with `.stagger-1`…`.stagger-7` delays. Content fades/slides in when the slide becomes active.

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

### Canonical source

Read `skills/slidegen/email-skeleton.html` for the full canonical skeleton. It contains the complete table-based email structure with inline CSS and all placeholder slots. Copy it verbatim and fill in the bracketed placeholders. All CSS must remain inline — never use `<style>` blocks or external stylesheets for email output.

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

When the invitation includes an event schedule, insert a table markup block inside the body cell. See `email-skeleton.html` for the schedule table template.

### Output
Save invitation letters to `tmp/` with a descriptive name, e.g. `tmp/invite-[event]-[role].html`.

## Deck Types
- **Reference**: Dense, reading-oriented, card-heavy.
- **Case File**: Briefing style, dark accents, argument cards with `.arg::before`.
- **Event Host**: Projection-ready, massive text (`.hero`), alternating backgrounds, live event features.
- **Meet the Teachers**: Public-facing guest event style. Blends theatrical projection with informative biographies and concept breakdowns.
- **Experience Sharing**: Elegant personal-presentation style. Warm cream backgrounds (`var(--bg-warm)`), editorial serif feel (`'Lora'`), generous whitespace, floating decorative shapes, reveal animations with stagger. Designed for talks, workshops, and storytelling — one idea per slide, tip cards for advice, score cards for metrics, promo cards for CTAs, QR cards for contact. Always uses `__THEME_URI__` on title and closing slides with `.illo` / `.closing-illo`.
- **Simplicity**: Ultra-minimal dark deck. Handwritten hero title (`'Beth Ellen'` cursive), massive centered question text, keyword chips with `.min-keyword` / `.min-keyword.hl`. No cards, no grids, no complex layouts. Background: `var(--bg-dark)` on every slide. Brand bar dark variant.

### Mandatory Brand Bar HTML
```html
<!-- src is either a CDN URL (default, fast) or a base64 data URI (offline mode) -->
<header class="brand-bar">
  <img src="__LOGO_URI__" alt="BPDU">
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

### Experience Sharing — Extra CSS & JS

For **Experience Sharing** decks, include these additional patterns after the base CSS.

**Fonts:**
```html
<link href="https://fonts.googleapis.com/css2?family=Lora:ital,wght@0,400;0,500;0,600;0,700;1,400;1,500&family=DM+Sans:ital,opsz,wght@0,9..40,300;0,9..40,400;0,9..40,500;0,9..40,700;1,9..40,400&display=swap" rel="stylesheet">
```

**Reveal animations (add to <style>):**
```css
.reveal, .reveal-left, .reveal-right, .reveal-scale {
  opacity: 0;
  transition: opacity .6s cubic-bezier(.16,1,.3,1), transform .6s cubic-bezier(.16,1,.3,1);
}
.reveal       { transform: translateY(25px) }
.reveal-left  { transform: translateX(-30px) }
.reveal-right { transform: translateX(30px) }
.reveal-scale { transform: scale(.88); transition-duration: .8s }
.slide.active .reveal,
.slide.active .reveal-left,
.slide.active .reveal-right,
.slide.active .reveal-scale {
  opacity: 1; transform: translateY(0) translateX(0) scale(1);
}
.slide.active .stagger-1 { transition-delay: .05s }
.slide.active .stagger-2 { transition-delay: .15s }
.slide.active .stagger-3 { transition-delay: .25s }
.slide.active .stagger-4 { transition-delay: .35s }
.slide.active .stagger-5 { transition-delay: .45s }
.slide.active .stagger-6 { transition-delay: .55s }
.slide.active .stagger-7 { transition-delay: .65s }
```

**Counter animation (add to <script>, triggers when slide gains `.active`):**
```js
const slides = document.querySelectorAll('.slide');
const observer = new IntersectionObserver((entries) => {
  entries.forEach(entry => {
    if (entry.isIntersecting) {
      entry.target.querySelectorAll('[data-counter]').forEach(el => {
        if (el.dataset.counted) return;
        el.dataset.counted = 'true';
        const target = parseFloat(el.dataset.counter);
        const start = performance.now();
        const animate = (now) => {
          const progress = Math.min((now - start) / 1400, 1);
          const eased = 1 - Math.pow(1 - progress, 3);
          el.textContent = (target * eased).toFixed(1);
          if (progress < 1) requestAnimationFrame(animate);
        };
        requestAnimationFrame(animate);
      });
    }
  });
}, { threshold: 0.45 });
slides.forEach(slide => observer.observe(slide));
```

Use `data-counter="7.5"` on score elements; the script animates from `0.0` to the target value.

## Phase 0 — Research & Content Brief

**Default behavior: ALWAYS run this phase.** Deep mode is the default for all decks regardless of type. Skip Phase 0 only when:
- The user explicitly says **#quick** / **#fast**, OR
- The user's language signals urgency or minimal-effort intent (e.g., "just give me," "rush through," "draft," "rough," "something simple").

This phase runs entirely in text — no HTML, no templates. Its output is a validated content brief that all slide content must be drawn from.

> **Content completeness rule:** Once the brief is locked, **do not truncate, compress, or omit any argument, clash, or piece of evidence to fit a predetermined slide count.** Slide count is emergent — it expands to fit the content. If the brief contains 12 arguments and 5 clashes, generate as many slides as needed to present every one of them. The model should never discard synthesized content just because it exceeds an expected deck length.

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

Write a structured brief covering all four BP teams. For each team write **at least 2–3 arguments**; if your research surfaces more distinct, well-sourced arguments, include them all. Each argument must have all four parts:

```
CLAIM      — one sentence stating what is true
MECHANISM  — 2–3 sentences explaining the causal chain (how/why, not just that)
EVIDENCE   — a named source + specific statistic, study finding, or real case
             ❌ "studies show..."   ✅ "MIT Media Lab (2023) found that..."
             ❌ "in many countries" ✅ "Germany's 2022 NetzDG law resulted in..."
IMPACT     — what concretely breaks down if this argument is lost; who suffers and how
```

Also write:
- **At least 2–3 key clashes** — the central tensions where the teams' arguments directly collide. If more distinct clash points exist, document all of them.
- **CG and CO extension angles** — what genuinely new ground each closing bench can add beyond opening

### Step 0e — Adversarial critique

Re-read the brief and challenge every argument with these questions. Rewrite any that fail:

1. **Is the evidence real and named?** If you wrote "research suggests" or "studies show" without a source, find a real one.
2. **Is the mechanism specific?** If the mechanism is just a restatement of the claim ("X causes harm because X is harmful"), rewrite it with an actual causal chain.
3. **Is the impact weighable?** Can you compare this impact against a competing one? If not, add a magnitude or scope qualifier.
4. **Is the extension genuinely new?** If CG/CO arguments are just rephrasing OG/OO, replace them with a distinct framing or stakeholder.

### Step 0f — Lock the brief

After revisions, the brief is locked. All `.arg` card content, pull quotes, clash slides, and stat figures in the HTML **must come directly from this brief**. DB-sourced arguments and web-sourced evidence must both be present where available. Do not invent new content during templating.

> **Critical:** Do not truncate, compress, or omit any content from the locked brief to fit a perceived slide budget. If the brief contains 15 arguments, 6 clashes, and 8 pieces of evidence, generate enough slides to present every single one. Slide count is a consequence of content depth, never a constraint.

---

## Generation Workflow

### Workflow A — Slide Deck (Reference / Case File / Event Host / Meet the Teachers / Simplicity)

Follow these steps when generating any standard slide deck.

1. **Locate scripts** — resolve `$SLIDEGEN` using the path-detection block above (repo path first, installed path fallback).
2. **Catalog** — run `python3 "$SLIDEGEN/catalog.py"` to see all 84 blocks and pick the groups you need.
3. **Plan** — decide which group files suit the topic and deck type; list them (e.g. `group-a.html` → `group-c.html`). For Case File / Reference decks, map each brief argument to a specific block. There is no slide budget — if the brief contains 20 distinct points, plan 20+ slides. Never merge or drop arguments to save space.
4. **Embed images** — run the embed script with the `--url` flag to write CDN URLs to files (default, fast):
   ```bash
   python3 "$SLIDEGEN/embed-images.py" --url \
     https://bpdebate.club/wp-content/uploads/2025/05/cropped-ChatGPT-Image-May-8-2025-10_18_18-PM.png \
     https://bpdebate.club/wp-content/uploads/2025/12/Untitled-design-3-1.png
   ```
   This writes two files to the **current working directory** (not to stdout):
   - `.logo_uri.txt` — the CDN URL for the logo
   - `.theme_uri.txt` — the CDN URL for the illustration

   > ⚠️ **Offline mode:** If the user explicitly requests a fully offline/self-contained file, omit `--url` to generate base64 data URIs instead. The file will grow to ~2.7 MB but works without internet.

   > ⚠️ **Never use the Read tool on `.png` files** (`BPDU_LOGO.png`, `BPDU_theme_image.png`). The Read tool sends PNG files to the API as image content blocks, which will cause a fatal "Could not process image" error. All image handling goes through the scripts — never touch the raw PNG files directly.

5. **Copy CSS** — read the relevant group file (e.g. `templates/group-c.html`) and copy its CSS classes verbatim into the output file's `<style>` block. Always include the full `:root` token block and all responsive `@media` rules.
6. **Write HTML** — build each `<section class="slide">` using the exact class names from the group file. Annotate each slide's `data-tag` with a short label.

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
   Replace `OUTPUT_FILENAME.html` with the actual filename.
   - **Default (CDN URLs):** file stays ~360 KB — this is correct and fast.
   - **Offline (base64 mode):** file jumps to ~2.7 MB — confirms both images are fully embedded.

   > ⚠️ **If the file stays at placeholder size after injection** (e.g. `__LOGO_URI__` still visible in the source), the `.illo` or `.closing-illo` elements were missing from the HTML. Go back, add them to the title and closing slides, re-save, and re-run the inject script.

### Workflow B — Simplicity Deck

Follow Workflow A steps 1–9, with these modifications:

- **Step 2 (Catalog):** Ignore the block catalog. Simplicity decks do not use the group template library — they use only the minimal CSS classes defined below.
- **Step 4 (Embed images):** Optional. Simplicity decks may omit the theme illustration entirely for an even smaller file. If used, inject only the logo URI.
- **Step 5 (CSS):** Do not copy group template CSS. Use **only** the base `:root` tokens, the base navigation chrome, and the **Simplicity Extra CSS** below.
- **Step 5 (Fonts):** Load `'Beth Ellen'` via `@font-face` (fallback: `cursive`) and `'Poppins'` for labels/body.
- **Step 6 (HTML):** Every `.slide` gets `background: var(--bg-dark)`. Every `.inner` gets `class="inner center"`. Use only these classes per slide:
  - Title slide: `.min-label` + `.min-hero` + `.min-sub`
  - Question slides: `.min-label` + `.min-question` + `.min-keywords` containing `.min-keyword` spans (add `.hl` to the primary keyword)
  - Closing slide: `.min-hero` + `.min-sub`
- **Step 7 (JS):** Use the standard navigation JS verbatim.
- **Step 8 (Save):** Use a descriptive name like `tmp/simplicity-[topic-slug].html`.

**Simplicity Extra CSS (add to `<style>` after base tokens):**

```css
/* Dark brand bar variant */
.brand-bar {
  background: rgba(20, 14, 6, 0.88);
  border-bottom: 1px solid rgba(255,255,255,0.08);
}
.brand-bar-name, .brand-bar-slide-tag { color: rgba(255,255,255,0.85); }

/* Beth Ellen handwritten hero */
@font-face {
  font-family: "Beth Ellen";
  font-style: normal;
  font-weight: 400;
  font-display: fallback;
  src: url('https://antony.bpdebate.club/wp-content/themes/impressionist/assets/fonts/beth-ellen_normal_400.ttf') format('truetype');
}

.min-hero {
  font-family: 'Beth Ellen', cursive;
  font-size: clamp(2.2rem, 6vw, 5rem); font-weight: 400;
  line-height: 1.15; color: white; text-align: center;
}
.min-label {
  font-size: clamp(10px, 1.2vw, 12px);
  font-weight: 700; letter-spacing: .22em;
  text-transform: uppercase; color: var(--primary);
  margin-bottom: clamp(16px, 2.5vh, 24px);
}
.min-question {
  font-size: clamp(1.6rem, 3.8vw, 3.6rem);
  font-weight: 800; line-height: 1.15; color: white;
  max-width: 900px; text-align: center;
}
.min-keywords {
  display: flex; flex-wrap: wrap; gap: clamp(10px, 1.5vw, 16px);
  justify-content: center; margin-top: clamp(20px, 3vh, 36px);
}
.min-keyword {
  background: rgba(255,255,255,0.08);
  border: 1px solid rgba(248,248,248,0.2);
  color: rgba(255,255,255,0.92);
  font-size: clamp(1rem, 2.2vw, 1.6rem); font-weight: 700;
  padding: clamp(8px, 1.4vh, 14px) clamp(16px, 2.4vw, 28px);
  border-radius: 999px; backdrop-filter: blur(8px);
}
.min-keyword.hl {
  background: var(--primary); color: var(--bg-dark); border-color: var(--primary);
}
.min-sub {
  font-size: clamp(0.9rem, 1.6vw, 1.2rem); color: rgba(255,255,255,0.55);
  margin-top: clamp(10px, 1.8vh, 16px); text-align: center;
}
```

**Simplicity HTML pattern:**

```html
<section class="slide active" id="s1" data-tag="Title">
  <div class="inner center">
    <p class="min-label a">Topic Category</p>
    <h1 class="min-hero a">Main Title</h1>
    <p class="min-sub a">Subtitle — Speaker Name</p>
  </div>
</section>

<section class="slide" id="s2" data-tag="Question">
  <div class="inner center">
    <p class="min-label a">Question 1</p>
    <h2 class="min-question a">What kind of ...?</h2>
    <div class="min-keywords a">
      <span class="min-keyword hl">Primary Answer</span>
      <span class="min-keyword">Secondary</span>
      <span class="min-keyword">Tertiary</span>
    </div>
  </div>
</section>
```

### Workflow C — Experience Sharing Deck

Follow Workflow A steps 1–9, with these modifications:

- **Step 2 (Catalog):** Focus on Group I blocks (`templates/group-i.html`) — s73–s84.
- **Step 5 (CSS):** After copying the base CSS from the group file, append the **Experience Sharing Extra CSS** (reveal animations, stagger delays, decorative shapes, gold divider, corner brackets, etc.) from the appendix below.
- **Step 5 (Fonts):** Load `'Lora'` + `'DM Sans'` via Google Fonts link instead of `'Poppins'`.
- **Step 7 (JS):** Append the **Counter Animation** JS snippet from the appendix below. Use `data-counter="7.5"` on score elements.
- **Step 8 (Save):** Use a descriptive name like `tmp/experience-[topic-slug].html`.

### Workflow D — Invitation Email

1. **Read skeleton** — read `skills/slidegen/email-skeleton.html` for the complete table-based email structure.
2. **Fill placeholders** — replace all bracketed placeholders (`[Event Name]`, `[Recipient Name]`, `[Sender Name]`, etc.) with real content.
3. **Optional schedule** — if the invitation includes a schedule, insert the schedule table markup from the skeleton inside the body cell.
4. **Save** — write the file to `tmp/` with a descriptive name, e.g. `tmp/invite-[event]-[role].html`.

> ⚠️ **Do NOT run `catalog.py` or `embed-images.py` for emails.** Emails use CDN-hosted logo/illustration URLs, not base64 data URIs. Emails do not need JS navigation or CSS variables.

## Output
Produce the complete HTML code for the requested presentation or email as a single file. Save it to `tmp/` with a descriptive filename:
- Slide decks: `tmp/casefile-[motion-slug].html`, `tmp/eventhost-[event-slug].html`, `tmp/experience-[topic-slug].html`, `tmp/simplicity-[topic-slug].html`
- Emails: `tmp/invite-[event]-[role].html`

> ⚠️ **Never run any git commands.** Do not commit, stage, push, or modify git history at any point. Git operations are exclusively the user's responsibility.
