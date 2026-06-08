---
name: meltwater-brand
description: >
  Apply Meltwater's 2025 brand guidelines when creating any presentation, slide deck, artifact, visual asset, or branded document. Trigger this skill whenever the user asks for a Meltwater-branded presentation, deck, one-pager, executive summary, slide, internal report, or any visual output that should look "on brand" for Meltwater. Also trigger when the user mentions Meltwater branding, brand consistency, or asks to make something look like Meltwater material. Use this skill even if the user just says "make it Meltwater" or "use our brand" — always read this file before generating any Meltwater-branded visual output.
---

# Meltwater Brand Skill

This skill encodes Meltwater's 2025 brand guidelines. Read and follow these rules for every branded output.

---

## Assets Available

All brand assets are bundled with this skill:

```
assets/
├── fonts/
│   ├── gt-walsheim-light.ttf        (+ .b64 for HTML embedding)
│   ├── gt-walsheim-regular.ttf      (+ .b64)
│   ├── gt-walsheim-medium.ttf       (+ .b64)
│   ├── gt-walsheim-bold.ttf         (+ .b64)
│   └── gt-walsheim-black.ttf        (+ .b64)
└── logos/
    ├── mw_logo_blue_landscape.png   (+ .b64) — teal logo, horizontal  ← DEFAULT
    ├── mw_logo_white_landscape.png  (+ .b64) — white logo, horizontal
    ├── mw_logo_blue_stacked.png     (+ .b64) — teal logo, vertical
    ├── mw_logo_white_stacked.png    (+ .b64) — white logo, vertical
    ├── mw_logo_charcoal_landscape.png (+ .b64) — charcoal logo, horizontal
    └── mw_logo_charcoal_stacked.png   (+ .b64) — charcoal logo, vertical
```

**Skill root path:** `/mnt/skills/user/meltwater-brand/`

### How to use logos in HTML/React artifacts

Read the `.b64` file for the logo you need, then inline it as a data URI:

```python
# In bash_tool:
logo_b64 = open('/mnt/skills/user/meltwater-brand/assets/logos/mw_logo_blue_landscape.png.b64').read()
# Then inject into HTML: <img src="data:image/png;base64,{logo_b64}" />
```

**Which logo to use:**
- White background → `mw_logo_blue_landscape.png` (teal logo)
- Teal/dark background → `mw_logo_white_landscape.png`
- Tight vertical space → use stacked variants
- Charcoal background → `mw_logo_charcoal_landscape.png`

### How to use GT Walsheim fonts in HTML/React artifacts

Read the `.b64` files for the weights you need and embed via `@font-face`:

```python
# In bash_tool:
font_light   = open('/mnt/skills/user/meltwater-brand/assets/fonts/gt-walsheim-light.ttf.b64').read()
font_regular = open('/mnt/skills/user/meltwater-brand/assets/fonts/gt-walsheim-regular.ttf.b64').read()
font_medium  = open('/mnt/skills/user/meltwater-brand/assets/fonts/gt-walsheim-medium.ttf.b64').read()
font_bold    = open('/mnt/skills/user/meltwater-brand/assets/fonts/gt-walsheim-bold.ttf.b64').read()
font_black   = open('/mnt/skills/user/meltwater-brand/assets/fonts/gt-walsheim-black.ttf.b64').read()
```

Then inject this CSS block into your HTML `<style>` tag (replace `{font_*}` with the actual b64 strings):

```css
@font-face {
  font-family: 'GT Walsheim';
  font-weight: 300;
  src: url('data:font/truetype;base64,{font_light}') format('truetype');
}
@font-face {
  font-family: 'GT Walsheim';
  font-weight: 400;
  src: url('data:font/truetype;base64,{font_regular}') format('truetype');
}
@font-face {
  font-family: 'GT Walsheim';
  font-weight: 500;
  src: url('data:font/truetype;base64,{font_medium}') format('truetype');
}
@font-face {
  font-family: 'GT Walsheim';
  font-weight: 700;
  src: url('data:font/truetype;base64,{font_bold}') format('truetype');
}
@font-face {
  font-family: 'GT Walsheim';
  font-weight: 900;
  src: url('data:font/truetype;base64,{font_black}') format('truetype');
}

body, * {
  font-family: 'GT Walsheim', 'Nunito Sans', Helvetica, sans-serif;
}
```

**For .pptx files:** Use the `.ttf` files directly from `assets/fonts/` — PptxGenJS accepts file paths.

