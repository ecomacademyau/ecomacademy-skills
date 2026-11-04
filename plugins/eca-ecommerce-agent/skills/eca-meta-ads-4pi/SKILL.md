---
name: eca-meta-ads-4pi
description: "Analyse a Meta ads account live via the official Meta Ads MCP (CSV fallback) with the 4PI framework and produce an ECA branded HTML report with scaling verdicts. Use for any Meta ads report, 4PI analysis, weekly ad report, creative or funnel analysis, CPM, CPA or NCPA questions, scaling, which ads to stop, landing page mismatch, 'check my ads' or 'run the 4PI', and for sale campaigns: Black Friday, BFCM, BOGO, flash sales, launches, 'how is the sale going', 'should I push budget', 'what should I kill or add'. Includes NCPA and new vs existing splits, lead gen, catalog (frequency bands, product set exclusion checks, product cuts) and promo modes (daily push, pace or pull back calls, kill and add rules), Firecrawl landing page audits and metastatus.com checks."
metadata:
  version: "2.5.0"
---

# Meta Ads 4PI Analyst v2.7.0

Analyse Meta ad performance with the 4PI framework (Spend, CPM, Frequency, CPA), map each campaign's funnel, diagnose creative and post-click problems, and deliver a **branded HTML report** the client can open in a browser. Print the skill version (v2.7.0, from this file's title) in the report footer so every report states which version produced it. Version history: `CHANGELOG.md` (v2.7.0 adds Catalog Product Checks: product set reads, exclusion tests, weekly product breakdowns, change verification, marginal cut maths, tripwires, overlap and budget step history).

**Before any analysis, read the Knowledge Base:** `references/4pi-knowledge-base.md`. It contains the full 4PI playbook — funnel decoder, golden rule, profitability proxy, creative diagnostics, macro calendar, Ad Concept Board, and tone rules. The analysis is only as good as fidelity to that framework.

---

## Workflow at a Glance

