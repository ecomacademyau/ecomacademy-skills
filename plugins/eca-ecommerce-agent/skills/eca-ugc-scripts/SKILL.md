---
name: eca-ugc-scripts
description: Write UGC-style short-form video scripts a brand can shoot themselves or hand to a creator — built to grab attention in the first 3 seconds, hold it, and drive an action. Use this skill whenever the user wants a video script, UGC script, ad script, TikTok/Reels/Shorts script, organic video idea, a "founder story" video, a "3 reasons why" video, a comment-reply video, a product-review video, an interview/street/podcast-style video, an "us vs them" or "before/after" video, an unboxing video, a creator brief, a hook for a video, or says "script me a video", "give me a UGC ad", "what should I film", "turn this product into a video", or "I need content for ads/social". Also trigger when the user is choosing what kind of video to make and wants help picking the format for their goal. Covers a growing set of UGC video types — Founder Ad Story, 3 Reasons Why, and Comment Reply are live now; Product Review, Interview, Us-vs-Them/Before-After, and Unboxing are being added. Works for any brand: it prefers the brand profile in brand-intelligence's `brand-data.md`, and falls back to this skill's `config.md`.
---

# UGC Scripts

Turn a brand + a goal into a ready-to-shoot short-form video script. Every script is engineered on the same spine — **grab → hold → act** — but each of the seven video types has its own hook logic and beats. You load the brand's real details, take a short **brief** (who we're targeting, the offer/angle, the avatar, and where the video sends people), help pick the right type **for that funnel stage**, then write the script and the shooting notes.

These scripts are meant to be *filmed*, by the founder/member or a creator — so they must sound like a real person talking, never like a brand reading ad copy. Read `references/00-engine.md` once per session; it holds the shared philosophy, the hook engine, timing, voice rules, and output format that all seven types use.

## Step 1 — Load the brand inputs (do this first)

Every script needs the brand's real specifics or it comes out generic. Get them in this order:

1. **Prefer `brand-data.md`** — if the brand-intelligence skill's `brand-data.md` exists, read it. It already has the founder story, hero product, the category frustration, the audience, voice, proof, objections, and the why-people-buy transformation — which is exactly what these scripts need. Use it.
2. **Fall back to `config.md`** — if there's no brand profile, read this skill's `config.md` for the minimum inputs, and ask the member for anything still missing (don't invent product facts, prices, or claims).
3. **Confirm the essentials** for the chosen type before writing: the hero product in one line, the specific frustration/feeling, who it's for, and any proof or real detail you'll lean on.

## Step 2 — Take the brief (ask before scripting)

Four things shape every choice below. **Pull what you can from `brand-data.md` first, then ask the member only for the genuine gaps** — propose an answer and have them confirm rather than asking cold. Use the AskUserQuestion tool for the quick multiple-choice ones (especially the funnel stage). Don't move on until you have all four.

1. **Funnel stage — who are we targeting?** The big one; it filters the video types in Step 3.
   - **New (TOF)** — cold, doesn't know the brand yet.
   - **Nurture (MOF)** — aware, weighing it up, comparing.
   - **Retain (BOF)** — existing/warm customers, ready to buy (again).
2. **The offer or angle** — what's this video about? A new product, a problem/solution, an event/sale, a bundle. (Check `brand-data.md` §7 Offers and §14 Promo calendar.)
3. **The avatar / persona / ICP** — the one specific person we're talking to. Default to the relevant persona in `brand-data.md` §12 and confirm which fits this video.
4. **The destination** — where the video sends people after watching (product page, collection, landing page, profile/link in bio). Default from `brand-data.md` §17/§7 and confirm.

These four drive the type, the hook, the beats, and the CTA — so lock them before writing.

## Step 3 — Choose the video type (gated by funnel stage)

Different stages need different videos. **Only suggest types whose funnel position includes the member's stage *and* that are Live.** If the best fit for the stage is still coming soon, say so and offer the closest live alternative. (Funnel positions follow the brand's creative-format taxonomy.)

| Video type | Funnel position | Status | File |
|---|---|---|---|
| Founder Ad Story | TOF · MOF | ✅ Live | `references/founder-ad-story.md` |
| 3 Reasons Why | TOF · MOF | ✅ Live | `references/3-reasons-why.md` |
| Comment Reply | TOF · MOF · BOF | ✅ Live | `references/comment-reply.md` |
| Product Review | MOF · BOF | 🔜 Coming soon | — |
| Interview (podcast/street) | TOF · MOF | 🔜 Coming soon | — |
| Us vs Them / Before-After | TOF · MOF | 🔜 Coming soon | — |
| Unboxing | MOF · BOF | 🔜 Coming soon | — |

**Suggest by stage (live types in bold):**
- **New / TOF:** **Founder Ad Story**, **3 Reasons Why**, **Comment Reply** *(coming: Interview, Us vs Them / Before-After)*
- **Nurture / MOF:** **Founder Ad Story**, **3 Reasons Why**, **Comment Reply** *(coming: Product Review, Interview, Us vs Them / Before-After, Unboxing)*
- **Retain / BOF:** **Comment Reply** *(coming: Product Review, Unboxing)*

Within the stage's options, pick by the angle: brand-new-to-you trust → Founder Ad Story; fast value / comparison → 3 Reasons Why; a specific doubt that blocks the sale → Comment Reply. **Recommend one, say why it fits their stage + angle, and offer a second to test against it.** If a member asks for a 🔜 type, write the closest Live one and note theirs is on the way — don't attempt a coming-soon type from scratch. **Founder Ad Story needs real founder details** (from `brand-data.md` §1 or asked from the member); if there's genuinely no founder story to tell, route to a non-founder type (3 Reasons Why or Comment Reply) rather than inventing one.

## Step 4 — Write the script

Open the chosen type's reference file and follow its beats, carrying the brief through:

- **Lead with the hook** (0–3s) from the engine, shaped by the **angle** and aimed at the **avatar** (talk to that one person). Vary the "spice," present a few — never ship one untested hook.
- **Hold with specifics that fit the stage** — TOF leans on the relatable problem/story; MOF on proof, comparison, and objections; BOF on the offer and how easy it is to buy (again). Real moments and numbers beat polished claims.
- **End on one clear action** — the **destination** is the CTA; one ask, named to one person.
- **Keep the voice human** — if a line sounds like a brand wrote it, rewrite it the way they'd say it to a friend.
- **Hit the timing** — show rough seconds per beat and a total; flag if it runs long.

## Step 5 — Deliver it to film

Output (format detailed in `00-engine.md`): the video type and why it fits; 3 hook options (safe / medium / spicy) to test; the full script as spoken lines with per-beat timing; on-screen text / b-roll / action notes in brackets; and shooting notes (framing, takes, what to avoid). Make it copy-paste ready for the member or a creator brief. **Standing rule: once the member approves the script, always export the final version to a Word (.docx) document (via the docx skill) and share it — automatically, every time.** See `00-engine.md` → "After approval — export to Word".

## Reusing for other brands

Brand-agnostic by design. With brand-intelligence installed, it just works off `brand-data.md`. Without it, copy `config.md`, fill the brand inputs once, and the seven types run off that. See `README.md`.
