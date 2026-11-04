# Changelog

## 1.1.0 (5 Nov 2026)
- Ships in the ECA Marketing Coworker, replacing eca-ugc-scripts. Every ECA skill that handed off to eca-ugc-scripts now hands off here.
- References brought into line with SKILL.md: competitor research is a message read through the Meta Ads MCP only (no browser, no TikTok Creative Center, no Ad Library links in packs, briefs or checklists), and the store is read through Shopify rather than the browser.
- The competitor list comes from the member and their files; "find them for me" goes to eca-competitor-analysis, not a keyword search.
- The ECA Ad Concept Board and Hook Bank are pointed to for the member's own browsing, never cited or linked in a brief.
- build_brief.py adds "Prepared by Ecommerce Academy" to every brief page itself, and drops "Watch the examples first" when there are no examples.
- The brief example no longer carries example links.
- Version numbers aligned (SKILL heading, metadata and changelog disagreed).

## 1.0.0 (4 Nov 2026)
- First release. Merges eca-ugc-scripts (founder story, 3 reasons why, comment reply, the hook engine, brand-data integration) with Ad Script Studio (no-guessing rule, account read, angle scoring, compliance, scorecard, creative log).
- The strategist chooses the angle, hooks and format from the evidence; the member approves a one-page strategy.
- New formats: yapper, problem-solution demo, us vs them, testimonial, unboxing.
- Scripts: creative_read.py (replaces gap.py; 4PI thresholds, recent vs earlier fatigue split, landing-page gap detection), check_copy.py, build_brief.py.
- Quick mode for "just give me something to film".
- Removed: the logged-out Ad Library scraper. Competitor research uses the Meta Ads MCP, a teardown, or ads the member describes.
