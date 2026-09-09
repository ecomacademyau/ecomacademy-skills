---
name: eca-bfcm-email-campaigns
description: "Build the email content calendar and full email copy for a Black Friday or Cyber Monday sale on a Shopify store, once the offer has been decided. Turns the locked offer, sale dates and send cadence into a ratio-and-topic calendar (Hero 30 percent, Product 40 percent, Education 20 percent, Plain text 10 percent), fills it with topic suggestions plus the best-performing past emails from Shopify and Klaviyo, refines it with the member, then drafts every email's subject lines, preview text, copy and layout and hands off one clean document plus a starter prompt for Claude Design. Use for a BFCM email calendar, a Black Friday or Cyber Monday email plan, a sale email content calendar, or a Claude Design handoff for sale emails. Requires eca-bfcm-offer-builder to have been run first, because the offer decides what every email says. Owns the email calendar and copy only."
---

# BFCM Email Content Calendar

Turns a sale offer into a fully planned, fully drafted email calendar: a ratio- and topic-driven skeleton, populated with real data from Shopify and Klaviyo, refined with the member, then drafted email-by-email (subject lines, preview text, copy, layout) and handed off as one clean document for Claude Design to build from.

## When to use this

Whenever the member wants to plan the emails for Black Friday/Cyber Monday or any other major sale period — a content calendar, a send schedule, topic suggestions, or the full drafted copy for each email. Not for deciding the offer itself, and not for the ads, SMS or on-site pieces of a campaign — those belong to sibling skills (see below).

## Where this sits in the Blueprint

The Offer Builder decides **what the offer is** and writes the shared campaign files. This skill decides **how the offer gets emailed** and writes its sends back into those same files.

**The Offer Builder must run first. This skill does not run without it.** That is not a preference, it is the order the work happens in: every email's headline, urgency, segment and send date is downstream of the offer, the depth and the phase calendar. Planning twelve emails and then discovering the offer is a spend-and-save rather than a site-wide percentage means rewriting all twelve. There is nothing useful to draft against a sale nobody has decided yet.

## Before you start — confirm Shopify and Klaviyo are connected

Do this first, before the Offer Builder question and before anything else. Stage 3 depends on real Shopify data (best-sellers, stock) and real Klaviyo data (past email performance, resend candidates) — building the calendar without checking first just means finding out the hard way, mid-Stage-3, that one of them isn't actually connected.

1. **Actually try each connector** with a lightweight read call (e.g. shop info from Shopify, account details from Klaviyo) rather than assuming a connection exists because the tools appear in the tool list — a listed tool isn't the same as a working, authenticated connection.
2. **If both work**, say so in one line and move straight to the Offer Builder question below.
3. **If either fails, or the tools aren't available at all**, stop and tell the member plainly which platform is missing and what it feeds:
   - **Shopify** — best-selling products and stock signals for the Product-type slots.
   - **Klaviyo** — past BFCM/sale email performance and resend candidates for Stage 3.
   Ask them to connect it before continuing — point them to wherever connectors are managed in their environment (search the connector registry / suggest the connector if that's how it's done) — then retry the check once they say it's connected.
4. **Only proceed without a connector if the member explicitly says so**, after being told plainly what they'd be giving up. If they choose to continue anyway, Stage 3 falls back to asking them directly for that information and labels it member-supplied rather than measured — never silently substitute a guess for missing data.

## Before you start — the offer must already exist

Once Shopify and Klaviyo are confirmed, check for the campaign files. Ask the member directly rather than checking silently, so they know what is happening:

> "Have you run the BFCM Offer Builder for this sale yet?"

**Then look for `bfcm/bfcm-<year>-master.md` and `bfcm/bfcm-<year>-calendar.csv` in the working folder.**

- **Both present** — read the offer one-liner, depth, dates and phase calendar from them, and **confirm every value back to the member** before treating it as locked. Files go stale, and a wrong assumption here propagates into every email.
- **Missing, or the member has not run it** — **stop here.** Do not offer to take the offer details verbally instead, and do not start a calendar you intend to fill in later. Say plainly what is missing and why it matters:

  > "I need the offer settled before I can plan the emails. Every subject line, every send date and every segment depends on what the offer actually is, so planning them first means rewriting them all once it changes. Run the BFCM Offer Builder and it will produce the offer, the dates and the phase calendar. Then come back here and I will build the whole email programme off it."

  Offer to run `eca-bfcm-offer-builder` for them now. That is the only forward path from here.

**If the Master File exists but the offer section is still `TO CONFIRM` or a placeholder**, treat it as not decided. A half-finished Master File is not a decision, and drafting against a provisional offer produces work that gets thrown away.

