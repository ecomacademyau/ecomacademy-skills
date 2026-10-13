---
name: eca-survey-questions
description: "Craft a tailored post-purchase survey for any ecommerce brand, new customer and returning customer, with every question and answer option mined from the brand's real data: the eca-brand-intelligence profile where it exists, plus reviews, website, Shopify and market research. Delivered in chat as a build sheet to set up by hand in Zigpoll, UserLoop or any survey tool. Use whenever someone mentions a post-purchase survey, PPS, Zigpoll or UserLoop questions, what should we ask our customers, how did you hear about us, HDYHAU, attribution survey, objection survey, what almost stopped you buying, purchase motivation, why do people buy from us, voice of customer survey, new versus returning customer survey, or set up a survey for a brand. Also trigger when someone wants to uncover their real objections, marketing angles or personas from customer feedback, even if they never say survey. Pairs with eca-survey-report, which analyses the answers."
---

# ECA Survey Questions

Build a post-purchase survey that is short enough to get answered and specific enough to change decisions. Every answer option comes from the brand's own data, never from a generic template. The output is a build sheet in chat that anyone can set up by hand in Zigpoll, UserLoop, KnoCommerce, Fairing or any other survey tool. This skill does not use any survey tool API or MCP.

The survey exists to answer three questions for the brand:

1. **Objections:** what almost stopped people buying, so we can counter it in ads, on the PDP, in the FAQ and in the website experience.
2. **Purchase motivation:** the main reason people buy, so we know which angle to lead with.
3. **Personas:** who they are, who they buy for and what problem they are solving.

Plus attribution where channels overlap. If a question does not feed one of these, cut it.

## Where this sits in the Marketing Coworker

`eca-brand-intelligence` tells you what the brand believes about its customers.
**This survey tests it against what customers actually say**, and
`eca-survey-report` turns the answers into angles, objections and personas that feed the
rest of the bundle.

```
eca-brand-intelligence  ->  eca-survey-questions  ->  (answers come in)  ->  eca-survey-report
       the hypothesis            the instrument                              the evidence
```

Run brand intelligence first where possible. A survey written from the brand's own data
asks sharper questions than one written from a blank page, and the questions aim at what
the profile is least sure of.

It runs perfectly well without it. Say which you are on, because a survey built from the
website alone has weaker answer options and should say so.

## When to use this

Any time someone wants to set up, rewrite or improve a post-purchase survey, or wants to find out why customers buy, what holds them back or where they heard about the brand. Works for any brand. If the person asks to analyse survey responses they already have, that is a different job; say so and stop.

## Steps

### 1. Confirm the brief (keep it quick)

Before asking anything, check what you already have: brand files, earlier conversation, uploads. Then confirm only what is missing:
- Which brand (and its website URL).
- Which survey: new customer, returning customer, or both. Default to both.
- Which marketing channels the brand runs: Meta, Google, TikTok, influencers, PR,
  podcasts, affiliates, email, retail stores, markets, wholesale. **Check `brand-data.md`
  §17 first** and confirm what is there rather than asking cold. Only ask outright when
  there is no brand profile, since this is rarely visible in the data.
- Which tool they will build in. This only affects the setup notes.

### 2. Gather the data

Read sources in this order and keep an **evidence log** as you go: every candidate motivation, objection, problem, alternative and audience, with how often it shows up and where.

