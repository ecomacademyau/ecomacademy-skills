# Shopify connector queries

All queries are validated against the Admin GraphQL schema. Use them exactly as written. Validate again with `validate_graphql_codeblocks` if Shopify reports a schema error.

`CUTOFF` is a frozen snapshot time, set once at the start of the run as the current time in UTC, for example `created_at:<='2026-09-23T00:00:00Z'`. Use the same value in every query in the run, so that the count and the pull cover exactly the same orders even if new orders arrive mid-pull.

## 1. Store check (run first)

```graphql
query($cutoff: String!) {
  shop { name myshopifyDomain ianaTimezone }
  ordersCount(query: $cutoff, limit: null) { count precision }
}
```
Variables: `{"cutoff": "created_at:<='CUTOFF'"}`

Record `myshopifyDomain`, `ianaTimezone` and `count`, then show the store name to the member and confirm it's the right store. **The connector can switch stores between calls without warning.** This was observed in testing, when one call answered from one store and the next call answered from another. Every later step re-checks the domain.

## 2. Chat path: paginated pull (≤ about 300 orders)

```graphql
query($first: Int!, $after: String, $cutoff: String!) {
  shop { myshopifyDomain }
  orders(first: $first, after: $after, sortKey: CREATED_AT, query: $cutoff) {
    pageInfo { hasNextPage endCursor }
    nodes {
      id createdAt cancelledAt test displayFinancialStatus discountCodes
      customer { id }
      totalPriceSet { shopMoney { amount } }
      lineItems(first: 20) { nodes { title quantity product { title } originalUnitPriceSet { shopMoney { amount } } } }
    }
  }
}
```
Variables: `{"first": 50, "cutoff": "created_at:<='CUTOFF'"}`, then add `"after": "<endCursor>"` for each next page. Pass `first: 50` as the tool parameter too.

- Save each response **verbatim** as `/home/claude/pages/page_N.json` (N = 1, 2, 3 ...). Copy it exactly; do not summarise, reformat or drop fields.
- If a page's `myshopifyDomain` differs from step 1, stop, discard all pages and tell the member the connector switched stores.
- If Shopify returns a query cost or throttling error, retry that page with `first: 25`.
- Continue until `hasNextPage` is false.

## 3. Bulk path: any size (Cowork or Claude Code only)

Start the export (the host will ask the member to confirm; this is read-only data export, nothing in the store changes):

```graphql
mutation {
  bulkOperationRunQuery(query: """
  { orders(query: "created_at:<='CUTOFF'") { edges { node {
      id createdAt cancelledAt test displayFinancialStatus discountCodes
      customer { id }
      totalPriceSet { shopMoney { amount } }
      lineItems { edges { node { title quantity product { title } originalUnitPriceSet { shopMoney { amount } } } } }
  } } } }
  """) { bulkOperation { id status } userErrors { field message } }
}
```

Poll every 20 to 30 seconds until `status` is `COMPLETED` (large stores can take several minutes):

```graphql
query($id: ID!) {
  shop { myshopifyDomain }
  bulkOperation(id: $id) { id status errorCode objectCount url }
}
```

Then download in bash: `curl -sSfL "<url>" -o /home/claude/orders.jsonl`. The URL expires, so download promptly. `objectCount` includes line items, so never use it as the order count; the order count comes from step 1.

If `curl` cannot reach the URL (plain claude.ai chat blocks it), the bulk path is not available here. Fall back to the CSV export.

## 4. Convert, then analyse

```bash
python scripts/shopify_to_csv.py --pages /home/claude/pages   # or --bulk /home/claude/orders.jsonl
    --expect-count <count from step 1> --timezone <ianaTimezone> --domain <myshopifyDomain> --out orders_flat.csv
```

The converter stops if the order count or store domain doesn't match. It removes test orders, converts times to the store's local time and writes a fixed set of columns. The analysis mapping is then always:

```
--customer customer_id --date created_at --product product --revenue order_total
--order-id order_id --line-price line_price --line-qty line_qty --status status --discount discount_code
```
