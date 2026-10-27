#!/usr/bin/env python3
"""Get a font file for the brand's named family, so captions and titles render in the brand font.

Order: ./brand/fonts/ (anything the member dropped in: .ttf/.otf/.woff2/.woff whose name contains the family),
then Google Fonts (free; downloads the TTF for the weight into ./brand/fonts/), else nothing (the template falls back
to a clean system font and says so).

Usage: python3 fetch_font.py "<Family>" [weight] [--fonts-dir ./brand/fonts]   → prints the file path, or nothing (exit 1)
"""
import re, sys, urllib.error, urllib.request
from pathlib import Path

# An old desktop UA makes Google Fonts answer with TTF urls instead of woff2.
UA = "Mozilla/5.0 (Windows NT 6.1; WOW64; rv:27.0) Gecko/20100101 Firefox/27.0"


def slug(s):
    return re.sub(r"[^a-z0-9]", "", s.lower())


def local(family, weight, fonts_dir):
    want = slug(family)
    if not fonts_dir.exists():
        return None
    cands = [p for p in fonts_dir.iterdir() if p.suffix.lower() in (".ttf", ".otf", ".woff2", ".woff") and want and want in slug(p.stem)]
    if not cands:
        return None
    # prefer a weight match ("Bold"/700, "Medium"/500, "Regular"/400), then ttf/otf over woff
    names = {700: ("bold", "700"), 500: ("medium", "500"), 400: ("regular", "400", "book"), 600: ("semibold", "600"), 800: ("extrabold", "800")}
    def score(p):
        s = slug(p.stem)
        return (any(t in s for t in names.get(int(weight), ())), p.suffix.lower() in (".ttf", ".otf"))
    return sorted(cands, key=score, reverse=True)[0]


def google(family, weight, fonts_dir):
    url = f"https://fonts.googleapis.com/css2?family={urllib.request.quote(family)}:wght@{weight}&display=swap"
    try:
        req = urllib.request.Request(url, headers={"User-Agent": UA})
        css = urllib.request.urlopen(req, timeout=30).read().decode("utf-8", "replace")
    except (urllib.error.URLError, OSError):
        return None
    # Google answers this UA with .ttf or .woff depending on the family; both work in the template (@font-face format map)
    m = re.search(r"url\((https://fonts\.gstatic\.com/[^)]+\.(ttf|otf|woff2|woff))\)", css)
    if not m:
        return None
    fonts_dir.mkdir(parents=True, exist_ok=True)
    dst = fonts_dir / f"{family.replace(' ', '')}-{weight}.{m.group(2)}"
    try:
        data = urllib.request.urlopen(urllib.request.Request(m.group(1), headers={"User-Agent": UA}), timeout=60).read()
    except (urllib.error.URLError, OSError):
        return None
    dst.write_bytes(data)
    return dst


def fetch(family, weight=700, fonts_dir=None):
    fonts_dir = Path(fonts_dir or Path.cwd() / "brand" / "fonts")
    return local(family, weight, fonts_dir) or google(family, weight, fonts_dir)


if __name__ == "__main__":
    args = [a for a in sys.argv[1:] if not a.startswith("--")]
    fd = sys.argv[sys.argv.index("--fonts-dir") + 1] if "--fonts-dir" in sys.argv else None
    if not args:
        sys.exit(__doc__)
    p = fetch(args[0], int(args[1]) if len(args) > 1 else 700, fd)
    if p:
        print(p)
    else:
        print(f"no font file for {args[0]!r} (not in ./brand/fonts, not on Google Fonts) — a system font will be used", file=sys.stderr)
        sys.exit(1)
