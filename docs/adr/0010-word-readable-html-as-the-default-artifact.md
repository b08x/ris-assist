# ADR-0010 — Word-readable HTML is the default artifact; the Python renderer is optional

Status:   Accepted
Date:     2026-08-07

Amends [ADR-0009](0009-servicenow-shaped-kb-output.md). The decision to ship a
ServiceNow-shaped, triage-first article stands; what changes is how the file
becomes uploadable.

## Context

ADR-0009 put `scripts/html_to_docx.py` on the critical path: draft HTML, run
the script, attach the `.docx`. That was written and tested on Linux. The
plugin runs on MSP-managed Windows workstations, where three of its
assumptions fail at once.

**No interpreter.** No Python, no `pip`, no `uv`, and no route to installing
any of them on a locked-down clinical workstation.

**Wrong shell.** Claude Code on native Windows uses Git Bash for the Bash tool
only when Git for Windows is installed; otherwise shell commands go through
PowerShell. `python3` is not a Windows command at all — the name resolves to a
Microsoft Store alias stub. And `${CLAUDE_PLUGIN_ROOT}` is substituted for the
model, not by PowerShell: pasted into a PowerShell command it stays literal.

**Observed, not theorised.** A live session was seen running
`find / -iname "*.json" -path "*site*"` to locate the site profile — a
POSIX-only command, sweeping the whole filesystem, for a path the `setup`
skill already requires be confirmed with the user. The portability problem and
a behavioural defect surfaced in the same trace.

The obvious escape — skip the file, paste the HTML into the article body — was
checked and rejected on evidence. ServiceNow's knowledge editor is TinyMCE,
which rewrites pasted markup. That rewriting is why the Word-import route
exists in the source skill; removing the file would have reintroduced the
problem the format was chosen to avoid.

## Decision

The article is written as **one self-contained HTML file carrying the Word
namespace declarations and a stylesheet that maps the format's elements onto
Word's sizes**. The analyst opens it in Word and saves as `.docx`. No
interpreter, no shell, no dependency.

`scripts/html_to_docx.py` is retained and demoted: a one-step convenience on
macOS, Linux, and WSL, offered only after confirming an interpreter exists.
A PowerShell + Word COM snippet is documented as a middle route for sites
where scripting is not blocked.

Shell examples throughout the skill and command are written PowerShell-first.
`${CLAUDE_PLUGIN_ROOT}` is resolved to an absolute path before it reaches a
shell. The knowledge skill gains an explicit rule against searching the
filesystem for the site profile.

`references/servicenow-format.md` becomes the single style spec, implemented
twice — once as the CSS in the Word header, once as the style assignments in
the script. Both carry the same numbers; changing one requires changing the
other.

## Alternatives considered

**Interpreter-resolution ladder — try `uv`, `py -3`, `python`, `python3`.**
Rejected as the primary path. A ladder is the right answer when an interpreter
exists somewhere and the question is which name reaches it. Here there is
nothing to reach. It also fails silently in the worst way: at 04:00, four
failed invocations then an unexplained stop.

**Require Git for Windows so the Bash tool is available.** Rejected. It makes
the plugin's core output depend on a developer tool being installed on a
clinical workstation, which is a request to a change-approval board, not a
prerequisite line in a README. It also would not have supplied Python.

**Drop `.docx` and paste HTML into the article body.** Rejected on evidence —
TinyMCE rewrites the markup. This was the preferred option before it was
checked, and is the reason it was checked.

**Emit RTF instead**, which Word opens natively and which is plain text the
model can write directly. Rejected as a second output format to maintain for a
problem the Word HTML header already solves, and one whose fidelity is harder
to reason about than HTML's.

**Ship a `.doc`-extensioned copy so a double-click opens Word.** Rejected as
the default: on many Office configurations it triggers the "file format and
extension don't match" prompt. Documented as an option the analyst can be
offered, not something done silently — a security prompt nobody expected is
how a tool loses trust in one step.

## Consequences

**Easier:** the default path has no dependencies at all, so it degrades to
"open this file" on any machine. The repository stops shipping code on the
critical path, which restores most of the "verify by reading prose" property
ADR-0009 gave up.

**Harder:** style rules now exist in two implementations — the Word header CSS
and the script's style assignments — and they can drift. Mitigated by naming
`servicenow-format.md` the spec both implement, but it is a real maintenance
cost accepted deliberately over dropping either path.

**Unconfirmed, flagged under G6:** LibreOffice's HTML filter flattens
`<ul>`/`<ol>` to plain paragraphs. Word's HTML import could not be tested in
the environment this was built in, so whether bullets survive as real list
formatting on the target workstations is not known. First real use answers it.
If Word flattens them too, the fix is `mso-list` hints in the header — in the
spec, not worked around inside individual articles. Tracked in
`docs/PROJECT-INSTRUCTIONS.md` open items.

**Behavioural fix carried with it:** the knowledge skill now states that the
site profile is asked for, never searched for. The `setup` skill already
required the path be confirmed with the user; knowledge simply never said what
to do when it wasn't known, and filled the gap with a filesystem sweep. A rule
that exists in one skill and is assumed in another is not enforced.
