# GenAI Lens Report — HTML Structure Reference

This document defines the mandatory section sequence, CSS patterns, and HTML component templates for the GenAI Lens HTML report. All reports follow this structure. Colours are applied via CSS variables set per-brand (see `brand-theming.md`).

---

## CSS Variables (set per-brand)

Every report must define these CSS variables on `:root`. The brand-theming workflow populates them.

```css
:root {
  --brand-primary: #E72024;      /* Header, footer, section headers, accents */
  --brand-primary-light: #FFF8F8; /* KPI card background, highlighted card bg */
  --brand-primary-border: #FAD7D8; /* KPI card border */
  --brand-secondary: #FFC72C;     /* TL;DR icon, "why it matters" callouts */
  --brand-accent: #9B1B1F;        /* Darker variant for secondary accents */
  --positive: #2E7D32;            /* Positive themes, positive list dots */
  --negative: var(--brand-primary); /* Negative themes — defaults to brand primary */
  --charcoal: #4C4D4F;            /* Secondary text */
  --dark: #1A1A1A;                /* TL;DR bar bg, dark card headers */
  --border: #EAEAEA;              /* Card borders */
  --border-light: #F4F4F4;        /* Inner dividers */
  --bg-light: #FAFAFA;            /* Quote block backgrounds */
  --bg-gold: #FFF6DC;             /* "Why it matters" background */
  --gold-border: #FFC72C;         /* "Why it matters" border */
  --white: #FFFFFF;
}
```

---

## Page Structure

```
Container (max-width: 1100px, centered)
├── Header (brand-primary background)
├── TL;DR Bar (dark background)
├── KPI Row (4 cards)
├── Section 01: Executive Summary
├── Section 02: Competitive AI Snapshot
├── Section 03: Strengths, Gaps & Sources
├── Section 04: The Narrative Loop
├── Section 05: Recommended Moves
└── Footer (brand-primary background)
```

---

## Global Styles

```css
* { box-sizing: border-box; margin: 0; padding: 0; }
body {
  font-family: 'Nunito Sans', -apple-system, BlinkMacSystemFont, sans-serif;
  color: #000;
  background: #fff;
  line-height: 1.5;
  -webkit-font-smoothing: antialiased;
}
.container { max-width: 1100px; margin: 0 auto; background: #fff; }
```

Google Fonts import:
```html
<link rel="preconnect" href="https://fonts.googleapis.com">
<link href="https://fonts.googleapis.com/css2?family=Nunito+Sans:wght@300;400;600;700;800;900&display=swap" rel="stylesheet">
```

---

## Component: Header

Full-width bar with the brand's primary colour as background.

**Required content:**
- Pill badge: "GenAI Lens Report" (uppercase, small, translucent white bg)
- Brand name: Large (38px), weight 900
- Subtitle: The prompt question(s) tested, in italics within the sentence
- Right-aligned metadata: Date range, LLM count + response count, "PREPARED BY MELTWATER"

```html
<div class="header"> <!-- background: var(--brand-primary) -->
  <div class="header-top">
    <div class="header-left">
      <div class="pill">GenAI Lens Report</div>
      <h1>[Brand Name]</h1>
      <div class="subtitle">How AI models answer: <em>"[Prompt question]"</em> — and what's encoded as fact about [Brand].</div>
    </div>
    <div class="header-meta">
      <div>[DATE RANGE]</div>
      <div>[N] LLMS · [N] RESPONSES</div>
      <div>PREPARED BY MELTWATER</div>
    </div>
  </div>
</div>
```

**CSS:**
```css
.header {
  background: var(--brand-primary);
  color: #fff;
  padding: 36px 44px 30px;
}
.header-top {
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  gap: 24px;
}
.header-left h1 {
  font-size: 38px;
  font-weight: 900;
  letter-spacing: -0.5px;
  margin-bottom: 6px;
}
.header-left .pill {
  display: inline-block;
  background: rgba(255,255,255,0.18);
  border: 1px solid rgba(255,255,255,0.4);
  padding: 4px 12px;
  border-radius: 100px;
  font-size: 11px;
  font-weight: 700;
  letter-spacing: 0.5px;
  text-transform: uppercase;
  margin-bottom: 14px;
}
.header-left .subtitle {
  font-size: 16px;
  font-weight: 400;
  max-width: 640px;
  opacity: 0.95;
  line-height: 1.45;
}
.header-meta {
  text-align: right;
  font-size: 11px;
  font-weight: 600;
  letter-spacing: 0.4px;
  opacity: 0.95;
  line-height: 1.7;
  min-width: 200px;
}
.header-meta div { white-space: nowrap; }
```

