#!/usr/bin/env python3
"""Lint ad scripts, hooks and briefs before the member sees them.

usage:
  python3 check_copy.py scripts.md [more files...] [--brand "Little Drift"] [--banned "SIDS,safe sleep"]
                        [--spelling au|us|uk] [--max-hook-words 12] [--wps 2.5]

Checks:
  ERRORS (exit code 1): em dashes, the member's banned words or claims.
  WARNINGS: AI-slop phrases, fake urgency words, banned hook openers, hooks over the word limit,
            the brand name inside a hook, US spellings when the market is AU or UK,
            sample scripts where the brand is said early or more than once, read-aloud timing per script.

Hooks are found on lines labelled H1, H2... (for example "| H1 | "spoken line" | ..." or "H2: spoken line").
The spoken part is the first quoted text on the line if there is one.
Sample scripts are the text under any markdown heading containing "sample script" (or "one way it could sound"),
up to the next heading. Stage directions in (round) or [square] brackets are not counted as spoken words.
Text inside HTML tags is ignored, so you can run it on a built brief too.
"""
import argparse, re, sys

SLOP = ['game-changer', 'game changer', 'elevate', 'unlock', 'level up', 'seamless', 'seamlessly', 'revolutionary',
        'revolutionise', 'revolutionize', 'look no further', 'say goodbye to', "in today's fast-paced world",
        'fast-paced world', 'trust me', "you won't believe", 'hidden gem', 'must-have', 'must have', 'holy grail',
        'next level', 'next-level', 'the best part?', 'elevated', 'effortlessly', 'transformative', 'cutting-edge',
        'unleash', 'supercharge', 'empower', 'curated', 'indulge', "it's not just", 'not just a', 'delve',
        'in a world where', 'imagine a world']
URGENCY = ['ends tonight', 'ends soon', 'last chance', 'limited time', 'selling out', 'sold out', 'only this week',
           'hurry', "don't miss out", 'dont miss out', 'while stocks last', 'today only', 'before it\'s gone',
           'before its gone', 'act now', 'running out']
BAD_OPENERS = ['have you ever', "hi, i'm", 'hi i\'m', 'hi im', 'hey guys', 'hi guys', 'pov:', 'pov ', 'introducing',
               'attention', 'stop scrolling', "you won't believe", 'here\'s why', 'heres why', 'let me tell you',
               'did you know', 'are you tired', 'tired of', 'sick of', 'struggling with']
US_TO_AU = {'mom': 'mum', 'moms': 'mums', 'mommy': 'mummy', 'color': 'colour', 'colors': 'colours',
            'colorful': 'colourful', 'favorite': 'favourite', 'favorites': 'favourites', 'flavor': 'flavour',
            'flavors': 'flavours', 'organize': 'organise', 'organized': 'organised', 'realize': 'realise',
            'realized': 'realised', 'center': 'centre', 'behavior': 'behaviour', 'apologize': 'apologise',
            'jewelry': 'jewellery', 'pajamas': 'pyjamas', 'diaper': 'nappy', 'diapers': 'nappies', 'cozy': 'cosy',
            'fiber': 'fibre', 'customize': 'customise', 'analyze': 'analyse', 'traveling': 'travelling',
            'gray': 'grey', 'neighbor': 'neighbour', 'neighbors': 'neighbours', 'honor': 'honour', 'odor': 'odour',
            'odors': 'odours', 'labor': 'labour', 'liter': 'litre', 'liters': 'litres', 'meter': 'metre',
            'stroller': 'pram', 'cookie': 'biscuit', 'cookies': 'biscuits', 'vacation': 'holiday',
            'sweater': 'jumper', 'fall': None, 'math': 'maths', 'pacifier': 'dummy', 'crib': 'cot',
            'onesie': None, 'zip code': 'postcode', 'mail': None, 'mailman': 'postie', 'gotten': 'got'}
HOOK_RE = re.compile(r'^\s*(?:[-*>]\s*)?(?:\|\s*)?\**\s*(H\d{1,2})\s*\**\s*[:|.)\-]\s*(.*)$', re.I)
QUOTE_RE = re.compile(r'["“]([^"”]{3,})["”]')
TAG_RE = re.compile(r'<[^>]+>')
BLOCK_RE = re.compile(r'<(style|script)[^>]*>.*?</\1>', re.S | re.I)
NEG_RE = re.compile(r"(don't|dont|never|avoid|no |not |without)[^.]{0,60}$", re.I)
HEAD_RE = re.compile(r'^\s{0,3}(#{1,6})\s+(.*)$')
DONT_HEAD = re.compile(r"never|don't|dont|avoid|banned|compliance|watch out|not say|claims|cut|removed|refus|declin", re.I)
# "you" near a body or health condition, including euphemisms: Meta personal attributes
ATTR_RE = re.compile(r"\b(you|your|you're|youre|you've)\b[^.!?]{0,45}\b(period|that week|time of the month|day 2|day two|cramps|acne|eczema|breakouts?|weight|belly|tummy|bloat\w*|hair loss|thinning|bald\w*|anxiety|anxious|depress\w*|wrinkles?|cellulite|incontinen\w*|bladder|ibs|diabet\w*|menopaus\w*|insomnia|can't sleep|cant sleep)\b", re.I)


