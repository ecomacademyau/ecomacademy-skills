# ECA Black Friday Blueprint

Everything you need for an outstanding BFCM, built on **your** data rather than on what the brand next door is doing.

Skills are added to this plugin in the lead-up to Black Friday. Install it once and you stay current.

## Skills

### `eca-bfcm-offer-builder` — decide the offer

Most BFCM offers get chosen in ten minutes, in a panic, in early November, by copying a competitor. This replaces that.

1. **Pulls the evidence** — last year's Q4 split into pre-BFCM, BFCM week and post-BFCM to year end, plus the daily shape, what was discounted and what it cost, ad spend by phase, email performance, and your last 90 days against the same 90 days last year. Plus list size now versus twelve months ago.
2. **Asks what you want this year** — objective, growth lever, revenue target, margin floor, stock to clear, stock to protect.
3. **Reconciles the two, honestly.** If your target needs a 3x lift and last year's deeper discount produced 1.4x, you find out in September rather than in December.
4. **Recommends three offers** — the core BFCM offer, a genuinely different Cyber Monday offer, and a Plan B with a pre-agreed trigger, so nobody panic-discounts at 9pm on Black Friday.

Every discount depth is checked against the break-even volume lift it needs. At 60% margin, 30% off needs to double your unit volume just to stand still — most people have never seen that number for their own business.

Output is the **BFCM Campaign Master File**, the single document the rest of the Blueprint reads from and adds to.

### `eca-bfcm-email-campaigns` — plan and write the emails

Takes the offer the Offer Builder settled and turns it into the whole email programme. **Run the Offer Builder first** — this one starts from the locked offer and won't run without it.

1. **Builds the calendar** from your sale dates and cadence, split across the proven mix — 30% Hero, 40% Product, 20% Education, 10% Plain text — with a Hero at launch and a Hero at last chance, because those two sends carry the event.
2. **Fills every slot with a real topic**, reframed around your actual offer, and surfaces your own best past emails from Klaviyo as resend candidates, each tagged with the metric that earned it the slot.
3. **Reviews it with you** as an editable calendar grid before a word of copy is written.
4. **Drafts every email** — three subject lines, preview text, full copy in your voice, a section-by-section layout, one CTA — each written to stand alone, because most people only see one.
5. **Hands off** a single document plus a ready-to-paste Claude Design prompt.

It uses the exact offer one-liner from the Master File rather than rewriting it, so the emails, the banner and the ads all say the same thing. Audience sizes come from real marketable segments, never a raw profile count.

## How the two skills work together

Both read and write one shared set of files in a `bfcm/` folder:

| File | Written by | Read by |
|---|---|---|
| `bfcm-<year>-master.md` | Offer Builder, then each channel skill fills its own section | Everything |
| `bfcm-<year>-calendar.csv` | Offer Builder and you, one writer only | Everything |
| `bfcm-<year>-runsheet.csv` | Append-only, every skill tags its own rows | The dashboard |
| `bfcm-<year>-dashboard.html` | Generated, never edited by hand | You, each morning |

The email skill appends every send to the runsheet tagged `OWNER=EMAIL` and places it against a **phase ID** rather than a hard-coded date. Move your launch and every email moves with it. Open the dashboard and the emails sit alongside every other channel, in order.

**Run them in order.** The email skill needs the offer settled before it starts, and will send you back to the Offer Builder if it isn't. Every subject line, send date and segment is downstream of what the offer actually is, so planning emails first just means rewriting them all once it changes.

## Connectors

Shopify is the spine and you really want it connected. Meta Ads and Klaviyo make the picture complete. Anything missing degrades to asking you for the numbers, clearly labelled as your recollection rather than measurement.

## For paid Ecommerce Academy members

Please keep it within the Academy. [ecomacademy.co](https://ecomacademy.co)
