---
name: genai-lens-report
description: "Generates brand-coloured HTML GenAI Lens intelligence reports from a GenAI Lens CSV/XLSX export. Use whenever the user asks to create a GenAI Lens report, GenAI analysis, LLM reputation report, AI visibility report, or GEO analysis. Trigger on 'GenAI Lens', 'GenAI report', 'LLM report', 'AI visibility', 'GEO report', 'how LLMs see [brand]', or when a Meltwater GenAI Lens export is uploaded. Also trigger on 'run the GenAI report', 'build the GenAI report', or brand reputation analysis from LLM/AI responses. Handles parsing, brand colour detection, sentiment/theme/source analysis, screenshot integration, executive insights, and final HTML rendering with PDF export. Always use even for partial requests (e.g. 'do the GenAI report from this CSV')."
---

# GenAI Lens Report Skill

## Overview

This skill generates executive-ready, brand-coloured HTML intelligence reports from Meltwater GenAI Lens data exports. Reports analyse how LLMs (ChatGPT, Google AI Mode, Google AI Overviews, Meta Llama, Deepseek, Perplexity) respond to brand-relevant queries and provide GEO (Generative Engine Optimisation) strategy recommendations.

The output is a single-page HTML document styled with the subject brand's colours, designed for both browser viewing and PDF export via Playwright. The format follows the structure defined in `references/html-structure.md`.

**Read `references/html-structure.md` before generating any report.** It contains the mandatory section sequence, content requirements, HTML/CSS component patterns, and layout specifications.

**Read `references/brand-theming.md` before applying brand colours.** It contains the brand colour detection workflow and CSS variable mapping.

---

## Inputs

The skill accepts three types of input:

1. **CSV/XLSX export from GenAI Lens** (required) — The primary data source.
2. **Screenshots from GenAI Lens UI** (optional) — May include Top Brands Visibility, Mentions, Sentiment, positive/negative aspects with counts, SOV panels. Extract data visually and integrate into analysis.
3. **User-specified details** (optional) — Additional context, specific angles to cover, prior report comparisons, client-specific framing, or MCP enrichment preferences.

---

## Workflow

### Step 0: Gather Context and Clarify

Before starting any analysis, ask the user:

1. **MCP enrichment**: "Should I also query Meltwater's live news and social monitoring tools to enrich this report with recent media coverage and social conversation data? This adds context beyond the GenAI Lens export but requires the Meltwater MCP connection."

2. **Review the data** and present a summary of what you found:
   - Brand name
   - Date range
   - Number of responses
   - Models tested
   - Prompts tested
   - Any screenshots provided and what they show

3. **Recommend additions**: Based on the data, suggest what else would strengthen the report:
   - "The data only covers 1 prompt — recommend expanding to 3-5 prompts for broader coverage."
   - "No competitive screenshot data was provided — I can build the competitive snapshot from the CSV but screenshot data on visibility scores, mention counts and sentiment would add precision."
   - "I notice [gap] — want me to address this with MCP data or flag it as a limitation?"
   - "Based on the themes I see, I'd recommend adding a section on [specific angle]."

4. **Ask any clarifying questions** before proceeding:
   - Is there a previous report to compare against?
   - Any specific narrative or angle the client cares about?
   - Should competitors be included in the competitive snapshot? Which ones?
   - Any topics to avoid or emphasise?

**Wait for user confirmation before proceeding to Step 1.**

### Step 1: Parse Inputs

**CSV/XLSX export** — The GenAI Lens export has two sheets:

| Sheet | Key Columns |
|-------|------------|
| `Overview` | Date range (From/To), Timezone, Selected models, Prompt folders + names + questions |
| `Results` | ID, Model name, Prompt folder, Prompt title, Prompt question, Prompt Response, Date, Sentiment (POS/NEU/NEG), Key phrases, Organizations and brands, Products and people, Cited links |

Parse with pandas. For CSV files, try `encoding='utf-16', sep='\t'` first; fall back to `encoding='utf-8', sep=','`. For XLSX, use openpyxl.

Extract:
- Date range
- Models tested
- All unique prompts (folder, title, question)
- Total response count
- Sentiment distribution (POS/NEU/NEG counts and percentages)
- Per-model sentiment breakdown
- All cited links (flatten, deduplicate, count frequency)
- All organizations/brands mentioned (flatten, deduplicate, count)
- All key phrases (flatten, deduplicate, count)
- Full response texts for thematic analysis

