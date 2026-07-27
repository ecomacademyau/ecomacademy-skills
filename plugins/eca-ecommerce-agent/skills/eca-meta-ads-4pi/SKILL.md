---
name: eca-meta-ads-4pi
description: "Analyse a Meta (Facebook) ads account live via the official Meta Ads MCP (ads_* tools; CSV fallback) using the 4PI framework and produce an ECA-branded HTML report with campaign/ad set/ad breakdowns, scaling verdicts, and recommendations. Use whenever the user mentions ad analysis, Meta ads report, 4PI analysis, creative analysis, ad performance review, weekly ad report, funnel analysis, CPM or CPA analysis, scaling ads, which ads to stop or are working, ad creative testing, campaign diagnosis, landing page mismatch, or post-click analysis, or asks to run the ad/weekly/performance report for any Meta ad account. Also trigger on Facebook Ads Manager CSV uploads, Ads Manager data, ad funnel health, frequency analysis, or audience saturation — even partial requests like 'check my ads', 'how are my campaigns doing', 'what should I test next', or 'run the 4PI'. Includes Firecrawl landing-page audits and metastatus.com platform checks."
---

# Meta Ads 4PI Analyst

Analyse Meta ad performance with the 4PI framework (Spend, CPM, Frequency, CPA), map each campaign's funnel, diagnose creative and post-click problems, and deliver a **branded HTML report** the client can open in a browser.

**Before any analysis, read the Knowledge Base:** `references/4pi-knowledge-base.md`. It contains the full 4PI playbook — funnel decoder, golden rule, profitability proxy, creative diagnostics, macro calendar, Ad Concept Board, and tone rules. The analysis is only as good as fidelity to that framework.

---

## Workflow at a Glance

