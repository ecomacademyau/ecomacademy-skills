#!/usr/bin/env python3
"""Keep the working copy of the brand (brand-data.md) in step with EcomOS.

EcomOS is the source of truth. The file is a copy: an edit made in the file is a change proposed to
EcomOS (UPLOAD), and whenever the two disagree EcomOS stands.

Saving to EcomOS (one `put_context` call per section; see references/ecomos-sync.md):
  python3 brand_sections.py --plan --remote "voice=3,products=2" --business "<name from ping>" [--adopt local|ecomos]
                                                          → what to do for every section, one line each:
                                                            UPLOAD (send it) · PULL (EcomOS is newer, copy it into the
                                                            file) · CONFLICT (changed in both) · ASK (this copy was never
                                                            linked to what EcomOS holds) · GONE (deleted in EcomOS) · OK.
                                                            --remote takes the key=version pairs `list_context` printed
                                                            ("none" when it lists no sections). --business is the business
                                                            name `ping` returned: a copy last saved to a different business
                                                            is refused (exit 6). Exit 0 = nothing to do, 5 = work listed.
  python3 brand_sections.py --section voice               → the exact text to send as `content` for that key
  python3 brand_sections.py --record voice=4 products=3 --business "<name>"
                                                          → after a successful put_context (or after copying a pulled
                                                            section into the file): remember the EcomOS version next to
                                                            the file's current text, in .ecomos-sync.json beside the file.
                                                            `key=gone` records that the member deleted that section in
                                                            EcomOS, so it is no longer part of the brand.
  python3 brand_sections.py --backup                      → copy the brand file to brand-data.before-ecomos-<date>.md beside
                                                            it, before EcomOS replaces sections of it

The structured brand for the Marketing Apps (`sync_brand`):
  python3 brand_sections.py --payload brand-sync.json    → the complete `sync_brand` arguments
                                                            {brand, sourcePath, sourceHash},
                                                            after checking brand-sync.json against references/brand-sync-schema.json
                                                            (missing brandName → exit 2; overlong strings/arrays are
                                                            clipped with a warning so one long list never blocks a sync)
  python3 brand_sections.py --gaps brand-sync.json       → what is still missing or unconfirmed, as a checklist:
                                                            structured fields the apps need that are empty, plus every
                                                            section of brand-data.md that still says TBD / [PLACEHOLDER].
                                                            Ends with VERDICT: COMPLETE (exit 0) · PATCH (exit 3: fill the
                                                            few gaps at sync time) · REBUILD (exit 4: run Mode A refresh first).

Also:
  python3 brand_sections.py [brand-data.md]              → JSON {path, sha256, brandName, sections: {"1": "…", …}} (large)
  python3 brand_sections.py --path-only                  → just the resolved path of the brand file

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
    if env:
        print(f"warning: $ECA_BRAND_FILE points at {env}, which does not exist; looking in the working folder instead", file=sys.stderr)
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
    return ("[BRAND NAME]" in head or "[YOUR BRAND NAME]" in head or "NOT YET CONFIGURED" in head
            or head.count("[PLACEHOLDER") > 2 or "TBD" in head[:600] and "Brand: [" in head)


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


def _read(path):
    """The file's text without a byte-order mark (EcomOS strips it, and a BOM hides the "# Brand:" line)."""
    return path.read_text(encoding="utf-8-sig")


def describe(path):
    text = _read(path)
    return {
        "path": str(path),
        "sha256": hashlib.sha256(text.encode("utf-8")).hexdigest(),
        "brandName": brand_name(text),
        "sections": split_sections(text),
    }


# ---- EcomOS context sections: which key each part of the file is saved under, and what has changed ----------------

