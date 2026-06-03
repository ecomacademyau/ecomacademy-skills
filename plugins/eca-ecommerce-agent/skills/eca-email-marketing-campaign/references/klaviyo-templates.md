# Klaviyo Push Workflow & Block Patterns

> **This file is brand-agnostic.** The brand-specific config (master template ID, sender defaults, audience) lives in `../klaviyo-config.md`. Read that first when pushing to Klaviyo — this file describes *how* to push; `klaviyo-config.md` describes *which template* and *where to send from*.

---

## One master template, three block patterns

This skill names three email styles — Banner+text+products, Text only, Banner+CTA+text — but they are **not** three separate Klaviyo templates. They are three ways of arranging DND blocks inside the **single master template** the brand has set in `klaviyo-config.md`.

**Why one master, not three:**
- Cloning one master is faster than maintaining three
- Brand styling (fonts, colours, header, footer, social block, unsubscribe) lives in one place
- If brand visuals change, there's only one template to update

Cloning the master gives you a fresh DND template that already carries the brand look. You then arrange blocks inside the content area to match the email's role.

---

## The DND-only rule (non-negotiable by default)

Every email this skill creates in Klaviyo must be drag-and-drop (SYSTEM_DRAGGABLE / DND), never CODE-type HTML.

**Why:** The brand owner needs to edit campaigns in Klaviyo's visual editor after Claude creates them. CODE templates open as raw HTML — not visually editable. DND templates can be edited block-by-block by anyone on the team.

**What this means in practice:**

