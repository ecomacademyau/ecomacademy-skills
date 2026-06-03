#!/usr/bin/env python3
"""
Render a campaign calendar as a PNG image.

Why an image: a styled HTML/Word table loses its borders and cell shading when
the .docx is opened in Word/Pages, collapsing into unreadable floating columns.
An image renders identically in Word, Pages, and the PDF. The editable per-step
detail still lives in the runsheet table + Email/SMS section of the brief.

Usage:
    python3 make_calendar.py spec.json out.png

spec.json:
{
  "weeks": [
    [ {"day":"20","label":"Capture begins — early-bird ads","phase":"cap"},
      {"day":"21","label":"Capture running","phase":"cap"}, ... up to 7 ... ],
    ...
  ]
}
Each week is Mon..Sun (pad with {"day":"15"} for empty days; omit "phase" if none).
Phases: cap, ea, launch, sale, last, close.
"""
import json, sys, textwrap
from PIL import Image, ImageDraw, ImageFont

ACCENT = (0, 200, 83)            # #00c853
PHASE = {
    "cap":   (232, 245, 233),    # capture — light green
    "ea":    (200, 230, 201),    # early access
    "launch":(129, 199, 132),    # launch — medium green
    "sale":  (241, 248, 233),    # sale — pale lime
    "last":  (102, 187, 106),    # last chance — strong green
    "close": (224, 224, 224),    # close — grey
}
PHASE_LABEL = [("Capture","cap"),("Early access","ea"),("Launch","launch"),
               ("Sale","sale"),("Last chance","last"),("Close","close")]
BORDER = (140, 140, 140)
INK = (33, 33, 33)
DAYS = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]

FB = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
FR = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"


def wrap(draw, text, font, maxw):
    words, lines, cur = text.split(), [], ""
    for w in words:
        t = (cur + " " + w).strip()
        if draw.textlength(t, font=font) <= maxw or not cur:
            cur = t
        else:
            lines.append(cur); cur = w
    if cur:
        lines.append(cur)
    return lines


def main():
    spec = json.load(open(sys.argv[1]))
    out = sys.argv[2]
    weeks = spec["weeks"]

    W = 2310
    pad = 14
    col = W // 7
    hdr_h = 50
    f_hdr = ImageFont.truetype(FB, 26)
    f_day = ImageFont.truetype(FB, 30)
    f_txt = ImageFont.truetype(FR, 24)
    f_leg = ImageFont.truetype(FR, 24)
    line_h = 30

    # measure row heights from wrapped label text
    scratch = ImageDraw.Draw(Image.new("RGB", (10, 10)))
    row_h = []
    for week in weeks:
        maxlines = 1
        for cell in week:
            lbl = cell.get("label", "")
            if lbl:
                n = len(wrap(scratch, lbl, f_txt, col - 2 * pad))
                maxlines = max(maxlines, n + 1)  # +1 for the date line
        row_h.append(max(150, 46 + maxlines * line_h))

    leg_h = 70
    H = hdr_h + sum(row_h) + leg_h + 8
    img = Image.new("RGB", (W, H), "white")
    d = ImageDraw.Draw(img)

    # header
    d.rectangle([0, 0, W, hdr_h], fill=ACCENT)
    for i, day in enumerate(DAYS):
        tw = d.textlength(day, font=f_hdr)
        d.text((i * col + (col - tw) / 2, (hdr_h - 26) / 2), day, font=f_hdr, fill="white")

    # weeks
    y = hdr_h
    for wi, week in enumerate(weeks):
        h = row_h[wi]
        for i in range(7):
            x = i * col
            cell = week[i] if i < len(week) else {}
            fill = PHASE.get(cell.get("phase"), (255, 255, 255))
            d.rectangle([x, y, x + col, y + h], fill=fill, outline=BORDER, width=2)
            if cell.get("day"):
                d.text((x + pad, y + 8), str(cell["day"]), font=f_day, fill=INK)
            lbl = cell.get("label", "")
            if lbl:
                ty = y + 8 + 38
                for ln in wrap(d, lbl, f_txt, col - 2 * pad):
                    d.text((x + pad, ty), ln, font=f_txt, fill=INK)
                    ty += line_h
        y += h

    # legend
    ly = y + 16
    lx = 4
    for name, ph in PHASE_LABEL:
        d.rectangle([lx, ly, lx + 26, ly + 26], fill=PHASE[ph], outline=BORDER, width=2)
        d.text((lx + 34, ly + 1), name, font=f_leg, fill=INK)
        lx += 40 + int(d.textlength(name, font=f_leg)) + 40

    img.save(out)
    print("wrote", out)


if __name__ == "__main__":
    main()
