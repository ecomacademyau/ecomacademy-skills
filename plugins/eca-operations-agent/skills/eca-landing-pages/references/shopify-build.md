# Building it into the Shopify theme (Claude Code)

Runs in **Claude Code** with the Shopify CLI. **The live theme is never edited.**

## 1. CLI + auth
```bash
shopify version || npm install -g @shopify/cli @shopify/theme
shopify theme list --store <store>.myshopify.com   # triggers login
```
Confirm the store domain with the member before connecting.

## 2. Duplicate the live theme
Pull the **live** theme, then push it back as a new **unpublished** dev theme. Never `--live`, never `--allow-live`.
```bash
mkdir -p eca-lp-build && cd eca-lp-build
shopify theme pull --store <store>.myshopify.com --live
shopify theme push --store <store>.myshopify.com --unpublished --theme "ECA LP — <campaign>"
```
Note the returned theme ID and preview URL.

**Check it's OS 2.0** before proceeding: the theme must have `templates/*.json` and a `sections/` directory with section groups. If it's a vintage theme, stop and tell the member — these templates need Online Store 2.0.

## 3. Install only what the format needs
Copy from this skill's `theme-files/`:
- `sections/eca-lp-*.liquid` → the theme's `sections/` (only the ones the chosen format uses)
- `snippets/eca-lp-*.liquid` → the theme's `snippets/`
- `templates/page.eca-lp-<format>.json` → the theme's `templates/`

Then **write the approved copy into the template JSON** so the page renders complete on first load — every value still lives in `settings`, so it all stays editable in the theme editor.

## 4. Push + preview
```bash
shopify theme push --store <store>.myshopify.com --theme <dev-theme-id>
```
Give the member the preview URL: `https://<store>.myshopify.com/?preview_theme_id=<id>`

## 5. Create the page (unpublished)
Create a Shopify page assigned to the new template, left unpublished. Via the Admin API (`pageCreate`) if available, otherwise give the member the two-click instruction: **Online Store → Pages → Add page → Template suffix = `eca-lp-<format>`**, save as hidden/unpublished.

## 6. Hand over
Preview URL · page URL · what to review · any remaining `{{PLACEHOLDER}}` items and what to supply · how to publish (publish the page, then the theme) · **and point the ad's destination URL at the new page**.

---

## Conventions for the section files

- **Every piece of content is a setting.** No hardcoded copy in Liquid. Use `text`, `richtext`, `image_picker`, `url`, `select`, `checkbox`, `color`, `product`, `video` setting types, each with a clear `label` and a sensible `default`.
- **Repeatable content uses blocks** (`{% for block in section.blocks %}`) with `max_blocks` — so the member can add/remove/reorder items in the theme editor.
- **Inherit the theme**, don't fight it: no hardcoded fonts or brand colours. Use `color_scheme` settings where the theme supports them, `rem`/relative units, and let headings inherit. Keep custom CSS scoped inside the section with a `.eca-lp-*` prefix.
- **Use native features first** — the theme's own product form / buy buttons for purchase, the review app's block for reviews, `image_url`/`image_tag` filters with `loading="lazy"` and `srcset` for images, native `<details>/<summary>` for accordions. Only hand-roll what nothing native covers.
- **Always include `{% schema %}`** with `presets` so the section can also be added to other templates.
- **Accessibility**: real heading hierarchy (one `h1` — the hero), `alt` on every image, buttons as `<a>`/`<button>` with discernible text.
- **Performance**: `loading="lazy"` on every below-fold image, no external JS/CSS frameworks, no web fonts.
