# Client Configs

One file per brand: `clients/<brand-slug>.md`. The slug should loosely match the Meta ad account name so the skill can auto-match (e.g. `acme.md` for "Acme Skincare").

## Onboarding a new client (first run)

If no config exists for the brand being analysed:

1. Ask the member (keep it to one round of questions): brand name, website URL, target CPA, gross margin % (optional — upgrades the profit proxy), primary + accent brand colors (offer to derive them from the website via Firecrawl if unknown), logo URL (optional).
2. Currency comes from the ad account — don't ask.
3. Proceed with the analysis using the answers.
4. At the end, output the completed config block in chat and tell the member to save it into the skill's `clients/` folder (or re-package the skill with it) so future runs skip onboarding.

## Config format

```markdown
# <Brand Name>

- account_hint: <part of the Meta ad account name, e.g. "Acme">
- website: https://...
- currency: AUD
- target_cpa: 40
- gross_margin_pct: 65        # optional; enables est. gross profit/order
- aov_baseline: 85            # optional; sanity check
- brand_primary: "#B4462B"
- brand_accent: "#1F3A5F"
- logo_url: https://...       # optional
- fonts: "Lora / Inter"       # optional override
- personas_source: <path or note, e.g. "eca-brand-intelligence brand-data.md" or "none">
- notes: <anything relevant: offer structure, seasonality, who owns creative, etc.>
```
