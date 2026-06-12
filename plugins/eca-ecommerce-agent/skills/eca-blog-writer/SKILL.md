---
name: eca-blog-writer
description: Research, write, and publish SEO + AI-answer-engine optimised blog posts for a Shopify store — end to end. Use this skill whenever the user wants a blog post, blog article, blog idea, content for their store blog, an SEO article, a "how-to" or listicle or comparison or buying guide, a product-review style post, a pillar/ultimate guide, an FAQ/answer post, or a myth-busting post. Also trigger for "what should I blog about", "find blog topics", "research keywords for content", "write an article about X", "turn this product into a blog post", "publish this to Shopify", or any request to create content designed to get indexed and cited in Google and AI engines (ChatGPT, Perplexity, AI Overviews) and drive click-throughs to products. The skill runs research → ideas → draft → structure/product-inserts → Shopify publish (as a draft for review). Brand-agnostic in logic; everything brand-specific lives in config.md.
---

# Blog Writer

This skill takes a Shopify store from "we should blog more" to a finished, structurally-correct, conversion-aware article sitting in Shopify ready to publish. It does four jobs in one flow:

1. **Research** — find topics real people are searching for (and asking AI engines) in this brand's category, using free methods first and paid SEO tools only if connected.
2. **Ideate** — turn that research into specific, ranked blog ideas, each tied to one of the proven post styles.
3. **Write** — draft the full article in the brand's voice, in the correct structure for its chosen style, optimised for both classic SEO and AI answer engines (GEO).
4. **Publish** — assemble the HTML (with product-insert cards + CTA blocks that drive click-throughs) and create the article in Shopify **as a draft for review** by default.

The skill is **brand-agnostic in logic, brand-specific in config**. The workflow, the post styles, the SEO/GEO rules, and the HTML components all work for any store. The only file you edit per brand is `config.md`. To use this for a different brand, fork the folder and edit `config.md` — see `README.md`.

## Before you start: load the brand and the config

Customer-facing content is only as good as your understanding of the brand. **Invoke the `eca-brand-intelligence` skill first** so the voice, products, ICP, and positioning are loaded. If it isn't available, read whatever brand brief the user points you to (and tell them the writing will be more generic without it).

Then read `config.md` in this folder for the brand-specific settings: the store's blog, default author, target market, products to feature, publishing default, and house style.

## The golden rule: validate, don't assume

This brand has been burned by silently-inferred defaults. Before writing a full post, confirm the few things that shape it — don't guess. Keep it to one quick pass (see Phase 0). If the user already gave you everything, just restate your understanding in one line and proceed.

## Two approval gates (always stop and wait)

This skill has **two hard checkpoints**. Do not skip or merge them, even if the user seems eager:

- **Gate 1 — Approve the title, the products, and the media.** After research, present the ranked blog ideas as **specific candidate headlines** and **stop**. Do not start writing until the user has (a) approved the **exact final title** and style — if they only name a topic, offer 2–4 concrete headlines and get the wording signed off, don't invent it yourself; (b) confirmed **which products** to feature/recommend; and (c) told you whether there's any **video or other media** to insert. Recommend titles, products, and a media plan so it's a quick yes/no — never just guess. (End of Phase 2 + Phase 2.5.)
- **Gate 2 — Approve the draft.** After writing, present the **full article here in chat for review** and **stop**. Take edits and revise as many rounds as needed. Do **not** create anything in Shopify until the user explicitly approves the draft. (Phase 4.5.)

Only after Gate 2 is passed do you publish (as a draft) in Phase 5. The order is always: research → **Gate 1** → write → **Gate 2** → Shopify draft.

## Two ways to run this skill

- **Idea-first (default):** the user wants topics. Run Phase 1 (research) → Phase 2 (ideas), present a ranked shortlist, get approval (Gate 1), write, present the draft for review (Gate 2), then publish.
- **Topic-given:** the user already has a topic/keyword (or a product to feature). Do a lighter Phase 1 to validate demand and grab the supporting questions, confirm the title/angle (Gate 1), then write and present for review (Gate 2) before publishing.

