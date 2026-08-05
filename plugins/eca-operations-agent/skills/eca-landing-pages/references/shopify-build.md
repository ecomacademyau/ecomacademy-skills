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

## 3a. Versioned sections — new pages get the latest, old pages never break

Section files are **version-namespaced** when their structure changes:

```
sections/eca-lp-hero.liquid       v1 — an older page may still use this
sections/eca-lp-hero-v2.liquid    v2 — current; new pages use this
```

Each file also carries a stamp on line 1 (`eca-lp-library vX.Y.Z`), and the skill ships `theme-files/VERSION`.

### The rule

**Install anything missing. Refresh same-name files to the current library version. Never touch a file whose name has been superseded.**

This is safe *by construction*, because of how versions are assigned:

| Situation | What you do | Why it's safe |
|---|---|---|
| File missing | Install it | Nothing to break |
| **File exists with the same name as a current library file** | **Overwrite with the current version** | A same-name file can only have had **additive** changes since (structural changes always get a new filename). Shopify keeps saved settings, new settings take their defaults, existing blocks still render — so pages built on it keep working *and* pick up fixes |
| File exists but its name is **superseded** (e.g. `eca-lp-hero.liquid` when the library ships `eca-lp-hero-v2.liquid`) | **Leave it completely alone** | An older page still renders from it. Never overwrite, never delete |
| File exists and has been **hand-edited** (content differs from its stamped release) | **Stop and ask** before replacing; offer a `.bak` copy | Their customisation is real work |

**The result:** duplicate a theme containing an old page, build a new page in it, and the new page gets **everything current** — new sections, new blocks, additive improvements and bug fixes — while the old page keeps rendering exactly as built.

### When to create a new version (`-v2`, `-v3`…)
Only for a **structural change** — something that would break a page built on the old file:
- settings moved into blocks, or blocks restructured
- a setting removed or its `id` changed
- markup reworked such that existing saved settings no longer apply

**Not** for cosmetic or additive changes (new optional setting, CSS tweak, bug fix) — those ship inside the current version, since existing pages keep working and benefit from the fix.

When you do create one: copy the file to the new name, bump the stamp, update the templates to reference it, and mark the previous file **deprecated** in the library (`manifest.json` → `deprecated_do_not_install`). The library ships only current versions — a member's theme already has its old file, so there's nothing to re-ship. **Never install a deprecated file into a theme.**

### Housekeeping
Old version files stay in the theme even if unused — never delete them, since a page you can't see may reference one. A few extra section files is normal; Shopify themes carry dozens.

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

**Also validate the Liquid itself** — Shopify's API rejects a file outright if it contains invalid Liquid, so the section silently fails to install:

```bash
# Comparisons are NOT allowed inside output tags. This is invalid and will be rejected:
#   {{ variant.compare_at_price > variant.price }}
# Use {% liquid assign x = false / if ... / endif %} then output {{ x }}.
grep -nE "\{\{[^}]*( > | < | != | == )[^}]*\}\}" sections/*.liquid && echo "INVALID LIQUID: comparison inside an output tag"

# Tag balance
for f in sections/*.liquid; do
  i=$(grep -c '{%- if \|{% if ' "$f"); e=$(grep -c '{%- endif\|{% endif' "$f")
  [ "$i" = "$e" ] || echo "UNBALANCED if/endif: $f ($i/$e)"
done
```

**And check the schema limits** — Shopify silently rejects a section file whose schema breaks them:

```bash
python3 - <<'EOF'
import re, json, glob
for f in sorted(glob.glob('sections/*.liquid')):
    sch = json.loads(re.search(r'{% schema %}(.*?){% endschema %}', open(f).read(), re.S).group(1))
    if len(sch.get('name','')) > 25:
        print(f"NAME TOO LONG ({len(sch['name'])}>25): {f} — {sch['name']}")
    for b in sch.get('blocks', []):
        if len(b.get('name','')) > 25:
            print(f"BLOCK NAME TOO LONG: {f} — {b['name']}")
    if len(sch.get('blocks', [])) > 50:
        print(f"TOO MANY BLOCK TYPES: {f}")
EOF
```

Known Shopify schema limits worth respecting: **section `name` ≤ 25 characters** (and block `name` too), max 50 block types, max 25 settings per block. Keep names short — the theme editor truncates long ones anyway.

