# Demo — the comms pipeline

A scripted walkthrough of one capability end to end, using the fictional
`examples/comms-profile.example.yaml`. No installation required: paste
`skills/comms/SKILL.md` and the example profile into a Claude session, then run
the four turns below in order.

Purpose: show that the branching is real — that the command resolves a variant
key, handles a defined variant, a *missing* variant, and a continuity case
differently, and says so each time.

**Everything here is fictional.** Riverside Regional Imaging does not exist.

---

## Setup

Give the session two things:

1. The comms skill instructions (`skills/comms/SKILL.md`)
2. The example comms profile (`examples/comms-profile.example.yaml`)

Then state: *"Treat the profile as this site's configuration. Assume no
ServiceNow access."*

---

## Turn 1 — the happy path

**Input**

```
/downtime unplanned RIS-to-PACS order interface
```

**What to watch for.** The command has an event class and a system but no
audience and no scope. Correct behavior is to ask — one question — not to pick
an audience and produce something.

**Expected shape**

> Which audience — radiologists, technologists, or IT/NOC?

Answer: `radiologists`.

**Expected draft characteristics**

- Uses the `unplanned / radiologists / teams` variant
- Leads with the action, not the failure
- Short — the profile notes radiologists read the first two lines
- Names the read path in site language: read direct from the PACS worklist
- Required fields present: incident reference, affected workflows, workaround,
  next update time
- Anything not supplied appears as `[TBD]` and is listed beneath the draft
- No ETA and no cause invented

**The demo point:** the draft is in the site's voice because the profile taught
it that voice, not because the model guessed well.

---

## Turn 2 — the branch that matters

**Input**

```
Same outage. Now one for the front desk.
```

**What to watch for.** The profile has no front-desk variant — it is listed
explicitly under `gaps`. This is the branch that separates a useful tool from a
confident one.

**Expected behavior**

- Substitutes the nearest defined variant (technologists / email)
- **Says** it substituted, and why
- Adapts register toward scheduling workflow rather than silently reusing tech
  instructions
- Offers `/comms-tune capture` to define the real variant
- Does not fabricate a distribution list — `distribution.front_desk` is
  defined, but the *template* is not, and the output distinguishes those

**The demo point:** the gap is visible in the output. A tool that quietly
produced a plausible front-desk notice would be worse, not better.

---

## Turn 3 — continuity

**Input**

```
/downtime update — still down, cause looks like the interface engine
queue, next update in 30 minutes
```

**Expected behavior**

- Uses `interval_update / all / teams`, where `continuity: required`
- Carries forward the incident reference, original start time, and previously
  stated impact — without being re-told them
- Leads with the delta, not a restatement
- Marks the cause `suspected`, per `conventions.cause_marking`
- Applies the severity-1 cadence from the profile

**The demo point:** the incident is a thread, not a series of unrelated
messages. Facts already published are carried, not re-derived.

---

## Turn 4 — the correction case

**Input**

```
Correction — it wasn't the queue. Interface engine is fine, it's the
downstream PACS listener. Resolved now.
```

**Expected behavior**

- Uses `resolved / all / email`, continuity required
- **Explicitly flags that a previously published fact changed** rather than
  quietly issuing a clean all-clear
- Marks the corrected cause `confirmed` only if stated as confirmed
- Lists residual actions, including "none" when there are none
- Applies the profile's apology rule: resolution notices only, one sentence

**The demo point:** this is the behavior that determines whether people keep
reading incident comms. Silent correction is how a comms trail loses its
audience.

---

## Optional turn 5 — customization

**Input**

```
/comms-tune capture
```

Paste any two fictional notifications. Watch for: extraction shown back for
confirmation *before* anything is written, inferences distinguished from
assumptions, and the local-storage reminder about staff names and contacts.

---

## What this demo does and does not prove

**Does:** that variant resolution branches on a real key; that a missing
variant produces a named substitution rather than a fabrication; that incident
continuity and correction are handled as first-class cases; that site language
comes from configuration rather than from the model's priors.

**Does not:** exercise the symbolic HL7 parse layer, the de-identification
gate, or any ServiceNow integration — none of which exist yet. The forensics
capability is deliberately not demoed, because demoing it before the parser
exists would demonstrate exactly the freestyle-parsing behavior this project
is built to avoid.

---

## Running it for a stakeholder

Twelve minutes, four turns, one screen. Lead with Turn 2 if you only get five
minutes — the substitution-with-disclosure branch is the one that answers
"how do I know it isn't making things up," and it answers it by demonstration
rather than assurance.
