#!/usr/bin/env python3
"""Render the customer service brief as ECA-styled HTML.

    python3 build_cs_brief.py findings.json --out cs-brief.html

Deliberately denser than the morning brief: no hero headline, no chart. This is a
working list someone acts on in the next ten minutes. The one thing given real visual
weight is whether the shipping promise is currently true, because every reply written
today contains it.
"""
import argparse
import datetime as dt
import html
import json
import sys

T = {"green": "#3DD62B", "green_dark": "#2FB61F", "green_tint": "#E8FAE6",
     "black": "#0A0A0A", "ink": "#1A1A1A", "g1": "#2C2C2C", "g2": "#555555",
     "g3": "#999999", "line": "#E0E0E0", "bg": "#F5F5F5", "card": "#FFFFFF",
     "warning": "#F5A623", "error": "#D0021B", "warn_tint": "#FDF3E3", "err_tint": "#FBEAEC"}

MARK = ('<svg viewBox="0 0 310 285" fill="none" xmlns="http://www.w3.org/2000/svg" class="mark">'
        '<g stroke="#3DD62B" stroke-width="22" stroke-linejoin="round" stroke-linecap="round">'
        '<path d="M31 254V121M105 254V60M179 254V158"/><path d="M20 254h270"/>'
        '<path d="M120 96 205 40l74 48"/><path d="M279 31v57h-57"/></g></svg>')


def esc(v):
    return html.escape(str(v if v is not None else ""))


def money(v):
    try:
        return "${:,.2f}".format(float(v))
    except (TypeError, ValueError):
        return esc(v)


def hrs(h):
    """One age format for the whole page.

    An earlier version switched to days at 48 hours, so the same order read as
    "92 hrs" in the stat row and "3.8 days" in the table. Two formats for one
    number on one page makes a reader stop and check, which is the opposite of
    what this brief is for.
    """
    try:
        h = float(h)
    except (TypeError, ValueError):
        return esc(h)
    if h < 72:
        return "{:.0f} hrs".format(h)
    return "{:.0f} days".format(round(h / 24))


def card(title, inner, note=None):
    n = '<p class="note">{}</p>'.format(esc(note)) if note else ""
    return '<section class="card"><h2>{}</h2>{}{}</section>'.format(esc(title), n, inner)


