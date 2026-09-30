#!/usr/bin/env python3
"""Render the compact interface panels used by the profile README."""
import base64
import html
import os


HERE = os.path.dirname(os.path.abspath(__file__))
ASSET_DIR = os.path.join(HERE, "..", "assets")
UI_DIR = os.path.join(ASSET_DIR, "ui")
ICON_DIR = os.path.join(ASSET_DIR, "toolkit", "icons")

SECTIONS = [
    ("01", "PROFILE", "SYSTEM IDENTITY", "#5eead4"),
    ("02", "NOW", "ACTIVE FOCUS", "#f59e0b"),
    ("03", "SELECTED WORK", "FEATURED BUILDS", "#60a5fa"),
    ("04", "TOOLKIT", "CAPABILITY MAP", "#34d399"),
    ("05", "ACTIVITY", "PUBLIC SIGNAL", "#a78bfa"),
    ("06", "CONNECT", "OPEN CHANNEL", "#fb7185"),
]

TOOLKIT = [
    ("LANGUAGES", [("icon", "Python", "python"), ("icon", "JavaScript", "javascript"), ("icon", "Dart", "dart")]),
    ("FRONTEND", [("icon", "React", "react"), ("icon", "Vite", "vite"), ("icon", "HTML5", "html5"), ("icon", "CSS3", "css3"), ("icon", "Tailwind", "tailwindcss")]),
    ("BACKEND", [("icon", "Django", "django"), ("icon", "Node.js", "nodejs"), ("icon", "Express", "express")]),
    ("MOBILE", [("icon", "Flutter", "flutter")]),
    ("DATA", [("icon", "MySQL", "mysql"), ("icon", "MongoDB", "mongodb")]),
    ("SYSTEMS + API", [("text", "REST APIs", ""), ("text", "WebSockets", ""), ("text", "Authentication", ""), ("text", "RBAC", "")]),
    ("AI", [("text", "Local LLMs", ""), ("text", "Prompt Engineering", ""), ("text", "AI Applications", "")]),
    ("WORKFLOW", [("icon", "Git", "git"), ("icon", "GitHub", "github")]),
]


def esc(value):
    return html.escape(value, quote=True)


def write_svg(filename, content):
    os.makedirs(UI_DIR, exist_ok=True)
    path = os.path.join(UI_DIR, filename)
    with open(path, "w", encoding="utf-8", newline="\n") as output:
        output.write(content)
    print(f"wrote {path}")


def icon_uri(name):
    path = os.path.join(ICON_DIR, f"{name}.svg")
    with open(path, "rb") as icon_file:
        encoded = base64.b64encode(icon_file.read()).decode("ascii")
    return f"data:image/svg+xml;base64,{encoded}"


def common_style():
    return """
    .surface { fill: #0d1117; }
    .surface2 { fill: #111820; }
    .border { fill: none; stroke: #30363d; }
    .rule { stroke: #30363d; }
    .title { fill: #f0f6fc; font-family: -apple-system, BlinkMacSystemFont, Segoe UI, sans-serif; }
    .body { fill: #c9d1d9; font-family: -apple-system, BlinkMacSystemFont, Segoe UI, sans-serif; }
    .muted { fill: #8b949e; font-family: ui-monospace, SFMono-Regular, Menlo, Consolas, monospace; }
    .tile { fill: #f6f8fa; stroke: #30363d; }
    @media (prefers-color-scheme: light) {
      .surface { fill: #ffffff; }
      .surface2 { fill: #f6f8fa; }
      .border, .rule { stroke: #d0d7de; }
      .title { fill: #1f2328; }
      .body { fill: #24292f; }
      .muted { fill: #59636e; }
      .tile { fill: #ffffff; stroke: #d0d7de; }
    }
    @media (prefers-reduced-motion: reduce) { animate { display: none; } }
"""


