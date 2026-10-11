---
name: eca-cs-email
description: "Open with a customer service brief, then work the inbox. The brief measures the store's real dispatch time from what actually shipped, says plainly whether the published shipping promise is currently true, and lists the customers about to complain before they write in. Then it finds every message genuinely waiting on a reply, oldest first, looks up the real order in Shopify with a clickable admin link, and drafts a reply in the brand's voice signed by whoever the member chose. Covers order status, shipping, products, returns, refunds, complaints, wholesale, creator collabs and press. Learns which replies can be trusted and asks before handling any of them alone. Use for inbox triage, answering or drafting customer emails, who has been waiting longest, or a daily support check. Nothing is sent without permission. Needs a mail connector and Shopify."
---

# Customer Service Email

Works the inbox: finds every message actually waiting on a reply, sorts it by how long it
has been waiting, looks up the real order in Shopify, and writes a reply in the brand's
voice as a Gmail draft.

It keeps a log of what it has handled. When the same question keeps coming back and the
same answer keeps being sent unchanged, it asks whether it should start handling that one
by itself. **It proposes. The member decides. It never promotes itself.**

**Nothing is ever sent without permission** — either the member's approval on the day, or
their explicit sign-off that a specific category can go automatically.

## Step 0 — The gate. Every run. Before anything else.

**Do not read the inbox until this passes.** Not to "have a quick look", not to see what
is waiting while setup is discussed. A triage pass before the answer book exists produces
confident replies built on nothing, and that is worse than no reply at all.

Check all four, in order, and stop at the first failure:

| Check | How | If it fails |
|---|---|---|
| 1. Mail connector works | one small search call | **Stop.** Help them connect it. There is no skill without a mailbox. |
| 2. Shopify works | `get-shop-info` | **Stop.** Help them connect it. See below. |
| 3. `cs-email/config.md` exists | read it | **Stop and run setup.** |
| 4. `cs-email/brand-answers.md` exists **and has verified entries** | read it, count entries marked verified | **Stop and finish setup.** |

**Shopify is required, not optional.** Most customer service email is about an order:
where is it, when does it ship, can I change it, I want to send it back. Without the
order record every one of those becomes "let me check and get back to you", which is
exactly the reply the member is trying to stop writing. Do not offer to proceed without
it.

**An answer book with no verified entries means setup did not finish.** The file existing
is not the test. If every entry still reads "not yet", go back and verify them with the
member before touching the inbox.

When a check fails, say plainly which one and what it blocks, then do that instead. Do
not report on the inbox as a consolation.

## Setup — run when the gate fails, not "on the first run"

The gate above decides when this runs. Treat it as the thing that happens whenever the
store is not ready, which includes a member who abandoned setup halfway the first time.


Writes its files into a **`cs-email/` folder in the member's working directory**, not
beside the skill. An installed skill lives in a read-only cache and cannot be written to,
so anything saved there is lost or fails outright.

```
cs-email/
  config.md            mailbox, signature, categories, thresholds, noise list
  brand-answers.md     the store's verified answers, read before every draft
  learned-replies.md   what has been handled, and what can be trusted to run alone
```

Create the folder if it is not there. Later runs read all three and go to work.

### Check the connectors by calling them

A tool in the tool list is not an authenticated connection. Make a real call.

| Connector | Test call | Without it |
|---|---|---|
| **A mail connector** | one small search | No skill. Stop and help them connect one. |
| **Shopify** | `get-shop-info` | No skill. Most support email is about an order. Stop and help them connect it. |

**On mail providers.** This skill is built and tested against the **Gmail** connector.
The logic itself is provider-agnostic, because the triage test is "who sent the last
message in this thread", which every mail system can answer. But only Gmail has been
verified end to end.

A different provider works if it can do four things: search a mailbox with a date filter,
return the messages in a thread with sender and timestamp, read a message body, and
**create a draft on an existing thread**. That last one is where most fall short.
Superhuman Mail covers Gmail and Outlook and does have draft creation. The Microsoft 365
connector can search Outlook but exposes no way to create a draft, so it can triage and
summarise but not draft.

