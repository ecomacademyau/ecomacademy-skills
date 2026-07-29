# Facebook Ads 4PI Analysis — Knowledge Base

Contents: Core philosophy · Misleading metrics · The 4PI framework · Funnel decoder · Golden rule · Campaign isolation · Ad status · Minimum data · Time windows · Audience segments · Attribution · Profitability (Profit per Order / GPT) · AOV · Creative diagnostics · Creative type & CPM · Format funnel tendencies · Ad Concept Board · Learning status · Macro calendar · 3 testing paths · CSV fallback processing · Tone & decision rules · Action labels

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

All 4PI analysis is campaign-scoped. Never mix ads across campaigns: CPM comparisons, spend %, funnel gaps — all per campaign. Different objectives, products, audiences make cross-campaign CPM comparison meaningless. Group by campaign first, run 4PI in each independently, map each funnel, diagnose each gap; summarise across campaigns only in the account-level summary.

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

## Audience Segment Context

Via MCP: only Advantage+ Shopping campaigns expose `user_segment_key` (new vs existing). Via CSV: Audience Segments column (New/Engaged/Existing). Use as diagnostic cross-validation of the frequency read, not the primary unit.

**Repeat purchase bias:** if a large share of purchases comes from existing customers, CPA/ROAS look strong but conversions were largely going to happen anyway. An ad that looks Scalable but converts mostly existing customers will not scale — the pool is too small. Truly scalable ads prove themselves in the new/prospecting segment. Flag whenever existing > 50% of purchases.

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

Ad Concept Board (source): https://hail-pond-0fc.notion.site/ebae3c1aaea34b8f9c85eaaa514d7f61?v=30f942daa302486d8c8d90731310b315

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

**Every active campaign section ends with an explicit scaling verdict** — one of three, always in 10–20% steps (bigger jumps reset learning; max one move per 3–4 days):

| Verdict | Conditions (ALL must hold for Scale; ANY triggers Trim) |
|---|---|
| **SCALE +10–20%** | Positive profit/order over 7d AND 30d · blended CPA at/below target (or clearly best vs recent history when no target) · a data-sufficient TOF ad with daily freq < 1.15 and flat/falling CPM · no CPM+frequency both-rising warning · hero ad past the data threshold and out of learning |
| **HOLD** | Default when mixed: hero below data threshold or in learning · hero handover in progress · windows disagree · macro event (Prime Day, BFCM…) distorting the read |
| **TRIM −10–20%** | Negative profit/order over 7d AND 30d · or CPM+frequency both rising with no TOF replacement ready · or daily frequency > 2.0 (saturation) |

Render the verdict as a checklist in the report — each condition with a pass/fail mark — so the reader sees *why*, not just the label. A HOLD should state what unlocks the next move and when (e.g. "re-check 16 Jul after the hero's 7-day read").

**Account sentiment (report header):** one badge + one plain sentence summarising how the account feels this week. Derive from 7d vs 30d deltas and funnel health:

- **STRONG** — CPA improving, profit/order up, funnel healthy or improving
- **STEADY** — stable metrics, no structural warnings
- **AT RISK** — profitable but a structural warning is live (funnel drying, hero fatigue, saturation, single-ad concentration)
- **DECLINING** — CPA worsening AND profit/order falling across windows

A week can be STRONG and still carry a risk note — sentiment is the headline, not the whole story.

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
