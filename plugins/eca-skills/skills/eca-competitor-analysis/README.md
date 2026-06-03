# Competitor Analysis Skill

Turn a single competitor URL (or brand name) into a structured teardown: their positioning and messaging, their pricing and offers, the Meta ads they're actually running, and a side-by-side comparison against your own brand — ending in concrete opportunities and ad ideas you can execute.

## What it does

Given a competitor, Claude will:

1. Load **your** brand context (via the `eca-brand-intelligence` skill) so the comparison is grounded in who you really are.
2. **Scan the competitor's website** — homepage, PDPs, pricing/bundles, subscription, about, checkout, and the entry popup — for positioning, messaging, pricing, and offers.
3. **Search the Meta Ads Library** for the ads they're running — volume, longevity (proven winners vs tests), angles, formats, and standout creative.
4. **Compare** competitor vs you on each axis and find the vacated space you can own.
5. Write a **markdown teardown** to your project folder, ending in executable opportunities and ad ideas.

## What you need

- **Claude in Chrome** (browser tools) — competitor storefronts and the Meta Ads Library are JavaScript apps that need a real browser to render.
- The **`eca-brand-intelligence` skill** (recommended) — for the "how do we compare" half. Without it, the comparison still runs but is lighter.

## How to use it

Just point Claude at a competitor:

- "Run a competitor teardown on https://[competitor].com"
- "What ads is [brand] running right now, and how do we compare?"
- "Tear down [brand] — pricing, messaging, the lot."
- "Compare us to our top 3 competitors" (uses the watchlist in `config.md`)

Claude confirms scope, gathers, compares, and saves the report.

## Files

```
competitor-analysis/
├── SKILL.md                      # the workflow (brand-agnostic)
├── config.md                     # YOUR settings — the only file to edit when forking
├── references/
│   ├── website-scan.md           # what to extract from a competitor site
│   └── meta-ads-library.md       # how to navigate the Meta Ads Library
├── assets/
│   └── report-template.md        # the teardown structure
└── README.md
```

## Forking for a different brand

The workflow logic is brand-agnostic — the only brand-specific content lives in `config.md`. To reuse this skill for another brand:

1. Copy the whole `competitor-analysis/` folder (rename it if you want both side-by-side, e.g. `competitor-analysis-acme/`).
2. Open `config.md` and edit:
   - **Our brand** — the brand name and where its context lives (a `eca-brand-intelligence` fork, or a brand file).
   - **Home market** — the default country for the Meta Ads Library.
   - **Known competitors** — the watchlist table.
   - **Output preferences** — format, save location, filename pattern.
3. That's it — don't touch `SKILL.md` or `references/`. They're designed to work for any brand.

## Sharing with your team

Package the folder as a `.skill` file (a zipped skill directory) and share it. Teammates install it, edit `config.md` for their setup, and they're running teardowns too.
