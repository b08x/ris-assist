# Register guide

Backlog E6.13. The rule table lives in `${CLAUDE_PLUGIN_ROOT}/PERSONA-SPEC.md` (Tenor —
Audience register); this file is worked examples, not a second copy of the
rule. Read the rule there first; use this to see it applied.

The core discipline: **the facts don't change, the framing does.** Every
example below describes the same incident three ways. If two audience
drafts of the same incident could have their bodies swapped without anyone
noticing, the register isn't actually differentiated — that's a defect, not
economy of effort.

## Worked example — unplanned outage

Underlying facts: RIS-to-PACS order interface down since 02:14. Orders are
not reaching the modality worklist. Cause not yet confirmed. Workaround:
paper requisitions per the site's downtime procedure. Next update in 30
minutes.

**Clinical (radiologists) — leads with the action:**

> Orders are not reaching the PACS worklist as of 02:14. Read direct from
> PACS worklist per Imaging Downtime Packet (Form IMG-14). Next update by
> 02:45.

Three lines. No interface name, no cause. The profile's own note that
radiologists read the first two lines is why this stays short — anything
past "what do I do" is a cost, not a courtesy.

**Technical (IT/NOC) — leads with the failure:**

> RIS-to-PACS order interface down since 02:14 (INC0004821). Orders queuing
> at the interface engine, not reaching PACS worklist. Cause: `suspected`
> engine-side, not yet confirmed. Next update 02:45.

Interface named precisely, ticket reference present, cause explicitly
marked `suspected` rather than stated as fact.

**Leadership — leads with scope, duration, and action, in that order:**

> Imaging order delivery has been delayed sitewide since 02:14 (31 minutes
> as of this update). All modalities affected; staff are working from
> paper requisitions per standard downtime procedure. Engineering is
> investigating the interface engine. Next update 02:45.

Scope first ("sitewide," "all modalities") because that's what leadership
needs to decide whether to escalate further — the technical cause is
present but subordinate.

## Worked example — resolved, with a correction

Same incident, now resolved, but the initially suspected cause turned out
wrong — see `docs/DEMO-comms.md` Turn 4 for the full scripted version.

**Wrong (silent correction):**

> Interface engine issue is resolved as of 03:10. Order delivery to PACS is
> normal.

This reads clean and is exactly the failure mode to avoid — a previously
published `suspected` cause has quietly vanished rather than being
corrected.

**Right (flagged correction):**

> Correction to the 02:14 update: the interface engine was not the cause.
> The PACS listener was the fault; engine and order delivery were unaffected
> once the listener restarted. Resolved as of 03:10. No residual actions.

Same resolution, but the change is named as a change. This is the same
principle as `${CLAUDE_PLUGIN_ROOT}/PERSONA-SPEC.md`'s Mode rule — "a previously stated fact
that changes gets flagged as changed" — applied to comms output rather than
to the model's own prior turns.

## Worked example — degraded performance, technical-only

Not every event reaches every audience. A queue depth warning that self-
resolves before clinical impact stays IT/NOC-only — sending it to clinical
audiences would train them to ignore imaging notifications generally.

> Interface engine queue depth elevated (140 msgs, threshold 100) starting
> 04:02. No clinical impact observed. Monitoring; will notify if this
> escalates. INC0004822 opened for tracking.

Leads with the failure (technical register), states explicitly that there's
no clinical impact rather than omitting clinical audiences silently — the
absence of a clinical draft should be a decision that's visible in the
comms-skill session, not something that just didn't happen.

## Applying this without a full profile

When no comms profile variant matches (`references/generic-templates.md`
fallback), the register rule still applies — only the site-local vocabulary
(procedure names, distribution lists) is missing. Use the generic template's
structure with the correct register, and label the draft "generic — not yet
tuned to this site" rather than guessing at site-local names to fill the
gap.
