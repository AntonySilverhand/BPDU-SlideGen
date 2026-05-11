# BPDU SlideGen

> 中文版：[:link: README.zh-CN.md](README.zh-CN.md)

A set of [Claude Code](https://claude.ai/code) agent skills for generating self-contained HTML slide presentations in the BP Debate Union visual style.

Think PowerPoint, but in HTML — fully keyboard-navigable, no build step, single-file output.

## Skills

| Skill | Trigger | What it does |
|-------|---------|--------------|
| `deep-analysis` | *"Analyze the motion..."* | Strategic, layered analysis of a BP motion (stakeholders, clashes, cases) |
| `slidegen` | *"Generate a slide deck on…"* | Produces a branded, single-file HTML presentation, case file, event host deck, or invitation email |
| `imagegen` | *"Generate an illustration for…"* | Creates or edits images via the Gemini API in the BPDU flat-cartoon style |

## Output

Every generated deck is a **single `.html` file** (~20–80 KB) with:
- Keyboard navigation (`←` `→` `Space`) and touch swipe
- Slide counter and progress bar
- Fixed BPDU brand bar on every slide
- Brand images loaded from `bpdebate.club` CDN (internet connection required)

> **v1.0.0 change:** Images are now loaded from hosted URLs instead of being base64-embedded. Files are ~50× smaller. For offline use, run `embed-images.py` in base64 mode.

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

**Option A: Built-in Claude Code Install (Recommended)**

Run this command inside the Claude Code prompt:
```
/plugins install https://github.com/AntonySilverhand/BPDU-SlideGen
```
*Note: This will install all skills in this repository.*

**Option B: Manual Symlink (For Developers)**

If you have cloned the repository locally and want to sync changes as you edit:
```bash
./scripts/symlink.sh
```

**Option C: Individual Skills (via agentskill.sh)**

If you only need specific skills:
```bash
ags install AntonySilverhand/BPDU-SlideGen@deep-analysis
ags install AntonySilverhand/BPDU-SlideGen@slidegen
# ... etc
```

**Manually**

Clone or download this repo and copy the `skills/` directory into your project root.

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
| `scripts/embed-images.py` | Writes brand image URIs to `.logo_uri.txt` / `.theme_uri.txt`. Default mode encodes base64; use `--url` for CDN URLs. |
| `scripts/validate.py` | Post-generation validation: checks brand bar, `.illo`, `CONFIG`, file size, etc. |

### Image embedding modes

```bash
# CDN mode (default, v1.0+) — files stay ~20–80 KB
python3 skills/slidegen/scripts/embed-images.py --url \
  https://bpdebate.club/wp-content/uploads/2025/05/cropped-ChatGPT-Image-May-8-2025-10_18_18-PM.png \
  https://bpdebate.club/wp-content/uploads/2025/12/Untitled-design-3-1.png

# Base64 mode — for fully offline decks (~2.7 MB)
python3 skills/slidegen/scripts/embed-images.py
```

## Deck Types

| Type | Best for | Size |
|------|----------|------|
| **Reference** | Dense reading material, debate rules | ~30–50 KB |
| **Case File** | Motion briefing, argument cards, clash analysis | ~30–60 KB |
| **Event Host** | Live projection, one idea per slide, massive text | ~15–30 KB |
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

### v1.0.0 — 2026-05-11

- **CDN-first images:** Brand assets now load from `bpdebate.club` URLs instead of base64 embedding. Generated files are ~50× smaller (~20–80 KB vs ~2.7–5.3 MB).
- **`embed-images.py --url`:** New flag to write hosted URLs to `.logo_uri.txt` / `.theme_uri.txt`. Base64 mode still available for offline use.
- **`validate.py`:** New post-generation validation script. Checks brand bar, `.illo`/`.closing-illo`, `CONFIG` for event decks, no `display:none` on `.slide`, and file size sanity.
- **Invitation Letter / Email deck type:** Added branded HTML email generation for panelist/judge/participant invites.
- **SKILL.md hardening:** Added `anti-triggers`, `allowed-tools`, `metadata`, negative constraints, and a "Before you finish" validation checklist.
- **Simplified workflow:** Removed the placeholder + injection step. URLs are written directly into generated HTML.
- **Batch-fixed existing files:** 16 existing HTML decks updated from base64 to URLs.
- **Removed deprecated skills:** `slide-theme` and `slide-export-tips` are no longer maintained. Theme application is now built into `slidegen`; export advice is superseded by the validation workflow.

### v0.x — pre-v1

- Initial skill set with `slidegen`, `deep-analysis`, `slide-theme`, `slide-export-tips`, and `imagegen`.
- Base64-embedded brand images for fully self-contained offline decks.
- 73-block template library (`slide-templates.html`).

---

## Authorization Disclaimer

This repository and its skills are open-source tools released under the MIT License.

**Content generated using these tools does not represent BP Debate Union unless explicitly published through official BPDU channels.**

BPDU's official communications are published at [bpdebate.club](https://bpdebate.club) and through verified BPDU social accounts. Any slide deck, document, or material produced by a third party using these tools — even if it carries BPDU branding elements — is not an official BPDU statement and should not be represented as one.

---

## License

MIT © 2026 BP Debate Union

See [`LICENSE`](./LICENSE) for full terms. Brand assets (`BPDU_LOGO.png`, `BPDU_theme_image.png`) are copyright BP Debate Union and may not be used to misrepresent affiliation with BPDU.
