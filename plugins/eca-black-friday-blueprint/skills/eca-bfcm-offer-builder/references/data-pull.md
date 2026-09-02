# Pulling the evidence

The offer recommendation is only as good as this step. Get the windows right, pull what you can, and **be explicit about what you could not get**.

## 0. Confirm every connector belongs to THIS store (do this first)

A connected account is not necessarily *their* account. Agency logins, multi-brand owners and course businesses routinely have several. Pulling the wrong one produces a confident, detailed, completely wrong analysis, and nothing downstream will catch it.

Before using a single number:

- **Shopify** — note the shop domain the tools return. Everything else is checked against it.
- **Klaviyo** — read the account details and match `organization_name` and `website_url` to the Shopify domain. If they do not match, stop and tell the member which account is connected.
- **Meta Ads** — list the ad accounts and match by name to the brand. Never assume the first one, and never assume there is only one. Also check `is_queryable` before querying.
- **Anything else** — same rule: prove it is theirs.

**Say which specific accounts you matched**, by name, in one line. If one cannot be matched, mark that whole data source `NOT AVAILABLE — wrong or unmatched account` and carry on without it.

## 1. Compute the windows first — never hardcode them

Black Friday moves every year. A hardcoded date silently compares the wrong week and every conclusion after it is wrong.

```bash
python3 scripts/bfcm_dates.py            # this year vs last year
python3 scripts/bfcm_dates.py 2026 --json
```

Windows produced, for both this year and last:

| Window | Definition |
|---|---|
| Pre-BFCM build-up | 1 Oct → the Sunday before BF week |
| BFCM week | Monday of BF week → Cyber Monday |
| Post-BFCM to EOY | day after Cyber Monday → 31 Dec |
| Full Q4 | 1 Oct → 31 Dec |

**Always state the actual dates back to the member.** "Last year's BFCM week was 23 Nov to 1 Dec 2025" lets them correct you if their sale ran on different dates. Many brands run their own window — if theirs differs, use theirs and say so.

## 2. Shopify — the spine of the analysis

Use the analytics query tool (ShopifyQL). These are **verified working**:

**Core trading metrics, per window:**
```sql
FROM sales
SHOW orders, gross_sales, discounts, net_sales, total_sales,
     average_order_value, new_customers, returning_customers
SINCE <start> UNTIL <end>
```

**Sessions and conversion rate, per window:**
```sql
FROM sessions SHOW sessions, conversion_rate SINCE <start> UNTIL <end>
```

**Daily shape across the event** — this is where the useful detail lives, because it shows which day actually carried the revenue and whether the sale peaked on launch or on the last day:
```sql
FROM sales SHOW orders, total_sales, discounts, average_order_value
TIMESERIES day SINCE <start> UNTIL <end>
```

**What sold, so the offer can be built around real winners:**
```sql
FROM sales SHOW gross_sales, net_sales, orders
GROUP BY product_title ORDER BY gross_sales DESC LIMIT 20
SINCE <start> UNTIL <end>
```

**Stock position now**, for any clear-stock objective — use the inventory query or the product/inventory tools, and get sell-through, not just units on hand.

**The discount rate does not tell you what the offer was.** Free shipping, gift-with-purchase, bundle pricing and threshold offers frequently do not appear in the discounts metric at all. A store can run seventeen emails and a full sale and still show a discount rate barely above a normal week. **Never characterise last year's offer from the discount number alone** — read the email campaign names and the on-site record first, then come back to the number.

**Discount detail.** ShopifyQL gives total discounts, not which code drove them. For the mechanic-by-mechanic breakdown, query orders and group by discount code via GraphQL, or read price rules. If that fails, **ask the member what they ran** — they remember. Record the answer as member-supplied, not measured.

## 3. Meta Ads

Pull spend and return per window, not just the total. The pre-BFCM build-up is often where the money is won or lost, and it is the number most brands never look at.

Per window, get: spend, purchases, purchase value, ROAS, CPM, CPA, frequency. Also note **what the ads were actually saying** last year, since a repeat of a winning angle is worth more than a new one.

If the account is not connected, ask for the four numbers that matter: spend, revenue, ROAS, and roughly when they turned spend up.

## 4. Klaviyo

**Read the campaign names first.** Before any metric, list the campaigns in the window and read their names in order. Brands name sends things like "VIP Early Access | Launch", "Black Friday | 1 day offer: Free Shipping", "Cyber Monday | Extended". That list reconstructs the entire offer structure, the phasing and the mechanics — none of which appears in any Shopify metric. It is the single cheapest, highest-value pull in this whole step.

**Campaigns in the window:** list campaigns for the date range, then pull the report for each — sent, opens, clicks, revenue. You are looking for which *send* carried the revenue, and whether the winner was the announcement, the reminder, or the last-chance email. That single fact shapes this year's send plan.