# "## N." in brand-data.md → the section key in EcomOS. Fixed: every ECA skill asks for these keys by name.
SECTION_KEYS = {
    1: "brand-essence", 2: "why-people-buy", 3: "voice", 4: "visual", 5: "messaging", 6: "products",
    7: "offer", 8: "proof", 9: "objections", 10: "market", 11: "competitors", 12: "personas",
    13: "operations", 14: "promo-calendar", 15: "seo", 16: "boilerplate", 17: "channels",
    18: "sources", 19: "open-questions",
}
OVERVIEW_KEY = "brand-overview"        # everything above "## 1." (name, URL, last updated, strategic direction)
REPORT_KEY = "market-research"         # market-research-report.md beside the brand file
REPORT_FILES = ("market-research-report.md", "market-research.md")
BRAND_KEYS = set(SECTION_KEYS.values()) | {OVERVIEW_KEY, REPORT_KEY}
MAX_SECTION_CHARS = 60000              # the EcomOS limit for one section (JavaScript string length)


def canonical(text):
    """The text exactly as it is sent and stored: LF line endings, no trailing spaces, trimmed (EcomOS trims too)."""
    text = text.replace("﻿", "")
    return "\n".join(line.rstrip() for line in text.replace("\r\n", "\n").replace("\r", "\n").split("\n")).strip()


def _units(text):
    """Length the way EcomOS (JavaScript) counts it."""
    return len(text.encode("utf-16-le")) // 2


