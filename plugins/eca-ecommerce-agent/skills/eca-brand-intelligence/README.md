# Brand Intelligence — a reusable Claude skill

A Claude skill that loads a brand's full identity into context before Claude writes copy, content, or strategic suggestions — and, when no profile exists yet, **builds that identity from the store URL**: crawling the site, running market and competitor research, and mining reviews for why people buy.

It's brand-agnostic by design: point the skill at any store URL and it builds that brand's profile from scratch.

**The finished brand is saved in the member's EcomOS**, section by section, over the `ecomos` MCP connection. That makes the brand independent of any one AI app, computer or folder: Claude, another AI app the member connects, and the Marketing Apps inside EcomOS all read the same brand, and the member can see and edit it in EcomOS → Business Brain. EcomOS is the source of truth: a copy is kept in the working folder (`./brand/brand-data.md`) when there is one, and whenever the two disagree the EcomOS version stands. Without an EcomOS connection the skill works exactly as before from that file.

## What's in the folder

```
brand-intelligence/
├── SKILL.md                          # Generic logic — two modes: Build and Apply. Same for every brand.
├── brand-data.md                     # Placeholder template only. The REAL brand lives in EcomOS, with a working copy in the member's folder: ./brand/brand-data.md
├── scripts/brand_sections.py         # Works out which sections to save to or pull from EcomOS, prints each section's text, checks completeness, builds the structured-brand payload
├── README.md                         # This file.
├── templates/
│   └── brand-data-template.md        # The full schema — 19 sections — used both as a fork scaffold and as the spec the Build mode fills.
└── references/
    ├── market-research.md            # Forum-first voice-of-customer + market pain-point research method, and the trainable report structure.
    ├── brand-file-location.md        # Where the brand lives: EcomOS first, then the working copy's lookup order
    ├── ecomos-sync.md                # Saving the brand to EcomOS (put_context per section + sync_brand) and reading it back (get_context)
    └── brand-sync-schema.json        # The JSON Schema the structured brand must match (exported from EcomOS)
```

## How it works — two modes

The skill always runs **Step 0** first: it looks for the brand in EcomOS, then for a working copy, and decides which mode applies. A filled local file that has never been saved to EcomOS is saved there at this point (the file stays where it is).

- **Mode A — Build.** If there is no brand profile, or it is mostly placeholders, the skill builds it. It first **recommends the connectors that make the build valuable** (Shopify, Klaviyo, a reviews app, the Claude in Chrome extension + desktop app, Semrush — see `references/connectors.md`), then asks for the store URL, then: crawls the homepage/about/product/FAQ/review pages (using the Shopify and reviews MCPs if connected), mines reviews for the before→after transformation and buying motivation, and runs **deep voice-of-customer research** — forum-first (Reddit, Quora, niche forums) plus competitor reviews (Amazon, Trustpilot, ProductReview), X, and Medium — to surface real pain points, why current solutions fail, and what consumers actually want (method in `references/market-research.md`). It also runs market-sizing and competitor desk research (Semrush for SEO territory if available). The build **outputs a standalone, trainable market-research report** alongside the profile, and drafts all 19 sections from the template. Anything it can't verify is flagged as a gap — it never invents brand facts. **The build is collaborative, not autonomous:** it stops at two mandatory checkpoints — **Gate 1** (you agree the positioning/direction and key assumptions before it drafts) and **Gate 2** (you sign off the finished profile and answer the founder-only questions before it saves). After sign-off every section, the research report and the structured brand are saved to EcomOS, each section with a short brief so other skills can load the brand without loading all of it.
- **Mode C — Deepen.** EcomOS scores how much it knows about the business (Brain depth, out of 100, five levels) and lists the questions still open. Say "Help me fill my Business Brain" and the skill talks you through them one question at a time, suggesting answers from what your store, reviews and Brain already show so you pick, tweak or say it your own way. Each answer is written into the right section as you go and the score moves with it. The same questions can be answered directly on the Business Brain page in EcomOS.
- **Mode B — Apply.** If the brand exists, the skill loads what the task needs — from EcomOS, only the sections that task uses, as briefs first — and grounds every output in the brand's real story, voice, products, offers, proof, objections, competitors, and customer. Corrections the member makes along the way are saved back to the section they belong to.

`SKILL.md` is brand-agnostic. The brand profile is brand-specific. That separation is the whole point of the design.

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

The brand belongs to the EcomOS business the member connected, so nothing in this folder changes per brand. Connect the business you are working on (`ping` names it) and invoke the skill with the store URL: Mode A builds that brand and saves it there. Without EcomOS, open Claude Code in that brand's folder, or point `$ECA_BRAND_FILE` at its file, and the skill builds `./brand/brand-data.md` there. Don't change `SKILL.md`'s body unless you're improving the generic logic.

## How to keep it current

A brand profile decays. Trigger an update on: product/price changes, new campaigns or repositioning, competitor moves, fresh customer research, or a visual refresh. Section 18 (Sources & confidence) records when each section was last verified — a good quarterly review anchor. To refresh against reality, ask Claude to "audit my brand profile against the current Shopify catalog and the live site" and flag what's stale. Edits made in EcomOS → Business Brain are picked up the next time the skill runs. EcomOS keeps the earlier versions of an edited section, so an edit can be undone from that page.

## Limitations

Mode A researches and drafts from real sources — it does not fabricate a brand with no online presence or founder input. Mode B applies the brand; the richer the profile is, the better every downstream asset gets. Time invested in the profile compounds across all future work.
