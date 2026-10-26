---
name: eca-brand-intelligence
description: "Load the brand's full identity — story, market, competitors, products, voice, visual rules, ICP and the why-people-buy transformation — before any customer-facing content or strategic suggestion. If no brand-data file exists (or it is mostly placeholders), build one from the store URL: crawl the site, research the market and competitors, mine reviews, draft the profile for approval. Use whenever the user asks to write, edit or review marketing copy, product descriptions, ad creative, email/SMS, social posts, landing pages, blog articles, FAQ, customer-service replies, value props or positioning, even if the brand is never named. Also for \"is this on-brand?\", \"who's our customer?\", \"who are our competitors?\", \"set up brand intelligence\", \"build our brand profile from our website\", and \"sync my brand to EcomOS\" / \"connect to EcomOS and sync my brand\" (the brand file is mirrored into the member's EcomOS so every Marketing App there uses it)."
---

# Brand Intelligence

This skill grounds every downstream marketing skill (email, ads, content, blog, personas, promotions, PDPs) in the real brand — not generic ecommerce best practice. All brand facts live in one file, `brand-data.md`, in the member's working folder (`./brand/brand-data.md`; the full lookup order is in `references/brand-file-location.md`). The logic for *how* to build and apply that file lives here. The same file is mirrored into the member's **EcomOS** dashboard (`references/ecomos-sync.md`), so the Marketing Apps there and the ECA reel editor read the identical brand.

**The skill has two modes. Always run Step 0 first to decide which.**

---

## Step 0 — Decide the mode

