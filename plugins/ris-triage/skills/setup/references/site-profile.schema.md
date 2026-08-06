# Site profile schema

Backlog E2.1. The site profile is what every skill except comms reads for
site-specific facts (comms has its own, narrower profile — see
`skills/comms/references/comms-profile.schema.md`). Written by the `setup`
skill's interview mode, edited by its edit mode, inspected by its review
mode. Lives at the configured local path, outside the plugin directory.

Unknown stays unknown: a field the interview didn't collect is absent from
the file, not present with a null or placeholder value. Skills read absence
as "not in your site profile" and say so — they don't distinguish "empty
string" from "never asked," so don't write one.

## Top-level shape

```yaml
version: 1
site: <site name>

systems: []
interfaces: []
identifier_formats: {}
escalation_matrix: []
sla_tiers: []
downtime_procedures: []
audiences: []
```

Every section below is optional at the file level — a fresh profile from a
partial interview is valid with only the sections actually answered.

---

## `systems`

The RIS/PACS/EHR/dictation/interface-engine inventory. One entry per system.

```yaml
systems:
  - role: ris                    # ris | pacs | ehr | dictation | interface_engine | worklist | other
    product: <vendor/product name>
    version: <version, if known>
    notes: <anything operationally relevant — HA pair, VM host, etc.>
```

`role` is a controlled vocabulary so the triage differential (RIS config /
interface / PACS / workstation / user) can address a branch by name rather
than fuzzy-matching free text. `other` is a legitimate answer — record what
it is in `notes`.

## `interfaces`

Named integration points between systems. This is what `/explain` and
`/triage` mean by "interface" — a logical link, not a message-level parse
target (that's the separate forensics plugin).

```yaml
interfaces:
  - name: <site's name for this interface>
    from: <system role or product name>
    to: <system role or product name>
    direction: unidirectional | bidirectional
    transport: <e.g. MLLP, file drop, API — only if known>
    criticality: <what breaks if this is down, one line>
```

`name` matters more than the technical fields — it's what a technical-
audience notification names, verbatim, per the comms register rule. If the
site calls it "the ADT feed," the notification says "the ADT feed," not
"the bidirectional patient-demographics interface."

## `identifier_formats`

How this site's identifiers look, so explainer answers and triage scope
statements use the site's actual formats rather than generic examples.

```yaml
identifier_formats:
  accession_number: <format/pattern, e.g. "IMG########">
  order_number: <format/pattern>
  mrn: <format/pattern>
  incident_ref: <format/pattern, e.g. "INC0#######">
```

## `escalation_matrix`

Who gets paged for what, in order.

```yaml
escalation_matrix:
  - tier: <name — e.g. "Tier 1", "On-call analyst">
    scope: <what this tier owns>
    contact: <role or distribution — never a personal name/number in this repo's examples>
    hours: <when this tier is reachable — "24/7", "business hours", etc.>
    escalates_to: <next tier name, or "none">
```

This is what `/triage`'s "recommended queue" and escalation-package
assembly cite by name (US-04, US-05). A queue recommendation with no
matching entry here says so instead of guessing.

## `sla_tiers`

Severity vocabulary this site actually uses.

```yaml
sla_tiers:
  - severity: <site's label — "Sev 1", "P1", "Critical", etc.>
    definition: <what qualifies>
    response_target: <time>
    resolution_target: <time, if defined>
```

Triage's severity justification (US-04) quotes `definition` directly rather
than paraphrasing — a routing dispute gets resolved by pointing at the
site's own words, not the plugin's interpretation of them.

## `downtime_procedures`

Named procedures clinical staff already know, referenced by name rather
than described generically.

```yaml
downtime_procedures:
  - name: <site's name for the procedure — e.g. "Imaging Downtime Packet">
    trigger: <when this procedure applies>
    summary: <one line — what staff actually do>
```

## `audiences`

The canonical roster of who exists and when they're reachable. This is
distinct from the comms profile's per-notification variant matrix — this
section answers "who is there," the comms profile answers "what do we send
each of them, and how." Comms reads this list; it doesn't duplicate it.

```yaml
audiences:
  - label: <site's own term for this group>
    reachable: 24/7 | business_hours | on_call_only
    notes: <anything that changes overnight — e.g. "overnight, page the house supervisor instead">
```

**Do not ship a default roster.** An earlier draft of this project hardcoded
a specific audience label without confirming it against any real site —
see `docs/PERSONA-SPEC.md`'s Tenor section. The interview asks; it does not
assume. A reasonable starting checklist to walk the user through — not a
default to assume unconfirmed — is: on-call radiologist, night techs, house
supervisor, next shift, on-call manager, IT/NOC, leadership.

---

## Degradation contract

Every skill reading this file follows the same rule (`docs/PERSONA-SPEC.md`,
Field): a missing section or field renders as "not in your site profile,"
never a plausible invention. A skill may answer generically with that gap
stated, but it does not fill the gap with a guess dressed as a fact.
