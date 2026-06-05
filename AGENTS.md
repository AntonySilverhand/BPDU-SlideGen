# Repository Guidelines

## Project Structure & Module Organization

This repository contains BPDU-focused agent skills for generating debate materials.

- `skills/slidegen/` holds the main slide-deck skill, including `SKILL.md`, `email-skeleton.html`, helper scripts, and reusable assets.
- `skills/slidegen/assets/templates/` contains per-group HTML template previews; prefer these over the monolithic `slide-templates.html` when editing deck blocks.
- `skills/deep-analysis/` contains the BP motion analysis skill.
- `skills/imagegen/` contains the image generation skill and its Python helper.
- `scripts/` contains repository-level utilities such as `symlink.sh`.
- Root `.html` files are generated examples or validation fixtures.

## Build, Test, and Development Commands

There is no package build step. Outputs are static HTML and Python scripts.

```bash
./scripts/symlink.sh
```
Symlinks local skills into the agent environment for development.

```bash
python3 skills/slidegen/scripts/catalog.py
```
Prints the slide template catalog for selecting canonical layout blocks.

```bash
python3 skills/slidegen/scripts/validate.py test-humor-debate.html
```
Validates generated slide HTML for required structure, brand bar, placeholders, and file-size warnings.

```bash
python3 skills/slidegen/scripts/embed-images.py --url <logo-url> <theme-url>
```
Updates slide image URI helpers for CDN-hosted assets. Run without `--url` only when offline base64 output is required.

## Coding Style & Naming Conventions

Use Python 3 with standard-library-first scripts and clear, small functions. Keep script entry points guarded by `if __name__ == "__main__":`. Use 4-space indentation for Python and 2-space indentation in HTML/CSS where practical.

Skill directories use lowercase hyphenated names, for example `deep-analysis` and `slidegen`. Generated decks should be descriptive lowercase HTML filenames such as `bowen-cup-host-deck.html`.

## Testing Guidelines

No formal unit test framework is configured. For slide-related changes, run `validate.py` against any edited or newly generated deck. For template changes, also run `catalog.py` to confirm the template library still parses. Keep generated examples small by using CDN URLs unless offline behavior is explicitly being tested.

## Commit & Pull Request Guidelines

Recent commits use short imperative or descriptive messages, for example `Refactor skill: auto-routing...`, `Fix image cropping...`, and `Update README for v1.0.0`. Follow that style: start with the action or changed area, then add a concise detail.

Pull requests should describe the affected skill or script, list validation commands run, and include screenshots or browser notes for visual template or deck changes. Link related issues when available.

## Security & Configuration Tips

Do not commit API keys. The optional image workflow reads `GEMINI_API_KEY` from the environment. Brand assets belong to BPDU; do not change usage terms or imply official BPDU endorsement beyond the repository disclaimer.
