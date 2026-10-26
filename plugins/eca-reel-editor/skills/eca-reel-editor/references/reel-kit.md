# Reel kit — the only questions the reel editor ever asks about the brand

Everything visual comes from `brand-data.md` §4 (colours, fonts, "never do visually"). Six things a brand file usually does not say are collected **once**, saved into §4 as a fenced ```reel-kit block, and synced to EcomOS. There is **no brand interview** in this skill: if the brand file is missing, stop and send the member to the brand-intelligence skill.

`python3 scripts/brand_from_eca.py` exits with code 3 and prints `{"gaps": [...], "suggested": {...}}` when something is missing. Ask **only** for the listed gaps, one question at a time, 2–4 concrete options each, with the suggested value as the default. Use AskUserQuestion where available. Then write `kit.json` and rerun `python3 scripts/brand_from_eca.py --kit kit.json`.

| key | question (plain words) | options → value |
|---|---|---|
| `captionMode` | How do you want captions? | one word at a time, big → `word` · short phrases near the bottom → `phrase` |
| `captionCase` | lowercase or Sentence case? | `lower` · `sentence` |
| `highlightColor` | Which colour for the key word in each caption? | the brand accent (default, show the hex) · another brand colour · `#hex` |
| `graphics` | How busy should the graphics be? | clean, one every 8–12 s → `minimal` · balanced, every 4–6 s → `balanced` (default) · busy, every 2–4 s → `busy` |
| `sfx` | Sound effects? | none → `none` · subtle whooshes at cuts → `subtle` (default) · pops and dings too → `lots` |
| `pacing` | How tight should the edit be? | natural, only long pauses and clear "um"s go → `natural` (default) · tight, 1.1×, most pauses go → `tight` · fast, 1.15× → `fast` |
| `cta` | What should every reel ask people to do? | e.g. "comment DOSE and I'll send the link", "tap the link in bio", "use code REEL10" |

Two more only when `gaps` lists them (the brand file has no usable palette or font):

| key | question | value |
|---|---|---|
| `colors` | Which hex codes are the brand's main (dark/text), accent (pop) and light (background) colours? Offer what the website uses if you can see it. | `{"ink": "#…", "accent": "#…", "light": "#…"}` |
| `fonts` | Which font for headlines, and which for body? (Google Fonts are free; a file in `./brand/fonts/` wins.) | `{"heading": "Poppins", "body": "Inter"}` |

## kit.json

```json
{
  "captionMode": "word",
  "captionCase": "lower",
  "highlightColor": "#E21B1B",
  "graphics": "balanced",
  "sfx": "subtle",
  "pacing": "natural",
  "cta": "comment DOSE and I'll send you the link"
}
```

## What gets written

`brand_from_eca.py --kit kit.json` appends this to the end of §4 of `brand-data.md` (or replaces an existing block), then builds `brand.json`:

````markdown
**Reel kit** (visual preferences for the ECA reel editor — edit here, then say "Sync my brand to EcomOS"):

```reel-kit
{ "captionMode": "word", "captionCase": "lower", "highlightColor": "#E21B1B", "graphics": "balanced", "sfx": "subtle", "pacing": "natural", "cta": "…" }
```
````

Then call the EcomOS `sync_brand` tool (via the brand-intelligence sync, `eca-brand-intelligence/references/ecomos-sync.md`) so the dashboard mirror carries `visual.reelKit`. If EcomOS is not connected, say so once and carry on.

## Later changes

When the member corrects something during an edit ("never outline captions", "always lowercase"), update the block (edit the JSON, rerun with `--kit`, or just rerun `brand_from_eca.py --force` after editing the file) — never a side file the next edit will not see.
