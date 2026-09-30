#!/usr/bin/env python3
"""Render the self-hosted project cards used by the profile README."""
import base64
import html
import os


HERE = os.path.dirname(os.path.abspath(__file__))
OUT_DIR = os.path.join(HERE, "..", "assets", "projects")
LOGO_DIR = os.path.join(OUT_DIR, "logos")

# Accent colors are sampled from each project's own logo artwork.
PROJECTS = [
    {
        "slug": "kodehax",
        "number": "01",
        "name": "KODEHAX ACADEMY",
        "logo": "kodehax.png",
        "language": "HTML",
        "accent": "#ffffff",
        "light_accent": "#000000",
        "secondary": "#ffffff",
        "description": [
            "AI-integrated learning platform for student, teacher, and",
            "administrator workflows.",
        ],
        "mobile_description": [
            "AI-integrated learning platform for student,",
            "teacher, and administrator workflows.",
        ],
        "stack": "Python / Django / AI integration / MySQL / Tailwind CSS",
        "mobile_stack": ["Python / Django / AI integration", "MySQL / Tailwind CSS"],
        "capabilities": ["ROLE WORKFLOWS", "AI ASSISTANCE", "ASSESSMENTS"],
    },
    {
        "slug": "provia",
        "number": "02",
        "name": "PROVIA",
        "logo": "provia.png",
        "language": "Python",
        "accent": "#fac432",
        "light_accent": "#695125",
        "secondary": "#9d9d9d",
        "description": [
            "Service marketplace connecting customer and provider workflows",
            "across discovery, booking, payments, and communication.",
        ],
        "mobile_description": [
            "Service marketplace connecting customer and",
            "provider workflows across discovery, booking,",
            "payments, and communication.",
        ],
        "stack": "Python / Django / MySQL / Channels / Tailwind CSS",
        "mobile_stack": ["Python / Django / MySQL", "Channels / Tailwind CSS"],
        "capabilities": ["BOOKING ENGINE", "WEBSOCKETS", "TRANSACTIONAL EMAIL"],
    },
    {
        "slug": "fintrack",
        "number": "03",
        "name": "FINTRACK",
        "logo": "fintrack.png",
        "language": "Dart",
        "accent": "#38a5f7",
        "light_accent": "#0874da",
        "secondary": "#fbc723",
        "description": [
            "Cross-platform finance application for transactions, budgets,",
            "reports, and offline-aware mobile workflows.",
        ],
        "mobile_description": [
            "Cross-platform finance application for",
            "transactions, budgets, reports, and",
            "offline-aware mobile workflows.",
        ],
        "stack": "Flutter / Dart / Provider / Repository Pattern / REST APIs",
        "mobile_stack": ["Flutter / Dart / Provider", "Repository Pattern / REST APIs"],
        "capabilities": ["SECURE TOKENS", "FINANCIAL REPORTS", "OFFLINE AWARE"],
    },
    {
        "slug": "nexo",
        "number": "04",
        "name": "NEXO",
        "logo": "nexo.svg",
        "language": "JavaScript",
        "accent": "#3b82f6",
        "light_accent": "#1d4ed8",
        "secondary": "#a855f7",
        "description": [
            "React product interface unifying conversations, projects,",
            "documents, knowledge, search, and workspace analytics.",
        ],
        "mobile_description": [
            "React product interface unifying conversations,",
            "projects, documents, knowledge, search, and",
            "workspace analytics.",
        ],
        "stack": "React / Vite / Zustand / Framer Motion / CSS",
        "mobile_stack": ["React / Vite / Zustand", "Framer Motion / CSS"],
        "capabilities": ["WORKSPACE UI", "COMMAND SEARCH", "STATE ARCHITECTURE"],
    },
]


def esc(value):
    return html.escape(value, quote=True)


def logo_data_uri(filename):
    path = os.path.join(LOGO_DIR, filename)
    extension = os.path.splitext(filename)[1].lower()
    media_type = "image/svg+xml" if extension == ".svg" else "image/png"
    with open(path, "rb") as logo_file:
        encoded = base64.b64encode(logo_file.read()).decode("ascii")
    return f"data:{media_type};base64,{encoded}"


