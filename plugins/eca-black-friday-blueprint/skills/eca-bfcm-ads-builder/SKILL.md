---
name: eca-bfcm-ads-builder
description: "Build finished Black Friday and Cyber Monday ad creative end to end. Takes the locked offer plus real product photos plus an inspo ad and generates the actual images through Higgsfield with the offer text baked in, the inspo's ratio first and the second ratio on approval, then writes bottom-of-funnel Meta copy and files everything in Notion and the campaign's shared files. Use for a black friday ad, BFCM creative, a cyber monday ad, sale or promo creative, build our BF ads, or when an inspo ad is uploaded alongside a sale offer. Requires eca-bfcm-offer-builder to have been run first, because the offer decides what the creative says. Needs Higgsfield connected to generate images, and falls back to a full creative brief and prompt when it is not."
---

# ECA BFCM Ads Builder

Takes a Black Friday offer, real product photos and an inspo ad, and produces finished launch-ready ad creative with the offer baked into the image. The inspo's own ratio first, the second ratio once approved, then bottom of funnel Meta copy, then filed in Notion.

This skill generates the actual ads. It does not hand back a prompt for someone else to run.

**Inspo** is the ad being built from. It is called inspo in the questions, in the Higgsfield media mapping, in the prompt and on the Notion row, so there is never any doubt which uploaded image is the layout master and which are the product.

## When to use this

Fire on: "black friday ad", "BFCM creative", "cyber monday ad", "build our BF ads", "make the black friday creative", "black friday static", "sale creative", "promo ad for the sale", "we need ads for the sale". Also fire when someone uploads an inspo ad while discussing a Black Friday, Cyber Monday or sale offer, even if they never say the words "black friday ad".

**Do not use this when the job belongs to a sibling skill:**

| The job | The skill |
|---|---|
| Deciding what the offer should be, from data | `eca-bfcm-offer-builder` |
| The email side of the sale | `eca-bfcm-email-campaigns` |
| Meta copy on its own, no image | `eca-ad-copywriting` (Marketing Coworker) |
| UGC and short-form video scripts | `eca-ugc-scripts` (Marketing Coworker) |

**The offer must already be decided. This skill does not run without it.** Building creative for an offer nobody has costed is wasted work, and it is expensive wasted work here because every re-roll spends credits. If there is no locked offer, stop and route to `eca-bfcm-offer-builder`.

## Non-negotiables

These exist because each one has cost real money before.

- **The product must be indistinguishable from the real packaging.** Never invent packaging, label wording, pack size, colour or closure. Prefer the brand's own live product images over supplied photos (step 4). If both are unclear, stop and ask.
- **Match the inspo's geometry, not its vibe.** The finished ad should be recognisable as the same layout: same camera height, same crop, same subject scale, same text zones at the same percentages. "Inspired by" is not the brief. A rebuild is.
- **Take the inspo's text positions, never its words or its line count.** The inspo shows where copy can sit. What the copy says is always the member's decision, asked at step 5. An inspo with five lines does not mean the ad needs five lines, and the ad should never inherit the inspo's phrasing, its claims or its offer.
- **When fidelity and geometry collide, the member chooses.** These two rules fight each other more often than you would expect and neither wins by default. See *The collision* in step 5. Picking one quietly and presenting the result as though there was no choice is the failure.
- **Never carry the inspo's brand assets.** Take geometry only. Discard its product, logo, wordmark, typeface, palette, talent and copy. Every prompt built from an inspo must contain an explicit exclusion line.
- **Never state a claim the brand cannot back.** Percentages, review counts, "biggest sale ever", "lowest price of the year" and stock scarcity must be sourced or confirmed by the member.
- **Never write a deadline that was not supplied.** No date given means no "ends Sunday", no countdown, no "last chance".
- **Never re-roll a concept that already passed.** When one arm of a test fails and the other passes, re-roll only the failing arm. Paying twice for an image already approved is the most common way this skill wastes credits.
- **Look at every generated image in Chrome.** You cannot see Higgsfield output any other way. Step 8 is not optional.
- **Say what you actually loaded and what you can actually see.** If brand intelligence was thin, say so before producing anything. If you could not view the generated images yourself, say that plainly rather than implying they passed.
- **House style:** Australian English, no em dashes anywhere, "mum" and "mums" never "mom" or "moms".

## Cost and pace discipline

This skill spends the member's credits and their afternoon. Both are budgets.

**The resolution ladder.** Meta's largest static spec is 1080x1920, so 2k output already oversamples everything this will ever serve at. Render cheap while deciding, and never above the ceiling.

| Stage | Settings | Count |
|---|---|---|
| Exploring concepts | `resolution: 1k`, `quality: medium` | **one variant per concept** |
| Final render of the approved concept | `resolution: 2k`, `quality: high` | two variants |
| Second ratio | `resolution: 2k`, `quality: high` | two variants |

**2k is the ceiling. Never render at 4k.** It costs several times more for pixels nothing displays. If label text will not hold at 2k, the answer is a different composition or a different base photo, not more pixels.

A higher-resolution render is a **new image, not an upscale**, so it must be verified again from scratch. Pass the approved exploration frame in as a reference with the scene carry over lock (step 10) so the scene, product, lighting and type styling survive. `upscale_image` is worth testing as a cheaper alternative, but it cannot recover label detail that was never rendered, so verify before trusting it.

