import os
import requests

# List of icon names
icons = [
    "astro","bash","blender","c","cpp","cloudflare","deno","discordjs","docker",
    "git","github","gradle","java","js","linux","netlify","markdown","ps","py",
    "raspberrypi","replit","vercel","vscode","windows"
]

icon_folder = os.path.join("assets", "icons")
font_folder = os.path.join("assets", "fonts", "work-sans")
os.makedirs(icon_folder, exist_ok=True)
os.makedirs(font_folder, exist_ok=True)

# Download icons
for icon in icons:
    url = f"https://skillicons.dev/icons?i={icon}&theme=dark"
    dest = os.path.join(icon_folder, f"{icon}.svg")
    print(f"Downloading {icon} icon...")
    r = requests.get(url)
    if r.ok:
        with open(dest, "wb") as f:
            f.write(r.content)
    else:
        print(f"Failed to download {icon}")

# Download Work Sans fonts (400 and 700, normal)
weights = [400, 700]
for weight in weights:
    font_url = f"https://cdn.jsdelivr.net/npm/@fontsource/work-sans/files/work-sans-latin-{weight}-normal.woff2"
    dest = os.path.join(font_folder, f"work-sans-latin-{weight}-normal.woff2")
    print(f"Downloading Work Sans {weight}...")
    r = requests.get(font_url)
    if r.ok:
        with open(dest, "wb") as f:
            f.write(r.content)
    else:
        print(f"Failed to download Work Sans {weight}")
print("Done.")