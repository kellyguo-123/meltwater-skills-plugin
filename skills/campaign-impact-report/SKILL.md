---
name: campaign-impact-report
description: >
  Generate a fully branded, client re-skinned Campaign Impact Report — an earned-media intelligence brief measuring the coverage, reach, and resonance of a brand's marketing or PR campaign. Use this skill whenever a user asks for a campaign report, campaign performance analysis, campaign impact brief, or any request to analyze how a brand's campaign, activation, launch, or initiative landed across earned media and social. Trigger on phrases like "build a campaign report for [brand]", "how did [campaign] perform", "what was the impact of [campaign]", "pull from Meltwater and analyze the [campaign] launch", or "campaign coverage report for [brand]". Combines live Meltwater data retrieval (not MIRA), daily volume trends, qualitative synthesis, and a fully client-branded standalone HTML report with a pure SVG chart. Audience is broken down by network using the correct metric per network (news estimated views, TV/radio reach, social reach). Always use for any brand plus campaign plus report combination.
---

# Campaign Impact Report Skill

Produces a fully client-branded (re-skinned), 11-section earned-media campaign performance brief (interactive HTML widget in chat + standalone downloadable HTML file) by pulling live data from Meltwater's unified retrieval tools and synthesizing it with the analyst's own judgment. Focus is on earned media: organic coverage, social amplification, message resonance, and standout content — not paid performance. Audience figures are broken down by network using the correct metric for each (news = estimated views, TV/radio = reach, social = reach).

---

## Step 0 — Gather parameters

Before pulling data, confirm the following (infer from conversation context where possible):

| Parameter | Default |
|-----------|---------|
| Brand name | Required |
| Campaign / activation | Required |
| Date range | Last 30 days |
| Channels | News, X/Twitter, Reddit, YouTube, Broadcast |
| Brand colors | Auto-detect (see Step 1a) |
| Brand logo | Auto-fetch, upload fallback (see Step 1a) |

If the campaign has a known hashtag or tagline, use it to sharpen retrieval, but it is not required.

---

## Step 1 — Establish client branding (full re-skin)

This report is fully re-skinned in the client's brand identity. The client's brand replaces Meltwater's visual identity throughout headers, section bars, KPI cards, charts, and accents. Meltwater appears only as a small "Powered by Meltwater" credit in the footer.

### 1a — Resolve brand colors

Build a client palette with these roles. Map the client's brand colors onto each role:

