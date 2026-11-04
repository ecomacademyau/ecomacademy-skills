# Campaign Types: Lead Gen and Catalog

The purchase 4PI (funnel map, TOF/MOF/BOF reads, NCPA, the purchase 4PI table) is built for campaigns that sell through ads doing different funnel jobs. Two campaign types don't fit it and get their own analysis:

- **Lead gen**: the result is a lead, not an order. No profit, no AOV, no NCPA.
- **Catalog**: Meta's catalog ads (Advantage+ catalog ads, formerly dynamic product ads). Treated as bottom of funnel by design, so there's no funnel to map.

Everything else with a purchase objective keeps the standard 4PI. Classify every campaign **before** Step 4 and print its type in the verification table.

## 1. Detecting the type

Classify at **ad-set level**, then roll up to the campaign.

| Type | How to tell (first match wins) |
|---|---|
| **Lead gen** | Campaign `objective` is `OUTCOME_LEADS` (or legacy `LEAD_GENERATION`), or the campaign's `results` indicator reports leads (`actions:leadgen.other` / `lead`) |
| **Catalog** | An ad set where catalog ads carry the majority of its 30-day spend. A catalog ad is one whose creative has a `product_set_id` (`ads_get_creatives`, mcp-data-pull.md §5). Fallback when creatives don't return the field: campaign objective `PRODUCT_CATALOG_SALES` |
| **Purchase** | Any other sales objective: the standard 4PI |
| **Other** (traffic, engagement, awareness, video views) | Snapshot row and one sentence (spend share, cost per result). No verdict, no section, never in the money maths |

**Roll-up:** a campaign is catalog when every ad set with spend is catalog. A campaign that mixes catalog and purchase ad sets stays **purchase**: its catalog ad sets are analysed with the catalog rules in a sub-block of that campaign's section. A catalog ad sitting inside a purchase ad set gets a **CATALOG** format badge and the normal purchase 4PI. This keeps an Advantage+ Shopping campaign with one catalog ad as the prospecting campaign it is.

## 2. Lead gen campaigns

**What's tracked:** cost per lead (CPL), daily frequency, and how CPL is tracking.

