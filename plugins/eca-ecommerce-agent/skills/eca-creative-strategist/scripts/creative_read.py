#!/usr/bin/env python3
"""Creative read of a Meta ad account from an Ads Manager CSV export (or CSVs written from Meta Ads MCP pulls).

usage:
  python3 creative_read.py ads_30d.csv [--daily campaign_daily_7d.csv] [--compare ads_7d.csv]
                           [--target-cpa 45] [--currency AUD] [--min-impressions 1000] [--out creative-read.md]

  ads_30d.csv      ad-level export for the main window (last 30 days is best). Rows per ad, or per ad per day.
  --daily          campaign-level export with a Day column (Breakdown > By time > Day), last 7 days. Powers the funnel read.
  --compare        a second ad-level export for a shorter window (last 7 days) to spot fatigue and trend.
  --target-cpa     the member's target CPA. Without it, ads are judged against their campaign's own blended CPA.

What it does (creative questions only; budget and scaling verdicts belong to the 4PI analysis):
  - groups ads into product lines by landing page
  - hook rate, hold rate, link CTR, purchases per click, CPA, ROAS per ad
  - the minimum-data bar before any verdict
  - each ad's first drop-off (hook, body, CTA/offer, post-click), using the same bands as the 4PI framework
  - winners to iterate, fatigue signals (with --compare), funnel stage per campaign (with --daily)
  - landing pages converting far worse than another page in the same campaign (not a script problem)
  - an angle-tagging table for you to fill in

Column names are matched case-insensitively against Ads Manager names and plain names
(ad name, campaign name, ad set name, delivery, landing url, spend, purchases, revenue, impressions,
reach, frequency, cpm, 3s plays, thruplays, link clicks, day).
"""
import argparse, csv, re, statistics, sys
from collections import defaultdict
from urllib.parse import urlparse

ALIASES = {
    'ad': ['ad name', 'ad_name', 'name'],
    'campaign': ['campaign name', 'campaign_name', 'campaign'],
    'adset': ['ad set name', 'adset name', 'ad_set_name', 'adset_name'],
    'delivery': ['delivery', 'ad delivery', 'delivery status', 'effective_status', 'status'],
    'url': ['landing url', 'landing_url', 'website url', 'link (ad settings)', 'link', 'url', 'link_url', 'destination url'],
    'spend': ['amount spent', 'spend', 'amount_spent'],
    'purchases': ['purchases', 'website purchases', 'actions:omni_purchase', 'results'],
    'result_type': ['result indicator', 'result type'],
    'revenue': ['purchases conversion value', 'website purchases conversion value', 'revenue', 'conversion value',
                'purchase conversion value'],
    'aov': ['average purchases conversion value', 'aov'],
    'roas': ['purchase roas (return on ad spend)', 'purchase roas', 'roas', 'website purchase roas', 'purchase_roas',
             'website purchase roas (return on advertising spend)'],
    'impr': ['impressions'],
    'reach': ['reach'],
    'freq': ['frequency'],
    'cpm': ['cpm (cost per 1,000 impressions)', 'cpm'],
    'p3': ['3-second video plays', '3 second video plays', '3s plays', 'plays_3s', '3_second_video_plays',
           'video_continuous_2_sec_watched_actions', '2-second continuous video plays'],
    'thumbstop': ['thumb stop ratio', 'thumbstop ratio', 'hook rate'],
    'thru': ['thruplays', 'thruplay', 'video_thruplay_watched_actions'],
    'clicks': ['link clicks', 'link_clicks', 'actions:link_click', 'outbound clicks'],
    # Only a real daily breakdown counts. Every export has "Reporting starts", so it is not a day column.
    'day': ['day', 'date', 'date_start'],
}

HOOK_BANDS = (20, 30)
HOLD_BANDS = (15, 25)
CTR_WEAK = 0.5
CTR_STRONG = 1.0


def num(v):
    if v is None:
        return 0.0
    s = str(v).strip()
    if s.lower() in ('', '-', 'n/a', 'not available', 'none'):
        return 0.0
    s = s.split('(')[0]
    s = re.sub(r'[^\d.\-]', '', s.replace(',', ''))
    try:
        return float(s) if s not in ('', '-', '.') else 0.0
    except ValueError:
        return 0.0


