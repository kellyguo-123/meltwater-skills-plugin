# Design guidance

Neutral principles for translating brand identity into report design. There are no defaults here — the principles below apply to every brand. The specifics (palette, type, layout) come from research, not from this document.

## The cardinal rule

**Do not borrow layout structure from a previous report.** Each report's bones — the order of sections, the visual rhythm, the way KPIs are presented, the way the cohort comparison is laid out, the way top creators are framed — must serve *this brand's* identity, not Claude's template memory.

A heritage spirits brand and a streetwear brand should not produce reports with the same skeleton in different colours. The skeleton itself is part of the brand expression.

## Picking a layout philosophy

Pick one and execute. Mixing two philosophies produces the "ugly mish-mash" the user warned about.

- **Centred and balanced** — symmetric hero, centred headlines, even KPI grids. Suits brands with formal/corporate identity.
- **Asymmetric editorial** — magazine-style spreads, sidebars, asymmetric column ratios, generous margins. Suits heritage, premium, lifestyle, hospitality brands.
- **Grid-dense / data-led** — many small cards, charts dominant, info packed in. Suits tech, scientific, B2B brands.
- **Maximalist / photo-bleed** — full-page imagery, big type laid over photography. Suits fashion, food, travel, festival brands.
- **Brutalist / raw** — exposed grid lines, oversized type, single-colour dominance, sharp edges. Suits avant-garde, design-led, startup brands.

The cohort deep-dive sections are the place where the layout philosophy shows most. A creator portrait gallery, a magazine contributors page, a stats showcase, an interactive playlist — all valid, all different.

## Typography

Pair a **display face** with a **body face**. Do not use only sans-serif unless the brand is genuinely a sans-only identity (Helvetica-purist brands, technical brands). Most premium and heritage brands have a serif somewhere — bring it in.

Quick reference on free Google Fonts pairings by aesthetic family. **These are starting points, not defaults — adjust per brand.**

| Aesthetic | Display | Body | Labels |
|---|---|---|---|
| Heritage / editorial | Cormorant Garamond, Fraunces, Playfair Display, Source Serif 4 | Source Serif 4, Lora, Crimson Text | Oswald, IBM Plex Mono |
| Athletic / sportswear | Anton, Big Shoulders Display, Oswald Bold | IBM Plex Sans, Roboto | Roboto Condensed |
| Technical / clinical | Space Grotesk, IBM Plex Mono, JetBrains Mono | IBM Plex Sans, Manrope | IBM Plex Mono |
| Luxury / hospitality | Tenor Sans, Italiana, Cormorant | Lora, Cormorant Garamond | Oswald light |
| Food / warm | DM Serif Display, Recoleta, Fraunces | Source Serif 4, Lora | Oswald |
| Festival / colour | Bowlby One, Bungee, Anton | Manrope, IBM Plex Sans | Oswald |
| Brutalist | Space Grotesk Bold, Roboto Mono Bold | IBM Plex Sans, Space Mono | Space Mono |

If unsure, **avoid Inter as a display face** — it shows up in too many AI-generated artifacts and has no character. Use it for small body/UI text only when nothing else fits.

## Colour

Three roles a brand colour can play. Pick one explicitly:

1. **Backdrop** — the brand colour is the page. Sections, hero, cards all use it as background. Suits brands whose colour *is* the brand (Coca-Cola red, Tiffany blue, IKEA blue).
2. **Accent** — the brand colour appears in small high-impact moments (links, callouts, dividers). Suits brands with a stark base — sportswear brands with a single electric accent on black, fashion houses with a signature ribbon colour on cream.
3. **Texture** — the brand colour is one component of a layered palette. Suits brands with a richer palette (heritage spirits with red + maroon + cream + foil, fashion houses with check patterns, drinks brands with mixed warm tones).

Pure black `#000000` and pure white `#FFFFFF` are very rare in real brand systems. Use warm off-blacks (`#1A1614`, `#1F1A18`) and warm off-whites or cream (`#F4EFE2`, `#FAF6F0`) unless the brand specifically uses pure values.

## Visual sophistication

Match the brand's level of refinement. A drinks brand with vintage heritage deserves foil borders, drop caps, paper textures. A scientific supplement brand deserves clean grids and monospace data labels. A streetwear brand deserves bold uppercase, harsh contrast, outline strokes.

**Don't over-decorate a minimal brand. Don't under-decorate a heritage brand.**

## Honest failure states

When data is missing — particularly demographics, where `profileDemographics` is known to time out — show an explicit "data unavailable" panel styled to the brand. Do not show empty cells. Do not invent or estimate. The honesty itself is part of the brand expression: a heritage magazine has an "Editor's Note"; a technical brand has a `[diagnostic: endpoint timeout]` code block; a luxury brand has a discreet italic note.

## The integrity check

Before saving, ask: would two different brand strategists, shown this report and any other report Claude has built recently, look at them and say *"these came from completely different studios"*?

If yes, the brand integrity is right.
If no, the skeleton is still leaking through, and the layout needs to be rethought.
