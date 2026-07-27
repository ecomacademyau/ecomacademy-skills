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
5. **Structure pulls**: level `campaign` (fields: id, name, objective, daily_budget, lifetime_budget, status, effective_status, amount_spent for 30d) and level `adset` (fields: id, name, campaign_id, daily_budget, optimization_goal, delivery_sub_status, attribution_setting, effective_status).
6. **Audience segment check (ASC campaigns only)**: for Advantage+ Shopping campaigns, re-pull key ads with `breakdowns: ["user_segment_key"]` to split new vs existing customers — this is the repeat-purchase-bias check. Only ONE breakdown per call. If the result comes back empty, retry without the breakdown and note "segment data unavailable".
7. **Delivered-market pull**: level `campaign`, `date_preset: "last_30d"`, `breakdowns: ["country"]`, fields `["id","name","amount_spent","impressions"]`. The market = the country carrying the majority of spend. There is no geo/targeting attribute in the field catalog, so this breakdown is the only way to know which market a campaign actually reaches — and **delivery beats the campaign name**. Required before any post-click audit (Step 6) and before any market/currency claim in the report.

Practical notes:

- Metrics require a time range; without one you get attributes only.
- The tool caps total entities returned — for large accounts, filter by campaign (`filtering: [{field:"ad.campaign_id", operator:"IN", value:[...]}]`) and pull per campaign rather than one giant pull.
- Don't pass both `date_preset` and `time_range`.
- Sort by `amount_spent_descending` so truncation drops the least important ads first.
- If a call errors on a field, drop the offending field and retry — don't abandon the pull.

### 4. Status classification

Combine `effective_status`/`delivery` with recent spend (from the daily pull):

- **ACTIVE** = delivery `active` AND spend > 0 within last 3 days
- **STOPPED** = delivery `off`/`inactive`/`completed`/paused-by-parent OR no spend in 7+ days
- **WINDING DOWN** = delivery `active` but daily spend down >50% over last 3 days

Learning status comes from the parent ad set's `delivery_sub_status`: `LEARNING` → treat metrics as unstable; `FAIL` → "Learning Limited" (not a death sentence — see Knowledge Base).

### 5. Creatives (for type detection + post-click audit)

`ads_get_creatives` with `creative_ids` (from the ad pull) — listing without IDs returns only id/name/status. Request full records to get `object_type`, `body`, `title`, `link_url`, `image_url`, `video_id`, `call_to_action_type`.

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
