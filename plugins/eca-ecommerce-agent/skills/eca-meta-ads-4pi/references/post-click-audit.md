# Post-Click Audit — Landing Page Mismatch Check

The creative is doing its job — people click. The page may be losing them. This audit determines whether that's true, **without producing confident, wrong findings**. Every rule below exists because the naive version (scrape the page, compare, report) fails in specific, predictable ways: wrong-market renders, phantom popups, noise mistaken for signal.

## Step 0 — Decompose the click BEFORE deciding it's the page

Never jump from "low CVR" to "the page is broken". Break the click into four steps per ad (30d window, ads with ≥100 clicks), then read where the drop happens:

| Step | From → to | Source |
|---|---|---|
| Click→page | link clicks → landing page views | `actions:link_click` → landing page views |
| Page→cart | landing page views → adds to cart | landing page views → adds to cart |
| Cart→buy | adds to cart → purchases | adds to cart → `actions:omni_purchase` |
| Purchases/click | end to end | purchases ÷ link clicks |

Print it as a table with a campaign row. **The diagnosis is in which step varies across creatives**, because everything downstream of the cart is creative-independent: if the page, price, shipping or checkout were losing people, the ad sending the worst traffic would also convert worst *after* add-to-cart.

| Pattern | Diagnosis |
|---|---|
| Click→page < ~80% | Page speed or broken link — **the page's fault** |
| Page→cart weak, cart→buy normal, on a **prospecting** ad | Traffic temperature. Cold traffic clicks more and buys less — **TOF economics, not a broken page. Do not audit.** |
| Page→cart weak, cart→buy normal, on a **retargeting/warm** ad | Message match — **audit the page** |
| Cart→buy < ~35–40% (all creatives alike) | Shipping shock, checkout friction, forced account creation — **page/offer's fault** |
| All three normal but CPA poor | Not post-click at all — look at CPM, audience, attribution |

Quantify the spread when you report it ("cart→buy varies 1.2pp across three creatives; page→cart varies 10.9pp — nine times wider"). That spread *is* the proof.

If landing-page-view or add-to-cart data is unavailable, fall back to purchases-per-link-click vs campaign median and say the decomposition wasn't possible.

## Trigger gates — ALL must pass before scraping a page

1. **Minimum-data bar.** The ad must clear the data threshold (≥ 7 days AND spend ≥ 2× target/blended CPA). Never audit an ad you just labelled *Insufficient data*.
2. **One-purchase swing test.** Recompute purchases-per-click with ONE more purchase. If that lands within ~80% of the campaign median, the gap is noise — don't audit.
3. **Decomposition points at the page** (Step 0): the weak step must be one the page controls. A prospecting ad losing people at page→cart with a healthy cart→buy is doing its job — say so and move on.

Cap at the 2–3 worst qualifying offenders per report — a diagnostic deep-dive, not a site crawl.

## Workflow

### 1. Establish the campaign's market — BEFORE looking at the page

From **delivery, not the campaign name**: `ads_get_ad_entities(level: "campaign", breakdowns: ["country"])`. The market is the country carrying the majority of spend. (There is no geo/targeting field in the API catalog — this breakdown is the only reliable source, and a campaign named "AU" can be delivering anywhere.)

Audit the page **the way that market's customer sees it**: an AU-delivered campaign against the AUD storefront, a US-delivered campaign against the USD storefront. Auditing an AU campaign against a USD render (or vice versa) produces confident, wrong findings about prices, offers and shipping.

### 2. Anchor on the store's base truth

If the Shopify connector is available: `shop { currencyCode }` + `products.priceRangeV2` gives the store's base currency and base prices. On multi-market stores (Shopify Markets), the campaign's market may *correctly* see a different currency than base — base is your anchor for reconciliation, not necessarily what the market sees.

### 3. Capture the ad promise

From `ads_get_creatives`: hook/headline (`title`), primary text (`body`), CTA type, the visual concept — and from the brand intelligence, which persona the ad speaks to. The `link_url` (or `object_story_spec` link) is the destination; if missing or an unresolvable tracking redirect, ask the user which page the ad points to.

### 4. Scrape geolocated to the market

`firecrawl_scrape(url, location: {country: "<market>"}, formats: ["markdown"], maxAge: 0)` — for copy, review language, structure. (These are the **firecrawl-mcp** tool and parameters — `location` is confirmed supported in the MCP schema.) `maxAge: 0` matters: the MCP serves cached renders by default, and a cached page can be days old or captured from a different geo — an audit on a stale render is a wrong audit. If the scrape fails (bot-blocked), note it and ask the user for a screenshot, or skip with a note. Never substitute a non-geolocated fetch and treat it as the market's view.

### 5. Reconcile currencies

