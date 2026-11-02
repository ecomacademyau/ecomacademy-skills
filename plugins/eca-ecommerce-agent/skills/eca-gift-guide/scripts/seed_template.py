#!/usr/bin/env python3
"""Turn the approved worksheet answers into a seeded Shopify page template.

    python3 seed_template.py guide.json --out page.eca-gift-guide.json [--check]

The template it writes renders the guide complete on first load, while every field
stays editable in the theme editor. That is the whole point of building this as
sections: the member fixes a heading themselves instead of coming back to Claude.

Why a seeder rather than hand-written JSON: section settings ids, block types and
the order array have to agree exactly or the page renders empty with no error. Doing
that by hand once is fine; doing it per store is how typos ship.
"""
import argparse
import json
import re
import sys

LIB = "1.0.0"


def block(btype, settings):
    return {"type": btype, "settings": settings}


def seed(d, base=None):
    """base: the store's own collection template, for the collection format.

    Its section order goes in the middle untouched. Never hand-write the product
    grid section: themes disagree on its name (Dawn calls it
    main-collection-product-grid, others main-collection), and naming the wrong one
    produces a collection page with no products on it and no error anywhere.
    """
    order, sections = [], {}

    def add(key, stype, settings, blocks=None):
        order.append(key)
        s = {"type": stype, "settings": settings}
        if blocks is not None:
            s["blocks"] = {}
            s["block_order"] = []
            for i, b in enumerate(blocks):
                bid = "{}_{}".format(key, i + 1)
                s["blocks"][bid] = b
                s["block_order"].append(bid)
        sections[key] = s

    cut = d.get("cutoff") or {}
    add("settings", "eca-gg-settings", {
        "show_cutoff": bool(cut.get("banner")),
        "cutoff_text": cut.get("banner", ""),
        "sticky": bool(cut.get("sticky")),
        "cutoff_link_url": cut.get("link_url", ""),
        "cutoff_link_text": cut.get("link_text", ""),
        "color_scheme": d.get("accent_scheme", ""),
    })

    ban = d.get("banner") or {}
    add("banner", "eca-gg-banner", {
        "layout": ban.get("layout", "split"),
        "show_placeholder": True,
        "image_alt": ban.get("image_alt", ""),
        "eyebrow": ban.get("eyebrow", ""),
        "heading": ban.get("heading") or d.get("title", "Christmas Gift Guide"),
        "heading_is_h1": True,
        "body": ban.get("body") or d.get("intro", ""),
        "cta_label": ban.get("cta_label", ""),
        "cta_url": ban.get("cta_url", ""),
    })

    links = d.get("quick_links") or []
    if links:
        add("quicklinks", "eca-gg-quicklinks", {
            "heading": d.get("quick_links_heading", "Shop by who it's for"),
            "style": d.get("quick_links_style", "tiles"),
            "columns": min(max(len(links), 2), 6),
        }, [block("link", {k: v for k, v in (
            ("collection", l.get("collection", "")),
            ("label", l.get("label", "")),
            ("url", l.get("url", ""))) if v}) for l in links])

    for i, sec in enumerate([] if base is not None else d.get("sections", [])):
        gifts = []
        for it in sec.get("items", []):
            # Prefer the product handle. A picked product keeps its own title, image,
            # price and stock, so the guide stays right when the catalogue moves -
            # which it does, daily, through December. Fall back to a manual tile only
            # for something that is not a product (a collection, an external page).
            g = {"note": it.get("note", "")}
            if it.get("handle"):
                g["product"] = it["handle"]
                if it.get("title"):
                    g["title"] = it["title"]
            else:
                g["title"] = it.get("title", "")
                g["url"] = it.get("url", "")
            gifts.append(block("gift", g))
        add("grid{}".format(i + 1), "eca-gg-grid", {
            "heading": sec.get("heading", ""),
            "lead": wrap_rich(sec.get("lead", "")),
            "anchor": sec.get("anchor", ""),
            "columns": sec.get("columns", 3),
            "show_price": sec.get("show_price", True),
            "hide_sold_out": True,
            "more_url": sec.get("more_url", ""),
            "more_text": sec.get("more_text", ""),
        }, gifts)

    opts = [] if base is not None else (d.get("options") or [])
    if opts:
        add("options", "eca-gg-options", {
            "heading": d.get("options_heading", "Left it too late?"),
            "lead": wrap_rich(d.get("options_lead", "")),
            "columns": min(max(len(opts), 1), 3),
        }, [block("option", {
            "title": o.get("title", ""),
            "detail": wrap_rich(o.get("detail", "")),
            "url": o.get("url", ""),
            "cta": o.get("cta", ""),
        }) for o in opts])

    faqs = [] if base is not None else (d.get("faqs") or [])
    if faqs:
        add("faq", "eca-gg-faq", {
            "heading": d.get("faq_heading", "Christmas delivery and returns"),
            "open_first": True,
        }, [block("qa", {"q": f.get("q", ""), "a": wrap_rich(f.get("a", ""))}) for f in faqs])

    if base is not None:
        # Drop the store's own sections in, between our top and our foot.
        for key in base.get("order", []):
            if key in base.get("sections", {}):
                sections[key] = base["sections"][key]
                order.append(key)

    seo = d.get("seo_text") or {}
    parts = seo.get("parts") or []
    if parts:
        add("seo", "eca-gg-seo", {
            "heading": seo.get("heading", "About these Christmas gifts"),
            "intro": wrap_rich(seo.get("intro", "")),
            "columns": seo.get("columns", "1"),
        }, [block("part", {"heading": p.get("heading", ""), "body": wrap_rich(p.get("body", ""))})
            for p in parts])

    return {"sections": sections, "order": order}


