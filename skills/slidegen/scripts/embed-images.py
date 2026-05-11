#!/usr/bin/env python3
"""
embed-images.py — Write image URIs for BPDU brand images to files.

Two modes:
  1. Base64 (default): encodes local PNGs to data URIs.
  2. URL (--url): writes hosted CDN URLs directly.

Base64 mode looks for images in this priority order:
  1. Repo root (cwd)  — BPDU_LOGO.png / BPDU_theme_image.png
  2. Bundled assets   — skills/slidegen/assets/  (relative to cwd)
  3. Script directory — assets/ next to this script

Usage:
  # Base64 mode (default)
  python3 skills/slidegen/scripts/embed-images.py

  # URL mode
  python3 skills/slidegen/scripts/embed-images.py --url \
    https://bpdebate.club/wp-content/uploads/2025/05/cropped-ChatGPT-Image-May-8-2025-10_18_18-PM.png \
    https://bpdebate.club/wp-content/uploads/2025/12/Untitled-design-3-1.png

Output files (written to cwd):
  .logo_uri.txt  — the full LOGO_URI string (one line)
  .theme_uri.txt — the full THEME_URI string (one line)
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
    args = sys.argv[1:]

    # URL mode
    if len(args) == 3 and args[0] == "--url":
        logo_uri  = args[1].strip()
        theme_uri = args[2].strip()

        logo_file  = Path.cwd() / ".logo_uri.txt"
        theme_file = Path.cwd() / ".theme_uri.txt"

        logo_file.write_text(logo_uri)
        theme_file.write_text(theme_uri)

        print(f"Logo URL written to: {logo_file.absolute()}  ({len(logo_uri):,} chars)", file=sys.stderr)
        print(f"Theme URL written to: {theme_file.absolute()}  ({len(theme_uri):,} chars)", file=sys.stderr)
        print("Use the inject one-liner to substitute __LOGO_URI__ / __THEME_URI__ placeholders.", file=sys.stderr)
        return

    # Base64 mode (default)
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