If `eca-brand-intelligence` is installed (sibling skill folder), pull its brand data at the drafting stage (Stage 5) for voice and product knowledge. If it isn't installed, ask the member for the brand's tone in a sentence or two and work from that — don't invent brand facts.

## Steps

### Stage 1 — Intake

Following the Offer Builder question above:

1. **What's the offer?** Take the **exact one-liner** from Master File §7 — the single plain sentence the customer reads, the one that already passed the Offer Builder's one-line test. Use that wording in the emails rather than writing a fresh description of it. A sale where the email says one thing, the banner says another and the ad says a third reads as three different offers, and the customer resolves that confusion by leaving. Confirm it back to the member, then treat it as fixed.
2. **What dates is the sale running?** Read them from `bfcm/bfcm-<year>-calendar.csv` and confirm them back, with the timezone from §1. Do not re-derive dates or ask the member to retype them — the calendar is the one source of truth, and asking again invites a second, conflicting answer.
3. **How often do you want to email?** Cadence, for example daily, or every other day, or twice daily in the last 48 hours. **This is the one thing the Master File does not set**, so it is the one thing to ask directly, every time.

Confirm the offer, the dates and the cadence back to the member as one short summary before building anything.

### Stage 2 — Build the skeleton calendar

**If a campaign calendar exists, read it first.** When `bfcm/bfcm-<year>-calendar.csv` is present, that file — not your own arithmetic — is the source of truth for when each phase runs. Load it and place sends against **phase IDs** (`LIST_BUILD`, `EARLY_ACCESS`, `WARM_UP`, `SALE_LIVE`, `BLACK_FRIDAY`, `WEEKEND`, `CYBER_MONDAY`, `POST_SALE`), never against dates you worked out yourself. If the member later moves the launch, the calendar changes and every email stays correctly placed. Hard-coding a date breaks silently the moment anything shifts.

Run `python3 ../eca-bfcm-offer-builder/scripts/sync_campaign.py bfcm/bfcm-<year>-calendar.csv bfcm/bfcm-<year>-runsheet.csv` at the start of the run to confirm the calendar is valid before building anything on top of it.

Then follow `references/content-ratios.md` to turn the date range and cadence into a slot count, then split those slots across Hero / Product / Education / Plain text by the ratio. Show the member the resulting shape in plain terms (e.g. "12 emails: 4 Hero, 5 Product, 2 Education, 1 Plain text") before filling in topics.

Fill each slot with a real topic from `references/topic-bank.md`, reframed around the actual offer — never leave a generic label like "Hero main offer" unedited in the calendar. If a Master File phase calendar exists, align Hero placements to the phase transitions (launch, early access, last chance, etc.).

**Present the skeleton as an editable calendar-grid document, not a plain table.** Follow `references/calendar-grid-format.md` and invoke the `design` skill to build it as a Claude Design canvas laid out like an actual month calendar — day-numbered date cells, with the email topic, audience segment, and (if applicable) SMS note stacked underneath each date that has a send. This is what gets reviewed in Stage 4, and what the member can keep editing directly afterward.

### Stage 3 — Pull the evidence

Connection status was already established up front. For whichever of Shopify/Klaviyo are connected, pull:

