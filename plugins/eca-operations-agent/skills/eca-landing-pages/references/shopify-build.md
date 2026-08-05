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

## 3. Install the files

Copy from this skill's `theme-files/`:
- **`snippets/` — copy ALL of them, every time.** Never cherry-pick snippets. They're tiny shared dependencies (CTA, placeholder, future helpers) and a section that renders a missing snippet throws a Liquid error on the live page. Copying the whole folder costs nothing and removes an entire class of bug.
- **`assets/` — copy ALL of them, every time** (if the folder exists), for the same reason.
- `sections/eca-lp-*.liquid` → only the ones the chosen format uses.
- `templates/page.eca-lp-<format>.json` → the chosen template.

**Rule: whole folders for dependencies (snippets, assets), selective only for sections and templates.**

## 3b. Verify dependencies BEFORE pushing (mandatory)

Never push a theme whose sections reference a file that isn't there. **Derive the dependency list from the code, not from memory** — this way it keeps working as the library grows and new helpers are added:

```bash
# From the theme root. Lists every snippet the installed ECA LP sections render,
# then reports any that are missing.
grep -ho "render[[:space:]]*'[^']*'" sections/eca-lp-*.liquid \
  | sed "s/.*'\(.*\)'/\1/" | sort -u \
  | while read -r snip; do
      [ -f "snippets/$snip.liquid" ] || echo "MISSING SNIPPET: snippets/$snip.liquid"
    done

# Sanity: every section referenced by the template exists
python3 - <<'EOF'
import json, glob, os
for t in glob.glob('templates/page.eca-lp-*.json'):
    d = json.load(open(t))
    for sid, sec in d.get('sections', {}).items():
        f = f"sections/{sec['type']}.liquid"
        if not os.path.exists(f):
            print(f"MISSING SECTION: {f} (used by {t})")
EOF
```

**If anything reports missing, copy it across and re-check before pushing.** A missing snippet doesn't fail quietly — it renders a Liquid error to real visitors.

Also worth running after the push: pull the preview URL and confirm the page renders (no `Liquid error` strings in the HTML).

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
