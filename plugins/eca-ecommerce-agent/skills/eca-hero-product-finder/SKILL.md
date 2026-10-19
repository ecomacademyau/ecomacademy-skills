---
name: eca-hero-product-finder
description: "Find which product a store should acquire new customers on with Meta ads, then show the order signals that shape the offer built around it. Handles repeat stores like skincare, supplements and pet food, one time purchase stores like ebikes and furniture, and gifting stores, plus a break even CPA check for small budgets. Use whenever someone says find my hero product, hero product, hero offer, what should I advertise, which product should I run ads on, which offer should I run, what to sell on Meta, best first purchase, entry product, which product brings customers back, repeat rate by product, first order analysis, break even CPA, or uploads an order export and asks about repeat customers or which product to scale. Trigger even if they never say hero. Pulls orders from the Shopify connector with CSV export as fallback, computes everything in code rather than estimating, and hands the finding to the ad copy, UGC and landing page skills."
---

# Hero Product Finder

Finds the product that should carry a store's Meta acquisition, and the order signals that shape the offer around it.

House style for every output: Australian English, no em dashes, association language only (never causal).

## Where this sits in the Marketing Coworker

```
eca-hero-product-finder  ->  which product to acquire on
         |
         +-> eca-survey-questions / eca-survey-report   why people buy it
         +-> eca-ad-copywriting / eca-ugc-scripts       the ads for it
         +-> eca-landing-pages                          the page they land on
         +-> eca-meta-ads-4pi                           whether it holds under the break even CPA
```

This is the first question in paid acquisition and the others are downstream of it. It
runs on its own and needs no other skill, but it is worth saying what comes next, because
a hero product with no offer and no ads is a finding nobody acted on.

**Read `brand-data.md` first if `eca-brand-intelligence` has been run.** Not for the
analysis, which is receipt-derived and must stay that way, but for two things around it:
§6 Products for the real product names and variants, which helps spot the aliases in step
4, and §7 Offer and pricing for what has already been tried. Never let the profile
influence the numbers.

## Product vs offer: say this at the start of every run

Members mix these up, and the difference decides what they do next.

- **Product:** the thing they sell. Gut Health Powder, a Cruiser ebike, a Mother's Day gift box.
- **Offer:** the full package a stranger sees: product or bundle, price, deal, and risk reversal. "Starter Kit: 2 tubs and a free scoop, free shipping, 30 day guarantee." One product can carry many offers.

The product decides WHO they acquire. The offer decides WHETHER a cold stranger buys, and whether the first order stays under break even CPA. This skill picks the hero product from data. The member then builds the hero offer around it. Never call the skill's pick an "offer".

## Rule zero: compute, do not estimate
Every number comes from `scripts/hero_product.py`. Never reason about the numbers, sample rows, or eyeball a total. If code execution is not available, say so and stop.

## Steps

1. **Open.** One line: "We're finding which product to acquire customers on, then what your orders say about the offer to wrap around it." Then give the product vs offer definition above in two sentences.

2. **Ask four things, in one message, and wait.**
   - **Store type:** "Do customers usually rebuy (repeat store), mostly buy once (one time purchase, like ebikes or furniture), or buy as gifts (gifting)? Or not sure?"
   - **Break even numbers from their Ecom OS:** "Grab your break even CPA and break even ROAS from your Ecom OS." Members already have these, so never ask them to calculate a margin. If they can only find one, use that one. Only if they have neither, ask for a store wide gross margin % as a fallback. If they have nothing, run without it and say the break even checks were skipped.
   - **Current cost per acquisition on Meta.** **Try to pull it before asking.** If the
     Meta Ads connector is available, get the last 30 days of spend and purchases for the
     account and compute it, then show the number and ask them to confirm rather than
     recall it. Two traps if you do: the connector returns `cost_per_omni_purchase` and
     `omni_purchase` rather than the field names you asked for, and a day with spend and
     no purchases comes back `null` rather than zero. Fall back to asking for the figure
     from Ads Manager, or a target if they don't advertise yet. If they have neither,
     skip it and say the break even check was skipped.
   - **Dataset status:** exactly "Is this real order history from a live business, or an illustrative/synthetic dataset?" Record the answer word for word; it is reproduced at the very end.