def render_section(number, title, meta, accent):
    return f'''<svg xmlns="http://www.w3.org/2000/svg" width="760" height="52" viewBox="0 0 760 52" role="img" aria-labelledby="title desc">
  <title id="title">{esc(number)} / {esc(title)}</title>
  <desc id="desc">{esc(meta.title())} section</desc>
  <style>
    {common_style()}
    .sectionNumber {{ fill: {accent}; font: 700 13px ui-monospace, SFMono-Regular, Menlo, Consolas, monospace; }}
    .sectionTitle {{ font: 700 16px ui-monospace, SFMono-Regular, Menlo, Consolas, monospace; letter-spacing: 0; }}
    .sectionMeta {{ font: 700 10px ui-monospace, SFMono-Regular, Menlo, Consolas, monospace; letter-spacing: 0; }}
    @media (max-width: 480px) {{
      .sectionNumber {{ font-size: 27px; }}
      .sectionTitle {{ font-size: 28px; }}
      .sectionMeta {{ font-size: 18px; }}
    }}
  </style>
  <rect class="surface" x="1" y="1" width="758" height="50" rx="6"/>
  <rect class="border" x="1" y="1" width="758" height="50" rx="6"/>
  <rect x="1" y="1" width="5" height="50" rx="2" fill="{accent}"/>
  <rect x="15" y="12" width="38" height="28" rx="4" fill="{accent}" fill-opacity="0.12" stroke="{accent}" stroke-opacity="0.55"/>
  <text class="sectionNumber" x="34" y="31" text-anchor="middle">{esc(number)}</text>
  <text class="title sectionTitle" x="69" y="32">{esc(title)}</text>
  <path d="M270 26H590" stroke="{accent}" stroke-opacity="0.24"/>
  <circle cx="603" cy="26" r="3" fill="{accent}"/>
  <text class="muted sectionMeta" x="738" y="30" text-anchor="end">{esc(meta)}</text>
</svg>
'''


def render_profile():
    rows = [
        ("WEB", "React interfaces connected to REST APIs and Django systems"),
        ("PLATFORM", "Authentication, RBAC, databases, realtime, and business workflows"),
        ("MOBILE", "Flutter applications with structured state and API integration"),
    ]
    rendered = []
    for index, (label, copy) in enumerate(rows):
        y = 64 + index * 28
        rendered.append(f'<text class="label" x="34" y="{y}">{label}</text>')
        rendered.append(f'<text class="body copy" x="146" y="{y}">{esc(copy)}</text>')
    return f'''<svg xmlns="http://www.w3.org/2000/svg" width="760" height="148" viewBox="0 0 760 148" role="img" aria-labelledby="title desc">
  <title id="title">Current development signal</title>
  <desc id="desc">Web, platform, and mobile capabilities currently in focus.</desc>
  <style>
    {common_style()}
    .kicker {{ fill: #5eead4; font: 700 11px ui-monospace, SFMono-Regular, Menlo, Consolas, monospace; }}
    .label {{ fill: #8b949e; font: 700 11px ui-monospace, SFMono-Regular, Menlo, Consolas, monospace; }}
    .copy {{ font-size: 13px; }}
    .active {{ fill: #34d399; font: 700 10px ui-monospace, SFMono-Regular, Menlo, Consolas, monospace; }}
    @media (prefers-color-scheme: light) {{ .label {{ fill: #59636e; }} }}
  </style>
  <rect class="surface" x="1" y="1" width="758" height="146" rx="7"/>
  <rect class="border" x="1" y="1" width="758" height="146" rx="7"/>
  <rect x="1" y="1" width="5" height="146" rx="2" fill="#5eead4"/>
  <text class="kicker" x="34" y="30">CURRENT SIGNAL</text>
  <circle cx="667" cy="26" r="4" fill="#34d399"><animate attributeName="opacity" values="1;0.35;1" dur="2.6s" repeatCount="indefinite"/></circle>
  <text class="active" x="726" y="30" text-anchor="end">ACTIVE</text>
  <path class="rule" d="M34 42H726"/>
  <path class="rule" d="M126 50V128"/>
  {''.join(rendered)}
</svg>
'''


def render_profile_mobile():
    rows = [
        ("WEB", ["React interfaces connected to REST APIs", "and Django systems"]),
        ("PLATFORM", ["Authentication, RBAC, databases,", "realtime, and business workflows"]),
        ("MOBILE", ["Flutter applications with structured", "state and API integration"]),
    ]
    rendered = []
    for index, (label, lines) in enumerate(rows):
        top = 48 + index * 46
        rendered.append(f'<text class="label" x="18" y="{top + 13}">{label}</text>')
        rendered.extend(f'<text class="body copy" x="88" y="{top + 7 + line_index * 14}">{esc(line)}</text>' for line_index, line in enumerate(lines))
        if index < 2:
            rendered.append(f'<path class="rule" d="M18 {top + 38}H342"/>')
    return f'''<svg xmlns="http://www.w3.org/2000/svg" width="360" height="190" viewBox="0 0 360 190" role="img" aria-labelledby="title desc">
  <title id="title">Current development signal</title>
  <desc id="desc">Web, platform, and mobile capabilities currently in focus.</desc>
  <style>
    {common_style()}
    .kicker {{ fill: #5eead4; font: 700 10px ui-monospace, SFMono-Regular, Menlo, Consolas, monospace; }}
    .label {{ fill: #8b949e; font: 700 9px ui-monospace, SFMono-Regular, Menlo, Consolas, monospace; }}
    .copy {{ font-size: 10.5px; }}
    .active {{ fill: #34d399; font: 700 9px ui-monospace, SFMono-Regular, Menlo, Consolas, monospace; }}
    @media (prefers-color-scheme: light) {{ .label {{ fill: #59636e; }} }}
  </style>
  <rect class="surface" x="1" y="1" width="358" height="188" rx="7"/>
  <rect class="border" x="1" y="1" width="358" height="188" rx="7"/>
  <rect x="1" y="1" width="5" height="188" rx="2" fill="#5eead4"/>
  <text class="kicker" x="18" y="26">CURRENT SIGNAL</text>
  <circle cx="298" cy="22" r="3.5" fill="#34d399"><animate attributeName="opacity" values="1;0.35;1" dur="2.6s" repeatCount="indefinite"/></circle>
  <text class="active" x="342" y="26" text-anchor="end">ACTIVE</text>
  <path class="rule" d="M18 36H342"/>
  {''.join(rendered)}
</svg>
'''


