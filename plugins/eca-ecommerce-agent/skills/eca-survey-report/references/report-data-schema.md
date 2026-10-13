# Report data schema

One JSON file, rendered by `templates/report-template.html`. `scripts/build_report.py` calculates every percentage and signal tag from your counts, validates the file and builds the HTML. `examples/example-report-data.json` is a complete worked example.

**Supply raw counts only.** Never write percentages or signal tags; the build script adds them and overwrites anything you put there. Text fields are plain text (no HTML). No em dashes.

Required: `meta`, `snapshot`, `objections`, `objection_cards`, `actions`, `method`. Everything else is optional and skipped if absent.

## The question object

Used by every chart. `all` is the all-time count, `period` this period's count.

```json
{
  "label": "Question 3",
  "q": "What almost stopped you from buying today?",
  "type": "single",
  "n_all": 291,
  "n_period": 88,
  "rows": [
    {"label": "Couldn't smell it online", "all": 101, "period": 27},
    {"label": "Nothing, it was an easy yes", "all": 66, "period": 22, "frictionless": true}
  ],
  "note": "optional caveat"
}
```
- `type`: `single`, `multi` (shares add to more than 100%) or `open` (rows are themes you bucketed from written answers; say so in `note`).
- Order rows by all-time count, with "Other" last.
- Mark the "Nothing, it was an easy yes" style answer with `"frictionless": true` on the objection question.
- If you only have all-time (for example a new question), omit `period` and `n_period`.

## meta
```json
{"brand": "Hollow Oak", "report_title": "Customers want to smell it before they buy", "accent_word": "smell it",
 "period_label": "September 2026", "alltime_label": "since launch on 1 June 2026",
 "source": "Zigpoll MCP", "generated": "2026-10-01", "skill_version": "2.0.0",
 "market_spelling": "AU"}
```

## snapshot
```json
{"intro": "one or two sentences: the headline story",
 "metrics": [{"label": "New customer answers", "value": "291", "sub": "88 this period"}],
 "note": "bases and definitions"}
```
4 to 6 metrics. Typical: answers (new, returning), top reason to buy, top objection, top channel, share who found it an easy yes. Values are text you write from the built numbers; keep them consistent with the charts.

## last_actions (optional, from the previous report's history block)
```json
{"items": [{"status": "done|not_done|unknown", "text": "...", "note": "..."}]}
```

## insights
`[{"title": "...", "body": "...", "action": "...", "source": "..."}]` (6 to 8)

## motivation
A question object for the main reason to buy.

## angles
`[{"angle": "...", "why": "...", "hooks": ["...", "..."], "best_for": "...", "source": "..."}]`

## objections
The question object for the main objection question (required).

## objection_cards (required)
```json
[{"theme": "Couldn't smell it online", "row_label": "Couldn't smell it online",
  "summary": "...",
  "why": {"q": "What made the scent hard to judge?", "type": "multi", "n_all": 85, "rows": [{"label": "...", "all": 39}]},
  "quotes": ["...", "..."],
  "counters": {"website": "...", "ads": ["hook", "hook"], "content": "...", "email": "..."},
  "source": "..."}]
```
`row_label` must match a row label in `objections` exactly; the build script pulls its share and tag from there.

## smaller_objections (optional)
One line of text for objections under 5 all-time answers.

## attribution
A question object plus `"comment": "..."` (the platform comparison note).

## audience (optional)
```json
{"who_for": {question object}, "problem": {question object, type "open"},
 "personas": [{"name": "...", "share": "...", "who": "...", "wants": "...", "worries": "...", "angle": "...", "source": "..."}]}
```

## products (optional)
```json
{"title": "...", "n": 280, "rows": [{"label": "Signature candles", "count": 138}], "note": "inference caveat",
 "objection_mix": {"cols": ["Scent", "Price"], "rows": [{"label": "Signature candles", "n": 138, "cells": [52, 18]}], "neutral_cols": [], "comment": "..."}}
```
All-time. Lines under 30 baskets are shaded out automatically.

## returning (optional)
```json
{"questions": [question objects], "comparison": {"q": "Who are you buying for today?", "rows": [{"label": "A gift", "new": 92, "new_n": 291, "ret": 41, "ret_n": 110}]},
 "moves": [{"title": "...", "body": "...", "source": "..."}]}
```

## other_questions (optional)
Question objects for any survey question not covered above.

## shifts_comment (optional)
One or two sentences about what is new this period. The shift list itself is calculated by the build script from every question object.

## actions (required)
```json
{"this_week": [{"channel": "Website", "title": "...", "body": "...", "source": "..."}],
 "this_month": [...], "test_next": [...]}
```
`channel`: Website, Ads, Content, Email or Product. Maximum 3 items in `this_week`.

## language_bank
`[{"theme": "...", "phrases": ["...", "..."]}]`

## questions_to_consider (optional)
`["..."]`

## method
Plain text; `\n\n` starts a new paragraph.

## history
```json
{"schema": 2, "brand": "slug", "period": "2026-09", "generated": "2026-10-01",
 "objection_shares_all": {}, "motivation_shares_all": {},
 "actions": [{"id": "a1", "channel": "Website", "text": "..."}]}
```
Write shares from the built report if you want them in history; the next run uses `actions` to fill `last_actions`.
