# Build sheet template

Deliver this straight in chat. Keep the section order. Replace everything in [brackets]. Each question uses the same block so it can be set up line by line in any survey tool.

---

## [Brand] post-purchase survey build sheet

**Snapshot**
- **Data used:** [e.g. brand DNA file, 214 reviews, website PDPs, FAQ and shipping policy, Shopify CSV]. [Note anything missing and which answers are lower confidence because of it.]
- **Diagnosis:** [e.g. multi-channel (Meta, TikTok, two markets), competitive category, problem-solving product, not a gifting brand.]
- **In:** [conditional questions included and the one-line reason for each.]
- **Out:** [conditional questions cut and why. Full list in "Left out" below.]

---

### New customer survey
*Longest path: [X] questions*

**Q1. [Question wording]**
- **Type:** [Single-select / Multi-select / Open text] · **Randomise:** [Yes, pin "Other" last / No] · **Required:** [Yes / Optional]
- **Answers:**
  - [Option]
  - [Option]
  - Other (please specify) *(pinned)*
- **Logic:** [All answers → Q2]
- **Why we ask:** [the decision this informs, one line]

*[Repeat the block for each question.]*

**Q[n]. What almost stopped you from buying today?**
- **Type:** Single-select · **Randomise:** Yes, pin "Nothing" and "Other" last · **Required:** Yes
- **Answers:**
  - [Objection A]
  - [Objection B]
  - [Objection C]
  - [Objection D]
  - Nothing, it was an easy yes *(pinned)*
  - Other (please specify) *(pinned)*
- **Logic:** [Objection A] → Q[n]a · [Objection B] → Q[n]b · [Objection C] → Q[n]c · [Objection D] → Q[n]d · Nothing / Other → Q[next]
- **Why we ask:** [one line]

**Q[n]a. [Follow-up for objection A]** *(only shown if "[Objection A]")*
- **Type:** Multi-select · **Randomise:** Yes, pin "Other" last · **Required:** Optional
- **Answers:**
  - [Option]
  - [Option]
  - [Option]
  - Other (please specify) *(pinned)*
- **Logic:** → Q[next]

*[Repeat for each objection follow-up.]*

---

### Returning customer survey
*Longest path: [X] questions*

*[Same block format for each question.]*

---

### Branching map

```
NEW CUSTOMER
Q1 → Q2 → Q3 → Q4 ┬ [Objection A] → Q4a ┐
                  ├ [Objection B] → Q4b ┤
                  ├ [Objection C] → Q4c ├→ Q5 → End
                  ├ [Objection D] → Q4d ┤
                  └ Nothing / Other ────┘

RETURNING CUSTOMER
Q1 → Q2 → Q3 → Q4 → End
```

---

### Evidence log (condensed)

| Answer option | Question | Source |
|---|---|---|
| [Option] | [Q3] | [e.g. 31 reviews mention it] |
| [Option] | [Q4] | [e.g. FAQ page, 6 reviews] |
| [Option] | [Q4] | Category standard |

*Only list options that came from data or are category standards. If an option can't go in this table, it shouldn't be in the survey.*

---

### Setup checklist ([tool name, or "any survey tool"])

- [ ] Two separate surveys: one shown to first-time customers, one to returning customers. Confirm your tool can target by first order vs repeat order.
- [ ] Randomised answer order switched on for every multiple-choice question, with "Other" and "Nothing" pinned last. If your tool can't randomise, flag it: the top options will be over-picked and the results skewed.
- [ ] Branching set up for every objection follow-up, and "Nothing" / "Other" skip straight to the next question. If your tool can't branch, replace all follow-ups with one optional open question: "Tell us a bit more about what nearly stopped you."
- [ ] "Other (please specify)" has a text box on every question.
- [ ] Placed on the thank you / order status page so it shows straight after purchase.
- [ ] Previewed on mobile: every question fits without scrolling.
- [ ] Don't change questions mid-run. Run for at least 30 days, and ideally 100+ responses per survey, before acting on the results.
- [ ] Read the objection results as "objections buyers overcame". People who left without buying aren't in this data.

---

### Left out

| Question | Why it was left out | Swap it in if... |
|---|---|---|
| [Question] | [e.g. cut by the 5-question cap] | [e.g. you care more about personas than channel mix right now] |
