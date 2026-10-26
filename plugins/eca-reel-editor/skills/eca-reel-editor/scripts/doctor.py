#!/usr/bin/env python3
"""Check everything the reel editor needs and say plainly whether you can edit.
Ends with one of: READY · READY WITH LIMITS (works, something optional is missing) · MISSING (fix before editing).
Usage: python3 doctor.py        exit 1 when something is MISSING, else 0"""
import os, platform, shutil, subprocess, sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import common

HERE = Path(__file__).resolve().parent
state = {"missing": False, "limits": False}


def ok(msg):
    print(f"  ✅ {msg}")


def warn(msg, fix=None):
    print(f"  ⚠️  {msg}" + (f"\n     {fix}" if fix else ""))
    state["limits"] = True


def no(msg, fix):
    print(f"  ❌ {msg}\n     fix: {fix}")
    state["missing"] = True


def platform_line():
    if common.IS_MAC:
        return f"macOS {platform.mac_ver()[0] or platform.release()} {platform.machine()}"
    if common.IS_WIN:
        rel, ver = platform.release(), platform.version()
        try:   # Windows 11 still reports release "10"; the build number tells them apart
            if rel == "10" and int(ver.split(".")[-1]) >= 22000:
                rel = "11"
        except ValueError:
            pass
        return f"Windows {rel} (build {ver}) {platform.machine()}"
    distro = ""
    try:
        for line in Path("/etc/os-release").read_text(encoding="utf-8").splitlines():
            if line.startswith("PRETTY_NAME="):
                distro = line.split("=", 1)[1].strip().strip('"')
    except OSError:
        pass
    return f"Linux {distro or platform.release()} {platform.machine()}".replace("  ", " ")


def claude_mcp_list():
    """stdout of `claude mcp list` (health check of every connector; ~20 s), or None when the CLI isn't on PATH / fails."""
    cli = shutil.which("claude") or (shutil.which("claude.cmd") if common.IS_WIN else None)
    if not cli:
        return None
    try:
        r = subprocess.run([cli, "mcp", "list"], capture_output=True, text=True, timeout=180, encoding="utf-8", errors="replace")
        return (r.stdout or "") + (r.stderr or "")
    except (OSError, subprocess.TimeoutExpired):
        return None


def main():
    common.utf8_console()
    print("Reel editor check")
    print(f"  🖥  {platform_line()}")

    # ---- tools
    if common.tool("ffmpeg"):
        ok("ffmpeg (on PATH)")
    elif common._npm_static("ffmpeg-static"):
        ok("ffmpeg (ffmpeg-static npm package; not on PATH)")
    else:
        fix = ("macOS: brew install ffmpeg" if common.IS_MAC else
               "Windows: winget install Gyan.FFmpeg (then open a new terminal), or `npm i -g ffmpeg-static ffprobe-static`" if common.IS_WIN else
               "Linux: sudo apt install ffmpeg (or your distro's package)")
        no("ffmpeg", fix)
    nd = common.node()
    if nd:
        try:
            ver = subprocess.run([nd, "-v"], capture_output=True, text=True, timeout=20).stdout.strip()
        except (OSError, subprocess.TimeoutExpired):
            ver = "(version unknown)"
        ok(f"Node.js {ver}")
    else:
        no("Node.js", "install the LTS version from https://nodejs.org")
    ok(f"Python {platform.python_version()}")
    if common.IS_WIN:
        warn("Windows: untested platform — please report problems", "macOS is the tested platform")
    elif not common.IS_MAC:
        warn("Linux: untested platform — please report problems", "macOS is the tested platform")

    # ---- HyperFrames skills: either location is fine
    if any((Path.home() / d / "skills" / "hyperframes").is_dir() for d in (".claude", ".agents")):
        ok("HyperFrames skills")
    else:
        no("HyperFrames skills", "npx skills add heygen-com/hyperframes")

    # ---- the reel template engine (gsap + synthesised sfx + catalog motions)
    eng = common.ENGINE
    def engine_ready():
        return all(p.is_file() and p.stat().st_size > 0 for p in (eng / "gsap.min.js", eng / "sfx" / "whoosh.wav"))
    if engine_ready():
        ok("reel template engine")
    else:
        try:
            subprocess.run([common.python(), str(HERE / "setup_engine.py")], capture_output=True, timeout=1800)
        except (OSError, subprocess.TimeoutExpired):
            pass
        if engine_ready():
            ok("reel template engine (just set up)")
        else:
            no("reel template engine", "python3 scripts/setup_engine.py")

    if shutil.which("deepFilter"):
        ok("noise removal (DeepFilterNet)")
    else:
        warn("DeepFilterNet not installed", "background noise removal falls back to ffmpeg's weaker filter. Install: uv tool install deepfilternet")

    # ---- brand file
    home = common.reels_home(create=False)
    brand_file = home / "brand.json"
    brand = None
    if brand_file.is_file():
        try:
            brand = common.load_json(brand_file)
        except ValueError as e:
            no(f"brand file ({brand_file}) is not valid JSON", f"fix it or re-make it: python3 scripts/brand_from_eca.py ({e})")
    if brand is not None:
        ok(f"brand file ({home})")
        # every font the brand names must exist, or captions silently fall back to a system font
        for role, f in (brand.get("fonts") or {}).items():
            p = (f or {}).get("file")
            if p and not Path(p).expanduser().exists():
                warn(f"{role} font file missing: {p}", "captions/titles will use a fallback font until it's in place")
            elif p:
                ok(f"{role} font ({f.get('family')})")
    elif brand is None and not brand_file.exists():
        print("  ➖ no brand.json yet — run `python3 scripts/brand_from_eca.py` to make it from brand-data.md")
    print("  ℹ️  the review page needs Claude Code's Artifact tools; Claude checks this when you start an edit (chat review otherwise)")

    # ---- EcomOS connector (product cards + reel logging) and, on the CapCut route, the CapCut connector
    mcp = claude_mcp_list()
    ecomos_fix = ("Add EcomOS as a custom connector in Claude (Settings → Connectors → Add custom connector → "
                  "https://ecomos.ecomacademy.co/mcp → Connect → Allow). If you already did that in claude.ai, ignore this: "
                  "`claude mcp list` only shows servers added from the terminal.")
    if mcp is None:
        warn("couldn't run `claude mcp list` (Claude Code CLI not on PATH?) — EcomOS connection unverified", ecomos_fix)
    elif "ecomos" in mcp.lower():
        ok("EcomOS connected")
    else:
        warn("EcomOS not connected — product cards and reel logging are off.", ecomos_fix)
    if brand and brand.get("capcut"):
        if (Path(os.environ.get("CAPCUT_SKILLS_DIR") or "/nonexistent").expanduser() / "capcut-stdraft-builder").is_dir():
            ok("CapCut helper scripts")
        else:
            warn("CapCut helper scripts not found", "the MP4 still works; for CapCut see references/capcut.md step 3")
        if mcp and "capcut_creation" in mcp:
            ok("CapCut connector added")
        else:
            warn("CapCut connector not added", "the MP4 still works; for CapCut see references/capcut.md step 2")

    # ---- disk
    free = common.free_gb(Path.home())
    if free >= 10:
        ok(f"{free} GB free disk")
    else:
        no(f"only {free} GB free disk", "free up 10+ GB (35+ GB for 4K exports)")

    if state["missing"]:
        print("MISSING: fix the ❌ items, then run this again.")
        sys.exit(1)
    elif state["limits"]:
        print("READY WITH LIMITS: you can edit; the ⚠️ items reduce quality or skip an optional extra.")
    else:
        print("READY")


if __name__ == "__main__":
    main()