def words(s):
    s = re.sub(r'\([^)]*\)|\[[^\]]*\]', ' ', s)
    return re.findall(r"[A-Za-z0-9$%']+", s)


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument('files', nargs='+')
    ap.add_argument('--brand')
    ap.add_argument('--banned', default='')
    ap.add_argument('--spelling', default='au', choices=['au', 'uk', 'us'])
    ap.add_argument('--max-hook-words', type=int, default=12)
    ap.add_argument('--wps', type=float, default=2.5)
    a = ap.parse_args()
    banned = [b.strip().lower() for b in a.banned.split(',') if b.strip()]
    errors, warns = [], []
    for path in a.files:
        raw = open(path, encoding='utf-8').read()
        is_html = path.lower().endswith(('.html', '.htm'))
        text = TAG_RE.sub(' ', BLOCK_RE.sub(' ', raw)) if is_html else raw
        lines = text.splitlines()
        # whole-text checks, line by line
        in_dont = False
        for i, line in enumerate(lines, 1):
            low = line.lower()
            hh = HEAD_RE.match(line)
            if hh:
                in_dont = bool(DONT_HEAD.search(hh.group(2)))
            if '\u2014' in line:
                errors.append(f'{path}:{i}: em dash. Use a comma, full stop or "and": {line.strip()[:90]}')
            if re.search(r'\s–\s', line):
                warns.append(f'{path}:{i}: spaced en dash reads as an em dash: {line.strip()[:90]}')
            for b in banned:
                mb = re.search(r'(?<![a-z])' + re.escape(b) + r'(?![a-z])', low) if b else None
                if mb:
                    if in_dont or NEG_RE.search(low[:mb.start()]) or re.search(r"never|don't|avoid|banned|not say|cut|removed", low):
                        warns.append(f'{path}:{i}: banned "{b}" appears in what looks like a do-not-say note. Fine if so: {line.strip()[:80]}')
                    else:
                        errors.append(f'{path}:{i}: banned word or claim "{b}": {line.strip()[:90]}')
            if not in_dont:
                ma = ATTR_RE.search(line)
                if ma and not NEG_RE.search(low[:ma.start()]):
                    warns.append(f'{path}:{i}: "you" next to a body or health condition ("{ma.group(0)[:50]}"). Meta personal attributes: use first person or the moment instead')
            for s in SLOP:
                if re.search(r'(?<![a-z])' + re.escape(s) + r'(?![a-z])', low):
                    warns.append(f'{path}:{i}: AI-slop phrase "{s}"')
            for u in URGENCY:
                mu = re.search(r'(?<![a-z])' + re.escape(u) + r'(?![a-z])', low)
                if mu and not NEG_RE.search(low[:mu.start()]):
                    warns.append(f'{path}:{i}: urgency wording "{u}". Only if it is true, with a real end date the member confirmed')
            if a.spelling in ('au', 'uk'):
                for us, au in US_TO_AU.items():
                    if au and re.search(r'(?<![a-z])' + re.escape(us) + r'(?![a-z])', low):
                        warns.append(f'{path}:{i}: US spelling or word "{us}", use "{au}"')
            m = HOOK_RE.match(line)
            if m:
                rest = m.group(2)
                q = QUOTE_RE.search(rest)
                spoken = q.group(1) if q else rest.split('|')[0]
                sp = spoken.strip().strip('*').strip()
                if not sp:
                    continue
                w = words(sp)
                if len(w) > a.max_hook_words:
                    warns.append(f'{path}:{i}: {m.group(1)} has {len(w)} spoken words (aim for {a.max_hook_words} or fewer): "{sp[:80]}"')
                sl = sp.lower().lstrip('"“\'( ')
                for o in BAD_OPENERS:
                    if sl.startswith(o):
                        warns.append(f'{path}:{i}: {m.group(1)} opens with "{o}": "{sp[:80]}"')
                if a.brand and a.brand.lower() in sl:
                    warns.append(f'{path}:{i}: {m.group(1)} says the brand name. Brand goes once, at the end')
                if sl.count('?') >= 2:
                    warns.append(f'{path}:{i}: {m.group(1)} stacks questions')
        # sample scripts
        sections, cur, cur_lvl = [], None, 0
        for i, line in enumerate(lines, 1):
            h = HEAD_RE.match(line)
            if h:
                lvl, title = len(h.group(1)), h.group(2)
                if cur and lvl <= cur_lvl:
                    sections.append(cur); cur = None
                tl = title.lower()
                if cur is None and ('sample script' in tl or 'one way it could sound' in tl):
                    cur = dict(title=title.strip('# ').strip(), start=i, body=[]); cur_lvl = lvl
                continue
            if cur is not None:
                cur['body'].append(line)
        if cur:
            sections.append(cur)
        for s in sections:
            body = ' '.join(s['body'])
            body_w = words(body)
            if not body_w:
                continue
            secs = len(body_w) / a.wps
            warns.append(f"{path}:{s['start']}: timing, \"{s['title'][:60]}\": {len(body_w)} spoken words, about {secs:.0f}s at {a.wps} words a second")
            if a.brand:
                bl = a.brand.lower()
                joined = ' '.join(body_w).lower()
                n = joined.count(bl)
                if n > 1:
                    warns.append(f"{path}:{s['start']}: brand said {n} times in \"{s['title'][:60]}\". Once, at the end")
                elif n == 1 and joined.find(bl) < 0.6 * len(joined):
                    warns.append(f"{path}:{s['start']}: brand said early in \"{s['title'][:60]}\". Move it to the CTA at the end")
    for e in errors:
        print('ERROR  ' + e)
    for w in warns:
        print('WARN   ' + w)
    print(f'\n{len(errors)} errors, {len(warns)} warnings. Timing lines are information; fix the rest or say why a flag is a false alarm.')
    sys.exit(1 if errors else 0)


if __name__ == '__main__':
    main()
