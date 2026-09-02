# When there is little or no history

A store with no BFCM behind it is not a reason to refuse. It is the member who most needs a plan and has the least to go on, and BFCM is expensive to get wrong the first time.

What must not happen is the skill quietly behaving as though it has evidence when it does not. So: **name the tier, say what it costs, and change the method accordingly.**

## Declare the evidence tier out loud, before anything else

| Tier | What you have | What changes |
|---|---|---|
| **1 — Full** | Sales platform connected, 13+ months, prior BFCM, ads and email connected | Everything in the main flow. History is the spine. |
| **2 — Partial** | Some connectors, or under 13 months, or no prior BFCM | The year scan still works on whatever exists. Comparisons to "last BFCM" do not. Say which is which. |
| **3 — Manual** | No connectors, but the store has traded | Member supplies the numbers. Everything is labelled member-supplied. The unit economics carry the plan. |
| **4 — None** | New store, or first season | No evidence at all. The plan rests entirely on margin arithmetic and the calendar. Targets are explicitly unvalidated. |

**Record the tier in the Master File and repeat it in the summary.** A recommendation built at Tier 4 must never be presented with the confidence of one built at Tier 1.

## The scan degrades better than the comparison does

This is worth knowing: a store with eleven months of trading and no prior Black Friday **can still run the whole-year outlier scan**. It cannot compare BFCM to BFCM, but it can find its own best-performing period and what that period cost in discount. For a first-timer that is often more useful than a BFCM comparison would have been, because it identifies a mechanic that already works on their own customers.

So at Tier 2, lead with the scan, not with the missing comparison.

`scripts/promo_outliers.py` takes plain rows, so it works with an export from any platform — WooCommerce, BigCommerce, Squarespace, a POS, or a spreadsheet the member keeps by hand. Ask for weekly revenue, orders and discounts for as far back as they have, and run the same analysis.

## Tier 3 and 4: what to ask for instead

Ask for these directly. Approximate is fine and better than nothing, as long as it is **labelled as their estimate**:

**Trading shape** — average monthly revenue and orders, or "roughly how many orders in a normal week". Current AOV. Roughly what share of sales are to returning customers.

**Unit economics — the part you cannot proceed without.** Gross margin. Product prices and what they cost to make. Shipping cost per order and any free-shipping threshold. Without margin there is no break-even, and without a break-even any discount recommendation is a guess.

**Audience** — email and SMS list size, roughly how engaged, monthly website visitors if they know.

**Stock** — what they have, what is arriving and when, anything that must move.

**Anything they have already run** — even one sale, one discount code, one email. A single data point they remember beats zero.

## What the plan rests on instead of history

At Tier 3 and 4, unit economics do the work history normally does:

1. **Break-even is the spine.** With margin and price you can still say exactly what volume lift a given discount needs. That analysis does not require any history at all, and it is the single most valuable thing you can give a first-timer.
2. **Push hard toward the no-discount column.** A store with no proof that discounting works on its customers should not open with its deepest possible offer. Gift with purchase, bundles, limited editions and extended returns all protect margin while the brand learns what its buyers respond to.
3. **Prefer a mechanic that produces data.** An early-access list, a clear code, a distinct bundle — things that will be measurable in the post-mortem. Next year's plan is built from this year's records.
4. **Set conservative targets and label them.** Write the target into the Master File as `UNVALIDATED — no historical basis` and say so in the summary. A first BFCM target is a hypothesis.

## Hard rules for low-evidence runs

- **Never substitute an industry benchmark for missing history.** No "most stores see a 3x uplift". You do not know their category, list quality, margin or traffic, and a fabricated benchmark is worse than an admitted gap because it will be planned against.
- **Never present member recollection as measurement.** Label it every time it appears, not once at the top.
- **Never let a missing connector become a silent assumption.** `NOT AVAILABLE — not connected` in the Master File, every time.
- **Say what the plan would look like with data**, so they understand what connecting things later would buy them. That is a genuine reason to connect, not a sales line.
- **Set up measurement now.** Before the campaign runs, agree what will be recorded: the code, the dates, the list size at launch, spend by channel. At Tier 4 the most valuable output of this whole skill may be that next year is a Tier 1 run.
