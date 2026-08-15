# Architectural Overview

Detailed architecture of RIS Assist — a Claude plugin for Radiology Information System support work.

---

## System Boundary

```
┌─────────────────────────────────────────────────────────────────────┐
│                        Claude Desktop                               │
│  ┌───────────────────────────────────────────────────────────────┐  │
│  │                    RIS Assist Plugin                          │  │
│  │  ┌─────────┐  ┌─────────┐  ┌─────────┐  ┌─────────┐        │  │
│  │  │Troublesh│  │Knowledge│  │ Comms   │  │Explainer│  ...    │  │
│  │  └────┬────┘  └────┬────┘  └────┬────┘  └────┬────┘        │  │
│  │       │            │            │            │               │  │
│  │       └────────────┴─────┬──────┴────────────┘               │  │
│  │                          │                                   │  │
│  │                   PERSONA-SPEC.md                            │  │
│  └──────────────────────────┬───────────────────────────────────┘  │
│                             │                                      │
└─────────────────────────────┼──────────────────────────────────────┘
                              │ reads/writes
                    ┌─────────▼─────────┐
                    │  Local Filesystem  │
                    │  (outside plugin)  │
                    │                    │
                    │  site-profile.yaml │
                    │  comms-profile.yaml│
                    │  *.html (articles) │
                    └────────────────────┘
```

**Boundary principle:** The plugin ships generic. Site-specific configuration lives outside the plugin directory, written by `/onboarding`, read at runtime by skills. Nothing site-specific ever enters the repository.

---

## Component Architecture

### The Five Skills

| Skill | Backlog | Purpose | Input | Output |
|-------|---------|---------|-------|--------|
| **troubleshoot** | E8 | Differential-driven ticket clarification | Vague ticket text | Symptom, scope, timeline, differential w/ confidence, recommended queue |
| **knowledge** | E7 | Resolved ticket → KB article | Worklog text | Self-contained HTML article + `.docx` |
| **comms** | E6 | Service-impact notifications | Event details | Drafted notification (event × audience × channel) |
| **explainer** | E5 | Domain concept explanation | Question | Depth-adjustable answer |
| **onboarding** | E2 | Cold-start site profile | Interview responses | YAML profile file |

### Skill Internal Structure

Every skill follows the same pattern:

```
skills/<skill>/
├── SKILL.md              # Behavior authority (invoked by command)
└── references/           # Domain knowledge (read by skill)
    ├── <topic>.md
    └── ...
```

**Invocation chain:**

```
User → /command → commands/<command>.md → skills/<skill>/SKILL.md → references/
```

**Exception:** `knowledge` has `scripts/html_to_docx.py` — the only executable code in the plugin (outside demo).

### The Persona

`docs/PERSONA-SPEC.md` is the single source of truth for the analyst persona. Three sections:

| Section | Defines | Example |
|---------|---------|---------|
| **Field** | Domain scope, two sources (site profile vs. references) | "Order lifecycle, accession vs. order number, MWL" |
| **Tenor** | Operational stance, confidence marking, audience register | "confirmed / likely / possible" marks on every conclusion |
| **Mode** | Execution framework, output conventions | "Observation separate from inference, always" |

**Governance rule:** If a skill's instructions and PERSONA-SPEC.md disagree, the spec wins; fix the skill. Skills reference the spec, never restate it.

---

## Data Flow: Knowledge Pipeline (Manual Mode)

```
┌──────────────┐     ┌──────────────┐     ┌──────────────┐     ┌──────────────┐
│   Worklog    │     │   SKILL.md   │     │  html_to_    │     │  ServiceNow  │
│  (pasted)    │────▶│  (model)     │────▶│  docx.py     │────▶│  (human      │
│              │     │              │     │  (code)      │     │   uploads)   │
└──────────────┘     └──────────────┘     └──────────────┘     └──────────────┘
      Source            Drafts HTML         Renders .docx        Attaches to
                                                   │             KB record
                                                   │
                                          ┌────────▼────────┐
                                          │  article.html   │
                                          │  (Word-openable │
                                          │   zero-dep alt) │
                                          └─────────────────┘
```

