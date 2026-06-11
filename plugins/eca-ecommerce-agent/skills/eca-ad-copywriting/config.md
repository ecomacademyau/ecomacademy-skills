# Ad Copywriting — Brand Config

This is the **only** file you edit when forking this skill for a different brand.
Everything in `SKILL.md` and `references/` is brand-agnostic.

## Our brand

- **Brand name:** [YOUR BRAND NAME]
- **Brand voice source:** the `eca-brand-intelligence` skill (invoke it before writing).
  If that skill isn't available, point Claude at your own brand brief / `brand-data.md`.

## Customer language sources (optional but powerful)

The best ad copy reuses the customer's own words. Point Claude at these if you have them:

- **Personas file:** [path, or "use the `eca-persona-builder` skill / its output"]
- **Customer reviews export:** [path to a .txt/.csv of reviews, if available]

Leave blank if you don't have them — the flow still runs, just lighter.

## Market

- **Default market / region:** [YOUR MARKET, e.g. Australia (AU)]
  Used for spelling, currency, and cultural references in the copy.

## House copy limits (defaults — only change if your account differs)

- **Headline:** max **45 characters** incl. spaces & emoji. No emoji at the start.
- **Primary text — short (V1):** max **~120 characters** incl. spaces & emoji. No CTA. No emoji at sentence start.
- **Primary text — long (V2):** emotion-led first line ≈100–140 chars, then 4 emoji-led benefit bullets, then a CTA with offer (+ optional URL).
- **Testing structure:** 3-2-2 (3 creatives of one angle, 2 headlines, 2 primary texts).

## Output preferences

- **Deliver in chat by default**, laid out in the 3-2-2 structure ready for Ads Manager.
- **Save a file?** [Yes/No] — if yes:
  - **Format:** Markdown (.md)
  - **Save location:** the project folder (the user's connected/working folder)
  - **Filename pattern:** `ad-copy-[brand]-[campaign]-[YYYY-MM-DD].md`
