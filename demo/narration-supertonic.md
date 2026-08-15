# Narrating the demo with Supertonic 3

The fully local path. Nothing leaves the machine, nothing is metered, and the
whole pipeline is a text file plus a script you can read in one sitting.

Companion files: `narration-supertonic.txt` (source), `build_narration.py`
(renderer).

---

## Setup

```bash
pip install supertonic soundfile numpy
python build_narration.py narration-supertonic.txt --voice M1 --out build/
```

Model assets download from Hugging Face on first run. After that the machine
can be offline — the README demonstrates it running on a Raspberry Pi and on an
e-reader in airplane mode.

Preset voices are named `M1`–`M5` and `F1`–`F5`. Audition a few; there's no
substitute for hearing them read your actual sentences. If you want your own
voice, Voice Builder produces a version-specific JSON profile you pass with
`--voice-json` — the open-weight repo itself is fixed-voice and ships no cloning
pipeline.

---

## What's different from the hosted approach

| | Supertonic 3 | ElevenCreative Studio |
|---|---|---|
| Where it runs | Your machine, offline after first fetch | Cloud |
| Cost per re-render | Nothing | Credits, past two free regens |
| Delivery control | Speed, quality steps, 10 expression tags | Audio tags, Actor Mode, voice settings |
| Pauses | Assembled in the build script | Timeline or break tags |
| Pronunciation | What you write is what it reads | Pronunciation dictionaries |
| Output | 44.1 kHz 16-bit WAV natively | 128 kbps up to 44.1 kHz by plan |
| Revision unit | A chunk in a text file | A paragraph in a web editor |

The trade is expressive range for control and iteration cost. For a technical
credibility piece — which this is — that trade is favorable. You want a steady,
unremarkable read, and you want to re-cut it fifteen times without thinking
about credits.

---

## Three things the script does deliberately

**Numerals stay as numerals.** `6:15 AM`, `extension 4412` — written normally,
not spelled out. Supertonic's README benchmarks text normalization specifically
against currency with decimal magnitudes, phone numbers with extensions, and
decimal technical units, cases where several hosted systems mishandle the read
without preprocessing. Spelling things out here is a workaround imported from a
different engine, and it makes the source harder to maintain.

**Acronyms are spaced.** `P A C S`, not `PACS`. There's no pronunciation
dictionary layer, so the text *is* the control surface. This is the one place
the Supertonic source diverges from the Studio source, which handles the same
problem with alias entries.

**Pauses are directives, not markup.** `@pause 0.9` inserts real silence during
assembly. Supertonic has no break tag; trying to punctuate your way to a
1.2-second beat is how you get an unnatural read. The long pause after "that's
how you prevent the next analyst from repeating the wrong diagnosis" is the most
important timing in the piece — it's silence, precisely measured, and it costs
nothing to adjust.

---

## Tuning

| Parameter | Default here | Notes |
|---|---|---|
| `--steps` | 10 | Quality range is 5–12, default 8. Narration benefits from 10; 12 is diminishing returns for the render time. |
| `--speed` | 0.97 | Range 0.7–2.0. Slightly under 1.0 reads as considered rather than slow. |
| `--lang` | `en` | Pass `na` for language-agnostic handling if you localize the script. |

Expression tags exist — ten of them, inline, angle-bracketed, including
`<breath>` and `<sigh>`. For this material use none, or at most a `<breath>`
before the closing data-provenance line. Check the model card for the full
tag list rather than guessing at names; an unrecognized tag reads as literal
text, which is a memorable way to ruin a take.

---

## The iteration loop

This is where local synthesis earns its place. Edit a chunk, re-run, listen. The
script writes `chunk_NNN.wav` per synthesis unit plus a per-section WAV plus
`full.wav`, and `manifest.json` carries exact offsets and durations for every
chunk — which is what you feed a caption generator or a timeline import.

Because synthesis is free and deterministic-ish, the useful workflow is the
opposite of the hosted one: don't re-roll hoping for a better take, *edit the
sentence*. If a line reads badly, the sentence is usually the problem. That
constraint tends to improve the script.

---

## Licensing, and a note on the archive

The sample code is MIT. **The model weights are OpenRAIL-M**, which is not an
OSI-approved open source license — it permits broad use but attaches use
restrictions. If generated audio is going in front of a client or into anything
commercial, read those restrictions rather than assuming MIT covers the whole
stack. This distinction is worth stating plainly in your own repo, since
"open source TTS" is doing a lot of eliding in most write-ups.

On archiving: the repository is active as of this writing, with the code under
MIT and the weights on Hugging Face. If you want durable local access
independent of what happens upstream, clone both the repo and the model assets
now and keep them —

```bash
git clone https://github.com/supertone-inc/supertonic.git
git lfs install
git clone https://huggingface.co/Supertone/supertonic-3 assets
```

— and record the commit hashes in your ADRs. That's a reasonable precaution for
any dependency you'd be stuck without, not a prediction about this one.

---

## Where this fits the project

There's a real symmetry worth naming. The plugin's argument is that a support
tool should run on configuration you can read, in an artifact you can inspect,
without sending clinical context to a service you don't control. Narrating the
demo of that argument with a 99M-parameter model running locally on your own
machine is not a gimmick — it's the same claim, applied to the toolchain that
makes the claim.

Worth one line in the demo's README.