If the member's provider cannot create drafts, say so at setup and offer to write the
replies into the chat for copying instead. Do not pretend the workflow is the same.

### Build the answer book

Most support email is the same dozen questions, and the skill cannot answer any of them
until it knows **this store's** answers.

Follow `references/building-brand-answers.md`: read the brand's own policy, FAQ, contact
and product pages, record each fact with its source URL and the date it was read, then
**walk the member through it and have them verify**.

Ask directly about the ones that cost money to get wrong: the return window, who pays
return postage, the dispatch cut-off, anything about allergens. And ask the question the
page cannot answer, which is whether the published policy is the one they actually
honour. Plenty of stores publish 30 days and quietly accept 60. The skill should state
what the member really does.

**A fact that has never been verified is never stated to a customer.** Summarise and flag
it instead.

If `eca-brand-intelligence` is installed, read `brand-data.md` first and only crawl for
the gaps. Do not rebuild what another skill already established with the member.

### Settle the configuration

- **The mailbox** this skill works.

- **Who the replies come from.** Ask it directly, do not infer it from the mailbox name:

  > "Who should these replies come from? A name the customer sees, and how you normally
  > sign off."

  Capture the name, any title or role, and the exact sign-off wording. Some stores sign
  with a person, some with a team, and the difference matters: a first name and "the
  support team" set completely different expectations about who is reading.

  **Ask whether it varies by category.** It often does. Order and shipping questions go
  out from the team; a complaint or a wholesale enquiry comes from the founder, because
  the customer should feel they reached someone who can decide. Record one default and
  any per-category exceptions.

  **Never invent a person.** If the member has not named someone, sign as the brand. A
  reply from a name that does not exist is found out the moment a customer asks for them
  by name, and it is the kind of thing a customer tells other people about.

  If the mailbox has history, show the member how past replies were actually signed and
  confirm that is still right, rather than asking them to recall it.
- **Which categories matter** to this store, from `references/categories.md`.
- **The waiting threshold** that counts as late. Default 48 hours.
- **The noise list** — notification senders to exclude. Start with the defaults and add
  to it whenever something slips through.
- **How often it should run.** Customer service is not a once-a-day job the way a
  morning brief is: a reply sitting from 9am until tomorrow is most of a day lost. Offer
  a cadence rather than asking cold.

  | Pattern | Cron | Suits |
  |---|---|---|
  | Twice each weekday | `0 9,14 * * 1-5` | Most stores. Morning sweep, afternoon catch-up. |
  | Weekday mornings | `0 9 * * 1-5` | Low volume, or one person handling it around other work. |
  | Three times daily | `0 8,12,16 * * *` | High volume, or a store promising same-day replies. |
  | On demand only | no schedule | Someone already lives in the inbox and wants help, not a routine. |

  Create it with `create_scheduled_task`. Say plainly that scheduled tasks run while the
  app is open, and one that falls due while it is closed runs at next launch.

- **Wholesale terms and shipping policy**, if the store answers those by email. Without
  them, those categories can only be summarised, not drafted.

## Attended and unattended runs are different

**Every scheduled run is a brand-new session with no memory of any previous one.** It does
not continue the conversation that set it up, or the one before it. Nothing carries across
except what is written down.

That changes what a run can do, so work out which kind this is before step 1. If a person
asked for this right now, it is **attended**. If it fired on a schedule, it is
**unattended** and nobody is there to approve anything.

| | Attended | Unattended |
|---|---|---|
| Build the brief | yes | yes |
| Show the queue before drafting | yes, and wait | no, skip and draft |
| Draft into the mailbox | yes | yes, nothing sends |
| Send an approved reply | yes, on explicit approval | never, except an `AUTO` category |
| Propose promoting a category | yes | no, hold it for the next attended run |
| Report | in the conversation | as the task notification |

An ad-hoc check during the day is **attended**, which is what makes it the moment to
approve and send what the scheduled runs have drafted.

