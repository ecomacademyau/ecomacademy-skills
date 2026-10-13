# Brand config

One config per brand: `survey-report-config-<brand-slug>.md`. It keeps answer mapping identical from one report to the next, which is what makes trends trustworthy.

Installed skills are read-only, so the member keeps the config in their project files (or re-packages the skill with it in this folder). Look in project files and uploads first, then here.

## First-run onboarding

1. Find both surveys in the data source (`references/data-pull.md`) and read every question and answer option.
2. If the brand has an `eca-survey-questions` build sheet, use its question order, objection themes and "why we ask" lines.
3. Draft the config below. Propose:
   - which question is the **main objection question** (single-select, seen by every new customer),
   - a canonical **theme** for each objection answer (merge answers that are the same thing worded differently, for example "delivery time" and "needed it by a date"),
   - **product line** groups from the brand's product names (5 to 10 lines; everything else goes to "Other"),
   - the **role** of each question (attribution, who_for, motivation, main_objection, follow_up:<theme>, problem, returning_reason, returning_open, other).
4. Show the draft to the member in one message and ask them to confirm or correct it.
5. Run the report, then hand the config back as a file and tell them to save it.

Never invent poll IDs, product names or themes. Everything comes from the live survey or the member.

## Config format

```markdown
# <Brand name> survey report config

- brand_slug: <slug>
- website: https://...
- market_spelling: AU | UK | US
- timezone: Australia/Brisbane
- currency: AUD
- source: zigpoll | userloop | csv
- account_id: <survey tool account id, if any>
- launch_date: YYYY-MM-DD
- config_version: YYYY-MM-DD   # bump whenever mapping changes

## Surveys
- new_customer_survey_id: <id>
- returning_customer_survey_id: <id>

## Questions (new customer)
| Order | Slide/question id | Short label | Type | Role |
|---|---|---|---|---|
| 1 | ... | How did you hear | single | attribution |
| 2 | ... | Main reason | single | motivation |
| 3 | ... | What almost stopped you | single | main_objection |
| 3a | ... | Follow-up: <theme> | multi | follow_up:<theme> |
| 4 | ... | Hoping it helps with | open | problem |

## Questions (returning customer)
| Order | Slide/question id | Short label | Type | Role |
|---|---|---|---|---|

## Objection theme mapping
| Answer text (exact) | Theme |
|---|---|
| ... | ... |
| Nothing, it was an easy yes | Frictionless |

## Product line mapping
| Product name contains | Line |
|---|---|
| ... | ... |

## Mapping change history
- YYYY-MM-DD: <what changed and why>
```
