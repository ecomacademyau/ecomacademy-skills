# Persona Builder — Brand Config

This is the **only** file you edit when forking this skill for a different brand.
Everything in `SKILL.md`, `references/` and `templates/` is brand-agnostic.

## Our brand

- **Brand name:** [YOUR BRAND NAME]
- **Brand context source (optional):** the `eca-brand-intelligence` skill — load it to sharpen persona language and know the product lineup.

## Data source — where the customer voice lives

Personas are only as honest as the data. Point Claude at one or more of:

- **Reviews export:** [path to a .txt/.csv of reviews — Judge.me, Okendo, Yotpo, Shopify, etc.]
- **Other voice-of-customer:** [support tickets, survey responses, testimonials, social comments]
- If nothing is on file, the user pastes a batch of reviews into the chat.

> Sample across all star ratings — the 1–3 star reviews carry the objections.

## How many personas

- **Default:** 3–5 distinct personas. Produce fewer if the data is thin, and say so.

## Output preferences

- **Format:** Markdown (.md)
- **Save location:** the project folder (the user's connected/working folder)
- **Filename pattern:** `personas-[brand]-[YYYY-MM-DD].md`
- **House style:** evidence-based; verbatim customer quotes in triggers; objections always included with a rebuttal angle; end with actionable strategy takeaways.
