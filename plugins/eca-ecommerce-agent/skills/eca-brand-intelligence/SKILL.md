---
name: eca-brand-intelligence
description: "Load the brand's full identity (story, market, competitors, products, voice, visuals, ICP, why people buy) before any customer-facing content or strategic suggestion, and keep it saved in the member's EcomOS so every AI app and Marketing App works from the same brand. If no brand profile exists (or it is mostly placeholders), build one from the store URL: crawl the site, research the market and competitors, mine reviews, draft the profile for approval, then save it to EcomOS. Use whenever the user asks to write, edit or review marketing copy, product descriptions, ad creative, email/SMS, social posts, landing pages, blog articles, FAQ, customer-service replies or positioning, even if the brand is never named. Also for \"is this on-brand?\", \"who's our customer?\", \"who are our competitors?\", \"set up brand intelligence\", \"build our brand profile from our website\", \"save my brand to EcomOS\" / \"sync my brand to EcomOS\", and \"help me fill my Business Brain\" / \"what's my Brain score?\"."
---

# Brand Intelligence

This skill grounds every downstream marketing skill (email, ads, content, blog, personas, promotions, PDPs) in the real brand — not generic ecommerce best practice. It researches and builds the brand profile (19 sections, structure in `templates/brand-data-template.md`), and applies it to the work.

**The brand lives in the member's EcomOS (their Business Brain), and EcomOS is always the source of truth** — not an AI app's memory, not a folder. The skill saves every section there over the `ecomos` MCP tools, so Claude, any other AI app the member connects and the Marketing Apps inside EcomOS all read the same brand, and the member can see and edit it on the Business Brain page. `references/ecomos-sync.md` is the how-to for saving and reading; read it before the first EcomOS call in a session. `./brand/brand-data.md` in the member's working folder is a **copy** (other ECA skills and scripts still read it): when it disagrees with EcomOS, EcomOS stands, and a change to the brand is saved to EcomOS first. It is the only copy when EcomOS is not connected (`references/brand-file-location.md`).

**The skill has three modes: Build (A), Apply (B) and Deepen (C). Always run Step 0 first to decide which.**

---

## Step 0 — Find the brand and decide the mode

**1. Look in EcomOS.** If the `ecomos` tools are in this session, call `ping` (it names the business this connection reads and writes) and `list_context`. The brand is saved there when the list includes `why-people-buy`. A list without it is empty, or holds only the short summaries EcomOS made from an older sync: the brand is not saved yet. Saved but with sections missing means the last save was interrupted: finish it, do not rebuild (`references/ecomos-sync.md` → "What `list_context` tells you").

