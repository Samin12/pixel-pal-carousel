"""Build repeatable Pixel-Pal image prompts from editable project.json. No API calls."""
from pathlib import Path
import json

ROOT = Path(__file__).resolve().parent
project = json.loads((ROOT / "project.json").read_text())
style = """STYLE BLOCK (keep identical across the deck):
Design system: clean modern educational carousel. Signature orange #FF5C1F is the single hero accent. Cute chunky 8-bit PIXEL-ART blob mascot — solid orange #FF5C1F body, darker-orange pixel shading on lower-left edges, two square black pixel eyes, stubby pixel arms/feet, no mouth, crisp hard pixel edges, no gradients on the character, retro game-sprite look. Same mascot identity on every slide."""

(ROOT / "prompts").mkdir(exist_ok=True)
requests = []
plan = ["# One question. A week's content.", "", "Seven-slide example for Samin's Content Systems. Generated with the repository's Pixel-Pal design system.", "", "Live model constraints require 3:4 portrait; do not submit unsupported 4:5. No invented customers, metrics or operational integration claims.", ""]
for s in project["slides"]:
    prompt = f"Instagram / LinkedIn carousel slide, portrait 3:4, flat editorial graphic-design layout — {s['archetype']} slide.\n\n{style}\n\n"
    if s["archetype"] == "HOOK":
        l1, l2, l3 = s["headline"].splitlines()
        prompt += f'''Background: near-black #0A0A0A with a faint low-opacity pixel-art night room (window, pixel moon, distant city lights), moody.
Headline in a warm SERIF, top-left, 3 lines: line1 "{l1}" in cream #F5F2ED, line2 "{l2}" in orange #FF5C1F about 1.6x larger, line3 "{l3}" in cream #F5F2ED — all spelled exactly, verbatim. A hand-drawn cream double-underline scribble beneath line3.
Small handwritten cream sub-line "{s['body']}" with a curved hand-drawn cream arrow pointing toward the mascot.
Mascot bottom-right, {s['pose']}, warmly lit.
A small white ">" chevron in a faint circle centered on the right edge (carousel nav).
'''
    else:
        prompt += f'''Background: pure white #FFFFFF.
Top-left section chip: pale-peach #FFF3E9 rounded pill with orange #FF5C1F "{s['number']:02d}" then dark-gray "{s['label']}" — spelled exactly, verbatim.
Headline in HEAVY BOLD SANS, ink black #111111, top-left: "{s['headline']}" with the word "{s['orange']}" in orange #FF5C1F — spelled exactly, verbatim.
Body, warm gray #5A5A5A, medium weight: "{s['body']}" — spelled exactly, verbatim.
Illustration anchored lower-center/side: the orange pixel blob mascot {s['pose']}.
'''
        if s.get("diagramLabels"):
            prompt += "All diagram labels, spelled exactly, verbatim: " + ", ".join(f'"{x}"' for x in s["diagramLabels"]) + ".\n"
        if s.get("bubble"):
            prompt += f'''Rounded white speech bubble with a tail: "{s['bubble']}" (the word "inquiries" in orange), spelled exactly, verbatim.\n'''
        if s.get("button"):
            prompt += f'''Above the illustration, a prominent solid-orange rounded call-to-action panel reads "{s['button']}" in white bold sans — spelled exactly, verbatim. Do not draw a URL or QR code.\n'''
        prompt += f'''Bottom pale-peach #FFF3E9 rounded tip-box, full width, small orange 8-point spark icon at left, text "{s['tip']}" — spelled exactly, verbatim.
Small gray ">" chevron nav dot centered on the right edge.
'''
    prompt += f'''\nSmall but clearly legible brand credit on the bottom margin: "{project['brand']}" — spelled exactly, verbatim. Keep that exact brand name on one line. No other brand names.
Layout: 8% safe side margins; comfortable top and bottom margins. Headline in the upper third; body below; illustration below the body; tip-box near bottom above the brand. Large type, readable at phone size. Preserve generous white space. Diagram labels should remain large and high contrast. No overlaps or crowded elements.
Typography crisp and legible, high contrast, no watermark, no gibberish text, no extra UI, professional graphic design.
'''
    path = ROOT / "prompts" / f"slide-{s['number']:02d}.txt"
    path.write_text(prompt)
    requests.append({"index": s["number"], "params": {"model": project["format"]["model"], "aspect_ratio": project["format"]["aspectRatio"], "resolution": project["format"]["resolution"], "quality": project["format"]["quality"], "prompt": prompt}})
    plan.extend([f"## {s['number']:02d} - {s['label']} ({s['archetype']})", "", s["headline"].replace("\n", " / "), "", f"Orange emphasis: {s['orange']}", "", s["body"], "", f"Illustration: {s['pose']}", "", f"Tip: {s['tip']}".rstrip(), ""])
(ROOT / "requests.json").write_text(json.dumps({"requests": requests}, indent=2, ensure_ascii=False) + "\n")
(ROOT / "slide-plan.md").write_text("\n".join(plan))
(ROOT / "caption.txt").write_text(project["caption"] + "\n")
print(f"Built {len(requests)} prompts with one shared style block.")