- **Brand files first.** If `eca-brand-intelligence` has been run, `brand-data.md` already
  holds most of what this step is for. Read it before anything else and take:

  | Section | What it gives this survey |
  |---|---|
  | **§2 Why people buy & the transformation** | motivation options, in customer language |
  | **§9 Objections → rebuttals** | the objection list, already mined from reviews |
  | **§12 ICP & personas** | who to write for, and whether the "who are you buying for" question qualifies |
  | **§3 Voice & tone** | how options should read, and the market's spelling |
  | **§6 Products** | real variants, shades, sizes for the specific options |
  | **§7 Offer & pricing** | whether price belongs in the objection list |
  | **§11 Competitors** | the alternatives-considered options, as solution types |
  | **§13 Operational facts** | the shipping threshold and returns policy the follow-ups need |
  | **§17 Channels** | **the attribution answer list**, which otherwise has to be asked for |
  | **§18 Sources & confidence** | which of the above is solid and which is a guess |

  §17 and §13 are the two that save the most time: the channel list is normally a question
  to the member, and the follow-ups need the real shipping threshold rather than a
  placeholder.

  **Treat §18 honestly.** Anything marked low confidence in the brand profile is a
  hypothesis, and a survey is exactly the instrument for testing it. Prefer those as
  answer options and note them in the evidence log as "to be confirmed by this survey".

  If there is no `brand-data.md`, also look for `brand/brand-dna.md`, `brand/icp-cards.md`
  and `brand/brand-voice.md`, or any persona files. Use whatever exists; never ask the
  person to recreate what they already have.
- **Reviews.** A review export (Judge.me, Okendo, Yotpo, Loox, Shopify reviews) or the
  reviews visible on product pages. Two routes worth trying before asking for an export:
  a reviews connector if one is set up, and the brand's own inbox, since Judge.me emails a
  notification per review whose subject parses as `<Name> left a <N> star review for
  '<Product>'` with the text in the body. If `eca-persona-builder` has been run, its
  personas were built from these same reviews; read them rather than re-mining from zero.
  - 4 and 5 star reviews hold two different kinds of sentence. Log them separately:
    - **Why they bought:** "I bought these because...", "I'd been looking for...", "After years of extensions...". These feed new customer motivation, problems solved and who it is for.
    - **What happened after:** "they stayed on all day", "so light I forgot I had them on". These show which benefits matter, but they describe an experience a new customer hasn't had yet. Use them to choose benefits, then rewrite them as the promise (step 5).
  - 1 to 3 star reviews give objections and disappointments.
  - Hunt for "I was sceptical", "I almost didn't", "I was worried", "I wasn't sure". These are objections buyers overcame, which is exactly what the survey measures.
- **Website.** The PDP headline and claims are the promise new customers bought into, so read them closely. Also the homepage promise, PDPs (price, variants, sizing or shades, ingredients or materials, how to use), FAQ (every FAQ is a known objection), shipping and returns policy (costs, thresholds, delivery times, international), and which trust signals are present or missing.
- **Shopify** (connector or CSV export if available). Product range and price points, AOV, top sellers, new vs returning split, countries shipped to, sales channels (online, POS, wholesale), gift note or gift wrap usage.
- **Market.** Search for competitor reviews (their complaints are category objections), Reddit and forum threads about the category, and what people use instead. Meta ad comments are gold for objections if the person can paste them.

**Minimum to proceed:** website URL plus reviews (export or visible on site). With less than that, say so, proceed, and mark the affected answer options as lower confidence.

### 3. Diagnose the business

Decide which conditional questions qualify. Full wording and answer guidance for each is in `references/question-bank.md`.