def render_now():
    rows = [
        ("01", "FRONTEND", ["Building product-oriented React interfaces with deliberate systems", "and interaction design."]),
        ("02", "BACKEND", ["Developing Django platforms with authentication, role-based", "workflows, APIs, and AI-assisted functionality."]),
        ("03", "MOBILE", ["Building Flutter applications around structured architecture,", "API integration, and practical user workflows."]),
    ]
    rendered = []
    colors = ["#60a5fa", "#34d399", "#f59e0b"]
    for index, (number, label, lines) in enumerate(rows):
        top = 44 + index * 56
        color = colors[index]
        rendered.append(f'<rect x="28" y="{top}" width="30" height="30" rx="5" fill="{color}" fill-opacity="0.12" stroke="{color}" stroke-opacity="0.55"/>')
        rendered.append(f'<text class="index" x="43" y="{top + 20}" text-anchor="middle" fill="{color}">{number}</text>')
        rendered.append(f'<text class="label" x="76" y="{top + 20}">{label}</text>')
        rendered.extend(f'<text class="body copy" x="168" y="{top + 13 + line_index * 17}">{esc(line)}</text>' for line_index, line in enumerate(lines))
        if index < 2:
            rendered.append(f'<path class="rule" d="M28 {top + 43}H732"/>')
    return f'''<svg xmlns="http://www.w3.org/2000/svg" width="760" height="218" viewBox="0 0 760 218" role="img" aria-labelledby="title desc">
  <title id="title">Current focus</title>
  <desc id="desc">Three active areas: frontend, backend, and mobile development.</desc>
  <style>
    {common_style()}
    .kicker {{ fill: #f59e0b; font: 700 11px ui-monospace, SFMono-Regular, Menlo, Consolas, monospace; }}
    .index {{ font: 700 10px ui-monospace, SFMono-Regular, Menlo, Consolas, monospace; }}
    .label {{ fill: #8b949e; font: 700 10px ui-monospace, SFMono-Regular, Menlo, Consolas, monospace; }}
    .copy {{ font-size: 13px; }}
    @media (prefers-color-scheme: light) {{ .label {{ fill: #59636e; }} }}
  </style>
  <rect class="surface" x="1" y="1" width="758" height="216" rx="7"/>
  <rect class="border" x="1" y="1" width="758" height="216" rx="7"/>
  <rect x="1" y="1" width="5" height="216" rx="2" fill="#f59e0b"/>
  <text class="kicker" x="28" y="28">FOCUS QUEUE</text>
  <text class="muted" x="732" y="28" text-anchor="end" font-size="10">03 ACTIVE TRACKS</text>
  {''.join(rendered)}
</svg>
'''


