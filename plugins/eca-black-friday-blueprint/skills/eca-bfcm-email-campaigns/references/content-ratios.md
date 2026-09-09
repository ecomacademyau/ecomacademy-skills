# Suggested ratios per content type

Source: the member's own reference guide. This is the **baseline mix** for a sale-period email calendar — not a hard rule. Always confirm with the member before locking a calendar built on it (see SKILL.md Stage 4).

| Content type | Ratio |
|---|---|
| Hero | 30% |
| Product | 40% |
| Education | 20% |
| Plain text | 10% |

## Turning the ratio into slot counts

1. Work out the total number of email slots: `(sale window in days ÷ days-per-send) `, rounded to a sensible whole number, using the member's chosen cadence.
2. Multiply the total by each ratio and round to the nearest whole email. If rounding creates a mismatch against the total, adjust the **Product** count first (it's the largest bucket and the least sensitive to being off by one) so the slot count still matches the total exactly.
3. For very short calendars (roughly 5 slots or fewer), the ratio can't be followed literally — instead keep the *shape* it implies: open and close on Hero (launch + last chance), put the single strongest sell in Product, and use Education/Plain text only if there's room. Say plainly when the ratio has been approximated for a short calendar rather than applied precisely.
4. Always place a Hero email at the very start (launch) and the very end (last chance/reminder) of the sale window regardless of where the ratio math lands — these are the two highest-leverage sends in any sale and shouldn't be crowded out.
5. **Align every slot to a phase.** `bfcm/bfcm-<year>-calendar.csv` always exists (this skill does not run without the Offer Builder), and it defines the phases: LIST_BUILD, EARLY_ACCESS, WARM_UP, SALE_LIVE, BLACK_FRIDAY, WEEKEND, CYBER_MONDAY, POST_SALE. Place a Hero at each phase transition and fill the space between with Product and Education. Record the phase ID against every slot, never just the date — if the member moves the launch, the phases move and the emails follow.

Show the resulting slot breakdown to the member in plain terms (e.g. "12 emails total: 4 Hero, 5 Product, 2 Education, 1 Plain text") before filling in topics, so they can sanity-check the shape before you populate it.
