# Where to get the order export

The skill needs one order-history file, as many months as possible (at least 12 is ideal, because the 180 day window excludes the most recent six months of new customers; gifting stores use a 365 day window and need about 18 months).

| Platform | Where | Customer ID | Date | Product | Revenue | Order ID | Line price / qty | Status | Discount |
|---|---|---|---|---|---|---|---|---|---|
| Shopify | Admin > Orders > Export > All orders, "CSV for Excel" (line items included) | Email | Created at | Lineitem name | Total | Name | Lineitem price / Lineitem quantity | Financial Status | Discount Code |
| WooCommerce | WooCommerce > Orders > Export (or an order export plugin), line-item rows | Customer ID or Billing Email | Order Date | Item Name | Order Total | Order ID | Item Cost / Quantity | Order Status | Coupon code (plugin dependent) |
| BigCommerce | Orders > Export, line-item template | Customer ID or Email | Order Date | Product Name | Order Total | Order ID | Product Unit Price / Quantity | Order Status | Coupon Code |
| Amazon | Seller Central > Reports > Fulfilment or Order reports | buyer ID if available (Amazon often hides buyer identity, so repeat analysis may not be possible) | purchase-date | product-name | item-price | amazon-order-id | item-price / quantity-purchased | order-status | promotion-ids |
| Any CSV | Any file with those four fields | | | | | | | | |

Column names vary by export version. Always confirm the mapping with the member before running.

## Privacy
Remove names, street addresses, phone numbers and payment details before uploading. **Keep the customer identifier.** Either leave the email column in place or replace it with a hashed or anonymous ID (the same customer must always get the same ID). Deleting it makes repeat purchases invisible.

## Shopify quirks the script already handles
- Each line item is its own row. The order Total and Financial Status only appear on the first row of each order, so revenue is taken per order ID and the status is spread across the whole order.
- Dates include a timezone offset. The store's local date is kept.


## If there is no order total column

A Shopify line item export has one row per product and **no order total column**. That is
normal and not a problem: pass `--line-price` (and `--line-qty` if the export has one) and
the order total is derived by summing the line values within each order.

`--revenue` is only needed when the export genuinely has an order total column. Where both
exist, the explicit column wins. Either way `RESULT_JSON.revenue_source` records which was
used, so the provenance is visible in the output.
