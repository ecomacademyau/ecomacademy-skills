# ECA Reel Editor (skill in the ECA Marketing Coworker)

Drop a raw talking-head clip into Claude Code and get back a finished vertical reel or Meta video ad **in your own brand**: cleaned-up audio, the "um"s and false starts cut, captions and graphics that match what you actually say, and — because you sell things — **product, review and offer cards** pulled from your Shopify store.

It runs on your computer and your Claude plan. Your footage never leaves your machine: transcription is local, rendering is local, and the private review page on your claude.ai account only ever sees a small preview.

## What you need

- **Claude Code** on a paid Claude plan (the review page uses Claude Code's Artifacts; older versions review in chat instead).
- **The ECA Marketing Coworker plugin** with a built brand: the reel editor reads `./brand/brand-data.md` from the brand-intelligence skill. No brand file → it sends you to build one first (about ten minutes). There is no brand questionnaire in this plugin.
- **EcomOS connected** (recommended): the Marketing Coworker already knows the EcomOS server. In Claude Code type `/mcp`, choose **ecomos**, **Authenticate**, sign in with your EcomOS Google account and press Allow. (claude.ai or the desktop app: Settings → Connectors → Add custom connector → `https://ecomos.ecomacademy.co/mcp`.) No terminal needed. That gives the editor your live products (image, price, link), keeps your brand in sync with the dashboard, and logs every reel you deliver. Without it the editor asks you for a product photo and price.
- **ffmpeg**, **Node.js** (LTS) and **Python 3.10+**. Mac: `brew install ffmpeg node`. Windows: install from ffmpeg.org / nodejs.org / python.org, or `npm i -g ffmpeg-static ffprobe-static`.
- **The HyperFrames skills** (free, from HeyGen): `npx skills add heygen-com/hyperframes`.
- About 10 GB of free disk (35 GB for 4K exports).
- Optional: an ElevenLabs key for tighter word timing (`ELEVENLABS_API_KEY` in `./reels/.env`); DeepFilterNet (`uv tool install deepfilternet`) for stronger background-noise removal.

## Install

The reel editor is part of the **ECA Marketing Coworker** plugin (it needs brand-intelligence from the same bundle). In Claude Code:

```
/plugin marketplace add ecomacademyau/ecomacademy-skills
/plugin install eca-ecommerce-agent --marketplace ecomacademyau/ecomacademy-skills
```

Then, in Claude Code, inside your brand folder: **"run the reel editor doctor check"**. It tells you plainly what is missing.

## Use it

1. Film yourself talking to camera (a phone is fine). Say the product's name when you hold it up; say the code if there is one.
2. In Claude Code, in your brand folder: **"edit this into a reel"** and drag the video in. (Or "turn this into a Meta ad", "cut this down and add my product".)
3. First time only: it asks up to six quick questions about captions, sounds, pacing and your usual call to action, writes the answers into §4 of your brand file as a *Reel kit*, and syncs them to EcomOS. Never again.
4. You get a private **Reel Review** page: tap words to cut, keep or drop each graphic (including the product, review and offer cards), play the rough cut, then say **"build preview"**.
5. Watch the draft, leave notes, say **"final"**. The MP4 lands in `./reels/delivered/`, and the reel is logged in EcomOS.

Nothing renders until you have approved it.

## The ecommerce cards

| card | shows | where the facts come from |
|---|---|---|
| **product** | product image, name, price (and the compare-at price struck through) | `get_products` from EcomOS → your Shopify store; or a photo + price you give |
| **review** | stars drawing in, the review count counting up, one real quote | the Proof section of your brand file (§8); never estimated |
| **offer** | end card: your call to action, a dashed discount code, your store URL | your CTA from the Reel kit; codes only from you |

Real numbers only. If the brand file has no review count, there is no review card.

## Where things live

```
your-brand-folder/
├── brand/
│   ├── brand-data.md      ← the brand (brand-intelligence writes it; the Reel kit block lands in §4)
│   └── fonts/             ← drop your brand fonts here (.ttf/.otf/.woff2); otherwise Google Fonts are fetched
└── reels/
    ├── brand.json         ← made from brand-data.md by scripts/brand_from_eca.py (don't edit by hand)
    ├── reel-brief.md      ← what Claude reads before proposing an edit
    ├── delivered/         ← finished MP4s
    └── 2026-10-26-launch/ ← one folder per reel (raw clip copy, transcript, edit.json, proj/, final.mp4)
```

Set `REELS_HOME` to put the workspace somewhere else. Never a cloud-synced folder (iCloud Desktop, OneDrive): big video files make it struggle.

## Platforms

Tested on macOS (Apple silicon). The scripts are Python and written to run on Windows and Linux too (libx264 instead of Apple's hardware encoder, so renders take longer), but **Windows is untested in this release** — please report anything odd.

## Privacy

- Your video, audio and transcript stay on your computer. The only things that leave it: a mono 64 kbps audio file to ElevenLabs *if* you set that key; a 540p preview to your own private claude.ai review page; and the brand summary + reel metadata (title, length, product name, a tiny thumbnail) to EcomOS.
- The EcomOS connection key is yours; revoke it any time from the Brand Profile card.

## Credits

Built on **[claude-reel-editor](https://github.com/nicolapocock/claude-reel-editor)** by Nicola Pocock ([@getgitgirl](https://instagram.com/getgitgirl)), MIT — the template engine (`build_reel.py`), the cut/tighten/QA pipeline and the Reel Review page are hers. This fork adds the brand-file integration, the EcomOS tools, the ecommerce cards and the cross-platform Python scripts. See `LICENSE` and `LICENSE-nicola-pocock`.
