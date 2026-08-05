---
name: eca-landing-pages
description: Build a high-converting landing page for an ad campaign directly into a Shopify theme — choose a format (Hero Product, Listicle, Social Proof, Kit/Subscription Bundle, or Advertorial), match the copy to the actual ad angle, and install it as editable theme sections. Use whenever the member wants a landing page, ad landing page, campaign page, LP, "a page for this ad", a sales page, an advertorial page, a listicle page, a bundle/kit page, wants to fix an ad-to-page mismatch, improve post-click conversion, or asks to build/install a page into their Shopify theme. Runs as an interactive guide where the member leads: they either tell you what they want or ask you to look at their ad account and suggest, you shape it together, then you write a brief they confirm before anything is built. Runs in Claude Code with the Shopify CLI: duplicates the live theme into a dev theme (never touches live), installs the section library and page template, and creates the page unpublished for review. Works with any Online Store 2.0 theme.
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

## How to run this: the member leads, you suggest

This is an **interactive guide, not an interrogation and not an autopilot.** The member decides what gets built; your job is to make deciding easy — offer options, recommend one with a reason, and take their answer. Rules:

- **Never decide for them.** Every meaningful choice (format, angle, product, offer, structure) is theirs. Recommend, don't assume.
- **Always give a recommendation with the question**, so they can just say "yes" — "I'd suggest Listicle, because your ad leads with '5 reasons'. Happy with that, or prefer another?"
- **One thing at a time.** Short exchanges beat a wall of questions. Use `AskUserQuestion` for choices.
- **Take their steer over your own analysis.** If they want a format you wouldn't have picked, say what you'd watch for in one line, then build what they asked for.
- **Nothing gets built until the brief is confirmed** (Step 3).

## Step 1 — Pick the starting point

Ask the member how they want to start:

- **A — "I know what I want."** They have the angle/product/format in mind. Go to Step 2 and shape it with them.
- **B — "Look at my ad account and suggest."** Pull their live Meta ads (via the Meta Ads MCP), find the ads worth building a page for — the spenders, the winners, and any with a landing-page mismatch — and come back with a short shortlist: *"These three are worth a page, here's why."* Let them choose.

If they've already told you the ad or the angle in their opening message, skip the question and confirm what you understood in one line.

## Step 2 — Interactive discovery (member-led)

Work through these with them, one at a time, each with your recommendation attached. Pull what you can first so you're asking informed questions, not blank ones:

- **Source material** — the ad this page serves. If the Meta Ads MCP is connected, pull the real creative copy, headline, angle and current destination URL (`ads_get_creatives`, `ads_get_ad_entities`). Otherwise ask them to paste the ad copy. *This is the raw material for message match.*
- **Brand** — read `brand-data.md` from `eca-brand-intelligence` for voice, personas, objections, proof and claim rules. Say so if it's missing (the copy will be more generic).
- **Format** — recommend one of the five from the ad's angle (`references/page-formats.md`) and explain why in a line. Their call.
- **Product / offer** — what the page sells, and the exact offer (price, bundle, subscription, discount).
- **Goal + destination** — buy now, add to cart, subscribe, or lead capture.
- **Media** — what imagery they have; recommend pulling a frame from the ad creative for continuity.
- **Installed apps** — check what's already on the store (reviews, subscriptions, FAQ, bundles) and plan to use their widgets rather than rebuilding. Ask if it's a close call. See `references/apps-and-assets.md`.
- **Anything to avoid** — claims, comparisons or wording that's off-limits.

Don't re-ask anything they've already answered.

## Step 3 — The brief (MANDATORY — confirm before building)

Write the brief back to them as a short, scannable summary and **stop.** It covers:

| | |
|---|---|
| **Format** | which of the five, and why it fits the ad |
| **The ad it serves** | campaign/ad name + the promise it makes |
| **Audience** | the persona and the objection to overcome |
| **Product & offer** | exactly what's sold, at what price/terms |
| **The hook** | 2–3 candidate headlines that echo the ad — let them pick or edit |
| **Page structure** | the section order for that format, in plain English |
| **Key messages** | the benefits, proof and guarantee you'll use (and where each came from) |
| **Apps in use** | which sections will use an installed app's widget (e.g. Judge.me reviews) vs a custom one |
| **Media plan** | which images/video go where, and which you'll create vs need from them |
| **Gaps** | anything you couldn't source, and what you need from them |
| **Destination** | the page URL and where the CTA sends people |

