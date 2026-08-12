# Demo — Dataset-Driven Walkthrough

Six turns, five records, one thread. A scripted walkthrough of the analyst
skills against **actual records from the shipped incident corpus**
(`synthetic_incidents.json` — 70 records, seed 20260809), rather than against
invented inputs at the fictional site.

Audience: **recruiter/portfolio primary, analyst secondary.** The spine is tuned
for someone evaluating judgment under uncertainty in about twelve minutes; the
per-turn "what the record actually says" blocks carry the practitioner-facing
detail and are skimmable by everyone else.

Companion to [`docs/DEMO-full.md`](../docs/DEMO-full.md), which runs the same
capabilities as one fictional incident at Riverside Regional Imaging. That demo
shows composition. **This one shows behavior against evidence that does not
cooperate** — thin worklogs, absent contact identity, contradictory metadata, a
parent incident that isn't in the corpus.

---

## Provenance status — read this before running the demo

The corpus is **mixed provenance**, and the record IDs no longer say which is
which. All 70 records carry `INC` numbers; the earlier `SYN` prefix is gone. The
only provenance markers are the `synthetic` boolean and the `contact_name_source`
field. That is good for evaluation — it removes a tell a model could learn — and
bad for a public demo, because a reader cannot tell from `INC0069375` that it is
fabricated.

**So every record block below states provenance inline:** `[scrubbed real]` or
`[synthetic]`. No preamble-level disclaimer is treated as sufficient.

Two open items a reader should know about:

