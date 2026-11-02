# Building into the theme

## 1. Duplicate the live theme — never edit it

```bash
shopify theme list --store <store>.myshopify.com
shopify theme pull --store <store>.myshopify.com --theme <live-theme-id> --path ./theme
```

Work in `./theme`. Push to a **new unpublished theme**, never to the live one. Name it so
the member can recognise it in a list six months from now: `ECA Gift Guide — Christmas`.

**Confirm the `.myshopify.com` domain with the member.** It is often not the storefront
domain, and a wrong guess either fails or, worse, succeeds against another store.

## 2. Copy the library in

```
theme-files/sections/*.liquid   ->  theme/sections/
page.eca-gift-guide.json        ->  theme/templates/
```

Copy all seven sections. They are self-contained — no snippets, no assets, no shared CSS
file — so a partial copy fails in a way the theme editor reports as a missing section
rather than anything useful.

## 3. Run the colour-scheme adapter

```bash
python3 scripts/adapt-color-schemes.py ./theme
```

Themes that predate colour schemes do not define any, and Shopify then shows a red
"color schemes must be defined" banner across the member's whole editor. The adapter
strips the setting on those themes. **Run it before every push.** Never leave that warning
on someone's screen: it reads as though the page is broken when it isn't.

## 4. Push

```bash
shopify theme push --store <store>.myshopify.com --unpublished --theme "ECA Gift Guide"
```

Note the theme id it returns — the handover links need it.

## 5. Create the page, unpublished

```graphql
pageCreate(page: {
  title: "Christmas Gift Guide",
  handle: "christmas-gift-guide",
  templateSuffix: "eca-gift-guide",
  isPublished: false,
  metafields: [
    {namespace:"global", key:"title_tag",       type:"single_line_text_field", value:"..."},
    {namespace:"global", key:"description_tag", type:"single_line_text_field", value:"..."}
  ]
})
```

`templateSuffix` is the filename without `page.` and without `.json`, so
`page.eca-gift-guide.json` is `eca-gift-guide`. Get it wrong and the page renders with the
default template and none of the guide: it looks blank, not broken, which is the most
confusing failure in this whole skill.

**No Shopify MCP?** Give the member the two-click version: Online Store → Pages → Add page,
then set the theme template to `eca-gift-guide` in the sidebar.

## 6. The three links

```
Edit the guide   https://admin.shopify.com/store/<handle>/themes/<theme_id>/editor?previewPath=%2Fpages%2Fchristmas-gift-guide
Preview it       https://<store>.myshopify.com/pages/christmas-gift-guide?preview_theme_id=<theme_id>
Page settings    https://admin.shopify.com/store/<handle>/pages/<page_id>
```

`<handle>` is the **myshopify subdomain**, not the storefront domain. A store whose
customers know it as `brandname.com` may be `brandname-co` in admin URLs, and the
storefront domain simply does not work there.

Never end a build with "the page has been created". Give the links, say what to check, and
say how to publish when they are happy.
