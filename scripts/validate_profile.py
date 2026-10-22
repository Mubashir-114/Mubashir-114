#!/usr/bin/env python3
"""Validate self-hosted references, SVG safety, data, and reproducible assets.

Uses only the standard library. Live link and browser checks are documented in
docs/profile-audit.md; they are separate from this deterministic offline check.
"""
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import unquote, urlsplit
import hashlib
import json
import re
import subprocess
import sys
import xml.etree.ElementTree as ET

ROOT = Path(__file__).resolve().parents[1]
SVG = "{http://www.w3.org/2000/svg}"


class References(HTMLParser):
    def __init__(self):
        super().__init__()
        self.urls = []
        self.ids = set()

    def handle_starttag(self, tag, attributes):
        attrs = dict(attributes)
        for key in ("href", "src", "srcset"):
            if key in attrs:
                self.urls.append(attrs[key])
        if "id" in attrs:
            self.ids.add(attrs["id"])
        if tag == "img":
            assert attrs.get("alt"), "README image needs alternative text"


def hashes():
    paths = [*ROOT.glob("assets/**/*.svg"), ROOT / "data/contributions.json",
             ROOT / ".github/workflows/update-profile-activity.yml"]
    return {str(p.relative_to(ROOT)): hashlib.sha256(p.read_bytes()).hexdigest() for p in paths}


def main():
    readme = (ROOT / "README.md").read_text(encoding="utf-8")
    refs = References()
    refs.feed(readme)
    refs.urls.extend(re.findall(r"(?<!!)\[[^\]]+\]\(([^)]+)\)", readme))
    for heading in re.findall(r"^## (.+)$", readme, re.M):
        refs.ids.add(re.sub(r"[^\w\- ]", "", heading.lower()).replace(" ", "-"))
    for url in refs.urls:
        parsed = urlsplit(url)
        assert parsed.scheme in ("", "https", "mailto"), f"Unexpected link scheme: {url}"
        if not parsed.scheme and parsed.path:
            target = (ROOT / unquote(parsed.path)).resolve()
            assert target.is_relative_to(ROOT) and target.is_file(), f"Missing local asset: {url}"
        if url.startswith("#"):
            assert url[1:] in refs.ids, f"Missing anchor: {url}"
        assert "budgetbee-app" not in url and "expense-manager-api" not in url, f"Use canonical link: {url}"
    assert "img.shields.io" not in readme, "Keep profile assets self-hosted"
    for path in ROOT.glob("assets/**/*.svg"):
        tree = ET.parse(path)
        root = tree.getroot()
        assert root.tag == SVG + "svg" and "viewBox" in root.attrib, path
        if "icons" not in path.parts and "logos" not in path.parts:
            assert root.find(SVG + "title") is not None, f"SVG title missing: {path}"
        ids = [node.attrib["id"] for node in root.iter() if "id" in node.attrib]
        assert len(ids) == len(set(ids)), f"Duplicate SVG IDs: {path}"
        for node in root.iter():
            tag = node.tag.rsplit("}", 1)[-1]
            assert tag not in {"script", "foreignObject", "animate", "animateTransform"}, f"Active SVG element in {path}"
            for attr, value in node.attrib.items():
                assert not attr.lower().startswith("on"), f"SVG event handler in {path}"
                if attr.rsplit("}", 1)[-1] == "href":
                    assert value.startswith(("data:image/", "#")), f"Remote SVG dependency in {path}"
    data = json.loads((ROOT / "data/contributions.json").read_text())
    assert sum(d["count"] for d in data["days"]) == data["total_contributions"]
    assert sum(d["count"] > 0 for d in data["days"]) == data["active_days"]
    assert data["range"]["end"] == data["days"][-1]["date"]
    before = hashes()
    for script, args in [("render_profile_ui.py", []), ("render_project_cards.py", []),
                         ("generate_activity.py", ["--from-cache"])]:
        subprocess.run([sys.executable, str(ROOT / "scripts" / script), *args], check=True, capture_output=True)
    assert hashes() == before, "Generated assets differ from their generator output"
    print(f"PASS: {len(set(refs.urls))} references; all SVG XML and safety checks; contribution totals; deterministic generators; cache and workflow unchanged")


if __name__ == "__main__":
    main()