def build(d):
    brand = d.get("brand", "Store")
    day = d.get("for_date") or dt.date.today().isoformat()
    try:
        pretty = dt.date.fromisoformat(day).strftime("%A %d %B %Y").replace(" 0", " ")
    except ValueError:
        pretty = day

    parts = []

    # --- the promise. The single most important thing on the page. ---
    pr = d.get("promise") or {}
    if pr:
        ok = bool(pr.get("holding"))
        parts.append(
            '<section class="verdict {}"><div class="v-tag">{}</div>'
            '<div class="v-body"><div class="v-head">{}</div>'
            '<div class="v-sub">{}</div></div></section>'.format(
                "ok" if ok else "bad",
                "Promise holding" if ok else "Promise is false",
                esc(pr.get("headline", "")), esc(pr.get("detail", ""))))

    # --- sentiment ---
    sn = d.get("sentiment") or {}
    if sn:
        gated = bool(sn.get("below_threshold"))
        parts.append(
            '<section class="sent {}"><span class="s-label">Sentiment</span>'
            '<span class="s-read">{}</span><span class="s-why">{}</span></section>'.format(
                "gated" if gated else "", esc(sn.get("read", "")), esc(sn.get("why", ""))))

    # --- the numbers ---
    if d.get("stats"):
        cells = "".join(
            '<div class="stat"><div class="st-l">{}</div><div class="st-v">{}</div>'
            '<div class="st-s">{}</div></div>'.format(
                esc(s.get("label")),
                hrs(s["hours"]) if "hours" in s else esc(s.get("value")),
                esc(s.get("sub", "")))
            for s in d["stats"])
        parts.append('<section class="stats">{}</section>'.format(cells))

    # --- about to complain ---
    ac = d.get("about_to_complain") or {}
    if ac.get("orders"):
        rows = "".join(
            '<tr><td class="mono"><a href="{}" target="_blank" rel="noopener">{}</a></td>'
            '<td>{}</td><td class="num hot">{}</td><td class="num">{}</td></tr>'.format(
                esc(o.get("admin_url", "#")), esc(o.get("name")), esc(o.get("customer")),
                hrs(o.get("hours")), money(o.get("value")))
            for o in ac["orders"])
        parts.append(card("About to complain",
                          '<table><thead><tr><th>Order</th><th>Customer</th>'
                          '<th class="num">Waiting</th><th class="num">Value</th></tr></thead>'
                          '<tbody>{}</tbody></table>'.format(rows),
                          ac.get("note")))
    elif ac:
        parts.append(card("About to complain",
                          '<div class="clear"><span class="tick">&#10003;</span>{}</div>'.format(
                              esc(ac.get("all_clear", "Nobody is past the window.")))))

    # --- inbox queue ---
    ib = d.get("inbox") or {}
    if ib.get("threads"):
        rows = ""
        for t in ib["threads"]:
            flag = ' <span class="pill hot">also overdue</span>' if t.get("also_overdue") else ""
            link = ('<a href="{}" target="_blank" rel="noopener">open</a>'.format(esc(t["url"]))
                    if t.get("url") else "")
            rows += ('<tr><td>{}{}</td><td>{}</td><td><span class="pill">{}</span></td>'
                     '<td class="num">{}</td><td class="num">{}</td></tr>').format(
                esc(t.get("who")), flag, esc(t.get("about")), esc(t.get("category", "")),
                hrs(t.get("hours")), link)
        parts.append(card("Waiting on a reply",
                          '<table><thead><tr><th>Who</th><th>About</th><th>Type</th>'
                          '<th class="num">Waiting</th><th class="num"></th></tr></thead>'
                          '<tbody>{}</tbody></table>'.format(rows), ib.get("note")))
    elif ib:
        parts.append(card("Waiting on a reply",
                          '<div class="clear"><span class="tick">&#10003;</span>{}</div>'.format(
                              esc(ib.get("all_clear", "Nothing waiting.")))))

    # --- housekeeping ---
    if d.get("housekeeping"):
        parts.append(card("Housekeeping", "".join(
            '<div class="hk">{}</div>'.format(esc(x)) for x in d["housekeeping"])))

    return TEMPLATE.format(T=T, mark=MARK, brand=esc(brand), day=esc(day),
                           pretty=esc(pretty), body="\n".join(parts),
                           gen=esc(d.get("generated_at") or
                                   dt.datetime.now().strftime("%Y-%m-%d %H:%M")))


