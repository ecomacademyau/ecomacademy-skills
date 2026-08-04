# ECA Landing Pages — a Claude Code skill

Build a high-converting landing page for an ad campaign directly into a Shopify theme — as **editable theme sections**, not a hardcoded one-off.

Built by **Ecommerce Academy**. Runs in **Claude Code** (needs the Shopify CLI).

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

## How it works
1. **Scope + pull the ad** — reads the real ad copy/angle from the Meta Ads MCP, plus `brand-data.md` for voice, personas, proof and claim rules.
2. **Write the content** — full copy presented for approval before anything is installed.
3. **Build into the theme** — Shopify CLI duplicates the **live theme into a dev theme** (live is never touched), installs only the sections that format needs, writes the approved copy into the template, pushes, and returns a preview link.
4. **Create the page unpublished** and hand over: preview URL, remaining placeholders, how to publish, and a reminder to point the ad at the new page.

## What gets installed
```
sections/
  eca-lp-hero.liquid              Hook + media + CTA + risk removal
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
