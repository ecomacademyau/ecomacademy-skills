# On-Site (Website) Design Spec

When the sale goes live, the website must carry the same offer as the inbox and the ads — instantly, on every key page. A customer who clicks an ad or email and lands on a normal-looking homepage assumes the sale isn't real. This spec covers the four surfaces to change, plus the theme swap and mobile checks.

Produce this as a checklist + the actual copy for each element, so the user can apply it (or, in plan+build mode with a store connector, apply some of it directly).

## 1. Announcement bar (every page)

A sitewide bar at the very top. The single most important on-site change — it's the one thing on every page.

- **Offer copy:** the headline offer in a few words ("[X]% OFF SITEWIDE — CODE [CODE]" / "2 FOR $48 THIS WEEK").
- **CTA:** "SHOP NOW" linking to the sale collection.
- **Optional features:** a **countdown timer** to the end (great for urgency); a **distinct colour** so it reads as "sale mode" (but stay within brand — see `campaign-config.md`).
- Keep it to one line that reads on mobile.

## 2. Homepage

- **Main banner / hero:** big "YOUR OFFER HERE" treatment — the offer headline, a SHOP NOW button, and a hero image. This replaces the everyday hero for the sale window.
  - Offer line, CTA, and image all on-brand. Don't bury the offer below the fold.
- **Featured products / collection:** an "Our Best Deals" row — the sale collection or hand-picked discounted SKUs, with a "Shop all deals" button.
  - Pick the collection that best represents the offer; lead with the strongest deals.

## 3. Collection page

The page customers land on from "Shop the sale".

- **Announcement bar:** as per homepage (carries through).
- **Offer banner:** "YOUR OFFER HERE" at the top of the collection, matching the homepage.
- **Offer buttons / links:** up to ~4 quick links (OFFER 1 / OFFER 2 / OFFER 3 / OFFER 4) so customers can jump to sub-offers or categories.
- **Sort best deals first:** order the collection so the strongest deals appear first.
- **Strikethrough pricing:** show the original price struck through next to the sale price wherever possible ($23.00 ~~$99.00~~) — the saving must be visible.
- **Offer badges:** a "YOUR OFFER" badge on product cards to emphasise what's on sale.

## 4. Product page

- **Announcement bar:** as per homepage.
- **Offer badge:** "YOUR OFFER" badge on the product image.
- **Strikethrough price:** sale price with the original struck through; include the buy-now-pay-later message if used.
- **Upsells:** ensure upsell / cross-sell widgets are working — a sale drives traffic, so capture AOV.

## 5. Theme swap (timeline-linked)

- **At public launch:** switch to the sale theme (the above changes live). This is an explicit timeline step.
- **At close:** revert to the everyday theme and remove the announcement bar, banners, and badges. Deactivate the discount.

## Mobile

**Test every surface on mobile** — announcement bar, homepage banner, collection page, product page. ~60% of traffic is mobile; the offer, the strikethrough price, and the CTA must all read clearly on a phone.

## Rules
- **Match the inbox and ads** — same offer, code, and dates everywhere.
- **Strikethrough + badges = visible saving.** If the customer can't see what they're saving, the sale isn't doing its job.
- **Don't leave it up after close.** Stale "SALE" bars erode trust and train customers to wait for discounts.
