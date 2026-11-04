# Changelog — eca-meta-ads-4pi

## v2.5.0 — 2026-10-23

**Lead gen and catalog campaigns get their own analysis** (new `references/campaign-types.md`). Every campaign is classified first: purchase, lead gen, catalog or other.

- **Detection** at ad-set level from the creative's `product_set_id` (now in the creative pull) and the campaign objective. A campaign with a few catalog ads stays purchase.
- **Lead gen:** judged on cost per lead (vs `target_cpl`, or its own 30 days), campaign daily frequency and the CPL trend. Data bar of 7 days and 10 leads, ordered labels with Hold as the default, its own SCALE / HOLD / TRIM table, a lead-quality check when a Klaviyo or CRM connector is available. No funnel map, profit, NCPA or purchase 4PI table.
- **Catalog:** always bottom of funnel, so no funnel map and never the account's missing TOF. Judged on daily frequency first (< 1.50 room to scale · 1.50 to < 1.80 healthy · 1.80 to < 2.00 hold · ≥ 2.00 saturated, TRIM checked first), then link CTR, CPA, profit/order and ROAS. Per order in every target mode; NCPA shown as context only, and the existing-customer rules (over-serving, repeat-purchase bias, SUSPECT check) don't apply to catalog. The judged account NCPA now covers purchase campaigns only.
- **Catalog losing money:** spend by product (`product_id` breakdown, verified live) to list products eating spend with no sales, recommend cutting them from the product set, and link the ECA catalog optimisation training.
- **Catalog frequency high:** recommend duplicating the catalog with short primary text written for a different audience.
- New campaign-level daily pull (campaign frequency can't be averaged from ads). Lead and other campaigns stay out of blended CPA, profit and sentiment; a lead-only account badges on CPL.
- Hooks and the post-click audit are for purchase campaigns (plus hooks for a lead ad labelled Fix).
- Client config gains `target_cpl`; Step 0's target question asks for it.

**Report readability.**

- Top 3 priorities move up to straight after the scorecard: decisions before detail.
- One snapshot table across 7d / MTD / 30d in Full as well as Quick (with campaign type).
- Collapsed "How to read this report" glossary under the header.
- Tables with more than 5 columns stack into cards on a phone: no sideways scrolling.
- Ads labelled Insufficient data (and ads stopped before the window) collapse into one list per campaign instead of a breakdown each.
- Slimmer purchase 4PI table (no Data OK? or AOV columns; Status kept; CPM carries its trend arrow).
- The HTML skeleton follows the new order; stacked-card tables use `<thead>`.
- Length target for Full: about 4,000 to 5,000 words; one home per number.

**Fix:** the account sentiment badge now checks STRONG before STEADY. Checked the other way round, STRONG could never show.

## v2.4.0 — 2026-10-23

**Audience segments and NCPA.** Every run now splits each sales campaign into new, engaged and existing customers and reports the cost per new customer.

- **Segment pulls on every sales campaign** (`breakdowns: ["user_segment_key"]`, 30d + 7d, plus a pre-event baseline when a promo overlaps). Verified live on manual CBO campaigns: the old "Advantage+ Shopping only" note was wrong and is gone.
- **NCPA** = all campaign spend ÷ (new + engaged purchases), with new-segment CPA, existing CPA, existing share and an account NCPA (fully loaded variant when non-purchase campaigns are ≥ 5% of spend).
- **Target modes**: `first_order` (`target_cpa`), `ltv` (`target_ncpa`) or `both`. Step 0's first question now asks per order or per new customer. In `ltv` mode NCPA replaces blended CPA in scaling verdicts, sentiment and ad labels (where ad-level NCPA exists); blended CPA is never judged against an LTV number.
- **Setup check**: OK · PARTIAL · SUSPECT · NOT SET UP · UNAVAILABLE, inferred from delivery at account level over 90 days (never from one campaign), always with "confirm in Ads Manager". Non-OK goes in the Watch line; NOT SET UP in `ltv`/`both` mode becomes a top-3 priority.
- **Delivery flags**: existing over-serving (existing frequency ≥ 3× new and ≥ 15% of spend → exclusion or cap test judged on NCPA), promo-window segment shift, TOF ads buying mostly existing customers, repeat-purchase bias now available on every campaign.
- **Shopify cross-check** (optional): new vs returning customers and the Meta NCPA floor (Meta spend ÷ Shopify new customers), only when the connector is on the client's own store. A Meta NCPA below the floor is flagged as over-claiming.
- **Promo distortion rule**: when the client's own sale overlaps the window, verdicts and sentiment use the clean pre-event read, with the promo number printed beside it.
- **Report**: NCPA KPI card, NCPA column in the snapshot tables and campaign stat grids, targets chip with the mode, new Audience Segments & NCPA card (Full mode).
- **Memory**: history schema gains `targets`, `segments_setup`, NCPA and existing-share fields, and an `audience` recommendation type; history is also saved to the attached claude.ai Project so it survives between sessions.
- **Client config**: `target_mode`, `target_ncpa`, `shopify_domain` (see `clients/README.md`).

## v2.3.1 — 2026-07-31

**Sentiment rebuilt around money — fixes chronic AT RISK inflation.** The old rule fired AT RISK on *any* live structural warning ("profitable but…"), so profitable accounts beating every target were badged amber and the badge stopped meaning anything.

- Sentiment now answers one question: is the account making money, and is that improving or eroding? Explicit thresholds per badge (profit/order sign and direction, CPA vs target, share of spend unprofitable, hero deterioration).
- CPM movement, funnel gaps / no TOF ad, single-ad concentration, frequency drift, learning status and macro events **can no longer set the badge**. They render as a neutral "Watch:" line in the header and feed the scaling verdict, which already exists to say "you can't grow safely yet".
- Small-Sample Rule now applies to sentiment (a noisy week under ~10 purchases is judged on 30d).
- No target CPA → judge on profit direction and unprofitable-spend share only; never infer a target.
- Calibration check: if the badge contradicts the sentence beside it, the badge is wrong.

## v2.3.0 — 2026-07-31

**Quick mode is now campaign-level** — length stays flat as accounts grow (target ≈2,000–2,500 words regardless of campaign count):

- One snapshot table instead of three (active-ads and funnel-health strings were identical across windows)
- **Funnel-health bar** per campaign (stacked TOF/MOF/BOF/SAT spend share + one-line gap verdict) replaces the per-ad funnel map
- **"Ads to act on"** table replaces the full 4PI ad-by-ad grid — only non-Keep ads, with the numbers that justify the call, plus "the other N ads: Keep/Hold, no change". Ad evidence is never dropped for an ad being actioned.
- **Campaign triage**: full treatment only for campaigns ≥10% of spend or carrying a red flag; the rest get a snapshot row and one sentence
- Diagnosis merged into Next Steps (≤100 words/campaign); Top Priorities capped at ~120 words each

**Post-click audit upgraded (Full mode):**

- **Four-step click decomposition** (click→page · page→cart · cart→buy · purchases/click) is now the standard method — localises the leak instead of just detecting one. The step that varies across creatives is the diagnosis; everything downstream of the cart is creative-independent.
- New third trigger gate: the decomposition must point at a step the page controls. A prospecting ad losing people at page→cart with healthy cart→buy is TOF economics — not audited.
- **Fix ladder** with page-type recommendations: copy/framing → reorder → section addition → advertorial/listicle lander → dedicated campaign landing page → quiz funnel. Cheapest fix that addresses the step; escalation note from advertorial tier up.
- Report-writing rules: ~400 words, verdict first, method never printed in the report, findings weighted by confidence and value.

## v2.2.1 — 2026-07-29

- **Trend-label correctness**: headline frequency/CPM and their trend endpoints must come from one series (mean of dailies; first-3 → last-3), with an explicit ±2% flat band. Fixes labels contradicting their own numbers ("rising (1.42 → 1.42)") and headlines sitting outside their own trend range. Frequency direction feeds the both-rising danger signal, so this is correctness, not cosmetics.
- **Small-Sample Rule**: ads with ≤2 purchases or <2× target CPA of spend in the 7-day window are judged on their 30-day figures, with both printed and the switch stated in one line. Codifies what the 29 Jul report did ad-hoc.

## v2.2.0 — 2026-07-16

- **Report depth modes**: third pre-flight question — Full report vs Quick check, with context-aware recommendation (Full for first reports / stale memory; Quick for routine re-runs). Quick keeps the identical analysis, verdicts, and history write, skips enrichment calls (YoY, benchmark, post-click, anomaly/opportunity) and renders the condensed report (scorecard + Since Last Report + funnel maps + 4PI tables + scaling verdicts + top 3 priorities). Post-click candidates in Quick mode are flagged in one line, not audited. History schema gains a `mode` field.

## v2.1.1 — 2026-07-16

- **Industry Benchmark card redesign**: percentile band graphic (p25/median/p75), per-campaign 30d ROAS table with quarter pills + bold ACCOUNT row, plain-language explainer, "Why ROAS only" bullets (cohort is USD — cost metrics never compared or converted cross-currency; ROAS is a ratio so it travels), "context, not a verdict" close. Data provider anonymised in all client-facing output.

## v2.1.0 — 2026-07-16

- **Year-over-year seasonality check**: account-level comparison of the 30d + MTD windows vs the same calendar dates last year, rendered as a card under the Account Snapshot. CPM leads (cleanest seasonality signal); material YoY CPM gaps (±20%) echo into the header macro chip. Graceful skip for accounts with no year-ago data.
- **Version stamping**: skill version in frontmatter + title; every report footer states the producing version.
- **Firecrawl freshness**: `maxAge: 0` on metastatus checks and post-click scrapes (the MCP caches by default); confirmed the firecrawl-mcp schema supports geolocated scraping (`location.country`).
- **Triple Whale benchmark fallback**: when Meta's peer benchmark returns no data, scrape benchmark.triplewhalelabs.com for the client's vertical (new `industry_vertical` config field) — free Meta-channel ROAS/CPA/CPM p25/median/p75, rendered as percentile placement, directional context only.

## v2.0.0 — 2026-07-13

Full rebuild of the original CSV-only skill:

- Official Meta Ads MCP as primary data source (live-verified field names), CSV fallback retained
- Data-freshness guard (never reuse a previous day's pulls; re-runs always re-pull)
- Pre-flight questions: target CPA (with "I don't know" → ecomOS pointer; never invented) + account/campaign scope
- Profit per Order = AOV − CPA (pre-COGS proxy; GPT column overrides on CSV path; margin % upgrade via client config)
- ECA Design System report skin (dark hero, stat grids, chip rows, CSS/SVG charts, frequency legend with exact values, VIDEO/STATIC format badges)
- Account sentiment badge + metastatus.com platform check in header
- Campaign scaling verdicts (SCALE +10–20% / HOLD / TRIM −10–20%) with pass/fail checklist
- Hardened post-click audit: trigger gates (data bar + one-purchase swing test), delivered-market from country breakdown, geolocated scrape, currency reconciliation with no FX maths, DOM-presence ≠ user-visible, "page is fine" is a valid outcome
- Report memory: week-over-week deltas + "Since Last Report" accountability card (history JSON beside + inside each report)
- Industry benchmark enrichment (LAST_28D, graceful skip when Meta returns no peer data)
- Andromeda hook generator (3–5 structurally-diverse hooks grounded in reviews/personas)
- Recommendations grounded in five named sources; escalations addressed to "the account owner"
