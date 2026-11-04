# Facebook Ads 4PI Analysis — Knowledge Base

Contents: Core philosophy · Misleading metrics · The 4PI framework · Funnel decoder · Golden rule · Campaign isolation · Campaign types (lead gen, catalog) · Ad status · Minimum data · Time windows · Audience segments, NCPA & target modes · Attribution · Profitability (Profit per Order / GPT) · AOV · Creative diagnostics · Creative type & CPM · Format funnel tendencies · Ad Concept Board · Learning status · Macro calendar · 3 testing paths · CSV fallback processing · Tone & decision rules · Action labels

---

## The Core Philosophy

Facebook is a **meritocracy**. Delivery is earned. Facebook's business model is to show people content they want to see. If your ad earns spend, Facebook believes in it. If it doesn't, no creative director's opinion matters — the market has voted.

Traditional metrics borrowed from email, search, and display — CTR, ROAS, conversion rate — are invalid inside Facebook as decision metrics. The only question that matters: **how is Facebook using this ad, and is it doing that job well?** Four metrics answer it completely.

## Why Common Metrics Mislead

- **CTR** is a ratio. Easiest way to a high CTR: show the ad to a small, targeted group. Lower CPM → larger denominator → lower CTR even if more people clicked. TOF CTR is always worse than retargeting CTR; comparing them is meaningless.
- **ROAS**: both numbers are wrong. Today's revenue was caused by spend from yesterday/last week/last month — numerator and denominator aren't correlated. Attribution windows make the revenue number itself off. Chasing ROAS dries up funnels: retargeting-heavy accounts look great on ROAS right up until revenue collapses. Directional use only.
- **Conversion rate** varies entirely by funnel position. A BOF ad always converts better; that's position, not quality. An ad with terrible CVR might be filling the whole funnel.
- **Hook rate** is a diagnostic (why an ad sits where it does), never a performance indicator.

## The 4PI Framework

### PI 1 — Spend: what is Facebook choosing to spend on this ad?

Low spend on a live ad = Facebook doesn't believe it earns more. Compare spend as % of the **campaign's** spend. Track the trend over the last 5–7 days (daily pull). A TOF prospecting ad will always out-spend a retargeting ad — correct and expected; it feeds the funnel the retargeting ad lives on.

### PI 2 — CPM: how expensive is it to show, relative to peers in the same campaign?

CPM is never good or bad in isolation — only relative to other ads in the same campaign. Low relative CPM = broad engagement, TOF signal. High relative CPM = narrow audience, retargeting, or people don't want the ad. CPM rising with flat/declining spend = the funnel is drying up. Context adjustments: image inventory is cheaper than video inventory; retargeting audiences cost more than prospecting — neither is a performance signal by itself.

### PI 3 — Frequency (daily): where in the funnel is Facebook placing it?

Use **day-level frequency** (from the `time_increment: "1"` pull — average the daily values), not the window aggregate; the aggregate is the trend line. Frequency is relative to spend — if spend doubled, frequency rises even with a stable audience.

**Funnel decoder (daily frequency):**

| Daily frequency | Position | Meaning |
|---|---|---|
| < 1.15 | TOF | Prospecting. Fills the funnel. |
| 1.15–1.40 | MOF | Mixed; retargeting beginning alongside prospecting. |
| > 1.40 | BOF | Heavy retargeting; 40%+ seeing it more than once/day. |
| > 2.0 | Saturation risk | Over-serving the same users. Needs new prospecting creative or audience expansion. |

Cross-check CPM and frequency — they should agree. Low CPM + low freq = confirmed TOF. High CPM + high freq = confirmed BOF. Disagreement → investigate (also check `cpp` vs `cpm`: cpp much higher than cpm confirms repeat-hitting).

**One computation, one label.** The headline daily frequency and its trend must come from the *same* series — the per-day values in the `time_increment: "1"` pull. Headline = mean of those dailies. Trend = mean of the first 3 dailies → mean of the last 3. Never mix in a window-aggregate frequency (a 7-day aggregate dedupes reach over 7 days and is a different, larger number — mixing the two produces a headline sitting outside its own trend range, which reads as a bug and undermines every other number on the page).

Direction label derives from those same two endpoints, with an explicit flat band: **rising** if last is >2% above first · **falling** if >2% below · **flat** otherwise. A label that contradicts the numbers printed beside it (e.g. "rising (1.42 → 1.42)") is a correctness failure, not a cosmetic one — frequency direction feeds the CPM-and-frequency-both-rising danger signal. Apply the identical rule to CPM trends.

### PI 4 — Efficiency: CPA, Profit per Order, AOV

- CPA (`cost_per_result`) compared only within the same campaign and against the target CPA.
- TOF ads are expected to have worse CPA — they fill the funnel. Don't kill TOF on CPA alone.
- BOF ads must have the lowest CPA in the campaign. A BOF ad with bad CPA gets the most intent-ready audience and still fails — the ad is bad. High CPA + low spend + BOF position = Facebook already knows; confirm and Stop.
- **Profit per Order** (see Profitability section) overrides CPA for scaling/budget decisions.
- **AOV** sets CPA tolerance: $50 CPA on $120 AOV is viable; on $60 AOV it likely isn't.

## Full Funnel Decoder (CPM × Frequency)

