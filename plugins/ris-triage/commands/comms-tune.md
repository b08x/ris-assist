---
description: Build or adjust this site's notification templates — variants, audiences, channels, required fields, and house voice.
argument-hint: "[capture|build|edit|review] [optional variant name]"
allowed-tools: Read, Write
---

Tune the comms profile that `/downtime` and the other notification drafts read
from. Use the **comms** skill's customization procedure.

Mode: `$ARGUMENTS` — if absent, ask which mode, briefly describing each.

## Modes

### capture — learn from what the site already sends
Fastest path when real past notifications exist.

1. Ask the user to paste two or three notifications they consider
   representative — ideally different event classes or audiences.
2. Extract, and show back for confirmation: section order, the fields that
   appear in every one, the fields that vary, salutation and sign-off
   conventions, how impact is described, how timing is expressed, and the
   register (formal / operational / plain).
3. State what was inferred versus what is being assumed, and ask only about
   the assumptions.
4. Write the resulting variants to the comms profile.

Remind the user once that pasted notifications are stored in their **local**
comms profile, outside the plugin, and that staff names or contact details
included in them will persist there.

### build — construct variants from scratch
When no past examples are available or the site wants to standardize.

Work through the variation axes below, one question at a time. Do not present
the whole matrix at once. Start from the single most common notification the
site sends and derive the rest as deltas from it, so the interview stays short.

Any axis can be answered with an existing document instead of dictated —
a distribution-list export, an approval-chain org chart, a style guide for
the **Voice** axis. Offer this explicitly rather than waiting for the user to
think of it. Structured input (a spreadsheet, a table) is read as rows and
columns, not prose, per this project's symbolic-parse-before-interpretation
commitment; free text still gets read and mapped by inference. Either way,
show the mapping and confirm it per axis before writing it — same as the
capture-mode confirmation below, and for the same reason: a spreadsheet typo
propagates exactly like a misheard answer.

### edit — change one thing
Take the named variant (or ask which), show its current definition, change only
what the user asks, and rewrite that entry. Do not re-run the interview.

### review — inspect coverage
List defined variants against the axes, name the gaps, and rank them by how
likely they are to be needed. Do not fill gaps automatically; offer to.

## Variation axes

Capture only what the site actually distinguishes. A site that sends the same
message to everyone has one variant, and that is a legitimate answer.

| Axis | Typical values |
|---|---|
| **Event class** | planned maintenance · unplanned outage · degraded performance · interval update · extended/revised ETA · resolved · post-incident summary |
| **Audience** | radiologists · technologists · next shift · referring clinicians · IT and NOC · service desk agents · leadership · vendor |
| **Channel** | email · Teams/Slack · ITSM broadcast · status page · in-application banner · paging/overhead · printed downtime packet |
| **Scope** | single modality · single reading room · one site · enterprise · interface-only (invisible to clinical users) |
| **Severity mapping** | how site severity tiers map to notification urgency and to who must approve |
| **Required fields** | what must never be omitted — incident reference, start time, affected workflows, workaround, ETA, next update time, contact |
| **Workflow instructions** | site-local downtime procedure names, paper requisition process, dictation fallback, PACS-direct read path |
| **Timing conventions** | timezone, 12/24-hour, update cadence per severity, quiet hours |
| **Voice** | formality, first person plural vs. impersonal, whether apology language is used, banned phrasing |
| **Boilerplate** | compliance or confidentiality footer, ticket-reference format, distribution list names |
| **Approval** | who drafts, who approves, who sends, per event class |
| **Language** | additional languages required, and for which audiences |

## Output

Write the profile to the configured local comms profile path. Then show a
compact summary of what changed — variants added, edited, or still missing —
and offer to generate one sample draft per new variant so the user can see the
result immediately.

## Constraints

- Ask one question at a time. Stop as soon as the site's real distinctions are
  captured; do not pursue axes the user has indicated are irrelevant.
- Never invent a downtime procedure name, distribution list, or approval chain.
  Unknown stays unknown, recorded as such in the profile.
- Preserve entries not under discussion. Editing one variant must not rewrite
  the others.
- An uploaded or pasted document is an input to confirm, not a shortcut past
  confirmation. Map it onto the relevant axis, show the mapping, and get the
  same per-axis confirmation a spoken answer would get before writing it.
