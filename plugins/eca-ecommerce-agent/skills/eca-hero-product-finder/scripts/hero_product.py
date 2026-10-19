#!/usr/bin/env python3
"""Hero product analysis. Every number in the finding comes from this script.

The script picks the hero PRODUCT (what to acquire customers on). It does not design the
OFFER (price, bundle, deal, guarantee); it only reports the order signals that inform it.

Modes:
  --inspect   print row count, columns, first 3 rows, product names and a guessed mapping
  (default)   run the analysis with a confirmed mapping

Routes (--store-type):
  repeat    customers rebuy. Rank on repeat rate with a confidence floor, then check the ROAS floor.
  onetime   most customers buy once (ebikes, furniture). Rank on first order profit.
  gifting   buyer is not the user, repeats are yearly. Rank on first order profit, 365 day window.
  auto      not sure: classify from the store wide repeat rate.

Example:
  python hero_product.py orders_flat.csv --customer customer_id --date created_at \
      --product product --revenue order_total --order-id order_id --line-price line_price \
      --line-qty line_qty --status status --discount discount_code \
      --store-type repeat --breakeven-roas 1.67 --breakeven-cpa 48 --cpa 45
"""
import argparse
import json
import sys

import pandas as pd

MIN_N = 100             # repeat gate: minimum first time customers
MIN_N_PROFIT = 30       # profit route: minimum first time customers to count as proven to sell
VOLUME_SHARE = 0.10     # gate: share of the best seller's first time customer count
SMALL_STORE = 100       # fewer first time customers than this in total: starting product fallback
LOW_REPEAT = 10.0       # store wide repeat rate (%) under this reads as a low repeat store
STRONG_REPEAT = 20.0    # at or above this reads as a repeat store
CLOSE_TO_FLOOR = 0.80   # first order profit at 80% or more of CPA counts as "close"
EXCLUDE_STATUS = ("refund", "cancel", "void", "voided", "chargeback")

GUESS = {
    "customer": ["customer_id", "customer id", "email", "customer email", "buyer", "customer"],
    "date": ["created_at", "created at", "order date", "date", "paid at", "purchase date"],
    "product": ["product", "lineitem name", "product name", "item", "title", "sku"],
    "revenue": ["order_total", "total", "order total", "revenue", "amount", "subtotal"],
    "order_id": ["order_id", "name", "order id", "order number", "id"],
    "line_price": ["line_price", "lineitem price", "item price", "price"],
    "line_qty": ["line_qty", "lineitem quantity", "quantity", "qty"],
    "status": ["status", "financial status", "order status"],
    "discount": ["discount_code", "discount code", "coupon", "coupon code"],
}


def wilson_lcb(k, n, z=1.96):
    if n == 0:
        return 0.0
    p = k / n
    d = 1 + z * z / n
    centre = (p + z * z / (2 * n)) / d
    margin = (z / d) * ((p * (1 - p) / n + z * z / (4 * n * n)) ** 0.5)
    return max(0.0, centre - margin)


def sample_note(n):
    if n < 30:
        return "THIN"
    if n < 100:
        return "LIMITED"
    return "SOLID"


def pct(x):
    """Accept 60, 60% or 0.6 and return a fraction."""
    if x is None:
        return None
    x = float(str(x).strip().rstrip("%"))
    return x / 100 if x > 1 else x


def inspect(df):
    print(f"Rows: {len(df)}")
    print(f"Columns: {list(df.columns)}")
    lower = {c.lower().strip(): c for c in df.columns}
    mapping = {f: next((lower[o] for o in opts if o in lower), None) for f, opts in GUESS.items()}
    pcol = mapping.get("product")
    if pcol:
        print("Product names (check for the same product under different names):")
        print(df[pcol].astype(str).str.strip().value_counts().to_string())
    print("First 3 rows:")
    print(df.head(3).to_string())
    print("Guessed mapping (confirm with the member before running):")
    print(json.dumps(mapping, indent=2))


def floor_status(profit, cpa):
    if cpa is None or profit is None:
        return "not checked"
    if profit >= cpa:
        return "covers"
    if profit >= CLOSE_TO_FLOOR * cpa:
        return "close"
    return "short"


