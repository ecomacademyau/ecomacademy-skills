#!/usr/bin/env python3
"""Build a creator brief (HTML, prints to A4 PDF) from a JSON file.

usage:
  python3 build_brief.py brief.json --out brief.html [--pdf] [--competitors "Brand A,Brand B"]

The JSON shape is shown in ../assets/brief-example.json. Required: brand.name, product.name, format.name,
idea, ideas (at least one, each with openers and talking_points). Everything else is optional and has a
sensible default for one-take formats (filming notes, dos and don'ts, what to send, quick check).

Light markup inside any text: **bold**, and [your detail] renders as a fill-in gap.

Safety checks (the brief goes to a creator, not the member):
  - an em dash anywhere stops the build (exit 2)
  - words that don't belong in a creator brief (CPA, ROAS, CPM, margin, spend, hook rate, deadline,
    competitor names passed with --competitors) are listed as warnings
"""
import argparse, html, json, os, re, shutil, subprocess, sys

INTERNAL = ['cpa', 'roas', 'cpm', 'ctr', 'margin', 'ad spend', 'budget', 'hook rate', 'hold rate', 'thruplay',
            'frequency', 'kill cpa', 'target cpa', 'deadline', 'post this', 'post it on', 'competitor', 'scorecard',
            'funnel', 'tof', 'mof', 'bof', 'retargeting', 'conversion rate']

DEFAULT_FILMING = [
    'Film straight through, vertical (9:16). Move around, grab the product, call someone in. It all happens in the same take.',
    'If you need a cut, make it one nobody notices. No jump cuts, text-heavy edits or music. Stumble? Laugh and keep going.',
    'Real and confident. Talk like you love it and you are happy to tell people. Watch the examples first.',
    'Natural window light. No ring light, filters or beauty mode. Phone at eye level. Quiet room, your voice first.',
]


def default_filming(d):
    """'Watch the examples first' only when there are examples to watch.

    A brief with no examples (the usual case: only videos someone has actually watched
    may be listed) would otherwise tell the creator to watch something that isn't there.
    """
    if d.get('examples'):
        return DEFAULT_FILMING
    return [line.replace(' Watch the examples first.', '') for line in DEFAULT_FILMING]


DEFAULT_DOS = ['Talk to your phone like it is a friend', 'Use your real details', 'Hold the product still for the close-ups',
               'Keep the offer to one relaxed line at the end']
DEFAULT_DONTS = ['Open with the brand name, the logo or the deal', 'Push the deal: no "hurry", "only this week" or "selling out"',
                 'Promise delivery dates, results or refunds', 'Read it off a screen', 'Use "POV:" openers']
DEFAULT_SEND = ['One full take for each opening line you film', 'Optional extra footage and photos', 'Everything raw and unedited']
DEFAULT_CHECK = ['One take, no cuts or very minimal', 'Product front held 2 seconds', 'Two close-ups', 'Product in use',
                 'Brand and offer said once, at the end', 'Vertical, unfiltered, voice clear']


def esc(s):
    s = html.escape(str(s or ''))
    s = re.sub(r'\*\*(.+?)\*\*', r'<strong>\1</strong>', s)
    s = re.sub(r'\[([^\]]+)\]', r'<span class="fill">[\1]</span>', s)
    return s


def li(items):
    return ''.join(f'<li>{esc(x)}</li>' for x in items or [])


def walk_strings(o, path=''):
    if isinstance(o, dict):
        for k, v in o.items():
            yield from walk_strings(v, f'{path}.{k}' if path else k)
    elif isinstance(o, list):
        for i, v in enumerate(o):
            yield from walk_strings(v, f'{path}[{i}]')
    elif isinstance(o, str):
        yield path, o


def check(data, competitors):
    errs, warns = [], []
    for p, s in walk_strings(data):
        if p.endswith(('url', 'thumb', 'logo')) or '.url' in p:
            continue
        if '\u2014' in s:
            errs.append(f'{p}: em dash: {s[:80]}')
        low = s.lower()
        for w in INTERNAL + [c.lower() for c in competitors]:
            if w and re.search(r'(?<![a-z])' + re.escape(w) + r'(?![a-z])', low):
                warns.append(f'{p}: "{w}" does not belong in a creator brief: {s[:80]}')
    return errs, warns


def font_link(fonts):
    fams = [f for f in (fonts.get('heading'), fonts.get('body')) if f]
    if not fams:
        return ''
    q = '&'.join('family=' + f.replace(' ', '+') + ':wght@400;600;700' for f in dict.fromkeys(fams))
    return f'<link href="https://fonts.googleapis.com/css2?{q}&display=swap" rel="stylesheet">'