**Screenshots** — Extract data from screenshots visually. Screenshot data often contains competitive context (visibility scores, mention counts, aspect counts) that the CSV alone may not capture.

### Step 2: Detect Brand Colours

Read `references/brand-theming.md` for the full brand colour detection workflow.

Summary:
1. Identify the brand name from the data.
2. Look up the brand's primary colour, secondary colour, and accent colour using known brand palettes (see reference file for Australian brand database).
3. If the brand is not in the database, use web search to find the brand's official website and extract colours from the logo/site.
4. Generate the CSS variable set for the report.
5. Confirm the colour palette with the user before rendering: "I'll use [Primary: #hex], [Secondary: #hex], [Accent: #hex] for the report. Does that look right?"

### Step 3: Analyse the Data

Perform the following analyses. **Read `references/html-structure.md` for exactly which analyses map to which sections.**

1. **Executive summary findings**: Identify the 4-6 most important findings. Each should be a single sentence with supporting evidence. Rank by commercial impact.

2. **KPI extraction**: Calculate 4 headline KPIs for the KPI row:
   - Recommendation rank or sentiment score
   - Inclusion/mention rate
   - Positive framing percentage
   - Primary negative theme or source risk level
   - Compare against competitors if data supports it.

3. **Competitive AI snapshot**: If the prompt names multiple brands or screenshot data shows competitive context, build a competitive card for each brand. For each:
   - Inclusion rate
   - Positive framing percentage
   - Top 3-4 positives (with evidence from responses)
   - Top 3-4 negatives (with evidence from responses)
   - Use each competitor's actual brand colour for their card top-bar and rank chip.

