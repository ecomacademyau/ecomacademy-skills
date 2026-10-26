#!/usr/bin/env python3
"""Split brand-data.md into its numbered sections and fingerprint it — the input for the EcomOS `sync_brand` tool.

Usage:
  python3 brand_sections.py [brand-data.md]              → JSON {path, sha256, brandName, sections: {"1": "…", …}}
  python3 brand_sections.py --path-only                  → just the resolved path of the brand file
  python3 brand_sections.py --payload brand-sync.json    → the complete `sync_brand` arguments:
                                                            {brand, sections, sourcePath, sourceHash}, after checking
                                                            brand-sync.json against references/brand-sync-schema.json
                                                            (missing brandName → exit 2; overlong strings/arrays are
                                                            clipped with a warning so one long list never blocks a sync)

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


def main(argv):
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
        print(json.dumps({"brand": brand, "sections": d["sections"], "sourcePath": d["path"], "sourceHash": d["sha256"]}, ensure_ascii=False))
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
