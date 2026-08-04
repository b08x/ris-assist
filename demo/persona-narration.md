# Narration script — the persona module

Companion visual: `persona-card.html`. Companion to `narration.md` (the
coverage demo) — same production conventions, different subject. Where the
coverage demo argues the *tool* is trustworthy, this one argues the
*persona* is — the thing every skill talks through.

Written to be spoken, not read. Lines under `SPEAK:` contain no markdown, no
symbols, no bracketed asides — feed them straight to a TTS engine. Everything
else is direction and never gets voiced.

Total spoken length: roughly three minutes at a measured pace. Six segments,
one per screen on `persona-card.html`.

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
Every skill in this plugin — clarifying a ticket, drafting a notification,
writing up a resolution — talks through the same voice. Fifteen years in
radiology IT. Calm. Allergic to filler.

SPEAK:
That voice isn't a writing style. It's a set of rules, and this is what they
look like on their own, without a ticket attached to them.

---

## Segment 2 — field, tenor, mode
**Screen: `#s2-field`, the three-card row.**

SPEAK:
The persona is built on three questions, asked of every response. What does
it know. How does it relate to the person reading it. How is what it says
organized.

SPEAK:
What it knows is bounded on purpose. Order lifecycle, interfaces, S L A
vocabulary, incident communications, K B capture. Not clinical
decision-making. Not message-level H L seven parsing — that's a separate
tool. Not anything that changes a production system.

SPEAK:
How it relates is the part that matters most. It hands off a draft. It does
not decide for you. And every conclusion it reaches carries a mark for how
sure it actually is.

---

## Segment 3 — confidence marking
**Screen: `#s3-confidence`, the three chips.**

**Direction: slow down here. This is the mechanic everything else depends on.**

SPEAK:
Three marks. Confirmed means it's stated somewhere — a ticket, a worklog, a
source you can point to. Likely means the evidence points that way, but
nobody said it outright, and the persona will tell you what would confirm
it. Possible means it fits the shape of the problem, and nothing more than
that.

SPEAK:
An unmarked claim is not a stylistic miss. It's a defect. That's a stronger
word than most tools would use about their own output, and it's used on
purpose.

---

## Segment 4 — the boundary that got tested
**Screen: `#s4-boundary`.**

**Direction: this is the segment to keep if you only keep one.**

SPEAK:
Here's a real example, not a hypothetical. An early draft of this project
hardcoded a specific notification audience as a default. Nobody had
confirmed that any real site actually organizes it that way.

SPEAK:
The persona's own rule is cite the source, or say none exists. Shipping an
unconfirmed default would have quietly broken the rule it exists to
enforce.

SPEAK:
So it stopped being a default. The audience list now comes from an
interview, every time, for every site. That's what this rule costs when
it's actually followed, and it's a small enough cost that there's no
excuse not to pay it.

---

## Segment 5 — one incident, three registers
**Screen: `#s5-register`. Click through Clinical, Technical, Leadership.**

SPEAK:
Same underlying facts, every time. An interface went down at two fourteen
in the morning. What changes is who's reading.

SPEAK:
The clinical version leads with what to do right now, and stops after three
sentences, because that's what this audience actually reads.

SPEAK:
The technical version leads with what broke, names the interface, and
marks the cause suspected, because it hasn't been confirmed yet.

SPEAK:
The leadership version leads with scope and duration, because that's the
information that decides whether this gets escalated further.

SPEAK:
Nothing about the incident changed across those three. Only the shape of
what's told first.

---

## Segment 6 — the close
**Screen: `#s6-close`, footer.**

SPEAK:
This isn't a simplified version of the persona for a demo. The rules on
this screen are the same rules every skill in the plugin actually runs on.

SPEAK:
The site and the incident in this walkthrough are invented, the same as
everywhere else in this project. Nothing here comes from a real hospital,
and no patient data touches any part of it.

---

## Direction notes

Pace it the same way as the coverage demo — slower than feels natural. This
is still a credibility piece, not a feature reel.

Hold segment four in silence for a beat after "so it stopped being a
default" before continuing. That's the sentence that proves the rule is
enforced, not just stated.

If you cut for time, keep segments one, three, and four. Two, five, and six
are the ones to drop first — the argument survives on naming the persona,
showing the confidence mechanic, and showing it once being tested for real.
