# The Five Landing Page Formats

Each format uses the same ten-element framework (`framework.md`) in a different order and emphasis. Pick by what the **ad** is doing. If unsure, recommend one and explain why in a line.

---

## 1. Hero Product — `page.eca-lp-hero.json`
**Use when:** the ad drives straight to one product with a clear promise. The default, and the safest choice for cold traffic on a single hero SKU.

**Section order**
1. `eca-lp-hero` — hook + image + CTA + risk-removal line
2. `eca-lp-benefits` — 3–5 outcome-led benefits
3. `eca-lp-proof` — demonstration/stats
4. `eca-lp-how-it-works` — numbered steps
5. `eca-lp-testimonials` / `eca-lp-reviews-embed`
6. `eca-lp-guarantee`
7. `eca-lp-faq`
8. `eca-lp-offer` — product + buy + final CTA

## 2. Listicle — `page.eca-lp-listicle.json`
**Use when:** the ad is "N reasons / N ways / N things", curiosity-led, or educational. Reads like content, sells like a page.

**Section order**
1. `eca-lp-hero` — the listicle promise ("7 reasons people are switching"). **No CTA button here** — leave the hero's button blank; the page hasn't earned the ask yet.
2. `eca-lp-listicle` — the numbered items (image left/right/alternating/none, set in the theme editor), then the **closing block** that introduces the product, then the CTA — with text that follows from the list ("Ditch the machine — try it"), not a generic "Shop now".
3. `eca-lp-proof`
4. `eca-lp-testimonials`
5. `eca-lp-guarantee`
6. `eca-lp-faq`
7. `eca-lp-offer`

**Item length — this matters.** Each numbered item needs **1-2 full paragraphs after its headline**, not a one-liner. Paragraph one names the problem or insight in the reader's world; paragraph two shows how it plays out differently with the product. A listicle of one-line bullets reads like a feature list and converts like one — the depth is what makes it feel like an article worth reading.

**Note:** each list item should stand alone and end with a reason to keep reading. It must feel like an article that convinces first — the product arrives *after* the list, as the conclusion the reader has already been led to.

## 3. Social Proof — `page.eca-lp-social-proof.json`
**Use when:** the ad leans on reviews, UGC, testimonials, or "everyone's switching". Proof does the selling; the copy just frames it.

**Section order**
1. `eca-lp-hero` — social-proof hook + rating/count
2. `eca-lp-proof` — the headline numbers (rating, customers, results)
3. `eca-lp-visual-proof` — real customer photos and videos (UGC), the strongest proof on the page
4. `eca-lp-testimonials` — 6+ quotes, varied objections
4. `eca-lp-reviews-embed` — the live review app feed
5. `eca-lp-benefits` — why they say that
6. `eca-lp-guarantee`
7. `eca-lp-faq`
8. `eca-lp-offer`

## 4. Kit / Subscription Bundle — `page.eca-lp-kit.json`
**Use when:** the ad sells a bundle, kit, or subscription. The job is making the value obvious and the commitment feel safe.

**Section order**
1. `eca-lp-hero` — the kit promise + what it replaces
2. `eca-lp-in-the-box` — image of everything laid out in one column, itemised list with values in the other
3. `eca-lp-benefits` — the outcome of having the whole kit
4. `eca-lp-how-it-works` — for subscriptions: delivery cadence, skip/cancel, how to change it
5. `eca-lp-proof`
6. `eca-lp-testimonials`
7. `eca-lp-guarantee` — for subscriptions, lead with "cancel anytime"
8. `eca-lp-faq` — heavy on commitment objections
9. `eca-lp-offer` — the bundle/subscription offer + saving

## 5. Advertorial — `page.eca-lp-advertorial.json`
**Use when:** the ad is story-led, founder, or news/native style. Reads as an article; the product arrives as the resolution.

**Section order**
1. `eca-lp-hero` — editorial headline + byline/dateline feel (no hard-sell chrome)
2. `eca-lp-article` — the long-form story body with inline images and soft CTAs
3. `eca-lp-proof`
4. `eca-lp-testimonials`
5. `eca-lp-guarantee`
6. `eca-lp-faq`
7. `eca-lp-offer` — the offer, arriving as the natural conclusion

**Required:** advertorials must carry a visible **advertising disclosure** (e.g. "Advertisement" / "Sponsored"). Keep the founder voice first-person and the story true — no invented awards, press or quotes. (The `eca-blog-writer` skill's advertorial framework covers the narrative structure in depth.)


---

## Sections on every page

- **`eca-lp-about`** — the human touch at the foot of every format: founder/team photo, a short story in their own voice, name and role. Use the real story from `brand-data.md` §1. Never invent a person, a quote, or a photo of one.
