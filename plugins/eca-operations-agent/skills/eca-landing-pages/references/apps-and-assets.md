# App-first & asset creation

Two rules that decide *how* a section gets built, before you write a line of Liquid.

---

## 1. App-first — never rebuild what an installed app already does

**Before creating any section, check whether the store already has an app or a native theme feature that does the job.** Merchants pay for these apps; their widgets carry real data (live review counts, real star ratings, subscription selling plans) that a hand-built section can only fake. Rebuilding them is worse for the member *and* worse for conversion.

### Check what's installed, first
- Inspect the theme for app blocks and embeds: look in `sections/*.liquid` and the theme's JSON templates for `"@app"` blocks and `shopify://apps/...` references, and check `settings_data.json` for app embeds.
- Ask Shopify (Admin API / `appInstallations` where scopes allow). If that's blocked, **ask the member**: *"I can see Judge.me on your store — want the page to use its review widget rather than a static one?"*
- Look at the live storefront: rendered review widgets, subscription selectors, bundle builders and upsell blocks all reveal the app stack.

### The rule
| If the store has… | Use | Don't |
|---|---|---|
| A **reviews app** (Judge.me, Loox, Okendo, Yotpo, Stamped) | its review widget / app block, and its star-rating badge near the CTA | hand-copy reviews into a static testimonial section |
| A **subscription app** (Recharge, Seal, Appstle) | its native selling-plan selector on the offer section | build a fake "subscribe" toggle |
| An **FAQ app** | its widget (if it also emits FAQPage schema) | duplicate the questions in a custom section |
| A **bundle / upsell app** | its bundle builder or offer block | rebuild the bundle logic |
| A **page builder** already in use (Shogun, PageFly, GemPages) | tell the member it exists and ask which they'd rather use | silently install a competing system |
| **Native theme sections** that already cover it (rich text, image with text, multicolumn, slideshow, collapsible content, featured product) | the theme's own section | a custom clone of it |

**How to apply it:** every ECA LP section supports `{ "type": "@app" }` blocks, so the member can drag the app's own block straight into it in the theme editor. When an app covers a section's job, either (a) drop the app block into that section, or (b) skip our section entirely and use the app's — and say which you did and why. **When it's genuinely a close call, ask the member rather than deciding for them.**

Only build custom when nothing installed does the job, or the member asks for it.

---

## 2. Images: always ship placeholders — the member supplies the real ones

**Do not choose, source or generate photographs for the page.** Picking images automatically produces layouts that look wrong — the wrong crop, the wrong subject, a product shot where a lifestyle shot belongs. The member knows their imagery; you don't. So:

**Every image slot ships as a placeholder.** The sections handle this natively: when an `image_picker` setting is empty, the section renders Shopify's built-in `placeholder_svg_tag` at the correct aspect ratio (16:9 hero, 4:3 steps, 1:1 product/kit items). The layout reads correctly straight away, and the member swaps in their own image in the theme editor with two clicks — no code, no re-deploy.

**What you do instead of choosing images:**
- **Set the right aspect ratio and position** for each slot so the layout is correct.
- **Write the image brief** — for every placeholder, tell the member exactly what shot belongs there: subject, framing, ratio. e.g. *"Hero, 16:9 — the product in use on a kitchen bench, natural light. A frame from your ad creative works best here."*
- **Recommend the ad's own creative for the hero** — it's the strongest message match — but let the member place it.
- **Write the `alt` text** as a suggestion in the brief so it's ready when they add the image.
- **List every placeholder in the pre-publish checklist.** The page is not ready to publish while placeholders remain.

**The only exception:** if the member explicitly asks you to place a specific image (or points you at one in their Files), use that one. Their call, not yours.

### Icons
Icons are different — they're generic symbols, not photography, so ship the real thing:
- **Use the theme's own icon set first** (`snippets/icon-*.liquid`) — guaranteed style match.
- Otherwise **inline an SVG** from a free, openly-licensed set that suits the theme: [Lucide](https://lucide.dev), [Heroicons](https://heroicons.com), [Feather](https://feathericons.com), [Phosphor](https://phosphoricons.com) (all MIT/ISC, fine commercially). Pick one set and stay consistent.
- **Inline, don't hot-link a CDN** — no external request, nothing breaks if the CDN dies, and `currentColor` makes the icon inherit the theme's colour automatically.

**Never** fake a testimonial headshot or use an image implying a claim the brand can't support. **Always** follow the file-naming convention (lowercase, hyphenated, keyword-bearing) for anything the member does upload.
