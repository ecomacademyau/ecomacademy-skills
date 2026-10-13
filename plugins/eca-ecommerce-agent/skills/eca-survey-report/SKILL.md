---
name: eca-survey-report
description: "Deep dive into any brand's post-purchase survey (new and returning customer surveys) and turn it into an ECA-branded HTML report: why customers buy, what almost stopped them and why, how they found the brand, who they are, why they come back, then concrete next steps for the website, ads and hooks, content and email. Use whenever someone says survey report, post-purchase survey report, PPS report, Zigpoll report, UserLoop report, 'run the survey report for [brand]', 'what are customers telling us', 'what almost stopped people buying', objections from the survey, HDYHAU or 'how did you hear about us' results, survey insights, voice of customer report, 'turn our survey into ad angles', or uploads a survey export CSV. Also the follow-on to eca-survey-questions once a survey has answers. Uses the Zigpoll or UserLoop MCP when connected, otherwise asks for CSV exports. Works for any brand."
---

# ECA Survey Report

A deep dive into a brand's post-purchase survey that ends in action. The report answers:

1. **Why do customers buy?** Each reason becomes an ad angle with hooks.
2. **What almost stopped them, and why?** Each objection becomes a card with the customer's own words and a counter for the website, ads, content and email.
3. **How did they find the brand?**
4. **Who are they and what problem are they solving?** Turned into personas.
5. **Why do they come back?** Turned into retention and email moves.
6. **What should we do next?** A prioritised action plan: this week, this month, test next.

All-time is the main lens because that is where the volume is. The current period shows what is new. The report shows no statistics: every share carries a plain signal tag (**Strong signal**, **Early signal**, **Too few answers yet**), and the build script decides the tags from the raw counts, so nothing is overstated.

## Where this sits in the Marketing Coworker

```
eca-brand-intelligence  ->  eca-survey-questions  ->  eca-survey-report  ->  the rest of the bundle
    the hypothesis            the instrument            the evidence           the work
```

Everything this report produces is an input to work that happens in another skill:
angles go to ad copy and video scripts, objection counters go to product pages, landing
pages, content and email, personas cross-check the persona builder, and the whole lot
offers to update `brand-data.md`. `references/feeding-the-bundle.md` has the map.

**A survey report that gets read and admired has failed.** It is finished when the
findings are in the hands of the skills that act on them.

## When to use this

Any time someone wants to understand, report on or act on post-purchase survey answers they already have, for any brand. If they want to write or rewrite the survey questions, that is `eca-survey-questions`; say so and stop.

## Steps

### 1. Confirm scope (one short round)

Check the conversation, uploads and project files first. Confirm only what is missing:
- **Brand.**
- **Period.** Default: the last full calendar month. If the new customer survey gets 50+ answers a fortnight and the member wants it, use the last full fortnight. All-time always runs from the survey launch date to the end of the period.
- **Data source.** Check the tool list yourself before asking (step 3).

### 2. Load the brand config

Look for `survey-report-config-<brand-slug>.md` in project files, uploads or this skill's `clients/` folder. If none exists, run the first-run onboarding in `clients/README.md`: read the live survey, propose the config (survey IDs, the role of each question, objection themes, product line groups, market spelling), get the member to confirm it, and hand it back as a file to save. The config keeps answer mapping identical from one report to the next.

Also load the brand profile. If `eca-brand-intelligence` has been run, read `brand-data.md`
and take §3 for voice and market spelling, §6 and §8 for what the brand can actually claim,
§9 for the objections it already believed it had, §12 for its current personas, and §17 for
its assumed channel mix. Those last three matter most, because **the report is partly a
test of them**: where the survey disagrees with the profile, that is a finding rather than
a discrepancy to tidy away.

Fall back to `brand-dna.md`, `icp-cards.md` and `brand-voice.md` if that is what exists,
and to the brand's website if nothing does. Also read the `eca-survey-questions` build
sheet if there is one: it records why each question was asked, and knowing the intent
makes the answers read better.

If the member has a previous report, read its embedded `survey-history` block (Artifact tool, action "read", if they give a link) to show which of last report's actions were done. Optional; never invent it.

### 3. Pull the data

Follow `references/data-pull.md`:
- **Zigpoll MCP** (`mcp__Zigpoll__*`): find both surveys, list slides, pull answer counts for all-time and for the period, pull the follow-up questions, pull every open-text answer, and pull responses with Shopify line items for product insight.
- **UserLoop MCP** (`mcp__UserLoop__*`): list surveys, pull counts per question for all-time and the period, pull open text.
- **Neither:** ask for CSV exports of both surveys from launch to today (exact wording in `references/data-pull.md`).

Write every count into a working file as you go, with the tool and dates that produced it.

### 4. Read every written answer

Read all open-text and "Other" answers, not a sample. Bucket them into themes (`references/analysis-rules.md`), keep the best quotes for each theme, and note any objection or motivation that appears in writing but is missing from the answer list. These become the language bank and a "questions to consider" note.

### 5. Build the insight layer

