# The CS brief findings file

`build_cs_brief.py` takes one JSON file and renders the page. Every block is optional:
leave one out and that section does not appear.

```jsonc
{
  "brand": "Acme Coffee",
  "for_date": "2026-10-12",
  "generated_at": "2026-10-12 09:00",

  // The only thing on the page with real visual weight. Green when holding, red when not.
  "promise": {
    "holding": false,
    "headline": "Nothing has shipped for 3 days. Do not promise 1 to 2 day dispatch today.",
    "detail": "Why, in one or two sentences. The batch pattern, the gap, what it means."
  },

  // below_threshold true renders it muted, for when there are too few signals to read.
  "sentiment": {
    "below_threshold": true,
    "read": "Only 4 signals this week. Too little to call a trend.",
    "why": "What those signals were."
  },

  // Pass "hours" as a number rather than a formatted string, so every age on the
  // page uses the same format. Hand-writing "92 hrs" into a label is how the stat
  // row and the table end up disagreeing about the same order.
  "stats": [
    {"label": "Waiting to ship", "value": "24", "sub": "$1,556 of orders"},
    {"label": "Oldest", "hours": 92, "sub": "#1038, since 8 Oct"}
  ],

  "about_to_complain": {
    "note": "Past 72 hours and none of them have written in yet.",
    "orders": [{"name": "#1038", "customer": "J. Smith", "hours": 92,
                "value": 36.90, "admin_url": "https://admin.shopify.com/store/<handle>/orders/<id>"}],
    "all_clear": "Shown instead when orders is empty."
  },

  "inbox": {
    "note": "Include the filtered-as-noise count here.",
    "threads": [{"who": "J. Smith", "about": "What they want, in a few words",
                 "category": "order-status", "hours": 88,
                 "also_overdue": true, "url": "https://mail.google.com/..."}],
    "all_clear": "Shown instead when threads is empty."
  },

  "housekeeping": ["Zero-value orders, old test orders, anything excluded from the figures."]
}
```

`also_overdue` on a thread puts a red pill beside the name. Use it when that person is
both waiting on a reply **and** has an overdue order, because they go to the top of the
queue and their reply needs the dispatch reality rather than the policy.

Admin URLs are built per `references/linking-to-shopify.md`. The handle is the myshopify
subdomain, not the storefront domain, and the id is the tail of the gid.
