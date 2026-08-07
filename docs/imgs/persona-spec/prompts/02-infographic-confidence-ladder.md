---
illustration: 02-infographic-confidence-ladder
type: infographic
style: minimal-flat
palette: macaron
aspect: 16:9
source_labels_from: docs/PERSONA-SPEC.md (Confidence marking table)
---

# Prompt 02 — Confidence mark evidence-bar ladder

## ZONES
- A three-step ladder ascending left-to-right. Each step is a horizontal
  rectangle. The top step is the narrowest (highest standard). The bottom
  step is the widest (lowest bar to clear).
- A vertical arrow on the far right of the ladder points upward, labeled
  "evidence bar" along its length.
- A footer band runs the full width below the ladder, separated by a thin
  horizontal rule.

## LABELS
- Top step label (verbatim mark from spec): `confirmed`
- Top step body text (verbatim evidence bar from spec):
  "Directly stated in the ticket, worklog, or a cited source. Quote or cite it."
- Middle step label: `likely`
- Middle step body text:
  "Consistent with available evidence, not directly stated. State what evidence, and what would confirm it."
- Bottom step label: `possible`
- Bottom step body text:
  "Plausible given the differential, not yet supported. State what would move it to `likely`."
- Right-edge vertical arrow label: "evidence bar"
- Footer band text (verbatim from spec):
  "Unmarked speculation is a defect."

## COLORS (macaron palette)
- `confirmed` step (top): soft mint green (#B8E6D2 approx) — highest
  standard, calm
- `likely` step (middle): soft peach (#FFD4B8 approx) — moderate
- `possible` step (bottom): soft lavender (#D4C5F9 approx) — exploratory
- Arrow: muted slate (#6B7280 approx)
- Footer band: light cream (#F5F1E8 approx)
- Step text: dark slate (#374151 approx)
- Step labels (`confirmed`, etc.) render in monospace (JetBrains Mono
  style) to signal they're code-like markers, not prose words.
- Background: off-white (#FAFAF5 approx)

## STYLE
- Flat infographic. Clean rectangles, no shadows.
- Sans-serif body (Inter / SF Pro); monospace for the three marks.
- Generous padding inside each step so the body text is legible.
- Visual register: documentation table, not poster.

## ASPECT
16:9 landscape. Ladder reads left-to-right with the arrow on the right;
footer band below.

## NEGATIVE CONSTRAINTS
- No people, no hands, no clocks.
- No checkmarks or x-marks (would imply good/bad; the marks are evidence
  thresholds, not pass/fail).
- No emojis.
