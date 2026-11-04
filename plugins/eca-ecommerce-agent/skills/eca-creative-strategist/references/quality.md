# Quality gate (step 7) and learning (step 9)

## 1. Scorecard (every script)

Score 1 to 5. **Anything under 4 gets rewritten and re-scored before the member sees it.** Show the final scores, and one line on what moved a score if you rewrote it.

| Criterion | A 5 looks like |
|---|---|
| Hook | Spoken, visual and text agree; mid-thought; a specific person or pain in 3 seconds; works muted; passes the swap test |
| Problem | A real, evidenced pain in the customer's words |
| Mechanism | Passes the swap test; shown on camera |
| Proof | Every claim shown or sourced; compliant |
| Retention | Product on screen by ~10 seconds; a re-hook every 5 to 8 seconds; no filler; length fits the format |
| CTA | One casual line: brand, offer, URL, once; no fake urgency; matches the landing page |

Be honest with the scores. A wall of 5s tells the member nothing.

## 2. QA checklist

- [ ] Brand file and creative log read; research done if they were thin.
- [ ] Every claim, stat and motive traces to a source. No invented reviews, numbers, stories or names.
- [ ] Each angle names its evidence on the strategy page.
- [ ] Opens on a real problem or situation in the customer's words.
- [ ] Matches the funnel stage and the job of the round.
- [ ] Read-aloud timing checked (about 2.5 words a second).
- [ ] Product shown inside the take: front, detail, in use.
- [ ] Compliance quick check passed (`compliance.md`).
- [ ] `check_copy.py` run and every flag fixed or explained.
- [ ] If this is an edit, only what was asked changed (compare with the previous version).

## 3. First-time-right rules (every delivery)

These are the mistakes that cause rounds of rework. Tick all of them.

- [ ] **Raw, confiding openers.** Sounds like telling a friend, not an ad.
- [ ] **Hooks from different structural types**, including a situation callout, a problem first and a proof first.
- [ ] **Product at the reveal**, not the logo or the brand name.
- [ ] **Brand said once, at the end**, together with the offer and URL.
- [ ] **Locked ideas untouched.** Word for word. Suggestions in a separate note.
- [ ] **Named talent verified.** Never guess a name.
- [ ] **No fake urgency.**
- [ ] **Offer notes in the strategy pack, not in the creator brief.** Creators get one casual offer line, nothing about margins or pricing strategy.
- [ ] **Creator brief is clean**: no metrics, internal notes, competitor names, deadlines or "post this" instructions.
- [ ] **Brief intro says what the brand sells, with the link.**
- [ ] **Yappers and founder stories are one take.**
- [ ] Every competitor reference names the brand, its days live and where it came from, with no Ad Library or snapshot link; every metric has its date window.
- [ ] One brand per file and folder.
- [ ] **No em dashes.** A comma, a full stop or "and".
- [ ] **No AI-slop phrases**: game-changer, elevate, unlock, level up, seamless, revolutionary, look no further, say goodbye to, in today's fast-paced world, trust me, you won't believe, hidden gem, must-have, holy grail, next level, "the best part?", repeated "not just X, it's Y", stacked rhetorical questions, triple-adjective lists.
- [ ] Spelling matches the member's market (Australian English by default: mum, colour, organise, favourite).

## 4. Ad naming (so the next round can learn)

Give every concept an ad name the member uses when they launch it, so results can be matched next round:

`CS<YYMMDD>_<PRODUCT>_<ANGLE>_<FORMAT>_H<n>`

Example: `CS261104_HARNESS_NOPULL_YAP_H2` (creative strategist round of 4 Nov 2026, dog harness, the "no pull" angle, yapper, hook 2). Short codes, capitals, no spaces. Put the list in the strategy pack and the creative log.

## 5. The creative log and the feedback loop

`./brand/creative-log.md` (template in `assets/creative-log-template.md`) sits next to the brand file. Create it on the first round; update it, never rebuild it.

**At the end of every round**, add: the date, the job, the angles with their evidence, the ad names, who's filming, and any locked or dead ideas the member gave you.

**When results come in** (the member tells you, or you read them at the next round's step 1), update the same day:
1. Test log row: date, ad name, angle, format, hook, talent, spend, purchases, CPA, hook rate, hold rate, verdict (winner, iterate, retest, dead, too early). Too early means under the minimum-data bar; don't call it.
2. Angles that beat target go to **Winning angles**, with the evidence.
3. Angles that lost a fair test go to **Dead angles**, with the reason. A dead angle can come back only with a different mechanism, not the same one reworded.
4. The best hooks by hook rate and CPA go to **Best hooks**, word for word.
5. Next round's testing order: hooks on the winning body first, then bodies, then formats.

Never write customer names or order details into the log.
