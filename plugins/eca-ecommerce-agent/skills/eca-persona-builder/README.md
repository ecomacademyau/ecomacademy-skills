# Persona Builder Skill (Voice-of-Customer → Personas)

Turn customer reviews into 3–5 detailed marketing personas — each grounded in real benefits, pain points, emotional triggers, buying behaviour and objections — ready to aim ads and copy at.

## What it does

Given a brand's reviews (or other voice-of-customer data), Claude will:

1. Confirm scope — which data, how many personas, what for.
2. Ingest the reviews and run a **nine-part analysis**: benefits, pain points, emotional drivers, purchase motivations, demographics, behaviour, segments, content preferences, objections.
3. Synthesise **3–5 distinct personas**, each with a name, the benefits they value, their pains, emotional triggers, buying behaviour, preferred tone, and a real review quote.
4. Write a **report** — analysis summary + personas + actionable strategy takeaways — saved to your project folder.

Every claim ties back to something customers actually said. No data, no personas — it won't invent an audience.

## What you need

- **Customer reviews** — an export (.txt/.csv) or a batch pasted into chat. Judge.me, Okendo, Yotpo, Shopify reviews all work.
- Recommended: the **`eca-brand-intelligence`** skill, to sharpen language and know the product lineup.

## How to use it

- "Build personas from our reviews" (point Claude at the file)
- "Analyse these reviews and tell me our customer types" + paste reviews
- "What are our buyer personas and what objections do they raise?"
- "Pull the emotional triggers and segments from our review export"

Then feed the result straight into `eca-ad-copywriting` or `eca-email-marketing-campaign`.

## Files

```
eca-persona-builder/
├── SKILL.md                          # the workflow (brand-agnostic)
├── config.md                         # YOUR settings — the only file to edit when forking
├── references/
│   └── analysis-framework.md         # the nine-part voice-of-customer analysis
├── templates/
│   ├── persona-template.md           # structure for one persona
│   └── persona-report-template.md    # structure for the full deliverable
└── README.md
```

## Forking for a different brand

The logic is brand-agnostic — the only brand-specific content lives in `config.md`. To reuse:

1. Copy the whole `eca-persona-builder/` folder.
2. Open `config.md` and edit:
   - **Brand name** and optional brand-context source.
   - **Data source** — where that brand's reviews/feedback live.
   - **How many personas** — default 3–5.
   - **Output preferences** — format, save location, filename.
3. Feed in that brand's reviews. Don't touch `SKILL.md`, `references/` or `templates/`.

## Sharing with your team

This skill ships inside the **eca-ecommerce-agent** plugin in the EcomAcademy marketplace — installing that one plugin keeps members current with every skill in the bundle. To share standalone, package the folder as a `.skill` file (a zipped skill directory).
