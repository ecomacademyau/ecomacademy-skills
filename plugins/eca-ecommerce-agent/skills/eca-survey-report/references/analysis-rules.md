# Analysis rules

Apply these every run so reports stay honest and comparable.

## 1. Periods

- **All-time** runs from the survey launch date to the end of the report period. It is the main lens.
- **This period** is the last full calendar month by default (or the last full fortnight for brands with 50+ new customer answers a fortnight). A partial period is never reported.
- Use the brand's timezone for boundaries.
- If a question's wording or answer list changed, all-time for that question starts at the change date. Say so in the method.
- A period with almost no answers (a collection outage) is reported as such in the method and the "this period" view shows "Too few answers yet" automatically.

## 2. Counts, not percentages

Supply raw counts for every answer, plus the number of people who answered the question (`n`). The build script calculates every percentage.
- Single-select: share = answer count / people who answered.
- Multi-select: share = people choosing the answer / people who answered. Shares add to more than 100%.

## 3. Signal tags (calculated by `scripts/signals.py`)

**How sure we are about a share (all-time):**
| Tag | Rule | Meaning for the reader |
|---|---|---|
| Strong signal | 100+ answers and 15+ choosing it | Safe to act on |
| Early signal | 30+ answers and 5+ choosing it | Act on it, keep watching |
| Too few answers yet | anything smaller | Read as a clue, not a finding |

**What is new this period (this period against the rest of all-time):**
| Tag | Rule |
|---|---|
| Strong signal | clear difference (two-proportion test, p < 0.05) |
| Early signal | likely difference (p < 0.20) |
| No real change | within normal variation |
| Too few answers yet | under 20 answers this period or in the rest of all-time |

The report never shows p values or confidence intervals. Write insights to match the tags: never call a "No real change" a trend, never build an action on a "Too few answers yet" share alone (it can support an action that stands on something stronger).

## 4. Written answers

Read every open-text and "Other" answer for all-time; note which fall in this period.
- Bucket into themes in the customer's language ("couldn't tell how it smells", not "product uncertainty").
- Count each answer once per theme; an answer can carry two themes.
- Keep 2 to 3 of the best quotes per theme for the objection cards and the language bank.
- Map clear "Other" answers back to an existing option's theme and count them there, stating it in the method.
- If a reason keeps appearing in writing but has no answer option, flag it in "questions to consider".

## 5. Small numbers

Follow-up questions (shown only to people who picked an objection) always have small bases. Read them as what people said, not how many. Show them on all-time where possible.

## 6. Product segmentation

From the Shopify line items attached to responses:
- One basket per respondent. A basket with several lines counts to the line with the highest value; state how many were mixed.
- Map products to lines with the config. Unmapped products go to "Other" and are listed in the method.
- Only call out a product-line difference when the line has 30+ baskets.

## 7. New versus returning

Compare only questions with the same wording and answers in both surveys.

## 8. Objections buyers overcame

Everyone in this data bought. The objection results show friction people pushed through, not the friction that lost sales. Say so in the objections section. If the brand needs the lost-sale view, recommend an exit-intent survey on the main product page in the action plan.