---

## Component: TL;DR Bar

A dark bar immediately below the header with a single-sentence headline finding.

```html
<div class="tldr">
  <div class="tldr-icon">!</div>
  <div class="tldr-text"><strong>[Bold headline phrase]</strong> [Supporting context sentence.]</div>
</div>
```

**CSS:**
```css
.tldr {
  background: var(--dark);
  color: #fff;
  padding: 18px 44px;
  display: flex;
  align-items: center;
  gap: 16px;
}
.tldr-icon {
  width: 36px; height: 36px;
  background: var(--brand-secondary);
  color: #000;
  border-radius: 50%;
  display: flex; align-items: center; justify-content: center;
  font-weight: 900;
  font-size: 18px;
  flex-shrink: 0;
}
.tldr-text { font-size: 14.5px; line-height: 1.5; font-weight: 400; }
.tldr-text strong { font-weight: 800; }
```

---

## Component: KPI Row

A 4-column grid of metric cards. Use brand-primary-light background, brand-primary-border for card borders.

```html
<div class="kpi-row">
  <div class="kpi">
    <div class="kpi-label">[LABEL]</div>
    <div class="kpi-value red">[VALUE]</div>  <!-- add .red class for brand-primary coloured values -->
    <div class="kpi-sub">[Context line]</div>
  </div>
  <!-- repeat 4x -->
</div>
```

**CSS:**
```css
.kpi-row {
  display: grid;
  grid-template-columns: repeat(4, 1fr);
  gap: 14px;
  padding: 24px 44px 8px;
}
.kpi {
  background: var(--brand-primary-light);
  border: 1px solid var(--brand-primary-border);
  border-radius: 10px;
  padding: 18px 18px 16px;
  page-break-inside: avoid;
  break-inside: avoid;
}
.kpi-label {
  font-size: 10.5px;
  font-weight: 700;
  text-transform: uppercase;
  letter-spacing: 0.6px;
  color: var(--charcoal);
  margin-bottom: 8px;
}
.kpi-value {
  font-size: 32px;
  font-weight: 900;
  color: #000;
  line-height: 1;
  margin-bottom: 6px;
}
.kpi-value.red { color: var(--brand-primary); }
.kpi-sub {
  font-size: 11px;
  color: var(--charcoal);
  line-height: 1.4;
}
```

---

## Component: Section Header

Used for each numbered section. Brand primary background, white text.

```html
<div class="section">
  <div class="section-header">
    <div class="label">[NN] · [SECTION LABEL]</div>
    <div class="title">[Insight-driven subtitle]</div>
  </div>
  <!-- section content -->
</div>
```

**CSS:**
```css
.section { padding: 28px 44px 4px; }
.section-header {
  background: var(--brand-primary);
  color: #fff;
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 12px 18px;
  border-radius: 6px;
  margin-bottom: 18px;
}
.section-header .label {
  font-size: 11px;
  font-weight: 700;
  letter-spacing: 1px;
  opacity: 0.9;
}
.section-header .title {
  font-size: 15px;
  font-weight: 800;
  letter-spacing: 0.3px;
}
```

---

## Section 01: Executive Summary

A vertical list of finding items, each with a coloured dot and title + description.

