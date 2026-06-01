# Promotional Campaign — a reusable Claude skill

A Claude skill that plans and builds a **complete promotional sale campaign** end-to-end — the offer, the email + SMS sequence, the paid ads, the on-site changes, and a dated Go-Live timeline. Built for any major discount or promotional event: EOFY, Taxmas, Black Friday / Cyber Monday, Click Frenzy, flash sales, bundle deals, clearance, free-shipping weekends.

The skill ships **brand-agnostic**. **The only brand-specific knowledge lives in one file: `campaign-config.md`**, which ships as a blank template (`campaign-config.template.md`). The **first time you use the skill it runs a quick Brand Setup** — it asks for your store, email/SMS platform, segments, voice, and colours, then fills in `campaign-config.md`. After that it's configured for your brand. Nothing else in the skill changes between brands.

## What's in the folder

```
promotional-campaign/
├── SKILL.md                       # The campaign-build framework + workflow. Same for every brand.
├── campaign-config.md             # Your brand's config (filled by first-run Brand Setup). The only per-brand file.
├── campaign-config.template.md    # Blank template; the source for a clean distributable + the basis for setup.
├── README.md                      # This file.
├── scripts/
│   ├── export_brief.py            # Stage 7 export: md → styled .docx/.pdf (EA house style + footer). Edit house-style constants at top.
│   ├── make_calendar.py           # Renders the Go-Live calendar as a PNG (readable in Word/Pages/PDF) from a JSON spec.
│   └── fonts/                     # Bundled Montserrat .ttf files (OFL), auto-installed at export for true-Montserrat PDFs.
└── references/
    ├── growth-levers.md           # The Promotion Builder — growth-lever framework + tactic matrix (Stage 1 intake)
    ├── go-live-timeline.md        # The 5-phase dated runsheet + cadence
    ├── email-plan.md              # Self-contained promo send arc (Email + SMS)
    ├── ads-plan.md                # Meta/TikTok funnel + Google updates
    ├── website-design.md          # Announcement bar / homepage / collection / product specs
    ├── klaviyo-push.md            # Push-to-Klaviyo workflow (plan+build mode)
    └── brief-template.md          # The single campaign brief deliverable structure
```

## What this skill does

It opens with a strategic **intake** — the Promotion Builder — then drives five coordinated workstreams off one offer and one calendar.

**Stage 1 — Promotion Builder (setup):** decide *why* before *what*. Pick the **growth lever** the promo should move (Conversion Rate / Average Order Value / Traffic-Awareness / Database Growth), set a **revenue/outcome goal**, name the **business goal(s)** (Clear Stock / Launch Product / New Customers / Leverage Event), then choose an **offer** from that lever's tactic column, plus **conditions** and **dates**. The lever decides where the campaign's weight goes (offer-led vs ads-led vs capture-led). Every input is confirmed with the user — nothing is assumed.

Stage 1 also **confirms which channels are in scope** (Email, SMS, Paid ads, On-site) — campaigns are often email-only or ads-only, so the skill builds only the channels the user is actually running and omits the rest. Then the in-scope workstreams:

1. **The offer** — what's discounted, the code, the window, eligibility.
2. **Email + SMS** — early-access capture → early access → launch → re-mail → top picks → time check → best sellers → last chance → (optional) extended. SMS on the three big beats only.
3. **Paid ads** — Early Bird (TOF) → Launch (TOF+MOF) → Sale+Catalog (MOF+BOF) on Meta/TikTok; copy + extension updates on Google.
4. **On-site** — announcement bar, homepage banner, collection page (strikethrough, badges, best-deals-first), product page, theme swap.
5. **Go-Live timeline** — the dated runsheet firing all of the above in order.

The deliverable is one **campaign brief** holding all five; in plan+build mode it also pushes the pieces live (Shopify discount, Klaviyo DND drafts, on-site changes). The brief is written as markdown (the canonical version) and can be exported to **.docx** or **.pdf** for handover via `scripts/export_brief.py` (Stage 7) — styled in the **Ecommerce Academy house style** (default font **Montserrat**, green `#00c853` accents, pastel light-green highlights) with a `Created using an Ecommerce Academy framework` footer on every page. (Montserrat `.ttf` files ship in `scripts/fonts/` and are auto-installed at export time, so PDFs render in true Montserrat.) Those house-style constants are skill-level (they survive brand forks) and live at the top of the export script; the client brand's own colours/voice stay in `campaign-config.md` and `brand-intelligence`.