def prep(df, a, out):
    # revenue is optional: without it the order total is derived from line price.
    need = [c for c in [a.customer, a.date, a.product, a.revenue] if c]
    if a.line_price:
        need.append(a.line_price)
    missing = [c for c in need if c not in df.columns]
    if missing:
        sys.exit(f"STOP: columns not found: {missing}")
    df = df.copy()
    parsed = pd.to_datetime(df[a.date], errors="coerce", format="mixed")
    if isinstance(parsed.dtype, pd.DatetimeTZDtype):
        parsed = parsed.dt.tz_localize(None)
    elif parsed.dtype == object:
        parsed = pd.to_datetime(df[a.date], errors="coerce", utc=True, format="mixed").dt.tz_localize(None)
        out["notes"].append("Mixed timezone offsets in dates: normalised to UTC.")
    df["_date"] = parsed
    fail = df["_date"].isna().mean()
    out["date_parse_fail_pct"] = round(fail * 100, 3)
    if fail > 0.01:
        sys.exit(f"STOP: {fail:.2%} of dates failed to parse (limit 1%).")
    df = df[df["_date"].notna()]
    df["_day"] = df["_date"].dt.normalize()

    if a.status and a.status in df.columns:
        s = df[a.status].astype(str).str.lower()
        bad = s.str.contains("|".join(EXCLUDE_STATUS), na=False) & ~s.str.contains("partial", na=False)
        if a.order_id and a.order_id in df.columns:
            bad = df[a.order_id].isin(set(df.loc[bad, a.order_id]))
        out["excluded_rows_status"] = int(bad.sum())
        df = df[~bad]
    else:
        out["notes"].append("No status column: refunds and cancellations could not be excluded.")

    df = df[df[a.customer].notna() & (df[a.customer].astype(str).str.strip() != "")]
    df["_cust"] = df[a.customer].astype(str).str.strip().str.lower()
    df[a.product] = df[a.product].astype(str).str.strip()
    if a.aliases:
        amap = json.load(open(a.aliases))
        df[a.product] = df[a.product].replace(amap)
        out["aliases_applied"] = amap
    if a.revenue and a.revenue in df.columns:
        df["_rev"] = pd.to_numeric(df[a.revenue], errors="coerce")
        out["revenue_source"] = "order total column: " + a.revenue
    else:
        # A line item export has no order total column, but the total is derivable:
        # sum the line values within each order. _rev must carry the order total on
        # every row of that order, because build() takes max per order id.
        qty0 = (pd.to_numeric(df[a.line_qty], errors="coerce").fillna(1)
                if (a.line_qty and a.line_qty in df.columns) else 1)
        lv = pd.to_numeric(df[a.line_price], errors="coerce").fillna(0) * qty0
        if a.order_id and a.order_id in df.columns:
            df["_rev"] = lv.groupby(df[a.order_id]).transform("sum")
            out["revenue_source"] = "derived: sum of line price x quantity per order"
        else:
            df["_rev"] = lv
            out["revenue_source"] = "derived: line price x quantity, no order id to group by"
    if a.discount and a.discount in df.columns:
        d = df[a.discount].fillna("").astype(str).str.strip()
        df["_disc"] = d.ne("") & d.str.lower().ne("nan") & d.str.lower().ne("none")
    else:
        df["_disc"] = False
    if a.line_price and a.line_price in df.columns:
        qty = pd.to_numeric(df[a.line_qty], errors="coerce").fillna(1) if (a.line_qty and a.line_qty in df.columns) else 1
        df["_lineval"] = pd.to_numeric(df[a.line_price], errors="coerce").fillna(0) * qty
        df["_qty"] = qty
        out["multi_product_credit_rule"] = "highest revenue line item (ties by product name)"
    else:
        df["_lineval"] = 0.0
        df["_qty"] = 1
        out["multi_product_credit_rule"] = "no line item price, fell back to product name order"
    return df


