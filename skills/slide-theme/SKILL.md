---
name: slide-theme
description: Applies or modifies the BPDU theme (branding, colors, typography) on an existing HTML slide deck.
---

# SlideTheme: BPDU Theme Applicator

Update an existing HTML slide deck to match the BP Debate Union (BPDU) design system.

## Input Context
- **Target File:** The HTML file to be updated.
- **Goal:** Ensure branding (logo, bar, fonts, colors) is consistent with the BPDU style.

## Key BPDU Design Standards
- **Primary Color:** `#F5C230` (Amber).
- **Secondary Colors:** Government (Blue: `#3B82F6`), Opposition (Red: `#EF4444`).
- **Brand Bar:** Must include `BPDU_LOGO.png`, "BP Debate Union", and dynamic slide tag.
- **Typography:** 'Poppins' or similar rounded sans-serif.

## Implementation Steps
1.  **Read Target File:** Analyze the existing structure.
2.  **Update CSS:** Ensure `:root` tokens match the BPDU palette.
3.  **Update Brand Bar:** Ensure the `header.brand-bar` exists and follows the standard markup.
4.  **Update Navigation JS:** If navigation is broken or non-standard, replace with the BPDU-verbatim snippet from `CLAUDE.md`.
5.  **Asset Check:** Ensure `BPDU_LOGO.png` and `BPDU_theme_image.png` are referenced with relative paths.

## Design Reference
Refer to `bp-debate-rules.html` for the canonical theme implementation.
- CSS variables
- Transitions (`translateX` for Reference/Case, `scale` for Event Host)
- Stagger animations (`.a` class)

## Output
Provide the complete updated HTML code for the slide deck. Overwrite the original file if requested.
