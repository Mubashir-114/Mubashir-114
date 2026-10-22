"""Small, dependency-free SVG helpers shared by the profile generators."""
from html import escape
from pathlib import Path
import xml.etree.ElementTree as ET

ROOT = Path(__file__).resolve().parents[1]
BG = "#0a0a0a"
IVORY = "#fcfaf5"
MUTED = "#a8a6a1"
CYAN = "#8edce6"
VIOLET = "#c4b5e8"


def text(x, y, value, size=16, cls="body", **attrs):
    attributes = " ".join(f'{key.replace("_", "-")}="{escape(str(val), quote=True)}"' for key, val in attrs.items())
    return f'<text x="{x}" y="{y}" class="{cls}" font-size="{size}" {attributes}>{escape(str(value))}</text>'


def svg(width, height, title, description, body):
    # Explicit opaque surfaces keep contrast independent of GitHub's theme or
    # the OS color preference. No external fonts, scripts, filters or animation.
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
