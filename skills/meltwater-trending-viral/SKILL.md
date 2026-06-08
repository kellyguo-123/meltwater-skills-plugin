---
name: meltwater-trending-viral
description: >
  Generate a fully branded Meltwater Trending & Viral Posts Report — a visual media intelligence brief showing the top viral posts, trending topics, and highest-engagement content for any brand, competitor, or topic. Use this skill whenever a user asks for a trending report, viral content analysis, top posts, most-shared content, engagement leaders, what's going viral, social trending brief, hot topics, top-performing content, or buzz analysis. Also trigger for "what's trending for [brand]", "show me the most viral posts about [topic]", "what content is performing best", "pull top engaging posts from Meltwater", "what's resonating with audiences", "build a viral content report", or "what's getting the most shares/likes/comments". This skill combines live Meltwater data retrieval (engagement-sorted), trend velocity analysis, AI synthesis, and a branded HTML infographic plus downloadable PDF with platform leaderboards and viral post cards. Always use for any brand/topic + viral/trending + report combination
---

# Trending & Viral Posts Report Skill

Produces a fully Meltwater-branded, 10-section trending intelligence brief (interactive HTML in chat + downloadable PDF) by pulling live engagement-ranked data from Meltwater's unified retrieval tools.

---

## Step 0 — Gather parameters

| Parameter | Default |
|-----------|---------|
| Brand / topic | Required |
| Date range | Last 7 days |
| Channels | News, Twitter/X, Instagram, TikTok, YouTube, Reddit |

**Broadcast (TV/radio/audio) is excluded by default.** Only add it if the user explicitly asks.

---

## Step 1 — Read the Meltwater brand skill

Read `/mnt/skills/user/meltwater-brand/SKILL.md` before building any visual output. Key values:

- **Teal** `#28BBBB` — headers, section bars, accents, footer
- **Purple** `#B627A1` — viral accents, peak-day bars, engagement badges
- **Orange** `#FF6221` — rising/hot signals
- **Gold** `#FFCC01` — peak moment highlights
- **Instagram pink** `#C13584` — Instagram platform colour
- **TikTok black** `#000000` — TikTok platform colour
- **Light Teal** `#C4F4F4` — card borders/backgrounds
- **Charcoal** `#4C4D4F` — secondary text
- **Font:** Nunito Sans (Google Fonts fallback)

---

## Step 2 — Pull Meltwater data

Use `unified_retrieval_document_retrieval_tool` and `unified_retrieval_statistics_retrieval_tool`. Always use exact `YYYY-MM-DD` dates. **Do not use MIRA.**

### 2a — Document retrieval (4 queries)

| # | Purpose | Query | Platforms | Sort | Limit |
|---|---------|-------|-----------|------|-------|
| 1 | Top viral social posts | `{topic} viral trending popular` | `["twitter","instagram","tiktok","reddit","youtube"]` | `engagement` | 15 |
| 2 | Top news by reach | `{topic} coverage story report` | `["news"]` | `reach` | 8 |
| 3 | Rising/emerging content | `{topic} new launch update announcement` | `["twitter","instagram","tiktok","reddit","news"]` | `relevance` | 8 |
| 4 | Cross-platform amplifiers | `{topic}` | `["youtube","reddit"]` | `engagement` | 6 |

If the user provides a `savedSearchId`, pass it to all queries via `savedSearchIds: [id]`.

Extract per document: `content`, `title`, `date`, `platform`, `url`, `author.name`, `author.handle`, `social_metrics` (reach, views, engagement, likes, shares, comments), `editorial_metrics` (newsguard-rating if present).

### 2b — Daily volume + platform breakdown (1 stats call)

One call covers both the daily trend chart and platform breakdown:

```
query: "{topic} trending viral"
platforms: ["news","twitter","instagram","tiktok","youtube","reddit"]
startDate: YYYY-MM-DD
endDate: YYYY-MM-DD
```

The response buckets by both `date` and `platform` — extract daily totals per platform, then sum across platforms for the trend chart.

**Stats tool note:** Keep queries to 3–5 words. Be consistent across calls.

---

## Step 3 — Synthesize insights

Anchor every claim in actual retrieved content.

