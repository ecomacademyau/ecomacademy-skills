<!-- Lives at cs-email/config.md in your working folder, never inside the installed skill. -->
# Customer service email configuration

## Mailbox
- **Provider**: <Gmail | Superhuman | Fastmail | Microsoft 365 | other>
- **Mail actually lives at**: <the service behind the app, e.g. Google Workspace on a
  custom domain, read in Apple Mail>
- **Mode**: full (can create drafts) | triage-only (search and read, no drafting)
- **Address**: <the inbox this skill works>

> Triage-only loses the learning loop: promotion compares sent replies against drafted
> ones, and there are no drafts to compare.

## Who replies come from
- **Default name**: <the name the customer sees>
- **Title or role**: <optional, e.g. Co-founder>
- **Sign-off wording**: <exactly as it should appear, e.g. "Sarah" or "The Acme team">
- **Per-category exceptions**:
  - complaint: <e.g. the founder>
  - wholesale: <e.g. the founder>
  - creator-collab: <e.g. the founder>

> Never sign as a person who does not exist. With no name given, sign as the brand.

## Store
- **Shopify storefront domain**: <e.g. example.co>
- **Shopify store handle**: <the myshopify subdomain, e.g. example-co — NOT the storefront domain>

> Admin links are built as `https://admin.shopify.com/store/<handle>/orders/<numeric-id>`.
> Deriving the handle from the storefront domain produces a dead link that looks fine.

## Categories in use
Tick what this store actually gets. See `references/categories.md`.
- [x] order-status
- [x] shipping
- [x] product-question
- [x] returns-refunds
- [x] complaint
- [ ] wholesale
- [ ] creator-collab
- [ ] press-partnership

## Schedule
- **Runs**: <cron, e.g. `0 9,14 * * 1-5` for twice each weekday>
- **Created as scheduled task**: <task id, or "on demand only">
- **Run naming**: `CS - <D Mon> - <Morning|Afternoon|Evening>`, in the store's timezone.
  Morning before 12:00, Afternoon 12:00 to 16:59, Evening after. Only use Evening if a
  third pass actually runs.

> Every scheduled run is a fresh session with no memory of the last one. Nothing carries
> across except this file, `brand-answers.md`, `learned-replies.md`, and the drafts sitting
> in the mailbox. Scheduled tasks run while the app is open; one that falls due while it is
> closed runs at next launch.

## Thresholds
- **Counts as late**: 48 hours waiting
- **Look back**: 30 days
- **Maximum drafted in one run**: 15

## Noise list
Senders and patterns that are never a customer. Add to this whenever one slips through.
- `noreply@`, `no-reply@`, `notifications@`
- `support@judge.me` — reviews, handled elsewhere
- Shopify, Stripe, Klaviyo and carrier system mail
- Subjects starting "Automatic reply", "Out of office", "Auto:"
- Anything carrying a List-Unsubscribe header

## Facts the skill may state
These live in `brand-answers.md`, built at setup from the store's own website and verified
by the member. Not here, because each one needs its source and verification date beside it.

- **Store URL to read them from**: <url>
- **Answer book last verified**: <date>
- **Re-read policy pages every**: 90 days

## Automation
Categories signed off for automatic sending. Written by the skill when the member agrees,
never by hand.
- (none yet)
