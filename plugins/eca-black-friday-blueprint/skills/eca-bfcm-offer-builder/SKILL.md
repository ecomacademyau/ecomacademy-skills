---
name: eca-bfcm-offer-builder
description: Build a data-backed Black Friday / Cyber Monday offer for a Shopify store — pull last year's Q4 and BFCM performance plus the last 90 days, cross-check it against what the member wants this year, and recommend a core BFCM offer plus a Cyber Monday offer and a pre-agreed Plan B. Use whenever someone mentions Black Friday, BFCM, Cyber Monday, Q4 planning, their Christmas or holiday sale, "what offer should we run", "what discount should we do", "how did we go last Black Friday", "plan our BFCM", "what worked last year", wants to decide a promotional offer or discount depth, wants to know whether a discount will actually make money, or is choosing between offer mechanics like site-wide percentage, spend and save, BOGO, gift with purchase or free shipping. Also trigger for "should we discount at all", stock-clearance planning for Q4, and setting BFCM revenue targets. Creates the BFCM Campaign Master File that the rest of the Black Friday Blueprint builds on.
---

# BFCM Offer Builder

## Members-only

> This skill is part of the **Black Friday Blueprint**, for paid Ecommerce Academy members. Please keep it within the Academy.

**The job: decide the offer on evidence, not on what everyone else is doing.**

Most BFCM offers are chosen in about ten minutes, in a panic, in early November, by copying a competitor. This skill replaces that with: what actually happened last year, what the business needs this year, and what the arithmetic says is survivable. Then it writes the decision down so the whole campaign can be built on it.

**The output is the BFCM Campaign Master File** — the file every other skill in the Black Friday Blueprint reads from and adds to. Getting it right here is what makes the rest of the plugin work.

---

## Run order

Do not skip ahead to the offer. The recommendation is worthless without the evidence, and the member will not trust it either.

1. Set up, match the accounts, and connect
2. Pull the evidence
3. Scan the whole year for the best offer they have already run
4. Show the evidence review **(gate: they confirm it matches reality)**
5. Intake — what they want this year, including margin and target
6. Reconcile ambition against evidence
7. Build the core offer, Cyber Monday offer and Plan B
8. Ask their sale dates, lock the calendar and the budget split
9. Approve **(gate)**
10. Write the Master File
11. Hand over

---

## Step 1 — Set up, match the accounts, and connect

Compute the dates first, so every window is right:

```bash
python3 scripts/bfcm_dates.py
```

State the key dates back to them: this year's Black Friday and Cyber Monday, last year's, and how many days they have. If they ran their sale on a different window last year, **use their window** and note it.

Then check what you can reach — and **check that each account is actually theirs**. Agency logins and multi-brand owners routinely have several; the wrong one produces a detailed, confident, entirely wrong analysis that nothing downstream will catch. Match Klaviyo's organisation and website to the Shopify domain, and match the Meta ad account by brand name. **Name the accounts you matched** in one line. See `references/data-pull.md` §0.

**Try each tool before saying it is unavailable** — do not tell someone to connect something you have not attempted.

| Connector | What it gives | Without it |
|---|---|---|
| **Shopify** | Revenue, orders, AOV, sessions, conversion, discounts, new vs returning, stock. The spine. | Do **not** refuse. Drop to a lower evidence tier and run on unit economics instead — see `references/no-history.md`. |
| **Meta Ads** | Spend, ROAS, CPA per phase, and what the ads said | Ask for spend, revenue and ROAS from memory. Label it member-supplied. |
| **Klaviyo** | Campaign and flow revenue, list size then and now | Ask which sends worked and what the list size is. Label it member-supplied. |
| **Anything else** | Other revenue sources, session behaviour | Ask once whether Q4 revenue came from anywhere else. |

