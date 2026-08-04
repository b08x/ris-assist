# Demo — the full plugin, one incident thread

A scripted walkthrough of all five capabilities — `setup`, `triage`, `comms`,
`knowledge`, `explainer` — as one connected incident rather than five
disconnected feature checks. Companion to [DEMO-comms.md](DEMO-comms.md),
which goes deeper on comms alone; this demo's point is that the capabilities
compose: triage's finding becomes comms' incident, becomes knowledge's
article, against one consistent site.

**Everything here is fictional.** Riverside Regional Imaging does not exist.

---

## Setup

Two paths:

**Installed plugin** (the real path — `README.md` install instructions),
then run `/setup review` once to confirm a profile is loaded, or point the
session at the example files directly for a scripted run without a live
interview:

**Paste path** (no installation required — same method as `DEMO-comms.md`):
give the session

1. All five `skills/*/SKILL.md` files (or the `analyst` agent definition,
   `agents/analyst.md`, plus `docs/PERSONA-SPEC.md`)
2. `examples/site-profile.example.yaml`
3. `examples/comms-profile.example.yaml`

Then state: *"Treat both profiles as this site's configuration. Assume no
ServiceNow access — manual mode throughout."*

---

## Turn 1 — `/triage`, the vague ticket

**Input**

```
/triage PACS won't open a study.
```

**What to watch for.** No scope stated. Correct behavior is one
discriminating question, not a guess.

**Expected shape**

> Before I can route this — is it happening for one user, or more broadly?

**User answers:** *nobody can pull up new orders on any modality.*

**Expected behavior on the follow-up** — ask for timeline next, since scope
just collapsed three of five differential branches (workstation, user, and
effectively PACS) in one answer:

> Started sometime after the 2am maintenance window, I think.

**Expected triage artifact**

- Symptom, scope (`confirmed` — sitewide), timeline (~02:00, `likely`
  change-window-related — the overnight rule fires here)
- Differential: **Interface** `likely` (sitewide/all-modality scope rules out
  workstation/user; change-window timing is a strong prior); RIS
  configuration `possible`, not yet ruled out; PACS/workstation/user ruled
  out by scope
- Recommended queue: Tier 2 — interface analyst, cited from
  `escalation_matrix`
- Severity: Sev 1, cited from `sla_tiers` — workaround exists (downtime
  packet) but that's flagged as a human call on urgency, not resolved
  silently
- Overnight framing: this is a page, not a queue-and-wait, and states what
  the person being woken needs in hand

**The demo point:** the differential visibly narrows as evidence comes in —
branches get ruled out with a stated reason, not silently dropped — and the
stop condition is "routable," not "out of questions."

---

## Turn 2 — `/downtime`, the happy path

**Input**

```
/downtime unplanned, RIS-to-PACS order interface, for radiologists and techs.
```

**Expected behavior**

- Uses `unplanned / radiologists_and_techs / teams` variant from the comms profile
- Leads with the action, short (profile notes radiologists read the first
  two lines)
- Names the read path and downtime procedure in site language: "read direct
  from PACS worklist," "Imaging Downtime Packet (Form IMG-14)"
- No cause stated, none invented
- Outstanding items listed: incident reference not yet assigned; next-update
  timing assumed from the Sev 1 cadence and flagged for confirmation

**The demo point:** the triage finding from Turn 1 (sitewide, 02:00, RIS-to-
PACS interface) flows straight into the notification's facts — nothing is
re-derived or re-asked that Turn 1 already established.

---

## Turn 3 — `/downtime`, interval update (continuity)

**Input**

```
Update — still down, looks like the interface engine restart from
maintenance didn't come back clean, next update in 30.
```

**Expected behavior**

- Uses `interval_update / all / teams`, `continuity: required`
- Carries forward incident reference, 02:00 start time, and sitewide impact
  from Turn 2 — without being re-told them
- Leads with the delta only: the interface-engine-restart theory, marked
  `suspected`
- Does not repeat the workaround, since nothing about it changed

**The demo point:** this is the branch `DEMO-comms.md` calls "the one that
matters" — an incident is a thread, not a series of restatements.