**Preflight the real numbers once per session.** Call `generate_image` with `get_cost: true` at each tier you intend to use and state the credits out loud before the first real call. Prices change; do not quote remembered ones.

**Round trips are the other budget.** This skill should reach generation in **two** exchanges with the member: one short ask for the offer and the assets (step 3), one informed decision block (step 5). Anything the brand's live store, the ad account or the Notion board can tell you, find out yourself rather than asking. A question the live site answers in one call is a question you should not have asked.

**Write less.** Every explanatory step below carries a length cap and the caps are the rule. Reasoning that does not change what the member decides is an internal check, not output. **The prompt itself is never printed.** It is written, passed to the model, and filed in Notion at step 13.

## Steps

### 0. Preflight. A gate, not a formality.

**Higgsfield must be connected or there is no image.** Load the tools, then call `balance`. It confirms auth and shows credits.

If it fails, stop. Do not start the questions, do not load brand data, do not ask for photos. A run that dies at step 7 has already spent the member's time on four answers.

**Not every member has Higgsfield, so do not assume they know what it is.** A bare "Higgsfield is not connected" tells someone who has never heard of it nothing and leaves them stuck. Say what it is, what it is for, and what happens next:

> "This skill generates the actual ad images through Higgsfield, an image generation service, and it isn't connected yet. It's a paid third-party tool with its own credits, separate from your Claude subscription. Once it's connected I can build the creative end to end. Without it I can still do everything up to the image: measure your inspo ad, decide the composition and the on-image copy, write the full generation prompt and the Meta copy, and file the brief. You'd then run the prompt in whatever image tool you use."

Then ask which they want: connect Higgsfield and run properly, or take the brief-only path now. **The brief-only path is a real deliverable, not a consolation** — steps 1 to 6, then 12, then 13, skipping generation and verification. Say plainly at handover that the images were not generated or checked.

**Say whether the balance is enough.** A full run at the ladder above is roughly four exploration images plus four finals. If the balance will not cover that, say so now and agree what gets cut, rather than running out mid-batch.

**Claude in Chrome must be connected or you cannot verify.** Call `tabs_context_mcp` with `createIfEmpty: true`. It should return a tabId. If it fails, say so now and agree with the member up front that they will be doing the checking, rather than discovering it after four images already exist.

If more than one Chrome is paired to the account, `tabs_context_mcp` errors until one is chosen. List them, ask which, call `select_browser` with that deviceId, then carry on. Never pick one yourself.

Notion is only needed at step 13. Check it there, not here.

Report in three lines, not a paragraph:

```
Higgsfield   OK, 420 credits (enough for a full run)
Chrome       OK
```

### 1. Load the brand intelligence

Look in this order and stop at the first useful hit, continuing to gather anything else available:

1. A dedicated brand intelligence skill for that brand, including its `references/` files
2. `brand-data.md`, `brand-dna.md`, `brand-voice.md`, `icp-cards.md` in the working folder, `./brand/`, or `./clients/[brand]/brand/`
3. Any client config from a sibling report skill
4. If none exist, scrape the live site with WebFetch, then Firecrawl if blocked, for palette hex values, typography, product range, sourced claims, review count and voice
5. If that also fails, ask for the site URL. Never proceed on guesses.

Extract only what the build needs: exact product names and pack specs, palette as hex with dominant versus accent, typography feel, the brand's own photography style, the buyer, the objection, and every sourced number.

**Re-check live any number that will go on the image.** Review counts, star ratings and prices drift, and a brand file a few months old is routinely out by a hundred reviews, sometimes carrying three conflicting figures for the same thing. Open the live site and read the current number yourself. A figure baked into a static runs for a month and cannot be edited afterwards, so a stale one is worse than no proof line at all. Say in one clause what you corrected.

**Cap: two lines plus any correction.** Say what loaded and what is missing. Not a brand summary. If you built it from the live site, offer in one clause to save a `brand-data.md` so the next run is instant.

### 2. Check the backlog. Never build the same ad twice.

Before choosing anything, look at what already exists:

- **The brand's BFCM board**, for what has already been produced this campaign and which photos it used
- **What is live right now**, via `ads_library_search` on the brand's page ID

`ads_library_search` takes `search_terms` or `page_ids`, plus `countries`, `ad_active_status` and `limit`. A bare brand name pulls in unrelated advertisers, so find the page ID from one loose search then re-query with `page_ids` for a clean list. **It has no media type filter**, so catalogue and dynamic tiles come back mixed in with real ads. Spot them by the `ad_creative_link_title`: a templated value like `{{product.name}}` is a catalogue tile nobody wrote. Ignore those when judging what the brand is running.

**Cap: one line.** "You have two BF statics live, both single bottle on cream, both percentage led. This one differs on cast, composition and offer framing." Then build something different. If a photo or a composition already appears on the board, do not reuse it unless the treatment is genuinely different.

### 3. The asset ask. Short, and only what you cannot find yourself.

Ask for three things in one block and nothing else. The rest waits for step 5, when you will actually know the layout.

1. **The offer.** **Do not ask for this if `bfcm/bfcm-<year>-master.md` exists** — read the locked one-liner from §7, the depth and the dates from §1 and §10, and confirm them back in one line. This skill's own rule about round trips applies to itself: a question the Master File answers is a question you should not have asked. Only ask verbatim when there is no Master File, and in that case stop first and route to `eca-bfcm-offer-builder`. Either way, if they volunteer the regular price, calculate the saving, the percentage and the per-unit cost and hold those as copy options.

   **The on-image offer line must say the same thing as §7's one-liner.** Not a tighter rewrite, not a punchier version. When the ad, the email and the site banner each phrase the sale differently, a customer reads three offers and resolves the confusion by leaving.