**Revenue per recipient, split by audience — this is mandatory.** Total campaign revenue hides the finding that usually changes the decision. Group the report by campaign and compare revenue per recipient across audiences. A small early-access or VIP segment routinely earns many times what a full-list broadcast does per person, and when it does, the constraint on the event was audience size, not offer depth. Report it as a table with recipients, revenue and revenue per recipient, and call out the ratio between the best and worst audience.

Also note the sends that **cost** list: high unsubscribe rate with no revenue is a real loss, especially on a small high-value segment.

**Flows** matter too. A large share of BFCM email revenue usually comes from abandoned-cart and browse-abandon flows working harder because traffic is higher, not from campaigns.

**List size now vs 12 months ago.** Do this honestly, because it is easy to get wrong:

- **Best:** a segment time series, which gives real historical membership.
- **Acceptable fallback:** current subscriber count, minus profiles that subscribed in the last 12 months. **State the limit plainly:** this ignores unsubscribes and churn, so it flatters growth. Label it as an estimate.
- **Never** present an estimate as a measurement.

## 5. Anything else connected

Use what is there and say what it added. Analytics tools with session recordings or heatmaps can explain *why* conversion moved. Google Ads, TikTok, Amazon and retail wholesale all belong in the revenue picture if the member sells there. Ask once: "anywhere else revenue came from last Q4 that I should count?"

## 6. Coarse first, then fine

Do not pull a year of daily rows into the conversation. Pull **weekly** for the long scan, find the periods that matter, then pull **daily** only around those. It costs a fraction of the tokens and it is also better analysis, because you look closely at the right fortnight instead of skimming 365 rows.

## 7. Rules for this step

- **Never state a trend from an aggregate.** A single number over a long window hides everything. Before claiming traffic fell, revenue grew, or conversion improved, pull the daily or weekly series and look at the shape. A busy October inside a 53-day average will tell you BFCM traffic collapsed when it did not.
- **Verify field names before querying.** Ad and email APIs reject plausible-sounding fields and rename them between releases. Ask for a specific field list rather than everything, both because unfiltered responses are enormous and because the error tells you the real name.
- **Try the tool before you say it is unavailable.** Do not tell a member to connect something you have not attempted.
- **Connected does not mean usable.** Plan gating, scopes and permissions all fail at query time. Test, then report.
- **Process large pulls in code, not in your head.** Daily rows across a quarter across four platforms is a lot of tokens and a lot of arithmetic errors. Write it to a file and compute.
- **Round money sensibly and keep currency explicit.** Mixed-currency stores need this stated once, clearly.
- **Every table gets its source and window.** Six weeks later nobody remembers where a number came from.
- **Never fabricate a benchmark.** If you do not have industry data, do not invent "typical BFCM uplift is 3x". Compare the brand against itself.

---

## 8. The whole-year outlier scan (do not skip this)

**The brand's best offer of the year is often not the Black Friday one.** Comparing this year's plan only against last year's BFCM hides the flash sale, the EOFY push, the launch or the January reactivation that beat it — sometimes on a fraction of the discount. Scanning the full year is what stops a member repeating a mediocre event simply because it happened in November.

### Pull

```sql
FROM sales SHOW orders, total_sales, discounts, average_order_value
TIMESERIES week SINCE <13 months ago> UNTIL today
```

Weekly, not daily. Then feed it to the script:

```bash
python3 scripts/promo_outliers.py rows.json
```

### What the script does, and why it is not just "biggest week"

- **It detrends.** A growing business makes every recent week look like an outlier. Each period is compared against its own trailing baseline (median of the previous 8), not the annual average.
- **It weights lift by what the lift cost.** A week that lifted revenue 40% on 5% discounting is a far better template than one that lifted 60% on 25%. Ranking on revenue alone rewards the most expensive events, which is exactly how brands end up repeating their least profitable one.
- **It separates free lifts.** Periods that grew with no increase in discount rate are the most interesting result the scan can produce, because whatever drove them was not price.

### Then explain the winners — and ask about the ones you cannot

The scan finds **when**. Only the record explains **why**. For each outlier period, check the email campaigns sent, the ad spend, and any launch or press in that window.

**Where the data cannot explain a period, ask the member.** This is a required step, not a nicety. The causes that never appear in Shopify or Klaviyo are exactly the ones that decide whether a period is repeatable: a wholesale or corporate order, a press mention, a viral post, a market or event, a stockout recovery inflating the following week, a supplier issue, a one-off partnership.

Record every outlier as explained by `data`, by `member` (recollection, labelled as such), or `unexplained`. **Never base a recommendation on an unexplained spike**, and never guess at a cause — a guessed explanation gets repeated back as fact.

### Feed it into the recommendation

Put the best template next to the BFCM plan explicitly. If the strongest efficiency of the year came from a mechanic the member is not planning to repeat, **say so before the offer is designed**, not after. If BFCM genuinely was their best event, that is worth stating too — it makes the case for going harder at it.
