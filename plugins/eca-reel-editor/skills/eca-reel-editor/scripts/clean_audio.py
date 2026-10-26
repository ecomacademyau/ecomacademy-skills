#!/usr/bin/env python3
"""Clean a talking-head voice track: light noise removal (DeepFilterNet + gate), de-essing, gentle EQ + compression,
two-pass loudness to -14 LUFS.
Usage: python3 clean_audio.py <clip> <out.wav> [--no-denoise]   (noise removal is ON by default: birds, traffic, fans, room hiss)"""
import array, json, math, os, re, shutil, sys, tempfile, wave
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import common

GATE = "agate=threshold=0.015:ratio=3:range=0.25:attack=4:release=150,"
# Rumble cut, take out boxiness, add clarity and air, tame harsh "s" sounds (the clarity boost exaggerates them),
# light 3:1 compression (keeps it natural, not squashed).
EQ = ("highpass=f=85,equalizer=f=220:t=q:w=1:g=-2.5,equalizer=f=3200:t=q:w=1:g=2.5,highshelf=f=9000:g=2,"
      "deesser=i=0.4:m=0.5:f=0.5,acompressor=ratio=3:threshold=-20dB:attack=5:release=80")
LN = "loudnorm=I=-14:TP=-1.5:LRA=7"


def noise_floor(path):
    """Sound-engineer check: the gaps between words must be quiet. 10th-percentile 50 ms level = the background."""
    with wave.open(str(path)) as w:
        sr = w.getframerate()
        a = array.array("h")
        a.frombytes(w.readframes(w.getnframes()))
    hop = int(sr * 0.05)
    lev = sorted(20 * math.log10(max(1.0, math.sqrt(sum(x * x for x in a[i:i + hop:4]) / (hop / 4))) / 32768)
                 for i in range(0, len(a) - hop, hop))
    return round(lev[len(lev) // 10])


def main():
    common.utf8_console()
    if len(sys.argv) < 3:
        sys.exit(__doc__)
    src_in, out = Path(sys.argv[1]).expanduser(), Path(sys.argv[2]).expanduser()
    denoise = sys.argv[3] if len(sys.argv) > 3 else "--denoise"
    ff = common.ffmpeg()

    with tempfile.TemporaryDirectory() as tmp:
        tmp = Path(tmp)
        src = tmp / "raw.wav"
        common.run([ff, "-v", "error", "-y", "-i", src_in, "-vn", "-ac", "1", "-ar", "48000", src], low=False)

        if denoise == "--denoise":
            df = shutil.which("deepFilter")
            if df:
                # capped at 30 dB: light, natural, no underwater artefacts
                common.run([df, "-a", os.environ.get("DENOISE_DB", "30"), src, "-o", tmp / "dfn"], low=False, capture=True)
                src = sorted((tmp / "dfn").glob("*.wav"))[0]
            else:
                print("note: DeepFilterNet not installed, using ffmpeg's built-in denoiser (weaker on birds/traffic)", file=sys.stderr)
                common.run([ff, "-v", "error", "-y", "-i", src, "-af", "afftdn=nf=-25", tmp / "dn.wav"], low=False)
                src = tmp / "dn.wav"

        # Gate: whatever noise survives between words is pulled down a further ~12 dB (no pumping on speech).
        chain = ("" if denoise == "--no-denoise" else GATE) + EQ

        # pass 1: measure
        err = common.run([ff, "-hide_banner", "-i", src, "-af", f"{chain},{LN}:print_format=json", "-f", "null", "-"],
                         check=False, low=False, capture=True).stderr
        m = re.search(r"^\{.*?^\}", err, re.S | re.M)
        if not m:
            sys.exit("loudnorm measurement failed:\n" + err[-800:])
        j = json.loads(m.group(0))
        # pass 2: apply
        common.run([ff, "-v", "error", "-y", "-i", src, "-af",
                    f"{chain},{LN}:measured_I={j['input_i']}:measured_TP={j['input_tp']}:measured_LRA={j['input_lra']}"
                    f":measured_thresh={j['input_thresh']}:offset={j['target_offset']}:linear=true",
                    "-ar", "48000", out], low=False)

    floor = noise_floor(out)
    print(f"background noise between words: {floor} dB (want -45 or quieter)", file=sys.stderr)
    if floor > -45:
        print("WARNING: still noisy - check the raw clip (wind/handling noise can't be fully removed)", file=sys.stderr)
    print(out)


if __name__ == "__main__":
    main()
