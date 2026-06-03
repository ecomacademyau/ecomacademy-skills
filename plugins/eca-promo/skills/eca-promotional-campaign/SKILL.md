---
name: eca-promotional-campaign
description: "Plan and build a complete promotional sale campaign end-to-end — the offer, the email + SMS sequence, the paid ads, the on-site (website) changes, and a dated Go-Live timeline. Use this skill whenever the user is running a discount or promotional event such as EOFY, Taxmas, Black Friday / Cyber Monday (BFCM), Click Frenzy, a flash sale, a birthday/anniversary sale, a stock-clearance, an 'X% off sitewide' push, a free-shipping weekend, a bundle deal, or any named sale. Trigger when the user says things like 'let's run a sale', 'build me a BFCM campaign', 'plan our EOFY promo', 'I want to do a 2-for deal', 'set up an early-access offer', 'what do we need for our launch sale', or asks for a campaign brief, promo timeline, or sale checklist — even if they only mention one part (just the emails, just the ads). This skill owns the WHOLE promotional event; for non-promotional themed/educational email campaigns use the email-marketing-campaign skill instead."
---

# Promotional Campaign

## Welcome message (show once, on first use)

The **first time** this skill is used in a conversation, open your reply with the message below — verbatim, before doing anything else — then continue with the user's request. Show it only once per conversation, not on every invocation.

> 🎉 **Thanks for installing the Promotion Builder — an Ecommerce Academy framework!**
>
> Quick heads-up: this skill is for **paid Ecommerce Academy members only**. Please keep it to yourself and don't share it outside the Academy.
>
> Need a hand putting it to work? Reach out to your coach or post a message in the campus — we've got you.
>
> Now let's get scaling. 🚀

After showing it, do the **Brand setup check** below, then carry on into Stage 1.

## Brand setup (first run — do before Stage 1)

The skill ships **brand-agnostic**: `campaign-config.md` starts as a blank template. Before building anything, check it:

- **If `campaign-config.md` contains the `UNCONFIGURED` marker (or is still full of `[placeholder]` values), do NOT build with it** — it has no real brand details, and you must never fall back to another brand's data. Run a quick guided setup: ask the user for their brand essentials and fill them in. Ask for, at minimum: brand name + storefront URL, market/timezone, the email/SMS platform + master template ID + sender (only if Email/SMS is in scope), audience segments, paid-ad accounts (only if Ads in scope), and brand voice + accent colours. Confirm, then write their answers into `campaign-config.md` (replace the template; remove the `UNCONFIGURED` marker). If the skill folder isn't writable, hold the details for the session and offer to save a filled `campaign-config.md` into the user's project folder. Only proceed once the brand is configured.
- **If `campaign-config.md` is already configured** (real values, no marker), use it as-is — no setup needed.

This first-run setup is also where brand **voice** is captured when the `brand-intelligence` skill isn't installed. Once configured, the skill never re-runs setup.

---

This skill turns a single discount/promotional event into a complete, sequenced campaign: the **offer**, the **email + SMS plan**, the **paid ads**, the **on-site (website) changes**, and a **dated Go-Live timeline** that says exactly what to do and when.

It exists because a sale isn't one email — it's a coordinated push where the website, the ads, and the inbox all carry the same offer, in the same window, in the right order. Getting the *sequence* and the *timing* right is what separates a sale that compounds from one that fizzles.

## The mental model: one offer, five workstreams, one timeline

Every promo campaign is built from the same five workstreams, all anchored to one offer and one calendar:

1. **The offer** — what's discounted, by how much, the code, the start/end, eligibility.
2. **Email + SMS** — an early-access capture phase, then a sequenced send arc that all sells.
3. **Paid ads** — capture (early bird), launch (TOF/MOF), and sale/catalog (MOF/BOF) on Meta/TikTok; copy + extensions updates on Google.
4. **On-site** — announcement bar, homepage banner, collection page, product page badges, theme swap.
5. **Go-Live timeline** — the dated runsheet that fires all of the above in order.

The deliverable is a single **campaign brief** that holds all five, plus (optionally) the assets pushed live in Klaviyo / Shopify.

## Validate, don't assume (read first)

