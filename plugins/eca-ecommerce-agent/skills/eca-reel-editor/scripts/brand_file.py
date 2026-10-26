"""Find and read the member's brand-data.md (the brand-intelligence file), and read/write its "Reel kit" block.

Resolution order (the same as eca-brand-intelligence/references/brand-file-location.md):
  $ECA_BRAND_FILE → ./brand/brand-data.md → ./brand-data.md → ./skills/*/brand-data.md → (none)
The plugin-folder fallback of brand-intelligence is deliberately not searched here: the reel editor is a separate
plugin and must never read or write inside another plugin's folder.

Reel kit: a fenced ```reel-kit JSON block at the end of "## 4. Visual identity" with the visual preferences the
reel editor asked for once (caption mode/case, highlight colour, graphics energy, sfx, pacing, CTA). This module
is the only thing that writes to brand-data.md, and it only ever touches that block.

Usage:  python3 brand_file.py path            → prints the resolved path
        python3 brand_file.py kit             → prints the reel-kit JSON (or {} when absent)
        python3 brand_file.py write-kit k.json → inserts/replaces the block in §4 (k.json = the answers)
"""
import glob, hashlib, json, os, re, sys
from pathlib import Path

KIT_FENCE = "reel-kit"
KIT_KEYS = ("captionMode", "captionCase", "highlightColor", "graphics", "sfx", "pacing", "cta")
# optional overrides stored in the same block when §4 had no usable palette / fonts
KIT_EXTRA = ("colors", "fonts")


def resolve(explicit=None):
    if explicit:
        p = Path(explicit).expanduser()
        return p.resolve() if p.exists() else None
    env = os.environ.get("ECA_BRAND_FILE")
    if env and Path(env).expanduser().exists():
        return Path(env).expanduser().resolve()
    cwd = Path.cwd()
    for rel in ("brand/brand-data.md", "brand-data.md"):
        if (cwd / rel).exists():
            return (cwd / rel).resolve()
    hits = sorted(glob.glob(str(cwd / "skills" / "*" / "brand-data.md")))
    return Path(hits[0]).resolve() if hits else None


def read(path):
    return Path(path).read_text(encoding="utf-8")


def sha256(text):
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def sections(text):
    """{'1': full text of '## 1. …' incl. heading, …}; the preamble is '0'."""
    out, key, buf = {}, "0", []
    for line in text.splitlines(keepends=True):
        m = re.match(r"^## +(\d+)\.", line)
        if m:
            if buf:
                out[key] = "".join(buf)
            key, buf = m.group(1), [line]
        else:
            buf.append(line)
    if buf:
        out[key] = "".join(buf)
    return out


def brand_name(text):
    m = re.search(r"^# +Brand:\s*(.+?)\s*$", text, re.M)
    return m.group(1).strip() if m else None


_KIT_RE = re.compile(r"```" + KIT_FENCE + r"[^\n]*\n(.*?)```", re.S)


def read_kit(text):
    m = _KIT_RE.search(text)
    if not m:
        return None
    try:
        kit = json.loads(m.group(1))
    except json.JSONDecodeError:
        return None
    return {k: v for k, v in kit.items() if v not in (None, "")}


def kit_gaps(kit):
    """Which reel-kit answers are still missing (CTA is optional when §7 has one, but we ask anyway — it is one question)."""
    kit = kit or {}
    return [k for k in KIT_KEYS if not kit.get(k)]


def write_kit(path, kit):
    """Insert or replace the reel-kit block at the end of §4. Returns the new file text's sha256."""
    path = Path(path)
    text = read(path)
    keep = {k: kit[k] for k in KIT_KEYS + KIT_EXTRA if kit.get(k)}
    block = "```" + KIT_FENCE + "\n" + json.dumps(keep, indent=2, ensure_ascii=False) + "\n```"
    if _KIT_RE.search(text):
        new = _KIT_RE.sub(lambda _m: block, text, count=1)
    else:
        secs = sections(text)
        if "4" not in secs:
            raise SystemExit("brand-data.md has no '## 4.' section — add the Visual identity section first")
        body = secs["4"].rstrip("\n")
        # keep a trailing '---' divider after the block, as the template does
        divider = ""
        m = re.search(r"\n-{3,}\s*$", body)
        if m:
            body, divider = body[: m.start()], "\n---"
        new_sec = body.rstrip() + "\n\n**Reel kit** (visual preferences for the ECA reel editor — edit here, then say \"Sync my brand to EcomOS\"):\n\n" + block + "\n" + divider + "\n\n"
        new = text.replace(secs["4"], new_sec, 1)
    path.write_text(new, encoding="utf-8")
    return sha256(new)


if __name__ == "__main__":
    cmd = sys.argv[1] if len(sys.argv) > 1 else "path"
    p = resolve()
    if cmd == "path":
        print(p or ""); sys.exit(0 if p else 1)
    if not p:
        sys.exit("no brand-data.md found: run the brand-intelligence skill first (it writes ./brand/brand-data.md)")
    if cmd == "kit":
        print(json.dumps(read_kit(read(p)) or {}, indent=2))
    elif cmd == "write-kit":
        kit = json.loads(Path(sys.argv[2]).read_text(encoding="utf-8"))
        print(write_kit(p, kit))
    else:
        sys.exit(__doc__)
