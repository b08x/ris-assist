---
name: setup
description: Cold-start interview that builds this site's profile — systems, interface names, escalation matrix, SLA tiers, audiences, downtime procedure names — and writes it to a local path outside the plugin. Also handles single-field edits later. Use when the plugin is first installed, when a skill reports a missing profile field, or when the user says "set up", "configure my site", "change my escalation contact", or /setup.
---

# Site profile setup

Implements backlog E2.2 (interview) and E2.3 (edit). Review mode is
lighter-weight and covered inline below rather than broken out further.

Persona: `${CLAUDE_PLUGIN_ROOT}/PERSONA-SPEC.md`. The never-invent rule and the audience-roster
caution (an earlier draft hardcoded a specific audience label — see
PERSONA-SPEC's Tenor section — it was never confirmed against a real site)
apply directly to this skill's interview.

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

## Interview sequence

**Before step 1, on a first run (no profile found at any previously
confirmed path):** ask where to write the profile — a full file path outside
the plugin directory. Do not assume a default (a sandbox output convention,
a dotfile location, anything else); this varies by host environment and is
exactly the kind of unconfirmed premise `docs/GUARDRAILS.md` G3 warns
against. Confirm the path back before writing anything, same as any other
answer in this interview. On later runs (edit/review mode, or a skill
reporting a missing profile field), ask the user for the existing path
rather than re-deriving or guessing it.

Schema: `references/site-profile.schema.md`. Walk its sections in this order,
one question at a time. Confirm each answer back before moving on — a
misheard system name propagates into every skill that reads it.

Any step whose answer is a list — systems, escalation tiers, SLA tiers,
audiences (steps 2, 5, 6, 8) — can be supplied as an existing document
instead of dictated: a spreadsheet export, a CMDB inventory, an on-call
schedule. Offer this explicitly rather than waiting for the user to think of
it. If what's offered is structured (CSV, a table, a spreadsheet), read it as
rows and columns, not prose — per this project's symbolic-parse-before-
interpretation commitment; free text still gets read and mapped by
inference. Either way, confirm the mapped result back per field, same as a
spoken answer — a pasted list is not exempt from the confirm-before-moving-on
rule, and a spreadsheet typo propagates exactly like a misheard word.

1. **Site name.** Used only in drafts and headers; not a distribution target.
2. **Systems.** "What's your RIS? PACS? Do you have a separate dictation
   platform? If you already have this written down — an inventory
   spreadsheet, a CMDB export — share that instead of typing it out." One
   system per turn is fine, but don't force a rigid order — if the user
   volunteers the interface engine next, take it. Ask `role` before
   `product` so answers map cleanly onto the schema's controlled vocabulary
   (`ris` / `pacs` / `ehr` / `dictation` / `interface_engine` / `worklist` /
   `other`).
3. **Interfaces.** For each pair of systems already named, ask if there's a
   named interface between them and what happens when it's down — that
   answer becomes `criticality`, which is what a differential branch will
   eventually cite. Don't ask about interfaces between systems that were
   never named in step 2.
4. **Identifier formats.** Quick — pattern, not full regex. "What does an
   accession number look like at your site? Just the shape — letters,
   digits, length."
5. **Escalation matrix.** Start from Tier 1 and ask "then who?" repeatedly
   until the answer is "vendor support" or "nobody, that's the end of the
   chain." This is naturally a deltas-from-the-previous-answer interview —
   don't ask reachability/hours separately unless the user's answer doesn't
   already imply it.
6. **SLA tiers.** Ask for the site's own severity labels first ("what do you
   call your highest severity?") before asking what qualifies — sites care
   about getting their own vocabulary right more than the response-time
   numbers, and getting the label right first makes the rest go faster.
7. **Downtime procedures.** "When PACS or RIS goes down, what do staff
   actually do?" One procedure per answer; ask what triggers each one.
8. **Audiences.** Last, and asked as two passes: who exists (the roster),
   then who's reachable overnight specifically — the second pass is not
   optional. Offer the starting checklist from the schema's `audiences`
   section as prompts, not defaults: "Some sites have an on-call
   radiologist, night techs, a house supervisor — which of these do you
   have, and who else?"

Stop the interview when a section is answered "we don't distinguish that" or
genuinely doesn't apply — record it as such (schema note: absence, not an
empty placeholder) so the question doesn't recur in `edit` mode.

## Rules

- Never invent a system name, interface name, distribution list, procedure
  name, or approval chain. Unknown is recorded as unknown.
- Accept "we don't distinguish that" as a complete answer and record it so the
  question is not asked again.
- The audience set is site- and shift-specific. Ask; do not assume a default
  roster. Ask separately about who is reachable overnight — it is usually a
  different set from the daytime one.
- An uploaded or pasted document is an input to confirm, not a shortcut past
  confirmation. Map it onto schema fields, show the mapping, and get the same
  per-field confirmation a spoken answer would get before moving on.

## Schema

See `references/site-profile.schema.md`.
