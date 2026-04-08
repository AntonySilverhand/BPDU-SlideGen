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
3.  **Update Brand Bar:** Ensure the `header.brand-bar` exists and follows the standard markup. The logo `src` must be the full data URI from `skills/slidegen/assets/BPDU_LOGO.b64` — never a relative file path, so the deck works on any device.
4.  **Update Navigation JS:** If navigation is broken or non-standard, replace with the BPDU-verbatim snippet from `CLAUDE.md`.
5.  **Asset Check:** Read `skills/slidegen/assets/BPDU_LOGO.b64` and `skills/slidegen/assets/BPDU_theme_image.b64` and paste their contents as inline `src` data URIs.

## Design Reference
Refer to `skills/slidegen/assets/slide-templates.html` for canonical CSS and HTML markup, and `CLAUDE.md` for the full design system specification.
- CSS variables and `:root` token block
- Transitions (`translateX` for Reference/Case, `scale` for Event Host)
- Stagger animations (`.a` class)

## Output
Provide the complete updated HTML code for the slide deck. Overwrite the original file if requested.