2. **The product references.** A clean unstyled shot on a plain background as the fidelity anchor, an in-hand shot for real scale, optionally a lifestyle shot. Ask which variant is the hero, and for all of them if the ad shows a multi-pack. **Say you will cross-check these against the live store**, so a member with outdated photos is not surprised later.
3. **The inspo.** One ad. If they say none, build from the brand's own best performing style and say so.

**Do not ask about composition, camera, arrangement, on-image copy, anchors or deadlines here.** All of those depend on the inspo's measured geometry, and you have not measured it yet. Asking now is how the on-image copy gets chosen blind and costs a whole re-roll to fix.

**Defaults, stated and acted on rather than asked:** bottom of funnel, the inspo's own ratio first, the second ratio on approval, `gpt_image_2`, and the resolution ladder above. Only raise one of these if the member's request contradicts it.

### 4. Read the product, verify it against the live store, measure the inspo

This is the analysis step. No questions to the member, no credits spent.

#### Read the packaging back

View every uploaded image and describe in writing what is actually on the packaging before writing a single line of prompt.

**Then verify against the brand's live store, and prefer the store's own images as references.** The store's product and variant images are current, consistently lit and shot from the same angle, which makes them a better reference set than a mixed bag of supplied photos. On Shopify, `/products/<handle>.js` returns the variant and media image URLs as JSON; pass those straight to `media_import_url` and use the returned `media_id`. This costs two calls and routinely catches an artwork generation the member believes has been replaced.

If the live store and the uploads disagree, **say which you are treating as current and why, and show the member the evidence** rather than asking them to recall. If the member contradicts what the store shows, put it to them once with what you found, then act on their answer.

**Count the distinct labels going in frame and say the number out loud.** One label repeated is easy. Four different labels in four different colours with four different text blocks is the hardest fidelity ask there is. That count drives the collision in step 5, so it belongs on the record before anything is generated.

#### Measure the inspo. Do not describe it.

Every layout zone comes out as a **number**, and those numbers go into the prompt verbatim.

A blueprint that says "text sits high" produces an ad that looks nothing like the inspo. A blueprint that says "badge at 26, headline at 33, product 44 to 60, supporting line at 68" produces one that does.

View the inspo and record:

- **Ratio.** 1:1, 4:5 or 9:16. This decides which ratio gets built first.
- **Format:** photo, graphic, split frame, POV, UGC still, screenshot
- **Camera:** height, angle, distance from subject
- **Layout zones as percentages of frame height:** where each text element sits, where the product sits, where the background bands start and stop
- **Subject scale:** what fraction of the frame width and height the product occupies
- **Hierarchy:** what the eye hits first, second, third
- **Colour blocking:** how many blocks, which dominates, where the contrast sits
- **Text treatment:** how many positions, case, weight, and each one's size relative to the largest
- **Energy:** clean and premium, loud and promotional, editorial, homemade
- **Whether the text is an overlay or a physical object in the scene.** A card, sign, note or label propped in shot behaves differently at step 6 and is worth naming now.

**Record the inspo's text positions as a menu, not a quota.** Note where copy can sit and at what relative size: a header above the offer, a supporting line below it, a footer. You are taking the positions so the member can choose from them at step 5. **Do not transcribe what the inspo says into the options.** Its wording, its claims and its offer are not yours, and an ad that uses three of its five positions is a correct rebuild, not an incomplete one. Unused positions close up; they never get filled with filler to match the inspo's density.

**Cap: six lines plus the numbers.** What is kept and what is discarded is a check you run, not a list you print. The exclusion line in the prompt is where that has to show up.

**Check the contrast will survive the swap.** If the inspo runs white type over a mid-tone scene and the brand's world is bright and pale, white type will vanish. Re-specify the type colour from the brand palette and state the substitution in one clause.

### 5. One decision block. Everything, once, informed.

You now know the offer, the product, the label count and the inspo's geometry. Put every remaining decision to the member in a single block.

1. **The anchor, if any.** Propose the price a customer actually pays today rather than RRP, and say why in one clause. Anchoring to a price nobody pays is exactly the comparison the ACCC pulls people up on. When the real paid price is genuinely messy across subscription, volume tiers and funnel SKUs, recommend no anchor.
2. **The on-image copy. Always asked, never inherited.** Say how many text positions the inspo's layout offers and roughly where they sit, then offer grounded candidates the member picks from: the offer formula (see the angle table below), the event name, review count and rating, made-in claim, guarantee, units per pack, per-unit cost. Pull the candidates from brand data and the live site, never from the inspo's own wording. **Say plainly that fewer is fine** and that unused positions close up rather than needing filler. Three text elements is the working maximum on a static regardless of what the inspo carries; go beyond it only when the member asks and the layout genuinely holds it.
3. **The deadline, if any urgency line is wanted.** A real date or no urgency line. Offer the plausible dates from the calendar rather than asking them to type one.
4. **The collision, when it applies.** See below.

Everything the member picks here should be actionable without a follow-up. If you find yourself asking a fifth question later, the block was written badly.

