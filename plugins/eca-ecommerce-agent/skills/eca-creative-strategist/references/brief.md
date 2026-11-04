# The creator brief (step 8)

One brief per product and format, for whoever films it (a paid creator, a customer, the founder, the member). It's the document they'll actually use on the day, so it has to be easy to scan: big clear headings, short lines, lots of white space, examples they can tap.

## 1. What goes in

1. **Cover**: a friendly hello, who the brand is with the link, what the product is and what makes it different in plain words, who it's for, length and format, the idea in two sentences, what this kind of video **is and isn't**, and the shape (the beats).
2. **Things to get in**: the must-says, each "in your own words"; the brand said once near the end; the one casual offer line.
3. **Watch these first**: 2 to 4 example videos as **clickable thumbnails** (a competitor's proven ad from the research, one of the member's winners, or a Concept Board example), each with its opening line and why it's there.
4. **The shots we need**: inside the one take, then optional extras.
5. **One page per idea**: the 3 to 5 opening lines (say, show, on screen), the talking points, the sample script ("one way it could sound"), shots for this idea, watch-outs (claims not to make).
6. **Filming, dos and don'ts, what to send, quick check.**

## 2. What never goes in

Ad metrics, CPA or ROAS, internal notes, competitor names in the creator's lines (an example video's link and a neutral title is fine), margins, pricing strategy, deadlines, or "post this" instructions. Creators only send files. The offer notes for the member live in the strategy pack.

## 3. How to build it

Write a JSON file in the shape of `assets/brief-example.json`, then:

```
python3 <skill>/scripts/build_brief.py brief.json --out brief-<product>-<format>.html [--pdf]
```

- Colours and fonts: take them from `brand-data.md` §4 or the store. Two colours is plenty: `brand` for headings, `accent` for labels and links. Headings render bold and dark by default so the page scans fast.
- Example thumbnails: use a real image URL or a local file if you have one. Without one, the script draws a clean play tile; the whole card stays clickable either way. Ad Library video links and thumbnails can expire, so prefer the Ad Library ad link (`https://www.facebook.com/ads/library/?id=<ad id>`) as the target.
- `--pdf` prints it to A4 using Playwright or a local Chrome if either is installed; otherwise open the HTML in Chrome and Print > Save as PDF (A4, margins none, background graphics on).
- The script refuses em dashes and warns on words that don't belong in a creator brief (CPA, ROAS, margin, competitor names you pass with `--competitors`). Fix the JSON and rebuild.

- The filming notes, dos and don'ts, what to send and the quick check have one-take defaults. When they don't fit the shoot (a night-time scene, a demo with a tripod, two people on camera), replace them with `filming`, `dos`, `donts`, `send` and `checklist`, or add to them with `filming_extra`. `greeting` sets the hello line ("Hey Priya!"); don't repeat it in `hello`.

Open the result and look at it before handing it over: every placeholder filled, nothing cut off, links work.

## 4. Writing for creators

- Speak to them like a person: "Hey! Thanks for doing this. None of it needs to be perfect."
- Talking points, not lines. "Learn the points, then say it your way with your real details."
- Hooks are the exception: "Say this opening word for word, then carry on in your own words. Do one full take per opening."
- "Only say what's true for you."
- Tell them what to send and how to name files. Nothing about posting.
