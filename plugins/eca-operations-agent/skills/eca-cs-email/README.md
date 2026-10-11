# ECA Customer Service Email

Works your support inbox: finds what is genuinely waiting, oldest first, checks the real
order in Shopify, and writes replies in your voice as Gmail drafts.

## It opens with a brief

Before a single reply gets written, it tells you what the store can honestly promise
today. It measures the real dispatch time from what actually shipped, not from your
policy page, and compares the two:

> "The promise is currently false. The site says 1 to 2 business days. Nothing has
> shipped for 4 days and the oldest unfulfilled order is 94 hours old."

That matters because every reply you write this morning contains a promise. Without it
you send a dozen "ships in 1-2 days" replies that are each a complaint in advance.

It also lists the customers whose orders are overdue **who have not written in yet**, and
offers to apologise first. An apology that arrives before the complaint is worth far more
than a good reply afterwards.

It reads sentiment first, from counted signals rather than a feel for the text: review
ratings, people writing twice, escalation words, the complaint share. Under five signals
it says so and calls no trend, because manufacturing a mood from two emails is how a
section like that gets skimmed past.

The brief renders in ECA styling, with the promise verdict given the only real visual
weight on the page and order numbers linking straight into Shopify admin.

Written for whoever works the inbox, who is often not the owner and has not read any
other report.

## Why oldest first

The emails that damage a brand are not this morning's. They are the ones that quietly
slipped and have been sitting for a fortnight. This leads with the longest wait, every
time, and flags anything past your threshold.

## Why it does not count unread

Unread is the wrong test. Someone can read an email and not answer it, and most unread
mail in a store inbox is newsletters, auto-replies and notifications anyway. This looks
at who spoke last in the thread. If it was the customer, it is waiting.

It also reports what it filtered, so you can see when the filter is wrong.

## It learns

Every reply it drafts gets logged. On the next run it checks what you actually sent
against what it wrote. Sent unchanged means the draft was right. Edited means it records
what you changed, which is worth more than the count.

When a question has come up five times and your last three replies went out unchanged,
and the answer comes straight from the order record rather than judgement, it asks:

> "Want me to start sending those automatically?"

You decide. It never promotes itself, it keeps logging everything it sends, and it drops
straight back to drafting if a case looks unusual or it gets one wrong.

Money, complaints, health questions and anything it cannot verify are never automated, no
matter how many times they come up.

## It learns your store's answers too

Setup reads your own website — shipping policy, returns policy, FAQ, product pages — and
builds an answer book of what your customers actually get told. Every fact carries the
page it came from and the date it was read.

Then it walks you through it, because these are the facts it will state to a customer.
It asks the ones that cost money to get wrong: the return window, who pays return
postage, the dispatch cut-off, anything about allergens. And it asks the question your
policy page cannot answer, which is whether the published policy is the one you actually
honour. Plenty of stores publish 30 days and quietly accept 60.

Nothing unverified is ever stated to a customer. It gets flagged instead.

It re-reads your policy pages every 90 days, and if you correct a draft on a point of
policy, your correction beats the website.

## Checking in during the day

Just ask, in any chat. The state lives in files rather than in a conversation, so a fresh
chat knows what this morning's scheduled run did. You never have to hunt for the
conversation where it was set up.

That is also where sending happens. A scheduled run has nobody there to approve anything,
so it drafts and stops. When you check in, it shows you what is waiting, you approve, and
it sends. The schedule prepares the work; you release it.

Ask twice in an afternoon and the second answer is a sentence, not a repeat.

## Mail providers

Built and tested against **Gmail**. The logic is provider-agnostic — the test is who sent
the last message in a thread — but Gmail is the verified path.

Another provider works if it can search with a date filter, return a thread's messages
with senders and timestamps, read a body, and **create a draft on an existing thread**.
That last one is where most fall short. Superhuman Mail covers Gmail and Outlook and can
draft. The Microsoft 365 connector can search Outlook but cannot create drafts, so it can
triage but not draft.

## Setup

Run it once. It checks your connectors by calling them, builds the answer book from your
site, asks which mailbox and who replies sign off as, which categories your store gets,
and your late threshold.

## Reusing it for another store

Nothing is hardcoded. Copy the folder, delete `config.md`, `brand-answers.md` and
`learned-replies.md`, and run it again against the new store's URL.
