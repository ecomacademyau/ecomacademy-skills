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
shopify theme pull \
  --store=<store-domain> \
  --theme=<dev-theme-id> \
  --path=<working-dir> \
  --force
```

After this completes, the working directory should contain `sections/`, `snippets/`, `templates/`, `assets/`, `config/`, `layout/`, `locales/` (and possibly `blocks/`).

---

## Step 4.5 — Detect theme variant

Determine which install path to take based on the pulled theme's file structure. Run this check from the working directory:

```bash
THEME_VARIANT="unknown"

if [ -f "sections/product-information.liquid" ] && [ -f "blocks/_product-details.liquid" ]; then
  THEME_VARIANT="horizon"
elif [ -f "templates/product.json" ]; then
  THEME_VARIANT="os2-generic"
elif [ -f "templates/product.liquid" ]; then
  THEME_VARIANT="legacy"
fi

echo "Theme variant: $THEME_VARIANT"
```

Interpret the result:

| Variant | What it means | Install path |
|---|---|---|
| `horizon` | Horizon-native theme. All ECA features supported. | **Step 5a + 6a + 6b** (full install) |
| `os2-generic` | OS 2.0 theme but not Horizon (Dawn, Sense, Refresh, Impulse, most paid themes). | **Step 5b + 6a + 6b** (fallback: append ECA sections to the merchant's existing product template) |
| `legacy` | Old theme with `product.liquid` only. OS 2.0 is required for ECA PDP. | **Step 5c** — abort with clear message |
| `unknown` | Can't detect. Ask the user what theme this is, then pick a path. | Ask before proceeding |

Tell the user which variant you detected and what path you're about to take.

---

## Step 5a — Horizon full install (variant = `horizon`)

The ECA PDP files ship inside this skill's directory at `theme-files/`. From the working directory:

```bash
SKILL_DIR="<absolute path to .claude/skills/eca-pdp or plugin cache equivalent>"

mkdir -p sections snippets blocks templates

cp -v "$SKILL_DIR/theme-files/sections/"*.liquid    sections/
cp -v "$SKILL_DIR/theme-files/snippets/"*.liquid    snippets/
cp -v "$SKILL_DIR/theme-files/blocks/"*.liquid      blocks/
cp -v "$SKILL_DIR/theme-files/templates/"*.json     templates/
```

What gets installed:

| Folder | Files | Why |
|---|---|---|
| `sections/` | `eca-value-props`, `eca-how-to-use`, `eca-ugc-gallery`, `eca-faq`, `eca-reviews-embed`, `eca-founder` | Six configurable sections |
| `blocks/` | `eca-pitch`, `eca-trust-row`, `eca-sizing-guide-link` | Horizon-native blocks for the buy box |
| `snippets/` | `eca-trust-icon`, `eca-product-schema` | Helpers |
| `templates/` | `product.eca-pdp.json` | Wires `product-information` section with ECA blocks + the six ECA sections in proven order |

Skip to Step 6.

---

## Step 5b — Non-Horizon OS 2.0 fallback (variant = `os2-generic`)

In this mode we **never replace** the theme's existing product template. We create a new `product.eca-pdp.json` based on the theme's `templates/product.json` and append the six ECA marketing sections after the merchant's existing buy box.

**Copy ECA sections + the trust-icon snippet** (skip blocks and the Horizon-specific JSON template):

```bash
SKILL_DIR="<absolute path to skill or plugin cache>"

mkdir -p sections snippets templates

cp -v "$SKILL_DIR/theme-files/sections/"*.liquid          sections/
cp -v "$SKILL_DIR/theme-files/snippets/eca-trust-icon.liquid" snippets/
```

**Generate the merged template.** Inline this with python3 — it strips Shopify's `//` and `/* */` JSON comments, copies the existing product.json, renames it, and appends the six ECA sections:

