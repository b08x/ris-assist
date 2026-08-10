# AGENTS.md - RIS Assist

## What This Is

RIS Assist is a Claude plugin for Radiology Information System (RIS) support work. It is **not** source code you build and run — it is documentation, commands, and skills that shape the Claude Desktop experience for overnight support engineers.

The repository **doubles as a plugin marketplace** (see `.claude-plugin/marketplace.json`).

---

## Repository Layout

```
RIS_Assist/
├── plugins/ris-assist/        # The main plugin content
│   ├── commands/             # 5 slash commands
│   │   ├── triage.md
│   │   ├── kb-draft.md
│   │   ├── downtime.md
│   │   ├── explain.md
│   │   ├── setup.md
│   │   └── comms-tune.md
│   ├── skills/               # 5 skills (SKILL.md files); 4 have a references/ dir
│   │   ├── triage/           #   no references/ — differential logic lives in SKILL.md itself
│   │   ├── knowledge/        #   references/{kb-template,servicenow-format}.md + scripts/html_to_docx.py
│   │   ├── comms/            #   references/{comms-profile.schema,generic-templates,register-guide}.md
│   │   ├── explainer/        #   references/{order-lifecycle,accession-vs-order-number,modality-worklist,report-status-flow,topology-patterns}.md
│   │   └── setup/            #   references/site-profile.schema.md
│   ├── agents/
│   │   └── analyst.md        # Persona as an invocable subagent (operational summary of PERSONA-SPEC.md)
│   ├── examples/             # Fictional site examples ("Riverside Regional Imaging")
│   │   ├── site-profile.example.yaml
│   │   ├── comms-profile.example.yaml
│   │   └── kb-article-*.example.html
│   └── .claude-plugin/
│       ├── plugin.json       # Plugin metadata
│       └── marketplace.json  # Makes this repo its own marketplace
├── demo/                     # Non-functional demo scripts
│   ├── build_narration.py    # Generates audio for demos using Supertonic
│   ├── coverage-demo.html / narration*.{md,txt}      # Comms-only demo (companion: docs/DEMO-comms.md)
│   └── persona-card.html / persona-narration*.{md,txt} # Persona-only demo (companion: docs/DEMO-full.md)
├── docs/                     # Project documentation
│   ├── adr/                  # Architectural decision records
│   ├── BACKLOG.md            # Feature prioritization
│   ├── DATA-PROVENANCE.md    # Synthetic data policy
│   ├── DEMO-comms.md         # Scripted walkthrough — comms skill alone
│   ├── DEMO-full.md          # Scripted walkthrough — all five skills, one incident thread
│   ├── GUARDRAILS.md         # Guardrails/G1-G10 patterns
│   ├── NON-GOALS.md          # Explicit non-goals and boundaries
│   ├── PERSONA-SPEC.md       # Single source of truth for the analyst persona (Field/Tenor/Mode)
│   ├── PROJECT-INSTRUCTIONS.md # Project rules for collaborative work
│   ├── ROADMAP.md             # ServiceNow/MS 365 connectors + parked forensics backlog (DEP-1/2, F-DEP-1/2/3)
│   ├── USER_STORIES.md       # Feature requirements
│   └── assets/               # Icons and logos
├── .claude-plugin/           # Root plugin config
│   └── marketplace.json
├── .gitignore
├── CONTRIBUTING.md
├── LICENSE (Apache-2.0)
├── README.md
└── AGENTS.md
```

---

## Key Architectural Principles

### 1. Separate Profile from Plugin Code

**Site profiles live OUTSIDE the plugin directory**. They are written by `/setup` during the cold-start interview. The plugin ships generic; nothing site-specific ever enters this repository.

**Why?**

- Installed plugins are cached and replaced on update. A profile inside would be lost on every upgrade.
- Risks site-specific data reaching the public repository.

**Profile locations** (user-configured):

- Site profile: systems, interfaces, escalation matrix, SLA tiers
- Comms profile: templates keyed by `event_class × audience × channel`

