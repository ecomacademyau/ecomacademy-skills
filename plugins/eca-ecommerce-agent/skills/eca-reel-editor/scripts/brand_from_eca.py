#!/usr/bin/env python3
"""brand-data.md (the brand-intelligence file) → reels/brand.json + reels/reel-brief.md. No brand interview, ever.

Usage: python3 brand_from_eca.py [brand-data.md] [--home ./reels] [--force] [--kit kit.json] [--fonts-dir ./brand/fonts]

  brand.json     what the render scripts read (Nicola Pocock's shape: colors{main,pop,light,caption,caption_accent},
                 fonts{head,body,accent}, captions, pacing, graphics, sfx, deliver_dir, …) + ecommerce extras
  reel-brief.md  what Claude reads before proposing an edit: voice rules, top angles, proof, CTA, claims to avoid, hero products

Regenerates only when the brand file's hash changed (or --force). Exit codes:
  0  written / up to date      3  visual gaps → stdout has {"gaps": [...], "suggested": {...}}: ask the member the ≤6
                                   Reel-kit questions once, save the answers as kit.json, rerun with --kit kit.json
                                   (that writes the ```reel-kit block into §4 of brand-data.md, then builds brand.json)
Fonts: ./brand/fonts/ first, then Google Fonts (TTF download), else the template's system fallback.
"""
import json, re, sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import common, brand_file  # noqa: E402
from fetch_font import fetch as fetch_font  # noqa: E402

HEX = r"#[0-9A-Fa-f]{6}\b"


def arg(flag, default=None):
    return sys.argv[sys.argv.index(flag) + 1] if flag in sys.argv else default


def lum(h):
    r, g, b = (int(h[i:i + 2], 16) / 255 for i in (1, 3, 5))
    return 0.2126 * r + 0.7152 * g + 0.0722 * b


def sat(h):
    r, g, b = (int(h[i:i + 2], 16) / 255 for i in (1, 3, 5))
    mx, mn = max(r, g, b), min(r, g, b)
    return 0 if mx == 0 else (mx - mn) / mx


def colours(s4):
    """{primary, accent, light, ink} from the §4 palette lines ('- Brand red (primary accent): `#E31A1C`')."""
    pairs = []
    for line in s4.splitlines():
        for m in re.finditer(HEX, line):
            label = line[: m.start()].lower()
            pairs.append((label, m.group(0).upper()))
    if not pairs:
        return {}
    def pick(pattern, exclude=()):
        for label, h in pairs:
            if re.search(pattern, label) and h not in exclude:
                return h
        return None
    ink = pick(r"near-black|black|\bink\b|charcoal|text|dark|navy|headline")
    light = pick(r"cream|background|light|off-white|neutral|paper|\bwhite\b|page")
    accent = pick(r"accent|primary|pop|highlight|cta|button|brand (red|blue|green|orange|pink|purple|yellow)", exclude=(ink, light))
    rest = [h for _, h in pairs if h not in (ink, light, accent)]
    if not ink:
        ink = min((h for _, h in pairs), key=lum)
    if not light:
        light = max((h for _, h in pairs), key=lum)
    if not accent:
        accent = max(rest or [h for _, h in pairs if h not in (ink, light)] or [ink], key=sat)
    return {"primary": accent, "accent": accent, "light": light if lum(light) > 0.6 else "#FFFFFF", "ink": ink}


def font_family(s4, role_pattern):
    block = labelled(s4, "Typography", 8) or s4          # the Typography lines, not the palette ("Body text: #222222")
    for line in block.splitlines():
        if re.search(HEX, line) or re.search(r"body text|text colou?r", line, re.I):
            continue
        if re.search(role_pattern, line, re.I) and ":" in line:
            after = line.split(":", 1)[1]
            after = re.sub(r"\(.*?\)", "", after)
            after = after.replace("`", "").replace("'", "").replace('"', "").replace("*", "")
            first = re.split(r"[,;/]|\bfallback\b|\bwith\b|\bweights?\b|\bbold\b|\bregular\b", after, maxsplit=1)[0].strip(" .-–—")
            first = re.sub(r"^(font|typeface)\s*", "", first, flags=re.I).strip()
            if first and len(first) <= 40:
                return first
    return None


def subsection(text, heading_pattern):
    """Text of a '### heading' (or bold-label paragraph) up to the next heading of the same or higher level."""
    m = re.search(r"^(#{2,4}) +" + heading_pattern + r".*$", text, re.M | re.I)
    if not m:
        return ""
    level = len(m.group(1))
    rest = text[m.end():]
    nxt = re.search(r"^#{1,%d} +" % level, rest, re.M)
    return rest[: nxt.start()].strip() if nxt else rest.strip()


