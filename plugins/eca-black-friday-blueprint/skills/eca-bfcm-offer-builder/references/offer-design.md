# Designing the offer

## Why before what

Most brands reach for a tactic before deciding what the promo is meant to move. "Let's do 20% off" is a decision about mechanics made before the decision about outcome, and it is why so many BFCM sales produce record revenue and worse profit than the month before.

Order of operations, always: **objective → growth lever → mechanic → depth → conditions**.

## The four growth levers

```
                 SALES
   Average Order Value  |  Conversion Rate
  ----------------------+----------------------
        Traffic         |     Database
                 MARKETING
```

| Lever | What it moves | Choose it when |
|---|---|---|
| **Conversion Rate** | More of the existing traffic buys | Shift stock, react to an event, turn visits into orders |
| **Average Order Value** | Each order is worth more | Lift basket size or margin without needing more traffic |
| **Traffic / Awareness** | More people arrive | Get in front of new audiences |
| **Database** | More people on the list | Build the asset you can sell to for free afterwards |

## Simple scales, complexity fails

**This governs every recommendation in this file.** An offer has to survive three seconds of a distracted person's attention on a phone, in the busiest, noisiest week of the retail year, while eleven other brands shout at them. Complexity is not a neutral design choice that costs a little clarity. It is the thing that kills offers.

Complexity costs three times over, and the second and third are the ones people forget:

1. **The customer has to understand it.** Every clause is a chance to give up. Confusion does not produce a question — it produces a closed tab.
2. **The member has to build it.** Tiers, exclusions and stacking rules are where discounts get misconfigured, and a misconfigured discount on Black Friday is a live fire with real money going out the door.
3. **You have to be able to tell whether it worked.** An offer with four moving parts cannot be attributed to any of them, so nothing is learned and next year starts from zero again.

A flat offer everyone understands beats a clever one that is theoretically optimal. Optimal-on-paper assumes the customer reads the paper.

### The one-line test — an offer fails until it passes

**Say the offer in one plain sentence, with no "and", no brackets, no asterisk, no second sentence.** If it cannot be said that way, it is not ready to recommend, no matter how good the maths looks.

| Passes | Fails |
|---|---|
| "30% off everything." | "30% off, or 40% when you spend $150, excluding new arrivals." |
| "Spend $100, save $25." | "Spend $100 save $20, $200 save $50, $300 save $90, cannot combine." |
| "Free shipping on every order." | "Free express shipping over $80 for members with code CYBER, one use." |
| "Buy 2, get the third free." | "Buy 2 get 1 free on selected lines, excluding bundles and sale items." |

The test is not "can I write it in one line" — anyone can compress anything. It is **would a stranger act on that line without asking a follow-up question.** If your one-liner needs a footnote to be honest, the offer is too complicated and the footnote is the proof.

### Score it before you recommend it

`scripts/offer_friction.py` counts the hoops so "too complicated" is a number you can put in front of the member rather than an opinion they can wave away.

```bash
python3 scripts/offer_friction.py --line "Spend $100, save $25" --threshold --build automatic
python3 scripts/offer_friction.py --line "<their offer>" --build code --tiers 3 \
        --conditions "no stacking,excl gift cards,excl bundles"
```

**0–1 clean · 2–3 acceptable, near the practical ceiling · 4+ rework before recommending.** It exits non-zero on a fail, and it names each thing adding friction so the conversation is about specific removals rather than a general feeling that something is too fiddly. Run it on the member's own idea too — a score of 12 beside a score of 1 makes the argument better than any amount of advocacy.

### Rewrite, do not annotate

When an offer fails the test, the fix is never a clearer explanation, a better banner, or a well-designed table of tiers. **The fix is a simpler offer.** Design effort spent making complexity legible is effort that should have been spent removing it.

Three tiers become one threshold. Four exclusions become one collection that is in or out. A code becomes an automatic discount. Every removal is a real gain, not a compromise.

### What to do when the member wants the complicated one

Members often arrive attached to an elaborate mechanic, usually because it models beautifully in a spreadsheet. Do not just agree, and do not lecture. **Show them the simple version beside it**, with the break-even for both, and say plainly what the complexity is buying and what it costs. Often the simple version earns nearly as much on paper and considerably more in practice, because the modelled version assumes perfect comprehension and perfect setup.

