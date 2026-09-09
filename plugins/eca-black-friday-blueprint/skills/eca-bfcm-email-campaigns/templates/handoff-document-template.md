# BFCM email calendar — handoff document

This is the shape of the final deliverable (Stage 6). **Post it in full, directly in the chat** — this is how the member receives it, not a file they have to go open. Separately, also save a copy to the project's `campaigns/` folder as markdown, named by date + slug, e.g. `campaigns/2026-11-bfcm-email-calendar.md`, so there's a record — but that save is a backup, not the delivery. Offer a `.docx` or `.pdf` export (via the `docx`/`pdf` skills) if the member wants a polished copy to send elsewhere.

---

## Campaign overview

- **Brand:** [name]
- **Offer:** [the offer, stated simply]
- **Sale window:** [start] – [end], [timezone]
- **Cadence:** [e.g. every day / every other day]
- **Content mix:** [Hero x / Product x / Education x / Plain text x — the locked ratio]
- **Footer (every email):** [the brand's standard footer — social links, unsubscribe, and anything else they normally include. Stated once here since it's the same on every send, rather than repeated in each email section below.]

## Email 1 — [Topic / working name]

- **Send date:** [date + time]
- **Type:** Hero / Product / Education / Plain text
- **Subject line options:**
  1. [option A]
  2. [option B]
  3. [option C]
- **Preview text:** [one line, complements the subject, doesn't repeat it]
- **Layout:** [section-by-section notes from `references/wireframe-layouts.md`, specific to this email — not just "use the Hero layout"]
- **Body copy:** [full copy, on-brand voice]
- **Primary CTA:** [button text] → [where it links]
- **Image/design notes:** [what should be in the hero image or product shots — mood, what's explicitly NOT in it, any badge/urgency element]
- **Standalone check:** [confirm this email makes full sense and still sells to someone who saw none of the others]

*(Repeat the "Email N" block for every locked email in the calendar.)*

---

## Starter prompt for Claude Design

Give the member a ready-to-paste prompt to kick off building these emails in Claude Design (the `design` skill / canvas). Adapt this shape to the actual campaign — don't hand over the placeholder text verbatim:

> Build [N] marketing emails for [brand]'s [offer name] sale ([dates]). Each email is a separate artboard. Use [brand]'s visual identity: [colours/fonts/logo notes — pull from brand-intelligence if installed, otherwise ask].
>
> Email 1 — [type]: [one-line brief pulling the layout + hero copy from the section above]
> Email 2 — [type]: [...]
> [... one line per email, in send order]
>
> Each email should follow the [Hero/Product/Education/Plain text] wireframe rules: [paste the relevant one-line summary from `references/wireframe-layouts.md` for that email's type]. Every email includes the standard footer noted in the campaign overview above (social links, unsubscribe, etc.) — carry it onto every artboard.

Tell the member they can hand this whole handoff document to Claude Design as context alongside the prompt, so every email's full copy and layout notes are available while it builds.
