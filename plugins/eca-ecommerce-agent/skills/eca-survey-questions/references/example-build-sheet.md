# Worked example: finished build sheet

> **Fictional brand, illustrative only.** This shows the format, depth and specificity to aim for. Never copy these questions' answers into a real brand's survey; every real answer must come from that brand's own evidence log.

---

## Fern & Field post-purchase survey build sheet

**Snapshot**
- **Data used:** brand DNA file, 186 reviews (Judge.me export), PDPs, FAQ, shipping policy, Shopify CSV (last 12 months). No ad comments supplied, so objection wording leans on reviews and FAQ.
- **Diagnosis:** Australian natural deodorant. Multi-channel (Meta ads, organic TikTok, 9 independent stockists). Problem-solving product. Competitive category. Not a gifting brand (fewer than 3% of reviews mention gifts).
- **In:** attribution (Meta, TikTok and stockists overlap), problem question (strong persona signal for a problem-solving product).
- **Out:** who are you buying for (not gifting), alternatives considered (cut by the 5-question cap), what would you love to see (asked to returning customers instead).

---

### New customer survey
*Longest path: 5 questions*

**Q1. How did you first hear about us?**
- **Type:** Single-select · **Randomise:** Yes, pin "Other" last · **Required:** Yes
- **Answers:**
  - Instagram
  - Facebook
  - TikTok
  - Friend or family recommendation
  - Google search
  - AI assistant (ChatGPT, Gemini, etc.)
  - In a store near me
  - Other (please specify) *(pinned)*
- **Logic:** All answers → Q2
- **Why we ask:** Meta reporting can't see TikTok, stockists or word of mouth. This shows where demand actually starts before we shift budget.

**Q2. What made you decide to buy from us?**
- **Type:** Single-select · **Randomise:** Yes, pin "Other" last · **Required:** Yes
- **Answers:**
  - Aluminium-free, built to actually work
  - No baking soda, made for sensitive skin
  - The scents sounded amazing
  - Refillable, less plastic
  - The reviews convinced me
  - Australian made
  - Other (please specify) *(pinned)*
- **Logic:** All answers → Q3
- **Why we ask:** the top answer becomes the lead angle for ads and the PDP headline.

**Q3. What almost stopped you from buying today?**
- **Type:** Single-select · **Randomise:** Yes, pin "Nothing" and "Other" last · **Required:** Yes
- **Answers:**
  - Not sure natural deodorant would work for me
  - Worried about smelling during the switch
  - The price compared to supermarket deodorant
  - The shipping cost
  - Not sure which scent to pick
  - Nothing, it was an easy yes *(pinned)*
  - Other (please specify) *(pinned)*
- **Logic:** "work for me" → Q3a · "during the switch" → Q3b · "price" → Q3c · "shipping" → Q3d · "scent" → Q3e · Nothing / Other → Q4
- **Why we ask:** each objection maps to a fix: an ad angle, a PDP section, an FAQ entry or an offer change. Read results as objections buyers overcame.

**Q3a. What made you unsure it would work for you?** *(only shown if "work for me")*
- **Type:** Multi-select · **Randomise:** Yes, pin "Other" last · **Required:** Optional
- **Answers:**
  - Other natural deodorants failed me before
  - I sweat a lot or have an active job
  - Australian summers feel too hot for it
  - The results looked too good to be true
  - Other (please specify) *(pinned)*
- **Logic:** → Q4

**Q3b. What worried you about the switch?** *(only shown if "during the switch")*
- **Type:** Multi-select · **Randomise:** Yes, pin "Other" last · **Required:** Optional
- **Answers:**
  - Didn't know how long the adjustment takes
  - Worried about smelling at work
  - Didn't know if the adjustment period is real
  - No clear guide on what to expect
  - Other (please specify) *(pinned)*
- **Logic:** → Q4

**Q3c. What made the price feel like a hurdle?** *(only shown if "price")*
- **Type:** Multi-select · **Randomise:** Yes, pin "Other" last · **Required:** Optional
- **Answers:**
  - I'm on a tight budget at the moment
  - Wasn't sure it was worth it until I tried it
  - Not sure how long one stick lasts
  - Supermarket deodorant is much cheaper
  - Other (please specify) *(pinned)*
- **Logic:** → Q4

