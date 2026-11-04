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
  * **Trend labels must match the numbers printed beside them.** Headline frequency and its trend come from one series (mean of dailies; first-3 → last-3 endpoints); direction word uses the ±2% flat band from the Knowledge Base. Before rendering any row, sanity-check it: the headline must fall inside — or plausibly near — its own trend range, and "rising" must never sit next to two equal values. Same rule for CPM trend chips.
  * **Frequency: exact number first, gauge second.** The daily frequency value is displayed as a large bold number (with its trend/range in small text, e.g. "1.17 ↓ falling (1.26 → 1.14)"), and the small gauge (markers at 1.15 and 1.40) sits beneath it as visual support. The funnel map is preceded by a **legend line** spelling out the decoder: < 1.15 TOF (prospecting) · 1.15–1.40 MOF · > 1.40 BOF (retargeting) · > 2.0 saturation, with the zone colors. Never show the gauge without the exact number.
- Numbers still appear next to every graphic — charts assist reading, never replace data.

## Readability rules (Full and Quick)

The reader is a busy owner, often on a phone. Every rule here serves one goal: they know what to do within the first screen, and nothing after it makes them scroll sideways or decode jargon.

- **Decisions before detail.** Header, scorecard, then the Top 3 priorities (section 2a). Every table after that is evidence for those three.
- **Length.** Full ≈ 4,000 to 5,000 words; Quick ≈ 2,000 to 2,500. Count before saving; if Full runs long, cut repetition and thin-ad copy first, never the numbers behind an action.
- **One home per number.** A figure is shown in full where it's computed (its table or card). The header sentence and the priorities may repeat the two or three numbers that drive the decisions; other sections point back ("see the segments card") instead of printing it again.
- **Plain words.** First use in the body is plain English with the short form after it ("cost per new customer (NCPA)"). Every short form used in the report is defined in the glossary.
- **Glossary.** A collapsed `<details class="glossary"><summary>How to read this report</summary>` directly under the header band, one line per term, only for terms the report uses: NCPA · New / engaged / existing customers · Funnel position (TOF / MOF / BOF from daily frequency) · Data bar and Insufficient data · Profit/order (pre-COGS) · Scaling verdict (SCALE / HOLD / TRIM) · Segment setup status · CPL (when a lead campaign is present) · Catalog frequency bands (when a catalog campaign is present). Ten lines at most.
- **No sideways scrolling on a phone.** Below 640px, every table with more than 5 columns renders as stacked cards: each row a card, each cell `label: value`. Give every such table `class="stack"`, write its header row inside `<thead>`, put `data-label` on every `<td>`, and use `@media (max-width:640px){ table.stack thead{display:none} table.stack tr{display:block;border:1px solid var(--eca-line);border-radius:10px;margin:8px 0;padding:6px 10px} table.stack td{display:flex;justify-content:space-between;gap:12px;border:0;padding:4px 0} table.stack td:before{content:attr(data-label);color:var(--eca-gray-2);font-size:11px} }`. Tables of 5 columns or fewer may scroll.
- **Collapse thin ads.** Ads labelled Insufficient data, and ads stopped before the window, don't get their own breakdown. List them in one collapsed `<details>` per campaign ("Too early to read: 8 ads") as a compact table: name · format · spend · days live · purchases. Full breakdowns are for ads with a decision attached.

## Report depth modes

Two render modes; same underlying analysis, same history file, same ECA design.

**Full**: the complete report, in the section order below, within the readability rules above (≈ 4,000 to 5,000 words).

**Quick** — the condensed weekly check. **Campaign-level by default; ad-level only where a decision is needed.** Target ≈2,000–2,500 words regardless of account size. Header eyebrow reads "Quick Check"; footer notes "Quick report — run a Full report for ad-level deep dives".

Structure:

