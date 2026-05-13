---
description: Connect a Shopify store via the Shopify CLI, duplicate the live theme into a development theme, and install a high-converting product page template (ECA PDP) into it. Built for Shopify's Horizon theme architecture. Use when the user says "install ECA PDP", "build me a high-converting product page", "set up the conversion product template", or asks to wire up the ECA PDP skill on a Shopify store.
---

# ECA PDP — Skill instructions

Invoked as `/eca-pdp:install` or via natural language.

You are helping a Shopify merchant install a research-backed, high-converting product page template ("ECA PDP") into a duplicated copy of their live theme. **Never push changes to the live theme** — always work in a development theme.

The skill ships with a complete set of Horizon-native theme files in `theme-files/` (relative to this skill's directory). Your job is to install Shopify CLI if missing, authenticate the user, duplicate their live theme into a safe development copy, copy the ECA PDP files into it, and push the result.

---

## Step 0 — Confirm intent and gather context

Before doing anything, **briefly** confirm with the user:

1. The store domain (e.g. `mystore.myshopify.com`). Ask if not provided.
2. That you'll be creating a **new unpublished development theme** that's a clone of their live theme. Nothing will change on the live storefront.
3. The current working directory will be used as the local workspace. Confirm or `cd` somewhere appropriate.

Then ask one final question:

> **"Is your live theme based on Shopify's Horizon? (If you're not sure, I can check.)"**

The ECA PDP template files are Horizon-native. If the user is not on Horizon (e.g. Dawn, Sense, Impulse, custom), the install will succeed but several blocks reference Horizon-specific blocks (`_product-details`, `_product-media-gallery`, `accelerated-checkout`, `accordion` / `_accordion-row`, `review`, `_product-card`, `_divider`). On non-Horizon themes, those will render as missing-block warnings in the theme editor. In that case, warn the user and offer to abort.

You can detect the theme name later via `shopify theme list --json` and check the `name` field for "Horizon" — but the user's answer is faster.

---

## Step 1 — Install / verify Shopify CLI

Run:

```bash
shopify version
```

- If it returns a version → continue.
- If the command is not found, install via one of:
  - **macOS (Homebrew):** `brew install Shopify/shopify/shopify-cli`
  - **Any platform (npm):** `npm install -g @shopify/cli@latest`
  - **Windows / others:** point user to https://shopify.dev/docs/api/shopify-cli

Ask the user which they prefer if it's not obvious from their system. Show the command, ask permission before running. After install, re-run `shopify version` to confirm.

**Common gotchas:**
- On macOS, `brew install Shopify/shopify/shopify-cli` may take a minute.
- If npm install fails with EACCES, prefer `npx @shopify/cli@latest theme list --store=...` instead of forcing a global install with sudo.

---

## Step 2 — Authenticate with the store

The CLI uses browser-based OAuth — no API keys to copy.

```bash
shopify theme list --store=<store-domain>
```

On first run, this opens the browser and asks the user to log in to the Partner / store admin. After authentication, it prints the list of themes in the store.

- Pass `--store=<store-domain>` so the user doesn't have to pick a store interactively.
- Use `--json` to get parseable output:

```bash
shopify theme list --store=<store-domain> --json
```

Parse the JSON. Find the theme where `"role": "main"` — that's the live theme. Note its `id` and `name`.

If `shopify theme list` errors with auth issues, run:

```bash
shopify auth logout
shopify theme list --store=<store-domain>
```

…and let the browser auth happen again.

---

## Step 3 — Duplicate the live theme

There are two reliable methods. **Prefer Method A** (the dedicated duplicate command). Fall back to Method B if it fails.

### Method A — `shopify theme duplicate` (preferred)

```bash
shopify theme duplicate \
  --store=<store-domain> \
  --theme=<live-theme-id> \
  --name="ECA Dev — <YYYY-MM-DD>"
```

The duplicate appears as an unpublished theme. Re-list themes to confirm and capture the new theme's `id`:

```bash
shopify theme list --store=<store-domain> --json
```

### Method B — Pull live → push as new unpublished theme

If `theme duplicate` is unavailable in the user's CLI version:

```bash
mkdir eca-dev-theme && cd eca-dev-theme

shopify theme pull \
  --store=<store-domain> \
  --live

shopify theme push \
  --store=<store-domain> \
  --unpublished \
  --json \
  --theme="ECA Dev — <YYYY-MM-DD>"
```

The final `--json` push prints the new theme ID. Capture it.

> ⚠ **Never run `shopify theme push --live` or `shopify theme publish`** in this flow. Both will overwrite the merchant's storefront.

---

## Step 4 — Pull the dev theme locally

Whichever method you used in Step 3, now make sure you have the dev theme's files on disk so you can drop the ECA PDP files in:

```bash
mkdir -p eca-dev-theme && cd eca-dev-theme
shopify theme pull \
  --store=<store-domain> \
  --theme=<dev-theme-id> \
  --force
```

The `--force` flag overwrites the working directory cleanly. After this completes, you should see `sections/`, `snippets/`, `blocks/`, `templates/`, `assets/`, `config/`, `layout/`, `locales/` inside the working directory.

If `blocks/` does not exist, the theme is not Horizon (Horizon introduced top-level `blocks/`). Warn the user and offer to abort the ECA PDP install.

---

## Step 5 — Copy ECA PDP files into the dev theme

The ECA PDP files ship inside this skill's directory at `theme-files/`. The absolute path is:

```
{SKILL_DIR}/theme-files/
```

…where `{SKILL_DIR}` is the directory containing this `SKILL.md`. From the user's `eca-dev-theme` working directory, copy in:

```bash
SKILL_DIR="<absolute path to .claude/skills/eca-pdp>"

mkdir -p sections snippets blocks templates

cp -v "$SKILL_DIR/theme-files/sections/"*.liquid    sections/
cp -v "$SKILL_DIR/theme-files/snippets/"*.liquid    snippets/
cp -v "$SKILL_DIR/theme-files/blocks/"*.liquid      blocks/
cp -v "$SKILL_DIR/theme-files/templates/"*.json     templates/
```

The files this skill installs:

**sections/** (each is a configurable, reorderable section in the theme editor)
- `eca-value-props.liquid` — objection-busters / value propositions, icon + text grid
- `eca-how-to-use.liquid` — numbered steps with image + heading + body
- `eca-ugc-gallery.liquid` — customer photo / video grid
- `eca-faq.liquid` — FAQ accordion with FAQPage structured data
- `eca-reviews-embed.liquid` — drop-in for Judge.me / Loox / Stamped / Yotpo / Okendo / Shopify Reviews
- `eca-founder.liquid` — about-the-founder section with photo + signature

**blocks/** (Horizon-native blocks, placeable inside `_product-details`)
- `eca-pitch.liquid` — reads the `custom.pitch` product metafield with fallback
- `eca-trust-row.liquid` — shipping + guarantee + secure-checkout icon row under ATC
- `eca-sizing-guide-link.liquid` — opens a `<dialog>` showing `custom.sizing_guide` metafield content

**snippets/**
- `eca-trust-icon.liquid` — inline SVG icon set (truck, shield, leaf, etc.)
- `eca-product-schema.liquid` — Product JSON-LD with reviews + offers

**templates/**
- `product.eca-pdp.json` — wires Horizon's `product-information` section with ECA blocks in the buy box, then orders the six ECA sections in the proven high-converting layout

After copying, verify nothing was missed:

```bash
ls -1 sections/eca-*.liquid snippets/eca-*.liquid blocks/eca-*.liquid templates/product.eca-pdp.json
```

---

## Step 6 — Push the ECA PDP files back to the dev theme

Push in **two phases**. This makes the install resilient: even if the template JSON fails to register (e.g. one referenced block has a schema error), the section/block/snippet files are already in the theme and the merchant can add them manually via the theme editor.

### Phase 6a — Push sections, blocks, snippets first

```bash
shopify theme push \
  --store=<store-domain> \
  --theme=<dev-theme-id> \
  --path=<working-dir> \
  --json \
  --force \
  --only="sections/eca-*.liquid" \
  --only="snippets/eca-*.liquid" \
  --only="blocks/eca-*.liquid"
```

If this push reports errors on a specific file (rare — only happens if liquid syntax is malformed), capture the filename, **continue** to phase 6b, and tell the user at the end which file failed. They can still add the working blocks/sections manually in the editor.

### Phase 6b — Push the template JSON

```bash
shopify theme push \
  --store=<store-domain> \
  --theme=<dev-theme-id> \
  --path=<working-dir> \
  --json \
  --force \
  --only="templates/product.eca-pdp.json"
```

If **this** push fails (most commonly: template references a block type that didn't make it in phase 6a), the merchant can still assemble the page manually in the theme editor — every ECA section and block is already in the editor's library from phase 6a. Tell the user what failed and that they can:
1. Either remove the offending block from `templates/product.eca-pdp.json` locally and re-push,
2. Or assign their default product template to a product, switch it to a duplicated copy via theme editor, and drag in the ECA sections individually.

The whole point of two-phase push: a failed template never blocks the merchant from accessing the section library.

### Verify

After both phases, confirm everything landed:

```bash
shopify theme info --theme=<dev-theme-id> --json --store=<store-domain> 2>&1 | head -5
```

Then list local files actually shipped:

```bash
ls -1 <working-dir>/sections/eca-*.liquid <working-dir>/snippets/eca-*.liquid <working-dir>/blocks/eca-*.liquid <working-dir>/templates/product.eca-pdp.json
```

---

## Step 7 — Tell the user what to do next

Print these next steps **and read them aloud** to the user. Show them as a numbered list:

1. **Create the metafields.** Open `Settings → Custom data → Products` and add the definitions documented in `METAFIELDS.md` (in the skill folder). The `custom.pitch` and `custom.sizing_guide` definitions are the most impactful.
2. **Assign the template.** Open any product → right sidebar → **Theme template** → select **ECA PDP**. Save.
3. **Open the theme editor on the dev theme.** Run `shopify theme open --theme=<dev-theme-id> --editor` or go to `Online Store → Themes → ECA PDP Dev → Customize`. Top-bar template selector → **Products → ECA PDP**.
4. **Wire up the reviews app.** Open the `ECA Reviews` section and pick the matching provider (Judge.me / Loox / etc.). Save.
5. **Preview the dev theme.** Click "Preview" in the theme list. Test the buy box, sticky behavior, accordion rows, sizing guide drawer, and scroll to FAQ.
6. **Publish when happy.** When the merchant is satisfied, they can publish the dev theme from `Online Store → Themes → ⋯ → Publish`. **You should not run `shopify theme publish` for them** — that's a destructive action they should do themselves.

---

## Troubleshooting

**"Missing block: eca-pitch" warnings in the theme editor**
→ The block files didn't make it into the theme. Re-run Step 5/6, paying attention to the `blocks/` folder copy.

**"Liquid syntax error: unknown filter 'metafield_tag'"**
→ Theme is on a very old Liquid version. Horizon supports `metafield_tag`. Confirm the duplicated theme is actually Horizon via `shopify theme list --json` and look at `processing` / `theme_store_id`.

**`shopify theme duplicate` not found**
→ Update CLI: `npm install -g @shopify/cli@latest`. Or fall back to Method B in Step 3.

**Buy-box stars don't show**
→ The `review` block reads `reviews.rating` / `reviews.rating_count` product metafields. Either install a reviews app that populates them (Judge.me, Loox, Stamped, Yotpo, Okendo all do), or remove the `stars` block from the template.

**Sizing guide trigger doesn't appear**
→ The trigger auto-hides unless the product has an option called `Size` OR the block setting `show_always` is checked.

---

## What this skill does NOT do

- It does not publish the dev theme. The user does that.
- It does not edit the customer's live theme. Ever.
- It does not create metafields automatically — Shopify CLI cannot create metafield definitions; the merchant must add them in `Settings → Custom data → Products`. `METAFIELDS.md` documents which ones to create.
- It does not install or configure a reviews app. The section supports six common ones via dropdown.

---

## When the user asks for variations

Common follow-ups and how to handle them:

- **"Can you change the section order?"** → Edit the `"order"` array in `templates/product.eca-pdp.json`, push the template only with `--only="templates/product.eca-pdp.json"`.
- **"Can I have two FAQ sections?"** → In the JSON template, copy the `eca_faq` section, give it a new key, add the new key to `"order"`. Push.
- **"Can I disable the founder section?"** → Two options: (a) remove `eca_founder` from the `"order"` array, or (b) tell the user they can remove it in the theme editor (no code changes needed).
- **"My theme isn't Horizon — can I still use this?"** → Honestly no, not without significant rework. The buy-box blocks (`_product-details`, `accordion`, `review`, `accelerated-checkout`) are Horizon-specific. The six ECA sections will work in any OS 2.0 theme, but the template JSON won't. Offer to install only the six sections plus an OS-2.0-friendly product template if requested.
