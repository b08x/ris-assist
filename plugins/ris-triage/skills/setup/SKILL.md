---
name: setup
description: Cold-start interview that builds this site's profile — systems, interface names, escalation matrix, SLA tiers, audiences, downtime procedure names — and writes it to a local path outside the plugin. Also handles single-field edits later. Use when the plugin is first installed, when a skill reports a missing profile field, or when the user says "set up", "configure my site", "change my escalation contact", or /setup.
---

# Site profile setup

STUB — implements backlog E2.2 and E2.3.

## Why the profile lives outside the plugin

Installed plugins are copied to a cache directory that is replaced on update.
A profile stored inside the plugin would be lost on every upgrade, and would
risk site-specific detail reaching the repository. The profile is written to a
local path the user controls; every skill reads it at runtime.

## Modes

- **interview** — first run. One question at a time. Derive later answers as
  deltas from earlier ones rather than walking a matrix.
- **edit** — change one field without re-interviewing. Preserve everything not
  under discussion.
- **review** — report which fields are populated, which are empty, and which
  gaps are likely to be needed soon. Do not auto-fill.

## Rules

- Never invent a system name, interface name, distribution list, procedure
  name, or approval chain. Unknown is recorded as unknown.
- Accept "we don't distinguish that" as a complete answer and record it so the
  question is not asked again.
- The audience set is site- and shift-specific. Ask; do not assume a default
  roster. Ask separately about who is reachable overnight — it is usually a
  different set from the daytime one.

## Schema

See `references/site-profile.schema.md` (TODO — backlog E2.1).