def render_card(project):
    language = esc(project["language"])
    accent = project["accent"]
    light_accent = project["light_accent"]
    secondary = project["secondary"]
    logo = logo_data_uri(project["logo"])

    chips = []
    chip_x = 40
    for capability in project["capabilities"]:
        width = max(112, 28 + len(capability) * 8.4)
        chips.append(
            f'<rect class="chip" x="{chip_x:.0f}" y="191" width="{width:.0f}" '
            f'height="30" rx="6"/>'
            f'<text class="chipText" x="{chip_x + width / 2:.1f}" y="211" '
            f'text-anchor="middle">{esc(capability)}</text>'
        )
        chip_x += width + 10

    lines = "".join(
        f'<text class="body" x="40" y="{112 + index * 27}">{esc(line)}</text>'
        for index, line in enumerate(project["description"])
    )

    return f'''<svg xmlns="http://www.w3.org/2000/svg" width="760" height="264" viewBox="0 0 760 264" role="img" aria-labelledby="title desc">
  <title id="title">{esc(project["name"].title())} project card</title>
  <desc id="desc">{' '.join(esc(line) for line in project["description"])} View the repository on GitHub.</desc>
  <defs>
    <linearGradient id="accentLine" x1="0" y1="0" x2="1" y2="0">
      <stop offset="0" stop-color="{accent}"/>
      <stop offset="0.72" stop-color="{secondary}"/>
      <stop offset="1" stop-color="{secondary}" stop-opacity="0"/>
    </linearGradient>
    <filter id="softGlow" x="-100%" y="-300%" width="300%" height="700%">
      <feGaussianBlur stdDeviation="4"/>
    </filter>
    <clipPath id="topEdge"><rect width="760" height="5" rx="2"/></clipPath>
  </defs>
  <style>
    .surface {{ fill: #0d1117; }}
    .border {{ fill: none; stroke: #30363d; }}
    .titleText {{ fill: #f0f6fc; font: 700 28px -apple-system, BlinkMacSystemFont, Segoe UI, sans-serif; }}
    .body {{ fill: #c9d1d9; font: 18px -apple-system, BlinkMacSystemFont, Segoe UI, sans-serif; }}
    .muted {{ fill: #8b949e; font: 12px ui-monospace, SFMono-Regular, Menlo, Consolas, monospace; }}
    .stack {{ fill: #c9d1d9; font: 14px ui-monospace, SFMono-Regular, Menlo, Consolas, monospace; }}
    .accentText {{ fill: {accent}; }}
    .chip {{ fill: #111827; stroke: #30363d; }}
    .chipText {{ fill: #aeb8c4; font: 700 11px ui-monospace, SFMono-Regular, Menlo, Consolas, monospace; }}
    .repo {{ fill: {secondary}; font: 700 13px ui-monospace, SFMono-Regular, Menlo, Consolas, monospace; }}
    @media (prefers-color-scheme: light) {{
      .surface {{ fill: #ffffff; }}
      .border {{ stroke: #d0d7de; }}
      .titleText {{ fill: #1f2328; }}
      .body, .stack {{ fill: #24292f; }}
      .muted {{ fill: #59636e; }}
      .accentText {{ fill: {light_accent}; }}
      .chip {{ fill: #f6f8fa; stroke: #d0d7de; }}
      .chipText {{ fill: #424a53; }}
      .repo {{ fill: #0550ae; }}
    }}
    @media (prefers-reduced-motion: reduce) {{ animate {{ display: none; }} }}
  </style>

  <rect class="surface" x="1" y="1" width="758" height="262" rx="8"/>
  <rect class="border" x="1" y="1" width="758" height="262" rx="8"/>
  <rect x="1" y="1" width="758" height="4" rx="2" fill="url(#accentLine)"/>
  <rect x="-100" y="1" width="90" height="4" fill="{secondary}" opacity="0.75" filter="url(#softGlow)" clip-path="url(#topEdge)">
    <animate attributeName="x" values="-100;770" dur="5.5s" repeatCount="indefinite"/>
  </rect>
  <rect x="1" y="1" width="5" height="262" rx="2" fill="{accent}"/>

  <text class="muted accentText" x="40" y="40" font-weight="700">{esc(project["number"])} / PROJECT</text>
  <circle cx="548" cy="35" r="5" fill="{accent}">
    <animate attributeName="opacity" values="1;0.45;1" dur="2.8s" repeatCount="indefinite"/>
  </circle>
  <text class="muted" x="720" y="40" text-anchor="end">GITHUB PRIMARY: {language}</text>
  <image href="{logo}" x="40" y="56" width="24" height="24" preserveAspectRatio="xMidYMid meet"/>
  <text class="titleText" x="74" y="78">{esc(project["name"])}</text>
  {lines}
  <text class="muted" x="40" y="174">STACK</text>
  <text class="stack" x="91" y="174">{esc(project["stack"])}</text>
  {''.join(chips)}
  <path d="M40 238H720" stroke="#30363d" stroke-opacity="0.65"/>
  <text class="repo" x="40" y="253">VIEW REPOSITORY  -&gt;</text>
</svg>
'''


