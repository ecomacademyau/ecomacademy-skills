---
name: eca-landing-pages
description: Build a high-converting landing page for an ad campaign directly into a Shopify theme — choose a format (Hero Product, Listicle, Social Proof, Kit/Subscription Bundle, or Advertorial), match the copy to the actual ad angle, and install it as editable theme sections. Use whenever the member wants a landing page, ad landing page, campaign page, LP, "a page for this ad", a sales page, an advertorial page, a listicle page, a bundle/kit page, wants to fix an ad-to-page mismatch, improve post-click conversion, or asks to build/install a page into their Shopify theme. Runs as an interactive guide where the member leads: they either tell you what they want or ask you to look at their ad account and suggest, you shape it together, then you write a brief they confirm before anything is built. Must be run in Claude Code inside a code editor (VS Code/Cursor), from the folder holding the brand data and skills, with the Shopify CLI connected: duplicates the live theme into a dev theme (never touches live), installs the section library and page template, and creates the page unpublished for review. Works with any Online Store 2.0 theme.
---

# ECA Landing Pages

Turn an ad into a landing page that actually converts the traffic it buys — built as **editable Shopify theme sections**, not a hardcoded one-off.

**The core principle: message match.** The page must continue the exact promise the ad made. The most common post-click killer is an ad that promises one thing and a page that opens with something else. Everything here serves that.

> Runs in **Claude Code** (needs the Shopify CLI + local theme access). Never edits the live theme — all work happens in a duplicated dev theme, and the page is created **unpublished** for review.

## Before you start — read this first

**Tell the member these three things up front, and check each one, before doing anything else.** Getting this wrong is the most common reason a run goes sideways.

**1. Run this in a code editor.** This skill edits real theme files, so it must run in **Claude Code inside a code editing tool** — VS Code, Cursor, or whichever editor they prefer. It can't be driven from a chat-only environment. If they aren't in one, stop and get them set up first.