4. **Strengths, gaps and sources**:
   - **Positives column**: Top 3-5 positive themes with response percentages and specific LLM quotes.
   - **Negatives column**: Top 3-5 negative themes/risks with response percentages and specific LLM quotes.
   - **Source table**: Top 7-10 most frequently cited sources/domains. For each: rank, source name, citation count, impact on brand narrative. Flag any owned-content gaps (e.g., brand's own site not appearing).
   - **Key gap callout**: Identify the single most important source gap and call it out.

5. **Narrative loop** (The Reputation Engine): Show how the brand's reputation flows through three stages:
   - **Social Media** (hard to control): Reddit threads, Facebook groups, Instagram creators cited by LLMs. Include specific quotes and citation counts.
   - **News Media** (manageable with PR): Key articles, reports (CHOICE, ACCC, industry reports) driving the narrative. Include specific publication names and citation counts.
   - **LLM/AI Answers** (the new frontier): How each model synthesises the above into its answer. Include specific model quotes.
   - Each stage gets a "Why it matters" callout.

6. **Recommendations**: 4-6 specific, actionable recommendations. Each must:
   - Be directly tied to a finding from the data
   - Have a bold, action-oriented title
   - Include specific detail on what to do and why
   - Be ranked by priority/urgency

7. **Business implications**: If the data warrants it (complex dataset, multiple risks), synthesise into 3 commercial risk/opportunity blocks. Each with: what LLMs say, business impact, recommended action.

### Step 4: Generate the HTML

Read `references/html-structure.md` for the exact section sequence, CSS component patterns, and layout specifications.

**Critical rules**:
- Use the brand colour CSS variables throughout — never hardcode Meltwater teal or any default palette.
- The header and footer use the brand's primary colour as background.
- KPI cards use a light tint of the brand's primary colour for background and the primary colour for accent values.
- Section headers use the brand's primary colour as background.
- Recommendation numbers, rank badges, source table rank numbers, and quote block left-borders all use the brand's primary colour.
- The TL;DR bar uses dark charcoal (#1A1A1A) background with the brand's secondary or accent colour for the icon.
- Competitor cards use each competitor's own brand colour for their top-bar.
- Green (#2E7D32) for positive themes/headers; brand primary colour for negative themes/headers.
- Include `@page` and `@media print` rules for clean PDF export.
- Use Google Fonts: `Nunito Sans` with weights 300, 400, 600, 700, 800, 900.
- Max container width: 1100px, centered.
- All content padding: 44px horizontal.

**Font**: Always use Nunito Sans from Google Fonts. This is the report font, distinct from Meltwater's own brand font.

### Step 5: Generate PDF

Use Playwright with Chromium for PDF export:

```bash
pip install playwright --break-system-packages
playwright install chromium
```

```python
from playwright.sync_api import sync_playwright
import time

with sync_playwright() as p:
    browser = p.chromium.launch()
    page = browser.new_page()
    page.goto(f'file:///path/to/report.html')
    time.sleep(2)  # Wait for fonts and SVG rendering
    page.pdf(
        path='report.pdf',
        format='A4',
        print_background=True,
        margin={'top': '0', 'right': '0', 'bottom': '0', 'left': '0'}
    )
    browser.close()
```

### Step 6: QA

Open the HTML file and visually inspect. Check for:
- Brand colours applied correctly throughout
- No text overflow or truncation
- Tables render cleanly
- Quote blocks are properly formatted
- KPI row is balanced (4 cards, equal width)
- Competitive cards are balanced (2x2 grid)
- Print/PDF view doesn't break cards across pages
- Footer contains correct brand name, date range, response count

### Step 7: Deliver

Copy both files to outputs:
```bash
cp report.html /mnt/user-data/outputs/[brand]_genai_lens_report.html
cp report.pdf /mnt/user-data/outputs/[brand]_genai_lens_report.pdf
```

Use `present_files` to share both.

---

## Adapting to Different Brands/Contexts

The skill adapts to the brand and context while maintaining the core section structure:

- **Retail brands** (Bunnings, Coles, Woolworths): Focus on pricing perception, competitor SOV, ethical reputation, product range comparisons.
- **Financial services** (ANZ, Westpac, CBA): Focus on trust signals, employer reputation, product comparison, regulatory framing.
- **Logistics/services** (Australia Post): Focus on service quality, competitor alternatives, aggregator displacement.
- **Government/public sector**: Measured, policy-aware tone. Focus on narrative accuracy, source quality, misinformation risk.
- **Tech/SaaS**: Focus on feature comparison, review site dominance, analyst mentions, competitive positioning.
- **Any brand**: The analysis framework (exec summary > competitive snapshot > strengths/gaps/sources > narrative loop > recommendations) is universal. The specific themes, risks, and recommendations must be derived from the actual data.

---

## Section Sequence

The report follows this mandatory section order (detailed specifications in `references/html-structure.md`):

1. **Header** — Brand name, prompt, date range, models, "Prepared by Meltwater"
2. **TL;DR bar** — Single-sentence headline finding
3. **KPI row** — 4 headline metric cards
4. **01: Executive Summary** — 4-6 key findings with evidence
5. **02: Competitive AI Snapshot** — 2x2 competitor cards (if competitive data exists)
6. **03: Strengths, Gaps & Sources** — Positive/negative themes (two-column) + source table + key gap callout
7. **04: The Narrative Loop** — Social > News > LLM flow with quotes and "Why it matters"
8. **05: Recommended Moves** — 4-6 numbered, prioritised recommendations
9. **Footer** — Brand name, date range, response count, models tested

Optional sections (add between 03 and 04 if data warrants):
- **Brand Detail Slide**: Detailed positive/negative aspect counts from screenshot data
- **Model Comparison**: Per-model behaviour differences when models diverge significantly

---

## Content Principles

1. **Every insight needs evidence**: Never make a claim without citing the specific data point (model name, response count, sentiment score, source domain, or quoted theme).

2. **Every recommendation needs a finding**: Recommendations must trace back to a specific gap identified in the analysis. Never include generic GEO advice not supported by the data.

3. **Headline-first writing**: Section titles should be insights, not topic labels. The subtitle should be the takeaway.

4. **Adapt the voice to the brand**: Retail gets direct, commercial tone. Government gets measured, policy-aware tone. Financial services gets trust-focused tone.

5. **Flag data gaps**: If the dataset only has 1 prompt, say so. If a model returned no results, note it. If sentiment is overwhelmingly neutral, explain what that means strategically.

6. **News source quality**: When referencing news articles, prioritise major Australian metro publications: AFR, The Australian, ABC News, The Age, SMH, Capital Brief, SBS, The Conversation, Crikey, The Guardian Australia. Filter out low-authority comparison sites unless they are significant LLM citation sources.

---

## Dependencies

```bash
pip install openpyxl pandas playwright --break-system-packages
playwright install chromium
```