## Two ways to run (chosen each campaign)

- **Plan only** — produce the brief; the user executes it.
- **Plan + build** — produce the brief, then push live (Shopify discount staged, Klaviyo emails as editable DND drafts, on-site changes the user approves).

Default is plan-only on the first pass — lock the plan in conversation before touching live systems.

## How it relates to the other skills

- **Fully standalone for email logic** — the promo send arc and template styles are baked into `references/email-plan.md`, so this skill works even if the `email-marketing-campaign` skill isn't installed.
- **Uses `brand-intelligence` if present** — pulls in brand voice/products at the drafting stage when that sibling skill is installed; otherwise asks the user for tone. It's optional.
- **Division of labour:** this skill owns *promotional sale events*. For non-promotional themed/educational email campaigns (flavour stories, founder letters, "the 30-second morning"), use `email-marketing-campaign` instead.

## Key rules baked in

1. **Validate, don't assume** — every campaign-shaping input (lever, offer, code, dates, audiences, conditions) is confirmed with the user before anything is built. No silent defaults.
2. **Start with the lever, not the tactic** — the Promotion Builder runs first; the offer is chosen to serve the chosen growth lever.
3. **One offer, said simply** — if the customer can't repeat it in five words, tighten it.
4. **Every message stands alone** — a recipient may see only one; each carries the full offer, code, deadline, and CTA.
5. **Website matches the inbox matches the ads** — same offer, code, and dates everywhere, in the same window.
6. **Dates in copy = Shopify expiry** — never shadow-extend; use the explicit "Offer Extended" message.
7. **DND-only in Klaviyo** — drag-and-drop templates only, so the brand owner can edit them.
8. **No go-live without a green light** — drafts and staged discounts only, until explicitly approved.

## Reusing for another brand — fork walkthrough

The framework, timeline, email arc, ad funnel, on-site spec, and brief template are all brand-agnostic. Only `campaign-config.md` carries brand specifics.

### Step by step

1. **Copy this folder** to the new brand's project (`skills/promotional-campaign/`).
2. **Replace `campaign-config.md`** with the new brand's setup:
   - Store URL, platform, currency/market, **timezone** for scheduling.
   - Offer defaults (discount creation style, typical mechanics, code style).
   - Klaviyo: the **API master** template ID (must be DND, no universal blocks) + a visual-reference master, and sender defaults.
   - Audience/segment IDs for each phase (early-access, all subscribers, engaged).
   - SMS provider + rules.
   - Paid ad accounts (Meta/TikTok/Google).
   - Brand voice/visual quick-reference (colours, fonts, tone).
3. **Point at the new brand's `brand-intelligence`** (optional) — if that sibling skill is used, make sure the brand has its own `../brand-intelligence/brand-data.md`. If not, the skill will ask for tone.
4. **Don't change** `SKILL.md`, `references/*.md`, or this README — they're brand-agnostic by design. If you want to change one, the change almost certainly belongs in `campaign-config.md`.
5. **Running multiple brands side-by-side?** Rename the folder (e.g. `promotional-campaign-acme/`) and update the `name:` field in `SKILL.md` frontmatter so Claude can disambiguate.

### What changes between brands

| File | Per brand? | Why |
|------|-----------|-----|
| `SKILL.md` | No | Framework + workflow are universal |
| `references/growth-levers.md` | No | The Promotion Builder framework is universal |
| `references/go-live-timeline.md` | No | The 5-phase structure is universal |
| `references/email-plan.md` | No | The send arc is universal |
| `references/ads-plan.md` | No | The funnel is universal |
| `references/website-design.md` | No | The on-site surfaces are universal |
| `references/klaviyo-push.md` | No | The push workflow uses the brand's config |
| `references/brief-template.md` | No | The brief structure is universal |
| `campaign-config.md` | **Yes** | Store, Klaviyo, audiences, ads, voice — all brand-specific |
| `../brand-intelligence/brand-data.md` | **Yes** (if used) | Voice, products, ICP |

## What this skill is NOT for

- **Non-promotional themed/educational campaigns** — use `email-marketing-campaign`.
- **Always-on lifecycle flows** (welcome, abandoned cart, post-purchase).
- **One-off ad-hoc emails** outside a sale.