- Use `klaviyo_clone_email_template` from a DND source (the brand's master, configured in `klaviyo-config.md`, must be DND)
- Use `klaviyo_update_dnd_email_template` to modify cloned DND templates
- If creating from scratch (rare), use `klaviyo_create_dnd_email_template`, never `klaviyo_create_email_template`
- When listing templates to pick a master, filter by `editorType === "SYSTEM_DRAGGABLE"` only — skip CODE templates entirely

If a different brand explicitly wants CODE templates, they can override this rule by removing it from their fork of `klaviyo-config.md`. The default for any brand using this skill is DND.

---

## DND block patterns per style

When cloning the master, arrange the inner content blocks to match the email's role. The three styles are:

### Style 1 — Banner + text + products

For Email 1 (Launch) and Email 3 (Proof) in a 4-email themed arc; Emails 3, 4, 5 in a 7-email promo arc.

DND block order inside the master content slot (using native block types):

1. **`header` block** — logo + nav links (already in the master)
2. **`image` block** — hero banner (600px wide, mobile-aware). Use a real Image block with a Klaviyo-hosted `assetId` — upload via `klaviyo_upload_image_from_url` first if the image isn't already in the library
3. **`text` blocks** — heading + body copy (~80–150 words, broken into separate text blocks for spacing)
4. **`button` block** — single primary CTA with `content` (button label) and `properties.href` (destination URL)
5. **`product` block** (or a 2/3-up product grid via columns) — 2–4 products *(optional, add for product-heavy emails)*
6. *(Optional)* **`text` block** — short note under products

The block types listed above are all native Klaviyo DND block types — Klaviyo's visual editor recognises them as their proper widgets (Header, Image, Text, Button, Product, Social) so the user can edit them with the right controls in the UI.

### Style 2 — Text only

For Email 2 (Educate) in the 4-email themed arc; Email 7 (Last Chance) in the 7-email promo arc.

DND block order:

1. **Text block** — full copy (no banner)
2. **Button block** — single CTA inline
3. *(Optional)* **Text block** — signature line ("— Founder Name, Brand")

Keep the layout minimal. The whole point is that the writing carries the email.

### Style 3 — Banner + CTA + text

For Email 4 (Offer) in the 4-email themed arc; Emails 1, 2, 6 in the 7-email promo arc.

DND block order:

1. **Image block** — hero banner with the offer/product visible
2. **Button block** — single big CTA
3. **Text block** — supporting copy (under the button, not above)

The button comes BEFORE the text — that's the point of this style. Click first, read second.

---

## Push-to-Klaviyo workflow

Once a campaign plan is locked (see Stage 5 in `SKILL.md`), the workflow to push it into Klaviyo as drafts:

### Step 0 — Pre-flight checks

- Read `klaviyo-config.md` to get the brand's master template ID, sender defaults, and any audience config
- Confirm hero images exist for each email (uploaded to Klaviyo's image library, OR hosted at a stable URL Claude can pass to `klaviyo_upload_image_from_url`)
- Confirm the user wants drafts (not scheduled sends) — Claude never schedules sends without explicit approval
- Confirm campaign date/time, send-from email (per `klaviyo-config.md`), and audience (which list/segment)

### Step 1 — Clone the master template for each email

For each email in the campaign:

```
klaviyo_clone_email_template(
  templateId: <master template ID from klaviyo-config.md>,
  newName: "<campaign-slug> — Email N — <subject-line>"
)
```

Example new name: `Made in Melbourne — Email 1 — Yes, we make it here`

This produces a fresh DND template per email. Capture each new template ID.

### Step 2 — Update each cloned template's content (requires API master, not a universal-block master)

Use `klaviyo_update_dnd_email_template` with the new template ID. Replace the master's placeholder blocks with the campaign-specific blocks per the style guide above.

**This step requires the master to contain NO universal blocks.** If the master has any universal blocks, this call will fail (see "universal blocks block API edits" above). Use the API master configured in `klaviyo-config.md`.

The full updated `definition` must be passed — the API replaces the whole thing, not just changed fields. So construct the definition from the existing template structure (placeholder layout from the master) and substitute:
- **Text blocks** (`type: text`): replace headline (`[HEADLINE]`) and body copy (`[BODY COPY paragraph N...]`) `data.content` HTML
- **Button block** (`type: button`): replace `data.content` (button label) and `data.properties.href` (URL)
- **Image block** (`type: image`): if a real campaign hero image is uploaded to Klaviyo (via `klaviyo_upload_image_from_url`, returning an `id` to use as `assetId`), replace `data.properties.src` and `data.properties.assetId`. If no hero is ready, leave the placeholder image in place — the user will swap it in Klaviyo's visual editor.
- **Header block** (`type: header`): typically left as-is (logo + nav links don't change per campaign). Update only if the campaign needs a different nav.

### Step 3 — Create the campaign

```
klaviyo_create_campaign(
  name: "<campaign-slug> — Email N",
  audiences: [list/segment IDs per klaviyo-config.md],
  send-from: <from-email per klaviyo-config.md>,
  subject: "<subject line — primary variant>"
)
```

Capture the campaign ID and its messageId.

### Step 4 — Attach the template to the campaign message

```
klaviyo_assign_template_to_campaign_message(
  messageId: <from step 3>,
  templateId: <cloned template ID from step 1>
)
```

### Step 5 — Report back

For each email pushed, report to the user:
- Campaign name + ID
- Template name + ID
- Direct link to the campaign draft in Klaviyo (format: `https://www.klaviyo.com/campaign/<campaign-id>/preview`)
- Any warnings (image not uploaded, link not set, etc.)

Leave campaigns as drafts. The user reviews and schedules them in Klaviyo.

---

## Important constraint: universal blocks block API edits

If a Klaviyo template uses **universal blocks** (reusable shared components — typically the social grid, footer text, header logo), the `klaviyo_update_dnd_email_template` API will reject any update with the error: *"Template {ID} contains universal blocks and cannot be updated."* This is by design — universal blocks are shared across multiple templates so they can't be modified per-template via API.

**The fix:** the brand needs a dedicated API-friendly master template (the one configured in `klaviyo-config.md`) that contains **NO universal blocks**. Every block in the master must be a regular DND block. This unlocks full API editing — content, CTAs, images can all be populated programmatically.

**Trade-off:** without universal blocks, the master loses the "edit once, propagate everywhere" benefit. The mitigation is to maintain TWO templates:

1. **API master** (in `klaviyo-config.md`) — no universal blocks, used for the push workflow
2. **Visual reference master** (also in `klaviyo-config.md`, as the secondary entry) — can have universal blocks, used for manually-built campaigns or as the visual gold standard

If the visual reference changes meaningfully, the API master is updated to match (manually in Klaviyo, or by recreating it via API).

---

## What this workflow must NEVER do

- Create CODE-type templates (DND only — see the DND-only rule above)
- Schedule sends without explicit user approval
- Modify the master template directly — always clone, never edit the source
- Overwrite existing templates by reusing names — always create new ones per campaign
- Hardcode brand-specific values (template IDs, from-addresses, list IDs) into this workflow file — those live in `klaviyo-config.md`