---

## Brand Foundations

### Color Palette

**Primary Colors** — Bold, vibrant, use sparingly and with purpose:

| Name | HEX | RGB | Pantone |
|------|-----|-----|---------|
| Meltwater Teal | `#28BBBB` | 40, 187, 187 | 3252 C |
| Purple | `#B627A1` | 182, 39, 161 | 247 C |
| Orange | `#FF6221` | 255, 98, 33 | 165 C |
| Gold | `#FFCC01` | 255, 204, 1 | 012 C |

**Secondary Colors** — Pastels for background enhancement only:

| Name | HEX | RGB | Pantone |
|------|-----|-----|---------|
| Light Teal | `#C4F4F4` | 196, 244, 244 | 317 C |
| Light Purple | `#F0D4EC` | 240, 212, 236 | 7436 C |
| Light Orange | `#FFDDCC` | 255, 221, 204 | 475 C |
| Light Gold | `#FCFCCC` | 252, 252, 204 | 0131 C |
| Black | `#000000` | 0, 0, 0 | — |
| Charcoal | `#4C4D4F` | 76, 77, 79 | 7540 C |
| Grey | `#EAEAEA` | 234, 234, 234 | 656 C |
| White | `#FFFFFF` | 255, 255, 255 | — |

**Color Rules:**
- Limit any single design to **2–3 complementary brand colors** — never the full palette
- White background with bold color pops is the core aesthetic
- Black is the only color for CTA buttons and main body text
- Do NOT create gradients (only Meltwater Summit/Mira AI product use them)

---

### Typography

**Priority order:** GT Walsheim → Nunito Sans (web fallback) → Helvetica (last resort)

**Font Weight Rules:**

| Context | Weight | GT Walsheim file |
|---------|--------|-----------------|
| Slide/Report Title | 900 (Black) | `gt-walsheim-black.ttf` |
| Section Headings | 700 (Bold) | `gt-walsheim-bold.ttf` |
| Subheadings | 500 (Medium) | `gt-walsheim-medium.ttf` |
| Body Copy | 400 (Regular) | `gt-walsheim-regular.ttf` |
| CTA Buttons | 400 (Regular) | `gt-walsheim-regular.ttf` |
| Bullet Points | 300 (Light) | `gt-walsheim-light.ttf` |

Rules:
- Never use all-light or all-bold on a single page — mix weights for hierarchy
- Bold = emphasis only
- Oblique variants available for all weights (e.g., `gt-walsheim-bold-oblique.ttf`)

---

### Logo

**Available logos** (see Assets section above for full list and loading instructions):

| File | Use when |
|------|----------|
| `mw_logo_blue_landscape.png` | Default — white backgrounds, horizontal space |
| `mw_logo_white_landscape.png` | Teal or dark backgrounds, horizontal space |
| `mw_logo_blue_stacked.png` | White backgrounds, square/tight spaces |
| `mw_logo_white_stacked.png` | Teal or dark backgrounds, square/tight spaces |
| `mw_logo_charcoal_landscape.png` | Charcoal/grey backgrounds, horizontal |

