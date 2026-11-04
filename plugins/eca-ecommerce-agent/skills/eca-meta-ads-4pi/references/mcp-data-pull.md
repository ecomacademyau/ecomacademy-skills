# Meta Ads MCP — Data Pull Guide (Official Meta Ads MCP)

This skill uses the **official Meta Ads MCP** (tools named `ads_*`, e.g. `ads_get_ad_accounts`, `ads_get_ad_entities`). Do NOT use third-party Meta connectors (`meta_get_*`) unless the official one is unavailable.

## Pull Sequence

### 1. Find the account

`ads_get_ad_accounts` → returns `ad_account_id`, `ad_account_name`, `currency`, `is_ads_mcp_enabled`, `is_queryable`.

- If `is_ads_mcp_enabled` is false, tell the user that account isn't enabled for Ads MCP yet and offer the CSV fallback.
- If multiple accounts match the brand loosely, confirm with the user before pulling.
- Note the account `currency` — use it for every money figure in the report.

### 2. Field verification (once per session)

Before the first `ads_get_ad_entities` call, verify any field you're unsure about with `ads_get_field_context`. The verified field names as of the last update of this skill:

| Concept | Field name | Levels | Notes |
|---|---|---|---|
| Spend | `amount_spent` | all | alias `spend` |
| Impressions | `impressions` | all | |
| Reach | `reach` | all | |
| CPM | `cpm` | all | |
| Frequency | `frequency` | all | avg per Meta Account over the window |
| Cost per 1K reached | `cpp` | all | validates CPM × frequency signal |
| Purchases | `actions:omni_purchase` | all | THE purchase count field |
| Results / CPA | `results`, `cost_per_result` | all | objective-based; for sales campaigns ≈ purchases / cost per purchase |
| ROAS | `purchase_roas` | all | Revenue = purchase_roas × amount_spent |
| Link clicks | `actions:link_click`, `cost_per_link_click` | all | outbound-intent proxy |
| Clicks (all) | `clicks`, `cpc`, `ctr` | all | includes reactions etc — use link_click for intent |
| Leads | `lead` | all | for lead-gen accounts |
| 3-sec video plays | `3_second_video_plays` | account/campaign/**adset only** | NOT available at ad level |
| 2-sec continuous plays | `video_continuous_2_sec_watched_actions` | all incl. ad | ad-level hook proxy |
| ThruPlays | `video_thruplay_watched_actions` | all incl. ad | |
| Video 25/50/75/95/100% | `video_p25_watched_actions` etc | all incl. ad | drop-off curve |
| Status (configured) | `status` | c/as/ad | ACTIVE, PAUSED, DELETED, ARCHIVED |
| Status (actual) | `effective_status`, `delivery` | c/as/ad | delivery: active/inactive/off/completed/error |
| Learning phase | `delivery_sub_status` | adset only | LEARNING, FAIL (= Learning Limited) |
| Attribution | `attribution_setting` | adset | e.g. 7d_click, 1d_view_7d_click |
| Budget | `daily_budget`, `lifetime_budget` | campaign/adset | |
| Objective | `objective` | campaign/ad | |
| Hierarchy | `campaign_id`, `adset_id`, `creative_id` | ad | creative_id → `ads_get_creatives` |
| Timing | `created_time`, `start_time`, `updated_time` | | for minimum-data threshold |

There is **no GPT, AOV, add-to-cart, outbound CTR, or hook-rate field** in the API catalog. Derive:

- `Revenue = purchase_roas × amount_spent`
- `AOV = Revenue / purchases`
- `Profit per Order (pre-COGS proxy) = AOV − CPA`
- `Link CTR = actions:link_click / impressions × 100` (label "link click CTR", not outbound CTR)
- `Hook rate (ad-level proxy) = video_continuous_2_sec_watched_actions / impressions × 100` — label as "2-sec hook rate"; the classic 3-sec hook rate is only available at ad-set level
- `Hold rate (proxy) = video_thruplay_watched_actions / video_continuous_2_sec_watched_actions × 100`
- `Purchases per link click = purchases / actions:link_click` — the post-click conversion proxy for Step 6

### 3. Core pulls

Standard ad-level field set (add `lead` for lead-gen accounts):

```
fields: ["id","name","campaign_id","adset_id","creative_id","effective_status",
         "amount_spent","impressions","reach","cpm","frequency","cpp",
         "actions:omni_purchase","results","cost_per_result","purchase_roas",
         "actions:link_click","cpc","ctr",
         "video_continuous_2_sec_watched_actions","video_thruplay_watched_actions",
         "created_time"]
```

Make these calls (each is one `ads_get_ad_entities` call):

1. **7d window**: level `ad`, `date_preset: "last_7d"`, fields above
2. **30d window**: level `ad`, `date_preset: "last_30d"`, fields above
3. **MTD window**: level `ad`, `time_range: '{"since":"<1st of month>","until":"<today>"}'`
4. **Daily frequency read**: level `ad`, `date_preset: "last_7d"`, `time_increment: "1"`, fields `["id","name","amount_spent","frequency","cpm","impressions"]` — this gives per-day rows. Use the **average of the daily frequency values** for the funnel decoder (the 7d/30d aggregate frequency is the trend line, not the decoder input). It also gives the last-5-days spend trajectory and CPM trend.
4b. **Campaign-level daily read**: level `campaign`, `date_preset: "last_7d"`, `time_increment: "1"`, fields `["id","amount_spent","impressions","reach","frequency","cpm","actions:omni_purchase","purchase_roas"]` (plus the lead field for lead campaigns). Gives campaign daily frequency and CPM for the both-rising danger signal, the catalog frequency band and the lead verdict. Ad frequencies can't be averaged into a campaign figure, because reach overlaps between ads. For a mixed purchase/catalog campaign, pull the catalog ad sets at level `adset` instead.
5. **Structure pulls**: level `campaign` (fields: id, name, objective, daily_budget, lifetime_budget, status, effective_status, amount_spent for 30d) and level `adset` (fields: id, name, campaign_id, daily_budget, optimization_goal, delivery_sub_status, attribution_setting, effective_status, created_time; `created_time` lets the next run verify a catalog duplicate).
6. **Audience segment pulls (every sales campaign, every run, Quick and Full)**: `breakdowns: ["user_segment_key"]` at campaign level for 30d and 7d, plus a clean baseline window when a promo overlaps. This is the new vs engaged vs existing split behind NCPA, the setup check and the repeat-purchase-bias check. Full spec in §3b. Only ONE breakdown per call.
7. **Delivered-market pull**: level `campaign`, `date_preset: "last_30d"`, `breakdowns: ["country"]`, fields `["id","name","amount_spent","impressions"]`. The market = the country carrying the majority of spend. There is no geo/targeting attribute in the field catalog, so this breakdown is the only way to know which market a campaign actually reaches — and **delivery beats the campaign name**. Required before any post-click audit (Step 6) and before any market/currency claim in the report.
8. **Year-over-year seasonality pulls** (account level, two calls): level `ad_account`, custom `time_range` = this report's 30d window shifted exactly one year back (e.g. `{"since":"2025-06-13","until":"2025-07-12"}`), and the same for the MTD window. Fields: `["amount_spent","impressions","cpm","frequency","results","cost_per_result","purchase_roas"]`. Interpretation rules live in the Knowledge Base ("Year-over-Year Seasonality Check" — CPM is the signal, the rest is directional). Empty/no data → the account is younger than a year for that window; skip with one line, never fill from industry lore.

Practical notes:

- Metrics require a time range; without one you get attributes only.
- The tool caps total entities returned — for large accounts, filter by campaign (`filtering: [{field:"ad.campaign_id", operator:"IN", value:[...]}]`) and pull per campaign rather than one giant pull.
- Don't pass both `date_preset` and `time_range`.
- Sort by `amount_spent_descending` so truncation drops the least important ads first.
- If a call errors on a field, drop the offending field and retry — don't abandon the pull.

### 3b. Audience segments & NCPA pulls

**Verified live 23 Oct 2026:** `breakdowns: ["user_segment_key"]` works on manual (non-Advantage+) sales campaigns, not only Advantage+ Shopping. The earlier "ASC only" note was wrong. The split follows the ad account's **audience segment settings** (existing customers + engaged audience definitions).

Values returned (one row per segment per entity):

| `user_segment_key` | Ads Manager name | Counts as |
|---|---|---|
| `prospecting` | New audience | new customer |
| `engaged` | Engaged audience | new customer (engaged, but not matched to the existing-customer definition) |
| `existing` | Existing customers | returning customer |
| `unknown` | unmatched | neither; flag if material (> 5% of spend) |

Meta assigns each person to one segment: existing first, then engaged, then new. So `prospecting` + `engaged` purchases are buyers Meta did not match to the existing-customer definition. That is the **new-customer proxy** behind NCPA.

Fields for every segment call: `["id","name","amount_spent","impressions","reach","frequency","cpm","actions:omni_purchase","purchase_roas"]` (`omni_purchase` is the canonical name `ads_get_field_context` returns; both resolve). Filter to the sales campaigns by id.

Calls:

1. **Campaign level, `last_30d`**: NCPA headline, segment mix, setup check.
2. **Campaign level, `last_7d`**: current-week NCPA.
3. **Campaign level, clean baseline** (custom `time_range`): whenever a promo, sale or BFCM overlaps the 7d or 30d window, also pull the 8 to 12 weeks before the event started. Existing customers flood in during promos, so promo-window NCPA is never the baseline. Print both and say which one drives the call.
4. **Ad level, `last_30d`** (Full mode only), filtered per campaign, for ads that clear the data bar: each ad's new-customer share, used to cross-check the funnel decoder (Knowledge Base, "Audience Segments, NCPA & Target Modes").
5. **Account level, `last_90d`** (`level: "ad_account"`): only when the 30d pull shows no `existing` row or no `engaged` row in any campaign. One campaign that excludes past purchasers will legitimately have no `existing` row, so never conclude "not set up" from a single campaign.

Parsing:

- Rows are separate objects carrying `user_segment_key`. Same rules as §7: a purchase field that is `null` or `"Not available"` = 0 purchases; money strings parsed the same way.
- Segment spend must sum to the entity's spend (to the cent, allowing rounding). If it doesn't, say so and don't compute NCPA for that entity.
- `reach` and `frequency` are deduped within each segment for that window. Compare segments only within the same window; a 90-day segment frequency is not comparable to a 7-day one.
- Error or empty result with the breakdown: retry once without the breakdown to confirm the entity has data, then mark segments **UNAVAILABLE**. Never estimate a split.

Setup status, computed once per account per run: **OK · PARTIAL · SUSPECT · NOT SET UP · UNAVAILABLE**. Rules, thresholds and the report wording are in the Knowledge Base, "Audience Segments, NCPA & Target Modes". The API has no field that exposes the segment definitions themselves, so every setup verdict is inferred from delivery and must say "confirm in Ads Manager".

**Shopify cross-check (optional; always attempt when the client's target is per new customer):**

- Only when a Shopify connector is available AND the `domain` field from `get-shop-info` (the store's primary domain, compared without `www.`) matches the client config's `shopify_domain`, or the host of `website` when `shopify_domain` isn't set. A connector signed into a different store must never feed this report: write "Shopify connector is on <other store>; Shopify cross-check skipped".
- ShopifyQL, same windows (store timezone): `FROM sales SHOW new_customers, returning_customers TIMESERIES day SINCE <start> UNTIL <end>`. Returning share = returning ÷ (new + returning).
- Report beside Meta's NCPA: the **Meta NCPA floor** = Meta spend in the window ÷ Shopify new customers (all channels). Meta can't have acquired more new customers than the store gained in total, so Meta's true NCPA can't sit below this floor. A Meta NCPA *below* the floor means Meta claims more new-customer purchases than the store had new customers: treat Meta's NCPA as optimistic and say so. Caveat in one line: Meta counts orders, Shopify counts customers, so a new customer ordering twice in the window inflates Meta's side slightly. Use Meta spend only: other paid channels' spend isn't in this skill's data, so a "total paid" figure would be a guess.
- Shopify days run on the store timezone, Meta days on the ad account timezone. State both when they differ; don't silently mix them.

### 3c. Campaign type and type-specific pulls

Classify every campaign as purchase, lead gen, catalog or other before analysing (rules: `references/campaign-types.md` §1). The creative pull (§5) already returns `product_set_id`, which marks catalog ads; the campaign pull's `objective` and `results` indicator mark lead gen.

- **Lead gen:** add the lead field to the window and daily pulls (`lead` or `actions:leadgen.other`; the campaign's `results` indicator names the right one).
- **Catalog, when losing money or when a product-cut recommendation is open from the last report:** `breakdowns: ["product_id"]` at ad level, last 30 days, filtered to the catalog campaign; fields `amount_spent`, `impressions`, `actions:link_click`, `actions:omni_purchase`. Verified live 23 Oct 2026: rows come back as `"<product id>, <product name>"` with spend and purchases. Rows are per ad and product: sum by product id before judging. Product-level `purchase_roas` can return `0` even with a purchase, so never judge a product on it. When verifying a cut from the last report, also pull last 7 days.

### 4. Status classification

Combine `effective_status`/`delivery` with recent spend (from the daily pull):

- **ACTIVE** = delivery `active` AND spend > 0 within last 3 days
- **STOPPED** = delivery `off`/`inactive`/`completed`/paused-by-parent OR no spend in 7+ days
- **WINDING DOWN** = delivery `active` but daily spend down >50% over last 3 days

Learning status comes from the parent ad set's `delivery_sub_status`: `LEARNING` → treat metrics as unstable; `FAIL` → "Learning Limited" (not a death sentence — see Knowledge Base).

### 5. Creatives (for type detection + post-click audit)

`ads_get_creatives` with `creative_ids` (from the ad pull) — listing without IDs returns only id/name/status. Request full records to get `object_type`, `body`, `title`, `link_url`, `image_url`, `video_id`, `call_to_action_type`, `product_set_id`. A `product_set_id` marks a catalog ad (`references/campaign-types.md` §1); if creatives don't return it, fall back to a campaign objective of `PRODUCT_CATALOG_SALES`.

- Creative type: `video_id` present → video; else image/carousel via `object_type`/`child_attachments`. Fall back to name heuristics ("UGC", "video", "static", "image") if ambiguous.
- `link_url` (or the link inside `object_story_spec`) is the landing page for the post-click audit.

### 6. Optional enrichment (use, don't lead with)

- `ads_insights_anomaly_signal` — account-level anomaly flags; mention in report as "Meta-flagged anomalies", never as a substitute for 4PI reads
- `ads_get_opportunity_score` — note score + top recommendations in the account summary
- `ads_insights_performance_trend` — corroborates CPM/frequency trend reads

### 6b. Industry benchmark (optional, one call per report)

`ads_insights_industry_benchmark(ad_account_id, date_preset: "LAST_28D")` — compares performance against aggregated peers ("similar advertisers"). Note this tool's date presets are UPPERCASE (`LAST_7D`, `LAST_28D`…), unlike `ads_get_ad_entities`.

- Prefer `LAST_28D` (peer aggregates need volume; 7d often comes back empty).
- Per the tool's own guidance: lead with **business outcome metrics** (cost per result) over surface metrics (CPM), and only compare like-for-like optimization goals.
- **Small accounts frequently get `"No industry benchmark data available"`** (verified live) — that is a normal outcome. Skip silently or write one line ("peer benchmark: not available for this account size"); never estimate industry figures from general knowledge to fill the gap.
- When data exists: one line in the account scorecard ("Cost/result vs similar advertisers: X% better/worse") and optionally per-campaign. Context, never the headline — 4PI verdicts do not change because of a benchmark.

### 6c. Industry benchmark fallback — Triple Whale (Firecrawl)

When Meta's peer benchmark returns no data (usual for smaller accounts), scrape Triple Whale's public benchmark for the brand's vertical:

`firecrawl_scrape("https://benchmark.triplewhalelabs.com/benchmarks/<industry_slug>/", formats: ["markdown"], maxAge: 0, waitFor: 6000)`

- **Slug** from the client config's `industry_vertical` (lowercase, underscores: `apparel_and_accessories`, `health_and_beauty`, `food_and_beverage`, `sports_and_outdoors`, `pets_and_animals`, `baby`, `consumer_electronics`, `home_and_garden`, …). Full industry list on https://benchmark.triplewhalelabs.com/benchmarks/ — if the vertical isn't in the config, ask once during onboarding and save it.
- **What you get free (verified live):** Meta-channel **ROAS, CPA, CPM** as p25 / median / p75 for the industry cohort. Everything else (CTR, CVR, AOV, ATC…) is paywalled ("Unlock Insights") — skip those, never infer them.
- **Render as the Industry Benchmark card** (html-report.md §3d): percentile band graphic + per-campaign 30d ROAS table with quarter pills + ACCOUNT row + "Why ROAS only" bullets + "context, not a verdict" close.
- **Currency rule (why ROAS only):** the cohort figures are **USD**. If the account currency is anything else, CPM and CPA are not comparable and must not be converted — **ROAS is a ratio, so it carries no currency; it's the one clean comparison**. Only when the account is USD may CPM/CPA join the card (the AOV-blend caveat still applies).
- **Anonymise the source in the report.** The provider's name never appears in any client-facing output — the card says "other <vertical> brands running Meta" / "the cohort". This reference file keeps the URL because the skill needs it to fetch; that's the only place it lives.
- **Caveats that stay in the card:** cohort blends every revenue and AOV band (the page's filters are client-side UI, not URL-addressable — you always get the default cohort); cohort attribution ≠ Meta attribution; directional context, never the headline — a healthy ROAS percentile changes nothing about a drying funnel.
- Scrape fails or vertical missing → skip with one line, same as the Meta benchmark.

Order of preference: Meta peer benchmark (like-for-like optimization goals) → industry cohort card → nothing (say so). Never both as if independent — pick the best available.

### 7. Response parsing (verified against live pulls)

The tool returns **formatted strings, not numbers**. Parse carefully:

- Money: `"AU$2,100.76 AUD"` → strip currency symbols/spaces, parse float
- Counts: `"21,641"` → strip commas
- Percentages: `"1.35%"` → CTR comes pre-multiplied
- `results` and `cost_per_result` are objects: `{"value": "14 (Website purchases)"}` — extract the number AND note the result type in parentheses (confirms what "result" means for that campaign)
- `"Not available"` appears for any metric with no data. For purchases, `results: "0 (...)"` alongside `actions:omni_purchase: "Not available"` means **zero purchases**, and `cost_per_result: "AU$0.00"` with 0 results means **no CPA**, not a $0 CPA
- `effective_status: "ADSET_PAUSED"` / `"CAMPAIGN_PAUSED"` = stopped via parent — treat as STOPPED
- `delivery_sub_status` may return "Not available" — learning status is best-effort; proceed without it rather than flagging it
- Date presets exclude today (`date_stop` = yesterday); custom `time_range` can include today. State the actual "as of" date in the report
- Contrary to the field catalog, **`3_second_video_plays` DOES populate at ad level** in practice — prefer it for hook rate (`3s plays / impressions`); `video_continuous_2_sec_watched_actions` often returns "Not available". Use whichever populates
- The daily (`time_increment: "1"`) pull only returns days with delivery, and pages by ad×day rows — filter to one campaign per call to stay under the row cap

### 8. Data freshness — never reuse stale pulls

Before building any report, check today's actual date (run `date` via bash if in doubt) against the `date_stop` returned by the pulls. The report's "as of" date must be **yesterday or today**. If the pulls in context are from an earlier day — long sessions, re-runs, "redo the analysis" requests — **re-pull everything fresh**. Reusing cached pulls from a previous day produces a report with wrong windows and stale numbers, which is worse than no report. A re-run request always means fresh data, never a re-render.

### 9. Error handling

- Token/auth errors (code 190 or "expired") → stop, tell the user to reconnect the Meta connector in settings. Never fabricate or reuse stale numbers.
- `is_queryable: false` → surface `not_queryable_reason`.
- Empty windows → report "no data in window", don't fill gaps.
