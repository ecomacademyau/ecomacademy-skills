# UGC Scripts — a reusable Claude skill

Writes UGC-style short-form video scripts (for paid ads or organic social) that a founder/member can shoot themselves or hand to a creator. Every script is engineered to **grab attention in the first 3 seconds, hold it, and drive one action** — and sound like a real person, not a brand.

Ships in the marketplace as **`eca-ugc-scripts`**.

## The seven video types

1. **Founder Ad Story** — origin-story monologue that builds trust ("that's me → I need that").
2. **3 Reasons Why** — fast, punchy value, three sharp reasons.
3. **Comment Reply** — answer a real (or representative) comment / objection.
4. **Product Review** — authentic recommendation, social-proof led.
5. **Interview (podcast/street)** — Q&A format, credibility + relatability.
6. **Us vs Them / Before–After** — differentiate vs the status quo, show the change.
7. **Unboxing** — desire + curiosity, what arrives and the first impression.

## How it works

```
ugc-scripts/
├── SKILL.md                     # Router: load brand inputs → pick/recommend a type → write script → shoot notes
├── config.md                    # Fallback brand inputs (used only if brand-data.md is absent)
├── README.md                    # This file
└── references/
    ├── 00-engine.md             # Shared: grab→hold→act, hook engine, timing, voice rules, output format
    ├── founder-ad-story.md      # Full framework (from the founder-ad worksheet)
    ├── 3-reasons-why.md         # Live
    └── comment-reply.md         # Live
    (Product Review, Interview, Us-vs-Them/Before-After, Unboxing — coming soon)
```

The member picks a type (or the skill recommends one based on their goal). The skill loads the brand's real details — **preferring brand-intelligence's `brand-data.md`**, falling back to `config.md` — then writes the script with hook options, per-beat timing, on-screen/b-roll notes, and shooting guidance.

## Brand inputs — two sources

- **With brand-intelligence installed:** the skill reads `brand-data.md` (founder story, product, frustration, audience, voice, proof, objections, transformation). Nothing else to set up.
- **Standalone:** copy `config.md`, fill the brand inputs once, and all seven types run off it.

## Status

**Live now (3):** Founder Ad Story, 3 Reasons Why, Comment Reply — fully dialled in.
**Coming soon (4):** Product Review, Interview, Us vs Them / Before-After, Unboxing — being added in upcoming releases.

## Fork for another brand

Brand-agnostic logic; brand specifics live in `brand-data.md` or `config.md`. To reuse: install/point at the brand profile, or fill `config.md`. The reference frameworks don't change between brands.