| Question | Include when | Skip when |
|---|---|---|
| How did you hear about us? | **Default: include.** Any brand with more than one channel, organic social, word of mouth, influencers, PR, retail, markets or wholesale. | Only if truly single-channel: one paid channel and nothing else. "Meta says most sales come from Meta" is NOT a reason to skip; platform reporting over-claims. |
| Who are you buying for? | Gifting brands, or reviews regularly mention buying for someone else, or gift wrap/notes are offered, or sales spike at gifting moments (Mother's Day, Christmas). | Products clearly bought for personal use, with reviews to back it up. |
| What did you consider before buying from us? | Categories with real substitutes where people compare (skincare, tanning, supplements, haircare, mattresses, apparel basics). | Impulse, novelty or low-price buys, or products with no clear alternative. |
| What problem are you trying to solve? | Products that solve a problem (thinning hair, sleep, skin concerns, pain, mess, time). | Pure aesthetic, fashion or gift purchases. |

### 4. Pick the questions within the length cap

**Hard cap: no single respondent sees more than 5 questions.** Count the longest path. A branched follow-up counts for the people who see it.

**New customer survey.** Always include the core three:
- Why did you buy from us? (motivation)
- What almost stopped you from buying? (objection)
- The objection follow-up (branched, so each person sees only one)

Fill the remaining 2 slots in this priority order, using only questions that qualified in step 3:
1. How did you hear about us? (one-tap warm-up, almost always earns a slot)
2. Who are you buying for? (gifting brands)
3. What problem are you trying to solve? (problem-solving products, strongest persona signal)
4. What did you consider before buying from us? (competitive categories)
5. What would you love to see from us? (usually cut here, because returning customers answer it better after using the product)

If the person has told you their biggest current problem, let it break ties. Conversion problem: objection and problem questions win. Channel mix or scaling decision: attribution wins.

**Order on screen:** attribution, who for, motivation, alternatives considered, objection, objection follow-up, open question last. Easy taps first, open text last.

**Returning customer survey** (fits within the cap):
1. What made you come back? (single-select, the repurchase trigger, feeds retention flows)
2. Who are you buying for? (only if it qualified in step 3)
3. What do you love most about our products? (open)
4. What else would you like to see from us? (open, feeds new product ideas)
5. How can we make your experience with us even better? (open, feeds product and CX fixes)

Record every question you cut and why, for the "Left out" section of the build sheet.

### 5. Write the answer options

- **Mine, don't invent.** Every option must trace to the evidence log. A few options are category standards (price, shipping cost); tag those as "category standard" rather than pretending they came from reviews.
- **Customer language.** Use the words from reviews. "My tan always goes patchy" beats "Uneven application concerns".
- **Match the customer's moment.** The new customer survey shows on the thank you page, before the parcel arrives. Every new customer option must describe what they wanted, expected or were convinced by (a promise, a feature, a price comparison, social proof, an offer), never how the product performed. Test each option by reading it as someone whose order hasn't shipped: if they couldn't know it yet, rewrite it as the promise or cut it.
  - "They stay put all day" becomes "Lashes that last all day".
  - "So light I can't feel them" only stays if the evidence shows people buy for it, reworded as a promise ("Lighter than extensions"). Otherwise cut it.
  - Returning customer options can describe experience, because they have it.
- **Specific beats generic.** "Not sure which shade suits my skin" beats "Product uncertainty". "Shipping cost to the US" beats "Shipping".
- **4 to 7 options plus "Other (please specify)".** Fewer than 4 means reasons are missing; more than 7 and people stop reading on mobile.
- **Short.** Aim for under 8 words per option.
- **No overlap.** In single-select lists, no two options can mean the same thing.
- **One reason per option.** "No glue, on in minutes" is two reasons, and they are two different ad angles. If it wins, you won't know which to run. Split it, or keep the one with more evidence.
- **Never name competitors.** Use solution types: "A salon spray tan", "Another self-tan brand", "Doing nothing and waiting".
- **Match the brand's market.** Australian brands get Australian English and "mum", not "mom". US brands get US spelling. Never use em dashes in survey copy.
- **Select type rules:**
  - Single-select: attribution, who for, motivation, the main objection question, what made you come back. Motivation is single-select on purpose: it forces the main reason, which is the main angle.
  - The main objection question MUST be single-select, or branching breaks because the tool cannot pick which follow-up to show.
  - Multi-select: alternatives considered and the objection follow-ups.
- **Randomise every multiple-choice question.** This is non-negotiable; position bias otherwise inflates whatever sits at the top. Always pin "Other (please specify)" and "Nothing" style options to the bottom.
- **The objection "nothing" option** should sound warm and natural, for example "Nothing, it was an easy yes". It skips the follow-up.

For attribution: split platforms people can name (Instagram, Facebook and TikTok as separate options), always include "Friend or family recommendation", "Google search" and "AI assistant (ChatGPT, Gemini, etc.)", and add only the channels this brand actually runs. Details in `references/question-bank.md`.

### 6. Write the objection follow-ups

Write one follow-up for every objection option except "Nothing" and "Other". Each follow-up:
- Is shown only to people who picked that objection (branching).
- Is multi-select, with 3 to 6 options plus "Other (please specify)".
- Asks why that objection mattered, in plain words. "What made the price feel like a hurdle?" not "Please elaborate on your price objection".
- Uses the starter banks in `references/objection-followups.md`, rewritten with this brand's specifics: their shipping threshold, their returns policy, their real product variants.

### 7. Deliver the build sheet in chat

Follow `templates/build-sheet.md` exactly. Deliver it straight in the chat, not as a file, unless the person asks for one. It contains: a brand snapshot (data used, diagnosis, what's in and out), the new customer survey, the returning customer survey, the branching map, a condensed evidence log, the tool setup checklist, and the "Left out" section.

For a fully worked example of the finished output, see `references/example-build-sheet.md`.

**Tell them what happens next.** Once the survey has answers, `eca-survey-report` turns
them into angles, objection counters and personas. Mention it in one line at the end, and
say roughly when it is worth running: enough answers to mean something is usually a few
weeks at normal order volume, not a few days.

Save the build sheet alongside the brand files so the report can read it later. It records
which question was asked for which reason, and a report that knows the intent reads the
answers better.

## What it needs

- `references/question-bank.md`: every question, exact wording options, select type, when to use, and answer guidance.
- `references/objection-followups.md`: objection types with specific main-question wording and follow-up answer banks.
- `templates/build-sheet.md`: the output format.
- `references/example-build-sheet.md`: a worked example for a fictional brand. Use it for format and depth only; never copy its answers.
- Data: `brand-data.md` from `eca-brand-intelligence` where it exists, reviews, website,
  Shopify (connector or CSV), web search. No survey tool connection is needed.
- `eca-survey-report` is the follow-on once answers exist. `eca-persona-builder` covers
  the same ground from reviews rather than surveys; read its output if present.

## Check before finishing

Run every check. Fix anything that fails before you deliver.

- [ ] Longest path in each survey is 5 questions or fewer.
- [ ] Motivation and objection questions are both in the new customer survey.
- [ ] Every answer option traces to the evidence log or is tagged "category standard". Nothing invented.
- [ ] Randomise is marked on every multiple-choice question, with "Other" and "Nothing" pinned to the bottom.
- [ ] The main objection question is single-select.
- [ ] Every objection option except "Nothing" and "Other" has its own branched follow-up, and "Nothing" skips to the next question.
- [ ] No competitor is named anywhere.
- [ ] Answer options are short, specific, non-overlapping and written in customer language.
- [ ] Every new customer option reads true for someone whose order hasn't arrived yet. No performance claims that need the product in hand.
- [ ] Every option holds exactly one reason.
- [ ] The attribution question was only skipped if the brand is truly single-channel, and the reason is written in the snapshot.
- [ ] The objection results are labelled as "objections buyers overcame". People who left without buying are not in this data; recommend an on-site exit survey if the brand needs that view.
- [ ] Spelling and terms match the brand's market. No em dashes.
- [ ] Every question has a one-line "Why we ask" that names the decision it informs.
- [ ] If `brand-data.md` exists, its §17 channels drove the attribution list and its §13
      facts drove the shipping and returns follow-ups, rather than placeholders.
- [ ] Anything the brand profile marked low confidence was considered as an answer option,
      since the survey is the instrument for settling it.

---
*Built with the TEACH framework. Hone it: run it on a real brand, see what it gets wrong, and tune the steps or sharpen the trigger above.*