**Read `brand-data.md` if the member has one** — not for voice, which this skill does not need, but for the facts that constrain the offer: products and price points (§6), their normal offer and discount strategy (§7), operational facts like shipping thresholds and cut-offs (§13), and the promotional calendar and seasonality (§14). That last one pairs directly with the year-wide scan in Step 3: the scan finds unexplained spikes, and §14 often explains them.

If there is no `brand-data.md`, ask for those specifics directly and say that is what you are doing. **Never fill the gaps with invented brand facts.** Voice and personas belong to the channel skills that write copy, not to this one.

**Declare the evidence tier** (`references/no-history.md`): Full, Partial, Manual or None. A member with a brand-new store, no connectors, or no prior Black Friday still gets a real plan — it just rests on margin arithmetic rather than history, targets are labelled unvalidated, and you say so plainly. **Never refuse to help because the data is thin, and never behave as though you have evidence you do not.**

Record the tier in the Master File and repeat it in the summary. A Tier 4 recommendation must never be delivered with Tier 1 confidence.

**Say in one line what you loaded and what is missing**, before pulling anything. This is the step that stops a confident recommendation being built on a third of the picture.

## Step 2 — Pull the evidence

Follow `references/data-pull.md` exactly. Pull, for last year: the four windows, the daily shape, top products, discount detail, ad spend by phase, email campaign performance. Then the last 90 days against the same 90 days last year, and list size now versus twelve months ago.

**Process it in code, not in your head.** Write the raw pulls to a working file and compute from that. Daily rows across a quarter across four platforms is where arithmetic errors and token waste both come from.

**Mark every gap.** `NOT AVAILABLE — reason` is a real answer and a useful one.

## Step 3 — Scan the whole year, not just BFCM

**The best offer they have run may not have been a Black Friday offer.** Pull thirteen months weekly and run `scripts/promo_outliers.py`. It detrends against a rolling baseline, so a growing business does not make every recent week look like a win, and it ranks lift **per point of extra discount**, so the most expensive event does not automatically look like the best one.

Then explain each outlier: what emails went out, what was being spent, what launched. **The scan finds when; only the record explains why.**

**Any outlier the data cannot explain must be qualified by the member before it is used.** Bring them the list and ask plainly: *"Late March lifted revenue 105% but cost 16 extra points of discount. What was running?"* They will remember a wholesale order, a press hit, a viral post, a stockout recovery, a one-off partnership, a market day. That answer decides whether the period is a repeatable template or a one-off you must exclude.

Record each outlier with **how it was explained**: `data` (a campaign or spend change accounts for it), `member` (their recollection, labelled as such), or `unexplained`. Then:

- **Never build a recommendation on an unexplained spike.** It is as likely to be a bulk order or a data artefact as a repeatable promotion.
- **Never guess the cause.** "This was probably an EOFY sale" is invention, and it will be quoted back as fact.
- **Say plainly when a period had to be excluded** and why. A member who knows the March number was one wholesale order is better informed than one shown a tidy list.

**This step still runs with thin data.** A store with eleven months and no prior Black Friday can still find its own best period — it just cannot compare BFCM to BFCM. At Tier 2, lead with the scan rather than apologising for the missing comparison. The script takes plain rows, so an export from any platform works, including a spreadsheet the member keeps by hand.

**Offer to write what you found back into `brand-data.md` §14.** The scan effectively discovers the brand's real promotional calendar, which is often better than what is recorded. Propose the addition, get a yes, then write it. It makes every future campaign smarter, not just this one.

Bring the result into the recommendation explicitly. If their most efficient event of the year was a January reactivation or an EOFY bundle rather than BFCM, the member needs to hear that **before** the offer is designed. If BFCM really was their best, say that too — it is an argument for going harder.

## Step 4 — The evidence review (gate)

Give them a **short, plain-English read** in chat. Not a data dump. Lead with the four things that change a decision:

1. What last year's BFCM actually produced, versus a normal week
2. Which day carried it, and whether the sale peaked at launch or at the end
3. What the discount cost, and whether the volume lift covered it
4. Where they are now versus this time last year, and whether the list is bigger

