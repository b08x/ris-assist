# RIS Support Triage Plugin — User Stories

Personas reflect a client-site radiology support environment operated by an MSP,
plus external adopters of the published plugin. Stories are numbered for
traceability into `BACKLOG.md` (each backlog epic lists the stories it serves).

**Scope note.** Message-forensics stories (US-01, US-02, US-08, US-09, US-10)
and the synthetic-corpus story (US-24) belong to the separate forensics plugin
per [ADR-0008](adr/0008-separate-forensics-plugin.md). They are retained here
with a **[FORENSICS]** tag rather than deleted, because the numbering is
referenced from the backlog and because the requirement did not stop existing —
it moved.

Deployment constraint carried by all stories: capabilities run on Claude Desktop
(plugin) with a parallel M365 Copilot track for live-PHI workflows. Stories that
require live PHI are tagged **[PHI]** and are Copilot-track or
post-approval-dependent.

---

## Persona A — Support Analyst (L1/L2 triage)

The primary user, and the overnight shift is the design target: working alone,
no senior analyst to ask, vendor support behind a callback queue. Generalist IT
background, variable radiology depth, often the least experienced person on the
account.

Audience labels used in stories below are placeholders. The real audience set
comes from the cold-start interview (US-22) and varies by site and by shift —
see `docs/PERSONA-SPEC.md`'s Tenor section and `skills/setup/references/site-profile.schema.md`.

**US-01 — Decode a message** [FORENSICS]
As a support analyst, I want to paste a de-identified HL7 v2 message and receive
a structured breakdown (message type, event, key identifiers, statuses,
timestamps) so that I don't hand-count pipes under time pressure.

- AC: Output identifies message type/trigger event, patient/order/accession
  identifiers, and relevant status fields, each labeled with segment-field
  coordinates (e.g., ORC-3, OBR-25).
- AC: Unknown or non-standard segments are flagged as "not in reference," never
  given an invented meaning.
- AC: Every diagnostic statement is marked *confirmed / likely / possible*.

**US-02 — Interpret an ACK/NAK** [FORENSICS]
As a support analyst, I want to paste an ACK/NAK and get an interpretation of
the error against this site's interfaces so that I know whether the fault is
ours, the receiving system's, or the engine's.

- AC: Distinguishes AA/AE/AR semantics and maps the error text to a likely
  fault origin using the site profile.

**US-03 — Clarify a vague ticket**
As a support analyst, I want the agent to generate the single most
discriminating question to ask a reporter, given what the ticket already says,
so that I reach a routable ticket in the fewest exchanges.

- AC: Agent maintains a visible differential (RIS config / interface / PACS /
  workstation / user) and explains which branches each question separates.
- AC: Questioning stops when a routing decision is determinable.

**US-04 — Route with justification**
As a support analyst, I want an assignment-group recommendation with a
severity/priority justification written in the SLA's own vocabulary so that
routing and priority disputes end faster.

- AC: Recommendation cites the site escalation matrix and SLA definitions by
  name; if the site profile lacks the needed entry, the agent says so instead
  of improvising.

**US-05 — Assemble an escalation package**
As a support analyst, I want a generated escalation package (timeline, evidence,
what's been ruled out, environment details) so that escalated tickets don't
bounce back for missing information.

**US-06 — Check for known errors first [PHI]**
As a support analyst, I want incoming symptoms matched against existing KB
articles and open problem records so that I don't re-solve solved problems.
(Depends on ServiceNow read access.)

**US-07 — Ask "why does it work this way"**
As a support analyst, I want to ask domain questions (accession vs. order
number, MWL, report status flow, order lifecycle) and get answers grounded in
the site topology, at the depth I ask for, so that I stop shoulder-tapping the
senior analyst.

---

## Persona B — Interface Analyst (L2/L3) [FORENSICS PLUGIN]

Owns the interface engine relationship; deeper HL7 fluency.

**US-08 — Diff messages** [FORENSICS]
As an interface analyst, I want to diff a failing message against a last-known
-good message at segment/field granularity so that I can isolate what changed.

- AC: Diff output is field-level, ignores expected variance (timestamps, control
  IDs) unless asked, and highlights structural differences separately from
  value differences.

**US-09 — Assess outage blast radius** [FORENSICS]
As an interface analyst, I want to name a down interface and get the ordered
downstream impact (which workflows fail, in what sequence symptoms will appear)
so that I can brief the incident channel before the tickets arrive.

- AC: Impact chain derives from the site topology file, not generic HL7 lore.

**US-10 — Triage a queue backlog** [FORENSICS]
As an interface analyst, I want guidance on which stuck message types are safe
to replay versus which require sequence-aware handling (ADT merges, cancels) so
that a replay doesn't corrupt downstream state.

- AC: Agent never claims to have executed a replay; replay authorization is
  explicitly flagged as a human decision.

---

## Persona C — Knowledge Manager / KCS Champion

Accountable for KB health under the MSP's knowledge process.

**US-11 — Draft a KB article from a resolution**
As a knowledge manager, I want a resolved ticket's worklog turned into a
KCS-conformant article draft so that knowledge capture happens at resolution
time instead of never.

- AC: Output conforms to the site's KB template (structure, fields, audience
  labels); observation and inference are separated in the body.