def labelled(text, label_pattern, max_lines=12):
    """Lines following a '**Label:**' line until a blank line or the next bold label."""
    m = re.search(r"^\*\*" + label_pattern + r"[^*]*\*\*:?\s*(.*)$", text, re.M | re.I)
    if not m:
        return ""
    out = [m.group(1).strip()] if m.group(1).strip() else []
    for line in text[m.end():].splitlines()[1:]:
        if not line.strip() or re.match(r"^\*\*[^*]+\*\*", line) or line.startswith("#"):
            break
        out.append(line.rstrip())
        if len(out) >= max_lines:
            break
    return "\n".join(out).strip()


def main():
    explicit = next((a for a in sys.argv[1:] if not a.startswith("--") and a not in (arg("--home"), arg("--kit"), arg("--fonts-dir"))), None)
    path = brand_file.resolve(explicit)
    if not path:
        sys.exit("no brand-data.md found — run the brand-intelligence skill first (it writes ./brand/brand-data.md).")
    home = Path(arg("--home") or common.reels_home()).expanduser().resolve()
    home.mkdir(parents=True, exist_ok=True)
    fonts_dir = Path(arg("--fonts-dir") or (path.parent / "fonts" if path.parent.name == "brand" else Path.cwd() / "brand" / "fonts"))

    if arg("--kit"):
        kit_in = json.loads(Path(arg("--kit")).read_text(encoding="utf-8"))
        brand_file.write_kit(path, kit_in)
        print(f"reel kit written into §4 of {path.name} — remember to sync the brand to EcomOS")

    text = brand_file.read(path)
    sha = brand_file.sha256(text)
    out_json = home / "brand.json"
    if out_json.exists() and "--force" not in sys.argv:
        try:
            if common.load_json(out_json).get("source_hash") == sha:
                print(f"brand.json up to date ({path.name} unchanged, {sha[:10]})")
                return
        except (OSError, ValueError):
            pass

    secs = brand_file.sections(text)
    name = brand_file.brand_name(text) or path.parent.parent.name
    s3, s4, s5, s6, s7, s8, s9, s15 = (secs.get(k, "") for k in ("3", "4", "5", "6", "7", "8", "9", "15"))
    kit = brand_file.read_kit(text) or {}
    col = {**colours(s4), **(kit.get("colors") or {})}
    head_family = (kit.get("fonts") or {}).get("heading") or font_family(s4, r"display|headline|heading")
    body_family = (kit.get("fonts") or {}).get("body") or font_family(s4, r"\bbody\b")

    gaps = brand_file.kit_gaps(kit)
    if not col.get("accent"):
        gaps.insert(0, "colors")
    if not head_family:
        gaps.insert(1 if "colors" in gaps else 0, "fonts")
    if gaps and not arg("--kit"):
        suggested = {
            "captionMode": "word", "captionCase": "lower", "highlightColor": col.get("accent", "#FF5A36"),
            "graphics": "balanced", "sfx": "subtle", "pacing": "natural",
            "cta": "",
            "colors": col, "fonts": {"heading": head_family, "body": body_family},
        }
        print(json.dumps({"gaps": gaps, "suggested": suggested, "brandFile": str(path)}, indent=2))
        sys.exit(3)

    # ---- fonts -------------------------------------------------------------------------------------------------
    def font_entry(family, weight, style=None):
        if not family:
            return None
        f = fetch_font(family, weight, fonts_dir)
        e = {"family": family, "weight": weight}
        if f:
            e["file"] = str(f)
        if style:
            e["style"] = style
        return e
    fonts = {}
    h = font_entry(head_family, 700)
    if h: fonts["head"] = h
    b = font_entry(body_family, 500) or font_entry(body_family, 400) or (dict(h, weight=500) if h else None)
    if b: fonts["body"] = b
    # accent = the emphasised caption word; an italic of the heading face reads as "the brand, leaning in"
    if h: fonts["accent"] = {**{k: v for k, v in h.items() if k != "file"}, "weight": 700, "style": "italic", **({"file": h["file"]} if h.get("file") else {})}

    # ---- ecommerce facts for the brief / cards ------------------------------------------------------------------
    hero = subsection(s6, r"hero product")
    hero_name = (re.search(r"^#{3,4} +Hero product\s*[—–-]\s*(.+?)\s*(\(|$)", s6, re.M | re.I) or [None, None])[1]
    hero_price = (re.search(r"\$(\d+(?:\.\d{1,2})?)", hero) or [None, None])[1]
    rating = (re.search(r"(\d\.\d)\s*(?:/\s*5|★|\*|stars)", s8) or [None, None])[1]
    count = (re.search(r"(\d{2,6})(?:\s*[–-]\s*\d{2,6})?\s*reviews", s8) or [None, None])[1]
    guarantee = (re.search(r"\*\*Guarantee[^*]*\*\*:?\s*(.+)", s8) or [None, ""])[1].strip()
    lean = labelled(s3, "Words (&|and) phrases we lean on")
    vocab = [name] + ([hero_name] if hero_name else []) + [w.strip(' "“”*') for w in re.split(r"[·•|]", lean) if 2 < len(w.strip(' "“”*')) < 30]
    vocab = list(dict.fromkeys(v for v in vocab if v))[:30]
    store_url = (re.search(r"\*\*Primary URL:\*\*\s*(\S+)", text) or [None, ""])[1]

    mode = kit.get("captionMode", "word")
    brand = {
        "name": name, "source_path": str(path), "source_hash": sha, "source": "brand-data.md via brand_from_eca.py",
        "resolution": [1080, 1920], "pacing": kit.get("pacing", "natural"), "graphics": kit.get("graphics", "balanced"), "max_seconds": 60,
        "colors": {"main": col.get("ink", "#171717"), "pop": col.get("accent", "#FF5A36"), "light": col.get("light", "#FFFFFF"),
                   "caption": "#FFFFFF", "caption_accent": kit.get("highlightColor") or col.get("accent", "#FF5A36"), "soft": col.get("accent", "#FF5A36")},
        "capcut": False, "capcut_font": None, "sfx": kit.get("sfx", "subtle"), "deliver_dir": str(home / "delivered"), "grade": None,
        "captions": {"mode": "word" if mode.startswith("word") else "phrase", "case": "lower" if str(kit.get("captionCase", "lower")).lower().startswith("low") else "sentence",
                     "size": 104 if mode.startswith("word") else 96, "y": 1250},
        "fonts": fonts, "cta": kit.get("cta", ""), "vocab": vocab, "store_url": store_url,
        "ecommerce": {"hero_product": {"name": hero_name, "price": float(hero_price) if hero_price else None},
                      "rating": float(rating) if rating else None, "review_count": int(count) if count else None, "guarantee": guarantee},
    }
    common.save_json(out_json, brand, indent=2)

    # ---- the brief Claude reads ---------------------------------------------------------------------------------
    pillars = re.findall(r"^\s*\d+\.\s+\*\*(.+?)\*\*.*?hook:\s*\*?[\"“]?(.+?)[\"”]?\*?\s*$", s5, re.M)
    hooks_line = labelled(s5, "Hooks")
    claims_avoid = subsection(s6, r"claims to avoid") or labelled(s6, "Claims to avoid")
    topics_avoid = labelled(s15, "Topics to avoid")
    never_visual = labelled(s4, "What to never do visually")
    objections = [l for l in s9.splitlines() if l.startswith("|") and not re.match(r"^\|\s*-", l) and "Objection" not in l][:5]
    brief = f"""# Reel brief — {name}
_Generated from {path.name} ({sha[:10]}) by brand_from_eca.py. Edit the brand file, not this._

## Voice (from §3)
{s3.split(chr(10), 1)[1].strip()[:3500] if chr(10) in s3 else s3[:3500]}

## Top angles (from §5) — lead with one of these
{chr(10).join(f"{i + 1}. **{p}** → hook: “{h.strip()}”" for i, (p, h) in enumerate(pillars[:3])) or s5[:1200]}
{('Hooks that work: ' + hooks_line) if hooks_line else ''}

## Proof you may show (from §8) — real numbers only
{s8.split(chr(10), 1)[1].strip()[:1800] if chr(10) in s8 else s8[:1800]}

## Hero product (from §6)
{(('**' + hero_name + '**' + chr(10)) if hero_name else '') + hero[:1200]}

## Objections to pre-empt (from §9)
{chr(10).join(objections)}

## Claims to avoid — never on a card or in a caption
{claims_avoid or '(none listed)'}
{('Topics to avoid: ' + topics_avoid) if topics_avoid else ''}

## Visual rules
- Never: {never_visual or '(none listed)'}
- Colours: ink {brand['colors']['main']} · pop {brand['colors']['pop']} · light {brand['colors']['light']} · caption highlight {brand['colors']['caption_accent']}
- Fonts: {', '.join(f"{r} = {f['family']}{' (file)' if f.get('file') else ' (system fallback)'}" for r, f in fonts.items()) or 'system fallback'}
- Captions: {brand['captions']['mode']} mode, {brand['captions']['case']} case · graphics {brand['graphics']} · sfx {brand['sfx']} · pacing {brand['pacing']}

## Call to action
{brand['cta'] or '(ask: what should the reel ask people to do?)'}
"""
    (home / "reel-brief.md").write_text(brief, encoding="utf-8")
    print(f"brand.json + reel-brief.md written to {home}")
    print(f"  colours: ink {brand['colors']['main']} · pop {brand['colors']['pop']} · light {brand['colors']['light']}")
    for r, f in fonts.items():
        print(f"  font {r}: {f['family']} {'← ' + f['file'] if f.get('file') else '(no file: system fallback)'}")
    print(f"  captions {brand['captions']['mode']}/{brand['captions']['case']} · graphics {brand['graphics']} · sfx {brand['sfx']} · pacing {brand['pacing']} · cta “{brand['cta']}”")


if __name__ == "__main__":
    main()
