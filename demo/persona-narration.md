# Narration script — the persona module

Companion visual: `persona-card.html`. Companion to `narration.md` (the
dataset-driven demo) — same production conventions, different subject. Where the
coverage demo argues the *tool* is trustworthy, this one argues the *persona*
is — the thing every skill talks through.

Written to be spoken, not read. Lines under `SPEAK:` contain no markdown, no
symbols, no bracketed asides — feed them straight to a TTS engine. Everything
else is direction and never gets voiced.

Total spoken length: roughly two and a half minutes at a measured pace. Five
segments, one per screen on `persona-card.html`.

---

## Pronunciation key

Same base key as `narration.md`, plus two new terms this script introduces.

| Written | Speak as |
|---|---|
| RIS | "R I S" — three letters |
| PACS | "packs" — one syllable |
| EHR | "E H R" |
| SLA | "S L A" |
| KB | "K B" |
| IMG-14 | "I M G fourteen" |
| INC0004821 | "incident zero zero zero four eight two one" |
| FTM | "F T M" |

---

## Segment 1 — the persona, named
**Screen: `#s1-identity`, masthead only.**

SPEAK:
Every skill in this plugin talks through the same voice. Fifteen years in radiology IT.
Exhausted. Allergic to corporate filler.

SPEAK:
It isn't a writing style. It's a survival mechanism. This is what those rules
look like when you aren't drowning in tickets.

---

## Segment 2 — field, tenor, mode
**Screen: `#s2-field`, the three-card row.**

SPEAK:
The persona asks three things before it talks. What does it actually know.
Who is it talking to. And how is the answer organized.

SPEAK:
What it knows is strictly bounded. Interfaces. Order lifecycles. It doesn't do
clinical decision-making. It doesn't parse raw H L seven. It doesn't push
changes to production. Because it knows better.

SPEAK:
How it relates is simple: it hands you a draft. It doesn't make the call for you.
And it tags every conclusion with exactly how sure it is.

---

## Segment 3 — confidence marking
**Screen: `#s3-confidence`, the three chips.**

**Direction: slow down here. This is the mechanic everything else depends on.**

SPEAK:
Three tags. 'Confirmed' means it's written in a log you can actually point to.
'Likely' means all the evidence points there, but nobody wants to say it out loud.
'Possible' means it matches the shape of the fire.

SPEAK:
An unmarked claim isn't a stylistic choice. It's a defect. A hallucination.
Other tools might call it an 'inference.' I call it a defect because I'm the
one who gets paged when it's wrong.

---

## Segment 4 — one incident, three registers
**Screen: `#s4-register`. Click through Clinical, Technical, Leadership.**

SPEAK:
The facts don't change. An interface died at two fourteen in the morning.
What changes is who you're talking to.

SPEAK:
The clinical version gives them the workaround and shuts up after three
sentences, because they aren't reading the fourth.

SPEAK:
The technical version names the interface and marks the cause suspected,
because you haven't proven it yet.

SPEAK:
The leadership version gives scope and duration, so they can decide who
else needs to be woken up.

SPEAK:
Same fire. Different buckets of water.

---

## Segment 5 — the close
**Screen: `#s5-close`, footer.**

SPEAK:
This isn't a watered-down demo persona. These are the actual rules running
underneath every skill in the plugin.

SPEAK:
All data in this demo is synthetic. No production data is used.

---

## Direction notes

Pace it the same way as the dataset demo — slower than feels natural. This
is still a credibility piece, not a feature reel.

If you cut for time, drop segment two first — the argument survives on
naming the persona, showing the confidence mechanic, and showing the
register in action. Segment five (the close) is not optional in any cut —
it's where the data-provenance disclosure lives.
