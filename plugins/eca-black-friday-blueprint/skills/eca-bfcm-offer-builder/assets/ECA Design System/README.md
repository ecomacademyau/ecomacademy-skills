# ECA Design System — report skin

The 4PI report chrome uses the **Ecommerce Academy™ (ECA)** brand, with the client named in the header ("Prepared for <Client>"). Client brand colors from `clients/<brand>.md` may appear only as small identity touches (e.g. client logo in the header); the report itself is ECA-branded.

## Rules (from the ECA design system)

- **Dark hero header:** `--eca-black` background, white text, ECA logo mark, green eyebrow label.
- **Headlines:** Nunito Sans (Mont substitute) 800–900, **ALL CAPS**, letter-spacing `-0.03em`, line-height 1.1. Section headers Title Case.
- **Body:** Montserrat 400–600, line-height 1.6. Sentence case.
- **Eyebrow labels:** Montserrat 700, ALL CAPS, letter-spacing `0.12em`, in `--eca-green`.
- **Light content sections:** white cards on `--eca-bg`, radius 12px, `1px solid --eca-line`, subtle shadow. No heavy drop shadows, no gradients, no pastels.
- **Action pills:** radius-full. Keep/Scalable = `--eca-success` tint · Hold/Watch = `--eca-warning` tint · Fix = `--eca-info` tint · Stop = `--eca-error` tint · Insufficient = gray tint.
- **Highlights & success signals:** `--eca-green` / `--eca-green-tint`. Featured cards may use `--eca-shadow-green`.
- **Alerts:** warning band = `--eca-warning` tint; danger band = `--eca-error` tint.
- **Logo:** priority order — (1) official PNGs if present in this folder (`ECA-Logo-HZ-White-Trans.png` on the dark header); (2) `eca-mark.svg` in this folder (vector recreation of the bar-chart-and-arrow mark — inline its contents into the report so the file stays self-contained) paired with the wordmark "ECOMMERCE ACADEMY™" rendered as heavy italic caps in Nunito Sans; (3) never skip branding. If official PNG files are ever added here, they take precedence over the SVG.
- **Voice in report copy:** direct, punchy, "you" language. Numbers for credibility. No emoji.

Tokens: `eca-tokens.css` in this folder.
