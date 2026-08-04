---
name: eca-landing-pages
description: Build a high-converting landing page for an ad campaign directly into a Shopify theme — choose a format (Hero Product, Listicle, Social Proof, Kit/Subscription Bundle, or Advertorial), match the copy to the actual ad angle, and install it as editable theme sections. Use whenever the member wants a landing page, ad landing page, campaign page, LP, "a page for this ad", a sales page, an advertorial page, a listicle page, a bundle/kit page, wants to fix an ad-to-page mismatch, improve post-click conversion, or asks to build/install a page into their Shopify theme. Runs in Claude Code with the Shopify CLI: duplicates the live theme into a dev theme (never touches live), installs the section library and page template, writes the copy from the real ad + brand data, and creates the page unpublished for review. Works with any Online Store 2.0 theme.
---

# ECA Landing Pages

Turn an ad into a landing page that actually converts the traffic it buys — built as **editable Shopify theme sections**, not a hardcoded one-off.

**The core principle: message match.** The page must continue the exact promise the ad made. The most common post-click killer is an ad that promises one thing and a page that opens with something else. Everything here serves that.

> Runs in **Claude Code** (needs the Shopify CLI + local theme access). Never edits the live theme — all work happens in a duplicated dev theme, and the page is created **unpublished** for review.

## The five formats

Pick by what the ad is doing (full detail + section order in `references/page-formats.md`):

| Format | Use when the ad… | Template |
|---|---|---|
| **Hero Product** | drives straight to one product with a clear promise | `page.eca-lp-hero.json` |
| **Listicle** | uses "N reasons / N ways" or curiosity-led angles | `page.eca-lp-listicle.json` |
| **Social Proof** | leans on reviews, UGC, testimonials, "everyone's switching" | `page.eca-lp-social-proof.json` |
| **Kit / Subscription Bundle** | sells a bundle, kit, or subscription offer | `page.eca-lp-kit.json` |
| **Advertorial** | is story-led, founder, or news/native style | `page.eca-lp-advertorial.json` |

If the member isn't sure, recommend one from the ad's angle and say why.

## Step 1 — Scope + pull the ad (do this first)

1. **Which ad/campaign is this page for?** If the **Meta Ads MCP** is connected, pull the actual ad: creative copy (primary text, headline), the angle, the creative type, and the landing page it currently points to (`ads_get_creatives`, `ads_get_ad_entities`). Use the real ad copy — it's the source of message match. If it isn't connected, ask the member to paste the ad copy/angle.
2. **Load the brand** — read `brand-data.md` from `eca-brand-intelligence` for voice, personas, objections, proof, offers and claim rules. Without it, the copy will be generic; say so.
3. **Confirm the essentials**: the product/offer the page sells, the format (recommend one), and the goal (buy now / add to cart / subscribe).
4. **Check the store + theme**: confirm the `.myshopify.com` domain and that the live theme is **Online Store 2.0**.

## Step 2 — Write the page content (before touching the theme)

Follow `references/framework.md` — every page carries the same ten elements in a format-appropriate order:

1. **Hook** that matches the ad's promise (echo its language)
2. **Matching image/video** for that angle
3. **Clear CTA with risk removal** above the fold
4. **Benefit / outcome / transformation** statement
5. **Proof the outcome is real** (data, results, demonstration)
6. **How it works / what's included**
7. **Risk removal / guarantee**
8. **Reviews & social proof**
9. **FAQs** (handling the real objections)
10. **Offer, product and final CTA**

**Rules:** use the brand's real voice; never invent claims, reviews, stats or guarantees — pull them from `brand-data.md` or the store, and if something's missing, put a clear `{{PLACEHOLDER}}` in and tell the member exactly what to supply. Present the full copy for approval **before** installing anything.

## Step 3 — Build into the theme (Claude Code + Shopify CLI)

Follow `references/shopify-build.md` exactly. Summary:

1. Verify/install the **Shopify CLI**; authenticate to the store.
2. **Duplicate the live theme** into an unpublished dev theme (e.g. `ECA LP — <campaign>`). **Never edit the live theme.**
3. Copy the needed **sections** from `theme-files/sections/` and the chosen **template** from `theme-files/templates/` into the dev theme. Only install the sections that format uses.
4. Fill the template JSON with the approved copy so the page renders complete — not empty placeholders — while every field stays editable in the theme editor.
5. Push to the dev theme and give the member the **preview link**.
6. **Create the Shopify page** (unpublished) and assign it the template.

## Step 4 — Hand over

Give the member: the preview URL, the page URL (unpublished), what to review, any `{{PLACEHOLDER}}` items still needing real content (with what to supply), and how to publish when happy. Remind them to **point the ad's destination URL at the new page** once live — the page only pays off if the ad sends traffic to it.

## Build rules

- **Use native Shopify/theme features wherever they exist** — the theme's own product/buy-buttons, review app blocks and image handling, standard section groups, `{{ section.settings }}`, `image_url` filters, and native `<details>` accordions. Only write custom Liquid where nothing native does the job.
- **Everything must be editable in the theme editor** — every headline, body, image, button, and list item is a section/block setting with a sensible default and a clear label. No hardcoded copy in Liquid.
- **OS 2.0 compatible, theme-agnostic** — don't depend on Horizon-only blocks; inherit the theme's fonts/colours rather than hardcoding a design system.
- **Approval gates**: approve the copy (Step 2), approve before install (Step 3). Never publish the page or the theme without an explicit yes.
- **Speed**: lazy-load below-fold images, keep custom CSS scoped and minimal, no external frameworks.
- **AEO**: the FAQ section emits **FAQPage JSON-LD** so the page can be cited by AI answer engines.

## Related skills
`eca-meta-ads-4pi` (flags the ad→page mismatch this skill fixes) · `eca-ad-copywriting` (the ad copy this page must match) · `eca-brand-intelligence` (voice, personas, proof) · `eca-seo-ai-audit` (checks the page once live).
