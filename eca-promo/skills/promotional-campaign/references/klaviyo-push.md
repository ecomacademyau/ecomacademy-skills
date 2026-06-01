# Klaviyo Push Workflow (plan + build mode)

How to push the locked email arc into Klaviyo as **editable drafts**. Only run this after the brief is locked and the user has chosen plan+build. The brand-specific master template ID, sender, and audiences live in `campaign-config.md` — read it first.

## The DND-only rule (non-negotiable by default)

Every email this skill creates in Klaviyo must be drag-and-drop (**SYSTEM_DRAGGABLE / DND**), never CODE-type HTML. The brand owner edits campaigns in Klaviyo's visual editor after creation; CODE templates open as raw HTML and can't be edited block-by-block.

In practice:
- Clone from the DND **API master** in `campaign-config.md` (`klaviyo_clone_email_template`).
- Modify clones with `klaviyo_update_dnd_email_template`.
- If creating from scratch (rare), use `klaviyo_create_dnd_email_template` — never `klaviyo_create_email_template`.
- When listing templates, only consider `editorType === "SYSTEM_DRAGGABLE"`.

## Why one master, three block patterns

The three template styles (Banner+text+products, Text only, Banner+CTA+text) are **block arrangements inside the one master**, not three templates. Cloning one master keeps brand styling (fonts, colours, header, footer, social, unsubscribe) in one place.

**Universal blocks block API edits.** If the master contains universal blocks, `klaviyo_update_dnd_email_template` rejects the update. That's why `campaign-config.md` names a dedicated **API master with no universal blocks** for this workflow (and a separate visual-reference master for manual builds).

## Block patterns per style

**Style 1 — Banner + text + products:** `header` → `image` (hero, needs a Klaviyo-hosted `assetId`) → `text` (headline + body) → `button` (single CTA) → `product` grid (2–4) → optional `text`.

**Style 2 — Text only:** `text` (full copy) → `button` (one CTA) → optional `text` (signature).

**Style 3 — Banner + CTA + text:** `image` (hero with offer visible) → `button` (big CTA) → `text` (supporting copy, AFTER the button).

All are native Klaviyo DND block types so they edit with the right widgets in the UI.

## Workflow

### Step 0 — Pre-flight
- Read `campaign-config.md`: API master ID, sender, audience IDs.
- Confirm hero images exist (uploaded to Klaviyo's library, or at a stable URL to pass to `klaviyo_upload_image_from_url`). Klaviyo static Image blocks need **both** `src` and `assetId`.
- Confirm the user wants **drafts** (never schedule sends without explicit approval), plus campaign date/time, from-address, and audience per email.

### Step 1 — Clone the master per email
```
klaviyo_clone_email_template(templateId: <API master ID>, newName: "<slug> — Email N — <subject>")
```
Capture each new template ID.

### Step 2 — Populate each clone
`klaviyo_update_dnd_email_template` with the new ID. Pass the FULL definition (the API replaces the whole thing). Substitute per the style: text blocks (headline + body), button (`content` label + `properties.href`), image (`src` + `assetId` if a hero is uploaded; else leave the placeholder for the user to swap). Header/footer typically unchanged.

### Step 3 — Create the campaign (draft)
```
klaviyo_create_campaign(name, audiences: [IDs per config], send-from: <config>, subject: <primary variant>)
```
Capture campaign ID + messageId.

### Step 4 — Attach the template
```
klaviyo_assign_template_to_campaign_message(messageId, templateId: <clone ID>)
```

### Step 5 — Report back
Per email: campaign name + ID, template name + ID, preview link (`https://www.klaviyo.com/campaign/<id>/preview`), and any warnings (image not uploaded, link missing). Leave everything as drafts for the user to review and schedule.

## Never
- Create CODE templates (DND only).
- Schedule sends or activate without explicit approval.
- Edit the master directly — always clone.
- Reuse names / overwrite existing templates.
- Hardcode brand values here — they live in `campaign-config.md`.

## SMS and the Shopify discount
- **SMS:** confirm the provider in `campaign-config.md` before scheduling; plan the copy regardless. Klaviyo SMS messages attach to a campaign similarly if that's the provider.
- **Shopify discount:** create it **staged/inactive** (auto-activates on the start date) unless told otherwise. The code, value, eligibility, and expiry must match the brief and the email copy exactly.
