# The Landing Page Framework — the ten elements

Every ECA landing page carries these ten elements. The *order* and *emphasis* shift by format (see `page-formats.md`), but nothing gets skipped — each one answers a question the visitor is asking, in the order they ask it.

> **The one rule above all: message match.** The page must continue the exact promise the ad made. If the ad promised "restaurant meals without the cooking", the page opens with that — not a generic brand welcome. Mismatch between ad and page is the single biggest post-click conversion killer, and it's what the `eca-meta-ads-4pi` skill flags as a landing-page problem.

---

## 1. Hook that matches the ad
The headline is the ad's promise, continued. **Echo the ad's own language** — ideally its strongest line, near-verbatim. The visitor should feel they landed in the right place within one second.
- Specific over clever. State the outcome, not the category.
- Sub-headline: one line that expands the promise or handles the first objection.
- *Ask:* would someone who just clicked that ad recognise this as the same offer?

## 2. A corresponding image (or video)
The visual must match the angle, not just be "a nice product shot". A founder-story ad → the founder. A before/after ad → the before/after. A demo ad → the demo.
- Best case: use a frame or clip from the actual ad creative — maximum continuity.
- Show the product in real use, not floating on white.

## 3. Clear CTA with risk removal — above the fold
One primary action, visible without scrolling, with the risk-reversal sitting right under it.
- Button text states the action + outcome ("Start my first box"), not "Submit".
- Under it, one line of risk removal: guarantee, free shipping, cancel anytime.
- One action per page. Competing CTAs split the decision.

## 4. Benefit / outcome / transformation
What life looks like after. Lead with the transformation, not the feature list.
- Before → after framing works: the struggle they arrived with, the state they get.
- Three to five benefits, each an *outcome* ("dinner on the table in ten minutes"), with the feature as support ("one pan, no prep").
- Pull the real transformation from `brand-data.md` §2 (why people buy).

## 5. Proof that the outcome is real
Immediately after the promise, prove it. This is where scepticism peaks.
- Demonstration (a short clip of it working), data/results, a specific number, a comparison, or an authority signal.
- Specific beats superlative: "4.9 from 2,000+ reviews" beats "loved by everyone".
- **Never invent proof.** Use only what's in `brand-data.md` / the store. If there's none, use a placeholder and tell the member what to supply.

## 6. How it works / what's included
Remove the "but how does this actually work for me?" friction.
- Three to four numbered steps, plainly worded.
- For kits/bundles/subscriptions: itemise exactly what arrives, with values if relevant.
- Set delivery/timing expectations here.

## 7. Risk removal / guarantee — **required on every page**
Every landing page must carry a risk reversal. If `brand-data.md` doesn't have one, **ask the member** — money-back window, free returns, warranty, free shipping, cancel-anytime, or a satisfaction promise. If they truly have none, tell them plainly it will cost conversions and help them find the smallest credible one. Never invent it.

State it properly, in its own moment: what it is, how long, and how to claim.
- Plain language, no asterisks. "Try it for 30 days. Don't love it, we refund you."
- Repeat it near every CTA in short form.

## 8. Reviews and social proof
Real customers in their own words. Use the store's **review app block** where one exists (Judge.me, Loox, Okendo, Yotpo) rather than pasting text.
- 3–6 quotes chosen to answer *different* objections, with names/photos if available.
- Include a mildly imperfect review if you have one — it raises credibility.
- Star rating + review count near the top CTA.

## 9. FAQs
Answer the real objections that stop the sale. Source them from `brand-data.md` §9 (objections) and §12 (pre-purchase questions) — not invented ones.
- 5–8 questions, answer-first (lead with the answer, then the detail).
- Cover: does it work, is it worth it, how do I use it, what if it doesn't suit me, shipping/returns.
- Emits **FAQPage JSON-LD** so AI answer engines can cite the page.

## 10. Offer, product and final call to action
Close with the actual offer and a way to buy without leaving.
- Restate the offer plainly: what they get, the price, any bundle saving or subscription discount.
- Use the theme's **native product/buy-buttons** block so it's a real add-to-cart, not a link to another page.
- Final CTA + the guarantee one more time.

---

## Copy rules
- **Voice**: the brand's, from `brand-data.md` §3. Never a generic DTC voice.
- **Claims**: only what §6 says is safe. No invented stats, awards, reviews or guarantees.
- **Specificity**: real numbers, timeframes, and objects. Vague copy doesn't convert or get cited.
- **Placeholders**: anything you can't source becomes an obvious `{{PLACEHOLDER}}` plus a clear note on what to supply — never a plausible-sounding invention.
- **Scannability**: short paragraphs, one idea per block, subheads that carry the argument if you only read them.
- **Every scroll-length needs a CTA** — repeat the primary action after each major block. *(Exception: listicles hold the CTA until after the list.)*
- **Urgency only if it's true** — a real deadline, genuine limited stock, a launch window or a price rise can be stated near the CTA. Never fake a countdown or an "only 3 left": it damages trust and can breach consumer law.
