---
name: comms
description: Draft and maintain radiology IT support notifications — downtime alerts, major-incident cadence updates, vendor tickets, change narratives, shift turnover. Use when the user needs to notify anyone about a service impact, or wants to tune this site's notification templates. Triggers include /downtime, /comms-tune, "draft a downtime notice", "we need to tell clinical", "send an update on the outage", "all clear".
---

# Communications

Notifications go out under time pressure, to people who will act on them. The
value of this skill is not prose quality — it is that nothing required is
missing and nothing unknown is invented.

Persona: `docs/PERSONA-SPEC.md`. The audience-register table (clinical /
technical / leadership) and the never-invent-a-required-field rule are
defined there — the steps below are this skill's application of them, not a
second copy.

## Files this skill reads

| File | Contents | If absent |
|---|---|---|
| Site profile | systems, interface names, downtime procedure names, escalation matrix, SLA tiers | Draft generically and say so; offer `/setup` |
| Comms profile | template variants keyed by event class × audience × channel, required fields, voice rules, approval chain | Use the generic templates in `references/`; offer `/comms-tune` |

Both live at the local configured path, outside the plugin directory, and
survive plugin updates.

## Generating a notification

1. **Resolve the variant key.** Event class, audience, channel. Ask for any
   part the user has not supplied — one question at a time.
2. **Select the template.** Exact match, else nearest defined variant with the
   substitution stated out loud, else generic reference template labelled as
   untuned.
3. **Fill slots from stated facts only.** Every required slot the user has not
   provided gets the placeholder token and appears in an outstanding-items list
   under the draft. An ETA, a cause, or an impact scope is never inferred.
4. **Apply audience register** per `docs/PERSONA-SPEC.md`'s Tenor table —
   clinical leads with the required action (workflow terms, site-named
   procedure — "orders will not reach the modality worklist," not "ORM_O01
   delivery is failing"); technical leads with the failure, interfaces,
   queues, and ticket reference; leadership leads with scope, duration, and
   what's being done, in that order.
5. **Mark causal claims.** `confirmed` or `suspected`, per the site's
   convention (comms' two-tier instance of the persona's general
   confidence-marking rule). An unmarked cause is a defect.
6. **Maintain continuity across a running incident.** Interval updates and
   all-clears carry forward the incident reference, original start time, and
   previously stated impact, and require only the delta from the user. Never
   silently change a previously published fact — if it has changed, say that it
   changed.

## Customizing the profile

Four modes, invoked by `/comms-tune`: **capture** (infer variants from pasted
examples), **build** (guided construction, deltas from the site's most common
notification), **edit** (one variant, no re-interview), **review** (coverage
against the axes, gaps ranked).

Design rules for the interview:

- One question per turn. Sites abandon matrices.
- Derive, don't enumerate. Establish the base notification, then ask only what
  differs for each additional variant.
- Accept "we don't distinguish that" as a complete answer and record it, so the
  question is not asked again.
- Confirm inferences explicitly when in capture mode — show what was extracted
  before writing it.
- Unknowns are recorded as unknown. Never fabricate a distribution list,
  procedure name, or approval chain to complete a profile.

## Boundaries

- This skill drafts. It does not send, publish, page, or post.
- It does not decide severity. It applies the site's severity mapping, and when
  the mapping is ambiguous it says so and asks.
- Approval chains are surfaced with the draft, never bypassed or assumed
  satisfied.

## References

- `references/generic-templates.md` — untuned fallbacks for each event class
- `references/comms-profile.schema.md` — profile structure and field meanings
- `references/register-guide.md` — audience register rules with worked examples
