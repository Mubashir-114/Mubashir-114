#!/usr/bin/env python3
"""Backward-compatible entry point for the local contribution renderer.

Usage: python scripts/generate_streak_svg.py [username] [output.svg]

The script intentionally does not call a third-party statistics service. It
renders data/contributions.json, which fetch_contributions.py refreshes from
GitHub's public contribution page.
"""
import json
import os
import sys

from render_heatmap_svg import IN_PATH, OUT_PATH, render


def main():
    username = sys.argv[1] if len(sys.argv) > 1 else os.environ.get("GH_PROFILE_USER")
    output = sys.argv[2] if len(sys.argv) > 2 else OUT_PATH

    with open(IN_PATH, encoding="utf-8") as data_file:
        data = json.load(data_file)

    if username and username != data.get("username"):
        raise SystemExit(
            f"contribution data belongs to {data.get('username')!r}, not {username!r}; "
            "run scripts/fetch_contributions.py first"
        )

    svg = render(data)
    with open(output, "w", encoding="utf-8") as output_file:
        output_file.write(svg)
    print(f"wrote {output} ({len(svg)} bytes)")


if __name__ == "__main__":
    main()
