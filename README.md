# Ecommerce Academy — Claude Code skills marketplace

Claude Code plugins for Shopify merchants. Plugins here run inside [Claude Code](https://claude.com/claude-code) and give you ready-made workflows for setting up, optimising, and shipping Shopify themes.

Built by **Ecommerce Academy**.

## Available plugins

| Plugin | What it does |
|---|---|
| [`eca-pdp`](./plugins/eca-pdp) | **ECA Product Detail Page.** Duplicates your live Shopify theme into a development copy, then installs a research-backed high-converting product page template into it. Built for Shopify Horizon. |

## How to install (one-time setup per member)

In any Claude Code session, run:

```text
/plugin marketplace add ecomacademyau/ecomacademy-skills
```

Claude Code fetches the marketplace catalog from this repo. You only do this once per machine.

## How to install a plugin

```text
/plugin install eca-pdp@ecomacademy-skills
```

Then use it by either:
- Typing the slash command: `/eca-pdp:install`
- Or just describing the task: *"Install ECA PDP on my store mystore.myshopify.com"*

## How to update

Plugins are versioned by git commit. To pull the latest version of a plugin you've installed:

```text
/plugin marketplace update ecomacademy-skills
```

Then re-run `/plugin install eca-pdp@ecomacademy-skills` if it doesn't auto-update.

## Troubleshooting

**`/plugin marketplace add` says "marketplace not found"**
→ Make sure you have the latest Claude Code. Run `claude --version` — if it's older than v2.0, update via `npm install -g @anthropic-ai/claude-code@latest`.

**The plugin's skill doesn't trigger**
→ Run `/plugin enable eca-pdp@ecomacademy-skills` to make sure it's active, then `/reload-plugins`.

**You see "/eca-pdp:install" listed but typing it doesn't do anything**
→ The skill is loaded but Claude needs context. Add the store domain to your prompt: *"Install ECA PDP on `mystore.myshopify.com`"*.

---

## For Ecommerce Academy admins — updating plugins

This repo is the source of truth. Every commit to `main` is a new version (because we omit the `version` field in plugin manifests, the git commit SHA is used).

To ship an update:

```bash
git add -A
git commit -m "Update ECA PDP sections"
git push origin main
```

Members' next `/plugin marketplace update` will pick up the change.

To pin a release (recommended for major changes):

1. Add `"version": "1.1.0"` to `plugins/eca-pdp/.claude-plugin/plugin.json`.
2. Commit + push.
3. Optionally tag the release: `git tag v1.1.0 && git push --tags`.

## License

MIT — see [LICENSE](./LICENSE).

---

Built with care by [Ecommerce Academy](https://github.com/ecomacademyau).
