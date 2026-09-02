#!/usr/bin/env python3
"""
Compute BFCM date windows for any year, so nothing is ever hardcoded.

Black Friday is the day after US Thanksgiving, which is the fourth Thursday of
November. It moves every year, so a hardcoded date is a bug waiting to happen and
a whole comparison built on the wrong week.

Usage:
    python3 bfcm_dates.py                # this year vs last year
    python3 bfcm_dates.py 2026           # that year vs the year before
    python3 bfcm_dates.py 2026 --json    # machine readable
"""
import sys, json
from datetime import date, timedelta


def black_friday(year: int) -> date:
    """Day after the fourth Thursday of November."""
    d = date(year, 11, 1)
    d += timedelta(days=(3 - d.weekday()) % 7)   # first Thursday (Mon=0 .. Thu=3)
    thanksgiving = d + timedelta(weeks=3)         # fourth Thursday
    return thanksgiving + timedelta(days=1)


def windows(year: int) -> dict:
    bf = black_friday(year)
    cm = bf + timedelta(days=3)
    return {
        "year": year,
        "thanksgiving": bf - timedelta(days=1),
        "black_friday": bf,
        "cyber_monday": cm,
        # Analysis windows
        "q4_start": date(year, 10, 1),
        "q4_end": date(year, 12, 31),
        "pre_bfcm_start": date(year, 10, 1),
        "pre_bfcm_end": bf - timedelta(days=6),      # up to the Sunday before BF week
        "bfcm_week_start": bf - timedelta(days=5),   # Monday of BF week
        "bfcm_week_end": cm,                          # through Cyber Monday
        "post_bfcm_start": cm + timedelta(days=1),
        "post_bfcm_end": date(year, 12, 31),
    }


def fmt(d):
    return d.isoformat() if isinstance(d, date) else d


def main():
    args = [a for a in sys.argv[1:] if not a.startswith("--")]
    as_json = "--json" in sys.argv
    year = int(args[0]) if args else date.today().year
    this, last = windows(year), windows(year - 1)

    if as_json:
        print(json.dumps({"this_year": {k: fmt(v) for k, v in this.items()},
                          "last_year": {k: fmt(v) for k, v in last.items()}}, indent=2))
        return

    for label, w in (("THIS YEAR", this), ("LAST YEAR (comparison)", last)):
        print(f"\n{label} — {w['year']}")
        print(f"  Black Friday        {w['black_friday']:%a %d %b %Y}")
        print(f"  Cyber Monday        {w['cyber_monday']:%a %d %b %Y}")
        print(f"  Pre-BFCM build-up   {w['pre_bfcm_start']} .. {w['pre_bfcm_end']}")
        print(f"  BFCM week           {w['bfcm_week_start']} .. {w['bfcm_week_end']}")
        print(f"  Post-BFCM to EOY    {w['post_bfcm_start']} .. {w['post_bfcm_end']}")
        print(f"  Full Q4             {w['q4_start']} .. {w['q4_end']}")

    days = (this["black_friday"] - date.today()).days
    if days >= 0:
        print(f"\n  {days} days until Black Friday {this['year']}.")
    print()


if __name__ == "__main__":
    main()
