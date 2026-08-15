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
3. Write one self-contained HTML file — Word header included — where the user
   asks, or the working directory if they haven't said. Never inside the
   plugin directory.
4. Hand it off: **Open with → Word → Save As `.docx`**, then attach to the KB
   record. Not a paste into the article body; the editor rewrites markup.
5. Report, under the draft and outside the article file: outstanding items
   (every gap token, every omitted ladder layer, every image left as a
   placeholder), then suggestions.

## Environment

Assume MSP-managed Windows: no Python, PowerShell unless Git for Windows is
present. Step 3 is deliberately interpreter-free for that reason.

Where a shell is used, write PowerShell first:

```powershell
Start-Process winword.exe -ArgumentList '"C:\path\to\article.html"'
```

Resolve `${CLAUDE_PLUGIN_ROOT}` to an absolute path before putting it in a
command — PowerShell does not expand it. The optional Python renderer
(`skills/knowledge/scripts/html_to_docx.py`) is for macOS, Linux, and WSL;
offer it only after confirming an interpreter exists, and never as
`python3`, which is not a Windows command.

Do not search the filesystem for the site profile. Ask for the path if it
isn't known — see the `onboarding` skill.

`Bash` is allowed for the handoff and optional render steps only. Nothing
here executes against a production system — see `docs/NON-GOALS.md`.

If the site profile is missing or the needed field is unpopulated, say so in one
line and offer `/onboarding`. Continue with generic behavior, labelled as untuned.
