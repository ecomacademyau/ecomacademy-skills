---
name: eca-persona-builder
description: Turn customer reviews (and other voice-of-customer data) into 3-5 detailed marketing personas — built from real benefits, pain points, emotional triggers, and buying behaviour, ready to aim ads and copy at. Use this skill whenever the user wants customer personas, buyer personas, marketing personas, audience segments, an ICP breakdown, "who is our customer", "analyse our reviews", "what do customers actually say", a voice-of-customer analysis, review mining, or wants to group customers into segments for targeting. Also trigger for "build me personas from these reviews", "what are our customer types", "pull the emotional triggers from our reviews", or "summarise the objections customers raise". The skill analyses review data across benefits, pain points, emotions, motivations, demographics, behaviour, objections, and content preferences, then outputs named personas. It works for any brand by swapping config.md and feeding in that brand's reviews.
---

# Persona Builder (Voice-of-Customer → Personas)

This skill mines a brand's **customer reviews** (and any other voice-of-customer data) and turns them into **3–5 named marketing personas** — each grounded in real benefits, pain points, emotional triggers, buying behaviour and objections, written so a marketer can immediately aim ads, copy and offers at them.

The goal is **detailed, emotionally-resonant personas** that downstream skills (especially `eca-ad-copywriting` and `eca-email-marketing-campaign`) can use to create highly targeted, on-the-mark creative.

The skill is **brand-agnostic in logic, brand-specific in config**. The workflow works for any brand; the only things that change are `config.md` (where the data lives, how many personas, output prefs) and the review data you feed in. To use for a different brand, fork the folder and edit `config.md` — see `README.md`.

## Before you start

1. **Read `config.md`** for this brand's settings — where the reviews live, how many personas to produce, and output preferences.
2. **Load brand context** if available (the `eca-brand-intelligence` skill) so persona language matches the brand and you know the product lineup. Not required, but it sharpens the output.
3. **Get the data.** You need real customer voice to do this honestly. Acceptable sources:
   - a reviews export (.txt / .csv) — Judge.me, Okendo, Yotpo, Shopify reviews, etc.
   - support tickets, survey responses, social comments, testimonials
   - if none exist yet, ask the user to paste a batch, or point you to where reviews live.

   **Do not invent reviews or personas.** If there's no data, say so — a made-up persona set is worse than none. With thin data, produce fewer personas and flag the low confidence.

## The analysis framework

The full nine-part analysis you run over the review corpus lives in `references/analysis-framework.md`. **Read it before analysing.** In short, you extract: customer benefits, pain points & challenges, emotional drivers, purchase motivations, demographic insights, behavioural insights, then synthesise customer segments (the personas), content preferences, and objections & concerns.

## Output templates

- A single persona is structured per `templates/persona-template.md`.
- The full deliverable (analysis summary + all personas + strategy takeaways) is structured per `templates/persona-report-template.md`.

Read both before writing the output so the deliverable is consistent and complete.

## Workflow

### Step 1 — Confirm scope (don't assume)

In one quick pass, confirm with the user:
- **The data source** — which reviews/feedback file or paste to analyse.
- **How many personas** — default 3–5 (per `config.md`); fewer if data is thin.
- **The purpose** — usually "to target ads and copy"; if they have a narrower goal (e.g. one product line, one market), scope to it.

If they've already given everything, restate it in one line and proceed.

### Step 2 — Ingest and read the data

Read the review corpus. If it's large, sample broadly across ratings (don't only read 5-star — the 1–3 star reviews carry the objections you need). Note recurring phrases verbatim; customer language is the gold here.

### Step 3 — Run the nine-part analysis

Work through `references/analysis-framework.md` over the whole corpus:
1. Customer benefits
2. Pain points & challenges
3. Emotional drivers
4. Purchase motivations
5. Demographic insights
6. Behavioural insights
7. Customer segments (→ the personas)
8. Content preferences
9. Objections & concerns

Capture the cross-cutting findings (1–6, 8, 9) — they become the analysis summary and feed every persona.

### Step 4 — Synthesise the personas

Group customers into **3–5 distinct personas** based on shared behaviours, motivations and needs. For each, fill `templates/persona-template.md`:
- **Name & description** — a memorable nickname + one-line who-they-are (e.g. "Busy Professional looking for focus", "Mindful wellness seeker").
- **Key benefits valued**
- **Primary pain points**
- **Emotional triggers**
- **Buying behaviour**
- **Preferred messaging tone/style**
- **Notable review quote(s)** — a real line that captures the persona (use the customer's actual words).

Make the personas genuinely distinct — if two overlap heavily, merge them. Anchor every persona in evidence from the reviews, not imagination.

### Step 5 — Write the report

Assemble the deliverable using `templates/persona-report-template.md`: the analysis summary (benefits, pains, emotions, motivations, demographics, behaviour, content prefs, objections), then the personas, then **key takeaways for marketing strategy** (the so-what: which angles, language and offers to lead with). Save it to the location in `config.md` (default: the project folder), named like `personas-[brand]-[YYYY-MM-DD].md`.

End with a short note on **how to use these downstream** — e.g. feed them into `eca-ad-copywriting` to write segment-specific headlines, or into `eca-email-marketing-campaign` to tune tone per segment.

## House rules that keep personas honest

- **Evidence over imagination.** Every claim ties back to something customers actually said. Mark anything inferred as a read, not a fact.
- **Mine the negative reviews** for objections — they're the most actionable part and the easiest to skip.
- **Use customer language verbatim** in triggers and quotes; it's what makes the personas usable for copy.
- **Distinct, not redundant.** 3–5 personas that genuinely differ beat 5 near-duplicates.
- **Low data = low confidence, stated.** Don't manufacture certainty the data doesn't support.

## What this skill is NOT for

- **Writing the ads themselves** — that's `eca-ad-copywriting` (feed these personas in).
- **A full brand brief** — that's `eca-brand-intelligence`; personas are one section of it. This skill goes deep on the customer specifically.
- **Inventing an audience with no data** — get reviews first.

## Reusing for other brands

Fork the folder, edit `config.md` (data source, persona count, output path), feed in that brand's reviews — `SKILL.md`, `references/` and `templates/` are brand-agnostic. See `README.md`.
