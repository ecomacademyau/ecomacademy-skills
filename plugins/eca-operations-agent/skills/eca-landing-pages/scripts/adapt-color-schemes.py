#!/usr/bin/env python3
"""
Adapt the ECA LP section library to the theme it's being installed into.

Shopify shows a red editor warning -- "To preview your changes, color schemes must be
defined in settings_data and settings_schema files" -- on any theme that has no
color_scheme_group. Our sections offer a Colour scheme dropdown, which is the right
control on modern themes and meaningless on older ones.

So: check the theme, and if it has no schemes, strip the color_scheme setting out of
the section files (the custom background / text pickers still work on every theme).

Usage:  python3 adapt-color-schemes.py <theme-dir>
Run it AFTER copying the section files into the theme and BEFORE `shopify theme push`.
Safe to re-run.
"""
import json, re, sys, pathlib

def main(theme_dir):
    theme = pathlib.Path(theme_dir)
    schema = theme / "config" / "settings_schema.json"
    if not schema.exists():
        sys.exit(f"No config/settings_schema.json under {theme} -- is this a theme directory?")

    has_schemes = "color_scheme_group" in schema.read_text()
    if has_schemes:
        print("Theme defines colour schemes -- leaving the Colour scheme setting in place.")
        return

    print("Theme has NO colour schemes. Removing the Colour scheme setting so the editor")
    print("doesn't warn. The Custom background / Custom text pickers still work.\n")

    changed = 0
    for f in sorted((theme / "sections").glob("eca-lp-*.liquid")):
        t = f.read_text()
        m = re.search(r"\{% schema %\}(.*?)\{% endschema %\}", t, re.S)
        if not m:
            continue
        sch = json.loads(m.group(1))
        before = len(sch.get("settings", []))
        sch["settings"] = [s for s in sch.get("settings", []) if s.get("type") != "color_scheme"]
        if len(sch["settings"]) == before:
            continue
        # the Liquid guards on `!= blank`, so a missing setting simply inherits
        t = t[:m.start()] + "{% schema %}\n" + json.dumps(sch, indent=2, ensure_ascii=False) + "\n{% endschema %}" + t[m.end():]
        f.write_text(t)
        changed += 1
        print(f"  stripped: {f.name}")

    print(f"\n{changed} section(s) adapted.")

if __name__ == "__main__":
    if len(sys.argv) != 2:
        sys.exit(__doc__)
    main(sys.argv[1])
