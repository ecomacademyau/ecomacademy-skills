# Product metafields for the ECA PDP template

These per-product metafields let merchants override defaults on a product-by-product basis. The template works without them — section settings provide sensible defaults — but per-product metafields are where this becomes a real conversion engine.

Create these in **Shopify admin → Settings → Custom data → Products → Add definition**.

## 1. Pitch (required for `eca-pitch` block)

A one-sentence benefit-led subtitle that sits between the rating stars and the price.

| Field | Value |
|---|---|
| Name | Pitch |
| Namespace and key | `custom.pitch` |
| Type | Rich text (or Multi-line text) |
| Description | One sentence describing the customer outcome |

**Example value:** _"Sleep faster, wake clearer — the magnesium blend designed for restless minds."_

## 2. Sizing guide (required for `eca-sizing-guide-link` block)

A rich-text table or block of measurements. The trigger auto-hides on products that don't have a `Size` option.

| Field | Value |
|---|---|
| Name | Sizing guide |
| Namespace and key | `custom.sizing_guide` |
| Type | Rich text |

## 3. Star rating (used by the buy-box `review` block)

Most reviews apps already create these. If yours doesn't, define them manually:

| Field | Value |
|---|---|
| Name | Rating |
| Namespace and key | `reviews.rating` |
| Type | Rating |
|  |  |
| Name | Rating count |
| Namespace and key | `reviews.rating_count` |
| Type | Integer |

> **Note:** Judge.me, Loox, Stamped, Yotpo, and Okendo all populate `reviews.rating` automatically. Skip this step if your reviews app is installed.

## Optional metafields

These aren't required but make the template more flexible if you want them.

### Highlight (buy-box callout)

A short text line you can pin above the title (e.g. *"Best-seller"*, *"New formula"*).

| Field | Value |
|---|---|
| Namespace and key | `custom.highlight` |
| Type | Single line text |

### Ingredients (extra accordion row)

Pre-formatted ingredient or material list.

| Field | Value |
|---|---|
| Namespace and key | `custom.ingredients` |
| Type | Rich text |

## Quick check

After creating the metafields, open any product and confirm you can see and edit them in the right-hand "Metafields" panel. They'll show up automatically — no template changes required.
