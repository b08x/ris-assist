# Generic templates

Backlog E6.12. Untuned fallbacks — used only when no comms profile exists,
or the profile exists but has no variant for the requested
event-class/audience/channel combination (`references/comms-profile.schema.md`
`gaps`). Every draft built from these is labeled **generic — not yet tuned to
this site** in the output; that label is not optional.

These templates supply structure, not voice. The register rule
(`references/register-guide.md`) still applies — lead with action for
clinical, failure for technical, scope for leadership — even with no site
vocabulary to draw on. Where a site-local name would normally appear
(procedure name, distribution list, interface name), use the placeholder
token and list it as outstanding.

## Planned

Sections: schedule, affected workflows, workaround, contact.

> **Planned maintenance — [system/interface]**
> Window: [start] to [end] ([timezone]).
> Affected: [workflows/systems affected].
> Workaround: [workaround, or "none — service unavailable during window"].
> Questions: [contact].

Lead time convention (if unknown): default to stating the window and letting
the reader judge urgency, rather than inventing a notice-period norm.

## Unplanned

Sections: what's happening, what to do now, what not to do, next update.

> **Service impact — [system/interface]**
> As of [time]: [what's happening, plainly — no invented cause].
> What to do: [workaround, or "[TBD]" if none stated].
> Do not: [anything explicitly to avoid, if stated].
> Next update: [time or cadence].

Cause is omitted entirely unless one was stated, in which case it's marked
`confirmed` or `suspected` per the general confidence-marking rule in
`docs/PERSONA-SPEC.md` — this template doesn't ship its own cause-marking
convention because the site profile's `cause_marking` setting decides
whether marking is required in the first place.

## Degraded

Sections: symptom, scope, monitoring status, escalation trigger.

> **Degraded performance — [system/interface]**
> Symptom: [observed symptom].
> Scope: [who/what is affected, or "no confirmed impact yet"].
> Status: monitoring. Will notify if this escalates to a service outage.
> Reference: [ticket ref, if one exists].

## Interval update

Sections: delta since last update, current status, next update time.
**Continuity is mandatory even in generic mode** — carry forward the
original incident reference and start time; state explicitly if a
previously published fact changed.

> **Update — [incident ref]**
> Since [last update time]: [delta only — not a restatement of the whole
> incident].
> Status: [current state].
> [If a fact changed: "Correction to the [time] update: [what changed]."]
> Next update: [time or cadence].

## Resolved

Sections: resolution statement, duration, cause status, residual actions.

> **Resolved — [incident ref]**
> [System/interface] restored as of [time]. Total duration: [start] to
> [end].
> Cause: [confirmed/suspected — or "not determined"].
> Residual actions: [list, or "none"].

"Residual actions: none" is written explicitly rather than omitted — an
absent line reads as an oversight, a stated "none" reads as checked.

## Vendor ticket

Sections: symptom, environment, what's been ruled out, reproduction (if
known), site identifiers.

> **Vendor ticket — [system/interface]**
> Symptom: [what's observed, from the reporter or worklog, not embellished].
> Environment: [system name/version if known, else "[TBD]"].
> Ruled out: [what's already been checked].
> Reproduction: [steps actually observed — never invented past the worklog].
> Site references: [accession/order/incident numbers per this site's
> identifier formats, if known].

## Shift turnover

Sections: state, next action, landmines.

> **Turnover — [date/shift]**
> Open: [ticket ref] — state: [current status]. Next action: [what the next
> shift should do]. Landmine: [anything non-obvious that will bite the next
> person if not flagged].

Repeat the three-line block per open item. An empty "landmines" line is
written as "none noted" rather than dropped.
