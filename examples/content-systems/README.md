# Samin's Content Systems: Pixel-Pal example

Seven finished portrait slides demonstrating a customer question becoming a repeatable content workflow and an invitation to book a conversation.

## Review and downloads

Open `index.html` in a browser to view every slide, copy the caption, or edit the source copy locally. `preview.png` is the contact sheet. `slides.zip` contains the seven original PNG exports. `carousel.pdf` contains all seven slides; its final page links to Samin's booking page.

Booking target: https://calendly.com/samin-dde/lets-see-what-ai-can-do-for-you

The PNGs are flattened generated artwork. The editable project is `project.json`, with literal slide copy, art direction, alt text, format, and caption. Its prompts can be edited and regenerated with the repository's workflow. This is not a layered Figma, Canva, or PowerPoint file. The browser editor downloads changes to JSON; it does not claim to edit text inside the existing PNGs.

## Source and workflow

- Repository: https://github.com/Samin12/pixel-pal-carousel
- Base commit: `2c53e9ef47fb90f76caeeb0eaace7f04f2cb3ed4`
- Review branch: `codex/content-systems-example`
- Original design rules: repository `SKILL.md` and `references/design-system.md`
- Engine used: Higgsfield connector, `gpt_image_2`, 2k, high quality.
- Format: live model metadata supports 3:4, not 4:5. Native output dimensions are recorded in `manifest.json`; original pixels are preserved.
- One generation per slide; at most four concurrent image jobs.

Edit `project.json`, then run these from this directory:

```bash
python3 build_prompts.py
python3 build_review.py
```

`prompts/slide-01.txt` through `slide-07.txt` are the full prompts. `requests.json` contains the exact connector request structure. The style block is identical across all slides and comes from the repository's locked template.

To regenerate one affected slide using an already authenticated Higgsfield CLI:

```bash
higgsfield generate create gpt_image_2 --aspect_ratio 3:4 --resolution 2k --quality high --wait < prompts/slide-02.txt
```

Generation uses your account's allowance or credits. This example does not embed credentials or run generation on page load. Inspect the new result before replacing its corresponding file in `slides/`.

After all seven approved PNGs are present, package them with:

```bash
python3 export.py --output /absolute/path/to/new-deliverables
```

The exporter requires Pillow, reportlab, and pypdf. It preserves original PNGs, assembles a contact sheet, creates the linked PDF, and records SHA-256 checksums. It performs no generation or publishing.

## Editorial boundaries

This is example marketing content, not a report of live customer results. No customers, testimonials, prices, guarantees, account metrics, or working-integration claims are invented. The conceptual Inquiry → Booked call path is an invitation flow, not a conversion promise. The carousel has not been published to social media.

The opening render includes a supporting footer: “Customer questions are content gold. One question can fuel posts, emails, videos and more.” This extra generated copy was reviewed for relevance and accuracy. The exact original generation request remains in `prompts/slide-01.txt`.

Final visual checks and technical evidence are recorded in `verification.json` and `manifest.json`.
