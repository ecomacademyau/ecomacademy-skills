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

## 2. Create the images and icons — don't ship empty boxes

A landing page with grey placeholder squares doesn't convert and doesn't get approved. **Produce real visuals wherever you can**, in this order of preference:

1. **The brand's own assets first.** Shopify Files (`files` / the asset library), product images, and any frames from the actual ad creative. *A frame from the ad is the single best hero image* — maximum message match. Check Shopify Files before making anything new.
2. **Generate what's missing** — if an image-generation tool is connected (e.g. Higgsfield, or any available image MCP), create the icons, illustrations, section imagery, and lifestyle shots the page needs. Pass the real product image as a reference so generated visuals stay on-brand and don't invent a product that doesn't exist.
3. **Icons**: prefer a simple inline SVG set you generate to match the brand, or the theme's own icon set, over sourcing random third-party icons.
4. **Upload to Shopify** (Files / theme assets) so the images live with the store and are picked in each section's `image_picker` setting.
5. **If you can't create the image, use a placeholder service** rather than shipping an empty box — the member needs to see the layout working. Use a neutral, correctly-sized placeholder that matches the page's aspect ratio, e.g.:
   - `https://placehold.co/1200x630?text=Hero+image` — plain, sized, captionable (set the text to the shot you need)
   - `https://picsum.photos/1200/630` — a real photo when you just need the layout to read naturally
   **Placeholders are temporary and must never go live.** Every one gets: a clear note in the handover saying what shot to supply, and a line in the "before you publish" checklist. Never use a placeholder for anything that implies a claim (no stock "results" photos, no stand-in faces presented as customers).
6. **Only if even that isn't appropriate**, leave a `{{PLACEHOLDER}}` and say exactly what's needed ("a 16:9 photo of the kit on a kitchen bench") so the member can brief a photographer or shoot it on a phone.

### Icons
Icons are different from photos — you can almost always ship the real thing.
- Use a **free, openly-licensed icon set that suits the theme's style**: [Lucide](https://lucide.dev), [Heroicons](https://heroicons.com), [Feather](https://feathericons.com), [Phosphor](https://phosphoricons.com) (all MIT/ISC and free for commercial use). Pick one set and stay consistent — mixing sets looks amateur.
- **Inline the SVG into the section rather than hot-linking a CDN.** Inlining means no external request (faster), nothing breaks if the CDN goes down, and the icon inherits the theme's colour via `fill="currentColor"` / `stroke="currentColor"` — so it matches the theme automatically. Match the theme's existing icon weight (outline vs solid) and stroke width.
- If the theme already ships an icon set (`snippets/icon-*.liquid` or an `icon` snippet), **use the theme's own icons first** — guaranteed style match.

**Never** invent a photo of a real person, fake a testimonial headshot, or generate an image implying a claim the brand can't make. **Always** set descriptive `alt` text and follow the file-naming convention (lowercase, hyphenated, keyword-bearing).
