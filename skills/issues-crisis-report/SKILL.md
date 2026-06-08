---
name: issues-crisis-report
description: >
  Generate a fully branded Meltwater Issues & Crisis Report — an 11-section media intelligence crisis brief for any brand or topic. Use this skill whenever a user asks for a crisis report, issues brief, reputation analysis, controversy report, or any request to analyze how a brand is being covered in the context of a specific controversy, scandal, or reputational threat. Also trigger when the user says things like "pull from Meltwater and build a crisis report on [brand]", "what's the crisis situation for [brand]", "build an issues brief for [brand] on [topic]", or "what are people saying about [brand] controversy". This skill combines live Meltwater data retrieval (not MIRA), daily volume trend analysis, qualitative synthesis, and a fully branded HTML infographic plus downloadable PDF with a pure SVG bar chart that renders correctly in both widget and PDF. Always use this skill for any brand plus controversy or crisis plus report combination.
---

# Issues & Crisis Report Skill

Produces a fully Meltwater-branded, 11-section crisis communications brief (interactive HTML in chat + downloadable PDF) by pulling live data from Meltwater's unified retrieval tools and synthesizing it with the analyst's own judgment.

---

## Step 0 — Gather parameters

Before pulling data, confirm the following (infer from conversation context where possible):

| Parameter | Default |
|-----------|---------|
| Brand name | Required |
| Crisis / topic | Required |
| Date range | Last 30 days |
| Channels | News, X/Twitter, Reddit, YouTube, Broadcast |

---

## Step 1 — Read the Meltwater brand skill

Before building any visual output, read `/mnt/skills/user/meltwater-brand/SKILL.md` for full brand guidelines. Key values:

- **Teal** `#28BBBB` — headers, section bars, accents, footer
- **Light Teal** `#C4F4F4` — card borders, card backgrounds
- **Orange** `#FF6221` — High severity risks, secondary spikes
- **Red** `#E24B4A` — Critical alerts, negative sentiment, crisis spikes
- **Purple** `#B627A1` — secondary accents
- **Gold** `#FFCC01` — Medium severity
- **Black** `#000000` — all body text
- **Charcoal** `#4C4D4F` — secondary text
- **Grey** `#EAEAEA` — dividers, neutral fills
- **Font:** Nunito Sans (Google Fonts fallback)

---

## Step 2 — Pull Meltwater data

Use `Meltwater:unified_retrieval_document_retrieval_tool` and `Meltwater:unified_retrieval_statistics_retrieval_tool`. Always use exact `YYYY-MM-DD` dates. **Do not use MIRA.**

### 2a — Document retrieval (run all 3 queries)

| # | Purpose | Query | Platforms | Sort |
|---|---------|-------|-----------|------|
| 1 | Top news coverage | `{brand} {topic} controversy criticism coverage` | `["news"]` | `reach` |
| 2 | Social sentiment & top posts | `{brand} {topic} backlash outrage reaction` | `["twitter","reddit","youtube"]` | `engagement` |
| 3 | Key voices & amplifiers | `{brand} {topic} politician MP journalist report` | _(all)_ | `relevance` |

For each document, extract:
- `content` (text), `title`, `date`, `platform`, `url`, `author.name`, `author.handle`
- `social_metrics` (reach, views, engagement)
- `editorial_metrics` (newsguard-rating if present)

### 2b — Volume statistics: weekly windows

Pull 5 weekly calls using `Meltwater:unified_retrieval_statistics_retrieval_tool` to get the shape of the story over time. Split the 30-day range into weekly buckets:

```
Week 1: startDate to startDate+6
Week 2: startDate+7 to startDate+13
Week 3: startDate+14 to startDate+20
Week 4: startDate+21 to startDate+27
Week 5: startDate+28 to endDate
```

Use a broad semantic query: `"{brand} {topic} controversy"` with `platforms: ["news","twitter","reddit","youtube","broadcast-tv","broadcast-audio"]`. Record `total.count` for each week.

### 2c — Volume statistics: day-by-day (for the chart)

