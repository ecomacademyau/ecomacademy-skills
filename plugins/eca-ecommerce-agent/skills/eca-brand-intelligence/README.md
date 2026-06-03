# Brand Intelligence — a reusable Claude skill

A Claude skill that loads a brand's full identity (story, market, competitors, products, voice, visual identity, ICP) into context before Claude writes copy, content, or strategic suggestions.

This version is a working template. Fill it in for your brand by swapping `brand-data.md`.

## What's in the folder

```
brand-intelligence/
├── SKILL.md                          # Generic logic — how Claude uses brand context. Same for every brand.
├── brand-data.md                     # Brand-specific data. SWAP THIS to use for a different brand.
├── README.md                         # This file.
└── templates/
    └── brand-data-template.md        # Blank scaffold for a new brand.
```

## How it works

When the skill triggers (e.g., Claude is asked to write copy, evaluate positioning, or answer a brand question), Claude reads `SKILL.md`, which instructs it to immediately read `brand-data.md`. Every subsequent output is grounded in the brand's real story, voice, products, competitors, and customer — not generic best-practice.

`SKILL.md` is brand-agnostic. `brand-data.md` is brand-specific. That separation is the whole point of the design.

## When this skill triggers

The skill's description in `SKILL.md` is written to trigger on:
- Writing/editing marketing copy, product descriptions, ad creative
- Email, SMS, social posts, landing pages, blog content
- FAQ and customer service replies
- Positioning, value-prop, and opportunity-evaluation work
- Questions like "is this on-brand?", "who's our customer?", "who are our competitors?"

It deliberately does *not* trigger on generic ecommerce questions ("what's a good email subject line length?") because those don't need brand context.

## How to use this skill for a different brand

1. **Fork the folder.** Copy `brand-intelligence/` somewhere new — either rename it (e.g., `brand-intelligence-acme/`) if you want both available, or replace the contents in place.
2. **Copy the template.** `cp templates/brand-data-template.md brand-data.md` (replacing the existing one).
3. **Fill it in.** Work through each section of `brand-data.md`. The headings are deliberate — every section earns its keep. If a section genuinely doesn't apply, leave a note saying so rather than deleting it.
4. **Update the skill name if needed.** If you want multiple brand-intelligence skills installed side-by-side (e.g., agency context), edit the `name:` field in `SKILL.md`'s frontmatter and rename the folder to match.
5. **Don't change `SKILL.md`'s body unless you're improving the generic logic.** That file is meant to work for any brand.

## How to keep it current

`brand-data.md` decays. Things that should trigger an update:
- Product lineup changes (new SKU, price change, discontinued line)
- New campaign or repositioning
- Competitor moves (a new entrant, big launch, repositioning)
- New customer research (segment data, persona shifts)
- Visual identity refresh
- Annual review (set a recurring reminder)

A good pattern: tag this file as a quarterly review item on the founder/marketing lead's calendar.

## Validation pattern

If you want Claude to fact-check the brand data against current reality, ask it to "audit `brand-data.md` against your live store / public site" — it can pull live product data and the public site, then flag where the file is out of date.

## Limitations

This skill *applies* the brand. It doesn't *invent* it. If `brand-data.md` is thin, Claude will produce on-brief-but-shallow output. Time invested in filling out `brand-data.md` compounds across every future piece of work.