#### The collision

Some layouts are actively hostile to packaging accuracy. Units tumbled, angled, overlapping, half inside a box, or sitting at different distances from the lens is precisely the geometry where labels drift, small type garbles and duplicate units come back inconsistent. The risk multiplies with every extra distinct label in frame, which is why step 4 counts them. **The single steepest-angled unit in the foreground is where it breaks**, because it is largest in frame and furthest from square.

When the inspo's geometry is one of those and the product is a multi-unit or multi-label ask, **put it to the member in three lines**: name the conflict, say which way you would go and why, then act on their answer.

- Flattening the layout to protect the labels gives an accurate ad that looks nothing like the inspo, which is the thing they asked you to rebuild.
- Copying the layout faithfully gives a recognisable ad with garbled packaging, which is dead on arrival.
- A third option exists and is often the best one: build both, one clean and one faithful, and let the image be the test variable instead of the copy.

**Building both doubles the exploration spend**, so say that when you offer it. At exploration resolution it is cheap; at final resolution it is not, which is why only the approved arms get rendered at 2k.

If you catch yourself writing "square to the lens, evenly spaced" into a prompt built from a messy inspo, that is the collision and it needed a question.

### 6. Write the prompt. Do not print it.

Write it, pass it to the model, move on. It gets filed in Notion at step 13 where the member can read it if a variant needs debugging. Printing it before generating costs the member a wall of text they did not ask for.

One continuous block in this order: format and ratio, camera and device, angle and composition, main subject with exact materials and imperfections, the three locks, supporting elements, environment, lighting with direction, palette as hex, mood, anti-AI cues, then the text specification, then the spelling guard.

**The product lock, always included:**

> Take the product from the product reference images and reproduce it exactly as shown: same label typography, same colour, same finish, same proportions, same cap and closure. Do not redesign, restyle, re letter or re typeset any part of the packaging.

Follow it with a per-variant description: for each distinct label, its colour, its wordmark, its descriptor lines verbatim, its badges, its flavour or variant chip, and its size and count numerals. Say explicitly where a badge is **absent** on one variant, or the model will add it for consistency.

**The wordmark orientation lock, whenever the wordmark runs vertically or any unit is not square to the lens:**

> On every unit, whatever angle it is lying or standing at, the wordmark is rotated ninety degrees ANTICLOCKWISE relative to its label, so that the word reads from the base toward the cap and the tops of its letters face the left edge of the label. It must never be rotated clockwise, never mirrored, never inverted and never set horizontally. This applies identically to units lying on their sides and to units seen at an angle.

Substitute the real direction. Without this, a tumbled unit comes back with the wordmark flipped, and that failure is invisible until you zoom.

**The inspo lock, always included:**

> Reference image `inspo` is the layout master. Rebuild its composition exactly: same camera height and angle, same crop and distance, same subject scale within the frame, same number and placement of colour blocks, same hierarchy and the same relative type sizes. Treat it as a template being re-shot with a different product in it. Do not copy its product, logo, wordmark, typeface, palette, talent or wording, and use none of its colours. Use only the text specified below; the inspo's own lines are not part of this image.

When a concept deliberately departs from the inspo's arrangement, narrow this lock to the frame, camera and text zones and say so, rather than leaving a contradiction in the prompt.

**Keep the locks apart, in these words.** The inspo governs **geometry**: where things sit, how big, what angle, what crop, what the eye hits first. The product references govern **appearance**: what the thing itself looks like. The text specification governs **wording**, and nothing else does. Name which reference governs which, and add a line saying none may influence the others. If the inspo is allowed to influence the product or the copy, the two compete and the model invents a third thing.

**Name every reference by what is in it, never by its slot number.** Upload order is not guaranteed to survive the widget, and "reference image 3" silently points at the wrong unit when it does not. "The bottle with the orange wordmark" and "the photograph of a parcel on green fabric" cannot be mis-slotted.

**The mood line carries the inspo's energy, not the brand's.** A homemade inspo described in the prompt as "calm, everyday premium" comes back as a tidy product shot. Write the energy you measured in step 4 and let the palette and the product lock do the brand work.

**Realism baseline:** `iPhone 15 Pro photo`, natural directional light with a named source and shadow direction, real materials, slight grain, slightly off centre, natural contact shadows. Apply those cues to the photographic layer only, never to typography or graphic blocks.

**Text specification:** name every element the member chose by position as a percentage of frame height, then give its exact colour as hex, its case, its weight and its size relative to the largest line. Where the member chose fewer elements than the inspo has positions, re-space the block so it sits balanced rather than leaving a gap where the inspo had a line. Apply the safe zone numbers below, and where a safe zone forces an element away from the inspo's position, move it and note which one moved. Then close the prompt with the spelling guard, which covers **every string in the image including text on the packaging**:

> The text must read exactly: "[string 1]", "[string 2]", "[string 3]". The badge on the label must read exactly: "[badge text]". No other text appears anywhere in the image.

Place names and small badge text garble more than headline text and nobody proofreads them. Put them in the guard.

### 7. Generate to explore. Cheap, and one per concept.

**Build the inspo's own ratio first.** If the inspo is 9:16, the first build is 9:16. If it is 1:1 or 4:5, the first build is 1:1. You cannot match a vertical layout in a square frame, so building the inspo's ratio first is what makes the accuracy rule achievable rather than aspirational.