| Role | Used for |
|------|----------|
| **Primary** | Header background, section header bars, footer, primary chart bars, numbered circles |
| **Secondary** | Standout accents, launch-day chart bars, highlight badges |
| **Light primary** | KPI card backgrounds, card borders, light fills (use a ~10–15% tint of primary, or the client's known light brand tone) |
| **Positive** | Positive sentiment segment (use primary if it reads as positive; otherwise a green) |
| **Caution / mixed** | Watch items, mixed sentiment (a gold/amber from the client palette, or `#FFCC01`) |
| **Negative** | Negative sentiment only, used sparingly (`#E24B4A` or a client red) |
| **Body text** | `#000000` |
| **Secondary text** | `#4C4D4F` |
| **Dividers / neutral** | `#EAEAEA` |

Sourcing brand colors, in order:
1. If the user supplies hex values, use them exactly.
2. If the brand has well-known official colors (e.g. Woolworths green `#178841` / yellow `#FFD100`), use those. State the palette you are using and the source.
3. If unknown, web_search "{brand} brand colors hex" or check the client's site, then confirm the palette with the user before building.

Always state the resolved palette back to the user before rendering, so they can correct it.

### 1b — Resolve brand logo

Get a usable client logo for the header, in this order:

1. **Web fetch (attempt first).** Use `image_search` for `"{brand} logo png transparent"` or `web_search` for the brand's official logo/press/media-kit page, then `web_fetch` the image URL returned. Note: `bash_tool` network access is allowlisted and excludes most image/CDN hosts, so do NOT rely on `curl`/`wget` to download — use the search + fetch tools, which can retrieve URLs surfaced by search. Save the asset to `/home/claude/{brand_slug}_logo.{ext}` and embed it base64-encoded in the HTML so the file stays portable.
2. **Validate before using.** Confirm the fetched asset is (a) the correct brand, (b) reasonable resolution, (c) ideally transparent PNG or SVG. A header background will be the client's primary color, so a logo that works on that color (white/reversed or transparent) is preferred. If only a logo-on-white is available, place it inside a small white rounded container in the header.
3. **Ask for upload (fallback).** If web fetch returns nothing usable, the wrong brand, or a low-quality asset, stop and ask the user to upload the logo (PNG or SVG). Read it from `/mnt/user-data/uploads/`, copy to `/home/claude/`, and embed base64.
4. **Wordmark fallback (last resort, only if user declines to upload).** Render the brand name as a styled wordmark in the header using the primary/secondary palette.

Embed the logo as base64 in both the in-chat widget HTML and the standalone HTML file so it renders identically in chat and in the downloadable file. Example:

```python
import base64, mimetypes
def logo_data_uri(path):
    mime = mimetypes.guess_type(path)[0] or "image/png"
    with open(path, "rb") as f:
        b64 = base64.b64encode(f.read()).decode()
    return f"data:{mime};base64,{b64}"
# <img src="{logo_data_uri(path)}" style="height:42px;" alt="{brand} logo">
```

### 1c — Typography

Default to Nunito Sans (Google Fonts) for readability. If the client has a known, freely-loadable brand font available on Google Fonts (e.g. Poppins, DM Sans), use it instead to strengthen the re-skin. Do not attempt to load licensed/self-hosted brand fonts that are not on Google Fonts; fall back to Nunito Sans.

Note: this is a performance report. The dominant accent is the client's primary color (positive/performance framing). Negative red is reserved only for genuinely negative sentiment.

---

## Step 2 — Pull Meltwater data

Use `Meltwater:unified_retrieval_document_retrieval_tool` and `Meltwater:unified_retrieval_statistics_retrieval_tool`. Always use exact `YYYY-MM-DD` dates. **Do not use MIRA.**

### 2a — Document retrieval (run all 3 queries)

| # | Purpose | Query | Platforms | Sort |
|---|---------|-------|-----------|------|
| 1 | Top earned coverage | `{brand} {campaign} launch coverage feature` | `["news"]` | `reach` |
| 2 | Social amplification & top posts | `{brand} {campaign} reaction buzz response` | `["twitter","reddit","youtube"]` | `engagement` |
| 3 | Advocates & amplifiers | `{brand} {campaign} influencer creator journalist review` | _(all)_ | `relevance` |

For each document, extract:
- `content` (text), `title`, `date`, `platform`, `url`, `author.name`, `author.handle`
- `social_metrics` (reach, views, engagement)
- `editorial_metrics` (newsguard-rating if present)

### 2b — Volume statistics: weekly windows

Pull 5 weekly calls using `Meltwater:unified_retrieval_statistics_retrieval_tool` to get the shape of the campaign over time. Split the 30-day range into weekly buckets:

```
Week 1: startDate to startDate+6
Week 2: startDate+7 to startDate+13
Week 3: startDate+14 to startDate+20
Week 4: startDate+21 to startDate+27
Week 5: startDate+28 to endDate
```

Use a broad semantic query: `"{brand} {campaign}"` with `platforms: ["news","twitter","reddit","youtube","broadcast-tv","broadcast-audio"]`. Record `total.count` for each week.

### 2c — Volume statistics: day-by-day (for the chart)

Pull individual day-by-day stats for accurate daily counts. Group into 1–3 day windows across the full date range. For each window call:

```
query: "{brand} {campaign}"
platforms: ["news","twitter","reddit","youtube","broadcast-tv","broadcast-audio"]
startDate: YYYY-MM-DD
endDate: YYYY-MM-DD (same or +1/+2 days)
```

Key days to isolate individually: launch day, major amplification moments, and any spike days you expect based on the documents retrieved. Record `total.count` for each window, then distribute proportionally within windows where needed.

**Important:** The statistics tool generates its own boolean query from your semantic input. Use broad, simple queries (3–5 words) for higher counts. Narrow queries with many AND/OR terms produce lower, more specific counts. Be consistent across calls so comparisons are valid.

### 2d — Audience metrics by network (do NOT sum into one cumulative score)

Different networks use different audience metrics. Never roll these into a single cumulative reach number — present them per network using the correct metric for each:

| Network | Metric to use | Field |
|---------|---------------|-------|
| News / online | **Estimated views** | `social_metrics.estimated_views` (or the stats tool's estimated views) |
| TV (broadcast-tv) | **Reach** | broadcast reach; label as TV |
| Radio (broadcast-audio) | **Reach** | broadcast reach; label as Radio |
| Social (twitter, reddit, youtube, etc.) | **Reach** | `social_metrics.reach` |

Rules:
- Break TV and Radio out separately wherever the data allows; only combine into "Broadcast" if they cannot be separated, and say so.
- Report each network's audience figure with its metric named in plain language (e.g. "News: 4.2M estimated views", "TV: 1.1M reach", "Radio: 380K reach", "Social: 2.6M reach").
- If you show any aggregate, label it clearly as indicative only, because it mixes estimated views (news) with reach (broadcast/social). Prefer not to show a single blended total.
- Where a metric is missing for a network, state "not available" rather than substituting another metric.

---

## Step 3 — Synthesize insights

Using retrieved documents and stats, derive the following. Anchor every claim in actual retrieved content. Separate observation from interpretation and flag uncertainty where the data is sparse or directional.

### 3a — Executive Summary (5 bullets)
- What the campaign was and when it launched (confirmed facts only)
- Headline result: total mentions + audience by network (News estimated views, TV/Radio reach, Social reach) — not a single blended figure
- Reception: Positive / Mixed / Neutral
- What resonated most (top message or moment)
- Top recommendation for the next phase

### 3b — Campaign timeline
Reconstruct from document dates: launch → amplification milestones → peak → current moment. Key triggers, notable coverage moments, peak day.

### 3c — Volume & velocity
- Weekly totals from Step 2b
- Daily counts from Step 2c
- Platform breakdown with audience by network using the correct metric per network (see Step 2d): News = estimated views, TV/Radio = reach (split where possible), Social = reach
- Direction: building, peaking, or tapering

### 3d — Sentiment & reception
Estimate: Positive / Mixed / Neutral / Negative split (%).
Lead with the positive segment. Break down into themes of reception (e.g. excitement, approval, curiosity, ambivalence). Ground each in actual content.

### 3e — Key messages & themes (3–5)
For each:
- Title
- Whether the intended campaign message is landing (on-message / adjacent / off-message)
- 2-sentence description grounded in retrieved content

### 3f — Top amplifiers & advocates
From documents, identify the earned reach drivers: media outlets, journalists, creators, influencers, organic advocates. Note reach/engagement figures where available.

### 3g — Top coverage & standout content (5 items)
Highest-reach or most engaging earned items. For each: headline/post summary, source, reach/engagement, why it stood out.

### 3h — Performance assessment
- Audience by network: News estimated views, TV reach, Radio reach, Social reach (not a single blended number)
- Engagement quality: depth of resonance, not just volume
- Message pull-through: did the intended message land
- Longevity: one-off spike vs sustained earned momentum

### 3i — Earned vs amplified
Brief read on how much momentum came from organic earned coverage versus creator/influencer amplification. If unclear from data, state so.

### 3j — Recommendations (5 items)
Actionable, prioritized, grounded in data. Focus on optimizing the next campaign phase: messaging, channel focus, advocate engagement, content formats.

### 3k — What's next / sustain & amplify
Forward-looking signals: how to extend momentum, upcoming moments to capitalize on, emerging themes worth leaning into.

---

## Step 4 — Build the HTML infographic

Render the report as an interactive HTML widget using `visualize:show_widget`. Call `visualize:read_me` with `["mockup", "data_viz"]` first.

### Layout structure (in order)

1. **Header (primary color)** — client logo (left), brand name, "Campaign Impact Report" pill, campaign name subtitle, meta row (date range, channels, generated timestamp). Use white/reversed text on the primary-color background.
2. **Headline bar (primary color)** — star/spark icon, 1–2 sentence campaign result summary (the key win)
3. **4 KPI cards** — primary-bordered, light-primary bg: Est. Total Mentions; Audience by network (compact: News views / TV+Radio reach / Social reach — not one blended number); Peak Day; Reception (e.g. "82% positive")
4. **Section 01 — Executive Summary** — 5 bullet items with colored dots (primary for wins, secondary for standout, caution color for watch)
5. **Section 02 — Campaign Timeline** — intro paragraph + timeline (date column, primary dot, connector line, text)
6. **Section 03 — Volume & Velocity** — daily bar chart (pure SVG — see below) + platform breakdown card (each network with its own metric labelled: News estimated views, TV reach, Radio reach, Social reach) + weekly trend card
7. **Section 04 — Sentiment & Reception** — single card with internal two-col layout: left (donut SVG + reception theme bars), right (reception drivers). Full-width note at bottom.
8. **Section 05 — Key Messages & Themes** — list of theme cards with badge (On-message / Adjacent / Off-message)
9. **Section 06 — Top Amplifiers & Advocates** — 4-col grid with name, role, badge, reach
10. **Section 07 — Top Coverage & Standout Content** — 5 cards with source, headline, badge, why it stood out
11. **Section 08 — Performance Assessment** — assessment items with left-border accent coloring (primary strong / secondary standout / caution watch) + summary table
12. **Section 09 — Earned vs Amplified** — short read on organic vs amplified split
13. **Section 10 — Recommendations** — 5 items with numbered primary-color circles
14. **Section 11 — What's Next** — arrow-prefixed items
15. **Footer (primary color)** — client logo or wordmark + report metadata, with a small "Powered by Meltwater" credit

### Sentiment donut — ALWAYS pure inline SVG

Never use Chart.js or any library for the sentiment donut. Use stroke-dasharray/stroke-dashoffset. Lead with the positive segment in the client primary color. Swap `#28BBBB` below for the client's primary (positive) and the inner text fill to match. Pattern (circumference = 251.327 for r=40):

```html
<svg width="90" height="90" viewBox="0 0 110 110">
  <g transform="rotate(-90 55 55)">
    <!-- Positive (82%): 251.327 × 0.82 = 206.088 -->
    <circle cx="55" cy="55" r="40" fill="none" stroke="#28BBBB" stroke-width="22"
      stroke-dasharray="206.088 251.327" stroke-dashoffset="0"/>
    <!-- Mixed/Neutral (13%): 251.327 × 0.13 = 32.672, offset = -206.088 -->
    <circle cx="55" cy="55" r="40" fill="none" stroke="#EAEAEA" stroke-width="22"
      stroke-dasharray="32.672 251.327" stroke-dashoffset="-206.088"/>
    <!-- Negative (5%): 251.327 × 0.05 = 12.566, offset = -238.760 -->
    <circle cx="55" cy="55" r="40" fill="none" stroke="#E24B4A" stroke-width="22"
      stroke-dasharray="12.566 251.327" stroke-dashoffset="-238.760"/>
  </g>
  <circle cx="55" cy="55" r="29" fill="#fff"/>
  <text x="55" y="51" text-anchor="middle" font-size="12" font-weight="900"
    fill="#28BBBB" font-family="Nunito Sans,sans-serif">82%</text>
  <text x="55" y="63" text-anchor="middle" font-size="9"
    fill="#4C4D4F" font-family="Nunito Sans,sans-serif">positive</text>
</svg>
```

Scale each segment: `dasharray = circumference × pct / 100`. Each offset = `-1 × sum_of_prior_segment_lengths`.

---

## Step 5 — Build the daily volume bar chart (CRITICAL: pure SVG only)

**Never use Chart.js or any JavaScript library for the volume chart.** Use a pure inline SVG generated from the data. This keeps the standalone HTML file fully portable and reliable — it renders identically in any browser, when emailed, or hosted, with no dependency on JS execution. Always use a pure inline SVG generated from the data.

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

# Color coding: highlight launch + peak amplification days
# Use the client palette: PRIMARY for peak, SECONDARY for launch, LIGHT_PRIMARY default
def bc(i, event_indices):
    colors = {'peak': PRIMARY, 'launch': SECONDARY, 'default': LIGHT_PRIMARY}
    return colors.get(event_indices.get(i), colors['default'])

# Include: gridlines, bars, x-axis date labels (every ~5th),
# dashed vertical lines for launch/peak, peak value labels,
# legend strip at bottom
```

Key SVG elements to include:
- Horizontal gridlines at round number intervals with Y-axis labels
- One bar per day, colored: light-primary default, solid primary for peak day, secondary for launch day
- Vertical dashed lines for launch and peak annotations
- X-axis labels on selected dates (not every bar — pick ~6–8 meaningful dates)
- Bold/colored x-labels for milestone days
- Peak value labels floating above the 2 tallest bars
- Legend strip at bottom: colored rect + label for each annotation

Inject the generated SVG directly into the HTML, replacing any `<canvas>` element.

---

## Step 6 — Output as standalone HTML

The deliverable is a single self-contained HTML file (no PDF). After the widget renders in chat, write a complete standalone HTML file, save it to outputs, and present it.

```python
import shutil

# 1. Write standalone HTML to /home/claude/{brand_slug}_campaign_report.html
#    - Complete <!DOCTYPE html>, <head>, <body>
#    - Fully self-contained: all CSS inline in <style> with @import for the chosen font
#    - Client palette as :root CSS variables (see Design rules)
#    - Logo embedded as base64 data URI (NOT a remote URL) so the file is portable
#    - Use the SAME pure inline SVG charts (donut + bar) — never Chart.js
#    - Real <a href="..."> links to source articles/posts are fine in HTML output
#      (keep them; they are useful in a browser). Open in a new tab with target="_blank".
#    - No external dependencies except the Google Fonts @import

# 2. Copy to outputs and present
shutil.copy(f"/home/claude/{brand_slug}_campaign_report.html",
            f"/mnt/user-data/outputs/{brand_slug}_campaign_report.html")
```

Then call `present_files` with the output HTML path.

Notes:
- Keep the in-chat interactive widget (Step 4) AND produce the standalone HTML file as the downloadable deliverable.
- Charts stay pure inline SVG so they render without any JS — this keeps the HTML portable and reliable when opened in any browser or emailed.
- For sharing as a link, the file can be dropped on Netlify (rename to `index.html`).

---

## Design rules

Define the resolved client palette once as CSS variables at the top of the stylesheet and reference them everywhere, so the re-skin is consistent and easy to verify:

```css
:root {
  --primary: #XXXXXX;        /* client primary */
  --secondary: #XXXXXX;      /* client secondary */
  --light-primary: #XXXXXX;  /* ~10-15% tint of primary */
  --caution: #FFCC01;        /* or client amber */
  --negative: #E24B4A;       /* used sparingly */
}
```

- Two-col grids: always `align-items: stretch` + `display: flex; flex-direction: column` on each card — prevents white space gaps between unequal-height cards
- Section 04 (Sentiment): single card with internal two-col layout — do NOT use two separate cards side by side (they will be unequal height)
- No gradients, no box shadows. `border: 1px solid #EAEAEA`, `border-radius: 10px` on all cards
- All body text `color: #000` or `color: #4C4D4F`
- Section headers: `background: var(--primary)`, white text, left label + right title
- KPI cards: `background: var(--light-primary)`, `border: 1px solid var(--primary)`
- Performance items: left-border accent system — primary for strong performance, secondary for standout, caution for watch/mixed
- Badge system: `.b-primary` (on-message/positive), `.b-secondary` (standout), `.b-gold` (adjacent/mixed), `.b-gray` (neutral), `.b-red` (off-message/negative — use sparingly)
- Header/footer use `var(--primary)` background with white/reversed logo and text
- Ensure text contrast on the primary background: if the client primary is light, use dark text and a dark logo variant instead of white

---

## Common issues & fixes

| Issue | Fix |
|-------|-----|
| Daily chart blank when file opened | Use pure SVG (see Step 5), never a Chart.js `<canvas>` — a canvas with no JS renders empty in a static HTML file |
| Sentiment card whitespace gap | Use single card with internal two-col grid, not two separate cards |
| Stats tool returning 0 counts | Simplify semantic query to 3–5 words; narrow queries with many AND/OR terms return fewer results |
| Inconsistent daily counts | Keep query consistent across all day-by-day calls; the tool generates its own boolean query |
| Weekly vs daily total mismatch | Normal — different query generations produce different boolean queries. Note this in the report |
| Long report scrolls awkwardly | No `height: 100vh` constraints on the root container; let content flow naturally in the page |
| Large tool result stored to file | Use bash_tool with python3 to parse: `outer = json.loads(raw); text = outer[0]['text']; data = json.loads(text)` |
| Logo download fails via curl/wget | bash network is allowlisted and blocks most image hosts. Use `image_search`/`web_search` then `web_fetch` the URL; if still no good asset, ask the user to upload |
| Logo missing/broken in HTML | Embed logo as base64 data URI, never a remote URL — keeps the file portable and avoids broken images |
| Logo invisible on header | Header background is the client primary color; use a white/reversed logo, or place a logo-on-white inside a white rounded container |
| Wrong brand logo fetched | Validate the asset is the correct brand before embedding; if unsure, ask the user to confirm or upload |
| Blended reach figure looks wrong | Don't sum across networks — news uses estimated views, TV/radio/social use reach. Show per-network metrics; label any aggregate as indicative only |

---

## Output checklist

Before presenting final output, verify:

- [ ] All 11 sections present and populated with real Meltwater data
- [ ] Daily volume chart is pure SVG (no Chart.js canvas)
- [ ] Sentiment donut is pure inline SVG (no Chart.js), positive-led in client primary color
- [ ] Section 04 uses single-card internal layout (no whitespace gap)
- [ ] Performance items use left-border accent color system
- [ ] Audience broken down by network with correct metric each (news = estimated views, TV/radio = reach split where possible, social = reach); no blended cumulative figure unless labelled indicative
- [ ] All facts cited from actual retrieved documents only
- [ ] Earned-media focus maintained throughout (no paid metrics invented)
- [ ] Standalone HTML file written, copied to outputs, and presented via `present_files`
- [ ] HTML is self-contained (inline CSS, base64 logo, SVG charts) — opens correctly with no external dependencies
- [ ] Client palette applied throughout via CSS variables; resolved palette stated to user
- [ ] Client logo embedded as base64 and visible in both widget and HTML file (or confirmed wordmark fallback)
- [ ] Text contrast holds on the primary-color header/footer
- [ ] Footer present on both HTML widget and HTML file, with "Powered by Meltwater" credit
