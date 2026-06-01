#!/usr/bin/env python3
"""
Export a campaign brief (markdown) to a polished .docx and/or .pdf.

Why this exists: a naive `pandoc brief.md -o brief.docx` emits tables with no
column grid and 0-width hints, so the wide runsheet/schedule tables overflow off
the page. This script instead goes markdown -> styled HTML -> LibreOffice, which
keeps wide tables inside the page, then injects a repeating footer (attribution +
page number) so it shows on every page of both formats.

Usage:
    python3 export_brief.py path/to/brief.md [--outdir DIR] [--formats pdf,docx]

House style (Ecommerce Academy) — edit here if the owning org's branding changes:
"""

# --- Ecommerce Academy house style (skill-level, survives brand forks) ---
ACCENT = "#00c853"           # accents: heading rules, blockquote bar, footer rule
HIGHLIGHT = "#e8f5e9"        # pastel light green: table headers, callout fills
FONT = "Montserrat"          # default font (Montserrat .ttf files ship in scripts/fonts/)
FONT_FALLBACK = "'Helvetica Neue', Arial, sans-serif"
FOOTER_TEXT = "Created using an Ecommerce Academy framework"
# Montserrat is bundled in scripts/fonts/ and installed automatically before
# rendering, so the PDF renders in true Montserrat. To use a different font,
# swap the .ttf files in scripts/fonts/ and update FONT/FONT_FALLBACK here.
# -------------------------------------------------------------------------

import argparse, os, re, shutil, subprocess, sys, tempfile, zipfile

CSS = f"""
@page {{ size: A4 portrait; margin: 1.4cm; }}
body {{ font-family: '{FONT}', {FONT_FALLBACK}; font-size: 11px; color:#222; line-height:1.45; }}
h1 {{ font-size: 21px; color:#111; margin:0 0 4px 0; }}
h2 {{ font-size: 15px; color:#111; border-bottom:2px solid {ACCENT}; padding-bottom:3px; margin:20px 0 8px; }}
h3 {{ font-size: 13px; color:#111; margin:14px 0 4px; }}
p, li {{ font-size:11px; }}
strong {{ color:#111; }}
em {{ color:#333; }}
code {{ background:{HIGHLIGHT}; padding:0 3px; border-radius:3px; font-size:10px; }}
blockquote {{ border-left:3px solid {ACCENT}; margin:8px 0; padding:2px 12px; color:#555; background:{HIGHLIGHT}; }}
table {{ width:100%; border-collapse:collapse; table-layout:fixed; font-size:8.5px; margin:8px 0; }}
th,td {{ border:1px solid #bbb; padding:3px 5px; vertical-align:top; word-wrap:break-word; overflow-wrap:anywhere; text-align:left; }}
th {{ background:{HIGHLIGHT}; font-size:8.5px; }}
hr {{ border:none; border-top:1px solid #ddd; margin:14px 0; }}
/* Calendar-grid timeline (Mon-Sun). Phase tints use the green house palette. */
table.cal {{ table-layout:fixed; font-size:7.5px; }}
table.cal th {{ background:{ACCENT}; color:#fff; text-align:center; font-size:8px; padding:3px 2px; }}
table.cal td {{ height:64px; vertical-align:top; padding:3px 4px; border:1px solid #cfcfcf; }}
table.cal td .d {{ display:block; font-weight:bold; font-size:9px; color:#111; margin-bottom:2px; }}
table.cal td.cap {{ background:#f1faf4; }}
table.cal td.ea {{ background:#e8f5e9; }}
table.cal td.launch {{ background:#c8e6c9; }}
table.cal td.sale {{ background:#f3faf5; }}
table.cal td.last {{ background:#a5d6a7; }}
table.cal td.close {{ background:#eeeeee; }}
.callegend span {{ display:inline-block; font-size:8px; padding:1px 6px; margin:0 4px 0 0; border:1px solid #cfcfcf; }}
"""