TEMPLATE = """<!doctype html>
<html lang="en"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>{brand} - Customer Service {day}</title>
<link href="https://fonts.googleapis.com/css2?family=Nunito+Sans:wght@700;800;900&family=Montserrat:wght@400;500;600&display=swap" rel="stylesheet">
<style>
:root{{color-scheme:light}}
*{{box-sizing:border-box}}
body{{margin:0;background:{T[bg]};color:{T[ink]};font-family:'Montserrat',system-ui,sans-serif;line-height:1.5;font-size:14px}}
.wrap{{max-width:820px;margin:0 auto;padding:0 18px 48px}}
.hero{{background:{T[black]};color:#fff;padding:14px 0}}
.hero .wrap{{padding-bottom:0;display:flex;align-items:center;gap:10px}}
.mark{{width:22px;flex:0 0 22px}}
.h-t{{font-family:'Nunito Sans',sans-serif;font-weight:800;text-transform:uppercase;letter-spacing:.02em;font-size:12.5px}}
.h-b{{color:{T[g3]};font-size:11.5px;margin-left:auto}}
.verdict{{display:flex;gap:14px;align-items:flex-start;border-radius:12px;padding:16px 18px;margin-top:20px}}
.verdict.bad{{background:{T[err_tint]};border-left:4px solid {T[error]}}}
.verdict.ok{{background:{T[green_tint]};border-left:4px solid {T[green]}}}
.v-tag{{font-family:'Nunito Sans',sans-serif;font-weight:800;text-transform:uppercase;font-size:10.5px;letter-spacing:.06em;white-space:nowrap;padding-top:3px}}
.verdict.bad .v-tag{{color:{T[error]}}}
.verdict.ok .v-tag{{color:{T[green_dark]}}}
.v-head{{font-family:'Nunito Sans',sans-serif;font-weight:800;font-size:17px;letter-spacing:-.02em;line-height:1.25}}
.v-sub{{font-size:13px;color:{T[g2]};margin-top:4px}}
.sent{{background:{T[card]};border-radius:10px;padding:12px 16px;margin-top:12px;display:flex;gap:10px;align-items:baseline;flex-wrap:wrap;box-shadow:0 1px 3px rgba(10,10,10,.06)}}
.s-label{{font-family:'Nunito Sans',sans-serif;font-weight:800;text-transform:uppercase;font-size:10.5px;letter-spacing:.06em;color:{T[g2]}}}
.s-read{{font-weight:600}}
.sent.gated .s-read{{color:{T[g2]};font-weight:500}}
.s-why{{color:{T[g3]};font-size:13px}}
.stats{{display:grid;grid-template-columns:repeat(auto-fit,minmax(130px,1fr));gap:1px;background:{T[line]};border-radius:10px;overflow:hidden;margin-top:12px}}
.stat{{background:{T[card]};padding:12px 14px}}
.st-l{{font-size:10px;text-transform:uppercase;letter-spacing:.06em;color:{T[g2]};font-weight:700}}
.st-v{{font-family:'Nunito Sans',sans-serif;font-weight:800;font-size:21px;letter-spacing:-.02em;margin:2px 0 1px}}
.st-s{{font-size:11.5px;color:{T[g3]}}}
.card{{background:{T[card]};border-radius:12px;padding:16px 18px;margin-top:12px;box-shadow:0 1px 3px rgba(10,10,10,.06)}}
h2{{font-family:'Nunito Sans',sans-serif;font-weight:800;text-transform:uppercase;letter-spacing:-.01em;font-size:12.5px;margin:0 0 10px;color:{T[g1]}}}
.note{{margin:-4px 0 10px;font-size:12.5px;color:{T[g2]}}}
table{{width:100%;border-collapse:collapse;font-size:13.5px}}
th{{text-align:left;background:{T[green_tint]};font-family:'Nunito Sans',sans-serif;font-weight:800;text-transform:uppercase;font-size:10px;letter-spacing:.05em;padding:7px 9px;color:{T[g1]}}}
td{{padding:8px 9px;border-bottom:1px solid {T[line]};vertical-align:middle}}
tr:last-child td{{border-bottom:0}}
.num{{text-align:right;white-space:nowrap}}
.hot{{color:{T[error]};font-weight:700}}
.mono{{font-variant-numeric:tabular-nums;font-weight:600}}
a{{color:{T[green_dark]};font-weight:600;text-decoration:none}}
a:hover{{text-decoration:underline}}
.pill{{display:inline-block;font-size:10.5px;text-transform:uppercase;letter-spacing:.04em;border:1px solid {T[line]};border-radius:999px;padding:1px 8px;color:{T[g2]};white-space:nowrap}}
.pill.hot{{border-color:{T[error]};color:{T[error]}}}
.clear{{background:{T[green_tint]};border-radius:8px;padding:12px 14px;font-weight:600;display:flex;gap:8px;align-items:center}}
.tick{{color:{T[green_dark]};font-size:16px}}
.hk{{font-size:12.5px;color:{T[g2]};padding:5px 0;border-bottom:1px solid {T[line]}}}
.hk:last-child{{border-bottom:0}}
.foot{{text-align:center;color:{T[g3]};font-size:11.5px;margin-top:18px}}
@media(max-width:560px){{.verdict{{flex-direction:column;gap:6px}} .v-head{{font-size:15px}}}}
</style></head>
<body>
<div class="hero"><div class="wrap">{mark}<span class="h-t">Customer Service</span>
  <span class="h-b">{brand} &middot; {pretty}</span></div></div>
<div class="wrap">
{body}
<p class="foot">Generated {gen} &middot; Ecommerce Academy</p>
</div></body></html>"""


def main():
    ap = argparse.ArgumentParser(description="Render the CS brief as ECA-styled HTML.")
    ap.add_argument("findings")
    ap.add_argument("--out", default="cs-brief.html")
    a = ap.parse_args()
    with open(a.findings, encoding="utf-8") as f:
        data = json.load(f)
    with open(a.out, "w", encoding="utf-8") as f:
        f.write(build(data))
    print("Wrote {}".format(a.out))
    return 0


if __name__ == "__main__":
    sys.exit(main())
