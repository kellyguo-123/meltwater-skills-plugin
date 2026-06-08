---
name: brand-pulse
description: >
  Generate a fully branded Meltwater "Brand Pulse" media intelligence infographic and downloadable PDF for any brand. Use this skill whenever a user asks for a brand report, brand pulse, brand health brief, media intelligence summary, sentiment analysis, social listening report, brand overview, or any request to analyze how a brand is covered across news and social media. Also trigger when the user says things like "pull from Meltwater and analyze [brand]", "give me a brand brief on [company]", "what's the media landscape looking like for [brand]", or "create a brand intelligence report". This skill combines live Meltwater data retrieval, AI synthesis, Meltwater-branded HTML infographic generation, and PDF export into one end-to-end workflow. Always use this skill for any brand + media intelligence + report combination — even if the user doesn't say "Brand Pulse" explicitly.
---

# Brand Pulse Skill

Produces a fully Meltwater-branded, multi-section media intelligence infographic (interactive HTML in chat + downloadable PDF) by pulling live data from Meltwater's retrieval tools and synthesizing it with AI.

---

## Step 0 — Gather parameters

Before pulling data, confirm the following (infer from conversation context where possible — only ask if missing):

| Parameter | Default |
|-----------|---------|
| Brand name | Required |
| Date range | Last 30 days |
| Languages | English and French |
| Competitors | Infer from industry (ask user to confirm or add) |
| Channels | News, X, Instagram, Facebook, TikTok, Reddit |

---

## Step 1 — Read the Meltwater brand skill

Before building any visual output, read `/mnt/skills/user/meltwater-brand/SKILL.md` for the full Meltwater brand guidelines (colors, typography, layout rules). Apply these throughout. Key values:

- **Teal** `#28BBBB` — headers, accents, section labels, footer
- **Light Teal** `#C4F4F4` — card borders, backgrounds
- **Orange** `#FF6221` — high-severity risk badges
- **Red** `#E24B4A` — critical badges, negative sentiment
- **Purple** `#B627A1` — secondary accents
- **Gold** `#FFCC01` — medium severity
- **Black** `#000000` — all body text
- **Charcoal** `#4C4D4F` — secondary text
- **Grey** `#EAEAEA` — dividers, neutral fills
- **Font:** Nunito Sans (Google Fonts fallback)

---

## Step 2 — Pull Meltwater data (run all queries)

Fire all queries below using `Meltwater:unified_retrieval_document_retrieval_tool`. Run them sequentially and collect results. Always use exact `YYYY-MM-DD` date formats for `startDate`/`endDate`.

### Query set

| # | Purpose | Query string | Platforms | Sort |
|---|---------|-------------|-----------|------|
| 1 | Top news by reach | `{brand} brand news coverage` | `["news"]` | `reach` |
| 2 | Social sentiment & top posts | `{brand} customer sentiment social media` | `["twitter","instagram","facebook","tiktok","reddit"]` | `engagement` |
| 3 | Positive product/innovation | `{brand} product launch new menu innovation praise` | _(all)_ | `relevance` |
| 4 | Risks & negative topics | `{brand} controversy complaint negative criticism` | _(all)_ | `relevance` |
| 5 | Community/brand love | `{brand} community charity collab love loyalty` | `["news","instagram","facebook"]` | `relevance` |

Adjust query strings to fit the brand's industry (e.g. for a tech brand swap "menu" for "feature release").

For each returned document, extract and store:
- `content` (post/article text)
- `title` (for news)
- `date`
- `platform`
- `url` ← **preserve for citations and source links**
- `author.name` / `author.handle`
- `social_metrics` (reach, views, engagement, shares, reactions)
- `editorial_metrics` (newsguard-rating if available)

---

## Step 3 — Synthesize insights

Using the retrieved documents, derive the following for each report section. Anchor every claim in actual retrieved content.

### 3a — Brand position (what customers love)
Identify 4 distinct positive themes from the data. Look for: iconic products, innovation launches, community initiatives, cultural resonance, celebrity collaborations, loyalty signals. Each theme needs a short title, icon, and 2–3 sentence description citing specific data points (post metrics, product names, source names).

### 3b — Sentiment & emotion breakdown
Estimate sentiment split (Negative / Positive / Neutral %) from the tone and volume of retrieved content. Then break down into 6 emotions: Anger, Sadness, Joy, Disgust, Anticipation, Fear. Ground each percentage in actual content themes found. Write a 2-sentence "emotion drivers" note explaining what's causing each dominant emotion.