def render_now_mobile():
    rows = [
        ("01", "FRONTEND", ["Building product-oriented React interfaces", "with deliberate systems and interaction", "design."]),
        ("02", "BACKEND", ["Developing Django platforms with authentication,", "role-based workflows, APIs, and AI-assisted", "functionality."]),
        ("03", "MOBILE", ["Building Flutter applications around structured", "architecture, API integration, and practical", "user workflows."]),
    ]
    rendered = []
    colors = ["#60a5fa", "#34d399", "#f59e0b"]
    for index, (number, label, lines) in enumerate(rows):
        top = 43 + index * 72
        color = colors[index]
        rendered.append(f'<rect x="16" y="{top}" width="28" height="28" rx="5" fill="{color}" fill-opacity="0.12" stroke="{color}" stroke-opacity="0.55"/>')
        rendered.append(f'<text class="index" x="30" y="{top + 19}" text-anchor="middle" fill="{color}">{number}</text>')
        rendered.append(f'<text class="label" x="54" y="{top + 19}">{label}</text>')
        rendered.extend(f'<text class="body copy" x="54" y="{top + 35 + line_index * 13}">{esc(line)}</text>' for line_index, line in enumerate(lines))
        if index < 2:
            rendered.append(f'<path class="rule" d="M16 {top + 64}H344"/>')
    return f'''<svg xmlns="http://www.w3.org/2000/svg" width="360" height="266" viewBox="0 0 360 266" role="img" aria-labelledby="title desc">
  <title id="title">Current focus</title>
  <desc id="desc">Three active areas: frontend, backend, and mobile development.</desc>
  <style>
    {common_style()}
    .kicker {{ fill: #f59e0b; font: 700 10px ui-monospace, SFMono-Regular, Menlo, Consolas, monospace; }}
    .index {{ font: 700 9px ui-monospace, SFMono-Regular, Menlo, Consolas, monospace; }}
    .label {{ fill: #8b949e; font: 700 9px ui-monospace, SFMono-Regular, Menlo, Consolas, monospace; }}
    .copy {{ font-size: 10px; }}
    @media (prefers-color-scheme: light) {{ .label {{ fill: #59636e; }} }}
  </style>
  <rect class="surface" x="1" y="1" width="358" height="264" rx="7"/>
  <rect class="border" x="1" y="1" width="358" height="264" rx="7"/>
  <rect x="1" y="1" width="5" height="264" rx="2" fill="#f59e0b"/>
  <text class="kicker" x="16" y="26">FOCUS QUEUE</text>
  <text class="muted" x="344" y="26" text-anchor="end" font-size="9">03 ACTIVE TRACKS</text>
  {''.join(rendered)}
</svg>
'''


def render_toolkit():
    rows = []
    for row_index, (category, items) in enumerate(TOOLKIT):
        y = 68 + row_index * 39
        rows.append(f'<text class="category" x="26" y="{y + 4}">{esc(category)}</text>')
        rows.append(f'<path class="rule" d="M142 {y - 18}V{y + 15}"/>')
        x = 160
        for kind, label, icon in items:
            if kind == "icon":
                width = 54 + len(label) * 6.4
                rows.append(f'<rect class="tile" x="{x}" y="{y - 17}" width="28" height="28" rx="5"/>')
                rows.append(f'<image href="{icon_uri(icon)}" x="{x + 4}" y="{y - 13}" width="20" height="20" preserveAspectRatio="xMidYMid meet"><title>{esc(label)}</title></image>')
                rows.append(f'<text class="tool" x="{x + 36}" y="{y + 4}">{esc(label)}</text>')
            else:
                width = 22 + len(label) * 6.3
                rows.append(f'<rect class="chip" x="{x}" y="{y - 14}" width="{width:.0f}" height="24" rx="5"/>')
                rows.append(f'<text class="chipText" x="{x + width / 2:.1f}" y="{y + 2}" text-anchor="middle">{esc(label)}</text>')
            x += width + 8
        if row_index < len(TOOLKIT) - 1:
            rows.append(f'<path class="rule" d="M26 {y + 21}H734"/>')
    return f'''<svg xmlns="http://www.w3.org/2000/svg" width="760" height="377" viewBox="0 0 760 377" role="img" aria-labelledby="title desc">
  <title id="title">Technology toolkit</title>
  <desc id="desc">Languages, frontend, backend, mobile, data, systems, AI, and workflow capabilities.</desc>
  <style>
    {common_style()}
    .kicker {{ fill: #34d399; font: 700 11px ui-monospace, SFMono-Regular, Menlo, Consolas, monospace; }}
    .category {{ fill: #8b949e; font: 700 9.5px ui-monospace, SFMono-Regular, Menlo, Consolas, monospace; }}
    .tool {{ fill: #c9d1d9; font: 12px -apple-system, BlinkMacSystemFont, Segoe UI, sans-serif; }}
    .chip {{ fill: #111820; stroke: #30363d; }}
    .chipText {{ fill: #aeb8c4; font: 700 9px ui-monospace, SFMono-Regular, Menlo, Consolas, monospace; }}
    @media (prefers-color-scheme: light) {{
      .category {{ fill: #59636e; }} .tool {{ fill: #24292f; }}
      .chip {{ fill: #f6f8fa; stroke: #d0d7de; }} .chipText {{ fill: #424a53; }}
    }}
  </style>
  <rect class="surface" x="1" y="1" width="758" height="375" rx="7"/>
  <rect class="border" x="1" y="1" width="758" height="375" rx="7"/>
  <rect x="1" y="1" width="5" height="375" rx="2" fill="#34d399"/>
  <text class="kicker" x="26" y="29">CAPABILITY MAP</text>
  <text class="muted" x="734" y="29" text-anchor="end" font-size="10">16 TOOLS / 08 DOMAINS</text>
  <path class="rule" d="M26 42H734"/>
  {''.join(rows)}
</svg>
'''