```bash
python3 <<'PY'
import json, re, pathlib

src = pathlib.Path("templates/product.json").read_text()

# Strip /* ... */ and // line comments that Shopify allows but stdlib json doesn't
src = re.sub(r"/\*.*?\*/", "", src, flags=re.S)
src = re.sub(r"^\s*//.*$", "", src, flags=re.M)

tpl = json.loads(src)

# 1) Set the customisable name shown in admin
tpl["name"] = "ECA PDP"

# 2) Define the six ECA marketing sections to append below the buy box
eca_sections = {
    "eca_value_props": {
        "type": "eca-value-props",
        "blocks": {
            "p1": {"type": "prop", "settings": {"icon": "check", "heading": "Backed by results", "body": "<p>One short sentence about a measurable benefit.</p>"}},
            "p2": {"type": "prop", "settings": {"icon": "leaf", "heading": "Clean ingredients", "body": "<p>Address the #1 objection in one line.</p>"}},
            "p3": {"type": "prop", "settings": {"icon": "shield", "heading": "30-day guarantee", "body": "<p>Tell them exactly what happens if they don't love it.</p>"}},
            "p4": {"type": "prop", "settings": {"icon": "heart", "heading": "Loved by 10,000+", "body": "<p>Social proof in plain numbers.</p>"}}
        },
        "block_order": ["p1", "p2", "p3", "p4"],
        "settings": {"eyebrow": "Why people choose this", "heading": "Built to do one thing — really well", "columns": 4, "padding-block-start": 64, "padding-block-end": 64}
    },
    "eca_how_to_use": {
        "type": "eca-how-to-use",
        "blocks": {
            "s1": {"type": "step", "settings": {"heading": "Open it up", "body": "<p>One sentence about the first step.</p>"}},
            "s2": {"type": "step", "settings": {"heading": "Apply or use it", "body": "<p>One sentence about the second step.</p>"}},
            "s3": {"type": "step", "settings": {"heading": "Enjoy the results", "body": "<p>One sentence about the outcome.</p>"}}
        },
        "block_order": ["s1", "s2", "s3"],
        "settings": {"eyebrow": "How it works", "heading": "Three simple steps", "columns": 3, "padding-block-start": 64, "padding-block-end": 64}
    },
    "eca_ugc": {
        "type": "eca-ugc-gallery",
        "blocks": {
            "u1": {"type": "media", "settings": {"handle": "@customer1"}},
            "u2": {"type": "media", "settings": {"handle": "@customer2"}},
            "u3": {"type": "media", "settings": {"handle": "@customer3"}},
            "u4": {"type": "media", "settings": {"handle": "@customer4"}}
        },
        "block_order": ["u1", "u2", "u3", "u4"],
        "settings": {"eyebrow": "Real people, real results", "heading": "From our community", "columns": 4, "padding-block-start": 64, "padding-block-end": 64}
    },
    "eca_faq": {
        "type": "eca-faq",
        "blocks": {
            "q1": {"type": "faq", "settings": {"question": "How long does shipping take?", "answer": "<p>Orders ship within 1 business day.</p>", "open_by_default": True}},
            "q2": {"type": "faq", "settings": {"question": "What's your return policy?", "answer": "<p>30 days, no questions asked.</p>"}},
            "q3": {"type": "faq", "settings": {"question": "Is this safe for sensitive use?", "answer": "<p>Address the top safety / suitability question.</p>"}},
            "q4": {"type": "faq", "settings": {"question": "How do I use it?", "answer": "<p>Summarise in two sentences.</p>"}}
        },
        "block_order": ["q1", "q2", "q3", "q4"],
        "settings": {"heading": "Frequently asked questions", "padding-block-start": 64, "padding-block-end": 64}
    },
    "eca_reviews": {
        "type": "eca-reviews-embed",
        "settings": {"provider": "judgeme", "heading": "What customers are saying", "padding-block-start": 64, "padding-block-end": 64}
    },
    "eca_founder": {
        "type": "eca-founder",
        "settings": {
            "eyebrow": "About the founder",
            "heading": "Why I built this",
            "body": "<p>Share the origin story in 2–4 short paragraphs.</p>",
            "name": "Your name",
            "title": "Founder & CEO",
            "padding-block-start": 64,
            "padding-block-end": 64
        }
    }
}

# 3) Merge into existing sections map (without clobbering existing keys).
#    Idempotent: if the merchant re-runs the skill, our keys overwrite cleanly
#    rather than stacking.
tpl.setdefault("sections", {})
for k, v in eca_sections.items():
    tpl["sections"][k] = v

# 4) Append to the order array (keep existing order intact). Skip any ECA key
#    that is already in the order so re-running doesn't create duplicates.
existing_order = tpl.get("order", [])
new_keys = [k for k in eca_sections.keys() if k not in existing_order]
rec_key = next((k for k in existing_order if "recommendation" in k.lower()), None)
if rec_key:
    idx = existing_order.index(rec_key)
    tpl["order"] = existing_order[:idx] + new_keys + existing_order[idx:]
else:
    tpl["order"] = existing_order + new_keys

# 5) Write the new template
pathlib.Path("templates/product.eca-pdp.json").write_text(
    json.dumps(tpl, indent=2)
)
print(f"Wrote templates/product.eca-pdp.json with order: {tpl['order']}")
PY
```

