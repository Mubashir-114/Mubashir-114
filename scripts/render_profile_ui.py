#!/usr/bin/env python3
"""Generate the V3.1 editorial header, section artwork, toolkit and navigation cards.

No monograms, external fonts or scripts. Finite CSS data-flow motion has a
visible static base and an explicit reduced-motion override.
"""
from html import escape
from profile_svg import svg, text, image_uri, premium, write, TILE_BG

SECTIONS = [
    ("About", "THE PERSON BEHIND THE WORK", "profile", "#8bb9ff"),
    ("Selected work", "FOUR IDEAS, BUILT WITH CARE", "work", "#b29bf7"),
    ("Current focus", "BUILDING + REFINING", "focus", "#65e1ad"),
    ("Technology toolkit", "FROM INTERFACE TO INFRASTRUCTURE", "toolkit", "#8bb9ff"),
    ("Contribution activity", "A CONTINUING PRACTICE", "activity", "#b29bf7"),
    ("Let's connect", "GOOD IDEAS START WITH A CONVERSATION", "connect", "#f0cf85"),
]

TOOLS = [
    ("LANGUAGES", [("Python", "python"), ("JavaScript", "javascript"), ("TypeScript", "typescript"), ("Dart", "dart")]),
    ("FRONTEND", [("React", "react"), ("Next.js", "nextjs"), ("Tailwind CSS", "tailwindcss")]),
    ("BACKEND", [("Django", "django"), ("Node.js", "nodejs"), ("Express", "express")]),
    ("MOBILE", [("Flutter", "flutter"), ("Provider", "provider")]),
    ("DATABASES", [("MySQL", "mysql")]),
    ("SYSTEMS + APIs", [("REST APIs", "restapi"), ("WebSockets", "websockets"), ("Authentication", "auth"), ("Role-based access", "rbac")]),
    ("WORKFLOW", [("Git", "git"), ("GitHub", "github"), ("GitHub Actions", "githubactions")]),
]


def illustration(kind, x, y, color="#8bb9ff", scale=1):
    paths = {
        "profile": '<circle cx="20" cy="12" r="7"/><path d="M6 37v-4a14 14 0 0 1 28 0v4"/>',
        "work": '<rect x="3" y="9" width="28" height="23" rx="4"/><path d="M10 3h27v23M9 17h15M9 24h10"/>',
        "focus": '<circle cx="20" cy="20" r="13"/><circle cx="20" cy="20" r="5"/><path d="M20 0v7m0 26v7M0 20h7m26 0h7"/>',
        "toolkit": '<path d="m12 9-9 11 9 11m16-22 9 11-9 11M23 5l-6 30"/>',
        "activity": '<path d="M2 32h36M6 27V17m9 10V6m10 21V12m10 15V2"/>',
        "connect": '<path d="M3 10h34v24H3zM3 10l17 13 17-13"/>',
        "screen": '<rect x="1" y="5" width="38" height="26" rx="4"/><path d="M14 38h12m-6-7v7M8 13h15m-15 7h23"/>',
        "service": '<rect x="3" y="2" width="34" height="14" rx="4"/><rect x="3" y="24" width="34" height="14" rx="4"/><path d="M10 9h12m-12 22h12M20 16v8"/>',
        "phone": '<rect x="10" y="1" width="22" height="38" rx="5"/><path d="M16 7h10m-7 26h4"/>',
        "mail": '<rect x="3" y="6" width="34" height="24" rx="4"/><path d="m5 8 15 11 15-11"/>',
        "linkedin": '<rect x="3" y="3" width="34" height="34" rx="7"/><path d="M11 15v14m0-19v.01M19 29v-7.5c0-2.8 1.8-4.5 4.5-4.5s4.5 1.7 4.5 4.5V29m-9-14v14"/>',
        "globe": '<circle cx="20" cy="20" r="16"/><path d="M4 20h32M20 4a24 24 0 0 1 0 32M20 4a24 24 0 0 0 0 32"/>',
    }
    return f'<g transform="translate({x} {y}) scale({scale})" fill="none" stroke="{color}" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round">{paths[kind]}</g>'


