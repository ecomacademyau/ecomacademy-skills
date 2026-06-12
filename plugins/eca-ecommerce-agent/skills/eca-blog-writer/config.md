# Blog Writer — Brand Config

This is the **only** file you edit when forking this skill for a different brand.
Everything in `SKILL.md`, `references/`, and `assets/` is brand-agnostic.

## Our brand

- **Brand name:** [YOUR BRAND NAME]
- **Brand voice + product source:** the `eca-brand-intelligence` skill (invoke it before writing).
  If that skill isn't available, point Claude at your own brand brief / `brand-data.md`.
- **Store domain:** [https://yourstore.com] — used to build live blog/product URLs.

## Shopify blog target

- **Blog to publish into:** [BLOG NAME or handle, e.g. "Tips" / "blogs"]
  Claude will list the store's blogs and match this. If left blank, Claude asks which blog.
- **Default article author:** [AUTHOR NAME, e.g. "The [Brand] Team"]
- **Custom article theme template (advanced, optional):** [templateSuffix, or leave blank for default]

## Publishing default

- **On finish:** **Create as draft for review** (`isPublished: false`). ← recommended default.
  Change to "publish live" only if you want posts to go public with no review step.

## Target market

- **Default market / region:** [YOUR MARKET, e.g. Australia (AU)]
  Used for spelling (e.g. -ise vs -ize), currency, and cultural references.
- **Semrush/SEO database:** [e.g. "au" / "us"] — used if a paid SEO tool is connected.

## Products to feature (the click-through targets)

The posts exist to drive clicks to these. List the heroes; Claude pulls live price/image/URL from Shopify.

| Product | URL / handle | One-line benefit (for insert cards) |
|---------|--------------|--------------------------------------|
| _Hero product_ | _/products/..._ | _e.g. the single biggest reason to buy_ |
| _Secondary_ | _/products/..._ | _..._ |

- **Standing offer / guarantee** (for CTA blocks): [e.g. "30-day money-back guarantee", "Free shipping over $X"]

## Post styles available

All seven live in `references/blog-styles.md`. Note any the brand prefers or wants to avoid:

1. Listicle  2. How-to / educational  3. Influencer / authority product review
4. Comparison / "best X for Y"  5. Question / FAQ answer-style  6. Ultimate guide / pillar  7. Myth-busting / problem-solver

- **Preferred styles:** [or "all"]
- **Influencer-style note:** only reference real public figures with factual, non-defamatory framing
  and no fabricated quotes/endorsements. When in doubt, attribute methods to the public record, not invented statements.

## Images

How the skill handles visuals (it proposes a plan at Gate 1 — these are the defaults it proposes from).

- **Editorial images:** ON by default — captioned images between sections, separate from product cards. Count scales with post length (a couple for short posts, more for guides). The skill proposes placement; you approve/adjust.
- **Sourcing order (hybrid):** 1) the brand's own photos / Shopify media library first; 2) generate on-brand images to fill gaps, always passing the real product as a reference.
- **Brand photo library:** [path or note, e.g. "search Shopify Files for lifestyle shots tagged …", or "none — generate"]
- **Visual style for generated images:** [e.g. "clean, natural light, [brand-colour] accents, real product in shot, no competitor machines/pods"]
- **Hero image:** always one at the top, 16:9 / about 1200x630 (doubles as the social/OG image). Make each post's hero visually distinct from the previous post's.
- **Filename + alt text:** filenames lowercase, hyphenated, keyword/topic-bearing (e.g. `liquid-coffee-concentrate-office-desk.jpg`); every image gets descriptive alt text.

## Writing rules (house style)

- **No em-dashes ("—") anywhere** in output. Use commas, full stops, colons, or brackets. (Hard rule, pre-publish check.)
- **Word count:** 1,000 to 1,500 (longer only for pillar/ultimate guides).
- **Search-volume threshold:** aim for roughly 1,000+ monthly searches (Keyword Planner) before committing a topic. [tune for your niche]

## SEO / GEO defaults

- **Meta description length:** about 150 to 160 characters, includes primary keyword, reads like a promise.
- **Internal links per post:** at least 1 product + 1 related post/collection.
- **Product-insert cards per post:** 2 to 4 (more reads as an ad).
- **FAQ block:** always include (3 to 6 real "People Also Ask" questions).
- **Influencer database (influencer-style posts only):** `references/influencer-database.md` [or your own list]. Ignored for the other six styles.

## Output preferences

- **Draft files:** save the article draft (HTML + a markdown working copy) to the project folder before publishing.
  - **Filename pattern:** `blog-[slug]-[YYYY-MM-DD].(md|html)`
- **House style:** helpful and educational first; selling woven in, never bolted on; answer-first openings.
