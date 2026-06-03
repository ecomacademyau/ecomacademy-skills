# Adding skills to the Ecommerce Academy marketplace

This repo is a Claude Code **plugin marketplace**. Members add it once, install the
`eca-skills` plugin, and from then on **every new skill you add to that plugin reaches
them automatically** on update. This doc is the playbook for keeping that flowing.

## The one rule that makes auto-distribution work

> **New skills go INSIDE the `eca-skills` plugin. Never ship a skill as its own new plugin.**

Claude Code only auto-updates plugins a member has **already installed**. A brand-new
*plugin* will not appear for existing members unless each of them installs it by hand.
But a new *skill folder added inside an already-installed plugin* flows to everyone the
next time they update. So the bundle (`plugins/eca-skills/skills/`) is the home for
everything you add.

## Naming rule

**Every skill name starts with `eca-`.** This is both the folder name and the `name:`
field in the skill's `SKILL.md` frontmatter. Examples:

- `eca-brand-intelligence`
- `eca-email-marketing-campaign`
- `eca-competitor-analysis`
- `eca-promotional-campaign`

Use kebab-case. Keep the folder name and the frontmatter `name:` identical.

## How to add a new skill (the whole workflow)

1. **Create the skill folder** at `plugins/eca-skills/skills/eca-<your-skill>/` with a
   `SKILL.md` inside. Set the frontmatter `name: eca-<your-skill>`.
2. **Keep brand specifics in a swappable config file** (e.g. `config.md`,
   `brand-data.md`, `klaviyo-config.md`) and ship a **placeholder/template**, never a
   member's real data. The workflow logic in `SKILL.md` stays brand-agnostic.
3. **No version bump needed.** `eca-skills` omits the `version` field in its
   `plugin.json`, so Claude Code uses the git commit as the version — **every push is
   automatically a new release.** Just commit and push.
4. **Commit & push** to the marketplace repo's main branch.
5. Members receive it on their next plugin update (see below).

No edits to `marketplace.json` or `plugin.json` are required to add a skill, because
`eca-skills` declares `"skills": "./skills"` and auto-discovers every `SKILL.md` under
that folder.

## How members get updates

Because this is a third-party (non-Anthropic) marketplace, **auto-update is OFF by
default** for members. Give them this one-time setup:

- **Easiest:** in the `/plugin` menu, turn **auto-update ON** for the `ecomacademy-skills`
  marketplace. Claude Code then refreshes at startup and prompts `/reload-plugins`.
- **Manual alternative:** run `/plugin update eca-skills` (or `/plugin update` for all).

First-time install for a new member:

```
/plugin marketplace add ecomacademyau/ecomacademy-skills
/plugin install eca-skills
```

## The other plugins in this marketplace

- **`eca-promotion`** — the promotional-campaign builder (scripts + fonts). Its one skill
  is `eca-promotional-campaign`. Like `eca-skills`, it omits an explicit `version`, so
  every commit is a release.
- **`eca-pdp`** — a Shopify CLI product-page tool (not a skill bundle).

Adding a **whole new plugin** (rare — only for something that isn't a skill) means adding
a folder under `plugins/` and a new entry in `.claude-plugin/marketplace.json`. Remember
existing members must install a brand-new plugin manually.

## Repo layout

```
ecomacademy-skills/
├── .claude-plugin/
│   └── marketplace.json          # lists eca-pdp, eca-promotion, eca-skills
├── plugins/
│   ├── eca-skills/               # THE BUNDLE — add new skills here
│   │   ├── .claude-plugin/plugin.json   # "skills": "./skills", no version
│   │   └── skills/
│   │       ├── eca-brand-intelligence/
│   │       ├── eca-email-marketing-campaign/
│   │       └── eca-competitor-analysis/
│   ├── eca-promotion/            # promo-campaign plugin (skill: eca-promotional-campaign)
│   └── eca-pdp/                  # Shopify product-page plugin
└── CONTRIBUTING.md
```
