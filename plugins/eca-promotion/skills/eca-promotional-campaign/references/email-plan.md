# Email + SMS Plan

The promotional send arc. Self-contained — this skill doesn't depend on any other skill for the email logic. Every message follows one rule above all: **it stands alone.** A recipient may only ever see one email, one SMS, or one re-mail. Each must carry the full offer, the code, the deadline, and a reason to act. No "as we mentioned yesterday", no "watch for tomorrow's email".

## The arc at a glance

| # | Message | Channel | Audience | Template style | Job |
|---|---------|---------|----------|----------------|-----|
| 0 | Early-Access **capture** (sign-up page/popup) | Site + ads | TOF traffic | — | Build the early-access list |
| 1 | Early Access | **Email + SMS** | Early-Access list | Banner + CTA + text | First dibs; reward loyalty; build anticipation |
| 2 | Public Launch | **Email + SMS** | All subscribers | Banner + CTA + text | Sale is live; max clarity |
| 2b | Re-mail to unopened (~12h later) | Email | Launch non-openers | (same as #2, new subject) | Recover the missed opens |
| 3 | Top Picks | Email | Engaged | Banner + text + products | Hero SKUs on offer; reduce decision friction |
| 4 | Time Check ("X days to go") | Email | Engaged | Banner + CTA + text | Mid-sale urgency |
| 5 | Best Sellers | Email | Engaged | Banner + text + products | Social-proof close |
| 6 | Last Chance | **Email + SMS** | All subscribers | Text only (email) | Final push; strongest urgency |
| 7 | Offer Extended *(only if extended)* | Email | Engaged | Banner + CTA + text | Explicit extension — never shadow-extend |

SMS fires only on the three highest-leverage beats — Early Access, Launch, Last Chance — to avoid burning the channel.

## What each message does

### 0 — Early-Access capture (page/popup)
Not an email — a landing page or on-site popup that offers early access in exchange for an email/SMS opt-in. Copy: a single promise ("Get first dibs on [event] — [headline offer], before everyone else"), one field, one button. This feeds the Early-Access list that message #1 sends to.

### 1 — Early Access (Email + SMS)
First dibs for the captured list / VIPs. Keep it short: one line on what they're getting and why they're first, one button. No product grids. **Email:** Banner + CTA + text. **SMS:** "You're in early 👀 [offer] is live for you now — [link]. Code [CODE]. Ends [date]."

### 2 — Public Launch (Email + SMS)
The sale is live for everyone. Maximum clarity, minimum friction: the offer, the code, the end date, one button. **Email:** Banner + CTA + text. **SMS:** "[Offer] is ON 🎉 [link]. Use [CODE]. Ends [date]."

### 2b — Re-mail to unopened (~12h after launch)
The exact launch email resent to people who didn't open #2, with a **different subject line** (and ideally a different preview). Same body, same offer. This alone typically recovers a meaningful chunk of opens.

### 3 — Top Picks
Lead with 4–8 hero SKUs that are on offer, with discounted prices visible. Short intro line, product grid, one CTA (or per-product CTAs). Banner + text + products.

### 4 — Time Check ("X days to go")
Mid-sale urgency anchored to the deadline ("3 days left", "halfway through"). One banner, one button, supporting copy. Banner + CTA + text.

### 5 — Best Sellers
"Not sure? Here's what everyone's buying." Top 4–6 bestselling discounted SKUs with star ratings / review snippets. One CTA at the bottom. Banner + text + products. **Inventory check before send** — don't headline a SKU that's about to sell out.

### 6 — Last Chance (Email + SMS, ~24h before end)
Final push, strongest urgency. **Email:** often text-only for a raw, personal "quick note" feel — 2–3 sentences, one CTA, signed by the founder. **SMS:** "Last chance ⏳ [offer] ends [time] tonight. [link] — code [CODE]."

### 7 — Offer Extended (only if genuinely extended)
A separate, explicit message — "We're keeping it open until [new date]." Never silently extend a sale you said was ending; it breaks trust and the website/discount dates must match the new copy.

## Drafting each message

For every email, produce:

- **Role in the arc** (from the table above)
- **Subject line — 3 A/B variants**, under ~50 chars where possible, mixing curiosity / benefit / specificity / urgency. No clickbait, no "!!!".
- **Preview text** — complements the subject (doesn't repeat it), ~80–120 chars. The re-mail (#2b) needs a fresh subject AND preview vs the launch.
- **Template style** — one of the three below.
- **Hero-image brief** — subject of the image, mood, aspect, and what's explicitly NOT in it (specific enough to brief a designer). For promos, put the offer price/mechanic in the banner.
- **Body copy** — full, on-brand copy structured for the template.
- **Single primary CTA** — one button. Secondary text links are fine; one button.
- **Standalone check** — confirm a cold reader gets the offer, code, deadline, and click target.

For SMS, produce: the copy (≤160 chars where possible), the link, and confirm code + deadline are present.

Pull in the `brand-intelligence` skill (if installed) for voice when writing copy; otherwise work from the brand tone the user gives you and the notes in `campaign-config.md`.

## Template styles (block-arrangement patterns)

These are three ways to arrange blocks inside the one master template — not three separate templates.

**1. Banner + text + products** — hero banner, body copy, product grid (2–4, max ~6). For Top Picks and Best Sellers. Marries a visual hook with browsable SKUs.

**2. Text only** — no banner, no grid; copy + one CTA, styled like a personal note. For Last Chance (raw urgency) and founder-voice moments.

**3. Banner + CTA + text** — one banner, one prominent button right under it, supporting copy below (button BEFORE text — click first, read second). For Early Access, Launch, Time Check, Offer Extended — anywhere one clear action wins.

**Mix styles across the arc** so the inbox doesn't feel repetitive. A typical promo run: CTA → CTA → products → CTA → products → text-only.

## Mobile-first reminders
- ~60% of opens are mobile. Banners must read at 320px; sale price legible on a phone.
- Single-column layouts; CTA buttons ≥44px tall.
- Subject + preview text drive ~80% of the open decision — spend effort there.

## Critical promo rules
- **Dates in copy = Shopify discount expiry.** Always.
- **Don't shadow-extend.** Use message #7 if extending.
- **Inventory check before Best Sellers / Top Picks.** Don't headline a SKU that runs out mid-send.
- **SMS sparingly.** Three beats only (Early Access, Launch, Last Chance) unless the user asks otherwise.
