# Documentation Index

Sorted by category, then by purpose. Each entry links to the file and states what it governs.

---

## Governance & Process

| File | Purpose | Governs |
|------|---------|---------|
| [`PROJECT-INSTRUCTIONS.md`](PROJECT-INSTRUCTIONS.md) | Collaboration rules for AI-assisted development | How the project is built, guarded, and verified |
| [`GUARDRAILS.md`](GUARDRAILS.md) | Ten named AI failure modes (G1–G10) | Development process, not runtime behavior |
| [`NON-GOALS.md`](NON-GOALS.md) | Design commitments — what the plugin will not do | Execution boundary, PHI handling, guessing policy |
| [`DATA-PROVENANCE.md`](DATA-PROVENANCE.md) | Synthetic-from-birth data policy | Test data, examples, de-identification gate |

## Requirements & Specifications

| File | Purpose | Governs |
|------|---------|---------|
| [`USER_STORIES.md`](USER_STORIES.md) | Feature requirements (US-01…US-29) | What each persona needs, acceptance criteria |
| [`BACKLOG.md`](BACKLOG.md) | Task prioritization (E1–E12, DEP-1/2/3) | What gets built, in what order, what's blocked |
| [`PERSONA-SPEC.md`](PERSONA-SPEC.md) | Analyst persona — Field, Tenor, Mode | Stance, confidence marking, audience register, boundaries |

## Architecture & Decisions

| File | Purpose | Governs |
|------|---------|---------|
| [`ARCHITECTURE.md`](ARCHITECTURE.md) | Detailed architectural overview | System boundary, data flows, dependencies, extension points |
| [`adr/README.md`](adr/README.md) | ADR index and format spec | How decisions are recorded |
| [`adr/0008-separate-forensics-plugin.md`](adr/0008-separate-forensics-plugin.md) | Message forensics split into own plugin | Scope boundary, dependency structure |
| [`adr/0009-servicenow-shaped-kb-output.md`](adr/0009-servicenow-shaped-kb-output.md) | ServiceNow-shaped KB output replaces KCS template | Article shape, triage-first ordering |
| [`adr/0010-word-readable-html-as-the-default-artifact.md`](adr/0010-word-readable-html-as-the-default-artifact.md) | Word-readable HTML is default; Python renderer optional | Zero-dependency path, PowerShell-first |

## Connector & Forensics Documentation

| File | Purpose | Governs |
|------|---------|---------|
| [`kb-serviceNow-ms365-connectors.md`](kb-serviceNow-ms365-connectors.md) | ServiceNow & MS 365 integration overview | Current capabilities, blocked dependencies, upload paths |
| [`FORENSICS-BACKLOG.md`](FORENSICS-BACKLOG.md) | Message forensics long-term backlog (parked) | FE1–FE5, blocking dependencies (F-DEP-1/2/3) |

## Demos & Walkthroughs

| File | Purpose | Governs |
|------|---------|---------|
| [`DEMO-full.md`](DEMO-full.md) | Scripted walkthrough — all five skills, one incident thread | End-to-end capability demonstration |
| [`DEMO-comms.md`](DEMO-comms.md) | Scripted walkthrough — comms skill alone | Notification drafting demonstration |

## Assets & Visuals

| Directory | Contents |
|-----------|----------|
| [`assets/`](assets/) | Icons and logos |
| [`imgs/`](imgs/) | Persona spec analysis and prompt images |

---

## Reading Order (by persona)

### New Analyst (onboarding)
1. `PERSONA-SPEC.md` — understand the persona
2. `DEMO-full.md` — see it in action
3. `USER_STORIES.md` — understand what each capability does

### Site Adopter (installing the plugin)
1. `README.md` (root) — installation and usage
2. `PROJECT-INSTRUCTIONS.md` — how to collaborate
3. `BACKLOG.md` — what's built, what's coming

### Governance Stakeholder (reviewing for compliance)
1. `DATA-PROVENANCE.md` — synthetic data policy
2. `NON-GOALS.md` — what the plugin won't do
3. `GUARDRAILS.md` — AI failure mode checks
4. `adr/` — decision records with alternatives considered

### Maintainer / Developer
1. `PROJECT-INSTRUCTIONS.md` — collaboration rules
2. `ARCHITECTURE.md` — detailed architecture and data flows
3. `BACKLOG.md` — current state and next sprint
4. `adr/README.md` — decision index
5. `CONTRIBUTING.md` (root) — PR policy