**2. Open the right folder.** They should be working in the folder that holds their **brand data, research and skills** — typically the **Marketing Coworker folder** they already use with Claude Code. That folder is where `brand-data.md`, personas, past research and the rest of the ECA skills live, and this skill leans on all of it. Working from an empty or unrelated folder means generic copy and no message match. Confirm the folder before you start, and say what you found (or didn't).

**3. Shopify CLI connected and running.** The build step needs the **Shopify CLI installed and authenticated** to their store. Verify early — don't discover it's missing after writing the whole page:
```bash
shopify version                                   # installed?
shopify theme list --store <store>.myshopify.com  # authenticated? (prompts login if not)
```
If it's missing: `npm install -g @shopify/cli @shopify/theme`. Confirm the exact `.myshopify.com` domain with the member — never guess it.

### Connections: what's required vs what makes it better

**The Shopify CLI and the Shopify MCP are different tools and this skill uses both differently** — don't confuse them. Check each and tell the member what you have:

| | What it does here | Needed? | Without it |
|---|---|---|---|
| **Shopify CLI** | Pulls the live theme, pushes the dev theme. The build itself. | **Required** | Can't build. Plan the page, then stop. |
| **`brand-data.md` in the folder** | Voice, personas, objections, proof, guarantee, claim rules. | **Strongly recommended** | Copy gets generic and you'll have to ask far more questions. Say so. |
| **Shopify MCP** (Admin API) | Creates the page unpublished (`pageCreate`), reads products for the offer/sticky-bar sections, and helps detect installed apps. | *Optional* | Fine — give the member the two-click manual instruction to create the page and assign the template, and ask them which apps they run. |
| **Meta Ads MCP** | Pulls the real ad copy, angle, creative and current destination URL — the raw material for message match. Also powers "look at my ad account and suggest". | *Optional* | Ask them to paste the ad copy and angle instead. Path B (suggest from the ad account) isn't available — say so rather than guessing. |

In Claude Code, MCPs are added with `claude mcp add …` — if a useful one is missing, tell the member what it would unlock and let them decide. **Never block on an optional connector**: run with what's there, say plainly what you couldn't do, and carry on.

**Only the CLI is a hard stop.** If it's missing, you can still plan the page with them — just don't start building until it's ready.

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
- **Risk removal / guarantee (required on every page)** — take it from `brand-data.md`. **If there isn't one, ask the member directly** what they can offer: money-back window, free returns, warranty, free shipping, cancel-anytime, or a satisfaction promise. If they genuinely have none, **tell them plainly that it will cost conversions** — a landing page asking for money with no risk reversal converts worse — and suggest the smallest credible one they could stand behind. Never invent a guarantee, and never ship the page without addressing this.
- **Scarcity / urgency (suggest it)** — ask whether anything *true* creates urgency: limited stock, a launch or seasonal window, a price rise, a bonus for the first N orders, a deadline on the offer. Bake it in near the CTA if so. **Only if it's real** — fake countdowns and invented "only 3 left" damage trust and can breach consumer law. If there's nothing genuine, say so and move on.
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
| **Key messages** | the benefits and proof you'll use (and where each came from) |
| **Risk removal** | the guarantee/risk reversal this page will carry — flagged if the brand has none |
| **Urgency** | any genuine scarcity or deadline to include, or "none — nothing truthful to use" |
| **Page config** | sticky add-to-cart on/off + product · hide navigation? · hide footer? |
| **Proof assets** | any real press logos, awards or certifications for the trust bar — or icon+text trust points if none |
| **Apps in use** | which sections will use an installed app's widget (e.g. Judge.me reviews) vs a custom one |
| **Image briefs** | each image slot with the shot needed (subject, framing, ratio) — all ship as placeholders for the member to fill |
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

**Images stay as placeholders** — write the *image brief* for each slot (subject, framing, aspect ratio, suggested alt text) rather than choosing pictures; the sections render native Shopify placeholders so the layout reads correctly until the member adds theirs. Ship real **icons** (theme set or inline SVG). Full method in `references/apps-and-assets.md`.

**Rules:** use the brand's real voice; never invent claims, reviews, stats or guarantees — pull them from `brand-data.md` or the store, and if something's missing, put a clear `{{PLACEHOLDER}}` in and tell the member exactly what to supply.

## Step 5 — Build into the theme (Claude Code + Shopify CLI)

Only after the brief is confirmed. Follow `references/shopify-build.md` exactly. Summary:

1. Verify/install the **Shopify CLI**; authenticate to the store.
2. **Duplicate the live theme** into an unpublished dev theme (e.g. `ECA LP — <campaign>`). **Never edit the live theme.**
3. Copy the needed **sections** from `theme-files/sections/` and the chosen **template** from `theme-files/templates/` into the dev theme. Only install the sections that format uses.
4. Fill the template JSON with the approved copy so the page renders complete — not empty placeholders — while every field stays editable in the theme editor.
5. Push to the dev theme and give the member the **preview link**.
6. **Create the Shopify page** (unpublished) and assign it the template.

## Step 6 — Hand over the page

**Always finish with three clickable links** (formats in `references/shopify-build.md` §6): **Edit the page** — the theme editor deep-linked to this page (`/admin/themes/<theme_id>/editor?previewPath=%2Fpages%2F<handle>`) so they can change copy, images and blocks straight away; **Preview it** — the storefront on the dev theme; and **Page settings** — the admin page for title, SEO and publishing. Never end a build with just "the page has been created". Then give them what to review, and a **before-you-publish checklist** listing every placeholder image and `{{PLACEHOLDER}}` still in the page with exactly what to supply for each (shot description, aspect ratio). Be explicit that **placeholder images must be replaced before the page goes live**. Then how to publish when happy. Remind them to **point the ad's destination URL at the new page** once live — the page only pays off if the ad sends traffic to it.

## Page-wide configuration

Every template includes an **ECA LP — Page settings** section (first in the order) that carries the landing-page-level options. Confirm both with the member in the brief:

- **Sticky add-to-cart bar** — appears after a set scroll depth with the product, price, add-to-cart and a risk-removal line. On by default; set the product it sells. Keeps the ask permanently in reach on mobile.
- **Hide site navigation — OFF by default. Never turn it on without asking.** It's a real conversion lever for cold paid traffic, but it also removes the member's header, cart and announcement bar, which is a jarring surprise if they didn't choose it. Offer it as a suggestion ("want a distraction-free page? I can hide the nav") and leave it off unless they say yes. Same for the footer — and note some ad platforms expect policy links (returns, privacy, contact) to stay reachable.

## Step 7 — Now write the ads for it (offer this every time)

A landing page only earns its keep if traffic arrives with the matching promise. Once the page is built, **offer to write the ads that point at it** — you already have everything they need (the angle, the hook, the audience, the offer, the proof, the guarantee):

- **`eca-ad-copywriting`** — headlines and primary text for the Meta campaign, built from this page's hook and angle so the ad and page say the same thing.
- **`eca-ugc-scripts`** — if the concept suits video (Founder Story, 3 Reasons Why, Comment Reply, Us vs Them), hand over the funnel tier and angle and let it script the shoot.

Hand them the page's hook, the persona, the objection it handles, the offer and the guarantee, so the ads inherit the same message. Then remind them to **point the campaign's destination URL at the new page** — the whole thing only works if the ad actually sends traffic there.

## How many pages? One per angle, not several per angle

Members often ask whether to build multiple landing pages for the same hook. **Default answer: no.**

- **One strong page per distinct angle** — yes. If they run a founder-story angle, a price-comparison angle and a convenience angle, each deserves its own page carrying that promise. That's message match, and it's the point of this skill.
- **Several pages for the *same* angle** — only when the traffic genuinely supports a test. A landing-page split test needs enough conversions per variant to mean anything (rough guide: **~100+ conversions per variant**, or several thousand sessions each). Below that, the result is noise and they've doubled their maintenance for nothing.
- **Test the ads first.** Creative variance is far larger than page variance in most accounts — it's normal to see a 10×+ spread in CPA between ads on the same page. Ads are cheaper and faster to test, so exhaust that lever before splitting page traffic.
- **If they do split-test**, change **one thing** (the hook, the format, or the offer — not all three), run both to the same audience, and decide up front what result would make them pick a winner.

Say this plainly if they ask for five pages off one angle — it's usually enthusiasm worth redirecting into five *ads*.

## Build rules

- **Leave the hero eyebrow blank unless the member asks for one.** The headline is the message match — an eyebrow pushes it down and competes with it, and offers/discounts convert better at the CTA and offer sections than above the hook. Don't fill it with the page type, a discount, or a generic label. It stays empty by default; the member can add one in the theme editor if they want.
- **The offer section is block-based too.** Badge, heading, offer detail, price, **product variations**, **inventory indicator**, **countdown timer**, add-to-cart, risk line, trust points and spacers are all movable blocks. Seed only what the offer needs. **Countdown has three modes:** *fixed* (a one-off deadline), *daily* and *weekly* (auto-resetting, so nobody has to keep changing dates). **Point the recurring modes at a real recurring cutoff** — the store's dispatch time is the honest and most persuasive use ("Order within 4h 12m for dispatch today"). All modes count down in the **store's timezone**, not the visitor's.

**Two honesty rules:** the badge and countdown must reflect something *true* — a real deadline, a real discount, a genuine dispatch cutoff. **Never a per-visitor evergreen timer that restarts for everyone** — that's fabricated scarcity, it erodes trust and can breach consumer law (the ACCC has pursued misleading urgency claims). And only add the **inventory indicator** if the store actually tracks inventory, or it'll show nothing.
- **The hero is block-based — build it from blocks, not fixed fields.** Headline, sub-headline, rating, button(s), trust points, custom text and spacers are each a **movable block**, so the member can reorder or remove any of them in the theme editor (drag the button above the rating, add a second CTA, drop the rating entirely). Seed the blocks the format needs and leave the rest out — don't add an eyebrow block unless they've asked for one. **Listicle and advertorial heroes get no CTA block** (the page has to earn the ask first).
- **Every page ends with `eca-lp-about`** — a short, human founder/team note before the final offer. Pull the real story from `brand-data.md` §1 and write it in their voice. If there's no founder story available, ask for a couple of lines rather than inventing one, and never fabricate a person or photo.
- **Alternate section backgrounds so the page has rhythm.** Every section has a **Colour scheme** dropdown (and optional custom background/text colours) in the theme editor. A long page in one flat colour reads as an undifferentiated wall and people stop scrolling. Alternate: give the hero, proof, offer and about sections a contrasting scheme and leave the rest inheriting, so the page reads as distinct chapters. **Prefer the theme's colour schemes over custom colours** — they carry text and button colours together, so a dark band still has readable text, and they stay on-brand if the member later changes their theme palette. Use the custom pickers only when the page needs an exact colour the theme doesn't have, and set the text colour too if the background is dark. **Don't colour every second section by reflex** — 2 or 3 contrast bands on a page is plenty; more looks like a ransom note.
- **Break up text-heavy sections with icons.** A grid of benefits with no visual relief reads flat. The benefits section has a **built-in icon set** (check, bolt, shield, truck, leaf, star, dollar, refresh…) that inherits the theme colour — assign one per benefit, matched to its meaning. No uploads needed.
- **Trust bar: only with real proof.** The `eca-lp-trust-bar` section carries either icon+text trust points (free shipping, guarantee, secure checkout — always safe) or **press logos / awards / certifications**. Only use logos the brand genuinely has — check `brand-data.md` §8 (proof) and **ask the member**. Never fabricate press or awards. If they have none, use the icon+text mode, which works for every brand.
- **Listicle items need real depth: 1-2 full paragraphs each**, not one-liners. Para 1 names the problem/insight in the reader's world; para 2 shows how it plays out differently. One-line items read like a feature list and convert like one.
- **Reviews: use the app's widget, don't write quotes yourself.** The testimonials section defaults to app-widget mode. Only write manual quotes if the member confirms they have no reviews app — and then use real customer words from `brand-data.md`, never invented ones. **Ask; don't assume.**
- **Listicles earn the ask — they don't open with one.** A listicle must read like an article: no CTA button before the list has done its convincing. Let the items build the case, then introduce the product in the closing block, then ask. The CTA text must follow from the list's argument ("Ditch the machine — try it") rather than a generic "Shop now".
- **Never expose internal page-type or format names in public copy.** The five format names (Hero Product, Listicle, Social Proof, Kit, Advertorial) are *our* build vocabulary — they mean nothing to a visitor and cheapen the page. Keep them out of eyebrows, headings, bylines, alt text, page titles and URL handles. The **only** exception is the legally-required advertising disclosure on advertorials, which is just "Advertisement" or "Sponsored" — never "Advertisement · Founder Story". Every visible word must be written for the customer, not for us.


- **When an app covers a section, don't also write your own content for it.** If the store has a reviews app, do not fill the testimonials section with hand-picked quotes *and* embed the app widget — that duplicates the same reviews twice on one page (it looks broken and it's what a real test caught). Instead switch the section to app-widget mode and leave a clear "add your app's block here" prompt. Same for FAQ, subscription and bundle apps. One source of truth per section.
- **App-first, then native, then custom.** Before building any section, check what the store already has — if a reviews/subscription/FAQ/bundle app is installed, use its widget or `@app` block rather than rebuilding it (every ECA LP section accepts `@app` blocks). Ask the member when it's a close call. See `references/apps-and-assets.md`.
- **Never choose images — always ship placeholders.** Auto-picked photos produce wrong-looking layouts. Every image slot renders Shopify's native `placeholder_svg_tag` at the right aspect ratio until the member picks their own in the theme editor. Your job is the **image brief** (subject, framing, ratio) for each slot, not the image. Only place a specific image if the member asks. **Icons are the exception** — inline the theme's own icon set or a free openly-licensed SVG (Lucide/Heroicons) using `currentColor`. See `references/apps-and-assets.md`.
- **Use native Shopify/theme features wherever they exist** — the theme's own product/buy-buttons, review app blocks and image handling, standard section groups, `{{ section.settings }}`, `image_url` filters, and native `<details>` accordions. Only write custom Liquid where nothing native does the job.
- **Everything must be editable in the theme editor** — every headline, body, image, button, and list item is a section/block setting with a sensible default and a clear label. No hardcoded copy in Liquid.
- **OS 2.0 compatible, theme-agnostic** — don't depend on Horizon-only blocks; inherit the theme's fonts/colours rather than hardcoding a design system.
- **Versioned sections: install missing, refresh same-name, never touch superseded.** Structural changes get a new filename (`eca-lp-hero-v2.liquid`); everything else is additive. So: install anything missing; **overwrite a same-name file with the current version** (safe by construction — same name means additive-only, so saved settings persist and pages keep working while picking up fixes); and **never overwrite or delete a superseded file** (`eca-lp-hero.liquid` once v2 exists) because an older page still renders from it. If a file has been hand-edited, ask before replacing. Net effect: duplicate a theme with an old page in it, build a new page, and the new page gets everything current while the old one is untouched. See `references/shopify-build.md` §3a.
- **Copy whole folders for dependencies.** Always copy **every** file in `theme-files/snippets/` (and `assets/` if present) — never cherry-pick. Then run the dependency check in `references/shopify-build.md` §3b, which derives what's needed from the section code itself, **before** pushing. A section rendering a missing snippet throws a Liquid error on a live page, and this keeps working as new helpers get added over time.
- **Never switch on anything that changes the member's storefront chrome without asking** — hiding the navigation or footer is opt-in, every time.
- **Always render a placeholder when an image slot is empty**, so the layout never collapses. Every section that can show an image ships its own placeholder CSS — don't rely on another section being present.
- **Approval gates**: the **brief must be confirmed (Step 3)** before anything is created, and nothing is published — page or theme — without an explicit yes.
- **Speed**: lazy-load below-fold images, keep custom CSS scoped and minimal, no external frameworks.
- **AEO**: the FAQ section emits **FAQPage JSON-LD** so the page can be cited by AI answer engines.

## Related skills
`references/apps-and-assets.md` (app-first + asset creation) · `eca-meta-ads-4pi` (flags the ad→page mismatch this skill fixes) · **`eca-ad-copywriting`** (write the ads that point at this page — offer this after every build) · **`eca-ugc-scripts`** (video ads for the same angle) · `eca-brand-intelligence` (voice, personas, proof) · `eca-seo-ai-audit` (checks the page once live).
