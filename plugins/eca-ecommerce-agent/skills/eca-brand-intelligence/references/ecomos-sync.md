# Sync the brand to EcomOS

`brand-data.md` is the single source of truth for the brand. EcomOS (the member's dashboard) keeps a **read-only mirror** of it so every Marketing App there — Offer Builder, Prompt Generator, Hook Library, the AI coach chat, the Ad Data Analyser, the Meta 4PI and Google Ads Spend analysts — writes in the brand's voice. The flow is one way: file → EcomOS. Nothing in EcomOS edits the file.

## When to sync

- **Right after Gate 2** writes (or rewrites) `brand-data.md`.
- **At the start of Mode B** when the file has changed since the last sync: call `get_brand` and compare its `sourceHash` with the file's sha256 (from `scripts/brand_sections.py`). Different → sync. Same → say nothing and carry on.
- When the member says **"Sync my brand to EcomOS"** (or "push my brand", "update EcomOS with my brand").
- After another skill changes the file (the reel editor adds a `reel-kit` block to §4, the survey skills add to §2/§9/§12).

## Is EcomOS connected?

The tools `ping`, `sync_brand`, `get_brand`, `get_products`, `log_reel` come from an MCP server named **`ecomos`**. If they are not in this session, the member has not connected Claude to EcomOS. Say it **once**, plainly, and move on with the task:

> Your brand isn't synced to EcomOS yet. In Claude Code, type `/mcp`, choose **ecomos**, pick **Authenticate**, and allow it on the EcomOS page that opens (sign in with the Google account you use for EcomOS). In claude.ai or the desktop app instead: Settings → Connectors → Add custom connector → name it EcomOS, URL `https://ecomos.ecomacademy.co/mcp` → Connect. Then tell me "Connect to EcomOS and sync my brand".

The tools may appear under the server name `ecomos` or as a claude.ai connector (`claude_ai_EcomOS`); either is fine. Never ask for a key in chat. Never try to call EcomOS over HTTP yourself.

## How to sync (3 steps, ~1 minute)

1. **Split and fingerprint the file**
   `python3 <this skill>/scripts/brand_sections.py` → `{path, sha256, brandName, sections}`. (It finds the file per `brand-file-location.md`.)

2. **Build the structured brand** — write `brand-sync.json` next to the brand file (in `./brand/`), following `references/brand-sync-schema.json` exactly. It is a faithful *extraction* of the file, not new thinking:
   - `brandName`, `tagline` (§4 sign-off line or §1), `storeUrl` (header "Primary URL")
   - `essence.oneLiner` (§1 one-liner), `mission`, `positioning` (the ⭐ strategic direction's lead positioning if present, else §1 "what makes us different" in one line)
   - `voice.tone` (§3 "voice in three words" → a list), `do` / `dont` (§3 lean-on words → do; avoid words + tone rules → dont), `vocabulary` (owned words), `sampleLines` (the ✅ on-brand examples)
   - `visual.colors` {primary, accent, light, ink} from §4 hexes (primary = the brand's main colour, accent = highlight/CTA, light = background/cream, ink = text/near-black), `fonts` {heading, body}, `logoUrl`, `never` (§4 "never do visually"), `reelKit` ← the ```reel-kit block in §4 if present
   - `pillars` [{name, hook}] from §5 ranked value props (hook = the quoted hook line), `angles` (§5 secondary angles + "hooks that work")
   - `products` [{name, handle?, price, role, oneLiner}] from §6: role `hero` for the hero product, `bundle`, `accessory`, `gift`, else `sub`; price as a number (no "$")
   - `offer` {aov?, discountPolicy, cta, guarantee} from §7 (+ §8 guarantee)
   - `proof` {rating, reviewCount, quotes [{text, source}], press} from §8 (use the lower review count when a range is given)
   - `objections` [{objection, rebuttal}] from the §9 table
   - `personas` [{name, summary, triggers}] from §12
   - `claimsToAvoid` from §6 "Claims to avoid" + §15 "topics to avoid"
   - `market` {category, competitors (names only)} from §10/§11
   - `confidence` {sectionName: high|med|low} from §18, `verifiedAt` = the header's "Last updated"
   Leave out anything the file marks `TBD`. Keep arrays within the schema caps (the script clips them anyway). Numbers are numbers.

3. **Check and send**
   `python3 <this skill>/scripts/brand_sections.py --payload ./brand/brand-sync.json` prints the complete `sync_brand` arguments `{brand, sections, sourcePath, sourceHash}` (exit 2 = fix the JSON; "note:" lines = something was clipped). Call the **`sync_brand`** tool with that object. On `{ok: true}` say one line: *"Synced to EcomOS — your Marketing Apps now use this brand."* Then `ping` is not needed.

If `sync_brand` returns an error, show it in one line and keep going with the member's actual task; a failed sync never blocks copywriting.

## What EcomOS does with it

`brandProfiles/{owner}` gets `brand` (the JSON), `sections` (the raw markdown by number, so the Brand Profile card can show the original wording), and six derived summary fields the older apps read. The Brand Profile card becomes read-only with a "Synced from Claude" badge; a manual edit there is refused with "Managed by Claude" and points back to this skill.
