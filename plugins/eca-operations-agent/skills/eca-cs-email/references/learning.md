# Learning which replies can be trusted

The point of this skill is not to draft the same email forever. It is to notice that a
question keeps coming back, that the same answer keeps being approved unchanged, and to
ask whether it should just handle that one from now on.

**It proposes. The member decides. It never promotes itself.**

## The log

`learned-replies.md` lives in the `cs-email/` folder in the member's working directory,
beside `config.md` and accumulates one
block per query type. It is the skill's memory between runs.

```markdown
## where-is-my-order
- **Seen**: 12
- **Last seen**: 2026-10-08
- **Status**: DRAFT
- **Answerable from**: Shopify order + fulfilment state
- **Approved unchanged**: 9 of 12
- **What the member changed**: twice added an apology when the order was over 5 days old
- **Pattern**: confirm the order number, give the ship date and tracking link from
  Shopify, apologise only if it is genuinely late
```

## How it knows a draft was good

This is the part that makes the counting mean something.

The skill saves its reply as a draft on the thread and logs it in
`cs-email/open-drafts.md`. On the next run it reconciles that log against `list_drafts`: a
line that has vanished means the draft was sent or discarded, and the thread shows which.
Without the log a run cannot do this at all, because it has no memory of what it wrote.

- **Sent unchanged** → the draft was right. Count it.
- **Sent with edits** → record *what* changed, not just that something did. The edit is
  the correction, and it is worth more than the count.
- **Not sent, thread still open** → the member has not got to it. Do not count it either way.
- **Replaced entirely** → the draft was wrong. Reset that category's unchanged run to zero
  and note why if it can be worked out.

Never count a draft as approved because it was not complained about.

## When a category becomes a candidate

All four, every time:

1. **Seen at least 5 times.** Three is a coincidence.
2. **The last 3 were sent with no material edit.** Wording tweaks do not count as material;
   a changed fact, promise, or tone does.
3. **It is answerable entirely from data the skill can verify** — an order record, a
   fulfilment status, a published policy. Not from judgement, memory or goodwill.
4. **It is not on the never-automate list below.**

Then, and only then, ask:

> "You have approved the same reply to *where is my order* five times now without
> changing it, and every one was answerable straight from the order record. Want me to
> start sending those automatically? I will keep drafting anything that is late,
> complicated, or from someone who has written before."

If the member says no, record that and stop asking. One ask per category.

## Never automate

No count makes these safe, because the cost of being wrong is not symmetrical:

- Refunds, returns, discounts, credits, or anything else involving money
- Complaints, or any message with a note of anger or disappointment in it
- A promise about a date the skill cannot verify
- Anything about an allergy, a health claim, or a safety question
- Wholesale terms, creator agreements, press
- A first message from someone who has never written before
- Anything where the right answer depends on what the member wants to do

## Once a category is automatic

Keep it honest:

- **Still log every send**, and show them in the next run's summary, so automatic never
  means invisible.
- **Fall back to a draft** whenever the specific case is unusual: the order is late, the
  customer has written more than once, the message carries a second question, or the
  tone is off.
- **Demote on any signal it got it wrong** — the customer replies again unhappy, or the
  member corrects it. Drop straight back to drafting, tell the member it happened, and
  do not re-propose for at least ten more sightings.

A category that has been demoted twice should stay manual. Something about it is harder
than it looks.
