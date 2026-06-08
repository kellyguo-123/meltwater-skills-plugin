# GenAI Lens Report — Brand Theming Reference

This document defines how to detect and apply brand colours to the GenAI Lens HTML report. Every report is rendered in the subject brand's visual identity, not Meltwater's.

---

## Colour Detection Workflow

### Step 1: Identify the brand

Extract the primary brand name from the GenAI Lens CSV data. This is typically the most frequently mentioned organization in the "Organizations and brands" column, or the brand explicitly named in the prompt question.

### Step 2: Look up brand colours

Check the brand database below first. If the brand is not listed:

1. Use web search to find the brand's official website.
2. Identify the primary brand colour from the logo, header, or hero section.
3. Identify a secondary colour (often used for CTAs, accents, or secondary navigation).
4. Derive the light tint and border colour from the primary.

### Step 3: Generate CSS variables

Map the brand colours to the report's CSS variable set:

| CSS Variable | Source | Fallback |
|-------------|--------|----------|
| `--brand-primary` | Brand's primary colour (dominant logo/header colour) | `#E72024` |
| `--brand-primary-light` | 5-8% opacity tint of primary on white | Calculated |
| `--brand-primary-border` | 15-20% opacity tint of primary on white | Calculated |
| `--brand-secondary` | Brand's secondary/accent colour | `#FFC72C` (gold) |
| `--brand-accent` | Darker variant of primary or a distinct tertiary colour | Calculated |
| `--positive` | Always `#2E7D32` (green) — not brand-dependent | `#2E7D32` |
| `--negative` | Defaults to `var(--brand-primary)` | — |

### Step 4: Confirm with user

Before rendering, present the colour palette to the user:

