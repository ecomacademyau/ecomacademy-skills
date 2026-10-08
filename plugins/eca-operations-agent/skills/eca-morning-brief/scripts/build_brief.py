#!/usr/bin/env python3
"""Render the morning brief as a self-contained, ECA-styled HTML page.

Takes a JSON file of findings and emits HTML. A generator rather than hand-written
markup means every brief looks identical, the styling cannot drift run to run, and
the actions always sort above the numbers.

    python3 build_brief.py findings.json --out brief.html

Every section is optional. A source that was unavailable is absent from the body and
named in "Not checked", so a missing connector never shows up as a zero that reads
like real data.
"""
import argparse
import datetime as dt
import html
import json
import urllib.parse
import sys

# ECA Design System. Keep in sync with assets/ECA Design System/eca-tokens.css.
T = {
    "green": "#3DD62B", "green_dark": "#2FB61F", "green_tint": "#E8FAE6",
    "black": "#0A0A0A", "ink": "#1A1A1A", "g1": "#2C2C2C", "g2": "#555555",
    "g3": "#999999", "line": "#E0E0E0", "bg": "#F5F5F5", "card": "#FFFFFF",
    "success": "#3DD62B", "warning": "#F5A623", "error": "#D0021B", "info": "#4A90E2",
}

MARK = ('<svg viewBox="0 0 310 285" fill="none" xmlns="http://www.w3.org/2000/svg" class="mark">'
        '<g stroke="#3DD62B" stroke-width="22" stroke-linejoin="round" stroke-linecap="round">'
        '<path d="M31 254V121M105 254V60M179 254V158"/><path d="M20 254h270"/>'
        '<path d="M120 96 205 40l74 48"/><path d="M279 31v57h-57"/></g></svg>')

CLAUDE_NEW = "https://claude.ai/new?surface=cowork&composer=mini&q="

SEVERITY = {"high": T["error"], "medium": T["warning"], "low": T["info"], "good": T["success"]}


def esc(v):
    return html.escape(str(v if v is not None else ""))


def money(v, cur="AUD"):
    try:
        return "${:,.2f}".format(float(v))
    except (TypeError, ValueError):
        return esc(v)


def delta_html(pct):
    """A change badge. Neutral under 5% so day-to-day noise doesn't read as signal."""
    if pct is None:
        return '<span class="delta flat">no baseline</span>'
    try:
        p = float(pct)
    except (TypeError, ValueError):
        return ""
    if abs(p) < 5:
        return '<span class="delta flat">{:+.0f}% flat</span>'.format(p)
    cls = "up" if p > 0 else "down"
    return '<span class="delta {}">{:+.0f}%</span>'.format(cls, p)


def _nice_ceiling(v):
    """Round a max up to a readable axis top."""
    if v <= 0:
        return 1.0
    import math
    mag = 10 ** math.floor(math.log10(v))
    for step in (1, 1.25, 1.5, 2, 2.5, 3, 4, 5, 7.5, 10):
        if v <= step * mag:
            return step * mag
    return 10 * mag