Both paths pass through both gates. A topic being pre-chosen satisfies Gate 1's intent, but still confirm the exact working title/angle before writing.

---

## Phase 0 — Confirm scope (one quick pass)

Confirm only what you can't safely infer from config + brand intelligence:

- **Goal:** ideas, or a finished post (or a batch)? How many?
- **Topic or open brief:** do they have a topic/keyword/product in mind, or should research pick?
- **Style:** which of the post styles (see `references/blog-styles.md`) — or let the research recommend the best fit per idea.
- **Product(s) to feature:** which product(s) the post should drive clicks to — recommend and confirm in Phase 2.5, don't assume. Default to config's heroes but suggest what's most relevant to this topic.
- **Media:** whether any video or other media should be embedded (confirmed in Phase 2.5).
- **Publish behaviour:** confirm the config default (draft for review). Only auto-publish live if the user explicitly says so.

Don't re-ask anything the user already specified.

---

## Phase 1 — Keyword & topic research (free first, paid if available)

The aim is to write about things people **actually search and ask** — not what we assume. Read `references/research.md` for the full method. Run the tiers in order and stop when you have enough signal (usually a primary keyword + 5–15 supporting questions/subtopics):

**Tier 1 — free, always available (no connector needed). This is the universal baseline:**

1. **Web search** the seed topic and read the top-ranking posts — note their angle, their H2s, and the gaps they leave.
2. **Harvest "People Also Ask" and autocomplete** — search the seed term and its variations; collect the questions and long-tail completions. These map directly to AI-answer-engine queries and featured snippets.
3. **Mine communities** — Reddit, forums, Quora, review sections, and the brand's own reviews/FAQ for the exact phrasing customers use and the problems they raise.
4. **Read AI answers** — ask the question the post will target the way a customer would, and note what a generative engine currently says and cites. Your job is to become a better source than what's there.
5. **Competitor blogs** — scan 2–3 competitor blogs (from the brand-intelligence competitor list) for topics that are working and angles to beat.

**Tier 2 — paid SEO tools, only if connected (optional power-up):**

- **Semrush** (if the Semrush MCP is connected): use `keyword_research` for volume/difficulty/intent, `trends_research` for trending terms, and `organic_research` to see what competitors rank for. Use this to *prioritise* the Tier-1 list by real volume and difficulty — not to replace it.
- **Ahrefs** or similar, if connected: same idea — validate and rank.
- **Google Search Console** data, if the user can provide it (export or connector): the gold mine for "striking distance" posts — queries the store already ranks #5–20 for, where one good article can jump it onto page one. If they have it, ask for the queries; if not, skip.

**Never block on a paid tool.** If none is connected, Tier 1 alone is enough to ship great posts — say so and move on. Note in the final output which tier the data came from so the user knows how hard the volume numbers are.

Output of this phase: a primary keyword/topic, search intent (informational / commercial / transactional), a cluster of supporting questions and subtopics, and the best-fit post style.

---

## Phase 2 — Blog ideas (ranked, specific, style-matched)

Turn the research into concrete ideas. For each idea give:

