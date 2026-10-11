# Linking to the order

Whenever a reply, a summary or a flag mentions an order, **give the member a direct link
to it in Shopify admin**. They will almost always want to look at it, and often to change
something: add a note, edit the address, refund a line, resend the confirmation. Making
them search for an order they were just told about is a small, repeated waste.

## The URL

```
https://admin.shopify.com/store/<store-handle>/orders/<numeric-order-id>
```

### Getting the store handle right

**The handle is the myshopify subdomain, not the storefront domain.** This is the part
that goes wrong and produces a dead link that looks plausible.

```
get-shop-info returns:
  domain      acmecoffee.com              <- NOT the handle
  shopDomain  acme-coffee.myshopify.com   <- handle is "acme-coffee"
```

Take the myshopify domain and drop `.myshopify.com`. Some tools return `shopDomain` and
some return `myshopifyDomain`; either works. Store it in config at setup so it is derived
once rather than guessed every run.

### Getting the order id right

`list-orders` returns a global id. The admin URL needs only the trailing number.

```
gid://shopify/Order/8321823277261   ->   8321823277261
```

Take everything after the final `/`. Do not use the order **name** (`#1042`) in the URL;
that is a display label and the link will not resolve.

### Worked example

```
Order #1042, gid://shopify/Order/8321823277261, store acme-coffee.myshopify.com
https://admin.shopify.com/store/acme-coffee/orders/8321823277261
```

## Where the link goes

**In everything the member reads. Never in anything the customer reads.**

- Thread summaries: link the order number inline, so `#1042` is clickable.
- Flags and escalations: always, because the member is about to act on it.
- The run report: every order mentioned.
- **The draft reply itself: never.** An admin link in a customer email exposes internal
  tooling and does not work for them anyway. Customers get the tracking link or the order
  status page, not admin.

## Related links worth giving

Where the situation calls for it, and again only to the member:

| Thing | URL |
|---|---|
| Customer record | `https://admin.shopify.com/store/<handle>/customers/<numeric-id>` |
| Draft order | `https://admin.shopify.com/store/<handle>/draft_orders/<numeric-id>` |
| All unfulfilled | `https://admin.shopify.com/store/<handle>/orders?selectedView=unfulfilled` |
| Product | `https://admin.shopify.com/store/<handle>/products/<numeric-id>` |

Same two rules apply: handle from the myshopify domain, id from the tail of the gid.

## If the order cannot be found

Say so plainly rather than linking to a guess. A customer quoting an order number that
does not exist usually means they ordered under a different email, bought from a
marketplace, or mistyped it. That is useful information and it belongs in the flag.
