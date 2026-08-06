---
name: knowledge
description: Turns a resolved ticket or worklog into a knowledge base article draft in the site's template, detects recurring incidents with no matching article, and flags articles made stale by a change or upgrade. Use when an incident is resolved and worth documenting, when the same question keeps recurring, or when the user says /kb-draft, "write this up", "is there an article for this".
---

# Knowledge capture

Implements backlog E7. Connected mode (E7.3/E7.4, ServiceNow read/write) is
blocked on DEP-1; manual mode is fully usable now and is the default.

Capture at resolution time, while the context still exists. That is the whole
argument — a quarterly documentation sprint never happens.

Persona: `${CLAUDE_PLUGIN_ROOT}/PERSONA-SPEC.md`. Observation/inference separation and
cite-or-decline apply to article bodies same as everywhere else.

## Modes

- **manual** — paste-ready draft with a field checklist. Works with no
  ServiceNow access at all. This is the default until DEP-1 resolves.
- **connected** — read the resolved incident, draft, and submit with category
  and workflow state. Requires a ServiceNow MCP connection.

## Manual mode procedure

1. **Take the worklog as given.** Paste, ticket text, or dictated summary —
   whatever the user provides is the entire source. Do not supplement it
   from general knowledge of how similar issues are usually resolved.
2. **Select the template.** Site profile's article template if one is
   defined; otherwise `references/kb-template.md`, labeled generic per the
   usual convention.
3. **Draft section by section**, marking the Cause section's confidence
   explicitly (`confirmed` / `likely` / `possible` — same scale as
   triage/persona spec, applied to root cause rather than to a differential
   branch).
4. **Run the field checklist** (`references/kb-template.md`) before
   presenting the draft as done. A checklist item that can't be filled is
   marked unknown in the draft, not silently dropped from the checklist.
5. **Separate suggestions from the article.** Anything that would improve
   the article but isn't supported by the worklog goes in a clearly
   separate suggestions block underneath — never merged into the draft body.

## Gap detection and stale-article flagging (E7.4/E7.5)

Both are blocked on DEP-1 for live operation (need incident/article read
access), but the manual-mode shape is: if the user describes a
recurring-sounding symptom or pastes several similar tickets, say so
explicitly and offer to draft a candidate article rather than silently
noting the pattern and moving on. Stale-article flagging works the same way
in manual mode — if the user mentions a change or upgrade, ask whether any
existing articles reference the old configuration, rather than scanning a
KB the skill has no access to.

## Rules

- Conform to the site's article template from the profile, not to a generic
  KB shape.
- Do not invent reproduction steps that were not in the worklog.