Then ask them to **confirm, change, or add.** Take edits and re-present as many times as needed. **Do not create a theme, a file, or a page until they've said yes.**

## Step 4 — Write the content (from the confirmed brief)

Follow `references/framework.md`. Every page carries the same ten elements in a format-appropriate order:

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

**Create the visuals as you go** — pull from the brand's Shopify Files and the ad creative first, generate icons/imagery with an image tool where one is connected, upload to Shopify, and only use a `{{PLACEHOLDER}}` when nothing can be sourced or made (then say exactly what shot is needed). Full method in `references/apps-and-assets.md`.

**Rules:** use the brand's real voice; never invent claims, reviews, stats or guarantees — pull them from `brand-data.md` or the store, and if something's missing, put a clear `{{PLACEHOLDER}}` in and tell the member exactly what to supply.

## Step 5 — Build into the theme (Claude Code + Shopify CLI)

Only after the brief is confirmed. Follow `references/shopify-build.md` exactly. Summary:

1. Verify/install the **Shopify CLI**; authenticate to the store.
2. **Duplicate the live theme** into an unpublished dev theme (e.g. `ECA LP — <campaign>`). **Never edit the live theme.**
3. Copy the needed **sections** from `theme-files/sections/` and the chosen **template** from `theme-files/templates/` into the dev theme. Only install the sections that format uses.
4. Fill the template JSON with the approved copy so the page renders complete — not empty placeholders — while every field stays editable in the theme editor.
5. Push to the dev theme and give the member the **preview link**.
6. **Create the Shopify page** (unpublished) and assign it the template.

## Step 6 — Hand over

Give the member: the preview URL, the page URL (unpublished), what to review, and a **before-you-publish checklist** listing every placeholder image and `{{PLACEHOLDER}}` still in the page with exactly what to supply for each (shot description, aspect ratio). Be explicit that **placeholder images must be replaced before the page goes live**. Then how to publish when happy. Remind them to **point the ad's destination URL at the new page** once live — the page only pays off if the ad sends traffic to it.

## Build rules

- **Never expose internal page-type or format names in public copy.** The five format names (Hero Product, Listicle, Social Proof, Kit, Advertorial) are *our* build vocabulary — they mean nothing to a visitor and cheapen the page. Keep them out of eyebrows, headings, bylines, alt text, page titles and URL handles. The **only** exception is the legally-required advertising disclosure on advertorials, which is just "Advertisement" or "Sponsored" — never "Advertisement · Founder Story". Every visible word must be written for the customer, not for us.


- **App-first, then native, then custom.** Before building any section, check what the store already has — if a reviews/subscription/FAQ/bundle app is installed, use its widget or `@app` block rather than rebuilding it (every ECA LP section accepts `@app` blocks). Ask the member when it's a close call. See `references/apps-and-assets.md`.
- **Ship real visuals, not empty boxes.** Brand files and ad frames first → generate with an image tool if one's connected → otherwise a correctly-sized **placeholder service** (placehold.co / picsum.photos) so the layout still reads. **Icons: inline a free openly-licensed SVG** (Lucide/Heroicons/Feather) using `currentColor` so it inherits the theme — or the theme's own icon set. **Placeholders never go live**: list every one in the handover and the pre-publish checklist.
- **Use native Shopify/theme features wherever they exist** — the theme's own product/buy-buttons, review app blocks and image handling, standard section groups, `{{ section.settings }}`, `image_url` filters, and native `<details>` accordions. Only write custom Liquid where nothing native does the job.
- **Everything must be editable in the theme editor** — every headline, body, image, button, and list item is a section/block setting with a sensible default and a clear label. No hardcoded copy in Liquid.
- **OS 2.0 compatible, theme-agnostic** — don't depend on Horizon-only blocks; inherit the theme's fonts/colours rather than hardcoding a design system.
- **Approval gates**: the **brief must be confirmed (Step 3)** before anything is created, and nothing is published — page or theme — without an explicit yes.
- **Speed**: lazy-load below-fold images, keep custom CSS scoped and minimal, no external frameworks.
- **AEO**: the FAQ section emits **FAQPage JSON-LD** so the page can be cited by AI answer engines.

## Related skills
`references/apps-and-assets.md` (app-first + asset creation) · `eca-meta-ads-4pi` (flags the ad→page mismatch this skill fixes) · `eca-ad-copywriting` (the ad copy this page must match) · `eca-brand-intelligence` (voice, personas, proof) · `eca-seo-ai-audit` (checks the page once live).
