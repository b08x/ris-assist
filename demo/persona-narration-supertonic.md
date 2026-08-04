# Narrating the persona module with Supertonic 3

The fully local path, matching `narration-supertonic.md`'s pipeline exactly
— same renderer, same voice options, same everything except the source
text and the visual it's timed against (`persona-card.html` instead of
`coverage-demo.html`).

Companion files: `persona-narration-supertonic.txt` (source),
`build_narration.py` (renderer — shared, unmodified).

---

## Setup

```bash
pip install supertonic soundfile numpy
python build_narration.py persona-narration-supertonic.txt --voice M1 --out build-persona/
```

Same model assets as the coverage demo — if you already fetched them for
that render, nothing downloads again.

Producing both modules with the same voice (`M1` or whichever you settled
on) keeps them sounding like one project rather than two. Audition once,
reuse the choice.

---

## What's different from the coverage-demo render

Nothing in the mechanics — see `narration-supertonic.md` for the full
comparison against ElevenCreative Studio, which applies unchanged here.
The only differences are content-level:

- **Six sections instead of six**, but shorter — this module runs about
  three minutes spoken versus the coverage demo's four, so the output
  directory (`build-persona/`) will have a smaller `full.wav` and fewer,
  shorter chunks.
- **New acronyms.** `S L A` and `K B` appear here and didn't in the
  coverage demo — spelled as separated letters in the source text, same
  convention as `R I S` and `P A C S`, for the same reason: no
  pronunciation-dictionary layer in this pipeline, so what's written is
  what's read.
- **A number written as words, not digits.** "Two fourteen in the morning"
  is spelled out in the source rather than left as "2:14 AM" — the
  original coverage-demo script leaves times as digits ("6:15 AM") because
  Supertonic normalizes them well in isolation, but "two fourteen" reads
  more naturally spoken than "zero two colon one four" would if the
  normalizer parsed it as a 24-hour timestamp rather than a clock time.
  Test both if the normalizer surprises you; spelling it out is the safe
  fallback used here.

---

## Pairing with the visual

`persona-card.html`'s six `id`-anchored sections (`#s1-identity` through
`#s6-close`) line up 1:1 with this script's six `@section` blocks. If you're
assembling a video rather than a live click-through, cut to each anchor at
the timestamp `build-persona/manifest.json` reports for the matching
section's first chunk.
