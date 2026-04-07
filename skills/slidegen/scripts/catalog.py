#!/usr/bin/env python3
# /// script
# dependencies = []
# ///
"""
catalog.py — Print a compact catalog of all layout blocks in slide-templates.html.

Usage:
  python3 skills/slidegen/scripts/catalog.py [path/to/slide-templates.html]

Default path: slide-templates.html (relative to cwd, i.e. the SlideGen repo root).

Output columns (TSV):
  ID  |  BlockCode  |  Name  |  Background  |  CSS classes / notes
"""

import re
import sys
from pathlib import Path

def main():
    template_path = Path(sys.argv[1]) if len(sys.argv) > 1 else Path("slide-templates.html")
    if not template_path.exists():
        print(f"Error: {template_path} not found.", file=sys.stderr)
        print("Run from the SlideGen repo root, or pass the path as an argument.", file=sys.stderr)
        sys.exit(1)

    html = template_path.read_text(encoding="utf-8")

    # --- 1. Extract background colors from CSS block ---
    # Lines like:  #s4  { background: white  }  /* Stats Row */
    bg_map: dict[str, tuple[str, str]] = {}
    bg_pattern = re.compile(
        r'#(s\d+)\s*\{\s*background:\s*([^}]+?)\s*\}\s*/\*\s*([^*]+?)\s*\*/'
    )
    for m in bg_pattern.finditer(html):
        slide_id, bg_raw, comment = m.group(1), m.group(2).strip(), m.group(3).strip()
        # Normalise CSS variable names to human-readable
        bg_nice = (bg_raw
                   .replace("var(--bg-dark)", "dark")
                   .replace("var(--bg-warm)", "warm")
                   .replace("var(--primary)", "amber")
                   .replace("var(--bg)", "white")
                   .replace("white", "white"))
        bg_map[slide_id] = (bg_nice, comment)

    # --- 2. Extract slide sections ---
    # Each section: <section class="slide..." id="sN" data-tag="...">
    # We also grab the first .tpl-label text for the CSS hint.
    section_pattern = re.compile(
        r'<section[^>]+id="(s\d+)"[^>]+data-tag="([^"]+)"[^>]*>(.*?)</section>',
        re.DOTALL,
    )
    tpl_label_pattern = re.compile(r'<code[^>]*class="tpl-label[^"]*"[^>]*>(.*?)</code>', re.DOTALL)

    rows = []
    for m in section_pattern.finditer(html):
        sid = m.group(1)
        data_tag = m.group(2).strip()
        body = m.group(3)

        # tpl-label may have HTML entities / tags — strip tags, decode common entities
        css_hint = ""
        lm = tpl_label_pattern.search(body)
        if lm:
            raw = lm.group(1)
            raw = re.sub(r'<[^>]+>', '', raw)   # strip inner tags
            raw = raw.replace("&nbsp;", " ").replace("&gt;", ">").replace("&lt;", "<").replace("&amp;", "&")
            css_hint = re.sub(r'\s+', ' ', raw).strip()

        bg_nice, bg_comment = bg_map.get(sid, ("—", ""))

        rows.append((sid, data_tag, bg_nice, css_hint))

    if not rows:
        print("No slides found — check the template path.", file=sys.stderr)
        sys.exit(1)

    # --- 3. Print catalog ---
    col_widths = [
        max(len(r[0]) for r in rows),
        max(len(r[1]) for r in rows),
        8,  # bg
    ]

    header = (
        f"{'ID':<{col_widths[0]}}  "
        f"{'Block / Name':<{col_widths[1]}}  "
        f"{'BG':<{col_widths[2]}}  "
        f"CSS classes & notes"
    )
    print(header)
    print("-" * min(120, len(header) + 40))

    for sid, data_tag, bg, css_hint in rows:
        print(
            f"{sid:<{col_widths[0]}}  "
            f"{data_tag:<{col_widths[1]}}  "
            f"{bg:<{col_widths[2]}}  "
            f"{css_hint}"
        )

    print(f"\n{len(rows)} blocks total.")

if __name__ == "__main__":
    main()