def wrap_rich(text):
    """richtext settings must be HTML. Shopify silently drops a bare string."""
    if not text:
        return ""
    t = str(text).strip()
    if t.startswith("<"):
        return t
    paras = [p.strip() for p in re.split(r"\n\s*\n", t) if p.strip()]
    return "".join("<p>{}</p>".format(p.replace("\n", " ")) for p in paras)


def check(d, tpl, fmt="page"):
    """The failures that produce a page that looks fine and isn't."""
    problems, warnings = [], []
    secs = [] if fmt == "collection" else d.get("sections", [])

    if not (d.get("cutoff") or {}).get("banner"):
        problems.append("no cut-off line. It is the most-read thing on the page; never guess it.")
    for s in secs:
        if not s.get("items"):
            problems.append("empty gift group: " + str(s.get("heading")))
        if not s.get("more_text"):
            warnings.append("no see-all text on: " + str(s.get("heading")))
        elif re.fullmatch(r"(see all|shop now|view all|shop more)\.?", s["more_text"].strip(), re.I):
            problems.append("see-all text says only '{}'. Name the thing: 'See all gifts for latte lovers'."
                            .format(s["more_text"].strip()))
        for it in s.get("items", []):
            if not it.get("url") and not it.get("handle"):
                problems.append("gift with neither a product handle nor a link: "
                                + str(it.get("title")))

    parts = (d.get("seo_text") or {}).get("parts") or []
    if not parts:
        problems.append("no SEO text at the foot. The page has almost nothing to rank on without it.")
    else:
        words = sum(len(str(p.get("body", "")).split()) for p in parts)
        if words < 150:
            warnings.append("the SEO text is only {} words. Aim for a solid paragraph per gift group."
                            .format(words))
        covered = {str(p.get("heading", "")).strip().lower() for p in parts}
        for s in secs:
            h = str(s.get("heading", "")).strip().lower()
            if h and h not in covered:
                warnings.append("no SEO paragraph for the group: " + str(s.get("heading")))

    if not (d.get("quick_links") or []):
        warnings.append("no quick links at the top. Most people arrive knowing who they are buying for.")

    text = json.dumps(tpl).lower()
    for ph in ("{{who}}", "{{cut-off", "{{heading"):
        if ph in text:
            problems.append("a placeholder is still in the template: " + ph)

    for w in warnings:
        print("  warn " + w)
    for p in problems:
        print("  FAIL " + p)
    if not problems:
        print("  checks passed" + (" with {} warning(s)".format(len(warnings)) if warnings else ""))
    return 1 if problems else 0


def main():
    ap = argparse.ArgumentParser(description="Seed the gift guide page template.")
    ap.add_argument("guide")
    ap.add_argument("--out", default="page.eca-gift-guide.json")
    ap.add_argument("--check", action="store_true")
    ap.add_argument("--format", choices=["page", "collection"], default="page",
                    help="page = the full guide; collection = banner and SEO text "
                         "wrapped around the store's own collection template")
    ap.add_argument("--base", help="the store's templates/collection.json "
                                   "(required for --format collection)")
    a = ap.parse_args()
    with open(a.guide, encoding="utf-8") as f:
        d = json.load(f)
    base = None
    if a.format == "collection":
        if not a.base:
            print("  FAIL --format collection needs --base <theme>/templates/collection.json.\n"
                  "       The product grid section has a different name in every theme, so it is\n"
                  "       read from the store's own template rather than guessed.")
            return 1
        with open(a.base, encoding="utf-8") as f:
            base = json.load(f)
    tpl = seed(d, base)
    with open(a.out, "w", encoding="utf-8") as f:
        json.dump(tpl, f, indent=2, ensure_ascii=False)
        f.write("\n")
    gifts = sum(len(s.get("items", [])) for s in d.get("sections", []))
    if a.format == "collection":
        kept = len(base.get("order", []))
        print("Wrote {} - {} section(s), {} of them the store's own, {} SEO paragraph(s)".format(
            a.out, len(tpl["order"]), kept,
            len((d.get("seo_text") or {}).get("parts") or [])))
    else:
        print("Wrote {} - {} section(s) in order, {} gift(s), {} FAQ(s), {} SEO paragraph(s)".format(
            a.out, len(tpl["order"]), gifts, len(d.get("faqs") or []),
            len((d.get("seo_text") or {}).get("parts") or [])))
    if a.check:
        return check(d, tpl, a.format)
    return 0


if __name__ == "__main__":
    sys.exit(main())