def example_card(ex):
    url = ex.get('url') or '#'
    thumb = ex.get('thumb')
    if thumb:
        visual = f'<img src="{html.escape(thumb, quote=True)}" alt="">'
    else:
        visual = '<div class="play"><span>&#9654;</span></div>'
    return (f'<a class="ex" href="{html.escape(url, quote=True)}" target="_blank" rel="noopener">'
            f'<div class="thumb">{visual}<div class="badge">&#9654; Watch</div></div>'
            f'<div class="exbody"><h3>{esc(ex.get("title"))}</h3>'
            + (f'<p class="q">"{esc(ex.get("opening_line"))}"</p>' if ex.get('opening_line') else '')
            + (f'<p>{esc(ex.get("why"))}</p>' if ex.get('why') else '') + '</div></a>')


def build(d):
    b, pr, fm = d['brand'], d['product'], d['format']
    col = b.get('colours', {}) or b.get('colors', {})
    fonts = b.get('fonts', {})
    brand_c, accent_c = col.get('brand', '#111111'), col.get('accent', '#2F6FEB')
    head_f = f"'{fonts['heading']}'," if fonts.get('heading') else ''
    body_f = f"'{fonts['body']}'," if fonts.get('body') else ''
    title = f"Your {pr['name']} brief | {fm['name']}"
    # The ECA credit is built in. It used to be a manual find-and-replace after building,
    # which is exactly the kind of step that gets skipped on the third brief of a round.
    foot = lambda n: f'<div class="foot"><span>{esc(b["name"])} · Prepared by Ecommerce Academy</span><span>{esc(title)} · {n}</span></div>'
    site = b.get('site_url', '')
    site_dom = re.sub(r'^https?://(www\.)?', '', site).rstrip('/')
    pages = []

    # cover
    shape = ''.join(f'<li><b>{esc(s.get("beat"))}:</b> {esc(s.get("text"))}</li>' for s in d.get('shape', []))
    logo = f'<img class="logo" src="{html.escape(b["logo"], quote=True)}" alt="{esc(b["name"])}">' if b.get('logo') else f'<div class="wordmark">{esc(b["name"])}</div>'
    it_is = li(d.get('it_is') or ['You, talking straight to your phone, in your own words', 'One take, showing the product as you go', 'A bit chatty, a bit messy. That is the point'])
    it_isnt = li(d.get('it_isnt') or ['An ad read, or reading off a screen', 'A list of features', 'An edited video with cuts, music or lots of text', 'A hard sell'])
    pages.append(f'''<section class="page">
 <div class="top">{logo}</div>
 <h1>{esc(title)}</h1>
 <p class="hello">{esc(d.get("greeting") or "Hey there!")}</p>
 <p>{esc(d.get("hello") or "Thanks so much for doing this. None of it needs to be perfect: real beats polished every time.")}</p>
 <div class="intro"><h3>Who we are</h3>
  <p>{esc(b["name"])}{f' (<a href="{html.escape(site, quote=True)}">{esc(site_dom)}</a>)' if site else ''}. This one is our <strong>{esc(pr["name"])}</strong>: {esc(pr.get("what_it_is"))} {esc(pr.get("what_makes_it_different"))} It's for {esc(pr.get("who_its_for"))}{f' <a href="{html.escape(pr["url"], quote=True)}">See the product &rsaquo;</a>' if pr.get("url") else ''}</p></div>
 <p class="meta">Length: <strong>{esc(fm.get("length", "30 to 60 seconds"))}</strong> · Format: vertical 9:16 · <strong>{esc(fm.get("delivery", "one take, no cuts or very minimal"))}</strong></p>
 <div class="sec"><h2>The idea</h2><p class="goal">{esc(d["idea"])}</p></div>
 <div class="sec"><h2>What we mean by a "{esc(fm["name"].lower())}" video</h2>
  <div class="cols"><div><h3>It is</h3><ul>{it_is}</ul></div><div><h3>It isn't</h3><ul>{it_isnt}</ul></div></div></div>
 {f'<div class="sec"><h2>The shape of the video</h2><p class="muted">Told like a chat with a friend, not a pitch. No greeting, start straight into it.</p><ol>{shape}</ol></div>' if shape else ''}
 {foot(1)}
</section>''')

    # page 2
    must = ''.join(f'<li><span class="fixed">{esc(m.get("text"))}</span> {esc(m.get("how", ""))}</li>' for m in d.get('must_say', []))
    must += f'<li><span class="fixed">{esc(b["name"])}, said once near the end with the offer</span>, never in your first line or when you first show the product.</li>'
    if d.get('offer_line'):
        must += f'<li><span class="fixed">The offer, casually, right at the end:</span> "{esc(d["offer_line"])}" That\'s it. No hurry.</li>'
    exs = ''.join(example_card(e) for e in d.get('examples', []))
    shots = d.get('shots', {})
    in_take = shots.get('in_take') or ['Hold the product front to camera for 2 seconds', 'A close-up of the main detail', 'Using or touching it']
    extras = shots.get('extras') or []
    n_ideas = len(d['ideas'])
    word = {1: 'One idea', 2: 'Two ideas', 3: 'Three ideas'}.get(n_ideas, f'{n_ideas} ideas')
    pages.append(f'''<section class="page">
 <div class="sec"><h2>Things to get in, in your own words</h2><ul>{must}</ul></div>
 <div class="sec"><h2>{word} to film</h2><p>{'Pick the one that sounds most like you, or film more than one. ' if n_ideas > 1 else ''}Learn the points, then say it your way with your real details. The opening lines are the one bit to say word for word: do one full take for each.</p></div>
 {f'<div class="sec"><h2>Watch these first</h2><p class="muted">Tap to watch. Different products maybe, but the energy we are after.</p><div class="exs">{exs}</div></div>' if exs else ''}
 <div class="sec"><h2>The shots we need</h2><div class="cols">
  <div><h3>Inside your one take</h3><ol>{li(in_take)}</ol></div>
  {f'<div><h3>Optional extra footage</h3><p class="muted">If you have it, send it. It is not part of the main video.</p><ul>{li(extras)}</ul></div>' if extras else ''}
 </div></div>
 {foot(2)}
</section>''')

    # idea pages
    for n, idea in enumerate(d['ideas'], 1):
        rows = ''.join(f'<tr><td>"{esc(o.get("say"))}"</td><td>{esc(o.get("show"))}</td><td>{esc(o.get("on_screen"))}</td></tr>' for o in idea.get('openers', []))
        tps = ''.join(f'<dt>{esc(t.get("beat"))}</dt><dd>{esc(t.get("text"))}</dd>' for t in idea.get('talking_points', []))
        ss = idea.get('sample_script') or {}
        sl = ''
        for ln in ss.get('lines', []):
            stage = f' <span class="stage">({esc(ln["stage"])})</span>' if ln.get('stage') else ''
            sl += f'<p>{esc(ln.get("say"))}{stage}</p>'
        sample = (f'<div class="sec"><h3>Here\'s one way it could sound. Say it your way, don\'t read it word for word.</h3>'
                  f'<div class="script"><div class="note">About {esc(ss.get("seconds", ""))} seconds, <strong>one take</strong>. Only say what\'s true for you.</div>{sl}</div></div>') if sl else ''
        pages.append(f'''<section class="page">
 <div class="label">Idea {n}</div>
 <h2 class="ideaname">{esc(idea.get("name"))}</h2>
 {f'<p class="muted">{esc(idea.get("summary"))}</p>' if idea.get("summary") else ''}
 <div class="sec"><h3>Opening lines: say one word for word, then carry on in your own words</h3>
  <table class="open"><tr><th>Say</th><th>Show</th><th>On screen</th></tr>{rows}</table></div>
 <div class="sec"><h3>Talking points</h3><dl class="tp">{tps}</dl></div>
 {sample}
 <div class="cols">
  <div><h3>Shots for this idea</h3><ul>{li(idea.get("shots") or ["As on page 2"])}</ul></div>
  <div><h3>Watch out for</h3><ul>{li(idea.get("watch_outs") or ["Only say what is true for you"])}</ul></div>
 </div>
 {foot(2 + n)}
</section>''')

    # last page
    send = d.get('send', {})
    naming = send.get('file_naming') or f"{re.sub(r'[^A-Za-z0-9]', '', b['name'])[:12]}_Idea1_Opening1_YourName.mp4"
    pages.append(f'''<section class="page">
 <div class="sec"><h2>{esc(d.get("filming_title") or "One take. Like you are sending a friend a video.")}</h2><ul>{li((d.get("filming") or default_filming(d)) + d.get("filming_extra", []))}</ul></div>
 <div class="sec"><h2>A few dos and don'ts</h2><div class="cols">
  <div><h3>Please do</h3><ul>{li(DEFAULT_DOS + d.get("dos", []))}</ul></div>
  <div><h3>Please don't</h3><ul>{li(DEFAULT_DONTS + d.get("donts", []))}</ul></div></div></div>
 <div class="sec"><h2>What to send us</h2><ul>{li(send.get("items") or DEFAULT_SEND)}</ul><p>Name files like <code>{esc(naming)}</code></p></div>
 <div class="sec"><h2>Quick check before you send</h2><div class="check">{''.join(f'<div>&#9744; {esc(c)}</div>' for c in (d.get("checklist") or DEFAULT_CHECK))}</div></div>
 <div class="sec"><p>Just send us the files, no need to post anything yourself. Thank you! The realer it is, the better it works.</p>
  <p class="sign">{esc(d.get("sign_off") or "Thanks heaps, " + b["name"])}</p></div>
 {foot(3 + n_ideas)}
</section>''')

    css = f'''@page{{size:A4;margin:0}}
:root{{--brand:{brand_c};--accent:{accent_c};--ink:#1A1A1A;--muted:#5A5A5A;--faint:#8A8A8A;--line:#E4E4E4;--paper:#FFFFFF;
--head:{head_f}'Helvetica Neue',Arial,sans-serif;--body:{body_f}'Helvetica Neue',Arial,sans-serif}}
*{{box-sizing:border-box}}
html{{background:#EEECE8}}
body{{margin:0;font:11px/1.65 var(--body);color:var(--ink);-webkit-print-color-adjust:exact;print-color-adjust:exact}}
.page{{width:210mm;min-height:297mm;padding:17mm 20mm 22mm;margin:8mm auto;background:var(--paper);position:relative;box-shadow:0 1px 6px rgba(0,0,0,.08);page-break-after:always;break-after:page}}
.page:last-child{{page-break-after:auto;break-after:auto}}
@media print{{html{{background:none}}.page{{margin:0;box-shadow:none}}}}
@media (max-width:800px){{.page{{width:auto;min-height:0;margin:0 0 12px;padding:24px 16px 48px}}.cols,.exs{{grid-template-columns:1fr !important}}}}
h1,h2,h3{{font-family:var(--head);color:var(--brand);margin:0}}
h1{{font-size:30px;line-height:1.1;font-weight:700;margin:10mm 0 5mm}}
h2{{font-size:17px;line-height:1.2;font-weight:700;margin:0 0 3mm}}
h3{{font-size:11.5px;font-weight:700;margin:0 0 2mm}}
p{{margin:0 0 2.4mm}}
.sec{{margin:0 0 8mm}}
.muted,.meta{{color:var(--muted)}}
.logo{{height:12mm}}
.wordmark{{font:700 14px var(--head);letter-spacing:.06em;text-transform:uppercase;color:var(--brand)}}
.hello{{font-weight:700;font-size:14px;color:var(--brand);margin:0 0 2mm}}
.intro{{border-top:1px solid var(--line);border-bottom:1px solid var(--line);padding:4mm 0;margin:5mm 0 4mm}}
a{{color:var(--accent);text-decoration:none;font-weight:600}}
.goal{{font-size:14px;line-height:1.55;font-weight:500;color:var(--brand)}}
.cols{{display:grid;grid-template-columns:1fr 1fr;gap:10mm}}
ul,ol{{margin:0;padding-left:5mm}}li{{margin:1.2mm 0}}
ol li::marker{{color:var(--accent);font-weight:700}}
.fixed{{font-weight:700;color:var(--brand)}}
.exs{{display:grid;grid-template-columns:1fr 1fr;gap:6mm}}
a.ex{{display:flex;gap:4mm;color:inherit;font-weight:400;border:1px solid var(--line);border-radius:3mm;padding:3mm;align-items:flex-start}}
a.ex:hover{{border-color:var(--accent)}}
.thumb{{position:relative;flex:0 0 22mm;height:39mm;border-radius:2mm;overflow:hidden;background:#1A1A1A}}
.thumb img{{width:100%;height:100%;object-fit:cover;display:block}}
.play{{width:100%;height:100%;display:flex;align-items:center;justify-content:center;background:linear-gradient(160deg,var(--brand),#000)}}
.play span{{color:#fff;font-size:22px;opacity:.9}}
.badge{{position:absolute;left:1.5mm;bottom:1.5mm;background:rgba(0,0,0,.65);color:#fff;font-size:8px;font-weight:700;padding:.6mm 1.6mm;border-radius:1mm}}
.exbody h3{{margin-top:.5mm}}
.q{{font-style:italic;color:var(--muted)}}
.label{{font-size:8.5px;font-weight:700;letter-spacing:.16em;text-transform:uppercase;color:var(--accent);margin-bottom:1.5mm}}
.ideaname{{font-size:24px;margin-bottom:4mm}}
table.open{{width:100%;border-collapse:collapse;margin-top:1mm}}
table.open th{{font-size:8.5px;font-weight:700;letter-spacing:.12em;text-transform:uppercase;color:var(--accent);text-align:left;padding:1.6mm 2mm;border-bottom:1px solid var(--line)}}
table.open td{{vertical-align:top;padding:2.2mm 2mm;border-bottom:1px solid var(--line)}}
table.open td:first-child{{font-weight:600;color:var(--brand);width:42%}}
.tp{{display:grid;grid-template-columns:34mm 1fr;gap:1.6mm 4mm;margin:0}}
.tp dt{{font-size:8.5px;font-weight:700;line-height:2;letter-spacing:.1em;text-transform:uppercase;color:var(--accent)}}
.tp dd{{margin:0}}
.script{{border-left:2px solid var(--accent);padding:1mm 0 1mm 6mm;margin-top:2mm}}
.script .note{{font-size:9.5px;color:var(--faint);margin:0 0 2.5mm}}
.script p{{font-size:11.5px;line-height:1.7}}
.stage{{color:var(--faint);font-style:italic;font-size:9.5px}}
.fill{{color:var(--muted);border-bottom:1px dotted #999}}
.check{{columns:2;column-gap:10mm}}.check div{{margin:0 0 1.8mm}}
code{{font:500 9.5px ui-monospace,Menlo,monospace;color:var(--muted)}}
.foot{{position:absolute;bottom:9mm;left:20mm;right:20mm;display:flex;justify-content:space-between;font-size:8px;letter-spacing:.08em;text-transform:uppercase;color:var(--faint)}}
.sign{{font:700 15px var(--head);color:var(--brand);margin-top:3mm}}'''
    return f'''<!doctype html>
<html lang="en-AU"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>{esc(title)}</title>{font_link(fonts)}<style>{css}</style></head>
<body>{''.join(pages)}</body></html>'''