Use a variety of dot colours: brand-primary, brand-accent, brand-secondary, charcoal, orange (#F26F21).

```html
<div class="exec-summary">
  <div class="exec-item">
    <div class="exec-dot dot-red"></div>  <!-- .dot-red = brand primary -->
    <div class="exec-content">
      <div class="exec-title">[Finding title — insight, not label]</div>
      <div class="exec-desc">[Evidence-backed description. Include specific numbers, model names, sources.]</div>
    </div>
  </div>
  <!-- repeat 4-6 items -->
</div>
```

**CSS:**
```css
.exec-summary { display: flex; flex-direction: column; gap: 10px; }
.exec-item {
  display: flex;
  gap: 14px;
  padding: 14px 18px;
  background: #fff;
  border: 1px solid var(--border);
  border-radius: 10px;
  align-items: flex-start;
  page-break-inside: avoid;
  break-inside: avoid;
}
.exec-dot {
  width: 10px; height: 10px;
  border-radius: 50%;
  margin-top: 7px;
  flex-shrink: 0;
}
.dot-red { background: var(--brand-primary); }
.dot-darkred { background: var(--brand-accent); }
.dot-gold { background: var(--brand-secondary); }
.dot-charcoal { background: var(--charcoal); }
.dot-orange { background: #F26F21; }
.exec-content { flex: 1; }
.exec-title { font-weight: 800; font-size: 13.5px; margin-bottom: 3px; color: #000; }
.exec-desc { font-size: 13px; color: var(--charcoal); line-height: 1.5; }
```

---

## Section 02: Competitive AI Snapshot

A 2x2 grid of competitor cards. Each card has a coloured top-bar using that competitor's brand colour.

The subject brand's card is highlighted with a thicker border and tinted background.

```html
<div class="compete-grid">
  <!-- Standard competitor card -->
  <div class="compete-card">
    <div class="top-bar" style="background: [competitor-brand-colour];"></div>
    <div class="body">
      <div class="compete-rank">
        <span class="rank-chip" style="background: [competitor-brand-colour];">#[N]</span>
        <span class="compete-name">[BRAND NAME]</span>
      </div>
      <div class="compete-stats">
        <div><span>INCLUSION</span> <strong>[N]%</strong></div>
        <div><span>POS FRAME</span> <strong>[N]%</strong></div>
      </div>
      <div class="compete-section-title pos">Positives</div>
      <ul class="compete-list pos">
        <li>[Point with evidence]</li>
      </ul>
      <div class="compete-section-title neg">Negatives</div>
      <ul class="compete-list neg">
        <li>[Point with evidence]</li>
      </ul>
    </div>
  </div>

  <!-- Subject brand card (highlighted) -->
  <div class="compete-card" style="border: 2px solid var(--brand-primary); box-shadow: 0 2px 0 var(--brand-primary);">
    <div class="top-bar" style="background: var(--brand-primary);"></div>
    <div class="body" style="background: var(--brand-primary-light);">
      <!-- same internal structure -->
    </div>
  </div>
</div>
```

**CSS:**
```css
.compete-grid {
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: 12px;
  align-items: stretch;
}
.compete-card {
  border-radius: 10px;
  overflow: hidden;
  border: 1px solid var(--border);
  background: #fff;
  page-break-inside: avoid;
  break-inside: avoid;
}
.compete-card .top-bar { height: 6px; }
.compete-card .body { padding: 16px 18px 18px; }
.compete-rank { display: flex; align-items: center; gap: 10px; margin-bottom: 12px; }
.rank-chip {
  display: inline-block;
  padding: 3px 10px;
  border-radius: 100px;
  font-size: 11px;
  font-weight: 800;
  color: #fff;
}
.compete-name { font-size: 18px; font-weight: 900; letter-spacing: 0.5px; color: #000; }
.compete-stats {
  display: flex; gap: 24px;
  margin-bottom: 14px;
  font-size: 11.5px;
  color: var(--charcoal);
}
.compete-stats strong { color: #000; font-weight: 800; font-size: 14px; margin-left: 6px; }
.compete-section-title {
  font-size: 10px;
  font-weight: 800;
  letter-spacing: 0.8px;
  text-transform: uppercase;
  margin: 10px 0 6px;
}
.compete-section-title.pos { color: var(--positive); }
.compete-section-title.neg { color: var(--brand-primary); }
.compete-list { list-style: none; margin-bottom: 4px; }
.compete-list li {
  font-size: 12px;
  line-height: 1.45;
  padding: 5px 0 5px 16px;
  position: relative;
  color: #000;
}
.compete-list.pos li::before {
  content: '';
  position: absolute;
  left: 0; top: 11px;
  width: 6px; height: 6px;
  background: var(--positive);
  border-radius: 50%;
}
.compete-list.neg li::before {
  content: '';
  position: absolute;
  left: 0; top: 11px;
  width: 6px; height: 6px;
  background: var(--brand-primary);
  border-radius: 50%;
}
```

---

## Section 03: Strengths, Gaps & Sources

### Two-column layout: Positives and Negatives

```html
<div class="twocol">
  <div class="card">
    <div class="card-header" style="background: var(--positive);">What LLMs say — Positives</div>
    <div class="item">
      <div class="label" style="color: var(--positive);">[Theme] <span style="color: var(--charcoal); font-weight:600; font-size:11px;">([N]% of responses)</span></div>
      <div class="desc"><em>"[LLM quote]"</em> — [Model name]. [Context.]</div>
    </div>
  </div>
  <div class="card">
    <div class="card-header red">What LLMs say — Negatives & Risks</div>
    <div class="item">
      <div class="label" style="color: var(--brand-primary);">[Theme]</div>
      <div class="desc">[Evidence-backed description.]</div>
    </div>
  </div>
</div>
```

### Source Table

```html
<div class="sources-card">
  <div class="card-header dark">Top Sources Feeding LLM Responses</div>
  <table class="sources">
    <thead>
      <tr>
        <th style="width: 32px;">#</th>
        <th>Source</th>
        <th style="width: 80px;">Mentions</th>
        <th>Impact on [Brand] narrative</th>
      </tr>
    </thead>
    <tbody>
      <tr>
        <td class="rank">1</td>
        <td class="source-name">[Source name]</td>
        <td class="mentions">[N]</td>
        <td class="impact">[One-line impact description]</td>
      </tr>
    </tbody>
  </table>
</div>
```

### Key Gap Callout

```html
<div class="key-gap">
  <strong>KEY GAP:</strong> [Single most important source gap finding.]
</div>
```

**CSS for two-column cards:**
```css
.twocol { display: grid; grid-template-columns: 1fr 1fr; gap: 14px; align-items: stretch; }
.card {
  background: #fff;
  border: 1px solid var(--border);
  border-radius: 10px;
  padding: 18px 20px;
  display: flex;
  flex-direction: column;
}
.card-header {
  font-size: 11px;
  font-weight: 800;
  letter-spacing: 0.8px;
  text-transform: uppercase;
  color: #fff;
  background: var(--positive);
  padding: 6px 12px;
  border-radius: 4px;
  margin: -18px -20px 14px;
  border-top-left-radius: 10px;
  border-top-right-radius: 10px;
}
.card-header.red { background: var(--brand-primary); }
.card-header.gold { background: var(--brand-secondary); color: #000; }
.card-header.dark { background: var(--dark); }
.card .item {
  margin-bottom: 12px;
  padding-bottom: 12px;
  border-bottom: 1px solid var(--border-light);
}
.card .item:last-child { border-bottom: none; margin-bottom: 0; padding-bottom: 0; }
.card .item .label { font-size: 13px; font-weight: 800; color: #000; margin-bottom: 4px; }
.card .item .desc { font-size: 12.5px; color: var(--charcoal); line-height: 1.5; }
.card .item .desc em { font-style: italic; color: #000; }
```

**CSS for source table:**
```css
.sources-card {
  background: #fff;
  border: 1px solid var(--border);
  border-radius: 10px;
  overflow: hidden;
  margin-top: 14px;
}
.sources-card .card-header { margin: 0; border-radius: 0; padding: 10px 18px; background: var(--dark); }
table.sources { width: 100%; border-collapse: collapse; font-size: 12.5px; }
table.sources th {
  text-align: left;
  padding: 10px 14px;
  background: #F8F8F8;
  font-size: 10.5px;
  font-weight: 800;
  letter-spacing: 0.6px;
  text-transform: uppercase;
  color: var(--charcoal);
  border-bottom: 1px solid var(--border);
}
table.sources td { padding: 11px 14px; border-bottom: 1px solid var(--border-light); vertical-align: top; }
table.sources tr:last-child td { border-bottom: none; }
table.sources tr { page-break-inside: avoid; break-inside: avoid; }
table.sources td.rank { font-weight: 900; color: var(--brand-primary); width: 32px; }
table.sources td.source-name { font-weight: 700; color: #000; }
table.sources td.mentions { font-weight: 800; color: var(--brand-primary); width: 70px; }
table.sources td.impact { color: var(--charcoal); }
```

**CSS for key gap:**
```css
.key-gap {
  background: var(--brand-primary-light);
  border: 1px solid var(--brand-primary);
  border-left: 4px solid var(--brand-primary);
  padding: 12px 16px;
  border-radius: 8px;
  margin-top: 14px;
  font-size: 13px;
  color: #000;
}
.key-gap strong { color: var(--brand-primary); font-weight: 800; }
```

---

## Section 04: The Narrative Loop

Three vertically stacked cards representing the reputation flow: Social Media > News Media > LLM/AI Answers.

Each card has a coloured header and contains quote blocks with "Why it matters" callouts.

```html
<div class="loop-grid">
  <div class="loop-card loop-social">
    <div class="step-header">
      <div class="num">01 — Hard to control</div>
      <div class="title">Social Media</div>
    </div>
    <div class="body">
      <div class="quote-block">
        <div class="quote-source">[Platform] · [Specific source] · [Context]</div>
        <div class="quote-text">"[Verbatim or near-verbatim quote from LLM response citing this source]"</div>
        <div class="quote-cite">[URL or source reference]</div>
      </div>
      <div class="why-matters">
        <strong>Why it matters:</strong> [Explanation of commercial/strategic significance]
      </div>
    </div>
  </div>
  <!-- loop-news and loop-llm follow same pattern -->
</div>
```

**Loop card header colours:**
- `.loop-social .step-header` → `background: var(--dark)` (#1A1A1A)
- `.loop-news .step-header` → `background: var(--charcoal)` (#4C4D4F)
- `.loop-llm .step-header` → `background: var(--brand-primary)`

**Quote block left-border colours match the loop card type:**
- `.loop-social .quote-block` → `border-left-color: var(--dark)`
- `.loop-news .quote-block` → `border-left-color: var(--charcoal)`
- `.loop-llm .quote-block` → `border-left-color: var(--brand-primary)`

**CSS:**
```css
.loop-grid { display: block; }
.loop-card {
  border: 1px solid var(--border);
  border-radius: 10px;
  overflow: hidden;
  background: #fff;
  margin-bottom: 14px;
  page-break-inside: avoid;
  break-inside: avoid;
}
.loop-card .step-header { padding: 14px 18px; color: #fff; }
.loop-card .step-header .num { font-size: 11px; font-weight: 800; letter-spacing: 1px; opacity: 0.85; }
.loop-card .step-header .title { font-size: 14px; font-weight: 900; letter-spacing: 0.3px; margin-top: 2px; }
.loop-card .body { padding: 16px 18px 18px; }
.loop-card .body > .quote-block { margin-bottom: 10px; }

.quote-block {
  background: var(--bg-light);
  border-left: 3px solid var(--brand-primary);
  padding: 10px 12px;
  border-radius: 4px;
}
.quote-source { font-size: 10.5px; font-weight: 800; color: var(--brand-primary); margin-bottom: 4px; letter-spacing: 0.3px; }
.quote-text { font-size: 12px; color: #000; line-height: 1.5; font-style: italic; margin-bottom: 4px; }
.quote-cite { font-size: 10px; color: var(--charcoal); }

.why-matters {
  background: var(--bg-gold);
  border: 1px solid var(--gold-border);
  padding: 10px 12px;
  border-radius: 6px;
  font-size: 11.5px;
  color: #000;
  line-height: 1.5;
  margin-top: 10px;
}
.why-matters strong { font-weight: 800; }

/* Loop card type overrides */
.loop-social .step-header { background: var(--dark); }
.loop-social .quote-block { border-left-color: var(--dark); }
.loop-social .quote-source { color: var(--dark); }
.loop-news .step-header { background: var(--charcoal); }
.loop-news .quote-block { border-left-color: var(--charcoal); }
.loop-news .quote-source { color: var(--charcoal); }
.loop-llm .step-header { background: var(--brand-primary); }
.loop-llm .quote-block { border-left-color: var(--brand-primary); }
.loop-llm .quote-source { color: var(--brand-primary); }
```

---

## Section 05: Recommended Moves

Numbered recommendation cards with brand-primary left border and numbered circles.

```html
<div class="recs">
  <div class="rec">
    <div class="rec-num">[N]</div>
    <div class="rec-content">
      <div class="rec-title">[Action-oriented title — verb-first, specific]</div>
      <div class="rec-desc">[Evidence-backed description. Cite the specific data point that drives this recommendation.]</div>
    </div>
  </div>
</div>
```

**CSS:**
```css
.recs { display: flex; flex-direction: column; gap: 12px; }
.rec {
  display: flex;
  gap: 14px;
  background: #fff;
  border: 1px solid var(--border);
  border-left: 4px solid var(--brand-primary);
  border-radius: 10px;
  padding: 16px 18px;
  page-break-inside: avoid;
  break-inside: avoid;
}
.rec-num {
  width: 32px; height: 32px;
  background: var(--brand-primary);
  color: #fff;
  border-radius: 50%;
  display: flex; align-items: center; justify-content: center;
  font-weight: 900;
  font-size: 14px;
  flex-shrink: 0;
}
.rec-content { flex: 1; }
.rec-title { font-size: 14px; font-weight: 800; color: #000; margin-bottom: 4px; }
.rec-desc { font-size: 12.5px; color: var(--charcoal); line-height: 1.5; }
```

---

## Component: Footer

Full-width bar with brand primary background.

```html
<div class="footer">
  <div class="footer-brand">PREPARED BY MELTWATER · GENAI LENS</div>
  <div class="footer-meta">
    <div>[BRAND] · [DATE RANGE] · [N] RESPONSES</div>
    <div>Prompt tested across [model list]</div>
  </div>
</div>
```

**CSS:**
```css
.footer {
  background: var(--brand-primary);
  color: #fff;
  padding: 22px 44px;
  margin-top: 28px;
  display: flex;
  justify-content: space-between;
  align-items: center;
}
.footer-brand { font-size: 11px; font-weight: 700; letter-spacing: 0.4px; opacity: 0.95; }
.footer-meta { font-size: 10.5px; text-align: right; opacity: 0.95; line-height: 1.5; letter-spacing: 0.3px; }
```

---

## Print / PDF Styles

```css
@page { size: A4; margin: 0; }
@media print {
  body { background: #fff; }
  .container { max-width: 100%; }
  .compete-card, .loop-card, .card, .rec, .exec-item, .kpi {
    page-break-inside: avoid;
    break-inside: avoid;
  }
  .section-header { page-break-after: avoid; break-after: avoid; }
  h1, h2, h3, .compete-name, .rec-title, .exec-title { page-break-after: avoid; break-after: avoid; }
}
.kpi { page-break-inside: avoid; break-inside: avoid; }
.compete-card, .loop-card, .card, .rec, .exec-item {
  page-break-inside: avoid;
  break-inside: avoid;
}
```

---

## Content Rules

1. **Section headers are insight-driven**: The `.title` in each section header should be a takeaway, not a generic label. "How Coles' reputation is built — and lost — in 2026" not "The Narrative Loop".

2. **Quote blocks require attribution**: Every `.quote-source` must name the platform, specific source, and context. Every `.quote-text` must be a real quote or close paraphrase from the LLM response data.

3. **Key gap must be specific**: The `.key-gap` callout should name the brand's own site, its citation count (often 0), and contrast it with a competitor's owned content performance.

4. **Recommendations are verb-first**: Every `.rec-title` starts with an action verb. "Build a...", "Reframe value around...", "Defend the...", "Treat [source] as...", "Lock in a..."

5. **Competitive cards use real brand colours**: Each competitor's `.top-bar` and `.rank-chip` use that competitor's actual brand colour, not the subject brand's colour. The subject brand's card uses `var(--brand-primary)`.

6. **Executive summary dots vary**: Use all available dot colours (dot-red, dot-darkred, dot-gold, dot-charcoal, dot-orange) across the exec summary items. Do not use the same colour for consecutive items.

7. **Adapt section count to data**: If there are fewer than 3 competitors in the data, the competitive snapshot may use a different grid (3x1 or 2x1). If the narrative loop doesn't have strong social media evidence, that card can be shorter or combined.
