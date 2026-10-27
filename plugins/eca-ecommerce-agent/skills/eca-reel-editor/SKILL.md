---
name: eca-reel-editor
description: "Edit a raw talking-head video (phone clip, selfie video, webcam recording) into a finished vertical reel, TikTok, Short or Meta video ad in the member's own brand, with ecommerce cards (product, reviews, offer code) from their Shopify store. Use when someone drops a video and says \"edit this\", \"make this a reel\", \"cut this down\", \"add captions and graphics\", \"turn this into an ad\", \"add my product to this\", or asks to set up the reel editor, and when they say \"I uploaded a clip in EcomOS\" or \"edit my latest reel\". Brand comes from brand-data.md (brand-intelligence) — never from an interview — and products, reviews and reel logging come from EcomOS when it is connected."
---

# ECA Reel Editor

Turns a raw talking-head clip into a finished, on-brand vertical reel or ad for a Shopify brand. Every look-and-feel choice (colours, fonts, caption style, sounds, CTA) comes from the member's **brand file** — `brand-data.md`, maintained by the brand-intelligence skill — never from defaults in this skill and never from a brand interview. Product shots, prices and review numbers come from the member's store through **EcomOS**. You do the editing; they only make the calls that are theirs: which lines go, which graphics stay, when it is done.

Two ways to run the same edit. **Hosted** (the default): the member uploads the clip on EcomOS → Marketing Apps → Reel Editor and EcomOS transcribes and renders; you edit through the `ecomos` tools and never install, download or run anything. **Local** (only on request, Claude Code on their own machine): transcription and rendering run on their computer with the scripts in this folder.

Built on Nicola Pocock's `claude-reel-editor` (MIT) — see `README.md` in this folder for attribution.

## 0. Before anything else

**Hosted or local — decide first, before touching any script.**
- If the EcomOS tools are in the session (server `ecomos`, or the claude.ai connector `claude_ai_EcomOS`) and they include `list_reels` → **hosted**. Full stop. Do not run `doctor.py`, do not transcribe, do not download a speech model, a font or a binary, and do not try to process a file dropped into chat. Go to **Hosted flow** below.
- If the EcomOS tools are there but `list_reels` is **not** among them → hosted editing is not switched on for this account yet. Say so in one line ("hosted reel editing isn't enabled on your EcomOS account yet — ask ECA to turn it on") and stop. Do **not** fall back to local in a sandbox.
- **Local only** when the member explicitly asks for it ("run it locally", "don't upload") **and** you are in Claude Code on their own machine where `python3 scripts/doctor.py` says READY. A sandbox (Cowork, claude.ai, a cloud session) is never local: if a download is blocked, that is the signal you are in the wrong mode, not a problem to work around. Never offer to fetch a model through the member's Chrome or ask them to allow-list a domain.

**Where you are (local path).** On the hosted path the brand comes from EcomOS: if `get_reel` says no brand is synced, run the brand-intelligence skill (it builds the brand file in ten minutes) and then "Sync my brand to EcomOS" before proposing a cut. Locally, work in the member's brand folder (the one with `./brand/brand-data.md`). The reel workspace is `./reels/` there (or `$REELS_HOME`). If there is no brand file in the lookup order (`$ECA_BRAND_FILE`, `./brand/brand-data.md`, `./brand-data.md`, `./skills/*/brand-data.md`), **stop**: say the brand-intelligence skill builds it in ten minutes, and offer to run it. Do not edit a clip without a brand file, even if they say "just use whatever".

**Tools (local path only, once per machine).** `python3 scripts/doctor.py` — ffmpeg, Node, Python, the HyperFrames skills, the template engine, disk, and whether EcomOS is connected. Ends READY / READY WITH LIMITS / MISSING. Fix ❌ items before editing (install steps are in the README). An EcomOS warning is not blocking: without it you ask for a product image and price instead of pulling them.

