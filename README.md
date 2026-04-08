# BPDU SlideGen

> 中文版：[:link: README.zh-CN.md](README.zh-CN.md)

A set of [Claude Code](https://claude.ai/code) agent skills for generating self-contained HTML slide presentations in the BP Debate Union visual style.

Think PowerPoint, but in HTML — fully keyboard-navigable, no build step, single-file output.

## Skills

| Skill | Trigger | What it does |
|-------|---------|--------------|
| `deep-analysis` | *"Analyze the motion..."* | Strategic, layered analysis of a BP motion (stakeholders, clashes, cases) |
| `slidegen` | *"Generate a slide deck on…"* | Produces a branded, single-file HTML presentation from a topic or outline |
| `slide-theme` | *"Apply the BPDU theme to…"* | Updates an existing HTML deck to match the BPDU design system |
| `slide-export-tips` | *"How do I export this to PDF?"* | Advises on printing / PDF export from generated HTML |
| `imagegen` | *"Generate an illustration for…"* | Creates or edits images via the Gemini API in the BPDU flat-cartoon style |

## Output

Every generated deck is a **single `.html` file** with:
- Keyboard navigation (`←` `→` `Space`) and touch swipe
- Slide counter and progress bar
- Fixed BPDU brand bar on every slide
- Fully embedded assets (no external dependencies beyond Google Fonts CDN)

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

## Usage

Invoke any skill by describing what you want in the Claude Code prompt:

```
Analyze the motion "THBT social media companies do more harm than good to democracy"
```

```
Generate a case file deck on the motion "This House Would ban social media for under-16s"
```

```
Generate an illustration of students debating, BPDU style, 16:9
```

```
Apply the BPDU theme to my existing presentation.html
```

## Design System

The BPDU visual identity uses:
- **Primary accent:** `#F5C842` (warm amber)
- **Typography:** Poppins / Nunito / DM Sans
- **Style:** Warm, flat-cartoon illustrations; generous whitespace; card-based layouts
- **Government / Opposition:** Blue `#3B82F6` / Red `#EF4444` (BP debate convention)

Full spec in [`CLAUDE.md`](./CLAUDE.md).

---

## Authorization Disclaimer

This repository and its skills are open-source tools released under the MIT License.

**Content generated using these tools does not represent BP Debate Union unless explicitly published through official BPDU channels.**

BPDU's official communications are published at [bpdebate.club](https://bpdebate.club) and through verified BPDU social accounts. Any slide deck, document, or material produced by a third party using these tools — even if it carries BPDU branding elements — is not an official BPDU statement and should not be represented as one.

---

## License

MIT © 2026 BP Debate Union

See [`LICENSE`](./LICENSE) for full terms. Brand assets (`BPDU_LOGO.png`, `BPDU_theme_image.png`) are copyright BP Debate Union and may not be used to misrepresent affiliation with BPDU.
