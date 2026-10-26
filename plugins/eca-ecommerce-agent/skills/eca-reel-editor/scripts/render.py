#!/usr/bin/env python3
"""Build the reel from edit.json and render it. Logs how long each part took to <reel>/timings.log.
Usage: python3 render.py <reel-folder> [--capcut] [--final]
Gentle by default: 2 Chrome workers at low priority, 1080p preview. --final renders at the brand resolution (4K)."""
import os, sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import common

HERE = Path(__file__).resolve().parent
LN = "loudnorm=I=-14:TP=-1.5:LRA=7"
# Optional music bed: sits ~18 dB under the voice and ducks further while she talks, then the whole mix to -14 LUFS.
MUSIC_MIX = ("[1:a]volume=-18dB,afade=t=in:d=0.5[m];[0:a]asplit[v][key];"
             "[m][key]sidechaincompress=threshold=0.02:ratio=6:attack=15:release=350[md];"
             f"[v][md]amix=inputs=2:duration=first:normalize=0,{LN}[a]")


def main():
    common.utf8_console()
    if len(sys.argv) < 2:
        sys.exit(__doc__)
    reel = Path(sys.argv[1]).expanduser().resolve()
    final = "--final" in sys.argv[2:]
    passthru = [a for a in sys.argv[2:] if a != "--final"]
    workers = os.environ.get("REEL_WORKERS", "2")          # each worker is a Chrome; 2 keeps a 16 GB laptop usable
    py, ff = common.python(), common.ffmpeg()
    brand = common.load_brand()
    r = brand.get("resolution", [1080, 1920])
    res = "portrait-4k" if (final and r[0] >= 2160) else "portrait"   # previews at 1080p: a quarter of the pixels of 4K

    # a preview cut leaves a 1080p master.mp4; re-cut it at the brand resolution so the final isn't an upscale
    if final:
        want, have = int(r[1]), common.probe_height(reel / "master.mp4")
        if have < want:
            print(f"master.mp4 is {have}p, re-cutting at {want}p for the final")
            env = dict(os.environ)
            env.pop("REEL_PREVIEW", None)
            common.run([py, HERE / "cut.py", reel], env=env, low=False)

    gsap = common.ENGINE / "gsap.min.js"
    if not (gsap.is_file() and gsap.stat().st_size > 0):
        common.run([py, HERE / "setup_engine.py"], low=False)

    common.stamp(reel, "build:start")
    common.run([py, HERE / "build_reel.py", reel, *passthru], low=False)
    common.stamp(reel, "build:end")

    common.stamp(reel, "render:start")
    common.run(common.hyperframes("render", reel / "proj", "--workers", workers, "-o", reel / "final.mp4",
                                  "--resolution", res, "--quality", "delivery", "--quiet"))
    common.stamp(reel, "render:end")

    # Final mix (video copied, not re-encoded).
    music = brand.get("music")
    music = Path(music).expanduser() if music else None
    final_ln = reel / "final_ln.mp4"
    if music and music.is_file():
        common.run([ff, "-v", "error", "-y", "-i", reel / "final.mp4", "-stream_loop", "-1", "-i", music,
                    "-filter_complex", MUSIC_MIX, "-map", "0:v", "-map", "[a]", "-c:v", "copy",
                    "-ar", "48000", "-c:a", "aac", "-b:a", "256k", final_ln])
    else:
        common.run([ff, "-v", "error", "-y", "-i", reel / "final.mp4", "-c:v", "copy", "-af", LN,
                    "-ar", "48000", "-c:a", "aac", "-b:a", "256k", final_ln])
    os.replace(final_ln, reel / "final.mp4")
    common.run([py, HERE / "timings.py", reel], low=False)


if __name__ == "__main__":
    main()