| CPM (in campaign) | Daily freq | Verdict |
|---|---|---|
| Lowest | < 1.15 | Strong TOF. Keep and feed it. |
| Lowest | 1.15–1.40 | MOF but efficient. Good complement. |
| Median | < 1.15 | TOF, less loved. Watch. |
| Median | > 1.40 | BOF. Evaluate CPA carefully. |
| Highest | > 1.40 | Confirmed BOF retargeting. Must justify CPA. |
| Highest | < 1.15 | Audience doesn't like it — broad reach at punishing cost. |
| Rising | Rising | **Danger.** Funnel drying up. Urgent new TOF creative. |
| Any | > 2.0 | **Saturation.** New prospecting creative or audience expansion. |

## The Golden Rule

> Lower CPM + lower frequency = more opportunity, more reach, funnel growing.
> Higher CPM + higher frequency = efficiency on paper, funnel dying.

A campaign that looks increasingly efficient (better CPA/ROAS) while CPM and frequency both rise is a campaign in decline. Revenue follows. **The cost-caps trap:** cost caps and Advantage+ Shopping deliberately drive higher CPM + frequency to look efficient — this is the mechanism that makes businesses look profitable right up until they close.

## Campaign-Level Isolation

All 4PI analysis is campaign-scoped. Never mix ads across campaigns: CPM comparisons, spend %, funnel gaps — all per campaign. Funnel-gap verdicts apply to purchase campaigns only; catalog ads never count as TOF. Different objectives, products, audiences make cross-campaign CPM comparison meaningless. Group by campaign first, run 4PI in each independently, map each funnel, diagnose each gap; summarise across campaigns only in the account-level summary.

## Campaign Types: Lead Gen and Catalog

Lead gen and catalog campaigns get their own analysis in `references/campaign-types.md`: their own metrics, data bar, labels, scaling verdict and report section. Never run them through the purchase 4PI table, the funnel map or an NCPA judgement. In short: lead gen is judged on cost per lead, daily frequency and the CPL trend; catalog is treated as bottom of funnel and is judged per order (CPA, profit/order) with daily frequency deciding whether it can scale (< 1.50 room to scale · 1.50 to < 1.80 healthy · 1.80 to < 2.00 hold · ≥ 2.00 saturated); link CTR and ROAS are context. Catalog ads never count as TOF, and the existing-customer rules below don't apply to catalog campaigns.

## Ad Status Detection

Classify before recommending anything (rules in mcp-data-pull.md §4). Framing:

| Status | What to say |
|---|---|
| ACTIVE | Keep/Hold/Fix/Watch/Stop/Scalable with number justification |
| STOPPED | "Already stopped — before reactivating, fix X" or "Stopped correctly — reactivate when [condition]" |
| WINDING DOWN | "Spend declining — watch 3 days. Below $X, treat as stopped." |
| Inactive 2+ weeks | "Historical data only. Conditions may have changed." |

Never tell someone to stop an ad that's already stopped. Never call an ad Scalable that stopped weeks ago.

## Minimum Data Requirements

Evaluate an ad only if BOTH: running ≥ **7 days of delivery** AND spend ≥ **2× target CPA** (from client config or the user — never invented). If no target CPA exists, use 2× the campaign's blended CPA purely as the data-sufficiency bar and label it as such — do NOT present it as a performance target anywhere in the report; instead state "no target CPA set" and judge CPA relative to campaign peers and profitability only. Below threshold → label **Insufficient data**, state the threshold, assign no other label. Early metrics are volatile; killing ads too early is the most common small-budget mistake.

## Small-Sample Rule (which window drives the action label)

Action labels are based on the **last 7 days** — except when the 7-day window is too thin to carry a verdict. An ad's 7-day figures are **statistically thin** when purchases ≤ 2 or spend < 2× target CPA in that window, even if its 30-day record clears the data bar.

For those ads: base the action label on the **30-day** CPA and profit, print the 7-day number too, and say why in one line — e.g. *"judged on 30d: the 7d GP/order of $56.83 comes from a single $99.90 order."* Never silently switch windows; the reader must see which window drove the call. Ads with healthy 7-day volume are always judged on 7 days, with 30d as trend context.

Why: one lucky (or unlucky) high-AOV order can swing a 1–2 purchase week by hundreds of percent. Acting on that noise is the same error as acting below the data-sufficiency bar, just one level up.

## Time Window Analysis

| Window | Role |
|---|---|
| Last 7 days | Primary. All action labels based on this. |
| Month to date | Pacing vs monthly budget/targets. |
| Last 30 days | Trend confirmation. |

Date math: MCP presets handle 7d/30d; MTD = custom range from the 1st. (CSV fallback: 7 days inclusive = report_date − 6 days; 30 days = −29. Off-by-one here corrupts every number.)

Usage: strong 7d but deteriorating 30d → flag as possible blip. Weak 7d but strong 30d → possible early fatigue, not permanently broken. Shifts in spend share/CPM/frequency between windows = Facebook changing how it uses the ad. A $20 CPA that was $35 over 30d is improving; the same $20 that was $15 is deteriorating — different actions for identical 7d numbers.

## Audience Segments, NCPA & Target Modes

Meta's `user_segment_key` breakdown works on every sales campaign, not just Advantage+ Shopping (pulls in mcp-data-pull.md §3b; CSV path: the Audience Segments column). It splits each campaign into **new (`prospecting`) · engaged · existing · unknown**, following the ad account's audience segment settings, and answers the question blended CPA can't: **what does it cost to win a customer who has never bought?**

### Formulas

