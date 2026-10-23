#!/usr/bin/env python3
"""Generate original CC0 sound effects; requires Python 3 and ffmpeg.

These synthesized cues replace the upstream effects as a set because the
upstream credits include CC BY-NC and CC Sampling+ recordings without mapping
every edited file to its source. No upstream recording is sampled here.

Usage: python3 -I tools/generate-tofu-sounds.py --output assets/sounds
"""

import argparse
import io
import math
from pathlib import Path
import random
import shutil
import struct
import subprocess
import wave

RATE = 44100
TAU = 2 * math.pi


def tone(t, frequency):
    return math.sin(TAU * frequency * t)


def bell(t, frequency):
    return (tone(t, frequency) + 0.3 * tone(t, frequency * 2.7)) * math.exp(-15 * t)


def synthesize(name, duration, seed):
    rng = random.Random(seed)
    frames = bytearray()
    for i in range(round(RATE * duration)):
        t = i / RATE
        progress = t / duration
        if name.startswith("button"):
            sample = bell(t, {"button1": 520, "button2": 660, "button3": 820}[name])
        elif name == "coin_insert":
            sample = bell(t, 1100) + 0.35 * bell(max(t - 0.07, 0), 1650) * (t > 0.07)
        elif name == "coin_get":
            sample = bell(t, 880) if t < 0.12 else bell(t - 0.12, 1320)
        elif name == "machine_start":
            phase = t % 0.09
            sample = bell(phase, 360 + 480 * progress) * (1 - progress)
        elif name == "drumroll":
            phase = t % 0.045
            sample = rng.uniform(-1, 1) * math.exp(-100 * phase) * (0.2 + 0.8 * progress)
        elif name == "evil_laugh":
            phase = t % 0.2
            sample = tone(t, 180) * math.exp(-18 * phase) * (0.6 + 0.4 * tone(t, 7))
        elif name in ("scratch_in", "scratch_out", "whoosh"):
            sample = rng.uniform(-1, 1) * math.sin(math.pi * progress) ** 2
            sample *= 0.4 + 0.6 * (progress if name != "scratch_out" else 1 - progress)
        elif name == "squeak":
            sample = math.sin(TAU * (900 * t + 700 * t * t)) * math.sin(math.pi * progress)
        elif name in ("bonk", "thump"):
            sample = tone(t, 150 if name == "bonk" else 75) * math.exp(-20 * t)
        elif name == "fart":
            sample = (tone(t, 65) + 0.3 * rng.uniform(-1, 1)) * math.exp(-5 * t)
        else:
            raise ValueError(name)
        fade = min(1, t / 0.005, (duration - t) / 0.02)
        amplitude = max(-1, min(1, sample * fade * 0.45))
        frames.extend(struct.pack("<h", round(amplitude * 32767)))
    stream = io.BytesIO()
    with wave.open(stream, "wb") as output:
        output.setnchannels(1)
        output.setsampwidth(2)
        output.setframerate(RATE)
        output.writeframes(frames)
    return stream.getvalue()


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", required=True, type=Path)
    args = parser.parse_args()
    ffmpeg = shutil.which("ffmpeg")
    if not ffmpeg:
        parser.error("ffmpeg is required to regenerate sounds, but not to run the app")
    args.output.mkdir(parents=True, exist_ok=True)
    effects = {
        "button1": 0.2,
        "button2": 0.2,
        "button3": 0.2,
        "coin_insert": 0.28,
        "coin_get": 0.45,
        "machine_start": 0.8,
        "drumroll": 1.6,
        "evil_laugh": 0.8,
        "scratch_in": 0.3,
        "scratch_out": 0.3,
        "whoosh": 0.3,
        "squeak": 0.18,
        "bonk": 0.2,
        "thump": 0.25,
        "fart": 0.45,
    }
    for seed, (name, duration) in enumerate(effects.items()):
        destination = args.output / (name + ".mp3")
        subprocess.run(
            [ffmpeg, "-nostdin", "-hide_banner", "-loglevel", "error", "-y",
             "-f", "wav", "-i", "pipe:0", "-map_metadata", "-1", "-c:a",
             "libmp3lame", "-b:a", "96k", "-write_xing", "0", str(destination)],
            input=synthesize(name, duration, seed), check=True,
        )
        print(destination.name)


if __name__ == "__main__":
    main()
