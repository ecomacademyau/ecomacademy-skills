# Ad Copywriting Skill (Meta / Facebook & Instagram)

Turn a landing page into launch-ready Meta ad copy: ten tight headlines and two primary-text variations, packaged into a 3-2-2 testing structure you can hand straight to a media buyer. Claude acts as a Creative Director + direct-response copywriter and runs it as a guided, step-by-step flow.

## What it does

Given a landing page and a few inputs, Claude will:

1. Load **your** brand voice (via `eca-brand-intelligence`) and **your customer's language** (personas + reviews, if available).
2. **Analyse the landing page** and adopt the brand's tone.
3. Gather the campaign inputs — USPs, target segments, offer, objective.
4. Write **10 headlines** (≤45 characters), spread across segments and emotion-vs-utility angles.
5. Write **2 primary texts** — a short punchy one and a long emotion-led one with benefit bullets + CTA.
6. Package the approved copy into the **3-2-2 method** (3 creatives of one angle, 2 headlines, 2 primary texts).

It's **interactive**: Claude pauses for your approval between each stage so you steer the output.

## What you need

- A **landing page** (URL or pasted content).
- Recommended: the **`eca-brand-intelligence`** skill for voice, and **`eca-persona-builder`** (or a personas/reviews file) for customer language. Without them the flow still runs — copy is just stronger with them.
- For URL analysis of a JS storefront: **Claude in Chrome** browser tools.

## How to use it

Just point Claude at a page:

- "Start with LP" — then paste your landing page
- "Write me Meta ad headlines for this landing page: [url]"
- "I need primary text for our [product] campaign"
- "Give me 10 Facebook headlines and two primary texts for cold traffic"

Claude analyses the page, gathers inputs, and walks you through headlines → primary text → 3-2-2.

## Files

```
eca-ad-copywriting/
├── SKILL.md                  # the guided workflow (brand-agnostic)
├── config.md                 # YOUR settings — the only file to edit when forking
├── references/
│   ├── copy-rules.md         # hard rules: char limits, headline + primary-text briefs, 3-2-2
│   └── frameworks.md         # the strategy: data-driven, funnel TOF/MOF/BOF, emotion+utility, FOMO
└── README.md
```

## Forking for a different brand

The workflow logic is brand-agnostic — the only brand-specific content lives in `config.md`. To reuse this skill for another brand:

1. Copy the whole `eca-ad-copywriting/` folder (rename if you want both side-by-side).
2. Open `config.md` and edit:
   - **Our brand** — brand name and where its voice lives (`eca-brand-intelligence` fork or a brand file).
   - **Customer language sources** — paths to a personas file and/or reviews export.
   - **Market** — default region for spelling/currency.
   - **House copy limits** — only if your account differs from the defaults.
   - **Output preferences** — deliver in chat and/or save a file.
3. Don't touch `SKILL.md` or `references/` — they work for any brand.

## Sharing with your team

This skill ships inside the **eca-ecommerce-agent** plugin in the EcomAcademy marketplace. Installing that one plugin keeps members current with every skill in the bundle. To share standalone, package the folder as a `.skill` file (a zipped skill directory).
