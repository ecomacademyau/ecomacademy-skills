# Mail providers

This skill needs a connected mailbox. It does not care which one, provided it can do four
things. Most of the work — the triage test, the categories, the learning — is
provider-neutral, because "who sent the last message in this thread" is a question every
mail system can answer.

## The four capabilities

| # | Capability | Used for | Without it |
|---|---|---|---|
| 1 | **Search with a date filter** | finding what arrived and what is waiting | no skill |
| 2 | **List a thread's messages with sender and timestamp** | the who-spoke-last test, ageing | no skill |
| 3 | **Read a message body** | knowing what they actually asked | no skill |
| 4 | **Create a draft on an existing thread** | the whole output | triage-only mode, below |

The first three are the skill. The fourth is how it delivers. A provider with 1 to 3 but
not 4 is still genuinely useful; it just hands the reply over differently.

## Where things stand

| Provider | Capabilities | Notes |
|---|---|---|
| **Gmail** | all four | The tested path. Everything in these references was verified against it. |
| **Superhuman Mail** | all four | Covers Gmail **and Outlook** accounts, and has draft creation. The practical route for most Outlook users. Untested here. |
| **Fastmail** | all four, apparently | Full mail toolset. Untested here. |
| **Microsoft 365** | 1 to 3 only | `outlook_email_search` can find and read, but the connector exposes no way to create a draft. **Triage-only.** |
| **Apple Mail** | none | A desktop app, not a service. There is no connector. See below. |

Check this rather than trusting the table, which will date. Call one small search at setup
and see what comes back, then establish whether drafting works before promising it.

## "I use Apple Mail" usually is not about Apple Mail

Apple Mail is a client, not a mail service. Someone reading mail in it has an account
behind it — iCloud, Gmail, a Microsoft account, Fastmail, or their own domain on some
host. **Ask where the mail actually lives, not which app they read it in.**

> "Which account is behind it? If you open Mail and look at the account name, is it an
> iCloud address, a Gmail or Google Workspace one, or a Microsoft one?"

- **Google Workspace behind Apple Mail** → connect Gmail. Everything works. This is common
  for stores on a custom domain and the member often does not realise their mail is Google.
- **Microsoft behind Apple Mail** → Microsoft 365, triage-only, or Superhuman for the full set.
- **iCloud behind Apple Mail** → no connector exists. Options below.
- **An IMAP host behind Apple Mail** → no connector unless that host has one. Fastmail does.

This one question resolves most "I do not use Gmail" cases into "actually, Gmail."

## When there is genuinely no connector

Be straight about it rather than half-running. Two honest routes:

1. **Forward support mail to a connected mailbox.** Most stores already route
   `support@` or `hello@` through something. A forwarding rule into a connectable account
   gets the whole skill working, and replies go out from the address they set in config.
2. **Run it triage-only** against whatever can be read, and take the drafts by hand.

Say which one they are on. Do not let someone believe they have a drafting assistant when
they have a reader.

## Triage-only mode

With search and read but no drafting, the skill still does most of its job:

- The CS brief in full. Dispatch, the promise, who is about to complain: none of that
  touches the mailbox beyond reading it.
- The queue, oldest first, categorised, noise filtered.
- Order lookups and admin links.
- The replies themselves, **written into the conversation** rather than the mailbox, ready
  to paste.

What it loses: the learning loop. Promotion depends on comparing what was sent against
what was drafted, and without drafts in the mailbox there is nothing to compare. **Say so
at setup.** A member on triage-only should know their skill will not get smarter the way
the full one does, rather than wondering later why it never offers to take anything over.

## Writing queries that are not Gmail

The query syntax in `references/finding-what-needs-a-reply.md` is Gmail's. The intent
behind each is portable; translate rather than copy.

| Intent | Gmail | Elsewhere |
|---|---|---|
| Recent inbox mail | `in:inbox newer_than:30d -in:draft` | a date-bounded search of the inbox folder |
| Exclude own sends | `labelIds` contains SENT | exclude the sent folder, or match on sender |
| Find review notifications | `from:support@judge.me newer_than:2d` | same sender filter, whatever the syntax |
| Exclude bulk | `category:promotions` | List-Unsubscribe header, or the provider's own bulk folder |

Where a provider cannot express an exclusion, do it after the fact: fetch, then filter in
the same way the noise list describes. Slower, same result.
