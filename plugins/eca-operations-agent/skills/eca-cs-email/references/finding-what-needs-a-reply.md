# Finding what actually needs a reply

Every query here was run against a live mailbox. The failure mode in this step is not an
error, it is a number that looks plausible and is wrong.

## Unread is the wrong test

In one real check, six unread threads contained zero customers: an app newsletter, a
survey notification, two out-of-office auto-replies, a reviews notification, and the
brand's own campaign, which appeared because it carried both SENT and INBOX labels.

Reported as "6 emails waiting", that is work that does not exist, every morning, until
the member stops believing the number.

## The right test: who spoke last

**A thread needs a reply when the most recent message in it came from someone else.**
Not when it is unread. Someone can read an email and not answer it, which is exactly how
a thread ends up waiting five weeks.

```
search_threads  query: in:inbox newer_than:30d -in:draft
```

Then for each thread, look at the last message:

- **From the store's own address** → answered. Skip it.
- **From anyone else** → it is waiting. Age it from that message's date.

Pull the thread with `get_thread` when the snippet is not enough to tell what they want.

## Filter the noise, and show your working

Exclude, before counting anything:

| Exclude | How to spot it |
|---|---|
| The brand's own sends | `labelIds` contains SENT |
| Automatic replies | Subject starts "Automatic reply", "Out of office", "Auto:" |
| Notification services | Sender matches `noreply@`, `no-reply@`, `notifications@`, `support@judge.me`, and whatever else config lists |
| Bulk and marketing | `category:promotions`, `category:social`, List-Unsubscribe present |
| Receipts and system mail | Shopify, Stripe, Klaviyo, shipping carriers, unless the member says otherwise |

**Report the filtered count alongside the real one.** "4 waiting, 11 filtered as noise"
makes the filtering visible and lets the member tell you when it is wrong. A single
number hides a bad filter until it has eaten something important.

Anything excluded that is borderline, list by subject. It costs one line and catches the
case where a real customer used a noreply-looking address.

## Order by how long they have waited

Oldest first, always. The ones that hurt a brand are not the ones that came in this
morning, they are the ones that quietly slipped.

Flag past the config threshold, default 48 hours. Note that a thread already apologised
to once, and then left again, is worse than one nobody has answered at all.

## Watch for the contact-form relay

Stores often route their site contact form through email, arriving with a generic
subject such as `New customer message on 28 July 2026 at 10:06 am`. The subject carries
no information, the whole query is in the body, and threads can run for weeks under the
same meaningless heading.

Read the body rather than the subject on these, and do not assume a long thread with one
subject is one conversation. It is often several.

## Get the order before writing a word

If a message mentions an order number, a product, shipping or a refund, look it up in
Shopify first.

```
list-orders   query: name:#1042
get-order     for the full line items and fulfilment state
```

**Never state an order status from the customer's description of it.** They are often
wrong, and a confident wrong answer about someone's money is the worst output this skill
can produce.
