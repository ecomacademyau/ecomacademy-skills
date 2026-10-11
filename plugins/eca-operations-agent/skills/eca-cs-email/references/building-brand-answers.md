# Building the answer book

Most support email is the same dozen questions. How long does shipping take, can I
return this, what is in it, how do I use it. A store cannot be helped with any of them
until the skill knows that store's actual answers.

Setup builds `brand-answers.md` by reading the brand's own website, then the member
verifies it. **Every fact in that file will be stated to a customer**, so it is worth the
few minutes.

## Start with what already exists

If `eca-brand-intelligence` is installed and `brand-data.md` has been built, read it
first. Section 13 holds operational facts and sections 4 and 8 hold product detail. Take
what is there, note it came from the brand profile, and only crawl for the gaps.

Do not rebuild what another skill has already established with the member.

## What to read, in order

Ask for the store URL if it is not in config, then fetch:

| Page | Usually at | What to take |
|---|---|---|
| Shipping policy | `/policies/shipping-policy`, `/pages/shipping` | Domestic and international times, costs, free threshold, dispatch cut-off, carriers |
| Refund policy | `/policies/refund-policy`, `/pages/returns` | Return window, condition required, who pays postage, refund vs exchange, exclusions |
| Terms of service | `/policies/terms-of-service` | Anything that contradicts the above |
| FAQ | `/pages/faq`, `/pages/help` | The questions the brand already knows it gets |
| Contact | `/pages/contact` | Stated response time, business hours, physical address |
| Product pages | from Shopify, the live ones | How to use, what is in it, sizes, storage, shelf life, allergens |
| About | `/pages/about` | Only what a customer might ask: where it is made, who makes it |

Shopify stores keep policies at `/policies/...` by default, and those pages are the
authoritative version, because that is what the checkout links to.

## Record a fact with its source

Every entry carries where it came from and when it was read:

```markdown
### Return window
**Answer**: 30 days from delivery, unopened, buyer pays return postage.
**Source**: https://example.com/policies/refund-policy
**Read**: 2026-10-09
**Verified by member**: not yet
```

Without the source, nobody can check it later, and policy pages change without anyone
telling the inbox.

## Verification is not optional

Present the drafted answer book and walk the member through it, section by section, before
anything uses it. Ask directly about the ones that cost money to get wrong:

- the return window and who pays return postage
- the dispatch cut-off and what "next day" actually means
- anything about allergens, ingredients or health
- whether the published policy is the one they actually honour

**That last question matters more than it looks.** Plenty of stores publish a 30-day
return policy and in practice accept 60. The skill should state what the member actually
does, not what the page says, and should note where the two differ.

Mark each section verified with a date. **A fact that has never been verified is never
stated to a customer** — summarise and flag it instead.

## Keeping it true

- **Re-read the policy pages every 90 days** and show the member any wording that changed.
- **Re-verify immediately** if a customer disputes a fact the skill stated, or the member
  corrects a draft on a policy point. That correction is worth more than the page.
- **Never infer a policy from a single past reply.** One exception made for one customer
  is not the policy, and promoting it to one is how a store ends up honouring something
  it never intended.

## When the answer is not written down anywhere

Some things only exist in the member's head. Ask for them once, during setup, and record
them with `**Source**: the member`:

- Wholesale minimums and pricing tiers, if the store does wholesale
- What happens when something arrives damaged
- Whether orders can be changed or cancelled after they are placed, and for how long
- Subscription pause, skip and cancel, if there is a subscription
- Anything the member would not want a stranger answering on their behalf

If they do not know, leave it blank. A blank is a flag to escalate, which is correct. A
guess is a promise the store may have to keep.
