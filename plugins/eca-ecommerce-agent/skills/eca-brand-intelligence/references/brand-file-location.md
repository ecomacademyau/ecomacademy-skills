# Where the brand file lives

Every ECA skill reads the same `brand-data.md`. Resolve it in this order and use the **first** match:

1. `$ECA_BRAND_FILE` — an explicit path in the environment (teams and agencies managing several brands set this per project).
2. `./brand/brand-data.md` — **the standard location.** Mode A (Build) always writes here. It sits in the member's working folder, so plugin updates never touch it and every skill in every plugin finds it.
3. `./brand-data.md` — a brand file dropped straight into the working folder.
4. `./skills/*/brand-data.md` — the older "skills folder per brand" layout (e.g. `./skills/brand-intelligence/brand-data.md`).
5. The plugin's own skill folder (`eca-brand-intelligence/brand-data.md`) — **legacy and read-only.** If this is the only copy, say so once and offer to copy it to `./brand/brand-data.md` (then use the copy). Never write a member's brand into the plugin folder: the next plugin release replaces that folder and would wipe it.

"Working folder" means the folder Claude Code was opened in (the project root). If none of the five exist, the brand has not been built yet → Mode A.

Companion files live next to the brand file: `market-research-report.md`, `./brand/fonts/` (the brand's font files for the reel editor), `./brand/assets/` (logos, stickers, product shots).

A one-liner for other skills: *"Read `brand-data.md` (resolve it per `eca-brand-intelligence/references/brand-file-location.md`: `$ECA_BRAND_FILE`, `./brand/brand-data.md`, `./brand-data.md`, `./skills/*/brand-data.md`, then the plugin folder as a read-only fallback)."*

Scripts can call `python3 <eca-brand-intelligence>/scripts/brand_sections.py --path-only` to print the resolved path, or use the same order themselves.
