# Connectors that make Brand Intelligence valuable

The build pulls from whatever's connected. With nothing connected it still works off the website + web research — but these connectors turn a decent profile into a sharp, evidence-backed one. At the start of a build (SKILL.md → Mode A, step A1): **check what's connected, recommend the gaps that matter for this brand, offer to help connect them, and degrade gracefully if the member skips.** Map each suggestion to what it unlocks so the value is obvious.

> How to suggest: only flag connectors that aren't already connected. Use the connector registry to surface them, or point the member to **Customize → Connectors** in the desktop app. Keep it to the few that move the needle — don't dump the whole list.

## Essential — connect these

### Shopify
The store's source of truth. Unlocks exact **products, prices, variants, collections** (Section 4), **offers / subscriptions** (Section 7), **units sold and other proof** (Section 8), and **real customer & order data** for the ICP (Section 12). Without it, product facts are scraped from the live site — workable, but you can miss variants, current prices, and anything not on the page.

### Klaviyo
The email/SMS brain. Unlocks **lists & segments** (real ICP data, Section 12), **campaign history and existing email copy** (a strong voice reference, Section 3), and **sender identity & channels** (Section 17). Bonus: it also powers the email-marketing and promotional-campaign skills, so it's worth connecting once.

### A reviews app (Judge.me, Yotpo, Okendo, Stamped, etc.)
Reviews are the **heart of Mode A**. They're the single richest source for the **why-people-buy transformation** (Section 2), **proof — star rating, counts, hero quotes** (Section 8), **objections** (Section 9), and **voice-of-customer language** (Section 12). A direct connector beats scraping the on-site widget (which is often JavaScript-rendered and hard to read).

## Highly useful — strongly recommended

### Claude in Chrome extension + Claude for Desktop
Make sure **both the desktop app and the Chrome extension are installed and connected.** This lets the skill **render JavaScript-heavy pages** that plain fetching returns empty — review widgets, competitor sites, the **Meta Ads Library**, and Reddit/Quora/forum threads. It's what makes the **market and competitor research** (Sections 10, 11) and the **forum-first voice-of-customer step** actually reach real pages instead of stalling on a blank shell.

### Semrush
Unlocks **keyword volumes, the category term to own, and competitor organic/keyword data** → SEO / content territory (Section 15), and sharpens the market and competitor framing (Sections 10, 11).

## Optional — nice-to-have

### Web analytics — GA4 or Microsoft Clarity
Validate the **ICP (Section 12)** with real audience demographics and on-site behaviour instead of inference. Microsoft Clarity also adds session recordings and heatmaps that reveal where buyers hesitate (useful for objections, Section 9).

### Meta Ads Library *(not a separate connector)*
See competitors' **live ads** for differentiation and angle ideas (Section 11). It's accessed through the browser, so it rides on the Claude in Chrome extension above.

### Google Search Console *(optional)*
The **real search queries** bringing people to the site → SEO / content territory (Section 15).

## Rules for using connectors in the build
- Detect what's already connected; **suggest only the missing ones**, and only those relevant to this brand.
- **Never block.** If a connector is absent, fall back to the website + web research and mark the affected sections **lower-confidence in Section 18**.
- When a connector *is* present, prefer it over scraping — live data beats a parsed page.
