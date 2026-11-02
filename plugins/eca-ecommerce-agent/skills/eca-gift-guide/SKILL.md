---
name: eca-gift-guide
description: "Build a Christmas gift guide for a Shopify store in whichever of three formats suits it: a full page template with a banner, quick-link tiles, a gift group per audience, last-minute options, FAQ and SEO text; a collection guide that wraps a banner, quick links and SEO text around the store own collection page; or a blog gift guide article that needs no code editor and runs from chat. Asks which before anything else. Runs the three-part gift guide worksheet as a guided interview across Family and Friends, Gotta Gift and Last Minute shoppers, reads the real catalogue to fill the gift slots, and finds or proposes the collections each tile needs. Use whenever someone wants a Christmas gift guide, a holiday gift page, gift ideas by recipient or budget, a last minute gift section, a Christmas collection or landing page, or asks what to put behind their Christmas ads. Never edits the live theme and never publishes."
---

# Christmas Gift Guide

Build the member's Christmas gift guide: one URL that carries every Christmas ad, email
and post.

**Three formats** — a full page template, a collection page with a banner and SEO text
around it, or a blog article. Step 0 picks between them, because only two of the three
need a code editor and the third runs from chat.

> The two theme formats run in **Claude Code** with the **Shopify CLI**, and never touch
> the live theme: all work happens in a duplicated dev theme, and the page is created
> **unpublished** for review.

## Step 0 — Which gift guide

**Ask this first, before checking anything else.** The three formats need different things,
so gating on the CLI before knowing the format turns away a member who did not need it.

1. **The full guide** — a page template: banner, quick-link tiles, a gift group per
   audience, last-minute options, FAQ, SEO text. Ranks best. *Needs the Shopify CLI and a
   code editor.*
2. **The collection guide** — the store's own collection page with a banner and quick
   links above it and SEO text below. Keeps the theme's sorting, filtering and pagination.
   Fastest thing that still looks designed. *Needs the Shopify CLI and a code editor.*
3. **The blog guide** — a gift guide as an article on the store's blog. *Needs nothing;
   runs from chat.*

`references/choosing-the-format.md` has the comparison and how to choose. **Recommend
one** rather than listing three and waiting: a store with one narrow range wants the
collection guide, a store with several recipient types wants the full guide, and a member
with no code editor wants the blog guide whatever else is true.

## Step 0b — The gate for that format

**Format 3 (blog) needs no gate beyond Shopify.** Skip to Step 1.

**Formats 1 and 2** need all three of these, checked before any work:

**1. A code editor.** These write real theme files, so they have to run in Claude Code
inside VS Code, Cursor, or whichever editor they use. They cannot be driven from a
chat-only window. If the member is not in one, **offer the blog guide instead** rather
than stopping dead — it reaches the same shoppers this week.

**2. The Shopify CLI, authenticated.**

```bash
shopify theme list --store <store>.myshopify.com
```

Missing? `npm install -g @shopify/cli @shopify/theme`. **Confirm the exact
`.myshopify.com` domain with the member — never guess it.**

**3. Shopify MCP (Admin API).** Optional but close to essential: it reads the catalogue so
the guide is built from real products, and creates the page. Without it the member picks
every product by hand in the theme editor.

**The CLI is the only hard stop**, and it is not a dead end — it is a reason to build
format 3 today.

## Step 1 — When is Christmas, for this store

Three facts the whole page hangs on, settled before the worksheet:

- **The delivery cut-off**, per shipping method, in the store's timezone. Ask directly and
  **confirm it back with the weekday**: "orders by 11am Friday 19 December" can be checked;
  "by the 19th" invites someone to get the day wrong.
- **Whether there is a pick-up point**, with address and Christmas hours.
- **Whether they sell gift cards**, and whether delivery is instant.

**If they do not know the cut-off, stop and get it.** Everything else can be refined after
launch. This one is a promise, and the seeder refuses to build without it.

## Step 2 — Run the worksheet

