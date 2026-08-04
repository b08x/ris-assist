---
name: knowledge
description: Turns a resolved ticket or worklog into a knowledge base article draft in the site's template, detects recurring incidents with no matching article, and flags articles made stale by a change or upgrade. Use when an incident is resolved and worth documenting, when the same question keeps recurring, or when the user says /kb-draft, "write this up", "is there an article for this".
---

# Knowledge capture

STUB — implements backlog E7.

Capture at resolution time, while the context still exists. That is the whole
argument — a quarterly documentation sprint never happens.

## Modes

- **manual** — paste-ready draft with a field checklist. Works with no
  ServiceNow access at all. This is the default until DEP-1 resolves.
- **connected** — read the resolved incident, draft, and submit with category
  and workflow state. Requires a ServiceNow MCP connection.

## Rules

- Conform to the site's article template from the profile, not to a generic
  KB shape.
- Separate observation from inference in the body, same as everywhere else.
- Do not invent reproduction steps that were not in the worklog.
