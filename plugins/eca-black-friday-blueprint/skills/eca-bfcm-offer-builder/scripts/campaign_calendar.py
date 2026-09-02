#!/usr/bin/env python3
"""
Build the BFCM campaign calendar: named phases, real dates, countdown.

Every downstream skill (email, ads, website, social) keys off the PHASE IDs in this
output, not off dates. That way a shifted launch date moves every channel plan at once
instead of leaving five skills quietly disagreeing about when the sale starts.

Dates are computed, never typed. Getting "the Monday of Black Friday week" wrong by one
day is the classic failure here, and it silently corrupts every send time downstream.

Usage:
  python3 campaign_calendar.py                          # defaults, this year
  python3 campaign_calendar.py --year 2026 --ea-days 7 --sale-lead 4 --ends 2026-12-01
  python3 campaign_calendar.py --json
  python3 campaign_calendar.py --csv > calendar.csv   # upload to Google Sheets
"""
import sys, json
from datetime import date, timedelta
from bfcm_dates import black_friday

PHASES = ["LIST_BUILD", "EARLY_ACCESS", "WARM_UP", "SALE_LIVE",
          "BLACK_FRIDAY", "WEEKEND", "CYBER_MONDAY", "LAST_CHANCE", "POST_SALE"]


def build(year, ea_days=7, sale_lead=4, ends=None, build_weeks=8, post_days=21):
    bf = black_friday(year)
    cm = bf + timedelta(days=3)
    ea_start = bf - timedelta(days=sale_lead + ea_days + 3)
    ea_end = ea_start + timedelta(days=ea_days - 1)
    sale_start = bf - timedelta(days=sale_lead)
    end = date.fromisoformat(ends) if ends else cm
    p = {
        "LIST_BUILD":   (ea_start - timedelta(weeks=build_weeks), ea_start - timedelta(days=1),
                         "Grow the early-access list. Nothing is sold yet."),
        "EARLY_ACCESS": (ea_start, ea_end, "VIP list only. Highest revenue per recipient of the whole event."),
        "WARM_UP":      (ea_end + timedelta(days=1), sale_start - timedelta(days=1),
                         "Sale closed. Tease, build anticipation, keep capturing."),
        "SALE_LIVE":    (sale_start, bf - timedelta(days=1), "Core offer open to everyone."),
        "BLACK_FRIDAY": (bf, bf, "Peak day. Plan B check point sits here."),
        "WEEKEND":      (bf + timedelta(days=1), cm - timedelta(days=1), "Sustain. Lowest-effort revenue of the window."),
        "CYBER_MONDAY": (cm, cm, "Different offer, different lever. Not a continuation."),
        "LAST_CHANCE":  (cm, end, "Final hours messaging.") if end > cm else None,
        "POST_SALE":    (end + timedelta(days=1), end + timedelta(days=post_days),
                         "Gifting and shipping cut-off. Often bigger than the sale itself."),
    }
    return {"year": year, "black_friday": bf, "cyber_monday": cm, "ends": end,
            "phases": {k: v for k, v in p.items() if v}}


def render(c, today=None):
    today = today or date.today()
    print("\nCAMPAIGN CALENDAR — BFCM {}".format(c["year"]))
    print("All times in the STORE's timezone. State it explicitly to the member.\n")
    print("  {:<14}{:<13}{:<13}{:>7}  {}".format("PHASE", "STARTS", "ENDS", "DAYS", "WHAT HAPPENS"))
    for name in PHASES:
        if name not in c["phases"]:
            continue
        s, e, what = c["phases"][name]
        n = (e - s).days + 1
        print("  {:<14}{:<13}{:<13}{:>7}  {}".format(name, s.isoformat(), e.isoformat(), n, what))

    print("\n  COUNTDOWN")
    for name in PHASES:
        if name not in c["phases"]:
            continue
        s = c["phases"][name][0]
        d = (s - today).days
        if d >= 0:
            print("    {:<14} starts in {:>4} days".format(name, d))
        else:
            print("    {:<14} STARTED {:>4} days ago".format(name, -d))

    lb = c["phases"].get("LIST_BUILD")
    if lb and lb[0] <= today:
        print("\n  NOTE: the list-build window has already started. Every day not spent")
        print("  capturing early-access signups is audience you will not have in November.")

    print("\n  STILL TO CONFIRM WITH THE MEMBER (these constrain the offer, not just the schedule):")
    print("    - store timezone, stated once and used everywhere")
    print("    - shipping cut-off dates for domestic and international")
    print("    - stock arrival dates for anything in the offer")
    print("    - blackout dates: existing campaigns, launches, holidays\n")


if __name__ == "__main__":
    a = sys.argv[1:]
    def opt(flag, cast, default):
        return cast(a[a.index(flag) + 1]) if flag in a else default
    c = build(opt("--year", int, date.today().year), opt("--ea-days", int, 7),
              opt("--sale-lead", int, 4), opt("--ends", str, None))
    if "--csv" in a:
        # Column order is a contract. Downstream skills read by PHASE_ID and by header
        # name, so add columns at the end rather than reordering these.
        print("PHASE_ID,STARTS,ENDS,DAYS,WHAT HAPPENS,OWNER,STATUS,NOTES")
        for name in PHASES:
            if name not in c["phases"]:
                continue
            s_, e_, what = c["phases"][name]
            print('{},{},{},{},"{}",,Not started,'.format(name, s_, e_, (e_ - s_).days + 1, what))
    elif "--json" in a:
        print(json.dumps({k: (v.isoformat() if isinstance(v, date) else
                              {n: [x[0].isoformat(), x[1].isoformat(), x[2]] for n, x in v.items()})
                          for k, v in c.items()}, indent=2))
    else:
        render(c)