def build(df, a, out, window):
    if a.order_id and a.order_id in df.columns:
        orders = (df.groupby(a.order_id)
                    .agg(cust=("_cust", "first"), day=("_day", "min"), rev=("_rev", "max"),
                         disc=("_disc", "max"), lines=("_qty", "sum"))
                    .reset_index())
    else:
        out["notes"].append("No order ID: each row treated as one order; line item exports may double count revenue.")
        orders = df.rename(columns={"_cust": "cust", "_day": "day", "_rev": "rev", "_disc": "disc", "_qty": "lines"})[["cust", "day", "rev", "disc", "lines"]].copy()
    orders["rev"] = orders["rev"].fillna(0)

    first_day = orders.groupby("cust")["day"].min().rename("first_day")
    data_start, data_end = orders["day"].min(), orders["day"].max()
    out["date_range"] = f"{data_start.date()} to {data_end.date()}"
    out["history_days"] = int((data_end - data_start).days)

    rows = df.merge(first_day, left_on="_cust", right_index=True)
    fr = rows[rows["_day"] == rows["first_day"]].copy()
    fr["_prod"] = fr[a.product]
    n_prod = fr.groupby("_cust")["_prod"].nunique()
    out["multi_product_first_orders"] = int((n_prod > 1).sum())
    fr = fr.sort_values(["_cust", "_lineval", "_prod"], ascending=[True, False, True])
    entry = fr.groupby("_cust")["_prod"].first().rename("entry")

    fo = orders.merge(first_day, left_on="cust", right_index=True)
    fo = fo[fo["day"] == fo["first_day"]]
    first_rev = fo.groupby("cust")["rev"].sum().rename("first_rev")
    first_disc = fo.groupby("cust")["disc"].max().rename("first_disc")
    first_lines = fo.groupby("cust")["lines"].sum().rename("first_lines")

    cust = pd.concat([first_day, entry, first_rev, first_disc, first_lines], axis=1)
    cust.index.name = "cust"
    cust = cust.reset_index()
    cust["first_month"] = cust["first_day"].dt.month

    cutoff = data_end - pd.Timedelta(days=window)
    cust["in_cohort"] = cust["first_day"] <= cutoff
    o = orders.merge(cust[["cust", "first_day"]], on="cust")
    later = o[(o["day"] > o["first_day"]) & (o["day"] <= o["first_day"] + pd.Timedelta(days=window))]
    cust["returned"] = cust["cust"].isin(set(later["cust"]))
    cust["ret_rev"] = cust["cust"].map(later.groupby("cust")["rev"].sum()).fillna(0)
    out["window_days"] = window
    out["cohort_cutoff"] = str(cutoff.date())
    return cust


def margin_for(product, a, margins):
    if margins and product in margins:
        return pct(margins[product])
    return pct(a.margin)