Then say what you could not measure.

**Ask them to confirm it matches their memory of last year.** They know things the data does not — a stockout, a shipping delay, a competitor, a supplier problem. That context changes the recommendation and it only ever arrives if you ask.

## Step 5 — Intake (member-led)

Now ask what they want. One thing at a time, with a recommendation attached where you have one from the data.

- **The main objective** — clear stock, increase revenue, acquire new customers, get customers back. Only one is primary. Push gently for a single answer.
- **The lever** they want to move — conversion rate, AOV, traffic, database, margin.
- **The offer they already have in mind**, if any. Ask early. If they have already half-decided, you need to know before you recommend something else.
- **Gross margin, and the depth they will not go past. Get this here, not later.** It is required for the break-even, and asking after the reconciliation means doing the whole analysis twice.
- **The revenue target — but show them the baseline first.** Compute the do-nothing-different projection (`references/offer-design.md`) and the orders-and-AOV table for several candidate targets, then let them pick against it. A target chosen in the abstract is how a plan becomes a fantasy. If they do not know their margin, that is the first thing to find out — say so plainly, and if they genuinely cannot get it, mark the recommendation directional only.
- **Stock they must clear**, and stock they must protect.
- **Constraints** — supplier limits, shipping cut-offs, wholesale or retail partners, anything already promised to the list.

**Never infer any of these.** Confirm every one back before building.

## Step 6 — Reconcile

This is the step that earns the skill its keep, and it is where most people would rather not look.

Put their intent next to the evidence and say where they agree and where they do not:

- If the target needs a 3x lift and last year's sale produced 1.4x on a deeper discount, **say that**, with both numbers, before designing anything.
- If they want to acquire new customers but last year's sale went 80% to existing customers, that is a different campaign than they think they are running.
- If they want to protect margin and the offer they have in mind needs a 200% volume lift to break even, show them the arithmetic.

Be straight and be kind. The goal is a plan that survives contact with December, not agreement in September. **Do not soften a number to be agreeable** — an unrealistic target set now becomes a panic discount later, which is exactly what this skill exists to prevent.

If the evidence supports what they want, say that clearly too, and move faster.

## Step 7 — Build the three offers

Follow `references/offer-design.md`.

**The core offer.** Objective → lever → mechanic → depth → conditions, in that order. Run the break-even and show it. Tie the recommendation to a specific number from the evidence — "your spend-and-save last year lifted AOV 22% and cost 9 points of margin, versus the site-wide 20% which cost 20 points for a 12% order lift" is a reason. "Spend and save works well" is not.

Offer **the no-discount column** genuinely, not as a token gesture. For a brand with real demand and thin margins it is often the better answer, and almost nobody considers it.

**The Cyber Monday offer.** Different mechanic, usually a different lever. Not a continuation.

**Plan B.** Trigger metric, threshold, exact check point, the switch, and who decides. Written down now, while everyone is calm.

Then settle the conditions list, and the scarcity, and check any pricing claim is one they can substantiate.

## Step 8 — Ask their sale dates, then lock the calendar and budget

An offer without dates is not a decision, and five downstream skills are blocked until this exists. **The dates are the member's to give, not yours to assume.**

```bash
python3 scripts/campaign_calendar.py --year <year> --ea-days <n> --sale-lead <n> --ends <date>
```

**Dates are computed, never typed.** Getting "the Monday of Black Friday week" wrong by a day silently corrupts every send time in every channel plan.

**Ask the member when their sale actually runs, before generating anything.** The script's defaults are a starting proposal, not a decision. Plenty of brands do not run the standard window: some open the week before, some run the whole of November, some skip Black Friday itself and own Cyber Monday, some extend to mid-December for the gifting run. Guessing here silently misdates every email, ad and on-site change downstream.

Ask it plainly and in their words:

