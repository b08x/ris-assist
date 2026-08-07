---
source: docs/PERSONA-SPEC.md
type: mixed (framework + infographic + comparison)
density: balanced
image_count: 4
style: minimal-flat
palette: macaron
language: en
aspect_default: landscape
---

# Outline — Persona Spec illustrations

## Illustration 1
**Position**: top of doc, before "## Field — domain scope"
**Purpose**: Make the three-axis partition (Field / Tenor / Mode) visible
before the reader parses any prose. Every rule in the spec belongs to
exactly one axis; the triad is the load-bearing structure.
**Visual content**: Three connected nodes labeled FIELD / TENOR / MODE.
Each node carries one short descriptor from the spec:
- Field — "domain scope (what the persona knows)"
- Tenor — "operational stance (how it relates)"
- Mode — "execution framework (how it's organized)"
A connecting line between each pair carries the rule from the spec:
"A rule that doesn't fit is two rules wearing one sentence."
**Filename**: 01-framework-field-tenor-mode.png

## Illustration 2
**Position**: after the "Confidence marking" table in Tenor
**Purpose**: Visualize the evidence-bar escalation so the difference between
`confirmed` / `likely` / `possible` is not just a table row but a step.
**Visual content**: Three ascending steps (ladder), labeled with the spec's
verbatim marks and evidence-bar text:
- bottom step: `possible` — "Plausible given the differential, not yet
  supported. State what would move it to `likely`."
- middle step: `likely` — "Consistent with available evidence, not directly
  stated. State what evidence, and what would confirm it."
- top step: `confirmed` — "Directly stated in the ticket, worklog, or a
  cited source. Quote or cite it."
At the foot of the ladder: "Unmarked speculation is a defect."
**Filename**: 02-infographic-confidence-ladder.png

## Illustration 3
**Position**: after the "Audience register" table in Tenor
**Purpose**: Make the audience-register principle concrete by placing the
spec's three verbatim example quotes side by side. Same underlying fact,
reshaped by who's reading — never by what's true.
**Visual content**: Three vertical panels labeled CLINICAL / TECHNICAL /
LEADERSHIP. Each panel carries the spec's verbatim example quote under the
matching "leads with" header:
- CLINICAL (leads with: "The action they must take"):
  "Orders will not reach the modality worklist — use paper requisitions
  until further notice."
- TECHNICAL (leads with: "The failure, named precisely"):
  "ORM_O01 delivery to PACS is failing since 02:14; interface engine shows
  queue depth climbing."
- LEADERSHIP (leads with: "Scope, duration, what's being done, in that
  order"):
  "Imaging orders have been delayed sitewide for 40 minutes; engineering is
  restarting the interface engine now."
Below all three: "Same fact. Different reader. The truth is unchanged."
**Filename**: 03-comparison-audience-register.png

## Illustration 4
**Position**: after the "Two sources, never blurred" table in Field
**Purpose**: Make the source-of-truth fork immediate. Site-specific claims
cite the site profile; generic domain claims cite `references/`. Mixing
without marking is a defect.
**Visual content**: A fork with two labeled branches from a single trunk
labeled "claim". Left branch: "site-specific" → ends at a box labeled
"SITE PROFILE" with the spec's rule: "Not in your site profile — never
invented." Right branch: "generic domain" → ends at a box labeled
"`references/`" with the spec's rule: "Answer generically, say so."
Below the fork: "Mixing without marking which is which is a defect, not a
style issue."
**Filename**: 04-infographic-two-sources.png

## Insertion order in PERSONA-SPEC.md
1. After the opening paragraph, before `## Field — domain scope`
2. After the "Confidence marking" table, before `**Cite-or-decline:**`
3. After the "Audience register" table, before `**Voice standards:**`
4. After the "Two sources, never blurred" table, before `**Experience is not a citable source.**`

## Style consistency notes
- All four illustrations use `style=minimal-flat` and `palette=macaron`.
  Same visual language so the four images read as a set.
- All four use the spec's verbatim labels. No paraphrase, no invented
  numbers. The three audience-register quotes come straight from the
  source.
- All four use `landscape` aspect (16:9) for layout consistency in a
  markdown doc.
