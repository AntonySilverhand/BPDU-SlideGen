# BPDU SlideGen

> 中文版：[:link: README.zh-CN.md](README.zh-CN.md)

A set of [Claude Code](https://claude.ai/code) agent skills for generating single-file HTML slide presentations in the BP Debate Union visual style.

Think PowerPoint, but in HTML — keyboard-navigable, no build step, and easy to edit.

## Skills

| Skill | Trigger | What it does |
|-------|---------|--------------|
| `deep-analysis` | *"Analyze the motion..."* | Strategic, layered analysis of a BP motion (stakeholders, clashes, cases) |
| `slidegen` | *"Generate a slide deck on…"* | Produces a branded HTML presentation, case file, event host deck, experience sharing deck, simplicity deck, language course artifact, or invitation email |
| `imagegen` | *"Generate an illustration for…"* | Creates or edits images via the Gemini API in the BPDU flat-cartoon style |

## Output

Generated slide decks are **single `.html` files** (typical CDN decks are ~20–80 KB) with:
- Keyboard navigation (`←` `→` `Space`) and touch swipe
- Slide counter and progress bar
- Fixed BPDU brand bar on every slide
- Brand images loaded from `bpdebate.club` CDN (internet connection required)

Invitation emails are also single HTML files, but use table-based inline CSS for email-client compatibility instead of slide navigation.

> **v1.0.0 change:** Slide brand images are loaded from hosted URLs by default instead of being base64-embedded. Files are ~50× smaller. For offline use, run `embed-images.py` in base64 mode.

## Installation

### Step 1 — Install an AI coding agent

Pick one:

**[Claude Code](https://claude.ai/code)** (recommended — skills were built and tested here)
```bash
npm install -g @anthropic-ai/claude-code
```

**[Gemini CLI](https://github.com/google-gemini/gemini-cli)**
```bash
npm install -g @google/gemini-cli
```

**[OpenCode](https://opencode.ai)**
```bash
curl -fsSL https://opencode.ai/install | bash
# or: npm install -g opencode-ai
```

All three require **Node.js 20+**.

---

### Step 2 — Install the skills

Claude Code discovers plain skills from `~/.claude/skills`. This repository is currently a skills package, not a Claude Code marketplace plugin.

**Option A: Local symlink (Recommended for developers)**

Clone the repository, then link the skills so edits take effect immediately:
```bash
git clone https://github.com/AntonySilverhand/BPDU-SlideGen.git
cd BPDU-SlideGen
./scripts/symlink.sh
```

**Option B: Manual copy**

```bash
mkdir -p ~/.claude/skills
cp -R skills/deep-analysis skills/slidegen skills/imagegen ~/.claude/skills/
```

**Option C: Individual Skills (via agentskill.sh)**

If you use the `ags` CLI and only need specific skills:
```bash
ags install AntonySilverhand/BPDU-SlideGen@deep-analysis
ags install AntonySilverhand/BPDU-SlideGen@slidegen
# ... etc
```

---

### Step 3 — Image generation (optional)

The `imagegen` skill requires a Gemini API key:

```bash
export GEMINI_API_KEY="your-key-here"
```

Install Python dependencies:

```bash
python3 -m venv venv && source venv/bin/activate
pip install requests
```

## Scripts

| Script | Purpose |
|--------|---------|
| `skills/slidegen/scripts/catalog.py` | Prints the compact catalog of canonical slide template blocks. |
| `skills/slidegen/scripts/embed-images.py` | Writes brand image URIs to `.logo_uri.txt` / `.theme_uri.txt`. Script default encodes base64; use `--url` for CDN URLs. |
| `skills/slidegen/scripts/validate.py` | Post-generation validation: checks brand bar, `.illo`, `CONFIG`, file size, etc. |

### Image embedding modes

```bash
# CDN mode (recommended for v1.0+) — files stay ~20–80 KB
python3 skills/slidegen/scripts/embed-images.py --url \
  https://bpdebate.club/wp-content/uploads/2025/05/cropped-ChatGPT-Image-May-8-2025-10_18_18-PM.png \
  https://bpdebate.club/wp-content/uploads/2025/12/Untitled-design-3-1.png

# Base64 mode (script default) — for fully offline decks (~2.7 MB)
python3 skills/slidegen/scripts/embed-images.py
```

## Deck Types

| Type | Best for | Size |
|------|----------|------|
| **Reference** | Dense reading material, debate rules | ~30–50 KB |
| **Case File** | Motion briefing, argument cards, clash analysis | ~30–60 KB |
| **Event Host** | Live projection, one idea per slide, massive text | ~15–30 KB |
| **Experience Sharing** | Workshops, personal talks, storytelling, QR contact slides | ~30–60 KB |
| **Simplicity** | Ultra-minimal dark decks, keyword chips, quick intros | ~15–30 KB |
| **Language Course** | Vocabulary modules, bilingual lessons, image-card course pages | varies |
| **Invitation / Email** | HTML email invites for panelists, judges, guests | ~15–25 KB |

## Usage

Invoke any skill by describing what you want in the Claude Code prompt:

```
Analyze the motion "THBT social media companies do more harm than good to democracy"
```

```
Generate a case file deck on the motion "This House Would ban social media for under-16s"
```

```
Generate an event host deck for our weekly round on May 23
```

```
Generate an experience sharing deck about my IELTS journey
```

```
Generate a simplicity deck for a quick icebreaker on curiosity
```

```
Generate a Spanish language course artifact about Wenzhou weather
```

```
Generate a judge invitation email for the Bowen Cup tournament
```

```
Generate an illustration of students debating, BPDU style, 16:9
```

```
Validate tmp/my-deck.html
```

## Design System

The BPDU visual identity uses:
- **Primary accent:** `#F5C842` (warm amber)
- **Typography:** Poppins / Nunito / DM Sans
- **Style:** Warm, flat-cartoon illustrations; generous whitespace; card-based layouts
- **Government / Opposition:** Blue `#3B82F6` / Red `#EF4444` (BP debate convention)

Full spec in [`CLAUDE.md`](./CLAUDE.md).

---

## Changelog

### v2.0.0 — 2026-06-05

- **Natural-language auto-routing:** `slidegen` now infers output type, speed mode, and debate/general domain from normal user prompts.
- **Experience Sharing deck type:** Added a warm personal-presentation workflow for workshops, talks, storytelling decks, score slides, promo cards, and QR contact endings.
- **Simplicity deck type:** Added an ultra-minimal dark deck workflow with handwritten hero titles, massive centered question text, and keyword chips.
- **Language Course Artifact deck type:** Added course/vocabulary templates with image cards, bilingual or target-language sentence practice, mobile dots, and a sentence-review overlay.
- **Expanded template library:** Reorganized templates into `group-a.html` through `group-j.html`; the current catalog has 88 rendered blocks.
- **Debate strategy integration:** Added `debate-strategy.md` and routing rules for BP strategy guides, prep strategy, PM speeches, and closing-bench constraints.
- **Content completeness workflow:** Added Phase 0 brief generation, locked-brief rules, and stronger safeguards against dropping arguments or evidence to fit slide counts.
- **Canonical email skeleton:** Moved invitation email structure into `skills/slidegen/email-skeleton.html` for reuse.
- **Contributor and install docs:** Added `AGENTS.md`, refreshed both READMEs, and fixed the developer symlink script to link only maintained skills.

### v1.0.0 — 2026-05-11

- **CDN-first images:** Brand assets now load from `bpdebate.club` URLs instead of base64 embedding. Generated files are ~50× smaller (~20–80 KB vs ~2.7–5.3 MB).
- **`embed-images.py --url`:** New flag to write hosted URLs to `.logo_uri.txt` / `.theme_uri.txt`. Base64 mode still available for offline use.
- **`validate.py`:** New post-generation validation script. Checks brand bar, `.illo`/`.closing-illo`, `CONFIG` for event decks, no `display:none` on `.slide`, and file size sanity.
- **Invitation Letter / Email deck type:** Added branded HTML email generation for panelist/judge/participant invites.
- **SKILL.md hardening:** Added `allowed-tools`, `metadata`, negative constraints, and a "Before you finish" validation checklist.
- **Simplified workflow:** Removed the placeholder + injection step. URLs are written directly into generated HTML.
- **Batch-fixed existing files:** 16 existing HTML decks updated from base64 to URLs.
- **Removed deprecated skills:** `slide-theme` and `slide-export-tips` are no longer maintained. Theme application is now built into `slidegen`; export advice is superseded by the validation workflow.

### v0.x — pre-v1

- Initial skill set with `slidegen`, `deep-analysis`, `slide-theme`, `slide-export-tips`, and `imagegen`.
- Base64-embedded brand images for fully self-contained offline decks.
- Earlier template library for `slide-templates.html`; the current catalog has 88 rendered blocks.

---

## Authorization Disclaimer

This repository and its skills are open-source tools released under the MIT License.

**Content generated using these tools does not represent BP Debate Union unless explicitly published through official BPDU channels.**

BPDU's official communications are published at [bpdebate.club](https://bpdebate.club) and through verified BPDU social accounts. Any slide deck, document, or material produced by a third party using these tools — even if it carries BPDU branding elements — is not an official BPDU statement and should not be represented as one.

---

## License

MIT © 2026 BP Debate Union

See [`LICENSE`](./LICENSE) for full terms. Brand assets (`BPDU_LOGO.png`, `BPDU_theme_image.png`) are copyright BP Debate Union and may not be used to misrepresent affiliation with BPDU.
