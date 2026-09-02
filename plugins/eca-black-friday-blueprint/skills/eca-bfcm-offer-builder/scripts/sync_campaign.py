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


def _offer_window(phases):
    """The window a customer can actually buy in — NOT the whole calendar.

    The full span includes LIST_BUILD and POST_SALE, which are not the sale. Labelling
    that span "sale window" tells the member the offer runs for four months.
    """
    selling = [p for p in phases
               if p["PHASE_ID"] in ("SALE_LIVE", "BLACK_FRIDAY", "WEEKEND",
                                    "CYBER_MONDAY", "LAST_CHANCE") and p["_s"]]
    if not selling:
        return ""
    s_, e_ = min(p["_s"] for p in selling), max(p["_e"] for p in selling)
    return "Offer live {} &ndash; {} &middot; ".format(
        s_.strftime("%-d %b"), e_.strftime("%-d %b %Y"))


def dashboard(phases, tasks, today, problems, brand="", year=""):
    """ECA Design System. Tokens in assets/ECA Design System/eca-tokens.css — keep in sync.

    Layout notes, because the obvious versions do not work:
    - The timeline is a FLEX strip with a min-width per segment, not an absolutely
      positioned to-scale bar. A 56-day list-build next to a 1-day Black Friday makes a
      true-to-scale timeline unreadable — November collapses into slivers and the labels
      overlap. Relative width still communicates length; exact dates live in the cards.
    - Phases are CARDS, not table rows. A table forces the phase name, dates and a long
      task list into one row, which leaves a column of dead space beside every task block.
    """
    if not phases:
        return "<p>No phases.</p>"

    def state_of(p):
        return "done" if p["_e"] < today else ("live" if p["_s"] <= today else "todo")

    # ---- timeline: flex segments, min-width so labels always fit ----
    segs = []
    for p in phases:
        days = max((p["_e"] - p["_s"]).days + 1, 1)
        st = state_of(p)
        tick = ""
        if st == "live":
            pos = (today - p["_s"]).days / days * 100
            tick = '<i class="tick" style="left:{:.1f}%"></i>'.format(min(max(pos, 2), 98))
        segs.append(
            '<div class="seg {}" style="flex:{}">{}'
            '<b>{}</b><span>{}</span></div>'.format(
                st, days, tick, html.escape(p["PHASE_ID"].replace("_", " ")),
                "{} day{}".format(days, "s" if days > 1 else "")))

    # ---- header stats ----
    live = next((p for p in phases if state_of(p) == "live"), None)
    nxt = next((p for p in phases if p["_s"] > today), None)
    bf = next((p for p in phases if p["PHASE_ID"] == "BLACK_FRIDAY"), None)
    done = sum(1 for t in tasks
               if (t.get("STATUS") or "").strip().lower() in ("done", "complete", "completed"))
    def nice(d):
        return d.strftime("%a %-d %b") if hasattr(d, "strftime") else str(d)

    stats = [("PHASE NOW",
              live["PHASE_ID"].replace("_", " ") if live else "NOT STARTED",
              "until {}".format(nice(live["_e"])) if live else
              ("starts {}".format(nice(phases[0]["_s"])) if phases else ""))]
    if nxt:
        stats.append((nxt["PHASE_ID"].replace("_", " ") + " IN",
                      "{}d".format((nxt["_s"] - today).days), nice(nxt["_s"])))
    if bf:
        d = (bf["_s"] - today).days
        stats.append(("BLACK FRIDAY", "{}d".format(d) if d >= 0 else "PASSED", nice(bf["_s"])))
    cm = next((p for p in phases if p["PHASE_ID"] == "CYBER_MONDAY"), None)
    if cm:
        d = (cm["_s"] - today).days
        stats.append(("CYBER MONDAY", "{}d".format(d) if d >= 0 else "PASSED", nice(cm["_s"])))
    if tasks:
        stats.append(("TASKS DONE", "{}/{}".format(done, len(tasks)),
                      "{} outstanding".format(len(tasks) - done)))

    # ---- phase cards ----
    cards = []
    for p in phases:
        st = state_of(p)
        d = (p["_s"] - today).days
        when = "LIVE NOW" if st == "live" else ("IN {} DAYS".format(d) if d > 0 else "DONE")
        days = (p["_e"] - p["_s"]).days + 1
        mine = [t for t in tasks if (t.get("PHASE_ID") or "").strip() == p["PHASE_ID"]]

        rows = ""
        for t in mine:
            status = (t.get("STATUS") or "").strip() or "-"
            cls = "ok" if status.lower().startswith(("done", "complete")) else "todo"
            note = (t.get("NOTES") or "").strip()
            rows += ('<li><span class="tdate">{}</span>'
                     '<span class="ttask">{}{}</span>'
                     '<span class="pill {}">{}</span>'
                     '<span class="towner">{}</span></li>').format(
                html.escape(t.get("WHEN", "") or "—"),
                html.escape(t.get("TASK", "")),
                '<em>{}</em>'.format(html.escape(note)) if note else "",
                cls, html.escape(status),
                html.escape((t.get("OWNER", "") or "").replace("_", " ")))
        body = ('<ul class="tasks">{}</ul>'.format(rows) if rows
                else '<p class="empty">No tasks yet.</p>')

        cards.append(
            '<section class="phase {st}">'
            '<div class="phead">'
            '<span class="badge {st}">{pid}</span>'
            '<span class="dates">{s} &rarr; {e}</span>'
            '<span class="len">{days} day{pl}</span>'
            '<span class="when {st}">{when}</span>'
            '</div>'
            '<p class="what">{what}</p>{body}</section>'.format(
                st=st, pid=html.escape(p["PHASE_ID"].replace("_", " ")),
                s=p["_s"], e=p["_e"], days=days, pl="s" if days > 1 else "",
                when=when, what=html.escape(p.get("WHAT HAPPENS", "")), body=body))

    warn = ('<div class="warn"><h3>CHECK BEFORE RELYING ON THESE DATES</h3><ul>{}</ul></div>'.format(
        "".join("<li>{}</li>".format(html.escape(x)) for x in problems)) if problems else "")

    return """<!doctype html><html lang="en"><meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>BFCM {year} Campaign{brandt}</title>
<link href="https://fonts.googleapis.com/css2?family=Nunito+Sans:wght@700;800;900&family=Montserrat:wght@400;500;600;700&display=swap" rel="stylesheet">
<style>
:root{{--eca-green:#3DD62B;--eca-green-dark:#2FB61F;--eca-green-tint:#E8FAE6;--eca-black:#0A0A0A;
--eca-ink:#1A1A1A;--eca-gray-2:#555555;--eca-gray-3:#999999;--eca-line:#E0E0E0;--eca-bg:#F5F5F5;
--eca-card:#FFFFFF;--eca-warning:#F5A623;--eca-error:#D0021B;--eca-info:#4A90E2;
--eca-radius-card:12px;--eca-shadow-sm:0 1px 3px rgba(10,10,10,.08);
/* system fallbacks appended so the file still renders correctly with no network */
--eca-display:'Nunito Sans',-apple-system,BlinkMacSystemFont,sans-serif;
--eca-body:'Montserrat',-apple-system,BlinkMacSystemFont,sans-serif}}
*{{box-sizing:border-box}}
body{{margin:0;background:var(--eca-bg);color:var(--eca-ink);font:15px/1.6 var(--eca-body)}}
h1,h2{{font-family:var(--eca-display);text-transform:uppercase;letter-spacing:-.02em;
line-height:1.1;font-weight:800;margin:0}}
header{{background:var(--eca-black);color:#fff;padding:1.75rem 2rem 2rem}}
.wrap{{max-width:1080px;margin:0 auto}}
.brandrow{{display:flex;align-items:center;gap:.6rem;margin-bottom:1.4rem}}
.mark{{width:24px;height:24px;flex:0 0 24px}}
.wordmark{{font-family:var(--eca-display);font-weight:900;font-style:italic;font-size:11px;
letter-spacing:.09em}}
.eyebrow{{font-family:var(--eca-display);font-size:10px;font-weight:800;letter-spacing:.16em;
color:var(--eca-green);margin:0 0 .45rem}}
header h1{{font-size:clamp(1.35rem,3vw,1.9rem);color:#fff}}
.prep{{color:var(--eca-gray-3);font-size:12.5px;margin:.45rem 0 0}}
.stats{{display:grid;grid-template-columns:repeat(auto-fit,minmax(150px,1fr));gap:.7rem;margin-top:1.4rem}}
.stat{{background:#141414;border:1px solid #262626;border-radius:var(--eca-radius-card);padding:.65rem .9rem}}
.stat b{{display:block;font-family:var(--eca-display);font-size:9.5px;font-weight:800;
letter-spacing:.11em;color:var(--eca-gray-3);margin-bottom:.15rem}}
.stat span{{font-family:var(--eca-display);font-weight:800;font-size:1.1rem;color:var(--eca-green);
display:block;line-height:1.15}}
.stat i{{display:block;font-style:normal;font-size:10.5px;color:var(--eca-gray-3);
margin-top:.2rem;font-variant-numeric:tabular-nums}}
main{{max-width:1080px;margin:0 auto;padding:1.75rem 2rem 3rem}}
.card{{background:var(--eca-card);border:1px solid var(--eca-line);border-radius:var(--eca-radius-card);
box-shadow:var(--eca-shadow-sm);padding:1.4rem;margin-bottom:1.4rem}}
.card>h2{{font-size:.85rem;margin-bottom:1.1rem}}
/* timeline: flex, not to-scale, so short phases stay legible */
.strip{{display:flex;gap:5px;align-items:stretch;overflow-x:auto;padding-bottom:2px}}
.seg{{position:relative;min-width:96px;flex-shrink:0;border-radius:8px;padding:.55rem .5rem;background:#F0F0F0;
border:1px solid var(--eca-line);text-align:center;overflow:hidden}}
.seg b{{display:block;font-family:var(--eca-display);font-size:9.5px;font-weight:800;
letter-spacing:.05em;color:var(--eca-gray-2);line-height:1.25}}
.seg span{{font-size:10px;color:var(--eca-gray-3)}}
.seg.done{{opacity:.45}}
.seg.live{{background:var(--eca-green);border-color:var(--eca-green-dark)}}
.seg.live b,.seg.live span{{color:var(--eca-black)}}
.tick{{position:absolute;top:0;bottom:0;width:2px;background:var(--eca-error)}}
.scale{{margin:.6rem 0 0;font-size:11px;color:var(--eca-gray-3);text-align:right}}
/* phase cards */
.phase{{border:1px solid var(--eca-line);border-radius:var(--eca-radius-card);
background:var(--eca-card);margin-bottom:.85rem;overflow:hidden}}
.phase.live{{border-color:var(--eca-green);box-shadow:0 0 0 2px rgba(61,214,43,.18)}}
.phase.done{{opacity:.6}}
.phead{{display:flex;flex-wrap:wrap;align-items:center;gap:.6rem;padding:.85rem 1.1rem;
background:#FAFAFA;border-bottom:1px solid var(--eca-line)}}
.phase.live .phead{{background:var(--eca-green-tint)}}
.badge{{font-family:var(--eca-display);font-size:10px;font-weight:800;letter-spacing:.08em;
padding:.32rem .7rem;border-radius:999px;background:var(--eca-black);color:#fff;white-space:nowrap}}
.badge.live{{background:var(--eca-green);color:var(--eca-black)}}
.badge.done{{background:#00000014;color:var(--eca-gray-2)}}
.dates{{font-variant-numeric:tabular-nums;font-size:13px;color:var(--eca-gray-2);white-space:nowrap}}
.len{{font-size:11.5px;color:var(--eca-gray-3);white-space:nowrap}}
.when{{margin-left:auto;font-family:var(--eca-display);font-size:10px;font-weight:800;
letter-spacing:.07em;padding:.3rem .65rem;border-radius:999px;background:#4A90E21A;
color:var(--eca-info);white-space:nowrap}}
.when.live{{background:var(--eca-green);color:var(--eca-black)}}
.when.done{{background:#00000010;color:var(--eca-gray-3)}}
.what{{margin:0;padding:.75rem 1.1rem;color:var(--eca-gray-2);font-size:13.5px}}
.tasks{{list-style:none;margin:0;padding:0 1.1rem 1rem}}
.tasks li{{display:grid;grid-template-columns:132px 1fr auto auto;gap:.75rem;align-items:baseline;
padding:.55rem 0;border-top:1px solid var(--eca-line);font-size:13.5px}}
.tdate{{font-variant-numeric:tabular-nums;color:var(--eca-gray-3);font-size:12px;white-space:nowrap}}
.ttask em{{display:block;font-style:normal;color:var(--eca-gray-3);font-size:12px;margin-top:.1rem}}
.towner{{font-family:var(--eca-display);font-size:9.5px;font-weight:800;letter-spacing:.06em;
color:var(--eca-gray-3);white-space:nowrap}}
.pill{{display:inline-block;padding:.15rem .6rem;border-radius:999px;font-size:11px;
font-weight:600;white-space:nowrap}}
.pill.ok{{background:var(--eca-green-tint);color:var(--eca-green-dark)}}
.pill.todo{{background:#F5A6231A;color:#9A6608}}
.empty{{margin:0;padding:0 1.1rem 1rem;color:var(--eca-gray-3);font-size:13px}}
.warn{{background:#D0021B0D;border:1px solid #D0021B55;border-left:4px solid var(--eca-error)}}
.warn h3{{font-family:var(--eca-display);text-transform:uppercase;font-size:.78rem;
color:var(--eca-error);margin:0 0 .55rem}}
.warn ul{{margin:0;padding-left:1.1rem;font-size:13.5px}}
footer{{max-width:1080px;margin:0 auto;padding:0 2rem 3rem;color:var(--eca-gray-3);font-size:11.5px}}
@media(max-width:760px){{header,main{{padding:1.25rem}}
.tasks li{{grid-template-columns:1fr auto;row-gap:.15rem}}
.tdate{{grid-column:1/-1}} .towner{{grid-column:2}}
.when{{margin-left:0}}}}
</style>
<header><div class="wrap">
<div class="brandrow">{mark}<span class="wordmark">ECOMMERCE ACADEMY&trade;</span></div>
<p class="eyebrow">ECA BLACK FRIDAY BLUEPRINT</p>
<h1>BFCM {year} Campaign Calendar</h1>
<p class="prep">{prep}{window}Generated {gen}</p>
<div class="stats">{stats}</div>
</div></header>
<main>
{warn}
<div class="card"><h2>Campaign timeline</h2><div class="strip">{segs}</div>
<p class="scale">Segment width shows relative length, not exact scale &middot; red line marks today</p></div>
<h2 style="font-size:.85rem;margin:0 0 .9rem">Phases &amp; tasks</h2>
{cards}
</main>
<footer>Generated by sync_campaign.py &middot; do not edit this file, changes will be overwritten.
Edit the calendar CSV and re-run sync.</footer></html>
""".format(year=year or today.year, brandt=(" — " + brand) if brand else "",
           prep=("Prepared for " + html.escape(brand) + " &middot; ") if brand else "",
           window=_offer_window(phases),
           mark=ECA_MARK, gen=today.isoformat(), warn=warn,
           segs="".join(segs), cards="".join(cards),
           stats="".join('<div class="stat"><b>{}</b><span>{}</span>{}</div>'.format(
               k, v, '<i>{}</i>'.format(html.escape(sub)) if sub else "")
               for k, v, sub in stats))


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
