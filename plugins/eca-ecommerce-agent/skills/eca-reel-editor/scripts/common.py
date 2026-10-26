"""Shared helpers for the ECA reel editor scripts. Works the same on macOS, Windows and Linux.

Every script imports from here instead of assuming "~", "/", `nice` or a Mac-only encoder:
  reels_home()        the member's reel workspace: $REELS_HOME, else ./reels (the working folder, next to ./brand/)
  load_brand()        brand.json from reels_home() (made by brand_from_eca.py from brand-data.md)
  ffmpeg()/ffprobe()  the binaries: PATH first, then the ffmpeg-static / ffprobe-static npm packages
  run(cmd, ...)       subprocess.run at low priority (os.nice on POSIX, BELOW_NORMAL_PRIORITY_CLASS on Windows)
  npx(), node()       the right executable names (npx.cmd on Windows)
  video_encoder(...)  hardware H.264 on a Mac, libx264 elsewhere
"""
import json, os, shutil, subprocess, sys
from pathlib import Path

IS_WIN = sys.platform.startswith("win")
IS_MAC = sys.platform == "darwin"
SKILL_DIR = Path(__file__).resolve().parent.parent
ENGINE = SKILL_DIR / "engine"
HYPERFRAMES = "hyperframes@0.8.145"          # pinned: the template engine was built against this render pipeline
NICE = 15


def reels_home(create=True) -> Path:
    """The reel workspace. Defaults to ./reels in the member's working folder (where ./brand/brand-data.md lives)."""
    home = Path(os.environ.get("REELS_HOME") or (Path.cwd() / "reels")).expanduser().resolve()
    if create:
        home.mkdir(parents=True, exist_ok=True)
    return home


def brand_path() -> Path:
    return reels_home() / "brand.json"


def load_brand() -> dict:
    p = brand_path()
    if not p.exists():
        sys.exit(f"no brand.json at {p}\nMake it from the brand file first:  python3 scripts/brand_from_eca.py")
    with open(p, encoding="utf-8") as fh:
        return json.load(fh)


def save_json(path, data, indent=1):
    Path(path).write_text(json.dumps(data, indent=indent, ensure_ascii=False), encoding="utf-8")


def load_json(path):
    with open(path, encoding="utf-8") as fh:
        return json.load(fh)


# ---- executables ------------------------------------------------------------------------------------------------

def _npm_static(pkg, export="default"):
    """Path exported by an installed ffmpeg-static / ffprobe-static package (optional fallback when ffmpeg isn't on PATH)."""
    nd = node()
    if not nd:
        return None
    js = {"ffmpeg-static": "console.log(require('ffmpeg-static'))",
          "ffprobe-static": "console.log(require('ffprobe-static').path)"}[pkg]
    for cwd in (ENGINE / "hf", SKILL_DIR, Path.cwd()):
        try:
            out = subprocess.run([nd, "-e", js], capture_output=True, text=True, cwd=str(cwd) if cwd.exists() else None, timeout=20).stdout.strip()
        except (OSError, subprocess.TimeoutExpired):
            continue
        if out and Path(out).exists():
            return out
    return None


def tool(name):
    """Full path of a command, or None. On Windows shutil.which also finds .cmd/.exe wrappers."""
    return shutil.which(name)


def ffmpeg():
    return tool("ffmpeg") or _npm_static("ffmpeg-static") or "ffmpeg"


def ffprobe():
    return tool("ffprobe") or _npm_static("ffprobe-static") or "ffprobe"


def ffmpeg_major() -> int:
    """Major version of the ffmpeg in use (0 when unknown)."""
    try:
        import re
        m = re.search(r"ffmpeg version n?(\d+)", subprocess.run([ffmpeg(), "-version"], capture_output=True, text=True).stdout)
        return int(m.group(1)) if m else 0
    except (OSError, ValueError):
        return 0


def filter_script_args(path):
    """ffmpeg 8 renamed -filter_complex_script to the generic '-/filter_complex <file>' form."""
    return ["-/filter_complex", str(path)] if ffmpeg_major() >= 8 else ["-filter_complex_script", str(path)]


def node():
    return tool("node")


def npx():
    return tool("npx") or ("npx.cmd" if IS_WIN else "npx")


def hyperframes(*args):
    """Command list for the pinned HyperFrames CLI."""
    return [npx(), "-y", HYPERFRAMES, *args]


def python():
    return sys.executable or ("python" if IS_WIN else "python3")


# ---- processes --------------------------------------------------------------------------------------------------

def low_priority_kwargs():
    """subprocess kwargs that keep a render from freezing the member's laptop."""
    if IS_WIN:
        return {"creationflags": getattr(subprocess, "BELOW_NORMAL_PRIORITY_CLASS", 0)}
    return {"preexec_fn": lambda: os.nice(NICE)}


def run(cmd, check=True, low=True, capture=False, text=True, **kw):
    """subprocess.run with low priority by default. `cmd` is a list; paths are stringified."""
    cmd = [str(c) for c in cmd]
    kwargs = dict(kw)
    if low:
        kwargs.update(low_priority_kwargs())
    if capture:
        kwargs.setdefault("capture_output", True)
    return subprocess.run(cmd, check=check, text=text, **kwargs)


def out(cmd, **kw):
    """stdout of a command (stripped), at normal priority."""
    return run(cmd, low=False, capture=True, **kw).stdout.strip()


def probe_duration(path) -> float:
    return float(out([ffprobe(), "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", path]))


def probe_height(path) -> int:
    return int(out([ffprobe(), "-v", "error", "-select_streams", "v:0", "-show_entries", "stream=height", "-of", "csv=p=0", path]))


def video_encoder(bitrate=None, maxrate=None, crf=None, preset="medium"):
    """ffmpeg video codec args: Apple's hardware encoder on a Mac (fast, quiet), libx264 everywhere else."""
    if IS_MAC and tool("ffmpeg") and "videotoolbox" in (out([ffmpeg(), "-hide_banner", "-encoders"]) or ""):
        args = ["-c:v", "h264_videotoolbox", "-profile:v", "high"]
        if bitrate:
            args += ["-b:v", bitrate, "-maxrate", maxrate or bitrate, "-bufsize", maxrate or bitrate]
        return args
    args = ["-c:v", "libx264", "-preset", preset]
    if crf is not None:
        args += ["-crf", str(crf)]
    elif bitrate:
        args += ["-b:v", bitrate, "-maxrate", maxrate or bitrate, "-bufsize", maxrate or bitrate]
    return args


def free_gb(path=None) -> int:
    p = Path(path or Path.home())
    while not p.exists():
        p = p.parent
    return int(shutil.disk_usage(p).free / 1024 ** 3)


def open_path(path_or_url):
    import webbrowser
    target = str(path_or_url)
    if "://" not in target:
        target = Path(target).resolve().as_uri()
    webbrowser.open(target)


def stamp(reel, tag):
    """Append '<unix-seconds> <tag>' to <reel>/timings.log (render stages)."""
    import time
    with open(Path(reel) / "timings.log", "a", encoding="utf-8") as fh:
        fh.write(f"{int(time.time())} {tag}\n")


def link_or_copy(src, dst):
    """Hard link when the filesystem allows it (no second copy of a big video), else copy."""
    try:
        os.link(src, dst)
    except OSError:
        shutil.copy(src, dst)


def utf8_console():
    """Make stdout/stderr UTF-8 so ✅/➖ and non-ASCII names print on a Windows console (cp1252 would raise)."""
    for stream in (sys.stdout, sys.stderr):
        try:
            stream.reconfigure(encoding="utf-8", errors="replace")
        except (AttributeError, ValueError):
            pass
