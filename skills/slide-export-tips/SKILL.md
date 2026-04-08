---
name: slide-export-tips
description: Provides advice on printing or exporting BPDU HTML slide decks to PDF.
---

# SlideExportTips: BPDU Presentation Export Guide

Advise users on the best practices for printing or exporting BPDU HTML slide presentations to PDF.

## Input Context
- **Target File:** The HTML presentation file.
- **Export Goal:** Clean, high-quality PDF.

## Export Instructions
1.  **Open File:** Use Chrome or a Chromium-based browser (Edge, Arc) for the most accurate rendering.
2.  **Toggle Print Styles (Optional):** If the deck has print-specific CSS, ensure it's active.
3.  **Print to PDF Settings:**
    - **Layout:** Landscape.
    - **Margins:** None or Minimum.
    - **Background Graphics:** Check "Background graphics" (Crucial for BPDU colors and images).
    - **Headers & Footers:** Uncheck "Headers and footers" (The brand bar and slide counter are enough).
    - **Scale:** Default or 100%.
4.  **Sequential Printing:** Since the slides are `position: absolute`, the standard browser "Print" might only see the active slide.
    - **Advice:** For a full deck PDF, it's often best to use a specialized tool or manually step through and print, or modify the CSS temporarily to `position: static` for printing.
    - **Advanced Tip:** Some BPDU decks include `@media print { .slide { position: static; opacity: 1; transform: none; display: block; break-after: page; } }` rules. Check the CSS for these rules.

## Design Reference
Check the target deck's `<style>` block for any existing `@media print` rules.
- Ensure the `brand-bar` is `display: none` or `position: relative` for printing if it overlaps.
- Hide `nav-btn`, `key-hint`, and `progress` bars.

## Output
A clear, step-by-step guide for the user to export their specific deck to PDF.