**Pulls:** the same windows as purchase campaigns, with the lead field (`lead` or `actions:leadgen.other`; the campaign's `results` indicator names the right one), plus the **campaign-level daily pull** (mcp-data-pull.md §3, item 4b) for campaign frequency and the daily CPL trend.

| Metric | Read |
|---|---|
| **CPL** (spend ÷ leads) | 7d and 30d, vs `target_cpl` when set. No target: vs the campaign's own CPL and sibling ad sets, and the report says "no CPL target set" |
| **CPL trend** | 7d CPL vs 30d CPL (the decision measure), with daily CPL as a mini chart. Rising = more than 5% above 30d; falling = more than 5% below; else flat |
| **Daily frequency** | mean of the campaign's daily frequencies. Lead campaigns should prospect: < 1.15 healthy · 1.15 to < 1.40 the audience is tiring · 1.40 to < 2.00 working a warm pool · ≥ 2.00 saturated |
| CPM, link CTR, spend pacing | context only, compared within the campaign |

**Data bar (per ad):** 7 days of delivery and **10 leads in the judged window**. Labels use 7 days; an ad with fewer than 10 leads in 7 days but 10 or more in 30 days is judged on 30 days, with both printed (the Small-Sample Rule). Below 10 leads in both: Insufficient data.

**Ad labels**, checked in this order, first match wins (the "comparison CPL" is `target_cpl`, or the campaign's 7d CPL when no target is set):

1. **Insufficient data**: under the data bar.
2. **Stop**: CPL ≥ 1.5× the comparison CPL.
3. **Fix**: daily frequency ≥ 2.00. New creative for the same offer.
4. **Scalable**: CPL at or below the comparison in 7d and 30d, CPL trend flat or falling, daily frequency < 1.15.
5. **Keep**: CPL at or below the comparison, daily frequency < 1.40.
6. **Watch**: 7d CPL more than 15% above the ad's own 30d, or daily frequency rising into 1.40 or above.
7. **Hold**: everything else.

**Scaling verdict (campaign)**, checked in this order: TRIM, then SCALE, else HOLD.

| Verdict | Conditions |
|---|---|
| **TRIM −10 to 20%** | any: CPL > 20% above `target_cpl` in 7d and 30d (no target: 7d CPL > 20% above 30d) · daily frequency ≥ 2.00 · CPL rising > 20% (7d vs 30d) while frequency rises |
| **SCALE +10 to 20%** | all: CPL at or below `target_cpl` in 7d and 30d (no target: 7d CPL at or below 30d) · CPL trend flat or falling · daily frequency < 1.15 and not rising |
| **HOLD** | everything else, including under the data bar |

**Lead quality** is the question CPL can't answer: cheap leads that never buy are a trap. When a Klaviyo connector is available, count the profiles that joined through the lead form's list or source in the last 30 days, and how many of them have a Placed Order event since joining. When it isn't, the report says "lead quality unchecked" and the next steps include the check. Never infer quality from CPL.

**Report section:** stat grid (Spend 7d · Budget/day · Leads 7d · CPL vs target · CPL 30d · Daily frequency · CPM · Link CTR) → one lead table `Ad | Status | Action | Spend 7d | Leads 7d | CPL 7d | CPL 30d | CPM | Daily freq | Daily spend` → scaling verdict card → next steps (≤ 3 bullets). No funnel map, purchase 4PI table, profit, NCPA or post-click audit. A hooks table only when an ad is labelled Fix (new creative for the same offer).

## 3. Catalog campaigns

**What's tracked:** daily frequency first, then CPA and profit/order (GPT when available). Link CTR and ROAS are shown as context; ROAS stays directional, as everywhere in this skill. Catalog ads retarget people who viewed or carted products, or show the catalog to a broad audience Meta picks; this skill treats both as bottom of funnel. So: **no funnel map, no TOF/MOF/BOF tags, and catalog ads never count as TOF** (see §4 for the account-level funnel gap). The new-customer share is shown as context, so a broad catalog that is in fact prospecting is visible.

**Frequency decides whether it can scale.** Use the mean of the campaign's daily frequencies from the campaign-level daily pull (mcp-data-pull.md §3, item 4b), rounded to 2 decimals before banding:

| Daily frequency | Band | Meaning |
|---|---|---|
| < 1.50 | **Room to scale** | Meta can still find fresh product viewers |
| 1.50 to < 1.80 | **Healthy** | the normal working zone for a catalog |
| 1.80 to < 2.00 | **Hold** | close to saturation; no budget increase |
| ≥ 2.00 | **Saturated** | the same people over and over; it can't scale |

**Economics, in every target mode:** catalog is judged **per order**, exactly like `first_order` mode: CPA vs `target_cpa` when one is stored (even in `ltv` mode, where it's otherwise display-only), and profit/order. No `target_cpa`: judge on profit/order and on CPA vs the catalog's own 30 days. Catalog buyers are mostly existing customers and recent product viewers, so its NCPA and existing share are shown as context, never judged, and the existing-customer rules (over-serving flag, repeat-purchase bias, SUSPECT check) don't apply to catalog campaigns.

**Scaling verdict (campaign)**, checked in this order: TRIM, then SCALE, else HOLD.

| Verdict | Conditions |
|---|---|
| **TRIM −10 to 20%** | any: profit/order negative in 7d and 30d · daily frequency ≥ 2.00 and CPA > 15% above `target_cpa` (no target: 7d CPA > 15% above its 30d) |
| **SCALE** | all: profit/order positive in 7d and 30d · CPA at or below `target_cpa` (no target: 7d CPA not more than 15% above its 30d) · frequency not rising. **+10 to 20%** when daily frequency < 1.50; **+10% at most** in the healthy band (1.50 to < 1.80) |
| **HOLD** | everything else: frequency 1.80 or above while profitable (with the duplicate recommendation below), mixed windows, or under the data bar |

**Losing money → find the products wasting spend.** When profit/order is negative, or CPA is above target with data behind it, pull spend by product (mcp-data-pull.md §3c): `breakdowns: ["product_id"]` at ad level, last 30 days, filtered to the catalog campaign. Rows come back per ad and product, so **sum by product id across ads** before judging. Products are judged on spend and purchases, never on product-level ROAS (it can return 0 even with a purchase). The comparison CPA is `target_cpa` when set, else the campaign's 30d CPA. Flag:

- products with spend ≥ 2× the comparison CPA and **0 purchases**,
- products with CPA > 2× the comparison CPA.

Show the 5 worst with their spend and purchases, recommend excluding them from the product set (a product-set filter), and link the training: [Catalog optimisation training (ECA Campus)](https://campus.ecomacademy.co/courses/products/ab0d008c-5711-4893-b162-af140a94a0bb/categories/c97185b6-0162-4d58-8037-db05a691e8b9/posts/306d7724-8b15-4ade-ab78-6001cb0794db?source=communities&group_slug=eca-campus-bij8r3). Store the flagged product ids in the recommendation (report-memory.md) so the next run can check them. If the breakdown errors or comes back empty, say so and recommend reviewing spend by product in Ads Manager; never estimate a product split.

**Frequency high (≥ 1.80 and rising, or ≥ 2.00) → duplicate the catalog.** Recommend a second catalog ad set or campaign with different primary text written for a different audience or reason to buy (for example gifting vs treating yourself, or another persona from the brand intelligence). Give 2 or 3 primary-text lines, each one or two short lines long: the catalog card already shows the product, price and name. Success signal: the duplicate's daily frequency under 1.50 while the original's stops rising.

**Ad labels inside a catalog campaign:** the standard labels and data bar, judged per order as above (CPA vs `target_cpa` or campaign peers, and profit/order). Stop needs negative profit or a CPA well above the campaign with data behind it. Scalable needs positive profit and daily frequency < 1.50; existing-customer volume doesn't block it in a catalog.

**Report section:** stat grid (Spend 7d · Budget/day · Purchases · CPA vs target · Profit/order · Daily frequency with its band · ROAS · Link CTR · CPM) → **frequency band bar** (the four bands with a marker at the campaign's daily frequency) → ad table `Ad | Status | Action | Spend 7d | % camp | Daily freq | Freq trend | CPA 7d | CPA 30d | Profit/order | Link CTR` → products to cut (only when losing money) → scaling verdict card → next steps (product cuts with the training link, the duplicate with its primary-text lines, budget). No funnel map, hooks table or post-click audit (catalog clicks land on many product pages, so there's no single page to audit).

## 4. Account-level effects

- **Funnel gap:** funnel-gap verdicts apply per purchase campaign only. Catalog ads never count as TOF. When no purchase campaign has a TOF ad (including a catalog-only account), the header Watch line still says "no TOF feeder".
- **Money maths** (blended CPA, profit/order, sentiment, share of spend in unprofitable campaigns): purchase and catalog campaigns only. Lead and other campaigns are left out of both numerator and denominator; their spend shows in the scorecard's spend card and the snapshot.
- **Account NCPA (judged):** purchase campaigns only. The fully loaded variant adds catalog, lead and other spend, labelled as such (Knowledge Base, "Audience Segments, NCPA & Target Modes").
- **Lead-only account:** no money badge is possible, so the header badge reads on CPL instead: STRONG (CPL at or below target and flat or falling) · STEADY (within 15% of target) · AT RISK (more than 15% above target, or rising more than 20%) · DECLINING (more than 30% above target in 7d and 30d). No target: judge the 7d CPL against its 30d with the same bands.
- **Quick mode:** the same type rules. Lead and catalog campaigns keep their stat grid, verdict and (catalog) products to cut, and show ads only when an ad is being actioned. "Other" campaigns never get a section, whatever their spend.