**2. Look for a working copy.** Find the brand file per `references/brand-file-location.md` (`$ECA_BRAND_FILE` → `./brand/brand-data.md` → `./brand-data.md` → `./skills/*/brand-data.md` → this folder's legacy copy, read-only). `python3 scripts/brand_sections.py --path-only` prints the resolved path. If the only copy is the legacy one inside this plugin folder, say so once and offer to copy it to `./brand/brand-data.md` — plugin updates replace this folder and would wipe it. In a chat with no folder there is no working copy, and that is fine.

**3. Decide.**

| EcomOS | Working copy | Do |
|---|---|---|
| saved | any | **Mode B — Apply**, reading from EcomOS. First do what `list_context` asks (sections marked `auto brief`, sections changed since the structured brand was synced) and, if a working copy exists, refresh it from EcomOS (`references/ecomos-sync.md` → "Keeping the copies in step"). |
| not saved yet | filled | Check the business `ping` named is the brand in the file; if it is not, stop and ask. Then **save it to EcomOS** now (`references/ecomos-sync.md` → "Saving the whole brand"; the completeness check there decides between saving and a refresh), then Mode B. Tell the member in one line that their brand is being saved to EcomOS and the file stays where it is. |
| not saved yet | missing, or more than ~30% still `[PLACEHOLDERS]` / `TBD` | **Mode A — Build**, then Mode B. First call `get_brand`: a `sourcePath` in the reply means a brand file exists on another computer or folder — tell the member and ask whether to work from there instead of rebuilding. |
| not connected | filled | **Mode B** from the file. Say once how to connect (`references/ecomos-sync.md` → "Is EcomOS connected?"). |
| not connected | missing or mostly placeholders | Ask once whether a brand profile was built before: it may be in EcomOS (connect first) or in another folder. If not, **Mode A**, saving to the working folder, then Mode B. Say once how to connect. |

**"Help me fill my Business Brain", "what's my Brain score?", "improve my Brain score"** → **Mode C — Deepen**, whatever the table says (it needs EcomOS connected).

A brand that exists but is thin or stale — the completeness check says REBUILD, several sections are still TBD, or it was last updated more than ~4 months ago — gets **Mode A as a refresh**: keep every section the member has approved, re-research only the gaps and whatever is stale, then Gate 1 and Gate 2 as usual. When the brand is in EcomOS, its age is the "Last updated" line in `brand-overview` and the dates `list_context` prints, and the sections you are refreshing are read with `get_context` (`depth:"full"`) first. A thin profile patched at save time is not brand intelligence.

Never work from a thin brand. It produces confident, wrong copy — building it first is always worth the few minutes.

---

## Mode A — Build the brand profile

Goal: produce a complete brand profile — every section of `templates/brand-data-template.md` — sourced from the brand's own website and real research, not invention, and save it to EcomOS. This is **tool-optional**: use whatever is connected, suggest tools if they are available,degrade gracefully, and mark anything you can't verify as a gap rather than guessing.

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
Ask the member for the **store URL** if you don't already have it, and ask whether there's any existing positioning, must-keep language, or direction they want respected (and anything that's off-limits). Keep it to one or two quick questions — the deeper founder-only items (mission, margins, discount depth) come at Gate 2 once the draft gives them context. Confirm you're building for the right brand before doing anything else. If EcomOS is connected, `ping` names the business the brand will be saved to — check it is this one — and `get_brand` returns any structured brand from an earlier sync: a head start to verify, not a finished profile.

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

**Output two things:** (1) a standalone **market-research report** (structure in `references/market-research.md`), written so a marketer who wasn't in the room can write on-message copy the same day — it is saved to EcomOS as the `market-research` section, and beside the working copy as `market-research-report.md` when there is a folder; and (2) distilled findings piped into Sections 2, 9, 10, 11, 12, and 15 of the brand profile, with sources logged in Section 18.

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

Only **after the member signs off** is anything saved. If they want changes, revise and re-present — never save a version they haven't approved.

### A8 — Save the approved brand to EcomOS
Follow `references/ecomos-sync.md` → "Saving the whole brand". In short:
1. **When there is a working folder**, write the profile to **`./brand/brand-data.md`** (create `./brand/`; never into this plugin folder) and the research report next to it as `market-research-report.md`.
2. **Check it is complete**: build the structured brand (`brand-sync.json`) and run the completeness check; fill what it lists from the live store, ask the member for the rest, and write the answers into the profile. A save that leaves colours or proof as TBD is a half-done job.
3. **Save every section** with `put_context` — one call per section, the full text word for word, plus a one-line `summary` and a `brief` you write for the skills that will read it — then the research report.
4. **Send the structured brand** with `sync_brand` so the Marketing Apps in EcomOS use it.
5. **Log** the build with `log_context`, and each direction the member corrected at the gates as a `general` learning.
6. Say "Saved to EcomOS" in two lines, with what is still to confirm.

If the `ecomos` tools are not in this session, the working copy is the brand for now: say once how to connect (`references/ecomos-sync.md` → "Is EcomOS connected?") and that "Save my brand to EcomOS" will save it there later. In a chat with neither EcomOS nor a folder, give the member the finished profile as a file to keep and tell them plainly it is not stored anywhere else yet.

Then continue to Mode B for the task that triggered the skill.

## Mode B — Apply the brand

The brand exists and is filled. Now use it.

### B1 — Load the brand for this task
**From EcomOS (whenever it is connected).** Call `get_context` with `for:` set to the skill doing the work (`ad-copywriting`, `email-marketing-campaign`, `blog-writer`, `landing-pages`, `product-page`, `cs-email`… — `list_context` prints the names). It returns the brand card, that skill's sections as briefs, and what was learned last time, inside a token budget. It also brings `brand-overview`, the member's approved strategic direction, which outranks the research in every other section. Then pull the whole text of the two or three sections the task leans on hardest (`keys:[…]`, `depth:"full"`; B2 says which; a reply that ends "NOT the whole text" means a section did not fit — raise `maxTokens`), and use `search_context` for a single fact. Do not load every section: it spends the member's tokens and buries what matters. When no skill name fits the task, pass the keys from B2.

**From the working copy (EcomOS not connected).** Read `brand-data.md` — the whole file. It may be behind what the member has in EcomOS; say so once if they have connected before.

Either way, every section earns its keep: essence (what story to tell), why-people-buy (the transformation to sell), voice (the words), visual identity (anything visual), messaging pillars (the angles), products (no invented SKUs), offers (on-strategy promos), proof (trust), objections (what to pre-empt), market & competitors (positioning), ICP (who you're speaking to), operational facts (accurate support/FAQ), promo calendar (timing), SEO territory (content). If a section says `TBD`, flag the gap rather than inventing content.

**Keep the brand current.** When the member corrects a brand fact during the work (a word they never use, a new price, a changed guarantee), update that one section in EcomOS straight away, bring the structured brand into line with it, and log the correction as a learning (`references/ecomos-sync.md` → "Keeping the copies in step"). When they say "save my brand to EcomOS" or "sync my brand to EcomOS", run "Saving the whole brand".

### B2 — Match the work to the right sections
Section keys for `get_context` are in brackets.
- **Product copy / PDPs** → Products, Why-people-buy, Proof, Objections, Offers, ICP, Voice (`products`, `why-people-buy`, `proof`, `objections`, `offer`, `personas`, `voice`)
- **Content / video scripts** → Why-people-buy, Messaging pillars, Voice, Market, Competitors, ICP (`why-people-buy`, `messaging`, `voice`, `market`, `competitors`, `personas`)
- **Email / SMS** → Voice, Why-people-buy, ICP, Offers, Promo calendar, Proof (`voice`, `why-people-buy`, `personas`, `offer`, `promo-calendar`, `proof`)
- **Ads (paid social/search)** → Messaging pillars, Why-people-buy, Objections, Competitors, Proof, ICP, Visual (`messaging`, `why-people-buy`, `objections`, `competitors`, `proof`, `personas`, `visual`)
- **Social organic** → Voice, Brand essence, Visual identity (`voice`, `brand-essence`, `visual`)
- **Landing pages** → Why-people-buy, Messaging pillars, Market + Competitors (positioning), Proof, Objections, ICP (`why-people-buy`, `messaging`, `market`, `competitors`, `proof`, `objections`, `personas`)
- **Blog / SEO** → SEO territory, Voice, Market, Products, ICP, Boilerplate (`seo`, `voice`, `market`, `products`, `personas`, `boilerplate`)
- **Customer-service replies** → Voice, Operational facts, Objections, Products (`voice`, `operations`, `objections`, `products`)
- **Strategy / opportunity evals** → Market, Competitors, Brand essence, Why-people-buy, Offers (`market`, `competitors`, `brand-essence`, `why-people-buy`, `offer`), plus `market-research` when the question is about the customer or the category

### B3 — Apply the voice, don't paraphrase the brief
Use the voice examples as a calibration target, not snippets to splice. Self-check before returning copy: would the founder read this aloud without wincing? Does it use any phrases the voice guide says to avoid? Is it doing the brand's job (selling, connecting, differentiating) — or just describing the product?

### B4 — Use competitors & market only when it sharpens the work
Don't shoehorn competitor mentions into customer-facing copy unless the comparison genuinely helps (a "why us" page, a comparison ad). But let competitor positioning inform the angle of attack — compete on the axis a rival has vacated.

### B5 — Flag conflicts
If the brief contradicts the brand (a hard-discount tone for a premium brand, a claim the product can't back up), say so and offer the on-brand alternative. The user can override knowingly. When the override is a standing preference rather than a one-off, record it in EcomOS with `log_context` (`kind:"learning"`; `skill` is the skill doing the work when it only concerns that kind of work, `"general"` when it is about the brand as a whole) so it is not argued again next time.

## Mode C — Deepen the Brain (a conversation, one question at a time)

EcomOS scores how much it knows about the business: **Brain depth**, out of 100, with five levels. The member sees the score, the level and the open questions on the Business Brain page, and can answer them there. This mode does the same job as a conversation, and the conversation is the point: the page is the form, you are the person who helps them think.

**Two rules shape everything below:**

1. **One question per message.** Never send a list of questions, not even a short one. A list is a form, and members stop answering forms. Ask one thing, deal with the answer, then ask the next.
2. **Every question comes with suggested answers.** You do the thinking first, from what the Brain, the store and the research already show, and the member picks one, changes one or says it their own way. A blank question makes them do your job.

It needs the `brain_depth` tool. If it is not in this session, EcomOS is not connected: say how to connect (`references/ecomos-sync.md` → "Is EcomOS connected?") and stop.

**C1 — Read the score and set it up.** Call `brain_depth`. It returns the score, the level, the points to the next level, and every open question with its id, the section it belongs to and its points. Tell the member in two or three lines: where they are, what the next level takes, and how this works ("I'll ask one thing at a time and suggest answers. Say *skip* to pass on one and *stop* whenever you've had enough; everything you answer is saved as we go."). Then go straight into the first question in the same message. Do not show them the list of open questions.

**C2 — If the brand profile has not been built** (`setup-profile` is open), say that the brand build answers most of these through research and offer it (Mode A). If they would rather just answer questions, carry on.

**C3 — Prepare the question before you ask it.** Take the most valuable open question, and stay on one topic until it is done so the conversation flows (finish the customer questions before jumping to operations). Then, before you ask, gather what could answer it:

- what the Brain already holds: the question's own section and its neighbours (`get_context`, `depth:"full"`, once per section; reuse it for later questions), `search_context` for a single fact, the market research report;
- what the live business shows: the catalogue and what sells (`get_products` with `detail:"full"` returns descriptions, variants, types and stock, plus `sales`: best sellers, what first-time customers buy first, free gifts and how often orders use a discount, counted from the store's recent Shopify orders), the review rating, count and wording, policies and FAQ on the site, colours and logo from the storefront.

**When `brain_depth` already carries the store's answer.** A question followed by a line starting `↳ Shopify already shows the answer` has been answered by the member's own store (their products and prices, the product new customers buy first). Ask those first: they are the quickest wins. Show what the store says and ask them to confirm or correct it; do not ask from scratch. A line starting `↳ What Shopify shows` is evidence, not the answer (how often orders use a discount does not tell you their discount *rule*): bring it into the question ("74% of your orders used a discount, about 11% off on average. Is that the plan, and is there a line you never cross?"). Either way the member still confirms before anything is saved.

From that, draft **two to four suggested answers**. What a suggestion may be depends on the kind of question:

- **A fact** (a price, a policy, a number, a name, a date): suggest only what a source shows, and name the source ("Your returns page says 30 days"). One sourced suggestion to confirm is enough. If nothing shows it, say you could not find it and ask openly. **Never guess a fact.**
- **A judgment** (voice, positioning, who the customer is, why they buy, objections, what makes them different): write real options, built from what the Brain and the reviews already say. Each one specific to this business, each one different from the others, in the member's own kind of language. No generic filler that would fit any store. Say which you would pick and why, in a few words.

**C4 — Ask it.** One message, one question:

- one short line on why it matters, when that is not obvious (what gets better once the Brain knows this);
- the question, in plain words (the wording `brain_depth` gives is a starting point: make it sound like a person asking);
- the suggestions, numbered;
- a close that makes answering easy: pick a number, change one, or say it in your own words.

If the app has a way to offer choices the member can click, use it, and always leave room for their own words.

> **Example.** *This one sharpens every ad and product page I write for you.*
> **What is the main thing holding people back from buying the first time?** From your reviews and FAQ, my guesses are:
> 1. "Will it taste as good as what I buy at the cafe?" (comes up in 14 reviews)
> 2. The price next to the supermarket version
> 3. Not sure how long a bottle lasts
>
> I'd put 1 first. Pick one, reorder them, or tell me what you actually hear from customers.

**C5 — Listen like a person, not a form.**

- **They picked or edited a suggestion:** that is their answer. Do not ask them to confirm it again.
- **The answer is thin or vague** ("quality", "everyone"): ask one follow-up that makes it usable ("Which customers say that most: the gift buyers or the ones buying for themselves?"). One follow-up, then take what you have.
- **They answered more than you asked:** take it all. If it covers other open questions, do not ask those again; say what you captured.
- **It contradicts what the Brain holds:** say so and ask which is right. What they confirm now stands.
- **"Skip", "not sure", "later":** move on without pushing. Do not tick it.
- **"None" or "doesn't apply":** that is an answer. Save it as such.
- **They ask what you think, or want to talk it through:** do that. Helping them reach an answer is the job; the tick comes after.

Never save a suggestion the member did not choose or confirm, and never tick a question the member did not answer.

**C6 — Save it straight away, show the gain, ask the next one.** Do not collect answers for later: an answer that is not saved is lost if they close the app.

1. **Write the answer into its section, properly.** Not a question-and-answer dump: put the fact where it belongs in the section's structure, replace any `TBD` it resolves (and tick it off in §19), keep the member's own words as quotes where the wording matters (voice, customer language), then `put_context` with `ifVersion`, a fresh `summary` and a fresh `brief`. A section that does not exist yet is created with its `## N. Title` heading from the key table in `references/ecomos-sync.md`.
2. **Tick it:** `brain_depth` with `answered: [that id]` (plus any others their answer covered). It returns the new score.
3. **Reply with one line of progress, then the next question in the same message** ("Saved to Objections. +5, you're at 66, four points from level 4."). Do not ask "shall I keep going?" after every answer; they will say stop.

Pause and check in only at a natural break: a level reached (make something of it), a topic finished, or about every five questions. Say in a line what is now covered and what is next, and let them carry on or stop.

Answers the member typed on the Business Brain page sit at the end of a section under a heading that starts **`### In the owner's words:`**. Whenever you meet one — here or at the start of Mode B — fold it into the section the same way and remove the heading, so skills read one coherent section. EcomOS marks those sections `auto brief`.

**C7 — Wrap up** when they stop or the questions run out:

1. Bring the structured brand into line and call `sync_brand` (`references/ecomos-sync.md` → "Keeping the copies in step"). Most checks are measured on the structured brand, so this is what makes the answers count everywhere. In a long sitting, do this at each check-in as well.
2. Call `brain_depth` once more and report where they started, where they are now, any level reached, and in one line what the next sitting would cover.
3. If there is a working copy, refresh it from EcomOS (`--plan`, then pull).

At the end of a Mode A or Mode B task you may mention the score once, in one line ("Your Business Brain is at 46 out of 100; five minutes on the open questions would take it to the next level"), when `list_context` shows it below 65. Never interrupt a task for it, and never bring it up twice in a session.

---

## What this skill is NOT for

- **One-off factual lookups** (e.g., "what's the SKU for vanilla?"). `search_context` or a look at the file is fine; a full invocation isn't required.
- **Generic ecommerce best-practice questions** ("what's a good subject-line length?"). No brand context needed.
- **Inventing brand strategy with no inputs.** Mode A researches and drafts from real sources; it does not fabricate a brand that doesn't exist online. If there's no site and no founder input, there's nothing to ground it in.

## Reusing for other brands

The brand belongs to the member's EcomOS business, not to this plugin, so one install serves any number of brands: the EcomOS connection decides which business is read and written (`ping` names it). A member with more than one store connects the one they are working on. Without EcomOS, open Claude Code in that brand's folder (or point `$ECA_BRAND_FILE` at its file) and Mode A builds `./brand/brand-data.md` there. The logic in this `SKILL.md` never changes — it's brand-agnostic by design. See `README.md` for the full walkthrough.