def render_chart(trend, highlight=None, marker=None, cur="AUD"):
    """Daily bars as inline SVG. No JS, no CDN, so it renders anywhere."""
    if not trend or len(trend) < 2:
        return ""
    W, H = 1000, 250
    PL, PR, PT, PB = 56, 14, 26, 42
    iw, ih = W - PL - PR, H - PT - PB
    vals = [float(p.get("value") or 0) for p in trend]
    top = _nice_ceiling(max(vals))
    n = len(trend)
    slot = iw / n
    bw = min(slot * 0.62, 46)

    out = ['<svg viewBox="0 0 {} {}" class="chart" preserveAspectRatio="xMidYMid meet" '
           'role="img" aria-label="Daily revenue">'.format(W, H)]

    # gridlines + y labels
    for i in range(5):
        y = PT + ih - (ih * i / 4)
        v = top * i / 4
        out.append('<line x1="{:.0f}" y1="{:.1f}" x2="{:.0f}" y2="{:.1f}" stroke="{}" '
                   'stroke-width="1"/>'.format(PL, y, W - PR, y, T["line"]))
        out.append('<text x="{:.0f}" y="{:.1f}" class="ax ax-y">${:,.0f}</text>'.format(
            PL - 9, y + 4, v))

    last_month = None
    for i, p in enumerate(trend):
        v = float(p.get("value") or 0)
        bh = (v / top) * ih if top else 0
        x = PL + slot * i + (slot - bw) / 2
        y = PT + ih - bh
        is_hi = highlight is not None and p.get("date") == highlight
        fill = T["black"] if is_hi else "#D6D3CC"
        out.append('<rect x="{:.1f}" y="{:.1f}" width="{:.1f}" height="{:.1f}" rx="2" fill="{}"/>'
                   .format(x, y, bw, max(bh, 1.5), fill))
        # x labels
        try:
            d = dt.date.fromisoformat(p["date"])
            lab, mon = str(d.day), d.strftime("%b").upper()
        except Exception:
            lab, mon = str(p.get("date", "")), None
        cx = x + bw / 2
        out.append('<text x="{:.1f}" y="{:.0f}" class="ax ax-x{}">{}</text>'.format(
            cx, PT + ih + 18, " hi" if is_hi else "", esc(lab)))
        if mon and mon != last_month:
            out.append('<text x="{:.1f}" y="{:.0f}" class="ax ax-m">{}</text>'.format(
                cx, PT + ih + 34, mon))
            last_month = mon

    # the inflection marker - what makes the chart say something
    if marker and marker.get("date"):
        idx = next((i for i, p in enumerate(trend) if p.get("date") == marker["date"]), None)
        if idx is not None:
            mx = PL + slot * idx
            out.append('<line x1="{:.1f}" y1="{}" x2="{:.1f}" y2="{}" stroke="{}" '
                       'stroke-width="1.5" stroke-dasharray="4 3"/>'.format(
                           mx, PT - 8, mx, PT + ih, T["warning"]))
            anchor = "end" if idx > n * 0.62 else "start"
            dx = -8 if anchor == "end" else 8
            out.append('<text x="{:.1f}" y="{}" class="mk" text-anchor="{}">{}</text>'.format(
                mx + dx, PT - 11, anchor, esc(marker.get("label", ""))))

    out.append("</svg>")
    return "".join(out)


def stat_block(s):
    return ('<div class="stat"><div class="s-label">{}</div>'
            '<div class="s-value">{}</div><div class="s-sub">{}</div></div>').format(
        esc(s.get("label")), esc(s.get("value")), esc(s.get("sub", "")))





def metric_card(m):
    return ('<div class="metric">'
            '<div class="m-label">{}</div>'
            '<div class="m-value">{}</div>'
            '<div class="m-sub">{}<span class="vs">{}</span></div>'
            '</div>').format(esc(m.get("label")), esc(m.get("value")),
                             delta_html(m.get("change_pct")), esc(m.get("baseline_label", "")))


def buttons_html(idx, btns):
    """Two kinds, both plain links. No JS anywhere in the brief.

    claude  opens a new Claude conversation with the whole job written into it
    open    a link to the system that owns the problem

    Chosen over the task bridge because it takes an arbitrary prompt with no setup
    and nothing left behind. Tested alternatives that do not work: callMcpTool
    cannot reach the scheduler (400), and clipboard writes are blocked in the
    artifact sandbox. runScheduledTask works but needs the task to exist first.
    """
    if not btns:
        return ""
    out = []
    for b in btns:
        label = esc(b.get("label", "Open"))
        if b.get("type") == "claude" and b.get("prompt"):
            url = CLAUDE_NEW + urllib.parse.quote(b["prompt"].strip(), safe="")
            out.append('<a class="btn primary" href="{}">{}</a>'.format(esc(url), label))
        elif b.get("url"):
            out.append('<a class="btn" href="{}" target="_blank" rel="noopener">{}</a>'
                       .format(esc(b["url"]), label))
    return '<div class="btns">{}</div>'.format("".join(out)) if out else ""


def action_row(idx, a):
    sev = SEVERITY.get(a.get("severity", "medium"), T["warning"])
    why = '<div class="a-why">{}</div>'.format(esc(a.get("why"))) if a.get("why") else ""
    src = '<span class="a-src">{}</span>'.format(esc(a.get("source"))) if a.get("source") else ""
    return ('<li class="action"><span class="dot" style="background:{}"></span>'
            '<div class="a-body"><div class="a-what">{}</div>{}{}</div>{}</li>').format(
        sev, esc(a.get("what")), why, buttons_html(idx, a.get("buttons")), src)