| Metric | Formula | Use |
|---|---|---|
| **New-customer purchases** | `prospecting` + `engaged` purchases | the proxy count (engaged = engaged but not matched as an existing customer) |
| **NCPA** (headline) | all campaign spend ÷ new-customer purchases | acquisition cost loaded with what the campaign spent on existing customers. Targets are judged against this one. |
| New-segment CPA | (`prospecting` + `engaged` spend) ÷ new-customer purchases | secondary: cost inside the new segments only |
| Existing CPA | `existing` spend ÷ `existing` purchases | what re-buying customers cost |
| Existing share | `existing` spend ÷ spend, and `existing` purchases ÷ purchases | repeat-purchase bias and over-serving |
| **Account NCPA** | Σ purchase-campaign spend ÷ Σ their new-customer purchases | the account headline, judged against `target_ncpa`. Catalog campaigns are excluded from the judged number (they retarget, `references/campaign-types.md`). When catalog, lead or other campaigns are ≥ 5% of spend, also show a **fully loaded** variant including all spend, labelled as such |

Why the loaded version leads: spend on existing customers is part of what the campaign costs to run. Dividing only new-segment spend by new purchases flatters the number.

The Small-Sample Rule applies: NCPA on fewer than ~10 new-customer purchases is noise. Judge on the 30-day or longer baseline figure and say which window drove the call.

### Target modes

A client's target is either per order or per new customer. Never mix the two.

| Mode | Config | What gets judged |
|---|---|---|
| `first_order` | `target_cpa` | blended CPA vs `target_cpa` (pre-v2.4 behaviour) |
| `ltv` | `target_ncpa` (a `target_cpa` may be stored for context) | **NCPA vs `target_ncpa`** in scaling verdicts and sentiment. Blended CPA is shown, never judged against the LTV number, and a stored `target_cpa` is display-only, except for catalog campaigns, which are always judged per order (`references/campaign-types.md` §3) |
| `both` | both | NCPA vs `target_ncpa` drives sentiment; scaling verdicts need **both** to pass (NCPA vs `target_ncpa` and blended CPA vs `target_cpa` each get a checklist line) |

**The LTV trap:** an LTV target only buys room on *new* customers. Judging blended CPA against an LTV number green-lights paying LTV prices for returning customers who would have bought from an email anyway. In `ltv` mode the KPI is NCPA.

If the mode is `ltv` or `both` but segments are **NOT SET UP** or **UNAVAILABLE**, NCPA can't be computed. Say so in the header and fall back to `target_cpa` if one exists (else judge on profit only, as with no target). NOT SET UP also makes "set up audience segments" a top-3 priority; UNAVAILABLE is an API gap, so the report just says "segment data unavailable this run, re-check next run".

**Minimum-data bar in `ltv` mode:** with no `target_cpa`, use 2× the campaign's blended CPA, labelled as a data bar. Never 2× target NCPA: that sets an ad-level bar far too high.

**Ad labels by mode** (identical in Quick and Full): `first_order` and `both` judge an ad's 7-day CPA against `target_cpa`; `ltv` judges it against campaign peers and profit/order, as with no target. Exceptions: catalog ads are judged per order in every mode, and lead ads on CPL (`references/campaign-types.md`). NCPA is a campaign-level and account-level number. The Full-mode ad-level segment pull (30d) adds each ad's new-customer share as context and for the funnel-decoder cross-check; it never changes an action label.

### Setup status (once per account, every run)

Evaluate in this order; **the first match sets the status** and any other matching signals are listed as flags under it: **UNAVAILABLE → NOT SET UP → SUSPECT → PARTIAL → OK**. Reach and frequency comparisons use the **30-day campaign pull of the largest purchase campaign by 30d spend** (never a catalog campaign: catalogs are mostly existing customers by design) (reach is deduped within a campaign, never summed across campaigns). Presence checks (`existing`/`engaged` rows) use the account-level 90-day pull whenever any sales campaign lacks a row.

| Status | Evidence | What the report says / the fix |
|---|---|---|
| **OK** | `existing` and `engaged` rows present in the account, `unknown` < 5% of spend, no SUSPECT signal | One line: "Audience segments set up" plus the mix |
| **PARTIAL** | at account level over 90 days, `existing` present but never `engaged`, or `engaged` present but never `existing` | "Engaged audience (or existing customers) isn't defined, so new-customer counts are approximate." Fix: define the missing segment in the ad account's audience segment settings |
| **SUSPECT** | set up, but any of: existing reach < 5% of the campaign's reach **and** existing frequency > 5× new frequency (a small matched pool being hit over and over) · `unknown` between 5% and 50% of spend · with the Shopify cross-check run on the same 30 days, Shopify returning share ≥ 40% while Meta's existing purchase share < 10% | "The existing-customer definition looks small or stale: returning buyers are probably landing in 'new', so NCPA is understated." Fix: check which customer list or purchase events define existing customers; sync the full customer list (Shopify or Klaviyo) and keep it refreshing |
| **NOT SET UP** | no `existing` and no `engaged` row at account level over 90 days (everything `prospecting`/`unknown`), or ≥ 50% of spend `unknown` | "Meta can't tell new from returning customers in this account, so there's no NCPA." Fix: define existing customers (synced customer list plus purchasers) and an engaged audience (site visitors, Facebook/Instagram engagers). Top-3 priority whenever the target mode is `ltv` or `both` |
| **UNAVAILABLE** | the breakdown errors or returns nothing while the campaign has data | "Segment data unavailable this run." Never estimate a split |

