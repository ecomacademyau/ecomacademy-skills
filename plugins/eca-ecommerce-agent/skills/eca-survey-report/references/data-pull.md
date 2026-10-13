# Data pull

Pick the first source that works: Zigpoll MCP, then UserLoop MCP, then CSV. Check the tool list yourself; never ask the member which tool they use before looking.

Write every number you pull into a working file (for example `work/<brand>-pull.json`) as you go, with the tool, filters and date range that produced it. The method section of the report is written from this file.

Dates: use the brand's local timezone for period boundaries and say which one in the method section. ISO dates in every call.

---

## Zigpoll MCP

### 1. Find the surveys
1. If the config has poll IDs, use them. Otherwise `list_polls` on the account (search "post" or "purchase"; status "any"). If there is more than one account, ask which one.
2. Identify the **new customer** and **returning customer** surveys from their titles and targeting. If unclear, `get_poll` and read the customer targeting (`orders_count` rules). Confirm with the member on first run.
3. `list_slides` for both. Check the slide IDs and wording against the config. A changed answer list or wording is a **comparability break** (see analysis rules).

### 2. Counts: all-time and this period
- `get_response_summary` with `slide_id` and `start_date` / `end_date` twice per question:
  - **all-time:** survey launch date to the end of the report period,
  - **this period:** the report period only.
- Record, for every answer, its count, plus the number of people who answered the question (`n`).
- `analyze_response_trends` with `poll_id` and `group_by` "month" is a fast cross-check of volume over time. Use it to spot a collection outage and mention it in the method.
- `analyze_participants` with `poll_id` and the period dates for participant totals.
- `analyze_dropoff` with `poll_id` for completion (share of starters reaching the last question) and the biggest drop point.

### 3. Follow-up questions
`get_response_summary` per follow-up slide for all-time and this period. Bases will be small; all-time is the one that goes on the objection cards.

### 4. Product segmentation
- `analyze_shopify_line_items` with `slide_id` (main objection question) for all-time gives products per answer (product insight needs the volume). It is a summary tool and **may truncate samples** per answer. If the totals do not reconcile with the answer counts, hand-tally instead:
- `list_responses` with `slide_id`, `created_after`, `created_before`, `limit` 5000, then read each response's attached line items and map them to product lines with the config. Paginate with `cursor` until done.
- Record how many responses carried line items. Responses without line items are excluded from product charts and the count is stated in the caveat.

### 5. Written answers
`list_responses` with `slide_id` of each open-text question (and each question with an "Other" box), `answer_type` "open-ended", from launch to the end of the period, paginating with `cursor`. Read every one before bucketing or choosing quotes.

### 6. Average order value (optional KPI)
If line items carry prices, AOV for respondents in the period can be computed from the responses pulled in step 4. Label it "AOV of respondents", not store AOV.

### Do not use
- `get_insights` as a source of numbers. It is AI-written and not reproducible; at most use it to spot a theme you then verify in the raw answers.
- Any write tool. This skill only reads.

---

## UserLoop MCP

1. `userloop_list_surveys` to find both surveys and their question IDs and types.
2. `userloop_analytics_counts` per question for all-time (launch to end of period) and for this period. It returns counts and, where available, revenue and AOV per answer.
3. `userloop_responses_timeseries` per survey to cross-check volume and spot an outage.
4. `userloop_responses_open` for every open-text question from launch to the end of the period (paginate with `offset`, limit 200).
5. `userloop_responses_raw` (paginate) when you need per-respondent rows, for example to tie branch follow-ups to the main answer or to segment by product if order data is included. Keep `redact_emails` true.

If a UserLoop tool asks for the member's opt-in, follow the connector prompt first.

---

## CSV fallback

Ask in one message:

> Please export both surveys (new customer and returning customer) as CSV covering launch date to today, with one row per response and the order or line-item columns included if your tool offers them.
> - **Zigpoll:** Dashboard > the survey > Responses > Export.
> - **UserLoop:** Survey > Responses > Export CSV.
> - **Other tools:** any per-response export with the response date and the question text in the headers.

If the menu wording differs in their account, ask them to look for "Export" on the survey's responses view rather than guessing paths.

Then:
1. Load with pandas. Print the columns and the first rows, and confirm which column is the date, which are questions, and which hold order data.
2. Filter to all-time (launch to end of period) and this period by response date.
3. Count per answer per window. Multi-select answers may arrive in one cell separated by commas or semicolons; split them.
4. State in the method section that the data came from a CSV export and the export date.

---

## Reconcile before analysing

- The sum of answer counts on a single-select question equals its response count. If not, find out why before going further.
- Branch follow-up bases should not exceed the count of the answer that feeds them.
- This period's count for each answer is never larger than its all-time count.

Record any unexplained mismatch in the method section.