- **Shopify** — current best-sellers and any relevant stock signals (e.g. what's worth a "low stock" or bundle push).
- **Klaviyo** — past Black Friday/sale campaign performance, and separately, best-performing non-sale/educational or brand-story campaigns. Pull open rate, click rate and revenue per recipient where available.
- **Klaviyo segments** — the real audiences behind the SEGMENT row on every calendar cell. List the account's segments and use the ones defined on **active subscription** and **engagement**, not a raw profile count. A profile count includes unsubscribed, suppressed and bounced people, is always too big, and every per-recipient figure derived from it is wrong. Name the segment each number came from.

  Two traps worth knowing before you quote a size. Segment history only exists from the date the segment was **created**, so a series that starts at zero and jumps is a segment being made, not a list growing — check the leading months before calling anything growth. And the recipient count on last year's largest sale send is a real measured snapshot of who was marketable that day, which makes it the best sanity check on any number you are about to plan against.

From this, build a short list of **resend candidates**: real past emails worth tweaking for this offer, each tagged with the metric that earned it the slot and which calendar slot it would suit. Slot these in alongside fresh topics in the underlying calendar data (see `templates/calendar-template.md` for the "Source" field) before it's rendered into the Stage 2 canvas.

For any platform the member explicitly chose to proceed without, ask them directly for that information instead of guessing, and label it member-supplied rather than presenting it as measured data. This applies to Shopify and Klaviyo only — the offer itself is never member-supplied at this stage, because it is already locked in the Master File.

### Stage 4 — Review with the member

Walk the member through the calendar-grid canvas built in Stage 2, plus a ratio check against the target split (say the maths in chat — keep the canvas itself clean and calendar-like). Frame it explicitly as a starting point built from the reference guide, not a fixed plan — ask what they want to swap. Apply changes by updating the canvas directly and republishing (or let the member edit it themselves in Claude Design) rather than only describing changes back in chat. Don't move to Stage 5 until the member has actively signed off on the calendar shape.

### Stage 5 — Draft each locked email

For every email in the locked calendar:

- **Subject line** — 3 variants.
- **Preview text** — one line, complements (doesn't repeat) the subject.
- **Layout** — section-by-section notes from `references/wireframe-layouts.md`, specific to this email's content and type.
- **Body copy** — full copy in the brand's voice.
- **Primary CTA** — one button, one destination.
- **Footer** — the brand's standard email footer (social links, unsubscribe, and anything else they normally include) per `references/wireframe-layouts.md` — every email gets one, regardless of type.
- **Standalone check** — confirm the email works for someone who saw none of the others in the series (no "as we mentioned earlier").

Work through the calendar with the member email by email rather than drafting all of them silently and dumping the result — catch tone or direction issues early.

### Stage 5.5 — Write the sends into the shared campaign files

The Black Friday Blueprint keeps one set of shared files per campaign so every channel shows up in the same runsheet and the same dashboard. An email plan that only exists in a chat transcript is invisible to the rest of the campaign — the member opens the dashboard on Black Friday morning and the emails simply are not there.

**This stage is not optional.** The `bfcm/` folder is guaranteed to exist, because this skill does not start without it. An email plan that never reaches the runsheet is invisible to every other part of the campaign.

**1. Append one row per send to `bfcm/bfcm-<year>-runsheet.csv`.** The runsheet is **append-only** — add your rows, never edit or delete another skill's. Tag every row `OWNER=EMAIL` so it is obvious who owns it and so no other skill touches yours.

| Column | What goes in it |
|---|---|
| `WHEN` | Send date, and time if known, in the store's timezone |
| `TASK` | `Send: <email topic>` — the real topic, not a generic label |
| `PHASE_ID` | The phase this send falls in, taken from the calendar |
| `OWNER` | `EMAIL` |
| `STATUS` | `Not started` |
| `NOTES` | Segment, and `resend` if it is a reworked past email |

**2. Fill Master File §13.** `bfcm/bfcm-<year>-master.md` reserves section 13 for "Email and SMS plan" and it currently reads *Reserved*. Replace that with the locked calendar: the slot table, the ratio check, the segment per send, and a pointer to the full handoff document. Leave the SMS half marked `TBD` if this run only covered email — do not quietly imply SMS is planned when it is not.

**3. Regenerate the dashboard.** Run `sync_campaign.py` again with `--html bfcm/bfcm-<year>-dashboard.html --markdown` so the emails appear alongside every other channel. It validates as it goes and will tell you if a date sits outside its phase.

**4. Log it in §21.** Add a change-log line naming this skill, the date, and what it added. The Master File is a shared document and the next skill to open it needs to know who changed what.

### Stage 6 — Produce the handoff document

Once every email is drafted and approved, assemble `templates/handoff-document-template.md` into a single document: campaign overview (including the brand's standard footer, stated once since it's the same on every send), then one section per email, then a ready-to-paste **Claude Design starter prompt** (the template shows the shape — adapt it to the real campaign, don't hand over placeholder text) that reminds Claude Design to carry the footer onto every artboard.

**Always post the full document and the starter prompt directly in the chat** — as message content the member can read and copy straight away, in full, not a summary of it. This is the actual delivery; never finish by only saving a file and telling the member to go find it. Also save a copy into the campaign's `bfcm/` folder for the record (`bfcm/bfcm-<year>-email-plan.md`), which is where every Black Friday Blueprint artefact lives, and mention in passing that it's saved there too — but treat that as a backup, not the deliverable. Offer a `.docx` or `.pdf` export if the member wants a polished copy to send elsewhere (read the `docx`/`pdf` skill's SKILL.md first) — the in-chat version is still what they should be able to read and act on without opening anything.

## What it needs (tools, templates, examples)

- `references/content-ratios.md` — the Hero/Product/Education/Plain text ratio and how to turn it into slot counts.
- `references/wireframe-layouts.md` — the section-by-section layout rules per email type.
- `references/topic-bank.md` — the topic menu per content type.
- `references/calendar-grid-format.md` — the visual spec for the Stage 2/4 calendar-grid canvas.
- `templates/calendar-template.md` — the underlying slot data (date/type/topic/source) that feeds the canvas; also the fallback table if the `design` skill isn't available.
- `templates/handoff-document-template.md` — the shape for the final handoff doc and Claude Design prompt.
- The `design` skill (Claude Design canvas), to build and update the calendar-grid document in Stages 2 and 4 — **if it is available in the session**. Check before promising a canvas. When it is not there, the table in `templates/calendar-template.md` is a perfectly good deliverable: say which one the member is getting and carry on, rather than stalling on a tool that may not exist in their environment.
- Shopify and Klaviyo tools/connectors, for Stage 3's real data — checked with an actual read call before anything else, per the "Before you start" section, not assumed from tool presence.
- `eca-bfcm-offer-builder`'s shared campaign files, all in the `bfcm/` folder — only read after the member confirms at the start that they've run the Offer Builder:
  - `bfcm/bfcm-<year>-master.md` — the offer one-liner (§7), targets, and §13 for this skill's own output.
  - `bfcm/bfcm-<year>-calendar.csv` — the phase dates. Read it, never write to it: it has one writer.
  - `bfcm/bfcm-<year>-runsheet.csv` — append your sends here, tagged `OWNER=EMAIL`, never editing another skill's rows.
  - `../eca-bfcm-offer-builder/scripts/sync_campaign.py` — validates both CSVs and regenerates the dashboard. Run at the start of the run and after any change.
- `eca-brand-intelligence`'s brand data, if installed, for voice at the drafting stage.

## Check before finishing

- The calendar's type breakdown genuinely matches (or deliberately and visibly deviates from) the target ratio.
- No email depends on the reader having seen a previous one in the series.
- Every email has exactly one primary CTA.
- Every layout recommendation actually matches its email type's wireframe rules — not just labelled with the type name.
- Every date in the calendar falls inside the confirmed sale window, at the confirmed cadence.
- No topic is repeated across the calendar (repeated content *types* are fine — repeated topics aren't).
- The handoff document has every locked email fully drafted — nothing left as a placeholder or TODO.
- The standard footer (social links, unsubscribe, etc.) is noted for every email — not dropped because it's the same one repeated.
- The full handoff document and the Claude Design starter prompt were posted directly in the chat — not just saved to a file with a pointer to go look at it.
- The offer wording in the emails is the **same one-liner** as Master File §7 — not a fresh rewrite that quietly describes a different offer.
- Every send was appended to `bfcm/bfcm-<year>-runsheet.csv` with `OWNER=EMAIL`, and no other skill's rows were touched.
- Master File §13 no longer says *Reserved*, and §21 has a change-log line for this run.
- `sync_campaign.py` was re-run afterwards and reported no problems — every send sits inside the phase it claims.
- Every audience number came from a named marketable or engaged segment, never a raw profile count.

## What this skill is NOT for

- **Deciding the offer itself** (mechanic, depth, break-even) — that's `eca-bfcm-offer-builder`, and it is a hard prerequisite, not an alternative. If the offer isn't settled, send them there rather than working around it.
- **Non-sale email programmes.** This skill assumes a sale with a locked offer and a phase calendar. For themed or educational campaigns with no promotional hook, that's `eca-email-marketing-campaign` in the Marketing Coworker.
- **The full multi-channel campaign** (ads, SMS, on-site changes, the dated Go-Live timeline). Those live in the other Black Friday Blueprint skills and in the shared runsheet. This skill owns the email content calendar and the per-email drafting and layout, and nothing else.
- **Non-sale themed or educational campaigns** with no promotional hook — that's `eca-email-marketing-campaign`.
- **Pushing emails live into Klaviyo** — this skill's deliverable is the handoff document and the Claude Design prompt, not Klaviyo drafts. If the member wants emails built in Klaviyo, point them to `eca-email-marketing-campaign` in the Marketing Coworker, which owns that workflow.

## Reusing for other brands

Brand-agnostic by design — nothing brand-specific is hardcoded, so this works for any Shopify store the member manages, including client stores. Brand voice comes from `eca-brand-intelligence` when installed, or a quick tone check with the member when it isn't. Nothing needs to change to reuse it on a different store, beyond running the Offer Builder for that store's sale first.

---
*Built with the TEACH framework. Hone it: run it on a real sale, see what it gets wrong, and tune the steps or sharpen the trigger above.*