def to_pdf(html_path, pdf_path):
    try:
        from playwright.sync_api import sync_playwright
        with sync_playwright() as p:
            br = p.chromium.launch()
            pg = br.new_page()
            pg.goto('file://' + os.path.abspath(html_path))
            pg.wait_for_timeout(800)
            pg.pdf(path=pdf_path, format='A4', print_background=True, margin={'top': '0', 'bottom': '0', 'left': '0', 'right': '0'})
            br.close()
        return True
    except Exception:
        pass
    for c in [os.environ.get('CHROME_PATH'), 'google-chrome', 'chromium', 'chromium-browser', 'chrome',
              '/Applications/Google Chrome.app/Contents/MacOS/Google Chrome']:
        if c and (shutil.which(c) or os.path.exists(c)):
            r = subprocess.run([shutil.which(c) or c, '--headless=new', '--no-pdf-header-footer',
                                f'--print-to-pdf={pdf_path}', 'file://' + os.path.abspath(html_path)], capture_output=True)
            if r.returncode == 0 and os.path.exists(pdf_path):
                return True
    return False


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument('json')
    ap.add_argument('--out', required=True)
    ap.add_argument('--pdf', action='store_true')
    ap.add_argument('--competitors', default='')
    a = ap.parse_args()
    d = json.load(open(a.json, encoding='utf-8'))
    for k in ('brand', 'product', 'format', 'idea', 'ideas'):
        if k not in d:
            sys.exit(f'Missing "{k}" in {a.json}. See assets/brief-example.json.')
    errs, warns = check(d, [c.strip() for c in a.competitors.split(',') if c.strip()])
    for w in warns:
        print('WARN   ' + w)
    if errs:
        for e in errs:
            print('ERROR  ' + e)
        sys.exit(2)
    with open(a.out, 'w', encoding='utf-8') as fh:
        fh.write(build(d))
    print(f'Wrote {a.out}')
    if a.pdf:
        pdf = re.sub(r'\.html?$', '', a.out) + '.pdf'
        if to_pdf(a.out, pdf):
            print(f'Wrote {pdf}')
        else:
            print('No headless browser found. Open the HTML in Chrome > Print > Save as PDF (A4, margins none, background graphics on).')


if __name__ == '__main__':
    main()
