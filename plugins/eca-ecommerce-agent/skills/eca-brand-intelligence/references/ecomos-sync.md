# Sync the brand to EcomOS

`brand-data.md` is the single source of truth for the brand. EcomOS (the member's dashboard) keeps a **read-only mirror** of it so every Marketing App there — Offer Builder, Prompt Generator, Hook Library, the AI coach chat, the Ad Data Analyser, the Meta 4PI and Google Ads Spend analysts — writes in the brand's voice. The flow is one way: file → EcomOS. Nothing in EcomOS edits the file.

## One file, one folder

The sync pushes **the brand file in the folder Claude Code is open in** (lookup order in `brand-file-location.md`). A member who has copies in several folders (Downloads, a Drive folder, an old skills folder) will sync whichever one they happen to be in — and the copies drift. When you find more than one `brand-data.md` for the same brand, say so, show their "Last updated" dates and TBD counts, and offer to make the richest one `./brand/brand-data.md` in their working folder and retire the rest. Do not merge files silently.

## When to sync

- **Right after Gate 2** writes (or rewrites) `brand-data.md`.
- **At the start of Mode B** when the file has changed since the last sync: call `get_brand` and compare its `sourceHash` with the file's sha256 (from `scripts/brand_sections.py`). Different → sync. Same → say nothing and carry on.
- When the member says **"Sync my brand to EcomOS"** (or "push my brand", "update EcomOS with my brand").
- After another skill changes the file (the reel editor adds a `reel-kit` block to §4, the survey skills add to §2/§9/§12).

## Is EcomOS connected?

The tools `ping`, `sync_brand`, `get_brand`, `get_products`, `log_reel` come from an MCP server named **`ecomos`**. If they are not in this session, the member has not connected Claude to EcomOS. Say it **once**, plainly, and move on with the task:

> Your brand isn't synced to EcomOS yet. In Claude Code, type `/mcp`, choose **ecomos**, pick **Authenticate**, and allow it on the EcomOS page that opens (sign in with the Google account you use for EcomOS). In claude.ai or the desktop app instead: Settings → Connectors → Add custom connector → name it EcomOS, URL `https://ecomos.ecomacademy.co/mcp` → Connect. Then tell me "Connect to EcomOS and sync my brand".

The tools may appear under the server name `ecomos` or as a claude.ai connector (`claude_ai_EcomOS`); either is fine. Never ask for a key in chat. Never try to call EcomOS over HTTP yourself.

## How to sync (4 steps, ~1–3 minutes)

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

3. **Make it complete before it goes across — the sync is the brand file's health check**
   `python3 <this skill>/scripts/brand_sections.py --gaps ./brand/brand-sync.json` prints two lists and ends with a **VERDICT**:
   - **COMPLETE** → go to step 4.
   - **PATCH** (a few gaps, file still fresh) → fill them now as described below, then step 4.
   - **REBUILD** (more than 4 app fields missing, more than 3 app-read sections still TBD, or the file is older than 120 days) → **do not patch it at sync time.** Tell the member in two lines that the brand file is too thin or too old to sync well, and that the proper fix is the brand-intelligence build: run **Mode A as a refresh** (keep everything the member already approved, re-research the gaps and anything stale, Gate 1, Gate 2), write the file, *then* sync. This is the same skill, so just proceed into Mode A unless they say "sync what's there anyway" — in which case sync, and list what is missing afterwards.

   For a PATCH verdict, the two lists are:
   - **MISSING** — fields the Marketing Apps and the reel editor actually read (accent/ink/light colours, heading font, logo, pillar hooks, product prices and the hero, CTA, guarantee, rating + review count, quotes, objections, personas, claims to avoid). **Do not sync past a MISSING list without trying to fill it.** For each item, in this order:
     1. *Look it up yourself where it is verifiable:* colours, fonts and the logo from the live storefront (fetch the homepage; theme CSS custom properties, the header logo `<img>`, Shopify theme settings if the Shopify MCP is connected), products and prices from Shopify, rating and count from the review widget or app. Present what you found as a proposal with its source — never as fact until the member confirms.
     2. *Ask the member for the rest* in one round (AskUserQuestion where available): hex codes with your proposals as defaults, the heading font, the usual CTA, the guarantee. "Skip for now" is a valid answer and is written as still TBD.
     3. *Write every confirmed answer into `brand-data.md`* in its own section (replace the TBD), add the source and today's date to §18, tick it off in §19, update `brand-sync.json`, and rerun `--gaps`.
   - **UNCONFIRMED** — sections that still say TBD / placeholder / "to be confirmed". Items in sections the apps read (§1–§9, §12) get the same treatment as MISSING. Items in §13/§14/§17 (operations, calendar, channels) are mentioned in one line and never block the sync.
   A brand file that comes back COMPLETE here is a brand file every skill can trust; that is the point of doing this on every sync.

4. **Send**
   `python3 <this skill>/scripts/brand_sections.py --payload ./brand/brand-sync.json` prints the complete `sync_brand` arguments `{brand, sourcePath, sourceHash}` (exit 2 = fix the JSON; "note:" lines = something was clipped). Call the **`sync_brand`** tool with exactly that object — it is a few KB. The raw markdown sections are **optional and off by default** (`--with-sections` adds them; nothing in EcomOS displays them yet), so never summarise or skip "because the file is long". On `{ok: true}` say one line: *"Synced to EcomOS — your Marketing Apps now use this brand."*, then a short "what went across" list and, if anything was skipped, a one-line "still to confirm" list. `ping` is not needed.

If `sync_brand` returns an error, show it in one line and keep going with the member's actual task; a failed sync never blocks copywriting.

## What EcomOS does with it

`brandProfiles/{owner}` gets `brand` (the JSON), optionally `sections` (raw markdown by number), and six derived summary fields the older apps read. The Brand Profile card becomes read-only with a "Synced from Claude" badge; a manual edit there is refused with "Managed by Claude" and points back to this skill.