**Brand → brand.json (local path; on the hosted path `get_reel` returns the brand brief and kit, skip this).** `python3 scripts/brand_from_eca.py`. It reads the brand file and writes `reels/brand.json` (what the scripts use) and `reels/reel-brief.md` (what you read before proposing cuts: voice, top angles, proof, hero product, objections, claims to avoid, CTA). It re-runs only when the brand file changed.
- Exit 3 = **visual gaps**: it prints `{"gaps": [...], "suggested": {...}}`. Ask only those questions (≤ 6, one at a time, options + the suggested default) per `references/reel-kit.md`, save `kit.json`, rerun with `--kit kit.json`. That writes a ```reel-kit block into §4 of `brand-data.md`. Then, if the `ecomos` tools exist, run the brand sync (`eca-brand-intelligence/references/ecomos-sync.md`) so EcomOS carries it. Once. Never again unless they change their mind.
- Fonts: a file in `./brand/fonts/` wins; otherwise the named Google font is downloaded; otherwise a clean system font with a note. Roca, Poppins, Inter, Montserrat — whatever §4 names.

**EcomOS.** When the EcomOS MCP tools are in the session (server `ecomos`, or the claude.ai connector `claude_ai_EcomOS`): `ping` once at the start of a session (say the business name back), `get_products` when a line mentions a product, `log_reel` after delivery. When they are not: say once "type `/mcp`, choose ecomos and Authenticate (or in claude.ai: Settings → Connectors → Add custom connector → `https://ecomos.ecomacademy.co/mcp`) so I can pull your products and log reels" and carry on with what they give you.

Read `reels/reel-brief.md` in full before step 3. It is short on purpose.

## Hosted or local?

Decided in §0: hosted whenever `list_reels` is available; local only on explicit request in Claude Code on their own machine. The brand, the cards and the house rules are identical on both paths. On the hosted path, if the member drops a video into chat, don't process it: ask them to upload it on **EcomOS → Marketing Apps → Reel Editor** (one drag-and-drop), then run `list_reels`.

### Hosted flow

**EcomOS now cuts the reel itself.** When a member uploads on the Reel Editor page they choose a style (Founder Explainer, Founder Story, Problem → Solution, 3 Reasons, Us vs Them, Regret Review, Comment Reply) and EcomOS transcribes, cuts, places the cards and renders the preview with no one asking. Members change it with the change box on the page or by switching style. So on the hosted path you are the **second opinion, not the editor**: `list_reels` → `get_reel` shows the current `edit`, `editNotes`, `style`, and `changes`. Do not re-propose from scratch. Ask what they want different, then either (a) tell them to type it in the change box, or (b) call `set_edit` with the adjusted edit and `render_reel` — never both. A reel in `editing`/`rendering` is busy; wait. A reel in `ready` with no style is waiting for a style: they pick one on the page (or you propose and `set_edit` the old way).

1. `list_reels` → pick the reel (status `ready` means the transcript is in; `planning` means they chose a template but have not uploaded yet — tell them to film and upload, do not edit). `get_reel` → read the word-timed transcript, the brand brief, `howToEdit` and, when present, `template` (the member started from one of the EcomOS reel templates: Founder Explainer, Founder Story, Problem → Solution, 3 Reasons, Us vs Them, Regret Review, Comment Reply). **When `template` is set, `template.brief` is the brief**: keep its beats in order, give each beat the cards it names, use the member's answers (product, points, offer) verbatim for card text, and if `template.script` exists expect the spoken lines to follow it — cut the takes that drift from it. Do not invent a different structure.
2. Propose the cut and the cards to the member exactly as in step 3 below (numbered lines, cuts, the ecommerce cards with real numbers from the brand brief and `get_products`). Wait for their yes.
3. `set_edit {reelId, edit: {keep: [[start,end],…], accentWords, cards: [{id,type,anchor,after?,end_anchor?,…}], tail}}` — anchors are spoken words from the transcript; `after` disambiguates repeated words. The cards are the same objects as a local `proposal.json`; y-positions and the "never cover the face" rule still apply (the brief says where the face sits only if you look at frames, so put cards low when in doubt: title y≈1080, review y≈1060, product y≈940).
4. `render_reel {reelId, mode: "preview"}` → tell the member it takes 1–3 minutes and they can watch it on the Reel Editor page. Poll `get_render` (every ~30 s, not more). It returns the QA result and **frames as images at every card** — look at them: inside the frame, readable, on brand, face clear, price exact. Fix the edit and re-render if not.
5. When the member approves: `render_reel {mode: "final"}` → `get_render final` → confirm QA PASS → tell them to download from the Reel Editor page. The reel is logged in EcomOS automatically (no `log_reel` call needed on the hosted path).

## 1–8. The edit, in order (local path)

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
