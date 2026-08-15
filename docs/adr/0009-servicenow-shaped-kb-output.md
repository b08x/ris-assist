# ADR-0009 — ServiceNow-shaped KB output replaces the KCS markdown template

Status:   Accepted
Date:     2026-08-07

## Context

E7.1 said "adapt the existing ServiceNow KB generator skill into the plugin;
conform output to KCS template shape from site profile." What actually shipped
in 1.0.0 was the second half. `skills/knowledge/references/kb-template.md` was
a KCS-shaped markdown template — problem, environment, resolution, cause — and
nothing from the ServiceNow generator came across: not the HTML import format,
not the triage-first ordering, not the HTML → DOCX renderer. The epic was
marked done on the half that was cheap.

The gap that leaves is not cosmetic. The article a night analyst produces at
04:00 has to end up in ServiceNow, and ServiceNow takes a Word import. A
markdown draft in a chat window means someone re-keys it later. Later is the
documentation sprint that never happens — the exact failure the skill opens by
arguing against. The skill's own premise was undercut by its output format.

Separately, the KCS section order is a knowledge-taxonomy order, not a working
order. Problem → environment → resolution → cause is how an article is
catalogued. It is not how the ticket was worked, and it is not the order the
next analyst reads it in at 3 AM, who wants scope first and cause last.

## Decision

The KCS markdown template is retired. `skills/knowledge` drafts in a
triage-first HTML shape that renders to ServiceNow-importable `.docx` via
`skills/knowledge/scripts/html_to_docx.py`.

The KCS *fields* are all retained as required sections — symptom, resolution,
cause with a confidence mark, verification, related. What changed is their
order and their container, not whether they are mandatory.

The step ladder is ordered by this plugin's own triage differential
(`skills/troubleshoot/SKILL.md`: scope, then workstation/user, application, interface,
advanced) rather than by the source skill's hardware-oriented layers
(physical → OS → driver). A KB article and a triage session on the same
incident now read in the same order.

`/draft-kb` gains `Bash` in `allowed-tools`, for the render step only.

## Alternatives considered

**Add ServiceNow rendering as an export stage after the KCS draft.** Rejected,
though it was the closer call of the three. It keeps two article shapes alive —
one authored, one exported — and every future change has to be made twice or
the two drift. It also does not fix the ordering problem, since the exported
article inherits the KCS section order.

**Offer both shapes and let the user pick per article** — incident write-up
versus reusable procedure. Rejected as scope inflation (G7). Two shapes is two
templates, two checklists, and a routing question asked at the worst moment.
If a real second genre emerges from use, it can be added then, with evidence.

**Keep the KCS template and skip DOCX entirely**, on the grounds that connected
mode (DEP-1) will eventually push articles through the API and make the file
moot. Rejected. DEP-1 has no date, manual mode is what exists, and building
around a dependency that may not land is how manual mode ended up
half-finished the first time.

**Port the source skill's hardware-oriented ladder unchanged.** Rejected as
vocabulary import (G2). Physical → OS → driver is the right ladder for a
monitor that will not power on and the wrong one for an order that never
reached the modality worklist. The plugin already has a differential validated
against its own domain; the article should use it.

## Consequences

**Easier:** the analyst's output is the artifact that gets uploaded. Article
order matches triage order, so an article can be drafted directly from a
`/troubleshoot` artifact without re-sequencing. The metadata line carries a version,
which is what E7.5's stale-article flagging keys on. Rendering is deterministic
code, consistent with ADR-0001 — the model drafts, the script renders, and the
script does not interpret content.

**Harder:** the repository now ships executable code, which it previously did
not (`CLAUDE.md` said markdown plus one non-functional demo script). That means
a Python dependency surface — `python-docx`, `Pillow` — pinned in a PEP 723
header, and a class of bug that cannot be found by reading prose for internal
consistency. `/draft-kb` now requires `Bash`, a real permission expansion for a
plugin whose pitch is that it does not execute; the boundary is stated in the
command file and in the skill's "Not this skill" section, and it is a line
worth watching rather than assuming holds.

**Committed to:** HTML as the authored form. Anyone tuning a site-specific
article template is now writing HTML, not markdown — a higher floor for
contributors, accepted because the import format is not negotiable and a
markdown-to-HTML intermediate would put a translation step between the author
and what ServiceNow receives.

**Known limit, stated rather than solved:** the renderer embeds an image only
from a base64 data URI. A bare image ID becomes a visible grey placeholder and
is reported on the console and in outstanding items. Screenshots of production
systems are presumed to contain patient data and are the site's call under its
own policy — this plugin does not redact (`docs/DATA-PROVENANCE.md`).

**Documentation:** `PERSONA-SPEC.md`'s per-skill output table, `README.md`,
`AGENTS.md`, `DEMO-full.md` Turn 4, and both example articles are updated to
the new shape. The two example articles are converted rather than kept as KCS
specimens — a stale example is a worse reference than no example.
