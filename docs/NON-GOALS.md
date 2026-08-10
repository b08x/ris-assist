# Non-Goals

What RIS Assist will not do, stated as plainly as what it will. These are design
commitments, not disclaimers — each one is enforced in skill instructions and
persona rules, and a change to any of them is an ADR-level decision.

## It does not execute

RIS Assist drafts, decodes, and recommends. It has no path to a state-changing
operation and is not intended to acquire one.

Specifically out of scope: replaying or resending messages, purging or
reordering queues, editing orders or reports, modifying interface
configuration, changing ticket state in the ITSM system beyond explicitly
scoped knowledge-article submission, and touching any production system.

Replay-safety guidance is advisory. The authorization is a human's, every time.

## It does not guess

An unrecognized segment, a site-local Z-segment with no reference entry, or a
field the site profile does not describe is reported as unknown. The persona
rule is cite-or-decline: a process claim names its source (SOP, SLA definition,
site profile) or states that no source exists.

Plausible-sounding invention is the specific failure this project is built to
avoid. A confidently wrong field mapping in a triage context does more damage
than no tool at all.

## It does not blur observation and inference

Every output separates what the message or record *says* from what RIS Assist
*concludes*, and every conclusion carries a confidence mark — `confirmed`,
`likely`, or `possible`. Unmarked speculation is a defect, not a style
preference.

## It does not make patient-safety-adjacent calls

Anything touching clinical workflow risk, patient identity resolution, or
diagnostic availability is flagged, packaged with the relevant evidence, and
handed to a human. RIS Assist does not weigh clinical trade-offs.

## It does not parse HL7 messages

Message forensics is a separate plugin, not a missing feature. It waits on data
access and on a symbolic parse layer, and shipping a model-interpreted version
in the meantime would be the exact behavior this project argues against. See
[ADR-0008](adr/0008-separate-forensics-plugin.md) and
Part 2 of [ROADMAP.md](ROADMAP.md).

## It is not a clinical tool

It does not interpret images, inform diagnosis, or produce anything intended
for clinical decision-making. It operates on information-system metadata and
support process — not on patient care.

## It does not handle identified PHI

The de-identification gate is deterministic script code, applied at ingress.
Workflows that genuinely require live patient data belong on platforms your
organization's compliance function has approved for that purpose. This plugin
is not that platform, and no configuration option makes it one.

## It does not carry your site's configuration into the world

Site profiles are written locally, outside the plugin directory, and never
enter this repository. See [DATA-PROVENANCE.md](DATA-PROVENANCE.md).

## It does not replace the senior analyst

The onboarding and explainer capabilities exist to reduce the number of
interruptions, not to substitute for judgment, escalation relationships, or
institutional knowledge that has never been written down. Where RIS Assist helps,
it helps by making that knowledge easier to capture — not by pretending to
already have it.