def find_cols(header):
    h = {c.lower().strip(): c for c in header if c}
    out = {}
    for key, names in ALIASES.items():
        for n in names:
            hit = next((orig for low, orig in h.items()
                        if low == n or low.startswith(n + ' (') or low.startswith(n + ' [')), None)
            if hit:
                out[key] = hit
                break
    # 'name' alone is ambiguous when campaign/ad set name columns also exist: only use it for ad if nothing else matched
    return out


def read_csv(path):
    with open(path, newline='', encoding='utf-8-sig') as fh:
        rows = [r for r in csv.DictReader(fh)]
    if not rows:
        sys.exit(f'{path}: empty CSV.')
    return rows, find_cols(rows[0].keys())


def line_of(url):
    if not url:
        return '(no landing URL)'
    p = urlparse(url if '//' in url else 'https://' + url)
    parts = [x for x in p.path.split('/') if x]
    for key in ('products', 'collections', 'pages'):
        if key in parts and parts.index(key) + 1 < len(parts):
            return f"{key[:-1]}: {parts[parts.index(key) + 1]}"
    return (p.netloc + '/' + '/'.join(parts[:2])).rstrip('/') or p.netloc


def page_of(url):
    if not url:
        return '(no landing URL)'
    p = urlparse(url if '//' in url else 'https://' + url)
    return (p.netloc + p.path).rstrip('/')


def pct(a, b):
    return (a / b * 100) if b else None


def band(v, lo, hi):
    if v is None:
        return 'n/a'
    return 'weak' if v < lo else ('OK' if v <= hi else 'strong')


def t(x, n=None):
    x = str(x or '')
    x = x[:n] if n else x
    return x.replace('|', '/')


def money(v, cur):
    return '-' if v is None else f'{cur}{v:,.2f}'


def f(v, d=1, suf=''):
    return '-' if v is None else f'{v:,.{d}f}{suf}'


def aggregate(rows, c):
    ads = defaultdict(lambda: defaultdict(float))
    meta = {}
    days = defaultdict(set)
    warn = []
    if 'purchases' in c and c['purchases'].lower().startswith('results') and 'result_type' in c:
        types = {(r.get(c['result_type']) or '').lower() for r in rows}
        if types and not any('purchase' in t for t in types if t):
            warn.append(f'"Results" column holds {", ".join(sorted(t for t in types if t)) or "unknown"}, not purchases. Purchase numbers below may be wrong.')
    for r in rows:
        name = (r.get(c['ad']) or '').strip()
        if not name or name.lower().startswith(('total', 'results from')):
            continue
        g = ads[name]
        for k in ('spend', 'purchases', 'revenue', 'impr', 'p3', 'thru', 'clicks', 'reach'):
            if k in c:
                g[k] += num(r.get(c[k]))
        if 'revenue' not in c:
            if 'aov' in c:
                g['revenue'] += num(r.get(c['aov'])) * num(r.get(c['purchases'])) if 'purchases' in c else 0
            elif 'roas' in c:
                g['revenue'] += num(r.get(c['roas'])) * num(r.get(c['spend']))
        if 'p3' not in c and 'thumbstop' in c:
            g['p3'] += num(r.get(c['thumbstop'])) / 100 * num(r.get(c['impr'])) if 'impr' in c else 0
        if 'freq' in c and 'impr' in c:
            g['freq_w'] += num(r.get(c['freq'])) * num(r.get(c['impr']))
        m = meta.setdefault(name, {})
        if 'url' in c and r.get(c['url']):
            m['url'] = r[c['url']]
        if 'campaign' in c and r.get(c['campaign']):
            m['campaign'] = r[c['campaign']]
        if 'adset' in c and r.get(c['adset']):
            m['adset'] = r[c['adset']]
        if 'delivery' in c and r.get(c['delivery']):
            m['delivery'] = r[c['delivery']]
        if 'day' in c and num(r.get(c['spend'])) > 0:
            days[name].add(r.get(c['day']))
    return ads, meta, days, warn