Follow `references/the-worksheet.md`. All three shopper types get filled — Family &
Friends, Gotta Gift, Last Minute — because they arrive in three different states of mind
and a single "Christmas" collection serves none of them.

**Filter the catalogue before you propose anything.** Most of a real product list must not
go in a gift guide. Exclude every time:

- **Draft, archived and unpublished products.** A `status:active` search still returns
  drafts, so check `status` and `publishedAt` on each one rather than trusting the query.
- **Discount duplicates of a live product** — the "(15% OFF)" twins kept for ad landing
  pages, usually tagged `noindex`. Linking one from a page built to rank is self-defeating.
- **Anything an app owns**, like the zero-dollar placeholders gifting and upsell apps install.
- **Anything at zero stock.** Say out loud when a well-fitting gift is out of stock —
  restocking it may be the highest-value thing the member does this week.

Gift cards are the exception to the stock rule: they report zero inventory and are always
available.

**Price bands must have real products in them.** Check before offering "under $50". And
only offer recipient tiles this catalogue serves — an empty "gifts for child" tile on a
shaving-gear store is worse than no tile.

## Step 3 — Find or create the collections

Every quick-link tile and every see-all link needs somewhere real to point. **Search
existing collections first and reuse them** — most stores already have more than they
remember.

Where there is nowhere to point, **propose** a collection and show what would be in it
before creating anything:

- **Price bands** are where a smart collection earns its place. A rule on `VARIANT_PRICE`
  keeps the tile accurate as stock and pricing shift through December with nobody
  maintaining it. Create with `ruleSet`, but **read the rules back with `sources`** —
  `Collection.ruleSet` is deprecated on read and the query is rejected outright, so a
  verification step written against it fails rather than warns.
- **Recipient and interest tiles** usually want a manual collection or a tag rule, because
  "gifts for someone who cooks" is a judgement, not a filter.

**Create nothing without a yes.** Show the rule, a sample of what it catches, and the
count. A smart rule that quietly catches the wrong products shows a Christmas shopper the
wrong thing.

## Step 4 — Write the guide

Write the data file per `references/guide-data-format.md`. Four things carry the page, and
`--check` enforces all four:

- **The banner.** The H1 lives here. One per page.
- **Quick links at the top.** Tiles or buttons into the right collection, because most
  people arrive already knowing who they are buying for. Label them the way a shopper
  would say it: "Gifts for latte lovers", never "Collection 3".
- **See-all links that name the thing.** "See all gifts for latte lovers", not "See all".
  The link text is the clearest signal on the page about what sits behind it, for a reader
  and a crawler alike.
- **The SEO prose at the foot** — a paragraph per gift group saying who it suits and why,
  naming the actual products. This is most of what the page can rank on and most of what
  an answer engine can quote. Write it for a person; the reader who finds it useful is the
  same signal the search engine is looking for.

Then follow `references/seo-and-aeo.md` for the headings and the meta.

**The blog guide stops here.** Hand the worksheet answers, the product picks, the FAQ and
the SEO paragraphs to **`eca-blog-writer`** and let it write and publish the article as a
draft. Tell it the cut-off sentence must appear verbatim and that every product link is a
real in-stock product. Do not write the article here — that skill has the structure,
the schema and the Shopify publishing step already.

**The collection guide** needs only the banner, the quick links and the SEO text: the gift
groups, options and FAQ belong to the full guide, and the seeder drops them for this
format. Pull the store's own collection template first, because **the product grid section
has a different name in every theme** — Dawn calls it `main-collection-product-grid`,
others `main-collection` — and naming the wrong one produces a collection page with no
products and no error anywhere.

```bash
# full guide
python3 scripts/seed_template.py guide.json --out page.eca-gift-guide.json --check

# collection guide: the store's own sections stay in the middle, untouched
python3 scripts/seed_template.py guide.json --format collection \
  --base ./theme/templates/collection.json \
  --out collection.eca-gift-guide.json --check
```