def render_header(mobile=False):
    w, h = (360, 386) if mobile else (960, 416)
    pad = 22 if mobile else 40
    body = '<style>@keyframes data-flow { from { stroke-dashoffset: 72; } to { stroke-dashoffset: 0; } } .trace { stroke-dasharray: 5 13; animation: data-flow 4s linear 1; } @media (prefers-reduced-motion: reduce) { .trace { animation: none; } }</style>'
    body += text(pad, 34, "INDEPENDENT DEVELOPER", 11.5 if mobile else 13, "label", letter_spacing="1.6")
    body += text(pad, 91 if mobile else 118, "Mubasheer KC", 38 if mobile else 61, "title")
    body += text(pad, 145 if mobile else 182, "Thoughtful interfaces.", 28 if mobile else 36, "title")
    body += text(pad, 181 if mobile else 226, "Connected experiences.", 28 if mobile else 36, "title")
    if mobile:
        body += text(pad, 225, "Full-Stack Developer", 17)
        body += text(pad, 250, "& Flutter Engineer", 17)
        body += '<path d="M22 280H338" stroke="#798bb1" stroke-opacity=".25"/>'
        for index, (label, kind) in enumerate([("INTERFACE", "screen"), ("SERVICES", "service"), ("MOBILE", "phone")]):
            x = 30 + index * 110
            body += illustration(kind, x + 19, 298, "#96baff", .65)
            body += text(x + 32, 350, label, 10.5, "mono", text_anchor="middle")
            if index < 2:
                body += f'<path class="trace" d="M{x+65} 312h38" stroke="#b29bf7" stroke-opacity=".6"/>'
        body += text(pad, 375, "KANNUR, KERALA, INDIA", 11, "mono")
    else:
        body += text(pad, 272, "Full-Stack Developer & Flutter Engineer", 20)
        body += '<path d="M40 311H528" stroke="#798bb1" stroke-opacity=".25"/>'
        body += text(pad, 348, "Interfaces with intention. Systems with structure.", 16, "muted")
        body += text(pad, 385, "KANNUR, KERALA, INDIA", 12, "mono", letter_spacing="1.2")
        body += '<g fill="none" stroke="#8bb9ff"><circle cx="740" cy="205" r="144" stroke-opacity=".12"/><circle cx="740" cy="205" r="113" stroke-dasharray="2 12" stroke-opacity=".18"/><path d="M620 286a144 144 0 0 1 185-209" stroke-opacity=".5"/><path d="M652 128 816 176 733 288Z" stroke-opacity=".2"/><path class="trace" d="M652 128 816 176 733 288 652 128" stroke="#b29bf7" stroke-opacity=".75"/></g>'
        for x, y, label, kind in [(620, 102, "UI", "screen"), (784, 150, "API", "service"), (701, 261, "MOBILE", "phone")]:
            body += f'<rect x="{x}" y="{y}" width="66" height="65" rx="15" fill="#111c30" stroke="#7692c7" stroke-opacity=".35"/>'
            body += illustration(kind, x + 21, y + 8, "#a6c6ff", .6)
            body += text(x + 33, y + 53, label, 10, "mono", text_anchor="middle")
        body += text(740, 379, "DESIGN  /  ENGINEER  /  REFINE", 11, "mono", text_anchor="middle", letter_spacing="1.2")
    return premium(w, h, "Mubasheer KC — Full-Stack Developer & Flutter Engineer", "Thoughtful interfaces. Connected experiences. Based in Kannur, Kerala, India.", body, "#8bb9ff", "#b49bf7", "#101b2a")


