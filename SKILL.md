---
name: pixel-pal-carousel
description: >
  Create Instagram/LinkedIn educational carousels in the "Pixel-Pal" design system —
  an orange 8-bit pixel-art blob mascot, a dark serif HOOK slide + white bold-sans
  INTERIOR slides, numbered section chips, hand-drawn accents (underline scribble,
  curved arrow), cream "tip" callout footers, and an edge chevron nav dot. Use when
  the user asks to make a carousel "in this design/format", references the pixel
  mascot / popcorn-blob style, or wants an educational slide deck about an AI / tech
  / how-to topic in Samin's channel aesthetic. Renders each slide with GPT Image 2.0
  (gpt_image_2) at 4:5 (1080x1350). One generate call per slide, run in parallel.
---
# Pixel-Pal Carousel

An educational-carousel design system reverse-engineered from a high-performing
reference deck. Orange pixel-art mascot + clean editorial typography + hand-drawn
accents. Legible, scroll-stopping, and repeatable slide-to-slide.

> READ `references/design-system.md` FIRST — it is the source of truth for the exact
> hex palette, the two slide archetypes, the mascot spec, the accent library, and
> the locked prompt template. This SKILL.md is the workflow; that file is the look.

## When to use
- "Make a carousel in this design/format" (with the pixel-blob reference)
- Educational / how-to / product-launch / explainer carousels for IG or LinkedIn
- Any deck that should match Samin's channel: clean, light, orange accent, playful mascot

## Model & format (LOCKED)
- **Model:** `gpt_image_2` (GPT Image 2.0). It is the ONLY model here — it renders
  exact text, layout, and typography. Never substitute Soul/Nano/Seedream for
  text-heavy slides.
- **Aspect ratio:** `gpt_image_2` does NOT support 4:5, so use `3:4` (its closest
  supported portrait ratio) for IG carousels. (Use `1:1` only if the user explicitly
  wants square.)
- **One `higgsfield_generate_image` call per slide.** For an N-slide deck, fire N
  calls IN PARALLEL (respect the workspace text2image concurrency cap — default 4;
  submit ≤cap, poll `higgsfield_job_status` to terminal, then submit the next batch).

## Workflow

1. **Get the content.** From the user's topic, transcript, URL, or notes. If a
   YouTube URL is given, pull the transcript/metadata (youtube-content /
   youtube-research / video_analyze) for concrete facts and talking points.

2. **Write the slide plan** (before any image). Decide slide count (5-7 is the sweet
   spot) and for EACH slide draft: archetype (HOOK vs INTERIOR vs CTA), section chip
   number+label, headline (mark which ONE word/phrase is orange), body copy, mascot
   pose+props, and any tip-box / speech-bubble text. Keep ONE idea per slide.
   Slide 1 is ALWAYS the dark serif HOOK. Last slide is usually a CTA/recap.

3. **Build each prompt** from the LOCKED template in `references/design-system.md`.
   Fill the placeholders; do NOT paraphrase the style block — it must be byte-stable
   across slides so the mascot and palette stay consistent. Put every literal string
   the slide must show in "double quotes" and add "spelled exactly, verbatim".

4. **Generate** all slides in parallel with `gpt_image_2`, `aspect_ratio:"4:5"`.
   Call `higgsfield_generate_models_explore(action='get', model_id='gpt_image_2')`
   once first if you need live params.

5. **QC pass (MANDATORY).** When jobs finish, run `image_analyze` on the full set
   and check: (a) every headline word spelled correctly, (b) the orange word is the
   RIGHT word, (c) mascot is consistent orange pixel-art across slides, (d) section
   chip numbers are sequential, (e) no cropped text, (f) tip-box present where
   planned. Regenerate any slide that fails (retry same prompt once; then simplify).

6. **Deliver.** `higgsfield_upload` every final slide and present them in order as
   MEDIA:<url>, slide 1 → N. Offer the caption + hook line.

## Pitfalls
- GPT Image sometimes renders long body paragraphs with typos — keep body copy short
  (≤ 2 short sentences) and always QC + regenerate.
- If the mascot drifts in color/style between slides, restate the mascot spec block
  verbatim and add "identical 8-bit pixel-art orange blob mascot as the other slides".
- Don't put more than ~7 words in a headline — it shrinks and loses impact.
- Keep exactly ONE accent color per slide besides orange (the reference uses blue
  ONLY for the "pictures/words" idea). Orange is the primary accent everywhere.
- The dark HOOK slide uses a SERIF headline; interior slides use BOLD SANS. Do not mix.