After this runs, `templates/product.eca-pdp.json` exists alongside the unchanged `templates/product.json`. Merchant assigns it per-product in Step 7.

**Tell the merchant clearly what they get vs miss in this mode:**
> "Your theme isn't Horizon, so I've installed a fallback. Your existing product page buy box (title, price, variants, ATC) stays exactly as-is — I've added six ECA marketing sections below it (value props, how-to-use, UGC, FAQ, reviews, founder). The Horizon-only buy-box upgrades (pitch metafield, trust row, sizing guide drawer) aren't installed because they depend on Horizon's block system. If you want the full ECA PDP buy box, you'd need to migrate to Horizon."

---

## Step 5c — Legacy theme abort (variant = `legacy`)

Tell the user:

> "Your theme uses the legacy `product.liquid` template, not OS 2.0 JSON templates. ECA PDP requires OS 2.0. Two paths forward: (1) upgrade your theme to its OS 2.0 version (most paid theme vendors offer this free), or (2) migrate to Shopify Horizon or Dawn. Once you're on OS 2.0, re-run this skill."

Delete the dev theme to avoid leaving orphan copies in the merchant's theme library:

```bash
shopify theme delete --store=<store-domain> --theme=<dev-theme-id> --force
```

Stop. Do not continue to Step 6.

---

## Verify file inventory before pushing

```bash
echo "Sections:"; ls -1 sections/eca-*.liquid 2>&1
echo "Snippets:"; ls -1 snippets/eca-*.liquid 2>&1
echo "Blocks:";   ls -1 blocks/eca-*.liquid 2>&1 || echo "(none — expected in fallback mode)"
echo "Template:"; ls -1 templates/product.eca-pdp.json 2>&1
```

---

## Step 6 — Push the ECA PDP files back to the dev theme

Push in **two phases**. This makes the install resilient: even if the template JSON fails to register (e.g. one referenced block has a schema error), the section/block/snippet files are already in the theme and the merchant can add them manually via the theme editor.

### Phase 6a — Push sections, blocks, snippets first

Build the `--only` flag list dynamically — fallback mode has no `blocks/eca-*` files, so don't pass that pattern (Shopify CLI errors on missing files):

```bash
PUSH_FLAGS=(
  --store=<store-domain>
  --theme=<dev-theme-id>
  --path=<working-dir>
  --json --force
  --only="sections/eca-*.liquid"
  --only="snippets/eca-*.liquid"
)

# Only push blocks/ if any eca-* blocks exist locally (Horizon path)
if ls blocks/eca-*.liquid 2>/dev/null | grep -q .; then
  PUSH_FLAGS+=(--only="blocks/eca-*.liquid")
fi

shopify theme push "${PUSH_FLAGS[@]}"
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