1. **Identify the client** → load/create brand config (`clients/`) + **load report memory** (previous run's history — `references/report-memory.md`)
2. **Pull data** → Meta Ads MCP (preferred) or CSV fallback
3. **Verify numbers** → print verification tables before analysing
4. **Run 4PI per campaign** → funnel map, action labels
5. **Creative diagnostics** → hook/hold/CTR waterfall
6. **Post-click audit (conditional)** → Firecrawl the landing page when traffic is good but conversion is poor
7. **Funnel-gap creative recommendations** → cross-reference personas + Ad Concept Board + Hook Bank
8. **Build the branded HTML report** → deltas vs last report + accountability card → save the report AND the new history file

---

## Step 0 — Ask Before Pulling (always, unless already answered)

Before running any pulls, ask the user two questions (use the AskUserQuestion tool when available; skip any question already answered by the request or the client config):

1. **"What's your current target CPA (blended)?"** — offer an **"I don't know"** option. If they don't know, reply with: *"See your ecomOS to know your target CPA per channel"*, then proceed with no target — CPA gets judged against campaign peers and profitability, and the report states "no target CPA set". Never invent a target.
2. **"Whole account, or a specific campaign?"** — offer "Whole account" and let them name a campaign. If a specific campaign is chosen, scope every pull and every section to it (the account snapshot shrinks to that campaign's three windows).

## Step 1 — Identify the Client & Load Brand Config

Ask which brand/account this analysis is for if not obvious from context.

- Check `clients/<brand-slug>.md` inside this skill for an existing config (brand colors, logo, currency, target CPA, website, personas pointer).
- If none exists, run the short onboarding in `clients/README.md`: ask for brand name, primary/accent colors (or derive from their website), logo URL, currency, target CPA, and website. Echo the completed config block back to the user so they can save it into the skill for next time.
- Also look for brand intelligence: search available skill/knowledge folders for `brand-data.md`, `brand-dna.md`, or `icp-cards.md` for this brand (e.g. from eca-brand-intelligence or icp-deep-dive). If found, read the personas, angles, and objections — they drive Step 7. If not found, proceed and note in the report that persona-level recommendations are generic.

**Target CPA** comes only from the client config or directly from the user — never invent one. If none is available, run the analysis without a target: judge CPA relative to campaign peers and profitability, state "no target CPA set" in the report, and for the minimum-data spend threshold use 2× the campaign's blended CPA (labelled as a data-sufficiency bar, not a performance target).

**Report memory:** also load the previous run's history now — look for `4pi-history-<brand-slug>*.json` in the outputs folder, else the embedded `fpi-history` block in the latest `4pi-report-<brand>-*.html`, else ask once for the last report file. Full workflow, schema, and accountability rules: `references/report-memory.md`. No memory found → first-run mode (say so in the report; never fabricate a baseline).

## Step 2 — Pull Data

### Option A: Official Meta Ads MCP (preferred)

Use the **official Meta Ads MCP** (tools named `ads_*`). Follow `references/mcp-data-pull.md` exactly — it has the verified field names. Summary:

- `ads_get_ad_accounts` → find the account, check `is_ads_mcp_enabled` and `is_queryable`, note the **currency** (it anchors every money figure in the report)
- `ads_get_field_context` → verify any uncertain field before querying
- `ads_get_ad_entities` at **ad level** for three windows (last_7d, MTD custom range, last_30d) plus a `time_increment: "1"` daily pull for the funnel decoder's daily frequency and the last-5-days spend trajectory
- `ads_get_ad_entities` at campaign + adset level for budgets, objectives, `delivery_sub_status` (learning phase), `attribution_setting`
- `ads_get_ad_entities` at **campaign level with `breakdowns: ["country"]`** → the **delivered market** per campaign. There is no geo/targeting field in the catalog, so this breakdown is the only way to know which market a campaign actually reaches — and delivery beats the campaign name. Needed for Step 6 and for any market/currency claim.
- `ads_get_creatives` (with creative_ids) → creative type, copy, and **landing page URL** (needed for Step 6)
- Optional enrichment: `ads_insights_anomaly_signal`, `ads_get_opportunity_score`, and `ads_insights_industry_benchmark` (peer comparison vs similar advertisers — see mcp-data-pull.md §6b; frequently returns "no data" for small accounts, skip gracefully) — supporting context only, never the headline

If the connector errors with an expired/invalid token, stop and tell the user to reconnect the Meta connector — do not fabricate data and do not silently fall back to old numbers.

### Option B: CSV upload (fallback)

If no working Meta MCP, ask for a Facebook Ads Manager export. CSV handling rules (column mapping, aggregation, date windows) live in the Knowledge Base under "Data Processing". The CSV path unlocks extras the API pull may not have: GPT column, audience segments, thumb-stop ratio. Use them when present.

## Step 3 — Verify Before Analysing

**Mandatory.** Print a verification table per time window before drawing any conclusion:

```
=== VERIFICATION: [WINDOW] ([dates]) ===
| Campaign | Ads w/ data | Spend | Purchases | Blended CPA | AOV | Profit/Order |
```

Sanity checks: 7d spend ≤ 30d spend; MTD spend ≤ 30d spend when the month is young; purchases and spend must be internally consistent (CPA ≈ spend/purchases). Every number in the final report must trace back to these pulls — never estimate, never fill gaps with plausible numbers. If a window has no data, say so.

## Step 4 — 4PI Analysis (Per Campaign, In Isolation)

All comparison is **within a campaign** — never across campaigns. For each ad:

1. **Spend** — % of campaign spend, trend (compare 3d/7d/30d run-rates)
2. **CPM** — lowest/median/highest in campaign, trend, creative-type context (image vs video)
3. **Frequency** — funnel position via the decoder (< 1.15 TOF | 1.15–1.40 MOF | > 1.40 BOF | > 2.0 saturation). Use the **average of the daily frequencies** from the `time_increment: "1"` pull as the decoder input; the 7d/30d aggregate frequency is the trend line. Cross-check CPM and frequency agree (and `cpp` vs `cpm`).
4. **Efficiency** — CPA (`cost_per_result`) vs campaign and vs target; **Profit per Order = AOV − CPA** (pre-COGS proxy; AOV = purchase_roas × spend ÷ purchases — see Knowledge Base "Profitability"). Profit/Order overrides raw CPA for scaling decisions. If a true GPT column exists (CSV path) or the client config has a gross-margin %, upgrade the proxy accordingly.

Classify each ad ACTIVE / STOPPED / WINDING DOWN and apply the minimum-data threshold (≥ 7 days AND spend ≥ 2× target CPA) **before** assigning any action label. Never recommend stopping an ad that is already stopped.

Action labels: **Keep / Hold / Fix / Watch / Stop / Scalable / Insufficient data** — nothing else. Every label needs a specific number as justification.

## Step 5 — Funnel Map, Danger Signals, Platform Status & Scaling Verdict

Map every ad to TOF/MOF/BOF per campaign. Name the gap ("No TOF ad — funnel not being fed", "All BOF — funnel drying up", "Healthy distribution"). If CPM **and** frequency are both rising, call it out loudly — that is the single loudest warning in the framework. Check the macro calendar (Knowledge Base) before blaming rising CPM on fatigue.

Also, per the Knowledge Base sections "Meta Platform Status Check" and "Budget Scaling Verdict":

- Check **metastatus.com/ads-manager** (+ /history) for incidents overlapping the window — flag in the report header, or state "no platform incidents in window".
- Compute each active campaign's **scaling verdict** (SCALE +10–20% / HOLD / TRIM −10–20%) with the pass/fail checklist.
- Compute the **account sentiment badge** (STRONG / STEADY / AT RISK / DECLINING) for the report header.

## Step 6 — Post-Click Audit (conditional)

Trigger this when an ad is **good at sending traffic but bad at converting it**: healthy spend + decent outbound clicks/CTR, but purchases-per-click clearly below campaign peers (or ATC rate fine but purchase rate poor).

Follow `references/post-click-audit.md` — do not shortcut it. Summary:

1. **Pass both trigger gates first.** (a) The ad must already clear the minimum-data bar — never audit an ad you just labelled *Insufficient data*. (b) The **one-purchase swing test**: recompute purchases-per-click with one more purchase; if that lands within ~80% of the campaign median, the gap is noise — don't audit, just note the small sample and move on.
2. **Establish the campaign's market BEFORE looking at the page** — from delivery, not from the campaign name. Pull `ads_get_ad_entities(level: "campaign", breakdowns: ["country"])`; the market is the country carrying the majority of spend. Audit the page **the way that market's customer sees it**: an AU-targeted campaign against the AUD storefront, a US-targeted campaign against the USD storefront. Auditing an AU campaign against a USD render (or vice versa) produces confident, wrong findings.
3. **Anchor on the store's base truth.** Shopify Admin API: `shop { currencyCode }` + `products.priceRangeV2` gives the base currency and base prices. On multi-market stores (Shopify Markets) the market may correctly see a different currency — base is your anchor, not necessarily what the market sees.
4. Get the landing page URL from `ads_get_creatives` (or ask the user which page the ad points to).
5. **Scrape geolocated to that market**: `firecrawl_scrape(url, location: {country: "<market>"})` — for copy, review language and structure.
6. **Reconcile.** Rendered currency matches the market → proceed, prices usable. Rendered currency ≠ market → *candidate finding* (page not localised for the market you're buying — a real conversion killer), **but verify in a real browser from that market before reporting**: a geolocated scrape is not proof of what the market sees, and headless fetches routinely miss market/currency treatment. Never convert — no FX maths on scraped prices, and every price quoted carries its currency.
7. **Cross-examine against the account's own numbers.** `ads_get_ad_accounts` gives the account `currency`; every Meta figure — including derived AOV — is in it. **AOV ÷ items-per-order ≈ the typical item price in that currency.** If the page's price points don't fit, the page is rendering a different currency. Needs no FX knowledge, works in any market. If a scraped fact contradicts the client config, assume the scrape is wrong until proven otherwise — never "correct" a client's config from a scrape.
8. Report the specific mismatch and 2–3 concrete fixes, stating the source and currency for every price quoted.

**DOM presence ≠ user-visible.** Never report a popup, banner or badge as live off the markup alone — disabled apps and unpublished sections leave complete markup behind. Verify computed visibility (`offsetParent`, bounding rect, `display`/`visibility`/`opacity`) in a real browser first.

Post-click problems are **not creative problems** — label the ad Fix with a landing-page note, don't kill a creative that's doing its job. Equally, **"the page is fine" and "the sample is too small to tell" are both complete, successful audits** — never go hunting for a cause just to have something to say.

## Step 7 — Funnel-Gap Creative Recommendations

Every recommendation must be grounded in — and explicitly reference — these five sources (skip a source only if it truly doesn't exist for this brand, and say so):

1. **Current account data** — what the 4PI numbers say is missing or fatiguing
2. **Brand intelligence / personas** (Step 1) — which persona, pain point, objection the new ad targets
3. **Customer reviews & social proof** — real customer language from the site/reviews (Firecrawl the site if needed); quote it when it shapes the angle
4. **Best practice** — format/funnel tendencies from the Knowledge Base (e.g. 9:16 for TOF, statics for BOF)
5. **The Ad Concept Board** — pick the concept by funnel tier and link its Foreplay board (Notion: https://hail-pond-0fc.notion.site/ebae3c1aaea34b8f9c85eaaa514d7f61?v=30f942daa302486d8c8d90731310b315)

State the success signal (target daily frequency + CPM position the new ad should land at).

**Hooks:** when the recommendation is a new creative test (not just a budget/landing-page action), generate 3–5 structurally-different opening hooks using `references/hook-generator.md` — grounded in the brand's product, personas, and review language. Also link [The Hook Bank](https://hooks.antoineorban.com/) for more.

**Hand off to the sister skills to actually produce the creative** (don't write full ad copy or scripts inline):
- **`eca-ad-copywriting`** — turn the recommended angle into headlines + primary text for the test.
- **`eca-ugc-scripts`** — when the concept is a video (UGC, Founder's Story, 3 Reasons Why, Comment Reply), hand it the funnel tier + angle and let it script the shoot.
- **`eca-brand-intelligence`** — the source of the personas, voice, objections and proof these recommendations must be grounded in.

**Escalation rule:** when a recommendation requires significant production effort, budget restructuring, offer changes, or you're not confident in the diagnosis, append: *"⚠ Double-check with the account owner before actioning."* Use it for genuinely big/uncertain calls, not routine ones — overuse makes it meaningless.

## Step 8 — Build the Branded HTML Report

Follow `references/html-report.md`. Reports use the **ECA Design System** (Ecommerce Academy branding — tokens and rules in `assets/ECA Design System/`), with the client named as "Prepared for <Brand>". Required section order:

1. Report header (brand logo/colors, date range, account totals, macro note)
2. Account snapshot — three window tables (7d / MTD / 30d)
3. Per campaign (sorted by spend desc): funnel map → 4PI table → ad breakdowns → diagnosis → next steps
4. Post-click audit findings (if run)
5. Account-level summary: top 3 priorities + systemic observations

Save as `4pi-report-<brand>-<YYYY-MM-DD>.html` in the outputs folder and present the file. **Also write the report memory**: `4pi-history-<brand>.json` next to the report AND the same JSON embedded in the report HTML as `<script type="application/json" id="fpi-history">` (schema in `references/report-memory.md`) — next week's run depends on it. Give a 3-bullet chat summary of the top priorities — the report is the deliverable, the chat is the headline.

---

## Core Rules (full list in Knowledge Base)

- Lead with 4PI — never headline with ROAS, CTR, or hook rate
- Every recommendation references a specific number
- Facebook is a meritocracy: spend is earned; low spend on a live ad means Facebook has voted
- Lower CPM + lower frequency = growing funnel; higher both = efficiency that's dying
- TOF ads with worse CPA are doing their job — say so when it applies
- Never "Scale" an ad or "Pause" anything — budget is campaign-level ("Scalable"), ads are stopped
- Profit per Order (AOV − CPA) overrides CPA for budget decisions; label it as a pre-COGS proxy
- Learning Limited is not a death sentence in small-budget accounts
- Image CPM ≠ video CPM; retargeting CPM ≠ prospecting CPM
- Cross-reference all three time windows before concluding anything

## Key References

- `references/4pi-knowledge-base.md` — the complete framework (read first, every time)
- `references/mcp-data-pull.md` — exact Meta MCP pull sequence and window math
- `references/post-click-audit.md` — Firecrawl landing-page mismatch workflow
- `references/report-memory.md` — week-over-week continuity, history schema, accountability card
- `references/hook-generator.md` — Andromeda-diverse hook generation for creative tests
- `references/html-report.md` — branded HTML report template and section spec
- `clients/README.md` — client brand config format and onboarding
