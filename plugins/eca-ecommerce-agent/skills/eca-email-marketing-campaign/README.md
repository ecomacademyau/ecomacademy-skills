# Email Marketing Campaign — a reusable Claude skill

A Claude skill that plans and drafts email marketing campaigns using the **"Famous For" method** — every campaign is famous for one topic, and every email earns its place by selling.

This is a brand-agnostic template. The only brand-specific knowledge lives in two swappable files: `../eca-brand-intelligence/brand-data.md` (voice, products, ICP) and `klaviyo-config.md` (Klaviyo master template, sender defaults). Swap those when forking.

## What's in the folder

```
email-marketing-campaign/
├── SKILL.md                          # The Famous For framework + workflow. Same for every brand.
├── klaviyo-config.md                 # Brand-specific Klaviyo config. SWAP when forking.
├── README.md                         # This file.
└── references/
    ├── campaign-series.md            # 4-email themed arc + 7-email promo arc
    ├── template-styles.md            # The three email styles
    ├── topic-types.md                # Category / Launch / Calendar / Promo
    ├── email-checklist.md            # Pre-send checklist
    └── klaviyo-templates.md          # Brand-agnostic Klaviyo push workflow + DND block patterns
```

## What this skill does

When invoked, the skill walks through:

1. **Topic discovery** — asks what you have in mind, optionally checks Klaviyo for what's run lately
2. **Topic confirmation** — proposes 3–5 options with a "famous for" framing for each
3. **Campaign plan** — builds the 4-email or 7-email arc inline in chat
4. **Drafting** — per email: subject lines (3 variants), preview text, template style, image brief, body copy, CTA
5. **Lock and document** — produces a clean campaign plan doc once you sign off
6. **Push to Klaviyo** (optional) — clones the brand's master template per email, populates DND blocks, creates campaigns as drafts ready to schedule

## The four campaign topic types

- **Category theme** — usage occasion, flavour story, lifestyle angle
- **Product launch** — new SKU, restock, bundle, format
- **Calendar event** — Mother's Day, Christmas, EOFY, etc.
- **Promotion** — discount, free shipping, BOGO

## The two series structures

- **4-email themed arc** (Give-Give-Give-Ask) — for themed, launch, and calendar campaigns. Launch → Educate → Proof → Offer.
- **7-email promo arc** — for promotions. Early Access → Launch → Sale Products → Category → Best Sellers → Ends Soon → Last Chance.

## The three template styles

These are *block-arrangement patterns inside one master Klaviyo template*, not three separate templates:

1. Banner + text + products
2. Text only
3. Banner + CTA + text

## How it relates to the brand-intelligence skill

The email skill pulls in the brand-intelligence skill at the **drafting** stage — voice rules, product details, ICP. The two skills are designed to work together but aren't auto-coupled; the email skill stays useful even on its own.

## Key rules baked into the skill

These rules are non-negotiable in the framework:

1. **Each email stands alone.** A recipient might only see one — every email contains the full hook + reason to click. No "as mentioned last week..." callbacks.
2. **Don't repeat recent campaigns.** Check Klaviyo for the last 6–8 weeks before suggesting topics.
3. **Don't run back-to-back promos.** Space them at least 2–3 themed campaigns apart.
4. **Every email sells.** Even the "Give" emails route to product. The Asks just get progressively stronger.
5. **Always DND in Klaviyo, never CODE.** Any email created in Klaviyo must be drag-and-drop so the brand owner can edit it in the visual editor.

## Reusing for other brands

The framework, workflow, and block patterns are brand-agnostic. Two files carry brand-specific config:

### Step-by-step fork

1. **Copy this folder** to wherever the new brand's project lives.
2. **Set up the new brand's Klaviyo master template.**
   - In Klaviyo, create (or pick) one DND template that carries the brand's fonts, colours, header, footer, social block, and unsubscribe. This is the "master" — every campaign email will clone from it.
   - Make sure it's drag-and-drop (SYSTEM_DRAGGABLE), not CODE.
   - Note its template ID.
3. **Replace `klaviyo-config.md`** for the new brand. Set:
   - Master template ID
   - Sender email + name
   - Default audience(s) if known
   - Any brand-specific Klaviyo preferences
4. **Make sure the brand has its own `brand-intelligence/brand-data.md`** in a sibling folder — the email skill leans on it for voice, products, and ICP during drafting.
5. **Don't change** `SKILL.md`, `references/*.md`, or this README — they're brand-agnostic by design. If you find yourself wanting to change one, the change probably belongs in `klaviyo-config.md` or `brand-data.md` instead.
6. **If running multiple brands side-by-side**, rename folders (e.g. `email-marketing-campaign-acme/`) and update the `name:` field in each `SKILL.md` frontmatter so Claude can disambiguate.

### What changes between brands

| File | Per brand? | Why |
|------|-----------|-----|
| `SKILL.md` | No | Framework + workflow are universal |
| `references/campaign-series.md` | No | Series structures are universal |
| `references/template-styles.md` | No | Block patterns are universal |
| `references/topic-types.md` | No | Topic types are universal |
| `references/email-checklist.md` | No | Pre-send checks are universal |
| `references/klaviyo-templates.md` | No | Push workflow is universal — uses the brand's config |
| `klaviyo-config.md` | **Yes** | Master template ID, sender, audience — all brand-specific |
| `../eca-brand-intelligence/brand-data.md` | **Yes** | Voice, products, ICP, market, competitors |

## What this skill is NOT for

- **Transactional or flow emails** (welcome series, abandoned cart, browse abandonment, post-purchase) — those are flows, not campaigns
- **SMS planning** unless explicitly part of a coordinated campaign
- **One-off ad-hoc emails** that aren't part of a campaign — just write them directly
