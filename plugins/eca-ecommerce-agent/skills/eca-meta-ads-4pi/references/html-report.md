# Branded HTML Report — Template & Spec

The deliverable is a **single self-contained HTML file** (no external assets except logo images and Google Fonts). Save as `4pi-report-<brand-slug>-<YYYY-MM-DD>.html` in the outputs folder and present it.

## Branding — ECA Design System (default)

Reports are branded as **Ecommerce Academy™ (ECA)** — read `assets/ECA Design System/README.md` and use the tokens in `assets/ECA Design System/eca-tokens.css` before building. In short: dark `#0A0A0A` hero header with the ECA green (`#3DD62B`) mark and eyebrow label, ALL-CAPS Nunito Sans headlines, Montserrat body, white 12px-radius cards on `#F5F5F5`, pill action badges using the ECA semantic colors (success `#3DD62B` / warning `#F5A623` / error `#D0021B` / info `#4A90E2`), no gradients, no serif fonts, no emoji.

The **client** appears as "Prepared for <Brand>" in the header (client logo small, if available from `clients/<brand>.md`). Client brand colors do NOT drive the report chrome — ECA does.

Map the generic variables used in this spec onto ECA tokens: `--brand`→`--eca-green`, `--accent`→`--eca-info`, `--good/warn/bad`→ECA semantic colors, `--paper`→`--eca-bg`, `--line`→`--eca-line`.

## Layout rules

- Max width ~1100px, generous whitespace, cards with soft shadows (`box-shadow: 0 6px 24px rgba(0,0,0,.06)`), 14–16px radius.
- Tables: full-width, sticky header row, zebra striping with `--brand-soft`, right-aligned numbers, tabular-nums.
- Action labels as pill badges: Keep/Scalable = `--good`, Hold/Watch = `--warn`, Fix = `--accent`, Stop = `--bad`, Insufficient data = `--muted`.
- Funnel positions as small tags: TOF (green tint), MOF (amber tint), BOF (blue tint), SAT (red tint).
- Danger signals (CPM+frequency rising, saturation) get a full-width alert band in `--bad` tint with a ⚠ prefix.
- "Double-check with the account owner" notes render as a distinct amber callout box.
- Print-friendly: `@media print` collapse shadows, avoid page-break inside cards.
- No JavaScript needed except (optional) a tiny `<script>` for collapsible ad-breakdown `<details>` styling. Use `<details>/<summary>` for per-ad deep dives so the report stays scannable.

## Readability & graphics (mandatory)

The reports are data-heavy; the design's job is to make them feel light:

- **Colored table headers** — header row uses `--eca-green-tint` background with `--eca-green-dark` text (not gray-on-white). Zebra rows stay subtle.
- **Inline graphics, pure CSS/SVG only** (no chart CDNs — the file must render offline forever):
  * **Daily-spend mini bar chart** per ad (7 tiny bars from the daily pull) — shows the spend trajectory at a glance instead of a "$X → $X → $X" string
  * **Spend-share bar** in the funnel map (horizontal bar sized to % of campaign spend)
  * **Frequency: exact number first, gauge second.** The daily frequency value is displayed as a large bold number (with its trend/range in small text, e.g. "1.17 ↓ falling (1.26 → 1.14)"), and the small gauge (markers at 1.15 and 1.40) sits beneath it as visual support. The funnel map is preceded by a **legend line** spelling out the decoder: < 1.15 TOF (prospecting) · 1.15–1.40 MOF · > 1.40 BOF (retargeting) · > 2.0 saturation, with the zone colors. Never show the gauge without the exact number.
- Numbers still appear next to every graphic — charts assist reading, never replace data.

## Required section order