def render_mobile_card(project):
    language = esc(project["language"])
    accent = project["accent"]
    light_accent = project["light_accent"]
    secondary = project["secondary"]
    logo = logo_data_uri(project["logo"])

    chips = []
    chip_x = 14
    for capability in project["capabilities"]:
        width = max(84, 20 + len(capability) * 5.1)
        chips.append(
            f'<rect class="chip" x="{chip_x:.0f}" y="207" width="{width:.0f}" '
            f'height="27" rx="5"/>'
            f'<text class="chipText" x="{chip_x + width / 2:.1f}" y="225" '
            f'text-anchor="middle">{esc(capability)}</text>'
        )
        chip_x += width + 6

    description = "".join(
        f'<text class="body" x="20" y="{96 + index * 18}">{esc(line)}</text>'
        for index, line in enumerate(project["mobile_description"])
    )
    stack = "".join(
        f'<text class="stack" x="20" y="{168 + index * 18}">{esc(line)}</text>'
        for index, line in enumerate(project["mobile_stack"])
    )

    return f'''<svg xmlns="http://www.w3.org/2000/svg" width="360" height="278" viewBox="0 0 360 278" role="img" aria-labelledby="title desc">
  <title id="title">{esc(project["name"].title())} project card</title>
  <desc id="desc">{' '.join(esc(line) for line in project["description"])} View the repository on GitHub.</desc>
  <defs>
    <linearGradient id="accentLine" x1="0" y1="0" x2="1" y2="0">
      <stop offset="0" stop-color="{accent}"/>
      <stop offset="0.72" stop-color="{secondary}"/>
      <stop offset="1" stop-color="{secondary}" stop-opacity="0"/>
    </linearGradient>
    <filter id="softGlow" x="-100%" y="-300%" width="300%" height="700%"><feGaussianBlur stdDeviation="4"/></filter>
    <clipPath id="topEdge"><rect width="360" height="5" rx="2"/></clipPath>
  </defs>
  <style>
    .surface {{ fill: #0d1117; }}
    .border {{ fill: none; stroke: #30363d; }}
    .titleText {{ fill: #f0f6fc; font: 700 22px -apple-system, BlinkMacSystemFont, Segoe UI, sans-serif; }}
    .body {{ fill: #c9d1d9; font: 12.5px -apple-system, BlinkMacSystemFont, Segoe UI, sans-serif; }}
    .muted {{ fill: #8b949e; font: 8.5px ui-monospace, SFMono-Regular, Menlo, Consolas, monospace; }}
    .stack {{ fill: #c9d1d9; font: 10px ui-monospace, SFMono-Regular, Menlo, Consolas, monospace; }}
    .accentText {{ fill: {accent}; }}
    .chip {{ fill: #111827; stroke: #30363d; }}
    .chipText {{ fill: #aeb8c4; font: 700 7.5px ui-monospace, SFMono-Regular, Menlo, Consolas, monospace; }}
    .repo {{ fill: {secondary}; font: 700 11px ui-monospace, SFMono-Regular, Menlo, Consolas, monospace; }}
    @media (prefers-color-scheme: light) {{
      .surface {{ fill: #ffffff; }} .border {{ stroke: #d0d7de; }} .titleText {{ fill: #1f2328; }}
      .body, .stack {{ fill: #24292f; }} .muted {{ fill: #59636e; }} .accentText {{ fill: {light_accent}; }}
      .chip {{ fill: #f6f8fa; stroke: #d0d7de; }} .chipText {{ fill: #424a53; }} .repo {{ fill: #0550ae; }}
    }}
    @media (prefers-reduced-motion: reduce) {{ animate {{ display: none; }} }}
  </style>
  <rect class="surface" x="1" y="1" width="358" height="276" rx="8"/>
  <rect class="border" x="1" y="1" width="358" height="276" rx="8"/>
  <rect x="1" y="1" width="358" height="4" rx="2" fill="url(#accentLine)"/>
  <rect x="-80" y="1" width="70" height="4" fill="{secondary}" opacity="0.75" filter="url(#softGlow)" clip-path="url(#topEdge)">
    <animate attributeName="x" values="-80;370" dur="5.5s" repeatCount="indefinite"/>
  </rect>
  <rect x="1" y="1" width="5" height="276" rx="2" fill="{accent}"/>
  <text class="muted accentText" x="20" y="29" font-weight="700">{esc(project["number"])} / PROJECT</text>
  <circle cx="216" cy="25" r="4" fill="{accent}"><animate attributeName="opacity" values="1;0.45;1" dur="2.8s" repeatCount="indefinite"/></circle>
  <text class="muted" x="340" y="29" text-anchor="end">GITHUB PRIMARY: {language}</text>
  <image href="{logo}" x="20" y="45" width="22" height="22" preserveAspectRatio="xMidYMid meet"/>
  <text class="titleText" x="52" y="65">{esc(project["name"])}</text>
  {description}
  <text class="muted" x="20" y="148">STACK</text>
  {stack}
  {''.join(chips)}
  <path d="M20 248H340" stroke="#30363d" stroke-opacity="0.65"/>
  <text class="repo" x="20" y="267">VIEW REPOSITORY  -&gt;</text>
</svg>
'''


def main():
    os.makedirs(OUT_DIR, exist_ok=True)
    for project in PROJECTS:
        output = os.path.join(OUT_DIR, f'{project["slug"]}.svg')
        with open(output, "w", encoding="utf-8", newline="\n") as output_file:
            output_file.write(render_card(project))
        print(f"wrote {output}")
        mobile_output = os.path.join(OUT_DIR, f'{project["slug"]}-mobile.svg')
        with open(mobile_output, "w", encoding="utf-8", newline="\n") as output_file:
            output_file.write(render_mobile_card(project))
        print(f"wrote {mobile_output}")


if __name__ == "__main__":
    main()
