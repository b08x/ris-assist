# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## What this repository is

RIS Triage is a **Claude plugin**, not an application. There is no build, lint,
or test command — the repository is markdown (slash commands, skills, docs)
plus one non-functional demo script. Verify any change by reading the
frontmatter and prose for internal consistency, not by running anything.

```bash
claude plugin validate .                              # validate plugin structure
/plugin marketplace add /absolute/path/to/this/repo    # local install for testing
/plugin install ris-triage@ris-triage
```

The repo doubles as its own plugin marketplace: root `.claude-plugin/marketplace.json`
points at `plugins/ris-triage/`. This layout (rather than a manifest at repo
root) exists so a second plugin — message forensics — can ship from the same
repo later (see `docs/adr/0008-separate-forensics-plugin.md`).

## Architecture

- **Commands** (`plugins/ris-triage/commands/*.md`) are thin stubs with YAML
  frontmatter (`description`, `argument-hint`, `allowed-tools`) that invoke a
  skill: `/triage`, `/kb-draft`, `/downtime`, `/explain`, `/setup`, `/comms-tune`.
- **Skills** (`plugins/ris-triage/skills/<name>/SKILL.md`) hold the actual
  behavior, each with `name`/`description` frontmatter and a **"Not this
  skill"** section defining its boundary. Only `skills/comms/` is fully
  implemented; the rest are stubs carrying correct frontmatter and behavioral
  rules but no full implementation — check for a `STUB` marker before assuming
  a skill does more than draft placeholder behavior.
- **Site profile / comms profile** are user data written by `/setup` and
  `/comms-tune` to a **local path outside this repository**. Never write
  site-specific config into this repo; `plugins/ris-triage/examples/comms-profile.example.yaml`
  is the schema reference, keyed to the fictional site "Riverside Regional Imaging."
- **Message forensics is a separate, not-yet-built plugin** (parked in
  `docs/FORENSICS-BACKLOG.md`). It waits on a symbolic (code, not model) HL7
  parse layer — see the "Symbolic parse before model interpretation"
  commitment below. Do not add HL7 parsing to this plugin.

## Design commitments (enforced in skill instructions, not just style)

- **Symbolic parse before model interpretation.** Anything decidable by code
  is decided by code; the model reasons over the result, never freestyle-parses
  raw structured data (e.g. pipe-delimited HL7).
- **Graceful degradation.** A missing profile field renders as "not in your
  site profile," never a plausible invention. An untuned template is labeled
  "generic — not yet tuned to this site."
- **Observation vs. inference.** Every diagnostic conclusion carries a
  confidence mark: `confirmed` / `likely` / `possible`. Unmarked speculation
  is a defect.
- **Cite-or-decline.** Process claims name the SOP, SLA definition, or site
  profile field — or state that no source exists. Never invent field
  mappings, procedure names, distribution lists, or approval chains.
- **It does not execute.** No replays, resends, queue operations, or any
  state-changing action — draft and recommend only. See `docs/NON-GOALS.md`.
- **Synthetic data only, from birth.** Never real clinical data, real site
  names, or de-identified derivatives of either — provenance survives
  scrubbing. See `docs/DATA-PROVENANCE.md`. PRs containing real clinical or
  site data are closed without merge (`CONTRIBUTING.md`).

## Conventions when adding or editing commands/skills

Command file frontmatter:
```yaml
---
description: One-line description of what the command does.
argument-hint: "[expected argument format or examples]"
allowed-tools: [...]
---
```

SKILL.md frontmatter requires `name` and `description` (description is
trigger-phrase rich — it's how the skill gets invoked). Stub skills should
carry a `STUB — implements backlog <E##>` marker and end with a **"Not this
skill"** section.

Naming: commands are `<action>.md`; skills are `<action>/SKILL.md`; example
configs are `*.example.yaml`.

## Docs that govern behavior, not just describe it

- `docs/NON-GOALS.md` — explicit boundaries; a change to any of them is an
  ADR-level decision.
- `docs/GUARDRAILS.md` — G1–G10, named failure modes for AI-assisted work on
  this repo itself (confident interpolation, vocabulary import, assumption
  laundering, scope inflation, etc.). When one fires, say so rather than
  routing around it — this applies to Claude Code sessions on this repo, not
  only to the shipped skills.
- `docs/adr/` — architectural decisions including rejected alternatives;
  substantive design changes get one, per `docs/adr/README.md` numbering.
- `docs/BACKLOG.md` — phase-sequenced (P0–P3, PX) with size tags (S/M/L) and
  `DEP-#` external-dependency references (ServiceNow MCP access, Copilot
  PHI/BAA, IP/OSS publication approval).

## Known pre-alpha state

`SCAFFOLD-NOTES.md` and `docs/PROJECT-INSTRUCTIONS.md` track open items,
including `TODO` placeholders in `plugin.json` / `marketplace.json` (owner,
repo URL) and an in-progress audience-taxonomy rework (the "front desk" label
in `demo/` is a flagged invention pending replacement). Check these before
assuming a name or field is final.
