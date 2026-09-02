#!/usr/bin/env python3
"""
Find the store's best promotional periods across a whole year, not just BFCM.

Why this exists: a brand's most effective offer is often not the Black Friday one.
Comparing this year's BFCM plan only against last year's BFCM hides a flash sale,
an EOFY push or a bundle launch that beat it on both revenue and margin.

Two things this does that a naive "biggest week" scan does not:

1. DETRENDS. A growing business makes recent weeks look like outliers. Every period is
   compared against its own trailing baseline, not the annual average.
2. WEIGHTS BY DISCOUNT COST. A week that lifted revenue 40% on a 5% discount is a far
   better template than one that lifted 60% on 25%. Revenue alone rewards the expensive
   promotions, which is how brands end up repeating their least profitable event.

Input: JSON list of period rows, each with:
    {"period": "2026-07-20", "orders": 94, "revenue": 6711.71, "discounts": 390.40}
  discounts may be positive or negative; the sign is ignored.

Usage:
    python3 promo_outliers.py rows.json
    python3 promo_outliers.py rows.json --baseline 8 --threshold 1.25
"""
import json, sys, statistics


def analyse(rows, baseline_n=8, threshold=1.25):
    for r in rows:
        r["discounts"] = abs(float(r.get("discounts", 0) or 0))
        r["revenue"] = float(r["revenue"])
        gross = r["revenue"] + r["discounts"]
        r["discount_rate"] = r["discounts"] / gross if gross else 0.0

    out = []
    for i, r in enumerate(rows):
        window = rows[max(0, i - baseline_n):i]
        if len(window) < 3:
            continue
        base_rev = statistics.median(w["revenue"] for w in window)
        base_disc = statistics.median(w["discount_rate"] for w in window)
        if base_rev <= 0:
            continue
        lift = r["revenue"] / base_rev - 1
        extra_disc = r["discount_rate"] - base_disc
        # revenue lift per extra point of discount. High = cheap lift.
        # Guard the near-zero case so a no-discount win is not divided into nonsense.
        eff = lift / extra_disc if extra_disc > 0.005 else None
        out.append({**r, "baseline_revenue": base_rev, "lift": lift,
                    "extra_discount": extra_disc, "efficiency": eff,
                    "is_outlier": r["revenue"] >= base_rev * threshold})
    return out


def report(rows, top=8):
    a = analyse(rows)
    events = sorted([r for r in a if r["is_outlier"]], key=lambda r: -r["lift"])[:top]
    if not events:
        print("No periods exceeded the threshold. Try a lower --threshold.")
        return

    print("\nOUTLIER PERIODS (vs each period's own trailing baseline)\n")
    print("  {:<12}{:>10}{:>9}{:>10}{:>12}{:>8}".format(
        "period", "revenue", "lift", "disc rate", "extra disc", "lift/pt"))
    for r in events:
        eff = "{:.1f}x".format(r["efficiency"]) if r["efficiency"] else "  free"
        print("  {:<12}{:>10}{:>9}{:>10}{:>12}{:>8}".format(
            r["period"], "${:,.0f}".format(r["revenue"]), "{:+.0f}%".format(r["lift"] * 100),
            "{:.1f}%".format(r["discount_rate"] * 100), "{:+.1f}pt".format(r["extra_discount"] * 100), eff))

    print("\n  BEST LIFT PER DISCOUNT POINT (the template worth repeating)")
    paid = [r for r in events if r["efficiency"]]
    for r in sorted(paid, key=lambda r: -r["efficiency"])[:3]:
        print("    {}  {:+.0f}% revenue for {:+.1f}pt of discount  ({:.1f}x)".format(
            r["period"], r["lift"] * 100, r["extra_discount"] * 100, r["efficiency"]))

    free = [r for r in events if not r["efficiency"]]
    if free:
        print("\n  LIFTS THAT COST NO EXTRA DISCOUNT (look hard at what drove these)")
        for r in sorted(free, key=lambda r: -r["lift"])[:3]:
            print("    {}  {:+.0f}% revenue at {:.1f}% discount rate, no increase on baseline".format(
                r["period"], r["lift"] * 100, r["discount_rate"] * 100))

    print("\n  Next step: for each period above, check what was actually running —")
    print("  email campaigns sent, ad spend, and any launch. The scan finds WHEN;")
    print("  only the campaign record explains WHY.\n")


if __name__ == "__main__":
    args = [a for a in sys.argv[1:] if not a.startswith("--")]
    if not args:
        sys.exit(__doc__)
    kw = {}
    if "--baseline" in sys.argv:
        kw["baseline_n"] = int(sys.argv[sys.argv.index("--baseline") + 1])
    if "--threshold" in sys.argv:
        kw["threshold"] = float(sys.argv[sys.argv.index("--threshold") + 1])
    data = json.load(open(args[0]))
    if kw:
        globals()["analyse"] = (lambda f: (lambda rows: f(rows, **kw)))(analyse)
    report(data)
