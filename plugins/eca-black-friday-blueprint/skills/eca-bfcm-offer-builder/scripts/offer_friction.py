#!/usr/bin/env python3
"""Score an offer's friction before recommending it.

Simple scales, complexity fails. This counts the hoops a customer has to jump
through and the ways the build can go wrong, so "too complicated" is a number
you can show the member rather than a matter of taste.

  python3 offer_friction.py --line "Spend $100, save $25" --threshold \
      --build automatic --conditions "no stacking"

Exit code is 1 when the offer needs rework, so it can gate a workflow.
"""
import argparse
import re
import sys

# Words that betray a second idea hiding inside a "one-line" offer.
JOINERS = re.compile(r"\b(and also|plus|as well as|excluding|except|when you|"
                     r"but only|provided|unless|then get)\b", re.I)


def main() -> int:
    ap = argparse.ArgumentParser(description="Score offer friction. Lower is better.")
    ap.add_argument("--line", required=True,
                    help="the one sentence the customer reads")
    ap.add_argument("--build", default="automatic",
                    choices=["automatic", "code", "app", "manual"],
                    help="how the discount is applied")
    ap.add_argument("--tiers", type=int, default=1,
                    help="number of discount tiers (1 = a single flat offer)")
    ap.add_argument("--threshold", action="store_true",
                    help="customer must reach a minimum spend")
    ap.add_argument("--conditions", default="",
                    help="comma-separated conditions, e.g. 'no stacking,excl gift cards'")
    ap.add_argument("--extra-step", action="store_true",
                    help="requires an action beyond buying (sign up, refer, enter)")
    ap.add_argument("--product-combo", action="store_true",
                    help="requires a specific combination of products")
    args = ap.parse_args()

    score, notes = 0, []

    def add(points: int, note: str) -> None:
        nonlocal score
        score += points
        notes.append((points, note))

    line = args.line.strip()
    words = len(line.split())
    if words > 12:
        add(1, f"the one-liner is {words} words — aim for 12 or fewer")
    if JOINERS.search(line):
        add(2, "the one-liner joins two ideas — that is two offers, not one")
    if re.search(r"[*†]|\(|\bT&C|\bterms\b", line, re.I):
        add(2, "the one-liner needs a footnote or bracket to be honest")
    elif re.search(r"\band\b", line, re.I):
        add(1, 'the one-liner contains "and" — check it is one offer, not two bolted together')
    if line.count(",") > 1:
        add(1, "more than one comma usually means more than one rule")

    if args.build == "code":
        add(1, "a code is something to remember, copy and mistype — prefer automatic")
    elif args.build == "app":
        add(2, "an app to build it is a dependency during the busiest week of the year")
    elif args.build == "manual":
        add(3, "manual setup on Black Friday is where real money goes out the door")

    if args.tiers > 1:
        add(args.tiers - 1,
            f"{args.tiers} tiers ask the customer to do arithmetic against their cart")
    if args.threshold:
        add(1, "a spend threshold is one condition — fine, if it is the only one")
    if args.product_combo:
        add(1, "requiring a specific product combination narrows who can act")
    if args.extra_step:
        add(2, "an action beyond buying loses most people who would have bought")

    conds = [c.strip() for c in args.conditions.split(",") if c.strip()]
    if conds:
        add(len(conds), f"{len(conds)} condition(s): " + "; ".join(conds))

    if score <= 1:
        verdict, ok = "CLEAN — recommend it", True
    elif score <= 3:
        verdict, ok = "ACCEPTABLE — near the practical ceiling", True
    else:
        verdict, ok = "TOO COMPLICATED — rework before recommending", False

    print(f'\nOffer:   "{line}"')
    print(f"Friction: {score}   {verdict}\n")
    if notes:
        print("What is adding friction:")
        for pts, note in sorted(notes, key=lambda n: -n[0]):
            print(f"  +{pts}  {note}")
    else:
        print("Nothing to flag. One sentence, no conditions, applies automatically.")

    if not ok:
        print("\nFix the offer, not the wording. Tiers -> one threshold. "
              "Exclusion list -> one collection in or out. Code -> automatic discount.")
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
