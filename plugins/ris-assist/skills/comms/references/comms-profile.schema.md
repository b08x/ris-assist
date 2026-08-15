# Comms profile schema

Backlog E6.5. The comms profile is narrower than the general site profile
(`skills/onboarding/references/site-profile.schema.md`) — it holds notification
*voice and variants*, not systems/interfaces/SLA facts. `/downtime` reads
both: site profile for facts (system names, procedure names), comms profile
for how to say them to whom.

`examples/comms-profile.example.yaml` is a complete worked instance of this
schema for the fictional site Riverside Regional Imaging — read it alongside
this file.

## Top-level shape

```yaml
version: 1
site: <site name>

conventions: {}
distribution: {}
approval: {}
workflow_language: {}
update_cadence: {}
voice: {}
variants: []
gaps: []
```

## `conventions`

Mechanical formatting facts that apply to every notification.

```yaml
conventions:
  timezone: <IANA zone>
  time_format: 12h | 24h
  placeholder_token: <string used for unfilled required fields, default "[TBD]">
  cause_marking: required | optional     # confirmed | suspected vocabulary
  incident_ref_format: <pattern>
  quiet_hours: <when to page instead of email, or vice versa>
```

## `distribution`

Names the site actually uses for each audience — a distribution list, a
channel, a group. Keys should match the `audiences` labels in the site
profile where both exist; they're allowed to diverge (a site profile
audience without a comms distribution entry just means no channel is
defined for them yet — record it in `gaps`, don't invent one).

```yaml
distribution:
  <audience label>: <distribution list, channel handle, or group name>
```

## `approval`

Who drafts, approves, and sends, per severity. `/downtime` surfaces this with
the draft; it never assumes approval is satisfied.

```yaml
approval:
  <severity label — matches site profile sla_tiers>: <chain, one line>
```

## `workflow_language`

Site-local names for procedures and fallbacks. Clinical-audience drafts use
these verbatim (register-guide.md) rather than a generic description.

```yaml
workflow_language:
  downtime_procedure: <name, matches a site-profile downtime_procedures entry>
  <other site-local term>: <what to call it>
```

## `update_cadence`

How often interval updates go out, per severity.

```yaml
update_cadence:
  <severity label>: <cadence, e.g. "every 30 minutes">
```

## `voice`

House style. Kept as narrow as the site actually enforces — most of this
section is a legitimate "we don't distinguish that."

```yaml
voice:
  formality: operational | formal | plain
  person: <e.g. "first person plural (we)">
  apology_language: <when apology language is used, if ever, and how much>
  banned_phrasing: []
```

## `variants`

The actual template matrix, keyed `event class × audience × channel`. This
is the product — `references/generic-templates.md` is only the fallback for
event/audience/channel combinations with no variant defined here.

```yaml
variants:
  - key: <event class> / <audience> / <channel>
    required_fields: []          # never inferred if absent — see comms/SKILL.md
    lead_with: action | failure | scope | delta | schedule | resolution
    sections: []                 # the draft's section order
    continuity: required         # only for interval_update / resolved keys
    notes: <anything that doesn't fit another field>
```

`lead_with` is the mechanical instantiation of the register rule in
`${CLAUDE_PLUGIN_ROOT}/PERSONA-SPEC.md`'s Tenor table and `references/register-guide.md`'s
worked examples — one word, but it's what the comms skill's step 4 actually
branches on.

## `gaps`

Recorded by `/comms-config review`, and read by `/downtime` when no variant
matches. A gap entry is not a TODO for the plugin to fill silently — it's
what makes a missing variant visible in output instead of invented.

```yaml
gaps:
  - "<audience/event/channel combination> — <what's missing and why it matters>"
```
