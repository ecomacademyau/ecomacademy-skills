---
name: eca-morning-brief
description: "Produce a daily morning brief for a Shopify store: what happened yesterday, what it means, and what needs doing today, published as an ECA-styled artifact with a button on each action that hands the job to Claude. Reads Shopify for sales, orders, dispatch, stock cover and a month-end forecast, Meta Ads for spend and return, and Gmail for customer service and new product reviews, then compares yesterday against the same weekday last week and writes a plain-language headline. Use whenever someone wants a morning brief, a daily store summary, a daily check of sales, ads, orders or inbox, an overview of what needs attention today, or asks to set up a recurring briefing. Can post to Slack. Requires Shopify connected; Meta Ads and Gmail are optional and the brief names whatever it could not check."
---

# Morning Brief

One page each morning that says what happened to the store yesterday, what it means, and
what needs doing about it, with a button on each action that hands the job to Claude.

It reads Shopify, Meta Ads and the inbox, writes a headline that states the finding in
plain words, and publishes an ECA-styled brief as a dated artifact. Optionally posts to
Slack.

**The brief exists to be acted on, not admired.** If a morning produces no actions, it
says so in one line and gets out of the way. A brief that invents three things to worry
about every day trains the reader to stop opening it.

## Setup, on the first run only

Setup writes `config.md` beside this skill. Once it exists, every later run reads it and
goes straight to work.

### 1. Check the connectors, by calling them

**Do not infer a connector works because its tools appear in the tool list.** A listed
tool is not an authenticated connection. Make a cheap real call and look at what comes
back.

| Connector | Test call | What it feeds |
|---|---|---|
| **Shopify** | `get-shop-info` | Sales, orders, dispatch, stock, the forecast |
| **Meta Ads** | `ads_get_ad_accounts` | Spend, ROAS, cost per purchase |
| **Gmail** | `search_threads` on one recent query | Customer service, and reviews via Judge.me notifications |

**Shopify is required. Without it there is no brief**, because every section except ads
depends on it. If it fails, say so plainly, help the member connect it, and stop. Do not
produce a brief of ad data alone and call it a morning brief.

**Meta Ads and Gmail are per-section.** If either is missing, offer to continue without
it and name exactly what the member loses. Record the choice in config so the daily run
does not re-ask every morning.

### 2. Settle the configuration

Ask only what cannot be discovered:

- **Which ad account.** List them with `ads_get_ad_accounts` and have the member pick.
  **Never guess.** Agencies and consultants routinely have dozens, and a brief reporting
  the wrong store's spend is worse than one reporting none.
- **The store timezone**, from `get-shop-info`. Confirm it rather than asking.
- **What time the brief should run.** Default 7am local.
- **Slack**: off, draft-and-ask, or post automatically to a named channel. Ask which;
  do not assume. If automatic, get the channel and say plainly that an unreviewed brief
  will go to everyone in it.
- **Thresholds**, offered with defaults rather than asked cold: stock cover under 4
  weeks, dispatch backlog older than 48 hours, a day-on-day change worth mentioning at
  5%, a review at 3 stars or under.

### 3. Offer the schedule

Create the recurring task with `create_scheduled_task` at the agreed time. Say that
scheduled tasks run while the app is open, and one that comes due while it is closed
runs at next launch.

## The daily run

### 1. Establish the window

Yesterday in the store's timezone, compared against **the same weekday last week**.

**Exclude today, always.** A partial day compared against a complete one reads as a
collapse, every single morning. This is the most common way a brief like this becomes
nonsense.

### 2. Gather

Follow `references/data-sources.md`, which holds the verified queries and the traps for
each source. In short: 15 days of daily Shopify sales, yesterday's product mix, unfulfilled
orders, 28-day inventory velocity, month-to-date for the forecast, 14 days of Meta daily
metrics, and the inbox.

Anything that fails, record in `unavailable` with a reason. **Never silently omit a
source.** A missing section the member does not know about is worse than a missing
section they do.

### 3. Decide what actually needs them

This is the judgement, and it is the whole value. Candidates:

- A metric that moved more than the threshold against the same weekday last week
- Ad spend with no return, or a day that bought nothing
- Orders past the dispatch threshold
- Stock under the cover threshold
- Customer email genuinely waiting, after noise filtering
- A review at or under the low-rating threshold

**Then cut the list.** Rank by what costs the most to ignore, keep what a person could
actually do something about today, and drop the rest. Three or four is a good morning.
More than six means the filter is not working.

**If nothing qualifies, say so.** "Nothing needs you this morning" is a valid and useful
brief.

### 4. Write the headline

One sentence naming what happened and what it means. Not a label.

- Good: "Both the store and the ad account broke on 3 October, and neither has recovered."
- Useless: "Store performance update for 8 October."

Then two or three sentences carrying the specific numbers, including the one that
complicates the story. A headline that only reports the good or the bad is not a report.

### 5. Write the action prompts

Each action gets a button that opens a new Claude conversation. Follow
`references/skill-routing.md`: name the skill that owns the job, give a real fallback
method for members who do not have it, hand over the findings marked as a starting point
to re-derive, carry the traps for that data source, say what is owed to whom, and name
the deliverable.

### 6. Build and publish

```bash
python3 scripts/build_brief.py findings.json --out brief.html
```

Publish with `create_artifact`, id `morning-brief-<YYYY-MM-DD>`, so each day is its own
readable page. Save the HTML alongside it for the record.

### 7. Slack, per config

Off: skip silently. Draft-and-ask: show the brief, then ask before posting. Automatic:
post to the configured channel and say that it went.

## Checks before finishing

- Today's partial day is excluded from every comparison.
- Every number that appears twice is the same number both times. Compute once, reuse.
- Every modelled figure is labelled as a projection with its method stated.
- Every unavailable source is named, with what it would have told them.
- Every action is something the member could act on today.
- Every button prompt names its skill and still works without it.
- The headline states a finding, not a category.

## Rules

- **Check connectors by calling them.** A tool in the list is not a working connection.
- **Never guess the ad account.** Members have dozens.
- **Exclude today.** Always.
- **Filter the inbox before counting it.** Newsletters, auto-replies, notification
  services and the brand's own sent mail are not customers waiting. An unfiltered unread
  count reports work that does not exist, and the brief loses its credibility in a week.
- **Exclude $0 and very old orders from the dispatch backlog.** A forgotten test order
  makes "oldest unfulfilled" meaningless forever.
- **Label projections as projections**, with the method beside them.
- **Say what you could not check**, every time, without being asked.
- **No invented urgency.** If the quiet day is just a quiet day, say that.

## Reference files

- `references/data-sources.md` — the verified queries per source, and the traps in each
- `references/skill-routing.md` — which skill owns which action, and the fallback rule
- `references/brief-data-format.md` — the findings JSON the generator expects
- `scripts/build_brief.py` — renders the ECA-styled HTML
- `config.md` — written at setup; the ad account, timezone, thresholds and Slack choice