**Q3d. What was the concern with shipping?** *(only shown if "shipping")*
- **Type:** Multi-select · **Randomise:** Yes, pin "Other" last · **Required:** Optional
- **Answers:**
  - Shipping cost was too high for one item
  - Didn't want to spend $60 to get free shipping
  - Delivery would take too long
  - Other (please specify) *(pinned)*
- **Logic:** → Q4

**Q3e. What made it hard to choose a scent?** *(only shown if "scent")*
- **Type:** Multi-select · **Randomise:** Yes, pin "Other" last · **Required:** Optional
- **Answers:**
  - Can't smell it before buying
  - Scent descriptions weren't clear enough
  - Too many scents to choose from
  - Worried it would be too strong
  - Other (please specify) *(pinned)*
- **Logic:** → Q4

**Q4. What were you hoping our deodorant would help you with?**
- **Type:** Open text · **Randomise:** n/a · **Required:** Optional
- **Logic:** → End
- **Why we ask:** the customer's own words for the problem, ready to use in hooks and for building personas.

---

### Returning customer survey
*Longest path: 4 questions*

**Q1. What brought you back today?**
- **Type:** Single-select · **Randomise:** Yes, pin "Other" last · **Required:** Yes
- **Answers:**
  - I ran out
  - I wanted to try a new scent
  - I loved how well it worked
  - There was a sale or offer
  - An email or text reminded me
  - Other (please specify) *(pinned)*
- **Logic:** → Q2
- **Why we ask:** shows whether retention runs on replenishment, range or offers, which shapes the email and SMS flows.

**Q2. What do you love most about our products?**
- **Type:** Open text · **Required:** Optional · **Logic:** → Q3
- **Why we ask:** the lead benefit for people who stay. Compare with Q2 of the new customer survey.

**Q3. What else would you love us to make?**
- **Type:** Open text · **Required:** Optional · **Logic:** → Q4
- **Why we ask:** new product and bundle ideas.

**Q4. How could we make your experience with us, or with our products, even better?**
- **Type:** Open text · **Required:** Optional · **Logic:** → End
- **Why we ask:** product and customer experience fixes.

---

### Branching map

```
NEW CUSTOMER
Q1 → Q2 → Q3 ┬ work for me    → Q3a ┐
             ├ the switch     → Q3b ┤
             ├ price          → Q3c ├→ Q4 → End
             ├ shipping       → Q3d ┤
             ├ scent          → Q3e ┤
             └ Nothing / Other ─────┘

RETURNING CUSTOMER
Q1 → Q2 → Q3 → Q4 → End
```

---

### Evidence log (condensed)

| Answer option | Question | Source |
|---|---|---|
| Aluminium-free, built to actually work | Q2 | 41 reviews ("why I bought" lines), PDP claim |
| No baking soda, made for sensitive skin | Q2 | 27 reviews, PDP claim |
| The scents sounded amazing | Q2 | PDP scent descriptions, 11 reviews say they chose it for the scent |
| Refillable, less plastic | Q2 | 12 reviews, brand DNA |
| Australian made | Q2 | Brand DNA, 8 reviews |
| Not sure natural deodorant would work for me | Q3 | 22 reviews ("I was sceptical") |
| Worried about smelling during the switch | Q3 | FAQ, 14 reviews mention adjustment |
| The price compared to supermarket deodorant | Q3 | 9 reviews, category standard |
| The shipping cost | Q3 | Shipping policy ($9.95 under $60), category standard |
| Not sure which scent to pick | Q3 | 5 scents on site, 6 reviews |

---

### Setup checklist (any survey tool)

- [ ] Two separate surveys: first-time customers and returning customers.
- [ ] Randomised order on Q1 to Q3 and Q3a to Q3e (new) and Q1 (returning), with "Other" and "Nothing" pinned last.
- [ ] Branching from Q3 to Q3a to Q3e; "Nothing" and "Other" go straight to Q4.
- [ ] "Other (please specify)" has a text box everywhere.
- [ ] Placed on the thank you / order status page.
- [ ] Previewed on mobile.
- [ ] Run for at least 30 days without edits before reading results.

---

### Left out

| Question | Why it was left out | Swap it in if... |
|---|---|---|
| Who are you buying for? | Not a gifting brand | Gift sales grow, or ahead of Mother's Day or Christmas |
| What else did you consider? | Cut by the 5-question cap | You plan "us vs supermarket" comparison ads; swap it for Q4 |
| What would you love to see from us? (new) | Returning customers answer it better | Never for new customers while the cap is 5 |