**Never wait for approval that cannot come.** An unattended run that stops and asks has
achieved nothing, and the member finds a half-finished job hours later. Draft
conservatively instead, and leave the decisions in the report.

**Never promote a category unattended.** The promotion question is the member handing over
trust, and it is asked in a conversation where they can push back, not in a notification
they skim.

### What carries between sessions

The memory is on disk and in the mailbox, not in context:

- **Drafts in the mailbox**, reconciled against `cs-email/open-drafts.md`, which is how a
  run tells its own drafts from the member's
- **`cs-email/learned-replies.md`**, counts, patterns and statuses
- **`cs-email/brand-answers.md`**, the verified facts
- **`cs-email/config.md`**, every setup decision

Read all of them at the start of every run. A run that skips them starts from nothing and
re-learns what the store already knew.

### Do not draft the same thread twice

With two or three runs a day this happens unless it is checked for, and two drafts on one
thread means someone sends the wrong one.

**Keep a log of what was drafted**, in `cs-email/open-drafts.md`. A run has no memory, so
without this it cannot tell its own draft from one the member wrote, or a draft left alone
from one that has been edited. Record one line per draft at the moment it is created:

```
| thread_id | draft_id | written (ISO) | category | first 80 chars of the body |
```

**At the start of every run**, call `list_drafts` and reconcile:

| What you see | What it means | Do |
|---|---|---|
| Draft on the thread, not in the log | The member wrote it | Leave it alone entirely |
| In the log, `date` unchanged, still unsent | Yours, untouched | Leave it. Report it as still waiting, with how long |
| In the log, `date` has moved | The member edited it, they are working on it | Leave it. Drop that category's unchanged run to zero |
| In the log, customer's last message is newer than the draft | Stale, they wrote again | Replace it, and say so in the report |
| In the log, no longer in `list_drafts` | Sent or discarded | Check the thread for a sent message, then feed it to the learning step and clear the line |

The `date` comparison is how an edit is detected: Gmail restamps a draft when it is saved.
**If a draft's date is ambiguous, read the body and compare it against the logged opening
rather than guessing.** Treat anything you cannot resolve as the member's, and leave it.

Clear lines from the log once a draft is sent or gone, or the file grows forever.

## Checking in during the day

Someone asking "check the emails" at 11am is a normal and frequent way to use this. It
needs no setup and no particular conversation.

**Any chat works.** The state lives in `cs-email/`, not in conversation history, so a check
in a brand-new chat knows exactly what the 9am scheduled run did. The member does not have
to find the chat where it was set up, and there is no "wrong" place to ask.

**This is where sending happens.** A scheduled run has nobody present, so it drafts and
stops. An ad-hoc check is attended, which makes it the moment to show what is sitting in
`cs-email/open-drafts.md`, take approval, and send what they approve. That is the natural
rhythm: the schedule prepares the work, the person checking in releases it.

If the member only wants that, do only that. "Anything to approve?" is not a request for
another brief.

**Give the delta, not the brief.** Same rule as a later scheduled run: what changed, what
crossed a threshold, what is still unsent. The full brief was this morning.

**Get terser each time.** A third check in one afternoon should be a sentence. "Nothing
new since 2pm, the two drafts are still unsent." Repeating a paragraph that has not changed
is how a useful habit becomes background noise.

**Only re-brief in full if they ask**, or if the promise verdict has flipped since the
morning, which changes every reply they are about to write.

## Each run

**Step 0 has passed by the time you are here.** If it has not, go back. Nothing below is
safe to do against an unconfigured store.

### 1. The CS brief

Follow `references/cs-brief.md`.

**First run of the day or a later one?** Check for `cs-email/cs-brief-<today>.html`. The
first run of the day gets the full brief. A later run gets **what changed since the last
one**: orders dispatched, new orders, emails answered or arrived, anything that crossed a
threshold, and the drafts still sitting unsent. At 2pm the sentiment has not moved and the
housekeeping is identical, so repeating them trains the reader to skim.

**If the promise verdict flipped, that gets full prominence again**, either way. A batch
going out and the promise coming back true changes every reply written that afternoon.

