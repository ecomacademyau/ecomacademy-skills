---
name: eca-seo-ai-audit
description: Audit a Shopify store for visibility in BOTH search engines (Google/Bing) and AI answer engines (ChatGPT, Perplexity, Claude, AI Overviews — GEO/AEO), score it 0–100 in plain English, and walk the member through the fixes as a simple Now / Later / Ongoing plan — applying them on approval. Use whenever the member wants an SEO audit, technical SEO check, store/site audit, help ranking in Google or AI, an "AI visibility" / "answer engine" / GEO / AEO review, wants to check schema, robots.txt, llms.txt, indexing, H1s, sitemaps, keywords, or asks "why aren't we showing up in Google/AI", "how do we get found by ChatGPT", "audit my store's SEO", or "make my store AI-ready". Requires Shopify, Google Search Console, Bing Webmaster, DataForSEO, and the Claude in Chrome connector — it helps connect any that are missing and won't run a half-blind audit without them. Built to run monthly. Works for any Shopify store.
---

# SEO + AI Audit (eca-seo-ai-audit)

**The job: raise a store's *visibility* in search (Google/Bing) and AI answer engines (ChatGPT, Perplexity, Claude, AI Overviews).** The skill connects the right tools → works out the best keywords and how the store currently appears → audits technical, on-page and off-page → gives a **simple score out of 100** → walks the member through the **quick wins first** as a **Now / Later / Ongoing** plan → and, on approval, makes the changes for them.

**The outcome that matters: move the Visibility Score as close to 100 as possible.** So work with *continuity* — complete one fix, re-score, and move straight to the next, driving down the whole plan rather than stopping after a single win.

## How to communicate (read first — this matters as much as the audit)
- **Write for a non-technical store owner.** Plain English, short sentences. Say *what* it is and *why it helps them get found* — skip the jargon.
- **Never be alarmist.** Don't dump scary numbers or exhaustive data; non-tech owners get overwhelmed. Surface only what matters and what to do about it.
- **Always lead with quick wins** — the fixes with the highest chance of increasing *visibility* for the least effort.
- **Visibility ≠ capture.** The job is getting *found* (indexed, ranked, AI-cited). CTR/clicks is a separate traffic thing — mention it if useful, but don't score it as SEO.

## Step 1 — Connect the tools (REQUIRED — do not proceed without them)
A thorough audit needs the full stack. **Check each is connected AND actually returning data (connected ≠ usable — try it). If any is missing or gated, STOP and help the member connect it before continuing — don't run a half-blind audit.**

