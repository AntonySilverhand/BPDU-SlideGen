# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

SlideGen is a set of **Claude Code agent skills** for generating self-contained HTML slide presentations. Think PowerPoint, but in HTML — fully keyboard-navigable (arrow keys + spacebar), no build step, single file output. Built by BP Debate Union (bpdebate.club).

Skills are authored following the [agentskills.io](https://agentskills.io/) specification.

## Slide Output Requirements

Every generated HTML presentation must:
- Be a **single self-contained `.html` file** (inline CSS + JS, no external dependencies beyond CDN fonts)
- Support keyboard navigation: `←`/`→` arrows to move between slides, `Space` to advance
- Support touch swipe navigation
- Show slide number / total (e.g. "3 / 12") somewhere unobtrusive
- Work when opened directly from the filesystem (no server required)

### Persistent brand bar (required on every deck)

Every deck must include a `position: fixed` brand bar at the top with the BPDU logo and name visible on **every** slide — not embedded per-slide. The bar uses frosted glass so it works over any slide background:

```html
<header class="brand-bar">
  <img src="BPDU_LOGO.png" alt="BPDU">
  <span class="brand-bar-name">BP Debate Union</span>
  <span class="brand-bar-dot"></span>
  <span class="brand-bar-slide-tag" id="slideTag"><!-- updated by JS --></span>
</header>
```

```css
.brand-bar {
  position: fixed; top: 0; left: 0; right: 0; height: var(--bar); /* --bar: 48px */
  z-index: 300;
  display: flex; align-items: center;
  padding: 0 clamp(16px, 3vw, 32px); gap: 10px;
  background: rgba(255,255,255,0.88);
  backdrop-filter: blur(14px);
  -webkit-backdrop-filter: blur(14px);
  border-bottom: 1px solid rgba(237,233,220,0.7);
}
```

The `data-tag` attribute on each `<section class="slide">` feeds the brand bar's slide tag via JS on every navigation. All `.slide` elements must have `padding-top: var(--bar)` so content clears the bar.

### Adaptive / responsive layout (required)

All sizing must use `clamp()` — never hardcoded `px` for font sizes or spacing. Key responsive breakpoints:

| Breakpoint | Changes |
|------------|---------|
| `≤ 900px` | Hide `.illo` / `.closing-illo`; stack `.inner.row` to column; `.roles` → 2-col grid |
| `≤ 600px` | `.parliament` → 1-col; `.criteria` → column; `.poi-grid` → 1-col; `.roles` → 2-col; reduce all padding |
| `≤ 400px` | `.roles` → 1-col |
| `≥ 1600px` | Expand `max-width` |

Illustrations (`min(360px, 35vw)` wide) automatically disappear at tablet width — content must be complete without them.

## BPDU Design System

All generated slides must match the BPDU visual identity observed in `Pasted image.png` and `BPDU_theme_image.png`:

**Color palette:**
- Primary / accent: warm amber-yellow `#F5C842` (or close match from the website's CTA buttons)
- Background: white `#FFFFFF` or off-white `#FAFAF8`
- Text: near-black `#1A1A1A`
- Secondary text / captions: medium gray `#6B6B6B`
- Highlight / code blocks: light warm tan `#FFF8E7`

**Typography:**
- Headings: a rounded, friendly sans-serif (e.g. `'Nunito'`, `'Poppins'`, or `'DM Sans'` via Google Fonts)
- Body: clean sans-serif, generous line-height (1.6+)
- Avoid rigid corporate fonts; the brand is friendly and intellectual

**Illustration / visual style:**
- Warm, flat-cartoon illustrations (see `BPDU_theme_image.png` — illustrated group portrait)
- Avoid cold blues or harsh contrast
- Logo (`BPDU_LOGO.png`): brain + lightning bolt on light teal; include as `<img>` in slide decks when branding is needed

**Layout:**
- Generous whitespace; content never fills more than ~70% of the slide width
- Left-aligned or centered text (not justified)
- Card-style content blocks with subtle rounded corners and very light shadows

## Asset Paths

Brand assets live at the repo root:
- `BPDU_LOGO.png` — logo, use in title/closing slides
- `BPDU_theme_image.png` — decorative group illustration

**CDN mode (default):** run `python3 skills/slidegen/scripts/embed-images.py --url [logo-url] [theme-url]` to write CDN URLs to `.logo_uri.txt` and `.theme_uri.txt`. Use `__LOGO_URI__` and `__THEME_URI__` placeholders in the HTML, then inject them after saving. The output stays small (~360 KB) but requires an internet connection to display images.

**Embedding mode (offline):** omit `--url` to generate base64 data URIs. The output is a fully self-contained file (~2.7 MB) with no external dependencies — use this only when the user explicitly requests an offline file.

Never reference raw PNG files with relative paths in the final output — use either CDN URLs or base64 data URIs.

## Skill Architecture

Skills in this repo follow the agentskills.io pattern: each skill is a Markdown file with YAML frontmatter describing its trigger and a prompt body that instructs Claude how to execute the task.

Active skills:
- `slidegen` — primary skill: takes a topic/outline, produces a branded HTML deck, experience sharing deck, or invitation email
- `deep-analysis` — motion research and content brief generation
- `imagegen` — AI illustration generation for slide decks

When building skills, keep the prompt body focused: describe the output format precisely (slide structure, CSS variables to use, JS navigation snippet) so the generating model produces consistent results across invocations.

## HTML Slide Template Pattern

`bp-debate-rules.html` is the canonical reference implementation. Study it before generating new decks.

### CSS tokens (always define these in `:root`)

```css
--primary: #F5C230;   --primary-light: #FFF6D6;  --primary-dark: #C49A00;
--bg: #FFFFFF;        --bg-warm: #FFFDF5;          --bg-dark: #1A1207;
--text: #1A1A1A;      --muted: #6B6B6B;            --border: #EDE9DC;
--gov: #3B82F6;       --gov-light: #EFF6FF;        --gov-mid: #BFDBFE;  --gov-dark: #1D4ED8;
--opp: #EF4444;       --opp-light: #FFF5F5;        --opp-mid: #FCA5A5;  --opp-dark: #B91C1C;
--radius: 16px;       --radius-lg: 28px;           --font: 'Poppins', system-ui, sans-serif;
```

Government/opposition color coding (blue/red) is a BP debate convention — always use it when content involves teams or sides.

### Slide transition system

Slides are `position:absolute; inset:0` with `opacity:0; transform:translateX(6%)`. Active slide: `opacity:1; transform:translateX(0)`. Exiting slide gets class `.exit` → `opacity:0; transform:translateX(-4%)`, removed after 520 ms. Never use `display:none` — it breaks transitions.

### Content stagger animation

Add class `.a` to every content child. The CSS animates them in with `translateY(22px)→0` + fade, using `nth-child` delays from `.08s` to `.59s`. This requires `.slide.active .a { animation: up ... }` rules for each nth-child. Always reset on slide transition (class removal/re-add triggers re-animation automatically).

### JS navigation (use verbatim)

```js
const slides = document.querySelectorAll('.slide');
const progress = document.getElementById('progress');
const counter  = document.getElementById('counter');
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
  counter.textContent  = `${cur + 1} / ${total}`;
  slideTag.textContent = slides[cur].dataset.tag || '';
}

document.addEventListener('keydown', e => {
  if (e.key === 'ArrowRight' || e.key === ' ') { e.preventDefault(); go(cur + 1) }
  if (e.key === 'ArrowLeft')                   { e.preventDefault(); go(cur - 1) }
});

// Touch swipe
let tx = 0;
document.addEventListener('touchstart', e => { tx = e.touches[0].clientX }, { passive: true });
document.addEventListener('touchend',   e => {
  const dx = e.changedTouches[0].clientX - tx;
  if (Math.abs(dx) > 48) go(dx < 0 ? cur + 1 : cur - 1);
});
```

### Reusable slide layout types

These eight layouts cover the patterns in `bp-debate-rules.html`:

| Layout | Class pattern | Use when |
|--------|--------------|----------|
| **Title** | `.inner.row` + `.illo` on right | Opening slide, always includes logo + illustration |
| **Stats** | `.stats` flex row of `.stat` cards | Quantitative overview, 3–5 numbers |
| **2×2 Grid** | `.parliament` CSS grid | Comparing 4 items (e.g. the four BP teams) |
| **Timeline list** | `.order` flex-column of `.order-item` | Ordered sequences (speaking order, steps) |
| **Bar + card grid** | `.poi-bar` + `.poi-grid` 2-col | Rules with a visual timeline element |
| **Role grid** | `.roles` 4-col grid of `.role` cards | Summarising many roles/items compactly |
| **Accent slide** | Full `background: var(--primary)` | One critical concept; dark text on yellow |
| **Dark closing** | `background: var(--bg-dark)` | Final CTA slide; white text, logo, illustration |

### BP Debate–specific conventions

- Always colour-code government content blue (`--gov*` tokens) and opposition content red (`--opp*` tokens)
- The 4-team parliament grid uses a `.divider-row` spanning both columns to separate opening from closing benches
- Whip speeches (7 & 8) always carry the note "no new arguments" in their description
- The Extension concept warrants its own accent slide — it is the most misunderstood BP rule

---

## Deck Types

Five distinct output types exist in this repo, grouped into three categories. Each has different design priorities and template blocks:

### Category 1 — Standard Slide Decks

These use blocks from Groups A–H (s0–s72) in the template library.

#### 1. Reference deck (`bp-debate-rules.html`)
Dense, card-heavy, designed for reading. Left-aligned layouts, many cards per slide, inner padding `clamp(16px,3.5vh,48px)`. Audience reads the slide.

#### 2. Case file deck (`casefile-fearing-death.html`)
Briefing-document style. Dark title/closing, amber accent for the central clash, argument cards with `.arg::before` left-colour bar, pull-quotes. Audience reads + host elaborates. Naming convention: `casefile-[motion-slug].html`.

#### 3. Event host deck (`event-host-deck.html`)
**Designed for live projection.** Host talks; slide is a visual anchor. Key rules:
- **One idea per slide.** Aim for 3–4 focal items per slide so the host can talk to it, but if the content demands more, add slides rather than cramming.
- **Text is massive.** `.hero` = `clamp(2.2rem,6vw,5.5rem)`. Readable from 5 metres.
- **Centred layout.** `.inner` uses `align-items:center; text-align:center`.
- **Alternating backgrounds** create rhythm: dark → light → amber → ...
- **Event CONFIG block** at top of `<script>`: `eventName`, `eventDate`, `motion`, `prepMinutes`.
- **Scale-based transitions** (`scale(.97)` → `scale(1)`), not translateX.
- **Live badge** in brand bar signals "this is a live event deck".

**Typical flow (example, not a limit):** `Welcome → Motion → How It Works → Four Teams → Speaking Order → POIs → Judging Criteria → Extension Rule → Prep Time → Good Luck → After the Round`. If the event has extra segments (e.g. guest speaker, Q&A, sponsor thanks), append them. The deck expands to fit the content.

#### 4. Meet the Teachers deck
Public-facing guest event style. Blends theatrical projection with informative biographies and concept breakdowns. Uses `.teacher-card` and `.motion-anatomy` blocks.

### Category 2 — Experience Sharing Decks

#### 5. Experience Sharing deck (`ielts-experience-sharing.html`)
Elegant personal-presentation style. Uses Group I blocks (s73–s84) exclusively.
- **Fonts:** `'Lora'` (serif headings) + `'DM Sans'` (body)
- **Backgrounds:** warm cream (`var(--bg-warm)`)
- **Animations:** reveal animations with stagger delays (`.reveal`, `.stagger-1`…`.stagger-7`)
- **Decorative:** floating shapes (`.deco-circle`, `.deco-ring`, `.deco-dot`)
- **Components:** tip cards, big score displays, philosophy diagrams, QR contact cards, self-introduction cards
- **Counter animation:** JS `IntersectionObserver` animates numbers from `0.0` to target

### Category 3 — Invitation Emails

#### 6. Invitation Email (`email-skeleton.html`)
Table-based HTML email with inline CSS. Not a slide deck — a 600px-wide email card.
- **Design:** warm cream outer (`#f5f0e6`), white card (`#ffffff`), amber accents (`#ffc62a`)
- **Compatibility:** no `<style>` blocks, all inline CSS for email client safety
- **Output:** `tmp/invite-[event]-[role].html`
