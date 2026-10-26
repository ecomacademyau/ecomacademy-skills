---
name: eca-reel-editor
description: "Edit a raw talking-head video (phone clip, selfie video, webcam recording) into a finished vertical reel, TikTok, Short or Meta video ad in the member's own brand, with ecommerce cards (product, reviews, offer code) from their Shopify store. Use when someone drops a video and says \"edit this\", \"make this a reel\", \"cut this down\", \"add captions and graphics\", \"turn this into an ad\", \"add my product to this\", or asks to set up the reel editor. Brand comes from brand-data.md (brand-intelligence) — never from an interview — and products, reviews and reel logging come from EcomOS when it is connected."
---

# ECA Reel Editor

Turns a raw talking-head clip into a finished, on-brand vertical reel or ad for a Shopify brand. Every look-and-feel choice (colours, fonts, caption style, sounds, CTA) comes from the member's **brand file** — `brand-data.md`, maintained by the brand-intelligence skill — never from defaults in this skill and never from a brand interview. Product shots, prices and review numbers come from the member's store through **EcomOS**. You do the editing; they only make the calls that are theirs: which lines go, which graphics stay, when it is done.

Footage never leaves their computer. Transcription is local (Whisper) unless they set an ElevenLabs key; rendering is local (HyperFrames + ffmpeg); the review page carries a 540p proxy on their own claude.ai account.

Built on Nicola Pocock's `claude-reel-editor` (MIT) — see `README.md` in this folder for attribution.

## 0. Before anything else

**Where you are.** Work in the member's brand folder (the one with `./brand/brand-data.md`). The reel workspace is `./reels/` there (or `$REELS_HOME`). If there is no brand file in the lookup order (`$ECA_BRAND_FILE`, `./brand/brand-data.md`, `./brand-data.md`, `./skills/*/brand-data.md`), **stop**: say the brand-intelligence skill builds it in ten minutes, and offer to run it. Do not edit a clip without a brand file, even if they say "just use whatever".

**Tools (once per machine).** `python3 scripts/doctor.py` — ffmpeg, Node, Python, the HyperFrames skills, the template engine, disk, and whether EcomOS is connected. Ends READY / READY WITH LIMITS / MISSING. Fix ❌ items before editing (install steps are in the README). An EcomOS warning is not blocking: without it you ask for a product image and price instead of pulling them.

**Brand → brand.json.** `python3 scripts/brand_from_eca.py`. It reads the brand file and writes `reels/brand.json` (what the scripts use) and `reels/reel-brief.md` (what you read before proposing cuts: voice, top angles, proof, hero product, objections, claims to avoid, CTA). It re-runs only when the brand file changed.
- Exit 3 = **visual gaps**: it prints `{"gaps": [...], "suggested": {...}}`. Ask only those questions (≤ 6, one at a time, options + the suggested default) per `references/reel-kit.md`, save `kit.json`, rerun with `--kit kit.json`. That writes a ```reel-kit block into §4 of `brand-data.md`. Then, if the `ecomos` tools exist, run the brand sync (`eca-brand-intelligence/references/ecomos-sync.md`) so EcomOS carries it. Once. Never again unless they change their mind.
- Fonts: a file in `./brand/fonts/` wins; otherwise the named Google font is downloaded; otherwise a clean system font with a note. Roca, Poppins, Inter, Montserrat — whatever §4 names.

**EcomOS.** When the EcomOS MCP tools are in the session (server `ecomos`, or the claude.ai connector `claude_ai_EcomOS`): `ping` once at the start of a session (say the business name back), `get_products` when a line mentions a product, `log_reel` after delivery. When they are not: say once "type `/mcp`, choose ecomos and Authenticate (or in claude.ai: Settings → Connectors → Add custom connector → `https://ecomos.ecomacademy.co/mcp`) so I can pull your products and log reels" and carry on with what they give you.

Read `reels/reel-brief.md` in full before step 3. It is short on purpose.

## 1–8. The edit, in order

Each reel gets its own folder: `reels/<yyyy-mm-dd>-<short-name>/`. Copy the raw clip in as `raw.<ext>` (never edit the original).

1. **Transcribe** — `python3 scripts/transcribe.py raw.<ext> transcript.json` (ElevenLabs Scribe when `ELEVENLABS_API_KEY` is set in the environment, `~/.config/reels/.env` or `reels/.env`; else local Whisper — timing drifts ~0.3 s, the scripts compensate; never cut on raw word times yourself).
2. **Clean the voice** — `python3 scripts/clean_audio.py raw.<ext> voice.wav` (`--no-denoise` only for a studio-quiet room). −14 LUFS, what Instagram and TikTok expect.
3. **Review — their call.** Look at the first and last 4 s (a frame every 0.5 s): cut camera setup, the reach for the phone, the "okay so". Then propose: lines to cut, fillers, the CTA at the end, under 60 s, **and the ecommerce cards** (below). Wait for their yes before cutting.
   - **Main path — the Reel Review page** (`references/review.md`): if the `Artifact` and `ArtifactData` tools exist (load them via tool search if deferred), run `python3 scripts/tighten.py <reel> --detect`, write `proposal.json`, export, build the assets, publish, send the link. They tap words to cut, keep/change/drop each graphic, play the rough cut, then say "build preview".
   - **Fallback — review in chat** (`references/rough-cut.md`): numbered lines with proposed cuts, then the card list.