def build(ads, meta, days):
    res = []
    for name, g in ads.items():
        m = meta.get(name, {})
        video = g['p3'] > 0 or g['thru'] > 0
        r = dict(ad=name, campaign=m.get('campaign', '(no campaign)'), adset=m.get('adset', ''),
                 delivery=m.get('delivery', ''), url=m.get('url', ''), line=line_of(m.get('url')), page=page_of(m.get('url')),
                 spend=g['spend'], purchases=g['purchases'], impr=g['impr'], clicks=g['clicks'], revenue=g['revenue'],
                 cpa=(g['spend'] / g['purchases']) if g['purchases'] else None,
                 roas=(g['revenue'] / g['spend']) if g['spend'] and g['revenue'] else None,
                 hook=pct(g['p3'], g['impr']) if video else None,
                 hold=pct(g['thru'], g['p3']) if video and g['p3'] else None,
                 ctr=pct(g['clicks'], g['impr']) if g['clicks'] else (0.0 if g['impr'] else None),
                 ppc=(g['purchases'] / g['clicks']) if g['clicks'] else None,
                 freq=(g['freq_w'] / g['impr']) if g.get('freq_w') and g['impr'] else None,
                 video=video, days=len(days.get(name, ())) if days else None)
        res.append(r)
    res.sort(key=lambda r: -r['spend'])
    return res


def judge(res, target, min_impr, bad_pages=None):
    bad_pages = bad_pages or {}
    by_camp = defaultdict(list)
    for r in res:
        by_camp[r['campaign']].append(r)
    camp_info = {}
    for cn, rs in by_camp.items():
        sp = sum(x['spend'] for x in rs)
        pu = sum(x['purchases'] for x in rs)
        ppcs = [x['ppc'] for x in rs if x['ppc'] is not None and x['clicks'] >= 20]
        camp_info[cn] = dict(spend=sp, purchases=pu, cpa=(sp / pu) if pu else None,
                             ppc_median=statistics.median(ppcs) if len(ppcs) >= 2 else None, ads=len(rs))
    for r in res:
        ci = camp_info[r['campaign']]
        bar_cpa = target or ci['cpa']
        r['share'] = pct(r['spend'], ci['spend'])
        r['enough_rates'] = r['impr'] >= min_impr
        r['enough_conv'] = bool(bar_cpa) and r['spend'] >= 2 * bar_cpa and (r['days'] is None or r['days'] >= 7)
        r['bar'] = f"spend >= 2x {'target' if target else 'campaign'} CPA ({2 * bar_cpa:,.0f})" if bar_cpa else 'no purchases in campaign to set a bar'
        steps = []
        if not r['enough_rates']:
            r['dropoff'] = f'Too few impressions to read (under {min_impr:,})'
            continue
        if r['video']:
            if r['hook'] is not None and r['hook'] < HOOK_BANDS[0]:
                steps.append('Hook: first 2 seconds not stopping the scroll. New spoken, visual and text hooks on this body')
            elif r['hold'] is not None and r['hold'] < HOLD_BANDS[0]:
                steps.append('Body: hook works, the middle loses them. Reveal the product earlier, cut filler, re-hook every 5 to 8s')
        if not steps and r['ctr'] is not None and r['ctr'] < CTR_WEAK:
            steps.append('CTA or offer: they watch but don\'t click')
        bp = bad_pages.get((r['campaign'], r['page']))
        if not steps and bp and r['clicks'] >= 40:
            steps.append(f"Post-click: this ad's landing page converts {bp[0]*100:.1f}% of clicks vs {bp[1]*100:.1f}% on {bp[2]} in the same campaign. Landing page, NOT a script problem")
        if not steps and r['ppc'] is not None and ci['ppc_median'] and r['clicks'] >= 40 and r['ppc'] < 0.6 * ci['ppc_median']:
            steps.append(f"Post-click: clicks fine, purchases per click {r['ppc']*100:.1f}% vs campaign median {ci['ppc_median']*100:.1f}%. Landing page or offer, NOT a script problem")
        if not steps and r['enough_conv'] and bar_cpa and r['cpa'] and r['cpa'] > 1.3 * bar_cpa and (r['hold'] or 0) >= HOLD_BANDS[0]:
            steps.append('Angle or offer: holds attention but buyers don\'t follow. Bring the reason to buy and the offer earlier, or change the angle')
        if not steps and r['enough_conv'] and r['purchases'] == 0:
            steps.append('No purchases past the data bar. Check position (TOF ads can earn this) before calling it')
        r['dropoff'] = steps[0] if steps else 'No creative drop-off flagged'
    return camp_info