If the CLI reports a file as rejected, read its error before retrying — a rejected section means the page renders without it.

**If anything reports missing, copy it across and re-check before pushing.** A missing snippet doesn't fail quietly — it renders a Liquid error to real visitors.

Also worth running after the push: pull the preview URL and confirm the page renders (no `Liquid error` strings in the HTML).

Then **write the approved copy into the template JSON** so the page renders complete on first load — every value still lives in `settings`, so it all stays editable in the theme editor.

### Colour schemes — check the theme supports them

Every section exposes a `color_scheme` setting. That control is populated by the theme's own scheme definitions, so before you rely on it:

```bash
grep -l "color_scheme_group" <theme-dir>/config/settings_schema.json
```

- **Found** — schemes work. Set them per section in the theme editor (or in the page template JSON via `"color_scheme": "scheme-2"`).
- **Not found** (older OS 2.0 themes) — the dropdown will be empty. Nothing breaks and every section still renders inheriting the page colours, but tell the member plainly that their theme predates colour schemes and they should use the **Custom background / Custom text** pickers on each section instead.

Either way the section Liquid only applies a scheme class when one is actually chosen, so an unset value always falls back to the theme's own colours.

## 4. Push + preview
```bash
shopify theme push --store <store>.myshopify.com --theme <dev-theme-id>
```
Give the member the preview URL: `https://<store>.myshopify.com/?preview_theme_id=<id>`

## 5. Create the page (unpublished)
Create a Shopify page assigned to the new template, left unpublished. Via the Admin API (`pageCreate`) if available, otherwise give the member the two-click instruction: **Online Store → Pages → Add page → Template suffix = `eca-lp-<format>`**, save as hidden/unpublished.

## 6. Hand over — always give the three links

**Every build ends with clickable links. Never just say "the page has been created" — the member should be one click from seeing and editing it.** Build them from the values you already have: the store domain, the dev theme ID, the page handle, and the page ID returned by `pageCreate`.

**1. Edit in the theme editor** (the important one — this is where they change copy, images and blocks):
```
https://<store>.myshopify.com/admin/themes/<theme_id>/editor?previewPath=%2Fpages%2F<handle>
```
Opens the theme editor with *this page* loaded, so every ECA LP section is right there in the left panel.

**2. Preview the page** (see it as a customer, on the dev theme):
```
https://<store>.myshopify.com/pages/<handle>?preview_theme_id=<theme_id>
```

**3. Page settings in admin** (title, SEO fields, publish toggle):
```
https://<store>.myshopify.com/admin/pages/<page_id>
```

Label them plainly, e.g.:
> **Edit the page** (theme editor) → *link*
> **Preview it** (as a customer) → *link*
> **Page settings** (title, SEO, publish) → *link*

Then: what to review · any remaining `{{PLACEHOLDER}}` items and the shot needed for each · how to publish (publish the page, then the theme) · **and point the ad's destination URL at the new page**.

**If you couldn't create the page via the API**, still give links 1 and 2 (they work as soon as the page exists) plus the two-click instruction to create it.

---

## Conventions for the section files

- **Every piece of content is a setting.** No hardcoded copy in Liquid. Use `text`, `richtext`, `image_picker`, `url`, `select`, `checkbox`, `color`, `product`, `video` setting types, each with a clear `label` and a sensible `default`.
- **Repeatable content uses blocks** (`{% for block in section.blocks %}`) with `max_blocks` — so the member can add/remove/reorder items in the theme editor.
- **Inherit the theme**, don't fight it: no hardcoded fonts or brand colours. Use `color_scheme` settings where the theme supports them, `rem`/relative units, and let headings inherit. Keep custom CSS scoped inside the section with a `.eca-lp-*` prefix.
- **Use native features first** — the theme's own product form / buy buttons for purchase, the review app's block for reviews, `image_url`/`image_tag` filters with `loading="lazy"` and `srcset` for images, native `<details>/<summary>` for accordions. Only hand-roll what nothing native covers.
- **Always include `{% schema %}`** with `presets` so the section can also be added to other templates.
- **Accessibility**: real heading hierarchy (one `h1` — the hero), `alt` on every image, buttons as `<a>`/`<button>` with discernible text.
- **Performance**: `loading="lazy"` on every below-fold image, no external JS/CSS frameworks, no web fonts.
