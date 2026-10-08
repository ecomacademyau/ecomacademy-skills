# ECA Morning Brief

One page each morning that tells you what happened to your store yesterday, what it
means, and what needs doing, with a button on each action that hands the job to Claude.

## What it reads

- **Shopify** — yesterday's sales against the same weekday last week, what sold, orders
  waiting to dispatch, weeks of stock cover, and a month-end forecast
- **Meta Ads** — spend, return and cost per purchase, and any day that spent without selling
- **Gmail** — customer email genuinely waiting, and new Judge.me reviews

Shopify is required. Meta Ads and Gmail are optional, and the brief names whatever it
could not check rather than quietly leaving it out.

## What makes it worth opening

It leads with a written headline, not a label. "Both the store and the ad account broke
on 3 October, and neither has recovered" tells you something. "Store performance update"
does not.

It only lists what you can act on. A morning with nothing wrong says so in one line and
gets out of the way.

Every action carries a button that opens a new Claude conversation with the whole job
already written into it, routed to the skill that owns that work where one is installed,
and carrying a full method where one is not.

## Setup

Run it once. It checks your connectors by actually calling them, asks which ad account to
use, confirms your timezone, sets your thresholds, asks how you want Slack handled, and
offers to schedule itself. After that it runs on its own.

## Reusing it for another store

Nothing brand-specific is hardcoded. Copy the folder, delete `config.md`, run it again.