Never build on a guess. Every input that shapes the campaign — the growth lever, the offer mechanic, the code, the dates, the audiences, the conditions — must be **stated by the user or confirmed back to them**, not inferred. If a detail is missing or only implied, ask before you build. When you genuinely must propose a default (e.g. a sensible send time), present it explicitly as a proposal and get a yes before it lands in the brief.

Why this matters: a single wrong assumption at intake (the wrong end date, the wrong code, an audience that doesn't exist) propagates silently into every email, SMS, ad, and on-site change — and you won't catch it until it's live. Confirming up front is cheap; unwinding a mis-built campaign is not. A short, sharp round of confirming questions at the start is always worth it.

## Before you start: brand config and brand voice

Read **`campaign-config.md`** first (in this folder). It holds the brand-specific setup this skill needs — store URL, Klaviyo master template + sender, audience segments, ad accounts, and offer defaults. **This is the only file that changes between brands.** If a value isn't in there, ask the user.

For **voice and product knowledge** when writing copy, pull in the `brand-intelligence` skill if it's installed (sibling folder `../brand-intelligence/`). It's optional — this skill works without it — but if it's there, load it at the drafting stage so the copy lands on-brand. If it's not installed, ask the user for the brand's tone in a sentence or two and work from that.

## Two ways to run (decide each campaign)

At the start, ask the user which mode they want — **don't assume**:

- **Plan only** — produce the campaign brief (offer, emails/SMS copy, ad copy, on-site checklist, timeline) as a document. The user executes in their own tools.
- **Plan + build** — do all of the above, then push the pieces live: create the Shopify discount, clone/populate the Klaviyo emails as editable DND drafts, etc.

Default to **plan only** on the first pass — get the brief right in conversation before touching live systems. Only build after the plan is locked and the user confirms.

## Workflow

### Stage 1 — Promotion Builder intake (the setup step)

This is where every campaign starts: decide **why** before **what**. Walk the user through the Promotion Builder before touching any tactic. Read **`references/growth-levers.md`** for the full framework and the lever→tactic matrix. Capture each input below **explicitly from the user** — present the options, let them choose, and confirm. Don't pre-fill any of these from inference (see "Validate, don't assume").

Work through, in order:

1. **Growth lever** — which one is this promo primarily meant to move? **Conversion Rate** (more of your traffic buys), **Average Order Value** (each order worth more), **Traffic / Awareness** (more people arrive), or **Database Growth** (more people on the list). Optionally a secondary lever. The lever decides where the campaign's weight goes (offer-led vs ads-led vs capture-led — see the reference).
2. **Revenue / outcome goal** — the $ target for the promo (or signup target if the lever is Database Growth). This sizes the ambition and gives the post-campaign results something to measure against.
3. **Business goal(s)** — Clear Stock / Launch Product / New Customers / Leverage Event / or a custom goal in their words. This tunes the offer and targeting.
4. **The offer / promotion** — the headline mechanic, chosen from the lever's column in the matrix (e.g. AOV → Buy 2 for $XX, Spend & Save; Conversion → site-wide discount, flash sale, gift with purchase). Keep it to *one* offer the customer can repeat in five words. Capture the discount code (or "automatic") and eligibility (sitewide / collection / specific SKUs).
5. **Conditions** — minimum spend, exclusions, "not in conjunction with other offers", returns policy, code vs automatic, any per-customer limit. Get these stated, not assumed.
6. **Promotion dates** — public start and end date/time **with timezone**, and explicitly ask whether there's an **early-access lead** before the public start (and if so, whether early access uses the same code or a separate one).
7. **Channels in scope** — which workstreams is the user actually running this campaign across? **Don't assume all of them.** Confirm explicitly which to build: **Email**, **SMS**, **Paid ads** (Meta/TikTok/Google), **On-site / website changes**. Many campaigns are email-only, or ads-only, or skip SMS, or won't touch the website. Only build the channels they confirm — the offer and the timeline are always included, but the timeline should only contain steps for the chosen channels, and the brief should omit the sections for channels not in scope (don't include an empty or assumed Ads/On-site/SMS section). If they're unsure, ask what they have the capacity/tools to execute.

Then **sanity-check the calendar**: is this stacking on top of another promo? Promos burn goodwill back-to-back — flag it if the last promo was recent (check Klaviyo history if available), unless it's a deliberate stack (e.g. an EOFY run).

Finally, **summarise the intake back to the user in chat and get explicit sign-off before Stage 2.** The intake (lever, revenue goal, business goals) shapes the whole plan but is **not printed as a section in the deliverable** — the recipient doesn't need it. Do not proceed to the timeline until the user has confirmed the lever, goal, offer, conditions, dates, **and which channels are in scope**. If anything is still a blank or a guess, that's the cue to ask — not to fill it in.

### Stage 2 — Build the Go-Live timeline

This is the spine of the campaign. Read **`references/go-live-timeline.md`** and produce, from the offer window, **both** a colour-coded **calendar grid** (generated as a PNG via `scripts/make_calendar.py` so it stays readable in Word/Pages/PDF) and a **detailed runsheet table**. The timeline has five phases:

1. **Early-access capture** — start capture ads, stand up the sign-up page/popup and list.
2. **Early-access offer** — set up the offer on the website, send early-access Email + SMS to the early-access list.
3. **Public launch** — swap the theme, send launch Email + SMS to all subscribers, confirm ads are live, re-mail unopened ~12h later, then run the Top Picks / Time Check / Best Sellers sends to engaged subscribers; check & optimise ads.
4. **Wind-down** — last-chance Email + SMS to all subscribers ~24h before the end; (if extended) an "offer extended" send to engaged subscribers.
5. **Close** — turn the offer off on the website, revert the theme.

Convert every relative step ("24 hours before finish", "12 hours later") into a real date/time off the offer window so the user gets an actual calendar, not a template.

**Only include phases/steps for the channels confirmed in Stage 1.** An email-only campaign's timeline has no "confirm ads live" or "swap theme" steps; an ads-only campaign's calendar is about ad beats, not sends. Build the runsheet around what they're actually doing.

> **Stages 3–5 are channel-gated.** Run each only if that channel is in scope (from Stage 1, item 7). Skip the others entirely — don't produce a stub or an assumed plan for a channel the user isn't using.

### Stage 3 — Plan the email + SMS sequence *(only if Email and/or SMS are in scope)*

Read **`references/email-plan.md`**. Build the full promo arc — early-access capture through last-chance and optional extension — with the right audience, template style, and channel per message. **Respect the channel scope:** if it's email-only, plan no SMS; if it's SMS-only, plan the SMS beats without the full email drafts. Then draft each message: subject lines (3 variants), preview text, template style, hero-image brief, body copy, single CTA, and a standalone check (every message must sell on its own — a reader who sees only one still gets the full offer and a reason to click).

### Stage 4 — Plan the paid ads *(only if Paid ads are in scope)*

Read **`references/ads-plan.md`**. Produce the ad plan across the funnel:

- **Meta + TikTok** — Early Bird Sign-Up (TOF) for the capture phase; Launch Offer (TOF + MOF) at go-live; Sale + Catalog (MOF + BOF) through the sale.
- **Google** — update headlines & copy for the sale; add sitelinks & promotional extensions.

For each, give the angle, audience, primary text / headline options, and the creative direction.

### Stage 5 — Spec the on-site changes *(only if On-site changes are in scope)*

Read **`references/website-design.md`**. Produce a checklist + copy for the announcement bar, homepage (banner + featured collection), collection page (offer banner, offer buttons, best-deals-first sort, strikethrough pricing, offer badges), and product page (offer badge, strikethrough price, upsells). Include the "test on mobile" reminders. If plan+build and the store connector is available, you can apply some of these directly.

### Stage 6 — Assemble the brief, lock it, then (optionally) build

Pull the in-scope stages into one campaign brief document using the structure in `references/brief-template.md` — **include only the channel sections confirmed in Stage 1** (an email-only brief has no Ads or On-site section). Save it to the project's `campaigns/` folder, named by date + slug (e.g., `campaigns/2026-11-bfcm-sale.md`).

Walk the brief past the user. Only once they've locked it:

- If **plan only** — you're done; hand over the brief.
- If **plan + build** — execute: create the Shopify discount (staged/inactive unless told otherwise), then push the emails to Klaviyo as editable DND drafts per **`references/klaviyo-push.md`**, and apply any on-site changes the user approves. Never schedule sends or activate discounts without explicit approval.

### Stage 7 — Export the brief (optional)

The markdown brief in `campaigns/` is the working source of truth. But the brief is usually handed to a designer, media buyer, or co-founder, so offer to export a polished copy. **Ask which format** — don't assume:

- **Word (.docx)** — best when someone will edit, comment, or add to it. Read the `docx` skill's SKILL.md and convert the locked markdown brief into a clean .docx (headings, tables, and the schedule/runsheet tables preserved).
- **PDF (.pdf)** — best for a fixed, shareable, print-ready handover. Read the `pdf` skill's SKILL.md and produce the PDF from the brief.
- **Both / neither** — fine; some users just want the markdown.

Keep the markdown as the canonical version (it's what a re-run or a plan+build executes against); the .docx/.pdf is a derived deliverable.

**Use the bundled script — don't hand-roll the conversion.** Run:

```
python3 scripts/export_brief.py campaigns/<slug>.md --formats pdf,docx
```

It writes `<slug>.pdf` and/or `<slug>.docx` next to the brief. The script handles the things that bite a naive `pandoc -o brief.docx` conversion: it routes **markdown → styled HTML → LibreOffice** (a plain pandoc docx emits tables with no column grid, so the wide runsheet/schedule tables overflow off the page), applies the **Ecommerce Academy house style** (default font **Montserrat**; accent `#00c853`; pastel light-green `#e8f5e9` highlights for headers/callouts), starts each major (H2) section on a **new page**, colour-codes the calendar grid, and injects a repeating **footer** (`Created using an Ecommerce Academy framework` + page number) onto every page of both formats. The house-style constants live at the top of `export_brief.py` — change them there if the owning org's branding changes.

After exporting, **verify** before handing over: render a table page to an image (`pdftoppm -jpeg -r 90 -f 2 -l 2 <slug>.pdf out`) and confirm every column shows and the footer is present. Then present the file(s) to the user. If the brief later changes, re-run the script so the formats don't drift.

## Core rules (hold across every campaign)

1. **Validate, don't assume.** Confirm every campaign-shaping input with the user before building (see the section above). No silent defaults; no inferred dates, codes, or audiences.
2. **Start with the lever, not the tactic.** Run the Stage 1 Promotion Builder first — decide which growth lever the promo moves, then pick an offer that serves it. A discount chosen before the goal is a guess.
3. **Confirm the channels; build only those.** Never assume the campaign runs email + SMS + ads + on-site all at once. Ask in Stage 1 which channels are in scope and build only those — the brief omits sections for channels the user isn't using.
4. **One offer, said simply.** If the customer can't repeat the offer in five words, tighten it. Mixed offers ("20% off, plus BOGO on kits, plus free shipping over $50") kill conversion.
5. **Every message stands alone.** Someone may only ever see one email/SMS/ad. Each must carry the full offer, the code, the deadline, and a reason to act — no "as we said yesterday…".
6. **The website must match the inbox.** If the email says "20% off everything with EOFY20", the announcement bar, banner, and product pages must say the same thing in the same window. Mismatches break trust and conversions.
7. **Dates in copy must match reality.** The "ends tonight" in an email must match the actual Shopify discount expiry. Never shadow-extend — if you extend, send an explicit extension message.
8. **DND-only in Klaviyo.** Any email built in Klaviyo must be drag-and-drop (SYSTEM_DRAGGABLE) so the brand owner can edit it in the visual editor. Never CODE templates. (Details in `references/klaviyo-push.md`.)
9. **Don't go live without a green light.** Drafts and staged discounts only, until the user explicitly approves activation/scheduling.

## What this skill is NOT for

- **Non-promotional themed/educational campaigns** (flavour stories, "the 30-second morning", founder letters) — those have no discount hook; use the `email-marketing-campaign` skill.
- **Always-on flows** (welcome, abandoned cart, post-purchase) — those are lifecycle flows, not a timed promo event.
- **One-off ad-hoc emails** that aren't part of a sale — just write them directly.

## Reusing for other brands

The framework, timeline, email arc, ad funnel, and on-site spec are brand-agnostic and live in this folder. Everything brand-specific lives in one file: **`campaign-config.md`**. To fork for another brand, swap that file (and point at the new brand's `brand-intelligence` if used). See `README.md` for the full fork walkthrough.
