# Hook Generator — Andromeda-Diverse Meta Ad Hooks

Use this when a Campaign Next Steps recommendation includes a **new creative test**. Generate **3–5 hooks** (not 20 — the report is a starting point, not a creative brief) across **different structural categories**, so the recommendation ships with something testable.

## Why structural diversity

Meta's Andromeda algorithm rewards variant diversity that's *structural* — different storytelling angles — not just different opening sentences on the same shot. Hooks from the same category compete with each other; hooks from different categories expand delivery.

## The 8 structural categories

1. **Outcome-first specificity** — "I [outcome] in [timeframe]"
2. **Counter-conventional** — "Stop [common advice], do [opposite]"
3. **Problem agitation** — "If you've ever [pain point], you'll get this"
4. **Founder POV / origin story**
5. **Mechanism reveal** — "The [ingredient/feature] that makes [outcome] possible"
6. **Social proof front-loaded** — "12,000 customers later, this is what we learned"
7. **Before/after timestamp** — "Day 0 vs Day 60"
8. **Comparison teardown** — "[Competitor] vs us — the actual difference"

## How to generate (act as a senior performance creative strategist for DTC brands)

Fill these from the brand intelligence, the account data, and scraped reviews — never invent product claims:

- PRODUCT/BRAND: 2–3 sentences
- TARGET CUSTOMER: who buys + why (from personas; note if the recommended test targets an *untapped* persona)
- KEY MECHANISM / DIFFERENTIATOR: what actually works / what makes it different
- TONE: brand voice

For each hook return, in a compact table:

| Hook (verbatim, ≤12 words) | Visual cue (1 sentence) | Structural category |

Rules:

- Pick categories that fit the diagnosed funnel gap (TOF gap → problem agitation, counter-conventional, outcome-first; BOF gap → social proof, comparison, before/after)
- Use real customer language from reviews where possible — a 15-year-old's own words beat copywriting
- Avoid every category already dominant in the account's live ads (structural diversity vs what's already running)
- Never fabricate statistics, customer counts, or timeframes — if reviews don't support "Day 60", don't write it
- Link [The Hook Bank](https://hooks.antoineorban.com/) after the table for deeper exploration

## Full prompt template (for when the user asks for the complete 20-hook run)

> You are a senior performance creative strategist for DTC brands. I need you to generate 20 structurally-different Meta ad hooks for the product/brand below. Meta's Andromeda algorithm rewards variant diversity that's structural — different storytelling angles — not just different opening sentences on the same shot. PRODUCT/BRAND: [...] TARGET CUSTOMER: [...] KEY MECHANISM / DIFFERENTIATOR: [...] TONE: [...] Generate the 20 hooks across these 8 structural categories (multiple hooks per category if relevant): [the 8 categories above]. For each hook, return: the verbatim opening line (max 12 words), the visual cue (1 sentence), and which Andromeda diversity dimension it occupies. Make the hooks specific to my product, not generic.