If nothing material changed, two lines and stop. Update the same day's artifact rather
than publishing a second.

A full run is a sentiment line, then two halves.

**Sentiment first**, because it changes how everything else gets written. Replying to a
souring inbox in a breezy tone is worse than replying slowly. Count real signals — review
ratings, people writing twice, escalation language, the complaint share — and **under five
signals do not call a trend**. "Three emails and one review, too little to read anything
into" is a complete and honest answer. Always name the cause, because sentiment with no
cause is a mood ring, and if tone is poor while dispatch is fine, say so: that points at
the product or at a promise marketing made that operations cannot keep.

**What the store can promise today.** Every reply written this morning contains a
promise, and the person writing them needs to know whether it is currently true. Measure
the real dispatch time from what actually shipped, never from the policy page, then
compare it against the promised window in `brand-answers.md` and say plainly which way it
falls:

> "The promise is currently false. The site says 1 to 2 business days. Nothing has
> shipped for 4 days and the oldest unfulfilled order is 94 hours old. Do not tell anyone
> their order ships in 1 to 2 days today."

**A run of zero-fulfilment days is the headline**, not a footnote. Dispatch stopping is a
thing that has happened and nobody has said out loud.

Then list **who is about to complain** — orders past the window whose customers have not
written in yet. An apology that lands before the complaint is worth far more than a good
reply afterwards. Offer to draft those proactively.

Exclude $0.00 rows and anything over 90 days from the figures, then name them in one line
so they are not invisible. They are review seeding, gifting and old tests, and they are a
different job.

**Assume the reader has seen nothing else.** Whoever works the inbox is often not the
owner and will not have read the morning brief.

If dispatch is fine, say so in one line and move on. A brief that manufactures concern
every morning gets skimmed, and then missed on the morning it matters.

**Render it.** Build the findings JSON per `references/cs-brief-data-format.md`, then:

```bash
python3 scripts/build_cs_brief.py findings.json --out cs-email/cs-brief-<date>.html
```

Publish it as an artifact so it opens from the sidebar, and keep the HTML in the
`cs-email/` folder. Order numbers link straight to Shopify admin, so the member can open
and act on one in a click. If the generator cannot run, fall back to the plain-text shape
in the reference and say that is what they are getting.

### 2. Find what is waiting

Follow `references/finding-what-needs-a-reply.md`.

**Unread is the wrong test.** A thread needs a reply when the last message in it came
from someone other than the store. Someone can read an email and not answer it, which is
exactly how a thread ends up waiting five weeks.

Filter the noise, then **report both numbers**: what is waiting, and what was filtered.
A single number hides a bad filter until it has eaten a real customer.

### 3. Sort oldest first

The ones that damage a brand are not this morning's, they are the ones that slipped.
Lead with the longest wait. Flag anything past the threshold.

**Cross-reference the brief.** Anyone waiting on a reply whose order is also overdue goes
to the very top. They are not asking a question, they are losing patience, and their
reply needs the dispatch reality from step 1 rather than the policy.

A thread that was apologised to once and then left again is worse than one nobody
answered at all. Say so.

### 4. Categorise

Per `references/categories.md`. Where a message does not fit, leave it `unclassified`
rather than forcing it. Where it fits two, the stricter handling wins.

### 5. Get the facts before writing

If a message touches an order, a product, shipping or a refund, look it up in Shopify
first. **Never state an order status from the customer's description of it.** They are
frequently wrong, and a confident wrong answer about someone's money is the worst thing
this skill can produce.

**Then link it.** Every order mentioned to the member gets a direct Shopify admin link,
so they can open it and act on it in one click rather than searching for an order they
were just told about. Follow `references/linking-to-shopify.md` — the store handle comes
from the myshopify domain, not the storefront domain, and the id is the tail of the gid.

The link goes in summaries, flags and the run report. **Never in the draft reply itself**,
where it exposes internal tooling and does not work for the customer anyway.

### 6. Show the member before drafting

**Attended runs only.** A short list: who is waiting, how long, what they want, which need
a person rather than a reply. Then stop. They may want to handle three of them personally,
and drafting those was wasted work.

