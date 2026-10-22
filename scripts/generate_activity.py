#!/usr/bin/env python3
"""Generate the profile activity SVG from GitHub GraphQL contribution data."""
from __future__ import annotations

import argparse
import datetime as dt
import json
import os
import sys
import urllib.error
import urllib.request
import xml.etree.ElementTree as ET
from zoneinfo import ZoneInfo


USERNAME = os.environ.get("GH_PROFILE_USER", "Mubashir-114")
TOKEN = os.environ.get("GITHUB_TOKEN") or os.environ.get("GH_TOKEN")
PROFILE_TIMEZONE = os.environ.get("PROFILE_TIMEZONE", "Asia/Kolkata")
HERE = os.path.dirname(os.path.abspath(__file__))
DATA_PATH = os.path.join(HERE, "..", "data", "contributions.json")
SVG_PATH = os.path.join(HERE, "..", "assets", "activity", "activity.svg")
API_URL = "https://api.github.com/graphql"

PALETTE = ["#202020", "#29444a", "#3c6570", "#608c9c", "#9daed5", "#c4b5e8"]
CELL = 12
GAP = 3
STEP = CELL + GAP
PAD = 22
LEFT_LABEL_W = 30


QUERY = """
query($login: String!, $from: DateTime!, $to: DateTime!) {
  user(login: $login) {
    login
    contributionsCollection(from: $from, to: $to) {
      contributionCalendar {
        totalContributions
        weeks {
          contributionDays {
            date
            contributionCount
            weekday
          }
        }
      }
    }
  }
}
"""


class ActivityError(RuntimeError):
    """Raised when activity data cannot be generated safely."""


