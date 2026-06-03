# Bundled fonts

**Montserrat ships with this skill** (the `.ttf` files in this folder, weights 400/500/600/700 + italics). The export script (`../export_brief.py`) installs them into the font cache before rendering, so the **PDF** comes out in true Montserrat and the `.docx` names Montserrat too.

Montserrat is licensed under the SIL Open Font License (OFL), which permits bundling and redistribution. Source: https://fonts.google.com/specimen/Montserrat (also published as the npm package `@expo-google-fonts/montserrat`, which is how these were obtained).

To change the document font for a fork: replace these `.ttf` files with the new family's files and update `FONT`/`FONT_FALLBACK` at the top of `../export_brief.py`. Any `.ttf`/`.otf` placed here is picked up automatically — no code change needed.