Pull individual day-by-day stats for accurate daily counts. Group into 1–3 day windows across the full date range. For each window call:

```
query: "{brand} {topic} controversy"
platforms: ["news","twitter","reddit","youtube","broadcast-tv","broadcast-audio"]
startDate: YYYY-MM-DD
endDate: YYYY-MM-DD (same or +1/+2 days)
```

Key days to isolate individually: any days where you expect spike events based on the documents retrieved. Record `total.count` for each window, then distribute proportionally within windows where needed.

**Important:** The statistics tool generates its own boolean query from your semantic input. Use broad, simple queries (3–5 words) for higher counts. Narrow queries with many AND/OR terms produce lower, more specific counts. Be consistent across calls so comparisons are valid.

---

## Step 3 — Synthesize insights

Using retrieved documents and stats, derive the following. Anchor every claim in actual retrieved content.

### 3a — Executive Summary (5 bullets)
- What happened (confirmed facts only)
- Why it matters
- Current status: Escalating / Stable / Declining
- Risk level: Low / Medium / High
- Immediate recommended action

### 3b — Timeline of events
Reconstruct from document dates: how the issue started → current moment. Key triggers, escalation moments, notable coverage spikes.

### 3c — Volume & velocity
- Weekly totals from Step 2b
- Daily counts from Step 2c
- Platform breakdown (Twitter/X usually dominates; note YouTube/Reddit for quality signal)
- Direction: escalating, peaking, or declining

### 3d — Sentiment & tone
Estimate: Negative / Mixed / Neutral split (%).
Break down into 5 emotions: Anger, Disgust, Sadness, Anticipation, Fear.
Ground each in actual content themes.

### 3e — Key narratives (3–5)
For each narrative:
- Title
- Whether factual, opinion-driven, or misinformation
- 2-sentence description grounded in retrieved content

### 3f — Key voices & amplifiers
From documents, identify: media outlets, journalists, MPs/politicians, influencers, watchdog accounts. Note reach figures where available.

### 3g — Top coverage (5 items)
Highest-reach or most viral items. For each: headline/post summary, source, reach, why it matters.

### 3h — Risk assessment
- Reputational: Low / Medium / High
- Business impact (sales, partnerships, traffic)
- Legal / regulatory considerations
- Longevity: short-term spike vs sustained

### 3i — Brand response
Summarize any official response found in documents. If none: "No official response identified."

### 3j — Recommendations (5 items)
Actionable, prioritized, grounded in data.

### 3k — What to watch
Forward-looking signals: escalation triggers, upcoming events, emerging narratives.

---

## Step 4 — Build the HTML infographic

Render the report as an interactive HTML widget using `visualize:show_widget`. Call `visualize:read_me` with `["mockup", "data_viz"]` first.

### Layout structure (in order)

1. **Teal header** — brand name, "Issues & Crisis Report" pill, brief subtitle, meta row (date range, channels, generated timestamp)
2. **Red alert bar** — "!" icon, 1–2 sentence crisis summary
3. **4 KPI cards** — teal-bordered, light teal bg: Est. Total Mentions, Reputational Risk, Peak Week, Brand Response
4. **Section 01 — Executive Summary** — 5 bullet items with colored dots (red for critical, gold for caution, teal for neutral)
5. **Section 02 — Situation Overview** — intro paragraph + timeline (date column, teal dot, connector line, text)
6. **Section 03 — Volume & Velocity** — daily bar chart (pure SVG — see below) + platform breakdown card + weekly trend card
7. **Section 04 — Sentiment & Tone** — single card with internal two-col layout: left (donut SVG + emotion bars), right (sentiment drivers). Full-width sentiment note at bottom.
8. **Section 05 — Key Narratives** — list of narrative cards with badge (Factual / Opinion / Counter-narrative / Misinformation)
9. **Section 06 — Key Voices & Amplifiers** — 4-col voice grid with name, role, badge, reach
10. **Section 07 — Top Coverage** — 5 coverage cards with source, headline, badge, impact note
11. **Section 08 — Risk Assessment** — risk items with left-border severity coloring (red/orange/gold) + summary table
12. **Section 09 — Brand Response** — no-response box or response summary
13. **Section 10 — Recommendations** — 5 items with numbered teal circles
14. **Section 11 — What to Watch** — arrow-prefixed watch items
15. **Teal footer** — Meltwater logo mark + report metadata