Upload with `media_upload_widget`, called as the only tool in that turn, for anything genuinely local. Anything that exists on the brand's own site goes through `media_import_url` instead, which needs no member interaction. **Label the inspo `inspo` in the media mapping**, and the rest by what is in them. Say the mapping in one line so it can be corrected.

Generate on **`gpt_image_2`** at **`resolution: 1k`, `quality: medium`, one variant per concept**. Confirm model IDs with `models_explore` first, since Higgsfield renames models between releases, and preflight with `get_cost: true` before the real call. Use `generate_image_batch` when concepts differ, then `jobs_wait`, then a single `show_generation_by_ids` for the set.

**GPT Image 2 is the primary engine** because baked-in offer text is the hard requirement and it renders type far more cleanly than the alternatives.

One variant per concept is enough to judge layout, composition, scene and gross label fidelity. Variants are for choosing between near-identical outputs, which is a question you do not have yet.

### 8. Verify in Chrome. Triage first, then deep-check the survivors.

**You cannot see Higgsfield output any other way.** The sandbox network is allowlisted to package registries, so the image CDNs are unreachable and `WebFetch` will not help. Without Chrome, every statement about a generated image is a guess based on the prompt that was written rather than the image that came back.

**Triage pass, one screenshot for the whole set.** Inject the result URLs into a page side by side and screenshot once. This answers, for every image at once:

1. **Is it the right product.** A variant carrying the inspo's product instead of the brand's is dead. Check this first, it kills a variant fastest.
2. **Does the composition match the inspo.** Open the inspo in the same strip and compare zone by zone against the step 4 numbers: camera height, crop, subject scale, each text element's percentage, how the colour blocking splits the frame. **If someone would not recognise it as the same layout, that is a reroll, not a note.**
3. **Is any of the inspo's wording present.** A line the member never chose has leaked across. Reroll it.
4. **Anything grossly broken.** Hands, anatomy, a subject cropped at a frame edge, text in the wrong place.
5. **Safe zones, measured.** Calculate where each text element actually sits as a percentage of image height from this same screenshot. Do not assume the prompt was followed.

Kill anything that fails triage before spending another call on it.

**Deep pass, survivors only, at source resolution.** A side-by-side strip is downscaled several times over, so checking labels on it is checking nothing. Load one image at close to its native width, position it on the region you need, and screenshot:

6. **Packaging, against the source.** Open the product reference alongside rather than checking against what you expect. Every word on the label, pack size and count numerals, badge text and spelling, cap and closure shape, wordmark orientation on every unit. Where several units appear, each carrying the correct label for its own variant.
7. **Every on-image string, letter by letter.** Do not skim. CHRISIMAS looks like CHRISTMAS at a glance, and FR1DAY looks like FRIDAY. Check the currency symbol matches numeral height and apostrophes are intact.
8. **Contrast.** Type against the background that actually generated, not the one you specified.

If something fails, rebuild **only the failing concept**. A passing arm is finished; re-rolling it alongside the failure doubles the cost of the fix for nothing.

If the same element fails twice across attempts, it is not a prompt problem. Change the base photo, change that element's position in the composition, or tell the member it cannot be done that way. Say which, and say it after the second failure rather than the third. **Do not reach for more pixels**; the ceiling is 2k and raising resolution is not a fix for a composition the model cannot hold.

**If the packaging drifts on every variant of a concept**, re-run that concept on `nano_banana_pro` at exploration resolution and present both. Nano Banana Pro locks packaging harder and garbles text more, so when it is used, verify the on-image copy twice as carefully. Do not run it as a matter of course when another arm already passed.

A large PNG can lock the tab. If a zoom returns a script injection timeout, wait two seconds and retry rather than renavigating.

**If Chrome is genuinely unavailable**, hand the member the check list from the final section, say plainly you could not see the images, and wait for their confirmation. A member verifying is fine. Nobody verifying is not.

### 9. Approval gate

> "Are we happy with the result, or do we need any editing changes?"

Show what survived, say what failed and why, and loop on the first ratio until approved. Do not move on early. Each loop should change one named thing, not be a blind re-roll.

**Say here how the files reach them.** You cannot download the images, so the member does it from the Higgsfield card. See step 13. Tell them at this gate, not after they have approved and are sitting waiting for a file.

### 10. Render the approved concept at 2k

Only now spend the real credits. For each approved concept, generate at **`resolution: 2k`, `quality: high`, two variants**, passing the approved exploration frame in as a reference alongside the product references, with a scene carry over lock:

> The approved photograph is the scene master. Re-shoot that exact scene: same product, same set, same surfaces, same lighting direction, same text treatment, same energy.

Keep the product lock, the wordmark orientation lock and the full text specification verbatim. Drop nothing.

**This is a new image, not an upscale.** Run step 8's deep pass on it. Most of the time it holds; occasionally an element that passed at 1k breaks at 2k or the reverse.

**2k is where this stops.** If the labels or the on-image text will not hold here after two attempts, change the composition or the base photo, or tell the member that element cannot be done that way. Do not escalate the resolution.

### 11. Generate the second ratio

Only after the first is signed off. Same prompt logic re-composed for the new frame, not a crop, at the same 2k and high.

Pass the approved image in as a reference so the scene, product, lighting and type styling carry across, and drop the inspo at this point. The inspo only exists in one ratio, so it can no longer govern geometry here, and dropping it removes any risk of its palette bleeding in. **Say in one clause that the second ratio is derived from the approved image rather than matched to the inspo**, so nobody expects the same layout fidelity twice.

