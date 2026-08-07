---
name: knowledge
description: Turns a resolved ticket or worklog into a ServiceNow-importable knowledge base article — triage-first HTML draft, rendered to .docx for upload — detects recurring incidents with no matching article, and flags articles made stale by a change or upgrade. Use when an incident is resolved and worth documenting, when the same question keeps recurring, or when the user says /kb-draft, "write this up", "turn this into a KB article", "is there an article for this".
---

# Knowledge capture

Implements backlog E7. Connected mode (E7.3/E7.4, ServiceNow read/write) is
blocked on DEP-1; manual mode is fully usable now and is the default.

Capture at resolution time, while the context still exists. That is the whole
argument — a quarterly documentation sprint never happens.

The corollary is that the output has to be the thing that gets uploaded. A
markdown draft that someone re-keys into ServiceNow the next morning is a
second task, and the second task is the one that does not happen. So manual
mode ends at a `.docx` the analyst can attach to a KB record, not at a draft
in the chat window.

Persona: `${CLAUDE_PLUGIN_ROOT}/PERSONA-SPEC.md`. Observation/inference separation and
cite-or-decline apply to article bodies same as everywhere else.

## Modes

- **manual** — triage-first HTML draft plus a rendered `.docx`, with an
  outstanding-items list and a separate suggestions block. Works with no
  ServiceNow access at all. This is the default until DEP-1 resolves.
- **connected** — read the resolved incident, draft, and submit with category
  and workflow state. Requires a ServiceNow MCP connection. The article shape
  is identical; only the transport changes.

## Manual mode procedure

1. **Take the worklog as given.** Paste, ticket text, or dictated summary —
   whatever the user provides is the entire source. Do not supplement it
   from general knowledge of how similar issues are usually resolved.
2. **Select the template.** Site profile's article template if one is
   defined; otherwise `references/kb-template.md`, labeled generic per the
   usual convention.
3. **Order the article the way the ticket was worked.** Scope first, then
   the differential branches in the order `skills/triage/SKILL.md` rules
   them out — workstation/user, application (RIS/PACS), interface, advanced.
   Carry only the layers the worklog supports. A layer with nothing behind
   it is omitted and listed as outstanding, never emitted as an empty
   heading and never filled from general knowledge.
4. **Draft section by section**, marking the Cause section's confidence
   explicitly (`confirmed` / `likely` / `possible` — same scale as
   triage/persona spec, applied to root cause rather than to a differential
   branch). A worklog with no cause in it gets "cause not established," not
   a mark on a guess.
5. **Format for the importer.** `references/servicenow-format.md` governs
   heading levels, bold and monospace use, image references, callouts, and
   what silently degrades. Never invent an image `src`.
6. **Run the field checklist** (`references/kb-template.md`) before
   presenting the draft as done. A checklist item that can't be filled is
   marked unknown in the draft, not silently dropped from the checklist.
7. **Write one self-contained file.** The article is a single HTML file
   opening with the Word header from `references/servicenow-format.md` —
   openable in Word on a workstation with no interpreter installed, which is
   the environment this has to work in. It goes where the user says, or the
   working directory if they haven't said; never inside the plugin
   directory.

   Then tell the analyst how to get it into ServiceNow: **Open with → Word →
   Save As `.docx`**, then attach. Do not tell them to paste the HTML into
   the article body — the editor rewrites pasted markup.

   `scripts/html_to_docx.py` renders the `.docx` in one step and is the
   better path on macOS, Linux, and WSL. Offer it only after confirming an
   interpreter exists. It is not the Windows path, and `python3` is not a
   Windows command.

   Report any image left as a placeholder. That is an outstanding item, not
   a rendering detail to discover after upload.
8. **Separate suggestions from the article.** Anything that would improve
   the article but isn't supported by the worklog goes in a clearly
   separate suggestions block underneath — in the response, never in the
   HTML, and therefore never in the `.docx`. Once the file leaves the
   session, generated content merged into the body is indistinguishable
   from recorded content.

## Screenshots

Screenshots make a troubleshooting article usable, and a screenshot of a
production worklist or study list almost certainly contains patient data.
This plugin does not ingest, redact, or de-identify it — see
`docs/DATA-PROVENANCE.md`.

So: use the exact image ID handed over, place it immediately after the step
it illustrates, and say plainly that whether a given screenshot can be
attached is the site's call under its own policy. If the answer is no, keep
drafting with placeholders. Never invent a `src`, and never treat an image
as available because the article would be better with one.

## Gap detection and stale-article flagging (E7.4/E7.5)

Both are blocked on DEP-1 for live operation (need incident/article read
access), but the manual-mode shape is: if the user describes a
recurring-sounding symptom or pastes several similar tickets, say so
explicitly and offer to draft a candidate article rather than silently
noting the pattern and moving on. Stale-article flagging works the same way
in manual mode — if the user mentions a change or upgrade, ask whether any
existing articles reference the old configuration, rather than scanning a
KB the skill has no access to. The metadata line's version and date exist
for exactly this; an article with no version cannot be flagged stale later.

## Environment

The workstation this runs on is MSP-managed Windows: no Python, no `pip`,
and PowerShell as the shell unless Git for Windows is installed. Three
consequences, and none of them are optional:

- **PowerShell syntax first**, bash second. `python3`, `find`, `ls`, and
  `$VAR` expansion are not portable. `python3` in particular is not a
  Windows command — the name resolves to a Store alias stub.
- **Resolve `${CLAUDE_PLUGIN_ROOT}` before it reaches a shell.** It is
  substituted for the model, not by PowerShell; pasted into a PowerShell
  command it stays literal and the command fails. Read the path, then use
  the absolute path in the command.
- **The default output must work with nothing installed.** That is why the
  article is Word-openable HTML rather than a script's output.

**Do not search the filesystem for the site profile.** It lives at a path
the user confirmed during `/setup`, outside the plugin directory. If the
path isn't known in this session, ask for it — the `setup` skill's own rule,
and asking costs one line where a filesystem sweep is slow, noisy, reaches
into places it has no business in, and is POSIX-only besides. No profile and
no answer means draft generically and say so.

## Rules

- Conform to the site's article template from the profile, not to a generic
  KB shape.
- Do not invent reproduction steps that were not in the worklog.
- The ladder is ordered by the triage differential, not by a generic
  troubleshooting script. A step that isn't tied to how this site's topology
  behaves is guessing with confidence.
- Rendering is code's job, interpretation is not. The script maps tags to
  Word styles; it does not decide content. This is the same
  symbolic-before-model commitment the rest of the project runs on.

## References

- `references/kb-template.md` — article shape, layer names, field checklist
- `references/servicenow-format.md` — import mechanics: the Word HTML
  header, the three routes to an uploadable file, what degrades, image and
  PHI handling
- `scripts/html_to_docx.py` — optional one-step HTML → DOCX renderer for
  macOS/Linux/WSL (PEP 723 header; `uv run` resolves `python-docx` and
  `Pillow` without a manual install). Not the Windows path.
- `${CLAUDE_PLUGIN_ROOT}/examples/kb-article-*.example.html` — worked
  articles against the fictional site, including one that degrades to Step 1
  alone because no incident underlies it

## Not this skill

Writing to ServiceNow. Rendering a `.docx` is a local file conversion, not a
state-changing action — the article still gets uploaded by a human, and
connected mode's submit path stays behind DEP-1 and an explicit human
approval either way. See `docs/NON-GOALS.md`.

Deciding whether an article should exist at all, or approving one for
publication. This skill drafts and flags; the knowledge owner decides.