### Sentiment donut — ALWAYS pure inline SVG

Never use Chart.js or any library for the sentiment donut. Use stroke-dasharray/stroke-dashoffset. Pattern (circumference = 251.327 for r=40):

```html
<svg width="90" height="90" viewBox="0 0 110 110">
  <g transform="rotate(-90 55 55)">
    <!-- Negative (78%): 251.327 × 0.78 = 196.035 -->
    <circle cx="55" cy="55" r="40" fill="none" stroke="#E24B4A" stroke-width="22"
      stroke-dasharray="196.035 251.327" stroke-dashoffset="0"/>
    <!-- Mixed (15%): 251.327 × 0.15 = 37.699, offset = -196.035 -->
    <circle cx="55" cy="55" r="40" fill="none" stroke="#28BBBB" stroke-width="22"
      stroke-dasharray="37.699 251.327" stroke-dashoffset="-196.035"/>
    <!-- Neutral (7%): 251.327 × 0.07 = 17.593, offset = -233.734 -->
    <circle cx="55" cy="55" r="40" fill="none" stroke="#EAEAEA" stroke-width="22"
      stroke-dasharray="17.593 251.327" stroke-dashoffset="-233.734"/>
  </g>
  <circle cx="55" cy="55" r="29" fill="#fff"/>
  <text x="55" y="51" text-anchor="middle" font-size="12" font-weight="900"
    fill="#E24B4A" font-family="Nunito Sans,sans-serif">78%</text>
  <text x="55" y="63" text-anchor="middle" font-size="9"
    fill="#4C4D4F" font-family="Nunito Sans,sans-serif">negative</text>
</svg>
```

Scale each segment: `dasharray = circumference × pct / 100`. Each offset = `-1 × sum_of_prior_segment_lengths`.

---

## Step 5 — Build the daily volume bar chart (CRITICAL: pure SVG only)

**Never use Chart.js or any JavaScript library for the volume chart.** Chart.js requires JS execution which does not run in PDF export, resulting in a blank white box. Always use a pure inline SVG generated from the data.

Use Python (`bash_tool`) to generate the SVG programmatically:

```python
data = [...]  # daily counts, one per day
labels = [...]  # short labels e.g. '10M','11M',...,'1A',...

W, H = 820, 215
pad_left, pad_right, pad_top, pad_bottom = 45, 15, 20, 50
chart_w = W - pad_left - pad_right   # 760
chart_h = H - pad_top - pad_bottom   # 145
n = len(data)
max_val = max(data)
bar_slot = chart_w / n
gap = 2.5
bar_w = bar_slot - gap

def bx(i): return pad_left + i * bar_slot + gap/2
def bh(v): return (v / max_val) * chart_h if max_val > 0 else 0
def by_(v): return pad_top + chart_h - bh(v)

# Color coding: identify key event days
def bc(i, event_indices):
    colors = {'spike': '#E24B4A', 'secondary': '#FF6221', 'default': '#28BBBB'}
    return colors.get(event_indices.get(i), colors['default'])

# Include: gridlines, bars, x-axis date labels (every ~5th),
# dashed vertical lines for key events, peak value labels,
# legend strip at bottom
```

Key SVG elements to include:
- Horizontal gridlines at round number intervals (e.g. 0, 100, 200, 300, 400) with Y-axis labels
- One bar per day, colored: teal default, red for primary spike event, orange for secondary events
- Vertical dashed lines for key annotated events
- X-axis labels on selected dates (not every bar — pick ~6–8 meaningful dates)
- Bold/colored x-labels for event days
- Peak value labels floating above the 2 tallest bars
- Legend strip at bottom: colored rect + label for each event annotation