3. **Get the data. Choose the path in this order** (exact queries in `references/shopify-queries.md`):

   **a. Shopify connector available?** Set a snapshot `CUTOFF` (current time in UTC). Run the store check query, show the store name and ask "Is this the right store?" Wait for a yes, because the connector can switch stores silently. Record domain, timezone and order count. Then route by order count:
   - **About 300 orders or fewer:** chat path. Pull 50 per page and save each response verbatim as `pages/page_N.json`. Re-check the domain on every page.
   - **More than 300, and bash can reach the internet (Cowork or Claude Code):** bulk path.
   - **More than 300 in plain chat:** say this store is too large to pull reliably here and runs best in Claude Cowork or Claude Code. Offer the CSV route (c) now.

   Then run `scripts/shopify_to_csv.py` with `--expect-count`, `--timezone` and `--domain`. If it prints STOP, relay the reason and stop. The mapping is fixed after this, so skip mapping confirmation in step 4.

   **b. Bulk download fails:** fall back to (c).

   **c. CSV fallback.** Ask for one order history export (see `references/export-guide.md`). Privacy: remove names, addresses, phone numbers and payment details, but **keep the customer identifier** (email, or a hashed ID), because deleting it breaks the analysis.

4. **Inspect and confirm.** Run `python scripts/hero_product.py <file> --inspect`.
   - For a CSV, show row count, columns, first three rows and the guessed mapping, then wait for confirmation.
   - Always show the product name list and ask whether any names are the same product (renames, "KIT" vs no "KIT"). If so, write `aliases.json` and pass `--aliases`. Split names shrink samples and can hide the hero.

5. **Declare the method, then run exactly it.** State before running:
   - First purchase = each customer's earliest order date. Entry product = the highest revenue line item on it. Disclose how many first orders had more than one product.
   - Repeat = an order on a strictly later date within the window: 180 days, or 365 days for gifting (repeat gifting buyers come back for the next occasion, often a year later).
   - Fair time cohort: repeat numbers only count customers whose first purchase is at least one window before the last date in the data. First order economics use every customer.
   - Revenue deduplicated by order ID. Fully refunded, cancelled and voided orders excluded; partial refunds kept. Test orders removed on connector paths. Guest orders with no customer ID left out.
   - Best seller = the product with the most first time customers.
   - Margin comes from the Ecom OS break even ROAS (margin = 1 ÷ break even ROAS), or from break even CPA ÷ average first order value if that's all they have.
   - Each product's break even CPA = its average first order value × margin: the most they can pay for a new customer on that product before the first order loses money. Talk in CPA first, ROAS second.

   Run:
   ```
   python scripts/hero_product.py <file> [mapping] --store-type <repeat|onetime|gifting|auto> \
     [--breakeven-roas 1.67] [--breakeven-cpa 48] [--cpa 45] [--discount discount_code] [--aliases aliases.json]
   # fallbacks if no Ecom OS numbers: [--margin 60] or [--margins margins.json]
   ```
   Use `auto` only when the member said "not sure". If it prints STOP, relay the reason and stop.

6. **Check the store type against the data.** If RESULT_JSON has `type_conflict`, show it plainly (for example "You said repeat store, but only 3% of customers bought again within 180 days") and ask which route to use. Rerun if they change it. Don't argue past one exchange: it is their store.

7. **Show the per product table.** Columns: product, first time customers, first order value, break even CPA for that product, and whether their current CPA is under it (covers = under, close = slightly over, short = well over), and for repeat stores, returned and repeat rate with the sample label (THIN under 30, LIMITED 30 to 99, SOLID 100+). Never show a rate without its sample size in the same row.

8. **Give the result for the route in RESULT_JSON `route`.** Read `references/routes.md` for exactly what to say for each status: HERO, HERO FAILS BREAK EVEN, SHORTLIST, STARTING PRODUCT and NONE.

9. **Give the offer signals.** This is where the product becomes an offer. Read the "Offer signals" section of `references/routes.md` and turn the numbers into two or three specific offer suggestions for the recommended product. Label them as suggestions to test, not findings.

10. **Close with the portable block**, then the dataset status verbatim:

