---
name: meltwater-reddit-intelligence
description: >
  Generate a fully branded Meltwater Reddit Intelligence Report — a multi-section media intelligence brief analyzing any subreddit or Reddit-scoped saved search. Use this skill whenever a user asks to analyze Reddit data, community sentiment, subreddit activity, or brand perception on Reddit using Meltwater. Also trigger when the user says things like "build a Reddit report for [brand]", "analyze [brand] on Reddit", "pull from Meltwater and analyze r/[subreddit]", "what is the Reddit community saying about [topic]", "Reddit intelligence for [brand]", or "run a Reddit brand pulse". Produces a Meltwater-branded HTML widget (rendered in chat) and a downloadable PDF with: daily volume chart, real sentiment breakdown, brand position, emerging themes, risks, complaint clusters, top posts with live links, opportunities, and strategic recommendations. Always use for any Reddit + Meltwater + analysis/report combination — even if the user doesn't say "Reddit Intelligence" explicitly.
---

# Meltwater Reddit Intelligence Skill

Produces a fully Meltwater-branded Reddit Intelligence Report by pulling live data from Meltwater's retrieval tools, synthesizing it with AI, rendering an interactive HTML widget, and exporting a downloadable PDF.

---

## Step 0 — Gather parameters

Confirm before pulling data (infer from conversation where possible):

| Parameter | Default |
|-----------|---------|
| Brand / topic name | Required |
| Saved Search ID | Required (look up with `list_searches_metadata` if not provided) |
| Date range | Last 30 days |
| Subreddit name | Infer from saved search name or ask |

If no saved search ID is provided, call `list_searches_metadata` with a name filter to find the right one. Inspect its structure with `get_search_runes` to confirm it's scoped to the right subreddit.

---

## Step 1 — Pull volume and sentiment stats (ALWAYS use statistics tool, NOT document tool)

**Critical:** The `unified_retrieval_document_retrieval_tool` returns only a semantic sample of the dataset — never use it for volume or sentiment numbers. Always use `unified_retrieval_statistics_retrieval_tool` for KPIs.

### 1a — Daily volume (required for chart)
```
tool: unified_retrieval_statistics_retrieval_tool
query: "total post count by day"
savedSearchIds: [<id>]
startDate: <start>
endDate: <end>
```
Returns `total.count` (total mentions) and `buckets` array with per-day counts. The **daily average** = total / number of days.

### 1b — Sentiment breakdown
```
tool: unified_retrieval_statistics_retrieval_tool
query: "<brand> Reddit posts count by sentiment"
platforms: ["reddit"]
savedSearchIds: [<id>]
startDate: <start>
endDate: <end>
```
Returns buckets keyed `neutral`, `negative`, `positive`, `unknown`. Compute percentages from total (exclude `unknown`).

---

## Step 2 — Pull qualitative documents (5 thematic queries)

Run all 5 queries using `unified_retrieval_document_retrieval_tool`. Use `limit: 15` and `sortBy: "engagement"` for each. All queries use the same `savedSearchIds`, `startDate`, `endDate`.

| # | Purpose | Query string |
|---|---------|-------------|
| 1 | Brand perception, loyalty, identity | `brand perception quality nostalgia loyalty community positive experiences` |
| 2 | Pricing, value, cost complaints | `price expensive value menu cost increase inflation` |
| 3 | Product launches, innovation, new items | `new product launch menu innovation praise excitement` |
| 4 | Operations, food safety, drive-thru, staff | `operations drive thru service staff food safety quality complaint` |
| 5 | Risks, controversy, boycott signals | `controversy complaint negative criticism boycott scandal` |

From each document, extract and store:
- `content` (post/comment text — the insight)
- `title` (thread title)
- `date`
- `url` — **preserve exactly for clickable links**
- `author.handle`
- `social_metrics.engagement` (= comment count in API)
- `social_metrics.reach`

### ⚠️ Critical API limitation: engagement ≠ upvotes

The API's `sortBy: "engagement"` sorts by **comment count**, NOT Reddit upvote score. The Meltwater UI sorts by **upvote score**. This means truly viral posts (high upvotes, moderate comments) may not surface via API engagement sort. When reporting "top posts," note this limitation and recommend checking the Meltwater UI for upvote-sorted view. Use comment count as the available proxy.

---

## Step 3 — Synthesize insights

Using all retrieved documents, derive the following. Anchor every claim in actual retrieved content.

### 3a — Brand position (4 themes)
Identify 4 distinct themes from the data: positive attachments, innovation signals, identity narratives, community dynamics. Each needs a 2-sentence description citing specific data points.

### 3b — Sentiment framing
With real numbers from Step 1b, frame the sentiment narrative. Note: Reddit communities often skew neutral (discussion-mode) at 40–55%, with negative outweighing positive 1.5–2.5x on brand subreddits.

