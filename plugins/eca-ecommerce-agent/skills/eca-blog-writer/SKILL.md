---
name: eca-blog-writer
description: Research, write, and publish SEO + AI-answer-engine optimised blog posts AND advertorial/founder-story sales pages for a Shopify store — end to end. Use this skill whenever the user wants a blog post, blog article, blog idea, content for their store blog, an SEO article, a "how-to" or listicle or comparison or buying guide, a product-review style post, a pillar/ultimate guide, an FAQ/answer post, a myth-busting post, OR an advertorial / advertorial blog post / PR push / PR or news-style article / native-advertising piece / founder story / "our story" page / story-led sales page (any angle). Also trigger for "what should I blog about", "find blog topics", "research keywords for content", "write an article about X", "turn this product into a blog post", "write an advertorial", "publish this to Shopify", or any request to create content designed to get indexed and cited in Google and AI engines (ChatGPT, Perplexity, AI Overviews), to convert paid traffic, or to drive click-throughs to products. The skill runs research → ideas → draft → structure/product-inserts → Shopify publish (as a draft for review). Brand-agnostic in logic; everything brand-specific lives in config.md.
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

- **Gate 1 — Approve the title, the products, and the media.** After research, present the ranked blog ideas as **specific candidate headlines** and **stop**. Do not start writing until the user has (a) approved the **exact final title** and style — if they only name a topic, offer 2–4 concrete headlines and get the wording signed off, don't invent it yourself; (b) confirmed **which products** to feature/recommend; and (c) approved an **image/media plan** — including the editorial (in-between) images, not just the product cards. Recommend titles, products, and a concrete image plan so it's a quick yes/no — never just guess, and never silently ship a post with no editorial images. (End of Phase 2 + Phase 2.5.)
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

## Phase 1 — Keyword & topic research (start with DataForSEO)

The aim is to write about what people **actually search and ask** — grounded in **real data**, not assumptions. **All Ecommerce Academy members have DataForSEO connected, so start there**, then enrich with the free methods for the *language* and *angle* raw numbers can't give. Read `references/research.md` for the full method + exact tools. Stop when you have enough signal (a primary keyword + 5–15 supporting questions + the AI-citation gap). **If DataForSEO isn't connected, fall back to the free methods and note volumes are directional — never block.**

**Start here — DataForSEO (real search + AI data):**
1. **Demand, difficulty & intent** for the seed keyword (`dataforseo_labs_google_keyword_overview`, `bulk_keyword_difficulty`, `search_intent`).
2. **The question cluster** — expand to related & question keywords (`keyword_ideas`, `keyword_suggestions`, `related_keywords`); the how/what/why/best/vs terms become your H2s and FAQ block.
3. **Striking-distance** — the store's own ranked keywords at position ~5–20 (`dataforseo_labs_google_ranked_keywords`) where one post jumps to page one; the fastest wins.
4. **The SERP + AI answers** — who ranks and whether there's an AI Overview (`serp_organic_live_advanced`), and **which sources AI engines cite for the topic** (`ai_opt_llm_ment_top_domains` / `ai_opt_llm_ment_top_pages`, `ai_optimization_llm_response`). Write to become a more citable source than those — this is the AEO win.

**Then enrich (free, always valuable):**

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

Output of this phase: a primary keyword/topic, search intent (informational / commercial / transactional), a cluster of supporting questions and subtopics, the **AI-citation gap** (which sources AI engines cite now, from DataForSEO — the gap your post fills), and the best-fit post style.

---

## Phase 2 — Blog ideas (ranked, specific, style-matched)

Turn the research into concrete ideas. For each idea give:

- **Working title** (the real headline wording, specific and click-worthy, includes the primary keyword naturally).
  - **Title formula:** every title should include at least **two of these three**: (1) a **name** that drives search (an influencer/expert/brand, where relevant), (2) a **number** ("Top 5", "7 Ways", "#1 Rule"), (3) a **clear outcome** ("...Without a Machine", "Stop the Afternoon Slump"). Keep the primary keyword near the front.
  - **CTR test:** picture the title sitting in the live Google results for that query. Would you click it over what's already there? If not, rewrite it before proposing.
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

