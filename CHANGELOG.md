# Changelog

All notable changes to the ECA skills bundle. Newest first.

## v1.17.0 - 2026-10-27

- The ECA Reel Editor now ships inside the Marketing Coworker (`eca-ecommerce-agent`) as the `eca-reel-editor` skill; the standalone `eca-reel-editor` plugin released earlier today is withdrawn from the marketplace (uninstall it if you added it).
- The Marketing Coworker declares the EcomOS MCP server: in Claude Code type `/mcp`, choose `ecomos`, Authenticate, allow it on the EcomOS page. No terminal, no URL to paste. (claude.ai / desktop chat: Settings → Connectors → Add custom connector → `https://ecomos.ecomacademy.co/mcp`.)

## v1.16.0 - 2026-10-27

- New plugin **ECA Reel Editor** (`eca-reel-editor` v0.1.0): drop a raw talking-head clip into Claude Code and get back a finished vertical reel or Meta video ad in your brand, with product, review and offer cards from your Shopify store via EcomOS. Built on Nicola Pocock's claude-reel-editor (MIT); Python scripts, Windows untested.
- Brand intelligence: the brand file lives in your working folder (`./brand/brand-data.md`; lookup order in `references/brand-file-location.md`) so plugin updates never touch it, and it syncs to EcomOS (`references/ecomos-sync.md`, "Sync my brand to EcomOS") so the Marketing Apps and AI coach there use the same brand.
- All skills that read `brand-data.md` now use the shared lookup order (operations agent v1.48.2, Black Friday blueprint v1.10.5).

## v1.15.0 - 2026-10-19

- Add hero product finder and survey skills, morning brief and customer service, and fix skill labels that were too long to load

## v1.14.0 - 2026-10-13

- Add survey skills, morning brief and customer service, and fix skill labels that were too long to load

## v1.47.0 - 2026-10-12

- Update to CS Skill

## v1.36.0 - 2026-10-09

- Added in daily bried

## v1.10.0 - 2026-09-15

- Added in BFCM Ads Builder

## v1.9.1 - 2026-09-09

- Added in Email Skill

## v1.13.0 - 2026-09-08

- Removed PDP and Promotions, depreciated skills

## v1.13.0 - 2026-09-08

- Update  to description length

## v1.7.0 - 2026-09-03

- Update to BFCM Offer Skill

## v1.12.15 - 2026-09-03

- Update to HTML overview

## v1.12.14 - 2026-09-02

- Rename to ECA Black Friday Blueprint

## v1.12.13 - 2026-09-02

- Added in Black Friday Blueprint

## v1.12.12 - 2026-08-06

- Advertorial editorial masthead, benefit image controls, colour-scheme adapter

## v1.12.11 - 2026-08-05

- Update to section layouts and usability

## v1.12.10 - 2026-08-05

- Visual Proof Update, Color Scheme for Sections

## v1.12.9 - 2026-08-05

- Updated Social Proof Section and Deep link after builds

## v1.12.8 - 2026-08-05

- Version control added to sections and blocks in landing pages.

## v1.12.7 - 2026-08-05

- Update to sections

## v1.12.6 - 2026-08-05

- Tweaks to Listicle

## v1.12.5 - 2026-08-05

- Updated the way placeholders are rendered

## v1.12.4 - 2026-08-05

- Added in update to listicle, placeholders and page wide configs

## v1.12.3 - 2026-08-05

- Update to landing pages skill

## v1.12.2 - 2026-08-04

- Update to Landing page builder to be more interactive, led by user not AI

## v1.12.1 - 2026-08-04

- Added Landing Page Builder Skill

## v1.12.0 - 2026-07-30

- Update to Meta Ads Analysis

## v1.11.0 - 2026-07-27

- Added in ECA Meta Ads Skill

## v1.10.0 - 2026-07-14

- Blog Writer now starts with DataForSEO — real search-volume, difficulty and question-keyword research to pick topics, plus AI-citation data so posts are written to get cited in ChatGPT/Perplexity/AI Overviews.

## v1.9.0 - 2026-07-07

- Audit shows the score + scorecard table in the chat summary, always routes content creation/rewrites through the blog skill, and adds an agentic-commerce readiness check (agents.md, UCP/MCP, AI-agent feeds).

## v1.8.1 - 2026-07-06

- Updated AEO & SEO To work towards 100/100

## v1.8.0 - 2026-07-06

- Updated ECA SEO Skill with more robust audit and implementation

## v1.7.0 - 2026-07-06

- Update to AEO skill to push to code and suggest content updates and blog skill.

## v1.6.0 - 2026-07-06

- Added in SEO / AIO Update

## v1.5.1 - 2026-06-23

- Added in Operations Coworker

## v1.5.0 - 2026-06-22

- Updated UGC inputs for better scripts, extended to 60secs if needed.

## v1.4.0 - 2026-06-19

- New Skill Added: UGC Script Writer

