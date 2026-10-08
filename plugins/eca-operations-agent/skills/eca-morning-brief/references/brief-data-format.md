# The findings file

`build_brief.py` takes one JSON file and renders the page. Every section is optional:
leave a key out and that section does not appear. This is deliberate, so a missing
connector produces a brief that is honest about the gap rather than one showing zeros.

```jsonc
{
  "brand": "Acme Coffee",
  "for_date": "2026-10-08",        // the day being reported
  "run_date": "2026-10-09",        // the morning it was written
  "currency": "AUD",

  "summary": {
    "headline": "One sentence naming what happened and what it means.",
    "deck": "Two or three sentences with the specific numbers, including the awkward one.",
    "highlight_date": "2026-10-08",             // bar drawn dark
    "marker": {"date": "2026-10-03", "label": "3 Oct · both break"},  // omit if nothing real
    "stats": [{"label": "Yesterday", "value": "$436.83", "sub": "6 orders"}]
  },

  "trend": [{"date": "2026-09-25", "value": 951.73}],   // 14 days, today excluded

  "actions": [{
    "what": "Find out what happened to the ads on 3 October",
    "why": "Why it matters, with the number that makes the case.",
    "severity": "high",           // high | medium | low, sets the dot colour
    "source": "Ads",              // the tag on the right
    "buttons": [
      {"type": "claude", "label": "Investigate it", "prompt": "The full brief..."},
      {"type": "open",   "label": "Open Ads Manager", "url": "https://..."}
    ]
  }],

  "store":    {"note": "...", "metrics": [...], "top_products": [...]},
  "forecast": {"note": "...", "metrics": [...], "method": "How it was worked out."},
  "ads":      {"note": "...", "metrics": [...], "movers": [...]},
  "dispatch": {"note": "...", "metrics": [...], "orders": [...], "flags": ["..."]},
  "stock":    {"note": "...", "items": [...], "all_clear": "Shown when items is empty."},
  "inbox":    {"note": "...", "metrics": [...], "threads": [...]},
  "reviews":  {"metrics": [...], "items": [{"rating": 5, "product": "...", "snippet": "..."}]},

  "unavailable": [{"name": "Meta Ads", "reason": "What it would have told them."}]
}
```

A metric is `{label, value, change_pct, baseline_label}`. `change_pct` under 5% renders
grey and flat rather than coloured, so ordinary variance stops looking like news. Omit it
entirely and the card reads "no baseline", which is honest.

**Compute each figure once and reuse it.** An early version showed 7-day revenue as
$2,869 in the summary and $1,831.85 in the store card, from two different calculations of
the same thing. One contradiction like that and the reader stops trusting the page.
