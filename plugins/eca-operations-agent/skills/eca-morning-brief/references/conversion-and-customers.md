# Conversion and customer mix

Two sections that answer different questions. The funnel says **where visitors are being
lost**. The customer mix says **whether the revenue is coming from new people or the same
people spending more**. Both change what the member should do, which is why they are in
the brief rather than in a dashboard.

## The funnel

```sql
FROM sessions
SHOW sessions, sessions_with_cart_additions, sessions_that_reached_checkout,
     sessions_that_completed_checkout, conversion_rate
TIMESERIES day SINCE -14d UNTIL today
```

Verified against a live store. `conversion_rate` comes back as a decimal, so 0.0226 is
2.26%. **Drop today's row** before summing, as everywhere else in this brief.

Sum the 14 complete days rather than reading a single day. Daily conversion on a store
doing 40 orders a week swings wildly on small numbers and means nothing day to day.

### Read it as three steps, not one number

A single conversion rate tells the member they have a problem. The step rates tell them
which problem, and those are three completely different jobs.

| Step | What a weak number points at |
|---|---|
| **Sessions → added to cart** | The product page, the offer, the price, or the traffic. People arrived and were not convinced. |
| **Cart → reached checkout** | Cart friction. Shipping cost appearing late, a clunky cart drawer, no express option. |
| **Reached checkout → paid** | Checkout friction. Payment methods, forced account creation, a final total that surprised them. |

**Name the biggest leak and only the biggest leak.** A brief that says all three could be
better is a brief nobody acts on. One sentence: "84% of carts reach checkout and 66% of
those pay, both fine. Only 4.1% of visitors add to cart at all, so the leak is the product
page, not the checkout."

### Benchmarks: use the store against itself

**The primary comparison is this store's own trailing average**, the same way every other
number in this brief works. A store that converted at 2.6% last month and 2.2% this month
has a real change worth reporting.

Rough ranges exist and are worth using as a **sanity flag only**, said plainly as rough:
add-to-cart is commonly 6 to 12% of sessions, cart to checkout 50 to 70%, checkout to paid
60 to 80%. **Say "roughly" and never treat these as a target.** A considered-purchase store
at a high price will sit below all of them and be perfectly healthy. If the member's own
trend is flat and only the rough range looks off, say that is worth a look rather than
that something is wrong.

### Size the opportunity, and label it a model

The useful version of a conversion finding is what fixing it is worth. Hold the downstream
rates constant and move only the weak step:

> "If add to cart reached 8% with the rest of the funnel unchanged, that is 139 orders over
> 14 days instead of 71. **This is a model, not a forecast**: it assumes the extra carts
> behave like the current ones, and they usually convert slightly worse."

The caveat is not optional. A number like that gets quoted in a meeting, and it should
arrive with its assumption attached.

### What to suggest

Suggest against the leak, not in general. Two or three, concrete, tied to what the data
says. **Never more than three**, and never a generic CRO checklist.

| Weak step | What to actually suggest |
|---|---|
| Sessions → cart | Does the page answer the first objection above the fold? Is the price doing the work the offer should? Is the hero image the product in use rather than on white? Where is traffic coming from, and does that audience match what the page promises? |
| Cart → checkout | Is shipping cost visible before the cart? Is there a free-shipping threshold and is it shown? Is express checkout on the cart as well as the product page? |
| Checkout → paid | Which payment methods are offered? Is account creation forced? Does the final total differ from what the cart implied? |

Where a sibling skill owns the fix, name it: a product page problem is
`eca-product-page` or `eca-landing-pages`, a traffic-quality problem is `eca-meta-ads-4pi`,
and what customers actually object to is `eca-survey-report`. Hedge with "if installed".

## Customer mix and AOV

```sql
FROM sales
SHOW customers, new_customers, returning_customers, returning_customer_rate, average_order_value
TIMESERIES week SINCE -84d UNTIL today
```

Weekly, not daily. Returning-customer rate on a single day is noise. Twelve weeks gives a
trend that means something and still fits in one pull.

