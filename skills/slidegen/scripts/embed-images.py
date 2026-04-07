#!/usr/bin/env python3
# /// script
# dependencies = []
# ///
"""
embed-images.py — Output base64 data URIs for BPDU brand images.

Looks for images in this priority order:
  1. Repo root (cwd)  — BPDU_LOGO.png / BPDU_theme_image.png
  2. Bundled assets   — skills/slidegen/assets/  (relative to cwd)
  3. Script directory — assets/ next to this script

Usage (run from repo root):
  python3 skills/slidegen/scripts/embed-images.py

Output: two shell-style variable lines, easy to read into a prompt or script:
  LOGO_URI=data:image/png;base64,<...>
  THEME_URI=data:image/png;base64,<...>

The agent should paste these values as the `src` attribute of <img> tags in
generated HTML so the deck works on any device without external files.
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

    print(f"# Source: {logo_path}", file=sys.stderr)
    print(f"# Source: {theme_path}", file=sys.stderr)

    logo_uri  = encode(logo_path)
    theme_uri = encode(theme_path)

    print(f"LOGO_URI={logo_uri}")
    print(f"THEME_URI={theme_uri}")

if __name__ == "__main__":
    main()
