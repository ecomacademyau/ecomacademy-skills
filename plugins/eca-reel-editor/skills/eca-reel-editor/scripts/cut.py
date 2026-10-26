#!/usr/bin/env python3
"""Apply the approved rough cut: keep spans from edl.json (in play order), speed up, optional colour grade, scale to the
brand resolution. Writes master.mp4 in the reel folder.
Usage: python3 cut.py <reel-folder>      (reads <reel-folder>/edl.json and <reels_home>/brand.json)"""
import os, sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import common
from pacing import pacing

reel = Path(sys.argv[1]).expanduser()
brand = common.load_brand()
edl = common.load_json(reel / "edl.json")

src, audio = reel / edl["source"], reel / edl.get("audio", "voice.wav")
spans = edl["keep"]
speed = pacing(brand)["speed"]
w, h = brand.get("resolution", [1080, 1920])
if os.environ.get("REEL_PREVIEW"): w, h = 1080, 1920          # previews cut at 1080p: a quarter of the work
grade = brand.get("grade")
FADE = 0.012  # tiny audio fades at every join so cuts never click

vp, ap = [], []
for k, (a, b) in enumerate(spans):
    vp.append(f"[0:v]trim=start={a}:end={b},setpts=PTS-STARTPTS[v{k}]")
    ap.append(f"[1:a]atrim=start={a}:end={b},asetpts=PTS-STARTPTS,"
              f"afade=t=in:d={FADE},afade=t=out:st={max(b - a - FADE, 0):.3f}:d={FADE}[a{k}]")
n = len(spans)
post = [f"setpts=PTS/{speed}", f"scale={w}:{h}:force_original_aspect_ratio=increase", f"crop={w}:{h}", "fps=30"]
if grade:
    if edl.get("grade_from") is not None:   # grade switches on at this reel second (a "before/after" moment)
        # shortcut: splits filters on commas, so a filter option containing a comma breaks; quote-aware split if one ever does
        grade = ",".join(f + (":" if "=" in f else "=") + f"enable='gte(t,{float(edl['grade_from']):.3f})'" for f in grade.split(","))
    post.insert(1, grade)
vcat = "".join(f"[v{k}]" for k in range(n)) + f"concat=n={n}:v=1:a=0," + ",".join(post) + "[vout]"
acat = "".join(f"[a{k}]" for k in range(n)) + f"concat=n={n}:v=0:a=1,atempo={speed}[aout]"

script = reel / "cut_filter.txt"
script.write_text(";".join(vp + ap) + ";" + vcat + ";" + acat, encoding="utf-8")
kept = sum(b - a for a, b in spans)
print(f"{n} spans, {kept:.1f}s kept -> {kept / speed:.1f}s at {speed}x, {w}x{h}")
if kept / speed > brand.get("max_seconds", 60):
    print(f"warning: longer than {brand.get('max_seconds', 60)}s - suggest more cuts")

# preview: fast (hardware 12M on a Mac, libx264 crf 20 veryfast elsewhere); final master: libx264 crf 16 on every platform
venc = (common.video_encoder(bitrate="12M", crf=20, preset="veryfast") if os.environ.get("REEL_PREVIEW")
        else ["-c:v", "libx264", "-preset", "medium", "-crf", "16"])
common.run([common.ffmpeg(), "-y", "-v", "error", "-stats", "-i", src, "-i", audio,
            *common.filter_script_args(script), "-map", "[vout]", "-map", "[aout]", *venc, "-pix_fmt", "yuv420p",
            "-c:a", "aac", "-b:a", "256k", "-movflags", "+faststart", reel / "master.mp4"])
print(reel / "master.mp4")
