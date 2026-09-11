"""Package approved generated PNGs. Never crops or alters the slide artwork.

Dependencies: Pillow, reportlab, pypdf. The project uses GPT Image 2 through Higgsfield.
This exporter needs no network, API key or image-generation account.
"""
from pathlib import Path
import argparse
import hashlib
import json
import shutil
import zipfile
from PIL import Image, ImageDraw, ImageFont
from reportlab.pdfgen import canvas
from pypdf import PdfReader

ROOT = Path(__file__).resolve().parent
parser = argparse.ArgumentParser()
parser.add_argument("--output", type=Path, required=True)
args = parser.parse_args()
out = args.output.resolve()
out.mkdir(parents=True, exist_ok=True)
project = json.loads((ROOT / "project.json").read_text())
slides = [ROOT / "slides" / f"slide-{s['number']:02d}.png" for s in project["slides"]]
assert len(slides) == 7 and all(p.exists() for p in slides), "Seven final slide PNGs are required."
dimensions = [Image.open(p).size for p in slides]
assert len(set(dimensions)) == 1, "Slide dimensions must match."
width, height = dimensions[0]
assert abs(width / height - 0.75) < 0.005, "Expected portrait 3:4 model output."

# Copy source and originals into the deliverable. Keep exports byte-identical.
for name in ["project.json", "requests.json", "caption.txt", "slide-plan.md", "index.html", "build_prompts.py", "build_review.py", "export.py", "README.md", "verification.json"]:
    path = ROOT / name
    if path.exists():
        shutil.copy2(path, out / name)
for dirname in ["prompts", "slides"]:
    shutil.copytree(ROOT / dirname, out / dirname, dirs_exist_ok=True)
with zipfile.ZipFile(out / "slides.zip", "w", zipfile.ZIP_DEFLATED) as archive:
    for path in slides:
        archive.write(path, path.name)

# A standard image-page PDF preserves the original complete composition.
pw, ph = 540, 540 * height / width
pdf_path = out / "carousel.pdf"
c = canvas.Canvas(str(pdf_path), pagesize=(pw, ph))
c.setTitle(project["title"])
c.setAuthor(project["brand"])
c.setSubject("Seven-slide Pixel-Pal example; booking CTA links to Samin's verified Calendly page.")
for s, path in zip(project["slides"], slides):
    c.bookmarkPage(f"slide-{s['number']}")
    c.addOutlineEntry(f"{s['number']:02d} - {s['label']}", f"slide-{s['number']}")
    c.drawImage(str(path), 0, 0, width=pw, height=ph)
    if s["number"] == 7:
        c.linkURL(project["bookingUrl"], (0, 0, pw, ph), relative=0, thickness=0)
    c.showPage()
c.save()
pdf = PdfReader(str(pdf_path))
assert len(pdf.pages) == 7
uris = [a.get_object().get("/A", {}).get("/URI") for a in pdf.pages[-1].get("/Annots", [])]
assert project["bookingUrl"] in uris

# Contact sheet: thumbnail packaging only; exported slide artwork is unchanged.
thumb_w = 430
thumb_h = round(thumb_w * height / width)
pad, gap, title_h, label_h = 40, 24, 130, 35
sheet_w = pad * 2 + thumb_w * 4 + gap * 3
sheet_h = title_h + 2 * (thumb_h + label_h + gap) + pad
sheet = Image.new("RGB", (sheet_w, sheet_h), "#F5F2ED")
draw = ImageDraw.Draw(sheet)
font_path = "/System/Library/Fonts/Supplemental/Arial.ttf"
try:
    title_font = ImageFont.truetype(font_path, 43)
    label_font = ImageFont.truetype(font_path, 20)
    sub_font = ImageFont.truetype(font_path, 24)
except OSError:
    title_font = label_font = sub_font = ImageFont.load_default()
draw.text((pad, 24), "One question. A week's content.", fill="#111111", font=title_font)
draw.text((pad, 80), "Samin's Content Systems  /  7-slide Pixel-Pal example", fill="#5A5A5A", font=sub_font)
for i, (s, path) in enumerate(zip(project["slides"], slides)):
    x = pad + (i % 4) * (thumb_w + gap)
    y = title_h + (i // 4) * (thumb_h + label_h + gap)
    with Image.open(path) as img:
        sheet.paste(img.convert("RGB").resize((thumb_w, thumb_h), Image.Resampling.LANCZOS), (x, y))
    draw.text((x, y + thumb_h + 8), f"{s['number']:02d} / {s['label']}", fill="#5A5A5A", font=label_font)
x = pad + 3 * (thumb_w + gap)
y = title_h + thumb_h + label_h + gap
draw.rectangle((x, y, x + thumb_w, y + thumb_h), fill="#FF5C1F")
for j, line in enumerate(["A real question.", "One useful answer.", "A repeatable process.", "A clear invitation."]):
    draw.text((x + 28, y + 80 + 65 * j), line, fill="white", font=sub_font)
draw.text((x + 28, y + thumb_h - 65), "Review-ready example", fill="white", font=label_font)
sheet.save(out / "preview.png")

manifest = {"title": project["title"], "brand": project["brand"], "repository": project["repository"], "baseCommit": project["baseCommit"], "model": project["format"], "slideCount": 7, "nativeWidth": width, "nativeHeight": height, "formatNote": "Native model output for the supported 3:4 setting; no cropping or stretching.", "bookingUrl": project["bookingUrl"], "pdfPages": len(pdf.pages), "pdfBookingLinkVerified": True, "files": []}
for path in sorted(out.rglob("*")):
    if path.is_file() and path.name not in {"manifest.json", "source.zip", "complete-carousel.zip"}:
        manifest["files"].append({"path": str(path.relative_to(out)), "bytes": path.stat().st_size, "sha256": hashlib.sha256(path.read_bytes()).hexdigest()})
(out / "manifest.json").write_text(json.dumps(manifest, indent=2) + "\n")
print(json.dumps({"output": str(out), "slides": 7, "dimensions": dimensions[0], "pdfPages": 7, "bookingLinkVerified": True, "preview": str(out / "preview.png")}))
