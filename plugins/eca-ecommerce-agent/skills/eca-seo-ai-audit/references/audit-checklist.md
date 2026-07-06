# The Audit Checklist — SEO + AI (GEO/AEO)

Score every item **Pass / Needs work / Missing** with the specific finding (which page/field, what's wrong). Three layers: Technical, On-page, and AEO/AI. Prioritise fixes by impact × effort.

> Context that shapes the AI layer (2026): AI answer engines don't index whole sites — they retrieve and cite. ChatGPT's web results are powered by **Bing** (Bing indexing is a prerequisite to be cited there). Perplexity and AI Overviews favour **recent, citable, answer-first** content. **FAQPage JSON-LD** is the single highest-impact structured-data type for AI (still parsed by AI engines even though Google retired the FAQ rich result for general search in May 2026). The metric that matters is **citation share** — how often the brand is named in AI answers vs competitors.

---

## Search Console & Bing Webmaster — the measurement layer (required)

> **Part of the required tool stack** (see SKILL.md Step 1). Without them the audit is half-blind — no real impressions/clicks/positions or index-coverage truth. Connect them (a connector, or read the dashboards via Claude in Chrome) before running.

Get found *and prove it*. Google Search Console (GSC) and Bing Webmaster Tools (BWT) are both the **diagnostics** that reveal problems the on-site checks miss and the **scoreboard** that shows the Visibility Score is moving for real reasons (real impressions, clicks, rankings). Connect them early and use their data throughout the audit and every monthly re-run.

| Check | What good looks like | Why it matters |
|---|---|---|
| **GSC connected & verified** | Property verified; coverage, performance & CWV readable | The best source of truth for how Google sees the store |
| **Bing Webmaster connected & verified** | Property verified (import from GSC is quick) | **Prerequisite for ChatGPT citation** — ChatGPT's web results run on Bing |
| **Sitemaps submitted** | `/sitemap.xml` submitted in both, no errors | Faster, complete indexation |
| **Index coverage clean** | Key pages Indexed; no unexpected Excluded/Errors; no manual actions | Catches deindexed/blocked pages on-site checks miss |
| **Query & CTR data reviewed** | Top queries, impressions, positions and low-CTR pages known | Prioritise by real opportunity; write titles/metas that lift CTR |
| **Core Web Vitals (field data)** | Green LCP/INP/CLS at the 75th percentile, mobile | Real-user speed — the version Google actually ranks on |
| **IndexNow enabled** | New/changed URLs pushed to Bing instantly (Shopify app) | Speeds AI discovery via Bing |

**GSC example-URL lists are hard to scrape** — the drill-down tables lazy-load and often won't extract via the page reader. Use GSC's **Export** button, or **cross-reference the reason breakdown with the store's live catalog** (draft/duplicate/test products, demo/thin pages) to identify the offending URLs — that mapping is more actionable than raw URLs anyway.

**No GSC/Bing connector? Read it via Claude in Chrome.** If the member is signed into Search Console / Bing Webmaster in their browser, open the dashboards with the browser tools and read the Performance and Index-coverage screens directly — no paid connector needed. **Confirm the right account *and* property first:** a signed-in Google account may only have *other* properties (e.g. an agency/parent-brand login), and hitting the store's property URL will return "you don't have access" — in which case the member must sign in with the owning account, be granted access (Settings → Users & permissions), or verify the property.

**Use this data in the audit:** set the baseline from GSC/BWT (real impressions/clicks/positions), prioritise fixes where impressions are high but CTR or position is weak, and on the monthly re-run **show GSC performance alongside the Visibility Score** so improvement is proven in real traffic, not just the checklist. These foundational checks are scored within the **Technical / crawlability** layer.

## Layer 1 — Technical / crawlability

| Check | What good looks like | How to check on Shopify |
|---|---|---|
| **robots.txt** | Serves at `/robots.txt`; blocks low-value paths (cart, checkout, internal search, account) without blocking products/collections; links the sitemap | Fetch `/robots.txt`; customise via `robots.txt.liquid` in the theme |
| **XML sitemap** | `/sitemap.xml` present, auto-updating, submitted to Google Search Console + Bing Webmaster | Shopify auto-generates; confirm it loads and is submitted |
| **Indexability** | Key pages return 200 and are indexable; no accidental `noindex`; thin/duplicate pages managed | Check meta robots + Search Console coverage |
| **Canonical tags** | Every page has a correct self-canonical; variant/duplicate URLs point to the canonical | Inspect page `<head>`; Shopify sets defaults but check collection/tag pages |
| **HTTPS + redirects** | All HTTPS; no redirect chains; old URLs 301 to new; no broken internal links (404s) | Crawl key pages; check redirects in Shopify admin |
| **Site speed / Core Web Vitals** | Fast LCP, low CLS on mobile; images compressed & lazy-loaded; minimal heavy apps | PageSpeed Insights / Search Console; audit theme + apps |
| **Mobile-friendly** | Responsive, tappable, readable on mobile | Render on mobile viewport |
| **URL structure** | Clean, readable handles; consistent; no orphan pages | Review product/collection handles |

## Layer 2 — On-page SEO

| Check | What good looks like | Where on Shopify |
|---|---|---|
| **Title tags** | Unique, ≤~60 chars, primary term near the front, brand at end | Page/product/collection **SEO title** field |
| **Meta descriptions** | Unique, ~150 chars, benefit + soft CTA (drives CTR) | **SEO description** field |
| **One H1 per page** | Exactly one H1, describes the page, contains the primary term | Theme templates; product/collection titles usually become H1 |
| **Heading hierarchy** | Logical H2/H3; questions as headings where relevant | Page/blog content + templates |
| **Image alt text** | Descriptive alt on product & content images | Product media alt fields; theme |
| **Unique product/collection copy** | Original, useful descriptions (not manufacturer boilerplate); collection pages have intro copy | Product/collection body; metafields |
| **Internal linking** | Products link to related products/collections; blog links to products; key pages ≤3 clicks deep | Content + navigation |
| **Content depth** | Important pages answer the query fully; blog covers buyer questions | Pages/blog |

**Blogging & internal linking carry real weight — for both SEO and AI.** A blog is how a store builds **topical authority** and targets the long-tail **question queries** AI answers; **answer-first blog posts, comparison/"best of" and buying-guide content are prime citation fodder** for ChatGPT/Perplexity/AI Overviews (and often the only pages that rank for informational queries). **Internal links** distribute authority, aid crawl/discovery, keep key pages ≤3 clicks deep, and pass relevance — especially **blog → product/collection** links, which also convert. Audit: is there a real content cadence? Do posts answer buyer questions and link to products? Are collections/products interlinked? Pair fixes with the **blog-writer** skill (answer-first drafts) and feed the questions from brand-data §9/§12 and the off-site category queries.

## Layer 3 — Structured data / schema (JSON-LD)

> **Verify on the RENDERED page, not theme source.** Shopify + review apps inject Organization, WebSite, BreadcrumbList, FAQPage and `aggregateRating` at render time — auditing the theme Liquid alone will report schema as missing when it's actually live. Render the page (Claude in Chrome) and enumerate the `@type`s.

| Schema | Why it matters | Notes for Shopify |
|---|---|---|
| **Product** | Rich results + AI product answers (name, image, price, availability, brand, GTIN, `aggregateRating`/`review`) | Most themes (e.g. Dawn) auto-emit basic Product JSON-LD; verify it includes brand, GTIN, and ratings — add via theme if missing |
| **FAQPage** | **Highest-impact for AI** — each Q&A is a citation candidate | Add JSON-LD on FAQ pages/sections (theme or via metafields) |
| **Organization / Brand** | Establishes the brand as an entity AI can recognise (logo, sameAs socials, contact) | Add to `theme.liquid` head, sitewide |
| **BreadcrumbList** | Site structure signals; breadcrumb rich results | Theme templates |
| **Article** | Blog posts eligible as sources | Blog template |
| **WebSite (SearchAction)** | Sitelinks search box | Theme head |
| **LocalBusiness** | If the brand has a physical presence | Only if applicable |
| **Validation** | No errors/warnings | Test with Rich Results Test / Schema validator |

## Layer 4 — AEO / AI answer-engine readiness (GEO)

| Check | What good looks like | Fix |
|---|---|---|
| **llms.txt** | A curated `/llms.txt` (markdown) listing the key URLs + one-line descriptions so LLMs grab the right pages | Create it; see fixes-playbook for the Shopify workaround |
| **Answer-first content** | The first ~200 words of key pages/posts *directly answer* the query (definition, direct answer), not a slow build-up | Rewrite intros to lead with the answer |
| **FAQs (real questions)** | Pages/sections answering the actual questions buyers ask (pull from brand-data §9 objections + §12 pre-purchase questions), each with a concise answer + FAQPage schema | Add FAQ content + schema |
| **Conversational Q&A headings** | Headings phrased as the questions people ask AI ("Is X worth it?", "X vs Y") | Restructure headings |
| **Entity clarity / E-E-A-T** | Clear About page, consistent brand name/NAP, author + expertise signals, real story | Strengthen About/author; consistency |
| **Citable facts & original data** | Specific numbers, comparisons, and any original data (LLMs prefer grounded, specific info to cite) | Add stats, comparisons, original insight |
| **Comparison & buying-guide content** | "Best…", "X vs Y", buying guides — the formats AI pulls into answers | Create comparison/guide pages |
| **Freshness** | Key pages updated recently; dates visible | Refresh + show updated dates |
| **Bing indexing** | Site verified in **Bing Webmaster Tools** (prerequisite for ChatGPT citation) | Submit + verify |
| **Reviews / social proof on-page** | Ratings and review text visible and in schema | Ensure reviews render + are in Product schema |
| **Crawlable to AI** | Not blocking AI crawlers you want (GPTBot, PerplexityBot, ClaudeBot) in robots.txt unless intentionally | Review robots directives |

## Layer 5 — Off-site AI & brand-entity signals (where AI actually gets its citations)

The uncomfortable truth for 2026: **~99% of AI citations are third-party** — only ~0.85% are a brand's own pages. AI answers are dominated by **Reddit, Wikipedia, YouTube, LinkedIn** and review/comparison sites, and **branded search volume is the single strongest predictor** of whether a brand gets cited. The store can't edit these surfaces, so this layer is audited as a **scored action plan**, not a set of store writes.

Before scoring, **run real category queries** in AI engines / web (e.g. "best [category] in [region]", "[brand] vs [competitor]", "is [product type] worth it") and see whether the brand is cited and **which domains are** — that tells you exactly where to show up.

| Check | What good looks like | Action (member-led) |
|---|---|---|
| **Branded search demand** | Branded searches (people searching the brand name) trending up — the strongest citation predictor | Grow demand: campaigns, PR, creators, memorable content — rising branded search lifts AI citation |
| **Category citation map** | You know which domains AI cites for your category, and you're present on them | Run category AI queries; list the cited domains; target those surfaces |
| **Reddit** | Authentic mentions/threads in relevant subreddits; real discussion (never spam) | Engage genuinely, answer questions helpfully, encourage honest discussion; monitor mentions |
| **Wikipedia / Wikidata** | A **Wikidata** entity so AI recognises the brand; a Wikipedia page only if genuinely notable | Create/claim the Wikidata entry; pursue Wikipedia only if it meets notability — never fake it |
| **YouTube** | Reviews/how-tos about or by the brand (heavily cited by AI) | Publish + encourage creator videos; optimise titles/descriptions to the real questions |
| **Third-party reviews & "best of" listicles** | Strong ratings on Trustpilot/ProductReview/Google; inclusion in "best [category]" roundups & comparisons | Earn reviews; pitch to be included in roundups/comparison articles |
| **Consistent brand entity** | Name, description, socials consistent across the web; `sameAs` in Organization schema links them | Standardise everywhere; link socials via schema (ties on-site to off-site) |
| **Digital PR / trusted mentions** | Mentions on trusted, topically-relevant sites — the third-party evidence AI trusts | Digital PR, guest content, original data others cite (pairs with the blog-writer + competitor-analysis skills) |

**Measure it over time:** track **citation share** — how often the brand is named in AI answers for category queries vs competitors — and re-check monthly. This is the north-star AI metric.

## Scoring — the 0–100 Visibility Score

Score every audit, **before and after fixes**, so the member sees exactly where they stand and how much they've improved.

**How it's scored:** rate each checklist item **Pass = 1 · Partial = 0.5 · Missing/Fail = 0**, average within a layer, ×100 = that layer's 0–100 score. Then weight the five layers into one **overall Visibility Score (0–100):**

| Layer | Weight |
|---|---|
| Technical / crawlability | 15% |
| On-page SEO | 20% |
| Structured data / schema | 20% |
| AEO / AI (on-site) | 20% |
| Off-site AI & brand-entity | 25% |

**Status bands** (per layer and overall): 🟢 **Strong 80–100** · 🟡 **Needs work 50–79** · 🔴 **Weak 0–49**.

**Always output the scorecard table:**

| Area | Weight | Score /100 | Status | Biggest gap |
|---|---|---|---|---|
| Technical / crawlability | 15% | — | 🟢/🟡/🔴 | … |
| On-page SEO | 20% | — | | … |
| Structured data | 20% | — | | … |
| AEO / AI (on-site) | 20% | — | | … |
| Off-site AI & brand-entity | 25% | — | | … |
| **Overall Visibility Score** | 100% | **—** | | |

**Before → After:** on a re-run (after fixes, or the monthly audit), show the comparison so progress is visible:

| Area | Before | After | Δ |
|---|---|---|---|
| … | 55 | 82 | +27 |
| **Overall Visibility Score** | **56** | **84** | **+28** |

Weights are adjustable per brand if priorities differ, but default to the table above. Keep the score honest — it's only useful if it moves for real reasons.

## Prioritising & applying fixes
- **Keep the goal straight: visibility ≠ capture.** This skill's job is *visibility* — getting **found** (indexed), **ranked**, and **cited by AI**. That is SEO / AIO. **CTR — getting the click once you're already shown — is *capture*, not visibility** (it's SERP conversion). Writing a title/meta is a legitimate on-page SEO element (relevance + keyword targeting), and lifting CTR is a valuable *traffic* win, but **CTR is not a reliable ranking signal, so never score it as an SEO/AIO gain**. Prioritise the true visibility levers — **indexing, rankings, AI citation** — first; surface CTR/SERP-conversion opportunities separately, labelled as "traffic now," not as ranking movement.
- Rank fixes **quick high-impact wins first** (usually FAQPage schema + FAQ content, answer-first intros, Product schema gaps, llms.txt, title/meta fixes, Bing verification).
- Tag each fix **[content]** (Shopify tools), **[theme]** (dev-theme/code), or **[off-site]** (action plan) — see `fixes-playbook.md`.
