#!/usr/bin/env python3
"""Split brand-data.md into its numbered sections and fingerprint it — the input for the EcomOS `sync_brand` tool.

Usage:
  python3 brand_sections.py [brand-data.md]              → JSON {path, sha256, brandName, sections: {"1": "…", …}}
  python3 brand_sections.py --path-only                  → just the resolved path of the brand file
  python3 brand_sections.py --payload brand-sync.json    → the complete `sync_brand` arguments
                                                            {brand, sourcePath, sourceHash} (+ sections with --with-sections),
                                                            after checking brand-sync.json against references/brand-sync-schema.json
                                                            (missing brandName → exit 2; overlong strings/arrays are
                                                            clipped with a warning so one long list never blocks a sync)
  python3 brand_sections.py --gaps brand-sync.json       → what is still missing or unconfirmed, as a checklist:
                                                            structured fields the apps need that are empty, plus every
                                                            section of brand-data.md that still says TBD / [PLACEHOLDER].
                                                            Exit 0 = complete, 3 = gaps to fill before syncing.

The brand file is found per references/brand-file-location.md:
  $ECA_BRAND_FILE → ./brand/brand-data.md → ./brand-data.md → ./skills/*/brand-data.md → the plugin folder (read-only).
Works on macOS, Windows and Linux (pathlib only, no shell).
"""
import glob, hashlib, json, os, re, sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
SKILL = HERE.parent
SCHEMA = SKILL / "references" / "brand-sync-schema.json"


def resolve_brand_file(explicit=None):
    """First existing brand file in the documented order; (path, source) or (None, None)."""
    if explicit:
        p = Path(explicit).expanduser()
        return (p.resolve(), "argument") if p.exists() else (None, None)
    env = os.environ.get("ECA_BRAND_FILE")
    if env and Path(env).expanduser().exists():
        return Path(env).expanduser().resolve(), "ECA_BRAND_FILE"
    cwd = Path.cwd()
    for rel, src in (("brand/brand-data.md", "working folder (./brand/)"), ("brand-data.md", "working folder")):
        if (cwd / rel).exists():
            return (cwd / rel).resolve(), src
    for hit in sorted(glob.glob(str(cwd / "skills" / "*" / "brand-data.md"))):
        return Path(hit).resolve(), "skills folder (legacy layout)"
    legacy = SKILL / "brand-data.md"
    if legacy.exists() and not _is_template(legacy):
        return legacy.resolve(), "plugin folder (legacy, read-only)"
    return None, None


def _is_template(path):
    try:
        head = path.read_text(encoding="utf-8", errors="replace")[:4000]
    except OSError:
        return True
    return "[BRAND NAME]" in head or head.count("[PLACEHOLDER") > 2 or "TBD" in head[:600] and "Brand: [" in head


def split_sections(text):
    """{'1': '## 1. Brand essence\\n…', …}; anything before the first numbered heading is '0'."""
    out, key, buf = {}, "0", []
    for line in text.splitlines(keepends=True):
        m = re.match(r"^## +(\d+)\.", line)
        if m:
            if buf:
                out[key] = "".join(buf).rstrip() + "\n"
            key, buf = m.group(1), [line]
        else:
            buf.append(line)
    if buf:
        out[key] = "".join(buf).rstrip() + "\n"
    return out


def brand_name(text):
    m = re.search(r"^# +Brand:\s*(.+?)\s*$", text, re.M)
    return m.group(1).strip() if m else None


def describe(path):
    text = path.read_text(encoding="utf-8")
    return {
        "path": str(path),
        "sha256": hashlib.sha256(text.encode("utf-8")).hexdigest(),
        "brandName": brand_name(text),
        "sections": split_sections(text),
    }


# ---- light schema check (no third-party deps; the server validates for real) -------------------------------------