> "When do you want the sale to actually run — when does it open to everyone, and when does it end?"

Then confirm what they said back as dates, with the weekday, before writing the calendar: *"So the offer is live Monday 23 November through Tuesday 1 December, with VIPs from Friday 13th."* Weekdays matter — people think in "the Monday before", and a date without a weekday is where off-by-one errors hide.

**If they do not know yet, say so in the Master File** as `TO CONFIRM` rather than quietly locking the default. A placeholder everyone knows is a placeholder is safe; a default that looks like a decision is not.

Then settle the rest with them:

- **Whether there is an early-access phase, and how long.** This is an offer decision, not a scheduling one — it sets the date the list-build has to start, and on most stores the early-access audience is worth several times the broadcast list per person.
- **When the core offer opens to everyone**, and when it ends.
- **The store's timezone**, stated once and used by everything downstream.
- **Shipping cut-offs**, domestic and international. These constrain the offer itself: there is no point building a bundle around stock that lands in December.
- **Stock arrival dates** for anything in the offer.
- **Blackout dates** — existing campaigns, launches, holidays.
- **The Plan B check point**, pinned inside BLACK_FRIDAY.

Then the **budget split**. Set it here, once, or each ad skill will assume it owns the whole budget. Anchor it to last year's spend and return rather than picking a number in the air, and hold something back for the Plan B switch — free shipping is not free.

The canonical phases, which every downstream skill will reference: `LIST_BUILD` · `EARLY_ACCESS` · `WARM_UP` · `SALE_LIVE` · `BLACK_FRIDAY` · `WEEKEND` · `CYBER_MONDAY` · `LAST_CHANCE` · `POST_SALE`. Do not invent new ones without adding them to the template first.

### Where the calendar lives

**Everything this plugin creates lives in a `bfcm/` folder** in the member's working directory. Create it on first run. One folder, one campaign, easy to find in December and easy to archive in January.

```
bfcm/
  bfcm-<year>-master.md         the Master File — every skill reads and appends
  bfcm-<year>-calendar.csv      source of truth for dates
  bfcm-<year>-runsheet.csv      source of truth for tasks (append-only)
  bfcm-<year>-dashboard.html    generated view, never edited by hand
```

Keeping the year in the filenames means next year's campaign sits alongside this one rather than overwriting it — and last year's files are exactly what the outlier scan and post-mortem want.

Two CSVs are the source of truth, and everything else is generated from them:

| File | Rows | Who writes it |
|---|---|---|
| `bfcm/bfcm-<year>-calendar.csv` | one per phase | **This skill and the member only.** Every other skill reads it. |
| `bfcm/bfcm-<year>-runsheet.csv` | one per task | **Append-only.** Each channel skill adds rows tagged with its own `OWNER` and never edits another's. |
| `bfcm/bfcm-<year>-dashboard.html` | — | Generated. Never edit by hand. |

The dashboard is branded with the **ECA Design System** (`assets/ECA Design System/`), the same one the 4PI reports use, so everything a member receives from the Academy looks like it came from the same place. Dark hero with the ECA mark, all-caps Nunito Sans headings, Montserrat body, white cards on `#F5F5F5`, green-tinted table headers, pill badges on the semantic colours. **No gradients, no serif, no emoji.** If you change a colour, change it in `eca-tokens.css` first and keep the generator in sync.

Separating the two is what makes multiple writers safe. The calendar answers *when the phases are* and needs one writer; the runsheet answers *what fires when* and needs many. Appends cannot collide; edits can.

```bash
mkdir -p bfcm
python3 scripts/campaign_calendar.py --year <year> --ea-days <n> --sale-lead <n> \
        --ends <their end date> --csv > bfcm/bfcm-<year>-calendar.csv
python3 scripts/sync_campaign.py bfcm/bfcm-<year>-calendar.csv bfcm/bfcm-<year>-runsheet.csv \
        --html bfcm/bfcm-<year>-dashboard.html --brand "<Brand>" --markdown
```