### 3a — Viral Pulse Summary (3 bullets)
- What's driving the highest engagement right now
- Which platform is leading (note: Instagram/TikTok often generate 5–10x engagement per post vs Twitter for the same story — always flag this if observed)
- Standout single item (highest engagement post) and any platform-surprise insight

### 3b — Trending Topics Leaderboard (5–8 topics)
Cluster all content by theme. For each: topic label (2–4 words), hottest platforms, momentum badge.

**⚠ This section goes SECOND — immediately after Viral Pulse Summary, before the viral post cards.**

### 3c — Top Viral Posts (up to 10)
From Queries 1 + 4. For each: platform, author/handle, post preview (~120 chars), date, engagement metrics, and "why it spread" explanation.

### 3d — Top News by Reach (up to 5)
From Query 2. For each: outlet, headline, date, reach, what made it travel.

### 3e — Engagement Volume Trend
Daily totals from Step 2b. Note the top 2 peak days and the events that caused them.

### 3f — Platform Breakdown
Character summary per platform. Key insight pattern: **Instagram/TikTok volume is low but per-post engagement is often much higher than Twitter** — always note this explicitly if the data supports it.

### 3g — Engagement Leaders (5–6)
Top voices/outlets by engagement. Note platform, content type, reach/engagement figure.

### 3h — Rising Content (3 items)
From Query 3. Newest content with strong early engagement signals.

### 3i — Content Format & Audience Signal
Best-performing formats (IG carousel vs Reel vs TikTok vs Twitter short-form) and emotional sharing motivations.

### 3j — Strategic Takeaways (5 items)
Actionable for content, comms, or marketing. Include platform-specific opportunities and any Instagram/TikTok engagement gap insight.

---

## Step 4 — Build the HTML infographic

Call `visualize:read_me` with `["mockup","data_viz"]` first, then render with `visualize:show_widget`.

### Section order (critical — do not reorder)

1. Teal header — topic, "Trending & Viral Report" pill, date range, meta row
2. Purple pulse bar — 1–2 sentence viral summary
3. 4 KPI cards (teal-bordered): Total Mentions · Top Platform · Peak Engagement Post · Peak Day
4. **Section 01** — Viral Pulse Summary (3 bullets)
5. **Section 02** — Trending Topics Leaderboard ← **directly after Viral Pulse**
6. **Section 03** — Top Viral Posts (2-col card grid)
7. **Section 04** — Top News by Reach
8. **Section 05** — Engagement Trend Chart (pure SVG)
9. **Section 06** — Platform Breakdown (3-col grid, 6 platforms)
10. **Section 07** — Engagement Leaders
11. **Section 08** — Rising Content (3-col row)
12. **Section 09** — Content Format & Audience Signal (single card, internal 2-col)
13. **Section 10** — Strategic Takeaways
14. Teal footer

### Platform badge colours

```css
.pt-tw { background: #1DA1F2; }  /* Twitter/X */
.pt-ig { background: #C13584; }  /* Instagram */
.pt-tt { background: #000000; }  /* TikTok */
.pt-yt { background: #FF0000; }  /* YouTube */
.pt-rd { background: #FF4500; }  /* Reddit */
.pt-nw { background: #4C4D4F; }  /* News */
```

### Viral post card spec

```html
<div class="post-card">
  <div class="post-header">
    <span class="plat-badge pt-[platform]">[Platform]</span>
    <span class="post-date">[Date]</span>
  </div>
  <div class="post-author">@[handle] · [Name]</div>
  <div class="post-preview">[First 120 chars]</div>
  <div class="eng-bar-wrap">
    <div class="eng-bar-fill" style="width:[pct]%;
      background: linear-gradient(to right,#B627A1,#28BBBB);"></div>
  </div>
  <div class="metrics-row">
    <span>❤️ [likes]</span><span>🔁 [shares]</span>
    <span>👁 [views]</span><span>↗ [reach]</span>
  </div>
  <div class="spread-note">💡 [Why it spread]</div>
</div>
```

Engagement bar: normalize against the highest-engagement item (= 100%).

### Trending Topics leaderboard spec

