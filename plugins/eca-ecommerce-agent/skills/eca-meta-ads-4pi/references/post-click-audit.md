# Post-Click Audit — Landing Page Mismatch Check

The creative is doing its job — people click. The page may be losing them. This audit determines whether that's true, **without producing confident, wrong findings**. Every rule below exists because the naive version (scrape the page, compare, report) fails in specific, predictable ways: wrong-market renders, phantom popups, noise mistaken for signal.

## Trigger gates — BOTH must pass before any audit

An ad qualifies only when it's **good at sending traffic but bad at converting it**: healthy spend + decent link CTR (≥ campaign average), but purchases-per-link-click clearly below campaign peers (or, CSV path: good outbound CTR + good ATC rate but poor ATC→purchase rate).

1. **Minimum-data bar.** The ad must already clear the data threshold (≥ 7 days AND spend ≥ 2× target/blended CPA). Never audit an ad you just labelled *Insufficient data* — its conversion gap is a sample-size artifact, not a page problem.
2. **One-purchase swing test.** Recompute the ad's purchases-per-click with ONE more purchase. If that hypothetical lands within ~80% of the campaign median, the observed gap is noise — do not audit; note the small sample and move on. (Example: 1 purchase / 30 clicks = 3.3%; with 2 purchases it's 6.7%; if the campaign median is 8%, the gap can't be distinguished from luck.)

Cap the audit at the 2–3 worst qualifying offenders per report — it's a diagnostic deep-dive, not a site crawl.

## Workflow

### 1. Establish the campaign's market — BEFORE looking at the page

From **delivery, not the campaign name**: `ads_get_ad_entities(level: "campaign", breakdowns: ["country"])`. The market is the country carrying the majority of spend. (There is no geo/targeting field in the API catalog — this breakdown is the only reliable source, and a campaign named "AU" can be delivering anywhere.)

Audit the page **the way that market's customer sees it**: an AU-delivered campaign against the AUD storefront, a US-delivered campaign against the USD storefront. Auditing an AU campaign against a USD render (or vice versa) produces confident, wrong findings about prices, offers and shipping.

### 2. Anchor on the store's base truth

If the Shopify connector is available: `shop { currencyCode }` + `products.priceRangeV2` gives the store's base currency and base prices. On multi-market stores (Shopify Markets), the campaign's market may *correctly* see a different currency than base — base is your anchor for reconciliation, not necessarily what the market sees.

### 3. Capture the ad promise

From `ads_get_creatives`: hook/headline (`title`), primary text (`body`), CTA type, the visual concept — and from the brand intelligence, which persona the ad speaks to. The `link_url` (or `object_story_spec` link) is the destination; if missing or an unresolvable tracking redirect, ask the user which page the ad points to.

### 4. Scrape geolocated to the market

`firecrawl_scrape(url, location: {country: "<market>"}, formats: ["markdown"])` — for copy, review language, structure. If the scrape fails (bot-blocked), note it and ask the user for a screenshot, or skip with a note. Never substitute a non-geolocated fetch and treat it as the market's view.

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

## Recommendation rules

- Landing page problems are flagged **to the client** — they're often not a media-buying fix. Frame accordingly. Label the ad **Fix** with a landing-page note; never kill a creative that's doing its job.
- Copy/headline change or moving a reviews block: recommend directly.
- New dedicated landing page, offer change, pricing, or template rebuild: append **"⚠ Double-check with the account owner before actioning."**
- **"The page is fine" and "the sample is too small to tell" are both complete, successful audits.** If no mismatch survives verification, say so — the cause may be price competitiveness, audience quality (check repeat-purchase bias / 1DV inflation), or checkout friction beyond the page. Never go hunting for a finding just to have something to say.
