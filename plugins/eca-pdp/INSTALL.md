# Manual install — ECA PDP

This is the no-CLI fallback path. **The recommended way is to let Claude run the `eca-pdp` skill, which does steps 1-3 automatically.** Use this doc only if you're installing by hand.

The ECA PDP kit is built for **Shopify's Horizon theme**. It will load on any OS 2.0 theme, but several buy-box blocks reference Horizon-only blocks (`_product-details`, `_product-media-gallery`, `accelerated-checkout`, `accordion`, `review`, `_product-card`, `_divider`) and will show as missing on non-Horizon themes.

---

## 1. Duplicate your live theme

In Shopify admin: **Online Store → Themes → ⋯ (next to live theme) → Duplicate**. Rename the copy to something like *"ECA Dev"*.

Never edit your live theme directly.

---

## 2. Copy the files into the duplicated theme

Open **Online Store → Themes → ECA PDP Dev → ⋯ → Edit code**.

From the `theme-files/` folder in this skill, paste each file into the matching folder in your theme:

```
theme-files/templates/product.eca-pdp.json   →  templates/
theme-files/sections/eca-*.liquid                    →  sections/
theme-files/snippets/eca-*.liquid                    →  snippets/
theme-files/blocks/eca-*.liquid                      →  blocks/
```

In the code editor, click **Add a new section / snippet / block / template** to create each file, then paste contents.

---

## 3. Create the metafields

Follow [METAFIELDS.md](./METAFIELDS.md) to create:
- `custom.pitch` (rich text)
- `custom.sizing_guide` (rich text)
- `reviews.rating` and `reviews.rating_count` (only if your reviews app doesn't already create these)

The template works without these — defaults come from section settings — but per-product overrides are where this becomes a real conversion engine.

---

## 4. Assign the template

1. Open any product in the admin.
2. Right sidebar → **Theme template** → select **ECA PDP**.
3. Save.

---

## 5. Customize in the theme editor

1. **Online Store → Themes → ECA PDP Dev → Customize**.
2. Top-bar template selector → **Products → ECA PDP**.
3. Every ECA section is editable and reorderable in the left sidebar.
4. The buy box (top section) has reorderable blocks too: title, stars, pitch, price, divider, variant picker, sizing guide, buy buttons, trust row, accordion.

---

## 6. Wire up your reviews app

Edit the **ECA Reviews** section and pick your provider from the dropdown:
- Judge.me
- Loox
- Stamped
- Yotpo
- Okendo
- Shopify Product Reviews
- Custom (paste your own embed HTML)

---

## 7. Test

Before publishing, test:
- [ ] Add a product to cart, confirm the URL updates with `?variant=…` on variant change.
- [ ] Resize to mobile (≤989px) — buy box stacks, value props collapse to 2 columns, UGC collapses to 2 columns.
- [ ] Click the **Sizing guide** trigger (only appears when a product option named `Size` exists, or the `show_always` setting is on).
- [ ] Open every accordion row in the buy box.
- [ ] `view-source:` shows a JSON-LD `Product` block and a `FAQPage` block.
- [ ] The buy-box rating stars are clickable and scroll to `#eca-reviews`.

---

## 8. Publish when ready

`Online Store → Themes → ECA PDP Dev → ⋯ → Publish`. Done.

---

## Theme compatibility notes

- **Built for Horizon.** Other Shopify-built themes (Dawn, Sense, Refresh, Craft, Studio) won't render the buy box correctly because the JSON template references Horizon-specific blocks.
- **OS 2.0 only.** The template won't load in legacy `product.liquid`-only themes.
- **CSS variables.** Uses `--color-foreground`, `--color-background`, `--color-border`, `--page-width`, `--font-body--family`, `--font-heading--family`, `--style-border-radius`. Horizon defines all of these; falls back to safe defaults elsewhere.
- **No CSS clashes.** Every selector is prefixed `eca-`.

---

## Updating

The ECA PDP files are namespaced `eca-*`. To uninstall, delete those files plus `templates/product.eca-pdp.json`, then reassign affected products to your default product template.

To pull a new version of the ECA PDP kit:
1. Replace the same files in your dev theme.
2. The theme editor will reload — your existing customizations to section settings are preserved by Shopify's JSON template merging.
