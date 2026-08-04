# Building the narration in ElevenCreative Studio

Companion to `narration-script.txt`. Everything here is tuned to how Studio
actually works, not to generic TTS practice.

> Note on naming: Studio is now **ElevenCreative Studio** (3.0). The older
> **Voiceover Studio** was retired in May 2026 — if you land there, you're in
> the wrong tool.

---

## 1. Why the script is shaped the way it is

Studio's atomic unit is the **paragraph**. Generation, regeneration, generation
history, and locking all operate per paragraph — and you get two free
regenerations per paragraph as long as the text and voice don't change.

That single fact drives the whole format:

- **One idea per paragraph.** When a line lands wrong, you re-roll that block
  for free instead of paying to regenerate a whole segment.
- **Short paragraphs beat long ones.** The hard cap is 5,000 characters, which
  you'll never approach — but a 4-sentence paragraph costs 4 sentences to fix,
  and a 1-sentence paragraph costs 1.
- **The punchlines are isolated.** "That distinction is the whole product" and
  the closing data-provenance line each sit alone. Those are the two you'll
  re-roll most, and they're the two that matter most.
- **Six chapters, not one.** Chapters export individually, so you can re-cut
  Chapter 4 without re-rendering the deck.

Create the six chapters manually in the Chapters sidebar and paste each section
in. Studio auto-detects chapters on import only from structured documents
(EPUB with Heading 1 is the reliable path) — for a script this short, manual is
faster than fighting the importer.

---

## 2. Model choice

| | **Eleven v3** | **Multilingual v2** |
|---|---|---|
| Delivery control | Inline audio tags — `[pause]`, `[serious]`, `[slowly]` | Punctuation and voice settings only |
| SSML `<break>` | Not supported | Supported, up to 3s |
| IPA pronunciation | Supported, roughly 80–90% consistent | Not via phoneme tags |
| Fit for this script | Better, if you stay disciplined | Perfectly adequate |

Default for new projects is Multilingual v2; switch in **Project settings**.

**Recommendation: v3, with almost no tags.** This is a credibility piece for
people deciding whether to trust a tool. Emotive tagging will actively hurt it —
a narrator who sounds excited about a hospital outage reads as a sales pitch.
Use at most:

- `[serious]` at the top of Chapter 4, once
- nothing else

If you find yourself adding a third tag, you're directing a performance the
content doesn't want. Resist it — restraint is the point.

**Do not use `<break>` tags for the silences.** Studio's own guidance is that
newer models may reduce or ignore them, and that precise timing belongs on the
timeline. Drag the gap between clips instead. That's where the beat of silence
after the Chapter 4 substitution line should live.

---

## 3. Pronunciation

Use the **Pronunciations Editor** (toolbar) rather than mangling the script
text. Two notation types are available: phoneme tags (IPA/CMU — model-dependent,
compatible with Flash v2 and v3) and **alias tags**, which are plain word
substitutions and work with every model.

For this script, alias tags are the right call — they're model-proof and
readable by anyone who inherits the project.

| Word | Alias |
|---|---|
| RIS | R. I. S. |
| PACS | packs |
| HL7 | H. L. seven |
| EHR | E. H. R. |
| MSP | M. S. P. |

Entries are case-sensitive, so add lowercase variants if the script ever uses
them. Preview each with the Play button in the editor before committing.

Two things are already handled in the script text rather than the dictionary,
because substitution is unreliable for them: **"six fifteen in the morning"**
(written out, not `6:15 AM`) and the incident number, which is spoken rather
than shown. If you change any facts in the demo, keep that convention.

---

## 4. Voice and settings

Pick a voice that sounds like a competent colleague explaining something at a
whiteboard — not a documentary narrator, not a commercial read. Mid-range,
unhurried, minimal vocal fry.

Starting settings:

| Setting | Value | Why |
|---|---|---|
| Stability | **60–65** | Above the common ~50 default. Higher is steadier and less emotionally variable, which is what this material wants. Too high goes monotone — back off if it flattens. |
| Similarity | **75** | The usual sweet spot; leave it. |
| Speed | **0.95** | Slightly under 1.0. The script asks for a measured pace, and this is more reliable than hoping the model reads it slowly. |
| Style exaggeration | **0** | ElevenLabs recommends leaving this at 0 generally, and it destabilizes output. |
| Speaker boost | Off | Adds latency for a subtle difference. |

Use **Override settings** if you want a single paragraph handled differently —
otherwise a change applies across the whole project and invalidates everything
you've already generated.

**Lock paragraphs as you approve them.** Locked paragraphs can't be
accidentally regenerated or have their voice changed, which matters once you're
30 clips in and adjusting a global setting.

---

## 5. If a line won't land

In order of what to try:

1. **Regenerate the paragraph** — free, twice, if text and voice are unchanged.
   Non-determinism means the second roll is often just better.
2. **Regenerate a selection** — select the offending phrase or sentence (a
   complete one; partial phrases produce worse seams) and re-roll only that.
3. **Repunctuate.** A period where you had a comma changes pacing more
   reliably than any tag.
4. **Actor Mode** — record yourself delivering the line and let it guide the
   performance. This is the tool for the Chapter 4 lines, where the pause
   placement and the flatness of "a confident wrong answer costs you more than
   no answer at all" carry the argument. Note that it replicates your accent
   along with everything else.

---

## 6. Assembly and export

- **Timeline for silence.** Add the beat after the substitution line in
  Chapter 4 by dragging clip spacing, not by adding a break tag.
- **No music under Chapter 4.** If you score the piece at all, duck out
  entirely for that chapter. Silence is doing work there.
- **Music track** is separate from narration and doesn't affect regeneration
  cost — safe to experiment with late.
- **Video track** if you're screen-recording the demo artifact: import the
  capture, align narration to the moment each grid cell is clicked. Sentence-
  level timing control is the reason to assemble here rather than in an editor.
- **Export** per chapter while iterating, whole project at the end. If every
  paragraph is already generated, export costs no additional credits.
  Auto-regenerate runs a quality check on bulk export and re-rolls flagged
  audio up to twice at no cost.
- Free/Starter/Creator plans export 128 kbps MP3 or WAV from a 128 kbps source;
  Pro and above get 44.1 kHz 16-bit WAV. If this is going in front of a client,
  check which tier you're on before you record the screen capture — you can't
  change the quality setting on an existing project.

---

## 7. Cuts

If you need a shorter version, drop Chapters 1 and 5. The argument survives on
2, 3, 4, and 6 — roughly two and a half minutes.

Chapter 6's final paragraph is not optional in any cut. In a managed-services
environment, "where did the data come from" is the first question anyone asks,
and answering it before it's asked is worth more than any capability claim in
the script.
