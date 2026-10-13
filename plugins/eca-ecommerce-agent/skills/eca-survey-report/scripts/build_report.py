#!/usr/bin/env python3
"""Calculate, validate and build an ECA survey report.

Usage:
  python3 build_report.py <report-data.json> <output.html>

The data file holds raw counts only (shape in references/report-data-schema.md).
This script calculates every percentage and signal tag with signals.py,
derives the "what's new this period" list, checks the file, and renders
templates/report-template.html into one self-contained HTML file.

Exits with code 1 and a list of problems if any hard check fails.
"""
import html
import json
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from signals import pct, level, shift  # noqa: E402

ROOT = Path(__file__).resolve().parent.parent
TEMPLATE = ROOT / "templates" / "report-template.html"
MARK = ROOT / "assets" / "eca-mark.svg"
EXAMPLE = ROOT / "examples" / "example-report-data.json"

EM_DASH = "\u2014"
MOVE_WORDS = re.compile(r"\b(rose|rising|risen|fell|falling|fallen|improved|improving|worsened|worsening|jumped|surged|plunged|dropped|grew|growing|trending|spiked|doubled|halved)\b", re.I)
CHANNELS = {"Website", "Ads", "Content", "Email", "Product"}


def walk_strings(obj, path="$"):
    if isinstance(obj, str):
        yield path, obj
    elif isinstance(obj, dict):
        for k, v in obj.items():
            if k == "_":
                continue
            yield from walk_strings(v, f"{path}.{k}")
    elif isinstance(obj, list):
        for i, v in enumerate(obj):
            yield from walk_strings(v, f"{path}[{i}]")


