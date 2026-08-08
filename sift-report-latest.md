---
name: sift-protocol-system-review
description: Full SIFT protocol system design review for ris-assist repository. Generated from iterative analysis sessions.
---

# SIFT Protocol System Design Review - ris-assist

STUB — implements comprehensive system analysis per sift-protocol skill. Consolidates findings from multiple iterative analysis passes.

> **Generated**: 2026-08-07  
> **Repository**: b08x/ris-assist  
> **Health Score**: 2/5  
> **Status**: Foundational risk - enforcement mechanisms missing

---

## 🔍 Preview: 4 Search Queries & Bias Critique

| # | Query | Bias Critique |
|---|-------|----------------|
| 1 | `"Claude plugin marketplace dependency isolation patterns"` | **Platform bias**: Assumes Claude's plugin sandbox provides isolation. Doesn't account for shared state via user prompts or filesystem access. Misses the repo's explicit rejection of shared state (see [AGENTS.md §1](#)). |
| 2 | `"YAML frontmatter schema validation for skill files"` | **Syntactic bias**: Focuses on schema compliance, not semantic correctness. A valid YAML can still violate persona rules (G4). |
| 3 | `"how to enforce synthetic data constraints in markdown templates"` | **Medium bias**: Overweights markdown parsing. The real constraint is at *ingress* (see [NON-GOALS.md](#): "deterministic script gate at ingress"). Templates are downstream of the gate. |
| 4 | `"plugin skill dependency graph visualization tools"` | **Tool bias**: Assumes visualization is the goal. The actual need is *dependency elimination*—the architecture explicitly avoids cross-skill dependencies (see [AGENTS.md §4](#): "Every skill degrades honestly"). |

**Revised approach**: Focus on *enforcement mechanisms* for existing architectural commitments, not discovery of new patterns.

---

## 📋 Identified Issues & Requirements Table

| Item | Type | Description & Context | Priority |
|------|------|----------------------|----------|
| 1.0 | Architecture | No explicit interface between `/triage` (command) and `triage/SKILL.md` (skill). Command files are STUBs but the invocation mechanism isn't documented or validated. | 5 |
| 1.1 | Architecture | Skills reference PERSONA-SPEC.md but there's no version pinning. A PERSONA-SPEC update could silently break all skills without detection. | 5 |
| 1.2 | Architecture | Cross-skill state leakage risk: No `SkillContext` schema defines what data can be passed between skills (e.g., triage → comms). | 4 |
| 1.3 | Architecture | Profile separation relies on user discipline. No runtime validation that site profiles remain outside the plugin directory. | 4 |
| 2.0 | Data Flow | The "deterministic script gate at ingress" (NON-GOALS.md) is described but not implemented. No actual gate exists in the repo to block PHI. | 5 |
| 2.1 | Data Flow | Example files use fictional "Riverside Regional Imaging" but no validation that custom site profiles follow synthetic data constraints. | 3 |
| 2.2 | Data Flow | Message forensics explicitly separated (ADR-0008) but triage lacks an explicit trigger condition to escalate to forensics plugin. | 4 |
| 3.0 | Resilience | Graceful degradation lacks telemetry. If a skill falls back to generic behavior, there's no log/record of the gap for `/setup` to address. | 4 |
| 3.1 | Resilience | No timeout for external MCP calls (ServiceNow, GitHub). A network partition could hang skills indefinitely. | 3 |
| 3.2 | Resilience | Missing profile fields → "not in your site profile" is correct behavior but not actionable. No gap tracking for `/setup`. | 3 |
| 4.0 | Governance | ADR-0008 (separate forensics plugin) doesn't specify *how* triage detects it needs forensics. The trigger condition is implicit only. | 4 |
| 4.1 | Governance | BACKLOG.md tracks DEP-1 (ServiceNow MCP) but doesn't document the fallback behavior for `/kb-draft` connected mode. | 3 |
| 4.2 | Governance | Persona rules duplicated across skills (G4: Provenance collapse). Skills restate PERSONA-SPEC.md content instead of linking. | 4 |
| 5.0 | Testing | No automated test suite for skills. Manual verification only. | 2 |
| 5.1 | Testing | No regression tests for ADR decisions. ADR-0008 could be violated by future code without detection. | 3 |

---

## ⚙️ Problem Analysis & Potential Solutions Table

| Issue/Requirement Ref. | Analysis/Root Cause | Proposed Solution/Approach | Confidence |
|----------------------|---------------------|---------------------------|------------|
| 1.0 | Command files declare `STUB — see skills/<skill>/SKILL.md` but there's no documented mechanism for how the command invokes the skill. This is a correctness gap: the contract is implied, not explicit. | Add `plugins/ris-assist/.claude-plugin/invocation.json` that explicitly maps commands → skills → entry points, with JSON Schema validation. Fail CI on invalid mappings. | 5 |
| 1.1 | PERSONA-SPEC.md is referenced by all skills but has no semantic versioning. A breaking change to persona rules (e.g., new confidence marking scale) requires manual audit of all SKILL.md files. | Add a `persona-version` field to PERSONA-SPEC.md frontmatter. Skills must declare compatible versions via `persona-version-compat` in their frontmatter. CI fails on mismatch. | 5 |
| 1.2 | Skills share no explicit interface contract. The `triage` skill could emit state that `comms` consumes without validation, leading to cross-skill coupling. | Define a `SkillContext` schema in `docs/adr/0011-skill-context-schema.md` that all skills must honor for cross-skill data. Schema includes: `session_id`, `site_profile_ref`, `user_context`, `skill_state`. | 4 |
| 1.3 | Profile separation relies on user discipline. A profile inside the plugin directory would be lost on update. No runtime validation exists. | Add a `profile-validator.py` script that checks at skill invocation: (1) profile path is outside plugin directory, (2) profile matches synthetic data patterns from DATA-PROVENANCE.md. | 4 |
| 2.0 | NON-GOALS.md states: "deterministic script gate at ingress" but this is aspirational. The repo accepts any input. No script exists. | Implement a Git pre-receive hook (`hooks/pre-receive-phigate`) that scans all new/changed files for PHI patterns using the regex library from `docs/DATA-PROVENANCE.md` Appendix A. Block commits with PHI. | 4 |
| 2.1 | Example files use "Riverside Regional Imaging" but there's no validation that custom site profiles follow the same synthetic pattern. | Extend `profile-validator.py` to check all YAML files in `examples/` and any user-provided profiles against synthetic constraints: no real system names, interfaces, distribution lists, or patient data derivatives. | 3 |
| 2.2 | ADR-0008 says forensics is separate, but triage has no explicit trigger. The current design relies on the analyst recognizing the need. | Add a `forensics_needed` boolean field to the triage differential output. When message-level analysis is required (e.g., pipe-delimited clinical data), triage sets this flag to `true`, blocks further processing, and emits a handoff: `{"action": "escalate", "target": "forensics-plugin", "reason": "message parsing required"}`. | 4 |
| 3.0 | Skills fall back to generic templates but don't emit telemetry. The gap between "site needs X" and "/setup can provide X" is invisible. | Add a `gap-log.json` (append-only, in user's `.claude-plugin/ris-assist/` directory) that skills append to when falling back. Each entry: `{"timestamp": ..., "skill": ..., "gap": ..., "context": ...}`. `/setup` reads this log to prioritize interview questions. | 4 |
| 3.1 | MCP calls have no timeout. A network partition to ServiceNow could hang `/kb-draft` connected mode indefinitely. | Wrap all MCP calls in a 10-second timeout with exponential backoff (max 3 retries). Fall back to manual mode with warning: `"[MCP UNAVAILABLE] Falling back to manual mode. DEP-1 may be down."`. | 3 |
| 3.2 | Missing profile fields → "not in your site profile" is correct but not actionable. No gap tracking for `/setup`. | Extend gap-log.json to include profile gaps: `{"type": "profile_gap", "field": "escalation_matrix", "skill": "triage"}`. `/setup` surfaces these as "Your site profile is missing these fields used in the last 24h". | 3 |
| 4.0 | ADR decisions have no test coverage. A future PR could add HL7 parsing to triage skill, violating ADR-0008. | Add an ADR compliance test suite in `tests/adr-compliance/`. Each ADR has a corresponding test: e.g., `test_adr_0008.py` greps for `hl7\|HL7\|parse.*message` in `skills/triage/` and fails if found. | 4 |
| 4.1 | BACKLOG.md lists DEP-1 as a blocker for `/kb-draft` connected mode but doesn't document the fallback behavior. | Add a `DEP-1 Fallback` section to BACKLOG.md and a `FALLBACK.md` in `docs/`: when MCP is unavailable, `/kb-draft` uses manual mode with a "connected mode unavailable (DEP-1)" label and disables ServiceNow submission. | 3 |
| 4.2 | Persona rules duplicated across skills (G4: Provenance collapse). `triage/SKILL.md` and `knowledge/SKILL.md` both restate confidence marking rules from PERSONA-SPEC.md. | Replace all duplicated persona rules in SKILL.md files with links to the relevant section of PERSONA-SPEC.md. Add a CI check (`tests/persona-no-duplication.py`) that flags any text matching PERSONA-SPEC.md content outside of direct links. | 5 |
| 5.0 | No automated test suite for skills. Changes to PERSONA-SPEC.md could break all skills silently. | Create a property-based test suite (`tests/skills/`) that: (1) generates synthetic tickets from `tests/fixtures/`, (2) invokes each skill, (3) validates outputs against persona rules and skill-specific requirements. | 2 |
| 5.1 | No regression tests for ADR decisions. ADR-0008 could be violated by future code without detection. | Implement ADR regression tests as part of CI. Each ADR has a `tests/adr/test_<adr-number>.py` that enforces the decision's constraints. Run on every PR. | 4 |

---

## 📌 Key Findings & Proposed Changes Summary

### 1. Critical Architectural Gaps (P0)

**Command-to-skill invocation is undocumented and unvalidated** (1.0). The entire plugin system relies on an implied contract. Without explicit mapping, the system cannot guarantee correct skill invocation.

**Persona versioning is missing** (1.1). The single source of truth (PERSONA-SPEC.md) has no mechanism to propagate breaking changes to dependent skills. This is a **correctness time bomb**.

**Deterministic ingress gate is unimplemented** (2.0). The non-goal of "no PHI" cannot be enforced without a gate. This is a **foundational risk** for the project's compliance stance.

### 2. Cross-Cutting Governance Issues (P0)

**ADR decisions lack enforcement** (5.1). Architectural decisions like ADR-0008 (separate forensics plugin) can be silently violated without test coverage. This undermines the entire ADR process.

**Persona rule duplication** (4.2) violates G4 (Provenance collapse). This is both a governance failure and a maintenance burden.

### 3. Resilience and Observability Gaps (P1)

**No telemetry for graceful degradation** (3.0). The system cannot improve what it cannot measure. Gap tracking is essential for the `/setup` interview to remain relevant.

**MCP calls lack timeouts** (3.1). External dependencies without resilience patterns will cause cascading failures. This blocks P2 features from shipping safely.

### 4. Data Integrity Risks (P1)

**Synthetic data constraints are unenforced** (2.1). Example files and custom profiles could drift from the synthetic-only policy without validation.

**Forensics escalation is implicit** (2.2). Triage cannot reliably detect when message forensics is needed, violating the separation commitment in ADR-0008.

### 5. Testing Vacuum (P2)

**No automated tests for skills** (5.0). The system is manually verified. This is unsustainable as the skill count grows and blocks safe iteration.

---

## 🚀 Potential Optimizations & Next Steps

### Ordered by Priority and Dependency

| Phase | Task | Dependencies | Effort | Impact |
|-------|------|--------------|--------|--------|
| **P0** | Implement pre-receive PHI gate (`hooks/pre-receive-phigate`) | None | M (1-2 days) | Blocks PHI at source; foundational for all data integrity |
| **P0** | Add command-to-skill invocation mapping (`invocation.json`) | None | S (<1 day) | Explicit contract; enables validation and testing |
| **P0** | Add persona versioning with CI check | invocation.json | S (<1 day) | Prevents silent persona rule breakage |
| **P0** | Replace duplicated persona rules with links + CI check | None | S (<1 day) | Fixes G4 violation; reduces maintenance burden |
| **P0** | Add ADR compliance tests (`tests/adr-compliance/`) | invocation.json | M (2-3 days) | Prevents architectural drift; enforces ADR decisions |
| **P1** | Implement gap telemetry (`gap-log.json`) | invocation.json | S (<1 day) | Enables data-driven `/setup` interviews |
| **P1** | Add MCP timeouts with fallback | None | S (<1 day) | Prevents hanging on external dependencies |
| **P1** | Add forensics trigger to triage differential | ADR compliance tests | M (1-2 days) | Explicit escalation path per ADR-0008 |
| **P1** | Create profile validator (`profile-validator.py`) | invocation.json | M (1-2 days) | Enforces profile separation and synthetic data |
| **P1** | Document DEP-1 fallback in BACKLOG.md and FALLBACK.md | None | S (<1 day) | Clarifies behavior; user expectation management |
| **P2** | Build property-based test suite for skills | invocation.json, ADR compliance tests | L (3-5 days) | Enables safe iteration; catches regressions |
| **P2** | Extend profile validator to example files | profile-validator.py | S (<1 day) | Prevents example drift from synthetic constraints |

### Parallelizable Work
- **P0 tasks are independent** and can be done in any order (except where noted).
- **P1 tasks** can start once P0 invocation.json is complete.
- **P2 tasks** require P0 and P1 foundations.

---

## 📚 Resource & Tool Assessment Table

| Resource/Tool | Usefulness Assessment | Notes | Rating |
|--------------|----------------------|-------|--------|
| [Git Hooks](https://git-scm.com/docs/githooks) | High | Pre-receive hooks can enforce PHI gate at the repo level. Already supported by Git; no new dependencies. | 5 |
| [JSON Schema](https://json-schema.org/) | High | Validating `invocation.json` and `SkillContext` schema. Standard, no runtime dependency for validation. | 5 |
| [Claude Code MCP](https://docs.anthropic.com/claude/code/mcp) | Medium | For MCP calls to ServiceNow/GitHub. Reliable but needs timeout/circuit breaker wrapping. | 3 |
| [pytest](https://docs.pytest.org/) | High | Test framework for ADR compliance tests and skill test suite. Python-native; aligns with existing scripts. | 5 |
| [Great Expectations](https://greatexpectations.io/) | Low | Data validation framework. Overkill for YAML/profile validation; custom scripts are sufficient. | 2 |
| [Semgrep](https://semgrep.dev/) | Medium | Static analysis for ADR compliance (e.g., detect HL7 parsing). Could replace custom grep tests. | 4 |
| [jsonschema (Python)](https://python-jsonschema.readthedocs.io/) | High | Runtime validation of `invocation.json` and `SkillContext`. Lightweight, already in Python ecosystem. | 5 |
| [structlog](https://www.structlog.org/) | Medium | Structured logging for gap telemetry. Nice-to-have but JSON lines are sufficient for `gap-log.json`. | 3 |

---

## 💻 Revised Code/Solution Overview

### New Files to Add
```
hooks/
└── pre-receive-phigate          # PHI gate (Bash + Python)
plugins/ris-assist/
├── .claude-plugin/
│   └── invocation.json          # Command→skill mapping with schema
├── tests/
│   ├── adr_compliance/
│   │   ├── test_adr_0008.py     # No HL7 parsing in triage
│   │   └── test_adr_0009.py     # KB article structure
│   ├── skills/
│   │   └── test_triage.py       # Property-based skill tests
│   └── persona_no_duplication.py # CI check for duplicated persona rules
└── scripts/
    ├── profile_validator.py     # Synthetic data constraint checker
    └── gap_telemetry.py          # gap-log.json management
docs/
├── adr/
│   └── 0011-skill-context-schema.md # Cross-skill data contract
├── FALLBACK.md                  # DEP-1 and other fallback behaviors
└── DATA-PROVENANCE.md           # Add Appendix A: PHI regex patterns
```

### Modified Files
| File | Changes |
|------|---------|
| `plugins/ris-assist/skills/*/SKILL.md` | Remove duplicated persona rules; add `persona-version-compat` to frontmatter; link to PERSONA-SPEC.md sections |
| `plugins/ris-assist/commands/*.md` | Add explicit reference to `invocation.json` mapping |
| `docs/PERSONA-SPEC.md` | Add `persona-version` to frontmatter |
| `docs/BACKLOG.md` | Add `DEP-1 Fallback` section; update priorities |
| `docs/AGENTS.md` | Update to reference new `invocation.json` and `SkillContext` schema |

### Key Code Snippets

**`invocation.json`**
```json
{
  "$schema": "https://json-schema.org/draft/2020-12/schema",
  "type": "object",
  "properties": {
    "commands": {
      "type": "object",
      "patternProperties": {
        "^/": {
          "type": "object",
          "properties": {
            "skill": { "type": "string" },
            "entry_point": { "type": "string" },
            "allowed_tools": { "type": "array", "items": { "type": "string" } }
          },
          "required": ["skill", "entry_point"]
        }
      }
    }
  },
  "required": ["commands"],
  "additionalProperties": false
}
```

**`hooks/pre-receive-phigate` (excerpt)**
```bash
#!/bin/bash
# Scan staged files for PHI patterns
python3 scripts/phi_scanner.py --staged
if [ $? -ne 0 ]; then
  echo "ERROR: PHI detected in staged files. Commit aborted."
  echo "See docs/DATA-PROVENANCE.md for synthetic data policy."
  exit 1
fi
```

**`tests/adr_compliance/test_adr_0008.py`**
```python
import subprocess

def test_no_hl7_parsing_in_triage():
    result = subprocess.run(
        ["grep", "-ri", "hl7\\|HL7\\|parse.*message", "plugins/ris-assist/skills/triage/"],
        capture_output=True
    )
    assert result.returncode != 0, (
        "ADR-0008 violation: HL7/message parsing detected in triage skill. "
        "Forensics must be separate (see docs/adr/0008-separate-forensics-plugin.md)."
    )
```

---

## 📈 Overall System Health/Viability Assessment

| Dimension | Current State | Target State | Gap | Risk Level |
|-----------|---------------|--------------|-----|------------|
| **Architecture** | Implicit contracts, undocumented invocation | Explicit interfaces, validated mappings | High | **Critical** |
| **Data Integrity** | Policy-only, no enforcement | Automated gates, runtime validation | High | **Critical** |
| **Governance** | ADRs untested, persona rules duplicated | ADR compliance tests, single source of truth | High | **Critical** |
| **Resilience** | No timeouts, no telemetry | Circuit breakers, gap logging | Medium | **High** |
| **Testing** | Manual only | Automated suite, property-based | High | **High** |
| **Documentation** | Comprehensive but unenforced | Linked, versioned, validated | Medium | **Medium** |

**Overall Health Score: 2/5**

**Justification**: The system has **strong architectural intent** (separation of concerns, explicit non-goals, synthetic data policy) but **critical enforcement mechanisms are missing**. The current state relies on **discipline over guardrails**. Without the P0 fixes (PHI gate, invocation mapping, persona versioning, ADR compliance tests), the project cannot guarantee its own foundational commitments. The system is **maintainable today but brittle tomorrow**—as the skill count grows and more analysts use it, the lack of automation will lead to silent failures and architectural drift.

**Viability**: **Conditional**. The project is viable **if** the P0 and P1 items are addressed. Without them, the risk of PHI leakage, architectural violation, and skill breakage increases non-linearly with usage. The plugin marketplace model (this repo is its own marketplace) amplifies this risk, as updates could silently break installed instances.

---

## 💡 Development Tip

**Start with the PHI gate and invocation mapping—they are the foundation for everything else.** The PHI gate (`hooks/pre-receive-phigate`) is the most critical because it enforces the project's non-negotiable constraint (no real clinical data). Without it, the entire synthetic data policy is a **hope, not a guarantee**. The invocation mapping (`invocation.json`) is the architectural backbone: once explicit, all other validations (ADR compliance, persona versioning, skill testing) can build on top of it.

**Use the existing Python scripts directory as the integration point.** The repo already has `plugins/ris-assist/skills/knowledge/scripts/html_to_docx.py`, so adding `profile_validator.py` and `phi_scanner.py` follows established patterns. This minimizes new dependencies and keeps the toolchain consistent.

**Make gap telemetry user-visible.** The `gap-log.json` should be surfaced to users via `/setup review` so they can see what their site profile is missing. This turns passive logging into active value, encouraging users to complete their profiles and reducing generic fallback behavior over time.

**Prioritize ADR compliance tests over skill tests.** ADR violations are **architectural regressions**—they're harder to fix later and can invalidate the entire design. Skill tests can be added incrementally; ADR tests must be comprehensive from day one.

**Tag all new code with the ADR it satisfies.** For example, `profile_validator.py` should have a header comment: `# ADR-0001: Profile separation enforcement (see docs/adr/0001-separate-profile-from-plugin.md)`. This makes the connection between architecture decisions and implementation explicit and traceable.

---

## GitHub Issues

The findings from this report have been converted to GitHub issues for tracking:

### P0 (Critical)
- [#1](https://github.com/b08x/ris-assist/issues/1) - Implement PHI ingress gate
- [#2](https://github.com/b08x/ris-assist/issues/2) - Define command-to-skill invocation mapping
- [#3](https://github.com/b08x/ris-assist/issues/3) - Add persona versioning
- [#4](https://github.com/b08x/ris-assist/issues/4) - Add ADR compliance tests
- [#5](https://github.com/b08x/ris-assist/issues/5) - Remove duplicated persona rules (G4 violation)

### P1 (High)
- [#6](https://github.com/b08x/ris-assist/issues/6) - Add explicit forensics escalation trigger
- [#7](https://github.com/b08x/ris-assist/issues/7) - Add gap telemetry and MCP timeouts

### Tracking
- [#8](https://github.com/b08x/ris-assist/issues/8) - System Health: 2/5 - Critical enforcement mechanisms missing

---

## Not this skill

This SIFT report analyzes the **system architecture and design** of the ris-assist repository. It does NOT:
- Perform message-level forensics (see separate forensics plugin per ADR-0008)
- Validate clinical data accuracy
- Test runtime behavior of installed plugins
- Analyze user-specific site profiles (which live outside the repo)
- Make patient-safety-adjacent calls (flags for human review only)