def _clip(value, schema, where, warnings):
    t = schema.get("type")
    if isinstance(value, str) and schema.get("maxLength") and len(value) > schema["maxLength"]:
        warnings.append(f"{where}: clipped to {schema['maxLength']} chars")
        return value[: schema["maxLength"] - 1].rstrip() + "…"
    if isinstance(value, list) and t == "array":
        if schema.get("maxItems") and len(value) > schema["maxItems"]:
            warnings.append(f"{where}: kept the first {schema['maxItems']} of {len(value)} items")
            value = value[: schema["maxItems"]]
        item_schema = schema.get("items", {})
        return [_clip(v, item_schema, f"{where}[{i}]", warnings) for i, v in enumerate(value)]
    if isinstance(value, dict) and t == "object":
        props = schema.get("properties", {})
        cleaned = {}
        for k, v in value.items():
            if k in props:
                if v is None:
                    continue
                cleaned[k] = _clip(v, props[k], f"{where}.{k}", warnings)
            elif schema.get("additionalProperties") not in (None, False):
                cleaned[k] = v
            else:
                warnings.append(f"{where}.{k}: not in the schema, dropped")
        for req in schema.get("required", []):
            if req not in cleaned:
                raise ValueError(f"{where}.{req} is required")
        return cleaned
    if "enum" in schema and value not in schema["enum"]:
        raise ValueError(f"{where}: {value!r} is not one of {schema['enum']}")
    if t == "number" and isinstance(value, str):
        try:
            return float(value.replace("$", "").replace(",", ""))
        except ValueError:
            raise ValueError(f"{where}: expected a number, got {value!r}")
    return value


def check_payload(brand):
    schema = json.loads(SCHEMA.read_text(encoding="utf-8")) if SCHEMA.exists() else {"type": "object", "required": ["brandName"], "additionalProperties": True}
    warnings = []
    cleaned = _clip(brand, schema, "brand", warnings)
    return cleaned, warnings


# Fields the Marketing Apps and the reel editor actually read. (path, label, section of brand-data.md, why it matters)
REQUIRED = [
    ("tagline", "tagline", "§4 / §1", "Brand Profile header, end cards"),
    ("essence.oneLiner", "one-liner", "§1", "every prompt opens with it"),
    ("voice.tone", "tone words", "§3", "copy voice in chat, Offer Builder, Prompt Generator"),
    ("visual.colors.accent", "accent / brand colour (hex)", "§4", "reel captions, price pills, swatches"),
    ("visual.colors.ink", "ink / text colour (hex)", "§4", "reel titles and cards"),
    ("visual.colors.light", "light / background colour (hex)", "§4", "reel end card"),
    ("visual.fonts.heading", "heading font", "§4", "reel titles"),
    ("visual.logoUrl", "logo URL", "§4", "Brand Profile card"),
    ("pillars", "messaging pillars with hooks (3+)", "§5", "Hook Library, ad hooks"),
    ("products", "products with prices (hero marked)", "§6", "product cards, Offer Builder"),
    ("offer.cta", "usual call to action", "§7", "reel end card, ads"),
    ("offer.guarantee", "guarantee / risk reversal", "§7 / §8", "ads, landing pages"),
    ("proof.rating", "review rating", "§8", "review card"),
    ("proof.reviewCount", "review count", "§8", "review card"),
    ("proof.quotes", "customer quotes (2+)", "§8", "review card, ads"),
    ("objections", "objections with rebuttals (3+)", "§9", "ads, Offer Builder"),
    ("personas", "personas (1+)", "§12", "chat, Prompt Generator, 4PI"),
    ("claimsToAvoid", "claims to avoid", "§6 / §15", "every copy prompt"),
    ("market.category", "category", "§10", "Google Spend brand split context"),
]
MINIMUMS = {"pillars": 3, "proof.quotes": 2, "objections": 3, "products": 1, "personas": 1, "voice.tone": 1, "claimsToAvoid": 1}