4. **Tighten, cut, speed** — `edl.json` from the approved lines (or `review_sync.py import`), `python3 scripts/tighten.py <reel>`, `python3 scripts/cut.py <reel>` (`REEL_PREVIEW=1` for a 1080p draft). Pacing and speed come from `brand.json`. Listen-check the joins: re-transcribe `master.mp4`.
5. **Graphics + captions — fill the template, don't design.** `python3 scripts/transcribe.py master.mp4 master_transcript.json`, `python3 scripts/auto_edit.py <reel>` → `edit.json`, then one pass by you: `"accent": true` on the one key word per sentence, and cards at the density `brand.json` `"graphics"` asks for (minimal ≈ every 8–12 s, balanced 4–6 s, busy 2–4 s). Card types and fields are in the header of `scripts/build_reel.py`; HyperFrames motions in `references/motions.md`. Every card shows what that exact line says — nothing decorative, nothing invented.
   - **Hook title**: ≤ ~10 characters a line, 2–3 lines, the only text with an outline.
   - **Ecommerce cards (this fork's additions):**
     - `product {name, price, url|src, compare_at?}` when they name or hold up a product. With EcomOS: `get_products` → pick the match by title/handle → `url` = its `imageUrl`, `price`/`compareAtPrice` as returned. Without: ask for one product photo + the price. Shopify CDN URLs are downloaded into `<reel>/assets/` by the build.
     - `review {rating, count, quote?, source?}` when they talk about customers, trust or results. Numbers from the brief's Proof section (brand file §8) — the **lower** figure when a range is given; a quote verbatim with its source. No proof in the brand file → no review card. Never round up, never estimate.
     - `offer {code, text, url?, expires?}` as the end card when there is a code or a CTA to act on. Text = the CTA from `brand.json` unless the clip says a different one; `url` defaults to the brand's store URL. Codes come from the member, never guessed.
   - Screenshots of a site they mention: `python3 scripts/screenshot.py <url> shots/<name>.png` (exit 2 = blocked; ask for one).
   - Preview: `REEL_PREVIEW=1 python3 scripts/render.py <reel>` (1080p, 2 low-priority workers). Final: `python3 scripts/render.py <reel> --final` (brand resolution; `--capcut` only if `brand.json` says so).
   Do **not** hand-write HyperFrames compositions or use other HyperFrames workflows here: slower, and they ignore the brand template. One missing effect they explicitly ask for → say it is slower, then use the `hyperframes` skill for that effect only.
6. **QA** — `python3 scripts/qa.py <reel>` (size, length, loudness, missing words when `expected.txt` exists). Then grab a frame at **every card** and look: inside the frame, readable, on brand, the face never covered, the product image not cropped to nothing, the price exactly what the store says. Fix `edit.json`, re-render, until it passes. Never pass QA by lowering the bar.
7. **Deliver** — `python3 scripts/deliver.py <reel>/final.mp4 "<clear name>"` → upload-ready MP4 in `reels/delivered/` (or `brand.json` `deliver_dir`). Open the folder for them if you can (`common.open_path`).
8. **Log it** — with EcomOS connected: `log_reel {title, durationSec, styleCodes: [], recipe: "meta-ad" | "organic" | "launch", product?, notes?}` and, if cheap, a ≤ 100 KB JPEG thumbnail (`thumbnailJpegBase64`). One call per delivered reel. Say "logged to EcomOS" in the wrap-up. Without EcomOS, skip silently.

Tell them what changed and what to check by ear: the cuts, names, brand words spelled right, the price.

## Their brand rules win

If the brand file and your taste disagree, the brand file wins. If they correct something during an edit ("never outline captions", "lowercase always"), update the ```reel-kit block (`references/reel-kit.md`) or §4 of `brand-data.md`, rerun `brand_from_eca.py --force`, and offer the EcomOS sync — not a side note that the next edit will not see.

## House rules (do not negotiate these)

- **Never cover the face.** Cards sit above the head or below the chin; move `y` rather than shrink the person.
- **Safe zones.** Nothing in the bottom ~420 px (Instagram UI) or the top ~200 px except the hook title; captions at `brand.json` `captions.y`.
- **Real proof only.** Ratings, review counts, prices, codes and quotes come from the store, EcomOS or the brand file. No "10,000+ happy customers" unless the file says it.
- **Claims to avoid** in the brief are never on a card or in a caption, even if the member says them on camera (flag it instead).
- **Nothing renders without their yes.** A preview is cheap; a wrong final is not.

## Windows

The scripts are Python and path-safe; `doctor.py` prints the platform. ffmpeg must be on PATH (or `npm i -g ffmpeg-static ffprobe-static`). Rendering uses libx264 instead of Apple's hardware encoder, so it is slower. Windows is **untested** in this release — say so if they ask, and ask them to report anything odd.

## Common mistakes

| Mistake | Instead |
|---|---|
| Starting a brand interview | Run brand-intelligence; this skill only asks the Reel-kit gaps, once |
| Typing a price or review count from memory | `get_products` / the brief; ask if neither has it |
| A product card for a product the clip never mentions | Each card shows what that exact line says |
| Cutting on Whisper word times blindly | Let `tighten.py`/`core.js` snap into the quiet gaps; listen-check joins |
| Graphics that decorate instead of illustrate | One card per thing said, at the brand's density |
| Fixing QA by lowering the bar | Fix `edit.json`, re-render |
| Logging the reel before QA passes | `log_reel` only after delivery |