```
HERO PRODUCT FINDING
Store type: [repeat / one time purchase / gifting] ([store repeat rate]% bought again within [window] days)
Status: [HERO / HERO, FAILS BREAK EVEN / SHORTLIST / STARTING PRODUCT / NONE]
Product: [name]  (test against: [second product], SHORTLIST only)
Why it won: [repeat: rate% on n first time customers, confidence floor x%, [ratio]x more likely to buy again than [best seller]] [one time or gifting: highest break even CPA among proven sellers, $[breakeven_cpa] per new customer]
First order: $[value] average
Break even: this product's break even CPA is $[breakeven_cpa] (break even ROAS [x]); your CPA of $[cpa] is [under it / slightly over it / well over it]
Offer to test: [one line, the strongest offer suggestion from step 9]
Provenance: receipt derived, order history [date range], [Shopify connector / CSV export]
```
Dataset status (as declared): "[their answer, word for word]"

Leave out any line whose inputs were not given (no Ecom OS numbers, no CPA). For NONE, write "Product: None, not enough evidence" and leave out the "Why it won" line.

11. **Hand it on.** The finding is the start of the work, not the end of it. Say what
    comes next and name the skill, hedged, because members have different bundles.

    > "You now know which product to acquire customers on. Next is the offer around it,
    > and the ads."

    | Next move | Skill, if installed | What to hand over |
    |---|---|---|
    | Write the ads | `eca-ad-copywriting` | The hero product, its break even CPA, and the offer suggestions from step 9. It builds the 3-2-2 test structure this step used to describe by hand. |
    | Film it | `eca-ugc-scripts` | The product and why customers buy it, for hooks in their own words. |
    | Know why they buy it | `eca-survey-questions`, or `eca-survey-report` if a survey is already running | This skill says *which* product. Those say *why*, which is what the ad copy needs. |
    | Give it a page worth sending traffic to | `eca-landing-pages` (Operations Coworker) | The hero product and the offer to test. |
    | Watch what the ads then do | `eca-meta-ads-4pi` | The break even CPA, as the line the campaign has to stay under. |

    **Offer the brand profile write-back.** If `eca-brand-intelligence` is installed, the
    hero finding belongs in `brand-data.md`: §6 Products marks which one carries
    acquisition, §7 Offer and pricing takes the break even CPA, and §5 Messaging pillars
    takes the angle the winning product implies. Show what would change and let the member
    accept it; never rewrite the profile silently.

## Rules
- Association only. Never say a product "causes" retention.
- Warn that customers bought through Meta usually repeat less than historical customers (history includes word of mouth and loyal fans). Recommend rerunning the skill on the next six months of Meta customers.
- Never recommend a product nobody can scale into (the volume gate).
- Never invent a missing field or a margin. Ask.
- Never analyse data from more than one store, or data whose order count didn't match.
- Only read from Shopify. The bulk export changes nothing in the store.
- The deliverable is the chat answer only. No files.

## What it needs
- Code execution with pandas.
- The Shopify connector (preferred), or an uploaded order export.
- `scripts/shopify_to_csv.py`: connector pages or bulk JSONL to the analysis file, with count, store and test order guards.
- `scripts/hero_product.py`: the analysis. Prints the table and RESULT_JSON; take every number from it.
- `references/routes.md`: what to say for each route and status, and how to read offer signals.
- `references/shopify-queries.md`: validated connector queries.
- `references/export-guide.md`: CSV export locations and column mappings.
- `brand-data.md` from `eca-brand-intelligence`, if installed, for product names and
  pricing history. Never for the numbers.

## Check before finishing
- The product vs offer distinction was stated, and the pick is called a product, never an offer.
- Store type, Ecom OS break even numbers and current CPA were asked; any skipped check is named. Break even is talked about in CPA first.
- The store was confirmed (connector) and `matches_expected: true`.
- Product name aliases were checked.
- Every rate has its n in the same row. Every number matches RESULT_JSON.
- Offer suggestions are labelled as suggestions to test.
- No causal language, no em dashes, Australian spelling. Dataset status quoted word for word.
- The next step named a skill and hedged it with "if installed", and handed over the
  specific finding rather than a general suggestion.
- No unfilled placeholder text reached the member.

---
*Built with the TEACH framework. Hone it: run it on a real store, see what it gets wrong, and tune the steps or sharpen the trigger above.*
