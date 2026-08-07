<div align="center">
  <img src="docs/assets/icon.svg" width="150" alt="RIS Assist icon — a single continuous stroke looping through one central node">
  <h1>RIS Assist</h1>
  <p>Ticket clarification, knowledge capture, incident communications, and analyst onboarding — for radiology IT support.</p>
  <p>
    <img src="https://img.shields.io/badge/status-pre--alpha-E8A13D" alt="Status: pre-alpha">
    <img src="https://img.shields.io/badge/license-Apache--2.0-8317B4" alt="License: Apache-2.0">
    <img src="https://img.shields.io/badge/built%20with-Claude-14101A" alt="Built with Claude">
  </p>
</div>

---

A Claude plugin for the people who keep a Radiology Information System running.

RIS support lives at a messy intersection: tickets arrive from radiologists, techs, and scheduling staff about a system wired into PACS, dictation, the EHR, and a tangle of HL7 interfaces. Most "RIS problems" are really integration problems, most triage knowledge lives in one senior analyst's head, and most of it walks out the door at every staff rotation.

RIS Assist packages that senior analyst's working method as a Claude plugin. It asks the one clarifying question that actually discriminates between causes. It turns resolved tickets into knowledge articles at the moment the context still exists. It drafts the downtime alert while you deal with the downtime. And it answers the domain questions a new analyst would otherwise have to interrupt someone to ask.

## Features

- **Triage**: Differential-driven ticket clarification — one discriminating question at a time — ending in a routable triage artifact with SLA-vocabulary justification.
- **Knowledge**: Resolved ticket to triage-first KB article as a self-contained HTML file. Closes the loop automatically where a ServiceNow connection is available.
- **Comms**: Templated downtime alerts, major-incident cadence updates, vendor tickets, change narratives, and shift-turnover summaries — audience-matched, required fields never invented.
- **Explainer**: Order lifecycle, accession vs. order number, MWL, report-status flow, and a guided onboarding path for analysts new to radiology.

## Installation

> Verify against current [Claude plugin docs](https://code.claude.com/docs) — the plugin surface is evolving quickly.

```bash
/plugin marketplace add <owner>/ris-assist
/plugin install ris-assist@ris-assist
```

Then run the cold-start interview when prompted, and keep the resulting site profile wherever your local secrets live — it is yours, not the plugin's.

## Usage

Interact with RIS Assist using the provided slash commands within Claude Desktop:

- `/triage`: Clarify and route a ticket.
- `/kb-draft`: Turn a resolved ticket into a knowledge base article.
- `/downtime`: Generate a downtime communication draft.
- `/explain`: Clarify radiology concepts and workflows.
- `/setup`: Run the cold-start interview to configure your site profile.
- `/comms-tune`: Tune communication preferences and templates.

> **Note:** RIS Assist drafts, decodes, and recommends. It does not execute state-changing operations, parse raw HL7, or process identified PHI. See [NON-GOALS.md](docs/NON-GOALS.md) for the complete list.

## The Analyst Persona

Every skill speaks through the same persona: fifteen years in radiology IT, calm, allergic to filler. Its rules are structural, not cosmetic — full spec in [`docs/PERSONA-SPEC.md`](docs/PERSONA-SPEC.md):

- **Observation is separated from inference**, always.
- Every diagnostic conclusion carries a confidence mark: *confirmed / likely / possible*.
- Process claims cite the SOP, SLA definition, or site topology by name — or state that no source exists.
- Anything absent from your site profile is declared absent, never given a plausible fiction.
- Anything patient-safety-adjacent or state-changing is flagged as a human decision.

## Architecture & Data

- **Deterministic where it matters.** Anything that can be decided by code is decided by code, and the model reasons over the result rather than over raw input. Message forensics ships as a separate plugin (see [ADR-0008](docs/adr/0008-separate-forensics-plugin.md)).
- **Your site stays yours.** The plugin ships generic. A cold-start interview writes a site profile to a local path outside the plugin. A fictional example site in [`plugins/ris-assist/examples/`](plugins/ris-assist/examples/) demonstrates the schema.
- **Synthetic from birth.** Every example in this repository is invented. Nothing derives from production clinical data. See the [data provenance statement](docs/DATA-PROVENANCE.md).

## Development Transparency

This plugin is developed in collaboration with Claude, and that process is part of what's published:

- **Decision records** in [`docs/adr/`](docs/adr/) capture why it's built this way.
- **[User stories](docs/USER_STORIES.md)** and the **[backlog](docs/BACKLOG.md)** are versioned here; their commit history is the project's paper trail.
- **Guardrails:** AI-assistance disclosure is maintained. The specific failure modes that collaboration is checked against are documented in [`docs/GUARDRAILS.md`](docs/GUARDRAILS.md).

## Contributing

Review the current phase (foundation) in [`docs/BACKLOG.md`](docs/BACKLOG.md) to align with ongoing work on the persona spec, site profile schema, and comms profile schema. Pull requests and issues are welcome.

## License

[Apache-2.0](LICENSE). Patent grant included on purpose — this is healthcare-adjacent tooling, and adopters' OSS reviews will thank you.