def run(df, a):
    out = {"notes": []}
    margins = json.load(open(a.margins)) if a.margins else None
    cpa = a.cpa
    df = prep(df, a, out)

    declared = a.store_type
    window = a.window or (365 if declared == "gifting" else 180)
    cust = build(df, a, out, window)
    coh = cust[cust["in_cohort"]]

    # Margin: per product file > store margin > from Ecom OS break even ROAS > from break even CPA
    store_aov = cust["first_rev"].mean()
    out["store_first_order_aov"] = round(store_aov, 2)
    if a.margin is not None:
        out["margin_source"] = "store margin given"
    elif a.breakeven_roas:
        a.margin = 1 / a.breakeven_roas
        out["margin_source"] = f"from break even ROAS {a.breakeven_roas} (margin = 1 / break even ROAS)"
    elif a.breakeven_cpa:
        a.margin = a.breakeven_cpa / store_aov
        out["margin_source"] = f"from break even CPA {a.breakeven_cpa} / store first order value {round(store_aov, 2)}"
    elif margins:
        out["margin_source"] = "per product margins only"
    else:
        out["margin_source"] = "none"
    if a.breakeven_roas and a.breakeven_cpa:
        m1, m2 = 1 / a.breakeven_roas, a.breakeven_cpa / store_aov
        if abs(m1 - m2) / max(m1, m2) > 0.2:
            out["notes"].append(f"Break even ROAS implies a {m1:.0%} margin but break even CPA implies {m2:.0%} on this data's first order value. The Ecom OS may use a different order value or period; the ROAS based margin was used.")
    store_margin = pct(a.margin)
    if a.breakeven_cpa:
        out["store_breakeven_cpa"] = a.breakeven_cpa

    # Store wide repeat rate and the data check against the declared type
    out["customers_total"] = int(len(cust))
    out["customers_in_cohort"] = int(len(coh))
    out["customers_excluded_too_recent"] = int(len(cust) - len(coh))
    sw = round(coh["returned"].mean() * 100, 1) if len(coh) else None
    out["store_repeat_rate_pct"] = sw
    if sw is None:
        observed = "unknown (history shorter than the window)"
    elif sw < LOW_REPEAT:
        observed = "low repeat"
    elif sw < STRONG_REPEAT:
        observed = "moderate repeat"
    else:
        observed = "repeat"
    out["observed_pattern"] = observed
    route = declared
    if declared == "auto":
        route = "repeat" if (sw is not None and sw >= LOW_REPEAT) else "onetime"
        out["notes"].append(f"Store type not declared: classified as {route} from a {sw}% store wide repeat rate.")
    if declared == "repeat" and sw is not None and sw < LOW_REPEAT:
        out["type_conflict"] = f"Declared a repeat store, but only {sw}% of customers bought again within {window} days."
    if declared in ("onetime", "gifting") and sw is not None and sw >= STRONG_REPEAT:
        out["type_conflict"] = f"Declared {declared}, but {sw}% of customers bought again within {window} days. The repeat route may suit this store better."
    out["store_type_declared"] = declared
    out["route"] = route

    # Per entry product table, always on ALL customers for first order economics,
    # and on the fair time cohort for repeat numbers
    def econ(g):
        n = len(g)
        m = margin_for(g.name, a, margins)
        aov = g["first_rev"].mean()
        gp = aov * m if m is not None else None
        return pd.Series({
            "first_time_all": n,
            "first_order_aov": round(aov, 2),
            "margin_pct": round(m * 100, 1) if m is not None else None,
            "first_order_profit": round(gp, 2) if gp is not None else None,
            "breakeven_cpa": round(gp, 2) if gp is not None else None,
            "breakeven_roas": round(1 / m, 2) if m else None,
            "profit_after_cpa": round(gp - cpa, 2) if (gp is not None and cpa is not None) else None,
            "floor": floor_status(gp, cpa),
            "multi_item_first_pct": round((g["first_lines"] > 1).mean() * 100, 1),
            "discounted_first_pct": round(g["first_disc"].mean() * 100, 1),
        })
    e = cust.groupby("entry").apply(econ, include_groups=False)
    r = (coh.groupby("entry")
            .agg(first_time=("cust", "size"), returned=("returned", "sum"), returning_revenue=("ret_rev", "sum"))
            if len(coh) else pd.DataFrame(columns=["first_time", "returned", "returning_revenue"]))
    t = e.join(r, how="left").reset_index().rename(columns={"index": "entry"})
    t[["first_time", "returned", "returning_revenue"]] = t[["first_time", "returned", "returning_revenue"]].fillna(0)
    t["first_time"] = t["first_time"].astype(int)
    t["returned"] = t["returned"].astype(int)
    t["repeat_rate_pct"] = [round(k / n * 100, 1) if n else None for k, n in zip(t["returned"], t["first_time"])]
    t["wilson_lcb_pct"] = [round(wilson_lcb(k, n) * 100, 1) for k, n in zip(t["returned"], t["first_time"])]
    t["sample"] = t["first_time"].map(sample_note)
    t["returning_revenue"] = t["returning_revenue"].round(2)
    # Repeat profit per first time customer (cohort)
    rp = []
    for _, x in t.iterrows():
        m = margin_for(x["entry"], a, margins)
        rp.append(round(x["returning_revenue"] / x["first_time"] * m, 2) if (m is not None and x["first_time"]) else None)
    t["repeat_profit_per_customer"] = rp
    t = t.sort_values("first_time_all", ascending=False).reset_index(drop=True)

    best = t.iloc[0]
    out["bestseller"] = {"product": best["entry"], "first_time_all": int(best["first_time_all"]),
                         "definition": "product with the most first time customers"}
    if store_margin:
        out["break_even_roas"] = round(1 / store_margin, 2)
        out["margin_used_pct"] = round(store_margin * 100, 1)
    if cpa is not None:
        out["cpa"] = cpa
    if store_margin is None and not margins:
        out["notes"].append("No break even numbers or margin given: break even checks skipped. Result ranks on first order value only.")

    total_first = int(t["first_time_all"].sum())
    out["first_time_customers_all"] = total_first

    # Offer signals: discounted first orders vs full price first orders (repeat, cohort only)
    if a.discount and len(coh) and coh["first_disc"].any() and (~coh["first_disc"]).any():
        dsc, full = coh[coh["first_disc"]], coh[~coh["first_disc"]]
        out["offer_signal_discount"] = {
            "discounted_first_orders": int(len(dsc)), "discounted_repeat_pct": round(dsc["returned"].mean() * 100, 1),
            "full_price_first_orders": int(len(full)), "full_price_repeat_pct": round(full["returned"].mean() * 100, 1)}
    if route == "gifting" or declared == "gifting":
        months = cust["first_month"].value_counts(normalize=True).sort_index()
        out["first_orders_by_month_pct"] = {int(k): round(v * 100, 1) for k, v in months.items()}

    # ROUTE: small store fallback applies to every route
    def starting_product(reason):
        s = best
        out["status"] = "STARTING PRODUCT"
        out["recommended"] = {"product": s["entry"], "reason": reason,
                              "first_time_all": int(s["first_time_all"]), "first_order_aov": float(s["first_order_aov"]),
                              "first_order_profit": s["first_order_profit"], "floor": s["floor"]}

    vol_floor = VOLUME_SHARE * best["first_time_all"]
    out["gates"] = {"volume_floor": round(vol_floor, 1), "min_n_repeat": MIN_N, "min_n_profit": MIN_N_PROFIT}

    if total_first < SMALL_STORE:
        starting_product(f"Fewer than {SMALL_STORE} first time customers in total: not enough data to pick a proven hero. Start with the best seller.")
    elif route == "repeat":
        if len(coh) == 0:
            starting_product(f"History shorter than the {window} day window: repeat rates can't be measured yet. Start with the best seller.")
        else:
            cb = t.sort_values("first_time", ascending=False).iloc[0]
            t["gate_volume"] = t["first_time"] >= VOLUME_SHARE * cb["first_time"]
            t["gate_n"] = t["first_time"] >= MIN_N
            surv = t[t["gate_volume"] & t["gate_n"]].sort_values(["wilson_lcb_pct", "first_time"], ascending=False)
            vol = t.sort_values(["returned", "first_time"], ascending=False).iloc[0]
            out["volume_winner"] = {"product": vol["entry"], "returned": int(vol["returned"]), "first_time": int(vol["first_time"])}
            rate = t[t["first_time"] > 0].sort_values(["repeat_rate_pct", "first_time"], ascending=False).iloc[0]
            out["rate_winner"] = {"product": rate["entry"], "repeat_rate_pct": float(rate["repeat_rate_pct"]),
                                  "first_time": int(rate["first_time"]), "sample": rate["sample"]}
            if surv.empty:
                out["status"] = "NONE"
                out["recommended"] = None
                out["notes"].append("No product clears the repeat gates: not enough evidence for a repeat based hero.")
            else:
                h = surv.iloc[0]
                # Break even: first order profit (the product's break even CPA) plus repeat profit must reach the actual CPA
                with_repeat = None
                if h["first_order_profit"] is not None and cpa is not None and h["repeat_profit_per_customer"] is not None:
                    with_repeat = floor_status(h["first_order_profit"] + h["repeat_profit_per_customer"], cpa)
                rec = {"product": h["entry"], "first_time": int(h["first_time"]), "returned": int(h["returned"]),
                       "repeat_rate_pct": float(h["repeat_rate_pct"]), "wilson_lcb_pct": float(h["wilson_lcb_pct"]),
                       "first_order_aov": float(h["first_order_aov"]), "first_order_profit": h["first_order_profit"],
                       "floor_first_order": h["floor"], "floor_with_repeat": with_repeat,
                       "same_as_bestseller": h["entry"] == cb["entry"]}
                rec["ratio_vs_bestseller"] = (round(h["repeat_rate_pct"] / cb["repeat_rate_pct"], 2)
                                              if cb["repeat_rate_pct"] else None)
                rec["bestseller_in_cohort"] = cb["entry"]
                out["recommended"] = rec
                out["status"] = "HERO"
                hc = coh[coh["entry"] == h["entry"]]
                if a.discount and (hc["first_disc"].sum() >= 30) and ((~hc["first_disc"]).sum() >= 30):
                    out["offer_signal_discount_hero"] = {
                        "discounted_first_orders": int(hc["first_disc"].sum()),
                        "discounted_repeat_pct": round(hc.loc[hc["first_disc"], "returned"].mean() * 100, 1),
                        "full_price_first_orders": int((~hc["first_disc"]).sum()),
                        "full_price_repeat_pct": round(hc.loc[~hc["first_disc"], "returned"].mean() * 100, 1)}
                if h["floor"] == "short" and with_repeat in ("short", None) and cpa is not None:
                    out["status"] = "HERO, FAILS BREAK EVEN"
                    alt = surv[(surv["floor"] != "short") & (surv["entry"] != h["entry"])]
                    if not alt.empty:
                        out["floor_safe_alternative"] = {"product": alt.iloc[0]["entry"],
                                                         "repeat_rate_pct": float(alt.iloc[0]["repeat_rate_pct"]),
                                                         "first_time": int(alt.iloc[0]["first_time"]),
                                                         "floor": alt.iloc[0]["floor"]}
                ex = t[~(t["gate_volume"] & t["gate_n"]) & (t["repeat_rate_pct"].fillna(0) > h["repeat_rate_pct"])]
                out["excluded_higher_rate"] = [
                    {"product": x["entry"], "repeat_rate_pct": float(x["repeat_rate_pct"]), "first_time": int(x["first_time"]),
                     "failed": [g for g, ok in (("volume floor", x["gate_volume"]), ("100 customer minimum", x["gate_n"])) if not ok]}
                    for _, x in ex.iterrows()]
    else:
        # One time purchase and gifting: rank on first order profit among proven sellers
        key = "first_order_profit" if (store_margin is not None or margins) else "first_order_aov"
        proven = t[(t["first_time_all"] >= MIN_N_PROFIT) & (t["first_time_all"] >= vol_floor)].sort_values(key, ascending=False)
        out["ranked_on"] = key
        if proven.empty:
            starting_product("No product has enough first time customers to compare. Start with the best seller.")
        else:
            short = proven.head(3)
            out["shortlist"] = [{"product": x["entry"], "first_time_all": int(x["first_time_all"]),
                                 "first_order_aov": float(x["first_order_aov"]), "first_order_profit": x["first_order_profit"],
                                 "profit_after_cpa": x["profit_after_cpa"], "floor": x["floor"]} for _, x in short.iterrows()]
            h = short.iloc[0]
            out["recommended"] = out["shortlist"][0]
            passing = short[short["floor"].isin(["covers", "close", "not checked"])]
            out["status"] = "SHORTLIST" if not passing.empty else "SHORTLIST, ALL FAIL BREAK EVEN"
            out["test_first"] = [x for x in passing["entry"].head(2)]

    cols = ["entry", "first_time_all", "first_order_aov", "breakeven_cpa", "floor", "first_time",
            "returned", "repeat_rate_pct", "sample", "multi_item_first_pct", "discounted_first_pct"]
    out["table"] = t[cols + ["first_order_profit", "breakeven_roas", "wilson_lcb_pct", "returning_revenue", "repeat_profit_per_customer", "profit_after_cpa"]].to_dict("records")
    print(t[cols].to_string(index=False))
    print("\nRESULT_JSON")
    print(json.dumps(out, indent=2, default=str))


