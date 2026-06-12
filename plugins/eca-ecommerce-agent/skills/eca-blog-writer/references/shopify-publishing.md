# Shopify Publishing

How to put the finished article into Shopify as a **draft for review** (the default). Uses the Shopify Admin GraphQL API via the connected Shopify MCP. Always `graphql_schema` → build → `validate_graphql_codeblocks` → `graphql_mutation`.

## Step 1 — Find the blog to publish into

Articles belong to a blog. List the store's blogs and match the one named in `config.md`:

```graphql
query Blogs {
  blogs(first: 20) {
    edges { node { id handle title } }
  }
}
```

Use the matching `node.id` (format `gid://shopify/Blog/123…`) as `blogId`. If config names no blog and there's more than one, ask which. Don't create a new blog unless the user asks. (To create one: `blogCreate(blog: { title: "…" })`.)

## Step 2 — The featured image

The `articleCreate` input accepts an image by URL directly:

```graphql
image: { url: "https://…/featured.jpg", altText: "descriptive, keyword-aware alt text" }
```

- If the image already lives on the store's CDN or any public URL, pass that URL.
- If you generated/edited an image locally, upload it to Shopify Files first (via `stagedUploadsCreate` → upload → `fileCreate`, or the store's media tooling) and use the resulting URL.
- Always set meaningful `altText` — it's an SEO/GEO and accessibility win.

## Step 3 — Create the article (draft by default)

`articleCreate` with `ArticleCreateInput`. Confirmed fields:

```graphql
mutation CreateArticle($article: ArticleCreateInput!) {
  articleCreate(article: $article) {
    article {
      id
      handle
      title
      isPublished
    }
    userErrors { field message }
  }
}
```

Variables:

```json
{
  "article": {
    "blogId": "gid://shopify/Blog/123456789",
    "title": "Primary-keyword-bearing title (~50–60 chars)",
    "handle": "clean-keyword-slug",
    "author": { "name": "AUTHOR FROM CONFIG" },
    "body": "<the full assembled HTML body — see assets/>",
    "summary": "<150–160 char excerpt, includes the primary keyword, reads like a promise>",
    "tags": ["topic", "category"],
    "image": { "url": "https://…/featured.jpg", "altText": "descriptive alt text" },
    "isPublished": false
  }
}
```

### Draft vs live
- **`isPublished: false`** → the article is created hidden. This is the **default** — it lets the user review and click publish. This mirrors the brand's draft-everything rule.
- Only set `isPublished: true` if the user explicitly asked to publish live now.
- To **schedule**: set `isPublished: false` (or use `publishDate` with an ISO 8601 future datetime) — `publishDate` sets when it becomes visible.

`author` is **required** and is an `AuthorInput { name }`. `title` is **required**.

## Step 4 — SEO title & meta description (metafields)

Shopify stores the SEO/meta-description override in the `global` metafield namespace. Set them so search engines and AI engines see the optimised version:

```graphql
metafields: [
  { namespace: "global", key: "title_tag",       type: "single_line_text_field", value: "SEO title ~50–60 chars" },
  { namespace: "global", key: "description_tag",  type: "multi_line_text_field",  value: "Meta description ~150–160 chars with the primary keyword" }
]
```

Include these inside the same `ArticleCreateInput` (the input accepts `metafields`). If a theme/SEO app manages meta tags differently, follow that app's field instead.

## Step 5 — Updating an existing article

Use `articleUpdate(id: $id, article: $input)` with the same input shape to edit body, fix a typo, swap the image, or flip `isPublished` to `true` when the user approves the draft.

## Step 6 — Report back

After a successful create, tell the user:
- the **admin URL** to review/publish: `https://admin.shopify.com/store/<store>/articles/<id>` (or the Blogs → article path),
- the **live URL it will have**: `https://<store-domain>/blogs/<blog-handle>/<article-handle>`,
- the **primary keyword**, the **products it links to**, and the **meta title/description** used,
- a reminder that it's a **draft** awaiting their publish click (unless they asked to go live).

## Embedding video and other media in the body

Only embed media the user approved in Phase 2.5. It all lives in the article `body` HTML.

**YouTube / Vimeo video** — use a responsive iframe wrapper so it scales on mobile:

```html
<div style="position:relative;padding-bottom:56.25%;height:0;overflow:hidden;margin:24px 0;border-radius:12px;">
  <iframe src="https://www.youtube.com/embed/VIDEO_ID" title="Descriptive video title"
    style="position:absolute;top:0;left:0;width:100%;height:100%;border:0;"
    allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture"
    allowfullscreen loading="lazy"></iframe>
</div>
```
Convert a normal YouTube watch URL (`watch?v=ID`) to the embed form (`/embed/ID`). Add a one-line caption beneath if helpful. A relevant video is also a dwell-time and engagement signal that helps SEO.

**Images supplied by the user** — upload to Shopify Files (or use a public URL) and insert with descriptive alt text and an optional caption:

```html
<figure style="margin:24px 0;">
  <img src="IMAGE_URL" alt="descriptive, keyword-aware alt text" style="width:100%;height:auto;border-radius:12px;display:block;" loading="lazy" />
  <figcaption style="font-size:13px;color:#777;margin-top:8px;text-align:center;">Optional caption</figcaption>
</figure>
```

**Other media** — infographics/comparison graphics are just images (use the figure pattern). For a downloadable (PDF etc.), upload to Shopify Files and link it. Keep every embed responsive and lazy-loaded so it doesn't slow the page (page speed affects both SEO and conversion).

## Advanced (optional): a custom article theme template

If a brand wants a distinct branded layout for these posts (different from their default article page), create a theme template `article.<suffix>.json`/`.liquid` in the theme and pass `templateSuffix: "<suffix>"` in the article input. This requires theme-file access (`themeFilesUpsert`) and theme/Liquid knowledge. Most stores don't need it — the body HTML components in `assets/` already give every post a consistent, on-brand structure that renders on any theme. Only go here if the user specifically asks for a custom article layout.

## Permissions
The Shopify connection needs content/blog write scope (`write_content`). If `articleCreate` fails with an access/permission error, tell the user which scope is missing and stop — don't retry blindly.
