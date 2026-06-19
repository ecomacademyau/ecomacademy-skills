# Brand Intelligence — a reusable Claude skill

A Claude skill that loads a brand's full identity into context before Claude writes copy, content, or strategic suggestions — and, when no profile exists yet, **builds that identity from the store URL**: crawling the site, running market and competitor research, and mining reviews for why people buy.

It's brand-agnostic by design: point the skill at any store URL and it builds that brand's profile from scratch, or drop in a pre-filled `brand-data.md`. Everything brand-specific lives in that one file.

## What's in the folder

```
brand-intelligence/
├── SKILL.md                          # Generic logic — two modes: Build and Apply. Same for every brand.
├── brand-data.md                     # Your brand's data — a placeholder until you build it (point the skill at your URL) or fill the template.
├── README.md                         # This file.
├── templates/
│   └── brand-data-template.md        # The full schema — 19 sections — used both as a fork scaffold and as the spec the Build mode fills.
└── references/
    └── market-research.md            # Forum-first voice-of-customer + market pain-point research method, and the trainable report structure.
```

## How it works — two modes

The skill always runs **Step 0** first to read `brand-data.md` and decide which mode applies:

- **Mode A — Build.** If `brand-data.md` is missing or mostly placeholders, the skill builds it. It asks for the store URL, then: crawls the homepage/about/product/FAQ/review pages (using the Shopify and reviews MCPs if connected), mines reviews for the before→after transformation and buying motivation, and runs **deep voice-of-customer research** — forum-first (Reddit, Quora, niche forums) plus competitor reviews (Amazon, Trustpilot, ProductReview), X, and Medium — to surface real pain points, why current solutions fail, and what consumers actually want (method in `references/market-research.md`). It also runs market-sizing and competitor desk research (Semrush for SEO territory if available). The build **outputs a standalone, trainable market-research report** alongside the profile, and drafts all 19 sections from the template. Anything it can't verify is flagged as a gap — it never invents brand facts. **The build is collaborative, not autonomous:** it stops at two mandatory checkpoints — **Gate 1** (you agree the positioning/direction and key assumptions before it drafts) and **Gate 2** (you sign off the finished profile and answer the founder-only questions before it saves).
- **Mode B — Apply.** If the file is filled, the skill loads it and grounds every output in the brand's real story, voice, products, offers, proof, objections, competitors, and customer.

`SKILL.md` is brand-agnostic. `brand-data.md` is brand-specific. That separation is the whole point of the design.

## What the brand profile captures (19 sections)

Brand essence · Why people buy & the transformation · Voice & tone · Visual identity / style guide · Messaging pillars / angle bank · Products · Offer & pricing strategy · Proof & credibility · Objections → rebuttals · Market · Competitors · ICP & personas · Operational facts & how-to-use · Promotional calendar & seasonality · SEO / content territory · Boilerplate · Channels · Sources & confidence · Open questions.

Each section names the downstream skills that consume it, so nothing is in the file that no one reads.

## When this skill triggers

- Writing/editing marketing copy, product descriptions, ad creative, email, SMS, social, landing pages, blog
- FAQ and customer-service replies
- Positioning, value-prop, and opportunity-evaluation work
- "Is this on-brand?", "who's our customer?", "who are our competitors?", "build our brand profile from our website"

It deliberately does *not* trigger on generic ecommerce questions ("what's a good subject-line length?") — those don't need brand context.

## How to use this skill for a different brand

1. **Fork the folder.** Copy `brand-intelligence/` somewhere new — rename it (e.g., `brand-intelligence-acme/`) if you want both available, or replace the contents in place.
2. **Delete the old `brand-data.md`** (or replace it with `templates/brand-data-template.md`).
3. **Invoke the skill with the new store URL.** Mode A builds the file from scratch. Or fill `brand-data.md` by hand from the template if you'd rather.
4. **Update the skill name if needed.** To run multiple brand-intelligence skills side by side, edit the `name:` field in `SKILL.md`'s frontmatter and rename the folder to match.
5. **Don't change `SKILL.md`'s body unless you're improving the generic logic.** It's meant to work for any brand.

## How to keep it current

`brand-data.md` decays. Trigger an update on: product/price changes, new campaigns or repositioning, competitor moves, fresh customer research, or a visual refresh. Section 18 (Sources & confidence) records when each section was last verified — a good quarterly review anchor. To refresh against reality, ask Claude to "audit `brand-data.md` against the current Shopify catalog and the live site" and flag what's stale.

## Limitations

Mode A researches and drafts from real sources — it does not fabricate a brand with no online presence or founder input. Mode B applies the brand; the richer `brand-data.md` is, the better every downstream asset gets. Time invested in the profile compounds across all future work.