def render_section(index, title, meta, kind, accent, mobile=False):
    w, h = (360, 62) if mobile else (960, 72)
    body = f'<style>.surface {{ fill: #111a2b; }} .border {{ stroke: #61759b; stroke-opacity: .25; }}</style><rect x="1" y="15" width="32" height="32" rx="9" fill="{accent}" fill-opacity=".11"/>'
    body += text(17, 36, f'{index:02}', 12, "accent", text_anchor="middle")
    body += text(46, 39, title, 24 if mobile else 31, "title")
    if not mobile:
        body += text(902, 40, meta, 11, "mono", text_anchor="end", letter_spacing=".8")
        body += illustration(kind, 919, 21, accent, .7)
    return svg(w, h, title, f'{index:02} / {title}', body)


def render_portfolio_hero(mobile=False):
    """Primary Portfolio CTA: Deep midnight navy surface with illuminated accents."""
    w, h = (360, 92) if mobile else (600, 96)
    pad = 20 if mobile else 28
    accent = "#8bb9ff"
    secondary = "#b49bf7"
    title_text = "VISIT MY PORTFOLIO ↗"
    subtitle_text = "Explore projects, case studies & the thinking behind them."
    body = f'''<defs>
<linearGradient id="hero-panel" x1="0" y1="0" x2="1" y2="1"><stop stop-color="#121b2d"/><stop offset="1" stop-color="#0a0d16"/></linearGradient>
<radialGradient id="hero-bloom"><stop stop-color="{accent}" stop-opacity=".16"/><stop offset="1" stop-color="{accent}" stop-opacity="0"/></radialGradient>
<linearGradient id="hero-edge"><stop stop-color="{accent}"/><stop offset=".6" stop-color="{secondary}"/><stop offset="1" stop-color="{secondary}" stop-opacity="0"/></linearGradient>
</defs><style>.surface {{ fill: url(#hero-panel); }} .border {{ stroke: {accent}; stroke-opacity: .30; }} .accent {{ fill: {accent}; }} .label {{ fill: {accent}; font-weight: 600; letter-spacing: .9px; }}</style>
<ellipse cx="{w*.88:.1f}" cy="{h*.2:.1f}" rx="{w*.4:.1f}" ry="{h:.1f}" fill="url(#hero-bloom)"/>
<path d="M16 1H{w-16}" stroke="url(#hero-edge)" stroke-width="2"/>
'''
    btn_r = 18 if mobile else 21
    btn_x = w - pad - btn_r
    btn_y = h / 2

    # Visual hierarchy: Title, Subtitle, and clear interactive badge
    if mobile:
        body += text(pad, 36, title_text, 18, "title", font_weight="600")
        body += text(pad, 62, subtitle_text, 11.5, "muted")
        body += f'<circle cx="{btn_x}" cy="{btn_y}" r="{btn_r}" fill="#162238" stroke="{accent}" stroke-opacity=".38"/>'
        body += text(btn_x, btn_y + 5.5, "↗", 16, "accent", text_anchor="middle")
    else:
        body += text(pad, 40, title_text, 22, "title", font_weight="600")
        body += text(pad, 68, subtitle_text, 13.5, "muted")
        body += f'<circle cx="{btn_x}" cy="{btn_y}" r="{btn_r}" fill="#162238" stroke="{accent}" stroke-opacity=".38"/>'
        body += text(btn_x, btn_y + 6.5, "↗", 19, "accent", text_anchor="middle")
    return svg(w, h, "Visit My Portfolio ↗", subtitle_text, body)


