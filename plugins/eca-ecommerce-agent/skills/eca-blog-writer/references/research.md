# Research Method — Free First, Paid If Available

The point of research is to write about what people **actually search and ask**, not what we assume, and to find the angle that beats what's already ranking. Run the tiers in order. Most posts only need Tier 1.

This skill must work for a member with **zero paid tools**. Treat Tier 1 as the universal baseline and Tier 2 as an optional accelerator. Never block on a paid connector — if it isn't there, say so and ship from Tier 1.

---

## Tier 1 — Free methods (no connector needed). Always do these.

### 1. Read the current top results
Web-search the seed topic. Open the top 3–5 ranking posts and note:
- their **angle** and who they're written for,
- their **H2 structure** (this reveals the sub-questions Google rewards for this topic),
- their **gaps** — what's missing, outdated, thin, or generic. That gap is your opening.

The goal isn't to copy — it's to write the post that deserves to outrank them.

### 2. Harvest the real questions (this is the GEO goldmine)
- Search the seed term and read the **"People Also Ask"** box; expand a few — each expansion spawns more. Collect them.
- Type the seed term into search and read the **autocomplete** suggestions; repeat with "how/what/why/best/vs + term" and "term + for/without/vs".
- These long-tail questions are exactly what people type into Google **and** ask ChatGPT/Perplexity. They become your H2s and FAQ block.

### 3. Mine voice-of-customer language
- **Reddit, Quora, forums, Facebook groups** in the niche — search the topic and read how real people phrase the problem and what they argue about.
- The **brand's own reviews, FAQs, and support tickets** — the highest-intent language you have. (If the `eca-persona-builder` output exists, use it.)
- Capture exact phrases; reuse them in headings and copy. Matching the searcher's words is half of ranking.

### 4. Check what the AI engines currently say
- Ask the target question the way a customer would and see what a generative engine answers and which sources it cites. Your job is to be a **better, more citable source** than those — more specific, better structured, more current, with data.

### 5. Scan competitor blogs
- From the brand-intelligence competitor list, look at 2–3 competitor blogs. What topics do they cover repeatedly (a sign it's working)? What angle can you beat? What have they not covered at all?

### 6. Validate search volume before writing (free)
Don't write a post until you know people actually search the topic. **Google Keyword Planner** (tools.google.com/keyword-planner) is free with a Google Ads account and is the go-to check:

- Enter the primary keyword (and, for influencer posts, the influencer's name plus "[name] products" and "[name] tips").
- Check **average monthly searches**.
- **Threshold: aim for roughly 1,000+ searches/month** combined across the primary terms before committing (tune per `config.md`; niche brands may set this lower). Note the secondary keywords it surfaces.
- No Keyword Planner access? Use the free signals above (autocomplete depth, number of People Also Ask, Reddit/forum activity) as a directional proxy, and say the volume is estimated.

This volume check is part of Gate 1: confirm demand before the title is approved, not after the post is written.

---

## Tier 2 — Paid SEO tools. Only if connected. Optional.

Use these to **prioritise and validate** the Tier-1 list with hard numbers — not to replace it.

### Semrush (if the Semrush MCP is connected)
- `keyword_research` — volume, keyword difficulty, and intent for the seed + the long-tails you collected. Promote low-difficulty / decent-volume / commercial-intent terms.
- `trends_research` — what's rising in the category right now (good for timely posts).
- `organic_research` — pull a competitor domain's ranking keywords to find topics they win that we don't.
- Set the database to the market in `config.md` (e.g. `au`).
- Workflow: discovery tool → `get_report_schema` → `execute_report`.

### Ahrefs (if connected)
- Equivalent keyword/volume/difficulty validation, plus its AI-search/brand-radar reports show where the brand is (or isn't) being cited by AI engines — useful for GEO gap-finding.

### Google Search Console (if the user can supply data)
- There isn't a standard GSC MCP connector at time of writing, so this is **opt-in**: if the user can export or paste their GSC "queries" report, it's the best source of all — it shows queries the store **already** ranks for.
- Look for **"striking distance" queries** (average position ~5–20, with impressions): writing or improving one post can push these onto page one. Prioritise these — they're the fastest wins.
- If they don't have it, skip silently; Tier 1 covers it.

---

## What to hand to the writing phase

Produce a compact research brief per topic:

- **Primary keyword** (+ a couple of close variants).
- **Search intent** — informational / commercial / transactional → drives style choice.
- **Difficulty/volume** — with a note on whether it's a hard number (paid tool) or a directional read (free methods).
- **Supporting questions** — the PAA/long-tail list that becomes H2s and the FAQ block.
- **Voice-of-customer phrases** — to reuse in copy.
- **The gap** — why our post will beat what's ranking, and why an AI engine would cite it.
- **Recommended style** (from `blog-styles.md`) and the **products** it should drive to.

Always note the data source/tier in the final output so the user knows how to weight the numbers.
