---
name: triage
description: Differential-driven ticket clarification for radiology IT support — asks the one most discriminating question at a time until the ticket is routable, then produces a triage artifact with scope, timeline, differential, confidence, and a recommended queue. Use when a vague or incomplete ticket arrives, when deciding where something should be routed, when justifying a severity, or when assembling an escalation package. Triggers include /triage, "where should this go", "is this worth paging someone", "the study won't open".
---

# Ticket clarification

STUB — implements backlog E8.

## Differential

RIS configuration · interface · PACS · workstation · user. Maintain it visibly.
Ask only questions that separate remaining branches. Stop when a routing
decision is determinable, not when questions run out.

## Overnight behavior

When the working context is the night shift, ask the change-window question
first: scheduled maintenance, patching, engine restarts, purge and archive jobs
are disproportionately the cause, and often the answer is "the thing running
right now on purpose."

Escalation overnight means waking someone. The output is not just a queue name
but whether a page is warranted and what the person being woken needs to have
in hand.

## Output

Symptom · scope (one user / one modality / everyone) · timeline · differential
with confidence marks · recommended queue · SLA-vocabulary severity
justification citing the site profile.

## Not this skill

Message-level analysis. That is the separate forensics plugin — see
`docs/adr/0008-separate-forensics-plugin.md`. If a message needs decoding, say
so and stop rather than interpreting it.
