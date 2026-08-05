# Changelog — ECA Landing Pages

Tracked so we know what changed between test runs. Newest first.

## v1.18.0 — auto-resetting countdown
- Countdown gains **daily** and **weekly** modes that reset themselves — no more editing end dates. Ideal for a real dispatch/order cutoff ("Order within 4h 12m for dispatch today").
- All modes now count down in the **store's timezone** (anchored to server-rendered time), so a customer in Perth and one in Sydney see the same cutoff.
- Guardrail documented: recurring timers must map to a genuine recurring deadline — never a per-visitor evergreen timer.

## v1.17.0 — block-based offer section
- **Offer rebuilt as blocks**: badge, heading, detail, price, variants, inventory, countdown, buy button, risk line, trust points, spacer.
- **Product variations**: native select that live-updates price, compare-at, saving, inventory and button state (no page reload, no dependencies).
- **Inventory indicator**: low-stock threshold with {qty} substitution, plus in-stock and sold-out states.
- **Countdown timer**: real end date/time, hides or shows an expired message when it passes.
- **Sale/urgency badge** with colour controls.

## v1.16.0 — star controls
- Stars are now **SVG, not the ★ text character** — consistent across themes and properly colourable.
- Rating block: **show/hide stars**, a **0–5 rating with half-star support**, and a **colour picker** (defaults to amber, or leave blank to inherit the theme).
- Same treatment on testimonial stars, with a section-level star colour.

## v1.15.0 — block-based hero + visual relief
- **Hero rebuilt as blocks**: headline, sub-headline, rating, button, trust points, custom text and spacer are all movable/reorderable in the theme editor. Applies to all five formats (shared section). Listicle/advertorial heroes ship without a CTA block.
- **Built-in icon set** (`eca-lp-icon` snippet, 17 inline SVGs inheriting theme colour) with an icon picker on the benefits section; templates pre-assign sensible icons.
- **New `eca-lp-trust-bar` section** under the hero: icon+text trust points (default, works for any brand) or real press/award logos — never fabricated.

## v1.13.0 — dependency safeguards
- Snippets and assets are now copied as **whole folders**, never cherry-picked.
- Added a **pre-push dependency check** that derives requirements from the section code itself (every `{% render %}` must resolve, every template section must exist) — so it keeps working as new helpers are added.
- Added `theme-files/manifest.json` as a convenience listing (not the source of truth).

## v1.12.0 — fixes from listicle test
- **Placeholders rebuilt**: replaced Shopify's `placeholder_svg_tag` (which silently renders nothing when a placeholder name isn't available) with a self-contained inline SVG snippet that always renders, with a label chip naming the shot needed.
- **Reviews default to the app widget** — testimonials ships with app-widget mode ON and no pre-seeded quotes; manual quotes only if the member confirms they have no reviews app.
- **Listicle items require 1–2 full paragraphs**, not one-liners.

## v1.11.0 — fixes from first real build
- Placeholder CSS added to **every** section that renders one (was only in the hero, so placeholders collapsed to zero height elsewhere).
- **Hide navigation now OFF by default** and must be offered, never assumed.

## v1.10.0 — ad handoff + page-count guidance
- Step 7: offer `eca-ad-copywriting` and `eca-ugc-scripts` after every build.
- Guidance: one page per distinct angle; split-test only with the traffic to support it.

## v1.9.0 — connections
- Required vs optional table (CLI required; Shopify MCP, Meta Ads MCP optional) and the CLI-vs-MCP distinction.

## v1.8.0 — prerequisites
- "Before you start": run in a code editor, open the folder with brand data, Shopify CLI connected.

## v1.7.0 — page config + format fixes
- New `eca-lp-settings` section: sticky add-to-cart bar + hide navigation/footer.
- Listicle: image left/right/alternating/none, article-first (no opening CTA), closing block before the ask.
- App-covered sections no longer duplicate their own content.
- Guarantee required on every page (ask if brand has none); suggest genuine scarcity/urgency only.

## v1.6.0 — eyebrow off
- Hero eyebrow off by default; never carries the page type or a discount.

## v1.5.0 — placeholders over chosen images
- Images always ship as placeholders; the skill writes the image brief instead of picking pictures.

## v1.2.0–1.4.0 — interactive guide
- Member-led flow with two entry paths, brief confirmation gate, app-first rule, asset guidance.

## v1.1.0 — initial
- Five formats, ten-element framework, 12 sections, 5 templates, dev-theme build.
