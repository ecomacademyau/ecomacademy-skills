#!/usr/bin/env python3
"""
Validate the campaign CSVs and regenerate the human views.

Two CSVs are the source of truth:
  bfcm-<year>-calendar.csv   one row per PHASE. One writer (the offer builder) plus the
                             member. Every other skill READS it.
  bfcm-<year>-runsheet.csv   one row per task. APPEND-ONLY. Each channel skill adds its
                             own rows tagged with OWNER and never edits another's.

Everything else is generated and can be deleted safely:
  bfcm-<year>-dashboard.html   what to open each morning
  a markdown mirror printed to stdout for the master file

Run this after any change, and at the start of every skill's run.

Usage:
  python3 sync_campaign.py calendar.csv [runsheet.csv] [--html out.html] [--brand "Name"] [--markdown]

The HTML uses the ECA Design System in assets/ECA Design System/. Keep the tokens in sync.
"""
import csv, sys, html
from datetime import date, datetime

PHASE_ORDER = ["LIST_BUILD", "EARLY_ACCESS", "WARM_UP", "SALE_LIVE", "BLACK_FRIDAY",
               "WEEKEND", "CYBER_MONDAY", "LAST_CHANCE", "POST_SALE"]


def parse_date(v, row, col, problems):
    """ISO only. Excel silently rewrites dates on save and that must not pass silently."""
    v = (v or "").strip()
    try:
        return datetime.strptime(v, "%Y-%m-%d").date()
    except ValueError:
        for fmt, desc in (("%d/%m/%Y", "d/m/Y"), ("%m/%d/%Y", "m/d/Y"), ("%d-%b-%y", "d-Mon-yy")):
            try:
                d = datetime.strptime(v, fmt).date()
                problems.append(
                    "{} {}: '{}' is not ISO. It looks like {}, which usually means a "
                    "spreadsheet rewrote it on save. Read as {} — CONFIRM this is right "
                    "before planning against it.".format(row, col, v, desc, d))
                return d
            except ValueError:
                continue
        problems.append("{} {}: '{}' is not a date I can read.".format(row, col, v))
        return None


def load_calendar(path):
    problems, phases = [], []
    with open(path, newline="", encoding="utf-8-sig") as f:
        for r in csv.DictReader(f):
            pid = (r.get("PHASE_ID") or "").strip()
            if not pid:
                continue
            if pid not in PHASE_ORDER:
                problems.append("Unknown PHASE_ID '{}'. Add it to the template before using it.".format(pid))
            s = parse_date(r.get("STARTS"), pid, "STARTS", problems)
            e = parse_date(r.get("ENDS"), pid, "ENDS", problems)
            if s and e and e < s:
                problems.append("{}: ENDS ({}) is before STARTS ({}).".format(pid, e, s))
            phases.append({**r, "PHASE_ID": pid, "_s": s, "_e": e})
    seen = [p["PHASE_ID"] for p in phases]
    if len(seen) != len(set(seen)):
        problems.append("Duplicate PHASE_IDs. Each phase must appear once.")
    for a, b in zip(PHASE_ORDER, [p for p in PHASE_ORDER if p in seen]):
        pass
    ordered = [p for p in phases if p["_s"]]
    ordered.sort(key=lambda p: PHASE_ORDER.index(p["PHASE_ID"]) if p["PHASE_ID"] in PHASE_ORDER else 99)
    for a, b in zip(ordered, ordered[1:]):
        if a["_e"] and b["_s"] and b["_s"] > a["_e"] + __import__("datetime").timedelta(days=1) \
                and a["PHASE_ID"] != "LIST_BUILD":
            problems.append("Gap between {} (ends {}) and {} (starts {}). Intentional?".format(
                a["PHASE_ID"], a["_e"], b["PHASE_ID"], b["_s"]))
    return ordered, problems


def load_runsheet(path):
    if not path:
        return []
    try:
        with open(path, newline="", encoding="utf-8-sig") as f:
            return [r for r in csv.DictReader(f) if (r.get("TASK") or "").strip()]
    except FileNotFoundError:
        return []


def markdown(phases, today):
    out = ["| Phase ID | Starts | Ends | Days | What happens |", "|---|---|---|---|---|"]
    for p in phases:
        n = (p["_e"] - p["_s"]).days + 1 if p["_s"] and p["_e"] else ""
        mark = " **(now)**" if p["_s"] and p["_e"] and p["_s"] <= today <= p["_e"] else ""
        out.append("| {}{} | {} | {} | {} | {} |".format(
            p["PHASE_ID"], mark, p["_s"], p["_e"], n, p.get("WHAT HAPPENS", "")))
    return "\n".join(out)


