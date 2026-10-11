# The customer service brief

Opens every run. Two halves: **what the store can honestly promise today**, then **who is
waiting on a reply**.

The first half is not a dashboard. It exists because every reply written this morning
contains a promise, and the person writing them needs to know whether that promise is
currently true. A store whose policy says "ships in 1 to 2 days" and is in fact four days
behind will otherwise send twelve replies that are each a complaint in advance.

**This brief is for whoever works the inbox**, who is often not the owner. Assume they
have not seen any other report and do not know the store was behind.

## First run of the day, or a later one

**The first run gets the full brief. Later runs the same day get what changed.**

Work out which this is: look for `cs-email/cs-brief-<today>.html`. If it is there, this is
a later run.

At 2pm, sentiment has not moved since 9am, the housekeeping line is word for word the same,
and a second near-identical page is how a reader learns to skim the one that matters. The
news in the afternoon is the delta.

### A later run reports

- **What moved**: orders dispatched since the last run, new orders in, emails answered,
  new emails arrived.
- **Anything that crossed a threshold**: an order passing 72 hours, a first complaint, a
  review under the bar. Crossing a line is news; sitting the same side of it is not.
- **Drafts still waiting**, from `cs-email/open-drafts.md`, with how long. A draft written
  at 9am and untouched at 2pm is the most actionable line on an afternoon brief.
- **The promise, only if its verdict changed.** Otherwise one line: "still false, 4 days."

**If the promise verdict flipped, that gets full prominence again**, either way. A batch
going out and the promise coming back true is the best news the inbox can get, and whoever
is replying needs to know within minutes, because it changes every reply they write.

**If nothing material changed, say so in two lines and stop.** "Since 9am: 2 new orders, no
dispatches, nothing crossed a threshold. The 4 drafts from this morning are still
unsent." That is a complete afternoon brief.

### Update, do not republish

Update the same day's artifact rather than publishing a second one, and keep the single
saved file per day at `cs-email/cs-brief-<date>.html`. One page per day that gets more
accurate, not three pages competing to be the current one.

## The sentiment read, first

**Full runs only.** One line at the very top saying how customers are feeling, and what is
driving it. It
goes first because it changes how everything below gets written. Replying to a souring
inbox in a breezy tone is worse than replying slowly.

### Measure it, do not sense it

Count real signals, never an impression of the text:

| Signal | Where from | What it means |
|---|---|---|
| Review ratings since the last run | the reviews notifications | the clearest single number |
| Repeat contacts | someone writing twice on one thread with no reply between | patience running out |
| Escalation language | "still waiting", "second time", "no response", "refund", "disappointed", "cancel" | counted, not interpreted |
| Complaint share | `complaint` and `returns-refunds` as a share of the queue | the shape of the week |
| Public threat | "leave a review", "chargeback", "report" | always escalate, never automate |

### Volume gate, or it is noise

**Under 5 signals, do not call a trend.** Say the number and stop:

> "Three emails waiting and one new review. Too little to read anything into."

That is a complete and honest sentiment line. Manufacturing a mood from two emails is how
this section becomes something people skim past.

With enough volume, give the read and what is behind it:

> "Souring. Four of nine waiting emails mention the wait, two people have written twice,
> and the only review since Friday was 2 stars about delivery. All of it traces to
> dispatch, not the product."

### Always name the cause

Sentiment with no cause is a mood ring. The useful version ties feeling to a fact the
member can act on, and most of the time that fact is already in the dispatch section
below. When tone is souring and dispatch has stopped, say they are the same story.

If sentiment is poor and dispatch is **fine**, that is a different and more interesting
finding. Say so plainly, because it points at the product, a recent change, or an
expectation the marketing set that operations cannot meet.

### Compare to the baseline, not to zero

Some inboxes are always a bit grumpy. What matters is whether this morning is worse than
this store's normal. Keep a rolling note of the last few runs' readings in
`cs-email/learned-replies.md` under `_sentiment` and compare against it. Without a
baseline, say "no baseline yet" rather than implying one.

## Half one: what you can promise today

### The real dispatch time, measured not stated

Work it out from what actually happened, never from the policy page.

```sql
FROM fulfillments SHOW orders_fulfilled, orders_shipped
TIMESERIES day SINCE <14 days ago> UNTIL <yesterday>
```

