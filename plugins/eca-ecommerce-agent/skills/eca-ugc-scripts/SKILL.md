---
name: eca-ugc-scripts
description: Write UGC-style short-form video scripts a brand can shoot themselves or hand to a creator — built to grab attention in the first 3 seconds, hold it, and drive an action. Use this skill whenever the user wants a video script, UGC script, ad script, TikTok/Reels/Shorts script, organic video idea, a "founder story" video, a "3 reasons why" video, a comment-reply video, a product-review video, an interview/street/podcast-style video, an "us vs them" or "before/after" video, an unboxing video, a creator brief, a hook for a video, or says "script me a video", "give me a UGC ad", "what should I film", "turn this product into a video", or "I need content for ads/social". Also trigger when the user is choosing what kind of video to make and wants help picking the format for their goal. Covers a growing set of UGC video types — Founder Ad Story, 3 Reasons Why, and Comment Reply are live now; Product Review, Interview, Us-vs-Them/Before-After, and Unboxing are being added. Works for any brand: it prefers the brand profile in brand-intelligence's `brand-data.md`, and falls back to this skill's `config.md`.
---

# UGC Scripts

Turn a brand + a goal into a ready-to-shoot short-form video script. Every script is engineered on the same spine — **grab → hold → act** — but each of the seven video types has its own hook logic and beats. The member picks a type (or you help them choose), you load the brand's real details, then you write the script and the shooting notes.

These scripts are meant to be *filmed*, by the founder/member or a creator — so they must sound like a real person talking, never like a brand reading ad copy. Read `references/00-engine.md` once per session; it holds the shared philosophy, the hook engine, timing, voice rules, and output format that all seven types use.

## Step 1 — Load the brand inputs (do this first)

Every script needs the brand's real specifics or it comes out generic. Get them in this order:

1. **Prefer `brand-data.md`** — if the brand-intelligence skill's `brand-data.md` exists, read it. It already has the founder story, hero product, the category frustration, the audience, voice, proof, objections, and the why-people-buy transformation — which is exactly what these scripts need. Use it.
2. **Fall back to `config.md`** — if there's no brand profile, read this skill's `config.md` for the minimum inputs, and ask the member for anything still missing (don't invent product facts, prices, or claims).
3. **Confirm the essentials** for the chosen type before writing: the hero product in one line, the specific frustration/feeling, who it's for, and any proof or real detail you'll lean on.

## Step 2 — Choose the video type

If the member already knows which type they want, go straight to its reference file. If they're not sure, help them choose based on their **goal** — match it, don't just list options:

| If the goal is… | Best type | Status | File |
|---|---|---|---|
| Build trust / tell the brand's origin (cold audiences) | **Founder Ad Story** | ✅ Live | `references/founder-ad-story.md` |
| Make the value obvious fast / punchy paid ad | **3 Reasons Why** | ✅ Live | `references/3-reasons-why.md` |
| Handle an objection that stops people buying | **Comment Reply** | ✅ Live | `references/comment-reply.md` |
| Authentic recommendation / social proof | **Product Review** | 🔜 Coming soon | — |
| Credibility + relatability, low-production | **Interview (podcast/street)** | 🔜 Coming soon | — |
| Differentiate vs the status quo / show a transformation | **Us vs Them / Before-After** | 🔜 Coming soon | — |
| Desire + curiosity / show what arrives | **Unboxing** | 🔜 Coming soon | — |

**Availability:** only the ✅ Live types are built right now. If a member wants a 🔜 type, write them the closest Live type instead and let them know that one's on the way — don't attempt a coming-soon type from scratch.

A quick way to decide (live types): cold traffic that doesn't know the brand → **Founder Ad Story**; warmer audiences weighing it up → **3 Reasons Why**; a specific doubt that stops the sale → **Comment Reply**. When in doubt, recommend one, say why, and offer a second to test against it.

## Step 3 — Write the script

Open the chosen type's reference file and follow its beats. For every script:

- **Lead with the hook** (0–3s). Generate options using the hook engine in `00-engine.md`, vary the "spice," and present a few to choose from — never ship one untested hook.
- **Hold with specifics** — real moments, real numbers, real objects beat polished claims. This is where videos die.
- **End on one clear action** — one ask, named to one person.
- **Keep the voice human** — if a line sounds like a brand wrote it, rewrite it the way they'd say it to a friend.
- **Hit the timing** — show rough seconds per beat and a total; flag if it runs long.

## Step 4 — Deliver it to film

Output (format detailed in `00-engine.md`): the video type and why it fits; 3 hook options (safe / medium / spicy) to test; the full script as spoken lines with per-beat timing; on-screen text / b-roll / action notes in brackets; and shooting notes (framing, takes, what to avoid). Make it copy-paste ready for the member or a creator brief. Save longer scripts as a file when the member wants to keep or hand them off.

## Reusing for other brands

Brand-agnostic by design. With brand-intelligence installed, it just works off `brand-data.md`. Without it, copy `config.md`, fill the brand inputs once, and the seven types run off that. See `README.md`.