def render_nav_card(title, subtitle, kind, accent, secondary, mobile=False):
    """Secondary Navigation CTA cards: Explore My Work (#selected-work) & Let's Connect (#contact)."""
    w, h = (360, 82) if mobile else (430, 84)
    pad = 18 if mobile else 22
    body = f'''<defs>
<linearGradient id="nav-panel" x1="0" y1="0" x2="1" y2="1"><stop stop-color="#111929"/><stop offset="1" stop-color="#0a0d15"/></linearGradient>
<radialGradient id="nav-bloom"><stop stop-color="{accent}" stop-opacity=".12"/><stop offset="1" stop-color="{accent}" stop-opacity="0"/></radialGradient>
<linearGradient id="nav-edge"><stop stop-color="{accent}"/><stop offset=".7" stop-color="{secondary}"/><stop offset="1" stop-color="{secondary}" stop-opacity="0"/></linearGradient>
</defs><style>.surface {{ fill: url(#nav-panel); }} .border {{ stroke: {accent}; stroke-opacity: .28; }} .accent {{ fill: {accent}; }} .label {{ fill: {accent}; }}</style>
<ellipse cx="{w*.85:.1f}" cy="{h*.15:.1f}" rx="{w*.35:.1f}" ry="{h:.1f}" fill="url(#nav-bloom)"/>
<path d="M14 1H{w-14}" stroke="url(#nav-edge)" stroke-width="1.6"/>
'''
    icon_box = 32
    icon_y = (h - icon_box) / 2
    body += f'<rect x="{pad}" y="{icon_y}" width="{icon_box}" height="{icon_box}" rx="8" fill="{accent}" fill-opacity=".08" stroke="{accent}" stroke-opacity=".25"/>'
    body += illustration(kind, pad + 6, icon_y + 3, accent, .5)
    text_x = pad + icon_box + 14
    body += text(text_x, 36 if mobile else 37, title, 17 if mobile else 19, "title", font_weight="600")
    body += text(text_x, 58 if mobile else 60, subtitle, 12 if mobile else 13, "muted")
    body += text(w - pad, 47, "↗", 20 if mobile else 22, "accent", text_anchor="end")
    return svg(w, h, title, subtitle, body)


def render_contact_card(title, subtitle, kind, accent, mobile=False):
    """Compact, coordinated contact cards for the bottom section."""
    w, h = (360, 74) if mobile else (282, 76)
    pad = 16 if mobile else 16
    body = f'''<defs>
<linearGradient id="contact-panel" x1="0" y1="0" x2="1" y2="1"><stop stop-color="#111827"/><stop offset="1" stop-color="#090d14"/></linearGradient>
</defs><style>.surface {{ fill: url(#contact-panel); }} .border {{ stroke: {accent}; stroke-opacity: .26; }} .accent {{ fill: {accent}; }}</style>
<path d="M12 1H{w-12}" stroke="{accent}" stroke-opacity=".4" stroke-width="1.5"/>
'''
    icon_box = 30
    icon_y = (h - icon_box) / 2
    body += f'<rect x="{pad}" y="{icon_y}" width="{icon_box}" height="{icon_box}" rx="7" fill="{accent}" fill-opacity=".09" stroke="{accent}" stroke-opacity=".22"/>'
    body += illustration(kind, pad + 5, icon_y + 3, accent, .48)
    text_x = pad + icon_box + 12
    body += text(text_x, 34, title, 14.5 if not mobile else 15, "body", font_weight="600", style="fill: #fcfaf5")
    body += text(text_x, 52, subtitle, 11.5 if not mobile else 12, "muted")
    body += text(w - pad, 42, "↗", 16, "accent", text_anchor="end")
    return svg(w, h, title, subtitle, body)


