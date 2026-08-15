---
description: Draft an all-clear or service-restored recovery notification for a chosen audience and channel.
argument-hint: "[restored|partially-restored] [system or interface] [original incident ref, if any]"
allowed-tools: Read, Write
---

Draft a recovery / all-clear notification using the **comms** skill. This is
the resolution-side counterpart to `/downtime` — same skill, same profile,
same continuity rules — scoped to the moment a service comes back rather than
the moment it goes down.

## Inputs

Arguments: `$ARGUMENTS`

If arguments are absent or partial, do not guess — ask for the missing pieces
one at a time, in this order: restoration state (fully restored / partially
restored), affected system, the original incident reference (if this is
closing out a prior downtime notice), audience.

## Procedure

1. Load the site profile and the comms profile from the configured local path.
   - If **no comms profile exists**, say so in one line and offer to run
     `/comms-config` to build one. Then continue with the built-in generic
     templates, labelling the output clearly as *generic — not yet tuned to
     this site*.
   - If the comms profile exists but lacks a `resolved`/all-clear variant, use
     the closest defined variant, name the substitution explicitly, and offer
     to capture the missing variant via `/comms-config`.

2. Select the template by the three-axis key defined in the comms profile:
   `event class × audience × channel`, using the `resolved` (or equivalent
   all-clear) event class.

3. **Check for prior-notice continuity.** If this recovery follows a downtime
   notice from this session or a stated incident reference, carry forward the
   original incident reference, start time, and previously stated impact
   scope — do not restate them from memory or infer them. If no prior notice
   is known, ask whether one exists before drafting a standalone all-clear.

4. Fill required slots from what the user has provided. For any required slot
   still unknown, insert the profile's configured placeholder token (default
   `[TBD]`) and list the outstanding items beneath the draft. **Never infer a
   restoration time, a root cause, or a residual-impact scope that the user
   did not state.**

5. Apply the site's register rules for the chosen audience — clinical-facing
   drafts lead with what the reader can now do again; technical drafts lead
   with what was fixed and what, if anything, is still being watched.

6. If restoration is partial, say so plainly and name what remains degraded —
   never round a partial recovery up to a full all-clear.

7. Output, in this order:
   - the draft, in the channel's format
   - a short list of unfilled required slots, if any
   - the configured send/approval note for that variant, if one is defined

## Constraints

- No speculation about root cause presented as fact. If a cause is stated,
  mark it `confirmed` or `suspected` per the comms profile's convention.
- Do not send anything. This command produces text for a human to review,
  approve, and dispatch.
- Never silently drop or change a fact already published in the original
  downtime notice — if something changed (e.g., scope narrowed), say that it
  changed rather than restating the original as still true.