def section(title, inner, note=None):
    n = '<p class="note">{}</p>'.format(esc(note)) if note else ""
    return '<section class="card"><h2>{}</h2>{}{}</section>'.format(esc(title), n, inner)


def table(headers, rows):
    head = "".join('<th{}>{}</th>'.format(' class="num"' if h.get("num") else "", esc(h.get("t", "")))
                   for h in headers)
    body = "".join("<tr>{}</tr>".format("".join(c for c in r)) for r in rows)
    return '<table><thead><tr>{}</tr></thead><tbody>{}</tbody></table>'.format(head, body)


def td(v, num=False, raw=False):
    return '<td{}>{}</td>'.format(' class="num"' if num else "", v if raw else esc(v))


def build(d):
    brand = d.get("brand", "Store")
    day = d.get("for_date") or dt.date.today().isoformat()
    cur = d.get("currency", "AUD")
    actions = d.get("actions", [])
    gone = d.get("unavailable", [])

    # The summary block. One written sentence saying what actually happened, then the
    # shape, then the headline numbers. A reader who stops here should still know.
    sm = d.get("summary") or {}
    parts = []
    if sm:
        try:
            dl_day = dt.date.fromisoformat(day).strftime("%A %d %B %Y").replace(" 0", " ")
        except ValueError:
            dl_day = day
        try:
            run = dt.date.fromisoformat(d.get("run_date") or dt.date.today().isoformat())
            dl = "{} &middot; covering {}".format(
                run.strftime("%A %d %B %Y").replace(" 0", " "), dl_day)
        except ValueError:
            dl = "covering {}".format(dl_day)
        chart = render_chart(d.get("trend", []), sm.get("highlight_date"),
                             sm.get("marker"), cur)
        stats = "".join(stat_block(x) for x in sm.get("stats", []))
        parts.append(
            '<section class="card summary"><p class="dateline">{}</p>'
            '<h1 class="head">{}</h1><p class="deck">{}</p>{}{}</section>'.format(
                dl, esc(sm.get("headline", "")), esc(sm.get("deck", "")), chart,
                '<div class="stats">{}</div>'.format(stats) if stats else ""))

    # Actions next. The brief exists to tell you what to do.
    if actions:
        act_inner = '<ol class="actions">' + "".join(
            action_row(i, a) for i, a in enumerate(actions)) + "</ol>"
    else:
        act_inner = ('<div class="allclear"><span class="tick">&#10003;</span>'
                     "Nothing needs you this morning. The numbers are below if you want them.</div>")
    parts.append(section("What needs you today", act_inner))

    st = d.get("store")
    if st:
        inner = '<div class="metrics">{}</div>'.format(
            "".join(metric_card(m) for m in st.get("metrics", [])))
        if st.get("top_products"):
            rows = [[td(p.get("title")), td(p.get("units"), num=True),
                     td(money(p.get("revenue"), cur), num=True)] for p in st["top_products"]]
            inner += table([{"t": "Top sellers yesterday"}, {"t": "Units", "num": True},
                            {"t": "Revenue", "num": True}], rows)
        parts.append(section("Store", inner, st.get("note")))

    ad = d.get("ads")
    if ad:
        inner = '<div class="metrics">{}</div>'.format(
            "".join(metric_card(m) for m in ad.get("metrics", [])))
        if ad.get("movers"):
            rows = [[td(m.get("name")), td(money(m.get("spend"), cur), num=True),
                     td(m.get("roas"), num=True), td(m.get("verdict"))] for m in ad["movers"]]
            inner += table([{"t": "Needs a look"}, {"t": "Spend", "num": True},
                            {"t": "ROAS", "num": True}, {"t": "Verdict"}], rows)
        parts.append(section("Ads", inner, ad.get("note")))


    fc = d.get("forecast")
    if fc:
        inner = '<div class="metrics">{}</div>'.format(
            "".join(metric_card(m) for m in fc.get("metrics", [])))
        if fc.get("method"):
            inner += '<p class="method"><strong>How this is worked out:</strong> {}</p>'.format(
                esc(fc["method"]))
        parts.append(section("Where the month lands", inner, fc.get("note")))

    dp = d.get("dispatch")
    if dp:
        inner = '<div class="metrics">{}</div>'.format(
            "".join(metric_card(m) for m in dp.get("metrics", [])))
        if dp.get("orders"):
            rows = [[td(o.get("name")), td(o.get("customer")),
                     td(money(o.get("total"), cur), num=True), td(o.get("waiting"), num=True)]
                    for o in dp["orders"]]
            inner += table([{"t": "Order"}, {"t": "Customer"}, {"t": "Value", "num": True},
                            {"t": "Waiting", "num": True}], rows)
        for note in dp.get("flags", []):
            inner += '<div class="unavail">{}</div>'.format(esc(note))
        parts.append(section("Dispatch", inner, dp.get("note")))

    sk = d.get("stock")
    if sk:
        if sk.get("items"):
            rows = []
            for it in sk["items"]:
                w = it.get("weeks_cover")
                cls = "bad" if (w is not None and w < 2) else ("warn" if (w is not None and w < 4) else "")
                rows.append([td(it.get("title")), td(it.get("on_hand"), num=True),
                             td(it.get("per_week"), num=True),
                             td('<span class="cover {}">{}</span>'.format(
                                 cls, esc("{:.1f} wks".format(w)) if w is not None else "n/a"),
                                num=True, raw=True)])
            inner = table([{"t": "Running low"}, {"t": "On hand", "num": True},
                           {"t": "Per week", "num": True}, {"t": "Cover", "num": True}], rows)
        else:
            inner = ('<div class="allclear"><span class="tick">&#10003;</span>{}</div>'.format(
                esc(sk.get("all_clear", "Nothing below the cover threshold."))))
        parts.append(section("Stock cover", inner, sk.get("note")))

    ib = d.get("inbox")
    if ib:
        inner = '<div class="metrics">{}</div>'.format(
            "".join(metric_card(m) for m in ib.get("metrics", [])))
        if ib.get("threads"):
            rows = []
            for t in ib["threads"]:
                link = ('<a href="{}" target="_blank" rel="noopener">open</a>'.format(esc(t.get("url")))
                        if t.get("url") else "")
                rows.append([td(t.get("from")), td(t.get("subject")),
                             td(t.get("waiting"), num=True), td(link, raw=True)])
            inner += table([{"t": "From"}, {"t": "Subject"}, {"t": "Waiting", "num": True}, {"t": ""}], rows)
        parts.append(section("Customer service", inner, ib.get("note")))

    rv = d.get("reviews")
    if rv:
        inner = '<div class="metrics">{}</div>'.format(
            "".join(metric_card(m) for m in rv.get("metrics", [])))
        if rv.get("items"):
            rows = []
            for r in rv["items"]:
                n = max(0, min(5, int(r.get("rating", 0) or 0)))
                stars = ('<span class="stars">{}<span class="dim">{}</span></span>'
                         .format("&#9733;" * n, "&#9733;" * (5 - n)))
                rows.append([td(stars, raw=True), td(r.get("product")), td(r.get("snippet"))])
            inner += table([{"t": "Rating"}, {"t": "Product"}, {"t": "What they said"}], rows)
        parts.append(section("Reviews", inner, rv.get("note")))

    # Never silently omit a source. A gap the member doesn't know about is worse than a gap.
    if gone:
        parts.append(section("Not checked this morning", "".join(
            '<div class="unavail"><strong>{}</strong> &mdash; {}</div>'.format(
                esc(g.get("name")), esc(g.get("reason"))) for g in gone)))

    gen = d.get("generated_at") or dt.datetime.now().strftime("%Y-%m-%d %H:%M")
    try:
        pretty = dt.date.fromisoformat(day).strftime("%A %d %B %Y").replace(" 0", " ")
    except ValueError:
        pretty = day

    return TEMPLATE.format(T=T, mark=MARK, brand=esc(brand), day=esc(day),
                           pretty=esc(pretty), body="\n".join(parts), gen=esc(gen))


