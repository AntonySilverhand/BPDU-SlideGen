#!/usr/bin/env python3
"""validate.py — Post-generation validation for slidegen output.

Checks a generated HTML file for structural correctness.
Exit code 0 = pass, non-zero = fail.

Usage:
  python3 skills/slidegen/scripts/validate.py tmp/deck.html
"""
import pathlib
import re
import sys

def validate(path: pathlib.Path) -> tuple[list[str], list[str]]:
    """Returns (errors, warnings)."""
    errors: list[str] = []
    warnings: list[str] = []
    html = path.read_text()

    # 1. No remaining placeholders (hard fail)
    if "__LOGO_URI__" in html:
        errors.append("Placeholder __LOGO_URI__ still present — run inject step.")
    if "__THEME_URI__" in html:
        errors.append("Placeholder __THEME_URI__ still present — run inject step.")

    # 2. Brand bar exists (hard fail)
    if '<header class="brand-bar"' not in html:
        errors.append("Missing brand bar (<header class=\"brand-bar\">).")

    # 3. Every .slide has padding-top to clear brand bar (hard fail)
    slide_sections = re.findall(r'<section[^>]*class="[^"]*slide[^"]*"[^>]*>', html)
    if not slide_sections:
        errors.append("No <section class=\"slide\"> elements found.")
    else:
        # Check CSS for padding-top: var(--bar) or explicit padding-top
        if "padding-top: var(--bar)" not in html and "padding-top:" not in html:
            warnings.append("Slides may not clear brand bar — no padding-top rule found.")

    # 4. .illo and .closing-illo exist (warn, not fail — some decks omit them)
    if '<div class="illo">' not in html:
        warnings.append("Missing title slide illustration (.illo).")
    if '<div class="closing-illo">' not in html:
        warnings.append("Missing closing slide illustration (.closing-illo).")

    # 5. For event decks: CONFIG object exists (hard fail)
    if 'class="slide"' in html and ("event" in html.lower() or "host" in html.lower()):
        if "const CONFIG" not in html and "var CONFIG" not in html:
            # Only flag if it looks like an event deck (has .hero or scale transitions)
            if "scale(0.97)" in html or "class=\"hero\"" in html:
                errors.append("Event deck missing CONFIG object.")

    # 6. No display:none on .slide elements (hard fail)
    if re.search(r'\.slide\s*\{\s*[^}]*display\s*:\s*none', html):
        errors.append("display:none found on .slide — breaks transitions.")

    # 7. File size sanity check (warn)
    size = path.stat().st_size
    if size > 500_000:
        warnings.append(f"File is {size:,} B (> 500 KB). Consider using hosted URLs instead of base64.")

    return errors, warnings

def main() -> int:
    if len(sys.argv) < 2:
        print("Usage: python3 validate.py <file.html>", file=sys.stderr)
        return 2

    path = pathlib.Path(sys.argv[1])
    if not path.exists():
        print(f"Error: file not found: {path}", file=sys.stderr)
        return 2

    errors, warnings = validate(path)
    size = path.stat().st_size

    if warnings:
        for w in warnings:
            print(f"  ⚠ {w}")

    if errors:
        print(f"FAIL  {path}  ({len(errors)} issue(s))")
        for e in errors:
            print(f"  ✗ {e}")
        return 1
    else:
        print(f"PASS  {path}  ({size:,} B)")
        return 0

if __name__ == "__main__":
    sys.exit(main())