Find the brand file per `references/brand-file-location.md` (`$ECA_BRAND_FILE` → `./brand/brand-data.md` → `./brand-data.md` → `./skills/*/brand-data.md` → this folder's legacy copy, read-only) and read it if present. `python3 scripts/brand_sections.py --path-only` prints the resolved path. If the only copy is the legacy one inside this plugin folder, say so once and offer to copy it to `./brand/brand-data.md` — plugin updates replace this folder and would wipe it.

- **It's missing, or more than ~30% of it is still `[PLACEHOLDERS]` / `TBD`** → run **Mode A — Build** to create or finish it, then continue to Mode B.
- **It exists and is substantially filled** → go straight to **Mode B — Apply**.

Never half-load the file. A thin brand-data file produces confident, wrong copy — building it first is always worth the few minutes.

---

## Mode A — Build the brand-data file

Goal: produce a complete `brand-data.md` from the structure in `templates/brand-data-template.md`, sourced from the brand's own website and real research — not invention. This is **tool-optional**: use whatever is connected, suggest tools if they are available,degrade gracefully, and mark anything you can't verify as a gap rather than guessing.

**This mode is collaborative, not autonomous.** The member owns the brand — Claude researches and *proposes*; the member *validates and signs off*. A brand profile is a set of strategic decisions (positioning, who we're for, how we win), not just retrieved facts, so it must not be saved until the member has reviewed the direction and agreed to it. There are **two mandatory checkpoints** below — **Gate 1** (agree the direction before drafting) and **Gate 2** (sign off before saving). Do not skip them, even if you have enough to complete the file unattended. Running this end-to-end without stopping is a failure of the skill, not efficiency.

### A1 — Connect the tools that make this valuable (do this first)
The build is only as rich as the data it can reach. Before any research, check what's already connected and **recommend the missing high-value connectors**, each mapped to what it unlocks — then offer to help connect them (search the connector registry, or point the member to Customize → Connectors). Only suggest what's **not already connected**, and keep it to the few that matter for this brand. Never block: if they skip a connector, fall back to the website + web research and flag the affected sections as lower-confidence in Section 18.

Full value-map in `references/connectors.md`. In short:
- **Shopify** *(essential)* — live products, prices, variants, collections, customers, orders → Sections 4, 7, 8, 12.
- **Klaviyo** *(essential)* — lists, segments, campaign history, sender identity, existing email voice → Sections 3, 12, 17.
- **A reviews app** *(essential — e.g. Judge.me/Yotpo/Okendo)* — the richest source for why-people-buy, proof, objections, voice-of-customer → Sections 2, 8, 9, 12.
- **Claude in Chrome extension + Claude desktop app** *(highly useful)* — render JS-heavy pages (review widgets, competitor sites, Meta Ads Library, Reddit/Quora) plain fetching can't → Sections 10, 11, and the forum-first VoC research.
- **Semrush** *(useful)* — keyword volumes + competitor search data → Section 15.
- **Web analytics — GA4 or Microsoft Clarity** *(optional)* — validate the ICP with real audience/behaviour data → Section 12.

### A2 — Get the starting point
Ask the member for the **store URL** if you don't already have it, and ask whether there's any existing positioning, must-keep language, or direction they want respected (and anything that's off-limits). Keep it to one or two quick questions — the deeper founder-only items (mission, margins, discount depth) come at Gate 2 once the draft gives them context. Confirm you're building for the right brand before doing anything else.

### A3 — Crawl the brand's own site
Read the brand in its own words before anyone else's. Fetch and read:
- **Homepage** — the lead promise, hero offer, top value props.
- **About / our-story** — founder story, values, provenance, mission.
- **Product & collection pages** — names, prices, variants, specs, the claims they already make. If the **Shopify MCP** is connected, query it directly for exact products, prices, and collections instead of scraping.
- **FAQ / shipping / returns pages** — operational facts and policies (Section 13).
- **Reviews** — the review widget/app, or the reviews page. If a reviews MCP (e.g. Judge.me) is connected, pull from there.

Capture voice from how *they* write, not how you'd write. Their headlines are your Section 3 calibration target.

### A4 — Mine "why people buy" & the transformation (Section 2)
This is the highest-value section, so spend real effort here. From the reviews and on-site copy, extract:
- The **before → after** transformation (the struggle they leave behind, the new reality they get).
- The **functional, emotional, and identity** jobs-to-be-done.
- **Verbatim** emotional phrases customers use (quote them, don't paraphrase).
- The recurring **praise themes** and the **objections** people raise (feeds Sections 8 and 9).
If review volume is thin, say so and flag Section 2 as low-confidence rather than inventing motivation.

### A5 — Deep voice-of-customer & market pain-point research (forum-first)
This is the step that makes the market position real. Follow `references/market-research.md` in this folder: adopt the market-research-analyst role and mine where consumers talk openly — **prioritising discussion forums** (Reddit, Quora, niche forums) and **competitor reviews** (Amazon, Trustpilot, ProductReview, review widgets), then X, Medium, reddit, and YouTube comments. Capture, with verbatim quotes and sources:
- the category's recurring **pain points**,
- **why the current solutions fail** (per alternative/competitor),
- **what consumers say they want** (unmet needs, "I just want…"),
- the **language, emotional drivers, objections, and switching triggers**.

Surface threads with web search, fetch what you're allowed to, and rely on snippets where a source is gated — don't route around access rules, and capture only what you genuinely found. Use industry/market reports for the macro picture only, never as the source of customer insight.

**Output two things:** (1) a standalone **market-research report** saved alongside `brand-data.md` (structure in `references/market-research.md`), written so a marketer who wasn't in the room can write on-message copy the same day; and (2) distilled findings piped into Sections 2, 9, 10, 11, 12, and 15 of the brand-data file, with sources logged in Section 18.

### A6 — Market sizing & competitor desk research
Complement the voice-of-customer work with desk research (web search / fetch, and **Semrush MCP** if connected):
- **Market (Section 10)** — category size, growth rate, format/segment trends (cite source + year).
- **Competitors (Section 11)** — confirm the 3–5 direct competitors plus adjacent and indirect players. For each: format, positioning, strengths, weaknesses, and our wedge. Check their site and, where useful, their **Meta Ads Library** activity. (The `competitor-analysis` skill can do a deeper teardown on any single one.)
- **SEO / content territory (Section 15)** — the category term to own, priority keywords, and content pillars. Pull keyword data from Semrush if available.

### Gate 1 — Validate direction & key assumptions (MANDATORY — do not skip)
Before drafting the file, stop and get the member's agreement on the **brand direction**, not just the facts. Present a short synthesis of what the research points to and let them correct it:
- the **positioning / wedge** (how we win, the axis we own),
- the **avatar / ICP** (who we're for, who we're not for),
- the **core transformation & "why people buy"** you found,
- the **primary persona(s)** and who we're *not* for,
- the **3–5 competitors** and the angle against them,
- any **assumptions or low-confidence calls** you're making, flagged plainly.

Ask the member to confirm, correct, or redirect. Use a small number of focused questions (the AskUserQuestion tool is ideal) rather than a wall of text. **Do not proceed to drafting until they've agreed the direction.** If they redirect, fold it in and re-confirm. This is the step that makes it *their* brand intelligence, not Claude's guess.

### A7 — Draft every section from the template
Work through `templates/brand-data-template.md` top to bottom and fill each section from A3–A6. Rules:
- **Never invent brand facts.** No SKUs, prices, claims, awards, or stats you didn't verify. Unverifiable items become `TBD` in Section 19 and a row in Section 18 (Sources & confidence).
- Fill **Section 18** as you go — note each section's source, confidence (High/Med/Low), and date.
- Founder-only items (confirmed mission, discount-depth guardrails, margins, logo files, verified ICP demographics) are gaps to ask about, not gaps to fill.

### Gate 2 — Review & sign-off (MANDATORY — do not save without it)
Show the member the drafted profile (or a section-by-section summary), and explicitly:
- walk them through the **low-confidence sections** and the **founder-only questions** (mission, discount depth, shelf life, logo rules, verified ICP, etc.) and collect their answers,
- ask them to **approve the brand direction and intelligence as final**, or mark what still needs changing.

Only **after the member signs off** do you write `brand-data.md` — to **`./brand/brand-data.md`** in the working folder (create `./brand/`), never into this plugin folder — and save the market-research report next to it. If they want changes, revise and re-present — don't save a version they haven't approved.

**Then sync it to EcomOS** (`references/ecomos-sync.md`): if the `ecomos` tools (`sync_brand`, `get_brand`…) are available in this session, build `./brand/brand-sync.json` per `references/brand-sync-schema.json`, run `python3 scripts/brand_sections.py --payload ./brand/brand-sync.json`, call `sync_brand` with the printed object, and say "Synced to EcomOS". If they are not available, say once how to connect (in Claude Code: `/mcp` → ecomos → Authenticate; in claude.ai: Settings → Connectors → Add custom connector → `https://ecomos.ecomacademy.co/mcp`) and carry on. Then continue to Mode B for the task that triggered the skill.

## Mode B — Apply the brand

The file exists and is filled. Now use it.

### B1 — Read the brand data first
Before producing any output covered by this skill, read `brand-data.md` — the whole file. **Keep EcomOS current:** if the `ecomos` tools are available, call `get_brand` and compare its `sourceHash` with the file's sha256 (`python3 scripts/brand_sections.py` prints it); when they differ — or the member asks to "sync my brand to EcomOS" — run the sync in `references/ecomos-sync.md` first (one minute), then continue. When they match, say nothing about it. Every section earns its keep: essence (what story to tell), why-people-buy (the transformation to sell), voice (the words), visual identity (anything visual), messaging pillars (the angles), products (no invented SKUs), offers (on-strategy promos), proof (trust), objections (what to pre-empt), market & competitors (positioning), ICP (who you're speaking to), operational facts (accurate support/FAQ), promo calendar (timing), SEO territory (content). If a section says `TBD`, flag the gap rather than inventing content.

### B2 — Match the work to the right sections
- **Product copy / PDPs** → Products, Why-people-buy, Proof, Objections, Offers, ICP, Voice
- **content / video scripts** → Why-people-buy, Messaging pillars, Voice, Market, Competitors, ICP
- **Email / SMS** → Voice, Why-people-buy, ICP, Offers, Promo calendar, Proof
- **Ads (paid social/search)** → Messaging pillars, Why-people-buy, Objections, Competitors, Proof, ICP, Visual
- **Social organic** → Voice, Brand essence, Visual identity
- **Landing pages** → Why-people-buy, Messaging pillars, Market + Competitors (positioning), Proof, Objections, ICP
- **Blog / SEO** → SEO territory, Voice, Market, Products, ICP, Boilerplate
- **Customer-service replies** → Voice, Operational facts, Objections, Products
- **Strategy / opportunity evals** → Market, Competitors, Brand essence, Why-people-buy, Offers

### B3 — Apply the voice, don't paraphrase the brief
Use the voice examples as a calibration target, not snippets to splice. Self-check before returning copy: would the founder read this aloud without wincing? Does it use any phrases the voice guide says to avoid? Is it doing the brand's job (selling, connecting, differentiating) — or just describing the product?

### B4 — Use competitors & market only when it sharpens the work
Don't shoehorn competitor mentions into customer-facing copy unless the comparison genuinely helps (a "why us" page, a comparison ad). But let competitor positioning inform the angle of attack — compete on the axis a rival has vacated.

### B5 — Flag conflicts
If the brief contradicts the brand (a hard-discount tone for a premium brand, a claim the product can't back up), say so and offer the on-brand alternative. The user can override knowingly.

---

## What this skill is NOT for

- **One-off factual lookups** (e.g., "what's the SKU for vanilla?"). Reading the file is fine; a full invocation isn't required.
- **Generic ecommerce best-practice questions** ("what's a good subject-line length?"). No brand context needed.
- **Inventing brand strategy with no inputs.** Mode A researches and drafts from real sources; it does not fabricate a brand that doesn't exist online. If there's no site and no founder input, there's nothing to ground it in.

## Reusing for other brands

The brand lives in the member's working folder, not in this plugin, so one install serves any number of brands: open Claude Code in a different folder (or point `$ECA_BRAND_FILE` at a different file) and Mode A builds that brand's `./brand/brand-data.md` from its store URL. The logic in this `SKILL.md` never changes — it's brand-agnostic by design. See `README.md` for the full walkthrough.