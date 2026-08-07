---
description: Draft a ServiceNow-importable knowledge base article from a resolved ticket or worklog.
argument-hint: "[incident ref or pasted worklog]"
allowed-tools: Read, Write, Bash
---

Invokes `skills/knowledge/SKILL.md`, manual mode. That file is the authority
on behavior; this command wires the arguments to it and states the flow.

Arguments: $ARGUMENTS

## Flow

1. Treat `$ARGUMENTS` as the entire source. Empty arguments means ask for the
   worklog, not draft from the incident reference alone.
2. Draft the article in the triage-first shape from
   `skills/knowledge/references/kb-template.md`, formatted per
   `skills/knowledge/references/servicenow-format.md`.
3. Write the HTML where the user asks, or the working directory if they
   haven't said. Never inside the plugin directory.
4. Render it:

   ```bash
   python3 ${CLAUDE_PLUGIN_ROOT}/skills/knowledge/scripts/html_to_docx.py <article>.html <article>.docx
   ```

5. Report, under the draft and outside the article file: outstanding items
   (every gap token, every omitted ladder layer, every image the converter
   left as a placeholder), then suggestions.

`Bash` is allowed for the render step only. Nothing here executes against a
production system — see `docs/NON-GOALS.md`.

If the site profile is missing or the needed field is unpopulated, say so in one
line and offer `/setup`. Continue with generic behavior, labelled as untuned.
