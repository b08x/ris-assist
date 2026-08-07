# Architecture Decision Records

Dated records of the decisions that shaped this project, including the
alternatives that were rejected and why. New ADRs are numbered sequentially and
never edited after acceptance — a reversal gets its own record that supersedes
the original.

## Format

Each ADR uses the same short structure:

```
# ADR-000N — Title

Status:   Proposed | Accepted | Superseded by ADR-000M
Date:     YYYY-MM-DD

## Context
What situation forced a decision.

## Decision
What was chosen, stated in one or two sentences.

## Alternatives considered
What else was on the table, and why it lost.

## Consequences
What this makes easy, what it makes hard, what it commits us to.
```

## Index

| # | Decision | Status |
|---|---|---|
| 0001 | Symbolic parse before model interpretation | Accepted |
| 0002 | Site profile lives outside the plugin, written by a cold-start interview | Accepted |
| 0003 | Synthetic-from-birth test data; de-identified production data excluded | Accepted |
| 0004 | Capability split by data sensitivity across platforms | Accepted |
| 0005 | Apache-2.0 license | Accepted |
| 0006 | Confidence marking and cite-or-decline as enforced persona rules | Accepted |
| 0007 | Elicitation stops at routability, not at question exhaustion | Accepted |
| [0008](0008-separate-forensics-plugin.md) | Message forensics split into its own plugin | Accepted |
| [0009](0009-servicenow-shaped-kb-output.md) | ServiceNow-shaped KB output replaces the KCS markdown template | Accepted |

*Backfill in progress (backlog E11.1) — the index lists decisions already made
in design; individual records are being written up.*
