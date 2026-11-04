# Account read (step 1)

Read-only, always. Never change a campaign, ad set, ad, budget or setting.

The goal isn't a performance report (that's eca-meta-ads-4pi). It's a **creative read**: which funnel stages have a working ad, which angles and structures are already in the account, where each ad loses people, what's winning and tiring, and what isn't a creative problem at all.

Contents: 1. Source order · 2. CSV export · 3. Meta Ads MCP pulls · 4. Running creative_read.py · 5. Reading it · 6. Angle inventory · 7. Since last round · 8. Output

## 1. Source order

1. **A recent 4PI report** (14 days or less): read its funnel map, action labels, creative diagnostics and open creative recommendations. Use them as your account read, and only pull fresh data if you need creative copy or per-ad hook and hold numbers the report doesn't carry. Don't contradict a 4PI verdict without fresh numbers.
2. **The official Meta Ads MCP** (tools named `ads_*`): §3.
3. **An Ads Manager CSV export**: §2. Many members can't connect MCPs. The CSV gives the same creative read.
4. **Nothing**: say what that costs ("no gap read, so the angles rest on customer evidence and competitor patterns") and carry on.

## 2. Ads Manager CSV export (what to ask the member for)

1. Ads Manager > **Ads** tab > date range **Last 30 days**.
2. Columns > Customise columns. Tick: Ad name, Campaign name, Ad set name, Delivery, Amount spent, Impressions, Reach, Frequency, CPM, Purchases (or Results), Cost per purchase, Purchases conversion value (or Purchase ROAS), Link clicks, 3-second video plays, ThruPlays, Website URL. Save the column set so next time is one click.
3. Reports > **Export table data** > CSV.
4. **Best extra, 30 seconds more:** the same export with Breakdown > By time > **Day**, at **campaign** level (Campaigns tab), last 7 days. This powers the funnel read. Period frequency is not daily frequency, so without it the funnel stage is a softer call.
5. Optional: Breakdown > Audience segments, for new vs returning customers (Advantage+ campaigns only).

If they can't find a column, carry on without it and note what's missing.

## 3. Meta Ads MCP pulls

Find the account with `ads_get_ad_accounts` (note `currency`, check `is_ads_mcp_enabled`; more than one possible match, ask). If unsure of a field, check `ads_get_field_context` first. Each pull is one `ads_get_ad_entities` call, sorted by `amount_spent_descending`:

Ad-level fields:
```
["id","name","campaign_id","adset_id","creative_id","effective_status",
 "amount_spent","impressions","reach","frequency","cpm",
 "actions:omni_purchase","cost_per_result","purchase_roas","actions:link_click",
 "3_second_video_plays","video_continuous_2_sec_watched_actions",
 "video_thruplay_watched_actions","created_time"]
```

1. **Last 30 days**, level `ad`, `date_preset: "last_30d"`.
2. **Last 7 days**, level `ad`, `date_preset: "last_7d"`.
3. **Daily frequency**, level `campaign`, `date_preset: "last_7d"`, `time_increment: "1"`, fields `["id","name","amount_spent","impressions","reach","frequency","cpm"]`. The funnel read uses the mean of these daily values per campaign.
4. **Creatives**: `ads_get_creatives` with the `creative_ids` from pull 1. Take `body`, `title`, `link_url`, `video_id`, `object_type`, `call_to_action_type`. This gives you the landing page (to group ads by product line), the offer each ad runs, the format, and the copy you'll tag angles from. `product_set_id` present means a catalog ad: no script for those.

Parsing notes (verified on live pulls): values come back as strings (`"A$2,100.76 AUD"`, `"21,641"`, `"1.35%"`). `"Not available"` means no data. `results: "0 (...)"` means zero purchases, so there's no CPA (not a $0 CPA). `3_second_video_plays` usually populates at ad level; if it doesn't, use `video_continuous_2_sec_watched_actions` and label it "2-sec hook rate". Date presets end yesterday, so state the "as of" date. Don't pass both `date_preset` and `time_range`. If a field errors, drop it and retry. On an auth error, stop and ask the member to reconnect; never reuse old numbers or make them up.

To feed the script, write the pulled rows to CSVs with these headers: `ad name, campaign name, ad set name, delivery, landing url, spend, purchases, revenue, impressions, reach, frequency, 3s plays, thruplays, link clicks` (and a separate daily file with `day, campaign name, spend, impressions, reach, frequency`).

