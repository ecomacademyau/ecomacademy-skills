# Klaviyo Config — [YOUR BRAND]

> **Brand-specific config — placeholder.** Fill this in with your brand's Klaviyo setup
> before running the push-to-Klaviyo workflow. Everything else in the skill is brand-agnostic.
> See `klaviyo-config.template.md` for the full annotated structure.

**Status:** NOT YET CONFIGURED.

## Master templates

### Primary — API master (used for the clone -> update -> assign workflow)
- **ID:** `[TEMPLATE_ID]`
- **Name:** `[Template name]`
- **Editor type:** `SYSTEM_DRAGGABLE` (DND)  <!-- must be DND so the API can populate body content -->
- **Universal blocks:** [None recommended — keep every block a regular DND block]
- **What's in it:** [Header / hero image / headline + body text / CTA button / footer + socials / unsubscribe]
- **Brand fonts & colours:** [body font, display font, primary hex, background hex]

### Secondary — Visual reference (optional)
- **ID:** `[TEMPLATE_ID]`
- **Name:** `[Template name]`

## Sender defaults
- **From name:** [Brand]
- **From email / reply-to:** [hello@yourbrand.com]

## Audience / lists & segments
- **Default send audience:** [list or segment name + ID]
- **Suppressions:** [any standard exclusions]
