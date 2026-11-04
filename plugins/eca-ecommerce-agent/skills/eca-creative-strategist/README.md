# ECA Creative Strategist

Your dedicated Meta ads creative strategist. It reads your ad results, your customers' words and what competitors keep paying for, decides what to test next and why, then writes video scripts and a creator brief someone can film this week.

Ships in the ECA Marketing Coworker plugin as **`eca-creative-strategist`**. It replaces `eca-ugc-scripts` (its founder story, 3 reasons why and comment reply frameworks live on inside it).

## What you get

- **A strategy page**: the job for this round (feed the top, build a closer, iterate a winner...), 3 angles with the evidence behind each, the format, who films, how long. You approve it.
- **Hooks first**: 3 to 5 per angle across different hook types, each with what to say, what to show and the on-screen text.
- **Scripts**: talking points to learn, a sample script as a guide, shots, length, a scorecard, ad names, draft ad copy.
- **A creator brief** (HTML, prints to PDF) that's clean to send: no metrics, no internal notes.
- **A creative log** in `./brand/creative-log.md` so every round learns from the last.

Just need something to film today? Ask for it. Quick mode skips the strategy pack and gives you the scripts.

## What it reads

| Source | How | Needed? |
|---|---|---|
| `brand-data.md` | From eca-brand-intelligence | Strongly recommended |
| Ad results | Meta Ads MCP, an Ads Manager CSV, or a recent 4PI report | Recommended |
| Reviews, survey answers | CSV exports or an eca-survey-report | Recommended |
| Competitor ads | Meta Ads MCP, a teardown, or ads you describe | Optional |

No MCPs needed: a CSV export and a reviews export are enough for a full round.

## Folder

```
eca-creative-strategist/
├── SKILL.md                    the flow: intake > account read > customer voice > patterns > strategy > hooks > scripts > QA > hand over > learn
├── references/                 one file per step, plus formats/ (yapper, demo, founder story, 3 reasons, comment reply, us vs them, testimonial, unboxing)
├── scripts/
│   ├── creative_read.py        creative read of an Ads Manager CSV (same thresholds as 4PI)
│   ├── check_copy.py           copy lint: em dashes, slop, fake urgency, personal attributes, US spelling, timing
│   └── build_brief.py          creator brief from JSON to HTML/PDF
└── assets/                     strategy pack, quick scripts, creative log templates, brief example
```

## Rules it never breaks

No invented facts, reviews, stats or names (`[CONFIRM]` instead). Read-only on ad accounts. No fake urgency. Brand said once, at the end. Compliance checked against Meta's rules and Australian consumer law (ACCC, TGA, FSANZ).
