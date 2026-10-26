#!/usr/bin/env python3
"""Screenshot a website for a "shot" card (e.g. the homepage of a tool you mention). ~5-10 s.
Usage: python3 screenshot.py <url> <out.png>
Exit 1: no browser found. Exit 2: the site answered with a blank/blocked page (the file is deleted)."""
import os, shutil, statistics, subprocess, sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import common


def find_browser():
    cands = []
    if common.IS_MAC:
        cands += ["/Applications/Google Chrome.app/Contents/MacOS/Google Chrome",
                  "/Applications/Chromium.app/Contents/MacOS/Chromium",
                  "/Applications/Microsoft Edge.app/Contents/MacOS/Microsoft Edge"]
    elif common.IS_WIN:
        pf, pf86, local = (os.environ.get(k, "") for k in ("ProgramFiles", "ProgramFiles(x86)", "LocalAppData"))
        cands += [os.path.join(pf, r"Google\Chrome\Application\chrome.exe"),
                  os.path.join(pf86, r"Google\Chrome\Application\chrome.exe"),
                  os.path.join(local, r"Google\Chrome\Application\chrome.exe"),
                  os.path.join(pf86, r"Microsoft\Edge\Application\msedge.exe"),
                  os.path.join(pf, r"Microsoft\Edge\Application\msedge.exe"),
                  os.path.join(local, r"Chromium\Application\chrome.exe")]
    cands += [shutil.which(n) for n in ("google-chrome", "google-chrome-stable", "chromium", "chromium-browser", "chrome", "msedge")]
    for c in cands:
        if c and Path(c).is_file() and os.access(c, os.X_OK):
            return c
    return None


def main():
    common.utf8_console()
    if len(sys.argv) < 3:
        sys.exit(__doc__)
    url, out = sys.argv[1], Path(sys.argv[2]).expanduser()
    ch = find_browser()
    if not ch:
        print("no Chrome/Chromium/Edge found - install Chrome, or use your own screenshot", file=sys.stderr)
        sys.exit(1)
    out.parent.mkdir(parents=True, exist_ok=True)
    common.run([ch, "--headless=new", "--disable-gpu", "--hide-scrollbars", "--window-size=1280,900",
                f"--screenshot={out}", url], check=False, low=False, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    if not out.exists():
        print(f"screenshot failed: {ch} wrote nothing for {url}", file=sys.stderr)
        sys.exit(1)
    # Some sites (claude.ai, anything behind Cloudflare) answer bots with a blank "verifying you are human" page.
    # Flag near-uniform screenshots so they never land in a reel.
    raw = common.run([common.ffmpeg(), "-v", "error", "-i", out, "-vf", "scale=48:32,format=gray", "-f", "rawvideo", "-"],
                     low=False, capture=True, text=False).stdout
    std = int(statistics.pstdev(raw)) if raw else 0
    if std < 14:
        print(f"blocked or blank screenshot (contrast {std}): try the tool's marketing site, or take the screenshot yourself", file=sys.stderr)
        out.unlink(missing_ok=True)
        sys.exit(2)
    print(out)


if __name__ == "__main__":
    main()
