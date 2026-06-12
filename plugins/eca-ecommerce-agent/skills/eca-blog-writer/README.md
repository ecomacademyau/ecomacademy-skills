# eca-blog-writer

Research, write, and publish SEO + AI-answer-engine optimised blog posts for any Shopify store — end to end. The skill runs **research → blog ideas → _you approve a title_ → write → _you review & tweak the draft_ → publish to Shopify as a draft**.

There are **two approval gates** so you stay in control: you approve a title/idea before any writing happens, and you review (and edit) the full article here before anything is created in Shopify. Nothing reaches your store without your sign-off.

It's built for stores that want content that gets **indexed and cited in Google and AI engines** (ChatGPT, Perplexity, AI Overviews) and that **sends qualified clicks to products**.

## What it does

1. **Research** — finds what people actually search and ask in the brand's category. Free methods first (web search, People Also Ask, autocomplete, communities, competitor blogs, reading what AI engines currently say); paid SEO tools (Semrush/Ahrefs) used only if connected; Google Search Console data used if the user can supply it.
2. **Blog ideas** — a ranked, specific shortlist, each tied to a proven post style and the product it drives to. **→ Gate 1: you approve a title, confirm which products to feature (it recommends, you decide), and flag any video/media to embed — before writing.**
3. **Writing** — full draft in the brand's voice, in the correct structure for the chosen style, optimised for SEO + GEO (answer-first, question H2s, tables, FAQ block).
4. **Structure & inserts** — assembles clean HTML with product-insert cards and a closing CTA block — the click-through engine.
5. **Review** — presents the full draft here for your review, edits, and sign-off. **→ Gate 2: nothing goes to Shopify until you approve.**
6. **Publish** — creates the article in Shopify **as a draft for review** by default (never live unless you ask).

## The seven post styles

Listicle · How-to / educational · Influencer / authority product review · Comparison / "best X for Y" · Question / FAQ answer-style · Ultimate guide / pillar · Myth-busting / problem-solver. Full structure for each in `references/blog-styles.md`.

## Requirements

- **Shopify MCP connected** (with `write_content` scope) — to publish.
- **`eca-brand-intelligence` skill** (recommended) — for brand voice, products, ICP. Works without it but writes more generically.
- **No paid SEO tool required.** Semrush / Ahrefs / GSC are optional power-ups that sharpen prioritisation if present.

## Use it for your brand (fork walkthrough)

Everything brand-specific lives in **one file**: `config.md`. The `SKILL.md`, `references/`, and `assets/` are brand-agnostic — don't edit them.

1. **Copy** this folder into your skills location.
2. **Open `config.md`** and fill in:
   - brand name + where Claude gets brand context (the `eca-brand-intelligence` skill, or your own brief),
   - your store domain and the **Shopify blog** to publish into, plus the default **author**,
   - your **target market** (spelling/currency) and Semrush database code if you use it,
   - the **products to feature** and your **standing offer/guarantee** (for the CTA blocks),
   - your **publishing default** (draft for review is recommended),
   - any preferred post styles.
3. That's it. Invoke the skill and ask for blog ideas, or hand it a topic/product to write about.

Nothing else needs touching — the research method, the SEO/GEO rules, the post-style structures, and the HTML components all work for any store.

## Files

```
eca-blog-writer/
├─ SKILL.md                         # the workflow (brand-agnostic)
├─ config.md                        # the ONLY file you edit per brand
├─ README.md                        # this file
├─ references/
│  ├─ research.md                   # tiered keyword/topic research (free first, paid optional)
│  ├─ blog-styles.md                # the 7 post styles + required structure for each
│  ├─ seo-geo-checklist.md          # on-page SEO + AI-answer-engine optimisation checklist
│  └─ shopify-publishing.md         # exact GraphQL to publish as a draft (articleCreate)
└─ assets/
   ├─ article-skeleton.html         # the reusable body structure ("template")
   ├─ product-insert-card.html      # inline "Recommended" product card
   └─ cta-block.html                # closing single/dual product CTA
```

## Notes

- **Draft by default.** Posts are created hidden (`isPublished: false`) so you review before going live.
- **Influencer style is fact-only.** It references real public figures' publicly-known methods — never fabricated quotes, endorsements, or partnerships. This keeps it legal and trustworthy (which is also what AI engines reward).
- **Quality over volume.** One well-researched, well-structured post beats five thin ones for both Google and AI engines.
