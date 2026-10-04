"""Local-only static website and public-export boundary checks (stdlib only)."""
from html.parser import HTMLParser
from pathlib import Path
import re
import subprocess
import sys
import xml.etree.ElementTree as ET

ROOT = Path(__file__).resolve().parent
PUBLIC_FILES = (
    "index.html", "styles.css", "site.js", "favicon.svg", "robots.txt",
    "sitemap.xml", ".nojekyll", ".gitignore", "README.md", "validate_site.py",
    "assets/map.jpg", "assets/weather.jpg", "assets/places.jpg",
    "assets/replay.jpg", "assets/routes.jpg",
)

class PageParser(HTMLParser):
    def __init__(self):
        super().__init__()
        self.ids = set()
        self.links = []
        self.image_count = 0
        self.h1_count = 0
        self.translated_count = 0

    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        if "id" in attrs:
            assert attrs["id"] not in self.ids, "Duplicate element ID"
            self.ids.add(attrs["id"])
        self.h1_count += tag == "h1"
        self.translated_count += "data-en" in attrs
        if tag in ("a", "link", "script", "img"):
            target = attrs.get("href", attrs.get("src", ""))
            self.links.append(target)
        if tag == "img":
            self.image_count += 1
            assert attrs.get("alt") and attrs.get("data-en-alt"), "Missing bilingual image description"
            assert attrs.get("width") == "720" and attrs.get("height") == "1565"
            assert attrs["src"].startswith("assets/") and attrs["src"].endswith(".jpg")
        if tag == "script":
            assert attrs.get("src") == "site.js", "Only local scripts are allowed"

def main():
    for name in PUBLIC_FILES:
        assert (ROOT / name).is_file(), f"Missing export file: {name}"
    html = (ROOT / "index.html").read_text()
    page = PageParser()
    page.feed(html)
    assert page.h1_count == 1 and page.image_count == 5
    assert page.translated_count >= 50
    for target in page.links:
        if target.startswith("#"):
            assert target == "#" or target[1:] in page.ids, f"Broken anchor: {target}"
        elif not target.startswith("https://"):
            assert (ROOT / target).is_file(), f"Missing local resource: {target}"
        else:
            assert target.startswith(("https://github.com/suhyeonii/islo-website", "https://suhyeonii.github.io/islo-website/")) or target == "https://www.openstreetmap.org/copyright", "Unexpected external link"
    assert "개발 중" in html and "NOT YET RELEASED" in html and "snowly" in html
    assert "not implemented" in html and "no Garmin partnership" in html
    assert "img/" not in html and ".PNG" not in html
    ET.parse(ROOT / "sitemap.xml")
    ET.parse(ROOT / "favicon.svg")
    text_files = [name for name in PUBLIC_FILES if not name.endswith(".jpg")]
    for name in text_files:
        text = (ROOT / name).read_text()
        assert not re.search(r"(?:authKey|serviceKey|access_token)\s*[=:]\s*[^\s<&]+", text, re.I), name
        assert ("Secrets" + ".xcconfig") not in text and ("/" + "Users/") not in text, name
    size = sum((ROOT / name).stat().st_size for name in PUBLIC_FILES)
    assert size < 2_000_000, f"Website too large: {size} bytes"
    subprocess.run(["node", "--check", str(ROOT / "site.js")], check=True)
    print(f"PASS: {len(PUBLIC_FILES)} allowed public files; 5 optimized images; {size:,} bytes total")
    print("PASS: local resources, anchors, bilingual labels, development disclosures, company and export boundary")
    print("Avatar redaction requires visual inspection of the generated files before publication.")
    if "--list" in sys.argv:
        print("\n".join(PUBLIC_FILES))

if __name__ == "__main__":
    main()