def iso_z(value: dt.datetime) -> str:
    return value.astimezone(dt.timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def local_window() -> tuple[dt.datetime, dt.datetime]:
    tz = ZoneInfo(PROFILE_TIMEZONE)
    now_local = dt.datetime.now(tz)
    end_dt = now_local
    start_dt = now_local - dt.timedelta(days=365)
    return start_dt, end_dt


def graphql_request(from_dt: dt.datetime, to_dt: dt.datetime) -> dict:
    if not TOKEN:
        raise ActivityError("GITHUB_TOKEN or GH_TOKEN is required for GitHub GraphQL contribution data")

    payload = json.dumps(
        {
            "query": QUERY,
            "variables": {
                "login": USERNAME,
                "from": iso_z(from_dt),
                "to": iso_z(to_dt),
            },
        }
    ).encode("utf-8")
    request = urllib.request.Request(
        API_URL,
        data=payload,
        headers={
            "Authorization": f"Bearer {TOKEN}",
            "Content-Type": "application/json",
            "Accept": "application/vnd.github+json",
            "User-Agent": "Mubashir-114-profile-activity",
        },
        method="POST",
    )

    try:
        with urllib.request.urlopen(request, timeout=30) as response:
            body = response.read().decode("utf-8")
    except urllib.error.HTTPError as exc:
        detail = exc.read().decode("utf-8", errors="replace")
        raise ActivityError(f"GitHub GraphQL request failed with HTTP {exc.code}: {detail}") from exc
    except urllib.error.URLError as exc:
        raise ActivityError(f"GitHub GraphQL request failed: {exc.reason}") from exc

    try:
        data = json.loads(body)
    except json.JSONDecodeError as exc:
        raise ActivityError("GitHub GraphQL returned malformed JSON") from exc

    if data.get("errors"):
        raise ActivityError(f"GitHub GraphQL returned errors: {data['errors']}")
    return data


def flatten_days(response: dict) -> list[dict]:
    user = response.get("data", {}).get("user")
    if not user:
        raise ActivityError(f"GitHub user not found or unavailable: {USERNAME}")

    calendar = (
        user.get("contributionsCollection", {})
        .get("contributionCalendar")
    )
    if not calendar or not isinstance(calendar.get("weeks"), list):
        raise ActivityError("GitHub GraphQL response did not include contribution calendar data")

    by_date: dict[str, int] = {}
    for week in calendar["weeks"]:
        for day in week.get("contributionDays", []):
            date_s = day.get("date")
            count = day.get("contributionCount")
            if not isinstance(date_s, str) or not isinstance(count, int):
                raise ActivityError("GitHub GraphQL response contained malformed contribution days")
            by_date[date_s] = count

    days = [{"date": date_s, "count": by_date[date_s]} for date_s in sorted(by_date)]
    if not days:
        raise ActivityError("GitHub GraphQL response contained no contribution days")
    return days


def compute_current_streak(days: list[dict], latest_local_date: dt.date) -> tuple[int, str | None, str | None]:
    idx = len(days) - 1
    latest_day = dt.date.fromisoformat(days[idx]["date"])
    if latest_day >= latest_local_date and days[idx]["count"] == 0:
        idx -= 1

    end_idx = idx
    streak = 0
    while idx >= 0 and days[idx]["count"] > 0:
        streak += 1
        idx -= 1

    if streak == 0:
        return 0, None, None
    return streak, days[idx + 1]["date"], days[end_idx]["date"]


def compute_longest_streak(days: list[dict]) -> tuple[int, str | None, str | None]:
    longest = 0
    run = 0
    run_start = 0
    longest_start = None
    longest_end = None

    for index, day in enumerate(days):
        if day["count"] > 0:
            if run == 0:
                run_start = index
            run += 1
            if run > longest:
                longest = run
                longest_start = days[run_start]["date"]
                longest_end = day["date"]
        else:
            run = 0

    return longest, longest_start, longest_end


def build_data(days: list[dict], latest_local_date: dt.date) -> dict:
    total = sum(day["count"] for day in days)
    active_days = sum(1 for day in days if day["count"] > 0)
    best = max(days, key=lambda day: day["count"])
    current_len, current_start, current_end = compute_current_streak(days, latest_local_date)
    longest_len, longest_start, longest_end = compute_longest_streak(days)

    monthly: dict[str, int] = {}
    for day in days:
        key = day["date"][:7]
        monthly[key] = monthly.get(key, 0) + day["count"]

    existing_generated_at = None
    if os.path.exists(DATA_PATH):
        try:
            with open(DATA_PATH, encoding="utf-8") as existing_file:
                existing = json.load(existing_file)
            if existing.get("days") == days:
                existing_generated_at = existing.get("generated_at")
        except (OSError, json.JSONDecodeError):
            existing_generated_at = None

    return {
        "username": USERNAME,
        "source": "github_graphql_contribution_calendar",
        "visibility": "contribution data available to the workflow token",
        "generated_at": existing_generated_at or dt.datetime.now(dt.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
        "range": {"start": days[0]["date"], "end": days[-1]["date"]},
        "total_contributions": total,
        "active_days": active_days,
        "avg_per_active_day": round(total / active_days, 1) if active_days else 0,
        "current_streak": {"length": current_len, "start": current_start, "end": current_end},
        "longest_streak": {"length": longest_len, "start": longest_start, "end": longest_end},
        "best_day": {"date": best["date"], "count": best["count"]},
        "monthly": [{"month": key, "total": monthly[key]} for key in sorted(monthly)],
        "days": days,
    }


def level_for(count: int) -> int:
    if count == 0:
        return 0
    if count <= 5:
        return 1
    if count <= 15:
        return 2
    if count <= 30:
        return 3
    if count <= 50:
        return 4
    return 5


def build_grid(days: list[dict]) -> list[list[tuple[str, int, int] | None]]:
    first = dt.date.fromisoformat(days[0]["date"])
    column: list[tuple[str, int, int] | None] = [None] * ((first.weekday() + 1) % 7)
    grid: list[list[tuple[str, int, int] | None]] = []

    for day in days:
        date = dt.date.fromisoformat(day["date"])
        weekday = (date.weekday() + 1) % 7
        while len(column) < weekday:
            column.append(None)
        column.append((day["date"], day["count"], level_for(day["count"])))
        if len(column) == 7:
            grid.append(column)
            column = []

    if column:
        while len(column) < 7:
            column.append(None)
        grid.append(column)

    return grid


def render_svg(data: dict) -> str:
    """Static calendar: visible without animation support, legible on either theme."""
    from profile_svg import svg, text
    grid = build_grid(data["days"])
    width = PAD * 2 + LEFT_LABEL_W + len(grid) * STEP
    grid_top = 80
    left = PAD + LEFT_LABEL_W
    body = text(PAD, 37, "A year of building", 30, "title")
    months = set()
    for column_index, column in enumerate(grid):
        for cell in column:
            if cell is None:
                continue
            date = dt.date.fromisoformat(cell[0])
            key = (date.year, date.month)
            if key not in months and date.day <= 7:
                months.add(key)
                body += text(left + column_index*STEP, 67, date.strftime("%b"), 16, "muted")
            break
        for row_index, cell in enumerate(column):
            if cell is None:
                continue
            date_s, count, level = cell
            body += (f'<rect x="{left+column_index*STEP}" y="{grid_top+row_index*STEP}" '
                     f'width="{CELL}" height="{CELL}" rx="2" fill="{PALETTE[level]}">'
                     f'<title>{date_s}: {count} contributions</title></rect>')
    for row, label in [(1, "M"), (3, "W"), (5, "F")]:
        body += text(PAD, grid_top+row*STEP+11, label, 14, "muted")
    body += text(PAD, 221, f'{data["total_contributions"]:,} contributions · {data["active_days"]} active days', 28)
    body += text(PAD, 254, f'{data["range"]["start"]} — {data["range"]["end"]}', 21, "muted")
    # Six swatches maintain a continuous less-to-more visual scale.
    for index, color in enumerate(PALETTE):
        body += f'<rect x="{width-PAD-172+index*16}" y="242" width="12" height="12" rx="2" fill="{color}"/>'
    body += text(width-PAD-182, 254, "LESS", 12, "muted", text_anchor="end")
    body += text(width-PAD, 254, "MORE", 12, "muted", text_anchor="end")
    # The same daily output carries both layouts, keeping workflow staging intact.
    # CSS inside an SVG image sees its rendered viewport width. On narrow screens,
    # replace tiny calendar labels with six real monthly totals and larger type.
    recent = data["monthly"][-6:]
    compact = text(PAD, 40, f'{data["total_contributions"]:,} contributions · {data["active_days"]} active days', 34)
    compact += text(PAD, 77, f'LAST SIX MONTHS / THROUGH {data["range"]["end"]}', 24, "muted")
    peak = max((month["total"] for month in recent), default=0) or 1
    step = (width-2*PAD)/6
    for index, month in enumerate(recent):
        center = PAD + step*(index+.5)
        height = month["total"]/peak*100
        compact += f'<rect x="{center-35:.2f}" y="{214-height:.2f}" width="70" height="{max(height,2):.2f}" rx="4" fill="#608c9c"/>'
        compact += text(f"{center:.2f}", f"{203-height:.2f}", month["total"], 26, "body", text_anchor="middle")
        label = dt.date.fromisoformat(month["month"]+"-01").strftime("%b")
        compact += text(f"{center:.2f}", 254, label, 28, "muted", text_anchor="middle")
    body = ('<style>.recent { display: none; } @media (max-width: 600px) { .year { display: none; } .recent { display: inline; } }</style>'
            + '<g class="year">' + body + '</g><g class="recent">' + compact + '</g>')
    desc = (f'{data["username"]}: {data["total_contributions"]} contributions over '
            f'{data["active_days"]} active days, {data["range"]["start"]} to {data["range"]["end"]}. '
            'Desktop shows a one-year calendar; mobile shows the last six monthly totals. '
            'Calendar intensity increases from dark gray to pale violet.')
    return svg(width, 278, "GitHub contribution activity", desc, body)


def write_outputs(data: dict, svg: str) -> None:
    ET.fromstring(svg)
    os.makedirs(os.path.dirname(DATA_PATH), exist_ok=True)
    os.makedirs(os.path.dirname(SVG_PATH), exist_ok=True)
    with open(DATA_PATH, "w", encoding="utf-8", newline="\n") as data_file:
        json.dump(data, data_file, indent=2)
        data_file.write("\n")
    with open(SVG_PATH, "w", encoding="utf-8", newline="\n") as svg_file:
        svg_file.write(svg.rstrip("\n") + "\n")


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--from-cache", action="store_true", help="Rebuild the SVG from committed data without a token or network")
    args = parser.parse_args()
    if args.from_cache:
        with open(DATA_PATH, encoding="utf-8") as cached_file:
            data = json.load(cached_file)
        # Preserve the data file and its generation timestamp exactly.
        svg = render_svg(data)
        ET.fromstring(svg)
        with open(SVG_PATH, "w", encoding="utf-8", newline="\n") as output:
            output.write(svg)
        print(f"wrote {SVG_PATH} from cached data ending {data['range']['end']}")
        return 0
    from_dt, to_dt = local_window()
    response = graphql_request(from_dt, to_dt)
    days = flatten_days(response)
    latest_local_date = dt.datetime.now(ZoneInfo(PROFILE_TIMEZONE)).date()
    data = build_data(days, latest_local_date)
    svg = render_svg(data)
    write_outputs(data, svg)
    print(
        f"wrote {SVG_PATH}: {data['total_contributions']} contributions, "
        f"current streak {data['current_streak']['length']}, "
        f"longest streak {data['longest_streak']['length']}"
    )
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except ActivityError as exc:
        print(f"activity generation failed: {exc}", file=sys.stderr)
        raise SystemExit(1)