def winners(res, target, camp_info):
    out = []
    for r in res:
        bar = target or camp_info[r['campaign']]['cpa']
        if r['enough_conv'] and r['cpa'] is not None and bar and r['cpa'] <= bar:
            out.append(r)
    return out


def page_gaps(res):
    """Pages in the same campaign where one converts clicks far worse than another (both with enough clicks)."""
    by = defaultdict(lambda: defaultdict(lambda: dict(clicks=0.0, purchases=0.0, ads=0)))
    for r in res:
        p = by[r['campaign']][r['page']]
        p['clicks'] += r['clicks']; p['purchases'] += r['purchases']; p['ads'] += 1
    flags = []
    for cn, pages in by.items():
        ok = {pg: v for pg, v in pages.items() if v['clicks'] >= 100}
        if len(ok) < 2:
            continue
        rates = {pg: v['purchases'] / v['clicks'] for pg, v in ok.items()}
        best = max(rates, key=rates.get)
        for pg, rt in rates.items():
            if pg != best and rates[best] > 0 and rt < 0.5 * rates[best]:
                flags.append((cn, pg, rt, best, rates[best], ok[pg]['clicks'], ok[best]['clicks']))
    return flags


def format_guess(name, video):
    n = name.lower()
    tags = [('founder', 'founder'), ('yap', 'yapper'), ('ugc', 'ugc'), ('demo', 'demo'), ('review', 'testimonial'),
            ('testimonial', 'testimonial'), ('unbox', 'unboxing'), ('3 reasons', '3 reasons'), ('3reasons', '3 reasons'),
            ('vs', 'us vs them'), ('comment', 'comment reply'), ('static', 'static'), ('image', 'static'),
            ('carousel', 'carousel'), ('catalog', 'catalog'), ('dpa', 'catalog')]
    for k, t in tags:
        if re.search(r'(^|[^a-z])' + re.escape(k), n):
            return t
    return 'video (type?)' if video else 'static or carousel?'


def daily_read(path):
    rows, c = read_csv(path)
    if 'day' not in c or 'freq' not in c:
        return None, 'Daily file needs Day and Frequency columns (Breakdown > By time > Day).'
    key = 'campaign' if 'campaign' in c else ('ad' if 'ad' in c else None)
    if not key:
        return None, 'Daily file needs a Campaign name column.'
    series = defaultdict(list)
    for r in rows:
        nm = (r.get(c[key]) or '').strip()
        if not nm or nm.lower().startswith('total'):
            continue
        fr = num(r.get(c['freq']))
        if not fr:
            continue
        cpm = num(r.get(c['cpm'])) if 'cpm' in c else (num(r.get(c['spend'])) / num(r.get(c['impr'])) * 1000 if 'spend' in c and 'impr' in c and num(r.get(c['impr'])) else 0)
        series[nm].append((r.get(c['day']), fr, cpm))
    out = []
    for nm, s in series.items():
        s.sort(key=lambda x: x[0])
        frs = [x[1] for x in s]
        cpms = [x[2] for x in s if x[2]]
        mean = statistics.mean(frs)
        def trend(v):
            if len(v) < 4:
                return 'n/a'
            a, b = statistics.mean(v[:3]), statistics.mean(v[-3:])
            if a == 0:
                return 'n/a'
            return 'rising' if b > a * 1.02 else ('falling' if b < a * 0.98 else 'flat')
        stage = 'TOF' if mean < 1.15 else 'MOF' if mean <= 1.40 else ('BOF, saturated' if mean > 2.0 else 'BOF')
        out.append(dict(name=nm, days=len(s), mean=mean, ftrend=trend(frs), ctrend=trend(cpms), stage=stage,
                        danger=trend(frs) == 'rising' and trend(cpms) == 'rising', by=key))
    return out, None