> "I'll use these colours for the [Brand] report:
> - Primary: [colour name] (#hex) — used for header, footer, section headers, accents
> - Secondary: [colour name] (#hex) — used for TL;DR icon, callout highlights
> - Accent: [colour name] (#hex) — used for secondary dot colours
>
> Does that look right?"

### Calculating tints

For `--brand-primary-light` (KPI card backgrounds):
- Take the primary hex, convert to RGB, mix at ~5-8% with white (#FFFFFF).
- Example: Primary `#E72024` → Light `#FFF8F8`
- Example: Primary `#00549F` → Light `#F0F6FB`
- Example: Primary `#178841` → Light `#F0FAF3`

For `--brand-primary-border` (KPI card borders):
- Mix at ~15-20% with white.
- Example: Primary `#E72024` → Border `#FAD7D8`
- Example: Primary `#00549F` → Border `#CCE0F0`

---

## Australian Brand Database

### Retail & Grocery

| Brand | Primary | Secondary | Accent | Notes |
|-------|---------|-----------|--------|-------|
| **Coles** | `#E72024` (red) | `#FFC72C` (gold) | `#9B1B1F` (dark red) | |
| **Woolworths** | `#178841` (green) | `#FFD100` (yellow) | `#0D5C2E` (dark green) | Include "Woolies" in queries |
| **Aldi** | `#00549F` (blue) | `#F7941D` (orange) | `#003B73` (dark blue) | |
| **IGA** | `#F26F21` (orange) | `#1A1A1A` (black) | `#C45A1A` (dark orange) | |
| **Bunnings** | `#008B3A` (green) | `#E72024` (red) | `#006B2D` (dark green) | |
| **JB Hi-Fi** | `#FFD800` (yellow) | `#000000` (black) | `#CC9900` (dark gold) | Use black text on yellow header |
| **Kmart** | `#E72024` (red) | `#FFFFFF` (white) | `#B81A1E` (dark red) | |
| **Target (AU)** | `#CC0000` (red) | `#FFFFFF` (white) | `#990000` (dark red) | |
| **Harvey Norman** | `#FFCC00` (yellow) | `#000000` (black) | `#CC9900` (dark gold) | |
| **Officeworks** | `#008B3A` (green) | `#E72024` (red) | `#006B2D` (dark green) | |
| **The Good Guys** | `#E30613` (red) | `#FFF200` (yellow) | `#B3050F` (dark red) | |
| **Costco (AU)** | `#E31837` (red) | `#005DA6` (blue) | `#B31229` (dark red) | |

### Financial Services

| Brand | Primary | Secondary | Accent | Notes |
|-------|---------|-----------|--------|-------|
| **CBA / CommBank** | `#FFCC00` (yellow) | `#000000` (black) | `#CC9900` (dark gold) | Use black text on yellow |
| **ANZ** | `#007DBA` (blue) | `#003F72` (navy) | `#005A8C` (dark blue) | |
| **Westpac** | `#D5002B` (red) | `#1C1C1C` (charcoal) | `#A10022` (dark red) | |
| **NAB** | `#C7001F` (red) | `#1A1A1A` (black) | `#9B0018` (dark red) | |
| **Macquarie** | `#000000` (black) | `#00A3E0` (blue) | `#333333` (dark grey) | |
| **AMP** | `#003DA5` (blue) | `#FFFFFF` (white) | `#002D7A` (dark blue) | |
| **Suncorp** | `#00A1DE` (blue) | `#FFB81C` (gold) | `#0078A8` (dark blue) | |
| **QBE** | `#003C71` (navy) | `#78BE20` (green) | `#002A50` (dark navy) | |

### Telco & Tech

| Brand | Primary | Secondary | Accent | Notes |
|-------|---------|-----------|--------|-------|
| **Telstra** | `#001E82` (navy) | `#FF6B00` (orange) | `#001560` (dark navy) | |
| **Optus** | `#1E2843` (dark blue) | `#00E676` (green) | `#141C30` (darker) | |
| **Vodafone (AU)** | `#E60000` (red) | `#FFFFFF` (white) | `#B30000` (dark red) | |
| **TPG** | `#00A3E0` (blue) | `#6CC24A` (green) | `#0078A8` (dark blue) | |
| **Atlassian** | `#0052CC` (blue) | `#FFFFFF` (white) | `#003D99` (dark blue) | |
| **Canva** | `#00C4CC` (teal) | `#7D2AE8` (purple) | `#009499` (dark teal) | |

### Airlines & Transport

| Brand | Primary | Secondary | Accent | Notes |
|-------|---------|-----------|--------|-------|
| **Qantas** | `#E40000` (red) | `#1A1A1A` (black) | `#B30000` (dark red) | |
| **Virgin Australia** | `#E10A0A` (red) | `#1A1A1A` (black) | `#B30808` (dark red) | |
| **Jetstar** | `#FF6600` (orange) | `#FFD100` (yellow) | `#CC5200` (dark orange) | |
| **Rex Airlines** | `#0A3161` (navy) | `#C6A664` (gold) | `#072347` (dark navy) | |

### Logistics & Services

| Brand | Primary | Secondary | Accent | Notes |
|-------|---------|-----------|--------|-------|
| **Australia Post** | `#DC1928` (red) | `#FFCC00` (yellow) | `#B3142A` (dark red) | |
| **Toll** | `#E4002B` (red) | `#1A1A1A` (black) | `#B30022` (dark red) | |
| **Linfox** | `#0033A0` (blue) | `#E4002B` (red) | `#002680` (dark blue) | |
| **StarTrack** | `#004B87` (blue) | `#FFB81C` (gold) | `#003766` (dark blue) | |

### Media & Entertainment

| Brand | Primary | Secondary | Accent | Notes |
|-------|---------|-----------|--------|-------|
| **Nine** | `#0072CE` (blue) | `#FFFFFF` (white) | `#0056A0` (dark blue) | |
| **Seven** | `#E72024` (red) | `#1A1A1A` (black) | `#B81A1E` (dark red) | |
| **ABC (AU)** | `#003C71` (navy) | `#FFFFFF` (white) | `#002A50` (dark navy) | |
| **SBS** | `#1A1A1A` (black) | `#E72024` (red) | `#333333` (dark grey) | |
| **Foxtel** | `#E50914` (red) | `#1A1A1A` (black) | `#B30710` (dark red) | |
| **TEG / Ticketmaster** | `#006CFF` (blue) | `#FFFFFF` (white) | `#0052CC` (dark blue) | |

### Insurance

| Brand | Primary | Secondary | Accent | Notes |
|-------|---------|-----------|--------|-------|
| **NRMA** | `#003DA5` (blue) | `#FFB81C` (gold) | `#002D7A` (dark blue) | |
| **RACV** | `#003DA5` (blue) | `#F7941D` (orange) | `#002D7A` (dark blue) | |
| **Allianz (AU)** | `#003781` (blue) | `#FFFFFF` (white) | `#002860` (dark blue) | |
| **Medibank** | `#00857C` (teal) | `#1A1A1A` (black) | `#006660` (dark teal) | |
| **NIB** | `#7AB800` (green) | `#1A1A1A` (black) | `#5C8C00` (dark green) | |

### FMCG & Consumer

| Brand | Primary | Secondary | Accent | Notes |
|-------|---------|-----------|--------|-------|
| **Vegemite** | `#FFD100` (yellow) | `#E72024` (red) | `#CC9900` (dark gold) | |
| **Lion** | `#003DA5` (blue) | `#FFB81C` (gold) | `#002D7A` (dark blue) | |
| **CUB** | `#1A1A1A` (black) | `#FFD100` (yellow) | `#333333` (dark grey) | |
| **Treasury Wine Estates** | `#6F1D46` (burgundy) | `#C4A35A` (gold) | `#4D1432` (dark burgundy) | |
| **Sanitarium** | `#007A33` (green) | `#FFC72C` (gold) | `#005C26` (dark green) | |

### Energy & Resources

| Brand | Primary | Secondary | Accent | Notes |
|-------|---------|-----------|--------|-------|
| **BHP** | `#E45325` (orange) | `#1A1A1A` (black) | `#C4431E` (dark orange) | |
| **Rio Tinto** | `#E72024` (red) | `#1A1A1A` (black) | `#B81A1E` (dark red) | |
| **AGL** | `#E74C3C` (red) | `#1A1A1A` (black) | `#C0392B` (dark red) | |
| **Origin Energy** | `#E44D26` (orange) | `#1A1A1A` (black) | `#C4401F` (dark orange) | |
| **Woodside** | `#003DA5` (blue) | `#FFFFFF` (white) | `#002D7A` (dark blue) | |
| **Santos** | `#009CDE` (blue) | `#FFFFFF` (white) | `#007AAD` (dark blue) | |

### Government / Public Sector

| Brand | Primary | Secondary | Accent | Notes |
|-------|---------|-----------|--------|-------|
| **Services Australia** | `#313131` (charcoal) | `#00698F` (teal) | `#1A1A1A` (black) | |
| **ATO** | `#313131` (charcoal) | `#00698F` (teal) | `#1A1A1A` (black) | |
| **Defence (AU)** | `#003366` (navy) | `#B8860B` (gold) | `#002244` (dark navy) | |

### Education

| Brand | Primary | Secondary | Accent | Notes |
|-------|---------|-----------|--------|-------|
| **University of Sydney** | `#E64626` (ochre) | `#003F72` (navy) | `#C43A1F` (dark ochre) | |
| **University of Melbourne** | `#094183` (navy) | `#003366` (dark navy) | `#072D5C` (darker navy) | |
| **ANU** | `#BE830E` (gold) | `#1A1A1A` (black) | `#98680B` (dark gold) | |
| **UNSW** | `#FFE600` (yellow) | `#1A1A1A` (black) | `#CCC200` (dark yellow) | |
| **Monash** | `#006DAE` (blue) | `#1A1A1A` (black) | `#005488` (dark blue) | |

---

## Competitor Brand Colours

When building the competitive snapshot (Section 02), each competitor's card uses their own brand colour for the `.top-bar` and `.rank-chip`. Look up competitors in the database above. If a competitor is not listed, use web search to find their primary brand colour.

---

## Special Cases

### Brands with yellow/gold as primary
For brands where the primary colour is yellow or gold (JB Hi-Fi, CBA, Harvey Norman, Vegemite), use black (#000000) as the text colour on the header and footer instead of white, and use the secondary colour (usually black) as `--brand-accent`.

Adjust the CSS:
```css
.header { background: var(--brand-primary); color: #000; }
.footer { background: var(--brand-primary); color: #000; }
.section-header { background: var(--brand-primary); color: #000; }
```

### Brands with very dark primary
For brands where the primary colour is very dark (navy, black, charcoal), the report may feel too heavy. In these cases:
- Use the secondary colour for section headers and accents.
- Keep the header and footer dark.
- Ensure sufficient contrast throughout.

### Brands not in the database
If the brand is not listed:
1. Search the web for "[Brand name] brand guidelines" or "[Brand name] logo colour hex".
2. Visit the brand's official website and extract the dominant colour from the header/logo.
3. Generate a complementary secondary colour if none is obvious.
4. Confirm with the user before proceeding.