```
list-orders  query: fulfillment_status:unfulfilled AND financial_status:paid
```

From those: the median hours from order to dispatch over the last 14 days, how many are
waiting now, the age of the oldest, and whether anything has shipped at all in the last
48 hours.

**A run of zero-fulfilment days is the headline.** Dispatch stopping is not a slow week,
it is a thing that has happened and nobody has said. Lead with it.

### Then the line that matters most

Compare the measured time against the promise in `brand-answers.md`.

> **The promise is currently false.** The site says orders ship within 1 to 2 business
> days. Nothing has shipped for 4 days and the oldest unfulfilled order is 94 hours old.
> Do not tell anyone their order ships in 1 to 2 days today.

Say it in those terms. Not "dispatch is running slightly behind", which is how someone
reads past it and writes the wrong reply anyway. If the promise still holds, say that too,
in one line, because it is what lets the responder write confidently.

### Who is about to complain

List the customers whose orders are past the promised window **and who have not written
in yet**. This is the most valuable thing in the brief, because an apology that arrives
before the complaint is worth far more than a good reply afterwards.

For each: order number, customer name, hours waiting, value, and an admin link. Offer to
draft a proactive note. Getting ahead of six people beats answering six angry emails.

### Exclude what is not a real order

Stores accumulate $0.00 rows in the unfulfilled queue: review seeding, influencer
gifting, test orders. They inflate the backlog and are a different job entirely.

Exclude anything at $0.00, and anything older than 90 days, from every figure. Then name
them in one line so they are not invisible: *"3 zero-value orders from 8 October, likely
review seeding, and a test order from 2024 that has been open 732 days."*

### Stock, only where it changes an answer

If something in the unfulfilled queue is out of stock, those orders are not late, they
are blocked, and the reply is completely different. Check only the products that appear
in waiting orders. Do not survey the catalogue; that is the stock skill's job.

## Half two: who is waiting on a reply

The inbox queue per `references/finding-what-needs-a-reply.md`: threads whose last
message is not from the store, oldest first, noise filtered and counted separately.

Cross-reference the two halves. **A waiting email from someone whose order is also
overdue is the top of the list**, every time. They are not asking a question, they are
about to lose patience, and the reply needs the dispatch context the first half just
established.

## Rendering it

```bash
python3 scripts/build_cs_brief.py findings.json --out cs-email/cs-brief-<date>.html
```

The data shape is in `references/cs-brief-data-format.md`. Publish it as an artifact so
the member can open it from the sidebar, and save the HTML into the `cs-email/` folder for
the record.

**The promise verdict is the only thing on the page with real visual weight.** It is the
one line that changes every reply written today, so it gets the banner and everything else
stays dense. Sentiment is a single line rather than a card, because when the volume gate
fires it is one sentence and should not take up a quarter of the screen.

**Use one age format for the whole page.** An earlier build switched from hours to days at
48 hours, so the same order read as "92 hrs" in the stat row and "3.8 days" in the table.
The generator now handles this; do not hand-write an age into a label or a note and
reintroduce it.

If the generator is unavailable for any reason, the plain-text shape below is a perfectly
good fallback. Say which one the member is getting.

## Shape of the brief, in plain text

Keep it short enough to read before starting work. Something like:

```
SENTIMENT           Souring, and it traces to dispatch rather than the product.
DISPATCH            Nothing shipped for 4 days. 24 orders waiting, $1,556, oldest 94 hrs.
THE PROMISE         Currently false. Site says 1-2 days, reality is 4+.
LIKELY TO COMPLAIN  6 orders past 72 hrs, none have written yet.
INBOX               4 waiting a reply, oldest 6 days. 11 filtered as noise.
OVERLAP             1 person is both waiting on a reply and overdue: #1042, J. Smith.
HOUSEKEEPING        3 zero-value orders, 1 test order from 2024.
```

Then the queue itself, oldest first, and get to work.

**No chart, no styling.** This is a working list someone acts on in the next ten minutes,
not a report they file. The morning brief is where the store gets presented; this is
where it gets handled.

## If dispatch is fine

Say so in one line and move to the inbox. A brief that manufactures concern every morning
gets skimmed, and then missed on the morning it matters.