```html
<table class="lb-table">
  <thead><tr><th>Rank</th><th>Topic</th><th>Platforms</th>
    <th>Share</th><th>Momentum</th></tr></thead>
  <tbody>
    <tr>
      <td><span class="rank-badge r1">1</span></td>
      <td><span class="topic-lbl">[Topic]</span></td>
      <td>[platform badges]</td>
      <td><div class="vol-bar-wrap">
        <div class="vol-bar-fill" style="width:[pct]%"></div></div></td>
      <td><span class="mom-badge mom-fire">🔥 Rising</span></td>
    </tr>
  </tbody>
</table>
```

Momentum badges: `.mom-fire` (purple bg) = Rising, `.mom-peak` (gold bg) = Peaking, `.mom-steady` (teal bg) = Steady.

---

## Step 5 — Build the engagement trend chart (CRITICAL: pure SVG only)

**Never use Chart.js or any JS library.** Use Python (`bash_tool`) to generate inline SVG:

```python
data = [...]    # daily mention counts (sum across all platforms per day)
labels = [...]  # date labels e.g. 'Apr 19'

# Width: 700 for 7-day windows, 820 for 14-day+ windows
W, H = 700, 180
pad_left, pad_right, pad_top, pad_bottom = 42, 12, 20, 45
chart_w = W - pad_left - pad_right
chart_h = H - pad_top - pad_bottom
n = len(data)
max_val = max(data)
bar_slot = chart_w / n
gap = 5
bar_w = bar_slot - gap

# Top 2 days = purple, rest = teal
sorted_idx = sorted(range(n), key=lambda i: data[i], reverse=True)
hot = set(sorted_idx[:2])

def bar_color(i): return '#B627A1' if i in hot else '#28BBBB'

# Include: gridlines, bars, x-axis labels, peak value labels, legend strip
```

Inject the SVG string directly into the HTML.

---

## Step 6 — Export to PDF

```python
# 1. Write /home/claude/{topic_slug}_trending_report.html
#    - Full <!DOCTYPE html> with all CSS inline
#    - Same pure inline SVG chart
#    - Replace <a href="..."> links with <span> elements

# 2. Playwright export
from playwright.sync_api import sync_playwright
with sync_playwright() as p:
    browser = p.chromium.launch()
    page = browser.new_page(viewport={"width": 1100, "height": 900})
    page.goto(f"file:///home/claude/{topic_slug}_trending_report.html")
    page.wait_for_timeout(3000)
    page.pdf(
        path=f"/home/claude/{topic_slug}_trending_report.pdf",
        format="A4", print_background=True,
        margin={"top":"0mm","bottom":"0mm","left":"0mm","right":"0mm"}
    )
    browser.close()

import shutil
shutil.copy(f"/home/claude/{topic_slug}_trending_report.pdf",
            f"/mnt/user-data/outputs/{topic_slug}_trending_report.pdf")
```

Call `present_files` with the output path.

---

## Design rules

- No gradients except the engagement bar fill (decorative exception)
- No box shadows. `border: 1px solid #EAEAEA`, `border-radius: 10px` on all cards
- Section 09 (Format + Audience): single card with internal 2-col — never two separate cards
- `align-items: stretch` on all 2-col grids to prevent unequal height gaps
- All body text `color: #000` or `color: #4C4D4F`
- Section headers: `background: #28BBBB`, white text

---

## Common issues & fixes

| Issue | Fix |
|-------|-----|
| Chart blank in PDF | Pure SVG only — Chart.js never executes in Playwright |
| Card height gaps in grid | Add `align-items: stretch` to grid container |
| Stats tool returning low counts | Simplify to 3–5 word query |
| Section 09 whitespace gap | Single card with internal 2-col, not two separate cards |
| Fonts not loading in PDF | `page.wait_for_timeout(3000)` before `page.pdf()` |

---

## Output checklist

- [ ] Sections in correct order: Viral Pulse → **Leaderboard** → Posts → News → Chart → Platforms → Leaders → Rising → Format → Takeaways
- [ ] No broadcast platforms unless explicitly requested
- [ ] Viral post engagement bars normalised (top post = 100%)
- [ ] Instagram/TikTok per-post engagement insight noted if applicable
- [ ] Trend chart is pure SVG (width 700 for 7-day, 820 for 14-day+)
- [ ] Platform breakdown shows Instagram and TikTok engagement insight
- [ ] Section 09 uses single-card internal 2-col layout
- [ ] PDF exported and presented via `present_files`
- [ ] Meltwater brand colours throughout
- [ ] Footer present on both HTML and PDF
