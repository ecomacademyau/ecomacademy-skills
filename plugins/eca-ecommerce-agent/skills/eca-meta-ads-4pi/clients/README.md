# Client Configs

One file per brand: `clients/<brand-slug>.md`. The slug should loosely match the Meta ad account name so the skill can auto-match (e.g. `acme.md` for "Acme Skincare").

## Onboarding a new client (first run)

If no config exists for the brand being analysed:

1. Ask the member (keep it to one round of questions): brand name, website URL, target mode and number(s) (per order = `target_cpa`, per new customer = `target_ncpa`, or both; plus `target_cpl` when the account runs lead gen campaigns), gross margin % (optional — upgrades the profit proxy), primary + accent brand colors (offer to derive them from the website via Firecrawl if unknown), logo URL (optional).
2. Currency comes from the ad account — don't ask.
3. Proceed with the analysis using the answers.
4. At the end, output the completed config block in chat and tell the member to save it into the skill's `clients/` folder (or re-package the skill with it) so future runs skip onboarding.

## Config format

```markdown
# <Brand Name>

- account_hint: <part of the Meta ad account name, e.g. "Acme">
- website: https://...
- currency: AUD
- target_mode: first_order    # first_order | ltv | both (see Knowledge Base, "Audience Segments, NCPA & Target Modes")
- target_cpa: 40              # per order; optional in ltv mode
- target_ncpa: 90             # per new customer; required in ltv / both mode
- target_cpl: 2.50             # per lead; only when the account runs lead gen campaigns
- gross_margin_pct: 65        # optional; enables est. gross profit/order
- aov_baseline: 85            # optional; sanity check
- brand_primary: "#B4462B"
- brand_accent: "#1F3A5F"
- logo_url: https://...       # optional
- fonts: "Lora / Inter"       # optional override
- industry_vertical: apparel_and_accessories   # Triple Whale benchmark slug — list at benchmark.triplewhalelabs.com/benchmarks/
- personas_source: <path or note, e.g. "eca-brand-intelligence brand-data.md" or "none">
- shopify_domain: example.com.au   # optional; the Shopify cross-check only runs when the connected store matches this
- notes: <anything relevant: offer structure, seasonality, who owns creative, etc.>
```