> `returning_customer_rate` is a decimal, so 0.4681 is 46.8%. **Drop the current partial
> week**, which otherwise reads as a collapse every Monday.

### The four readings that matter

AOV and returning rate are only interesting together. Each pairing is a different story
and a different action:

| AOV | Returning rate | What it usually means |
|---|---|---|
| Flat or down | Up | Revenue is being held up by the same people buying again, often on discount. Acquisition is the problem, not retention. |
| Up | Down | Fewer, bigger orders. Often a narrowing audience or a price rise absorbing the gap. Watch new-customer count, not revenue. |
| Down | Down | The clearest warning in the brief. Both halves weakening at once. Say so plainly. |
| Up | Up | Genuinely healthy. Say it in one line and move on. |

**Read it beside ad spend.** Rising returning-customer share while paid spend climbs is
the most expensive pattern a store can run: paying prospecting prices to reach people who
would have come back anyway. That belongs in the actions, not in a metric card.

### What to suggest

- **AOV falling** — check whether discount codes are carrying more orders than they were,
  whether the mix has shifted to cheaper products, and whether a bundle or threshold
  exists at all. A free-shipping threshold slightly above current AOV is the usual first
  move.
- **Returning rate falling** — a retention and email question before it is a product one.
  `eca-email-marketing-campaign` if installed, and check whether the post-purchase flow is
  still running at all.
- **Returning rate rising while new customers fall** — do not celebrate it. The store is
  shrinking to its loyalists. Lead with the new-customer number.

**One suggestion per finding.** The brief's job is to make the next move obvious, not to
list everything that could be improved.

## Channels: where the orders actually came from

The brief reads Meta Ads directly because there is a connector for it. **There is no
first-party Google Ads connector**, and most members will not have a paid aggregator. That
is not a reason to ignore Google: Shopify reports which channel each order came from, and
that covers every channel at once without connecting anything.

```sql
FROM sales SHOW orders, total_sales
GROUP BY order_referrer_source, order_referrer_name
ORDER BY total_sales DESC LIMIT 12
SINCE <14 days ago> UNTIL <yesterday>
```

Verified against a live store. One real result, over a fortnight:

```
(direct / none)      32 orders   $1,810
search / google      19 orders   $1,363
social / facebook    19 orders   $1,237
social / instagram    5 orders   $  283
search / bing         1 order    $   67
```

A Meta-only brief would have reported the Facebook line and missed that Google delivered
just as many orders. **Always run this, even when Meta Ads is connected**, because it is
the only view that shows the channels nobody has wired up.

### What this can and cannot tell you

Be exact about this, because the temptation is to treat it as a channel P&L and it is not.

| It can say | It cannot say |
|---|---|
| How many orders and how much revenue each channel produced | What any of it cost, except Meta where the connector gives spend |
| Whether a channel moved week on week | ROAS for anything but Meta |
| That a channel exists at all, which is often the finding | Whether `search / google` was paid or organic. Shopify does not split them. |

**Never present a Google ROAS the brief cannot compute.** Report orders and revenue, say
plainly that spend is not visible, and leave it there.

**The blank referrer row is usually the biggest one** and it is not a channel. It is
direct traffic, app traffic, stripped UTMs and anything the browser did not pass along.
Name it as unattributed rather than calling it direct, and never let it top a channel
ranking without that caveat.

**This is Shopify's last-click view.** It will disagree with what Meta reports, often by a
lot, because the platforms count differently and both are self-interested. Where they
disagree, say so rather than picking the flattering one. That disagreement is itself worth
a line in the brief when a budget decision is pending.

### Getting Google spend in, for members who want it

Setup should ask, once, and record the answer so later runs do not re-ask:

- **No connector**, the default. Orders and revenue by channel from Shopify, no spend, no
  ROAS. Say so in the ads section rather than leaving a gap the member has to notice.
- **A paid aggregator** such as Supermetrics or Adspirer, which can reach Google Ads.
  If one is connected, pull Google spend and compute return properly.
- **Manual**, where the member pastes yesterday's Google spend. Only worth offering if
  they ask; a daily manual step rarely survives a fortnight.
