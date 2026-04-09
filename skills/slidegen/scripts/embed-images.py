#!/usr/bin/env python3
"""
embed-images.py — Write base64 data URIs for BPDU brand images to files.

Looks for images in this priority order:
  1. Repo root (cwd)  — BPDU_LOGO.png / BPDU_theme_image.png
  2. Bundled assets   — skills/slidegen/assets/  (relative to cwd)
  3. Script directory — assets/ next to this script

Usage (run from repo root):
  python3 skills/slidegen/scripts/embed-images.py

Output files (written to cwd):
  .logo_uri.txt  — the full LOGO_URI string (one line, no variable name prefix)
  .theme_uri.txt — the full THEME_URI string (one line, no variable name prefix)

This avoids stdout truncation for large base64 strings. Read both files with
the Read tool and paste their contents as img src attributes.
"""

import base64
import sys
from pathlib import Path

SCRIPT_DIR = Path(__file__).parent.resolve()
ASSET_DIR  = SCRIPT_DIR.parent / "assets"

SEARCH_DIRS = [
    Path.cwd(),
    Path.cwd() / "skills" / "slidegen" / "assets",
    ASSET_DIR,
]

def find_image(filename: str) -> Path | None:
    for d in SEARCH_DIRS:
        p = d / filename
        if p.exists():
            return p
    return None

def encode(path: Path) -> str:
    data = path.read_bytes()
    b64  = base64.b64encode(data).decode("ascii")
    return f"data:image/png;base64,{b64}"

def main():
    logo_path  = find_image("BPDU_LOGO.png")
    theme_path = find_image("BPDU_theme_image.png")

    ok = True
    if not logo_path:
        print("Error: BPDU_LOGO.png not found in search path.", file=sys.stderr)
        ok = False
    if not theme_path:
        print("Error: BPDU_theme_image.png not found in search path.", file=sys.stderr)
        ok = False
    if not ok:
        print("Searched:", file=sys.stderr)
        for d in SEARCH_DIRS:
            print(f"  {d}", file=sys.stderr)
        sys.exit(1)

    logo_uri  = encode(logo_path)
    theme_uri = encode(theme_path)

    logo_file  = Path.cwd() / ".logo_uri.txt"
    theme_file = Path.cwd() / ".theme_uri.txt"

    logo_file.write_text(logo_uri)
    theme_file.write_text(theme_uri)

    print(f"Logo URI written to: {logo_file.absolute()}  ({len(logo_uri):,} chars)", file=sys.stderr)
    print(f"Theme URI written to: {theme_file.absolute()}  ({len(theme_uri):,} chars)", file=sys.stderr)
    print("Paste the full contents of each file as the img src attribute.", file=sys.stderr)

if __name__ == "__main__":
    main()
