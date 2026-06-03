# Competitor Analysis — Brand Config

This is the **only** file you edit when forking this skill for a different brand.
Everything in `SKILL.md` and `references/` is brand-agnostic.

## Our brand

- **Brand name:** [YOUR BRAND NAME]
- **Our brand context source:** the `eca-brand-intelligence` skill (invoke it before comparing).
  If that skill isn't available, point Claude at your own brand brief / `brand-data.md`.

## Home market

- **Default ad-library country:** [YOUR MARKET, e.g. Australia (AU)]
  Meta Ads Library results are country-scoped; use this unless the user names another region.

## Known competitors

A starting watchlist so the user can say "run the usual list" or "compare us to our top 3".
Keep this current as the landscape shifts.

| Brand | URL | Note |
|-------|-----|------|
| _Add competitor_ | _https://_ | _e.g. closest positioning rival_ |
| _Add competitor_ | _https://_ | _e.g. price leader_ |
| _Add competitor_ | _https://_ | _e.g. premium / category-adjacent_ |

> Tip: fill this in once and the skill can run a multi-competitor sweep on request.

## Output preferences

- **Format:** Markdown (.md)
- **Save location:** the project folder (the user's connected/working folder)
- **Filename pattern:** `competitor-teardown-[brand]-[YYYY-MM-DD].md`
- **House style:** decision-useful and concise; separate observed facts from inferred reads;
  always end with concrete, executable opportunities and ad ideas.
