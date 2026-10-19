#!/usr/bin/env python3
"""Flatten Shopify order data into the CSV that hero_product.py reads.

Accepts either:
  --pages DIR    a folder of page_*.json files, each one graphql_query response (connector path)
  --bulk FILE    the JSONL file from a bulkOperationRunQuery export (bulk path)

Always pass --expect-count (the ordersCount read at the start, from the SAME shop domain)
and --timezone (the shop's ianaTimezone). The script stops if the order count written
does not match, because a mismatch means orders were lost or duplicated in transit.

Output columns (fixed, so the analysis mapping never changes):
  customer_id, created_at, order_id, product, line_price, line_qty, order_total, status, discount_code
"""
import argparse
import glob
import json
import os
import sys

import pandas as pd


def money(obj):
    try:
        return float(obj["shopMoney"]["amount"])
    except (TypeError, KeyError, ValueError):
        return None


def status_of(o):
    if o.get("cancelledAt"):
        return "cancelled"
    return (o.get("displayFinancialStatus") or "").lower()


def order_rows(o, items):
    base = {
        "customer_id": (o.get("customer") or {}).get("id"),
        "created_at": o["createdAt"],
        "order_id": o["id"],
        "order_total": money(o.get("totalPriceSet")),
        "status": status_of(o),
        "discount_code": ",".join(o.get("discountCodes") or []),
        "_test": bool(o.get("test")),
    }
    if not items:
        items = [{"title": "(no line items)", "quantity": 0}]
    out = []
    for li in items:
        product = (li.get("product") or {}).get("title") or li.get("title")
        out.append({**base, "product": (product or "").strip(),
                    "line_price": money(li.get("originalUnitPriceSet")),
                    "line_qty": li.get("quantity")})
    return out


def read_pages(folder):
    rows, domains = [], set()
    files = sorted(glob.glob(os.path.join(folder, "page_*.json")),
                   key=lambda p: int(os.path.basename(p).split("_")[1].split(".")[0]))
    if not files:
        sys.exit(f"STOP: no page_*.json files in {folder}")
    for f in files:
        data = json.load(open(f))
        data = data.get("data", data)
        if "shop" in data:
            domains.add(data["shop"]["myshopifyDomain"])
        for o in data["orders"]["nodes"]:
            items = (o.get("lineItems") or {}).get("nodes", [])
            rows += order_rows(o, items)
    return rows, domains


def read_bulk(path):
    orders, items = {}, {}
    with open(path) as fh:
        for line in fh:
            if not line.strip():
                continue
            r = json.loads(line)
            if "__parentId" in r:
                items.setdefault(r["__parentId"], []).append(r)
            elif r.get("id", "").startswith("gid://shopify/Order/"):
                orders[r["id"]] = r
    rows = []
    for oid, o in orders.items():
        rows += order_rows(o, items.get(oid, []))
    return rows, set()


def main():
    p = argparse.ArgumentParser()
    g = p.add_mutually_exclusive_group(required=True)
    g.add_argument("--pages")
    g.add_argument("--bulk")
    p.add_argument("--expect-count", type=int, required=True)
    p.add_argument("--timezone", required=True)
    p.add_argument("--domain", help="expected myshopifyDomain; every page must match")
    p.add_argument("--out", default="orders_flat.csv")
    a = p.parse_args()

    rows, domains = read_pages(a.pages) if a.pages else read_bulk(a.bulk)
    if a.domain and domains and domains != {a.domain}:
        sys.exit(f"STOP: pages came from more than one store {sorted(domains)}; expected {a.domain}. Discard and re-pull.")

    df = pd.DataFrame(rows)
    got = df["order_id"].nunique()
    if got != a.expect_count:
        sys.exit(f"STOP: {got} orders written but Shopify reported {a.expect_count}. Data lost or duplicated; do not analyse.")

    n_test = df.loc[df["_test"], "order_id"].nunique()
    df = df[~df["_test"]].drop(columns="_test")
    n_guest = df.loc[df["customer_id"].isna(), "order_id"].nunique()

    # UTC -> the store's local wall-clock time
    ts = pd.to_datetime(df["created_at"], utc=True).dt.tz_convert(a.timezone).dt.tz_localize(None)
    df["created_at"] = ts.dt.strftime("%Y-%m-%d %H:%M:%S")

    df.to_csv(a.out, index=False)
    print(json.dumps({
        "orders_written": got, "matches_expected": True,
        "test_orders_removed": int(n_test),
        "guest_orders_no_customer_id": int(n_guest),
        "date_range_local": f"{ts.min().date()} to {ts.max().date()}",
        "distinct_products": int(df["product"].nunique()),
        "out": a.out,
    }, indent=2))


if __name__ == "__main__":
    main()