def render_toolkit_mobile():
    rows = []
    for row_index, (category, items) in enumerate(TOOLKIT):
        top = 44 + row_index * 60
        rows.append(f'<text class="category" x="16" y="{top + 10}">{esc(category)}</text>')
        if items[0][0] == "icon":
            available = 328
            cell = available / len(items)
            for item_index, (_, label, icon) in enumerate(items):
                center = 16 + cell * (item_index + 0.5)
                rows.append(f'<rect class="tile" x="{center - 13:.1f}" y="{top + 16}" width="26" height="26" rx="5"/>')
                rows.append(f'<image href="{icon_uri(icon)}" x="{center - 9:.1f}" y="{top + 20}" width="18" height="18" preserveAspectRatio="xMidYMid meet"><title>{esc(label)}</title></image>')
                rows.append(f'<text class="tool" x="{center:.1f}" y="{top + 53}" text-anchor="middle">{esc(label)}</text>')
        else:
            widths = [16 + len(label) * 5.2 for _, label, _ in items]
            total = sum(widths) + 6 * (len(widths) - 1)
            x = (360 - total) / 2
            for width, (_, label, _) in zip(widths, items):
                rows.append(f'<rect class="chip" x="{x:.1f}" y="{top + 21}" width="{width:.1f}" height="23" rx="5"/>')
                rows.append(f'<text class="chipText" x="{x + width / 2:.1f}" y="{top + 36}" text-anchor="middle">{esc(label)}</text>')
                x += width + 6
        if row_index < len(TOOLKIT) - 1:
            rows.append(f'<path class="rule" d="M16 {top + 58}H344"/>')
    return f'''<svg xmlns="http://www.w3.org/2000/svg" width="360" height="530" viewBox="0 0 360 530" role="img" aria-labelledby="title desc">
  <title id="title">Technology toolkit</title>
  <desc id="desc">Languages, frontend, backend, mobile, data, systems, AI, and workflow capabilities.</desc>
  <style>
    {common_style()}
    .kicker {{ fill: #34d399; font: 700 10px ui-monospace, SFMono-Regular, Menlo, Consolas, monospace; }}
    .category {{ fill: #8b949e; font: 700 8.5px ui-monospace, SFMono-Regular, Menlo, Consolas, monospace; }}
    .tool {{ fill: #c9d1d9; font: 8.5px -apple-system, BlinkMacSystemFont, Segoe UI, sans-serif; }}
    .chip {{ fill: #111820; stroke: #30363d; }}
    .chipText {{ fill: #aeb8c4; font: 700 7.5px ui-monospace, SFMono-Regular, Menlo, Consolas, monospace; }}
    @media (prefers-color-scheme: light) {{
      .category {{ fill: #59636e; }} .tool {{ fill: #24292f; }}
      .chip {{ fill: #f6f8fa; stroke: #d0d7de; }} .chipText {{ fill: #424a53; }}
    }}
  </style>
  <rect class="surface" x="1" y="1" width="358" height="528" rx="7"/>
  <rect class="border" x="1" y="1" width="358" height="528" rx="7"/>
  <rect x="1" y="1" width="5" height="528" rx="2" fill="#34d399"/>
  <text class="kicker" x="16" y="26">CAPABILITY MAP</text>
  <text class="muted" x="344" y="26" text-anchor="end" font-size="9">16 TOOLS / 08 DOMAINS</text>
  <path class="rule" d="M16 36H344"/>
  {''.join(rows)}
</svg>
'''


def main():
    for number, title, meta, accent in SECTIONS:
        write_svg(f"section-{number}.svg", render_section(number, title, meta, accent))
    write_svg("profile-signal.svg", render_profile())
    write_svg("profile-signal-mobile.svg", render_profile_mobile())
    write_svg("now.svg", render_now())
    write_svg("now-mobile.svg", render_now_mobile())
    write_svg("toolkit.svg", render_toolkit())
    write_svg("toolkit-mobile.svg", render_toolkit_mobile())


if __name__ == "__main__":
    main()
