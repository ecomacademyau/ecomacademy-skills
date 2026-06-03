---
name: eca-competitor-analysis
description: Run a full competitor teardown from a single URL — scan the competitor's website for positioning and messaging, pull their pricing and offers, dig through the Meta Ads Library to see the ads they're actually running, then compare all of it against our own brand and surface concrete opportunities and ad ideas. Use this skill whenever the user drops a competitor's URL or name and wants to know "what are they doing", asks to "analyse a competitor", "tear down [brand]", "see what ads [brand] is running", "check the ad library", "how do we compare to X", wants competitor pricing/messaging/offers, or is hunting for ad ideas and angles by studying rivals. Trigger even if they only ask for one piece (just the ads, just the pricing) — and trigger even if they don't say the word "competitor" but are clearly sizing up another brand in our space.
---

# Competitor Analysis

This skill turns a single competitor URL (or brand name) into a structured teardown: what they say, what they charge, what ads they run, and — crucially — how that stacks up against *us* and where the openings are.

The skill is **brand-agnostic in logic, brand-specific in config**. The workflow below works for any brand. The only thing that changes per brand is `config.md` (our known competitors, where to find our own brand context, and output preferences). To use this for a different brand, fork the folder and edit `config.md` — see `README.md`.

## The shape of a good teardown

The goal is not a data dump. A good teardown is *decision-useful*: it tells the operator what the competitor is doing, then immediately answers "so what?" for our brand. Every section should make the reader think either "we should copy that" or "they've left that wide open for us." Keep that lens on throughout — you are scouting for moves we can make, not writing a Wikipedia entry.

## Before you start: load our side of the comparison

The "how do we compare" half of this skill is only as good as our understanding of our own brand. **Invoke the `eca-brand-intelligence` skill first** so our positioning, products, pricing, ICP, and competitor list are loaded into context. The comparison and the ad ideas should be grounded in who we actually are — not generic best practice.

Then read `config.md` in this folder for the brand-specific settings (our known competitor list, output location, any house preferences).

If `eca-brand-intelligence` isn't available in the current environment, fall back to reading whatever brand context the user points you to, and tell them the comparison will be lighter without it.

## Workflow

Work through these phases in order. Phases 1–3 gather; phase 4 compares; phase 5 writes. Don't write the report until you've gathered, or you'll end up padding with assumptions.

### Phase 0 — Confirm scope (don't assume)

Before crawling anything, confirm with the user in one quick pass — this brand has been burned by silent inferred defaults, so validate rather than guess:

- **The competitor**: the exact URL or brand name. If they gave a name, find the official site first.
- **What they care about most this time**: the default is the full teardown (positioning + pricing + Meta ads + comparison). If they only want one slice (e.g., "just show me their ads"), do that and skip the rest.
- **Region for the ad library**: Meta Ads Library results are country-scoped. Default to the brand's home market in `config.md` unless told otherwise.

If the user already gave you everything, don't re-ask — just restate your understanding in one line and proceed.

### Phase 1 — Website scan (positioning, messaging, pricing, offers)

Read `references/website-scan.md` for the full checklist of what to extract and which pages to hit. In short:

1. Start with the homepage, then walk the key pages: a top product page (PDP), pricing/bundles, any "why us"/about page, and the cart/checkout entry (for shipping thresholds, guarantees, first-order offers).
2. Pull the **positioning and messaging**: the hero hook, primary and secondary value props, tone of voice, who they're clearly targeting, and the proof/trust signals they lean on (reviews, press, certifications, founder story).
3. Pull the **pricing and offers**: product range and price points, bundles, subscription/subscribe-and-save, any live promo, shipping and returns terms, money-back guarantees, and the first-order incentive (the popup/discount that greets new visitors).

**On tooling:** competitor sites are almost always JavaScript-rendered storefronts (Shopify and similar), so a plain fetch will return an empty shell. Use the Claude in Chrome tools — navigate to the page, then read the rendered text. If a fetch comes back as a bare page skeleton or "enable JavaScript", that's your signal to switch to the browser, not to retry the fetch. Capture the discount popup before dismissing it — it's often where the real offer lives.

### Phase 2 — Meta Ads Library (the ads they're actually running)

Read `references/meta-ads-library.md` for the step-by-step. The Meta Ads Library is a public, JavaScript-heavy app, so it needs the browser tools too. The short version:

1. Go to the Ads Library, set the country to the target region, set category to "All ads", and search the competitor's brand/Page name.
2. Record the **volume and longevity** — how many ads are active, and how long the oldest active ones have been running. Ads that have run for months are proven winners; that's where the signal is. New ads are tests.
3. Read the creative for **angles and hooks** — what problem/desire each ad leads with, the dominant messaging themes, and the offers featured.
4. Note the **formats** — UGC vs polished, static vs video, single image vs carousel — and which angle each format is carrying.
5. Flag the **standout ads worth stealing** — describe them concretely enough that we could brief a designer or shoot a version.

If a competitor has no ads in the library, that itself is a finding (they may not run paid Meta, or run under a different Page name — note it and move on).

### Phase 3 — (Optional) anything else the user asked for

If the user named a specific extra angle (e.g., email capture flow, a particular collection), gather it here. Otherwise skip.

### Phase 4 — Compare against us

Now bring in our brand (loaded in the pre-step). For each axis you gathered — positioning, pricing/offers, ad angles — line the competitor up against us and ask:

- Where are they **stronger** (something we should consider matching or countering)?
- Where are they **weaker or absent** (a gap we can own)?
- Where are we **already differentiated**, and are we saying it loudly enough?

The most valuable output is the *vacated axis*: the positioning or offer space the competitor has left open. If they own "cheapest", we don't fight on price — we attack the axis they ignored (quality, ritual, speed, story). Use our real brand positioning from `eca-brand-intelligence` to find that angle, don't invent one.

### Phase 5 — Write the report

Use the structure in `assets/report-template.md` exactly — it's ordered so a reader gets the "so what" fast. Save it as a markdown file to the location specified in `config.md` (default: the project folder), named like `competitor-teardown-[brand]-[YYYY-MM-DD].md`.

Two rules that keep the report honest:

- **Separate observed from inferred.** If you saw a price on the page, state it plainly. If you're reading between the lines ("likely targeting time-poor professionals"), mark it as a read, not a fact. The operator needs to know which is which.
- **End on action.** The final section is concrete opportunities and ad ideas we can actually execute — each one tied back to a specific gap or winner you found. Vague advice ("improve messaging") is a failure; "they have no subscription offer and we do — lead an ad with the convenience angle they can't match" is the bar.

Always include a Sources section linking the pages and ad library searches you used, so the operator can verify and go deeper.

## What this skill is NOT for

- **Inventing competitor data.** If you couldn't access a page or the ad library returned nothing, say so. A confident-sounding made-up teardown is worse than an honest gap.
- **One-off lookups.** "What's brand X's website?" doesn't need the full machinery.
- **Our own brand audit.** That's `eca-brand-intelligence`. This skill points outward at rivals.

## Reusing for other brands

Fork the folder, edit `config.md` (known competitors, home market, our-brand source, output path), and you're done — the workflow logic doesn't change. See `README.md` for the walkthrough.