Re-specify every text position for the new frame using the numbers below. Same verification, minus the inspo comparison.

### 12. Write the Meta copy

Two primary texts and two headlines, all bottom of funnel and all specific to this offer.

Bottom of funnel means the reader already knows the product. No brand story, no education, no "did you know". Offer, proof, urgency, action.

#### Pull the control from last year's Black Friday

Do not write all four from scratch when the account already knows what worked. Before writing anything:

1. **Get ad-level performance for last year's BFCM window.** `ads_get_ad_entities` at `level: ad`, date range set to the equivalent period last year, not the last 30 days.
2. **Rank by profit after ad spend**, not by ROAS and not by spend. Spend times (ROAS minus 1). The order differs from the ROAS order and the second one is the truth. Mention the biggest loser too if one stands out; a top spender at sub-1 ROAS is worth the member knowing about before they set this year's budgets.
3. **Get the creative id off the winning ad.** `ads_get_ad_entities` again with `object_ids` set to the winners and `fields: ["id","name","creative_id"]`. The ad id is not the creative id, and the copy hangs off the creative.
4. **Get the copy off that creative.** `ads_get_creatives` with `creative_ids` **and** `fields: ["id","name","body","title"]`. You must pass both. Listing without `creative_ids` returns only id, name, account_id and status, the copy is silently omitted, and you would conclude there was none. `body` is primary text in Ads Manager, `title` is headline.
5. **Pull the top two or three, not just the winner.** A catalogue or dynamic ad returns no `body` or `title` at all, so the nominal winner sometimes has no written copy to take. Having the runner-up already in hand saves a round trip.
6. **Use the winner's copy verbatim as the control.** Do not improve it, modernise it, or fix its grammar. It earned its place by performing, and changing it means you no longer have a control.
7. **If the offer has moved since, change only the numbers that are now false.** List exactly what you changed and say plainly it is no longer a pure control. A price that no longer exists is not a control, it is a lie. Everything else stays, including the emoji and any maths that does not quite add up.
8. **Flag any claim in the control you cannot verify**, such as an undated urgency line or a duration claim, rather than silently keeping or silently fixing it. Keeping it is usually right; hiding it is not.
9. **Record which ad it came from and its cost per purchase** alongside the control, so the next person knows it is a real baseline rather than something invented.

If there is no history, or the account is new, write a control and say plainly that it is a placeholder rather than a proven baseline.

#### Write the test

The test is this year's offer written fresh. The comparison then means something: proven copy against the new offer, same image, same audience, rather than two guesses racing each other.

| Asset | Rule |
|---|---|
| Primary text, short | Under 125 characters so it never truncates behind "see more". Offer in the first five words. |
| Primary text, longer | Three to five short lines. Line one is the offer, one line of proof, one line of deadline or CTA. Line breaks, not a paragraph. |
| Headlines, both | Under 40 characters, ideally under 30. Not a sentence. Offer or single benefit. |

Write flat and specific. Clever costs comprehension, and comprehension is what gets the click.

**Say the launch matrix out loud.** Assets times copy sets is the real ad count, and it is usually bigger than the member is picturing. Offer a tighter cut if the full matrix looks like more than they want to build.

### 13. File it in Notion

> "Do you want this added to your Notion?"

If no, stop here and hand over the approved files.

If yes, check Notion is reachable now (`notion-get-users`), then create a board named `[Brand] BFCM [Year]`, for example `Acme BFCM 2026`. Ask where it should live the first time and remember the answer for the rest of the session. Look at how the member already names per-brand boards and match it.

#### Getting the images out of Higgsfield

**You cannot download them.** The Higgsfield result CDN refuses server-side requests: curl from the sandbox and curl from the member's own machine both return 403, and only an authenticated browser session can fetch a result URL. So the approved images cannot be written into the member's folder and cannot be uploaded into the Notion library by you.

The member downloads both from the Higgsfield generation card. Say so at the step 9 approval gate so nobody waits on a file that was never coming. File the board with the result URLs and the Higgsfield job ids beside them, so the assets stay traceable once the URLs expire, and leave a named file slot on the row for the member to drop the files into.

#### Columns versus pages

**Columns are for what gets sorted, filtered and scanned. Pages are for what gets read or pasted.**

On the row as columns: asset name, concept, ratio, status, offer, angle, result URL, job id, engine, verification notes, file slot.

On a page, never in a column:

- **The full prompt**, in each asset row's page body, with the media mapping above it. Nobody scans a prompt; they open it once when a variant needs debugging.
- **The Meta copy**, as its own page in the board, each block in its own code block so it gets a clean copy button. One page for the whole board rather than repeated on every asset row, so a copy edit is one edit. Put the control's source ad, cost per purchase and any unverified claims at the top of it.
- **The campaign brief**: offer maths, the collision decision and which way the member went, the inspo used, the backlog check, and a table of every number on the creative with where it came from.

Long copy in a property column truncates in the table, hides its line breaks, and has to be clicked into one cell at a time. It is the single most common way this board ends up unusable.

#### Naming, when this is a new campaign

If this run starts a new BFCM campaign rather than adding to one already on the board, name every asset to the convention. The 4PI analyst and Meta reporting read names, not images.