def render_profile(mobile=False):
    w, h = (360, 258) if mobile else (960, 158)
    items = [("screen", "Interfaces", "Clarity in every interaction.", "#8bb9ff"), ("service", "Services", "Structure behind the scenes.", "#b49bf7"), ("phone", "Mobile", "Care across platforms.", "#77d8c0")]
    body = ''
    for index, (kind, title, copy, color) in enumerate(items):
        if mobile:
            y = 23 + index * 79
            body += illustration(kind, 20, y + 4, color, .8)
            body += text(68, y + 21, title, 21, "title") + text(68, y + 46, copy, 14)
            if index < 2:
                body += f'<path d="M68 {y+61}H338" stroke="#6c7e9b" stroke-opacity=".2"/>'
        else:
            x = 28 + index * 316
            body += illustration(kind, x, 27, color, .95)
            body += text(x + 56, 50, title, 25, "title") + text(x, 111, copy, 16)
            if index < 2:
                body += f'<path d="M{x+286} 28v100" stroke="#6c7e9b" stroke-opacity=".2"/>'
    return premium(w, h, "How I approach the work", "Interfaces: clarity in every interaction. Services: structure behind the scenes. Mobile: care across platforms.", body)


def render_now(mobile=False):
    w, h = (360, 244) if mobile else (960, 192)
    body = text(24, 32, "CURRENT BUILD", 12, "label")
    body += f'<image href="{image_uri("assets/projects/logos/fintrack-jade.png")}" x="24" y="51" width="52" height="52"/>'
    body += text(90, 84, "FinTrack 2.0", 29, "title")
    body += text(24, 134, "Refining connected finance workflows.", 16)
    if mobile:
        body += '<path d="M24 158H336" stroke="#79cbb1" stroke-opacity=".2"/>'
        body += text(24, 190, "React interfaces. Django platforms.", 16)
        body += text(24, 216, "Structured Flutter applications.", 16)
    else:
        body += '<path d="M464 28v136" stroke="#79cbb1" stroke-opacity=".2"/>'
        body += text(500, 50, "ALSO IN FOCUS", 12, "label")
        body += text(500, 91, "Thoughtful React interfaces.", 19)
        body += text(500, 122, "Django platforms + structured Flutter apps.", 18)
    return premium(w, h, "Current focus", "Refining FinTrack 2.0 and connected finance workflows. Also focused on React interfaces, Django platforms and structured Flutter applications.", body, "#77d8c0", "#8bb9ff", "#101d24")


def tool_item(label, icon, x, y, size=15, mobile=False):
    """Unified technology item with standardized container, padding, and typography."""
    if mobile:
        box = 28
        rx = 7
        icon_dim = 18
        icon_pad = 5
        text_x = x + box + 9
        label_size = size
    else:
        box = 32
        rx = 8
        icon_dim = 22
        icon_pad = 5
        text_x = x + box + 10
        label_size = size

    icon_path = f"assets/toolkit/icons/{icon}.svg"
    return (
        f'<rect x="{x}" y="{y-box+9}" width="{box}" height="{box}" rx="{rx}" fill="{TILE_BG}"/>'
        f'<image href="{image_uri(icon_path)}" x="{x+icon_pad}" y="{y-box+9+icon_pad}" width="{icon_dim}" height="{icon_dim}" preserveAspectRatio="xMidYMid meet"/>'
        + text(text_x, y, label, label_size, "body")
    )


