# Brand research

The skill provides no styling defaults. Every report's visual identity is built from the brand's own design language, discovered fresh per build. This document is how to do that research efficiently.

## Goal

Come out of Step 3 with answers to these six questions:

1. **Logo** — what is the visual mark? Wordmark? Symbol? Combination?
2. **Primary palette** — what colour(s) dominate the brand's marketing? Is the brand colour used as a *fill* (the colour is the brand — full-bleed backgrounds, banner wordmarks) or as an *accent* (the brand colour appears sparingly against a stark base)?
3. **Secondary palette** — what supporting colours, neutrals, foils?
4. **Typography character** — heritage serif? Geometric sans? Bold display? Hand-written? What free Google Fonts equivalents would you reach for?
5. **Visual treatment** — photo-led? Type-led? Illustration-led? Maximalist? Minimal? Photographic mood (warm, cool, saturated, muted)?
6. **Aesthetic family** — one named category you commit to.

## Sources, in order

### 1. The brand's primary website

`web_fetch` on the brand's homepage. Look in the returned HTML for:

- **CSS variables** — `--color-primary`, `--brand-red`, `--font-display` etc. tell you what the brand's own designers consider canonical.
- **Inline `<style>` blocks** — frequently-used hex codes, font-family declarations.
- **`<link>` tags for Google Fonts** — direct read of the brand's chosen typefaces.
- **`<img>` and `<svg>` tags for logos** — capture the SVG markup if you can; it tells you the wordmark's shape and weight.
- **Hero copy and headline treatment** — is the brand all-caps and assertive, or sentence-case and conversational?

If the site is JS-rendered and `web_fetch` returns very little, do not panic — fall through to source 2.

### 2. Brand image search

`image_search` with these queries (run in parallel):

- `"<brand> logo"` — capture the wordmark's letterforms and primary colour
- `"<brand> packaging"` — see the brand colour in its native context
- `"<brand> advertising campaign"` — read the brand's photographic/illustrative style
- `"<brand> billboard"` or `"<brand> instagram"` — current marketing tone

You're not trying to copy these images. You're trying to *understand* the brand's visual mood so the report feels like it could have come from the same studio.

### 3. Brand colour reference sites

For verified hex codes, sites like `logos-world.net`, `brandcolorcode.com`, `brandfetch.com` are useful triangulation. Don't rely on a single source — cross-check at least two.

### 4. Wikipedia / brand history

A 30-second skim of the brand's Wikipedia entry tells you the founding year, the heritage story, the recent positioning shifts. Heritage brands (founded 18th or 19th century — spirits, sauces, banking, fashion houses) often want their heritage *visible* in any branded artifact. Modern challenger brands (founded post-2010 — DTC products, supplements, drinks startups) often want the opposite.

## Aesthetic family — a checklist of options

Pick one and commit. Do not pick "modern minimal" as a default — that is a non-answer that produces generic output. Some genuine options:

- **Heritage spirits magazine** — warm cream paper, serif display, drop caps, foil-coloured rules, asymmetric editorial spreads. Suits heritage drinks brands, premium spirits, vintage-positioned products.
- **Athletic sportswear** — stark black/white base with one electric accent colour, bold condensed sans-serif, KPI-grid layouts, outline-stroke headlines. Suits athletic apparel, performance equipment, gym/fitness brands.
- **Technical / clinical** — white background, monospace or grotesk type, data-heavy, scientific diagrams. Suits supplements, wearables, medical/scientific brands.
- **Club / nightlife** — saturated brand colour, high contrast, big bold display, photographic energy. Suits energy drinks, premium spirits with party positioning, nightlife brands.
- **Hospitality / luxury** — generous whitespace, refined serif, gold/champagne accents, restrained palette. Suits luxury hotels, premium spirits, fashion houses.
- **Outdoor adventure** — earth tones, sans body with display serif accent, photographic full-bleed. Suits outdoor apparel, expedition gear, lifestyle brands.
- **Food / kitchen** — warm tones, ingredient photography, generous photography, friendly serif. Suits cooking brands, sauces, baking ingredients.
- **Festival / colour-block** — vibrant multi-colour palette, geometric shapes, playful display sans. Suits seltzer brands, energy drinks, youth products.
- **Brutalist / raw** — exposed type, monochrome with one harsh accent, geometric blocks. Suits avant-garde fashion, art houses, design-led startups.
- **Retro / vintage** — period-specific palette and type (mid-century, 70s, 90s). Suits brands actively trading on nostalgia.
- **Newspaper / editorial** — masthead, double rules, drop caps, pull quotes, serif body. Suits journalistic brands, financial publications, premium B2B.

If none of these fits, describe a new one in two or three words. Don't default.

## What to write down before Step 4

Capture this in a short Markdown block before going to user confirmation:

```
Brand: <brand>
Aesthetic family: <one named category>
Primary palette: <hex> (used as <fill | accent | texture>)
Secondary palette: <hex>, <hex>, <hex>
Typography: <display font>, <body font>, <labels font>
Visual treatment: <layout philosophy in one phrase>
Tone: <2-3 word characterisation>
```

Bring this into Step 4 and confirm with the user before writing any HTML.
