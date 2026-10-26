#!/usr/bin/env python3
"""One-time: fetch the animation library and make the sound effects. Re-run safely any time.
Usage: python3 setup_engine.py"""
import hashlib, json, os, re, subprocess, sys, urllib.request
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import common

E = common.ENGINE
GSAP_URL = "https://cdn.jsdelivr.net/npm/gsap@3.13.0/dist/gsap.min.js"
GSAP_SHA = "96c01b81f44a3290e2b4532f55e2c9534b2adc43273a19f3756b2cb41f0fd0b6"   # gsap 3.13.0: refuse a tampered download

# Sound effects synthesised with ffmpeg: no downloads, no licences to worry about.
SFX = [
    ("whoosh", "anoisesrc=d=0.5:c=pink:a=0.6", "highpass=f=500,lowpass=f=6000,afade=t=in:d=0.28:curve=exp,afade=t=out:st=0.28:d=0.22"),
    ("pop", "sine=f=620:d=0.12", "vibrato=f=12:d=0.4,afade=t=out:st=0.02:d=0.10,volume=1.6"),
    ("snap", "anoisesrc=d=0.06:c=white:a=0.9", "highpass=f=2200,afade=t=out:st=0.005:d=0.05"),
    ("chime", "sine=f=1320:d=0.7", "aecho=0.6:0.5:60:0.35,afade=t=out:st=0.05:d=0.65"),
    ("swish", "anoisesrc=d=0.25:c=pink:a=0.5", "highpass=f=900,lowpass=f=7000,afade=t=in:d=0.12:curve=exp,afade=t=out:st=0.12:d=0.13"),
    ("typing", "aevalsrc='0.7*random(0)*lt(mod(t\\,0.085)\\,0.006)':d=0.9", "highpass=f=1500,lowpass=f=8000,volume=1.8"),
]
# HyperFrames catalog motions (carousels, captions, charts, social cards): fetched from HyperFrames, not shipped in this repo.
MOTIONS = ["caption-camera-follow", "carousel-vision-1", "carousel-path-1", "carousel-circle-1", "carousel-orbit-1", "hw-arrow",
           "hw-underline", "oversized-cursor", "notification-stack", "code-terminal-run", "chat-message", "yt-comment-card",
           "instagram-follow", "count-up", "animated-bar-chart", "mk-line-graph", "native-notification-pop", "x-follow-card", "chart-story"]
HF_JSON = {"$schema": "https://hyperframes.heygen.com/schema/hyperframes.json",
           "registry": "https://raw.githubusercontent.com/heygen-com/hyperframes/main/registry",
           "paths": {"blocks": "compositions", "components": "compositions/components", "assets": "assets"}}


def nonempty(p):
    return p.is_file() and p.stat().st_size > 0


def gsap():
    dst = E / "gsap.min.js"
    if nonempty(dst):
        return
    data = urllib.request.urlopen(urllib.request.Request(GSAP_URL, headers={"User-Agent": "eca-reel-editor"}), timeout=120).read()
    if hashlib.sha256(data).hexdigest() != GSAP_SHA:
        sys.exit("gsap download failed its checksum - not installing it")
    tmp = E / "gsap.min.js.tmp"
    tmp.write_bytes(data)
    os.replace(tmp, dst)


def sfx():
    ff = common.ffmpeg()
    (E / "sfx").mkdir(parents=True, exist_ok=True)
    for name, src, af in SFX:
        dst = E / "sfx" / f"{name}.wav"
        if not nonempty(dst):
            common.run([ff, "-v", "error", "-y", "-f", "lavfi", "-i", src, "-af", af, "-ar", "48000", "-ac", "2", dst], low=False)
    # Bring every effect up to a -1 dB peak: synthesised noise comes out ~20 dB quieter than a voice and disappears in the mix.
    for f in sorted((E / "sfx").glob("*.wav")):
        norm = f.with_name(f.name + ".norm")
        if norm.exists():
            continue
        err = common.run([ff, "-hide_banner", "-i", f, "-af", "volumedetect", "-f", "null", "-"], check=False, low=False, capture=True).stderr
        m = re.search(r"max_volume: (-*[0-9.]*) dB", err)
        if not m:
            continue
        gain = round(-1 - float(m.group(1)), 2)
        tmp = f.with_name(f.name + ".tmp.wav")
        common.run([ff, "-v", "error", "-y", "-i", f, "-af", f"volume={gain}dB", tmp], low=False)
        os.replace(tmp, f)
        norm.touch()


def motions():
    H = E / "hf"
    H.mkdir(parents=True, exist_ok=True)
    if not (H / "hyperframes.json").exists():
        (H / "hyperframes.json").write_text(json.dumps(HF_JSON, separators=(",", ":")), encoding="utf-8")
    if not (H / "package.json").exists():
        (H / "package.json").write_text('{"name":"engine","private":true,"type":"module"}\n', encoding="utf-8")
    for m in MOTIONS:
        if (H / "compositions" / f"{m}.html").exists() or (H / "compositions" / "components" / f"{m}.html").exists():
            continue
        try:
            common.run(common.hyperframes("add", m), cwd=str(H), low=False, capture=True, timeout=600)
        except (subprocess.CalledProcessError, subprocess.TimeoutExpired, OSError):
            print(f"note: couldn't fetch motion {m}", file=sys.stderr)


def main():
    common.utf8_console()
    E.mkdir(parents=True, exist_ok=True)
    gsap()
    sfx()
    motions()
    print(f"engine ready: {E}")


if __name__ == "__main__":
    main()