### 3c — Emerging themes (3 clusters)
Group the retrieved content into 3 narrative clusters (e.g. "product innovation", "political controversy", "crisis association"). Each cluster gets 2 sub-points with title + 2-sentence description.

### 3d — Risks
Identify up to 4 risks. Assign severity: **Critical** (active brand damage, boycott momentum, legal/humanitarian association), **High** (brand equity erosion, perception shift), **Medium** (latent reputation risk). Each risk needs a title and 2–3 sentence description with specific evidence from the data.

### 3e — Customer complaints
Identify 4 complaint categories (e.g. product quality, value, staff, authenticity, labour practices, innovation). Each gets a short label and 2-sentence description.

### 3f — Competitive landscape
For each competitor: assess threat level (Active Threat / Watch / Low Overlap / Emerging), and write 1–2 sentences on why. Look for direct competitor mentions in boycott posts, comparison posts, or switching intent signals in the retrieved data.

### 3g — Top posts by engagement
Select the 7 highest-engagement posts from the retrieved data. For each, preserve the exact `url` for the clickable "View post ↗" link. Include platform, author handle, date, a short quote from the content, and all available metrics (reach, views, engagements).

### 3h — News citations
Select 5–7 news articles or high-reach posts. For each, preserve the exact `url` for the "Read ↗" / "View ↗" link. Include source name, date, reach, and a short title.

### 3i — Strategic recommendations
Write 5 prioritised, actionable recommendations grounded in the data. Each has a bold title and 2–3 sentence rationale. Order by urgency (crisis response first, then opportunity capture).

---

## Step 4 — Build the HTML infographic

Render the full report as an interactive HTML widget using `visualize:show_widget`. Load `visualize:read_me` with `["mockup", "data_viz"]` first.

### Layout structure (in order)

1. **Teal header** — brand name, "Brand Pulse Report" title, period + channels + languages meta row
2. **Dual crisis alert bar** (if any Critical risks exist) — red background, "!" icon, 2-sentence summary
3. **4 KPI cards** — teal-bordered, light teal background: Est. Mention Volume, Sentiment Balance, Top Social Reach, Innovation Signal
4. **Section 01 — Brand position summary** — two-col grid (stretch-aligned):
   - Left card: "What customers love" — 4 theme items with icon + title + body
   - Right card: "Aggregated sentiment summary" — donut chart (pure inline SVG, NOT Chart.js) + horizontal sentiment bars + emotion breakdown bars + sentiment note
5. **Section 02 — Emerging themes** — three-col card grid, 2 sub-items each
6. **Section 03 — Emerging risks** — full-width, left-bordered risk items with severity badges
7. **Section 04 — Customer complaints** — 2×2 grid of orange-tinted chips
8. **Section 05 — Competitive threat & opportunity** — single card, 5 competitor rows with brand initials, description, and signal pill
9. **Section 06 — Viral moments & top posts** — single card, 7 post rows each with platform badge (clickable `<a href="">` link), content, metrics, tag, and "View post ↗" link button
10. **Section 07 — News sources & citations** — single card, news rows with coloured dot, title, meta, and "Read ↗" / "View ↗" link button
11. **Section 08 — Strategic recommendations** — 5 teal-accented rec items with numbered circle
12. **Teal footer** — Meltwater logo mark + report metadata

### Sentiment donut chart — ALWAYS use pure inline SVG

Never use Chart.js or any external JS library for the sentiment donut. Always render it as a static inline SVG using stroke-dasharray/stroke-dashoffset. This ensures the chart renders in both the HTML widget AND the PDF export. Use this pattern:

```html
<svg width="110" height="110" viewBox="0 0 110 110" xmlns="http://www.w3.org/2000/svg">
  <g transform="rotate(-90 55 55)">
    <!-- Each segment: r=40, stroke-width=22, cx/cy=55 -->
    <!-- circumference = 251.327 -->
    <!-- Negative segment (62%): dash = 155.82 -->
    <circle cx="55" cy="55" r="40" fill="none" stroke="#E24B4A" stroke-width="22"
      stroke-dasharray="155.8235 251.3274" stroke-dashoffset="0"/>
    <!-- Positive segment (27%): dash = 67.86, offset = -155.82 -->
    <circle cx="55" cy="55" r="40" fill="none" stroke="#28BBBB" stroke-width="22"
      stroke-dasharray="67.8584 251.3274" stroke-dashoffset="-155.8235"/>
    <!-- Neutral segment (11%): dash = 27.65, offset = -223.68 -->
    <circle cx="55" cy="55" r="40" fill="none" stroke="#EAEAEA" stroke-width="22"
      stroke-dasharray="27.6457 251.3274" stroke-dashoffset="-223.6818"/>
  </g>
  <!-- White center -->
  <circle cx="55" cy="55" r="29" fill="#fff"/>
</svg>
```

