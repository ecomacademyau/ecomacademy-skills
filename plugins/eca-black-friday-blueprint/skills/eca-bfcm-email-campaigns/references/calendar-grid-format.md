# Calendar-grid visual format

The skeleton calendar (Stage 2) and its review (Stage 4) are presented as an **editable calendar-grid document**, not a plain table — built with the `design` skill (Claude Design canvas) so the member can review it as an actual calendar and keep editing it directly afterward (drag/retype cells, move sends) rather than only through chat.

## Layout

- **Page title**: the campaign name, e.g. "[Brand] — BFCM [year] Email Calendar".
- Laid out as a real calendar: rows of cells running Monday→Sunday (or however the member's week starts), one cell per date in the sale window. Split across multiple weeks/rows the way a wall calendar does, not a single long strip.
- Each date cell is headed by its day number in a coloured bar (a light accent tint reads best — pale green worked well in the member's own reference; match the brand's accent colour if `eca-brand-intelligence` is installed).
- Inside each date that has a send, stack up to three short rows, each labelled with a small channel icon/tag:
  - **EDM** — the email topic/subject in a few words, with an AM/PM tag if there are two sends that day (e.g. "Launch – Hero offer (AM)" / "Launch Reminder (PM)").
  - **SEGMENT** — the audience for that send (e.g. "Full list (ex recent buyers)", "Engaged 180 days", "Window Shoppers").
  - **SMS** — a short SMS note, only when the calendar includes an SMS send that day.
- Leave a date's rows blank if nothing is scheduled that day — don't force content into every cell just to fill it.

## Building it

1. Work out the full slot data first (date, type, topic, segment/audience if known, source) — this is the same data `templates/calendar-template.md` captures, so keep the two in sync rather than maintaining the grid as a separate source of truth.
2. Invoke the `design` skill to create the canvas, laying it out per the spec above. Use the member's actual sale dates and topics — never placeholder text.
3. Present the canvas to the member for Stage 4's review. They can either edit it directly themselves (Claude Design supports click-to-select, inline text editing) or tell Claude what to change, with Claude updating the canvas and republishing.
4. Keep `templates/calendar-template.md`'s table as the fallback presentation if the `design` skill isn't available in the session for any reason — tell the member plainly that's what's happening rather than silently downgrading the deliverable.

## What NOT to do

- Don't ship the ratio math (e.g. "4 Hero, 5 Product...") as text baked into the canvas itself — say that part in chat, and keep the canvas itself clean and calendar-like, the way the member's own reference does.
- Don't cram every topic-bank label onto the grid unedited — every cell's text should already be reframed around the real offer, exactly as `references/topic-bank.md` requires.
