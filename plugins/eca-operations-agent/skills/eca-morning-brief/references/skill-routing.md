# Routing each action to a skill

Every action button opens a new Claude conversation with a written prompt. That prompt
should **name the skill that already knows how to do the job**, so the work runs through
the brand's own playbook rather than being improvised from scratch each morning.

## The rule

Name the skill, then give the method anyway.

> "If the `eca-meta-ads-4pi` skill is installed, use it and follow it. If it is not,
> do the job directly: pull the last 21 days from ad account ..., broken down by ..."

**The fallback has to be a real method, not a gesture.** A prompt that says "use the X
skill" and nothing else is worthless to anyone who does not have X, which on the public
download is most people. Write the fallback so the conversation still produces the
answer, and let the skill make it better rather than make it possible.

Never claim a skill exists. Say "if it is installed". The brief cannot see which skills
the member has, and a prompt asserting a skill that is not there sends the conversation
looking for something it will never find.

## The map

Skills marked **planned** are not built yet. Reference them anyway: the prompt costs
nothing today and starts working the day the skill ships, with no change to this file
beyond moving the row.

| What the action is about | Skill to prefer | Status | What the fallback must cover |
|---|---|---|---|
| Meta ad performance, spend, ROAS, a drop | `eca-meta-ads-4pi` | installed | Pull account, campaign, ad set and ad level for the window; name what changed and when |
| Customer service email | `eca-cs-email` | planned | Read unanswered customer mail, summarise, draft replies, send nothing |
| Product reviews | `eca-review-replies` | planned | Find reviews via Judge.me notification emails, draft per-review replies, flag low ratings |
| Stock cover and reordering | `eca-stock-cover` | planned | On-hand against 28-day velocity, weeks of cover, flag under threshold |
| Dispatch and fulfilment | none | — | Unfulfilled paid orders with ages, daily fulfilment counts, average hours to dispatch |
| SEO and AI visibility | `eca-seo-ai-audit` | installed | Crawl, schema, indexing, the obvious technical checks |
| Blog and content | `eca-blog-writer` | installed | Keyword research, then draft to the house structure |
| Ad creative | `eca-bfcm-ads-builder` | installed | Only during a sale campaign; it needs a locked offer |
| Email campaigns | `eca-email-marketing-campaign` | installed | Topic, series shape, subject lines, copy |
| A sale offer | `eca-bfcm-offer-builder` | installed | Last year's data, break-even, three offers |
| Brand voice for any copy | `eca-brand-intelligence` | installed | Read `brand-data.md` before writing anything customer-facing |

## Writing the prompt itself

Each one is a brief to a capable colleague who was not in the room. Six things:

1. **The job and a title.** "Work out what happened to the ads on 3 October. Title it
   *The 3 October ad drop*." A titled conversation is findable next week.
2. **The skill line.** Prefer the skill, give the fallback method.
3. **What the brief found, marked as a starting point.** Hand over the numbers, then say
   plainly to re-derive them. The brief can be wrong, and a prompt that presents its
   figures as settled fact propagates the error instead of catching it.
4. **The traps.** Anything learned about that data source belongs here, every time:
   Meta renames `purchases` to `omni_purchase` and returns `null` rather than zero for a
   day with no sales; ShopifyQL returns nothing for `SINCE -1d UNTIL -1d` so single past
   days need explicit dates; today's row is always partial; Judge.me subject lines parse
   as `<Name> left a <N> star review for '<Product>'`.
5. **What is owed, and to whom.** "Post nothing until I approve" for anything customer
   facing. "This is mine to decide" where it is just a decision. Silence here is how a
   draft becomes a sent email.
6. **The finish.** Name the deliverable. "Finish with the most likely cause, what you
   ruled out, and the first three things to change today."

Keep it under about 1,000 characters. It travels in a URL, and a prompt longer than that
is usually carrying detail the conversation can fetch for itself.
