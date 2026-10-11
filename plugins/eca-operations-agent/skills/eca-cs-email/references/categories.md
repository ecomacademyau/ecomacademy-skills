# Categories, and how each is handled

The inbox is not one job. A refund request, a stockist enquiry and a press request need
different tone, different information and different people. Sorting first is what stops
every reply sounding like the same form letter.

Config decides which categories a store cares about. These are the defaults.

| Category | What it looks like | Handling |
|---|---|---|
| `order-status` | Where is it, has it shipped, tracking | Answer from the order record, and give the member an admin link to it. Candidate for automation once learned. |
| `shipping` | Delivery times, costs, destinations, cut-offs | Answer from published policy. Candidate once learned. |
| `product-question` | How to use it, what is in it, which to choose | Answer from product data and brand knowledge. Draft, do not automate: the wrong answer here is a health or allergy answer. |
| `returns-refunds` | Wants money back, wrong item, damaged | **Always draft.** Money and goodwill. |
| `complaint` | Unhappy, angry, disappointed, threatening a review | **Always draft, flag to the member first.** Often wants a person, not a reply. |
| `wholesale` | Shop wanting to stock the brand | Draft from the wholesale terms in config. High value, usually deserves a human. |
| `creator-collab` | Sample requests, usage rights, paid content | **Always draft.** It is a commercial negotiation, not a ticket. Terms are the member's call. |
| `press-partnership` | Media, podcasts, brand partnerships | Summarise and hand to the member. Do not draft unless asked. |
| `supplier-ops` | Suppliers, 3PL, manufacturing | Not customer service. Summarise and route. |
| `spam-noise` | Cold outreach, SEO pitches, scrapers | Count it, name it, never draft. |

**When a message does not fit, say so** rather than forcing it into the nearest box. An
`unclassified` pile the member can glance at is more useful than confident misfiling.

**One message can be two categories.** A complaint that is also a refund request is both,
and the handling is the stricter of the two.

## Writing the reply itself

- **Load the brand voice first.** If `eca-brand-intelligence` is installed, read
  `brand-data.md`. Otherwise read the last several replies the member actually sent and
  match those. Never invent a house style.
- **Sign it the way config says.** The default name, or the per-category exception where
  there is one — complaints and wholesale often come from the founder rather than the
  team, because the customer should feel they reached someone who can decide. A reply
  signed by the wrong person is immediately obvious to a repeat customer, and signing as
  a person who does not exist is found out the moment someone asks for them by name.
- **Answer the question that was asked.** Then stop. A reply that also upsells reads as a
  reply that did not care.
- **Apologise only when there is something to apologise for.** A reflexive "sorry for the
  delay" on a same-day reply devalues the real one.
- **Flag, do not guess.** If the answer needs something only the member knows, write what
  can be written and mark the gap plainly rather than filling it.
