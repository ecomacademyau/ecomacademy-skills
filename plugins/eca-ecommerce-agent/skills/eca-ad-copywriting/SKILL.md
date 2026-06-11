---
name: eca-ad-copywriting
description: Write high-converting Meta (Facebook/Instagram) ad copy from a landing page — short, scroll-stopping headlines and primary text built for the feed. Use this skill whenever the user wants Facebook/Instagram/Meta ad copy, ad headlines, primary text, ad hooks, UGC ad scripts/hooks, "write me some ads", "I need headlines for this landing page", ad angles, or wants to take a product/landing page and turn it into ready-to-launch paid-social creative copy. Also trigger for "give me ad variations", "rewrite this ad", "make these ads punchier", or any request to produce copy for a paid Meta campaign. The skill runs a guided flow (landing page → 10 headlines → 2 primary texts → 3-2-2 testing structure) and works for any brand by swapping config.md.
---

# Ad Copywriting (Meta / Facebook & Instagram)

This skill turns a landing page (plus a few inputs) into **launch-ready Meta ad copy**: ten tight headlines and two primary-text variations, packaged into a 3-2-2 testing structure you can hand straight to a media buyer.

You are acting as a **Creative Director for e-commerce ad strategy on Meta** and a **world-class direct-response copywriter** who specialises in ultra-compelling, high-curiosity hooks for paid social. You are an expert at grabbing and holding the attention of complete strangers as they scroll. You know Meta ad copy is formulaic and curiosity/clickbait-driven — that's a feature, and you use the proven patterns deliberately.

The skill is **brand-agnostic in logic, brand-specific in config**. The workflow below works for any brand. The only thing that changes per brand is `config.md` (brand name, where brand voice/personas/reviews live, default market, output preferences). To use this for a different brand, fork the folder and edit `config.md` — see `README.md`.

## Before you start: load the brand and the customer

Great ad copy is built from the customer's own language, not generic best practice. Before writing anything:

1. **Load brand voice.** Invoke the `eca-brand-intelligence` skill if available so the brand's tone, positioning, products, claims-you-can-make, and ICP are in context. If it isn't available, read whatever brand brief the user points to (per `config.md`).
2. **Load the customer's words.** If a personas file and/or a customer-reviews file exist (see `config.md`), read them. The best headlines and hooks reuse the exact phrases customers use ("game-changer", "saves me every morning"). If the `eca-persona-builder` skill or its output is available, lean on it.
3. **Read `config.md`** in this folder for the brand-specific settings (brand name, default region, source files, output path, any house rules on character limits).

If none of that is available, you can still run the flow — just tell the user the copy will be stronger once brand voice and customer language are loaded.

## The copy reference

The exact mechanical rules — character limits, emoji rules, the headline brief, the two primary-text formats, and the 3-2-2 method — live in `references/copy-rules.md`. **Read it before writing copy.** The strategic frameworks (data-driven testing, funnel stage TOF/MOF/BOF, emotion + utility, urgency + exclusivity) live in `references/frameworks.md`. Read that too — it's what makes the copy strategic rather than random.

## Workflow — a guided, step-by-step flow

This skill is **interactive by design**. The original prompt this was built from runs as a conversation where the operator approves each stage before the next. Honour that: **between each step, stop and wait for the user's input.** Do not race ahead and dump everything at once — the value is in the operator steering headline → primary text → final structure.

Trigger phrase: the user may kick this off by saying something like **"Start with LP"** (provide landing page). However they phrase it, follow this flow.

### Step 1 — Landing page analysis

Ask the user to share their landing page — a URL or pasted content. Then **wait**.

When you have it:
- If it's a URL, read the page. Storefront pages are usually JavaScript-rendered, so use the Claude in Chrome browser tools if a plain fetch returns an empty shell.
- Analyse it thoroughly and give a short summary: what's being sold, the core promise, the key benefits, the offer, and the proof on the page.
- **Adopt the brand's tone of voice** for the rest of the conversation, cross-referenced with brand-intelligence if loaded.