def render_toolkit(mobile=False):
    w, h = (360, 804) if mobile else (960, 530)
    body = ''
    y = 24
    # Standard desktop 4-column positions for predictable visual rhythm
    desktop_cols = [216, 396, 576, 756]

    for index, (category, items) in enumerate(TOOLS):
        color = ["#9fc7ff", "#b9a1ff", "#8ed5c5"][index % 3]
        if mobile:
            body += text(20, y + 12, category, 12, "mono", style=f"fill: {color}")
            if category == "LANGUAGES":
                positions = [(20, y + 46), (180, y + 46), (20, y + 88), (180, y + 88)]
                row_h = 120
            elif category == "SYSTEMS + APIs":
                positions = [(20, y + 46), (180, y + 46), (20, y + 88), (180, y + 88)]
                row_h = 120
            elif category in ("FRONTEND", "BACKEND", "WORKFLOW"):
                positions = [(20, y + 46), (180, y + 46), (20, y + 88)]
                row_h = 120
            elif category == "MOBILE":
                positions = [(20, y + 46), (180, y + 46)]
                row_h = 82
            else:  # DATABASES
                positions = [(20, y + 46)]
                row_h = 82

            for (label, icon), (ix, iy) in zip(items, positions):
                body += tool_item(label, icon, ix, iy, 12.5 if len(label) > 13 else 13.5, mobile=True)
        else:
            row_h = 70
            body += text(26, y + 27, category, 13, "mono", style=f"fill: {color}")
            for tool_index, (label, icon) in enumerate(items):
                col_x = desktop_cols[tool_index]
                body += tool_item(label, icon, col_x, y + 27, 14 if len(label) > 15 else 15, mobile=False)

        if index < len(TOOLS) - 1:
            body += f'<path d="M20 {y+row_h-12}H{w-20}" stroke="#8095b7" stroke-opacity=".18"/>'
        y += row_h

    desc = "Languages: Python, JavaScript, TypeScript, Dart. Frontend: React, Next.js, Tailwind CSS. Backend: Django, Node.js, Express. Mobile: Flutter, Provider. Databases: MySQL. Systems and APIs: REST APIs, WebSockets, authentication, role-based access. Workflow: Git, GitHub, GitHub Actions."
    return premium(w, h, "Technology toolkit", desc, body, "#8bb9ff", "#b49bf7", "#111928")


def render_footer(mobile=False):
    w, h = (360, 76) if mobile else (960, 82)
    body = '<style>.surface { fill: #111a2b; } .border { stroke: none; }</style>'
    body += f'<path d="M0 1H{w}" stroke="#8bb9ff" stroke-opacity=".25"/>'
    body += text(4, 38, "Mubasheer KC", 22 if mobile else 26, "title")
    if not mobile:
        body += text(w - 4, 38, "Thoughtful interfaces. Connected experiences.", 15, "muted", text_anchor="end")
    else:
        body += text(4, 64, "Built with care. Always improving.", 13, "muted")
    return svg(w, h, "Mubasheer KC", "Built with care. Always improving.", body)


def main():
    for mobile in (False, True):
        suffix = "-mobile" if mobile else ""
        write(f"assets/header{suffix}.svg", render_header(mobile))
        write(f"assets/footer{suffix}.svg", render_footer(mobile))
        write(f"assets/ui/profile-signal{suffix}.svg", render_profile(mobile))
        write(f"assets/ui/now{suffix}.svg", render_now(mobile))
        write(f"assets/ui/toolkit{suffix}.svg", render_toolkit(mobile))
        for index, (title, meta, kind, accent) in enumerate(SECTIONS, 1):
            write(f"assets/ui/section-{index:02}{suffix}.svg", render_section(index, title, meta, kind, accent, mobile))

        # Primary Portfolio CTA (Hero)
        write(f"assets/cta/visit-portfolio{suffix}.svg", render_portfolio_hero(mobile))

        # Secondary Navigation Cards
        write(f"assets/cta/explore-work{suffix}.svg", render_nav_card("Explore My Work ↗", "Projects, systems & products I've built.", "work", "#8bb9ff", "#b49bf7", mobile))
        write(f"assets/cta/chat-with-me{suffix}.svg", render_nav_card("Let's Connect ↗", "Have an idea? I'd love to hear it.", "connect", "#b29bf7", "#8bb9ff", mobile))

        # Compact Contact Cards
        write(f"assets/ui/contact-email{suffix}.svg", render_contact_card("Email Me", "Direct professional contact.", "mail", "#f0cf85", mobile))
        write(f"assets/ui/contact-linkedin{suffix}.svg", render_contact_card("LinkedIn", "Connect professionally.", "linkedin", "#8bb9ff", mobile))
        write(f"assets/ui/contact-portfolio{suffix}.svg", render_contact_card("Visit Portfolio", "Explore my work.", "globe", "#b29bf7", mobile))


if __name__ == "__main__":
    main()
