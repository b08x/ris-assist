# Narration script — dataset-driven demo

Written to be spoken, not read. Lines under `SPEAK:` contain no markdown, no
symbols, no bracketed asides — feed them straight to a TTS engine. Everything
else is direction and never gets voiced.

Total spoken length: roughly five minutes at a measured pace. Seven segments,
each independently usable if you want shorter cuts.

Source data: every turn uses an actual record from the 100-record synthetic
RIS incident dataset. The incident numbers, workstations, descriptions, and
work notes are real shapes — names and identifiers have been replaced.

---

## Pronunciation key

Set these before generating, or the output will mangle them.

| Written | Speak as |
|---|---|
| RIS | "R I S" — three letters |
| PACS | "packs" — one syllable |
| HL7 | "H L seven" |
| EHR | "E H R" |
| INC0059264 | "incident zero zero five nine two six four" |
| INC0059600 | "incident zero zero five nine six zero zero" |
| SYN0100030 | "incident S Y N zero one zero zero zero three zero" |
| SYN0100055 | "incident S Y N zero one zero zero zero five five" |
| IMG-14 | "I M G fourteen" |
| ETA | "E T A" |
| AD | "A D" |
| ADFS | "A D F S" |

Numbers like 387RRS should be spoken "three eight seven R R S." If your
engine reads it as a number, spell it in the source line.

---

## Segment 1 — the dataset

**Screen: dataset overview — 100 records, slice view.**

SPEAK:
Here's a hundred incidents from a synthetic radiology support operation.
A hundred tickets with real shapes — vague descriptions, empty worklogs,
recurring issues, shift-change failures. Names, identifiers, and clinical
details have been replaced through a deterministic scrub map.

SPEAK:
We're going to run five skills against this data. Troubleshoot, downtime
communications, knowledge capture, domain explanation, and overnight
framing. Each one uses an actual dataset record as input.

---

## Segment 2 — troubleshoot, the vague ticket

**Screen: dataset record INC0059264 appears. "RA unable to launch Synapse (again)."**

SPEAK:
Incident zero zero five nine two six four. Short description: "R A unable
to launch Synapse, again." Sev two. Single workstation. No scope stated in
the description.

SPEAK:
The troubleshoot skill's first move is scope. One user or many? The answer
collapses four of five branches. Single user — it's workstation or user,
not interface, not R A S, not PACS.

SPEAK:
But notice the parenthetical. "Again." That's a recurrence signal. The
skill should surface it: prior occurrence suggests a local state problem
rather than a systemic failure.

---

## Segment 3 — downtime, empty worklog

**Screen: dataset record INC0059600. "Blanchard Valley Medical Center is facing issues
with orders not crossing and Powersribe is not allowing there order to
complete or reports to cross to over."**

SPEAK:
Incident zero zero five nine six zero zero. The description is a sentence
fragment with two typos and no incident number. The worklog is empty. The
severity is medium. Patient care impact: direct.

SPEAK:
The comms skill resolves the variant key, picks the template, and fills
required slots from stated facts only. Stated facts: orders are not
crossing at Blanchard Valley. That's it.

SPEAK:
Everything the template requires that the user didn't provide gets a
bracket TBD. No invented ETA. No guessed cause. No inferred scope. This
is the core contract.

---

## Segment 4 — the interval update

**Screen: continuation of INC0059600. New input: "Update — Blanchard Valley orders
are flowing again. Reports still queued."**

SPEAK:
Same incident, twenty minutes later. Orders restored. Reports still
queued. The vendor says the outbound interface was stuck.

SPEAK:
The skill carries forward the incident number, the original start time,
and the scope. It leads with the delta: orders back, reports still
queued. And it marks the cause suspected — the vendor says it was stuck,
but no root cause is confirmed.

SPEAK:
And notice the correction. The initial assumption was R A S-side. The
actual fix was in the PowerScribe outbound interface. The skill makes that
correction visible, not buried. That's not a nice to have. That's how you
prevent the next analyst from repeating the wrong diagnosis.

---

## Segment 5 — knowledge capture

**Screen: dataset record SYN0100030. Work notes show a three-day resolution
ending with "Identified orphaned Synapse process. Killed via Task Manager."**

SPEAK:
Incident S Y N zero one zero zero zero three zero. PowerScribe not
sending transcribed reports to Synapse. The worklog spans three days.
Remoted in. Awaited callback. Closed after user verification. Time
worked: forty-four minutes.

SPEAK:
The knowledge capture skill reads the worklog and builds the article
around what it actually supports. The worklog documents a workstation
layer fix — orphaned process, cache cleared, relaunched. That's one
ladder rung.

SPEAK:
The application layer, the interface layer, the advanced layer — nothing
in the worklog supports those. The skill lists them as outstanding, not
filled. It doesn't invent reproduction steps from general knowledge. That
separation is the whole product.

---

## Segment 6 — the domain question

**Screen: mid-incident, analyst asks "what's the difference between accession
number and order number?"**

SPEAK:
The analyst is mid-incident and asks a domain question. The explain skill
answers in one or two sentences and offers to go deeper. Shortest answer
first, always.

SPEAK:
"The order number identifies the request. The accession number identifies
the imaging exam R A S and PACS actually performs. They're usually
assigned by different systems, at different lifecycle stages, and are not
interchangeable." That's it. The practical consequence follows in one
more sentence.

SPEAK:
Even mid-incident, the skill doesn't dump the full reference. It answers
the question asked and offers to go deeper. That restraint is the
contract.

---

## Segment 7 — overnight framing, the close

**Screen: dataset record SYN0100055. "EPIC logon slow at shift change — AD token
validation failing." Critical severity.**

SPEAK:
Incident S Y N zero one zero zero zero five five. EPIC logon slow at
shift change. A D token validation failing. Multiple users. Single site.
Critical severity.

SPEAK:
The analyst is on alone overnight. The skill's first move isn't the
differential — it's the change window question. Shift-change timing is
when scheduled restarts and patching typically land. Knowing whether there
was a window helps narrow this fast.

SPEAK:
The severity justification cites the site profile's S L A tiers
definition verbatim. Not invented language. The real definition, applied
to the real facts. That's the contract all five skills share.

SPEAK:
All data in this demo is synthetic. Incident numbers, workstations,
and work notes have been replaced. No production data is used.

---

## Direction notes

Pace it slower than feels natural. This is a demo for people evaluating
whether to trust a tool, and confidence in the delivery reads as sales
pressure.

Do not add music under segments four or five. Let the correction and the
ladder-layer omission sit in silence for a beat before the next line.

If you cut for time, drop segments one and six. The argument survives on
two, three, four, five, and seven.

The last two sentences of segment seven are not optional. In a
managed-services environment the first question anyone asks is where the
data came from, and answering it before it's asked is worth more than
anything else in the script.
