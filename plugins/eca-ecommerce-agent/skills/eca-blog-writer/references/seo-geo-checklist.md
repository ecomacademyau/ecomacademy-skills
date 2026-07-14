# SEO + GEO Checklist

Two overlapping goals: rank in classic search (**SEO**) and get cited by AI answer engines — ChatGPT, Perplexity, Google AI Overviews, Gemini, Copilot (**GEO**, generative engine optimisation). The good news: they reward most of the same things. GEO adds a few structure/citation requirements on top of solid SEO. Run every post against this list before publishing.

## The single most important rule
**Answer the core question in the first ~50–200 words.** AI engines that retrieve in real time (Perplexity, AI Overviews) judge a page largely on its opening — they pull from pages that answer directly and early. The same opening wins featured snippets. Don't warm up to the answer; lead with it, then deepen.

## On-page SEO

- [ ] **Primary keyword** appears in: the title, the first paragraph, at least one H2, the URL slug, and the meta description. Natural use only — no stuffing.
- [ ] **Title tag** ~50–60 characters, keyword near the front, compelling.
- [ ] **Meta description** ~150–160 characters, includes the keyword, reads like a promise/benefit. (Set via the article's `global.title_tag` / `global.description_tag` metafields — see `shopify-publishing.md`.)
- [ ] **URL slug** short, lowercase, hyphenated, keyword-bearing, no stop-word clutter.
- [ ] **One `<h1>`** (Shopify renders the article title as H1 — don't add a second). Logical `<h2>`/`<h3>` hierarchy beneath.
- [ ] **Editorial images between sections** — captioned figures that illustrate the content (separate from product cards), roughly one every 2 to 3 sections, scaled to length. They lift dwell time/engagement and can rank in image search. A post of only text + product boxes is under-built.
- [ ] **Descriptive `alt` text** on every image (helps SEO, accessibility, and image search; AI engines read it too).
- [ ] **Image filenames follow a convention** — lowercase, hyphenated, keyword/topic-bearing (e.g. `liquid-coffee-concentrate-office-desk.jpg`), not `IMG_1234.jpg`.
- [ ] **Hero image is visually distinct** from the previous blog's hero (don't reuse the same shot post after post).
- [ ] **All images the right ratio** (hero ~16:9 / 1200x630) and uploaded to the store CDN.
- [ ] **Internal links** — at least one to the product(s) and one to a related post/collection. This spreads authority and keeps readers on-site.
- [ ] **External link** to 1–2 credible sources where a claim benefits — signals trustworthiness.
- [ ] **Content depth** that fully covers the topic. Match or beat the comprehensiveness of what's ranking; don't pad.
- [ ] **Readability** — short paragraphs (2–4 sentences), plain language, front-loaded sentences.

## GEO — getting cited by AI engines

- [ ] **Answer-first opening** (the rule above).
- [ ] **Question-style headings** that mirror how people ask ("How do I…", "What is…", "Is X better than Y"). Each H2 is a self-contained answerable unit.
- [ ] **Self-contained sections** — each section makes sense lifted out of context, because that's how an AI quotes it.
- [ ] **Definitive, specific statements** — numbers, timeframes, named steps, concrete examples. Vague copy doesn't get cited; specifics do.
- [ ] **Data & citations** — include relevant stats/facts and cite the source. Citation-friendly, evidence-backed pages are disproportionately pulled into generated answers.
- [ ] **At least one table** — comparison tables, spec tables, and "X vs Y" tables are extracted directly into AI answers and snippets.
- [ ] **Lists** — numbered for sequences/rankings, bulleted for sets. Highly extractable.
- [ ] **An FAQ block** of 3–6 real "People Also Ask" questions with concise, complete answers. The highest-leverage single GEO element — it feeds AI answers and FAQ-rich results. (Add FAQPage structured data if the theme supports it.)
- [ ] **Freshness signals** — current facts, a recent date; update cornerstone posts periodically. AI engines favour current sources.
- [ ] **Entity clarity** — name the brand, products, and key concepts explicitly and consistently so engines associate them correctly.
- [ ] **Beat the current AI citations** — from the DataForSEO AI-mention data (research phase), you know which sources AI cites for this topic today; this post must be more specific, better-structured and more current than them, so it earns the citation.

## Structured data (if the theme/app allows)
- [ ] `Article` / `BlogPosting` schema (most Shopify themes add this automatically).
- [ ] `FAQPage` schema for the FAQ block.
- [ ] `Product` schema on the linked products (the PDP handles this).

## Conversion (the reason the post exists)
- [ ] **2–4 product-insert cards**, each placed where the content naturally calls for the product.
- [ ] The product framed as the **practical answer** to the problem the post solves — not bolted on.
- [ ] **Contextual inline link** on the product's first mention in the body.
- [ ] **Closing CTA block** with the offer/guarantee from config.
- [ ] Every `{{PLACEHOLDER}}` in the insert components replaced with real data. **Verify none remain.**

## Final pre-publish pass
- [ ] Read it as a customer: does the opening answer the question? Would you click the product?
- [ ] Read it as an AI engine: could you quote three self-contained, factual passages from it?
- [ ] **No em-dashes anywhere** ("—") in the body, title, meta description, captions, or product cards. Search the final HTML for the character and remove every one. No en-dash ranges either ("5-10", not "5–10").
- [ ] **Word count 1,000 to 1,500** (longer only for pillar/ultimate guides).
- [ ] No keyword stuffing, no fabricated facts/quotes, no leftover placeholders, no broken links.
- [ ] Brand voice consistent throughout.