### 3c — Emerging themes (3 clusters)
Group content into 3 narrative clusters (e.g., pricing pressure, product quality, operations). Each cluster has 2 sub-points with a title and 2-sentence description.

### 3d — Risks (3–4 risks)
Assign severity: **Critical** (active brand damage, food safety, viral negative), **High** (identity/loyalty erosion, pricing defection), **Medium** (latent risks). Each needs a title, severity, and 2–3 sentence description with evidence.

### 3e — Complaint clusters (4 categories)
Group recurring complaints: product quality, price/value, operations/service, discontinued items or loyalty. 2-sentence description each.

### 3f — Top posts (7 posts)
Select 7 highest-engagement posts from the retrieved data. Preserve exact `url` values. Include title, author, date, quote from content, engagement stats, and a tag (Viral, Positive, Negative, Insight).

### 3g — Opportunities (4 items)
Identify 4 business opportunities grounded in community signals: innovation wins, revival opportunities, loyalty fixes, narrative campaigns.

### 3h — Recommendations (5 items)
Write 5 prioritised, actionable recommendations ordered by urgency. Each has a bold title and 2–3 sentence rationale.

---

## Step 4 — Build the HTML widget

Render as an interactive HTML widget using `visualize:show_widget`. Load `visualize:read_me` with `["mockup", "data_viz"]` first.

### Layout (in order)

1. **Teal header** — brand name, "Reddit Intelligence Report" title, date range + saved search ID meta
2. **4 KPI cards** (teal bg) — Total Mentions, Daily Average (with ↓/↑ delta if prior period available), Dominant Sentiment, Peak Day
3. **Section 00 — Daily Volume Chart** — inline SVG bar chart (see spec below), legend
4. **Section 01 — Brand Position + Sentiment** — two-col: left = 4 brand themes with icons; right = sentiment donut (inline SVG) + sentiment bars with actual counts + emotion breakdown + note
5. **Section 02 — Emerging Themes** — 3-col card grid
6. **Section 03 — Risks** — left-bordered risk items with severity badges (Critical=red, High=orange, Medium=gold)
7. **Section 04 — Complaints** — 2×2 orange-tinted grid
8. **Section 05 — Top Posts** — ranked post rows with platform badge, date, content quote, stats, tag pill, and **clickable "View post ↗" link** using exact `url` from data
9. **Section 06 — Opportunities** — 2×2 teal-tinted grid
10. **Section 07 — Recommendations** — 5 numbered teal items
11. **Teal footer** — Meltwater brand + metadata

### Meltwater brand colors
- Teal: `#28BBBB` (headers, accents, section labels)
- Light Teal: `#C4F4F4` (card borders, backgrounds, KPI borders)
- EAF9F9: section/KPI background
- Orange: `#FF6221` (high severity, peak bars)
- Red: `#E24B4A` (critical severity, negative sentiment)
- Gold: `#FFCC01` (medium severity)
- Purple: `#B627A1` (secondary emotion)
- Charcoal: `#4C4D4F` (secondary text)
- Grey: `#EAEAEA` (dividers)
- Font: Nunito Sans (Google Fonts import)

### Daily volume bar chart — ALWAYS use inline SVG (never Chart.js)

Chart.js canvas does not render in Playwright PDF exports. Always use pure inline SVG computed from the daily bucket data.

```python
# Compute from Step 1a daily buckets:
SVG_W, SVG_H = 730, 155
LP, RP, TP, BP = 38, 6, 8, 28
chart_w = SVG_W - LP - RP   # usable width
chart_h = SVG_H - TP - BP   # usable height
max_val = max(bucket counts)
n = len(buckets)             # number of days
slot = chart_w / n
bar_w = min(14, slot * 0.7)
bar_offset = (slot - bar_w) / 2

# Bar colors:
# count >= 1000: #FF6221 (peak/orange)
# count >= 700:  #28BBBB (elevated/teal)
# count < 700:   #C4F4F4 (baseline/light teal)

# For each day i, count v:
h = v * chart_h / max_val
x = LP + i * slot + bar_offset
y = TP + chart_h - h
# <rect x="{x:.1f}" y="{y:.1f}" width="{bar_w}" height="{h:.1f}" fill="{color}" rx="2"/>

# Y-axis gridlines at 0, max/4, max/2, 3*max/4, max
# X-axis labels every ~5 days + first + last
# Annotate peak bar with value
```

Generate the SVG string in Python, embed directly in HTML as `<svg viewBox="0 0 730 155" style="width:100%;height:auto;">`.

### Sentiment donut — ALWAYS use inline SVG (never Chart.js)