REL_NS = "http://schemas.openxmlformats.org/officeDocument/2006/relationships"
FOOTER_CT = "application/vnd.openxmlformats-officedocument.wordprocessingml.footer+xml"


def soffice(*args):
    profile = f"file://{tempfile.mkdtemp(prefix='lo_')}"
    cmd = ["soffice", "--headless", f"-env:UserInstallation={profile}", *args]
    subprocess.run(cmd, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)


def build_html(md_path, html_path):
    body = subprocess.run(
        ["pandoc", md_path, "--from", "gfm", "-t", "html5"],
        check=True, capture_output=True, text=True,
    ).stdout
    # Page breaks: LibreOffice honours an inline `page-break-before:always` but ignores
    # attempts to *cancel* a break, so we only ADD breaks — never suppress. The first two
    # sections (checklist + offer) share page one with the title; every section after that
    # starts a fresh page.
    LEAD_SECTIONS = 2
    _seen = {"n": 0}
    def _brk(m):
        _seen["n"] += 1
        if _seen["n"] <= LEAD_SECTIONS:
            return m.group(0)
        return "<h2 style='page-break-before:always' "
    body = re.sub(r"<h2 ", _brk, body)
    # Drop the markdown "---" section dividers: page breaks now separate sections, and a
    # stray <hr> next to a forced break strands itself on an otherwise-blank page.
    body = re.sub(r"<hr\s*/?>", "", body)
    # Resolve relative <img src> to absolute paths so LibreOffice embeds them.
    md_dir = os.path.dirname(os.path.abspath(md_path))
    def _abs(m):
        src = m.group(2)
        if src.startswith(("http://", "https://", "/", "data:")):
            return m.group(0)
        return f'{m.group(1)}{os.path.join(md_dir, src)}"'
    body = re.sub(r'(<img[^>]+src=")([^"]+)"', _abs, body)
    # Constrain images to the page width. LibreOffice ignores CSS width on images but
    # honours pixel width/height attributes, so set them from the real image dimensions.
    PAGE_W = 680  # ~18cm of A4 content at 96dpi
    def _size(m):
        tag, src = m.group(0), m.group(1)
        if tag.lower().find("width=") != -1 or not os.path.isfile(src):
            return tag
        try:
            from PIL import Image
            w, h = Image.open(src).size
        except Exception:
            return tag
        tw = min(PAGE_W, w)
        th = round(tw * h / w)
        return tag[:-1] + f' width="{tw}" height="{th}">'
    body = re.sub(r'<img[^>]+src="([^"]+)"[^>]*>', _size, body)
    with open(html_path, "w") as f:
        f.write(f"<!DOCTYPE html><html><head><meta charset='utf-8'>"
                f"<style>{CSS}</style></head><body>{body}</body></html>")


def install_bundled_fonts():
    """Install any .ttf/.otf in scripts/fonts/ so LibreOffice renders them in the PDF."""
    font_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "fonts")
    files = []
    if os.path.isdir(font_dir):
        for ext in ("*.ttf", "*.otf"):
            files += __import__("glob").glob(os.path.join(font_dir, ext))
    if not files:
        return
    dest = os.path.expanduser("~/.fonts")
    os.makedirs(dest, exist_ok=True)
    for f in files:
        shutil.copy(f, dest)
    subprocess.run(["fc-cache", "-f", dest], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)


def footer_xml():
    rpr = (f"<w:rPr><w:rFonts w:ascii='{FONT}' w:hAnsi='{FONT}'/>"
           f"<w:color w:val='808080'/><w:sz w:val='15'/></w:rPr>")
    return (
        "<?xml version='1.0' encoding='UTF-8' standalone='yes'?>"
        "<w:ftr xmlns:w='http://schemas.openxmlformats.org/wordprocessingml/2006/main' "
        f"xmlns:r='{REL_NS}'>"
        "<w:p><w:pPr>"
        f"<w:pBdr><w:top w:val='single' w:sz='6' w:space='4' w:color='{ACCENT.lstrip('#').upper()}'/></w:pBdr>"
        "<w:jc w:val='center'/>" + rpr + "</w:pPr>"
        f"<w:r>{rpr}<w:t xml:space='preserve'>{FOOTER_TEXT}     Page </w:t></w:r>"
        f"<w:r>{rpr}<w:fldChar w:fldCharType='begin'/></w:r>"
        f"<w:r>{rpr}<w:instrText xml:space='preserve'> PAGE </w:instrText></w:r>"
        f"<w:r>{rpr}<w:fldChar w:fldCharType='end'/></w:r>"
        "</w:p></w:ftr>"
    )