Inject the generated SVG directly into the HTML, replacing any `<canvas>` element.

---

## Step 6 — Export to PDF

After the HTML widget renders in chat, write a complete standalone HTML file and export via Playwright.

```python
# 1. Write standalone HTML to /home/claude/{brand_slug}_crisis_report.html
#    - Complete <!DOCTYPE html>, <head>, <body>
#    - All CSS inline in <style> with @import for Nunito Sans
#    - Use SAME pure inline SVG charts (donut + bar) — never Chart.js
#    - Replace all <a href="..."> link buttons with plain <span> elements

# 2. Render with Playwright
from playwright.sync_api import sync_playwright
with sync_playwright() as p:
    browser = p.chromium.launch()
    page = browser.new_page(viewport={"width": 1100, "height": 900})
    page.goto(f"file:///home/claude/{brand_slug}_crisis_report.html")
    page.wait_for_timeout(3000)  # allow fonts to load
    page.pdf(
        path=f"/home/claude/{brand_slug}_crisis_report.pdf",
        format="A4",
        print_background=True,
        margin={"top": "0mm", "bottom": "0mm", "left": "0mm", "right": "0mm"}
    )
    browser.close()

# 3. Copy to outputs and present
import shutil
shutil.copy(f"/home/claude/{brand_slug}_crisis_report.pdf",
            f"/mnt/user-data/outputs/{brand_slug}_crisis_report.pdf")
```

Then call `present_files` with the output path.

---

## Design rules

- Two-col grids: always `align-items: stretch` + `display: flex; flex-direction: column` on each card — prevents white space gaps between unequal-height cards
- Section 04 (Sentiment): single card with internal two-col layout — do NOT use two separate cards side by side (they will be unequal height)
- No gradients, no box shadows. `border: 1px solid #EAEAEA`, `border-radius: 10px` on all cards
- All body text `color: #000` or `color: #4C4D4F`
- Section headers: `background: #28BBBB`, white text, left label + right title
- KPI cards: `background: #F4FEFE`, `border: 1px solid #C4F4F4`
- Risk items: left-border severity system — red (`#E24B4A`) for Critical, orange (`#FF6221`) for High, gold (`#FFCC01`) for Medium
- Badge system: `.b-red` (critical), `.b-orange` (high/factual-framed), `.b-gold` (medium), `.b-teal` (counter/positive), `.b-gray` (neutral/cultural)

---

## Common issues & fixes

| Issue | Fix |
|-------|-----|
| Daily chart blank in PDF | Replace Chart.js with pure SVG (see Step 5). This is the most common failure — JS never executes in Playwright PDF export |
| Sentiment card whitespace gap | Use single card with internal two-col grid, not two separate cards |
| Stats tool returning 0 counts | Simplify semantic query to 3–5 words; narrow queries with many AND/OR terms return fewer results |
| Inconsistent daily counts | Keep query consistent across all day-by-day calls; the tool generates its own boolean query |
| Weekly vs daily total mismatch | Normal — different query generations produce different boolean queries. Note this in the report |
| PDF cuts off content | No `height: 100vh` constraints on root container; Playwright A4 handles multi-page automatically |
| Fonts not loading in PDF | Add `page.wait_for_timeout(3000)` before `page.pdf()` call |
| Large tool result stored to file | Use bash_tool with python3 to parse: `outer = json.loads(raw); text = outer[0]['text']; data = json.loads(text)` |

---

## Output checklist

Before presenting final output, verify:

- [ ] All 11 sections present and populated with real Meltwater data
- [ ] Daily volume chart is pure SVG (no Chart.js canvas)
- [ ] Sentiment donut is pure inline SVG (no Chart.js)
- [ ] Section 04 uses single-card internal layout (no whitespace gap)
- [ ] Risk items use left-border severity color system
- [ ] All facts cited from actual retrieved documents only
- [ ] No official response: clearly stated if none found
- [ ] PDF exported and presented via `present_files`
- [ ] Meltwater brand colors throughout (teal headers, white body, black text)
- [ ] Footer present on both HTML widget and PDF
