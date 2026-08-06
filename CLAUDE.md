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
  skill"** section defining its boundary. All five (triage, knowledge, comms,
  explainer, setup) are implemented; four of the five (all but `triage`) have
  a `references/` subdirectory of supporting docs (schemas, templates, generic
  fallbacks) — triage's differential logic lives directly in its `SKILL.md`.
  What's still
  missing is the `/comms-tune` build/capture/edit/review interview modes
  themselves and some slash-command wiring — check `docs/BACKLOG.md` for
  exact per-item status rather than assuming from a skill's presence alone.
- **`docs/PERSONA-SPEC.md` is the single source of truth for the analyst
  persona** — stance, confidence marking, audience register, boundaries.
  `plugins/ris-triage/agents/analyst.md` (an invocable subagent) and every
  `SKILL.md` reference it rather than restating it; if a skill's instructions
  and the spec disagree, the spec wins. **Do not duplicate persona rules into
  a skill file** — link to the relevant section instead.
  **Packaging note:** only `plugins/ris-triage/` ships to the plugin cache on
  install, so runtime references use `${CLAUDE_PLUGIN_ROOT}/PERSONA-SPEC.md`,
  which resolves to `plugins/ris-triage/PERSONA-SPEC.md` — a packaged copy of
  the root file. Edit `docs/PERSONA-SPEC.md`, then re-copy it to
  `plugins/ris-triage/PERSONA-SPEC.md` before shipping; the two must not
  drift.
- **Site profile / comms profile** are user data written by `/setup` and
  `/comms-tune` to a **local path outside this repository**. Never write
  site-specific config into this repo. `plugins/ris-triage/examples/site-profile.example.yaml`
  and `.../comms-profile.example.yaml` are the schema references (schemas
  themselves live in each skill's `references/`), keyed to the fictional site
  "Riverside Regional Imaging."
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
trigger-phrase rich — it's how the skill gets invoked). Every skill ends with
a **"Not this skill"** section defining its boundary, and states which
backlog epic it implements (`Implements backlog E##`). Pieces blocked on an
external dependency (e.g. ServiceNow MCP) say so inline and describe the
manual-mode fallback rather than being left unbuilt silently.

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

`docs/PROJECT-INSTRUCTIONS.md`'s "Current state" section tracks open items,
currently just unconfirmed overnight technical assumptions (change-window
faults, DST boundary cases) flagged under GUARDRAILS G3. Check it before
assuming a name or field is final.

Two demo pairs exist and are companions, not alternatives: `docs/DEMO-comms.md`
+ `demo/coverage-demo.html`/`narration*` goes deep on the comms skill alone;
`docs/DEMO-full.md` + `demo/persona-card.html`/`persona-narration*` walks all
five skills as one incident thread and then isolates the persona itself.
Keep both in sync with `examples/site-profile.example.yaml` and
`examples/comms-profile.example.yaml` — the two demos deliberately reference
the same fictional site and incident details.
