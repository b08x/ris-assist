# KB article template — ServiceNow-shaped, triage-first

Backlog E7.1. This is the article shape the `knowledge` skill drafts in.
It replaces the KCS-shaped markdown template that shipped through 1.0.0 —
see `docs/adr/0009-servicenow-shaped-kb-output.md` for why, and for what
was kept.

Used when the site profile defines no article template of its own, in which
case output is labelled **generic — not yet tuned to this site**, same
convention as comms' generic templates. If the site profile defines its own
template shape, that governs instead of this.

Two things this shape is doing at once, and both are load-bearing:

- **Importable.** The draft is HTML that converts to a `.docx` ServiceNow
  accepts, so the analyst's output is the artifact that gets uploaded, not a
  markdown draft someone has to re-key at the end of a shift.
- **Triage-first.** The procedure is ordered the way the ticket would have
  been worked — scope first, then the differential branches in the order
  `skills/triage/SKILL.md` rules them out. An article that reads in a
  different order than the work was done is an article nobody follows.

The KCS fields did not go away. Symptom, cause with a confidence mark,
resolution, verification, and related are all still required sections; they
are named and ordered for the reader who is mid-incident rather than for a
knowledge taxonomy.

---

## Structure

```
🛠️ Introduction          — purpose, applies-to, stop conditions
🔎 Step 1                 — confirm symptom and scope  (KCS: symptom)
💻 / 🖥️ / 🔌 Steps 2…n    — checks in differential order  (KCS: resolution)
✅ Verification           — how resolution was confirmed
🧭 Cause                  — with confidence mark
🚀 Escalation             — when to stop and who gets it
📎 Related                — ticket ref, site profile fields, source
```

Steps 2…n carry only the layers the worklog actually supports. A layer with
nothing behind it is **omitted from the article and listed in the
outstanding-items block** — never emitted as an empty heading, and never
filled from general knowledge of how this class of problem is usually fixed.

## The skeleton

```html
<h1>[Symptom-oriented title — what someone would search for at 3 AM,
     not an internal ticket number]</h1>
<p class="metadata">KB[NUMBER] | v[VERSION] | [YYYY-MM-DD]</p>

<h2>🛠️ Introduction</h2>
<p>[One-sentence purpose: what this article gets the reader to.]</p>
<ul>
  <li><strong>Applies to:</strong> [systems, named in site profile
      vocabulary — or <code>[not in site profile]</code>]</li>
  <li><strong>STOP conditions:</strong> [what ends the procedure and sends
      it to a human — patient-safety-adjacent findings, anything
      state-changing the reader is not authorized to do]</li>
</ul>

<h2>🔎 Step 1: Confirm the symptom and scope</h2>
<p>[What was observed, quoted or closely paraphrased from the worklog.]</p>
<ul>
  <li>Scope observed: [one user / one workstation / one modality /
      sitewide]</li>
  <li><strong>Confidence: confirmed</strong> — reported, not inferred.</li>
</ul>

<h2>💻 Step 2: [Layer name]</h2>
<h3>1. [Task name]</h3>
<ul>
  <li>[Action, exactly as the worklog records it]</li>
  <li>[Action naming UI]: press <code>Win + X</code> &gt;
      <strong>Device Manager</strong></li>
</ul>
<img src="IMAGE_ID" alt="[What the screenshot shows]">

<h2>✅ Verification</h2>
<p>[How resolution was confirmed. <code>[not stated]</code> is a valid and
   complete entry.]</p>

<h2>🧭 Cause</h2>
<p>[What the worklog states as the cause.]
   <strong>Confidence: confirmed | likely | possible</strong> —
   [what the mark rests on].</p>

<h2>🚀 Escalation</h2>
<ul>
  <li>[Which tier, named from the site profile's escalation matrix — or
      <code>[not in site profile]</code>]</li>
  <li>[What the person being escalated to needs in hand]</li>
</ul>

<h2>📎 Related</h2>
<ul>
  <li>Ticket reference: [INC…] or <code>[not stated]</code></li>
  <li>Site profile fields cited: [field names]</li>
  <li>Related articles: [titles] or <code>[none known]</code></li>
</ul>
```

## Layer names for steps 2…n

The ladder mirrors the triage differential, in the order that skill rules
branches out (`skills/triage/SKILL.md`). Use only the layers the worklog
supports, in this order:

| Icon | Layer | Covers |
|---|---|---|
| 💻 | Workstation and user | Single machine, single session, viewer client, procedural/filter issues |
| 🖥️ | Application — RIS or PACS | Order status, scheduling rules, worklist configuration, PACS node/listener state |
| 🔌 | Interface and integration | A link between systems: queue depth, service state, delivery failing one direction |
| 🚀 | Advanced and vendor | Anything requiring a component admin, a vendor, or a change window |

Scope (Step 1) comes before all of them because it is the split that
eliminates the most branches at once — the same reason `/triage` asks it
first.

## Confidence marks

Same scale as everywhere else in this plugin
(`${CLAUDE_PLUGIN_ROOT}/PERSONA-SPEC.md`), applied to root cause rather than
to a differential branch:

- `confirmed` — the worklog states it and says it was verified
- `likely` — strong evidence in the worklog, not independently verified
- `possible` — the resolution worked without the cause being isolated

Never omit the mark to make the article read more authoritative than the
worklog supports. If the worklog offers no cause at all, say **cause not
established** and explain why a mark is not being applied — an unmarked
guess sends the next analyst to the wrong owner.

## What never enters the HTML

Two blocks are emitted **in the response, underneath the draft** — never
inside the article file, and therefore never inside the `.docx`:

- **Outstanding items.** Every `[not stated]` / `[not in site profile]`
  token in the draft, plus every ladder layer omitted for lack of source.
  This is the field checklist's result, made visible.
- **Suggestions.** Anything that would improve the article but is not
  supported by the worklog — a missing verification step, a related symptom
  worth cross-referencing, a proactive check that would have caught this.
  Offered, not included (GUARDRAILS G1).

Merging either one into the article body is the specific failure this
separation exists to prevent: it makes generated content indistinguishable
from recorded content the moment the file leaves the session.

## Field checklist

Before presenting a draft as complete, confirm each of these is either
filled or explicitly marked unknown — never silently blank:

- [ ] Title is symptom-oriented (what someone would search for), not an
      internal ticket number
- [ ] Metadata line present; unknown KB number is `KB[TBD]`, not omitted
- [ ] Applies-to names systems in site profile vocabulary, or marks the gap
- [ ] STOP conditions stated, including anything patient-safety-adjacent
- [ ] Scope recorded in Step 1
- [ ] Every step in the ladder traces to the worklog, not to general
      knowledge of "how this is usually fixed"
- [ ] Omitted ladder layers appear in outstanding items
- [ ] Cause carries a confidence mark, or states that cause is not
      established
- [ ] Verification stated or marked `[not stated]`
- [ ] Escalation tier cited from the site profile, or marked as absent
- [ ] Every image reference uses a provided ID; no invented `src` values
- [ ] Suggestions block is outside the article body