## 4. Running creative_read.py

```
python3 <skill>/scripts/creative_read.py ads_30d.csv \
  [--daily campaign_daily_7d.csv] [--compare ads_7d.csv] \
  [--target-cpa 45] [--currency AUD] [--out creative-read.md]
```

It reads Ads Manager column names directly, groups ads by product line (landing page), works out hook rate, hold rate, link CTR and purchases per click per ad, applies the minimum-data bar, finds each ad's first drop-off, compares 7-day against 30-day when you pass `--compare`, decodes the funnel from daily frequency, and lists the ad names for you to tag. Read its output, don't paste it at the member.

## 5. Reading it

**Bands** (the same as the 4PI framework, so members never get two answers):

| Metric | Weak | OK | Strong |
|---|---|---|---|
| Hook rate (3s plays / impressions) | under 20% | 20 to 30% | over 30% |
| Hold rate (ThruPlays / 3s plays) | under 15% | 15 to 25% | over 25% |
| Link CTR (link clicks / impressions) | under 0.5% | 0.5 to 1% | over 1% |
| Purchases per link click | judged against the other ads in the same campaign | | |

These are starting points. The account's own best ads are the better benchmark.

**The drop-off (first failing step wins):**
1. Low hook: the first 2 seconds don't stop the scroll. New spoken, visual and text hooks on the same body.
2. Good hook, low hold: the body loses them. Reveal the product earlier, cut filler, re-hook every 5 to 8 seconds.
3. Good hold, low link CTR: they watch but don't click. Fix the CTA or the offer framing.
4. Good CTR, poor purchases per click: **landing page or offer, not a script.** Say it before writing anything. Suggest the member runs the post-click audit in eca-meta-ads-4pi.
5. Good hold, poor CPA: the angle pulls watchers, not buyers. Bring the reason to buy and the offer into the first 15 to 30 seconds, or change the angle.
6. Frequency climbing with CTR falling: fatigue. Refresh the hook first.

**Minimum data before any verdict**: 7 days of delivery and spend of at least 2x target CPA (no target: 2x the campaign's blended CPA, labelled as a data bar only). Fewer than about 1,000 impressions: don't read rates at all. High ROAS on tiny spend is noise.

**Funnel read** (mean daily frequency per campaign): under 1.15 TOF, 1.15 to 1.40 MOF, over 1.40 BOF, over 2.0 saturated. Cross-check with CPM: low CPM and low frequency is confirmed TOF. CPM and frequency both rising is the loudest warning there is: the funnel is drying up and needs new TOF creative. TOF ads with a worse CPA are doing their job; don't call them failures.

**Image vs video**: image ads show no video metrics, which is normal. Image CPM is cheaper than video CPM, so don't compare them like for like.

## 6. Angle inventory

Tag every ad with spend in the window (from its name, body and title, and the video if you can watch it):
- **Angle**: the reason to buy it sells, in a few words ("no pressure on lashes", "cheaper than a cleaner").
- **Hook type**: outcome first, counter-conventional, problem agitation, founder story, mechanism reveal, social proof first, before/after, comparison, situation callout, story in motion, pattern interrupt, offer-led.
- **Format**: yapper, demo, founder, 3 reasons, comment reply, us vs them, testimonial, unboxing, static, carousel, catalog.
- **Funnel position** from its campaign's frequency and its own CPM.

Then read the gaps: no TOF hooks (every ad offer-led), every winner the same structure, nothing answers the top objection, one product line takes 80% of spend, a winning angle with only one hook ever tested. The over-used combinations tell you what not to make; the missing ones tell you what to make.

## 7. Since last round

If `creative-log.md` lists ads from a previous round, find them in the data by their names. For each: launched or not, spend, purchases, CPA, hook and hold rate, verdict (winner, iterate, retest, dead, too early). Put them in the log (`quality.md` §5) and open the strategy page with one line on what last round taught you.

## 8. Output (goes in the strategy pack)

- Data source and window, with the "as of" date and currency.
- Product lines by spend, with CPA.
- Funnel coverage per campaign, one line each.
- The 3 to 5 findings that drive this round, each with its number.
- What's winning (iterate it) and what's tiring (replace it).
- **Not a creative problem**: landing pages, offers or product lines a script won't fix.