Both are read at runtime by the skills; neither is committed to git.

### 2. Synthetic Data Only

**All test data is synthetic from birth.** The fictional example site is "Riverside Regional Imaging" — every name is invented. Nothing derives from production clinical data, not even de-identified derivatives.

See `docs/DATA-PROVENANCE.md` for the full policy.

**Consequence**: Do not use real patient data, real system names, or real interface names in this repo.

### 3. Symbolic Parse Before Model Interpretation

This is a design commitment, not a TODO:

- Envelope extraction, segment splitting, and field mapping happen in reviewable code.
- A model freestyle-parsing pipe-delimited clinical data is the failure mode this project exists to prevent.
- Message forensics is a **separate plugin** (see `docs/adr/0008-separate-forensics-plugin.md`).

### 4. Graceful Degradation

Every skill degrades honestly:

- Missing profile field → says "not in your site profile", never invents.
- Untuned template → labels output "generic — not yet tuned to this site".
- Unknown system name → records as unknown, does not assume a value.

### 5. Persona Has One Source of Truth

`docs/PERSONA-SPEC.md` is the single source for the analyst persona — stance,
confidence marking, audience register, boundaries. `agents/analyst.md` (the
invocable subagent) and each skill's `SKILL.md` reference it rather than
restating it; if a skill's instructions and the spec disagree, the spec wins
and the skill gets fixed. **Do not duplicate persona rules into a skill file**
— link to the relevant section of `PERSONA-SPEC.md` instead.

The audience register in that spec is deliberately generic (Clinical /
Technical / Leadership, by tenor) and never hardcodes a specific roster — an
earlier draft hardcoded a specific audience label as a default without
confirming it against a real site (GUARDRAILS G2). The label itself has since
been scrubbed from every doc, demo, and example; the fix is that the roster
is interview-derived, every time, with the general lesson (not the specific
invented term) documented in the spec and demonstrated in
`demo/persona-narration.md`.

---

## The Five Skills

### `/triage` - Ticket Clarification

**Purpose**: Differential-driven clarification of vague tickets. Asks one discriminating question at a time until the ticket is routable.

**File**: `plugins/ris-assist/commands/triage.md` → invokes `skills/triage/SKILL.md`

**Behavior**:

- Maintains a differential: RIS configuration · interface · PACS · workstation · user
- Asks questions that separate remaining branches only
- Overnight: asks the change-window question first (scheduled maintenance, patching, engine restarts are disproportionately common)
- Output includes: symptom, scope, timeline, differential with confidence marks (`confirmed`/`likely`/`possible`), recommended queue, SLA vocabulary severity justification

