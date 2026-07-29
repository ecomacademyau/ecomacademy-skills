# Changelog — meta-ads-4pi-analyst

## v2.2.1 — 2026-07-29

- **Trend-label correctness**: headline frequency/CPM and their trend endpoints must come from one series (mean of dailies; first-3 → last-3), with an explicit ±2% flat band. Fixes labels contradicting their own numbers ("rising (1.42 → 1.42)") and headlines sitting outside their own trend range. Frequency direction feeds the both-rising danger signal, so this is correctness, not cosmetics.
- **Small-Sample Rule**: ads with ≤2 purchases or <2× target CPA of spend in the 7-day window are judged on their 30-day figures, with both printed and the switch stated in one line. Codifies what the 29 Jul report did ad-hoc.

## v2.2.0 — 2026-07-16

- **Report depth modes**: third pre-flight question — Full report vs Quick check, with context-aware recommendation (Full for first reports / stale memory; Quick for routine re-runs). Quick keeps the identical analysis, verdicts, and history write, skips enrichment calls (YoY, benchmark, post-click, anomaly/opportunity) and renders the condensed report (scorecard + Since Last Report + funnel maps + 4PI tables + scaling verdicts + top 3 priorities). Post-click candidates in Quick mode are flagged in one line, not audited. History schema gains a `mode` field.

## v2.1.1 — 2026-07-16

- **Industry Benchmark card redesign**: percentile band graphic (p25/median/p75), per-campaign 30d ROAS table with quarter pills + bold ACCOUNT row, plain-language explainer, "Why ROAS only" bullets (cohort is USD — cost metrics never compared or converted cross-currency; ROAS is a ratio so it travels), "context, not a verdict" close. Data provider anonymised in all client-facing output.

## v2.1.0 — 2026-07-16

- **Year-over-year seasonality check**: account-level comparison of the 30d + MTD windows vs the same calendar dates last year, rendered as a card under the Account Snapshot. CPM leads (cleanest seasonality signal); material YoY CPM gaps (±20%) echo into the header macro chip. Graceful skip for accounts with no year-ago data.
- **Version stamping**: skill version in frontmatter + title; every report footer states the producing version.
- **Firecrawl freshness**: `maxAge: 0` on metastatus checks and post-click scrapes (the MCP caches by default); confirmed the firecrawl-mcp schema supports geolocated scraping (`location.country`).
- **Triple Whale benchmark fallback**: when Meta's peer benchmark returns no data, scrape benchmark.triplewhalelabs.com for the client's vertical (new `industry_vertical` config field) — free Meta-channel ROAS/CPA/CPM p25/median/p75, rendered as percentile placement, directional context only.

## v2.0.0 — 2026-07-13

Full rebuild of the original CSV-only skill:

- Official Meta Ads MCP as primary data source (live-verified field names), CSV fallback retained
- Data-freshness guard (never reuse a previous day's pulls; re-runs always re-pull)
- Pre-flight questions: target CPA (with "I don't know" → ecomOS pointer; never invented) + account/campaign scope
- Profit per Order = AOV − CPA (pre-COGS proxy; GPT column overrides on CSV path; margin % upgrade via client config)
- ECA Design System report skin (dark hero, stat grids, chip rows, CSS/SVG charts, frequency legend with exact values, VIDEO/STATIC format badges)
- Account sentiment badge + metastatus.com platform check in header
- Campaign scaling verdicts (SCALE +10–20% / HOLD / TRIM −10–20%) with pass/fail checklist
- Hardened post-click audit: trigger gates (data bar + one-purchase swing test), delivered-market from country breakdown, geolocated scrape, currency reconciliation with no FX maths, DOM-presence ≠ user-visible, "page is fine" is a valid outcome
- Report memory: week-over-week deltas + "Since Last Report" accountability card (history JSON beside + inside each report)
- Industry benchmark enrichment (LAST_28D, graceful skip when Meta returns no peer data)
- Andromeda hook generator (3–5 structurally-diverse hooks grounded in reviews/personas)
- Recommendations grounded in five named sources; escalations addressed to "the account owner"