1. Header (sentiment badge, platform status, macro chip, targets chip, collapsed glossary) + account scorecard with memory deltas, then the **Top 3 priorities**, placed as in Full but capped at ≤120 words each.
2. **Since Last Report card — never cut.** It's the point of a weekly. Render as a table (recommendation · verdict · outcome number), not prose.
3. **One snapshot table, not three.** Active-ad counts and funnel-health strings are identical across windows — repeating them three times is duplication, not information. Columns: `Campaign | Type | Status | Spend 7d | Spend MTD | Spend 30d | CPA 7d (vs 30d) | NCPA 30d | Existing % of purchases | Profit/Order | Funnel health | Profitable?` + an ACCOUNT row. Lead campaigns show CPL in the CPA cell and a dash for NCPA, existing %, profit and Profitable?; catalog campaigns show their daily frequency band in the funnel cell; other campaigns show spend and a dash elsewhere. The ACCOUNT row's CPA and profit cover purchase and catalog campaigns only; say so in a footnote, since its CPA won't equal total spend ÷ purchases when lead or other campaigns run. Segment setup status that isn't OK goes in the header Watch line; the full Segments & NCPA card is Full-mode only. When the Shopify cross-check ran, its one line (new / returning customers, Meta NCPA floor) sits directly under the snapshot table.
4. **Campaign triage — the length control.** Full treatment only for campaigns that are **≥10% of account spend OR carry a red flag** (negative profit/order, saturation, both-rising CPM+frequency, a stop/scale decision pending). Everything else: its snapshot row plus one sentence, no heading. A campaign at 1.6% of spend does not get a section, and an "other" campaign (traffic, engagement, awareness) never does, whatever its spend.
5. Per qualifying campaign — **campaign-level, not ad-by-ad** (lead gen and catalog: their Quick layout in `references/campaign-types.md` §4; purchase campaigns:)
   - Compact stat grid
   - **Funnel health bar**: one stacked bar of spend share by funnel position (TOF / MOF / BOF / SAT) with % labels, plus a one-line verdict naming the gap ("balanced on paper — but TOF is one ad"). This replaces the per-ad funnel map table.
   - **"Ads to act on"** — only ads with a non-Keep action (Stop / Fix / Scalable / Insufficient-but-notable), with the columns that justify the call (format badge, daily freq, spend share, CPM, CPA 7d/30d, action). Close with one line: "The other N ads: Keep or Hold, no change this week." Never drop ad evidence for an ad you're asking them to action — a recommendation without its numbers is an assertion.
   - **Scaling verdict card** (unchanged — it's decision-grade)
   - **Diagnosis + Next Steps merged** into one block, ≤100 words per campaign, max 3 bullets. No hooks table — name the concept and link the Foreplay board in one line.
6. (Priorities sit after the scorecard, item 1, **≤120 words each**. A priority longer than the account snapshot is the mode arguing with itself.)

Drops in Quick: ad breakdown `<details>` blocks, per-ad funnel map, full 4PI ad-by-ad table, creative diagnostics detail, hooks table, post-click audit (flag qualifying ads in one line), Audience Segments & NCPA card (NCPA and existing share stay in the snapshot table), seasonality card, industry benchmark card, promo post-mortems, systemic observations paragraph.

Both modes save the history JSON with a `"mode"` field. A Quick run still counts as the previous report for the next run's memory.

## Required section order

1. **Header band** — logo, brand, report title, "as of" date, date range, primary window, account currency. Plus, in the header: **(a) Account sentiment badge** — STRONG (green) / STEADY (blue) / AT RISK (amber) / DECLINING (red) with one plain-English sentence. **Sentiment measures money only** (Knowledge Base, "Account sentiment"); the sentence must state the money position, and the badge must agree with it — if they contradict, the badge is wrong. **(b) Watch flags line** — up to 3 structural items in neutral gray, prefixed "Watch:" (e.g. "no TOF feeder · 58% of spend on one ad"). Never styled as an alert: these are things to keep an eye on, not things going wrong. **(c) Meta platform status line** from metastatus.com; **(d)** macro-environment note if the window overlaps a calendar event (including the client's own sale or promo); **(e)** a targets chip stating the mode, e.g. "Target: $65 per new customer (LTV mode) · $21 per order shown for context", or "no target set" (add the CPL target when lead campaigns run); **(f)** the collapsed "How to read this report" glossary (Readability rules).
2. **Account scorecard** — KPI cards (purchase, CPA, AOV and profit cards cover purchase and catalog campaigns only; add a **Leads** card with CPL vs `target_cpl` when lead campaigns run): Total spend (7d, all campaigns), Purchases, Blended CPA vs `target_cpa` (only when one is set; never against `target_ncpa`), **NCPA** (account, with new-customer purchases and existing share as the sub-line; vs `target_ncpa` in `ltv`/`both` mode, where it's the highlighted card), Blended AOV, Profit/Order (pre-COGS, or GPT if CSV), directional ROAS. Small deltas vs 30d run-rate. When report memory exists, each KPI also shows its **delta vs the previous report** (arrow + value; for cost metrics down = green). When the Meta peer benchmark returned data, one line here ("Cost per result vs similar advertisers: X% better/worse — Meta peer benchmark, LAST_28D"). The industry-cohort benchmark gets its own card instead — see §3d.
2a. **Top 3 priorities**: directly after the scorecard, before any detail. Numbered, each with the specific number that justifies it, ≤150 words each, written as instructions ("Cut BAU to $100/day today", not "BAU may be over-funded"). The rest of the report is the evidence for these three.
2b. **"Since Last Report" card** (only when memory exists — `references/report-memory.md`): header "vs report of <date> (N days ago)" with the sentiment shift, then every previous recommendation with its verified verdict — ✔ Actioned (+ outcome number) / ✘ Not actioned (+ current cost of inaction) / ◐ Due later / ？ Can't verify — followed by one-line NEW ads (green NEW badge + launch date) and GONE/stopped ads ("stopped ✔ as recommended" where applicable). Verdicts come from the current pull, never assumption. First-run mode: replace this card with one line — "First tracked report — week-over-week comparison starts next run."
3. **Account snapshot**: one table across the three windows, the same as Quick (columns in "Report depth modes", item 3), sorted by 7-day spend (campaign sections use the same order). Active-ad counts and funnel-health strings are identical across windows, so three tables are duplication, not information; the analysis still cross-references all three windows. When a promo overlaps the window, add the promo split table underneath (clean baseline vs promo days).
3b. **Audience Segments & NCPA card** (Full mode; directly after the snapshot, before the Seasonality card):
   - **Title:** "AUDIENCE SEGMENTS & NCPA". **Setup status pill** beside it: OK (green) · PARTIAL (amber) · SUSPECT (amber) · NOT SET UP (red) · UNAVAILABLE (gray), with the one-line evidence and "confirm in Ads Manager" on any non-OK status.
   - **One table per sales campaign** (30d, plus the pre-event baseline when a promo overlaps): `Segment | Spend | % of spend | Purchases | CPA | Reach | Frequency` for New · Engaged · Existing (+ Unknown when > 1% of spend), then a bold row: **NCPA = spend ÷ new + engaged purchases**, with the new-segment CPA in small text.
   - **Account NCPA row** (and the fully loaded variant when non-purchase campaigns are ≥ 5% of spend) against `target_ncpa`, with a pass/fail mark in `ltv`/`both` mode.
   - **Shopify line** when the cross-check ran: "Shopify: X new / Y returning customers (Z% returning) · Meta NCPA floor $N". When it didn't, one line saying why ("no Shopify connector on this store" / "connector is on another store").
   - **Flags** as small callouts: existing over-serving (with both frequencies), SUSPECT list, promo-window shift. Each carries the number that triggered it.
   - **Close** with one plain sentence on what NCPA means for the target, e.g. "NCPA $47 against a $65 LTV target: acquisition is inside target; the issue is the 17% of spend recycling 1,507 existing customers at frequency 45."
   - NOT SET UP or UNAVAILABLE: the card shrinks to the status pill, the evidence line and the fix.

3c. **Seasonality vs Last Year card** — under the snapshot, after the Audience Segments & NCPA card (§3b) when that card is rendered. Compact comparison of the 30d window (and MTD) against the same calendar dates one year earlier, account level: a small table or chip row per metric — `Spend · CPM · CPA · Purchases` — showing this year, last year, and the % delta, **CPM visually leading** (it's the seasonality signal; the KB "Year-over-Year Seasonality Check" section has the trust levels). End with one plain-English sentence: e.g. "CPM is +32% vs this time last year — the market is pricier, not the creative worse" or "CPM flat YoY — this month's CPA rise is ours, not seasonal." If the YoY CPM gap ≥ ~20%, also surface it in the header macro chip. No year-ago data → replace the card with one line ("account has no data for this period last year — seasonality check unavailable").
3d. **Industry Benchmark card** (when cohort data was fetched — directly after the Seasonality card). Fixed layout; keep it exactly this simple:
   - **Title:** "INDUSTRY BENCHMARK — <VERTICAL> (META)". **Never name the data provider anywhere in the report** — refer only to "the cohort" / "other <vertical> brands running Meta".
   - **Subtitle**, one line: "Your ROAS against other <vertical> brands running Meta. ROAS only — reasons below the chart."
   - **Percentile band graphic:** a horizontal bar in three tones (light gray → pale green → brand green), tick markers labelled p25 / median / p75 with the cohort values beneath each, "better →" right-aligned. Pure CSS.
   - **Explainer strip** in plain language: "p25 — a quarter of brands fall below this line. p75 — three quarters fall below it, so clearing p75 puts you in the top quarter."
   - **Table:** `Campaign | 30D ROAS | Quarter`. One row per campaign with meaningful 30d data, plus an **ACCOUNT** row (bold) for the blended figure. Paused campaigns included with a gray "paused" note. Quarter pill per row: **Top quarter** (green, > p75) · **3rd quarter** (amber, median–p75) · **2nd quarter — below median** (red, p25–median) · **Bottom quarter** (red, < p25).
   - **"Why ROAS only" section**, three bullets, adapted to the actual currencies: (1) *Currency* — "This report is <CUR>. The cohort is USD. Cost figures are not comparable, and nothing here has been converted." (2) *Order value* — the cohort blends every AOV band; a CPA that works on a US$500 basket is fatal on a <CUR>150 one. (3) *ROAS is a ratio, so it carries no currency — the one clean comparison available.* **Exception:** if the account currency IS USD, CPM and CPA rows may be added to the band/table — the AOV-blend caveat still applies and stays in the bullets.
   - **Closing line:** "**Read it as context, not a verdict.**" + one sentence connecting to the 4PI read (e.g. "X being the only campaign below the cohort median is an outside dataset agreeing with the 4PI read. Nothing here changes a recommendation in this report — a healthy ROAS percentile says nothing about a funnel with no TOF feeder.").
4. **Per-campaign sections** (sorted by 7-day spend, descending). Lead gen and catalog campaigns use their own layouts (`references/campaign-types.md`). Purchase campaigns, each:
   - **Campaign stat grid — never a run-on "·"-separated line.** Render the campaign header numbers as a grid of small labelled stat cells (same `.kpis`/`.kpi` pattern as the account scorecard, smaller). One number per cell, label above, context below. Cells: Spend 7d (with 30d below) · Budget/day (with actual pacing below) · Purchases 7d · Blended CPA (vs `target_cpa` only, never `target_ncpa`) · **NCPA** (vs `target_ncpa` in `ltv`/`both` mode; existing share of purchases as the sub-line) · AOV · Profit/Order · ROAS directional · CPM range (low–med–high as the sub-line) · Ads (active / testing / stopped as the sub-line). A reader should get the campaign's state in one glance without parsing a sentence.
   - **Funnel map table**: `Ad | Funnel | Daily Freq | Spend Share | CPM | Daily Spend Trend` + funnel-gap verdict line. **Every ad carries a creative-format badge** (VIDEO dark / STATIC light / CAROUSEL) next to its name, sourced from `ads_get_creatives` (`video_id` → video; `object_type` SHARE/PHOTO → static; CAROUSEL → carousel; name keywords as last resort). The legend line includes the format badges with the reminder to **compare CPM within format** — video inventory prices higher than static, so a $15 video and an $11 static can be equally cheap; never read a static-vs-video CPM gap as a performance signal.
   - **4PI table**: `Ad | Status | Action | Spend 7d | % Camp | CPM (with trend arrow) | Daily Freq | Funnel | CPA 7d | CPA 30d | Profit/Order`. Status (Active / Stopped / Winding down) stays, so nobody is told to stop an ad that's already stopped. In Full mode, when the ad-level segment pull ran, add `New 30d` (share of the ad's purchases from new or engaged buyers: context for the funnel decoder; it never changes the label). Insufficient data already says the data bar wasn't met, and AOV lives in the breakdown chip row, so neither gets a column.
   - **Ad breakdowns** (collapsible `<details>` per ad, only for ads with a decision attached: Keep, Hold, Fix, Watch, Stop, Scalable; thin ads are collapsed per the Readability rules) — structured, not a bullet dump:
     * `<summary>`: ad name + action pill + one-line verdict
     * **Chip row**: small stat chips (Spend · % of campaign · CPM · Daily freq · CPA · AOV · P/Order · ROAS) — scannable at a glance. When memory has this ad id, append "was $X" to the CPA and Spend chips ("CPA $22.56 · was $43.93 ✔"); ads not in memory get a green NEW badge in the summary line.
     * **Three labelled mini-blocks** in a 3-column grid (stack on mobile):
       - *Delivery* — status, learning status, creative type, last-5-days spend trajectory, freq & CPM trend arrows
       - *Economics* — purchases, CPA vs peers/target, AOV, profit/order, attribution or repeat-purchase flags
       - *Creative* — hook / hold / link CTR vs thresholds, drop-off note
     * **The read** — 1–2 plain-English sentences: what Facebook is doing with this ad and why the action label follows. This is the only prose; everything else is chips and labelled values.
   - **Campaign diagnosis**: Direction (up/down/flat 7d vs 30d) · Funnel health & gap · Profitability · Risk ("what breaks in 7 days if nothing changes")
   - **Scaling verdict card** (active campaigns only): the SCALE +10–20% / HOLD / TRIM −10–20% verdict as a prominent badge, followed by the condition checklist with ✓/✗ marks (see Knowledge Base "Budget Scaling Verdict"). A HOLD states what unlocks the next move and the date to re-check.
   - **Campaign next steps** — every recommendation grounded in and citing: current account data, brand intelligence/personas, customer reviews (quote real language), best practice (format tendencies), and the Ad Concept Board (Foreplay link). Structure: 1) Next creative to test — gap it solves, concept, why, persona + angle, format, success signal, **plus a 3–5 hook table generated per `references/hook-generator.md`** when the recommendation is a creative test (purchase campaigns; lead and catalog follow `references/campaign-types.md`). 2) Budget recommendation with numbers. 3) Ads to act on now.