def _get(d, path):
    for k in path.split("."):
        if not isinstance(d, dict) or k not in d:
            return None
        d = d[k]
    return d


def gaps(brand, text):
    missing = []
    for path, label, section, why in REQUIRED:
        v = _get(brand, path)
        empty = v in (None, "", [], {}) or (isinstance(v, list) and len(v) < MINIMUMS.get(path, 1))
        if path == "products" and not empty:
            if not any(isinstance(p, dict) and p.get("price") not in (None, "") for p in v):
                missing.append((path, "product prices", section, why)); continue
            if not any(isinstance(p, dict) and p.get("role") == "hero" for p in v):
                missing.append((path, "which product is the hero", section, why)); continue
        if path == "pillars" and not empty and not any(isinstance(p, dict) and p.get("hook") for p in v):
            missing.append((path, "hook lines on the pillars", section, why)); continue
        if empty:
            missing.append((path, label, section, why))
    tbd = []
    for num, body in split_sections(text).items():
        n = len(re.findall(r"\bTBD\b|\[PLACEHOLDER|\[[A-Z][A-Za-z /]+\]|to be confirmed|needs (founder )?sign-off", body))
        if n:
            title = (re.match(r"^## +\d+\.\s*(.+)$", body, re.M) or [None, "preamble"])[1]
            tbd.append((num, title.strip(), n))
    return missing, tbd


def main(argv):
    if "--gaps" in argv:
        payload_path = Path(argv[argv.index("--gaps") + 1])
        p, src = resolve_brand_file()
        if not p:
            sys.exit("no brand-data.md found — run brand-intelligence Mode A first")
        text = p.read_text(encoding="utf-8")
        brand = json.loads(payload_path.read_text(encoding="utf-8"))
        missing, tbd = gaps(brand, text)
        if not missing and not tbd:
            print("COMPLETE: every field the apps use is filled and no section says TBD."); return
        if missing:
            print("MISSING (the apps read these — fill before syncing):")
            for path, label, section, why in missing:
                print(f"  - {label}  [{section}; used by: {why}]")
        if tbd:
            print("UNCONFIRMED in brand-data.md (TBD / placeholder / to-be-confirmed):")
            for num, title, n in tbd:
                print(f"  - §{num} {title}: {n} item(s)")
        sys.exit(3)

    if "--path-only" in argv:
        p, src = resolve_brand_file()
        if not p:
            sys.exit("no brand-data.md found (see references/brand-file-location.md) — run brand-intelligence Mode A first")
        print(p)
        return
    if "--payload" in argv:
        payload_path = Path(argv[argv.index("--payload") + 1])
        explicit = next((a for a in argv[1:] if not a.startswith("--") and a != str(payload_path)), None)
        p, src = resolve_brand_file(explicit)
        if not p:
            sys.exit("no brand-data.md found — run brand-intelligence Mode A first")
        d = describe(p)
        try:
            brand, warnings = check_payload(json.loads(payload_path.read_text(encoding="utf-8")))
        except ValueError as e:
            print(f"brand-sync.json: {e}", file=sys.stderr)
            sys.exit(2)
        for w in warnings:
            print("note:", w, file=sys.stderr)
        out = {"brand": brand, "sourcePath": d["path"], "sourceHash": d["sha256"]}
        if "--with-sections" in argv:   # the raw markdown is optional (nothing in EcomOS shows it yet) and makes the tool call ~40 KB
            out["sections"] = d["sections"]
        print(json.dumps(out, ensure_ascii=False))
        return
    explicit = next((a for a in argv[1:] if not a.startswith("--")), None)
    p, src = resolve_brand_file(explicit)
    if not p:
        sys.exit("no brand-data.md found (see references/brand-file-location.md) — run brand-intelligence Mode A first")
    d = describe(p)
    d["foundVia"] = src
    print(json.dumps(d, ensure_ascii=False))


if __name__ == "__main__":
    main(sys.argv)
