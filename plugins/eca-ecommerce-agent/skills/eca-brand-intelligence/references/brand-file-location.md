# Where the brand lives

**1. EcomOS, when it is connected.** The brand is saved in the member's EcomOS as sections (`voice`, `products`, `personas`…) that any AI app reads with the `ecomos` tools: `get_context` with `for:"<skill>"` for the sections a skill needs, `search_context` for one fact. How it is saved and kept current is in `ecomos-sync.md`. **EcomOS is the source of truth:** when it and a local file disagree, EcomOS stands, and a change to the brand is saved there first.

**2. The working copy, `brand-data.md`.** A copy of the same brand in the member's working folder, refreshed from EcomOS. It is the only copy when EcomOS is not connected, and scripts (the reel editor's, the completeness check) read it. Resolve it in this order and use the **first** match:

1. `$ECA_BRAND_FILE` — an explicit path in the environment (teams and agencies managing several brands set this per project).
2. `./brand/brand-data.md` — **the standard location.** Mode A (Build) always writes here. It sits in the member's working folder, so plugin updates never touch it and every skill in every plugin finds it.
3. `./brand-data.md` — a brand file dropped straight into the working folder.
4. `./skills/*/brand-data.md` — the older "skills folder per brand" layout (e.g. `./skills/brand-intelligence/brand-data.md`).
5. The plugin's own skill folder (`eca-brand-intelligence/brand-data.md`) — **legacy and read-only.** If this is the only copy, say so once and offer to copy it to `./brand/brand-data.md` (then use the copy). Never write a member's brand into the plugin folder: the next plugin release replaces that folder and would wipe it.

"Working folder" means the folder Claude Code was opened in (the project root). If none of the five exist and EcomOS does not hold the brand either, the brand has not been built yet → Mode A.

Companion files live next to the brand file: `market-research-report.md`, `brand-sync.json` (the structured brand sent to EcomOS), `.ecomos-sync.json` (which EcomOS version each section matches; written by the script), `./brand/fonts/` (the brand's font files for the reel editor), `./brand/assets/` (logos, stickers, product shots).

A one-liner for other skills: *"Get the brand from EcomOS when the `ecomos` tools are connected (`get_context` with `for:\"<this skill>\"`); otherwise read `brand-data.md` (resolve it per `eca-brand-intelligence/references/brand-file-location.md`: `$ECA_BRAND_FILE`, `./brand/brand-data.md`, `./brand-data.md`, `./skills/*/brand-data.md`, then the plugin folder as a read-only fallback)."*

Scripts can call `python3 <eca-brand-intelligence>/scripts/brand_sections.py --path-only` to print the resolved path, or use the same order themselves.