**Usage rules:**
- Logo only in: **Meltwater Teal** (#28BBBB), **Black**, or **White**
- Background must be solid and clean (white or Meltwater Teal only)
- Minimum size: 68px wide
- Never stretch, recolor, add taglines, or modify the logo
- The "eyecon" (eye symbol alone) requires corporate approval before standalone use

---

## Presentation Standards

### Slide Design Philosophy
- Bold and value-communicating — every slide should land a clear point in 3 seconds
- Clean and uncluttered — content and graphics must not compete
- Limit to 2–3 colors per slide
- One visual motif throughout (rounded image frames, teal accent bars, icons in circles)

### Slide Structure Pattern
- **Title slides / section dividers:** Full Meltwater Teal background, white text — bold and large
- **Content slides:** White background, black body text, Teal/Purple/Orange accents
- Use a "sandwich" structure: bold teal title slide → white content slides → teal closing slide

### Typography on Slides
```
Title:        GT Walsheim Black (900), large (40–60pt equivalent)
Subheading:   GT Walsheim Bold (700)
Body/bullets: GT Walsheim Light (300)
```

### Photography Guidelines
- Remove backgrounds from single-person/device images; replace with bold brand color background
- Group photos: keep background, place in a branded rounded frame with bold shapes
- **Always round image corners** — smooth aesthetic is core to the brand
- No AI-generated images, no Photoshop effects, no illustrations
- Add brand color backgrounds or shapes to photos whenever possible

### Iconography
- Icons use Meltwater primary colors only
- Display in filled circles (teal preferred)
- Style: thin line icons on colored circle backgrounds

---

## HTML/React Artifact Approach

When creating a branded HTML or React artifact (slide deck, one-pager, dashboard):

**Step 1:** Read the b64 font files you need (at minimum: light, regular, bold, black)
**Step 2:** Read the appropriate logo b64 file
**Step 3:** Embed both into your CSS/HTML as shown in the Assets section above

```css
/* Core brand CSS variables */
:root {
  --meltwater-teal: #28BBBB;
  --meltwater-purple: #B627A1;
  --meltwater-orange: #FF6221;
  --meltwater-gold: #FFCC01;
  --light-teal: #C4F4F4;
  --charcoal: #4C4D4F;
  --black: #000000;
  --white: #FFFFFF;
  --grey: #EAEAEA;
}
```

**Structural pattern for a branded slide/page:**
1. Header/title area: `background: #28BBBB; color: white;` with GT Walsheim Black
2. Body: white background, `#000000` text, GT Walsheim Regular
3. Accent elements (borders, icons, badges): teal or purple, used sparingly
4. Footer: Meltwater logo (use embedded b64 PNG)
5. Rounded corners on all image containers and cards (`border-radius: 12px` minimum)

---

## PowerPoint (.pptx) Approach

Read `/mnt/skills/public/pptx/SKILL.md` for technical workflow, then apply these Meltwater-specific values:

**Color constants:**
```javascript
const MW_TEAL     = '28BBBB';
const MW_PURPLE   = 'B627A1';
const MW_ORANGE   = 'FF6221';
const MW_GOLD     = 'FFCC01';
const MW_BLACK    = '000000';
const MW_WHITE    = 'FFFFFF';
const MW_GREY     = 'EAEAEA';
const MW_CHARCOAL = '4C4D4F';
```

**Font path for PptxGenJS:**
```javascript
// Use TTF files directly
const FONT_PATH = '/mnt/skills/user/meltwater-brand/assets/fonts/';
// e.g., pptx.defineFontFace('GT Walsheim', [{ data: fs.readFileSync(FONT_PATH + 'gt-walsheim-bold.ttf') }])
```

**Logo path for PptxGenJS:**
```javascript
const LOGO_PATH = '/mnt/skills/user/meltwater-brand/assets/logos/mw_logo_blue_landscape.png';
```

**Slide templates:**
1. **Title Slide** — Full teal (`#28BBBB`) background, large white GT Walsheim Black title, subtitle in Light Teal
2. **Section Divider** — Teal background, large bold number + white section title
3. **Content Slide** — White background, teal header bar, black body text, logo bottom-right
4. **Data/Chart Slide** — White background, teal + purple + orange for multi-series data
5. **Closing Slide** — Full teal background, white text

---

## Common Mistakes to Avoid

| ❌ Don't | ✅ Do Instead |
|----------|--------------|
| Use all 6+ colors at once | Pick 2–3 per design |
| Use gradients | Use solid brand colors |
| Use illustrations | Use real photography with brand treatment |
| Apply logo taglines or modifications | Use logo as-is from assets/ |
| Use web font URLs for GT Walsheim | Embed from the .b64 files in assets/fonts/ |
| Heavy clutter on slides | One clear message per slide |
| Mix too many font weights | Black title → Bold heading → Light body |
| Show logo smaller than 68px | Maintain minimum size |
| Use AI-generated stock photos | Use real people photography |

---

## Output Checklist

Before finalizing any Meltwater-branded output:
- [ ] 2–3 colors max per page/slide
- [ ] Teal used as primary brand signal
- [ ] Black for all body text and CTAs
- [ ] Font weight hierarchy: Black/Bold title → Medium sub → Light bullets
- [ ] GT Walsheim embedded from assets/fonts/ (not a CDN)
- [ ] Logo loaded from assets/logos/ via b64 embed
- [ ] Logo present on all content pages (horizontal, teal or white depending on background)
- [ ] Rounded image corners if photography is used
- [ ] No gradients, no illustrations, no AI images
- [ ] Clean, uncluttered layout — content and visuals don't compete
- [ ] Title/closing slides use full teal background
