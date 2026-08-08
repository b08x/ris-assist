# Narration script — coverage demo

Written to be spoken, not read. Lines under `SPEAK:` contain no markdown, no
symbols, no bracketed asides — feed them straight to a TTS engine. Everything
else is direction and never gets voiced.

Total spoken length: roughly four minutes at a measured pace. Six segments,
each independently usable if you want shorter cuts.

---

## Pronunciation key

Set these before generating, or the output will mangle them.

| Written | Speak as |
|---|---|
| RIS | "R I S" — three letters |
| PACS | "packs" — one syllable |
| HL7 | "H L seven" |
| EHR | "E H R" |
| INC0084219 | "incident zero zero eight four two one nine" |
| IMG-14 | "I M G fourteen" |
| ETA | "E T A" |
| MSP | "M S P" |

Numbers like 6:15 AM should be spoken "six fifteen in the morning." If your
engine reads it as "six colon fifteen," spell it out in the source line.

---

## Segment 1 — the problem
**Screen: coverage grid, nothing selected yet.**

SPEAK:
An order interface drops at three in the morning. The ER is screaming about a stat head CT. Someone has to tell the radiologists where to read from, the techs which paper downtime process to start, and the oncoming shift what they're walking into. Nobody has a template for any of this.

SPEAK:
So it isn't one message. It's a grid. Event class down one side, audience across
the top. And most sites have never written most of these down.

---

## Segment 2 — reading the grid
**Screen: slow pan across the grid. Hold on the next shift column.**

SPEAK:
Here is the coverage grid. The filled cells are the seven templates someone actually
documented five years ago. The hatched cells are the void.

SPEAK:
Look at the next-shift column. Empty. The incoming analyst gets whatever the outgoing one
managed to type into a handoff note before passing out. That isn't a broken process.
That's just Tuesday.

---

## Segment 3 — the happy path
**Screen: click Unplanned / Radiologists / Techs. Draft appears.**

SPEAK:
Start with one they do have. Unplanned outage, radiologists. Here are the facts
we know: the order interface went down at six fifteen in the morning, we have an
incident number, and we do not have a cause or an estimated time to repair.

SPEAK:
Radiologists don't care that your broker is dropping ACKs. They care that they can't dictate.
The draft gives them the PACS worklist workaround and the downtime phone
extension. Three sentences. Because by sentence four, they're already calling the helpdesk to yell at you.

SPEAK:
Notice the ETA is blank. It doesn't invent one, because guessing an ETA is how you lose your job.

---

## Segment 4 — the gap
**Screen: click Unplanned / Next shift. Hold on the substitution banner.**

**Direction: this is the segment to keep if you only keep one.**

SPEAK:
Now the interesting one. Same outage, next shift, and there is no template for
this cell.

SPEAK:
Here's a gap. No template. An AI that wants to please you will hallucinate a
distribution list and invent a downtime procedure. This one doesn't. It flags
what it borrowed and tells you it's provisional.

SPEAK:
A confident hallucination at 4 AM doesn't just look bad. It creates a patient safety event.

---

## Segment 5 — your own facts
**Screen: edit the facts box, add a suspected cause, redraft.**

SPEAK:
Add a suspected cause, it marks it suspected. Confirm it, it marks it confirmed.
It tracks your certainty instead of flattening it.

SPEAK:
The form numbers, the paper colors, the extensions — those come from your site
profile, not a training corpus. You don't want a generic apology. You want the exact
sequence of numbers that makes the paging system stop beeping.

---

## Segment 6 — the close
**Screen: pull back to the full grid.**

SPEAK:
So the deliverable isn't the drafts. It's the grid. It shows a support lead
exactly which of their notifications are standardized and which are still living
in somebody's head, and it turns that into a list of things to fix.

SPEAK:
The site in this demo is invented. The templates, the form numbers, the phone
extension, the incident number — all fictional. Nothing here came from a real
hospital, and no patient data touches any part of this.

---

## Direction notes

Pace it slower than feels natural. This is a demo for people evaluating whether
to trust a tool, and confidence in the delivery reads as sales pressure.

Do not add music under segment four. Let the substitution banner sit in silence
for a beat before the next line.

If you cut for time, drop segments one and five. The argument survives on two,
three, four, and six.

The last two sentences of segment six are not optional. In a managed-services
environment the first question anyone asks is where the data came from, and
answering it before it's asked is worth more than anything else in the script.
