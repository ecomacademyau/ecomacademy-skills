# Where each number comes from, and what goes wrong

Every query below was run against a live store before being written down. The traps are
real failures, not hypotheticals, and each one produces a wrong answer quietly rather
than an error.

## Before anything: test the connector, do not assume it

A tool appearing in the tool list is not an authenticated connection. Call something
cheap and read the response.

```
Shopify    get-shop-info                 also gives you the timezone and currency
Meta Ads   ads_get_ad_accounts           also gives you the account list to choose from
Gmail      search_threads, small query   also tells you the mailbox is the right one
```

Shopify failing means no brief. The other two mean a named gap in today's brief.

## Shopify

### Daily sales, for the comparison and the chart

```sql
FROM sales SHOW orders, total_sales, average_order_value
TIMESERIES day SINCE -14d UNTIL today
```

One call gives yesterday, the same weekday last week, and the 14 bars the chart needs.

> **The partial-day trap.** The last row is today, and it is a few hours old. Against a
> complete day it reads as a 90%+ collapse. Drop it before any comparison or chart. This
> is the single most likely way this brief becomes nonsense.

### What sold yesterday

```sql
FROM sales SHOW net_items_sold, gross_sales
GROUP BY product_title ORDER BY net_items_sold DESC LIMIT 8
SINCE 2026-10-08 UNTIL 2026-10-08
```

> **Relative single days return nothing.** `SINCE -1d UNTIL -1d` gives an empty result
> set, not an error, so the section silently renders empty. Use explicit dates for any
> single past day.

> Rows with an empty `product_title` and zero units come back in the results. Filter them.

### Dispatch

```
list-orders  query: fulfillment_status:unfulfilled AND financial_status:paid
```

Age each from `createdAt` in the store's timezone.

> **The forgotten test order.** Stores accumulate $0.00 orders that sit unfulfilled for
> years. One real example had been open since October 2024. Included naively, "oldest
> unfulfilled" reads as 730 days every morning forever. Exclude $0.00 orders and anything
> past 90 days from the backlog, and mention them once as housekeeping.

Daily fulfilment counts, for whether dispatch is batching:

```sql
FROM fulfillments SHOW orders_fulfilled, orders_shipped, orders_delivered
TIMESERIES day SINCE 2026-10-01 UNTIL 2026-10-08
```

> There is no time-to-fulfilment column. `avg_time_to_fulfillment` does not exist and
> errors. Derive dispatch speed from order ages instead.

### Stock cover

```sql
FROM inventory SHOW ending_inventory_units, inventory_units_sold
GROUP BY product_title ORDER BY inventory_units_sold DESC LIMIT 12
SINCE <28 days ago> UNTIL <yesterday>
```

Weeks of cover = `on_hand / (units_sold / 28) / 7`.

> **Placeholder inventory.** Variants reading exactly 1000, 3977, 4000 and similar are
> usually untracked or placeholder counts rather than real stock. Cover computed from
> them is meaningless. Say which numbers can be trusted rather than reporting cover for
> all of them.

> Deep analysis belongs to the stock skills. The brief only flags what is under the
> threshold and hands off.

### The forecast

```sql
FROM sales SHOW total_sales, orders TIMESERIES month SINCE <5 months ago> UNTIL today
```

Month to date is actual. Project the remainder on **the last seven days' daily average**,
not the month-to-date average: a month that started strong and broke mid-way will be
flattered by its own early days. State the method next to the number, always.

## Meta Ads

```
ads_get_ad_entities
  ad_account_id  <from config, never guessed>
  level          ad_account
  date_preset    last_14d
  time_increment "1"
  fields         amount_spent, purchase_roas, cost_per_purchase, purchases, impressions
```

> **The connector renames your fields.** You ask for `cost_per_purchase` and `purchases`;
> it returns `cost_per_omni_purchase` and `omni_purchase`. Read the names that come back
> rather than the ones you sent, or every value reads as missing.

> **Null is not missing, it is zero.** A day with spend and no sales returns
> `purchase_roas: null` and `omni_purchase: null`. Rendered naively this prints "null" or
> breaks the arithmetic. It is a real zero-purchase day and usually the most important
> thing in the section.

> **Members have dozens of accounts.** One real list ran to thirty, across different
> brands and currencies. The account comes from config. Never pick one.

## Gmail

### Customer service

```
search_threads  query: in:inbox is:unread newer_than:2d -in:draft
```

> **Most unread mail is not a customer.** In one real check, all six unread threads were
> an app newsletter, a survey notification, two out-of-office auto-replies, a Judge.me
> notification, and the brand's own campaign showing up because it carried both SENT and
> INBOX labels. Reported raw, that is "6 emails waiting" every morning and the brief
> loses its credibility inside a week.
>
> Filter out: known notification senders, anything whose labels include SENT, automatic
> replies, and bulk or marketing mail. Report **needs a reply** and **filtered as noise**
> as separate numbers so the filtering is visible and checkable.

### Reviews, without a reviews connector

```
search_threads  query: from:support@judge.me newer_than:2d
```

Judge.me emails a notification per review, and the subject parses cleanly:

```
<Name> left a <N> star review for '<Product>'
```

Rating and product come straight from the subject, the text from the snippet. This is why
the brief needs no separate reviews integration, which matters for portability: any store
running Judge.me gets this for free.
