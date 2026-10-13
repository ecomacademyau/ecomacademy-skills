#!/usr/bin/env python3
"""Signal tags for survey shares. Standard library only.

The report never shows statistics. It shows one of these plain tags, which
this module decides from the raw counts so the wording stays honest.

Level tags (how sure we are about a share, all-time):
  Strong signal        n >= 100 and count >= 15
  Early signal         n >= 30 and count >= 5
  Too few answers yet  anything smaller

Shift tags (this period against the rest of all-time):
  Too few answers yet  period n < 20, or rest-of-all-time n < 20
  Strong signal        two-proportion test p < 0.05
  Early signal         p < 0.20
  No real change       otherwise

Usage:
  python3 signals.py level --count 27 --n 88
  python3 signals.py shift --pc 27 --pn 88 --ac 101 --an 291
"""
import argparse
import json
import math
from statistics import NormalDist

LEVEL_TAGS = ("Strong signal", "Early signal", "Too few answers yet")
SHIFT_TAGS = ("Strong signal", "Early signal", "No real change", "Too few answers yet")


def pct(count, n):
    return round(100.0 * count / n, 1) if n else 0.0


def level(count, n):
    if n >= 100 and count >= 15:
        return "Strong signal"
    if n >= 30 and count >= 5:
        return "Early signal"
    return "Too few answers yet"


def _p_value(x1, n1, x2, n2):
    pooled = (x1 + x2) / (n1 + n2)
    if pooled in (0, 1):
        return 1.0
    se = math.sqrt(pooled * (1 - pooled) * (1 / n1 + 1 / n2))
    z = (x1 / n1 - x2 / n2) / se
    return 2 * (1 - NormalDist().cdf(abs(z)))


def shift(period_count, period_n, all_count, all_n):
    """Compare this period with the rest of all-time (all-time minus this period)."""
    rest_count, rest_n = all_count - period_count, all_n - period_n
    delta = round(pct(period_count, period_n) - pct(all_count, all_n), 1) if period_n and all_n else 0.0
    if period_n < 20 or rest_n < 20:
        return "Too few answers yet", delta
    p = _p_value(period_count, period_n, rest_count, rest_n)
    if p < 0.05:
        return "Strong signal", delta
    if p < 0.20:
        return "Early signal", delta
    return "No real change", delta


def main():
    ap = argparse.ArgumentParser()
    sub = ap.add_subparsers(dest="cmd", required=True)
    a = sub.add_parser("level")
    a.add_argument("--count", type=int, required=True)
    a.add_argument("--n", type=int, required=True)
    b = sub.add_parser("shift")
    for k in ("pc", "pn", "ac", "an"):
        b.add_argument(f"--{k}", type=int, required=True)
    args = ap.parse_args()
    if args.cmd == "level":
        print(json.dumps({"pct": pct(args.count, args.n), "tag": level(args.count, args.n)}))
    else:
        tag, delta = shift(args.pc, args.pn, args.ac, args.an)
        print(json.dumps({"period_pct": pct(args.pc, args.pn), "all_pct": pct(args.ac, args.an), "delta_pts": delta, "tag": tag}))


if __name__ == "__main__":
    main()