```
YYMMDD_Product_type_Funnel_Angle_Headline_Format_v#
```

Example:

```
261121_Concentrate_static_BOF_MixMatch_MixAndMatch4For80_1x1_v1
```

| Field | Rule |
|---|---|
| `YYMMDD` | Always. Sorts chronologically, unambiguous in every country. Never DDMMYY or MMDDYY. |
| `Product` | Short, consistent across every ad for that product |
| `type` | `static`, `video`, `carousel` |
| `Funnel` | `TOF`, `MOF`, `BOF` |
| `Angle` | A fixed token, reused across every ad on that angle, so Ads Manager can group them |
| `Headline` | The actual headline, camelCase, no spaces, so a human can read the report |
| `Format` | `1x1`, `4x5`, `9x16` |
| `v#` | Variation number within the set. When two concepts are being tested, keep one concept on `v1` and the other on `v2` across both ratios so the pairs line up. |

Angle and headline both. Drop the angle and grouping breaks. Drop the headline and nobody can read the report. No spaces anywhere: underscores separate fields, camelCase inside a field.

### 14. Write the ads into the shared campaign files

The Black Friday Blueprint keeps one set of shared files per campaign, in a `bfcm/` folder, so every channel lands in the same runsheet and the same dashboard. The Notion board is the creative workspace; these files are how the ads show up in the campaign the member actually opens on Black Friday morning. Do both.

**Skip only if there is no `bfcm/` folder**, and say so rather than skipping silently.

**1. Fill Master File §14.** `bfcm/bfcm-<year>-master.md` reserves section 14 for the Meta Ads plan and it currently reads *Reserved*. Replace it with: the concepts built, the angle and funnel stage of each, the ratios produced, the asset names to the convention above, where the files live, and a link to the Notion board if one was made. Anyone reading the Master File should be able to see what creative exists without opening Higgsfield.

**2. Append the launch tasks to `bfcm/bfcm-<year>-runsheet.csv`.** Append-only: add your rows, never edit another skill's. Tag every row `OWNER=ADS`.

| Column | What goes in it |
|---|---|
| `WHEN` | When the creative needs to be live in Ads Manager, which is **before** the phase starts, not on the day |
| `TASK` | `Creative live: <asset name>` |
| `PHASE_ID` | The phase it supports, from `bfcm/bfcm-<year>-calendar.csv` |
| `OWNER` | `ADS` |
| `STATUS` | `Not started` |
| `NOTES` | Ratio, angle, and the Notion row or result URL |

Place these against **phase IDs**, never hard-coded dates. If the member moves the launch, the creative deadline moves with it.

**3. Regenerate the dashboard.** Run `python3 ../eca-bfcm-offer-builder/scripts/sync_campaign.py bfcm/bfcm-<year>-calendar.csv bfcm/bfcm-<year>-runsheet.csv --html bfcm/bfcm-<year>-dashboard.html --markdown`. It validates as it goes and will flag a task sitting outside its phase.

**4. Log it in §21**, naming this skill, the date, and what it added.

## On-image copy: BFCM angle formulas

Use these when proposing the text baked into the ad at step 5. Name the angle, give the option, let them choose. These are the candidates; the inspo's own lines never are.

| Angle | Formula | Example |
|---|---|---|
| Bundle price | `[N] FOR $[X]` | "4 FOR $80" |
| Percentage | `[N]% OFF [scope]` | "25% OFF SITEWIDE" |
| Dollar saving | `SAVE $[X]` | "SAVE $20" |
| Unit maths | `[N] [units]. $[X] each.` | "60 COFFEES. $1.33 EACH." |
| Anchor | `WAS $[X]. NOW $[Y].` | "WAS $99. NOW $80." |
| Event name | `BLACK FRIDAY` | header line above the offer |
| Early access | `EARLY ACCESS` | "EARLY BLACK FRIDAY" |
| Deadline | `ENDS [day or date]` | "ENDS SUNDAY" |
| Gift with purchase | `FREE [item] WITH [threshold]` | "FREE JIGGER OVER $50" |

**Claim safety on these:** a deadline needs a supplied date. Scarcity, "biggest sale ever" and "lowest price of the year" need the member to confirm they are true. An anchor price needs the real regular price, not a rounded guess. The event name is safe on its own; it names the occasion rather than making a claim. If a proposed line rests on an unverified claim, say so beside the option so they can accept the risk knowingly.

**Avoid glyphs that garble.** Stars, ampersands and apostrophes are the three that come back mangled most often. "4.8 FROM 329 REVIEWS" survives where a star character does not.

**Flag a discount that fights the brand's own pricing.** If the per-unit sale price undercuts the subscription price, the member's best customers have an incentive to pause and buy the bundle instead. Say it once at the offer stage. It may well be a trade they want, but it should be knowing.

## Placement and safe zones

Meta unified Stories and Reels into a single 9:16 safe zone in March 2026, built around the tightest placement. The bottom zone is far bigger than most people assume.

| Placement | Size | Ratio | Top clear | Bottom clear | Sides clear |
|---|---|---|---|---|---|
| Feed square | 1080x1080 | 1:1 | ~10% | ~10% | ~10% |
| Stories and Reels | 1080x1920 | 9:16 | 14% (~250px) | **35% (~672px)** | 6% (~65px) |

On 9:16 the usable band is pixels **250 to 1248**, roughly 51 percent of the frame. Anything below that is covered by the CTA button and the caption and is invisible. A supporting line at 76 percent of frame height is not a small miss, it is text nobody will ever see.

