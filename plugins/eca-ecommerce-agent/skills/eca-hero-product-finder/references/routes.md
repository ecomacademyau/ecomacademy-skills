# Routes, statuses and offer signals

Read the `route` and `status` fields in RESULT_JSON and follow the matching section. Every number comes from RESULT_JSON.

## Repeat route (`route: repeat`)

Give three outputs first:
- **Volume winner:** most returning customers in absolute terms (`volume_winner`). Usually just the biggest product.
- **Rate winner:** highest raw repeat rate with its sample size (`rate_winner`). If THIN or LIMITED, say plainly that a handful of customers can fake an impressive percentage.
- **Hero product:** the product that cleared all three gates: at least 100 first time customers, at least 10% of the best seller's first time customers, and the best Wilson lower bound (confidence floor) among the survivors. Name any higher rate product the gates knocked out and which gate it failed (`excluded_higher_rate`).

Then compare with the best seller: "A customer starting on [hero] is [ratio_vs_bestseller] times as likely to buy again within [window] days as one starting on [bestseller_in_cohort]." If `same_as_bestseller` is true, say the best seller is also the hero, which is a good result: the product that sells most also brings people back.

### Status HERO
The hero clears the repeat gates, and either no CPA was given or their CPA is under (or close to) the product's break even CPA, alone or once repeat profit is counted. Recommend it.

### Status HERO, FAILS BREAK EVEN
The hero brings the best customers back, but their CPA is well over its break even CPA, even counting repeat profit. Say it directly: "This is the product your best customers start on, but at a $[cpa] CPA against a $[breakeven_cpa] break even CPA, it loses money on the budget you have." Then:
- If `floor_safe_alternative` exists, name it as the product to start with now.
- Either way, point to the offer: a bundle or a higher value first order is how the hero clears the floor. Lifting the first order value lifts the break even CPA. This is the clearest case of the offer doing the work the product can't.

### Status NONE
No product clears the gates. Say "not enough evidence yet" is a correct answer. Recommend starting with the best seller if its floor is not "short", and rerunning in six months.

## One time purchase and gifting routes (`route: onetime` or `gifting`)

Repeat rate is not the decision here. A low repeat rate is normal for these stores, not a problem.

### Status SHORTLIST
Products are ranked on break even CPA, which is first order profit (or on first order value if no Ecom OS numbers or margin were given, per `ranked_on`) among proven sellers: at least 30 first time customers and at least 10% of the best seller's volume. Show the shortlist, then:
- Recommend testing the first two in `test_first` against each other in one campaign, not all three. Small budgets can't split three ways and still get a clear winner. Keep the one with the best profit after ad cost after at least two to three weeks.
- Remind them that a high ticket product can convert worse from a cold scroll. Profit per order ranks the options; Meta decides between them.

### Status SHORTLIST, ALL FAIL BREAK EVEN
Their CPA is over the break even CPA of every proven product. With no repeat purchases to recover it, the offer has to fix it: raise first order value (bundle, accessories, premium version) or lower the cost per customer. Say this plainly.

### Gifting only
Show `first_orders_by_month_pct` as the occasions that drive the store (for example "35% of first orders land in November and December, 15% in May"). Their buyers come back for the next occasion, so plan campaigns around those peaks. Use "mum" and "mums" in any marketing language (Mother's Day, mum gifts).

## Starting product (any route, `status: STARTING PRODUCT`)
Too few customers, or history shorter than the window. Say: "You don't have enough orders yet to prove a hero. Start with your best seller: it has already shown it sells." Compare their CPA with its break even CPA, and tell them to rerun the skill in six months.

## Offer signals

Turn these into two or three specific offer suggestions for the recommended product. They are suggestions to test, not findings.

- **Break even CPA vs actual CPA** (`breakeven_cpa`, `floor`, `cpa`): if their CPA is over the product's break even CPA ("short" or "close"), the offer needs to lift the first order value, which lifts the break even CPA. Suggest a bundle, a starter kit, or a threshold (free shipping over a value above the current average).
- **Multi item first orders** (`multi_item_first_pct` in the table): if a meaningful share of first orders already contain more than one item, customers are bundling on their own. A bundle offer formalises what they already do.
- **Discount vs full price first orders** (`offer_signal_discount_hero`, or store wide `offer_signal_discount`): if customers whose first order used a discount code come back noticeably less than full price customers, don't lead the offer with a discount. Lead with value instead: bundle, bonus, guarantee. If they come back about the same, a first order discount is fine. Say this is association: discount buyers may differ for other reasons, and the store wide figure is mixed across products.
- **One time purchase stores:** the offer is about removing risk from a big decision: guarantee, free returns, finance options, a test ride or trial. Accessories bought later are a bonus, not the plan.
- **Gifting stores:** the offer is about the occasion and the deadline: order by dates, gift wrap, a card, delivery promises before the occasion.

Never present an offer suggestion as something the data proves. The data shows what customers did; the offer is what the member tests next.