**Not this skill**: Message-level analysis (that's the forensics plugin).

### `/kb-draft` - Knowledge Capture

**Purpose**: Turns resolved tickets into knowledge base article drafts.

**Files**:

- Command: `plugins/ris-assist/commands/kb-draft.md`
- Skill: `plugins/ris-assist/skills/knowledge/SKILL.md`

**Modes**:

- **Manual** (default): triage-first, Word-openable HTML article (analyst does Open with → Word → Save As `.docx`), plus outstanding items and a separate suggestions block; works with zero ServiceNow access and zero installed tooling. The Python renderer is optional and not the Windows path — see ADR-0010
- **Connected**: reads resolved incident, drafts, and submits with category/workflow state (blocked: DEP-1 — requires ServiceNow MCP access)

**Article shape** (see ADR-0009): scope first, then the triage differential's branches in order — workstation/user, application (RIS/PACS), interface, advanced — then verification, cause with a confidence mark, escalation, related. Only the layers the worklog supports are emitted; the rest are listed as outstanding.

**Rules**:

- Conform to the site's article template from the profile
- Separate observation from inference (same as everywhere else)
- Do not invent reproduction steps that were not in the worklog
- Suggestions and outstanding items live in the response, never in the HTML or the `.docx`
- Never invent an image `src`; screenshots of production systems are presumed to contain patient data and are the site's call
- No article gaps are accepted — gaps are recorded in the profile as stale-article flags

### `/downtime` - Communications

**Purpose**: Drafts service-impact notifications (downtime, major-incident updates, vendor tickets, change narratives, shift turnover).

**Files**:

- Command: `plugins/ris-assist/commands/downtime.md`
- Skill: `plugins/ris-assist/skills/comms/SKILL.md`

**Key concept**: Comms variants are keyed by three axes: `event_class × audience × channel`.

**Workflow** (from `/downtime` command):

1. Resolve the variant key from user input
2. Select the template from the comms profile
3. Fill required slots from stated facts only (never infer ETA, cause, or impact scope)
4. Apply the audience register:
   - **Clinical audiences**: lead with action the reader must take, name downtime procedure explicitly, describe impact in workflow terms
   - **Technical audiences**: lead with the failure, include interface and queue names
   - **Leadership**: lead with scope, duration, and actions underway
5. Mark causal claims as `confirmed` or `suspected` (per comms profile convention)
6. For interval updates: carry forward incident reference, original start time, and previously stated impact

**If comms profile missing**: say so in one line and offer `/comms-tune`. Then continue with built-in generic templates, labelling output clearly.

**Comms profile structure** (example in `plugins/ris-assist/examples/comms-profile.example.yaml`):

- `version`, `site` (fictional in example)
- `conventions`: timezone, time format, placeholder token, cause marking (required), incident ref format, quiet hours
- `distribution`: distribution lists by role
- `approval`: approval chains by severity level
- `workflow_language`: site-local names for downtime procedures, paper requisition slips, dictation fallback, etc.
- `voice`: formality, person ("first person plural (we)"), apology language, banned phrases
- `variants`: keyed by event class × audience × channel, each with:
  - `required_fields`
  - `lead_with` (action/scopes/delta/resolution)
  - `sections`
  - `lead_time`
  - `continuity` (required for interval updates and all-clears)
  - `notes`
- `gaps`: explicitly recorded gaps (present so absence is visible)

### `/explain` - Domain Explanation & Onboarding

**Purpose**: Explains radiology IT domain concepts at adjustable depth. Also runs a sequenced onboarding path for analysts new to the account.

**Files**:

- Command: `plugins/ris-assist/commands/explain.md`
- Skill: `plugins/ris-assist/skills/explainer/SKILL.md`

**Coverage** (backlog E5.1):

- Order lifecycle
- Accession vs. order number
- Modality worklist (MWL)
- Report status flow
- RIS ↔ PACS ↔ EHR topology patterns

**Rules**:

- Generic domain claims come from `references/` (order lifecycle, accession vs.
  order number, MWL, report status flow, RIS↔PACS↔EHR topology — each with
  three depth tiers)
- Site-specific claims come from the site profile
- If profile lacks the detail, say so and answer generically with that caveat stated
- Default to the shortest answer that actually answers, then offer to go deeper

### `/setup` - Cold-Start Interview

**Purpose**: Builds the site profile during first run, then handles single-field edits later.

**Files**:

- Command: `plugins/ris-assist/commands/setup.md`
- Skill: `plugins/ris-assist/skills/setup/SKILL.md`

**Modes**:

- **Interview** (first run): one question at a time. Derive later answers as deltas from earlier ones rather than walking a full matrix.
- **Edit**: change one field without re-interviewing. Preserve everything not under discussion.
- **Review**: report which fields are populated, empty, and gaps likely to be needed soon. Do not auto-fill.

**Rules**:

- Never invent a system name, interface name, distribution list, procedure name, or approval chain. Unknown is recorded as unknown.
- Accept "we don't distinguish that" as a complete answer and record it.
- The audience set is site- and shift-specific. Ask separately about who is reachable overnight (usually different from daytime).
- Site profile schema: `skills/setup/references/site-profile.schema.md` (E2.1)

### `/comms-tune` - Customize Profiles

**Purpose**: Customizes the comms profile (build variants, edit templates, review gaps).

**File**: `plugins/ris-assist/commands/comms-tune.md`

Four modes:

- **capture**: infer variants from pasted examples
- **build**: guided construction, deltas from most common notification
- **edit**: one variant, no re-interview
- **review**: coverage against the axes, gaps ranked

Design rules for the interview:

- One question per turn
- Derive, don't enumerate (establish base, then ask only what differs)
- Accept "we don't distinguish that" and record it
- Confirm inferences explicitly when in capture mode
- Unknowns are recorded as unknown

---

## Slash Commands

### Command File Format

Each slash command is a markdown file with a YAML frontmatter header:

```yaml
---
description: One-line description of what the command does.
argument-hint: "[expected argument format or examples]"
allowed-tools: [List of allowed Claude tools, e.g., Read, Write]
---
```

Required fields in SKILL.md:

- `name`: skill identifier (used by the platform to invoke it)
- `description`: detailed, trigger-phrase rich description

Standard pattern for command files that invoke skills:

```markdown
STUB — see `skills/<skill_name>/SKILL.md` for the behavior this command invokes.

Arguments: $ARGUMENTS

If the site profile is missing or the needed field is unpopulated, say so in one
line and offer `/setup`. Continue with generic behavior, labelled as untuned.
```

### File Naming

- Commands: `<action>.md` (e.g., `triage.md`, `kb-draft.md`)
- Skills: `<action>/SKILL.md` (e.g., `triage/SKILL.md`)
- Example configs: `*.example.yaml`

---

## Project-Wide Patterns

### SKILL.md Structure

Each SKILL.md file follows this pattern:

```yaml
---
name: <identifier>
description: Detailed description with trigger phrases.
---

# <Skill Name>

STUB — implements backlog <E##>.

## <Section>

Content...

## Not this skill

<Explanation of what this does NOT do.>
```

**Always include**:

- `name` and `description` in YAML frontmatter
- STUB marker referencing the backlog item
- **"Not this skill"** section at the end explaining boundaries (especially for skills that are "don't cross" like triage not doing message forensics)

### Decision Records (ADR)

Architectural decisions go in `docs/adr/`. Each ADR is numbered chronologically and follows the chronological index in `docs/adr/README.md`.

Example: `0008-separate-forensics-plugin.md` explains why message forensics is a separate plugin.

### Backlog (BACKLOG.md)

Feature prioritization follows the platform-constraint sequencing:

- **P0**: foundation & governance groundwork
- **P1**: domain explainer + comms (ships first, no approval dependencies)
- **P2**: KB pipeline (blocked by ServiceNow MCP access)
- **P3**: ticket clarification
- **PX**: Copilot parallel track (deferred until BAA/PHI confirmed)

Use the format: `[ ] ID (Size) — description` where Size = S (≤half day), M (1–3 days), L (multi-day).

External dependencies are tracked as DEP-1 (ServiceNow MCP), DEP-2 (Copilot PHI/BAA), DEP-3 (IP/OSS approval).

### Non-Goals (NON-GOALS.md)

Explicit non-goals are a design commitment, enforced in skill instructions and persona rules. Each non-goal is a paragraph explaining what the project will not do and why.

Key non-goals:

- Does not execute (no state-changing operations)
- Does not guess (unrecognized segments = unknown)
- Does not blur observation and inference (every conclusion needs a confidence mark)
- Does not make patient-safety-adjacent calls (flags them for human)
- Does not parse HL7 messages (separate forensics plugin)
- Does not handle identified PHI (deterministic script gate at ingress)
- Does not carry site config into the world (profiles live outside plugin)
- Does not replace the senior analyst (onboarding reduces interruptions, not substitution)

### Guardian Rules (GUARDRAILS.md)

Ten specific failure modes (G1-G10) that are checked for:

- **G1** — Confident interpolation: when generating anything not stated by user or present in artifacts, mark it as generated.
- **G2** — Vocabulary import: when domain terms enter from the model, name them as assumptions on first use.
- **G3** — Assumption laundering: before building substantially on unconfirmed assumptions, restate them as unconfirmed.
- **G4** — Provenance collapse: distinguish "I suggested" from "you decided."
- **G5** — Silent correction: when contradicting something said earlier, say you are contradicting it.
- **G6** — Fabricated specificity: verify tool/plugin/platform specifics against docs; if unsure, mark as unverified.
- **G7** — Scope inflation: push back on additions that outrun the phase; say when something belongs in the backlog.
- **G8** — Demo ahead of substrate: refuse to demo capabilities whose supporting mechanism doesn't exist yet.
- **G9** — Agreement drift: keep disagreeing where warranted, even late in the thread.
- **G10** — Artifact substitution: keep the distinction visible between derived documents and the work itself.

When a guardrail fires, say so in the response rather than routing around it. Bias toward flagging.

---

## Development Workflow

### Adding New Skills or Commands

1. Create the directory structure: `plugins/ris-assist/skills/<new_skill>/` or `plugins/ris-assist/commands/<new_command>.md`
2. Create SKILL.md or command markdown file with proper YAML frontmatter
3. Add name and description to the skill
4. Implement STUB marker if implementing backlog item
5. Add relevant references to `plugins/ris-assist/skills/<skill>/references/` if needed
6. Document in BACKLOG.md under the appropriate epic and phase
7. Update THIS FILE (AGENTS.md) if adding cross-cutting knowledge

### Modifying Existing Skills or Commands

1. Read the existing file to understand current implementation
2. Make changes following the established patterns
3. Ensure any guardrails (G1-G10) or non-goals are respected
4. Update documentation (BACKLOG.md, GUARDRAILS.md) as needed
5. If modifying a command that invokes a skill, update the STUB reference

### Documentation Standards

- ADRs: create in `docs/adr/` with numbered filename and index entry
- Non-goals: one paragraph per item, explaining commitment
- BACKLOG.md: use consistent format, track phases, and DEP-# references
- USER_STORIES.md: feature requirements with US-# identifiers
- BACKLOG and USER_STORIES: keep commit history as the project's paper trail

### Contributing

PRs containing real clinical data are closed without merge. Add test cases by extending the generator or contributing fictional fixtures produced by it (see `docs/DATA-PROVENANCE.md`).

---

## Command Reference (Quick)

| Command | Purpose | Triggers | Main Skill |
| --------- | --------- | ---------- | ------------ |
| `/triage` | Clarify tickets, route them | "where should this go", "is this worth paging someone" | triage |
| `/kb-draft` | Draft KB article from resolved ticket | "write this up", "is there an article for this" | knowledge |
| `/downtime` | Draft service notifications | "draft a downtime notice", "we need to tell clinical", "all clear" | comms |
| `/explain` | Explain domain concepts, onboarding | "what is an accession number", "walk me through the order lifecycle", "I'm new to this account" | explainer |
| `/setup` | Build site profile, edit fields | "set up", "configure my site", "change my escalation contact" | setup |
| `/comms-tune` | Customize comms profiles | (implicit, invoked by commands) | comms |

---

## External Dependencies (DEP-#)

These are tracked, not owned:

- **DEP-1**: ServiceNow MCP access decision (scope: read incidents/write KB)
- **DEP-2**: M365 Copilot PHI/BAA coverage confirmation
- **DEP-3**: Employer/client IP + OSS publication approval

When referring to these in docs, use "DEP-#".

---

## Additional Resources

- **Installation**: `/plugin marketplace add <owner>/ris-assist` → `/plugin install ris-assist@ris-assist` (per README.md)
- **Data Provenance**: Why synthetic-only data policy exists (docs/DATA-PROVENANCE.md)
- **Architectural Decisions**: Rejected alternatives and design choices (docs/adr/)
- **Project Instructions**: Collaborative work rules (docs/PROJECT-INSTRUCTIONS.md)
