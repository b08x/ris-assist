#!/usr/bin/env python3
"""
Render the coverage-demo narration with Supertonic 3, fully on-device.

    pip install supertonic soundfile numpy
    python build_narration.py narration-supertonic.txt --voice M1 --out build/

Produces:
    build/<NN>_<section>.wav    one file per section
    build/full.wav              everything, with pauses
    build/manifest.json         chunk text, duration, offset — for captioning

Why a build script rather than one synthesize() call:

  * Supertonic has no break/pause markup. Silence is assembled here, not
    requested from the model.
  * Chunk-level files are the unit of revision. Re-render one chunk, rebuild,
    done — no credits, no regeneration limits, no cloud round trip.
  * The manifest gives exact offsets, which is what a caption or timeline
    import needs.

Code MIT (matching the Supertonic sample code). Note that the *model weights*
are OpenRAIL-M, which carries use restrictions — check them before shipping
generated audio in a commercial context.
"""

import argparse
import json
import re
import sys
from pathlib import Path

import numpy as np
import soundfile as sf

SAMPLE_RATE = 44100  # Supertonic outputs 44.1 kHz natively

SECTION_RE = re.compile(r"^@section\s+(\S+)\s*$")
PAUSE_RE = re.compile(r"^@pause\s+([\d.]+)\s*$")


def parse(path: Path):
    """Yield ('section', name) | ('pause', seconds) | ('text', chunk)."""
    section_seen = False
    buffer: list[str] = []

    def flush():
        nonlocal buffer
        if buffer:
            yield ("text", " ".join(buffer).strip())
            buffer = []

    for raw in path.read_text(encoding="utf-8").splitlines():
        line = raw.rstrip()

        if line.lstrip().startswith("#"):
            continue

        if not line.strip():
            yield from flush()
            continue

        m = SECTION_RE.match(line)
        if m:
            yield from flush()
            section_seen = True
            yield ("section", m.group(1))
            continue

        m = PAUSE_RE.match(line)
        if m:
            yield from flush()
            yield ("pause", float(m.group(1)))
            continue

        buffer.append(line.strip())

    yield from flush()

    if not section_seen:
        print("warning: no @section directives found — everything lands in one file",
              file=sys.stderr)


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("script", type=Path)
    ap.add_argument("--out", type=Path, default=Path("build"))
    ap.add_argument("--voice", default="M1",
                    help="preset voice style name (e.g. M1, F1)")
    ap.add_argument("--voice-json", type=Path, default=None,
                    help="Voice Builder JSON for a custom voice profile")
    ap.add_argument("--lang", default="en",
                    help='language code, or "na" for language-agnostic')
    ap.add_argument("--steps", type=int, default=10,
                    help="quality 5-12; default 8, 10 is a good narration setting")
    ap.add_argument("--speed", type=float, default=0.97,
                    help="0.7-2.0; slightly under 1.0 suits explanatory narration")
    ap.add_argument("--lead-in", type=float, default=0.3,
                    help="silence at the very start, seconds")
    ap.add_argument("--tail", type=float, default=0.8,
                    help="silence at the very end, seconds")
    args = ap.parse_args()

    if not args.script.exists():
        print(f"error: {args.script} not found", file=sys.stderr)
        return 1

    from supertonic import TTS

    tts = TTS(auto_download=True)
    if args.voice_json:
        # Voice Builder profiles are the supported route to a custom voice;
        # the open-weight repo ships fixed preset voices only.
        style = tts.get_voice_style(voice_path=str(args.voice_json))
    else:
        style = tts.get_voice_style(voice_name=args.voice)

    args.out.mkdir(parents=True, exist_ok=True)

    def silence(seconds: float) -> np.ndarray:
        return np.zeros(int(seconds * SAMPLE_RATE), dtype=np.float32)

    full: list[np.ndarray] = [silence(args.lead_in)]
    section_audio: list[np.ndarray] = []
    section_name = "00_intro"
    section_index = 0
    manifest: list[dict] = []
    chunk_no = 0

    def write_section():
        nonlocal section_audio, section_index
        if not section_audio:
            return
        section_index += 1
        out = args.out / f"{section_index:02d}_{section_name}.wav"
        sf.write(out, np.concatenate(section_audio), SAMPLE_RATE)
        print(f"  → {out.name}")
        section_audio = []

    for kind, value in parse(args.script):
        if kind == "section":
            write_section()
            section_name = value
            print(f"[{value}]")

        elif kind == "pause":
            pad = silence(value)
            full.append(pad)
            section_audio.append(pad)

        else:
            chunk_no += 1
            offset = sum(len(a) for a in full) / SAMPLE_RATE
            wav, duration = tts.synthesize(
                text=value,
                lang=args.lang,
                voice_style=style,
                total_steps=args.steps,
                speed=args.speed,
            )
            audio = np.asarray(wav).squeeze().astype(np.float32)
            full.append(audio)
            section_audio.append(audio)

            chunk_path = args.out / f"chunk_{chunk_no:03d}.wav"
            sf.write(chunk_path, audio, SAMPLE_RATE)

            manifest.append({
                "chunk": chunk_no,
                "section": section_name,
                "offset_sec": round(offset, 3),
                "duration_sec": round(float(np.atleast_1d(duration)[0]), 3),
                "file": chunk_path.name,
                "text": value,
            })
            print(f"  {chunk_no:03d} {float(np.atleast_1d(duration)[0]):5.2f}s  "
                  f"{value[:58]}{'…' if len(value) > 58 else ''}")

    write_section()

    full.append(silence(args.tail))
    mix = np.concatenate(full)
    sf.write(args.out / "full.wav", mix, SAMPLE_RATE)

    (args.out / "manifest.json").write_text(
        json.dumps({
            "sample_rate": SAMPLE_RATE,
            "voice": args.voice_json.name if args.voice_json else args.voice,
            "lang": args.lang,
            "total_steps": args.steps,
            "speed": args.speed,
            "total_sec": round(len(mix) / SAMPLE_RATE, 2),
            "chunks": manifest,
        }, indent=2),
        encoding="utf-8",
    )

    print(f"\nfull.wav — {len(mix) / SAMPLE_RATE:.1f}s, {chunk_no} chunks")
    print("re-render one chunk by editing the script and running again; "
          "synthesis is local and free.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
