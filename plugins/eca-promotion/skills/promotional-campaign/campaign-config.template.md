# Campaign Config — TEMPLATE (UNCONFIGURED)

<!-- UNCONFIGURED: brand setup not yet done. The skill detects this marker and runs the
     first-run Brand Setup before building anything. Once a brand's details are filled in
     and this marker/heading is removed, the skill treats the config as ready. -->

> This is the blank template that ships with the skill. On first use, the skill walks you
> through entering your brand's details and fills this file in. You can also edit it directly.
> **This is the only file that differs between brands** — everything else in the skill is generic.

**Last updated:** [date]
**Maintained by:** [your name / email]

---

## Store

- **Brand:** [brand name]
- **Storefront:** [https://yourstore.com]
- **Platform:** [Shopify / other]
- **Currency / market:** [e.g. AUD, Australia]
- **Timezone for scheduling:** [e.g. AEST/AEDT]
- **Shop-all / sale landing:** [URL or "create a sale collection per campaign"]

## Offer defaults

- **Discount creation:** [e.g. create as staged/inactive in Shopify by default; never activate without approval]
- **Typical mechanics you run:** [% off / multi-buy / bundle / free shipping threshold]
- **Code style:** [e.g. short, uppercase, event-named]
- **Eligibility default:** [sitewide / category / specific SKUs]

## Klaviyo (or other email/SMS platform)

> Needed only if Email/SMS is in scope. The push workflow clones a master DND template per email.

### Primary — API master (used by the push workflow)
- **ID:** [template ID]
- **Name:** [template name]
- **Editor type:** SYSTEM_DRAGGABLE (DND) — must have NO universal blocks so the API can populate it.

### Visual reference master (optional)
- **ID / Name:** [if you keep a separate visually-built master]

### Sender defaults
- **From email:** [hello@yourstore.com]
- **From name:** [brand]
- **Reply-to:** [email]

### Image hosting
- Upload images to the platform to get an assetId before referencing them in image blocks.

## Audiences / segments

> Confirm exact list/segment IDs. Used to target each phase.

| Phase | Audience | ID |
|-------|----------|----|
| Early-access | [VIP / existing customers] | [id] |
| Public launch | [all subscribers] | [id] |
| Mid-sale sends | [engaged subscribers] | [id] |
| Last chance | [all subscribers] | [id] |

## SMS

- **Provider:** [Klaviyo SMS / other] — confirm before scheduling any SMS.
- SMS fires on the big beats only (Early Access, Launch, Last Chance).

## Paid ads accounts

> Needed only if Paid ads are in scope.

| Channel | Account / notes |
|---------|-----------------|
| Meta | [ad account / pixel] |
| TikTok | [ad account / pixel] |
| Google | [account] |

## Brand voice & visuals

> If you also use the `brand-intelligence` skill, the full identity lives there. Otherwise capture the essentials here.

- **Tone in a sentence:** [e.g. warm, confident, no-gimmick]
- **Primary accent colour:** [#hex]
- **Background / secondary:** [#hex]
- **Body text:** [#hex]
- **Display font / body font:** [fonts]
- **Avoid (visual/voice):** [shouty clearance styling, banned phrases, etc.]