On an unattended run, skip this and go straight to drafting, but draft more
conservatively: anything you would have flagged for a decision gets drafted with the
uncertainty stated plainly in the text, so the member sees the question when they open it.

### 7. Draft

Into the mail connector as a draft on the right thread, per the writing rules in
`references/categories.md`.

**Use the real dispatch time from step 1, not the published one**, whenever a reply
promises a date. The answer book holds the policy; the brief holds what is actually
happening. When they disagree, what is happening wins, and the reply should be honest
about it rather than repeating a promise the store is not currently keeping.

**Read `cs-email/brand-answers.md` before writing a word.** It holds the store's verified facts on
shipping, returns, products and policy, and it is the difference between a reply that
answers the question and one that says "let me check". If the answer is not in there and
not in Shopify, say so in the draft and flag it rather than inventing a policy.

Load the brand voice too — `eca-brand-intelligence` if installed, otherwise the last
several replies the member actually sent.

**Sign it as config says**, including any per-category exception. A complaint signed by
the team when the member said complaints come from the founder is the wrong reply, even
if every word above the sign-off is right.

Drafts, not sends. The member opens the mailbox, reads, adjusts, sends.

**Log every draft as you create it** into `cs-email/open-drafts.md`: thread id, draft id,
the draft's own date, the category, and the first 80 characters of the body. The next run
has no memory and cannot otherwise tell your draft from the member's, which is how a
thread ends up with two.

### 8. Learn from what happened last time

Follow `references/learning.md`. **Work from `cs-email/open-drafts.md`**: any line that has
disappeared from `list_drafts` was sent or discarded, and that is the signal. Check the
thread for a sent message, compare it against the logged opening, then clear the line.

- Sent unchanged → the draft was right, count it
- Sent with edits → **record what changed**, which is worth more than the count
- Not sent yet → do not count it either way

Update `cs-email/learned-replies.md`. If a category now meets every promotion test, ask once
whether it should go automatic — **in an attended run only**. Unattended, record that it is
a candidate and raise it next time someone is actually there. If the member says no, record that and stop asking.

**Keep the answer book honest too.** If the member corrected a draft on a point of
policy, that correction beats the website: update `cs-email/brand-answers.md`, mark it as coming
from them, and re-verify. Re-read the policy pages every 90 days and show them anything
that changed. A question with no answer in the book goes in its Gaps list.

### 9. Name the run, and say what it found

Two fields, two jobs. Set both with `update_scheduled_task` at the end of every run.

**Title — the name.** Always this shape:

```
CS - 12 Oct - Morning
CS - 12 Oct - Afternoon
```

Day and short month, no leading zero, in the **store's timezone** rather than wherever the
machine thinks it is. The session label comes from the hour of the run:

| Run time, store local | Label |
|---|---|
| before 12:00 | Morning |
| 12:00 to 16:59 | Afternoon |
| 17:00 onward | Evening |

Only use Evening if the store actually runs a third pass. On a twice-daily schedule there
are two names and they should stay predictable, because a consistent shape is what makes a
list scannable.

**Description — what it found.** The one-line summary shown in the sidebar, so the member
can tell whether to open it without opening it:

```
4 waiting, oldest 4 days. Promise false, nothing shipped 3 days.
Nothing waiting. 2 drafts unsent from this morning.
All clear, inbox empty, dispatch on time.
```

- **Lead with the exception.** A broken promise or a four-day wait outranks a count.
- **Numbers, not adjectives.** "A few emails need attention" could mean anything, so it
  means nothing.
- **Say when it is clear.** "All clear" is worth reading and saves them a click.
- **Under about 70 characters.**
- **Update it every run, including the quiet ones.** If this morning said "promise false"
  and a batch has since gone out, that line is now wrong and sitting there looking
  current. A stale line is worse than a generic one, because someone will act on it.

This applies to runs with a task behind them. An ad-hoc chat takes its name from the
conversation, which this skill does not control, so open with the headline rather than a
preamble.

### 10. Report

