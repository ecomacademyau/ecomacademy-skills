# The guide data file

`seed_template.py` takes one JSON file and writes the seeded page template. See
`templates/guide-example.json` for a filled example.

```jsonc
{
  "title": "Christmas Gift Guide",

  // The banner across the top. Both halves matter: the bar is for people, and the
  // FAQ answer below is what an answer engine can lift. A bar alone cannot be quoted.
  "cutoff": {
    "banner": "Christmas delivery: order by 11am Friday 19 December",
    "sticky": true,
    "link_url": "/policies/shipping-policy", "link_text": "Shipping details"
  },

  "banner": {
    "layout": "split",            // split | split-right | stacked | text
    "heading": "Christmas Gift Guide",   // this is the page H1
    "image_alt": "describe the gift or the scene, not the layout",
    "body": "One or two sentences.",
    "cta_label": "Shop all gifts", "cta_url": "/collections/gifting"
  },

  // Tiles at the top, for people who already know who they are buying for.
  "quick_links_heading": "Start with who it's for",
  "quick_links_style": "tiles",   // tiles | buttons
  "quick_links": [
    {"collection": "gifting", "label": "Gifts for coffee lovers"}
  ],

  "sections": [{
    "heading": "The best gifts for someone who loves coffee",  // write it as a search
    "lead": "One line of context.",
    "anchor": "coffee-lovers",    // lets a quick link jump here
    "columns": 3,
    "more_url": "/collections/gifting",
    "more_text": "See all gifts for coffee lovers",   // name the thing, never "See all"
    "items": [
      {"handle": "coffee-starter-pack", "note": "Why this suits them."},
      {"title": "Something that isn't a product", "url": "/pages/...", "note": "..."}
    ]
  }],

  "options_heading": "Left it too late?",
  "options": [{"title": "Digital gift card", "detail": "...",
               "url": "/products/gift-card", "cta": "Buy a gift card"}],

  "faq_heading": "Christmas delivery and returns",
  "faqs": [{"q": "When is the last day to order for Christmas delivery?", "a": "..."}],

  // The prose at the foot. A paragraph per gift group, naming the actual products.
  "seo_text": {
    "heading": "About these Christmas gifts",
    "intro": "...",
    "columns": "1",
    "parts": [{"heading": "matches the gift group above", "body": "150-250 words."}]
  }
}
```

**Use `handle`, not `title` and `url`.** A picked product keeps its own title, image, price
and stock, so the guide stays accurate as the catalogue moves. The manual form is for
things that are not products.

**Match each `seo_text` part heading to a gift group heading.** The checker warns on a
group with no paragraph, because that group has nothing to rank on.

**Plain text is fine for every rich field** — `lead`, `detail`, `a`, `body`, `intro`. The
seeder wraps it in paragraphs. Shopify silently drops a bare string in a richtext setting,
which renders as an empty section rather than an error.

## What `--check` does

**Fails** on: no cut-off line; an empty gift group; a gift with neither a handle nor a
link; a see-all link that says only "See all" or "Shop now"; no SEO text; a leftover
`{{PLACEHOLDER}}`.

**Warns** on: thin SEO text; a gift group with no matching paragraph; no quick links.

It cannot judge whether the products are the right products. That is the worksheet's job.
