import re
import base64
import urllib.parse
from pathlib import Path

SVG_PATH = Path("test.svg")
ICON_DIR = Path("assets/icons")
FONT_DIR = Path("assets/fonts/work-sans")
OUTPUT_PATH = Path("test-embedded.svg")

# 1. Read SVG
svg = SVG_PATH.read_text(encoding="utf-8")

# 2. Embed icons as data URIs
def svg_to_data_uri(svg_path):
    svg_content = svg_path.read_text(encoding="utf-8")
    # URL-encode the SVG content for data URI
    data_uri = "data:image/svg+xml;utf8," + urllib.parse.quote(svg_content)
    return data_uri

def replace_icon(match):
    src = match.group(1)
    icon_path = ICON_DIR / Path(src).name
    if icon_path.exists():
        data_uri = svg_to_data_uri(icon_path)
        return f'src="{data_uri}"'
    else:
        print(f"Warning: Icon not found: {icon_path}")
        return match.group(0)

svg = re.sub(r'src="assets/icons/([^"]+\.svg)"', replace_icon, svg)

# 3. Embed fonts as base64 data URIs in @font-face
def font_to_data_uri(font_path):
    font_bytes = font_path.read_bytes()
    b64 = base64.b64encode(font_bytes).decode("ascii")
    return f"data:font/woff2;base64,{b64}"

def embed_font_face_block(svg, font_dir):
    def font_face_replacer(match):
        weight = match.group("weight")
        style = match.group("style")
        font_file = font_dir / f"work-sans-latin-{weight}-{style}.woff2"
        if font_file.exists():
            data_uri = font_to_data_uri(font_file)
            return (
                f"@font-face {{\n"
                f"  font-family: 'Work Sans';\n"
                f"  src: url('{data_uri}') format('woff2');\n"
                f"  font-weight: {weight};\n"
                f"  font-style: {style};\n"
                f"}}"
            )
        else:
            print(f"Warning: Font not found: {font_file}")
            return match.group(0)

    # Regex for @font-face blocks for Work Sans
    font_face_pattern = re.compile(
        r"@font-face\s*{\s*font-family:\s*'Work Sans';\s*src:\s*url\([^)]+\)\s*format\('woff2'\);\s*font-weight:\s*(?P<weight>\d+);\s*font-style:\s*(?P<style>\w+);\s*}",
        re.MULTILINE,
    )
    return font_face_pattern.sub(font_face_replacer, svg)

svg = embed_font_face_block(svg, FONT_DIR)

# 4. Write output
OUTPUT_PATH.write_text(svg, encoding="utf-8")
print(f"Embedded SVG written to {OUTPUT_PATH}")