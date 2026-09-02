# BFCM Campaign Master File — template

This is the spine of the Black Friday Blueprint. **One file per brand per year**, written by this skill and appended to by every skill that follows.

**Filename:** `bfcm/bfcm-<year>-master.md`.

Everything the Black Friday Blueprint creates lives in a **`bfcm/` folder** in the member's working directory — master file, calendar, runsheet and dashboard. One folder per campaign year's worth of artefacts, kept together so nothing is hunted for in December, and so last year's files are still there when next year's outlier scan and post-mortem want them.

## Rules for every skill that touches this file

1. **Never overwrite another skill's section.** Fill your own, leave the rest.
2. **Never silently change an approved decision.** If new evidence contradicts a locked offer, say so, propose the change, and get approval before editing. Then log it in the change log.
3. **Every number carries its source and date window.** A figure with no provenance is a guess, and three skills downstream nobody will remember which.
4. **Mark what you could not get.** `NOT AVAILABLE — <reason>` beats a blank, and beats an estimate presented as fact.
5. **Update the header block** (`Last updated`, `Last updated by`) on every write.
6. **Add to the change log** whenever a decision changes.
7. **Section numbers are fixed.** Never renumber. A later skill renumbering sections breaks every earlier reference, and nobody notices until the runsheet points at the wrong plan. Sections 1-12 belong to the Offer Builder; 13-19 are owned one each by Email & SMS, Meta Ads, Google Ads, Website Setup, Social Campaigns, Go-Live Runsheet and the post-mortem; 20-21 are shared.
8. **Read the calendar by PHASE ID, never by date.** If the member moves the launch, only section 10 changes and every channel plan stays correct.

---

