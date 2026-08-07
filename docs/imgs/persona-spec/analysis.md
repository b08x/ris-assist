---
source: docs/PERSONA-SPEC.md
analyzed_by: baoyu-article-illustrator §Step 2
date: 2026-08-07
---

# Analysis — Persona Spec

## Content type
**Methodology / spec.** Not a narrative or tutorial — a behavioral contract for
an AI persona, organized as a three-axis taxonomy (Field / Tenor / Mode) with
tables, hard-boundary callouts, and a worked-validation exchange at the end.

## Purpose
**Visualization.** The reader (a contributor or auditor) needs to see at a
glance:
- How Field × Tenor × Mode partition the rules
- How confidence-mark evidence bars escalate
- How audience register reshapes one fact for three readers
- How "site-specific vs. generic domain" splits the source-of-truth

This is a spec meant to be referred to repeatedly. Illustrations earn their
keep if they make the structure navigable without re-reading the prose.

## Core arguments (the rules a visual must preserve)
1. **Field × Tenor × Mode is the partition.** Every rule belongs to exactly
   one axis. A rule that doesn't fit is two rules wearing one sentence.
2. **Confidence marks are load-bearing.** `confirmed` requires a quote or
   citation; `likely` states its evidence; `possible` states what would
   move it. Unmarked speculation is a defect.
3. **Two sources, never blurred.** Site-specific claims cite the site
   profile; generic domain claims cite `references/`. Mixing without marking
   is a defect, not a style issue.
4. **Audience register reshapes wording, not truth.** Clinical leads with
   the action the reader must take; Technical with the failure named
   precisely; Leadership with scope/duration/action.
5. **Drafts and recommends only.** Read-only is a hard boundary, not a
   stylistic preference. Patient-safety-adjacent or state-changing is
   flagged and handed to a human.

## Illustration positions

| # | Position in article | Why here | Type candidate |
|---|---|---|---|
| 1 | Top of doc, before "Field — domain scope" | The whole spec is partitioned by these three axes; show the partition as a triad before the reader parses prose | framework |
| 2 | After the "Confidence marking" table in Tenor | The 3-row evidence-bar table is dense; a ladder visualizes the escalation at a glance | infographic |
| 3 | After the "Audience register" table in Tenor | Three parallel example quotes already exist verbatim in the spec — perfect raw material for three side-by-side panels | comparison |
| 4 | After the "Two sources, never blurred" table in Field | The fork in the table is the entire point; a fork diagram makes the never-blur rule immediate | infographic |

These four positions map to four images. They are non-overlapping
(framework → three axes; ladder → one axis; register → three audiences;
fork → two sources) and cover the spec's four load-bearing tables.

## What to avoid
- **Do not illustrate "the analyst" as a person.** The spec is about a
  behavioral contract, not a character. Anthropomorphizing would mislead.
- **Do not decorate the boundary rules ("never executes", "no identified
  PHI") with imagery.** They are stop signs. A heavy border around them in
  prose is enough.
- **Do not invent labels.** Every label in a prompt must be drawn from the
  spec's own wording. The audience-register panel uses the spec's three
  example quotes verbatim; the confidence ladder uses the spec's three
  marks and their evidence bars verbatim.

## Density
**Balanced (4 images).** The spec is short and every table is a candidate.
Four is the right number: one per axis-as-structure plus one for the
register table (which is dense enough to warrant its own visual).