If they still want it after seeing both, build it — it is their store and their call. Record in the Master File that the simpler alternative was offered and declined, along with the one-liner it would have had. Next year's post-mortem will want to know.

## The tactic bank

Mechanics are grouped by **the lever they move**, and within each lever they are ordered **least friction first**. Do not pull a tactic from a column you are not trying to move — and do not reach past the top of a column without a reason you can say out loud.

**Start at the top. Move down only when the simpler mechanic genuinely cannot do the job.** "It is a bit boring" is not a reason. Boring converts.

### Reading the friction tiers

- **Tier 1 — reach for these first.** One sentence, no threshold to calculate, no code to remember, and Shopify can run it natively as an automatic discount. The customer understands it at a glance and the member cannot misconfigure it badly.
- **Tier 2 — fine, with one condition.** A single threshold or a single qualifying rule. Still one sentence. This is the practical ceiling for most stores.
- **Tier 3 — only with a specific reason.** Multiple conditions, extra customer steps, or app/manual setup. These need real justification, and they need someone with time to build and monitor them during the busiest week of the year.

### Conversion Rate

- **Tier 1** — Site-wide discount · Free shipping · Collection discount
- **Tier 2** — Gift with purchase · Clearance / final sale tier · Flash sale on one clear window
- **Tier 3** — Secret sale · Shop & win · Influencer coupon codes · Referral award

### Average Order Value

- **Tier 1** — A single fixed bundle at one price · Buy one get one
- **Tier 2** — Spend & Save at **one** threshold · Buy X for $XX · Gift with purchase at one threshold
- **Tier 3** — Multi-tier spend & save · Tiered discount by basket size · Spend to win · VIP program · Live shopping event · Personal shopping

**On tiered spend-and-save specifically.** It is the most over-recommended mechanic in BFCM, because in a spreadsheet each tier looks like free incremental margin. In the checkout it asks the customer to do arithmetic against their cart, and most will not. If AOV is the lever, **one threshold set just above current AOV** captures most of the available lift for a fraction of the confusion. Recommend the single threshold first, every time.

### Traffic / Awareness

- **Tier 1** — Meta Ads · Google Ads · Video ads
- **Tier 2** — SEO · Product reviews · Affiliate marketing
- **Tier 3** — Public relations · Offline marketing

### Database

- **Tier 1** — On-site capture · Early access sign-up for the sale
- **Tier 2** — Off-site sign-ups · Event sign-ups · In-store sign-up
- **Tier 3** — Off-site competitions · Partnerships · Referral marketing

### No discount

**Read this column out loud to every member before they commit to a percentage.** These protect margin, and several outperform a discount on a brand with genuine demand.

- **Tier 1** — "Not on sale" sale · New drop · Extended returns window · Gift guides
- **Tier 2** — Limited edition product · Members-only products · Holiday packages · Charity donations · Extended warranties
- **Tier 3** — Customisation · Digital product add-on · Collaborations · Partner program

## Objective → lever → mechanic

| Objective | Usual lever | Mechanics that fit | Watch for |
|---|---|---|---|
| **Clear stock** | Conversion Rate | Markdowns on the specific SKUs, clearance tier, bundle the slow item with a fast one | Discounting the whole store to move three SKUs. Target it. |
| **Increase revenue** | AOV, then CVR | Spend & Save, Buy X for $XX, tiered thresholds | Revenue up, profit down. Check the break-even below. |
| **Acquire new customers** | Traffic + CVR | First-order offer, gift with purchase, strong entry bundle | Acquisition cost. A cheap first order is only good if they come back. |
| **Reactivate customers** | Database + CVR | Early access for the list, members-only pricing, win-back bundle | Training the list to only buy on sale. |
| **Protect margin** | AOV or No discount | Gift with purchase, extended warranty, limited edition, bundle | Doing nothing while competitors shout. Silence is also a choice with a cost. |

## The break-even check — run this every time