def _tokens(text):
    """EcomOS reports a section's size as ceil(length / 4); mirror it so the two numbers compare exactly."""
    return -(-_units(text) // 4)


def _sha(text):
    return hashlib.sha256(text.encode("utf-8")).hexdigest()[:16]


def context_sections(path):
    """([{key, label, title, content}], skipped) for the overview, each numbered section, and the research report."""
    out, skipped = [], []
    for num, body in split_sections(_read(path)).items():
        content = canonical(body)
        if not content:
            continue
        if num == "0":
            out.append({"key": OVERVIEW_KEY, "label": "overview", "title": "Brand overview", "content": content})
            continue
        key = SECTION_KEYS.get(int(num))
        if not key:
            skipped.append(f"§{num}")
            continue
        title = (re.match(r"^## +\d+\.\s*(.+)$", content, re.M) or [None, key])[1].strip()
        out.append({"key": key, "label": f"§{num}", "title": title, "content": content})
    for name in REPORT_FILES:
        report = path.parent / name
        if report.exists():
            content = canonical(_read(report))
            if content:
                out.append({"key": REPORT_KEY, "label": name, "title": "Market research report", "content": content})
            break
    return out, skipped


def _state_path(path):
    """One record per brand file, so two brand files in one folder never share versions."""
    return path.parent / (".ecomos-sync.json" if path.name == "brand-data.md" else f".ecomos-sync.{path.stem}.json")


def load_state(path):
    """{"business": name|None, "sections": {key: {sha, version} | {sha, gone: True}}}; anything unreadable is dropped."""
    try:
        data = json.loads(_state_path(path).read_text(encoding="utf-8"))
    except (OSError, ValueError):
        data = {}
    if not isinstance(data, dict):
        data = {}
    sections = {}
    for key, v in (data.get("sections") or {}).items() if isinstance(data.get("sections"), dict) else []:
        if isinstance(v, dict) and isinstance(v.get("sha"), str) and (isinstance(v.get("version"), int) or v.get("gone") is True):
            sections[key] = v
    business = data.get("business") if isinstance(data.get("business"), str) else None
    return {"business": business, "sections": sections}


def save_state(path, state):
    _state_path(path).write_text(json.dumps({
        "note": "Written by brand_sections.py: which EcomOS business this brand file is saved to and which version each section matches. Safe to delete: the next plan then asks which copy is current.",
        "business": state.get("business"),
        "sections": state["sections"],
    }, indent=2, sort_keys=True, ensure_ascii=False) + "\n", encoding="utf-8")


def parse_pairs(items, what, allow_gone=False):
    """["voice=3,products=2", "offer=1"] → {"voice": 3, "products": 2, "offer": 1}; "v3" is accepted for 3."""
    out = {}
    for chunk in items:
        for pair in re.split(r"[,\s]+", chunk.strip()):
            if not pair or pair.lower() == "none":
                continue
            m = re.match(r"^([a-z0-9][a-z0-9-]*)=(?:v?(\d+)|(gone))$", pair)
            if not m or (m.group(3) and not allow_gone):
                sys.exit(f"{what}: expected key=version (e.g. voice=3), got {pair!r}")
            out[m.group(1)] = "gone" if m.group(3) else int(m.group(2))
    return out


def _same_business(a, b):
    return re.sub(r"\s+", " ", a).strip().lower() == re.sub(r"\s+", " ", b).strip().lower()


def plan(path, remote=None, adopt=None):
    """(rows, notes). One action per section. `remote` is {key: version} from list_context, or None when not given."""
    state = load_state(path)["sections"]
    local, skipped = context_sections(path)
    notes = []
    if skipped:
        notes.append(f"Not saved: {', '.join(skipped)} — only the overview, sections 1-19 and the research report have a key in EcomOS.")
    if remote is None:
        notes.append("No --remote given: only changes made in the file are listed. Pass the key=version pairs from list_context to also catch edits made in EcomOS.")
    elif state and not any(k in BRAND_KEYS for k in remote):
        notes.append("EcomOS holds none of this brand's sections, so the earlier save record does not apply to it (new business, or the store was cleared). Treating every section as new.")
        state = {}
    rows = []
    for s in local:
        key, known = s["key"], state.get(s["key"])
        here = _sha(s["content"])
        changed_here = not known or known.get("sha") != here
        there = remote.get(key) if remote is not None else None
        row = {**s, "tokens": _tokens(s["content"]), "chars": _units(s["content"])}
        if row["chars"] > MAX_SECTION_CHARS:
            row.update(action="TOO LONG", why=f"{row['chars']} characters; EcomOS takes {MAX_SECTION_CHARS} per section")
        elif known and known.get("gone"):
            if there is not None:
                row.update(action="CONFLICT", version=there, why=f"the member deleted this section in EcomOS and it is back at v{there} — often the short summary EcomOS makes from the structured brand, not their text. Read it before choosing")
            else:
                row.update(action="OK", why="deleted in EcomOS by the member; kept only in this copy")
        elif remote is None:
            if changed_here:
                row.update(action="UPLOAD", if_version=known["version"] if known else None,
                           why="changed in the file since the last upload" if known else "not uploaded from this copy yet")
            else:
                row.update(action="OK", why=f"matches EcomOS v{known['version']} as last seen")
        elif there is None and known:
            row.update(action="GONE", why=f"was in EcomOS at v{known['version']} and has been deleted there")
        elif there is None:
            row.update(action="UPLOAD", if_version=None, why="EcomOS does not have it")
        elif not known:
            if adopt == "local":
                row.update(action="UPLOAD", if_version=there, why=f"replaces what EcomOS holds (v{there})")
            elif adopt == "ecomos":
                row.update(action="PULL", version=there, why=f"EcomOS v{there} replaces this copy")
            else:
                row.update(action="ASK", version=there, why=f"EcomOS already holds v{there} and this copy has never been linked to it")
        elif there < known["version"]:
            row.update(action="CHECK", version=there, why=f"EcomOS shows v{there} but this copy last saw v{known['version']}; versions never go down, so the connection is probably on a different business than this file was saved to")
        else:
            changed_there = there != known["version"]
            if changed_here and changed_there:
                row.update(action="CONFLICT", version=there, why=f"edited in the file and in EcomOS (v{known['version']} → v{there})")
            elif changed_there:
                row.update(action="PULL", version=there, why=f"edited in EcomOS (v{known['version']} → v{there})")
            elif changed_here:
                row.update(action="UPLOAD", if_version=known["version"], why="changed in the file since the last upload")
            else:
                row.update(action="OK", why=f"matches EcomOS v{there}")
        rows.append(row)
    if remote is not None:
        have = {s["key"] for s in local}
        for key in sorted(k for k in remote if k in BRAND_KEYS and k not in have):
            rows.append({"key": key, "label": "-", "title": key, "action": "PULL", "version": remote[key],
                         "why": "in EcomOS, not in this copy"})
    return rows, notes


LEGEND = {
    "UPLOAD": "`--section <key>` prints the text; call put_context {key, title, content, summary, brief, ifVersion} with that text unchanged "
              "(always write summary and brief; leave ifVersion out when none is shown). The reply's tokens must equal the number above "
              "(different = the text was altered on the way: send it again). Then `--record <key>=<version from the reply>`.",
    "PULL": "get_context {keys:[key], depth:\"full\", maxTokens:30000}. If the section's heading in the reply says \"brief, full is N tok\" you did not get "
            "the whole text: do not use it. The reply drops the section's first heading line, so keep the one in the file (\"## N. Title\"; \"# Brand: …\" for "
            "brand-overview; the report's own title) and replace the text under it. A section the file lacks goes in at its number with its \"## N. Title\" "
            "line; a missing report becomes market-research-report.md beside the brand file. Then `--record <key>=<version>`.",
    "CONFLICT": "EcomOS stands. Read the EcomOS version (as for PULL) and tell the member in a few lines what their file says differently. If they want that change in "
                "their brand, apply it on top of the EcomOS text and save it (put_context with ifVersion=<EcomOS version>, then put the saved text in the file); "
                "otherwise PULL. Never upload the file's version over the EcomOS one.",
    "ASK": "this copy has never been linked to what EcomOS holds. If the brand is not saved in EcomOS yet (only the short summaries from an older sync), "
           "rerun with --adopt local. If the brand is saved there, EcomOS is the source of truth: run --backup, rerun with --adopt ecomos, and tell the member "
           "the file was refreshed from EcomOS and where the old copy is.",
    "GONE": "the member deleted it in EcomOS, so it is no longer part of the brand. `--record <key>=gone`, do not use that section, and say so in one line. "
            "Bring it back only if the member asks (put_context without ifVersion, then --record the version).",
    "CHECK": "stop. Call ping and compare the business with the brand in this file before saving or pulling anything.",
    "TOO LONG": "shorten the section in the file first (move detail out of the profile; split a long research report into the report and an appendix kept only in the folder).",
}


def print_plan(rows, notes, path):
    todo = [r for r in rows if r["action"] != "OK"]
    print(f"Brand file: {path}")
    for n in notes:
        print(f"note: {n}")
    if not todo:
        print("Nothing to do: every section matches.")
        return 0
    for r in rows:
        if r["action"] == "OK":
            continue
        head = f"{r['action']:<8} {r['key']:<16} {r['label']:<9}"
        if r["action"] == "UPLOAD":
            iv = "" if r.get("if_version") is None else f" ifVersion={r['if_version']}"
            print(f"{head} title=\"{r['title']}\"{iv} expect tokens={r['tokens']}  — {r['why']}")
        else:
            print(f"{head} — {r['why']}")
    ok = len(rows) - len(todo)
    if ok:
        print(f"OK       {ok} section(s) already match.")
    print()
    for kind in ("CHECK", "UPLOAD", "PULL", "CONFLICT", "ASK", "GONE", "TOO LONG"):
        if any(r["action"] == kind for r in todo):
            print(f"{kind:<8} → {LEGEND[kind]}")
    return 5


def check_business(path, business):
    """Exit 6 when this brand file was last saved to a different EcomOS business than the one connected now."""
    saved = load_state(path)["business"]
    if business and saved and not _same_business(saved, business):
        print(f"STOP: this brand file was last saved to the EcomOS business \"{saved}\", and the connection is on \"{business}\".\n"
              "Saving or pulling now would mix two brands. Ask the member which business this folder belongs to. If the connection is wrong, "
              "they reconnect EcomOS on the right business. If this folder really belongs to the connected business now, delete "
              f"{_state_path(path).name} beside the brand file and plan again.")
        sys.exit(6)


def backup(path):
    import datetime, shutil
    target = path.with_name(f"{path.stem}.before-ecomos-{datetime.date.today().isoformat()}{path.suffix}")
    n = 1
    while target.exists():
        n += 1
        target = path.with_name(f"{path.stem}.before-ecomos-{datetime.date.today().isoformat()}-{n}{path.suffix}")
    shutil.copy2(path, target)
    print(f"backed up to {target}")


def record(path, pairs, business=None):
    state = load_state(path)
    local = {s["key"]: s for s in context_sections(path)[0]}
    import datetime
    today = datetime.date.today().isoformat()
    for key, version in pairs.items():
        if key not in local:
            sys.exit(f"--record: no section '{key}' in {path.name} (keys: {', '.join(local)})")
        sha = _sha(local[key]["content"])
        state["sections"][key] = {"sha": sha, "gone": True, "at": today} if version == "gone" else {"sha": sha, "version": version, "at": today}
    if business:
        state["business"] = business
    save_state(path, state)
    print(f"recorded {', '.join(f'{k}={v}' if v == 'gone' else f'{k}=v{v}' for k, v in pairs.items())} in {_state_path(path)}")


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


APP_SECTIONS = {"1", "2", "3", "4", "5", "6", "7", "8", "9", "12"}   # sections the Marketing Apps / reel editor read
PATCH_MAX_MISSING = 4        # more missing app fields than this → REBUILD
PATCH_MAX_TBD_SECTIONS = 3   # more app-read sections still TBD than this → REBUILD
STALE_DAYS = 120             # a brand file older than this is re-researched, not patched


def file_age_days(text):
    import datetime
    m = re.search(r"\*\*Last updated:\*\*\s*(\d{4}-\d{2}-\d{2})", text) or re.search(r"Last updated:?\s*(\d{4}-\d{2}-\d{2})", text)
    if not m:
        return None
    try:
        return (datetime.date.today() - datetime.date.fromisoformat(m.group(1))).days
    except ValueError:
        return None


def verdict_for(missing, tbd, text):
    """COMPLETE / PATCH / REBUILD with the reasons, so the skill routes the member to the right amount of work."""
    app_tbd = [t for t in tbd if t[0] in APP_SECTIONS]
    age = file_age_days(text)
    reasons = []
    if not missing and not tbd:
        return "COMPLETE", reasons
    if len(missing) > PATCH_MAX_MISSING:
        reasons.append(f"{len(missing)} app fields missing (patch limit {PATCH_MAX_MISSING})")
    if len(app_tbd) > PATCH_MAX_TBD_SECTIONS:
        reasons.append(f"{len(app_tbd)} app-read sections still TBD (patch limit {PATCH_MAX_TBD_SECTIONS})")
    if age is not None and age > STALE_DAYS:
        reasons.append(f"file last updated {age} days ago (older than {STALE_DAYS})")
    if reasons:
        return "REBUILD", reasons
    reasons.append(f"{len(missing)} missing field(s), {len(app_tbd)} app-read section(s) with TBDs" + (f", {age} days old" if age is not None else ""))
    return "PATCH", reasons


def _values_after(argv, flag):
    """Everything after `flag` up to the next --option."""
    out = []
    for a in argv[argv.index(flag) + 1:]:
        if a.startswith("--"):
            break
        out.append(a)
    return out


def main(argv):
    for stream in (sys.stdout, sys.stderr):   # headings carry "→" and brand files carry anything; never die on a Windows code page
        try:
            stream.reconfigure(encoding="utf-8", errors="replace")
        except (AttributeError, ValueError):
            pass
    if "--plan" in argv or "--section" in argv or "--record" in argv or "--backup" in argv:
        env = os.environ.get("ECA_BRAND_FILE")
        if env and not Path(env).expanduser().exists():
            sys.exit(f"$ECA_BRAND_FILE points at {env}, which does not exist. Fix or unset it; refusing to guess another brand file.")
        p, src = resolve_brand_file()
        if not p:
            sys.exit("no brand-data.md found (see references/brand-file-location.md). With no working copy there is nothing to compare: EcomOS is the brand.")
        if src.startswith("plugin folder"):
            sys.exit(f"the only brand file is the legacy copy inside the plugin folder ({p}), which plugin updates replace. Copy it to ./brand/brand-data.md in the working folder first.")
        business = " ".join(_values_after(argv, "--business")).strip() or None if "--business" in argv else None
        if "--section" in argv:
            want = (_values_after(argv, "--section") or [""])[0]
            sections = context_sections(p)[0]
            hit = next((s for s in sections if s["key"] == want), None)
            if not hit:
                sys.exit(f"--section: no section '{want}' in {p.name} (keys: {', '.join(s['key'] for s in sections)})")
            sys.stdout.write(hit["content"] + "\n")
            return
        if "--backup" in argv:
            backup(p)
            return
        check_business(p, business)
        if "--record" in argv:
            pairs = parse_pairs(_values_after(argv, "--record"), "--record", allow_gone=True)
            if not pairs:
                sys.exit("--record: give key=version pairs, e.g. --record voice=4 products=3")
            record(p, pairs, business)
            return
        remote = parse_pairs(_values_after(argv, "--remote"), "--remote") if "--remote" in argv else None
        adopt = (_values_after(argv, "--adopt") or [None])[0] if "--adopt" in argv else None
        if adopt not in (None, "local", "ecomos"):
            sys.exit("--adopt takes local or ecomos")
        rows, notes = plan(p, remote, adopt)
        sys.exit(print_plan(rows, notes, p))

    if "--gaps" in argv:
        payload_path = Path(argv[argv.index("--gaps") + 1])
        p, src = resolve_brand_file()
        if not p:
            sys.exit("no brand-data.md found — run brand-intelligence Mode A first")
        text = _read(p)
        brand = json.loads(payload_path.read_text(encoding="utf-8"))
        missing, tbd = gaps(brand, text)
        verdict, reasons = verdict_for(missing, tbd, text)
        if verdict == "COMPLETE":
            print("VERDICT: COMPLETE — every field the apps use is filled and no section says TBD."); return
        if missing:
            print("MISSING (the apps read these):")
            for path, label, section, why in missing:
                print(f"  - {label}  [{section}; used by: {why}]")
        if tbd:
            print("UNCONFIRMED in brand-data.md (TBD / placeholder / to-be-confirmed):")
            for num, title, n in tbd:
                print(f"  - §{num} {title}: {n} item(s)")
        print(f"VERDICT: {verdict} — " + "; ".join(reasons))
        print("  PATCH   = fill these few items now (live store lookups, then one round of questions), write them into the file, sync."
              if verdict == "PATCH" else
              "  REBUILD = too thin or stale to patch at sync time: run brand-intelligence Mode A (refresh) first — research the gaps, Gate 1, Gate 2 — then sync.")
        sys.exit(3 if verdict == "PATCH" else 4)

    if "--path-only" in argv:
        p, src = resolve_brand_file()
        if not p:
            sys.exit("no brand-data.md found (see references/brand-file-location.md) — run brand-intelligence Mode A first")
        print(p)
        return
    if "--payload" in argv:
        at = argv.index("--payload") + 1
        payload_path = Path(argv[at])
        explicit = next((a for i, a in enumerate(argv) if i >= 1 and i != at and not a.startswith("--")), None)
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
        # Sections are not sent here: each is saved with its own put_context call (see --plan), which also carries its brief.
        out = {"brand": brand, "sourcePath": d["path"], "sourceHash": d["sha256"]}
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
