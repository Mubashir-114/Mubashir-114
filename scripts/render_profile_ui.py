#!/usr/bin/env python3
"""Render MKL profile artwork and the retained optional UI panels.

GitHub renders SVGs as images: links belong in Markdown, typography uses local
fallbacks, and motion is omitted. All assets have explicit opaque backgrounds.
"""
import base64
import xml.etree.ElementTree as ET
from profile_svg import ROOT, CYAN, VIOLET, svg, text, write

SECTIONS = ["Profile", "Current focus", "Selected work", "Technical toolkit", "Contribution activity", "Let's build something useful"]
TOOLS = [("Flutter", "flutter"), ("Dart", "dart"), ("Python", "python"), ("Django", "django"),
         ("React", "react"), ("Node.js", "nodejs"), ("MySQL", "mysql"), ("Git", "git")]


def mark(x, y, width):
    # Keep the official paths and proportions. Inline geometry inherits color;
    # standalone SVGs cannot reliably load external styles or other SVG files.
    source = ET.parse(ROOT / "assets/brand/mkl-monogram.svg").getroot()
    paths = ''.join(ET.tostring(child, encoding="unicode") for child in source if child.tag.endswith("g"))
    return f'<svg x="{x}" y="{y}" width="{width}" height="{width*1120/1590:.2f}" viewBox="{source.attrib["viewBox"]}" fill="#fcfaf5">{paths}</svg>'


def render_header(mobile=False):
    w, h = (360, 286) if mobile else (760, 292)
    pad = 22 if mobile else 32
    body = '<defs><linearGradient id="aurora"><stop stop-color="#8edce6"/><stop offset=".55" stop-color="#abc5eb"/><stop offset="1" stop-color="#c4b5e8"/></linearGradient></defs>'
    body += mark(pad, 20, 57 if mobile else 68)
    body += text(w-pad, 42, "MUBASHEER KC", 11, "mono", text_anchor="end", letter_spacing="1")
    body += f'<path d="M{pad} 80H{w-pad}" stroke="#343434"/>'
    if mobile:
        body += text(pad, 122, "Thoughtful interfaces.", 29, "title")
        body += text(pad, 160, "Connected experiences.", 29, "title")
        body += text(pad, 202, "Full-Stack Developer", 16)
        body += text(pad, 226, "& Flutter Engineer", 16)
        body += text(pad, 264, "KANNUR, KERALA, INDIA", 11, "mono")
    else:
        body += text(pad, 132, "Thoughtful interfaces.", 41, "title")
        body += text(pad, 180, "Connected experiences.", 41, "title")
        body += text(pad, 220, "Full-Stack Developer & Flutter Engineer", 18)
        body += text(pad, 263, "KANNUR, KERALA, INDIA", 12, "mono")
        # Preserve the existing UI / API / DATA artwork as a quiet static motif.
        for index, label in enumerate(["UI", "API", "DATA"]):
            x = 554 + index*56
            body += f'<rect x="{x}" y="202" width="46" height="32" rx="6" fill="#141414" stroke="#343434"/>'
            body += text(x+23, 223, label, 10, "mono", text_anchor="middle")
            if index < 2:
                body += f'<path d="M{x+46} 218h10" stroke="#8edce6" stroke-opacity=".6"/>'
    body += f'<path d="M{pad} {h-1}H{w-pad}" stroke="url(#aurora)" stroke-width="2"/>'
    return svg(w, h, "MKL — Mubasheer KC", "Thoughtful interfaces. Connected experiences. Full-Stack Developer and Flutter Engineer in Kannur, Kerala, India.", body)


def render_cta(label, detail, primary=False):
    body = text(20, 30, label, 20, "title") + text(20, 52, detail, 12, "muted")
    body += text(308, 37, "↗" if primary else "→", 24, "accent", text_anchor="end")
    if primary:
        body += '<path d="M20 1H100" stroke="#8edce6" stroke-width="2"/>'
    return svg(332, 72, label, detail, body)


def render_toolkit(mobile=False):
    w, columns = (360, 4) if mobile else (760, 8)
    h = 176 if mobile else 108
    body = ''
    cell = (w-32)/columns
    for index, (label, icon) in enumerate(TOOLS):
        x = 16 + cell*(index % columns + .5)
        y = 20 + (index//columns)*76
        encoded = base64.b64encode((ROOT / f"assets/toolkit/icons/{icon}.svg").read_bytes()).decode("ascii")
        body += f'<rect x="{x-19}" y="{y}" width="38" height="38" rx="9" fill="#fcfaf5"/>'
        body += f'<image href="data:image/svg+xml;base64,{encoded}" x="{x-12}" y="{y+7}" width="24" height="24"/>'
        body += text(x, y+61, label, 12, "body", text_anchor="middle")
    return svg(w, h, "Core toolkit", "Flutter, Dart, Python, Django, React, Node.js, MySQL and Git.", body)


def render_panel(title, lines, mobile=False):
    w, h = (360, 152) if mobile else (760, 112)
    body = text(22, 32, title, 23, "title")
    for index, line in enumerate(lines):
        body += text(22, 64+index*24, line, 14)
    return svg(w, h, title, " ".join(lines), body)


def main():
    write("assets/header.svg", render_header())
    write("assets/header-mobile.svg", render_header(True))
    write("assets/cta/visit-portfolio.svg", render_cta("Visit portfolio", "Case studies, approach and more", True))
    write("assets/cta/explore-work.svg", render_cta("Explore selected work", "Four projects across web and mobile"))
    write("assets/cta/chat-with-me.svg", render_cta("Let's collaborate", "Connect with Mubasheer on LinkedIn"))
    write("assets/footer.svg", svg(760, 56, "MKL — Built with care", "Thoughtful interfaces. Connected experiences.", text(24, 35, "MKL", 25, "title") + text(736, 33, "Built with care. Always improving.", 14, "muted", text_anchor="end")))
    write("assets/footer-mobile.svg", svg(360, 64, "MKL — Built with care", "Built with care. Always improving.", text(20, 40, "MKL", 27, "title") + text(340, 38, "Built with care.", 14, "muted", text_anchor="end")))
    for index, title in enumerate(SECTIONS, 1):
        write(f"assets/ui/section-{index:02}.svg", svg(760, 48, title, f"Section {index}: {title}", text(20, 32, f"{index:02}  /  {title}", 24, "title")))
    # Retained optional panels use the same visual language; the public README
    # omits overlapping profile/focus panels to avoid repeating the introduction.
    for mobile in (False, True):
        suffix = "-mobile" if mobile else ""
        write(f"assets/ui/toolkit{suffix}.svg", render_toolkit(mobile))
        lines = ["Web interfaces. Backend services.", "Flutter experiences. Connected data."] if mobile else ["Web interfaces, backend services and Flutter experiences."]
        write(f"assets/ui/profile-signal{suffix}.svg", render_panel("Across the stack", lines, mobile))
        lines = ["Refining FinTrack 2.0.", "Building clearer product workflows."] if mobile else ["Refining FinTrack 2.0 and building clearer product workflows."]
        write(f"assets/ui/now{suffix}.svg", render_panel("Current focus", lines, mobile))


if __name__ == "__main__":
    main()