Scale `stroke-dasharray` values to match actual sentiment percentages: `circ * pct / 100`. Each segment's `stroke-dashoffset` = `-1 * sum_of_prior_segment_lengths`.

### Source links
Every post in section 06 must have a teal "View post ↗" button as an `<a href="{url}">` element. Every news item in section 07 must have a "Read ↗" or "View ↗" button linked to the exact `url` from the Meltwater result. If no URL is available, omit the button rather than linking to `#`.

### Design rules
- Two-col `section-gap` grids must use `align-items: stretch` so cards match height
- Left card and right card must each be `display: flex; flex-direction: column` so content fills the height
- Emotion note at the bottom of the sentiment card should use `margin-top: auto` to anchor to the bottom only if it fills the gap naturally; otherwise distribute using padding
- No gradients, no box shadows on cards (only `border: 1px solid #EAEAEA`)
- All body text `color: #000` or `color: #4C4D4F` — never hardcoded dark greys
- `border-radius: 10px` on all cards

---

## Step 5 — Export to PDF

After the HTML widget renders in chat, export a downloadable PDF using Playwright (headless Chromium). Do not use wkhtmltopdf — it does not support modern CSS grid or flexbox reliably.

```python
# 1. Write the full standalone HTML to /home/claude/{brand_slug}_brand_pulse.html
#    - Must be complete with <!DOCTYPE html>, <head>, <body>
#    - Include all CSS inline in <style> tags
#    - Use the SAME inline SVG donut (not Chart.js)
#    - Google Fonts @import in <style> for Nunito Sans

# 2. Render to PDF with Playwright
from playwright.sync_api import sync_playwright

with sync_playwright() as p:
    browser = p.chromium.launch()
    page = browser.new_page()
    page.goto(f'file:///home/claude/{brand_slug}_brand_pulse.html')
    page.wait_for_timeout(1000)  # allow fonts to load
    page.pdf(
        path=f'/home/claude/{brand_slug}_brand_pulse.pdf',
        format='A4',
        print_background=True,
        margin={'top': '0mm', 'bottom': '0mm', 'left': '0mm', 'right': '0mm'}
    )
    browser.close()

# 3. Copy to outputs and present
import shutil
shutil.copy(f'/home/claude/{brand_slug}_brand_pulse.pdf',
            f'/mnt/user-data/outputs/{brand_slug}_brand_pulse.pdf')
```

Then call `present_files` with the output path.

**Important:** In the standalone HTML used for PDF export, replace all `<a href="...">` link buttons with plain `<span>` elements showing the domain name (e.g. `twitter.com ↗`) — hyperlinks in PDFs are not reliably clickable across all viewers, so display the source domain as readable text instead.

---

## Common issues & fixes

| Issue | Fix |
|-------|-----|
| Sentiment donut missing from PDF | Replace Chart.js canvas with inline SVG (see Step 4) |
| White space gap between two-col cards | Add `align-items: stretch` to `.two-col` grid and `display: flex; flex-direction: column` to each `.card` |
| Post URLs missing | Check `resource.url` field in each document result — it's nested under `resource`, not at the top level |
| Too many irrelevant results | Add brand name explicitly to query string and use `savedSearchIds` if available |
| PDF cuts off content | Playwright A4 format handles multi-page automatically — ensure no `height: 100vh` constraints on the root container |
| Emoji not rendering in PDF | Playwright/Chromium supports emoji — no fix needed; if missing, use Unicode text symbols instead |

---

## Output checklist

Before presenting the final output, verify:

- [ ] All 8 sections present and populated with real data
- [ ] 4 items in "What customers love" (no white space gap)
- [ ] Sentiment donut rendered as inline SVG (visible in both widget and PDF)
- [ ] Emotion breakdown has 6 rows with percentages summing to ~100%
- [ ] Every post in section 06 has a working source link
- [ ] Every news item in section 07 has a working source link
- [ ] PDF exported and presented via `present_files`
- [ ] Meltwater brand colors used throughout (teal headers, white body, black text)
- [ ] Footer present on both HTML and PDF
