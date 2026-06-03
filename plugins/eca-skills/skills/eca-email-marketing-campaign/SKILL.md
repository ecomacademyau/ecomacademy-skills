---
name: eca-email-marketing-campaign
description: Plan and draft email marketing campaigns using the "Famous For" method — one campaign, one topic, a sequence of emails that all sell. Use this skill whenever the user asks for help with email campaigns, Klaviyo campaigns, email sequences, newsletter ideas, promo emails, product launch emails, holiday/calendar emails, subject lines, email copy, email plans, or a "what should we send this week/month" question. Also use it when the user wants to brainstorm campaign themes, audit recent sends, or build out a multi-email arc. The skill covers topic selection (with Klaviyo history checks to avoid duplicates and back-to-back promos), the 4-email themed series and 7-email promo series, three template styles, subject lines, copy, and image direction. Each email is planned to stand on its own so recipients who only see one still get the full pitch.
---

# Email Marketing Campaign

This skill helps plan and draft email marketing campaigns using the **"Famous For" method**: every campaign is famous for *one* topic, and every email in the campaign earns its place by selling.

## Core principles (read before every campaign)

These four rules govern every campaign. If a draft violates one, fix it before sending it back.

1. **Famous for one topic.** A campaign has a single, sharp theme. If you can't say what the campaign is famous for in five words, the topic isn't tight enough.
2. **Don't repeat recent campaigns.** Before suggesting a topic, check what's been sent in the last 6–8 weeks. If the topic has been covered, either skip it or find a genuinely fresh angle.
3. **Don't run back-to-back promotions.** Promo campaigns burn audience goodwill if stacked. Space them out — at least 2–3 themed campaigns between promos unless the customer has explicitly asked otherwise (e.g., end-of-financial-year stack).
4. **Every email sells.** Even the "Give" emails in a themed series have a product link and a reason to click. The framework calls them Give-Give-Give-Ask, but in practice every email is Give-and-Ask. The Asks just get progressively stronger.

## When to invoke the brand-intelligence skill

The brand-intelligence skill (in `../eca-brand-intelligence/`) holds the brand's voice, products, ICP, and competitor positioning. Pull it in at the **drafting** stage, not during topic discovery. Topic discovery is more about calendar, performance, and category-level thinking. Once you're writing subject lines and body copy, you need the voice rules.

If brand context appears genuinely useful earlier (e.g., the user asks "is this campaign idea on-brand?"), pull it in earlier — just don't make the user wait while you load it unnecessarily.

## Workflow

### Stage 1 — Discover the topic

Don't auto-pull Klaviyo unless the user signals they want history-grounded suggestions. Start by asking what they have in mind. Useful opening questions:

- What's the goal of this campaign — revenue, list warming, new product seeding, list growth, retention?
- Anything time-anchored coming up (calendar event, launch, restock, seasonal peak)?
- Any topic you've been wanting to push?
- Should we check what we've sent recently to avoid overlap, or are you already across that?

From the conversation, propose 3–5 topic options spanning the four topic types:

- **Category theme** — a coffee usage occasion, flavour story, lifestyle theme (e.g., "Iced coffee season", "The 30-second morning")
- **Product launch** — new SKU, restock, new flavour, new bundle
- **Calendar event** — Mother's Day, Father's Day, Valentine's, Christmas, EOFY, Click Frenzy, Black Friday
- **Promotion** — discount, free shipping, BOGO, threshold offer

For each suggested topic, give a one-line "famous for" framing — e.g., *"The campaign that makes your brand famous for being the iced-coffee shortcut."* If you can't write that line, the topic isn't sharp enough.

### Stage 2 — Sanity-check against Klaviyo history (when relevant)

Once a topic is roughly chosen, pull recent Klaviyo campaign history if you haven't already. Look for:

- Have we run this topic in the last 6–8 weeks? If so, kill it or sharpen the angle.
- What was our last promo and when? If <3 weeks ago and this is another promo, flag the back-to-back risk.
- Which recent campaigns performed best (open rate, click rate, revenue per recipient)? Reuse what worked — angle, subject line style, send time.
- Which underperformed? Avoid repeating those patterns.