1. **Identify the client** → load/create brand config (`clients/`) + **load report memory** (previous run's history — `references/report-memory.md`)
2. **Pull data** → Meta Ads MCP (preferred) or CSV fallback
3. **Verify numbers** → print verification tables before analysing
4. **Classify each campaign, then analyse it by type** → purchase campaigns: 4PI, funnel map, action labels, **NCPA and audience-segment read** (new · engaged · existing, setup status); lead gen and catalog: their own reads (`references/campaign-types.md`), and every catalog campaign gets the **Catalog Product Checks** below (product set read, exclusion test, weekly products); **promo campaigns** (sale, BOGO, BFCM, launch): Promo Mode below, with daily PUSH / PACE / PULL BACK budget calls and kill / keep / add content rules
5. **Creative diagnostics** → hook/hold/CTR waterfall
6. **Post-click audit (conditional)** → Firecrawl the landing page when traffic is good but conversion is poor
7. **Funnel-gap creative recommendations** → cross-reference personas + Ad Concept Board + Hook Bank
8. **Build the branded HTML report** → deltas vs last report + accountability card → save the report AND the new history file

---

## Step 0 — Ask Before Pulling (always, unless already answered)

Before running any pulls, ask the user three questions (four when a sale is running) — in one AskUserQuestion call when available; skip any question already answered by the request or the client config:

1. **"What's your target, and is it per order or per new customer?"** Options: **"Per order (CPA, first-order mode)"**, **"Per new customer (NCPA, LTV mode)"**, **"Both"**, **"I don't know"**; the user types the number(s) in the free-text answer (e.g. "$65 NCPA, $21 CPA"). This sets the **target mode** (`first_order` / `ltv` / `both`, Knowledge Base "Audience Segments, NCPA & Target Modes"). If they don't know, reply with: *"See your ecomOS to know your target CPA per channel"*, then proceed with no target — CPA gets judged against campaign peers and profitability, and the report states "no target CPA set". If they pick a mode but give no number, ask once for it. Add to the same question: "and a cost per lead if you run lead campaigns" (`target_cpl`). Never invent a target. Skip the question when the client config already has `target_mode` and its number(s).
2. **"Whole account, or a specific campaign?"** — offer "Whole account" and let them name a campaign. If a specific campaign is chosen, scope every pull and every section to it (the account snapshot shrinks to that campaign's three windows).
3. **"Full report, or Quick check?"** — two options, with the recommended one chosen by context: **Full** recommended for a client's first report or when the last report is >2 weeks old; **Quick** recommended for routine re-runs when report memory exists. Describe them honestly in the options: *Full — complete deep dive: ad breakdowns, creative hooks, post-click audit, seasonality + industry benchmark* · *Quick — same analysis and verdicts, condensed report: scorecard, top priorities, one snapshot table, scaling verdicts and only the ads to act on (fewer tokens, faster)*. Skip the question when the request already says it ("quick check", "full report", "light version").
4. **Promo plan, only when a sale is running or starts within 14 days** (the request, client config or history says so): end date and time, offer mechanic, budget plan, stock ceiling and promo target or cost data (Promo Mode §2). Skip it when the history already holds the plan for this promo. If no sale was mentioned but Step 2 detects a promo campaign, ask it then.

**What Quick mode changes — and what it never changes.** The analysis is identical in both modes: all core pulls (three windows, daily, structure, campaign-level audience segments, creatives for format badges), verification tables, 4PI maths, status detection, thresholds, action labels, scaling verdicts, and the report memory read + write. Quick mode only (a) skips the optional enrichment calls — YoY seasonality pulls, industry benchmark, anomaly/opportunity, post-click scrapes — and (b) renders the condensed report. If an ad meets the post-click trigger gates in Quick mode, don't run the audit — flag it in one line: "TEST#X qualifies for a post-click audit — run a Full report to investigate." Never degrade the analysis itself to save tokens; verdicts must be equally trustworthy in both modes.

**Quick mode is campaign-level** (full spec in html-report.md "Report depth modes"): a funnel-health bar per campaign instead of a per-ad funnel map, an "Ads to act on" table instead of the full 4PI ad-by-ad grid, diagnosis merged into next steps, priorities capped at ~120 words. **Campaign triage is what keeps length flat as accounts grow**: full treatment only for campaigns ≥10% of account spend or carrying a red flag; the rest get their snapshot row and one sentence. Target ≈2,000–2,500 words whether the account has one campaign or six. Ad-level evidence still appears for every ad you're asking them to action — never recommend a stop without its numbers.

## Step 1 — Identify the Client & Load Brand Config

Ask which brand/account this analysis is for if not obvious from context.

- Check `clients/<brand-slug>.md` inside this skill for an existing config (brand colors, logo, currency, target mode with `target_cpa` / `target_ncpa`, `target_cpl` for lead campaigns, website, personas pointer).
- If none exists, run the short onboarding in `clients/README.md`: ask for brand name, primary/accent colors (or derive from their website), logo URL, currency, target mode with its number(s) (`target_cpa` and/or `target_ncpa`), and website. Echo the completed config block back to the user so they can save it into the skill for next time.
- Also look for brand intelligence: `brand-data.md` per `eca-brand-intelligence/references/brand-file-location.md` (`$ECA_BRAND_FILE`, `./brand/brand-data.md`, `./brand-data.md`, `./skills/*/brand-data.md`), then `brand-dna.md` or `icp-cards.md` for this brand (e.g. from icp-deep-dive). If found, read the personas, angles, and objections — they drive Step 7. If not found, proceed and note in the report that persona-level recommendations are generic.

**Targets** (`target_cpa`, `target_ncpa`) and the **target mode** come only from the client config or directly from the user — never invent one. In `ltv` mode the KPI is NCPA, never blended CPA against the LTV number. If none is available, run the analysis without a target: judge CPA relative to campaign peers and profitability, state "no target CPA set" in the report, and for the minimum-data spend threshold use 2× the campaign's blended CPA (labelled as a data-sufficiency bar, not a performance target). Lead gen campaigns use `target_cpl` (from the config or the Step 0 answer); none given: write "no CPL target set" and judge CPL against the campaign's own windows.

**Report memory:** also load the previous run's history now — look for `4pi-history-<brand-slug>*.json` in the outputs folder, else in the attached claude.ai Project if there is one (Projects tool: `project_search`/`project_read`, e.g. `claude/4pi-history-<brand-slug>.json`; the outputs folder usually doesn't survive between sessions), else the embedded `fpi-history` block in the latest `4pi-report-<brand>-*.html`, else ask once for the last report file. Full workflow, schema, and accountability rules: `references/report-memory.md`. No memory found → first-run mode (say so in the report; never fabricate a baseline).

## Step 2 — Pull Data

### Option A: Official Meta Ads MCP (preferred)

Use the **official Meta Ads MCP** (tools named `ads_*`). Follow `references/mcp-data-pull.md` exactly — it has the verified field names. Summary:

- `ads_get_ad_accounts` → find the account, check `is_ads_mcp_enabled` and `is_queryable`, note the **currency** (it anchors every money figure in the report)
- `ads_get_field_context` → verify any uncertain field before querying
- `ads_get_ad_entities` at **ad level** for three windows (last_7d, MTD custom range, last_30d) plus a `time_increment: "1"` daily pull for the funnel decoder's daily frequency and the last-5-days spend trajectory
- `ads_get_ad_entities` at campaign + adset level for budgets, objectives, `delivery_sub_status` (learning phase), `attribution_setting`, and `promoted_object` (it carries the catalog ad set's `product_set_id`)
- `ads_get_ad_entities` at **campaign level with `breakdowns: ["country"]`** → the **delivered market** per campaign. There is no geo/targeting field in the catalog, so this breakdown is the only way to know which market a campaign actually reaches — and delivery beats the campaign name. Needed for Step 6 and for any market/currency claim.
- **Year-over-year seasonality pulls** at **account level**: the same calendar windows shifted one year back (custom `time_range`, e.g. this 30d window in the previous year, and the same MTD range last year). Fields: `amount_spent, impressions, cpm, frequency, results, cost_per_result, purchase_roas`. Rules and interpretation: Knowledge Base "Year-over-Year Seasonality Check". No data last year → skip gracefully.
- **Audience-segment pulls** (`breakdowns: ["user_segment_key"]`, every sales campaign, 30d + 7d, plus a pre-event baseline when a promo overlaps; account level over 90 days before calling segments missing). Works on manual campaigns, not only Advantage+ Shopping. Spec: mcp-data-pull.md §3b. Quick and Full; the ad-level segment pull is Full only.
- **Campaign type** for every campaign: lead gen (objective or results are leads), catalog (creative has a `product_set_id`), purchase, or other. Lead and catalog campaigns get a campaign-level daily pull for frequency, lead campaigns get the lead field, and every catalog campaign gets the product set read and the weekly `product_id` breakdown in **Catalog Product Checks** below (verified live). Spec: mcp-data-pull.md §3c and `references/campaign-types.md`. Promo campaigns (Promo Mode §1) also get a since-launch custom range pull, a last 3 days pull and the pre-event baseline.
- **Shopify cross-check** (optional; attempt whenever the target mode is `ltv` or `both`): only if a Shopify connector is on the client's own store (`get-shop-info` domain matches). Pulls new vs returning customers for the Meta NCPA floor (Meta spend ÷ Shopify new customers). Never use a connector signed into another store.
- `ads_get_creatives` (with creative_ids) → creative type, copy, and **landing page URL** (needed for Step 6)
- Optional enrichment: `ads_insights_anomaly_signal`, `ads_get_opportunity_score`, and `ads_insights_industry_benchmark` (peer comparison vs similar advertisers — see mcp-data-pull.md §6b; frequently returns "no data" for small accounts, skip gracefully) — supporting context only, never the headline

If the connector errors with an expired/invalid token, stop and tell the user to reconnect the Meta connector — do not fabricate data and do not silently fall back to old numbers.

### Option B: CSV upload (fallback)

If no working Meta MCP, ask for a Facebook Ads Manager export. CSV handling rules (column mapping, aggregation, date windows) live in the Knowledge Base under "Data Processing". The CSV path unlocks extras the API pull may not have: GPT column, thumb-stop ratio. On this path audience segments come from the Audience Segments column (the API path pulls them with `user_segment_key`). Use them when present.

## Step 3 — Verify Before Analysing

**Mandatory.** Print a verification table per time window before drawing any conclusion:

```
=== VERIFICATION: [WINDOW] ([dates]) ===
| Campaign | Type | Ads w/ data | Spend | Purchases (or leads) | Blended CPA (or CPL) | AOV | Profit/Order |
```

Plus one segment table per window pulled with `user_segment_key`:

```
=== SEGMENTS: [WINDOW] ([dates]) ===
| Campaign | New spend / purch | Engaged spend / purch | Existing spend / purch | Unknown spend | Σ spend = campaign? | NCPA |
```

Sanity checks: segment spend sums to campaign spend (else no NCPA for that campaign); 7d spend ≤ 30d spend; MTD spend ≤ 30d spend when the month is young; purchases and spend must be internally consistent (CPA ≈ spend/purchases). Every number in the final report must trace back to these pulls — never estimate, never fill gaps with plausible numbers. If a window has no data, say so.

## Step 4 — 4PI Analysis (Per Campaign, In Isolation)

**Route by campaign type first.** Lead gen and catalog campaigns follow `references/campaign-types.md`: their own metrics, data bar, labels, scaling verdict and report section. Catalog campaigns also run the Catalog Product Checks below. Never run them through the purchase 4PI table, the funnel map or an NCPA judgement. **Promo campaigns** follow Promo Mode below: since-launch windows, the promo data bar, promo target and kill CPA, and their own labels. The rest of this step is the purchase 4PI.

All comparison is **within a campaign** — never across campaigns. For each ad:

1. **Spend** — % of campaign spend, trend (compare 3d/7d/30d run-rates)
2. **CPM** — lowest/median/highest in campaign, trend, creative-type context (image vs video)
3. **Frequency** — funnel position via the decoder (< 1.15 TOF | 1.15–1.40 MOF | > 1.40 BOF | > 2.0 saturation). Use the **average of the daily frequencies** from the `time_increment: "1"` pull as the decoder input; the 7d/30d aggregate frequency is the trend line. Cross-check CPM and frequency agree (and `cpp` vs `cpm`).
4. **Efficiency** — CPA (`cost_per_result`) vs campaign and vs target; **Profit per Order = AOV − CPA** (pre-COGS proxy; AOV = purchase_roas × spend ÷ purchases — see Knowledge Base "Profitability"). Profit/Order overrides raw CPA for scaling decisions. If a true GPT column exists (CSV path) or the client config has a gross-margin %, upgrade the proxy accordingly.

5. **New-customer efficiency (campaign level):** NCPA (all campaign spend ÷ new + engaged purchases), existing share of spend and purchases, existing vs new frequency. In `ltv` mode NCPA vs `target_ncpa` replaces blended CPA vs target in the campaign's verdict; in `both` mode both must pass. Ad labels follow the Knowledge Base "Ad labels by mode" (identical in Quick and Full). Promo overlapping the window → judge always-on campaigns on the pre-event baseline and say so (Knowledge Base, "Promo distortion rule").

Classify each ad ACTIVE / STOPPED / WINDING DOWN and apply the minimum-data threshold (≥ 7 days AND spend ≥ 2× target CPA) **before** assigning any action label. Never recommend stopping an ad that is already stopped.

Labels come from the **7-day** window, with one exception: an ad whose 7 days are statistically thin (≤ 2 purchases, or spend < 2× target CPA in that window) is judged on its **30-day** figures instead — print both and state which drove the call (Knowledge Base, "Small-Sample Rule"). Frequency and CPM headline values and their trend labels must be computed from one series and agree with each other (same section, "One computation, one label").

Action labels: **Keep / Hold / Fix / Watch / Stop / Scalable / Insufficient data** — nothing else. Every label needs a specific number as justification.

## Step 5 — Funnel Map, Danger Signals, Platform Status & Scaling Verdict

Map every ad to TOF/MOF/BOF per campaign. Name the gap ("No TOF ad — funnel not being fed", "All BOF — funnel drying up", "Healthy distribution"). If CPM **and** frequency are both rising, call it out loudly — that is the single loudest warning in the framework. Check the macro calendar (Knowledge Base) before blaming rising CPM on fatigue.

Also, per the Knowledge Base sections "Meta Platform Status Check" and "Budget Scaling Verdict":

- Set the **audience-segment setup status** (OK · PARTIAL · SUSPECT · NOT SET UP · UNAVAILABLE) and the **existing over-serving** flag per the Knowledge Base. Non-OK statuses go in the Watch line with "confirm in Ads Manager"; NOT SET UP in `ltv`/`both` mode becomes a top-3 priority; UNAVAILABLE is reported as an API gap to re-check next run.
- Check **metastatus.com/ads-manager** (+ /history) for incidents overlapping the window — flag in the report header, or state "no platform incidents in window".
- Compute each active campaign's **scaling verdict** (SCALE +10–20% / HOLD / TRIM −10–20%) with the pass/fail checklist. Lead gen and catalog campaigns use their own verdict tables (`references/campaign-types.md`); for catalog, daily frequency decides whether it can scale (< 1.50 room · 1.50 to < 1.80 healthy · 1.80 to < 2.00 hold · ≥ 2.00 saturated), and the budget step history (Catalog Product Checks §8) can turn a SCALE into a HOLD. **Promo campaigns get PUSH / PACE / PULL BACK instead** (Promo Mode §5).
- Compute the **account sentiment badge** (STRONG / STEADY / AT RISK / DECLINING) for the report header. **Sentiment measures money only** — profit/order, CPA vs target (NCPA vs `target_ncpa` in `ltv`/`both` mode), share of spend that's unprofitable, all on purchase and catalog campaigns only (lead and other campaigns stay out of the money maths; a lead-only account badges on CPL, `references/campaign-types.md` §4). CPM moves, funnel gaps, single-ad concentration and frequency drift never set the badge on their own; they become the header's **Watch flags** line and feed the scaling verdict instead. An always-amber badge is a useless badge — see Knowledge Base, "Account sentiment", including the calibration check (if the badge contradicts its own sentence, the badge is wrong).

## Catalog Product Checks (every catalog campaign)

What a catalog campaign sells is decided by its product set, and the product set is edited in Commerce Manager, so its changes never appear in the ad account's activity log. The frequency bands and product cut rules in `references/campaign-types.md` §3 still apply; these checks make sure the set is what everyone thinks it is, and that a cut is worth making. Run them in Full mode on every catalog campaign, and in Quick mode whenever the user says a product was added or excluded, or history holds an open product cut or tripwire.

### 1. Read the product set, not just the spend

Take the set id from the catalog ad set's `promoted_object.product_set_id` (ad set level pull), then `ads_catalog_list_product_sets(entity_id: <set id>)` for its `name`, `product_count` and `filter_rule`. Print the exclusion rules under the catalog row of the verification table.

### 2. Test every exclusion against the catalogue

For each product the filter is meant to exclude, query the set itself: `ads_catalog_list_products(entity_id: <set id>, filter: {"or":[{"retailer_id":{"eq":"<id>"}}, ...]})`, or a name filter. If the product comes back, the exclusion is not working. Name rules written with `neq` are exact matches, so a plural, a renamed title or a new edition breaks them without any warning (Up On The Rooftop, Oct 2026: the rule said "Terracotta Watering Spikes", the catalogue item was "Terracotta Watering Spike", and the spike kept about 22% of DPA spend for five weeks after it was meant to be out). Recommend `i_not_contains` on a stable stem ("watering spike") or `retailer_id` exclusions. Never write "excluded" in a report until the product returns zero rows from the set and near zero spend in delivery.

### 3. Read products by week, not by 30 days

Pull the ad level `breakdowns: ["product_id"]` with `time_increment: 7` over the last 8 weeks, alongside the 30 day sum the cut rules use. A 30 day total blends the weeks before and after a change and hides the week a product appeared or vanished. Rows come back per product per period and the page stops at 200 rows without saying so: rows ≈ products × periods, so split the range (about 3 weeks per call for a 50 product catalogue), and check that each period's product rows add up to the ad's spend for that period. If they don't, the pull is truncated: shorten the window before concluding anything. Daily product breakdowns on a big catalogue almost always truncate.

### 4. Verify a change happened before crediting it

When the user or the history credits a result to a change (a product removed, a budget move, a new ad), confirm the change in delivery first. Budget, status and targeting edits: `ads_account_get_activity_logs` filtered to the campaign. Product set edits: only the weekly product breakdown shows them (the product's spend drops to near zero from the change week). No sign of the change: say so plainly, show the evidence, then explain what actually moved the number. Never agree that a change worked because the timing fits.

### 5. Before cutting a product, use the marginal comparison

The cut rules flag candidates. Before recommending the cut, compare the product's last 10 to 14 days with the rest of the catalogue's CPA over the same days, and with both over the full 8 weeks. Removing a product moves its spend to the rest of the catalogue at the rest's current rate, not its long run average. **Expected gain = product spend ÷ rest CPA − product purchases**; state it in purchases and in the campaign CPA it would produce. If the rest of the catalogue is currently buying worse than the product, keep the product with a tripwire (§6) and say why. Product breakdowns credit a purchase to the product shown in the ad, which isn't always the product bought: say so whenever a product level CPA drives a recommendation, and recompute with one purchase more and one less. If the call flips, it's Watch, not cut.

### 6. Tripwire for a volatile product kept in the set

Remove it if either: a week where it spends 2× target or more with 0 purchases, or its rolling 14 day CPA passes 1.5× target. Store the tripwire with the product ids in the recommendation (`references/report-memory.md`) and check it every run.

### 7. Overlap with a dedicated campaign

When a product in the catalog also has its own prospecting campaign, flag that part of its catalog sales are probably people the dedicated campaign warmed up; the catalog reaches them at a lower CPM and takes the credit. Print both CPMs. It can't be sized without a lift test, so it tips a close call towards excluding the product, never becomes a number of its own.

### 8. Budget step history

Pull the catalog ad set's budget changes for the last 6 weeks from `ads_account_get_activity_logs` (event category `budget`). Raises above +10% per step in the healthy band, or raises adding up to more than +30% in a month while the rest of catalogue CPA climbs, are a Watch flag and a HOLD reason, printed with the dates and amounts.

### Report

In the catalog section, after the products to cut: a **product set card** (set name, product count, the exclusion rules with a working / not working tick each) and, when a product is under discussion, a weekly table `Week | Campaign CPA | Product share of spend | Product purchases | Rest of catalogue CPA`.

## Promo Mode: sale, launch and BFCM campaigns

Sale campaigns are not evergreen campaigns with a deadline. They harvest demand the always-on campaigns built, they run on a discounted margin, and they end. The evergreen checklist (7 day windows, a TOF ad, 10 to 20% budget moves every 3 to 4 days) gives wrong answers for them: it can never say yes to a good promo, and it reacts days too late for a 4 day event. Promo mode replaces the reads, labels and verdicts for **promo campaigns only**; always-on campaigns running beside them keep the standard 4PI with the Promo distortion rule (Knowledge Base).

### 1. Detect and classify

A campaign is **promo** when any of these hold: its name carries a sale marker (SALE, BOGO, BFCM, BLACK FRIDAY, CYBER, CLICK FRENZY, EOFY, FLASH, LAUNCH, % OFF, GWP); its creatives carry an offer with a deadline or quantity limit (`body` / `title`: "ends", "last chance", "limited", "Buy 3 Get 1", "% off"); or the user, client config or history says a sale is live. Print the type in the verification table. Length decides cadence:

| Promo length | Cadence | Label window |
|---|---|---|
| Short, 7 days or less (BFCM, flash, Click Frenzy) | Daily read, Quick by default | Since launch, plus yesterday and last 3 days |
| Medium, 8 to 21 days | Every 2 to 3 days | Since launch, plus last 3 days |
| Long, over 21 days | Weekly | Standard 7d / 30d, with the promo economics in §3 |

A catalog campaign during a sale stays catalog (`references/campaign-types.md`) and gets the feed check in §6.

### 2. The promo plan (ask once, store in history)

Ask once per promo, in Step 0 when a sale is known or as soon as Step 2 detects one, in a single AskUserQuestion: **end date and time** (with timezone), **offer mechanic**, **planned total spend or daily budget plan**, **stock ceiling for the hero products**, and either a **promo target CPA** or the product cost data to compute one (client config `gross_margin_pct`, or the ecomOS economics tab). Store it under `promo` in the history JSON (`references/report-memory.md`) so every daily run judges against the same plan, with each day's call appended. Missing pieces: no end date → judge efficiency, never pacing, and say so; no budget plan → treat the current daily budget × days left as the plan; unattended run → proceed with those defaults and say which were assumed. State the ad account's timezone for "today" and the end time.

### 3. Promo economics: the target moves with the offer

**Promo target CPA = evergreen per order target × (gross profit per order on the offer ÷ gross profit per order at full price).** Compute it from cost data, never guess. Two worked examples:

- 30% off sitewide on an 80.7% gross margin: gross profit per $100 of RRP falls from $80.74 to $50.74, so the promo target is about 0.63 × the evergreen target.
- Buy 3 get 1 free on an 85.6% margin product: margin on the bundle falls to about 80.7%, so the target barely moves (about 0.94 ×).

No cost data: hold the promo to the evergreen target and print "promo margin not adjusted". Profit per order during a promo uses the margin after the discount when cost data exists; the AOV minus CPA proxy overstates a promo (it rewards the bigger basket and ignores the discount), so label it clearly when it's all there is. **Kill CPA = 1.5 × promo target.**

### 4. Reading a promo

- **Data bar:** 24 hours live and spend at or above 1 × promo target for a first read; 2 × promo target before a Stop. A 4 day sale cannot wait 7 days.
- **Yesterday is provisional:** purchases keep landing for days after a click, so yesterday's CPA improves over the next reads. Never stop or pull back on a single day; act on two consecutive reads or on the since-launch number.
- **No TOF test and no funnel gap verdict** inside a promo campaign: harvesting is its job.
- **Frequency:** deadline reminders are part of the job, so the saturation line moves: daily frequency up to 2.0 is normal, above 2.5 is saturation mid-sale, above 3.0 in the final 48 hours. CPM + frequency both rising counts as a warning only when CPA rises with them on two consecutive reads.
- **CPM context:** compare with the same day of the last comparable event (BFCM day 2 vs last year's day 2) from history or a custom range pull, never with the last 30 days. Event CPMs run 2 to 5x.
- **Trust order:** Shopify MER (only when the Shopify connector is on the client's own store) over Meta's attributed purchases, because view through and engaged view credit spike during sales.
- **Who buys:** new vs existing share from `user_segment_key` against the pre-event baseline. A promo selling mostly to existing customers is a discount, not growth: say so with the numbers.

### 5. Budget calls: PUSH / PACE / PULL BACK (daily, per promo campaign)

Checked in this order: PULL BACK, then PUSH, else PACE. One move per read, at most one per day. Render as the big badge with a pass/fail checklist, like the evergreen verdict.

| Call | Conditions |
|---|---|
| **PULL BACK −20 to 30%** | any: since-launch CPA above 1.3 × promo target on two consecutive reads with at least 2 × target spent · Shopify MER below the plan's floor on two consecutive days · stock covering less than 2 days of projected sales |
| **PUSH +20 to 30%** | all: since-launch CPA at or below promo target · last 3 days CPA at or below 1.1 × promo target · hero daily frequency under 2.0 (2.5 in the final 48 hours) · stock covers projected sales to the end date · more than 24 hours left |
| **PACE** | everything else: follow the plan |

Bigger and faster than evergreen on purpose: in a short sale a learning reset costs less than missing the window. Where available, set the plan's increases in advance with Meta's budget scheduling. Weight the plan to the first 24 hours and the final 48 hours; the middle days are the dip. Spending ahead of plan is fine when PUSH holds: spend follows demand, not the calendar.

**At the end date:** turn the promo off on time, return always-on budgets to their pre-promo level the same day, and treat any always-on raise made on promo numbers as a TRIM candidate. Never recommend extending an advertised deadline (misleading under Australian Consumer Law, and the same principle elsewhere): recommend a new, clearly different offer instead, with "⚠ Double-check with the account owner before actioning."

### 6. Content calls: kill, keep, add

Every line in the report's Kill / Keep / Add list carries the number that triggered it.

**Kill (Stop)**, any:
- spend at or above 2 × promo target with 0 purchases
- since-launch CPA above the kill CPA (1.5 × target) with at least 2 × target spent
- the top spender only after two consecutive reads over the kill CPA, never on one bad day
- phase copy that has expired (early access or "starts tomorrow" once the sale is live; "ends tonight" after the end date): stop it when the phase ends

**Starved ads:** after 48 hours under 5% of campaign spend in a campaign with 3 or more ads, Facebook has voted. With CPA at or under target on that small spend and more than 3 days left, move it into its own ad set; otherwise replace it with a structurally different creative, not a copy.

**Keep:** everything else that clears the data bar at or under the kill CPA.

**Add**, any:
- one ad carries more than 75% of campaign spend with more than 3 days left
- the hero's daily frequency passes 2.0 (2.5 in the final 48 hours)
- the hero's link CTR falls 30% or more from its launch day level, or its CPA rises 25% or more over its since-launch level on two consecutive reads
- a phase starts (launch, final 48 hours, last chance)

Add into the existing promo ad set rather than spinning up new ad sets: new ad sets split the budget and start from zero data.

**The bench:** a promo is only as reactive as the creative ready before launch. In the pre-sale report, recommend at least three structurally different promo creatives per phase: the offer announcement (mechanic and end date readable without sound in the first 2 seconds), product proof plus offer, founder or UGC plus offer, a last chance or countdown version, and static offer cards for BOF. Urgency and scarcity claims must be true (end dates, limited stock, sold out counts). **Catalog during a promo:** check the feed shows the sale price or an offer overlay, otherwise the catalog advertises the sale hero at full price to people who have seen the offer.

### 7. Incrementality (every promo report)

The promo campaign always looks good because it collects what the always-on campaigns built, so judge the account, not the campaign: total purchases, spend and CPA across all campaigns (plus Shopify MER when available) for the promo days vs the same number of days before; the always-on campaigns' purchases before vs during (cannibalisation); and the new customer share vs baseline. After the end date, read 7 and 14 days after against the pre-event baseline (the hangover).

### 8. Debrief (first run after the end date)

One card, saved to history as `promo_debrief` so the offer builder (`eca-bfcm-offer-builder`) and next year's event can read it: plan vs actual spend; promo target vs actual CPA and MER; best and worst creative by phase; every PUSH and PULL BACK day and what followed; incrementality and hangover; stock outs; three lessons for the next sale.

### 9. Report layout in promo mode

Header gets a PROMO chip ("Day 3 of 4 · ends Sun 30 Nov, 23:59 account time") and the day's call. The promo campaign section comes first: pacing bar (spent vs plan, days left), the call with its checklist, ad table `Ad | Phase | Spend since launch | % camp | CPA since launch | CPA last 3 days | Daily freq | Action`, the Kill / Keep / Add list, the incrementality card, then the always-on campaigns as usual. Daily reads default to Quick; Full at launch and for the debrief.

## Step 6 — Post-Click Audit (Full mode; conditional)

Purchase campaigns only (lead gen and catalog skip it: `references/campaign-types.md`). Trigger this when an ad is **good at sending traffic but bad at converting it**: healthy spend + decent outbound clicks/CTR, but purchases-per-click clearly below campaign peers (or ATC rate fine but purchase rate poor).

Follow `references/post-click-audit.md` — do not shortcut it. Summary:

0. **Decompose the click first** (click→page · page→cart · cart→buy · purchases/click, per ad with a campaign row). The step that varies across creatives is the diagnosis: everything downstream of the cart is creative-independent, so a prospecting ad losing people at page→cart with a healthy cart→buy is **TOF economics, not a broken page** — say so and don't audit. Quantify the spread; it's the proof.
1. **Pass all three trigger gates.** (a) The ad clears the minimum-data bar — never audit an ad you just labelled *Insufficient data*. (b) The **one-purchase swing test**: recompute purchases-per-click with one more purchase; if that lands within ~80% of the campaign median, the gap is noise. (c) The decomposition points at a step the page actually controls.
2. **Establish the campaign's market BEFORE looking at the page** — from delivery, not from the campaign name. Pull `ads_get_ad_entities(level: "campaign", breakdowns: ["country"])`; the market is the country carrying the majority of spend. Audit the page **the way that market's customer sees it**: an AU-targeted campaign against the AUD storefront, a US-targeted campaign against the USD storefront. Auditing an AU campaign against a USD render (or vice versa) produces confident, wrong findings.
3. **Anchor on the store's base truth.** Shopify Admin API: `shop { currencyCode }` + `products.priceRangeV2` gives the base currency and base prices. On multi-market stores (Shopify Markets) the market may correctly see a different currency — base is your anchor, not necessarily what the market sees.
4. Get the landing page URL from `ads_get_creatives` (or ask the user which page the ad points to).
5. **Scrape geolocated to that market**: `firecrawl_scrape(url, location: {country: "<market>"})` — for copy, review language and structure.
6. **Reconcile.** Rendered currency matches the market → proceed, prices usable. Rendered currency ≠ market → *candidate finding* (page not localised for the market you're buying — a real conversion killer), **but verify in a real browser from that market before reporting**: a geolocated scrape is not proof of what the market sees, and headless fetches routinely miss market/currency treatment. Never convert — no FX maths on scraped prices, and every price quoted carries its currency.
7. **Cross-examine against the account's own numbers.** `ads_get_ad_accounts` gives the account `currency`; every Meta figure — including derived AOV — is in it. **AOV ÷ items-per-order ≈ the typical item price in that currency.** If the page's price points don't fit, the page is rendering a different currency. Needs no FX knowledge, works in any market. If a scraped fact contradicts the client config, assume the scrape is wrong until proven otherwise — never "correct" a client's config from a scrape.
8. Report the specific mismatch and the fix, chosen from the **fix ladder** (copy/framing → reorder → section addition → **advertorial/listicle lander** → **dedicated campaign landing page** → quiz funnel). Always the cheapest fix that addresses the diagnosed step; escalate to a new page only when the mismatch is structural — an education- or founder-story-led ad pointing at a bare PDP is the classic advertorial case, a bundle/promo ad pointing at a generic collection is the dedicated-lander case. State the expected signal (which decomposition step should move, and roughly to what), the source and currency for every price quoted, and add the account-owner escalation note for anything at advertorial tier or above.

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

**Hooks:** when the recommendation is a new creative test in a purchase campaign, or a Fix on a lead ad (not just a budget/landing-page action), generate 3–5 structurally-different opening hooks using `references/hook-generator.md` — grounded in the brand's product, personas, and review language. Also link [The Hook Bank](https://hooks.antoineorban.com/) for more. Catalog campaigns get 2 or 3 short primary-text lines for a duplicate instead of hooks.

**Hand off to the sister skills to actually produce the creative** (don't write full ad copy or scripts inline):
- **`eca-ad-copywriting`** — turn the recommended angle into headlines + primary text for the test.
- **`eca-creative-strategist`** — when the concept is a video (UGC, Founder's Story, 3 Reasons Why, Comment Reply), hand it the funnel tier + angle and let it script the shoot.
- **`eca-brand-intelligence`** — the source of the personas, voice, objections and proof these recommendations must be grounded in.

**Escalation rule:** when a recommendation requires significant production effort, budget restructuring, offer changes, or you're not confident in the diagnosis, append: *"⚠ Double-check with the account owner before actioning."* Use it for genuinely big/uncertain calls, not routine ones — overuse makes it meaningless.

## Step 8 — Build the Branded HTML Report

Follow `references/html-report.md`. Reports use the **ECA Design System** (Ecommerce Academy branding — tokens and rules in `assets/ECA Design System/`), with the client named as "Prepared for <Brand>". Required section order:

1. Report header (brand logo/colors, date range, account totals, sentiment, Watch line, platform status, macro note, targets chip) with the collapsed "How to read this report" glossary
2. Account scorecard, then the **Top 3 priorities** (decisions before detail, html-report.md §2a), then the Since Last Report card
3. Account snapshot: one table across 7d / MTD / 30d with campaign type and NCPA, then the **Audience Segments & NCPA card** (Full mode, html-report.md §3b), the **Seasonality vs Last Year card** (§3c) and the Industry Benchmark card when fetched (§3d)
4. Per campaign (sorted by spend desc; a live promo campaign first, in its promo layout, Promo Mode §9), laid out by type. Purchase: funnel map → 4PI table → ad breakdowns (ads with a decision only; thin ads collapsed) → diagnosis → scaling verdict → next steps. Lead gen and catalog: their own layouts (`references/campaign-types.md`), with the catalog's product set card (Catalog Product Checks, Report)
5. Post-click audit findings (if run)
6. Systemic observations

Follow the html-report.md "Readability rules": ≈ 4,000 to 5,000 words for Full, one home per number, plain words with a glossary, stacked tables on a phone.

Save as `4pi-report-<brand>-<YYYY-MM-DD>.html` in the outputs folder and present the file. **Also write the report memory**: `4pi-history-<brand>.json` next to the report AND the same JSON embedded in the report HTML as `<script type="application/json" id="fpi-history">` (schema in `references/report-memory.md`) — next week's run depends on it. When the session is attached to a claude.ai Project, also save the history JSON there (`project_write`, path `claude/4pi-history-<brand>.json`) so it survives the session. Give a 3-bullet chat summary of the top priorities — the report is the deliverable, the chat is the headline.

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
- In `ltv` mode the KPI is NCPA (spend ÷ new + engaged purchases); Meta's "new" is a proxy, not Shopify's first order
- Never call audience segments missing from one campaign; check the account over 90 days and say "confirm in Ads Manager"
- Lead gen and catalog campaigns are never run through the purchase 4PI: lead gen is CPL, frequency and trend; catalog is always BOF and scales on daily frequency
- A product exclusion is never assumed: read the product set's filter and query the set for the product before calling anything excluded
- Never credit a change until delivery shows it happened; a result that fits the timing is not proof
- Decisions before detail: the Top 3 priorities come straight after the scorecard
- Promo campaigns are judged on the promo plan, never the evergreen checklist: since-launch windows, a promo target from the offer's margin, daily PUSH / PACE / PULL BACK, and kill / add rules with the triggering number on every line

## Key References

- `references/4pi-knowledge-base.md` — the complete framework (read first, every time)
- `references/mcp-data-pull.md` — exact Meta MCP pull sequence and window math
- `references/post-click-audit.md` — Firecrawl landing-page mismatch workflow
- `references/report-memory.md` — week-over-week continuity, history schema, accountability card
- `references/campaign-types.md` — lead gen and catalog analysis (detection, metrics, verdicts, product cuts, report layouts)
- **Catalog Product Checks** (this file) — product set read, exclusion test, weekly product breakdown, change verification, marginal cut maths, tripwires, overlap, budget step history
- **Promo Mode** (this file) — sale, BOGO, BFCM and launch campaigns: plan, promo economics, daily budget calls, kill / keep / add, incrementality, debrief
- `references/hook-generator.md` — Andromeda-diverse hook generation for creative tests
- `references/html-report.md` — branded HTML report template and section spec
- `clients/README.md` — client brand config format and onboarding