What was waiting, what was drafted, what needs them personally, what was filtered, and
anything sent automatically — **automatic never means invisible**.

## Rules

- **Never triage before the gate passes.** An inbox read against an empty answer book
  produces replies that sound confident and are made up.
- **Nothing is sent without permission.** Either approval that day, or a standing
  sign-off for that category.
- **Never automate money, complaints, health or a promise you cannot verify.** No count
  makes those safe; the cost of being wrong is not symmetrical.
- **Never wait for approval in an unattended run.** Nobody is there. Draft and report.
- **Never promote a category to automatic outside a conversation.**
- **Never write a second draft on a thread that already has one.** Reconcile
  `list_drafts` against the log first, and when it cannot be resolved, assume the draft is
  the member's and leave it.
- **Never make the member find a particular chat.** State is in `cs-email/`, so any
  conversation can pick up where the last run left off.
- **Never repeat a full brief later in the same day.** Report the delta, and update the
  existing artifact rather than publishing another.
- **Never call a sentiment trend from under five signals.** Say the number instead.
- **Never promise a dispatch time the store is not currently meeting.** Measure it, do
  not read it off the policy page.
- **Never state an order fact without checking Shopify.**
- **Always give the member a clickable link to any order mentioned**, and never put an
  admin link in a customer-facing draft.
- **Never sign as a person who does not exist.** Sign as the brand instead.
- **Never state a policy that is not verified in `brand-answers.md`.** An unverified fact
  is a promise the store may have to keep. Flag it instead.
- **Never infer a policy from one past reply.** An exception made once for one customer
  is not the policy.
- **Count a draft as good only if it was sent unchanged.** Silence is not approval.
- **Report the filtered count.** Invisible filtering is how a real customer gets dropped.
- **Apologise only when there is something to apologise for.** A reflexive apology on a
  same-day reply devalues the real one.
- **Flag, do not guess.** Mark the gap rather than filling it.
- **Demote on any sign it got it wrong**, and say that it happened.

## Check before finishing

- Step 0 passed before the inbox was read.
- The run knew whether it was attended, and behaved accordingly.
- The run knew whether it was the first of the day, and briefed accordingly.
- `list_drafts` was reconciled against `cs-email/open-drafts.md` before anything was written.
- No thread received a second draft alongside an existing one.
- Sent and discarded drafts were cleared from the log.
- The dispatch time quoted in any reply is the measured one, not the published one.
- Anyone waiting on a reply whose order is also overdue was handled first.
- Every thread listed genuinely has a non-store message last.
- Nothing was counted as waiting that is a newsletter, auto-reply or the brand's own send.
- Every order fact in every draft came from Shopify, not from the customer.
- Every policy fact stated came from a verified entry in `brand-answers.md`.
- Drafts are on the right threads, signed per config, including category exceptions.
- Every order mentioned to the member carries a working admin link, and no draft contains one.
- Anything needing a human is marked as such rather than quietly drafted.
- `cs-email/learned-replies.md` reflects what actually happened, including the edits.
- No automatic reply went out in a category on the never-automate list.

## Reference files

- `references/finding-what-needs-a-reply.md` — the triage test, verified queries, noise
- `references/categories.md` — the taxonomy, handling per category, writing rules
- `references/cs-brief.md` — the opening brief: real dispatch time, the promise, who is about to complain
- `references/cs-brief-data-format.md` — the findings JSON the generator expects
- `scripts/build_cs_brief.py` — renders the brief in ECA styling
- `references/learning.md` — the log, the promotion tests, the never-automate list
- `references/linking-to-shopify.md` — building admin links that actually resolve
- `references/building-brand-answers.md` — how the answer book is built and kept true
- `templates/brand-answers.md` — the answer book's shape
- `templates/learned-replies.md` — the starting shape of the log
- `cs-email/brand-answers.md` — written at setup; the store's verified answers, read before every draft
- `cs-email/open-drafts.md` — what has been drafted and not yet sent, reconciled each run
- `cs-email/config.md` — written at setup; mailbox, signature, categories, thresholds, noise list
