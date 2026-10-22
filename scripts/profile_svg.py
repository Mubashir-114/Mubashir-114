"""Small, dependency-free SVG helpers shared by the profile generators."""
from html import escape
from pathlib import Path
import xml.etree.ElementTree as ET

ROOT = Path(__file__).resolve().parents[1]

# Surfaces
BG = "#0a0a0a"
BASE_DARK = "#101626"
BASE_NAVY = "#101b2a"
TILE_BG = "#eceff6"

# Core Palette
IVORY = "#fcfaf5"
BODY = "#d4d4d4"
MUTED = "#a8a6a1"
CYAN = "#8edce6"
BLUE = "#8bb9ff"
VIOLET = "#b29bf7"
EMERALD = "#65e1ad"
AMBER = "#f0cf85"

# Borders & Dividers
BORDER_SUBTLE = "#343434"
DIVIDER_SUBTLE = "#8095b7"

# Standard Radii
RADIUS_CARD = 12
RADIUS_TILE = 8
RADIUS_PILL = 8


def text(x, y, value, size=16, cls="body", **attrs):
    attributes = " ".join(f'{key.replace("_", "-")}="{escape(str(val), quote=True)}"' for key, val in attrs.items())
    return f'<text x="{x}" y="{y}" class="{cls}" font-size="{size}" {attributes}>{escape(str(value))}</text>'


def svg(width, height, title, description, body):
    # Explicit opaque surfaces keep contrast independent of GitHub's theme or
    # the OS color preference. No external fonts or scripts. Callers may add
    # finite CSS motion with an explicit reduced-motion fallback.
    return f'''<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" viewBox="0 0 {width} {height}" role="img" aria-labelledby="title desc">
<title id="title">{escape(title)}</title><desc id="desc">{escape(description)}</desc>
<style>
  .surface {{ fill: {BG}; }}
  .border {{ fill: none; stroke: #343434; }}
  text {{ font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif; }}
  .body {{ fill: #d4d4d4; }}
  .title {{ fill: {IVORY}; font-family: Georgia, "Times New Roman", serif; }}
  .muted {{ fill: {MUTED}; }}
  .accent {{ fill: {CYAN}; }}
  .mono {{ fill: {MUTED}; font-family: Consolas, "Liberation Mono", monospace; }}
</style>
<rect class="surface" x="0.5" y="0.5" width="{width-1}" height="{height-1}" rx="12"/>
<rect class="border" x="0.5" y="0.5" width="{width-1}" height="{height-1}" rx="12"/>
{body}
</svg>
'''


def write(path, content):
    ET.fromstring(content)
    target = ROOT / path
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(content, encoding="utf-8", newline="\n")
    print(f"wrote {path}")


def image_uri(path):
    """Embed local source artwork so GitHub has no nested network dependency."""
    import base64
    path = ROOT / path
    mime = "image/svg+xml" if path.suffix == ".svg" else "image/png"
    return f"data:{mime};base64,{base64.b64encode(path.read_bytes()).decode('ascii')}"


def premium(width, height, title, description, body, accent="#8db8ff", secondary="#b5a1ff", base="#101626"):
    """A tinted, self-contained surface; static content is always visible."""
    decor = f'''<defs>
<linearGradient id="panel" x1="0" y1="0" x2="1" y2="1"><stop stop-color="{base}"/><stop offset="1" stop-color="#0a0d14"/></linearGradient>
<radialGradient id="bloom"><stop stop-color="{accent}" stop-opacity=".13"/><stop offset="1" stop-color="{accent}" stop-opacity="0"/></radialGradient>
<linearGradient id="edge"><stop stop-color="{accent}"/><stop offset=".62" stop-color="{secondary}"/><stop offset="1" stop-color="{secondary}" stop-opacity="0"/></linearGradient>
</defs><style>.surface {{ fill: url(#panel); }} .border {{ stroke: {accent}; stroke-opacity: .26; }} .accent {{ fill: {accent}; }} .label {{ fill: {accent}; font-weight: 600; letter-spacing: .7px; }}</style>
<ellipse cx="{width*.88:.1f}" cy="{height*.18:.1f}" rx="{width*.44:.1f}" ry="{height:.1f}" fill="url(#bloom)"/>
<path d="M16 1H{width-16}" stroke="url(#edge)" stroke-width="2"/>
'''
    return svg(width, height, title, description, decor + body)


def action_pill(width, height, label, kind, accent="#65e1ad", base="#0e1726"):
    """Compact, premium action button for project repositories and case studies."""
    icons = {
        "case": '<rect x="1" y="2" width="12" height="12" rx="2.5"/><path d="M4 6h6M4 9h4"/>',
        "repo": '<path d="M4 14v-4a3 3 0 0 1 3-3h4m0 0-2.5-2.5M11 7l-2.5 2.5"/><circle cx="4" cy="14" r="1.5"/><circle cx="11" cy="7" r="1.5"/>',
        "backend": '<rect x="1" y="2" width="14" height="4.5" rx="1.5"/><rect x="1" y="9.5" width="14" height="4.5" rx="1.5"/><circle cx="4" cy="4.25" r=".75" fill="currentColor"/><circle cx="4" cy="11.75" r=".75" fill="currentColor"/>',
    }
    icon_svg = f'<g transform="translate(13 10)" fill="none" stroke="{accent}" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round">{icons.get(kind, icons["case"])}</g>'
    body = f'''<defs>
<linearGradient id="pill-bg" x1="0" y1="0" x2="1" y2="1"><stop stop-color="{base}"/><stop offset="1" stop-color="#0a0d14"/></linearGradient>
</defs><style>.pill-surface {{ fill: url(#pill-bg); }} .pill-border {{ fill: none; stroke: {accent}; stroke-opacity: .32; }}</style>
<rect class="pill-surface" x="0.5" y="0.5" width="{width-1}" height="{height-1}" rx="8"/>
<rect class="pill-border" x="0.5" y="0.5" width="{width-1}" height="{height-1}" rx="8"/>
{icon_svg}
{text(34, 22.5, label, 12.5, "body", font_weight="550")}
{text(width-14, 22.5, "↗", 12.5, "accent", style=f"fill: {accent}", text_anchor="end")}
'''
    return f'''<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" viewBox="0 0 {width} {height}" role="img" aria-labelledby="title desc">
<title id="title">{escape(label)} ↗</title><desc id="desc">{escape(label)} action link</desc>
<style>
  text {{ font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif; }}
  .body {{ fill: #e6edf3; }}
  .accent {{ fill: {accent}; font-weight: 600; }}
</style>
{body}
</svg>
'''