ECA_MARK = ("""<svg viewBox="0 0 310 285" fill="none" xmlns="http://www.w3.org/2000/svg" class="mark">"""
            """<g stroke="#3DD62B" stroke-width="22" stroke-linejoin="round" stroke-linecap="round">"""
            """<path d="M31 254V121M105 254V60M179 254V158"/><path d="M20 254h270"/>"""
            """<path d="M120 96 205 40l74 48"/><path d="M279 31v57h-57"/></g></svg>""")


def dashboard(phases, tasks, today, problems, brand="", year=""):
    """ECA Design System. Tokens in assets/ECA Design System/eca-tokens.css — keep in sync."""
    if not phases:
        return "<p>No phases.</p>"
    start, end = phases[0]["_s"], max(p["_e"] for p in phases)
    span = max((end - start).days, 1)
    def pct(d): return (d - start).days / span * 100

    bars = []
    for p in phases:
        left, width = pct(p["_s"]), max((p["_e"] - p["_s"]).days + 1, 1) / span * 100
        state = "done" if p["_e"] < today else ("live" if p["_s"] <= today else "todo")
        bars.append('<div class="bar {}" style="left:{:.2f}%;width:{:.2f}%" title="{} to {}">'
                    '<span>{}</span></div>'.format(state, left, width, p["_s"], p["_e"],
                                                   html.escape(p["PHASE_ID"])))
    marker = ('<div class="today" style="left:{:.2f}%"><span>TODAY</span></div>'.format(pct(today))
              if start <= today <= end else "")

    live = next((p for p in phases if p["_s"] <= today <= p["_e"]), None)
    nxt = next((p for p in phases if p["_s"] > today), None)
    bf = next((p for p in phases if p["PHASE_ID"] == "BLACK_FRIDAY"), None)
    stats = []
    stats.append(("PHASE NOW", live["PHASE_ID"] if live else "NOT STARTED"))
    if nxt:
        stats.append(("NEXT", "{} in {}d".format(nxt["PHASE_ID"], (nxt["_s"] - today).days)))
    if bf:
        d = (bf["_s"] - today).days
        stats.append(("BLACK FRIDAY", "{}d".format(d) if d >= 0 else "PASSED"))
    done = sum(1 for t in tasks if (t.get("STATUS") or "").strip().lower() in ("done", "complete", "completed"))
    if tasks:
        stats.append(("TASKS DONE", "{}/{}".format(done, len(tasks))))

    rows = []
    for p in phases:
        d = (p["_s"] - today).days
        when, cls = ("LIVE", "live") if p["_s"] <= today <= p["_e"] else \
                    (("IN {}D".format(d), "") if d > 0 else ("DONE", "done"))
        mine = [t for t in tasks if (t.get("PHASE_ID") or "").strip() == p["PHASE_ID"]]
        tl = "".join(
            '<li><span class="w">{}</span> {} <span class="pill {}">{}</span>'
            '<span class="own">{}</span></li>'.format(
                html.escape(t.get("WHEN", "") or ""), html.escape(t.get("TASK", "")),
                "ok" if (t.get("STATUS") or "").lower().startswith(("done", "complete")) else "todo",
                html.escape(t.get("STATUS", "") or "-"), html.escape(t.get("OWNER", "") or ""))
            for t in mine)
        rows.append(
            '<tr class="{}"><td class="pid">{}</td><td class="num">{}</td><td class="num">{}</td>'
            '<td><span class="pill {}">{}</span></td><td>{}{}</td></tr>'.format(
                cls, html.escape(p["PHASE_ID"]), p["_s"], p["_e"],
                "ok" if cls == "live" else ("mute" if cls == "done" else "info"), when,
                html.escape(p.get("WHAT HAPPENS", "")),
                "<ul class='tasks'>{}</ul>".format(tl) if tl else ""))

    warn = ('<div class="warn"><h3>CHECK BEFORE RELYING ON THESE DATES</h3><ul>{}</ul></div>'.format(
        "".join("<li>{}</li>".format(html.escape(x)) for x in problems)) if problems else "")

    return """<!doctype html><html lang="en"><meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>BFCM {year} Campaign{brandt}</title>
<link href="https://fonts.googleapis.com/css2?family=Nunito+Sans:wght@700;800;900&family=Montserrat:wght@400;500;600;700&display=swap" rel="stylesheet">
<style>
:root{{--eca-green:#3DD62B;--eca-green-dark:#2FB61F;--eca-green-tint:#E8FAE6;--eca-black:#0A0A0A;
--eca-ink:#1A1A1A;--eca-gray-2:#555555;--eca-gray-3:#999999;--eca-line:#E0E0E0;--eca-bg:#F5F5F5;--eca-card:#FFFFFF;
--eca-warning:#F5A623;--eca-error:#D0021B;--eca-info:#4A90E2;--eca-radius-card:12px;
--eca-shadow-sm:0 1px 3px rgba(10,10,10,.08);
/* system fallbacks appended so the file still renders correctly with no network */
--eca-display:'Nunito Sans',-apple-system,BlinkMacSystemFont,sans-serif;
--eca-body:'Montserrat',-apple-system,BlinkMacSystemFont,sans-serif}}
*{{box-sizing:border-box}}
body{{margin:0;background:var(--eca-bg);color:var(--eca-ink);font:15px/1.6 var(--eca-body)}}
h1,h2,h3{{font-family:var(--eca-display);text-transform:uppercase;letter-spacing:-.02em;line-height:1.1;
font-weight:800;margin:0}}
header{{background:var(--eca-black);color:#fff;padding:2rem 2rem 2.25rem}}
.hwrap{{max-width:1120px;margin:0 auto}}
.brandrow{{display:flex;align-items:center;gap:.7rem;margin-bottom:1.5rem}}
.mark{{width:26px;height:26px;flex:0 0 26px}}
.wordmark{{font-family:var(--eca-display);font-weight:900;font-style:italic;font-size:12px;
letter-spacing:.08em;color:#fff}}
header h1{{font-size:clamp(1.4rem,3vw,2rem);color:#fff}}
.eyebrow{{font-family:var(--eca-display);font-size:11px;font-weight:800;letter-spacing:.14em;
color:var(--eca-green);margin-bottom:.4rem}}
.prep{{color:var(--eca-gray-3);font-size:13px;margin-top:.35rem}}
.stats{{display:flex;flex-wrap:wrap;gap:.75rem;margin-top:1.5rem}}
.stat{{background:#141414;border:1px solid #262626;border-radius:var(--eca-radius-card);
padding:.7rem 1.1rem;min-width:130px}}
.stat b{{display:block;font-family:var(--eca-display);font-size:10px;font-weight:800;
letter-spacing:.1em;color:var(--eca-gray-3)}}
.stat span{{font-family:var(--eca-display);font-weight:800;font-size:1.15rem;color:var(--eca-green)}}
main{{max-width:1120px;margin:0 auto;padding:2rem}}
.card{{background:var(--eca-card);border:1px solid var(--eca-line);border-radius:var(--eca-radius-card);
box-shadow:var(--eca-shadow-sm);padding:1.5rem;margin-bottom:1.5rem}}
.card>h2{{font-size:.95rem;margin-bottom:1.25rem}}
.strip{{position:relative;height:70px}}
.bar{{position:absolute;top:10px;height:32px;border-radius:8px;display:flex;align-items:center;
justify-content:center;overflow:hidden;background:#EDEDED;border:1px solid var(--eca-line)}}
.bar span{{font-family:var(--eca-display);font-size:9px;font-weight:800;letter-spacing:.06em;
padding:0 8px;white-space:nowrap;color:var(--eca-gray-2)}}
.bar.done{{opacity:.45}}
.bar.live{{background:var(--eca-green);border-color:var(--eca-green-dark)}}
.bar.live span{{color:var(--eca-black)}}
.today{{position:absolute;top:0;bottom:18px;width:2px;background:var(--eca-error)}}
.today span{{position:absolute;top:100%;left:-14px;font-family:var(--eca-display);font-size:9px;
font-weight:800;letter-spacing:.08em;color:var(--eca-error)}}
table{{width:100%;border-collapse:collapse}}
th{{background:var(--eca-green-tint);color:var(--eca-green-dark);font-family:var(--eca-display);
font-size:10px;font-weight:800;letter-spacing:.1em;text-align:left;padding:.7rem .75rem}}
td{{padding:.8rem .75rem;border-bottom:1px solid var(--eca-line);vertical-align:top}}
tr:nth-child(even) td{{background:#FAFAFA}}
tr.live td{{background:var(--eca-green-tint)}} tr.done td{{opacity:.5}}
.pid{{font-family:var(--eca-display);font-size:11px;font-weight:800;letter-spacing:.05em;white-space:nowrap}}
.num{{font-variant-numeric:tabular-nums;white-space:nowrap;color:var(--eca-gray-2)}}
.pill{{display:inline-block;padding:2px 10px;border-radius:999px;font-size:11px;font-weight:600;
white-space:nowrap}}
.pill.ok{{background:var(--eca-green-tint);color:var(--eca-green-dark)}}
.pill.info{{background:#4A90E21A;color:var(--eca-info)}}
.pill.mute{{background:#0000000D;color:var(--eca-gray-3)}}
.pill.todo{{background:#F5A6231A;color:#9A6608}}
.tasks{{margin:.6rem 0 0;padding:0;list-style:none;font-size:13px}}
.tasks li{{padding:.3rem 0;border-top:1px solid var(--eca-line);display:flex;flex-wrap:wrap;
align-items:center;gap:.5rem}}
.w{{font-variant-numeric:tabular-nums;color:var(--eca-gray-2);font-size:12px;min-width:112px}}
.own{{color:var(--eca-gray-3);font-size:11px;margin-left:auto}}
.warn{{background:#D0021B0D;border:1px solid #D0021B55;border-left:4px solid var(--eca-error)}}
.warn h3{{font-size:.8rem;color:var(--eca-error);margin-bottom:.6rem}}
.warn ul{{margin:0;padding-left:1.1rem;font-size:13.5px}}
footer{{max-width:1120px;margin:0 auto;padding:0 2rem 3rem;color:var(--eca-gray-3);font-size:12px}}
@media(max-width:720px){{header,main{{padding:1.25rem}}.w{{min-width:0}}}}
</style>
<header><div class="hwrap">
<div class="brandrow">{mark}<span class="wordmark">ECOMMERCE ACADEMY&trade;</span></div>
<p class="eyebrow">BLACK FRIDAY BLUEPRINT</p>
<h1>BFCM {year} Campaign Calendar</h1>
<p class="prep">{prep}Generated {gen} &middot; the CSVs are the source of truth</p>
<div class="stats">{stats}</div>
</div></header>
<main>
{warn}
<div class="card"><h2>Campaign timeline</h2><div class="strip">{bars}{marker}</div></div>
<div class="card"><h2>Phases &amp; tasks</h2>
<table><tr><th>Phase</th><th>Starts</th><th>Ends</th><th>When</th><th>What happens</th></tr>
{rows}</table></div>
</main>
<footer>Generated by sync_campaign.py &middot; do not edit this file, changes will be overwritten.
Edit the calendar CSV and re-run sync.</footer></html>
""".format(year=year or today.year, brandt=(" — " + brand) if brand else "",
           prep=("Prepared for " + html.escape(brand) + " &middot; ") if brand else "",
           mark=ECA_MARK, gen=today.isoformat(), warn=warn, bars="".join(bars), marker=marker,
           rows="".join(rows),
           stats="".join('<div class="stat"><b>{}</b><span>{}</span></div>'.format(k, v) for k, v in stats))


if __name__ == "__main__":
    a = [x for x in sys.argv[1:] if not x.startswith("--")]
    if not a:
        sys.exit(__doc__)
    today = date.today()
    phases, problems = load_calendar(a[0])
    tasks = load_runsheet(a[1] if len(a) > 1 else None)

    if problems:
        print("PROBLEMS FOUND — resolve before planning against these dates:", file=sys.stderr)
        for p in problems:
            print("  ! " + p, file=sys.stderr)
    else:
        print("Calendar valid: {} phases, no problems.".format(len(phases)), file=sys.stderr)
    if tasks:
        print("Runsheet: {} tasks from {} skill(s).".format(
            len(tasks), len({t.get("OWNER", "") for t in tasks})), file=sys.stderr)

    if "--html" in sys.argv:
        out = sys.argv[sys.argv.index("--html") + 1]
        brand = sys.argv[sys.argv.index("--brand") + 1] if "--brand" in sys.argv else ""
        open(out, "w", encoding="utf-8").write(dashboard(phases, tasks, today, problems, brand))
        print("Wrote " + out, file=sys.stderr)
    if "--markdown" in sys.argv or "--html" not in sys.argv:
        print(markdown(phases, today))
