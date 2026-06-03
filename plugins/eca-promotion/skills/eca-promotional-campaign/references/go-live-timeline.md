# Go-Live Timeline

The timeline is the spine of the campaign — the dated runsheet that fires the offer, the emails/SMS, the ads, and the on-site changes in the right order. Build it from the offer window in Stage 1, converting every relative step into a real date/time so the user gets an actual calendar, not a template.

**Only include steps for the channels confirmed in Stage 1.** If the campaign is email-only, the runsheet has no "confirm ads live" or "swap theme" rows and the calendar shows send beats only; an ads-only campaign's timeline is built around ad beats. Don't put a channel on the calendar that the user isn't running.

## The five phases

```
[ Early-access capture ] → [ Early-access offer ] → [ PUBLIC LAUNCH ] → [ Wind-down ] → [ Close ]
```

### Phase 1 — Early-access capture (lead time before the sale)

Goal: build a warm list of people who get first dibs, so launch day opens with momentum.

- **Start Early-Access Capture ads** (Meta/TikTok, TOF) driving to the sign-up page/popup.
- **Stand up the sign-up page + list** — a simple landing page or on-site popup offering early access in exchange for an email/SMS opt-in. Wire it to the "Early Access" list in `campaign-config.md`.

Typical lead time: 1–2 weeks before public launch (longer for big events like BFCM, shorter for a flash sale).

### Phase 2 — Early-access offer starts

Goal: reward the captured list with first access before the public.

- **Set up the offer on the website** (discount created/staged, sale collection ready) — but keep the main theme as-is for now.
- **Send Early-Access Email + SMS to the Early-Access list.**

Typical timing: 12–48h before public launch.

### Phase 3 — Public launch (the core of the campaign)

This is the busiest phase. Order matters.

1. **Update the website to the sale theme** (announcement bar, homepage banner, collection/product changes — see `website-design.md`).
2. **Send Launch Email + SMS to all subscribers.**
3. **Confirm ads have launched** — Launch Offer ads (TOF + MOF) live on Meta/TikTok; Google copy/extensions updated.
4. **Re-mail unopened ~12h later** — resend the launch email (new subject line) to anyone who didn't open.
5. **Send Top Picks email to engaged subscribers** — hero SKUs on offer.
6. **Send Time Check email to engaged subscribers** — e.g. "3 days to go" urgency.
7. **Send Best Sellers email to engaged subscribers** — social-proof close.
8. **Check ads & optimise as needed** — kill underperformers, scale winners, watch frequency/ROAS.

Space the Top Picks / Time Check / Best Sellers sends across the sale window (see cadence below).

### Phase 4 — Wind-down

- **~24h before the offer ends — send Last Chance Email + SMS to all subscribers.** Strongest urgency.
- **If (and only if) the offer is genuinely extended — send an "Offer Extended" email to engaged subscribers.** Never shadow-extend; the extension must be explicit and the website/discount dates must match.

### Phase 5 — Close

- **Turn the offer off on the website** (deactivate the discount, remove badges/announcement bar).
- **Revert the theme** to the everyday look.
- Optional but recommended: pull the post-mortem numbers (revenue, by-email performance, ad ROAS) for the brief's results section.

## Cadence guidance

Promos compress — the whole arc usually runs 5–14 days, not weeks. Map the sends to the window:

**Example — a 7-day public sale with a 10-day capture lead:**

| Day (relative) | Date | Action | Channel | Audience |
|---|---|---|---|---|
| –10 | … | Start capture ads + sign-up page live | Ads + site | TOF |
| –1 | … | Set up offer on site; Early-Access send | Email + SMS | Early-Access list |
| 0 (launch AM) | … | Theme live; Launch send; confirm ads live | Email + SMS + Ads | All subscribers |
| 0 (+12h) | … | Re-mail to unopened | Email | Launch non-openers |
| +2 | … | Top Picks | Email | Engaged |
| +4 | … | Time Check ("3 days to go") | Email | Engaged |
| +5 | … | Best Sellers | Email | Engaged |
| +6 (24h before end) | … | Last Chance | Email + SMS | All subscribers |
| +7 (end) | … | (If extended) Offer Extended | Email | Engaged |
| +7/+8 | … | Turn offer off; revert theme; pull results | Site | — |

For a **short flash sale (2–3 days)**, drop the capture phase and compress: Launch → re-mail unopened → Best Sellers/Time Check (pick one) → Last Chance. For a **big event (BFCM)**, lengthen the capture lead and consider splitting BF and CM as two launch beats.

## When you build the timeline

1. Take the public start and end date/time from the locked offer (with timezone from `campaign-config.md`).
2. Back-calculate the capture lead and early-access send.
3. Forward-calculate the re-mail (+12h), the mid-sale sends, and the last-chance (–24h).
4. Output **both** a calendar-grid summary and the dated runsheet table (see below) — this becomes the "Go-Live timeline" section of the brief.
5. Flag any collisions with other campaigns or with weekends/holidays that affect open rates.

## Presenting the timeline: calendar grid + detailed runsheet

A dense phase table alone is hard to read at a glance, so the brief leads with a **calendar grid** (the "what happens when" view) and then gives the **detailed runsheet table** (the full per-step detail). Produce both, under `### Campaign calendar` and `### Detailed runsheet`.

**Render the calendar as an image, not an HTML/Word table.** A styled HTML table loses its borders and cell shading when the `.docx` is opened in Word/Pages and collapses into unreadable floating columns. So generate the calendar as a PNG with the bundled generator, which looks identical everywhere:

1. Write a small JSON spec — a Mon–Sun grid covering the campaign span (capture → close), one array per week, each day `{"day": "24", "label": "LAUNCH — theme live · Email + SMS", "phase": "launch"}`. Pad empty days with just `{"day": "18"}`. Keep labels terse (full detail lives in the runsheet table + Email/SMS section). Phases: `cap`, `ea`, `launch`, `sale`, `last`, `close`.
2. Run: `python3 scripts/make_calendar.py spec.json campaigns/<slug>-calendar.png`
3. In the brief, under `### Campaign calendar`, reference the image: `![Campaign calendar](<slug>-calendar.png)`. The export script auto-sizes embedded images to the page width.

Then `### Detailed runsheet` with the table follows, as in the schedule example above. (The PNG already includes the green header, phase-coloured cells, and a legend — `make_calendar.py` owns that styling.)