**Run `sync_campaign.py` at the start of every skill's run and after every change.** It validates and regenerates; it never invents. It catches the two things that actually go wrong: a spreadsheet silently rewriting `2026-11-27` into `27/11/2026` on save, and phases that overlap, invert or leave gaps. Paste its markdown output into Master File §10 so the plan reads in one document.

CSV rather than a Google Sheet because the member can still open it in Excel or Sheets and change a date in ten seconds, **and** skills can write it with ordinary file tools. The Drive connector can create and read a Sheet but cannot edit cells, so a Sheet would have been read-only to every skill. Export one for sharing if they want — as a copy, not the source.

**Everything downstream reads phases by ID, never by date.** If the member later moves the launch, section 10 changes and every channel plan stays correct.

## Step 9 — Approve (gate)

Present all three offers together, each with its mechanic, depth, margin position, forecast and reasoning. **Nothing is written to the Master File until they say yes.**

Expect them to change something. Rebuild the break-even when they do, rather than waving it through.

## Step 10 — Write the Master File

Create `bfcm/bfcm-<year>-master.md` (make the folder if it does not exist) from `references/master-file-template.md`. Fill sections 1 through 12. Leave 13 through 19 as reserved headings, one per downstream skill. **Never renumber them.** Log assumptions with their assumed values in 20, and start the change log in 21.

**Every number carries its source and window.** Later skills, and the member in six weeks, will rely on this.

## Step 11 — Hand over

Give them, briefly: the file, the three offers in one line each, the single biggest risk you saw in the evidence, and the next decision they need to make. Tell them the rest of the Black Friday Blueprint builds from this file, so if the offer changes, it changes here first.

---

## Rules

- **Never state a trend from an aggregate.** Pull the series and look at the shape first. One long-window number hides everything, and a busy month inside it will make you report a collapse that never happened.
- **Never read the offer off the discount rate.** Free shipping, gifts and bundle pricing often do not register there at all. Read the campaign names before you characterise what they ran.
- **Label modelled numbers as models where they appear**, with the assumed value shown. Quoted twice, an assumption becomes a fact by the third mention.
- **Count marketable subscribers, never all profiles.** A raw profile count includes unsubscribed, suppressed and bounced people. It is always too big, and every per-recipient number derived from it is wrong. Use an active-subscriber segment and an engaged-90-day segment, and name which one each figure came from.
- **Check the first months of any segment time series.** Zeros followed by a step change means the segment was created then, not that the list grew. Reporting that as growth is a confidently wrong answer nothing downstream will catch.
- **Never invent a benchmark.** No "typical BFCM uplift is 3x". Compare the brand against itself. If you do not have a figure, say so.
- **Never present an estimate as a measurement.** Especially list size twelve months ago, and any member-recalled number.
- **Never recommend a depth without the break-even in front of them.**
- **Never propose fake scarcity or an unsubstantiated "was" price.** Both are misleading conduct and BFCM is when regulators look.
- **Never let the answer be "match the competitor".** It is the most common BFCM mistake and it optimises for someone else's margin, stock position and customer base.
- **One primary objective.** A sale trying to do four things does none of them.
- **Confirm every input.** A wrong assumption at intake propagates through every skill that reads this file.
- **Say what you could not get**, every time, without being asked.

## Reference files

- `references/data-pull.md` — windows, verified queries per platform, honest fallbacks
- `references/offer-design.md` — levers, tactic bank, break-even maths, Cyber Monday and Plan B design, compliance
- `references/master-file-template.md` — the Master File schema and the rules for every skill that touches it
- `scripts/bfcm_dates.py` — computes BFCM windows for any year
- `scripts/promo_outliers.py` — finds the best promotional periods across the whole year, detrended and weighted by discount cost
- `scripts/campaign_calendar.py` — builds the phase calendar with computed dates and a countdown