**Editorial images (propose a plan — don't skip these).** These are the captioned, in-between-the-sections images that make a post feel like a real article — distinct from the product-insert cards. They break up the copy, lift dwell time and engagement (a ranking signal), and can rank in image search. **Proactively propose an image plan** scaled to the post's length and style: where each image sits and what it shows (e.g., "a desk-latte shot in the latte section, a comparison visual under the table, a lifestyle shot near the close"). Let the post's length decide the count — roughly a couple for a short FAQ post, more for a how-to or pillar guide; the hero is always one on top. Don't stuff; every image must earn its place.

Source them **hybrid, in this order** (state which was used so the user knows):
1. **The brand's own photos / Shopify media library first** — search the store's Files/media for a fitting lifestyle or contextual shot before anything else.
2. **Generate on-brand images to fill gaps** — when there's no suitable existing shot and an image-generation tool is available, generate one that matches the brand's visual style. **Always pass the real product in as a reference** for fidelity (the same way the hero was made), so the actual product/label appears — never an AI-invented product.

Present the plan and let the user approve it, swap in their own photos, change placement, or dial the count up/down. (Honour any per-brand image preferences in `config.md`.)

**Video.** Ask whether a video should be embedded and where — a YouTube/Vimeo demo, a product clip, a UGC clip. (Embedded via a responsive iframe — see `references/shopify-publishing.md`.)

**Other media.** A comparison graphic, an infographic, a downloadable, or a customer review/quote to feature.

If the user supplies media, get the URLs/files and note placement. If they have no photos and don't want generated ones, confirm you'll proceed with the hero + product cards only — but always offer the image plan first rather than defaulting to text-only. Capture all of this before Phase 3 so the structure is built around the visuals, not bolted on after.

## Phase 3 — Write the post

Once a topic + style is locked, read the matching section of `references/blog-styles.md` for that style's required structure, then read `references/seo-geo-checklist.md` and write the article to hit both.

**Advertorial is a special case.** If the chosen style is advertorial (Style 8), read `references/advertorial-framework.md` and follow that framework instead of the standard article shape. It is **angle-agnostic**: at Gate 1 pick the angle (news/PR investigative, founder story, personal review, exposé, or listicle-news) and craft the hook, recommending options rather than defaulting to the founder story. Key differences: it is written to convert paid traffic rather than rank, usually published as a Shopify **Page** (not a blog article), and needs real proof and (for news/PR) real on-the-record sources, gathered at Gate 1, never fabricated. It **must include the advertising disclaimer**, and must not impersonate a real outlet/journalist or invent experts, quotes, or awards. The keyword-volume gate and the Phase 6 indexing step are optional for advertorials; the no-em-dash rule and both approval gates still apply.

Non-negotiables for every post (the GEO + SEO baseline):

- **No em-dashes. Anywhere. Ever.** Do not use the "—" character in the body, the title, the meta description, image captions, or product-card copy. Em-dashes read as an AI tell. Use a comma, a full stop, a colon, or brackets instead, and rewrite the sentence if needed. Avoid en-dash ranges too: write "5 to 10" or "5-10", not "5–10". This is a hard rule and a pre-publish check.
- **Length: 1,000 to 1,500 words.** Long enough to fully cover the topic, tight enough to stay read. Pillar/ultimate guides can run longer.
- **No walls of text.** Short paragraphs, broken up with subheadings, bullets, tables, and images. A reader should be able to skim the structure and get the gist.
- **Answer-first opening / hook in the first sentence.** The first ~50 to 200 words must directly answer the post's core question. No slow warmup. AI engines (Perplexity, AI Overviews) weight the opening heavily when deciding what to cite, and it earns featured snippets.
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
- **Editorial images** placed between sections per the approved plan — as captioned `<figure>`s with descriptive `alt` text, roughly one every 2–3 sections (scaled to length). These are separate from the product cards: their job is to illustrate the point and break up the copy. Link one or two through to the product where it's natural (as the reference post does), but most can simply support the content. Use library images first, then generated-on-brand (product-referenced) ones to fill gaps.
- **Approved video / other media** placed where Phase 2.5 said it should go — videos via a responsive iframe (see `references/shopify-publishing.md`). Don't add media the user didn't approve.
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

## Phase 6 — After it goes live: index it and measure it

This runs only once the user actually **publishes** the post live (the default is a draft, so prompt them when they confirm it's live).

**Submit for indexing immediately.** Without this, Google can take a week or more to find the post.
- Go to search.google.com/search-console, select the store's property, paste the full live blog URL into the inspection bar, and click **Request Indexing**. Wait for "URL added to priority crawl queue".
- There's no standard GSC API connector, so this is a guided manual step: give the user the exact URL to submit and the click path. If a GSC connector is ever available, use it.

**Set a 6-week check.** Offer to create a scheduled reminder (6 weeks out) to review the post's impressions and clicks in Search Console. If it's getting impressions for the target keyword, that's the signal to consider a small Google Search ad to amplify the organic traffic. Once the brand has 3 to 5 posts live, compare impressions and treat the best performer as the benchmark.

(Repurposing into email/social is intentionally out of scope for this skill, use the brand's email and ad-copy skills for that.)

## A note on quality over volume

The goal is posts that get indexed and cited and that send qualified clicks to products — not a content farm. One genuinely useful, well-structured, well-researched post beats five thin ones for both Google and AI engines. Write each post so that if a customer found only this page, they'd get the full answer and the obvious next step (the product).
