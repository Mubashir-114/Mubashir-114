#!/usr/bin/env python3
"""Generate the profile activity SVG from GitHub GraphQL contribution data."""
from __future__ import annotations

import datetime as dt
import html
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

PALETTE = ["#161b22", "#164e63", "#0891b2", "#2563eb", "#7c3aed", "#c084fc"]
CELL = 12
GAP = 3
STEP = CELL + GAP
PAD = 22
LEFT_LABEL_W = 30
TOP_LABEL_H = 20
TITLEBAR_H = 30

BG = "#0d1117"
BG2 = "#111827"
FRAME = "#30363d"
MUTED = "#7d8590"
ACCENT = "#5eead4"
PRIMARY = "#60a5fa"
HIGHLIGHT = "#c084fc"

COL_T = 0.018
ROW_T = 0.045
CELL_DUR = 0.42


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
    days = data["days"]
    latest_date = data["range"]["end"]
    grid = build_grid(days)
    column_count = len(grid)
    art_w = column_count * STEP
    art_h = 7 * STEP
    canvas_w = PAD + LEFT_LABEL_W + art_w + PAD
    stats_h = 88
    canvas_h = TITLEBAR_H + TOP_LABEL_H + art_h + stats_h + PAD

    month_labels = []
    seen_months: set[tuple[int, int]] = set()
    for column_index, column in enumerate(grid):
        for cell in column:
            if cell is None:
                continue
            date = dt.date.fromisoformat(cell[0])
            key = (date.year, date.month)
            if key not in seen_months and date.day <= 7:
                seen_months.add(key)
                month_labels.append((column_index, date.strftime("%b")))
            break

    css = f"""
@keyframes cell {{
  0%   {{ opacity: 0; transform: translateY(-6px); }}
  100% {{ opacity: 1; transform: translateY(0); }}
}}
.c {{ opacity: 0; animation: cell {CELL_DUR:.2f}s cubic-bezier(.2,.8,.2,1) both; }}
@media (prefers-reduced-motion: reduce) {{
  .c {{ opacity: 1; animation: none; }}
}}
""".strip()

    parts = [
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{canvas_w}" height="{canvas_h}" '
        f'viewBox="0 0 {canvas_w} {canvas_h}" role="img" aria-labelledby="title desc" '
        f'font-family="ui-monospace, SFMono-Regular, Menlo, Consolas, monospace">',
        f'<title id="title">{html.escape(data["username"])} GitHub contribution activity</title>',
        '<desc id="desc">A one-year contribution grid with total, streak, and active-day statistics.</desc>',
        f'<style>{css}</style>',
        '<defs>',
        f'<linearGradient id="hbg" x1="0" y1="0" x2="0" y2="1">'
        f'<stop offset="0" stop-color="{BG2}"/><stop offset="1" stop-color="{BG}"/></linearGradient>',
        '</defs>',
        f'<rect width="{canvas_w}" height="{canvas_h}" rx="12" fill="url(#hbg)"/>',
        f'<rect x="0.5" y="0.5" width="{canvas_w - 1}" height="{canvas_h - 1}" rx="12" '
        f'fill="none" stroke="{FRAME}" stroke-width="1" stroke-opacity="0.55"/>',
        f'<line x1="0" y1="{TITLEBAR_H}" x2="{canvas_w}" y2="{TITLEBAR_H}" stroke="{FRAME}" stroke-opacity="0.35"/>',
    ]

    for index, dot_color in enumerate(["#ff5f56", "#ffbd2e", "#27c93f"]):
        parts.append(f'<circle cx="{PAD + index * 16}" cy="{TITLEBAR_H / 2}" r="5" fill="{dot_color}"/>')

    parts.append(
        f'<text x="{canvas_w / 2}" y="{TITLEBAR_H / 2 + 4}" fill="{MUTED}" font-size="12" '
        f'text-anchor="middle">{html.escape(data["username"])}@github: ~/activity --year</text>'
    )

    grid_top = TITLEBAR_H + TOP_LABEL_H
    grid_left = PAD + LEFT_LABEL_W

    for column_index, label in month_labels:
        x = grid_left + column_index * STEP
        parts.append(f'<text x="{x}" y="{TITLEBAR_H + 14}" fill="{MUTED}" font-size="10">{label}</text>')

    for weekday_index, weekday_name in [(1, "Mon"), (3, "Wed"), (5, "Fri")]:
        y = grid_top + weekday_index * STEP + CELL * 0.78
        parts.append(f'<text x="{PAD}" y="{y:.1f}" fill="{MUTED}" font-size="9">{weekday_name}</text>')

    for column_index, column in enumerate(grid):
        gx = grid_left + column_index * STEP
        for row_index, cell in enumerate(column):
            if cell is None:
                continue
            date_s, count, level = cell
            gy = grid_top + row_index * STEP
            delay = column_index * COL_T + row_index * ROW_T
            plural = "s" if count != 1 else ""
            latest_marker = f' stroke="{HIGHLIGHT}" stroke-width="1.5"' if date_s == latest_date else ""
            parts.append(
                f'<rect class="c" x="{gx}" y="{gy}" width="{CELL}" height="{CELL}" rx="2.5" '
                f'fill="{PALETTE[level]}"{latest_marker} style="animation-delay:{delay:.3f}s">'
                f'<title>{date_s}: {count} contribution{plural}</title></rect>'
            )

    legend_y = grid_top + art_h + 6
    legend_x = canvas_w - PAD - (len(PALETTE) * (CELL - 1) + 70)
    parts.append(
        f'<text x="{legend_x}" y="{legend_y + CELL * 0.8:.1f}" fill="{MUTED}" '
        f'font-size="10" text-anchor="end">Less</text>'
    )
    lx = legend_x + 8
    for color in PALETTE:
        parts.append(f'<rect x="{lx}" y="{legend_y}" width="{CELL - 1}" height="{CELL - 1}" rx="2.2" fill="{color}"/>')
        lx += CELL
    parts.append(f'<text x="{lx + 4}" y="{legend_y + CELL * 0.8:.1f}" fill="{MUTED}" font-size="10">More</text>')

    separator_y = legend_y + CELL + 14
    parts.append(f'<line x1="0" y1="{separator_y}" x2="{canvas_w}" y2="{separator_y}" stroke="{FRAME}" stroke-opacity="0.25"/>')

    current_streak = data["current_streak"]["length"]
    longest_streak = data["longest_streak"]["length"]
    total = data["total_contributions"]
    active_days = data["active_days"]
    date_range = data["range"]
    ly = separator_y + 24

    parts.append(
        f'<text x="{PAD}" y="{ly}" font-size="13" fill="{ACCENT}">'
        f'<tspan font-weight="700">{total:,}</tspan>'
        f'<tspan fill="{MUTED}"> contributions in the last year</tspan></text>'
    )
    parts.append(
        f'<text x="{canvas_w - PAD}" y="{ly}" font-size="12" fill="{MUTED}" text-anchor="end">'
        f'{date_range["start"]} &#8594; {date_range["end"]}</text>'
    )
    ly += 24
    parts.append(
        f'<text x="{PAD}" y="{ly}" font-size="13" fill="{MUTED}">current streak '
        f'<tspan fill="{ACCENT}" font-weight="700">{current_streak} days</tspan>'
        f'<tspan fill="{MUTED}">   &#183;   longest </tspan>'
        f'<tspan fill="{PRIMARY}" font-weight="700">{longest_streak} days</tspan></text>'
    )
    parts.append(
        f'<text x="{canvas_w - PAD}" y="{ly}" font-size="12" fill="{MUTED}" text-anchor="end">'
        f'<tspan fill="{HIGHLIGHT}" font-weight="700">{active_days}</tspan> active days</text>'
    )

    parts.append("</svg>")
    return "".join(parts)


def write_outputs(data: dict, svg: str) -> None:
    ET.fromstring(svg)
    os.makedirs(os.path.dirname(DATA_PATH), exist_ok=True)
    os.makedirs(os.path.dirname(SVG_PATH), exist_ok=True)
    with open(DATA_PATH, "w", encoding="utf-8", newline="\n") as data_file:
        json.dump(data, data_file, indent=2)
        data_file.write("\n")
    with open(SVG_PATH, "w", encoding="utf-8", newline="\n") as svg_file:
        svg_file.write(svg)
        svg_file.write("\n")


def main() -> int:
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