A discount is a price cut, and a price cut has to be paid for in volume. Work out how much extra volume the offer needs just to stand still, and **show the member the number before they choose the depth**.

For a gross margin `M` (as a decimal) and a discount `D` (as a decimal), the extra unit volume required to hold gross profit flat is:

```
required volume uplift = D / (M - D)
```

At 60% gross margin:

| Discount | Volume lift needed to break even |
|---|---|
| 10% | +20% |
| 20% | +50% |
| 30% | +100% |
| 40% | +200% |
| 50% | +500% |

At 40% gross margin:

| Discount | Volume lift needed to break even |
|---|---|
| 10% | +33% |
| 20% | +100% |
| 30% | +300% |
| 40% | breaks even at zero margin — never do this |

Two things follow. **A deep discount on a thin margin is arithmetic that cannot work.** And **the member's actual margin is required input** — if they do not know it, that is the first thing to find out, not something to assume. If they genuinely cannot provide it, say clearly that the recommendation is directional only.

### Gift with purchase is usually the cheapest lever you have

A discount costs you the full percentage. A gift costs you only its COGS, while the customer values it at retail.

At gross margin `M`, a gift with RRP `R` costs `R x (1 - M)`. At 69% margin a $14.95 item costs $4.63. Added to a $120 order that is an **effective discount of 3.9%**, not 12.5%, and it needs roughly a 6% volume lift to break even rather than 22%.

This is why gift-with-purchase and threshold bonuses so often beat a straight percentage on the same headline generosity. Run this calculation before proposing any percentage discount, and show the member both numbers.

Then sanity-check against last year: did the discount they ran actually produce that volume lift? The answer is usually no, and it is the single most useful thing this skill can show them.

## Always compute the do-nothing baseline first

Before any target conversation, work out what this year's event produces **if nothing changes except the business's existing growth**: last year's orders multiplied by the current order growth rate, at last year's AOV multiplied by the current AOV growth rate.

That number reframes everything honestly. A target that looks like 4x last year may be 2.5x the realistic baseline, and the gap between those two framings is the difference between an ambitious plan and a fantasy. Show the baseline, then show what each candidate target requires in orders and AOV, as a table. Let the member pick against the table rather than in the abstract.

## Designing the three offers

### The core offer
The main event, live for the whole window. It must:

1. **Pass the one-line test** — before anything else. Write the actual sentence the customer will read and put it at the top of the recommendation. If you cannot write it, you do not have an offer yet.
2. **Move the lever** tied to the stated objective.
3. **Be defensible on margin** at the forecast volume.
4. **Beat last year's mechanic** for a reason you can name from the data.
5. **Be buildable in Shopify natively**, ideally as an automatic discount with no code. If it needs an app, manual work, or a support person explaining it, that cost is part of the offer and must be stated.

Take the simplest mechanic that moves the lever, then stop. The instinct to add "and also free shipping over $X" is where good offers go to die — it doubles the thinking and adds almost nothing, because the customer already decided at the headline.

### The Cyber Monday offer
Cyber Monday is not "the sale continues". Traffic returns with different intent: later buyers, more considered, more mobile, and many arriving after seeing the brand for the first time on Friday. A repeated offer gets ignored by everyone who already saw it.

Make it **genuinely different**, and usually pointed at a different lever:
- Core was site-wide CVR? Make Cyber Monday an AOV play — bundle, spend-and-save, gift with purchase.
- Core was AOV? Make Cyber Monday a narrower, sharper CVR play on a specific collection.
- Or make it access rather than depth: a limited drop, a members-only door, the bundle that sold out on Friday coming back.

**Different does not mean more complicated.** The Cyber Monday offer gets the same one-line test, and it is a fresh sentence rather than an amendment to Friday's. "Everything 30% off" followed by "Free shipping on everything, today only" is two clean offers. "30% off, plus free shipping, plus the bundle tier unlocks" is one confusing one. If the second offer can only be explained by referring to the first, it is a continuation wearing a costume.

**Do not go deeper than the core offer** unless the member accepts that Friday's buyers will feel punished for buying early. If they do go deeper, plan the goodwill fix in advance — usually a credit to early buyers.

