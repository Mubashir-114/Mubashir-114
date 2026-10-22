#!/usr/bin/env python3
"""Render expressive project-owned cards with verified scope and source links.

V3 selectively restores the original accent rails, feature chips and larger
cards. Canonical repository/case-study links remain native README anchors.
"""
from profile_svg import image_uri, premium, text, write

PROJECTS = [
    dict(slug="fintrack", name="FinTrack 2.0", logo="fintrack-jade.png", repo="fintrack_app", case="fintrack-2",
         category="CONNECTED FINANCE", status="Active development", accent="#65e1ad", secondary="#2ba889", base="#0c1b1a",
         description=["A connected personal-finance app for accounts, budgets,", "reports and the deterministic FIN companion."],
         mobile=["Accounts, budgets and reports,", "connected to a deterministic FIN."],
         stack="Flutter / Dart / Node.js / Express / MySQL", mobile_stack=["Flutter / Dart / Node.js", "Express / MySQL"],
         highlights=["MULTI-ACCOUNT LEDGER", "LIVING BUDGETS", "DETERMINISTIC FIN"], short=["LEDGER", "BUDGETS", "FIN"]),
    dict(slug="kodehax", name="kodehax academy", logo="kodehax-color.png", repo="kodehax_academy", case="kodehax-academy",
         category="DEVELOPER EDUCATION", status="Learning workflows implemented", accent="#70baff", secondary="#b086ff", base="#111a30",
         description=["A role-aware learning platform for classrooms, coding", "challenges, assessments and Groq-assisted tutoring."],
         mobile=["Classrooms, coding challenges", "and Groq-assisted learning."],
         stack="Python / Django / MySQL / Tailwind CSS / Groq", mobile_stack=["Python / Django / MySQL", "Tailwind CSS / Groq"],
         highlights=["ROLE WORKFLOWS", "CODING PRACTICE", "GROQ TUTORING"], short=["ROLES", "PRACTICE", "GROQ"]),
    dict(slug="provia", name="Provia", logo="provia.png", repo="Provia", case="provia",
         category="SERVICE MARKETPLACE", status="Active development / mock checkout", accent="#f3cf69", secondary="#c39337", base="#211b11",
         description=["Service discovery and booking workflows, connected", "through real-time customer-provider communication."],
         mobile=["Service discovery, booking", "and customer-provider chat."],
         stack="Python / Django / MySQL / Channels / Daphne", mobile_stack=["Python / Django / MySQL", "Channels / Daphne"],
         highlights=["BOOKING LIFECYCLE", "WEBSOCKET CHAT", "MOCK CHECKOUT"], short=["BOOKING", "CHAT", "MOCK PAY"]),
    dict(slug="nexo", name="Nexo", logo="nexo.svg", repo="Nexo-frontend", case="nexo",
         category="PRODUCTIVITY WORKSPACE", status="Frontend demonstration / mock AI", accent="#8aaeff", secondary="#ba8bfa", base="#17152c",
         description=["A React workspace for conversations, documents and", "projects, built around domain-specific Zustand stores."],
         mobile=["Conversations, documents", "and projects in one workspace."],
         stack="React / Vite / Zustand / Framer Motion", mobile_stack=["React / Vite / Zustand", "Framer Motion"],
         highlights=["WORKSPACE STATE", "DOCUMENTS + PROJECTS", "MOCK RESPONSES"], short=["STATE", "PROJECTS", "MOCK AI"]),
]


def render_card(project, mobile=False, index=1):
    w,h = (360,350) if mobile else (960,324)
    pad = 20 if mobile else 32
    color = project["accent"]
    logo_x,logo_y,logo_size = (278,51,62) if mobile else (790,43,120)
    body = text(pad,30 if mobile else 33,f'{index:02} / {project["category"]}',11 if mobile else 13,"label")
    body += f'<rect x="{logo_x-7}" y="{logo_y-7}" width="{logo_size+14}" height="{logo_size+14}" rx="{16 if mobile else 26}" fill="{color}" fill-opacity=".06" stroke="{color}" stroke-opacity=".2"/>'
    body += f'<image href="{image_uri("assets/projects/logos/"+project["logo"])}" x="{logo_x}" y="{logo_y}" width="{logo_size}" height="{logo_size}" preserveAspectRatio="xMidYMid meet"/>'
    body += text(pad,81 if mobile else 87,project["name"],27 if mobile else 39,"title",font_weight="600")
    lines = project["mobile"] if mobile else project["description"]
    for line_index,line in enumerate(lines):
        body += text(pad,(147 if mobile else 126)+line_index*(25 if mobile else 27),line,17 if mobile else 20)
    if mobile:
        for line_index,line in enumerate(project["mobile_stack"]):
            body += text(pad,210+line_index*22,line,14,"muted")
    else:
        body += text(pad,194,project["stack"],16,"muted")
    x=pad
    for label in (project["short"] if mobile else project["highlights"]):
        size=12 if mobile else 13
        width=len(label)*(7 if mobile else 8)+26
        y=252 if mobile else 218
        body += f'<rect x="{x}" y="{y}" width="{width}" height="30" rx="7" fill="{color}" fill-opacity=".07" stroke="{color}" stroke-opacity=".23"/>'
        body += text(x+width/2,y+20,label,size,"body",text_anchor="middle")
        x+=width+8
    line_y = 302 if mobile else 274
    body += f'<path d="M{pad} {line_y}H{w-pad}" stroke="{color}" stroke-opacity=".2"/>'
    body += text(pad,line_y+27,project["status"],12.5 if mobile else 14,"accent")
    if not mobile:
        body += text(w-pad,line_y+27,"VIEW REPOSITORY  ↗",13,"accent",text_anchor="end")
    desc=f'{project["name"]}. {" ".join(project["description"])} {project["stack"]}. {project["status"]}.'
    return premium(w,h,project["name"],desc,body,color,project["secondary"],project["base"])


def render_mobile_card(project,index=1):
    return render_card(project,True,index)


def main():
    for index,project in enumerate(PROJECTS,1):
        write(f'assets/projects/{project["slug"]}.svg',render_card(project,index=index))
        write(f'assets/projects/{project["slug"]}-mobile.svg',render_mobile_card(project,index))


if __name__ == "__main__":
    main()
