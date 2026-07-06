# Fixes Playbook — how to apply each fix safely

Golden rule: **propose → approve → apply.** Content goes through the Shopify tools; theme/technical goes through a **dev theme** (never the live theme). Show a before/after and get a yes before every write. Re-check each fix landed.

## Two lanes

### Lane A — Content fixes (via the Shopify tools / Admin API)
Lower risk, reversible, no theme edit. Apply after approval, one batch at a time.

| Fix | How |
|---|---|
| **SEO title & meta description** | Update the page/product/collection/article SEO fields (via the Shopify tools, or `metafields` `global.title_tag` / `global.description_tag`). One at a time or batched; show before/after. **⚠️ With `productUpdate`/`SEOInput`, always send BOTH `title` and `description` together — omitting one NULLS it (wipes the existing value). Read the current SEO first and pass both.** |
| **Product / collection descriptions** | Rewrite to be unique, useful, answer-first; update the body via the Shopify product/collection update tools. Keep the brand voice (brand-data.md); never invent specs/claims. |
| **Image alt text** | Set descriptive alt on product media. |
| **FAQ content** | Create/expand FAQ as a page or product/collection metafield; source questions from brand-data §9 (objections) + §12 (pre-purchase questions); concise answer-first responses. |
| **Blog / comparison / buying-guide content** | Draft answer-first articles (lead with the answer in the first ~200 words); publish as blog articles. Pair with the blog-writer skill for depth. |
| **Internal links** | Add related-product/collection links and blog→product links in body content. |

### Lane B — Theme / technical fixes (via a DEV theme, or as code to paste)
> **Where to do code/theme edits:** these belong in **Claude Code**, which can work the theme via the Shopify CLI / git. If the member isn't in Claude Code, direct them to connect and switch to it — don't attempt code edits from the chat environment. Every change still goes: propose → member approves → apply → member previews → publish.
Higher risk — **duplicate the live theme to a development theme first** (same pattern as the eca-pdp skill / Shopify CLI), make the change there, let the member **preview then publish**. If no dev-theme access, hand over the exact code to paste and where.

| Fix | How |
|---|---|
| **Product JSON-LD gaps** | Many themes auto-emit Product schema; add missing fields (brand, GTIN, `aggregateRating`, `review`) via a JSON-LD block in the product template. |
| **FAQPage JSON-LD** | Add a `<script type="application/ld+json">` FAQPage block that mirrors the visible FAQ, using Liquid to inject the Q&A. (Highest-impact AI fix — do this early.) |
| **Organization / Brand + WebSite schema** | Add sitewide JSON-LD to `theme.liquid` `<head>` — name, logo, `sameAs` socials, contact; WebSite with SearchAction. |
| **BreadcrumbList / Article schema** | Add to collection/product and blog templates. |
| **robots.txt.liquid** | Customise to block low-value paths (cart, search, account) and keep products/collections open; ensure AI crawlers (GPTBot, PerplexityBot, ClaudeBot) aren't blocked unless intended; reference the sitemap. |
| **H1 fixes** | Ensure exactly one H1 per template; fix templates emitting zero or multiple H1s. |
| **llms.txt** | See below — Shopify needs a workaround. |

### Lane C — Off-site / brand-entity signals (recommendations, NOT store edits)
The Layer-5 items live outside the store, so they can't be "applied" via Shopify — they become a **prioritised action plan** the member executes over time, plus **monitoring**. For each: state the current gap (from the category-citation queries), the specific action, and who/what does it. Hand off where other skills help: **blog-writer** for comparison/"best of"/answer content AI cites, **competitor-analysis** to see rivals' AI presence, **ugc-scripts** for the YouTube/creator angle. Re-run the category AI queries monthly to track **citation share**. Do not fake reviews, Reddit posts, or Wikipedia pages — inauthentic signals get discounted and risk the brand.

### Lane D — App-based fixes (when an app is the right tool)
Many high-value Shopify fixes are delivered by **apps**, not theme/content edits — and several schema signals you find on a rendered page come from apps (e.g. a review app injecting `aggregateRating`/`review`, an SEO app injecting Organization/Breadcrumb/FAQ schema). Recommend the app route when it's the safer/faster path than theme surgery — but choose deliberately.

**First, check what's already installed** (Shopify → installed apps) so you (a) attribute rendered schema/features to the right app, (b) don't recommend a duplicate, and (c) can just *configure what's there* instead of adding more. *(`appInstallations` may be access-denied depending on the connector's scopes — if so, infer the app from the rendered `@type`s or ask the member to open Settings → Apps.)*

| Need | App category | Well-known examples |
|---|---|---|
| Review + star schema (`aggregateRating`) | Reviews | Judge.me, Okendo, Loox, Yotpo |
| Auto JSON-LD (Organization, Breadcrumb, FAQ, Product), meta tags, redirects, alt text | SEO suite | Yoast SEO for Shopify, Avada/Booster SEO, SearchPie, Smart SEO |
| FAQ page + FAQPage schema | FAQ (often inside an SEO suite) | — |
| Image compression, lazy-load, defer JS (Core Web Vitals) | Speed | TinyIMG, Avada, Hyperspeed |
| Serving `/llms.txt`, AI/agent feeds | AI/GEO | emerging llms.txt apps |
| 404s / redirects | Redirects (often inside an SEO suite) | — |

**Rules when recommending an app:**
- **App bloat is the #1 Shopify speed killer** — every app adds scripts. Prefer apps that render **server-side** (theme / `content_for_header`) over client-side JS, consolidate overlapping apps, and **remove unused ones**. One good SEO suite usually beats five single-purpose apps.
- **Watch for duplicate/conflicting schema** — two apps both emitting Product or Organization schema = invalid/duplicate structured data. Enumerate the rendered `@type`s and de-dupe.
- **Verify on the rendered page** after install/config (same render rule as Layer 3) — confirm the app actually outputs what it promises, validly.
- Match the app to what the store already has and needs; prefer well-reviewed, actively-maintained apps and note pricing. Don't blind-recommend a single app.

## llms.txt on Shopify (the tricky one)
Shopify doesn't let you drop an arbitrary file at the site root. Options, best first:
1. **Template/route approach** — create a page/template that renders the markdown and serve it at a clean path (e.g. `/pages/llms` or a custom template), and/or
2. **App/proxy** that serves `/llms.txt`, or
3. If root `/llms.txt` truly isn't achievable, publish the curated list as a page and link it, and still provide the file to the member.
Content: a short markdown file — an H1 with the brand, a one-line description, then a curated list of the **key URLs** (top products, collections, About, best guides/FAQs) each with a one-line description. Keep it lean; it's a map to your best pages, not a dump of the whole site.

## Order of operations (typical high-impact first)
1. FAQPage schema + real FAQ content **[theme + content]**
2. Answer-first rewrites of key page/post intros **[content]**
3. Product schema gaps — brand, GTIN, ratings **[theme]**
4. llms.txt **[theme/workaround]**
5. Title/meta gaps + unique descriptions **[content]**
6. Organization/WebSite/Breadcrumb schema **[theme]**
7. Bing Webmaster verification + sitemap submit **[member action]**
8. robots.txt tidy + H1 fixes **[theme]**

## After applying
Re-fetch/re-render each changed page to confirm the fix is live and valid (schema validates, one H1, meta present). Log every change with date so the monthly re-run can show progress.
