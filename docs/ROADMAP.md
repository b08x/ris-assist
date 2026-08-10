# RIS Assist — Roadmap

Two parallel tracks of work that are blocked on external decisions rather than on
engineering capacity: the **ServiceNow & MS 365 connector integration** (some of
which is live today in manual mode, the rest blocked on DEP-1 and DEP-2), and
the **message forensics plugin** (parked entirely per ADR-0008, waiting on
F-DEP-1). Both live here because they share the same shape: external dependency
at the gate, internal work that becomes visible the moment the gate clears.

| Part | Status | What unblocks it |
|------|--------|------------------|
| [Part 1 — ServiceNow & MS 365 connector integration](#part-1--servicenow--ms-365-connector-integration) | Manual mode operational; connected mode blocked | DEP-1 (ServiceNow MCP scope), DEP-2 (Copilot PHI/BAA) |
| [Part 2 — Message forensics long-term backlog](#part-2--message-forensics-long-term-backlog) | Parked, not scheduled | F-DEP-1 (access to message data), F-DEP-2 (site profile stable), F-DEP-3 (local model evaluation) |

---

## Part 1 — ServiceNow & MS 365 connector integration

**Applies to:** RIS Assist plugin (pre-alpha, as of 2026-08-07)
**STOP conditions:** This section describes current capabilities and blocked dependencies. Do not assume connected-mode features exist — verify DEP-1/DEP-2 status before promising functionality.

---

### 🔎 Scope

RIS Assist interacts with two external platforms through different integration stages:

| Platform | Current State | Dependency |
|----------|--------------|------------|
| **ServiceNow** | Manual mode operational; connected mode blocked | DEP-1: ServiceNow MCP scope decision |
| **MS 365 Copilot** | Deferred entirely; no code exists | DEP-2: M365 Copilot PHI/BAA coverage |

This section explains what works today, what's blocked, and how to configure each connector when it becomes available.

---

### 💻 ServiceNow Integration

#### Current capability: Manual-mode KB pipeline

The knowledge skill (`/kb-draft`) produces ServiceNow-importable `.docx` files through a deterministic pipeline:

```
Worklog (pasted text) → Model drafts HTML → Code renders .docx → Human uploads to ServiceNow
```

**What the model does:** Drafts a triage-first KB article in HTML, ordered by the triage differential (scope → workstation/user → application → interface → advanced).

**What code does:** Converts HTML to a `.docx` that survives ServiceNow's Word import. The script (`html_to_docx.py`) maps HTML tags to Word styles — it does not interpret content.

**Why this order matters:** The article reads in the same order the ticket was worked. A KCS-ordered article (problem → environment → resolution → cause) is a taxonomy order; nobody reads that at 3 AM. The triage-first order is what a follow-the-sun analyst actually needs.

#### Three paths to an uploadable file

| Path | Dependencies | Platform | Use when |
|------|-------------|----------|----------|
| **Word-openable HTML** (default) | None | Any | MSP-managed Windows with no interpreter |
| **PowerShell + Word COM** | Word installed, COM not locked down | Windows | Want `.docx` without manual Save As |
| **Python renderer** | `python-docx`, optionally `Pillow` | macOS, Linux, WSL | Better path outside Windows |

**Path 1 — Word-openable HTML (recommended default):**

The article is a self-contained HTML file with Word namespace declarations and a CSS stylesheet. Open in Word (not the browser), then Save As `.docx`.

```powershell
Start-Process winword.exe -ArgumentList '"C:\path\to\article.html"'
```

Or: right-click → **Open with** → **Word**, then **Save As** → **Word Document (\*.docx)**.

> **Critical:** Open in Word, not a browser. Browsers render it fine and copy out of it badly — the copy lands back in TinyMCE's rewriting, which is the exact problem the Word-import route exists to avoid.

**Path 2 — PowerShell COM:**

```powershell
$word = New-Object -ComObject Word.Application
$doc  = $word.Documents.Open("C:\path\to\article.html")
$doc.SaveAs2("C:\path\to\article.docx", 16)   # 16 = wdFormatDocumentDefault
$doc.Close(); $word.Quit()
```

Fails where COM automation is locked down. Fall back to Path 1, not to pasting into TinyMCE.

**Path 3 — Python renderer:**

```bash
# bash / macOS / Linux / WSL
python3 scripts/html_to_docx.py article.html article.docx

# PowerShell (note: py -3, not python3)
py -3 .\scripts\html_to_docx.py .\article.html .\article.docx
```

Dependencies: `python-docx>=1.1`, `Pillow>=10.0` (optional — images use default sizing without Pillow). The script carries a PEP 723 header, so `uv run` resolves deps automatically.

> **Windows gotcha:** `python3` is not a Windows command. The name resolves to a Microsoft Store alias stub that does nothing. Use `py -3` or `python`, and only after confirming an interpreter exists.

#### ServiceNow import format spec

`skills/knowledge/references/servicenow-format.md` is the single authority on what converts and what degrades. Key rules:

| Element | Converts to | Notes |
|---------|------------|-------|
| `<h1>` | Title (24pt bold) | Exactly one per article |
| `<h2>` | Heading 1 (18pt bold) | Major phases |
| `<h3>` | Heading 2 (14pt bold) | Numbered tasks |
| `<strong>` / `<b>` | Bold | UI elements, expected states, confidence marks |
| `<code>` | Courier New 10pt, red | Keyboard shortcuts, paths, commands, gap tokens |
| `<span class="warning">` | Red bold | Stop conditions, patient-safety warnings |
| `<pre>` | Courier New 9pt, shaded block | Log excerpts, multi-line commands |
| `<ul>` / `<ol>` | Lists (2 levels) | `<ol>` for ordered resolution steps |
| `<img src="data:image/...;base64,...">` | Embedded image | Scaled to max 6.5" width |
| `<img src="anything else">` | Grey placeholder | Honest gap, not broken link |
| `<div class="callout warning">` | Pink shaded table cell | Stop conditions |
| `<div class="callout info">` | Blue shaded table cell | Informational |
| `<div class="callout note">` | Grey shaded table cell | Notes |

**What silently degrades:**
- Inline `style` attributes, CSS classes not listed above, anything in `<head>`
- Floating or right-aligned images
- Lists nested 3+ levels
- Fonts other than Arial and Courier New
- Colour beyond black, red warnings, and grey metadata
**Metadata line (required):**

```html
<p class="metadata">KB0010624 | v1.0 | 2026-08-07</p>
```

Unassigned number: `KB[TBD]` — present and visibly unfilled, never omitted. An article with no version cannot be flagged stale later.

#### Heading shift convention

The converter shifts headings down one level because ServiceNow renders the article title separately from the body. HTML `<h2>` becomes DOCX Heading 1. This is by design — the spec and the script implement the same numbers; change one, change both.

#### Image handling

Only base64 data URIs are embedded. Any other `src` — including a bare image ID — becomes a visible `[Image: alt text]` placeholder. This is deliberate: a placeholder is an honest gap; a broken image link is not.

**Screenshots and PHI:** A screenshot of a production worklist almost certainly contains patient data. RIS Assist does not ingest, redact, or de-identify images. When an image is offered, state plainly that screenshot handling is the site's call under its own policy, and keep drafting with placeholders if the answer is no.

#### What not to do

| Anti-pattern | Why it fails | Correct approach |
|-------------|-------------|----------------|
| Paste HTML into ServiceNow article body | TinyMCE rewrites pasted markup | Open HTML in Word, Save As `.docx`, attach |
| Use `python3` on Windows | Resolves to Store alias stub | Use `py -3` or `python` after confirming exists |
| Search filesystem for site profile | POSIX-only, slow, reaches into places it shouldn't | Ask the user for the path |
| Merge suggestions into article body | Generated content indistinguishable from recorded content once file leaves session | Keep suggestions in the response, outside the HTML |
| Rename `.html` to `.docx` | Triggers "file format and extension don't match" prompt on many configs | Offer it, don't do it silently |

#### Connected mode (blocked: DEP-1)

When ServiceNow MCP access is granted with read/write scope, the knowledge skill gains:

| Capability | Backlog | Requires |
|-----------|---------|----------|
| Read resolved incident → auto-draft | E7.3 | ServiceNow MCP read |
| Submit draft with category/workflow state | E7.3 | ServiceNow MCP write |
| KB gap detection (recurring symptoms, no article) | E7.4 | ServiceNow MCP read |
| Known-error matching against live KB | E8.7 | ServiceNow MCP read |
| Stale-article flagging from change events | E7.5 | ServiceNow MCP read |

**Status:** DEP-1 scope decision is pending. Manual mode is fully usable now and is the default. The article shape is identical in both modes — only the transport changes.

#### User stories affected

| Story | Status | Dependency |
|-------|--------|-----------|
| US-06 — Check for known errors first | Blocked | DEP-1 (ServiceNow read) |
| US-12 — Detect KB gaps | Blocked | DEP-1 (ServiceNow read) |
| US-14 — Push to ServiceNow | Blocked | DEP-1 (ServiceNow write) |

---

### 🔌 MS 365 / Copilot Integration

#### Current state: Deferred (PX track)

No MS 365 integration code exists. The entire Copilot parallel track is deferred until DEP-2 (M365 Copilot PHI/BAA coverage confirmation) resolves.

**Why it exists as a concept:** Some workflows genuinely require live patient data (PHI). Claude Desktop is not a BAA-approved platform for PHI. Microsoft 365 Copilot, with a signed BAA, is. The split is by data sensitivity, not by feature preference.

#### What's planned (E12 — Copilot Parallel Track)

| Epic | Description | Size | Status |
|------|------------|------|--------|
| E12.1 | Port capability instructions + reference docs to SharePoint knowledge-source format | M | Not started |
| E12.2 | Copilot Studio agent for live-ticket clarification | L | Not started |
| E12.3 | Power Automate flow: envelope extraction + segment split pre-parse for live messages | L | Not started |
| E12.4 | Decision record: what runs where, by data sensitivity | S | Not started |

#### DEP-2: What needs to resolve

DEP-2 is the M365 Copilot PHI/BAA coverage confirmation. This determines:

1. **Whether the Copilot track proceeds at all** — if PHI posture cannot be confirmed, the track stays deferred
2. **What data sensitivity levels Copilot can handle** — the BAA scope defines what's in-bounds
3. **Whether Power Automate flows can touch live HL7 messages** — envelope extraction on live data requires PHI approval

**Status:** Request submitted (E10.3), determination pending.

#### Architecture: what runs where

When DEP-2 resolves, the split is by data sensitivity:

| Platform | Handles | Does not handle |
|----------|---------|----------------|
| **Claude Desktop (plugin)** | De-identified data, synthetic examples, site profiles, KB drafts from pasted worklogs | Live PHI, raw HL7 with patient data |
| **M365 Copilot** | Live ticket clarification, message forensics on live data, PHI-adjacent workflows | Anything that doesn't require PHI |

The boundary is not "Claude is better at X" — it's "which platform has a signed BAA for this data class."

#### SharePoint knowledge-source format (E12.1)

When E12.1 ships, the same reference docs that power the Claude plugin skills will be mounted as SharePoint knowledge sources. This is a different mount, not a different document — the source markdown is the same, the consumption path changes.

**What this means for users:** The explainer skill's domain knowledge (order lifecycle, accession vs. order number, MWL, report status flow, RIS↔PACS↔EHR topology) becomes available to Copilot users through SharePoint, without duplicating the content.

#### Copilot Studio agent (E12.2)

A Copilot Studio agent for live-ticket clarification. This is the Copilot-track equivalent of the `/triage` skill — same differential logic, same question-selection algorithm, but running on a BAA-approved platform against live ticket data.

**What it does not replace:** The Claude Desktop plugin's triage skill continues to work for de-identified or pasted ticket data. The Copilot agent is not "the better version" — it's "the version that can touch PHI."

#### Power Automate flow (E12.3)

Envelope extraction + segment split pre-parse for live HL7 messages. This is the symbolic parse layer ([FE2](#fe2--symbolic-parse-layer-was-core-e91-e92)) implemented as a Power Automate flow rather than a local script.

**Why Power Automate:** The flow runs in Microsoft's BAA-approved environment, so it can touch live messages. A local script cannot.

**What it does:** Extracts the message envelope, splits segments, maps fields into a structured representation — all in reviewable code, not model interpretation. The structured output then feeds the Copilot agent or the Claude plugin (depending on data sensitivity).

---

### ✅ Verification

Before assuming a connector works:

- [ ] **ServiceNow:** Can you open the generated `.html` in Word and Save As `.docx` without errors?
- [ ] **ServiceNow:** Does the `.docx` survive ServiceNow's Word import without hand-repair?
- [ ] **ServiceNow:** Is DEP-1 resolved? Check `docs/BACKLOG.md` for current status.
- [ ] **MS 365:** Is DEP-2 resolved? Check `docs/BACKLOG.md` for current status.
- [ ] **Python renderer:** Does `uv run scripts/html_to_docx.py --help` work on the target machine?
- [ ] **Images:** Are all images base64 data URIs, not bare IDs?

---

### 🧭 Cause

The split between "works now" (ServiceNow manual mode) and "doesn't exist yet" (MS 365 Copilot) is caused by two independent dependencies:

- **DEP-1** (ServiceNow MCP scope) — technical integration decision, can be granted incrementally
- **DEP-2** (Copilot PHI/BAA) — compliance/legal decision, binary go/no-go

**Confidence: confirmed** — these dependencies are documented in `docs/BACKLOG.md` (lines 22-23), `docs/PROJECT-INSTRUCTIONS.md` (lines 29-30), and tracked as E10.3/E10.4.

---

### 🚀 Escalation

- **ServiceNow scope questions:** Escalate to the client's ServiceNow admin and the MSP's integration lead. The scope decision (read incidents, write KB, or both) determines which backlog items unblock.
- **Copilot BAA questions:** Escalate to the client's compliance/legal team and the MSP's security officer. The BAA scope determines whether the PX track proceeds.
- **IP/OSS approval:** DEP-3 (employer/client IP + OSS publication approval) is separate from the above and gates public repository publication.

---

### 📎 Related

- `docs/BACKLOG.md` — E7 (KB pipeline), E12 (Copilot track), DEP-1/DEP-2 tracking
- `docs/USER_STORIES.md` — US-06, US-12, US-14 (ServiceNow), US-15–US-19 (comms)
- `docs/adr/0009-servicenow-shaped-kb-output.md` — why the article shape changed
- `docs/adr/0010-word-readable-html-as-the-default-artifact.md` — why the default path has zero dependencies
- `plugins/ris-assist/skills/knowledge/references/servicenow-format.md` — the import format spec
- `plugins/ris-assist/skills/knowledge/scripts/html_to_docx.py` — the HTML→DOCX renderer
- `docs/NON-GOALS.md` — execution boundary, PHI handling
- `docs/GUARDRAILS.md` — G6 (fabricated specificity) applies to connector claims

---

# Part 2 — Message forensics long-term backlog

Parked, not scheduled. Split out of the core plugin per
[ADR-0008](adr/0008-separate-forensics-plugin.md).

Nothing here has a phase. This backlog is a record of what the work is and what
it waits on, so the shape of it isn't rediscovered later.

## Blocking dependencies

| | Dependency | Status |
|---|---|---|
| **F-DEP-1** | Access to message data for development and validation | Not requested |
| **F-DEP-2** | Site profile schema stable enough to encode interface topology | Follows core E2 |
| **F-DEP-3** | Local model evaluation, if grammar-constrained generation is pursued | Not started |

F-DEP-1 is the real gate. Everything else can proceed once it clears.

---

## FE1 — Data hygiene (was core E3)

Moved wholesale. These existed to serve forensics and were gating core phase 0
for no reason.

- [ ] FE1.1 (M) — Synthetic HL7 v2 message generator (ORM/ORU/ADT/SIU;
      fictional patients; structurally valid; seedable)
- [ ] FE1.2 (S) — Generate and commit the reference corpus, including
      deliberately malformed messages for negative tests
- [ ] FE1.3 (M) — Deterministic de-identification gate: PID/NK1/IN1/GT1
      scrub/synthesize pass, plus a free-text (OBX/NTE) second pass
- [ ] FE1.4 (S) — Test suite: de-id gate against the synthetic corpus,
      including PHI planted in free text
- [ ] FE1.5 (S) — Data provenance statement specific to this plugin

Note: `docs/DATA-PROVENANCE.md` already states the synthetic-from-birth policy
for the core plugin. When FE1 is built, that document either extends to cover
both or forks — decide then.

## FE2 — Symbolic parse layer (was core E9.1–E9.2)

The whole argument rests on this existing before any model interpretation.

- [ ] FE2.1 (L) — Parser: envelope extraction, segment splitting, field mapping
      into a structured representation. Code, not model.
- [ ] FE2.2 (M) — Reference tables: segment/field definitions for ORM/ORU/ADT/
      SIU; common ACK error codes; Z-segments handled as declare-unknown
- [ ] FE2.3 (S) — Decide build-vs-adopt: an existing HL7 library (hl7apy, HAPI)
      versus a purpose-built parser. Adopting is likely correct; record the
      decision as an ADR either way.

## FE3 — Diagnosis layer (was core E9.3–E9.6)

- [ ] FE3.1 (M) — Diagnosis instructions: reason over parsed structure, apply
      confidence marking, hypothesize fault origin from site topology
- [ ] FE3.2 (M) — Message diff with expected-variance suppression
      (timestamps, control IDs) separated from structural difference
- [ ] FE3.3 (M) — Blast-radius analysis from the topology graph
- [ ] FE3.4 (M) — Replay-safety advisory, with hard human-authorization flag on
      any sequence-sensitive case (ADT merges, cancels)
- [ ] FE3.5 (S) — `/decode` command
- [ ] FE3.6 (M) — Evaluation set: known-fault synthetic messages with expected
      findings, run as regression

## FE4 — Grammar-constrained generation (new, speculative)

Investigated 2026-08-04. Worth recording, not worth committing to.

GBNF constrains *generation*, not parsing — it will not parse inbound messages,
so it has no role in FE2. Two places it could earn its keep:

- [ ] FE4.1 (S) — **Spike first.** Test whether a local model holds up under
      HL7-shaped constrained decoding at all. Heavily delimited output with long
      fields is a regime where constrained sampling sometimes degrades badly.
      An hour with a generic-tier grammar answers it. Everything below is
      contingent on this.
- [ ] FE4.2 (M) — Generic structural grammar: MSH with hardcoded encoding
      characters, segment/field/repetition/component/subcomponent hierarchy,
      escape sequences, `\r` terminator
- [ ] FE4.3 (M) — Message-type overlays constraining segment order and
      cardinality for the two or three types forensics actually reasons about.
      Do not attempt field-by-field coverage of a full ORM — that is weeks of
      work for test fixtures that need representative structure, not exhaustive
      conformance.
- [ ] FE4.4 (M) — Semantic validator for what a context-free grammar cannot
      express: message type agreeing with segments present, order numbers
      matching across ORC/OBR, values drawn from HL7 tables, conditional
      requiredness by trigger event, timestamp ordering
- [ ] FE4.5 (S) — Mutation harness for malformed cases. A strict grammar cannot
      emit invalid messages; generate valid then mutate, keeping a labelled
      expected-failure per case (feeds FE3.6).
- [ ] FE4.6 (S) — Consider GBNF for constraining *forensic output* to a schema
      with mandatory confidence marking — arguably a better use than HL7 itself,
      since it makes the marking structurally unskippable rather than
      instruction-dependent.

Applies only to local model pipelines (llama.cpp and derivatives). The Anthropic
API does not accept GBNF.

The provenance argument is the strongest reason to do this at all: "generated
from a published grammar" is more defensible to a compliance reviewer than
"generated from a script."

## FE5 — Packaging

- [ ] FE5.1 (S) — Second plugin directory and `marketplace.json` entry
- [ ] FE5.2 (S) — README stating the access dependency plainly, and that the
      plugin does not ship until the parse layer exists
- [ ] FE5.3 (S) — Decide whether the de-identification gate stays here or is
      promoted to a shared component (flagged as a future decision in ADR-0008)

---

## What is deliberately not here

SFL-based analysis. The forensic *narrative* — how a finding gets written up —
may benefit from register and modality analysis, but that belongs with the
clarification work in the core plugin. HL7 messages are not natural language;
segment parsing is a formal grammar problem, and applying systemic functional
linguistics to it would be forcing the frame.