def inject_footer(src_docx, out_docx):
    """Add a repeating footer (attribution + page number) to every page."""
    zin = zipfile.ZipFile(src_docx, "r")
    items = {n: zin.read(n) for n in zin.namelist()}
    zin.close()

    # 1) document.xml: ensure xmlns:r, add footerReference, give the footer room
    doc = items["word/document.xml"].decode("utf-8")
    if "xmlns:r=" not in doc:
        doc = doc.replace("<w:document ", f"<w:document xmlns:r='{REL_NS}' ", 1)
    doc = re.sub(r"(<w:sectPr[^>]*>)",
                 r"\1<w:footerReference w:type='default' r:id='rIdFtr1'/>", doc, count=1)
    # widen bottom margin + footer distance so the footer is visible
    doc = re.sub(r'w:footer="\d+"', 'w:footer="397"', doc)
    doc = re.sub(r'w:bottom="\d+"', 'w:bottom="1134"', doc)
    items["word/document.xml"] = doc.encode("utf-8")

    # 2) relationships
    rels = items["word/_rels/document.xml.rels"].decode("utf-8")
    rels = rels.replace("</Relationships>",
        f"<Relationship Id='rIdFtr1' Type='{REL_NS}/footer' Target='footer1.xml'/></Relationships>")
    items["word/_rels/document.xml.rels"] = rels.encode("utf-8")

    # 3) content types
    ct = items["[Content_Types].xml"].decode("utf-8")
    ct = ct.replace("</Types>",
        f"<Override PartName='/word/footer1.xml' ContentType='{FOOTER_CT}'/></Types>")
    items["[Content_Types].xml"] = ct.encode("utf-8")

    # 4) the footer part
    items["word/footer1.xml"] = footer_xml().encode("utf-8")

    with zipfile.ZipFile(out_docx, "w", zipfile.ZIP_DEFLATED) as zout:
        for name, data in items.items():
            zout.writestr(name, data)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("md")
    ap.add_argument("--outdir")
    ap.add_argument("--formats", default="pdf,docx")
    a = ap.parse_args()

    md = os.path.abspath(a.md)
    outdir = os.path.abspath(a.outdir) if a.outdir else os.path.dirname(md)
    base = os.path.splitext(os.path.basename(md))[0]
    formats = {x.strip() for x in a.formats.split(",")}
    tmp = tempfile.mkdtemp(prefix="export_")

    install_bundled_fonts()
    html = os.path.join(tmp, "brief.html")
    build_html(md, html)

    # HTML -> docx (LibreOffice keeps the fixed table layout), then add the footer
    soffice("--convert-to", "docx:MS Word 2007 XML", "--outdir", tmp, html)
    raw_docx = os.path.join(tmp, "brief.docx")
    final_docx = os.path.join(tmp, f"{base}.docx")
    inject_footer(raw_docx, final_docx)

    made = []
    if "docx" in formats:
        dest = os.path.join(outdir, f"{base}.docx")
        shutil.copy(final_docx, dest); made.append(dest)
    if "pdf" in formats:
        soffice("--convert-to", "pdf", "--outdir", tmp, final_docx)
        dest = os.path.join(outdir, f"{base}.pdf")
        shutil.copy(os.path.join(tmp, f"{base}.pdf"), dest); made.append(dest)

    shutil.rmtree(tmp, ignore_errors=True)
    for m in made:
        print("wrote", m)


if __name__ == "__main__":
    main()
