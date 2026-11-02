# The section library

Seven sections, each self-contained: its own CSS inline, no shared assets, no snippets to
install. Every one inherits the theme's colour scheme by default and takes the theme's own
fonts, so the guide looks like the store rather than like a skill.

| Section | Does | Use |
|---|---|---|
| **Page settings** | The cut-off bar, optionally sticky | Once, first. The only place the date lives |
| **Banner** | The top of the page: image, H1, intro, button | Once |
| **Quick links** | Tiles or buttons into collections | Once, near the top |
| **Gift grid** | One gift group, with a see-all link | **Once per group** |
| **Last-minute options** | Gift cards, express, click and collect | Once |
| **FAQ** | Questions plus the FAQPage schema | Once |
| **About these gifts (SEO)** | A paragraph per group, at the foot | Once |

## Things worth knowing

**The gift grid is the repeatable one.** Add it once per group — by recipient, by interest,
by price band. Three to five groups is the usual shape; more than six and the page stops
being a guide and becomes a catalogue.

**Pick products, don't type them.** A gift block with a product picked keeps its own title,
image, price and stock automatically, so the guide stays right as the catalogue moves —
and it moves daily through December. The manual fields exist for things that aren't
products: a collection, a guide, an external page. *Hide sold-out products* is on by
default and should stay on.

**The FAQ schema cannot drift from the page.** The visible list and the FAQPage JSON-LD are
built from the same blocks in the same loop, so they cannot disagree. That also means a
wrong answer is wrong in both places — the schema is not a second chance to check.

**Each gift grid emits its own ItemList** naming the products in order. That is what gets a
gift guide quoted as a source rather than just ranked.

**Alternate the colour schemes.** A long page in one flat colour reads as a wall and people
stop scrolling. Give the banner and one or two bands a contrasting scheme and let the rest
inherit, so the page reads as chapters. Two or three contrast bands is plenty — more looks
like a ransom note. Prefer the theme's schemes over the custom pickers: they carry text and
button colours together, so a dark band still has readable text, and they stay right if the
member later changes their palette.

**Anchors let the quick links jump down the page** instead of away from it. Set an anchor
id on a gift grid and point a quick-link tile at `#that-id`. Worth doing for the groups the
member most wants read; send the rest to the collection.

**Images are placeholders until the member picks them.** Every image slot renders Shopify's
native placeholder at the right ratio, so the layout reads correctly from the first load.
Your job is the image brief, not the picture.