**Key properties:**
- **Deterministic rendering:** Code maps HTML tags to Word styles; model drafts content, code renders
- **Zero-dependency default:** Word-openable HTML works on any Windows machine with Word
- **Style single source:** `servicenow-format.md` is the spec; CSS in Word header + script styles implement it
- **Heading shift:** HTML `<h2>` → DOCX Heading 1 (ServiceNow renders title separately from body)

---

## Data Flow: Triage Differential

```
User: "PACS won't open a study"
            │
            ▼
┌───────────────────────────────────────────────────────┐
│                  TROUBLESHOOT SKILL                     │
│                                                       │
│  Differential:                                        │
│  ┌─────────────────┐  ┌─────────────────┐            │
│  │ RIS Config      │  │ Interface       │            │
│  │ (order status)  │  │ (queue depth)   │            │
│  └────────┬────────┘  └────────┬────────┘            │
│           │                    │                       │
│  ┌────────▼────────┐  ┌───────▼─────────┐            │
│  │ PACS            │  │ Workstation     │            │
│  │ (listener/node) │  │ (single user)   │            │
│  └────────┬────────┘  └───────┬─────────┘            │
│           │                    │                       │
│           └────────┬───────────┘                       │
│                    ▼                                   │
│              User (procedural)                         │
│                                                       │
│  Stop condition: ONE branch live at "likely"+          │
│  Output: symptom, scope, timeline, differential,      │
│          recommended queue, SLA justification          │
└───────────────────────────────────────────────────────┘
```

**Question selection:** Pick the question whose two possible answers rule out the most branches. If you can predict the next question regardless of the answer, it wasn't discriminating.

**Overnight prior:** Change-window question asked first (scheduled maintenance is disproportionately the cause at 2 AM).

---

## Data Flow: Communications

```
User: "Draft a downtime notice for radiology"
            │
            ▼
┌───────────────────────────────────────────────────────┐
│                    COMMS SKILL                         │
│                                                       │
│  1. Resolve variant key:                              │
│     event_class × audience × channel                  │
│                                                       │
│  2. Select template:                                  │
│     Exact match → nearest variant → generic fallback  │
│                                                       │
│  3. Fill slots from STATED FACTS ONLY:                │
│     ┌─────────┐  ┌─────────┐  ┌─────────┐           │
│     │ Required│  │ Required│  │ Unknown │           │
│     │ Field 1 │  │ Field 2 │  │ Field 3 │           │
│     │ ✓ filled│  │ ✓ filled│  │ [gap]   │           │
│     └─────────┘  └─────────┘  └─────────┘           │
│                                                       │
│  4. Apply audience register:                          │
│     Clinical → action first                           │
│     Technical → failure first                         │
│     Leadership → scope first                          │
│                                                       │
│  5. Mark causal claims: confirmed / suspected         │
└───────────────────────────────────────────────────────┘
            │
            ▼
     Draft notification + outstanding items
     (never invents ETA, cause, or impact scope)
```

---

## Dependency Map

### External Dependencies (DEP-#)

| ID | Dependency | Status | Blocks |
|----|-----------|--------|--------|
| **DEP-1** | ServiceNow MCP access (read incidents / write KB) | Pending | E7.3, E7.4, E8.7 |
| **DEP-2** | M365 Copilot PHI/BAA coverage | Pending | E12.1–E12.4 |
| **DEP-3** | Employer/client IP + OSS publication | Pending | Public repo publication |

### Internal Dependencies

```
PERSONA-SPEC.md ◄────────────────────────────────────┐
       │                                              │
       ├── troubleshoot/SKILL.md                     │
       ├── knowledge/SKILL.md                        │
       ├── comms/SKILL.md                            │
       ├── explainer/SKILL.md                        │
       └── onboarding/SKILL.md                       │
                                                    │
agents/analyst.md ─── references ───────────────────┘
```

**No circular dependencies.** Skills reference the persona spec; the persona spec references nothing in the plugin.

---

## Deployment Architecture