- **Working title** (specific and click-worthy, includes the primary keyword naturally).
- **Style** (which template from `references/blog-styles.md`).
- **Primary keyword + search intent.**
- **Why it'll rank** — the gap it fills vs what's already out there, and why an AI engine would cite it.
- **Products it drives to** — the natural click-through(s).
- **Priority** — High/Med/Low based on demand × relevance × commercial intent (× how easily we can outrank what's there).

Present as a ranked shortlist and let the user pick. **This is Gate 1 — stop here and wait for the user to approve a title + style before writing.** Don't write any post (or several silently) until they've chosen. If they want tweaks to a title or a different angle, revise the shortlist and re-present.

**Suggest specific titles, and approve the exact final headline — don't just confirm a topic.** Each shortlist item must be a real, ready-to-use **headline** (the actual wording), not a broad subject area. If the user picks a topic or a loose direction, do **not** invent the final headline yourself and proceed — offer 2–4 concrete headline options for that topic (with the research rationale for each) and get them to approve or edit the exact wording first. The approved headline is what you write to; never write under a title the user hasn't seen and signed off on.

---

## Phase 2.5 — Confirm products & media (part of Gate 1)

Once the title is approved and **before writing**, lock two things — recommend, then let the user approve or change. Don't guess your way past this.

**Products to feature / recommend.** Propose the specific product(s) this post should drive clicks to, with a one-line reason each (pull live title/price/image from Shopify; default to the heroes in `config.md`, but suggest the ones most relevant to *this* topic — they may differ from the usual heroes). Ask the user to confirm the list, swap items, add their own, or set the order. The post is built around whatever they approve here.

**Video & other media.** Ask whether anything should be embedded, and where:
- **Video** — a YouTube/Vimeo URL, a product demo, a UGC clip. (Embedded via an iframe — see `references/shopify-publishing.md`.)
- **Images** — lifestyle shots, diagrams, before/afters, a hero image they want used. If they don't supply images, use product imagery from Shopify and say so.
- **Other** — a comparison graphic, an infographic, a downloadable, a customer review/quote to feature.

If they have media, get the URLs/files and note where each should sit (e.g., "demo video under the how-to steps"). If they have none, confirm you'll proceed with text + product/Shopify imagery only. Capture all of this before Phase 3 so the structure is built around it, not bolted on after.

## Phase 3 — Write the post

Once a topic + style is locked, read the matching section of `references/blog-styles.md` for that style's required structure, then read `references/seo-geo-checklist.md` and write the article to hit both.

Non-negotiables for every post (the GEO + SEO baseline):

- **Answer-first opening.** The first ~50–200 words must directly answer the post's core question — don't warm up to it. AI engines (Perplexity, AI Overviews) weight the opening heavily when deciding what to cite, and it earns featured snippets.
- **Question-style H2s** that mirror how people search and ask ("How do I…", "What is…", "Is X better than Y…"). One clear idea per heading.
- **Scannable structure** — short paragraphs, lists, and at least one comparison/spec **table** where it fits. AI engines and snippet algorithms lift tables and lists directly.
- **Definitive, factual statements** with specifics (numbers, timeframes, steps). Cite sources/data where a claim benefits from it — citation-friendliness is what gets a page pulled into a generated answer.
- **Natural keyword use** — primary keyword in the title, first paragraph, one H2, and the meta description; supporting questions as H2s/H3s. Never stuff.
- **One topic, fully covered.** Depth and topical completeness beat thin posts for both Google and AI engines.
- **Brand voice** from brand-intelligence throughout. Helpful and educational first — the selling is woven in, not bolted on.
- **An FAQ block** near the end (3–6 Q&As) using the real "People Also Ask" questions from Phase 1. This is the single highest-leverage GEO element — it directly feeds AI answers and FAQ-rich results.
- **Internal + external links** — link to the product(s) and to 1–2 related posts/collections; link out to a credible source where it supports a claim.

Write the body in clean semantic HTML (see Phase 4) so it drops straight into Shopify.

---

## Phase 4 — Structure & product inserts (the click-through engine)

The reason these posts make money is the **inserts** — the product cards and CTA blocks woven through an otherwise genuinely useful article. Use the components in `assets/` and the rules in `references/shopify-publishing.md`.

Assemble the article body from these building blocks:

- **Featured image** at the top (set as the article image, see Phase 5).
- **Answer-first intro**, then a **table of contents** for longer posts (anchors to each H2).
- **Body sections** per the chosen style's structure.
- **Approved media** placed where Phase 2.5 said it should go — embed videos via a responsive iframe and insert any supplied images with descriptive `alt` text and an optional caption (see `references/shopify-publishing.md`). Don't add media the user didn't approve.
- **Product-insert cards** — `assets/product-insert-card.html`. Drop one in where the content naturally calls for the product (e.g., right after describing the problem it solves). Pull real product data (title, price, URL, image, one-line benefit) from the Shopify store. 2–4 per post is the sweet spot; more than that reads as an ad.
- **Inline contextual links** — link the product name the first time it's mentioned in the body.
- **FAQ block** near the end.
- **Closing CTA block** — `assets/cta-block.html` — a strong dual/single product call-to-action with the guarantee/offer from config.
- Fill the components by replacing the `{{PLACEHOLDERS}}`. Never leave a placeholder in the final HTML — verify before publishing.

Keep the HTML clean and theme-friendly: semantic tags, inline styles only inside the insert components (so they render regardless of theme), descriptive `alt` text on every image (also an SEO/GEO win), and `rel="noopener"` on external links.

**On "templates" in Shopify:** the reusable structure lives in this skill's `assets/` (the body skeleton + insert components) — that's what keeps every post consistent and is injected into the article body. If a brand wants a dedicated branded *theme* template for articles (a custom `article.{suffix}.liquid` layout), that's an advanced, optional step covered in `references/shopify-publishing.md`; set it via the article's `templateSuffix`. Most stores don't need it — the body components are enough.

---

## Phase 4.5 — Review gate (approve the draft before Shopify)

**This is Gate 2. Do not touch Shopify until the user approves.**

When the article is written and assembled, present it to the user **for review here** first:

- Show the **full draft** — render the readable copy in chat (headings, intro, the comparison table, FAQ, and where the product cards and CTA sit). Also save the working draft to the project folder (HTML + a markdown copy) per `config.md` so they can open it.
- Surface anything that needs a human eye: **any factual claims, numbers, prices, or stats** the user should confirm; the **meta title/description**; the **target keyword**; and **which products** it links to.
- Then **stop and ask for sign-off or edits.**

Revise on their feedback — tighten copy, swap the angle, fix a claim, change the products, adjust the CTA — and re-present. Loop as many rounds as needed. Only when the user clearly says it's good do you move to Phase 5.

Never create the Shopify article (even as a hidden draft) before this approval. "Draft in Shopify" is not a substitute for the user reading it here first.

## Phase 5 — Publish to Shopify (as a draft, by default)

Only after Gate 2 sign-off. Read `references/shopify-publishing.md` for the exact GraphQL. The short version:

1. **Pick the blog.** List the store's blogs (`blogs` query) and use the one named in `config.md`. If config doesn't name one, ask which blog. Don't create a new blog unless asked.
2. **Upload/choose the featured image** and set it as the article `image` (with alt text).
3. **Create the article** with `articleCreate`:
   - `title`, `author` (from config), `blogId`, `body` (the assembled HTML), `summary` (the meta-description-length excerpt), `handle` (clean, keyword-bearing slug), `tags`, and `image`.
   - **`isPublished: false`** — this is the draft-for-review default. Only set `true` if the user explicitly asked to publish live.
   - Set the **SEO title and meta description** via the article's `metafield`s (`global.title_tag`, `global.description_tag`) — see the reference; the meta description should be ~150–160 chars, include the primary keyword, and read like a promise.
4. **Validate** the mutation with `validate_graphql_codeblocks` before running it.
5. **Report back** with: the article admin URL (to review/publish), the live URL it *will* have, the target keyword, the products it links to, and the meta title/description used. Remind the user it's a draft awaiting their publish click.

Never publish live without explicit instruction. If publishing fails on a credential/permission error, tell the user which scope is missing rather than retrying blindly.

---

## A note on quality over volume

The goal is posts that get indexed and cited and that send qualified clicks to products — not a content farm. One genuinely useful, well-structured, well-researched post beats five thin ones for both Google and AI engines. Write each post so that if a customer found only this page, they'd get the full answer and the obvious next step (the product).