5. **Post-click audit** (Full mode; ~400 words — see `references/post-click-audit.md` "Writing the section"): verdict first, then the four-step decomposition table (click→page · page→cart · cart→buy · purchases/click, per ad + campaign row), the spread sentence that proves where the leak is, then each real finding with its numbers and a fix from the ladder (copy → reorder → section → advertorial/listicle → dedicated lander → quiz). Unconfirmed items get one "verify" line. Never print the diagnostic pattern table itself — that's method, not findings.
6. **Systemic observations** (the Top 3 priorities moved to 2a): one short paragraph each on cross-campaign patterns, repeat-purchase bias, attribution concerns and profitability concerns, only where there's something to say. Include Meta anomaly signals / opportunity score notes here if pulled.
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
    {{SENTIMENT_BADGE_AND_SENTENCE}} {{WATCH_LINE}} {{STATUS_MACRO_TARGET_CHIPS}}
    <details class="glossary"><summary>How to read this report</summary> ... one line per term ... </details>
  </header>
  <section class="kpis"> ... KPI cards ... </section>
  <section class="card"><h2>Top 3 Priorities</h2> ... </section>
  <section class="card"><h2>Since Last Report</h2> ... </section>  <!-- or the first-run line -->
  <section class="card"><h2>Account Snapshot</h2> ... one table across 7d / MTD / 30d (class="stack") ... </section>
  <section class="card"><h2>Audience Segments &amp; NCPA</h2> ... </section>  <!-- Full -->
  <section class="card"><h2>Seasonality vs Last Year</h2> ... </section>    <!-- Full -->
  <!-- per campaign, by 7-day spend; layout by type -->
  <section class="card">
    <h2>{{CAMPAIGN NAME}}</h2>
    ... stat grid, funnel map, 4PI table (purchase) | lead or catalog layout ...
    <details><summary>{{AD NAME}} — full breakdown</summary> ... </details>  <!-- ads with a decision only -->
    <details><summary>Too early to read: {{N}} ads</summary> ... compact table ... </details>
    <h3>Diagnosis</h3> ... <h3>Scaling verdict</h3> ... <h3>Next steps</h3> ...
  </section>
  <section class="card"><h2>Post-Click Audit</h2> ... </section>  <!-- Full, if run -->
  <section class="card"><h2>Systemic Observations</h2> ... </section>
  <footer><p>Generated {{DATE}} · 4PI framework · Profit/Order is pre-COGS (AOV − CPA){{OR_GPT_NOTE}}</p></footer>
</div>
</body>
</html>
```

Adapt freely within the brand variables — the section order and data-integrity rules are fixed; the aesthetics flex with the client.
