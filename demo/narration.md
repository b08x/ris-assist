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
Every hospital sends notifications when a system goes down. The order interface
fails, and someone has to tell the radiologists, and the technologists, and the
front desk, and each of those groups needs to hear something different. The
radiologists need to know where to read from. The technologists need to know
which paper process to start. Leadership needs to know how big this is.

SPEAK:
So it isn't one message. It's a grid. Event class down one side, audience across
the top. And most sites have never written most of these down.

---

## Segment 2 — reading the grid
**Screen: slow pan across the grid. Hold on the front desk column.**

SPEAK:
This is one site's actual coverage. The filled cells are notifications they have
a template for. Seven of them. The hatched cells are the ones they don't.

SPEAK:
Look at the front desk column. Nothing. Every unplanned outage, every planned
maintenance window, and the people answering the phone get whatever someone
types in the moment. That's not a criticism of the site. That's what normal
looks like.

---

## Segment 3 — the happy path
**Screen: click Unplanned / Radiologists. Draft appears.**

SPEAK:
Start with one they do have. Unplanned outage, radiologists. Here are the facts
we know: the order interface went down at six fifteen in the morning, we have an
incident number, and we do not have a cause or an estimated time to repair.

SPEAK:
The draft leads with what the radiologist has to do, not with what broke. It
tells them to read direct from the PACS worklist. It gives them the phone
dictation extension. Three sentences, because this site's profile says
radiologists read the first two lines and stop.

SPEAK:
And notice what is missing. There is no estimated time to repair, because nobody
gave it one. It's listed underneath as an unfilled field instead of being
invented. That distinction is the whole product.

---

## Segment 4 — the gap
**Screen: click Unplanned / Front desk. Hold on the substitution banner.**

**Direction: this is the segment to keep if you only keep one.**

SPEAK:
Now the interesting one. Same outage, front desk, and there is no template for
this cell.

SPEAK:
A tool that wanted to look impressive would just write something. This one tells
you first. It says which template it borrowed from, it says the structure is
provisional, and then it gives you the draft anyway so you are not stuck.

SPEAK:
That's the behavior worth arguing about in a support organization. Not whether
the writing is good. Whether you can tell, at a glance, which parts of the output
the tool actually knew and which parts it borrowed. A confident wrong answer
costs you more than no answer at all, and it costs you it later, when someone
has already acted on it.

---

## Segment 5 — your own facts
**Screen: edit the facts box, add a suspected cause, redraft.**

SPEAK:
Change the facts and it changes with them. Add a suspected cause, and the draft
marks it suspected, because that's how you phrased it. Say it's confirmed, and it
says confirmed. It tracks your certainty rather than flattening it.

SPEAK:
And none of the site language here comes from the model. The downtime packet form
number, the yellow requisition slips, the dictation extension — all of that comes
out of a configuration file for this site. Swap the file, and the voice changes
with it. The tool is generic. The output is not.

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