1. **Header band** — logo, brand, report title, "as of" date, date range, primary window, account currency. Plus, in the header: **(a) Account sentiment badge** — STRONG (green) / STEADY (blue) / AT RISK (amber) / DECLINING (red) with one plain-English sentence; **(b) Meta platform status line** from metastatus.com ("no platform incidents in window" or the flagged incident); **(c)** macro-environment note if the window overlaps a calendar event.
2. **Account scorecard** — KPI cards: Total spend (7d), Purchases, Blended CPA vs target, Blended AOV, Profit/Order (pre-COGS, or GPT if CSV), directional ROAS. Small deltas vs 30d run-rate. When report memory exists, each KPI also shows its **delta vs the previous report** (arrow + value; for cost metrics down = green). When the industry benchmark returned data, one line here: "Cost per result vs similar advertisers: X% better/worse (Meta peer benchmark, LAST_28D)".
2b. **"Since Last Report" card** (only when memory exists — `references/report-memory.md`): header "vs report of <date> (N days ago)" with the sentiment shift, then every previous recommendation with its verified verdict — ✔ Actioned (+ outcome number) / ✘ Not actioned (+ current cost of inaction) / ◐ Due later / ？ Can't verify — followed by one-line NEW ads (green NEW badge + launch date) and GONE/stopped ads ("stopped ✔ as recommended" where applicable). Verdicts come from the current pull, never assumption. First-run mode: replace this card with one line — "First tracked report — week-over-week comparison starts next run."
3. **Account snapshot** — three tables (Last 7 Days / MTD / Last 30 Days): `Campaign | Status | Spend | Active Ads | Funnel Health | Blended CPA | Profit/Order | Profitable?`. Active Ads count is identical across all three (it's current state). Sorted by spend desc.
4. **Per-campaign sections** (sorted by spend desc). Each:
   - **Campaign stat grid — never a run-on "·"-separated line.** Render the campaign header numbers as a grid of small labelled stat cells (same `.kpis`/`.kpi` pattern as the account scorecard, smaller). One number per cell, label above, context below. Cells: Spend 7d (with 30d below) · Budget/day (with actual pacing below) · Purchases 7d · Blended CPA (vs target if set) · AOV · Profit/Order · ROAS directional · CPM range (low–med–high as the sub-line) · Ads (active / testing / stopped as the sub-line). A reader should get the campaign's state in one glance without parsing a sentence.
   - **Funnel map table**: `Ad | Funnel | Daily Freq | Spend Share | CPM | Daily Spend Trend` + funnel-gap verdict line. **Every ad carries a creative-format badge** (VIDEO dark / STATIC light / CAROUSEL) next to its name, sourced from `ads_get_creatives` (`video_id` → video; `object_type` SHARE/PHOTO → static; CAROUSEL → carousel; name keywords as last resort). The legend line includes the format badges with the reminder to **compare CPM within format** — video inventory prices higher than static, so a $15 video and an $11 static can be equally cheap; never read a static-vs-video CPM gap as a performance signal.
   - **4PI table**: `Ad | Status | Data OK? | Spend 7d | % Camp | CPM | CPM trend | Daily Freq | Funnel | CPA | Profit/Order | AOV | Action`
   - **Ad breakdowns** (collapsible `<details>` per ad) — structured, not a bullet dump:
     * `<summary>`: ad name + action pill + one-line verdict
     * **Chip row**: small stat chips (Spend · % of campaign · CPM · Daily freq · CPA · P/Order · ROAS) — scannable at a glance. When memory has this ad id, append "was $X" to the CPA and Spend chips ("CPA $22.56 · was $43.93 ✔"); ads not in memory get a green NEW badge in the summary line.
     * **Three labelled mini-blocks** in a 3-column grid (stack on mobile):
       - *Delivery* — status, learning status, creative type, last-5-days spend trajectory, freq & CPM trend arrows
       - *Economics* — purchases, CPA vs peers/target, AOV, profit/order, attribution or repeat-purchase flags
       - *Creative* — hook / hold / link CTR vs thresholds, drop-off note
     * **The read** — 1–2 plain-English sentences: what Facebook is doing with this ad and why the action label follows. This is the only prose; everything else is chips and labelled values.
   - **Campaign diagnosis**: Direction (up/down/flat 7d vs 30d) · Funnel health & gap · Profitability · Risk ("what breaks in 7 days if nothing changes")
   - **Scaling verdict card** (active campaigns only): the SCALE +10–20% / HOLD / TRIM −10–20% verdict as a prominent badge, followed by the condition checklist with ✓/✗ marks (see Knowledge Base "Budget Scaling Verdict"). A HOLD states what unlocks the next move and the date to re-check.
   - **Campaign next steps** — every recommendation grounded in and citing: current account data, brand intelligence/personas, customer reviews (quote real language), best practice (format tendencies), and the Ad Concept Board (Foreplay link). Structure: 1) Next creative to test — gap it solves, concept, why, persona + angle, format, success signal, **plus a 3–5 hook table generated per `references/hook-generator.md`** when the recommendation is a creative test. 2) Budget recommendation with numbers. 3) Ads to act on now.
5. **Post-click audit** (if run) — one card per audited ad: ad promise vs page reality, the mismatch, fixes, escalation note if applicable.
6. **Account-level summary** — Top 3 priorities (numbered, each with a specific number) + systemic observations paragraph (cross-campaign patterns, repeat-purchase bias, attribution concerns, profitability concerns). Include Meta anomaly signals / opportunity score notes here if pulled.
7. **Footer** — "Generated [date] · 4PI framework · Data: Meta Ads API ([windows pulled])" + pre-COGS disclaimer when using the proxy.

## Writing rules inside the report

Same tone rules as the Knowledge Base: numbers in every recommendation, campaign-scoped comparisons, lead with gaps not wins. Keep the "signal" column to one plain-English line ("Facebook is using this as its main prospecting workhorse", "High CPM for broad reach — audience isn't loving it").

## Skeleton

Use this structure (fill all `{{ }}`; repeat blocks as needed):

