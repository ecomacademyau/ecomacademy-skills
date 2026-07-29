# Report Memory — Week-over-Week Continuity & Accountability

Each report is no longer a snapshot: it opens against the previous one. Memory turns "here's this week" into "here's what changed, what we recommended, whether it was actioned, and what happened next" — the accountability loop that proves the work over time.

## Where memory lives

Installed skills are read-only, so state lives **next to the reports**, in two redundant places:

1. **`4pi-history-<brand-slug>.json`** — written to the same outputs folder as the report, every run.
2. **Embedded in the report itself** — the same JSON inside the report HTML as `<script type="application/json" id="fpi-history">…</script>` just before `</body>`. The report file IS a backup of its own state.

## At the START of every run (after Step 0, before pulling)

1. Look for the most recent `4pi-history-<brand-slug>*.json` in the outputs/working folder (Glob).
2. If none: look for the most recent `4pi-report-<brand-slug>-*.html` and read the embedded `fpi-history` block.
3. If neither: ask the user once — "Do you have the last report file to compare against?" If not, run in **first-run mode**: the report says "First tracked report — week-over-week comparison starts next run." Never fabricate a baseline.

## History schema (write exactly this shape)

```json
{
  "schema": 1,
  "brand": "j-walk",
  "report_date": "2026-07-12",
  "generated": "2026-07-13",
  "mode": "full",
  "currency": "AUD",
  "sentiment": "STRONG",
  "account": {"spend_7d": 538.62, "purchases_7d": 28, "cpa_7d": 19.24, "aov_7d": 49.16, "ppo_7d": 29.92},
  "campaigns": [
    {"id": "…", "name": "…", "status": "active", "scaling_verdict": "HOLD",
     "spend_7d": 523.97, "cpa_7d": 19.41, "ppo_7d": 31.03, "funnel_gap": "TOF forming"}
  ],
  "ads": [
    {"id": "…", "name": "…", "campaign_id": "…", "format": "video",
     "action": "Watch", "status": "ACTIVE", "spend_7d": 175.70, "cpa_7d": 43.93,
     "daily_freq": 1.45, "ppo_7d": 6.14}
  ],
  "recommendations": [
    {"id": "r1", "type": "creative_test", "text": "Brief teen-voiced Problem→Solution 9:16", "due": null},
    {"id": "r2", "type": "review_ad", "text": "Re-read TEST#14 at 7-day bar", "due": "2026-07-16"},
    {"id": "r3", "type": "budget", "text": "HOLD $70/day; +10–20% if TEST#14 confirms", "due": "2026-07-16"}
  ]
}
```

`type` ∈ stop | budget | creative_test | landing_page | review_ad | config | other. Keep `text` short and verifiable.

## At REPORT time (what memory adds to the report)

1. **Header delta chip row** — "vs last report (N days ago)": CPA Δ, Profit/Order Δ, spend Δ, sentiment shift (e.g. "AT RISK → STRONG"). Green/red per direction (remember: for CPA, down is green).
2. **"Since Last Report" card** — first card after the account scorecard. For each previous recommendation, a verdict verified **from the current pull, never from assumption**:
   - ✔ **Actioned** — with the outcome number ("Stop TEST#13 → stopped 14 Jul; campaign CPA since: $18.90")
   - ✘ **Not actioned** — with the current cost of inaction, stated plainly, no scolding
   - ◐ **Due later** — not yet at its due date
   - ？ **Can't verify** — say what data would settle it. Never guess.
   How to verify: stop recs → current `effective_status` of that ad id; budget recs → current `daily_budget` vs remembered; creative tests → any ad created after the last report date (match by `created_time`); review_ad → whether the ad now clears the data bar and what its numbers say.
3. **NEW / GONE badges** — ads present now but not in memory get a green **NEW** badge (with launch date); ads in memory but absent/stopped now are listed in one line ("since last report: TEST#13 stopped ✔ as recommended").
4. **Per-ad deltas** — in each ad's chip row, add "vs last report" to CPA and spend chips when the ad id matches memory (e.g. "CPA $22.56 · was $43.93 ✔").
5. **Trend continuity** — if the previous report flagged a danger (funnel drying, hero fatigue), open that campaign's section by resolving it: did it play out, stabilise, or reverse?

## At the END of every run

Write the new history JSON (file + embedded block). Tell the user in the chat summary that the history file rides along with the report — keep them in the same folder.

## Rules

- **Verify, never assume.** Every ✔/✘ verdict must be backed by the current pull. "Probably actioned" is a ？.
- **Memory never overrides fresh data.** It provides context and accountability, not numbers.
- **Missing memory is fine.** First-run mode is a complete, valid report — don't manufacture comparisons.
- **One previous report is enough.** Compare against the latest only; don't build multi-week charts from memory files unless the user asks (then read as many as exist).
- **Quick and Full runs are equal citizens.** Both write the full history schema (with `"mode"`); a Quick run is a valid baseline for the next comparison.
- Stale memory (>21 days old): still use it, but label the gap ("comparing to the report of 12 Jul — 4 weeks ago; treat deltas as directional").