- Rendered currency **matches** the market → proceed; prices usable.
- Rendered currency **≠** the market → a *candidate finding* (the page may not be localised for the market you're buying — a real conversion killer), **but verify in a real browser from that market before reporting it**. A geolocated scrape is not proof of what the market sees; headless fetches routinely miss Shopify Markets' currency treatment.
- **Never convert.** No FX maths on scraped prices, ever. Every price quoted in the report carries its currency.

### 6. Cross-examine against the account's own numbers

`ads_get_ad_accounts` gives the account `currency`; every Meta figure — including derived AOV — is in it. **AOV ÷ items-per-order ≈ the typical item price in that currency.** If the page's visible price points can't produce that AOV, the page is rendering a different currency or the wrong market. This check needs no FX knowledge and works in any market.

If a scraped fact contradicts the client config, **assume the scrape is wrong until proven otherwise** — never "correct" a client's config from a scrape.

### 7. Compare ad promise vs page reality

| Dimension | Question | Common failure |
|---|---|---|
| Message match | Does the page headline repeat/extend the ad's promise? | Ad promises "50% off bundles", page shows full-price catalog |
| Persona match | Does the page speak to the persona and awareness level the ad hooks? | UGC ad targets problem-aware beginners; page is spec-heavy for experts |
| Offer integrity | Same price, discount, bundle, shipping promise as the ad — in the market's currency? | Price shock, discount requiring a hidden code, unlocalised currency |
| Proof & trust | Reviews, UGC, guarantees near the CTA? | Ad leans on social proof; page has none above the fold |
| Friction | Is the next step obvious and fast? | Homepage instead of PDP, forced account creation, wall of text before the buy box |

**DOM presence ≠ user-visible.** Never report a popup, banner, badge or discount widget as live from markup alone — disabled apps and unpublished theme sections leave complete markup behind. Verify computed visibility (`offsetParent`, bounding rect, `display`/`visibility`/`opacity`) in a real browser before reporting it. A finding about an element the customer never sees is worse than no finding.

### 8. Report

For each audited ad: the specific mismatch (quote the ad line vs the page line), the **source and currency of every price quoted**, 2–3 concrete fixes ordered by effort (copy tweak → section addition → new dedicated lander), and the success signal (purchases-per-click closing toward campaign median).

## Fix ladder — what to recommend, cheapest first

Match the fix to the diagnosed step. Always offer the cheapest fix that addresses it; only escalate to a new page when the mismatch is structural.

| # | Fix | When it's the right call | Effort |
|---|---|---|---|
| 1 | **Copy/framing change on the existing page** (H1 echoes the ad's hook, benefit language matches, offer stated in the market's currency) | Message match is off but the page type is right | Minutes |
| 2 | **Reorder the existing page** — proof above the buy box, offer module relabelled to lead with the benefit | Elements exist but are below the fold or buried | ~1 hour |
| 3 | **Section addition** — founder block, comparison table, FAQ answering the ad's objection | The ad promises something the page never mentions | Half a day |
| 4 | **Advertorial / listicle lander** ("5 things mums notice…", "Why teenage skin needs…") | The ad is education- or story-led (founder story, problem-agitation, LEARN MORE CTA) and the PDP jumps straight to SKU + price. Cold traffic isn't ready for a buy box. | Days |
| 5 | **Dedicated campaign landing page** — offer-specific, one CTA, no site nav | The ad sells a bundle/offer the PDP can't express, or a promo needs its own destination | Days + build |
| 6 | **Quiz / routine-finder funnel** | The audience doesn't know which product they need (persona evidence: "don't know where to start") | Project |

Rules of thumb: a **founder-story or education-led ad pointing at a bare PDP** is the classic advertorial case — the ad sells a movement, the page sells a SKU. A **promo/bundle ad pointing at a generic collection** is the dedicated-lander case. Anything fixable with a headline rewrite should never be answered with "build a new page".

Every recommendation from tier 4 down carries **"⚠ Double-check with the account owner before actioning"** — those are build decisions, not media tweaks. State the expected signal too: which step of the decomposition should move, and to roughly what ("page→cart from 7.6% toward the 18.8% campaign blend").

## Recommendation rules

- Landing page problems are flagged **to the client** — they're often not a media-buying fix. Frame accordingly. Label the ad **Fix** with a landing-page note; never kill a creative that's doing its job.
- Copy/headline change or moving a reviews block: recommend directly.
- New dedicated landing page, offer change, pricing, or template rebuild: append **"⚠ Double-check with the account owner before actioning."**
- **"The page is fine" and "the sample is too small to tell" are both complete, successful audits.** If no mismatch survives verification, say so — the cause may be price competitiveness, audience quality (check repeat-purchase bias / 1DV inflation), or checkout friction beyond the page. Never go hunting for a finding just to have something to say.

## Writing the section (report output)

Target **~400 words**. Structure: verdict first → decomposition table → the spread sentence that proves it → the one or two real findings with their numbers and fix tier → anything unconfirmed as a single "verify" line.

- **Never print the diagnostic method in the report.** The pattern table above is skill methodology — the reader gets the conclusion it produced, not the decision tree. A client re-reading "how to interpret funnel decomposition" every week is a report lecturing instead of reporting.
- **Weight by confidence and value.** A finding you've concluded is probably an artifact gets one line, not a paragraph — never as much space as a confirmed, fixable leak.
- Rank findings by leverage (biggest gap × cheapest fix first), not by the order you found them.
