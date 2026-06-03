---
name: eca-brand-intelligence
description: Load the brand's full identity — story, market, competitors, products, voice, visual rules, and ICP — before producing any customer-facing content or making strategic suggestions. Use this skill whenever the user asks Claude to write, edit, or review marketing copy, product descriptions, ad creative, email/SMS, social posts, landing-page content, blog articles, FAQ, customer-service replies, value-prop work, or positioning decisions — even if the user doesn't mention the brand by name. Also trigger when the user asks "is this on-brand?", "how would we say X?", "who's our customer?", "who are our competitors?", or wants to evaluate an opportunity against the brand's positioning. The skill works for any brand by swapping the `brand-data.md` file.
---

# Brand Intelligence

This skill loads a brand's full identity into context so any subsequent copy, content, or strategic recommendation is grounded in the real brand — not generic ecommerce best practice.

The skill is **brand-agnostic in structure but brand-specific in content**. The logic for *how* to use brand context lives in this `SKILL.md`. The actual brand details live in `brand-data.md`. To use this skill for a different brand, fork the folder and replace `brand-data.md` (see `templates/brand-data-template.md` and `README.md`).

## How to use this skill

### Step 1 — Always read the brand data first

Before producing any output covered by this skill, read `brand-data.md` in this folder. The whole file. Don't skim — every section earns its keep:

- **Brand essence** tells you what story to tell
- **Voice & tone** dictates the words to use and avoid
- **Visual identity** governs anything visual (image briefs, ad mocks)
- **Products** prevents you inventing SKUs, prices, or claims that don't exist
- **Market** gives you the macro story to anchor positioning
- **Competitors** tells you who we're winning against and how
- **ICP & personas** tells you who you're speaking to

If a section says "TBD — needs founder input", flag the gap to the user rather than inventing content. Inventing brand facts is the single most damaging thing this skill can produce.

### Step 2 — Match the work to the right sections

Different tasks lean on different parts of the brand data. Use this as a guide, not a rigid rule:

- **Product copy / PDPs** → Products, ICP, Voice, Brand essence
- **Email / SMS** → Voice, ICP, current campaign context
- **Ads (paid social / search)** → ICP, Competitors (for differentiation hooks), Voice, Visual identity
- **Social organic** → Voice, Brand essence, Visual identity
- **Landing pages** → All of the above; especially Market + Competitors for positioning, ICP for hierarchy
- **Blog / SEO** → Voice, Market, Products, ICP
- **Customer service replies** → Voice (warmth/brand-appropriate empathy), Products (accurate info)
- **Strategic suggestions / opportunity evals** → Market, Competitors, Brand essence, Products

### Step 3 — Apply the voice, don't paraphrase the brief

The voice section in `brand-data.md` describes how the brand actually speaks. Use the example phrases as a calibration target, not as snippets to splice in. If the brand voice is "warm, direct, slightly cheeky", a paragraph that *describes* the voice without *embodying* it has failed the brief.

A quick self-check before returning copy:
- Would the founder read this aloud without wincing?
- Does it contain any phrases the voice guide says to avoid?
- Is it doing the brand's job (selling, connecting, differentiating) — or just describing the product?

### Step 4 — Cite competitors and market only when it sharpens the work

Don't shoehorn competitor mentions into customer-facing copy unless the comparison is genuinely useful (e.g., a "why us" page, a comparison ad). But *do* let competitor positioning inform the angle of attack — if a competitor owns "cheapest", we don't compete on price; we compete on the axis they've vacated.

### Step 5 — Flag conflicts

If the user's brief asks for something that contradicts the brand (e.g., a hard discount tone when the brand is positioned premium, or a claim the product can't back up), say so. Offer the on-brand alternative. The user can override — but they should make that call knowingly.

## What this skill is NOT for

- **Generating brand strategy from scratch.** This skill *applies* the brand; it doesn't invent it. If the brand data is thin, the right move is to fill `brand-data.md` first, not to wing it.
- **One-off factual lookups** (e.g., "what's the SKU for vanilla?"). Reading the file is fine, but a full skill invocation isn't required.
- **Generic ecommerce best-practice questions** ("what's a good email subject line length?"). Those don't need brand context.

## Reusing for other brands

This skill folder is designed to be forked. Copy the folder, swap `brand-data.md` for a new brand's version (use `templates/brand-data-template.md` as the starting point), and rename the skill if you want both available side-by-side (e.g., `brand-intelligence-acme/`). The logic in this `SKILL.md` doesn't need to change — it's brand-agnostic by design.

See `README.md` for the full fork-and-customize walkthrough.