Follow `references/insight-layer.md`:
- **Key insights:** 6 to 8 cards, each with the finding, the number behind it and the action it leads to.
- **Angles:** one per motivation with real volume, each with 2 to 3 hooks.
- **Objection cards:** one per objection with at least 5 all-time answers, ordered by all-time share. Each has why it mattered (follow-up answers), the customer's words, and counters for the website, ads, content and email.
- **Personas:** 2 to 4, built from who they buy for, the problem they are solving, motivation and product line.
- **Retention moves** from the returning survey.
- **Action plan** grouped into this week, this month and test next, each item tagged with its channel and traced to the data.
- **Language bank:** reusable customer phrases grouped by theme.

Use the brand's market spelling. Never name competitors. Never recommend a claim the brand cannot back.

### 6. Build the report

1. Write the data file in the shape defined in `references/report-data-schema.md` (see `examples/example-report-data.json`, a worked example for a fictional brand). Supply **raw counts only**; do not write percentages or tags.
2. Run `python3 scripts/build_report.py <data.json> <output.html>`. It calculates every percentage, signal tag and "what's new" shift with `scripts/signals.py`, renders `templates/report-template.html` in the ECA Design System, embeds the history block, and refuses to build if a check fails.
3. Fix whatever the build script reports and rerun. If a written insight contradicts a calculated tag (for example, calling something a trend when it is tagged "No real change"), rewrite the insight, not the data.

### 7. Deliver

- If the Artifact publishing tool is available, publish the HTML as "<Brand> Survey Report · <period>". If updating a previous report, pass its link so the member keeps one URL.
- Otherwise save it to the outputs folder and present the file.
- In chat, three lines only: the biggest objection and its counter, the strongest angle,
  and the first action to take this week. **If the survey contradicted the brand profile,
  that replaces one of the three.** A brand that believed it sold on convenience and finds
  buyers choosing it on price has learned the most valuable thing in the report, and it
  should not be buried in a section.
- On a first run, also hand over the config file and tell the member to save it.

### Then hand the findings on

Follow `references/feeding-the-bundle.md`. Offer the specific next moves by name, with the
finding attached, rather than a general suggestion to use the report:

> "The biggest objection is shade uncertainty, 31% of all answers, and the follow-ups say
> it is about matching rather than range. That is a PDP section. If `eca-landing-pages` is
> installed I can build the block, or `eca-blog-writer` can write a shade-matching guide
> that answers the same question in search."

**Never assert a skill is installed.** Members have different bundles. Say "if X is
installed", and hand over the finding either way so the work is doable without it.

And offer the write-back: the survey is primary research from actual buyers, which
outranks the inference behind much of `brand-data.md`. Show what would change and how many
answers sit behind each change. **Never rewrite the profile silently** — a brand profile
that shifts under someone without their say is worse than one that is out of date.

## What it needs

- `references/data-pull.md`: Zigpoll, UserLoop and CSV pull sequences.
- `references/analysis-rules.md`: periods, signal tags, bucketing written answers, small numbers, product segmentation.
- `references/insight-layer.md`: how to write insights, angles, objection cards, personas, actions and the language bank.
- `references/report-data-schema.md`: the data file the template renders.
- `clients/README.md`: first-run onboarding and the brand config format.
- `references/feeding-the-bundle.md`: which skill each finding goes to, and the
  `brand-data.md` write-back.
- `templates/report-template.html`: the ECA-branded renderer.
- `scripts/signals.py`: signal tags. `scripts/build_report.py`: calculates, validates and builds.
- `assets/eca-tokens.css`, `assets/eca-mark.svg`: ECA design tokens and logo mark.
- `examples/example-report-data.json`: a full worked example for a fictional brand. Use it for shape and depth only; never copy its numbers or wording.

## Check before finishing

The build script enforces the starred items.

- [ ] * Every share comes from raw counts, with the base shown.
- [ ] * Every signal tag was calculated, not written by hand.
- [ ] * No insight title claims a change that is not tagged Strong or Early signal.
- [ ] * Every insight, angle, counter and action names its source in the data.
- [ ] * No em dashes anywhere.
- [ ] * Nothing from the example brand leaked in.
- [ ] Every written answer was read, not sampled.
- [ ] Objections are labelled "objections buyers overcame" (people who did not buy are not in this data).
- [ ] Quotes carry no names, emails, order numbers or identifying health details.
- [ ] Spelling matches the brand's market. No competitor named. No claim the brand cannot back.
- [ ] The action plan has no more than 3 items in "this week".
- [ ] Each finding was handed to a named skill with the finding attached, not a general
      suggestion to use the report.
- [ ] Where the survey contradicted `brand-data.md`, that was said plainly and offered as
      an update rather than applied silently.
- [ ] Personas were offered as a cross-check against `eca-persona-builder`, and any
      disagreement between review-built and survey-built personas was reported as a
      finding rather than reconciled away.

---
*Built with the TEACH framework. Hone it: run it on a real brand, read it as the brand owner would, and tune the steps or sharpen the trigger above.*