The API doesn't expose the segment definitions, so every non-OK status is inferred from delivery: the report says "confirm in Ads Manager" and never claims certainty. Setup status is structural. It goes in the header **Watch line** and never sets the sentiment badge, except that NOT SET UP or UNAVAILABLE in `ltv` or `both` mode removes the NCPA target test (see Target modes).

### Meta "new" is not Shopify "new"

`prospecting` means "not matched to the existing-customer definition", not "first order ever". Customer-list matching is never complete, so some "new" purchases are returning customers and Meta's NCPA is **optimistic**: treat it as a floor. When the Shopify cross-check runs (mcp-data-pull.md §3b), print the **Meta NCPA floor** (Meta spend ÷ all Shopify new customers) beside it. Meta's NCPA below that floor means Meta claims more new-customer purchases than the store gained new customers from every channel combined: over-claiming, with the caveat that Meta counts orders and Shopify counts customers.

### Delivery flags from the segment split

- **Existing over-serving** (Watch flag; feeds next steps; purchase campaigns only, never catalog): existing frequency ≥ 3× new frequency in the same window AND existing ≥ 15% of campaign spend. Meta is recycling customers it can re-hit cheaply instead of finding new ones; for a brand with strong email and retention this is the least incremental money in the account. Recommend a 2-week test: exclude existing customers from the campaign (or cap their share where Meta's existing-customer budget cap is available), judged on **NCPA**, not blended CPA (blended CPA usually rises because existing customers convert well). Add the account-owner escalation note if Meta is the brand's main retention channel.
- **Promo windows:** existing share jumps during sales because returning customers buy clearance. Report it, don't treat it as a problem, and never use promo-window NCPA as the baseline: the pre-event window drives the call.
- **Funnel-decoder cross-check** (ad level, Full mode): a TOF ad (daily frequency < 1.15) should take roughly 70%+ of its purchases from new + engaged. A "TOF" ad whose purchases are mostly existing customers is a decoder disagreement: investigate before calling it a prospecting workhorse. A BOF ad buying mostly existing customers is doing its job.
- **Repeat purchase bias** (purchase campaigns only; catalog buyers are expected to be mostly existing): if existing > 50% of a campaign's purchases, CPA and ROAS look strong but most of those conversions were going to happen anyway. An ad that looks Scalable but converts mostly existing customers won't scale: the pool is too small. Truly scalable ads prove themselves on new-customer purchases; never label an ad Scalable on existing-customer volume.

**Worked example** (example brand, BAU campaign, 12 weeks before a sale): spend $6,335.89; new 128 + engaged 6 = 134 new-customer purchases, so NCPA $47.28 against a $65 LTV target (inside) while blended CPA was $38.17. Existing customers took 17% of spend at frequency 45 against 3.7 for new. On the 30-day check the same campaign showed existing reach at 3.7% of campaign reach and existing frequency 7× new (20.1 vs 2.86): over-serving flag plus a SUSPECT list. During the sale itself existing customers rose to 35% of purchases: a promo window, not the baseline.

## Attribution Interpretation

Most accounts run 7-day click / 1-day view (`attribution_setting` on the ad set). 1-day-view purchases = saw ad, didn't click, bought within 24h — often existing customers, brand-search traffic, or other channels' conversions that Meta claims credit for.

**Detection without an attribution breakdown:** an ad with very low link CTR (or high CPC) but disproportionately high purchases → likely 1DV inflation. Investigate when purchases are high relative to clicks. Healthy benchmark: 7DC 60–80%, 1DV 20–40%. If 1DV dominates, the ad captures existing demand rather than creating it — affects scaling potential.

## Profitability — Profit per Order (and GPT when available)

**MCP path (default):** the API has no gross-profit field. Use the proxy:

> **Profit per Order = AOV − CPA** where AOV = (purchase_roas × spend) / purchases, CPA = cost_per_result

This is **pre-COGS** — it's revenue per order minus acquisition cost, not true gross profit. Always label it "Profit/Order (pre-COGS)" in reports. If the client config includes a gross-margin %, upgrade it: `Profit per Order = AOV × margin − CPA` and label "est. gross profit/order".

**CSV path:** if a GPT column exists, read it directly (never recalculate) and it **overrides** the proxy. Aggregate GPT as a purchase-weighted average: `sum(GPT × purchases) / sum(purchases)`.

**Decision matrix** (applies to whichever profitability figure you have):

| Scenario | Meaning | Action |
|---|---|---|
| Good CPA + positive profit | Efficient AND profitable | Keep or Scalable |
| Good CPA + negative profit | **Trap** — cheap sales that lose money | Fix or Stop. Flag immediately. |
| High CPA + positive profit | AOV absorbs the cost | Hold, monitor |
| High CPA + negative profit | Expensive and unprofitable | Stop |
| No purchases | Nothing to read | Judge on 4PI position and funnel role |

Profitability overrides CPA for budget decisions. Never label an ad Scalable with negative profit/order, even on a great CPA. TOF ads may run low/negative profit while filling the funnel — don't penalise unless they've run long enough for downstream conversions to have materialised. BOF ads must be profitable; a BOF ad losing money on the most intent-ready audience means the ad or the offer is broken. Read profitability per window (7d/MTD/30d) — profitable over 30d but not the last 7 signals deterioration.

## AOV

AOV sets CPA tolerance. Compare AOV across ads within a campaign — an ad drawing higher-value buyers can justify a worse CPA. Track the trend: declining AOV = the ad is attracting cheaper customers as it fatigues or slides down-funnel to discount-seekers. AOV dropping AND profit dropping = worse customers over time; flag it.

## Creative Diagnostics (Secondary Layer — after 4PI)

Diagnostics explain *why* an ad sits where it does and *what to fix* — never whether it's good. Skip unavailable metrics with "data not available"; don't guess.

| Metric | Source (MCP) | Poor | Average | Strong |
|---|---|---|---|---|
| Hook rate (2-sec proxy at ad level) | `video_continuous_2_sec_watched_actions / impressions` | <20% | 20–30% | >30% (>40% excellent) |
| Hold rate | `thruplays / 2-sec plays` (proxy) | <15% | 15–25% | >25% |
| Link CTR | `actions:link_click / impressions` | <0.5% | 0.5–1% | >1% (>2% excellent) |
| Purchases per link click | `purchases / link clicks` | vs campaign peers | | |

(CSV path: Thumb Stop Ratio × 100 = hook rate; Hold Rate and Outbound CTR populate at ad level only — empty at segment level is normal, aggregate to ad level, don't flag as missing. Image ads showing 0 video metrics is expected.)

**Drop-off waterfall:**

```
Low hook            → fix the first 2 seconds (new hook, opening frame, pattern interrupt)
Good hook, low hold → fix the video body/pacing
Good hook+hold, low link CTR → fix the CTA or offer framing
Good link CTR, low purchase rate → LANDING PAGE problem → run the post-click audit (Firecrawl)
                                   Not a creative fix. Don't kill the creative.
```

## Creative Type & CPM Context

Image ads: lower CPM (less competitive inventory, all placements); tend to stop the scroll only for brand-aware viewers. Video ads: higher CPM (competitive inventory), more engaging for cold audiences. Never compare image CPM to video CPM as like-for-like. Retargeting CPM > prospecting CPM structurally. When CPM and frequency are both high, decide whether it's creative type, audience type, or fatigue before acting. Detect type from `ads_get_creatives` (`video_id`, `object_type`) or ad-name keywords (static/image/photo vs video/UGC/reel); if unclear, say so.

## Creative Format — Funnel Tendencies

| Format | Typical position | Why |
|---|---|---|
| Square image 1:1 | MOF–BOF | All placements, high inventory, shown to aware audiences |
| 9:16 vertical video | TOF | Stories/Reels-limited inventory → broader, newer audiences |
| 4:5 video | Varies | Content decides, not format |
| Long-form 60s+ | MOF–BOF | Only the interested watch; self-selecting |
| Us-vs-Them comparison (4:5) | TOF | Conquests market-aware strangers |
| UGC testimonial | MOF | Trust-building for aware non-converters |
| Founder story | MOF–BOF | 1–3 min stories need existing interest |

If a campaign is missing TOF, don't test another square image or long video — test 9:16 vertical or a comparison ad.

## Ad Concept Board — by Funnel Position

Notion source: https://hail-pond-0fc.notion.site/ebae3c1aaea34b8f9c85eaaa514d7f61?v=30f942daa302486d8c8d90731310b315

**TOF (fill the funnel):**

| Concept | Format | Foreplay board |
|---|---|---|
| Problem → Solution | Image, Video | https://app.foreplay.co/share/boards/ZdOkbfohWlTOCN79bRQ1 |
| Negative Marketing | Video, Image | https://app.foreplay.co/share/boards/qxgqhg8cnf4ZcUEd3oeD |
| UGC | Video | https://app.foreplay.co/share/boards/vEDoQoQryJogIk3r5UGa |
| Founder's Story | Video | https://app.foreplay.co/share/boards/6wdOoAI3tckZH0MlZbyL |
| Before & After | Image, Video | https://app.foreplay.co/share/boards/Is88CH3lw8VhJdubzsQg |
| 3 Reasons Why | Video, Image | https://app.foreplay.co/share/boards/8dHc5B2lEdoaTvRoB7ud |
| Headlines | Image | https://app.foreplay.co/share/boards/opKfcBFrigF6krDferXh |
| Ugly Ads | Video, Image | https://app.foreplay.co/share/boards/CxQXPI0okF6BCQm9Ptv2 |

**MOF (nurture & educate):**

| Concept | Format | Foreplay board |
|---|---|---|
| Features/Benefits Point-out | Image, Video | https://app.foreplay.co/share/boards/8l4Fsqk3Nn6P7MAjeXBb |
| Golden Nuggets Reviews | Image | https://app.foreplay.co/share/boards/9oCj9yS79PnLIPHOKqYK |
| UGC Comparison | Video | https://app.foreplay.co/share/boards/7ggT943LTPELRVXZScgH |
| Statistics | Video, Image | https://app.foreplay.co/share/boards/HA7Wb4KEsUZIxz9N23dZ |
| Post-it Notes | Image, Video | https://app.foreplay.co/share/boards/G9V3NweEphDlWXCzSGMM |

**BOF (close the deal):**

| Concept | Format | Foreplay board |
|---|---|---|
| Testimonials | Image, Video, Carousel | https://app.foreplay.co/share/boards/DSIMXXzBdQ5ZBloRew64 |
| Offers | Video, Image | https://app.foreplay.co/share/boards/BfXKDuphV5dXNd2Nzby4 |
| Carousels | Carousel | https://app.foreplay.co/share/boards/HNaP12hEAagXHfFdq34u |
| Unboxing ASMR | Video | https://app.foreplay.co/share/boards/Es9cFox8pSNeECyuCRf9 |

**Full-funnel:** EGC & BTS (https://app.foreplay.co/share/boards/SWgt1mJko0xpcmHPAU8P), Whitelisting (https://app.foreplay.co/share/boards/al7YuLZWv4YukY0nyP0W), Gifting (https://app.foreplay.co/share/boards/sgyifQdb2mCpu55ZhCaI), TikTok Comment (https://app.foreplay.co/share/boards/ZJxc71SDCbPLCindaw3s)

Using the board: match the gap to the tier → pick 1–2 concepts → explain WHY the concept fills the gap → link the Foreplay board → state the success signal (target frequency + CPM position). Pair with a hook from https://hooks.antoineorban.com/ and aim the angle at a specific persona from the brand intelligence.

## Learning Status

| Status | Interpretation |
|---|---|
| Learning (`delivery_sub_status: LEARNING`) | Metrics unstable. No strong recommendations. Label Watch unless clearly catastrophic. |
| Learning Limited (`FAIL`) | Common in small-budget accounts, NOT automatically negative. Many profitable ads live here forever. Note it; don't penalise it alone. Only a concern when paired with poor CPA, declining spend, or rising frequency. |
| Active (no sub-status) | Metrics reliable. Full 4PI applies. |

## Macro Environment Calendar

If the date range overlaps these, note it in the report header — CPM/frequency rises may be seasonal, not structural. Compare to the same period last year if data exists. Events compound.

| Event | Timing | Impact |
|---|---|---|
| BFCM | Late Nov | Severe — CPMs 2–5× |
| Christmas/Boxing Day | Mid–late Dec | High until Dec 25, drop after |
| New Year sales | Jan 1–7 | Moderate |
| Valentine's | Feb 1–14 | Moderate (gifting) |
| Easter | Mar/Apr | Mild–moderate |
| Mother's Day | May (AU/US) | Moderate (gift/wellness) |
| Father's Day | Sep AU / Jun US | Moderate |
| EOFY | June (AU) | Moderate |
| Amazon Prime Day | ~July | Moderate–high, hits non-Amazon too |
| Back to school | Aug–Sep | Moderate |
| Singles Day | Nov 11 | Moderate–high |
| Click Frenzy (AU) | ~Nov | Moderate |
| US elections | Even years, Oct–Nov | Significant US inflation |

## Budget Scaling Verdict (per campaign) & Account Sentiment

Lead gen and catalog campaigns use their own verdict tables (`references/campaign-types.md`); the table below is for purchase campaigns.

**Every active campaign section ends with an explicit scaling verdict** — one of three, always in 10–20% steps (bigger jumps reset learning; max one move per 3–4 days):

| Verdict | Conditions (ALL must hold for Scale; ANY triggers Trim) |
|---|---|
| **SCALE +10–20%** | Positive profit/order over 7d AND 30d · blended CPA at/below target (or clearly best vs recent history when no target) · a data-sufficient TOF ad with daily freq < 1.15 and flat/falling CPM · no CPM+frequency both-rising warning · hero ad past the data threshold and out of learning |
| **HOLD** | Default when mixed: hero below data threshold or in learning · hero handover in progress · windows disagree · macro event (Prime Day, BFCM…) distorting the read |
| **TRIM −10–20%** | Negative profit/order over 7d AND 30d · or CPM+frequency both rising with no TOF replacement ready · or daily frequency > 2.0 (saturation) |

Render the verdict as a checklist in the report — each condition with a pass/fail mark — so the reader sees *why*, not just the label. A HOLD should state what unlocks the next move and when (e.g. "re-check 16 Jul after the hero's 7-day read").

**Target mode in the checklist:** in `ltv` or `both` mode the "CPA at/below target" line reads **campaign NCPA at/below `target_ncpa`** and prints both numbers (e.g. "NCPA $47.28 vs $65 ✓ · blended CPA $38.17 shown for context"). With segments NOT SET UP or UNAVAILABLE, fall back as described in "Target modes" and say so on that line.

**Promo distortion rule:** when the client's own sale, promo or launch overlaps the 7d or 30d window, **always-on campaigns** (live before the promo started) still pick up promo-driven orders (site-wide conversion jumps, email traffic, 1-day-view credit). Judge their CPA/NCPA lines on the clean pre-event window, print the promo-window number beside it, and say which drove the call. **Promo-only campaigns** have no baseline: judge them on their own window against the promo's operating rules (e.g. a kill CPA) and the data bar. A budget raise made on promo-inflated numbers is a TRIM candidate once the promo ends.

**Account sentiment (report header): sentiment measures MONEY, not structure.**

One question only: *is this account making money, and is that improving or eroding?* A badge that fires on every structural imperfection is a badge that always reads amber — and an always-amber badge carries no information and needlessly alarms the operator. Structural issues are real, but they belong in Watch flags and in the scaling verdict, not in the sentiment.

Evaluate top-down at **account level**, on purchase and catalog campaigns only (lead and other campaigns are left out of every spend share and CPA here; a lead-only account badges on CPL, `references/campaign-types.md` §4), in this order; first match wins. STRONG is checked before STEADY because every STRONG account also meets STEADY's conditions: checked the other way round, STRONG could never show. STEADY is also the default when nothing else matches.

| Badge | Conditions |
|---|---|
| **DECLINING** (red) | Profit/order negative over 7d AND 30d · or profit/order fell >25% (7d vs 30d) while CPA rose >15% · or >40% of spend sits in campaigns with negative profit/order |
| **AT RISK** (amber) | Profit/order negative over 7d but positive over 30d (just turned) · or CPA >15% above target with spend flat/rising · or 20–40% of spend in unprofitable campaigns · or a hero carrying >60% of spend whose CPA has deteriorated >25% (fatigue **materialising**, not merely possible) |
| **STRONG** (green) | Profit/order positive and stable-or-up 7d vs 30d, CPA at/below target or clearly improving, no unprofitable campaign above ~10% of spend. When a promo skips the direction tests (Promo distortion rule), STRONG also needs the clean read to sit comfortably inside target and no SUSPECT segment setup making NCPA optimistic; otherwise STEADY |
| **STEADY** (blue) | Profit/order positive, CPA within ~15% of target, no material unprofitable spend. The default when no other row matches |

**Never set the badge on these alone** — they are Watch flags, not risk:

- **CPM movement.** CPM is an input price, not an outcome. It matters only once it reaches CPA and profit — and the YoY check exists to say whether it's the whole market rather than this account.
- **Funnel gaps / no TOF ad.** Already handled by the scaling verdict (no TOF → HOLD). Encoding it again as AT RISK double-counts it — this is the single biggest cause of sentiment inflation.
- **Single-ad concentration.** Normal below ~10 ads. It counts only when the concentrated ad's economics are actually deteriorating.
- **Frequency drift, learning status, macro events, platform incidents.** Context, not verdicts.
- **A noisy week under ~10 purchases.** The Small-Sample Rule applies to sentiment: judge on 30d and say so.

**No target CPA set** → judge on profit/order direction and unprofitable-spend share only. Never infer a target to produce a verdict.

**Target mode:** in `ltv` or `both` mode every "CPA vs target" condition in the badge table reads as **account NCPA vs `target_ncpa`**; blended CPA stays in the sentence for context. If segments are NOT SET UP or UNAVAILABLE, use `target_cpa` when one exists, else the no-target rule above, and say which in the sentence. The Promo distortion rule (above) applies here too: when a promo flatters the standard windows, set the badge on the clean pre-event read for always-on campaigns plus the promo campaigns' own numbers, skip the 7d-vs-30d direction tests for that run, and say so in the sentence.

**Watch flags line** (header, neutral gray, max 3): the named structural items — "no TOF feeder", "58% of spend on one ad", "hero frequency rising", "audience segments not set up", "existing customers over-served (frequency 45 vs 3.7)". Visible, specific, not dressed as an emergency.

**Calibration check before publishing: if the badge contradicts the sentence beside it, the badge is wrong.** "AT RISK — every economic target is being beaten" is a self-refuting header. Write the sentence from the money first, then pick the badge that matches it.

## Meta Platform Status Check

Before finalising, check https://metastatus.com/ads-manager and https://metastatus.com/ads-manager/history (firecrawl-mcp `firecrawl_scrape` with `maxAge: 0` — the MCP caches by default and a cached status page defeats the purpose of a status check; any web-fetch tool works as fallback). If any Ads Delivery / Reporting / Creation incident overlaps the analysis window, flag it in the report header — delivery dips and metric weirdness during an incident are platform noise, not ad performance. If clean, say so in one line ("no platform incidents in window"). If the check fails, write "platform status unchecked" — never guess.

## Year-over-Year Seasonality Check

Answers one question: **"is this period genuinely weak/strong, or is it just this time of year?"** A bad month that was equally bad last year is seasonality; a bad month that was strong last year is a real problem.

**Pull** (account level only): the report's 30d window and MTD window shifted exactly one year back, via custom `time_range` (e.g. 13 Jun–12 Jul 2026 → 13 Jun–12 Jul 2025). Fields: spend, impressions, CPM, frequency, results, cost_per_result, purchase_roas.

**How to read each metric YoY:**

| Metric | YoY meaning | Trust level |
|---|---|---|
| **CPM** | The cleanest seasonality signal — auction price for this audience at this time of year. CPM up 30% YoY with similar targeting = market inflation; expect higher CPAs everywhere and don't blame creative. | High |
| Spend | Context only — budget decisions changed it | Directional |
| CPA / purchases | Directional — account structure, creatives, offers all changed since last year | Directional |
| ROAS | Weakest — attribution and AOV both drift | Lowest |

**Rules:**

- Account level only. Never compare individual ads or campaigns YoY — they're different objects.
- YoY context **explains**, it never **excuses**: "CPM +35% YoY" reframes a rising-CPM read as seasonal, but a funnel-drying signal (CPM AND frequency rising now) still stands regardless of last year.
- Check the macro calendar for both years — if last year's window contained an event this year's doesn't (or vice versa), say so before comparing.
- If the YoY CPM gap is material (roughly ±20%), echo it into the report header's macro status chip — it changes how every CPM read in the report should be interpreted.
- Account has no data for the period last year (younger account) → one line: "no year-ago data — seasonality check unavailable"; never substitute industry lore for the missing year.
- Calendar dates, not weekday-aligned — note that weekday mix differs slightly YoY; it's a seasonality read, not a precision instrument.

## The 3 Testing Paths

**The queue rule:** recommend the next test even when the current hero is strong — *especially* then. A 4-day breakout is still in learning and can regress; every winner's fatigue clock starts the day it wins; creative takes 1–2 weeks to produce, so waiting for fatigue signals means running 3 weeks behind the decay curve; and per Andromeda, a structurally different concept expands delivery instead of cannibalising the hero. When recommending alongside a strong hero, say explicitly that it's the next rung, not a replacement — it launches small and either backs up a confirmed winner or replaces an unconfirmed one.

1. **Build a better prospecting ad** — when everything is MOF/BOF and CPM+frequency are rising. Goal: new ad lands at daily freq < 1.15 with CPM ≤ campaign's lowest. Direction: 9:16 vertical, us-vs-them, problem-first hook. Avoid testimonials/founder stories here.
2. **Build a true BOF closer** — when TOF feeds the funnel but nothing specialises in closing. Goal: freq > 1.40, high CPM (expected), lowest CPA in campaign. Direction: objection-overcoming, conversion-stage testimonials, strong offer + urgency, long founder story.
3. **Replace a weak ad at its own level** — when an ad does a specific job poorly (high CPM, bad CPA for position, low spend earned). Match the format/intent, fix the diagnosed drop-off. Success: more spend earned, lower CPM, better CPA at the same position.

## CSV Fallback — Processing Rules

Column mapping: Campaign name / Ad set name / Ad name / Day / Delivery status / Amount spent (any currency) / Impressions / Reach / Frequency / CPM / Results-Purchases / Cost per result / Purchase ROAS / AOV ("Average purchases conversion value") / GPT / Adds to cart / Outbound CTR (ad level only) / Outbound clicks / 3-second video plays / ThruPlays / Thumb Stop Ratio / Hold rate (ad level only) / CPC / Cost per 1,000 Accounts Centre accounts reached.

Critical rules:

- **AOV is a per-purchase average, not revenue.** Revenue = purchases × AOV, computed per row BEFORE aggregating. If the column is "Purchase conversion value" (no "average"), it IS total revenue. Getting this wrong skews ROAS 2–10×.
- Aggregation: sum spend/impressions/purchases/ATC/revenue; weighted-average AOV & GPT by purchases; weighted-average CPM/frequency/thumb-stop by impressions.
- Windows: 7d = report_date − 6 days inclusive; 30d = −29; MTD from the 1st. Filter `Day >= start AND Day <= end`.
- CPM if missing = spend/impressions × 1000.
- Status: ACTIVE = 'active' + spend within 3 days of report date; STOPPED = 'inactive'/'not_delivering' or no spend 7+ days; WINDING DOWN = active but spend down >50% over 3 days.
- Frequency trend: compare first half vs second half of range (impression-weighted). Rising = moving down-funnel.
- Ad-level-only metrics (Hold Rate, Outbound CTR, CVR) are empty on segment rows — normal, aggregate to ad level, never flag as missing.

## Tone & Decision Rules

1. Lead with 4PI always — never headline with hook rate or ROAS.
2. Campaign isolation in language too: "highest CPM **in this campaign**", never "for the account".
3. Status + data threshold checked before every recommendation.
4. Stopped ads: acknowledge stopped first, then the reactivation condition.
5. A TOF ad with bad CPA is not automatically bad — say so when it applies.
6. CPM + frequency both rising → call it out loudly. Loudest warning in the framework.
7. Every recommendation references a specific number. "Stop — CPA $112 vs campaign median $48, highest CPM at $44 vs low of $23" — not "stop this".
8. Below data threshold → "Insufficient data" + what's needed. No other label.
9. Fewer than 7 days of data → note frequency averages are less reliable.
10. Be direct. The reader is a busy operator: what does it mean, what do I do today?
11. Don't lead with what looks good — lead with what's missing and what's about to break.
12. Frequency is relative to spend — note when spend moved too.
13. Never "Scale" an ad. Budget is campaign-level; the label is **Scalable**.
14. Learning Limited is not a death sentence.
15. Account for creative type when reading CPM.
16. Account for audience type when reading CPM.
17. Flag repeat purchase bias (>50% existing customers).
18. Check the macro calendar before calling fatigue.
19. Flag attribution anomalies (low CTR + high purchases = possible 1DV inflation).
20. Cross-reference all three time windows before concluding.
21. Profit/Order (or GPT) overrides CPA for profitability decisions.
22. AOV context always accompanies CPA judgements.
23. When on the AOV−CPA proxy, always label it pre-COGS. Never present it as true gross profit.
24. Recommendations that involve big spends, offer changes, restructures, or shaky confidence get: "⚠ Double-check with the account owner before actioning."
25. Never invent inputs the user didn't give: no fabricated target CPA, margin, budget, or benchmark. Missing input → say it's missing and work with what exists.
26. In `ltv` mode the KPI is NCPA. Never judge blended CPA against an LTV or per-new-customer target.
27. Meta's "new" is not Shopify's "new": label NCPA as Meta's proxy unless the Shopify cross-check has run, and call it optimistic when the existing-customer definition looks SUSPECT.
28. Never conclude audience segments are "not set up" from one campaign; check the account over 90 days and say "confirm in Ads Manager".

## Action Labels

| Label | When |
|---|---|
| **Keep** | Good 4PI across the board; CPA at/below target; profit positive |
| **Hold** | Mixed signals; not bad enough to stop, not strong enough to scale |
| **Fix** | Specific issue named: hook, hold, CTA, offer, landing page, saturation, negative profit |
| **Watch** | Learning phase, short window, or unconfirmed trend shift |
| **Stop** | Underperforming with sufficient data; or negative profit with sufficient data |
| **Scalable** | Strong CPA, positive profit/order, high earned spend share, consistent across windows. Budget moves at campaign level. |
| **Insufficient data** | < 7 days or spend < 2× target CPA |

Never "Scale Ad" or "Pause". Ads are stopped, budgets are campaign-level. Positive profit/order is required for Scalable.
