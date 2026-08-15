---
name: troubleshoot
description: Differential-driven ticket clarification for radiology IT support — asks the one most discriminating question at a time until the ticket is routable, then produces a triage artifact with scope, timeline, differential, confidence, and a recommended queue. Use when a vague or incomplete ticket arrives, when deciding where something should be routed, when justifying a severity, or when assembling an escalation package. Triggers include /troubleshoot, "where should this go", "is this worth paging someone", "the study won't open".
---

# Ticket clarification

Implements backlog E8.

Persona: `${CLAUDE_PLUGIN_ROOT}/PERSONA-SPEC.md`. Confidence marking (`confirmed`/`likely`/
`possible`), cite-or-decline, and the differential's three process types
(happened / believed / structurally true) are defined there — this skill
applies them, it doesn't redefine them.

## Differential

Five branches. Maintain the list visibly across turns — show which branches
remain live and which a question ruled out, not just the final answer.

| Branch | Typically looks like | First-pass discriminator |
|---|---|---|
| **RIS configuration** | Order stuck at a stage no interface touches (never scheduled, scheduling rule mismatch) | Does the order exist in RIS at all, and at what status? (`explainer` skill's `order-lifecycle.md` stages) |
| **Interface** | Order/report visible on one side of a link, not the other (RIS shows scheduled, modality worklist empty) | Is the same symptom happening for *every* order through that link, or just this one? All-or-nothing points here. |
| **PACS** | Images/orders reach PACS but don't display, or a listener/node is down | Is this reproducible on more than one workstation? If yes, PACS-side; if only one, workstation branch. |
| **Workstation** | Single machine, single user, everyone else fine | Does the same user see the problem on a different workstation? Confirms user vs. workstation. |
| **User** | Procedural — wrong worklist filter, wrong patient context, training gap | Ruled in only after workstation and PACS are ruled out, or when the symptom description is procedural from the start ("I can't find the study" vs. "the study won't load"). |

Ground each branch's discriminating question in the domain reference it
maps to (`explainer/references/`) rather than a generic troubleshooting
script — a discriminator that isn't actually tied to how this site's
topology behaves isn't discriminating, it's guessing with confidence.

## Selecting the next question

At each turn, the live branches are whatever the differential hasn't ruled
out yet. Pick the question whose two possible answers would rule out the
most branches, not the question that's easiest to ask or most obviously
"next." A useful check: if you can predict the same next question regardless
of how the last one was answered, it wasn't actually discriminating — it was
sequence, not triage.

Scope (one user / one modality / everyone) is almost always the highest-value
early split — it eliminates workstation/user immediately if the answer is
"everyone," and eliminates PACS/interface immediately if the answer is "one
user, one workstation, everyone else fine." Ask it early unless the ticket
already states it.

**Stop condition is routable, not exhausted.** Once one branch remains live
at `likely` or better and the others are ruled out or clearly subordinate,
stop and produce the artifact — do not keep asking toward `confirmed` for
its own sake. A `likely`-confidence routing with the reasoning shown is a
legitimate, complete output.

## Overnight behavior

When the working context is the night shift, ask the change-window question
first: scheduled maintenance, patching, engine restarts, purge and archive jobs
are disproportionately the cause, and often the answer is "the thing running
right now on purpose." This inverts the usual differential order — it's a
prior drawn from an experienced overnight analyst's institutional knowledge of
the account, not a generic starting point, and it still gets a `likely`/
`possible` mark like any other inference rather than being treated as
confirmed (`PERSONA-SPEC.md`, "Experience is not a citable source").

Escalation overnight means deciding whether to page the on-call senior
analyst, who may be slow to reach — not handing off to someone readily
available. The output is not just a queue name but whether a page is
warranted and what the person being woken needs to have in hand.

## Output

Symptom · scope (one user / one modality / everyone) · timeline · differential
with confidence marks (per persona spec) · recommended queue · SLA-vocabulary
severity justification citing the site profile — or stating that no matching
tier exists.

Worked example, using the fictional `examples/site-profile.example.yaml`:

> **Symptom:** Orders not appearing on modality worklist.
> **Scope:** All modalities, all users — `confirmed` (reporter stated
> "nobody can see new orders").
> **Timeline:** Started approx. 02:14, ongoing.
> **Differential:**
> - Interface (RIS-to-PACS order interface) — `likely`. Sitewide,
>   all-modality scope rules out workstation and user branches; RIS shows
>   orders scheduled (order exists past the RIS-configuration branch).
> - RIS configuration — ruled out. Orders reach "scheduled" status
>   normally per the reporter.
> - PACS / workstation / user — ruled out by scope (sitewide, not
>   single-machine or single-user).
> **Recommended queue:** Tier 2 — interface analyst, per
> `escalation_matrix`.
> **Severity:** Sev 1 — "sitewide or all-modality impact, no workaround
> available" per `sla_tiers`. Workaround (paper requisitions) exists per
> `downtime_procedures`, which the severity definition doesn't exclude —
> flagged as a judgment call for the human, not resolved silently.

## Known-error matching

Backlog E8.7. Connected mode (matching against live KB articles and open
problem records) is blocked on DEP-1 (ServiceNow MCP read access). Manual
mode works now: if the user pastes existing KB article titles/summaries or
says "check against these," compare the current symptom/differential
against what's pasted and note a possible match with the same confidence
discipline as everything else — `possible` unless the match is close enough
to state as `likely`. Do not claim a KB search happened if nothing was
actually provided to search.

## Escalation package

Backlog E8.5. When a ticket escalates, assemble: the triage artifact above,
what's been ruled out and why (the differential's dead branches, not just
the live one), and any environment details the user has stated. This is the
same artifact as `/troubleshoot`'s normal output plus the ruled-out reasoning made
explicit — not a separate format to construct from scratch.

## Not this skill

Message-level analysis. That is the separate forensics plugin — see
`docs/adr/0008-separate-forensics-plugin.md`. If a message needs decoding, say
so and stop rather than interpreting it.
