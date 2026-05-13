# ECA PDP — Claude Skill

A Claude skill that installs a research-backed, high-converting product detail page template (ECA PDP) into a duplicated copy of a merchant's live Shopify theme. Built for **Shopify Horizon**.

Built by **Ecommerce Academy**.

## What it does

1. Installs / verifies the Shopify CLI
2. Authenticates with the merchant's store
3. Duplicates the **live theme** into an unpublished **ECA PDP Dev** theme — your live storefront is never touched
4. Copies a complete set of high-converting product page files into the dev theme
5. Pushes the result and gives the merchant clear next steps (metafields, template assignment, theme editor, publishing)

## How to use it

In Claude Code, say:

> *"Install the ECA PDP skill on `mystore.myshopify.com`."*

Claude will pick up [SKILL.md](./SKILL.md) and walk through the 7-step flow.

For manual install (no CLI), see [INSTALL.md](./INSTALL.md).

## What gets installed in the theme

Built on the layout backed by current product-page CRO research (above-the-fold buy box, sticky pricing column, layered trust signals, objection-handling sections in the proven order):

```
templates/product.eca-pdp.json
sections/
  eca-value-props.liquid       Objection busters / value props
  eca-how-to-use.liquid        Numbered "how it works" steps
  eca-ugc-gallery.liquid       Customer photos + videos
  eca-faq.liquid               FAQ accordion (with FAQPage JSON-LD)
  eca-reviews-embed.liquid     Judge.me / Loox / Stamped / Yotpo / Okendo / Shopify
  eca-founder.liquid           About-the-founder
blocks/
  eca-pitch.liquid             Reads custom.pitch metafield
  eca-trust-row.liquid         Shipping + guarantee icons under ATC
  eca-sizing-guide-link.liquid Drawer reads custom.sizing_guide metafield
snippets/
  eca-trust-icon.liquid        Inline SVG icon set
  eca-product-schema.liquid    Product JSON-LD with reviews + offers
```

## The buy box (top section)

Built using Horizon's native `product-information` section with these blocks in this order:

1. **Title** (`text` block, h2 preset)
2. **Star rating** (Horizon `review` block — pulls from reviews app metafields)
3. **Pitch** (ECA block — pulls from `custom.pitch` metafield, one-sentence outcome)
4. **Price** (Horizon `price` block — sale price first, installments on)
5. **Divider**
6. **Variant picker** (with swatches enabled)
7. **Sizing guide link** (ECA block — auto-hides if no Size option)
8. **Buy buttons** (qty + ATC + accelerated checkout)
9. **Trust row** (ECA block — shipping + 30-day guarantee icons)
10. **Accordion** with 4 rows: Description / Shipping / Returns / 4th row of your choice

## The page below the fold

In high-converting-tested order:

1. Value props (4-column icon + headline + body grid)
2. How to use (numbered steps with images)
3. UGC gallery (customer photo / video grid, square by default)
4. FAQ (with FAQPage structured data for AI Overviews + rich results)
5. Reviews app embed
6. About the founder (image + story + signature)
7. Product recommendations (Horizon's native `product-recommendations`)

## Required metafields

See [METAFIELDS.md](./METAFIELDS.md). The template works without them — but per-product `custom.pitch` is the highest-impact thing you can set.

## Theme compatibility

| Theme | Works? |
|---|---|
| Horizon | ✅ Built for it |
| Dawn / Sense / Refresh / Craft / Studio | ⚠ Sections work; JSON template references Horizon-only blocks |
| Older paid themes | ⚠ OS 2.0 required |
| Legacy `product.liquid`-only themes | ❌ Not supported |

## Layout rationale

The ECA PDP layout is built on these established CRO findings:

- **Above-the-fold buy box.** Image + title + rating + price + variant + ATC must be visible without scroll on first load. Buy box is sticky on desktop (handled by Horizon's `_product-details` `sticky_details_desktop` setting).
- **Star rating above price.** Reviews are the highest-impact element on a PDP. Star rating sits between the title and pitch, before price.
- **One-sentence pitch.** Outcome-driven subtitle (from the `custom.pitch` metafield) before price. Beats descriptive product copy for conversion.
- **Sale price first.** Strikethrough original, dollar savings on the same line. Concrete savings convert better than "20% off".
- **Buttons not dropdowns** for variants. Color swatches enabled.
- **Trust row directly below ATC.** Free shipping + 30-day guarantee — defuses the two biggest cart-abandonment reasons at the moment they arise.
- **Accordion for shipping / returns / description.** Keeps the buy box compact while keeping every answer one click away.
- **Value props before reviews.** Objection-busters appear immediately after the buy box for users who scroll instead of buying.
- **How-it-works before UGC.** Reduces "I'm not sure how to use this" friction before showing social proof.
- **UGC before reviews.** Visual social proof primes the user for the textual reviews app embed below.
- **FAQ with FAQPage JSON-LD.** Both serves the user and qualifies for Google rich results / AI Overview citations.
- **Founder section last.** Brand story works best after the user is already considering the product, not before.

## Member install

In Claude Code, members run these two commands once:

```text
/plugin marketplace add ecomacademyau/ecomacademy-skills
/plugin install eca-pdp@ecomacademy-skills
```

Then invoke the skill by typing `/eca-pdp:install` or naturally: *"Install ECA PDP on my store mystore.myshopify.com"*.

---

Built by [Ecommerce Academy](https://github.com/ecomacademyau).