```
┌─────────────────────────────────────────────────────────┐
│                  MSP-Managed Windows                     │
│                                                         │
│  ┌───────────────────────────────────────────────────┐  │
│  │              Claude Desktop                        │  │
│  │  ┌─────────────────────────────────────────────┐  │  │
│  │  │         RIS Assist Plugin                    │  │  │
│  │  │         (cached directory)                   │  │  │
│  │  └─────────────────────────────────────────────┘  │  │
│  └───────────────────────────────────────────────────┘  │
│                                                         │
│  ┌───────────────────────────────────────────────────┐  │
│  │              Local Filesystem                      │  │
│  │  C:\Users\<analyst>\ris-assist\                   │  │
│  │  ├── site-profile.yaml                            │  │
│  │  ├── comms-profile.yaml                           │  │
│  │  └── articles\                                    │  │
│  │      └── *.html                                   │  │
│  └───────────────────────────────────────────────────┘  │
│                                                         │
│  No Python, no pip, PowerShell unless Git for Windows   │
└─────────────────────────────────────────────────────────┘
```

**Environment constraints:**
- `python3` is not a Windows command (resolves to Store alias stub)
- `${CLAUDE_PLUGIN_ROOT}` is model-substituted, not PowerShell-expanded
- Shell examples are PowerShell-first, bash second
- Default output must work with nothing installed

---

## Extension Points

### Adding a New Skill

1. Create `plugins/ris-assist/skills/<new-skill>/SKILL.md`
2. Add `name` and `description` in YAML frontmatter
3. Reference `PERSONA-SPEC.md` (never restate persona rules)
4. Add `references/` directory if domain knowledge needed
5. Create `plugins/ris-assist/commands/<action>.md` that invokes the skill
6. Document in `BACKLOG.md` under appropriate epic

### Adding a New Agent

1. Create `plugins/ris-assist/agents/<name>.md`
2. Reference `PERSONA-SPEC.md` for behavioral rules
3. Agent is an alternative invocation path for the skill

### Profile Extension

Site and comms profiles are extensible by user:
- `/onboarding` writes site profile (interview mode)
- `/comms-config` writes comms profile (capture/build/edit/review modes)
- Profiles live outside the plugin directory

---

## Quality Attributes

| Attribute | How Achieved |
|-----------|-------------|
| **Reliability** | Graceful degradation: missing profile → honest "not configured", never invent |
| **Observability** | Confidence marks on every conclusion; observation/inference separation |
| **Maintainability** | Single source of truth (PERSONA-SPEC.md); ADRs for every decision |
| **Portability** | Zero-dependency default (Word-openable HTML); PowerShell-first |
| **Security** | Synthetic data only; de-identification gate in code; no PHI in repo |
| **Auditability** | Guardrails G1–G10 checked against; unsquashed commit history |

---

## Anti-Patterns (Documented & Prevented)

| Anti-Pattern | Prevention | Reference |
|-------------|-----------|-----------|
| Confident interpolation | G1: mark generated content | GUARDRAILS.md |
| Vocabulary import | G2: name assumptions on first use | GUARDRAILS.md |
| Assumption laundering | G3: restate unconfirmed assumptions | GURAIDRAILS.md |
| Provenance collapse | G4: distinguish "suggested" from "decided" | GUARDRAILS.md |
| Silent correction | G5: flag when contradicting earlier facts | GUARDRAILS.md |
| Fabricated specificity | G6: verify tool/platform specifics | GUARDRAILS.md |
| Scope inflation | G7: push back on additions that outrun the phase | GUARDRAILS.md |
| Demo ahead of substrate | G8: refuse to demo before mechanism exists | GUARDRAILS.md |
| Agreement drift | G9: keep disagreeing where warranted | GUARDRAILS.md |
| Artifact substitution | G10: keep derived docs distinguishable from work | GUARDRAILS.md |

---

## Open Items

| Item | Status | Reference |
|------|--------|-----------|
| Word list formatting (ul/ol) | Unconfirmed under G6 | ADR-0010 |
| Overnight technical distinctions | Asserted from general patterns, not confirmed | PERSONA-SPEC.md |
| Connected-mode ServiceNow | Blocked on DEP-1 | BACKLOG.md E7.3 |
| MS 365 Copilot track | Deferred on DEP-2 | BACKLOG.md E12 |
| /troubleshoot, /explain, /onboarding wiring | Commands exist, may not be fully connected | BACKLOG.md E8.6 |
| /comms-config interview modes | Partially implemented | BACKLOG.md E6.6–E6.9 |