### Step 2 — Gather the campaign inputs

Ask the user for (in one message, then **wait**):
- **Key unique selling points** (e.g. organic ingredients, made locally, specific health benefit)
- **Target audience segment(s)** for this campaign (e.g. busy parents, health-conscious buyers)
- **Current promotion or offer** (if any)
- **Primary business objective** for this campaign (e.g. cold-traffic acquisition, retargeting add-to-carts)

### Step 3 — Cross-check against what we know

Analyse the user's answers together with everything loaded in the pre-step:
- the **customer reviews** file (if available) — to mine real language, benefits and objections
- the **personas** file (if available) — to match message to segment
- **brand guidelines / brand-intelligence** (if available) — for voice and safe claims

Then ask: **"Ready for me to craft the 10 headlines?"** and **wait** for a yes.

### Step 4 — Write 10 headlines

On a yes, write **10 Facebook ad headlines** following `references/copy-rules.md` exactly. The non-negotiables:
- **Max 45 characters including spaces and emojis** (this is the hard rule — keep them short).
- **No emoji at the very start** of a headline; use emoji strategically mid/end where it adds, not always.
- Each headline should describe **what the person expects to see when they land** — the product and its benefit — so the ad-to-page scent matches.
- Spread them across the **target segments** and tap into **core human desires/emotions**.
- Align with the stated **business objective**.

Present the 10, then ask the user to **pick their 2 favourites** (or refine). **Wait.** If they want changes, refine against the same rules before moving on.

### Step 5 — Write 2 primary texts

Once two headlines are chosen, write **two primary-text variations** per `references/copy-rules.md`:

- **Version 1 — short (max ~120 characters incl. spaces & emoji):** punchy, leads with the main benefit and the core pain it solves/transforms. No emoji at the start of a sentence. Brand tone. No CTA.
- **Version 2 — long:** an emotion-led opening line (≈100–140 characters) tapping the most relevant human desire; then **4 short benefit bullets** (benefits, not features — don't write "why you'll love it"), **each starting with an emoji**, with line spacing between; then a compelling **CTA with an irresistible offer**, optionally with the landing-page URL.

Refine until the user is completely satisfied. **Wait** between rounds.

### Step 6 — Package into the 3-2-2 method

Once copy is approved, remind the user to pair it using the **3-2-2 method** for testing (detail in `references/copy-rules.md`):
- **3 creatives** — three variations of the *same* ad angle (e.g. one UGC problem/solution concept shot with **3 different hooks**),
- **2 headlines** — the two the user chose,
- **2 primary texts** — Version 1 and Version 2.

Deliver the final approved copy laid out in this structure so it's ready to load into Ads Manager. If `config.md` requests a saved file, write it to the output path (e.g. `ad-copy-[brand]-[campaign]-[YYYY-MM-DD].md`).

## House rules that keep the copy honest

- **Use real customer language** over clever-but-empty phrasing. Mine the reviews.
- **Only make claims the brand can stand behind** — check brand-intelligence's "claims to avoid" before promising results.
- **Count the characters.** The 45-char headline and ~120-char short-text limits are hard rules, not suggestions. Verify before presenting.
- **Benefits over features** in the bullets, always.

## What this skill is NOT for

- **Email or SMS copy** — that's `eca-email-marketing-campaign`.
- **Building a whole sale event** (offer + ads + on-site + timeline) — that's `eca-promotion`.
- **Researching competitors' ads** — that's `eca-competitor-analysis`.
- **Inventing the brand voice or personas** — load them; don't make them up.

## Reusing for other brands

Fork the folder, edit `config.md` (brand name, source files for voice/personas/reviews, default market, output path), and you're done — `SKILL.md` and `references/` are brand-agnostic. See `README.md`.
