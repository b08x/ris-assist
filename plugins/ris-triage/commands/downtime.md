---
description: Draft a downtime or service-impact notification for a chosen audience and channel.
argument-hint: "[planned|unplanned|degraded|update|resolved] [system or interface]"
allowed-tools: Read, Write
---

Draft a downtime notification using the **comms** skill.

## Inputs

Arguments: `$ARGUMENTS`

If arguments are absent or partial, do not guess — ask for the missing pieces
one at a time, in this order: event class, affected system, scope, audience.

## Procedure

1. Load the site profile and the comms profile from the configured local path.
   - If **no comms profile exists**, say so in one line and offer to run
     `/comms-tune` to build one. Then continue with the built-in generic
     templates, labelling the output clearly as *generic — not yet tuned to
     this site*.
   - If the comms profile exists but lacks the requested variant, use the
     closest defined variant, name the substitution explicitly, and offer to
     capture the missing variant via `/comms-tune`.

2. Select the template by the three-axis key defined in the comms profile:
   `event class × audience × channel`.

3. Fill required slots from what the user has provided. For any required slot
   still unknown, insert the profile's configured placeholder token (default
   `[TBD]`) and list the outstanding items beneath the draft. **Never infer an
   ETA, a cause, or an impact scope that the user did not state.**

4. Apply the site's register rules for the chosen audience — clinical-facing
   drafts reference downtime procedures by their site-local names and lead
   with what the reader must *do*; technical drafts lead with what is broken.

5. Output, in this order:
   - the draft, in the channel's format
   - a short list of unfilled required slots, if any
   - the configured send/approval note for that variant, if one is defined

## Constraints

- No speculation about cause presented as fact. If a cause is stated, mark it
  `confirmed` or `suspected` per the comms profile's convention.
- Do not send anything. This command produces text for a human to review,
  approve, and dispatch.
- If the user asks for an all-clear or resolution notice, check whether the
  profile requires prior-notice continuity (carrying forward the original
  incident reference and start time) and include it.
