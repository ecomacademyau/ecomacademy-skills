# Ecommerce Academy — Skills

Claude Code plugins for Shopify merchants by Ecommerce Academy. Works in **Cowork** (the Claude desktop app) and **Claude Code**.

> For paid Ecommerce Academy members only. Please don't share outside the Academy.

## Install

```
/plugin marketplace add ecomacademyau/ecomacademy-skills
/plugin install eca-pdp@ecomacademy-skills
/plugin install eca-promotion@ecomacademy-skills
```

Or in Cowork: **Customize → Plugins → Add marketplace**, paste `ecomacademyau/ecomacademy-skills`, then install the plugin you want.

> Note: `marketplace add` takes the GitHub `owner/repo`; `install` takes the marketplace name (`ecomacademy-skills`).

## Updating

**Maintainer:** edit the plugin, commit, and push to GitHub. These plugins don't pin a `version`, so any new commit is treated as an update — no version bump needed.

**Members — to get updates:**
- **Recommended (hands-off):** enable **auto-update** for the `ecomacademy-skills` marketplace once. Claude then refreshes it and applies updates at app startup automatically.
- **Manual (Cowork):** Plugins → open the **ecomacademy-skills** marketplace → **Update** (refreshes the catalog), then update the plugin.
- **Manual (Claude Code):** `/plugin marketplace update` then `/plugin update eca-promotion`.

There's no silent background check unless auto-update is enabled, so members who want it fully hands-off should switch that on.

## Plugins

### eca-pdp
Connects to a Shopify store via the Shopify CLI, duplicates the live theme into a development theme, and installs a research-backed high-converting product page template. Built for Shopify's Horizon theme architecture.

### eca-promotion
Plan and build a complete promotional sale campaign end-to-end — offer, email + SMS, paid ads, on-site changes, and a dated Go-Live timeline. On first use it runs a quick **Brand Setup** to configure it for your store, then exposes the `promotional-campaign` skill. Need help? Reach out to your coach or post in the campus.