```markdown
# BFCM <YEAR> Campaign Master File — <BRAND>

> Written by the ECA Black Friday Blueprint. Every skill in the plugin reads and appends to this file.

| | |
|---|---|
| **Brand** | <brand> |
| **Store** | <store>.myshopify.com |
| **Market / timezone** | <market> / <tz> |
| **Currency** | <ccy> |
| **Status** | Offer approved / In build / Live / Complete |
| **Evidence tier** | 1 Full / 2 Partial / 3 Manual / 4 None — *and what that means for confidence* |
| **Calendar CSV** | `bfcm/bfcm-<year>-calendar.csv` |
| **Runsheet CSV** | `bfcm/bfcm-<year>-runsheet.csv` (append-only) |
| **Dashboard** | `bfcm/bfcm-<year>-dashboard.html` (generated) |
| **Created** | <date> |
| **Last updated** | <date> |
| **Last updated by** | <skill name> |
| **Accounts matched** | Shopify <domain> · Klaviyo <org> · Meta <ad account name> |

---

## 1. Campaign at a glance

| | |
|---|---|
| **Core offer** | <one line> |
| **Cyber Monday offer** | <one line> |
| **Plan B** | <one line, plus its trigger> |
| **Primary objective** | Clear stock / Increase revenue / Acquire new customers / Reactivate customers |
| **Growth lever** | Conversion Rate / Average Order Value / Traffic / Database |
| **Revenue target** | $<x> |
| **Key dates** | Early access <d> · Live <d> · Black Friday <d> · Cyber Monday <d> · Ends <d> |

---

## 2. Evidence — last year's Q4

> Source: <tools used>. Windows computed by `scripts/bfcm_dates.py`.

### 2.1 By phase

| Phase | Window | Revenue | Orders | AOV | CVR | Sessions | New % | Returning % |
|---|---|---|---|---|---|---|---|---|
| Pre-BFCM build-up | | | | | | | | |
| BFCM week | | | | | | | | |
| Post-BFCM to EOY | | | | | | | | |
| **Full Q4** | | | | | | | | |

### 2.2 What was on offer last year

| Discount / offer | Mechanic | Depth | Window | Orders | Revenue | Avg discount per order |
|---|---|---|---|---|---|---|

### 2.3 Ad spend last year

| Phase | Spend | Revenue attributed | ROAS | CPM | CPA |
|---|---|---|---|---|---|

### 2.4 Email last year

| Campaign | Sent | Recipients | Open % | Click % | Revenue |
|---|---|---|---|---|---|

### 2.5 What the data actually says

- **Worked:** <specific, with the number that proves it>
- **Did not work:** <specific>
- **Best single day:** <date, revenue, what was running>
- **The discount that cost the most margin for the least volume:** <specific>
- **Unknowns:** <what could not be measured and why>

---

## 2.6 The best offers of the whole year

> From `scripts/promo_outliers.py`. Detrended against a rolling baseline and ranked by lift per point of extra discount, so the most expensive event does not look like the best one.

| Period | Revenue | Lift vs baseline | Discount rate | Extra discount | Lift per point | What was running | Explained by | Repeatable? |
|---|---|---|---|---|---|---|---|---|

> **Explained by** must be one of `data`, `member` or `unexplained`. An unexplained spike is never used as the basis for a recommendation, and a member-explained one is labelled as recollection, not measurement. Note any period excluded, and why.

**Best template of the year:** <period, mechanic, and why it beat the others>

**Did BFCM win?** <yes or no, stated plainly, with the comparison>

**Lifts that cost no extra discount:** <periods, and what drove them>

---

## 3. Evidence — last 90 days

| Metric | Last 90 days | Same 90 days last year | Change |
|---|---|---|---|
| Revenue | | | |
| Orders | | | |
| AOV | | | |
| Conversion rate | | | |
| Sessions | | | |
| New vs returning | | | |
| Ad spend | | | |
| Blended ROAS | | | |

**Read:** <two or three lines on the trend and what it means for what is realistic this year>

---

## 4. Evidence — audience and list

| | Now | 12 months ago | Change | Segment used |
|---|---|---|---|---|
| Marketable email subscribers | | | | |
| Marketable SMS subscribers | | | | |
| Engaged (90 days) | | | | |
| Suppressed / unengaged | | | | |

> **Marketable, not total.** A raw profile count includes unsubscribed, suppressed and bounced people, is always too big, and corrupts every per-recipient figure derived from it. Name the segment each number came from.

**Method + limits:** <how historical size was derived, and what it does not account for>
**Segment age check:** <confirm each segment existed 12 months ago. A series that starts at zero and jumps is a segment being created, not a list growing.>

---

## 5. What the member wants this year

> Captured at intake, in their words, and confirmed back before anything was built.

| | |
|---|---|
| **Objective** | |
| **Growth lever** | |
| **Revenue target** | |
| **Offer they had in mind** | |
| **Margin floor / no-go depth** | |
| **Stock they must clear** | |
| **Stock they must protect** | |
| **Constraints** | |

---

## 6. The reconciliation

Where the member's ambition and the evidence agree, and where they do not. **This section exists so nobody is surprised in December.**

| Their intent | What the evidence says | Verdict |
|---|---|---|

**Stretch check:** <target vs what last year plus current trend supports, stated plainly>

---

## 7. THE CORE OFFER

| | |
|---|---|
| **Offer** | |
| **Mechanic** | |
| **Lever it moves** | |
| **Why this one** | <tied to a specific number in section 2 or 3> |
| **Discount code** | |
| **Eligibility / exclusions** | |
| **Conditions** | |
| **Scarcity** | Time / Product / Bonus — and why it is real |
| **Starts / ends** | |
| **Early access** | |
| **Margin at this depth** | |
| **Break-even volume lift needed** | |
| **Forecast** | Revenue $<x> · Orders <x> · AOV $<x> |

---

## 8. Cyber Monday offer

| | |
|---|---|
| **Offer** | |
| **Why it differs from the core offer** | |
| **Mechanic** | |
| **Starts / ends** | |
| **Margin** | |

---

## 9. Plan B

> Decided in advance so nobody panic-discounts at 9pm on Black Friday.

| | |
|---|---|
| **Trigger metric** | |
| **Threshold** | |
| **Check point** | <exact date and time> |
| **The switch** | |
| **Who decides** | |
| **What must NOT change** | |

---

## 10. Campaign calendar

> Generated by `scripts/campaign_calendar.py`. **Every downstream skill keys off the PHASE ID, not the date.** Change a date and it moves everywhere; hardcode a date in a channel plan and it will silently disagree with the others.

**Live calendar (source of truth):** <Google Sheet URL, or "markdown below" if Drive is not connected>
**Snapshot last synced:** <date> by <skill>

**Sync rule.** The sheet is the member's to edit; skills read it and never write to it. Every skill re-reads it at the start of a run and compares against the snapshot below. If they differ: update the snapshot, say what moved, and flag any plan built on the old dates.

**Store timezone:** <tz — stated once, used by every skill>
**Sale dates given by the member:** CONFIRMED on <date> / **TO CONFIRM** — never leave a generated default sitting here as though it were a decision
**In their words:** "<what they actually said about when the sale runs>"

| Phase ID | Starts | Ends | Days | What happens |
|---|---|---|---|---|
| LIST_BUILD | | | | |
| EARLY_ACCESS | | | | |
| WARM_UP | | | | |
| SALE_LIVE | | | | |
| BLACK_FRIDAY | | | | |
| WEEKEND | | | | |
| CYBER_MONDAY | | | | |
| LAST_CHANCE | | | | |
| POST_SALE | | | | |

**Hard constraints**

| | Date | Source |
|---|---|---|
| Domestic shipping cut-off | | |
| International shipping cut-off | | |
| Stock arrival for offer items | | |
| Blackout dates | | |

**Plan B check point:** <exact date and time, inside BLACK_FRIDAY>

---

## 11. Budget allocation

> Set here so the ad skills read one number instead of each assuming it owns the whole budget.

| Channel | Budget | Phases it runs in | Owner skill |
|---|---|---|---|
| Meta Ads | | | |
| Google Ads | | | |
| Social / organic | | | |
| Email & SMS | | | |
| Contingency for Plan B | | | |
| **Total** | | | |

**Last year's comparison:** <spend and return, so the number is anchored to something>

---

## 12. Targets and success metrics

| Metric | Last year | Target | Actual |
|---|---|---|---|

---

## 13. Email and SMS plan
*Reserved — Email & SMS Plan skill.*

## 14. Meta Ads plan
*Reserved — Meta Ads skill.*

## 15. Google Ads plan
*Reserved — Google Ads skill.*

## 16. Website setup
*Reserved — Website Setup skill.*

## 17. Social campaigns
*Reserved — Social Campaigns skill.*

## 18. Go-live runsheet
*Reserved — Go-Live Runsheet skill. Runs last, once every channel plan above exists. Its job is resolving the conflicts between them.*

## 19. Results and post-mortem
*Reserved — written after the event. Feeds next year's outlier scan.*

---

## 20. Assumptions and open questions

Every modelled number lives here **with its assumed value**, not just its name. A modelled figure quoted twice becomes a fact by the third mention.

| # | Assumption | Value used | Basis | Measured or modelled | Owner |
|---|---|---|---|---|---|

### Open questions

| # | Question | Status | Owner |
|---|---|---|---|

---

## 21. Change log

| Date | Skill | What changed | Approved by |
|---|---|---|---|
```
