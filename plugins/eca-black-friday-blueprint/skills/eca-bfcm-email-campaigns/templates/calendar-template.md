# Calendar slot data (feeds the calendar-grid canvas)

This table is the **underlying data**, not the member-facing deliverable — the actual presentation is the calendar-grid canvas built via the `design` skill, per `references/calendar-grid-format.md`. Build this table first (in chat, so it's fast to iterate on) to nail down every slot, then render it into the canvas. Fill every row; don't leave a topic as a generic label from the topic bank without naming the real offer/product.

If the `design` skill isn't available in the session for some reason, this table becomes the fallback deliverable — tell the member plainly that's what's happening rather than silently downgrading from the calendar-grid format.

| # | Send date | Phase ID | Type | Topic | Segment | Source | Notes |
|---|---|---|---|---|---|---|
| 1 | [date] | EARLY_ACCESS | Hero | [specific topic] | [named Klaviyo segment] | New | [why this slot, this topic] |
| 2 | [date] | SALE_LIVE | Product | [specific topic] | [named Klaviyo segment] | Resend candidate: [past email name, e.g. "+34% CTR vs campaign avg"] | ... |
| ... | | | | | | | |

**Phase ID** comes from `bfcm/bfcm-<year>-calendar.csv` and is required on every row — it is what the runsheet append in Stage 5.5 uses, and what keeps the plan correct when dates move.

**Segment** is a named Klaviyo segment, never a raw profile count.

**Type** is one of: Hero / Product / Education / Plain text (see `references/content-ratios.md` and `references/wireframe-layouts.md`).

**Source** is one of:
- `New` — a fresh topic from the topic bank or the member's own idea.
- `Resend candidate: [name + one metric]` — a real past email surfaced from Klaviyo in Stage 3, worth tweaking for this offer. Always cite the metric that earned it the slot (e.g. open rate, click rate, revenue per recipient vs. campaign average) so the member can see why it's suggested, not just that it is.

After the table, show the ratio check: how many of each Type the calendar actually has, against the target split, so the member can see at a glance whether it's on-ratio or intentionally off (and why).

Ask directly: *"Happy with this shape, or is there anything you want to swap out?"* — don't move to drafting individual emails until the member has actively signed off on the calendar, not just gone quiet.