### Plan B
Decided in advance, in writing, **so nobody panic-discounts at 9pm on Black Friday**. That is the point of it. Panic discounting mid-event is the single most expensive mistake in BFCM and it happens because no threshold was agreed while everyone was calm.

Plan B needs five things:

1. **A trigger metric** — usually revenue against target, sometimes conversion rate or sell-through on the SKUs being cleared
2. **A threshold** — a specific number, e.g. "below 60% of the day-one revenue target"
3. **A check point** — an exact date and time, e.g. "Black Friday 2pm"
4. **The switch** — the exact change, e.g. "add free shipping site-wide" or "open the bundle tier early"
5. **Who decides** — one named person

Good Plan B switches add a reason to buy without moving the headline price: free shipping, a gift with purchase, an extended window, a bonus product, unlocking a tier early. Cutting the price deeper is the last resort, not the first, because it cannot be undone and it teaches the list to wait.

Write the trigger so it can be checked in one query.

## Label every modelled number as a model

Any figure you produced by assumption rather than measurement — a decay rate on list value, a forecast conversion, an assumed repeat rate — must be named as an assumption **at the point it appears**, with the assumed value stated. Not in a footnote, and not only in the assumptions log.

The failure mode is subtle: a modelled number quoted twice becomes a fact by the third mention, and it will be repeated back to the member in December as if it had been measured.

## Scarcity — only if it is real

Three honest kinds: **time** (a real deadline), **product** (genuinely limited stock or a limited run), **bonus** (a gift for the first N orders, and you stop at N).

Fake countdowns that reset, and "only 3 left" on an item with 400 in the warehouse, are misleading conduct. In Australia that is the ACL, in the US the FTC, in the UK the CMA. Beyond the legal exposure, customers recognise it and it costs more trust than it buys urgency.

## Pricing claims — the BFCM-specific trap

"Was $X, now $Y" requires the item to have genuinely been sold at $X for a reasonable period immediately before. Inflating a price in October to discount it in November is the most-enforced deceptive pricing issue there is, and BFCM is when regulators look.

Rules for this skill:
- Never propose a "was" price the brand has not actually been trading at
- Never propose an RRP comparison the member cannot substantiate
- If they want a strikethrough, ask when the item last sold at that price, and record the answer in the Master File
- "Up to X% off" requires a meaningful number of items at the maximum depth

## Conditions — every one is friction, so start from none

The section below is often read as a checklist of conditions to *add*. It is the opposite. **Every condition is a small tax on comprehension and a place the build can go wrong.** Three exclusions do not sound like much until they are the difference between a customer buying and a customer closing the tab, or between a discount that works and one that quietly applies to gift cards all weekend.

**Default to none. Add a condition only when leaving it out causes a real, nameable loss** — margin destroyed, stock oversold, a legal or partner obligation broken. "It feels safer" is not a nameable loss. Neither is "in case someone games it": a handful of people getting a slightly better deal costs far less than every customer having to parse a rule.

Where a condition must exist, prefer the version the customer never has to think about:

| Instead of | Prefer | Why |
|---|---|---|
| A discount code | An automatic discount | Nothing to remember, copy, or mistype |
| Four excluded collections | One collection that is in, or out | One rule instead of four |
| "One use per customer" | No limit, unless there is a real arbitrage risk | Rarely worth the confusion it causes |
| Tiered thresholds | One threshold | Removes arithmetic at the checkout |
| Complex stacking rules | Discounts do not stack, stated plainly once | Ambiguity here generates support tickets and chargebacks |

**These still have to be decided, even when the answer is "no condition".** Deciding is not the same as adding — an unstated default is how a sale ends up applying to wholesale partners at 2am. Settle each one and write the answer down, keeping as many as possible at "none":

Minimum spend · exclusions (new arrivals, bundles, gift cards, already-discounted lines) · stacking with other codes and automatic discounts · subscription orders · whether it applies to returns and exchanges · one use per customer · start and end times **with timezone** · whether wholesale or retail partners are affected · what happens to orders placed minutes after the end.

**Then read the final one-liner again with every surviving condition included.** If it no longer passes the one-line test, the conditions have eaten the offer — go back and remove until it does.
