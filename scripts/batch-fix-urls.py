#!/usr/bin/env python3
"""Batch-fix existing HTML files: replace base64 data URIs with hosted URLs."""
import pathlib
import sys

LOGO_URL = "https://bpdebate.club/wp-content/uploads/2025/05/cropped-ChatGPT-Image-May-8-2025-10_18_18-PM.png"
THEME_URL = "https://bpdebate.club/wp-content/uploads/2025/12/Untitled-design-3-1.png"

def main():
    root = pathlib.Path(".")
    logo_b64 = (root / ".logo_uri.txt").read_text().strip()
    theme_b64 = (root / ".theme_uri.txt").read_text().strip()

    targets = list(root.glob("*.html")) + list(root.glob("tmp/*.html"))
    fixed = 0
    skipped = 0

    for p in targets:
        html = p.read_text()
        before = len(html)
        new_html = html.replace(logo_b64, LOGO_URL).replace(theme_b64, THEME_URL)
        after = len(new_html)

        if after == before:
            skipped += 1
            print(f"  SKIP  {p}  ({before:,} B) — no base64 found")
            continue

        p.write_text(new_html)
        fixed += 1
        saved = before - after
        print(f"  FIX   {p}  {before:,} B → {after:,} B  (saved {saved:,} B)")

    print(f"\nDone: {fixed} fixed, {skipped} skipped.")
    return 0

if __name__ == "__main__":
    sys.exit(main())
