# ECA Landing Pages — a Claude Code skill

Build a high-converting landing page for an ad campaign directly into a Shopify theme — as **editable theme sections**, not a hardcoded one-off.

Built by **Ecommerce Academy**.

## Before you start
1. **Run it in a code editor** — this skill edits real theme files, so it needs **Claude Code inside VS Code, Cursor or your editor of choice**. It can't run from a chat-only window.
2. **Open the folder with your brand data, research and skills** — usually the **Marketing Coworker folder** you already use with Claude Code. That's where your `brand-data.md`, personas and research live, and the page copy is only as good as what it can read.
3. **Have the Shopify CLI installed and connected** to your store (`shopify version`, then `shopify theme list --store your-store.myshopify.com`). Install with `npm install -g @shopify/cli @shopify/theme` if needed.

### Connections
| | Needed? | What it adds |
|---|---|---|
| **Shopify CLI** | **Required** | Pulls your live theme and pushes the dev theme — the build itself |
| **`brand-data.md`** in the folder | Strongly recommended | Your voice, personas, objections and proof — without it the copy is generic |
| **Shopify MCP** | Optional | Creates the page for you and reads your products; without it you create the page in two clicks |
| **Meta Ads MCP** | Optional | Pulls your real ad copy for message match, and powers "look at my ad account and suggest" |

*The Shopify CLI and the Shopify MCP are different tools — the CLI handles theme files, the MCP handles products and pages. Only the CLI is a hard requirement.*

## The five formats
| Format | Use when the ad… |
|---|---|
| **Hero Product** | drives straight to one product with a clear promise |
| **Listicle** | uses "N reasons / N ways" or curiosity-led angles |
| **Social Proof** | leans on reviews, UGC, testimonials |
| **Kit / Subscription Bundle** | sells a bundle, kit or subscription |
| **Advertorial** | is story-led, founder or news/native style |

## The framework (every page)
Hook matching the ad → matching image → CTA with risk removal → benefit/transformation → proof → how it works / what's included → guarantee → reviews & social proof → FAQs → offer + final CTA.

**The core principle is message match** — the page continues the exact promise the ad made. Mismatch is the biggest post-click killer (and what `eca-meta-ads-4pi` flags).

## How it works — you lead, it suggests

It runs as an **interactive guide**. You make the calls; it brings the options, a recommendation and the data.

1. **Pick your starting point** — *"I know what I want"*, or *"look at my ad account and suggest"* (it pulls your live ads and comes back with a shortlist worth building pages for).
2. **Shape it together** — format, angle, product, offer, media. Every question comes with a recommendation so you can just say yes.
3. **Confirm the brief** — it writes the whole plan back to you (format, hook options, structure, key messages, media, gaps). **Nothing is built until you approve it.**
4. **It builds** — Shopify CLI duplicates your **live theme into a dev theme** (live is never touched), installs only the sections that format needs, writes the copy into the template, pushes, and returns a preview link.
5. **Hand over** — page created unpublished: preview URL, any remaining placeholders, how to publish, and a reminder to point the ad at the new page.
6. **Write the matching ads** — it then offers to run `eca-ad-copywriting` (headlines + primary text) and `eca-ugc-scripts` (video scripts) off the same angle, so the ad and the page say the same thing.

### How many pages should I build?
**One per distinct angle, not several per angle.** Different angles (founder story vs price vs convenience) each deserve their own page — that's message match. Multiple pages for the *same* angle only pay off once you have the traffic to split-test properly (roughly 100+ conversions per variant). Test your **ads** first: creative variance is much bigger than page variance, and it's faster and cheaper to learn from.

## What gets installed
```
sections/
  eca-lp-settings.liquid          Page config: sticky add-to-cart + hide nav/footer
  eca-lp-hero.liquid              Hook + media + CTA + risk removal
  eca-lp-trust-bar.liquid         Trust points or press/award logos

  eca-lp-benefits.liquid          Outcome-led benefits grid
  eca-lp-listicle.liquid          Numbered reasons with inline CTAs
  eca-lp-how-it-works.liquid      Numbered steps
  eca-lp-whats-included.liquid    Kit/bundle contents + total value
  eca-lp-proof.liquid             Demo/stats proof
  eca-lp-testimonials.liquid      Quote cards
  eca-lp-reviews-embed.liquid     Native review app embed / app block
  eca-lp-guarantee.liquid         Risk removal
  eca-lp-faq.liquid               Accordion + FAQPage JSON-LD
  eca-lp-offer.liquid             Offer + native add-to-cart
  eca-lp-article.liquid           Advertorial body (with ad disclosure)
snippets/
  eca-lp-cta.liquid               Reusable CTA + risk-removal line
  eca-lp-placeholder.liquid       Always-renders image placeholder
  eca-lp-icon.liquid              Built-in inline icon set (inherits theme colour)
templates/
  page.eca-lp-{hero,listicle,social-proof,kit,advertorial}.json
```

## Design principles
- **Everything editable** — every headline, image, button and list item is a section/block setting in the theme editor. No hardcoded copy.
- **Native first** — the theme's own product form for add-to-cart, the review app's block for reviews, `<details>` accordions, `image_tag` with lazy loading.
- **Theme-agnostic** — any Online Store 2.0 theme; inherits the theme's fonts and colours rather than imposing a design system.
- **Never invents** — no fabricated reviews, stats or guarantees; anything unsourced becomes a clear `{{PLACEHOLDER}}` with a note on what to supply.
- **Safe** — dev theme only, page created unpublished, approval before install and before publish.

## Related skills
`eca-meta-ads-4pi` · `eca-ad-copywriting` · `eca-brand-intelligence` · `eca-seo-ai-audit`