```
circumference = 2 * π * 40 = 251.3274
neutral_dash  = neutral_pct  * 251.3274
negative_dash = negative_pct * 251.3274
positive_dash = positive_pct * 251.3274

neutral segment:  stroke-dashoffset=0
negative segment: stroke-dashoffset = -neutral_dash
positive segment: stroke-dashoffset = -(neutral_dash + negative_dash)
```

Colors: Neutral=`#CCCCCC`, Negative=`#E24B4A`, Positive=`#28BBBB`

### Source links
Every post in Section 05 must have a `<a href="{url}" target="_blank">View post ↗</a>` button. Only link if `url` is a real URL from the data — never use `#`.

---

## Step 5 — Export to PDF

After the HTML widget renders in chat, write a standalone HTML file and export via Playwright.

```python
# 1. Write standalone HTML to /home/claude/{slug}_reddit_report.html
#    - Full <!DOCTYPE html> with <head>, <body>
#    - All CSS inline in <style> tags (import Nunito Sans via @import url())
#    - Same inline SVG charts (no Chart.js)
#    - Replace all <a href="..."> link buttons with <span class="post-src">{domain} ↗</span>
#      (hyperlinks aren't reliably clickable in all PDF viewers)

# 2. Render to PDF with Playwright
from playwright.sync_api import sync_playwright
import shutil

slug = brand_name.lower().replace(" ", "_")
with sync_playwright() as p:
    browser = p.chromium.launch()
    page = browser.new_page(viewport={"width": 860, "height": 1200})
    page.goto(f'file:///home/claude/{slug}_reddit_report.html')
    page.wait_for_timeout(3000)   # allow fonts + SVG to render
    page.pdf(
        path=f'/home/claude/{slug}_reddit_report.pdf',
        format='A4',
        print_background=True,
        margin={'top': '0mm', 'bottom': '0mm', 'left': '0mm', 'right': '0mm'}
    )
    browser.close()

shutil.copy(
    f'/home/claude/{slug}_reddit_report.pdf',
    f'/mnt/user-data/outputs/{slug}_reddit_report.pdf'
)
# 3. Call present_files with the output path
```

---

## Common issues & fixes

| Issue | Fix |
|-------|-----|
| Volume = 873 instead of 17.9K | You used document_retrieval (sample) instead of statistics_retrieval. Always use statistics for KPIs. |
| Chart.js missing from PDF | Replace with inline SVG — Chart.js canvas requires browser JS which Playwright PDF doesn't execute before capture |
| Foot massage / viral post missing from top posts | API engagement = comment count; UI engagement = upvotes. High-upvote/low-comment posts won't surface via API sort. Note limitation in report. |
| "Impossible query" 500 error | Platform conflict: don't combine `platforms: ["forum"]` with subreddit-specific `savedSearchIds`. Use `query: "*"` with savedSearchIds only, or use `platforms: ["reddit"]` without platform: forum. |
| Sentiment query fails with "can't filter only on date range" | Add a semantic query string alongside savedSearchIds — can't pass date range without a query |
| Top post URLs missing | `url` is nested at `resource.url` in document results — extract from `resource` key, not top-level |
| PDF cuts content | Playwright A4 handles multi-page automatically. Ensure no `height: 100vh` constraints on root container |

---

## Output checklist

- [ ] KPI numbers sourced from `statistics_retrieval` (not document sample)
- [ ] Sentiment percentages match statistics API (neutral typically 40–55% on Reddit)
- [ ] Daily volume chart uses inline SVG with all 30 days visible, colored by threshold
- [ ] Sentiment donut is inline SVG (not Chart.js canvas)
- [ ] Section 05 top posts have working `<a href>` links to exact Reddit URLs
- [ ] PDF exported via Playwright with `print_background=True`, A4, zero margins
- [ ] PDF link buttons replaced with plain text domain references
- [ ] Footer shows saved search ID, date range, total mentions, daily avg
- [ ] Meltwater brand colors applied throughout

---

## Quick reference: data pull summary

```
Step 1a: statistics_retrieval → "total post count by day"        → KPIs + chart data
Step 1b: statistics_retrieval → "<brand> posts count by sentiment" → Sentiment %s
Step 2a: document_retrieval   → "brand perception nostalgia..."   → Section 01 themes
Step 2b: document_retrieval   → "price expensive value..."        → Section 02+04 pricing
Step 2c: document_retrieval   → "new product launch innovation..."→ Section 02+06 innovation
Step 2d: document_retrieval   → "operations drive thru service..."→ Section 02+03+04 ops
Step 2e: document_retrieval   → "controversy complaint negative..."→ Section 03 risks
```

All document pulls: `savedSearchIds: [<id>]`, `startDate`, `endDate`, `limit: 15`, `sortBy: "engagement"`