Required stack (and what each unlocks):
- **Shopify** (read + write) — read the catalog/SEO fields; apply approved fixes.
- **Google Search Console** — real impressions, clicks, positions, index coverage.
- **Bing Webmaster** — Bing indexing (the prerequisite for ChatGPT citation).
- **DataForSEO** — real rankings, keyword volumes, page-speed (Lighthouse), backlinks, AI-mention data. Custom connector: `https://mcp.dataforseo.com/mcp` (member's API login).
- **Claude in Chrome** — render pages to read live schema, and read the GSC/Bing dashboards directly when there's no paid connector.

**Check before you suggest connecting — never recommend linking a tool you haven't tried.** For each tool, actually attempt to use it first (open Search Console / Bing Webmaster via Claude in Chrome and confirm the property loads; make a real DataForSEO/Shopify call). Only suggest connecting a tool once you've confirmed it's genuinely missing or failing — suggesting "connect Bing" when it's already accessible in the browser is a bug.

Act on gaps, don't just flag them:
- Search the connector registry and surface **Connect buttons** (Supermetrics or Ahrefs can pipe GSC/Bing; DataForSEO is a custom connector).
- **GSC/Bing the free way:** if the member is signed into Search Console / Bing Webmaster in Chrome, read the dashboards directly via Claude in Chrome — confirm the **right account *and* property** (a signed-in account may only have other properties).
- Watch for **connected-but-unusable**: plan-gated (e.g. Semrush/DataForSEO without the right plan) or scope-denied. Help resolve or swap before proceeding.

## Step 2 — Keywords & how you currently appear
Before judging the site, learn what it should rank for and where it stands. Using **GSC + Bing + DataForSEO**:
- **Current appearance** — top queries, positions, impressions and which pages rank (GSC/Bing Performance); note branded vs non-branded.
- **Best keywords to target** — the highest-opportunity terms: category-relevant, real search volume, and where the store already has a foothold (ranking ~5–20, or lots of impressions) so it can climb fastest.
- **AI appearance** — is the brand mentioned/cited in AI answers for the category, and who is cited instead? (DataForSEO AI-mention data.)
- **Content gaps → a content plan** — from **GSC** (queries you get impressions for but don't rank or have no dedicated page, and question/informational-intent searches) + **DataForSEO** (keyword ideas, related & question keywords, search intent, and the **topics AI cites competitors for**), list the specific articles/pages worth creating. This feeds the blog-writer handoff in Step 7 / Step 8.
Output a short target-keyword list, the content-gap list, and a one-line "here's where you stand", in plain English.

## Step 3 — Technical audit
Foundations & crawlability (`references/audit-checklist.md`, Layers 1 & 3): index coverage (GSC), robots.txt, sitemap, llms.txt, **agentic-commerce setup** (agents.md + UCP/MCP endpoints + AI-agent feeds — if absent, recommend installing/configuring the agentic app), canonicals, **rendered** schema (via Chrome — never theme source alone), and real page speed / Core Web Vitals (DataForSEO Lighthouse + GSC). Also:
- **Build a full page inventory (every URL).** Pull all products/collections/pages/blogs from Shopify + `/sitemap.xml`, cross-check against GSC index coverage (indexed vs not, and *why*), and run a **DataForSEO On-Page crawl** for a page-by-page status. So nothing's missed — you can account for every page.
- **Run a duplicate-content pass — two kinds:**
  - *Duplicate URLs* (Shopify traps): `/products/` vs `/collections/…/products/` paths, variant & pagination canonicals, filtered/sorted/tag URL sprawl, near-duplicate / sale-clone / test products. Separate *expected* duplication (correctly canonicalised) from the real problem (see Guardrails).
  - **Do the heavy data work in code, not in context.** For the full inventory *and* the content-duplication comparison: pull the URLs/descriptions in bulk, then run the reconciliation and the exact-match + similarity comparison **programmatically in the sandbox** (hash for exact dupes, a text-similarity pass for near-dupes), and surface only the **flagged results / summary**. **Never read every product's full description into the conversation** — that's token-expensive and won't scale past a few dozen products.
  - *Duplicate body copy* (text): **pull every product, collection and page description + meta from Shopify and compare them for similarity** — flag identical or near-identical descriptions, manufacturer boilerplate, and sale-clones carrying the main product's copy (supplement with DataForSEO Content Analysis). Rewrite the duplicates or consolidate the pages.

## Step 4 — On-page audit
(Layer 2): titles & meta (relevance / keyword targeting for the Step-2 keywords), one descriptive H1, heading structure, unique product/collection copy, content depth, internal linking, image alt.

## Step 5 — Off-page audit
(Layer 5): backlinks / authority (DataForSEO, if enabled) and **off-site AI presence** — brand mentions, third-party/review/listicle presence, Reddit/Wikipedia/YouTube, and citation share. This is usually the biggest AI-visibility gap.

## Step 6 — Deliver: full report on file + simple summary in chat
Produce **two** things:
1. **The full, detailed audit as a markdown file**, saved to the member's folder — every layer with the real numbers and findings, the per-layer scores, the keyword & current-appearance tables, the measurement data (GSC/Bing/DataForSEO), and the specific fixes. This is the record they keep and track month to month. Do the *thorough* audit here.
2. **A short, plain-English summary in chat** — **show the overall Visibility Score /100 AND the scorecard table** (the per-area breakdown with 🟢/🟡/🔴 status) right in the chat, then the simple picture (where they're strong, where the easy wins are), non-technical and non-alarmist. The score + table are the at-a-glance view; **explain the findings simply — don't make them read the file.** Lead the chat with this summary; the file holds the depth. Share the file with the member.

## Step 7 — The plan: Now / Later / Ongoing
Turn findings into an easy plan, **quick wins (highest visibility gain, least effort) first**, each explained step-by-step in plain language:
- **Now** — quick, high-impact visibility wins (fix a weak/wrong title on a page already getting impressions, submit sitemaps to GSC/Bing, add a missing FAQ answer, fix a broken redirect).
- **Later** — bigger projects (indexing/catalog cleanup, comparison/answer content, schema additions).
- **Ongoing** — habits that compound: **publish answer-first content from the data-driven content plan** (the queries, questions and AI-citation gaps found in Step 2), **handed to the `blog-writer` skill** to write and draft to Shopify (it produces SEO + AI-answer-engine-optimised posts — answer-first, question-headed, comparison/"best of", buying guides); build off-site/AI presence; and re-audit + re-score monthly. This content loop is the compounding lever for *both* search and AI visibility.

## Step 8 — Implement (on approval)
Where you can, **make the changes for the member** — but always show the change, get approval, then apply: content via the Shopify tools; **anything that needs code/theme editing → have the member do it in Claude Code** (if they're not there, tell them to connect and switch to it) rather than editing code from here; app-based via config (`references/fixes-playbook.md`); **when creating OR rewriting any content, always call the `eca-blog-writer` skill to write it** — new pages/posts/FAQs *and* rewrites of existing product/collection/page copy. The audit decides *what's* needed; blog-writer writes it on-brand and SEO + AEO optimised. Never write substantive content inline. **Any content this skill adds or creates ships SEO + AEO ready — including its structured data.** Answer-first and question-headed, with a proper title, meta description, H1/heading structure and internal links, PLUS the matching schema: **FAQ content → always FAQPage JSON-LD; blog posts → Article schema; product/collection copy → keep Product/Collection schema intact.** Never publish content without its schema — if the schema is theme/code-level, generate it and route that edit to **Claude Code** (or the store's SEO/FAQ app), and don't call the content "done" until the schema is **live and validated on the rendered page**. Re-check it landed, **re-score**, and show the before → after so the win is visible.

**Be persistent — work the plan to the end.** After each approved fix lands and is re-scored, **move straight to the next item** (propose → approve → apply → re-score → next), ticking off Now → Later → Ongoing, until the plan is done or the member stops. Don't stop after one win or wait to be re-prompted — keep momentum toward the highest score. Keep them oriented as you go: "X of Y done, score now Z, next up is…". Pause only when the member defers, or a step needs *their* action (Claude Code for code/theme, an external account/verification).

## Guardrails
- **Required tools first** — connect the full stack (Step 1) or stop; no partial audits.
- **Double-check anything that needs explaining** — never report a raw/alarming number without drilling into the *why* and separating expected from actionable. **Verify on the real thing, not one source:** confirm schema *and page content* on the **RENDERED page (Claude in Chrome)** — Shopify's API often returns blank/thin content for pages whose text is injected by theme sections, page-builder apps or metafields, so never flag a page "empty/thin" (or feed it to the duplicate/thin-content checks) from an API response alone.
- **Visibility ≠ capture** — don't score CTR/clicks as SEO.
- **Every action requires the member's explicit approval — no exceptions.** Propose → approve → apply. Never edit the live theme directly; real data only, no invented facts.
- **Code/theme edits belong in Claude Code.** If a fix needs editing code (theme files, `robots.txt.liquid`, JSON-LD snippets, H1 templates, etc.) and the member isn't already in **Claude Code**, tell them to connect and use Claude Code to make those updates — don't attempt code edits from here. Content edits (SEO fields, product/collection copy, metafields) can be done here via the Shopify tools, on approval.
- **Process large data in code, not in context.** Full crawls, page inventories and content-duplication comparisons must run in the sandbox and return only the flagged results — never pull a whole catalog's text into the conversation (it doesn't scale and burns tokens).
- **Content you add is SEO + AEO ready, or it isn't done.** Every FAQ, post, page or product edit ships answer-first *and* with its structured data (FAQPage / Article / Product). Publishing FAQ questions with no FAQPage schema is a bug — pair content with its schema every time.
- **Content creation or rewrite → always call `eca-blog-writer`.** The audit identifies what content is needed; it does not write substantive content itself.
- **Persistent — drive toward 100.** The outcome is the Visibility Score as close to 100 as possible; keep working the fix list step by step, completing each and moving to the next. Don't drop the thread after one fix.
- **Non-alarmist, plain English, quick-wins-first** — every time.

## Reusing
Works for any Shopify store; brand-agnostic. See `README.md`.
