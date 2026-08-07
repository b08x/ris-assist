<p align="center">
  <img src="docs/assets/icon.svg" width="150" alt="RIS Triage icon — a single continuous stroke looping through one central node">
</p>

<h1 align="center">RIS Triage</h1>

<p align="center"><strong>Ticket clarification, knowledge capture, incident communications,<br>
and analyst onboarding — for radiology IT support.</strong></p>

<p align="center">A Claude plugin for the people who keep a Radiology Information System running.</p>

<p align="center">
  <img src="https://img.shields.io/badge/status-pre--alpha-E8A13D" alt="Status: pre-alpha">
  <img src="https://img.shields.io/badge/license-Apache--2.0-8317B4" alt="License: Apache-2.0">
  <img src="https://img.shields.io/badge/built%20with-Claude-14101A" alt="Built with Claude">
</p>

---

## What this is

RIS support lives at a messy intersection: tickets arrive from radiologists,
techs, and scheduling staff about a system wired into PACS, dictation, the
EHR, and a tangle of HL7 interfaces. Most "RIS problems" are really
integration problems, most triage knowledge lives in one senior analyst's
head, and most of it walks out the door at every staff rotation.

RIS Triage packages that senior analyst's working method as a Claude plugin.
It asks the one clarifying question that actually discriminates between
causes. It turns resolved tickets into knowledge articles at the moment the
context still exists. It drafts the downtime alert while you deal with the
downtime. And it answers the domain questions a new analyst would otherwise
have to interrupt someone to ask.

It is built for the overnight support engineer first — alone, no senior
analyst to ask, vendor support behind a callback queue — and degrades
gracefully into daylight. Only the message-forensics work is
radiology-specific; the rest is shape-identical for any 24/7 support desk.

It is a triage assistant, not an operator: it drafts, decodes, and
recommends. It does not execute, and it does not guess. See
[What it will not do](#what-it-will-not-do).

## Capabilities

| Skill | What it does |
|---|---|
| **Triage** | Differential-driven ticket clarification — one discriminating question at a time — ending in a routable triage artifact with SLA-vocabulary justification |
| **Knowledge** | Resolved ticket → triage-first KB article as a self-contained, Word-openable HTML file (Open with → Word → Save As `.docx`, no installed tooling required); gap detection; stale-article flags. Closes the loop automatically where a ServiceNow MCP connection is available |
| **Comms** | Templated downtime alerts, major-incident cadence updates, vendor tickets, change narratives, and shift-turnover summaries — audience-matched, required fields never invented |
| **Explainer** | Order lifecycle, accession vs. order number, MWL, report-status flow, and a guided onboarding path for analysts new to radiology |

Slash commands: `/triage` · `/kb-draft` · `/downtime` · `/explain`
· `/setup` · `/comms-tune`

**Message forensics is a separate plugin**, not a missing feature — see
[ADR-0008](docs/adr/0008-separate-forensics-plugin.md). It waits on data access
and on a symbolic parse layer, and shipping a model-interpreted version in the
meantime would be the exact behavior this project argues against. Parked work
is tracked in [FORENSICS-BACKLOG.md](docs/FORENSICS-BACKLOG.md).

## The analyst persona

Every skill speaks through the same persona: fifteen years in radiology IT,
calm, allergic to filler. Its rules are structural, not cosmetic — full spec
in [`docs/PERSONA-SPEC.md`](docs/PERSONA-SPEC.md):

- **Observation is separated from inference**, always.
- Every diagnostic conclusion carries a confidence mark: *confirmed / likely / possible*.
- Process claims cite the SOP, SLA definition, or site topology by name — or state that no source exists.
- Anything absent from your site profile is declared absent, never given a plausible fiction.
- Anything patient-safety-adjacent or state-changing is flagged as a human decision.

## How it's built

Three design commitments shape everything here:

**Deterministic where it matters.** Anything that can be decided by code is
decided by code, and the model reasons over the result rather than over raw
input. This is why message forensics ships separately: a language model
freestyle-parsing pipe-delimited clinical data is the failure mode this
project exists to avoid, and the parse layer has to exist first.

**Your site stays yours.** The plugin ships generic. On first run, a
cold-start interview asks about *your* RIS, interfaces, escalation matrix,
and SLA tiers, and writes a site profile to a local path outside the plugin —
it survives updates and never touches this repository. A fictional example site in
[`plugins/ris-triage/examples/`](plugins/ris-triage/examples/) demonstrates the
schema.

**Synthetic from birth.** Every example in this repository is invented.
Nothing derives from production clinical data — not even de-identified
derivatives, because provenance survives scrubbing. See the
[data provenance statement](docs/DATA-PROVENANCE.md).

## Install

> Verify against current [Claude plugin docs](https://code.claude.com/docs)
> — the plugin surface is evolving quickly.

```
/plugin marketplace add <owner>/ris-triage
/plugin install ris-triage@ris-triage
```

Then run the cold-start interview when prompted, and keep the resulting site
profile wherever your local secrets live — it is yours, not the plugin's.

## What it will not do

- Execute message replays, resends, or any state-changing operation
- Handle identified PHI — workflows requiring live patient data belong on
  platforms your compliance team has approved for them
- Invent a process, a distribution list, an approval chain, or present
  speculation as finding
- Parse HL7 messages — that is the separate forensics plugin
- Make patient-safety-adjacent calls — those are flagged, packaged, and
  handed to a human

The full statement lives in [`docs/NON-GOALS.md`](docs/NON-GOALS.md).

## Development transparency

This plugin is developed in collaboration with Claude, and that process is
part of what's published:

- **Decision records** in [`docs/adr/`](docs/adr/) capture why it's built
  this way — symbolic-first parsing, the site-profile split, synthetic-only
  data, and the rest — including rejected alternatives.
- **[User stories](docs/USER_STORIES.md)** and the
  **[backlog](docs/BACKLOG.md)** are versioned here; their commit history is
  the project's paper trail.
- The **AI-assistance disclosure** below is maintained, not performed:
  design, drafting, and reference material are co-developed with Claude;
  behavior rules and published claims are validated by a human before
  release. [`docs/GUARDRAILS.md`](docs/GUARDRAILS.md) documents the specific
  failure modes that collaboration is checked against.

## Roadmap

Current phase: **foundation** — scaffold, site-profile schema, persona spec,
and the governance approvals that gate publication. The sequencing and its
reasoning are in [`docs/BACKLOG.md`](docs/BACKLOG.md).

## License

[Apache-2.0](LICENSE). Patent grant included on purpose — this is
healthcare-adjacent tooling, and adopters' OSS reviews will thank you.