`--check` exits non-zero on a missing cut-off, an empty gift group, a gift with nowhere to
point, a lazy see-all link, missing SEO text, or a leftover `{{PLACEHOLDER}}`. It warns on
thin SEO text, a gift group with no matching paragraph, and no quick links. Run it every
time; it cannot tell you whether the products are the right products, but it catches
everything that produces a page which looks finished and isn't.

## Step 5 — Build into the theme

Detail in `references/building-into-the-theme.md`.

1. **Duplicate the live theme** into an unpublished dev theme, e.g. `ECA Gift Guide`.
   **Never edit the live theme.**
2. Copy `theme-files/sections/` and the seeded template into the dev theme. The library is
   self-contained — each section carries its own CSS and there are no shared assets.
3. **Run the colour-scheme adapter before every push**:
   `python3 scripts/adapt-color-schemes.py <theme-dir>`. On themes with no colour schemes
   it strips the setting so Shopify does not show a red "color schemes must be defined"
   banner across the member's editor. Never leave that warning on their screen — it reads
   as though the page is broken when it isn't.
4. Push to the dev theme.
5. **Full guide:** create the page unpublished and assign it the template — `pageCreate`
   with `templateSuffix: "eca-gift-guide"`, `isPublished: false`, and the SEO metafields
   `global.title_tag` and `global.description_tag`.
   **Collection guide:** the collection already exists, so there is nothing to create —
   set its **template** to `eca-gift-guide` in the collection's admin page, and write its
   SEO title and description there. Check the collection is the right one and that it has
   products in it before switching the template.

For the full guide, **use the same handle every year** — `christmas-gift-guide`, never
`christmas-gift-guide-2026`. A URL that accrues links across five Christmases is worth far
more than a fresh one each November. If the page exists, `pageUpdate` it rather than
creating a second one.

## Step 6 — Hand it over

**Always finish with three clickable links** (formats in
`references/building-into-the-theme.md`):

- **Edit the guide** — the theme editor deep-linked to this page, so they can change
  copy, images, tiles and order straight away.
- **Preview it** — the storefront on the dev theme.
- **Page settings** — the admin page for title, SEO and publishing.

Then a **before-you-publish checklist** naming every placeholder image still on the page
and what to supply for each, and these three:

1. **Read the cut-off date out loud** and check the weekday against a calendar.
2. **Publish, then submit the URL for indexing** in Search Console the same day.
3. **Link to it** from the nav, the homepage and the footer. A gift guide with no internal
   links is an island.

Say plainly if they are building late. **A guide published in mid-December will not rank
for Christmas** — Google needs weeks. Paid and email carry it this year, and the page is
aged and ready for next. Better said now than wondered about in January.

## Rules

- **Never guess the delivery cut-off.** It is a promise, and a wrong one costs a customer.
- **Never touch the live theme.** Duplicate, build, hand over the preview.
- **Never publish the page.** They publish it.
- **Never create a collection without showing what is in it first.**
- **Never offer a shipping or pick-up option the store does not have.** A pick-up tile on
  a store with no premises is the fastest way to lose trust in December.
- **Never link a product that is out of stock**, and re-check availability at build time
  rather than trusting a list written an hour ago.
- **Never choose photos.** Ship placeholders and write the image brief — subject, framing,
  ratio, alt text. Auto-picked photos produce wrong-looking layouts.
- **Never change the URL between years.**
- **Never build a format the member cannot maintain.** A full guide on a store with eight
  products looks padded; say so and build the collection guide instead.

## Reference files

- `references/choosing-the-format.md` — the three formats, and which suits this store
- `references/the-worksheet.md` — the three shopper types and what each is really asking
- `references/seo-and-aeo.md` — ranking, and being quotable by answer engines
- `references/guide-data-format.md` — the data file the seeder takes
- `references/building-into-the-theme.md` — the CLI build, the adapter, the handover links
- `references/section-library.md` — what each section does and when to reach for it
- `templates/guide-example.json` — a worked example for a fictional store
- `scripts/seed_template.py` — builds the seeded page template, with `--check`
- `scripts/adapt-color-schemes.py` — run before every push