```html
<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>{{BRAND}} — 4PI Report {{DATE}}</title>
<link href="https://fonts.googleapis.com/css2?family=Lora:wght@500;600&family=Inter:wght@400;500;600&display=swap" rel="stylesheet">
<style>
  :root{ /* variables from client config, see above */ }
  body{margin:0;background:var(--paper);color:var(--ink);font:15px/1.55 Inter,sans-serif}
  .wrap{max-width:1100px;margin:0 auto;padding:32px 20px}
  h1,h2,h3{font-family:Lora,serif;line-height:1.2}
  .card{background:var(--card);border:1px solid var(--line);border-radius:16px;
        box-shadow:0 6px 24px rgba(0,0,0,.06);padding:24px;margin:20px 0}
  table{width:100%;border-collapse:collapse;font-variant-numeric:tabular-nums}
  th{position:sticky;top:0;background:var(--card);text-align:left;font-size:12px;
     text-transform:uppercase;letter-spacing:.06em;color:var(--muted);
     border-bottom:2px solid var(--line);padding:10px 8px}
  td{padding:10px 8px;border-bottom:1px solid var(--line)}
  tr:nth-child(even) td{background:var(--brand-soft)}
  td.num{text-align:right}
  .pill{display:inline-block;padding:2px 10px;border-radius:999px;font-size:12px;font-weight:600}
  .pill.keep,.pill.scalable{background:#1E7B4D1A;color:var(--good)}
  .pill.hold,.pill.watch{background:#B58A001A;color:var(--warn)}
  .pill.fix{background:#1F3A5F1A;color:var(--accent)}
  .pill.stop{background:#B3352B1A;color:var(--bad)}
  .pill.insufficient{background:#8A85781A;color:var(--muted)}
  .tag{display:inline-block;padding:1px 8px;border-radius:6px;font-size:11px;font-weight:600}
  .alert{background:#B3352B14;border-left:4px solid var(--bad);padding:14px 18px;border-radius:8px;margin:16px 0}
  .check{background:#B58A0014;border-left:4px solid var(--warn);padding:14px 18px;border-radius:8px;margin:16px 0}
  .kpis{display:grid;grid-template-columns:repeat(auto-fit,minmax(160px,1fr));gap:14px}
  .kpi{background:var(--card);border:1px solid var(--line);border-radius:14px;padding:16px}
  .kpi .v{font-size:24px;font-weight:600;font-family:Lora,serif}
  .kpi .l{font-size:12px;color:var(--muted);text-transform:uppercase;letter-spacing:.05em}
  details{border-top:1px solid var(--line);padding:10px 0}
  summary{cursor:pointer;font-weight:600}
  .chips{display:flex;flex-wrap:wrap;gap:8px;margin:12px 0}
  .chip{background:var(--brand-soft);border:1px solid var(--line);border-radius:10px;padding:6px 12px;font-size:12.5px}
  .chip b{display:block;font-size:14px;font-variant-numeric:tabular-nums}
  .miniblocks{display:grid;grid-template-columns:repeat(auto-fit,minmax(220px,1fr));gap:12px;margin:12px 0}
  .mini{background:var(--paper);border:1px solid var(--line);border-radius:12px;padding:12px 14px;font-size:13px}
  .mini h4{margin:0 0 8px;font-size:11px;text-transform:uppercase;letter-spacing:.06em;color:var(--muted)}
  .mini dl{margin:0}.mini dt{color:var(--muted);font-size:11.5px}.mini dd{margin:0 0 6px;font-weight:500}
  @media print{.card{box-shadow:none;break-inside:avoid}}
</style>
</head>
<body>
<div class="wrap">
  <header class="card" style="border-top:6px solid var(--brand)">
    <img src="{{LOGO_URL}}" alt="" style="height:40px"> <!-- omit tag entirely if no logo -->
    <h1>{{BRAND}} — Meta Ads 4PI Report</h1>
    <p>As of {{REPORT_DATE}} · Window: {{RANGE}} · Primary: last 7 days · Currency: {{CUR}}</p>
    {{MACRO_NOTE_IF_ANY}}
  </header>
  <section class="kpis"> ... KPI cards ... </section>
  <section class="card"><h2>Account Snapshot</h2> ... three window tables ... </section>
  <!-- per campaign -->
  <section class="card">
    <h2>{{CAMPAIGN NAME}}</h2>
    ... header stats, funnel map, 4PI table ...
    <details><summary>{{AD NAME}} — full breakdown</summary> ... </details>
    <h3>Diagnosis</h3> ... <h3>Next steps</h3> ...
  </section>
  <section class="card"><h2>Post-Click Audit</h2> ... </section>
  <section class="card"><h2>Top Priorities</h2> ... </section>
  <footer><p>Generated {{DATE}} · 4PI framework · Profit/Order is pre-COGS (AOV − CPA){{OR_GPT_NOTE}}</p></footer>
</div>
</body>
</html>
```

Adapt freely within the brand variables — the section order and data-integrity rules are fixed; the aesthetics flex with the client.
