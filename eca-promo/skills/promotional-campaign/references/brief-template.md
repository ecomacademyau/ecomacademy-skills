# Campaign Brief Template

The single deliverable that holds all five workstreams. Save to the project's `campaigns/` folder as `campaigns/<YYYY-MM>-<slug>.md` (e.g. `campaigns/2026-11-bfcm-sale.md`). Fill every section from Stages 1–5. Keep it skimmable — the user should be able to hand it to a designer, a media buyer, or load it into Klaviyo themselves.

The Promotion Builder intake (lever, revenue goal, business goals) drives the plan but is **not printed** in the deliverable — it's working context, not something the recipient needs.

Section order matters for the export: the **checklist** comes first and the **Offer** second, because the export keeps those two sections together on page one with the title; every section after that starts on a fresh page.

```markdown
# Campaign — [Event], [headline offer]

**Famous for:** [the offer in five words]
**Hero offer:** [mechanic + code]
**Type:** Promotion — [event]
**Mode:** [plan only / plan + build]
**Plan locked:** [date]

## Pre-flight checklist
- [ ] [the things to confirm / set up before go-live — Shopify discount mechanism, segment IDs, SMS provider, inventory, images, send times, dates-match-copy, etc.]

## 1. The offer
- **Mechanic:** [X% off / 2-for-$X / etc. — from the lever's tactic column]
- **Code:** `[CODE]` (or "automatic")
- **Eligibility:** [sitewide / category / SKUs; any minimum]
- **Conditions:** [min spend, exclusions, not-in-conjunction, returns, per-customer limit]
- **Public window:** [start date/time → end date/time, timezone]
- **Early-access window:** [if any — and same code or separate]
- **Shopify status:** [staged / active / draft + discount node ID if created]

## 2. Go-Live timeline (runsheet)
[Dated table — every step with a real date/time. From go-live-timeline.md.]

| Day | Date | Action | Channel | Audience |
|-----|------|--------|---------|----------|
| … | … | … | … | … |

## 3. Email + SMS sequence  — *include only if Email/SMS in scope*
[Overview table, then each message fully drafted.]

### Schedule
| # | Date | Message | Channel | Audience | Subject (primary) | Template |
|---|------|---------|---------|----------|-------------------|----------|

### Message details
[Per email: 3 subject variants, preview text, template style, hero-image brief, body copy, CTA, standalone check.]
[Per SMS: copy (≤160 chars), link, code + deadline confirmed.]

## 4. Paid ads  — *include only if Paid ads in scope*
### Meta + TikTok
[Per beat (Early Bird TOF / Launch TOF+MOF / Sale+Catalog MOF+BOF): audience, primary text options, headline options, creative direction, CTA + destination.]
### Google
[Headline/copy updates; promotion + sitelink extensions.]

## 5. On-site changes  — *include only if On-site in scope*
[Checklist + copy for: announcement bar, homepage banner + featured collection, collection page (banner, offer buttons, sort, strikethrough, badges), product page (badge, strikethrough, upsells), theme swap, mobile test.]

## 6. Close & results
- [ ] Turn offer off on website; revert theme; deactivate discount.
- **Results (post-campaign):** [revenue, by-email performance, ad ROAS — fill after the sale.]
```

## Notes
- Convert all relative timings to real dates before saving — the brief is a runsheet, not a template.
- The same offer, code, and dates must appear identically in sections 1, 3, 4, and 5. If they drift, fix it before locking.
- The intake (lever, revenue goal, business goals) is confirmed with the user in Stage 1 and shapes everything, but isn't printed as a section — the recipient doesn't need it.
- **Include only the channel sections confirmed in Stage 1.** Sections 3 (Email/SMS), 4 (Ads), and 5 (On-site) are each optional — drop the ones the user isn't running. Renumber what remains so there are no gaps, and make sure the timeline only references the channels that are actually in the brief.
- Keep the order: checklist first, Offer second (the export pairs them on page one), then sections 2–6, then the Voice cross-check. Don't add `---` dividers between sections — page breaks separate them, and a stray rule strands a blank page.
- If plan-only, the checklist + sections 1–6 are the whole deliverable. If plan+build, the brief is the source of truth the build steps execute against.
- This markdown file stays the canonical version. Per Stage 7, export a polished **.docx**/**.pdf** via `scripts/export_brief.py` for handover — saved alongside the brief with the same slug. Re-export if the brief changes so formats don't drift.