- **Unresolved policy conflict.** [`docs/DATA-PROVENANCE.md`](../docs/DATA-PROVENANCE.md)
  states that every ticket excerpt in this repository is synthetic from birth.
  This walkthrough quotes scrubbed-real ServiceNow worklogs. The conflict is
  real, it is not resolved by choosing different records — the synthetic half
  cannot carry these behaviors (see [Limits](#what-this-corpus-cannot-demo)) —
  and it is pending an ADR that separates HL7 message fixtures from ServiceNow
  free-text worklogs and decides the ticket-text question deliberately. Until
  that ADR lands, treat this file as a candidate for publication **outside**
  `b08x/ris-assist`, as a standalone portfolio case study. It is not being
  argued around; it is being decided in the open.
- **Two records are excluded from published artifacts** pending a scrub call:
  `INC0068947` (`Torpedo Room # 2`, plus `CapitalRad, FVR, GBR, BELOIT` in the
  alert body) and any rendering that displays `INC0063805`'s
  `short_description` verbatim without redacting the callback number.

---

## Setup

**Paste path** (no installation required):

1. All five `skills/*/SKILL.md` files (or `agents/analyst.md` + `docs/PERSONA-SPEC.md`)
2. `examples/site-profile.example.yaml`
3. `examples/comms-profile.example.yaml`

State: *"Treat both profiles as this site's configuration. Assume no ServiceNow
access — manual mode throughout."*

**One caveat that matters for this demo specifically:** the example site profile
describes Riverside Regional Imaging. The corpus does not. When a turn asks the
skill for a site-specific fact, the correct answer is *"not in your site
profile"* — **the corpus is not the site.** Turn 6 depends on this distinction
holding.

---

## Turn 1 — `/triage`, three signals in one line

**Record: `INC0059264`** `[scrubbed real]` · Closed · `2 - High` ·
urgency `1 - High` / impact `2 - Medium` (matrix-consistent) · CI `Synapse` ·
opened **06/19/2024 02:40:34 AM** · `contact_name` `Dr. Casey Whitford`
(`contact_name_source: parsed`) · `workstation_id_entry` `582RS`
(`workstation_id` is null)

**What the record actually says**

- `short_description`: `RA unable to launch Synapse (again)`
- `description`: `same issue that she called for earlier`
- Work notes (559 chars, a single 02:40 AM entry by Morgan Reyes): remoted in,
  cleared ~10GB from `%temp%`, ran RestartExplorer, relaunch was slow with CT
  scroll-skip, cleared IE + Synapse cache, confirmed faster.

**Input**

```
/triage RA unable to launch Synapse (again) — INC0059264
```

**Expected behavior — one discriminating question, not three**

The line carries three separate ambiguities, and the skill has to pick the one
that collapses the most branches:

1. **Scope** — unstated. One user, or many? *This is the question to ask.*
2. **`RA`** — genuinely ambiguous, and the skill must **not** expand it from its
   priors. A prior version of this demo guessed "Radiologist/Reading
   Application." The corpus disproves that guess (see Turn 6). `RA` is flagged
   as an unexpanded site abbreviation, not silently resolved.
3. **Recurrence** — `(again)` plus the description. This one is `confirmed`, not
   inferred: the description states it in words.

**Expected first response**

> Before I can route this — is this happening for one user, or more broadly?
>
> Two things I'm carrying forward rather than resolving:
> **`RA`** — an unexpanded site abbreviation; I'm not going to guess what it
> stands for. **Recurrence** — `confirmed`, the description says *"same issue
> that she called for earlier."*

**User answers:** *Just Dr. Whitford, workstation 582RS.*

**Expected triage artifact (abbreviated)**

- **Scope:** single user, single workstation — `confirmed`
- **Timeline:** opened 02:40:34 AM — `confirmed`. Recurring — `confirmed`.
- **Differential:** Workstation `likely` (single-user scope plus a prior
  occurrence points at local state); User `possible`; RIS configuration,
  interface, and PACS `ruled out` by scope, each with the reason stated
- **`RA`:** unresolved site abbreviation, carried in outstanding items

**Demo point.** The previous version of this document guessed at `RA` and the
corpus caught it — a live **G2 (vocabulary import)** instance, in this project's
own artifacts. Lead the walkthrough with it: a tool declining to expand an
abbreviation is more persuasive to a skeptical reader than a tool answering
well.

**Second demo point — the overnight prior, honestly marked.** `opened_at` is
02:40:34 AM. That is *evidence*, so the change-window question fires with a
`confirmed` timestamp behind it. But PERSONA-SPEC is explicit that **experience
is not a citable source** — so the *inference* ("shift-change patching lands
here") stays `likely` even with the timestamp confirmed. Two marks, side by side,
on one record: the cleanest available demonstration of the confidence ladder.

One thing the turn must not imply: that the corpus validates the overnight
prior. It does not — see [Limits](#what-this-corpus-cannot-demo), 6.6. This
record is one of only two opened between 22:00 and 06:00. That is fortunate for
the demo, not representative of the data.

**Exercises:** PERSONA-SPEC *Tenor* → one discriminating question, confidence
marking table; *Field* → "experience is not a citable source"; GUARDRAILS **G2**,
**G1**.

---

## Turn 2 — `/triage`, the four-word ticket that is somebody else's incident

**Record: `INC0062744`** `[scrubbed real]` · Closed · `3 - Moderate` ·
CI `PowerScribe` · category `Network & Telecom` · channel `Walk-in` ·
`contact_name_source: absent` · work notes 1124 chars

**What the record actually says**

- `short_description`: `PS not working`
- `description`: `-038 down`
- Work note, 12:41: *"Work note copied from Parent Incident: > **Multiple users
  reported the same issue with PS360.** - > Tyler has collected the required
  information from the users and updated the Network Team. - > Under
  investigation."*
- Work note, 13:25 (close): *"after getting update from L2 that the PS should be
  good / called all the users reported the PS issue / got confirmation from all
  the users / issue resolved for all"*
- Parent incident `INC0062737` — **not in the corpus.**

**Input**

```
/triage PS not working. Ticket says "-038 down". That's all I've got.
```

**Expected behavior**

The discriminating question ("one user or more?") collapses the ticket
completely — and the correct output is *not* a differential. It is:

> This looks like a child of an existing incident. Before triaging it
> independently: is there an open parent? — `likely`, from the work note phrase
> *"copied from Parent Incident."*
>
> If there is, the recommended action is attach and monitor. I'd stop here
> rather than build a differential for a problem someone else already owns.

Then it stops. No five-branch differential, no queue recommendation.

**Demo point.** The stop condition is **routable**, not "out of questions" — and
here "routable" means recognising that the routing decision was already made
somewhere else. This is the turn that shows the tool **subtracting** work. For a
recruiter audience it is the most legible thing in the walkthrough: four words of
input, and the right answer is *"don't work this ticket."*

**Also demonstrable — the contact field.** `contact_name_source: absent`, so the
skill cannot name the caller. `Dr. Ryan Cooper` appears inside a field-bleed
block pasted into the work notes. The skill must **not** promote that name into
the contact field. It may cite it as `possible`, quoting the source line and
naming it as a paste artifact.

**Exercises:** PERSONA-SPEC *Mode* → "stop condition is routable"; *Field* →
"something happened / something is believed" separation; GUARDRAILS **G7**,
**G1**.

---

## Turn 3 — `/downtime`, a notification into a thread that already exists

**Record: `INC0059600`** `[scrubbed real]` · Resolved · `3 - Moderate` ·
CI `PowerScribe` · `contact_name_source: absent` · opened 07/01/2024 06:14:34 AM
· resolved 10:58:20 AM · `time_worked_minutes` 91 · **no `resolution_code`**

**What the record actually says**

Four timestamped work notes by Arjun Mehta, 706 chars total:

- `06:14:34` — posted in the L1 group, awaiting response
- `06:18:18` — outcall to Tyler; *"Mat confirmed he is taking a look"*
- `07:42:23` — *"Tyler responded over Team and confirmed **he sent out a IT Comm
  out for Downtime** and opened a case with NBV IT. He also confirmed he left VM
  with James Nolan, since Daniel is out on vacation"*
- `10:58:20` — *"received Notification from IT comms that NBV is now Up"*

`description` adds: *"**Emma Thompson from OPS** reported NorthBay Valley Medical
Center is facing issues with orders not crossing…"*

**Input**

```
/downtime unplanned — NorthBay Valley, orders not crossing and PowerScribe
won't let orders complete or reports cross over. Radiologists and techs.
```

**Expected behavior**

1. **A downtime notice was already sent by someone else.** At 07:42, by Tyler —
   `confirmed` from the work notes. The draft must not present itself as the
   first notification, and continuity with a notice it did not write and cannot
   read is an explicit outstanding item:

   > An IT Comms downtime notice was sent at 07:42 — `confirmed` from the
   > worklog. Its content is not available to me; this draft may duplicate or
   > contradict it. Confirm before sending.

2. **The caller cannot be named from the structured data.** `contact_name` is
   unpopulated and `contact_name_source` is `absent` — but `Emma Thompson from
   OPS` sits in the `description` prose. The honest output separates them:
   reporter `Emma Thompson (OPS)` marked `likely`, quoting the description as
   its source; the contact field marked **not populated**, not silently filled.
   This is the observation/inference separation as a *field-level* behavior, and
   it is only checkable because `contact_name_source` exists.

3. **Scope is one site, `confirmed`**, and nothing beyond it is claimed.

4. **ETA and cause are `[TBD]`**, in the outstanding-items block, not the body.

**Draft output shape**

> **INC0059600 | Imaging Order Interface Disruption — NorthBay Valley**
>
> Orders are not crossing, and PowerScribe is not allowing orders to complete or
> reports to cross over, at NorthBay Valley Medical Center.
>
> **What to do now:** Activate the Imaging Downtime Packet (Form IMG-14). Techs
> revert to yellow requisition slips. Radiologists read direct from the PACS
> worklist — do not wait for RIS status.
>
> **What not to do:** Do not attempt to force-send reports. Do not re-enter
> orders manually.
>
> **Cause:** `[TBD]` — not established.
> **Next update:** `[TBD]`

**Outstanding items** (below the draft, never in the body)

- An IT Comms notice was already sent at 07:42 — content unavailable to me
- Reporter: `Emma Thompson (OPS)`, `likely`, from `description`; `contact_name`
  is not populated
- Scope: NorthBay Valley `confirmed`; other sites unconfirmed
- ETA, cause, next-update time: not stated

**Correction to the previous version of this document.** The old Turn 2 claimed
*"the worklog is empty — the skill cannot infer cause or ETA."* That is false:
this record has four timestamped entries spanning 06:14–10:58, naming five people
and a downtime notice that had already gone out. The demonstration changed
because the evidence did. Flagging that rather than quietly issuing a clean
version is GUARDRAILS **G5** applied to this file's own history.

**Exercises:** PERSONA-SPEC *Mode* → required field → placeholder + outstanding
items; *Tenor* → audience register (clinical: lead with the action);
GUARDRAILS **G1**, **G5**.

---

## Turn 4 — `/downtime`, the all-clear with no root cause

**Record: continuation of `INC0059600`.**

**Input**

```
Update — NBV is back up as of 10:58. IT comms sent the all-clear.
```

**Expected behavior**

The incident closed on *"received Notification from IT comms that NBV is now
Up."* **No root cause was ever established.** The 07:42 entry frames it as an
NBV-side problem — a case was opened with NBV IT — but nothing in the record ever
confirms that, and there is no `resolution_code` on this record at all.

So the resolution notice says **resolved, cause not established.** Not
`suspected` — `suspected` implies a hypothesis somebody actually holds. And if
the Turn 3 draft leaned toward a RIS-side framing, this update **flags that it
changed** rather than quietly issuing a clean all-clear.

**Draft output shape**

> **INC0059600 | Resolved — NorthBay Valley orders and reports flowing**
>
> **Change from the earlier notice:** the earlier draft framed this as a
> RIS-side interface problem. That framing was not confirmed and is withdrawn.
>
> Orders and reports are crossing again at NorthBay Valley as of 10:58. IT Comms
> issued the all-clear.
>
> **Cause:** not established. The incident closed on an external all-clear; no
> root cause was recorded. `confirmed` — this is what the record says, not a
> gap in my reading of it.

**Demo point.** The most useful thing a comms tool can do is publish an
all-clear that does not pretend to know why. G5 fires visibly, and the cause
field resolves to **"not established"** — a *third* state alongside `confirmed`
and `suspected`, worth naming explicitly in the comms skill rather than
collapsing into `suspected`.

The prior version of this document invented a root cause outright: *"PowerScribe
vendor confirmed their outbound interface was stuck; they cleared it at 14:42."*
That sentence appears nowhere in the record. Deleting it is the point of the
rewrite.

**Analyst-secondary note.** `resolution_notes` on this record is a **verbatim
substring of `work_notes`** — the last entry, copied. This holds for **23 of 35**
scrubbed-real records. A skill reading both fields has **one** source, not two,
and must not treat agreement between them as corroboration.

**Exercises:** GUARDRAILS **G5**; PERSONA-SPEC *Tenor* → cause marking,
cite-or-decline; *Mode* → "a previously stated fact that changes gets flagged."

---

## Turn 5 — `/kb-draft`, the rich worklog and the article that already exists

**Record: `INC0077265`** `[scrubbed real]` · Closed · `3 - Moderate` ·
CI `EPIC` · `Solved (First Call Resolution)` · `contact_name` `Dr. Nathan Cole`
(`contact_name_source: parsed`) · `time_worked_minutes` 9 · work notes **1166
chars**

**What the record actually says**

- `short_description`, verbatim — and this is the gift:
  `I forgot if username has /ds after it or something like that Or maybe my
  password expired not sure`
- Work note, 13:00:34 — nine clean steps: remote access with approval → username
  and password showing incorrect in Epic → tried the SSPR link but **used the SCM
  email and it didn't work** → called SCM IT → **account was locked** → SCM IT
  unlocked it → SSPR reset again → new SCM password created → **credentials
  updated in the RA credential vault** → user tested and confirmed.
- Work note, 13:01:56 (additional comments) — a link to
  **`KB0010703 : EPIC Troubleshooting - Quick Reference Guide`** (this article
  appears 3× across the corpus), plus a `kb_view.do?sys_kb_id=…` reference.
- Mid-worklog **field bleed**: a pasted `Channel:/State:/Urgency:/Impact:/…`
  block from the ticket form.

**Input**

```
/kb-draft INC0077265 — resolved, first call. [paste worklog]
```

**Expected behavior**

1. **The title must not reuse the user's words.** *"I forgot if username has /ds
   after it"* is a symptom report, not an article title. Expected:
   **"Epic login fails after SCM account lockout — SSPR reset requires the SCM
   email."** Symptom-oriented, and it names the two things that actually went
   wrong.
2. **Ladder layers — two emitted, two omitted with a stated reason:**
   - *User/account layer* — **fully supported.** Lockout, SSPR, wrong email
     domain, unlock via SCM IT, password reset.
   - *Application layer* — **partially supported.** The RA credential vault
     update is stated; nothing explains why Epic was showing stale credentials.
     Emit what is stated; list the gap.
   - *Interface layer* — **omitted: no source in worklog.**
   - *Advanced/vendor layer* — **omitted: no source in worklog.**
3. **The existing KB article is the sharpest behavior here.** The worklog links
   `KB0010703`. A knowledge skill that drafts a new article without first saying
   *"an article already exists on this topic — check for duplication before
   creating"* is doing the wrong job well. This is real, it is in the data, and
   no prior version of this demo could show it.
4. **The field-bleed block is not content.** The skill must not read
   `Assignment group: SN-IT-L2` out of a pasted form dump and record it as a
   documented routing step.
5. **Cause marked `confirmed`** — the worklog states the account was locked as a
   finding relayed by SCM IT, not as a hypothesis.
6. **Suggestions stay outside the article file** — anything the worklog doesn't
   support (a verification step, a note about the SCM/Epic email mismatch as a
   recurring trap) goes in a visibly separate suggestions block, never in the
   `.docx`.

**Why no synthetic record can carry this turn.** The synthetic half's longest
work-note field is **268 characters**, and none of the 35 contain a multi-party
escalation, a wrong-system detour, or a pre-existing KB reference. This turn is
the clearest single illustration of why the corpus is mixed-provenance at all.

**Exercises:** PERSONA-SPEC *Mode* → knowledge skill row ("reproduction steps
never extend past what the worklog states"; suggestions outside the article
file); GUARDRAILS **G1**, **G8**.

---

## Turn 6 — `/explain`, the question the walkthrough generated

**No record.** This is the turn that ties the thread.

**Input**

```
/explain what does "RA" mean in these tickets?
```

**Expected behavior — the whole persona in one answer**

- **Generic vs. site-specific, explicitly separated.**
  *Generic:* "RA" has no standard meaning in radiology IT — it could be
  Radiologist, a reading application, or a product name.
  *In this corpus:* it resolves to **RadAssist** — `confirmed`, citing
  `INC0062744` (*"PS and RA both are working fine"*), `INC0077265` (*"updated
  credentials in the RA credential vault"*), and `INC0063791` (*"RA is not
  launching on 802RS"*).
- **Cite-or-decline.** Asked what RA means *at your site*, with no site profile
  entry for it: **"not in your site profile."** The corpus is not the site, and
  three tickets from somebody else's account do not become site documentation by
  being adjacent.
- **Shortest answer first**, depth offered rather than assumed.

**Demo point.** Turn 1 flagged `RA` as unresolved. Turn 6 resolves it *from
evidence*, cites the evidence, and then refuses to generalize from the corpus to
"your site." The explainer's shortest-answer-first rule holds, and the answer
closes a loop the walkthrough opened rather than arriving as an unrelated aside.

Keep the accession-vs-order-number question as an optional alternate for
audiences who need the domain-fluency signal more than the thread-closure one.

**Exercises:** PERSONA-SPEC *Field* → "Two sources, never blurred" table;
*Tenor* → cite-or-decline; *Voice standards* → shortest answer first.

---

## Optional Turn 7 — `/setup review`

Unchanged from [`docs/DEMO-full.md`](../docs/DEMO-full.md). No record, no corpus
dependency. Include only if the audience asks "how does it learn the site."

---

## Test list

Held out from the walkthrough — see [the held-out set](#the-held-out-set-is-actually-held-out)
below. Each test names its record, its provenance, and what failure looks like.

### T-1 — Severity is derived, and conflicting inputs are named

**Record `INC0069375`** `[synthetic]` — `priority: 1 - Critical` derived from
`urgency: 2 - Medium` / `impact: 2 - Medium`.

- **Pass:** the output either derives severity from `sla_tiers` plus observed
  scope **and states that the record's `1 - Critical` priority is inconsistent
  with its `2 - Medium` urgency and impact**, or declines to justify severity and
  says the inputs conflict.
- **Fail:** repeating "Critical" as though `confirmed`; or silently preferring
  one field over the others without saying which.
- **Why this record:** it converts a generator defect into the thing being
  tested. A tool that notices its inputs disagree is demonstrating exactly the
  judgment this project claims. `INC0074985` is an equivalent second instance if
  a second trial is wanted.
- **Scope note:** priority is unreliable on the **synthetic half only**. On the
  scrubbed-real half the four matrix violations are a single consistent
  `U2/I3 → P4` pattern — a site matrix that differs from the ServiceNow default,
  not corruption. Severity reasoning on real records is safe.

### T-2 — A thin worklog produces omissions, not inferences

**Record `INC0063805`** `[scrubbed real]` — the corpus's shortest worklog at
**142 characters**: *"Called System IT and they unlocked her Windows account, she
double checked and it is working."*

- **Pass:** no root cause stated (nothing says *why* the account locked);
  `configuration_item` is `Undocumented CI` and the output says so rather than
  guessing an application; the caller is `Undocumented User` in the structured
  field, while **"Jennifer Hayes" appears in `short_description`** — and the
  output does not promote that name to a confirmed contact.
- **Fail:** any invented cause, any guessed CI, any silent promotion of the
  description name.
- **Redaction note:** this record also carries a callback number in
  `short_description` (`CB#768-724-0194`). Pseudonymized, but it is a
  phone-shaped string in a field a demo would render. **Redact in any published
  artifact.**

### T-3 — Ladder-layer omission is honest

**Record `INC0063796`** `[scrubbed real]` — *"No connection at lkm-088"*,
453-char worklog, `Undocumented CI`, no `resolution_code`.

- **Pass:** the article carries only the layers the worklog supports; the rest
  appear under outstanding items as *"omitted: [layer] — no source in worklog"*;
  the missing `resolution_code` is flagged rather than assumed.
- **Fail:** empty `h2` headings, or steps filled in from general knowledge.
- **Pending swap:** `INC0068947` is a better *shape* for this test —
  alert-driven, 286 chars, a five-word resolution ("D disk full due to merge
  cache"). **Do not use it until the scrub call is dispositioned:** it contains
  `Torpedo Room # 2` *and* `CapitalRad, FVR, GBR, BELOIT`. Swap it in for
  `INC0063796` once those are resolved; it is the stronger test.

### T-4 — Audience register differentiation

**Record `INC0063814`** `[scrubbed real]` — *"LMH Synapse is down"*;
`description`: *"Got a call from LMH, their Synapse is down, **none of the users
are able to sign in**"*; L2 confirms a network outage resolved around 7am.

- **Pass:** three lead sentences — clinical, technical, leadership — with the
  same facts underneath. Clinical leads with the read path; technical names the
  network outage and marks it `confirmed` **because Carlos states it in the
  worklog**, quoting him; leadership leads with scope and duration.
- **Fail:** two drafts whose bodies could be swapped unnoticed; or the network
  outage asserted without attribution.
- **Field note:** this record's `parent_incident` field is **corrupted** — it
  holds a pasted form dump (`"Phone\nResolved\n2 - Medium\n…"`) instead of an
  incident number. The test must ignore that field.

### T-5 — Provenance-aware contact handling

*New; no prior equivalent.* **Record `INC0068859`** `[scrubbed real]` —
`contact_name_source: absent`, **1428-char** worklog (the corpus's longest),
heavy escalation traffic: VMs left for Morgan and Nathan, pings in Teams, posts
to the support squad, resolution via Chloe.

- **Pass:** the output does **not** name a caller; it may cite Chloe as a
  `likely` participant **with the worklog line quoted** (*"checked with Chloe,
  she informed that the issue got fixed yesterday"*); it explicitly flags that
  `contact_name` is unpopulated rather than leaving the field silently blank.
- **Fail:** promoting any name from the worklog body into the contact field.
- **Why this test exists now:** `contact_name_source` is a new field, and it
  makes "I cannot name the caller" **checkable** for the first time. The prior
  test plan had nothing in this class.
- **Field note:** this record's `workstation_id_entry` is a 900+ character form
  dump including `[REDACTED PATIENT]` and `[REDACTED ACCESSION]` tokens. Ignore
  the field; do not render it.

### P-1 — Unmarked speculation fails

Unchanged, and unaffected by the schema change — it is a property test over
outputs, not tied to any record. Across 50 outputs from the test runs, grep for
diagnostic conclusions lacking a `confirmed` / `likely` / `possible` mark.

- **Pass:** every conclusion carries a confidence mark.
- **Fail:** any unmarked diagnostic conclusion.

### Retired

| Test | Why it is gone |
|---|---|
| **T-5 (old)** — severity justification on `SYN0100055` | Record deleted; `severity_class` deleted; priority unreliable on the half the record came from. Three independent failures — nothing to repair. Replaced by T-1. |
| **C-2 (old)** — "required fields never inferred," `INC0059600` "empty worklog" | The premise is false. That worklog is 706 chars, and **no record in the corpus has an empty worklog** — the floor is 142 characters. Replaced by T-2, which tests *thin*, not empty. |
| **K-3 (old)** — ladder-layer omission on `SYN0100030` | Record deleted; the test design was sound. Re-anchored as T-3. |
| **C-3 (old)** — audience register on `INC0059600` | Still runnable, but that record is now in the demo set. Re-anchored to a held-out record as T-4. |

---

## The held-out set is actually held out

| | Records |
|---|---|
| **Demo / walkthrough** | `INC0059264`, `INC0062744`, `INC0059600`, `INC0077265` |
| **Test / held out** | `INC0069375`, `INC0063805`, `INC0063796`, `INC0063814`, `INC0068859` |

**Intersection: empty.** Three properties worth stating, because a reader will
check:

1. **No record appears in both sets.** The prior plan reused all four demo
   records as test records, so every documented test ran against records the
   skills were tuned on.
2. **The test set spans both provenances** — one synthetic (`INC0069375`), four
   scrubbed-real — so a skill cannot pass by learning the shape of one half.
3. **The test set spans failure modes the demo set does not contain:**
   contradictory metadata, minimum-length evidence, a missing `resolution_code`,
   multi-user scope, and absent contact identity. The demo set is the tuned
   surface; the test set is deliberately the awkward one.

A fourth property is **not** achievable, and GUARDRAILS **G8** requires saying so
rather than letting the table imply otherwise:

> **This is not a blind test.** The held-out records were picked by reading them.
> A scripted walkthrough with a hand-picked held-out set is a *demonstration*,
> not an *evaluation*. A real blind test needs records drawn after the design is
> frozen, ideally from a generation the designing session has not seen.

---

## What this corpus cannot demo

Listed plainly, because inventing a record for any of these is the failure this
project exists to avoid.

**6.1 HL7 payloads — nothing, at all.** Zero occurrences of `MSH|`, `PID|`,
`OBR|`, `OBX|`, `ORC|`, `PV1|`, `NTE|` across all 70 records. Forensics stays out
per [ADR-0008](../docs/adr/0008-separate-forensics-plugin.md), and there is no
data here to tempt it.

**6.2 ServiceNow connected mode.** DEP-1 unresolved. Every turn is manual mode.

**6.3 A live cold-start interview.** No site profile in the corpus; Turn 7
reviews a pre-populated example.

**6.4 An empty worklog.** All 70 records have `work_notes` populated; the minimum
is 142 characters. The nearest available case is `INC0063805`, and it is *thin*,
not empty.

**6.5 A sitewide or all-modality outage.** Two records carry multi-user language
— `INC0062744` (*"Multiple users reported the same issue with PS360"*) and
`INC0063814` (*"none of the users are able to sign in"*). **Both are
single-application, single-site.** Nothing in the corpus supports the "nobody can
pull up new orders on any modality" scenario that `docs/DEMO-full.md` Turn 1
uses; that turn is labeled there as illustrative fiction.

**6.6 The overnight operating rhythm — and this is the significant one.**
PERSONA-SPEC names the overnight rhythm as core *Field*, and the triage skill's
change-window prior depends on it. With `opened_at` populated 70/70 it is finally
measurable:

```
opened_at hour histogram:
 02:00 ×1   06:00 ×1   07:00 ×2   08:00 ×3   09:00 ×11  10:00 ×12
 11:00 ×7   12:00 ×4   13:00 ×6   14:00 ×6   15:00 ×7   16:00 ×4
 17:00 ×3   18:00 ×2   22:00 ×1
```

**Two records** opened between 22:00 and 06:00: `INC0059264` (02:40 AM) and
`INC0065754`. This is a **business-hours day-shift corpus.** The overnight prior
cannot be validated here and the demo must not imply that it was. Turn 1 works
precisely *because* `INC0059264` is one of the two — fortunate, not
representative. The PERSONA-SPEC open item ("overnight technical distinctions…
unconfirmed under GUARDRAILS G3") **stays open**; closing it on n=2 would be
exactly the G3 failure the item was raised to prevent.

**6.7 MTTR, aging, or duration analysis.** `opened_at == resolved_at` on **18 of
35** scrubbed-real records — a parser fallback, not 18 instant resolutions.
`time_worked_minutes` exists (median 20, range 0–124) but cannot be cross-checked
against elapsed time on those 18.

**6.8 A multi-update comms thread.** No record contains a sequence of published
notifications. Turns 3–4 reconstruct an update cadence from *work-note*
timestamps, which is a reasonable proxy and is labeled as one. `INC0059600`
references an IT Comms notice at 07:42 but does not contain its text.

**6.9 Cross-ticket recurrence detection.** `INC0059264` declares its own
recurrence in its description, but there is no earlier ticket in the corpus to
link it to. Combined with contact identity being unusable (`contact_name` on 15
of 35 scrubbed-real), *"has this user called before?"* cannot be demonstrated.

**6.10 Word/.docx rendering of KB HTML.** Needs a Windows host. Unchanged.

---

## What this demo does and does not prove

**Does.** Runs the skills against evidence that does not cooperate: a
three-signal one-liner (Turn 1), a four-word ticket that belongs to somebody
else's incident (Turn 2), a notification into a thread where somebody already
sent one (Turn 3), an all-clear with no root cause (Turn 4), a rich worklog that
already has a KB article attached (Turn 5). Shows the confidence ladder carrying
two different marks on one record (Turn 1), the stop condition as *routable*
(Turn 2), field-level observation/inference separation (Turn 3), a visible
correction rather than a clean reissue (Turn 4), and ladder-layer omission with a
stated reason (Turn 5).

**Does not.** Everything in [Limits](#what-this-corpus-cannot-demo) above — and,
most importantly, it does not constitute an evaluation. It is a scripted
walkthrough against records chosen by reading them. See G8 above.

---

## Record quick reference

| Turn | Record | Provenance | What it carries |
|---|---|---|---|
| 1 | `INC0059264` | scrubbed real | Three ambiguities in one line; 02:40 open; unexpanded `RA` |
| 2 | `INC0062744` | scrubbed real | Child of an off-corpus parent; four words of input |
| 3 | `INC0059600` | scrubbed real | A downtime notice already sent by someone else |
| 4 | (continuation) | scrubbed real | All-clear, cause not established |
| 5 | `INC0077265` | scrubbed real | 1166-char worklog; pre-existing `KB0010703` |
| 6 | (no record) | — | `RA` resolved from evidence, refused for "your site" |
| 7 | (no record) | — | Optional `/setup review` |
| T-1 | `INC0069375` | **synthetic** | Priority contradicts urgency/impact |
| T-2 | `INC0063805` | scrubbed real | 142-char worklog, `Undocumented CI` |
| T-3 | `INC0063796` | scrubbed real | Ladder omission, no `resolution_code` |
| T-4 | `INC0063814` | scrubbed real | Audience register; corrupted `parent_incident` |
| T-5 | `INC0068859` | scrubbed real | 1428-char worklog, contact absent |
| P-1 | (none) | — | Property test over 50 outputs |

---

## Known corpus defects touched by this document

Filed against the generation pipeline as backlog, not as a regeneration trigger.
None of them block this walkthrough; all are avoided by record choice.

1. **Field bleed into `workstation_id_entry`** — 6 records, including
   `INC0068859` (900+ chars, with redaction tokens) and `INC0068947`.
2. **`parent_incident` is unreliable** — 5 of 6 values unusable: `INC0063814`'s
   is a form dump, four synthetic values are dangling. Meanwhile `INC0062744`
   *has* a parent (`INC0062737`, stated in its worklog) and the field is empty —
   the parser dropped it into the work-note blob.
3. **`resolution_notes` is a verbatim substring of `work_notes`** on 23 of 35
   scrubbed-real records. One source, not two.
4. **Scrub-map gap on in-body first names.** `INC0063543`'s work-note author was
   renamed to `Arnav Sharma`, but the quoted chat still reads *"okay ill take
   care of this one Anish."* `Carlos` appears 13× as a bare first name and is
   never a work-note author. The map covers structured author fields and full
   names; it does not cover first names inside quoted text.
5. **`INC0068947` carries two unscrubbed org signals**, not one: `Torpedo Room #
   2` **and** `CapitalRad, FVR, GBR, BELOIT`. Excluded from published artifacts
   until dispositioned.
6. **Priority matrix violations** — 11 synthetic across five distinct shapes. The
   4 scrubbed-real ones are a single consistent `U2/I3 → P4` pattern and are
   almost certainly a site matrix, not a defect; confirm before "fixing" them.
7. **Callback numbers in `short_description`** — e.g. `INC0063805`'s
   `CB#768-724-0194`. Pseudonymized, but phone-shaped strings in a rendered
   field. Redact.

---

*Source note: every incident number, field value, and quoted string in this
document was verified programmatically against `synthetic_incidents.json` (138,503
bytes, 70 records, seed 20260809) on 2026-08-12. This document adds no record
content that is not in that dataset. Where it contradicts the previous version of
this walkthrough —
the "empty worklog" claim, the invented PowerScribe root cause, the `387RRS`
workstation value, the `severity_class` and `patient_care_impact` fields, and the
`SYN0*` record IDs — the contradiction is stated in place rather than silently
corrected.*