**US-12 — Detect KB gaps**
As a knowledge manager, I want recurring incident patterns with no matching
article surfaced so that the KB grows where demand actually is.

**US-13 — Flag stale articles**
As a knowledge manager, I want articles referencing changed interfaces or
upgraded systems flagged for review after a change so that the KB doesn't decay
silently.

**US-14 — Push to ServiceNow [PHI]**
As a knowledge manager, I want approved drafts submitted to ServiceNow with
correct category and workflow state so that the loop closes without copy-paste.
(Depends on ServiceNow MCP with write scope.)

---

## Persona D — Support Lead / Shift Lead

Owns communications, handoffs, and the incident cadence.

**US-15 — Draft a downtime alert**
As a support lead, I want a downtime alert generated from a template (planned /
unplanned / degraded / resolved) with audience variants (clinical, IT,
leadership) so that notifications go out fast, complete, and in the right
register.

- AC: Clinical variant references downtime procedures by their site-local
  names; all variants populate required fields (severity, affected workflows,
  workaround, ETA, next-update time) or explicitly mark them unknown.

**US-16 — Run major-incident comms cadence**
As a support lead, I want interval update drafts that carry forward prior
facts and require only the delta so that MIM comms stay consistent across a
long incident.

**US-17 — Generate a shift-turnover summary**
As a support lead, I want open items summarized as state / next action /
landmines so that follow-the-sun handoffs don't drop context.

**US-18 — Draft a vendor ticket**
As a support lead, I want vendor-facing write-ups (RIS vendor, PACS vendor,
engine vendor) generated in the structure each vendor's support process
expects so that vendor tickets get worked instead of clarified.

**US-19 — Draft change and post-incident narratives**
As a support lead, I want change-request narratives (risk, impact, backout,
clinical-workflow implications) and post-incident review drafts reconstructed
from the ticket worklog so that process documents stop being the bottleneck.

---

## Persona E — New Analyst (onboarding)

Rotated onto the account with little or no radiology background.

**US-20 — Self-serve onboarding**
As a new analyst, I want a guided explainer path through the domain (topology,
order lifecycle, key identifiers, common failure modes) so that I'm useful in
days instead of weeks and stop consuming senior-analyst time.

- AC: Explanations adjust depth on request and cite the site topology file for
  anything site-specific.

---

## Persona F — Site Adopter (external analyst at another org)

Installs the published plugin at an unrelated site.

**US-21 — Install in one command**
As a site adopter, I want to add the marketplace and install the plugin from
the public GitHub repo so that setup is a command, not a wiring project.

**US-22 — Cold-start my site profile**
As a site adopter, I want a first-run interview that asks about my RIS, PACS,
interface names, escalation contacts, and SLA tiers, and writes a local site
profile outside the plugin directory so that the plugin becomes site-aware
without my configuration ever touching the public repo or being lost on
plugin update.

- AC: All capability skills read the local profile at runtime and degrade
  gracefully (stating what's missing) when a field is unpopulated.

**US-23 — Change one thing later**
As a site adopter, I want to update a single profile field (a contact, an
interface name) without re-running the whole interview so that maintenance is
proportional to the change.

**US-24 — Trust the data hygiene** [FORENSICS]
As a site adopter, I want all bundled test data to be synthetic-from-birth,
with the generator included, so that I can demonstrate to my own compliance
team that nothing in the artifact derives from production clinical data.

---

## Persona G — Maintainer / Developer

Builds and publishes the plugin; accountable for the transparency commitment.

**US-25 — Publish with process transparency**
As the maintainer, I want the repo to carry dated ADRs, an AI-assisted
development disclosure, and an unsquashed commit history so that the
development process is itself inspectable, not just the result.

**US-26 — Validate before release**
As the maintainer, I want plugin validation and an install smoke test in the
release path so that pathing/JSON failures never reach adopters.

**US-27 — Keep the boundary documented**
As the maintainer, I want a NON-GOALS / human-in-the-loop statement maintained
as a first-class doc so that what the agent will not do (execute replays, make
patient-safety-adjacent calls, guess field mappings) is as visible as what it
does.

---

## Persona H — Governance Stakeholder (client/MSP compliance, employer OSS review)

**US-28 — Approve the publication**
As a governance stakeholder, I want a short statement of exactly what is
published (generic logic + fictional example site), with the private/public
boundary explained, so that I can sign off quickly.

**US-29 — Verify the PHI posture**
As a governance stakeholder, I want the de-identification gate to be
deterministic and inspectable (code, not a prompt request) so that the PHI
control is auditable.

- AC: PID/NK1/IN1/GT1 handling and free-text (OBX/NTE) second pass are
  implemented in reviewable script code with test coverage against the
  synthetic corpus.