TEMPLATE = """<!doctype html>
<html lang="en"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>{brand} - Morning Brief {day}</title>
<link href="https://fonts.googleapis.com/css2?family=Nunito+Sans:wght@700;800;900&family=Montserrat:wght@400;500;600&display=swap" rel="stylesheet">
<style>
:root{{color-scheme:light}}
*{{box-sizing:border-box}}
body{{margin:0;background:{T[bg]};color:{T[ink]};font-family:'Montserrat',system-ui,sans-serif;line-height:1.6;font-size:15px}}
.wrap{{max-width:860px;margin:0 auto;padding:0 20px 56px}}
.hero{{background:{T[black]};color:#fff;padding:16px 0 14px}}
.hero .wrap{{padding-bottom:0;display:flex;align-items:center;gap:11px}}
.mark{{width:24px;height:auto;display:block;flex:0 0 24px}}
.hero-t{{font-family:'Nunito Sans',sans-serif;font-weight:800;text-transform:uppercase;letter-spacing:.02em;font-size:13px}}
.hero-b{{color:{T[g3]};font-size:12px;margin-left:auto}}
.summary.card{{margin-top:22px}}
.summary{{padding:28px 30px 26px}}
.dateline{{font-size:11.5px;text-transform:uppercase;letter-spacing:.07em;color:{T[g3]};font-weight:600;margin:0 0 12px}}
.head{{font-family:'Nunito Sans',sans-serif;font-weight:900;text-transform:uppercase;letter-spacing:-.03em;line-height:1.08;font-size:27px;margin:0 0 12px;color:{T[ink]};max-width:34ch}}
.deck{{font-size:15px;color:{T[g2]};margin:0;max-width:62ch}}
.chart{{width:100%;height:auto;display:block;margin:22px 0 4px;overflow:visible}}
.ax{{font-family:'Montserrat',sans-serif;font-size:12px;fill:{T[g3]}}}
.ax-y{{text-anchor:end}}
.ax-x{{text-anchor:middle}}
.ax-x.hi{{fill:{T[ink]};font-weight:700}}
.ax-m{{text-anchor:middle;font-size:10px;letter-spacing:.08em;fill:{T[g3]}}}
.mk{{font-family:'Montserrat',sans-serif;font-size:12px;font-weight:600;fill:{T[warning]}}}
.stats{{display:grid;grid-template-columns:repeat(auto-fit,minmax(140px,1fr));gap:0;
       border-top:1px solid {T[line]};margin-top:18px}}
.stat{{padding:16px 18px 2px;border-right:1px solid {T[line]}}}
.stat:last-child{{border-right:0}}
.s-label{{font-size:10.5px;text-transform:uppercase;letter-spacing:.07em;color:{T[g2]};font-weight:700}}
.s-value{{font-family:'Nunito Sans',sans-serif;font-weight:800;font-size:30px;letter-spacing:-.03em;line-height:1.15;margin:4px 0 2px}}
.s-sub{{font-size:12.5px;color:{T[g3]}}}
.card{{background:{T[card]};border-radius:12px;padding:22px 24px;margin-top:26px;box-shadow:0 1px 3px rgba(10,10,10,.08)}}
h2{{font-family:'Nunito Sans',sans-serif;font-weight:800;text-transform:uppercase;letter-spacing:-.02em;font-size:15px;margin:0 0 16px;color:{T[g1]}}}
.note{{margin:-8px 0 16px;font-size:13px;color:{T[g2]}}}
.actions{{list-style:none;margin:0;padding:0}}
.action{{display:flex;gap:12px;align-items:flex-start;padding:13px 0;border-bottom:1px solid {T[line]}}}
.action:last-child{{border-bottom:0;padding-bottom:0}}
.dot{{width:9px;height:9px;border-radius:999px;margin-top:8px;flex:0 0 9px}}
.a-body{{flex:1}}
.a-what{{font-weight:600}}
.a-why{{font-size:13px;color:{T[g2]};margin-top:2px}}
.a-src{{font-size:11px;text-transform:uppercase;letter-spacing:.04em;color:{T[g3]};border:1px solid {T[line]};border-radius:999px;padding:2px 9px;white-space:nowrap;margin-top:4px}}
.method{{font-size:12.5px;color:{T[g2]};background:{T[bg]};border-radius:8px;padding:11px 13px;margin:16px 0 0}}
.cover{{font-weight:700}}
.cover.warn{{color:{T[warning]}}}
.cover.bad{{color:{T[error]}}}
.btns{{display:flex;gap:8px;flex-wrap:wrap;margin-top:10px}}
.btn{{font-family:'Montserrat',sans-serif;font-size:12.5px;font-weight:600;padding:6px 13px;
     border-radius:999px;border:1px solid {T[line]};background:{T[card]};color:{T[g1]};
     cursor:pointer;text-decoration:none;display:inline-block;line-height:1.5}}
.btn:hover:not(:disabled){{border-color:{T[g3]};background:{T[bg]}}}
.btn.primary{{background:{T[green]};border-color:{T[green]};color:{T[black]}}}
.btn.primary:hover:not(:disabled){{background:{T[green_dark]};border-color:{T[green_dark]}}}
.btn:disabled{{opacity:.45;cursor:not-allowed}}
.bridge-note{{display:none;font-size:12.5px;color:{T[g2]};background:{T[card]};border-radius:8px;
             padding:12px 15px;margin-top:22px;border-left:3px solid {T[g3]}}}
.allclear{{background:{T[green_tint]};border-radius:8px;padding:16px 18px;font-weight:600;display:flex;gap:10px;align-items:center}}
.tick{{color:{T[green_dark]};font-size:19px}}
.metrics{{display:grid;grid-template-columns:repeat(auto-fit,minmax(150px,1fr));gap:12px}}
.metric{{background:{T[bg]};border-radius:8px;padding:13px 15px}}
.m-label{{font-size:11px;text-transform:uppercase;letter-spacing:.05em;color:{T[g2]};font-weight:600}}
.m-value{{font-family:'Nunito Sans',sans-serif;font-weight:800;font-size:23px;letter-spacing:-.02em;margin:3px 0 2px;line-height:1.2}}
.m-sub{{font-size:12px;display:flex;gap:7px;align-items:baseline;flex-wrap:wrap}}
.delta{{font-weight:600}}
.delta.up{{color:{T[success]}}} .delta.down{{color:{T[error]}}} .delta.flat{{color:{T[g3]}}}
.vs{{color:{T[g3]}}}
table{{width:100%;border-collapse:collapse;margin-top:18px;font-size:14px}}
th{{text-align:left;background:{T[green_tint]};font-family:'Nunito Sans',sans-serif;font-weight:800;text-transform:uppercase;font-size:11px;letter-spacing:.04em;padding:9px 11px;color:{T[g1]}}}
td{{padding:9px 11px;border-bottom:1px solid {T[line]};vertical-align:top}}
tr:last-child td{{border-bottom:0}}
.num{{text-align:right;white-space:nowrap}}
.stars{{color:{T[warning]};white-space:nowrap;letter-spacing:1px}}
.stars .dim{{color:{T[line]}}}
a{{color:{T[green_dark]};font-weight:600}}
.unavail{{background:{T[bg]};border-left:3px solid {T[g3]};border-radius:0 8px 8px 0;padding:11px 14px;font-size:13.5px;color:{T[g2]};margin-bottom:9px}}
.unavail:last-child{{margin-bottom:0}}
.foot{{text-align:center;color:{T[g3]};font-size:12px;margin-top:26px}}
@media(max-width:620px){{.head{{font-size:23px}} .card{{padding:18px}} .summary{{padding:20px}}
  .stat{{border-right:0;border-bottom:1px solid {T[line]}}} .stat:last-child{{border-bottom:0}}
  .s-value{{font-size:25px}}}}
</style></head>
<body>
<div class="hero"><div class="wrap">{mark}<span class="hero-t">Morning Brief</span>
  <span class="hero-b">{brand}</span>
</div></div>
<div class="wrap">
{body}
<p class="foot">Generated {gen} &middot; Ecommerce Academy</p>
</div></body></html>"""


def main():
    ap = argparse.ArgumentParser(description="Render the morning brief as ECA-styled HTML.")
    ap.add_argument("findings", help="path to the findings JSON")
    ap.add_argument("--out", default="brief.html")
    a = ap.parse_args()
    with open(a.findings, encoding="utf-8") as f:
        data = json.load(f)
    with open(a.out, "w", encoding="utf-8") as f:
        f.write(build(data))
    n = len(data.get("actions", []))
    print("Wrote {} - {} action(s), {} source(s) unavailable".format(
        a.out, n, len(data.get("unavailable", []))))
    return 0


if __name__ == "__main__":
    sys.exit(main())