def main():
    p = argparse.ArgumentParser()
    p.add_argument("csv")
    p.add_argument("--inspect", action="store_true")
    for f in ["customer", "date", "product", "revenue", "order-id", "line-price", "line-qty", "status", "discount"]:
        p.add_argument(f"--{f}")
    p.add_argument("--store-type", choices=["repeat", "onetime", "gifting", "auto"], default="auto")
    p.add_argument("--margin", help="store wide gross margin after product cost, shipping and fees, e.g. 60 or 0.6")
    p.add_argument("--margins", help='JSON file of per product margins, e.g. {"Gut Health Powder": 65}')
    p.add_argument("--cpa", type=float, help="current cost per acquisition on Meta (Ads Manager), or a target")
    p.add_argument("--breakeven-roas", type=float, help="break even ROAS from the Ecom OS; margin = 1 / this")
    p.add_argument("--breakeven-cpa", type=float, help="break even CPA from the Ecom OS; used for margin if no break even ROAS")
    p.add_argument("--window", type=int, help="repeat window in days (default 180, gifting 365)")
    p.add_argument("--aliases", help='JSON file mapping old names to one name, e.g. {"PERFECTION": "PERFECTION KIT"}')
    a = p.parse_args()
    df = pd.read_csv(a.csv, low_memory=False)
    if a.inspect:
        inspect(df)
    else:
        if not all([a.customer, a.date, a.product]):
            sys.exit("STOP: --customer, --date and --product are required.")
        if not a.revenue and not a.line_price:
            sys.exit("STOP: need either --revenue (an order total column) or "
                     "--line-price (plus --line-qty if there is one), so order value "
                     "can be derived. A Shopify line item export has no order total "
                     "column, so pass the line price instead.")
        run(df, a)


if __name__ == "__main__":
    main()