Surface the findings to the user before locking the topic.

### Stage 3 — Build the campaign plan (inline)

Walk the user through the plan in chat first. Don't produce a doc yet — iteration is faster in conversation. Format:

```
CAMPAIGN: [Famous-For line]
TYPE: [Themed / Launch / Calendar / Promo]
DATES: [Send window, cadence]
EMAILS:
  1. [Title] — [series role] — [one-line concept] — [template style]
  2. ...
```

For themed/launch/calendar campaigns, use the **4-email themed series** (see `references/campaign-series.md`). For promotion campaigns, use the **7-email promo series**.

Cadence: **2 emails per week** unless the user requests otherwise. For the 7-email promo series, that means ~3.5 weeks of sends — but in practice promos compress to 1–2 weeks, so the cadence rules bend for promos.

### Stage 4 — Draft each email (still inline)

Each email gets:

- **Role in the series** (e.g., "Educate / inform — Give")
- **Subject line** — 3 variants, A/B-able. Keep under 50 chars where possible. Mix curiosity, benefit, and specificity.
- **Preview text** — one line that complements (doesn't repeat) the subject. ~80–120 chars.
- **Template style** — one of the three (see `references/template-styles.md`)
- **Hero image direction** — what's in the image, mood, what's NOT in it. Specific enough to brief a designer.
- **Body copy** — full copy, on-brand voice, structured for the chosen template
- **CTA** — the single primary CTA. One per email. Secondary links are fine, but one button.
- **Standalone check** — confirm the email works for someone who didn't see the prior email and won't see the next. Each email contains the full hook + reason to click.

**Critical rule:** never write an email that depends on the prior one. No "as we mentioned last week...", no "in our next email we'll...". If a reader's first touchpoint is email #3, it must still make sense and still sell.

### Stage 5 — Lock and document

When the user signs off, produce a clean campaign plan document (`.md` or `.docx`) saved to the project workspace. The doc should include everything from Stage 3 + 4 so the user can hand it to a designer, copywriter, or load it into Klaviyo themselves.

Default format: markdown saved to the project workspace under a `campaigns/` folder, named with the campaign date and slug (e.g., `campaigns/2026-06-iced-coffee-season.md`). If the user asks for docx, use the docx skill.

If the user wants the emails created directly as Klaviyo drafts, follow Stage 6 below.

### Stage 6 — Push to Klaviyo (only when explicitly requested)

If the user asks to push the campaign to Klaviyo:

1. **Read `klaviyo-config.md`** (top level of this skill folder) — it has the brand's master template ID, sender defaults, and any audience config. This file is brand-specific and intentionally separate from the workflow logic.
2. **Follow the full workflow in `references/klaviyo-templates.md`** — brand-agnostic step-by-step for cloning, updating, creating campaigns, and assigning templates.

The non-negotiables (applied regardless of brand):

- **Always DND, never CODE.** Every email created in Klaviyo must be drag-and-drop (SYSTEM_DRAGGABLE). The brand owner needs to edit them in the Klaviyo visual editor. CODE templates aren't visually editable. Use `klaviyo_clone_email_template` from a DND source, `klaviyo_update_dnd_email_template` to modify, `klaviyo_create_dnd_email_template` only if creating fresh.
- **Clone the master.** Every email starts as a clone of the brand's master template (configured in `klaviyo-config.md`). Don't modify the master directly — always clone first.
- **Drafts only.** Never schedule sends without explicit user approval.
- **Report back per email** with campaign ID, template ID, and a Klaviyo preview link so the user can review.

## Series structures

### A. Themed / launch / calendar campaigns — 4 emails

| # | Role | Job | Default template |
|---|------|-----|------------------|
| 1 | Launch / introduce | Open the theme. Hook the reader on why this topic matters now. | Banner + text + products |
| 2 | Educate / inform | Teach something useful about the topic — context, how it works, why it's true. | Text only |
| 3 | Proof / how to | Show it working — customer reviews, recipe/how-to, transformation, comparison. | Banner + text + products |
| 4 | Product & offer | The strongest sell of the four. Offer, urgency, clearest CTA. | Banner + CTA + text |

Even though 1–3 are "Give", every one of them includes a product link and a reason to click through. The Ask in #4 is just the most direct.

See `references/campaign-series.md` for fuller detail and example arcs.

### B. Promotion campaigns — 7 emails

| # | Role | Job | Default template |
|---|------|-----|------------------|
| 1 | Early Access | List-favourites get first dibs. Build anticipation. | Banner + CTA + text |
| 2 | Launch Offer | Sale is live. Clean, immediate. | Banner + CTA + text |
| 3 | Sale Products | Lead with the hero SKUs on offer. | Banner + text + products |
| 4 | Category Sale / Banners | Browse-style email with multiple category links. | Banner + text + products |
| 5 | Best Sellers | Social proof + bestselling discounted SKUs. | Banner + text + products |
| 6 | Ends Soon | 48-hour reminder. Urgency, scarcity. | Banner + CTA + text |
| 7 | Last Chance | Ends tonight. Strongest urgency. | Text only |

Promo cadence usually compresses to 1–2 weeks. Adjust spacing accordingly. See `references/campaign-series.md`.

## Template styles

Three approved styles. Pick the one that fits the email's job, not personal preference:

1. **Banner + text + products** — Visual hook, narrative, product grid below. Best for emails 1, 3 in themed series; 3, 4, 5 in promo series.
2. **Text only** — A letter from the founder, a story, a "here's what we believe" piece. Best for educate/inform emails and "last chance" promo finales (raw urgency).
3. **Banner + CTA + text** — Single banner, one button, supporting copy. Best for promo launches, early access, ends-soon emails — anything where one clear action wins.

See `references/template-styles.md` for usage, anti-patterns, and image briefing notes.

## Topic selection guidance

See `references/topic-types.md` for the four topic types with examples, ICP-fit notes, and "famous for" framing.

## Klaviyo integration

Two files govern Klaviyo work:

- **`klaviyo-config.md`** (top level of this skill folder) — brand-specific config. Master template ID, sender defaults, audience info. Swap this file when forking the skill for another brand.
- **`references/klaviyo-templates.md`** — brand-agnostic workflow. DND-only rule, per-style block patterns, push-to-Klaviyo workflow.

## Pre-send checklist (apply to every campaign)

See `references/email-checklist.md` for the full list. Highlights:

- [ ] Each email's subject line is < 50 chars and on-brand
- [ ] Each email has a single primary CTA
- [ ] Each email stands alone — no references to other emails in the series
- [ ] No phrases on the brand "avoid" list (see brand-intelligence)
- [ ] Hasn't been run in last 6–8 weeks
- [ ] Not a promo following another promo within 2–3 weeks
- [ ] Cadence is 2/week (themed) or adjusted for promo compression
- [ ] Plan saved to `campaigns/` folder once locked

## What this skill is NOT for

- **Transactional or flow emails** (welcome series, abandoned cart, browse abandonment, post-purchase). Those are flows, not campaigns. Different skill territory.
- **SMS planning** unless the user explicitly wants a coordinated email + SMS campaign.
- **Writing one-off ad-hoc emails** that aren't part of a campaign. Just write them directly without the full framework.

## Reusing for other brands

This skill is structured to be portable. The framework, series, templates, push workflow, and checklist are brand-agnostic and live in `SKILL.md` and `references/`. The brand-specific parts live in two places:

- **`../eca-brand-intelligence/brand-data.md`** — voice, products, ICP, market, competitors, visual identity
- **`klaviyo-config.md`** (top level of this skill folder) — Klaviyo master template ID, sender defaults, audience config

To fork this skill for a different brand:
1. Swap `../eca-brand-intelligence/brand-data.md` for that brand's version
2. Swap `klaviyo-config.md` for that brand's version (set their master template ID, sender defaults, etc.)
3. Nothing else needs to change.

See `README.md` for the full fork walkthrough.
