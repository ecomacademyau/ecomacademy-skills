# Intake (step 0)

## 1. Look before you ask

Members hate answering questions their files already answer. Check the working folder, `./brand/` and any folder named after the brand. Load what exists:

| File (any name close to this) | What you take from it |
|---|---|
| `brand-data.md` (eca-brand-intelligence) | Products, prices, mechanism, why people buy (§2), voice (§3), messaging pillars (§5), offers (§7), proof (§8), objections (§9), competitors (§11), personas (§12), promo calendar (§14), sources and confidence (§18), open questions (§19) |
| `./brand/creative-log.md` (this skill) | Locked ideas, dead ideas, past rounds and their ad names, winning and dead angles, best hooks, verified creators. Update it, never rebuild it |
| `4pi-report-*.html` / `4pi-history-*.json` (eca-meta-ads-4pi) | Funnel map per campaign, action labels, creative findings, open recommendations, target CPA. Reuse if it's 14 days old or less |
| Survey report or raw survey export (eca-survey-report, Zigpoll, Fairing, KnoCommerce, UserLoop, Typeform) | Why they bought, who for, what nearly stopped them, sample size |
| Persona files (eca-persona-builder, icp cards) | Who to aim each angle at |
| Competitor teardown (eca-competitor-analysis) | Proven patterns, already researched |
| Reviews export (Judge.me, Okendo, Yotpo, Loox, Trustpilot, marketplace) | Reasons to buy, objections, customer words |
| Ads Manager CSV export(s) | The account read when the MCP isn't connected |
| Past briefs and scripts, with results if known | What's been tried |
| Offer notes | Current offer, exact wording, end date |

If `brand-data.md` and the live store disagree on a price or offer, the store wins. Flag it so the brand file gets fixed.

Then tell the member, in two lines: "Found: brand file (updated 12 Oct), 30-day ads export, 214 reviews. Missing: survey data, competitor list, target CPA."

## 2. Ask for the gaps in one round

Skip anything already answered. Group the questions, don't drip-feed them. Propose an answer where you can ("Your 4PI report from last week says $42, still right?") rather than asking cold.

1. **Target CPA** (and kill CPA if they have one). If they don't know: "EcomOS shows your target CPA per channel." Otherwise judge against the account's own best ads and say so. Never invent one.
2. **Products to push** this round, in priority order. Any launch?
3. **Who will film**: a paid UGC creator (verified name only), a real customer, the founder, the member, staff. This changes which formats are possible.
4. **The offer**: exact wording, real end date or evergreen, free shipping threshold.
5. **Locked ideas** to film as written, and **dead ideas** never to rebuild.
6. **Claims**: anything they can't say (health, results, "best", "number 1", awards), and any certification or award they can name.
7. **Ad data**: if no CSV is in the folder and the Meta MCP isn't connected, ask for an export (how-to in `account-read.md` §2). Not having it doesn't block the round.
8. **Competitors**: 3 to 6 they compete with. If they say "find them for me", point them to **eca-competitor-analysis** or the competitor section of **eca-brand-intelligence**: a keyword search never decides the list (`competitors.md` §1). Optional in Quick mode.
9. **Market and spelling**, if the brand file doesn't say (Australian English by default).

## 3. Read the store yourself

Use the **Shopify** connector for each product you'll advertise: price, compare-at price (a compare-at above the price means it's on sale, which changes what the script can say), live discounts, variants and stock. For what's on the pages themselves (what's in the box, materials or ingredients, the shipping threshold, any offer banner, the FAQ and returns wording), read the product description from Shopify or ask the member to paste it. Record it with the date. If the store says something different from the member or the brand file, ask which is right.

## 4. No brand file and no time

Best: run **eca-brand-intelligence** with the store URL first. It takes a while but every ECA skill uses the result.

If the member needs scripts today, build a minimal brief instead, and say it's a stopgap:
- the product in one line, price, product page URL [SITE]
- the mechanism in one line, and how the camera proves it
- who buys, for whom, the moment [MEMBER / REVIEWS]
- the top 3 objections [REVIEWS / MEMBER]
- the offer in exact wording [SITE / MEMBER]
- banned claims [MEMBER]
- 5 to 10 short customer quotes from the product page reviews [REVIEWS]

Tag every fact with its source and date: [SITE], [REVIEWS], [SURVEY], [ADS], [MEMBER], [RESEARCH]. Unknowns stay "unknown", with who can answer.

## 5. The gate

Scripts need, per product: what it is and the price, the mechanism, who buys and why (sourced), the top objections, the current offer wording, and banned claims. Missing any? Ask before writing. Steps 1 to 3 can run while you wait. In Quick mode, a `[CONFIRM]` on a missing item is acceptable if the member is filming today, but the claim it covers stays out of the script until it's confirmed.