**So on 9:16, all the text stacks high as one tight block in the top third.** Badge, headline and supporting line together, finishing by about 45 percent at the very latest. Everything below that is untouched photograph, which is where the product goes.

**The safe zone beats the inspo.** If the inspo puts a text element in the dead zone, as most organic-styled ads do, move it into the band and note which element moved and why. Copying an invisible caption position accurately is still an invisible caption.

### Overlay text versus a physical sign, and the undershoot

These behave differently and the difference is worth knowing before you prompt.

**Overlay text undershoots.** Models do not follow "keep the bottom 35 percent clear" reliably. What works is two explicit horizontal lines with the block stacked between them:

> Imagine a horizontal line at 9 percent of the image height, and a second at 36 percent. Every piece of text and every coloured bar must sit entirely between those two lines, stacked tightly together as one compact block. Absolutely nothing above the 9 percent line. Absolutely nothing below the 36 percent line.

GPT Image 2 prompted at 9 and 36 reliably produces a block measuring 4 to 33, which is the target. Prompted at 4 and 33 it jams the text against the top edge. **So: prompt to 9 and 36, measure against 4 and 33.**

**A physical sign inside the scene does not undershoot.** A card, board or note propped in shot lands close to where it is prompted, because it is an object in a composition rather than a typographic layer. Prompt the card's own top and bottom as percentages and expect it within two or three points. It also cannot go to 4 percent without being cropped at the frame edge, so it will sit lower, nearer 17 to 47, which is still comfortably inside Meta's real 14 to 65 band.

Measure in Chrome as a percentage of image height either way. Do not eyeball it. Report the measured numbers, name which line sits closest to a boundary, and let the member decide rather than rerolling something that has nowhere higher to go.

## Check before finishing

- The offer line on the image says the same thing as Master File §7's one-liner, not a rewrite of it.
- Master File §14 no longer reads *Reserved*, and §21 has a change-log line for this run.
- Every creative deadline was appended to the runsheet as `OWNER=ADS`, against a phase ID rather than a fixed date, and no other skill's rows were touched.
- If Higgsfield was unavailable, the handover says plainly that the images were never generated or verified, and what the member received instead.

**Run this yourself in Chrome. Do not print it for the member.** Printing it is the fallback for when Chrome is unavailable, not the normal path.

**Preflight and spend**
- Higgsfield confirmed, and the balance checked against what the run will cost, before any questions were asked
- Chrome confirmed, or its absence agreed with the member up front
- Exploration ran at 1k with one variant per concept, and finals at 2k. **Nothing was rendered at 4k.**
- No concept was re-rolled after it had already passed

**Inspo match**
- Built in the inspo's own ratio first
- Camera height, angle and crop match
- Subject occupies the same fraction of the frame
- Every text element sits at an inspo position, or moved for a safe zone with the move noted
- Colour blocking splits the frame the same way
- Someone shown both would call it the same layout
- If geometry was traded away for fidelity, the member made that call, it was not decided quietly

**Copy on the image**
- Every line on the creative was chosen by the member at step 5, not inherited from the inspo
- None of the inspo's wording, claims or offer appears anywhere in the image
- Where the member chose fewer elements than the inspo has positions, the block is re-spaced rather than padded

**Product**
- References were cross-checked against the brand's live store, not taken on trust from the uploads
- Wordmark is the right way up and the right way round on every unit, especially any that is lying down or angled
- Every word on the packaging matches the reference, nothing invented, nothing re-lettered
- Badge text spelled correctly, including place names
- Pack size and count numerals are correct, these garble more than anything else
- Cap, closure and bottle or box shape match the reference
- Where several units appear, each carries the correct label for its own variant
- Nothing from the inspo's product has carried across

**Text**
- Every on-image string zoomed and read letter by letter at source resolution, not off a side-by-side strip
- Price digits and the currency symbol are correct and the symbol matches the numeral height
- Apostrophes are intact, or the copy was written to avoid them
- No urgency wording unless a date was actually supplied

**Structure**
- None of the inspo's logo, typeface, palette, talent or copy has carried across
- Type has enough contrast against the actual background of the generated scene
- Safe zones measured as a percentage, not assumed, and the overlay versus physical-sign difference accounted for
- Human anatomy is correct if a person or hand is in frame, and nobody is cropped at a frame edge

**Campaign**
- Backlog checked, catalogue tiles excluded, and this set differs from what is already live
- Control copy pulled from last year's BFCM winner ranked by profit after ad spend, or flagged as a placeholder
- Any number changed in the control is listed, and the control flagged as no longer pure
- Any unverifiable claim left in the control is flagged rather than silently kept or silently fixed
- Source ad and its cost per purchase recorded alongside the control
- Named to the convention if this is a new campaign

**Copy and style**
- Australian English, no em dashes, "mum" not "mom"
- Every number on the creative and in the Meta copy traces back to brand data, the live site, last year's account data, or something the member confirmed
- Any stale brand-file number was re-checked live before it went on an image

**Notion**
- Prompts, Meta copy and the campaign brief are on pages, not in property columns
- Result URLs and job ids on the row, with an empty file slot for the member's upload

---
*Built with the TEACH framework. Hone it: run it on a real task, see what it gets wrong, and tune the steps or sharpen the trigger above.*