class Build:
    def __init__(self, d):
        self.d = d
        self.errors, self.warnings = [], []
        self.shifts = []

    # ---------- enrichment ----------
    def question(self, q, where, short=None, collect_shifts=True):
        if not q:
            return
        n_all, n_per = q.get("n_all"), q.get("n_period")
        if not isinstance(n_all, int) or n_all <= 0:
            self.errors.append(f"{where}: n_all must be a positive whole number")
            return
        if n_per is not None and (not isinstance(n_per, int) or n_per < 0):
            self.errors.append(f"{where}: n_period must be a whole number")
            n_per = None
        rows = q.get("rows", [])
        if not rows:
            self.errors.append(f"{where}: no rows")
        tot_all = 0
        for i, r in enumerate(rows):
            for bad in ("pct", "all_pct", "period_pct", "tag", "signal"):
                if bad in r:
                    self.warnings.append(f"{where}.rows[{i}] had '{bad}' written by hand; ignored and recalculated")
            a = r.get("all")
            if not isinstance(a, int) or a < 0:
                self.errors.append(f"{where}.rows[{i}] '{r.get('label')}' needs an all-time count")
                continue
            if a > n_all:
                self.errors.append(f"{where}.rows[{i}] count {a} is larger than n_all {n_all}")
            tot_all += a
            info = {"all_pct": pct(a, n_all), "tag": level(a, n_all)}
            p = r.get("period")
            if p is not None and n_per:
                if p > a:
                    self.errors.append(f"{where}.rows[{i}] period count {p} is larger than its all-time count {a}")
                tag, delta = shift(p, n_per, a, n_all)
                info.update({"period_pct": pct(p, n_per), "shift": tag, "delta": delta})
                if collect_shifts and tag in ("Strong signal", "Early signal"):
                    self.shifts.append({"q": short or q.get("q", ""), "label": r.get("label", ""),
                                        "all_pct": info["all_pct"], "period_pct": info["period_pct"],
                                        "delta": delta, "tag": tag, "n_all": n_all, "n_period": n_per})
            r["_"] = info
        if q.get("type") == "single" and rows and tot_all and abs(tot_all - n_all) > max(2, 0.02 * n_all):
            self.warnings.append(f"{where}: single-select counts add to {tot_all}, n_all is {n_all}; check for a missing answer")
        q["_"] = {"small": n_all < 30}

    def enrich(self):
        d = self.d
        self.question(d.get("motivation"), "motivation", "Reason to buy")
        self.question(d.get("objections"), "objections", "Objection")
        self.question(d.get("attribution"), "attribution", "How they found you")
        aud = d.get("audience") or {}
        self.question(aud.get("who_for"), "audience.who_for", "Buying for")
        self.question(aud.get("problem"), "audience.problem", "Problem to solve")
        ret = d.get("returning") or {}
        for i, q in enumerate(ret.get("questions", []) or []):
            self.question(q, f"returning.questions[{i}]", "Returning: " + q.get("q", "")[:40])
        for i, q in enumerate(d.get("other_questions", []) or []):
            self.question(q, f"other_questions[{i}]")
        cmp_ = ret.get("comparison")
        if cmp_:
            for i, r in enumerate(cmp_.get("rows", [])):
                try:
                    r["_"] = {"new_pct": pct(r["new"], r["new_n"]), "ret_pct": pct(r["ret"], r["ret_n"])}
                except (KeyError, TypeError):
                    self.errors.append(f"returning.comparison.rows[{i}] needs new, new_n, ret, ret_n counts")

        obj = d.get("objections") or {}
        by_label = {r.get("label"): r for r in obj.get("rows", [])}
        for i, c in enumerate(d.get("objection_cards", []) or []):
            row = by_label.get(c.get("row_label"))
            if not row or "_" not in row:
                self.errors.append(f"objection_cards[{i}].row_label '{c.get('row_label')}' does not match a row in objections")
            else:
                c["_"] = dict(row["_"])
                if row["all"] < 5:
                    self.warnings.append(f"objection_cards[{i}] is built on fewer than 5 answers; move it to smaller_objections")
            if c.get("why"):
                self.question(c["why"], f"objection_cards[{i}].why", collect_shifts=False)

        prod = d.get("products")
        if prod:
            n = prod.get("n") or 0
            for r in prod.get("rows", []):
                r["_"] = {"pct": pct(r.get("count", 0), n), "small": r.get("count", 0) < 30}
            mix = prod.get("objection_mix")
            if mix:
                for r in mix.get("rows", []):
                    r["_"] = {"small": r.get("n", 0) < 30}

        self.shifts.sort(key=lambda s: -abs(s["delta"]))
        d["_shifts"] = self.shifts

    # ---------- checks ----------
    def check(self):
        d = self.d
        for key in ("meta", "snapshot", "objections", "objection_cards", "actions", "method"):
            if not d.get(key):
                self.errors.append(f"missing required section '{key}'")
        meta = d.get("meta", {})
        for k in ("brand", "period_label", "report_title"):
            if not meta.get(k):
                self.errors.append(f"meta.{k} is empty")

        for p, s in walk_strings(d):
            if EM_DASH in s:
                self.errors.append(f"em dash in {p}")

        if EXAMPLE.exists() and meta.get("brand"):
            ex_brand = json.loads(EXAMPLE.read_text()).get("meta", {}).get("brand", "")
            if ex_brand and ex_brand.lower() != meta["brand"].lower():
                needles = {ex_brand.lower(), ex_brand.lower().replace(" ", "-")}
                for p, s in walk_strings(d):
                    if any(n in s.lower() for n in needles):
                        self.errors.append(f"example brand '{ex_brand}' leaked into {p}")

        real_shift = any(s["tag"] in ("Strong signal", "Early signal") for s in self.shifts)
        for i, c in enumerate(d.get("insights", []) or []):
            m = MOVE_WORDS.search(c.get("title", ""))
            if m and not real_shift:
                self.errors.append(f"insights[{i}] title says '{m.group(0)}' but nothing this period is tagged Strong or Early signal; describe the level, not a change")

        def need_source(sec, items):
            for i, x in enumerate(items or []):
                if not x.get("source"):
                    self.errors.append(f"{sec}[{i}] has no source; every item must trace to the data")

        need_source("insights", d.get("insights"))
        need_source("angles", d.get("angles"))
        need_source("objection_cards", d.get("objection_cards"))
        need_source("audience.personas", (d.get("audience") or {}).get("personas"))
        need_source("returning.moves", (d.get("returning") or {}).get("moves"))
        acts = d.get("actions") or {}
        for grp in ("this_week", "this_month", "test_next"):
            need_source(f"actions.{grp}", acts.get(grp))
            for i, a in enumerate(acts.get(grp, []) or []):
                if a.get("channel") not in CHANNELS:
                    self.errors.append(f"actions.{grp}[{i}] channel must be one of {sorted(CHANNELS)}")
        if len(acts.get("this_week", []) or []) > 3:
            self.errors.append("actions.this_week has more than 3 items")
        if not any(acts.get(g) for g in ("this_week", "this_month", "test_next")):
            self.errors.append("actions has no items")

        for i, c in enumerate(d.get("objection_cards", []) or []):
            cnt = c.get("counters") or {}
            for k in ("website", "ads", "content", "email"):
                if not cnt.get(k):
                    self.errors.append(f"objection_cards[{i}].counters.{k} is empty")

        if len(d.get("insights", []) or []) > 8:
            self.errors.append("more than 8 insights")
        if "overcame" not in json.dumps(d).lower():
            self.warnings.append("no 'objections buyers overcame' label found")


def build(data_path, out_path):
    d = json.loads(Path(data_path).read_text())
    b = Build(d)
    b.enrich()
    b.check()
    for w in b.warnings:
        print(f"WARNING: {w}")
    if b.errors:
        print("BUILD FAILED:")
        for e in b.errors:
            print(f"  - {e}")
        sys.exit(1)

    mark = MARK.read_text()
    mark = re.sub(r"<!--.*?-->", "", mark, flags=re.S)
    mark = " ".join(mark.split()).replace("'", "\\'").replace("<svg ", '<svg aria-hidden="true" ', 1)

    def js_json(o):
        return json.dumps(o, ensure_ascii=False).replace("</", "<\\/")

    title = f"{d['meta']['brand']} Survey Report \u00b7 {d['meta']['period_label']}"
    out = (TEMPLATE.read_text()
           .replace("__TITLE__", html.escape(title))
           .replace("__REPORT_DATA__", js_json(d))
           .replace("__HISTORY__", js_json(d.get("history", {})))
           .replace("__ECA_MARK__", mark))
    if EM_DASH in out:
        print("BUILD FAILED: em dash found in rendered output")
        sys.exit(1)
    Path(out_path).write_text(out)
    print(f"OK: wrote {out_path} ({Path(out_path).stat().st_size/1024:.1f} kB), "
          f"{len(b.shifts)} shift(s) this period, {len(b.warnings)} warning(s)")


if __name__ == "__main__":
    if len(sys.argv) != 3:
        print(__doc__)
        sys.exit(2)
    build(sys.argv[1], sys.argv[2])
