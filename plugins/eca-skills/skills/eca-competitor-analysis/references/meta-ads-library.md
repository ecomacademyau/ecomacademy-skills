# Meta Ads Library Walkthrough

The Meta Ads Library is a free public tool showing every ad currently running across Facebook and Instagram. It's the single best window into what a competitor is actually spending money on — and what's working for them.

URL: `https://www.facebook.com/ads/library/`

## Tooling

The Ads Library is a heavy JavaScript app — it will not render through a plain fetch. Use the Claude in Chrome browser tools: navigate to the search URL, let it load, then read the rendered page text and scroll to load more results.

## Steps

1. **Open the library** and set:
   - **Country** → the target region (default from `config.md`; ads are country-scoped).
   - **Ad category** → "All ads".
2. **Search the competitor** by brand / Facebook Page name. If the brand name returns nothing, try variations (with/without "official", country suffixes) — they may run under a slightly different Page name. No results after that is itself a finding.
3. **Open the Page's active ads** and work through them.

You can often jump straight to a search with a URL like:
`https://www.facebook.com/ads/library/?active_status=active&ad_type=all&country=AU&q=BRANDNAME&media_type=all`
(swap `country` and `q`).

## What to record

### Volume & longevity (the most important signal)
- **How many ads are active** right now.
- **How long the longest-running active ads have been live** (each ad shows a "Started running on" date). An ad that's been running for months is a *proven winner* — competitors don't keep paying for losers. New ads are tests. Weight your attention toward the long-runners.
- **How many variations** of the same concept are running (signals a concept they're scaling).

### Angles & hooks
- The **lead problem or desire** each ad opens with.
- **Recurring themes** across the set — the messages they keep betting on.
- **Offers featured** in the ads (discounts, bundles, free shipping, guarantees).

### Formats
- UGC / creator-style vs polished brand production.
- Static image vs video vs carousel.
- Which angle each format is carrying (e.g., "video for the founder story, static for the discount").

### Standout ads worth stealing
Pick the few strongest and describe each concretely enough to brief a creative: the hook line, the visual, the format, the offer, and why it likely works. This is the part the operator will act on.

## Turning it into ad ideas

Cross the competitor's proven angles with the **gaps from our brand comparison**:
- An angle they run hard that we've never tried → test our version.
- A claim they *can't* make that we can (e.g., we have a subscription, they don't) → lead with the angle they can't match.
- A format they over-rely on → differentiate with the one they're ignoring.

Each idea in the report should name the gap or winner it came from, so it's defensible — not a random brainstorm.