def danger_msg(d):
    if not d['danger']:
        return 'saturated: refresh creative or widen the audience' if d['mean'] > 2.0 else ''
    if d['mean'] > 1.40:
        return 'CPM AND frequency rising on warm traffic: the pool is saturating because the top of the funnel is not feeding it. New TOF creative first, then refresh this one'
    return 'CPM AND frequency rising: funnel drying up, needs new TOF creative'


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument('csv')
    ap.add_argument('--daily')
    ap.add_argument('--compare')
    ap.add_argument('--target-cpa', type=float)
    ap.add_argument('--currency', default='$')
    ap.add_argument('--min-impressions', type=int, default=1000)
    ap.add_argument('--out')
    a = ap.parse_args()
    cur = a.currency if a.currency.endswith('$') or len(a.currency) == 1 else a.currency + ' '

    rows, c = read_csv(a.csv)
    need = [k for k in ('ad', 'spend', 'impr') if k not in c]
    if need:
        sys.exit(f'Missing columns: {need}. Found: {list(rows[0].keys())}')
    ads, meta, days, warn = aggregate(rows, c)
    res = build(ads, meta, days if 'day' in c else None)
    flags = page_gaps(res)
    bad = {(cn, pg): (rt, br, best) for cn, pg, rt, best, br, ck, bk in flags}
    camp_info = judge(res, a.target_cpa, a.min_impressions, bad)

    out = []
    P = out.append
    P(f'# Creative read | {a.csv.split("/")[-1]}')
    P(f'Target CPA: {money(a.target_cpa, cur) if a.target_cpa else "not set, so ads are judged against their campaign blended CPA"}. '
      f'Hook = 3s plays / impressions. Hold = ThruPlays / 3s plays. Link CTR = link clicks / impressions. Purchases per click = purchases / link clicks.')
    P(f'Bands (same as 4PI): hook under {HOOK_BANDS[0]}% weak, over {HOOK_BANDS[1]}% strong. Hold under {HOLD_BANDS[0]}% weak, over {HOLD_BANDS[1]}% strong. Link CTR under {CTR_WEAK}% weak, over {CTR_STRONG}% strong. Purchases per click judged against the campaign.')
    missing = [lbl for k, lbl in (('p3', '3-second video plays'), ('thru', 'ThruPlays'), ('clicks', 'Link clicks'),
                                  ('purchases', 'Purchases'), ('url', 'Website URL'), ('campaign', 'Campaign name'))
               if k not in c and not (k == 'p3' and 'thumbstop' in c)]
    if missing:
        P(f'Missing columns: {", ".join(missing)}. Add them in Columns > Customise for a full read.')
    if 'day' not in c:
        P('No Day column in the main file, so "7 days of delivery" is not checked; only the spend bar is.')
    for w in warn:
        P(f'WARNING: {w}')
    P('')

    tot_s = sum(r['spend'] for r in res); tot_p = sum(r['purchases'] for r in res)
    P(f'**Account in this file:** spend {money(tot_s, cur)}, purchases {f(tot_p, 0)}, blended CPA {money(tot_s / tot_p, cur) if tot_p else "-"}, {len(res)} ads, {len(camp_info)} campaigns.\n')

    P('## Product lines (by landing page)')
    lines = defaultdict(lambda: dict(spend=0.0, purchases=0.0, ads=0))
    for r in res:
        L = lines[r['line']]; L['spend'] += r['spend']; L['purchases'] += r['purchases']; L['ads'] += 1
    P('| Product line | Ads | Spend | Share | Purchases | CPA |\n|---|---|---|---|---|---|')
    for k, L in sorted(lines.items(), key=lambda kv: -kv[1]['spend']):
        P(f"| {t(k)} | {L['ads']} | {money(L['spend'], cur)} | {f(pct(L['spend'], tot_s), 0, '%')} | {f(L['purchases'], 0)} | {money(L['spend'] / L['purchases'], cur) if L['purchases'] else '-'} |")
    if a.target_cpa:
        losing = [k for k, L in lines.items() if L['spend'] >= 2 * a.target_cpa and (not L['purchases'] or L['spend'] / L['purchases'] > 1.5 * a.target_cpa)]
        if losing:
            P(f"\nLines past the data bar with CPA over 1.5x target: {', '.join(losing)}. Check offer and product economics before scripting more for them.")

    P('\n## Campaigns')
    P('| Campaign | Ads | Spend | Purchases | Blended CPA |\n|---|---|---|---|---|')
    for cn, ci in sorted(camp_info.items(), key=lambda kv: -kv[1]['spend']):
        P(f"| {t(cn)} | {ci['ads']} | {money(ci['spend'], cur)} | {f(ci['purchases'], 0)} | {money(ci['cpa'], cur)} |")

    P('\n## Ads by spend, with the first drop-off')
    P('| Ad | Campaign | Spend (share) | Purch | CPA | ROAS | Hook | Hold | Link CTR | Purch/click | Data bar | First drop-off |\n|---|---|---|---|---|---|---|---|---|---|---|---|')
    for r in res:
        P(f"| {t(r['ad'], 70)} | {t(r['campaign'], 40)} | {money(r['spend'], cur)} ({f(r['share'], 0, '%')}) | {f(r['purchases'], 0)} | {money(r['cpa'], cur)} | {f(r['roas'], 2)} | "
          f"{f(r['hook'], 1, '%')} {band(r['hook'], *HOOK_BANDS) if r['hook'] is not None else ''} | {f(r['hold'], 1, '%')} {band(r['hold'], *HOLD_BANDS) if r['hold'] is not None else ''} | "
          f"{f(r['ctr'], 2, '%')} | {f(r['ppc'] * 100 if r['ppc'] is not None else None, 1, '%')} | {'met' if r['enough_conv'] else 'not met'} | {r['dropoff']} |")
    P('\nData bar: ' + '; '.join(sorted({f"{cn}: {r['bar']}" for r in res for cn in [r['campaign']]})[:6]) + '. Below the bar, no conversion verdict.')

    wins = winners(res, a.target_cpa, camp_info)
    P('\n## Winners to iterate (past the data bar, CPA at or under ' + ('target' if a.target_cpa else 'campaign blended CPA') + ')')
    if wins:
        for r in wins:
            nxt = 'Test new hook types on this body.' if r['video'] else 'A static: its angle is a candidate to carry into a video.'
            P(f"- {r['ad']} ({r['campaign']}): CPA {money(r['cpa'], cur)}, spend {money(r['spend'], cur)}, hook {f(r['hook'], 1, '%')}, hold {f(r['hold'], 1, '%')}. {nxt}")
    else:
        P('- None past the data bar yet.')

    P('\n## Not a creative problem')
    any_flag = False
    for cn, pg, rt, best, br, ck, bk in flags:
        any_flag = True
        P(f"- {cn}: {pg} converts {rt*100:.1f}% of clicks vs {br*100:.1f}% on {best} ({ck:,.0f} vs {bk:,.0f} clicks). Fix or swap the landing page before blaming creative.")
    for r in res:
        if r['dropoff'].startswith('Post-click'):
            any_flag = True
            P(f"- {r['ad']}: {r['dropoff']}")
    if not any_flag:
        P('- Nothing flagged from this data.')

    if a.compare:
        crow, cc = read_csv(a.compare)
        cads, cmeta, cdays, _ = aggregate(crow, cc)
        cres = {r['ad']: r for r in build(cads, cmeta, cdays if 'day' in cc else None)}
        P(f'\n## Recent vs earlier ({a.compare.split("/")[-1]} vs the rest of {a.csv.split("/")[-1]})')
        P('"Earlier" = the main window minus the short window, so the two periods don\'t overlap. If hook rate or CTR falls while purchases per click holds, the creative is tiring, not the page.')
        P('| Ad | CPA recent vs earlier | Hook | Link CTR | Purch/click | Read |\n|---|---|---|---|---|---|')
        for r in res:
            s = cres.get(r['ad'])
            if not s or s['spend'] <= 0:
                continue
            g, h = ads[r['ad']], cads[r['ad']]
            e = {k: g[k] - h[k] for k in ('spend', 'purchases', 'impr', 'p3', 'clicks')}
            if e['spend'] <= 0 or e['impr'] <= 0:
                P(f"| {t(r['ad'], 60)} | {money(s['cpa'], cur)} vs - | {f(s['hook'], 1, '%')} vs - | {f(s['ctr'], 2, '%')} vs - | - | all spend is recent, too new to compare |")
                continue
            ecpa = e['spend'] / e['purchases'] if e['purchases'] > 0 else None
            ehook = pct(e['p3'], e['impr']) if r['video'] and e['p3'] > 0 else None
            ectr = pct(e['clicks'], e['impr']) if e['clicks'] > 0 else None
            eppc = e['purchases'] / e['clicks'] if e['clicks'] > 0 else None
            read = []
            if s['cpa'] and ecpa and s['cpa'] > 1.2 * ecpa:
                read.append('CPA worse')
            if s['hook'] and ehook and s['hook'] < 0.85 * ehook:
                read.append('hook rate dropping')
            if s['ctr'] and ectr and s['ctr'] < 0.85 * ectr:
                read.append('CTR dropping')
            page_ok = s['ppc'] is not None and eppc and s['ppc'] >= 0.85 * eppc
            fat = ('hook rate dropping' in read or 'CTR dropping' in read) and ('CPA worse' in read)
            tag = ('FATIGUE (creative, purchases per click held): ' if fat and page_ok else 'FATIGUE: ' if fat else '')
            P(f"| {t(r['ad'], 60)} | {money(s['cpa'], cur)} vs {money(ecpa, cur)} | {f(s['hook'], 1, '%')} vs {f(ehook, 1, '%')} | {f(s['ctr'], 2, '%')} vs {f(ectr, 2, '%')} | "
              f"{f(s['ppc'] * 100 if s['ppc'] is not None else None, 1, '%')} vs {f(eppc * 100 if eppc else None, 1, '%')} | {tag}{', '.join(read) or 'steady'} |")
        P('Check the short export really sits inside the main window (same end date). Window frequency is a trend line only; the funnel stage comes from daily frequency.')

    if a.daily:
        dr, err = daily_read(a.daily)
        P('\n## Funnel read (mean daily frequency)')
        if err:
            P(err)
        else:
            P('Under 1.15 TOF, 1.15 to 1.40 MOF, over 1.40 BOF, over 2.0 saturated. Trend = first 3 days vs last 3 days, 2% flat band.')
            P('| ' + ('Campaign' if dr and dr[0]['by'] == 'campaign' else 'Ad') + ' | Days | Mean daily frequency | Stage | Frequency trend | CPM trend | Warning |\n|---|---|---|---|---|---|---|')
            for d in sorted(dr, key=lambda x: x['name']):
                P(f"| {t(d['name'])} | {d['days']} | {d['mean']:.2f} | {d['stage']} | {d['ftrend']} | {d['ctrend']} | {danger_msg(d)} |")
    else:
        P('\nFunnel read: needs a campaign-level daily export (Breakdown > By time > Day). Window frequency is not daily frequency, so no stage call was made from it.')

    P('\n## Angle inventory (fill in angle and hook type from the ad copy and video)')
    P('| Ad | Campaign | Spend share | Format (guess from name) | Angle | Hook type |\n|---|---|---|---|---|---|')
    for r in res:
        if r['spend'] > 0:
            P(f"| {t(r['ad'], 70)} | {t(r['campaign'], 40)} | {f(r['share'], 0, '%')} | {format_guess(r['ad'], r['video'])} | ? | ? |")

    txt = '\n'.join(out)
    if a.out:
        with open(a.out, 'w', encoding='utf-8') as fh:
            fh.write(txt + '\n')
    print(txt)


if __name__ == '__main__':
    main()
