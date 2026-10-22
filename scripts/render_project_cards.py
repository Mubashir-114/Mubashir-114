#!/usr/bin/env python3
"""Render compact project cards. Verification: docs/profile-audit.md."""
import base64
from profile_svg import ROOT, CYAN, VIOLET, svg, text, write

PROJECTS = [
    dict(slug="fintrack", name="FinTrack 2.0", logo="fintrack-2.png", repo="fintrack_app", case="fintrack-2",
         status="Active development", tagline="Personal finance, thoughtfully connected.",
         mobile=["Personal finance,", "thoughtfully connected."],
         stack="Flutter / Dart / Node.js / Express / MySQL", accent=CYAN),
    dict(slug="kodehax", name="kodehax academy", logo="kodehax.png", repo="kodehax_academy", case="kodehax-academy",
         status="Implemented learning workflows", tagline="A place to learn, practice and build.",
         mobile=["A place to learn,", "practice and build."],
         stack="Python / Django / MySQL / Tailwind CSS / Groq", accent=VIOLET),
    dict(slug="provia", name="Provia", logo="provia.png", repo="Provia", case="provia",
         status="Active development / mock checkout", tagline="Service discovery meets connected booking.",
         mobile=["Service discovery meets", "connected booking."],
         stack="Python / Django / MySQL / Channels / Daphne", accent="#d8cba5"),
    dict(slug="nexo", name="Nexo", logo="nexo.svg", repo="Nexo-frontend", case="nexo",
         status="Frontend demo / mock AI", tagline="Conversations, documents and projects. Together.",
         mobile=["Conversations, documents", "and projects. Together."],
         stack="React / Vite / Zustand / Framer Motion", accent="#abc5eb"),
]


def logo_data_uri(filename):
    path = ROOT / "assets/projects/logos" / filename
    mime = "image/svg+xml" if path.suffix == ".svg" else "image/png"
    return f"data:{mime};base64,{base64.b64encode(path.read_bytes()).decode('ascii')}"


def render_card(project, mobile=False):
    width, height = (360, 204) if mobile else (760, 156)
    pad = 20 if mobile else 28
    name_y = 65 if mobile else 67
    body = f'<path d="M{pad} 1H{pad+68}" stroke="{project["accent"]}" stroke-width="2"/>'
    body += text(pad, 29, project["status"], 11 if mobile else 12, "accent")
    body += f'<rect x="{pad}" y="{name_y-25}" width="30" height="30" rx="6" fill="#181818"/>'
    body += f'<image href="{logo_data_uri(project["logo"])}" x="{pad+3}" y="{name_y-22}" width="24" height="24" preserveAspectRatio="xMidYMid meet"/>'
    body += text(pad+42, name_y, project["name"], 28 if mobile else 30, "title")
    if mobile:
        for index, line in enumerate(project["mobile"]):
            body += text(pad, 101+index*21, line, 16)
        stack = project["stack"].split(" / ")
        split = 3 if project["slug"] == "fintrack" else 2
        for index, line in enumerate([" / ".join(stack[:split]), " / ".join(stack[split:])]):
            body += text(pad, 159+index*20, line, 12, "muted")
    else:
        body += text(pad, 100, project["tagline"], 18)
        body += text(pad, 131, project["stack"], 13, "muted")
        body += text(width-pad, 31, "VIEW SOURCE  ↗", 11, "mono", text_anchor="end")
    desc = f'{project["name"]}. {project["status"]}. {project["tagline"]} {project["stack"]}.'
    return svg(width, height, project["name"], desc, body)


def render_mobile_card(project):
    return render_card(project, mobile=True)


def main():
    for project in PROJECTS:
        write(f'assets/projects/{project["slug"]}.svg', render_card(project))
        write(f'assets/projects/{project["slug"]}-mobile.svg', render_mobile_card(project))


if __name__ == "__main__":
    main()