---

## Turn 4 — `/kb-draft`, capture at resolution

**Input**

```
/kb-draft — resolved now, restarting the interface engine service manually
cleared it. Worklog: engine restart after maintenance left the RIS-to-PACS
queue stalled; ops restarted the engine service at 03:10, queue drained,
orders resumed flowing within 2 minutes. Confirmed root cause: engine
service didn't reattach to the RIS-to-PACS queue after the scheduled
restart.
```

**Expected behavior**

- No site-specific KB template on file → uses `skills/knowledge/references/kb-template.md`,
  labeled generic in the output
- Title is symptom-oriented, not a ticket number
- Cause marked `confirmed` — the worklog states it as confirmed, not inferred
- Resolution steps trace exactly to the worklog — two steps, nothing added
- Outstanding: incident reference, not stated
- A suggestion (post-restart verification step for the runbook) appears in a
  visibly separate suggestions block, never merged into the article body

**The demo point:** the same incident that generated a page in Turn 1 and a
notification in Turns 2–3 becomes institutional knowledge in Turn 4, at the
moment the context still exists — the argument `knowledge/SKILL.md` opens
with, demonstrated rather than asserted.

---

## Turn 5 — `/explain`, unrelated aside

**Input**

```
/explain what's the difference between accession number and order number?
```

**Expected behavior**

- Depth 1 answer first (one or two sentences), not the full reference doc
- States the practical consequence (searching PACS by order number finds
  nothing) rather than only the definitional difference
- Offers to go deeper (site-specific identifier formats) rather than
  dumping them unprompted

**The demo point:** explainer's shortest-answer-first rule holds even
mid-incident — this turn is deliberately placed after resolution to show the
skill doesn't need an incident in progress to be useful, and doesn't
over-answer when one just wrapped.

---

## Optional turn 6 — `/setup review`

**Input**

```
/setup review
```

**Expected behavior**

- Reports populated vs. empty sections against `site-profile.schema.md`
- Does not auto-fill anything
- For this example profile: `systems`, `interfaces`, `escalation_matrix`,
  `sla_tiers`, `downtime_procedures`, `audiences` all populated;
  `identifier_formats.mrn` present but approximate ("7 digits" rather than a
  full pattern) — worth flagging as a real gap rather than treating an
  approximate answer as equivalent to a precise one

---

## What this demo does and does not prove

**Does:** that the five capabilities compose against one site profile and
one comms profile without contradicting each other; that confidence marks
move (`likely` → `confirmed`) as evidence changes rather than staying static;
that an incident's facts flow forward through triage → comms → knowledge
without re-derivation; that a generic fallback (KB template, in Turn 4) is
labeled as such rather than presented as site-tuned.

**Does not:** exercise the symbolic HL7 parse layer, the de-identification
gate, ServiceNow connected mode, or a live cold-start interview (Turn 6 uses
a pre-populated example rather than running the interview live) — none of
which exist yet or apply here. Forensics is deliberately excluded — see
[ADR-0008](adr/0008-separate-forensics-plugin.md).

---

## Companion — the persona, on its own

The six turns above show the persona applied to an incident. `demo/persona-card.html`
plus its narration (`demo/persona-narration.md` for ElevenCreative Studio,
`demo/persona-narration-supertonic.md` for the fully-local path) is a
three-minute module that isolates the persona itself — Field/Tenor/Mode,
confidence marking, the audience-register example, and the hardcoded-default
boundary story from `docs/PERSONA-SPEC.md` — with no ticket attached. Useful
as a standalone credibility piece, or as a lead-in before Turn 1 if a
stakeholder asks "why should I trust what it says" before "what does it do."

## Running it for a stakeholder

Fifteen minutes, six turns, one incident. If time is short, run Turns 1–3
only — clarification into a live notification is the shortest path to "this
isn't a template filler, it's reasoning over evidence." Add Turn 4 if the
audience cares about knowledge management specifically; add Turn 5 or 6 only
if there's time left over, since neither depends on the incident thread.
