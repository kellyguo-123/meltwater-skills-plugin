---
name: genai-lens-framework
description: "Builds a client-branded GenAI Lens Prompt Framework HTML for any company. Pre-sale deliverable showing proposed account structure: categories, example prompts, funnel stages, prompt type mix, competitors, package alignment. Trigger on 'GenAI Lens framework', 'prompt framework', 'GAIL framework', 'prompt plan', 'set up GenAI Lens for [client]', 'build the framework for [company]', or any request to structure prompts for a GenAI Lens prospect. NOT for analysing existing data (use genai-lens-report). This produces the framework BEFORE data collection. Always trigger even for partial requests like 'what prompts should we track for [brand]'."
---

# GenAI Lens Prompt Framework Skill

Generates a client-branded HTML document presenting the proposed GenAI Lens prompt architecture for a prospect. Output is a single interactive HTML file with collapsible division cards, styled in the client's brand colours with Meltwater as "prepared by" branding.

## Inputs

- **Company name** (required)
- **Divisions/categories** (optional — researched if not provided)
- **Competitor set** (optional — 3-4 researched if not provided)
- **Total prompt count** (optional — defaults to 500)
- **Package tier** (optional — Lite 250 / Pro 500 / Enterprise 1000 / Enterprise+ 1200, defaults to Pro)

## Workflow

### Step 0: Confirm and Research

1. Confirm the company name. Ask if ambiguous.
2. Web search the company: divisions, products, competitors, geography, recent news.
3. Detect brand colours: check `genai-lens-report/references/brand-theming.md` Australian Brand Database first. If not found, web search for brand hex colours.
4. Propose structure to user and wait for confirmation:
   - Categories (4-7) with descriptions
   - Competitors (3-4)
   - Package tier and prompt count
   - Prompt distribution across categories
   - Brand colours: Primary, Secondary, Accent

### Step 1: Generate Prompts

Generate **10 prompts per category**. Each prompt has: `text`, `funnel`, `type`, `activity`.

**Funnel stages** (default — adapt if warranted):
- `awareness` (#3B82F6) — Brand discovery, category exploration
- `research` (#8B5CF6) — Deep evaluation, features
- `comparison` (#F59E0B) — Head-to-head "X vs Y"
- `intent` (#22C55E) — Ready to buy/act

**Prompt types** with target mix:
- `brand` (~30%) — Direct brand mention
- `category` (~30%) — Industry/category query, brand should appear in answer
- `competitive` (~25%) — Head-to-head comparison
- `journey` (~15%) — Unbranded decision-stage

**Quality rules:** Write as natural human questions for LLMs. Include brand name in ~40-50% of prompts. Use competitor names in comparison prompts. Make prompts specific to the company's actual products and markets. Aim for ~20% awareness, 30% research, 30% comparison, 20% intent across the full set.

### Step 2: Build the HTML

Single self-contained HTML file. Fonts: DM Sans + Space Mono via Google Fonts. All CSS in `<style>`, all data/JS in `<script>`.

**Section order:**
1. **Header** — Meltwater logo SVG + divider + client name + "GenAI Lens Framework"
2. **Hero** — Dark gradient. Label: "Prompt Architecture / Account Structure". H1: "GenAI Lens Prompt Framework" (brand-coloured span). Client-specific subtitle.
3. **Stats bar** — 4 cells: Total Prompts, Categories, Competitors Tracked, LLM Models (always 7)
4. **Package bar** — Tier name + specs left, stacked distribution bar + legend right. Segments coloured per category.
5. **Funnel legend** — Colour-coded stage dots and labels
6. **Division cards** — Collapsible. Header: emoji icon + name + description + type mix micro-bar + prompt count badge + chevron. Expanded: prompt table (4 cols: Prompt, Funnel Stage, Prompt Type, Activity) + "Showing X of Y" progress bar.
7. **Competitor strip** — Client as primary tag (brand colour), competitors as grey tags
8. **Total strip** — Dark bar. Big number + "Total prompts across all categories" + "Customised to [Client]..."
9. **Footer** — "Confidential. Prepared for [Client] by Meltwater Solutions Consulting." + Meltwater eyecon + year

**JS behaviour:** Division data as JS array, injected on load. Accordion toggle (one open at a time). Prompt rows animate in with staggered delay.

### Step 3: Apply Brand Colours

Use client brand colours for all accents. CSS variables:
- `--brand-primary`, `--brand-primary-dark`, `--brand-primary-light` (5-8% tint), `--brand-primary-border` (15-20% tint), `--brand-secondary`
- Meltwater structural greys are fixed (`--mw-dark`, `--mw-navy`, `--mw-grey-*`)
- Funnel/type colours are fixed (blue, purple, amber, green)

Brand colour applies to: stat numbers, prompt count badges, open card border, chevron active, quote marks, progress bar, total number, primary competitor tag.

**Yellow/gold brands:** Use black text on coloured backgrounds. **Very dark brands:** Use secondary colour for stat numbers and accents.

### Step 4: Output

Save to `/mnt/user-data/outputs/[client_slug]_genai_lens_framework.html`. Use `present_files`.

## Category Guidelines

- **Multi-division company:** Map to actual business segments
- **Single-product / SaaS:** Map to use case themes or buyer personas
- **Retail / consumer:** Product categories, customer segments, brand perception themes
- **Financial services:** Product lines + reputation themes
- **Government:** Service areas + policy domains
- Always include a Corporate/Reputation/ESG cross-cutting category
- Use the company's own language for category names
- Distribute prompts unevenly by commercial importance

## Competitor Selection

- 3-4 direct competitors in same market
- Prefer competitors the prospect would recognise
- Include one aspirational/premium if relevant
- For AU companies, prefer AU competitors unless global

## Package Specs

| Tier | Prompts | Models | Frequency |
|------|---------|--------|-----------|
| Lite | 250 | 5 | 48 hours |
| Pro | 500 | 7 | 48 hours |
| Enterprise | 1,000 | 8 | Daily |
| Enterprise+ | 1,200 | 9 | Daily |

## Division Icon Colours

Assign in order per category:
```
indigo:  bg #EEF2FF, fg #4F46E5
orange:  bg #FFF7ED, fg #EA580C
pink:    bg #FDF2F8, fg #DB2777
emerald: bg #ECFDF5, fg #059669
blue:    bg #EFF6FF, fg #2563EB
violet:  bg #F5F3FF, fg #7C3AED
yellow:  bg #FEF9C3, fg #CA8A04
```

## Meltwater Logo SVG

Use in header and footer:
```html
<svg viewBox="0 0 160 28" fill="none" xmlns="http://www.w3.org/2000/svg">
  <path d="M14 0C6.268 0 0 6.268 0 14s6.268 14 14 14 14-6.268 14-14S21.732 0 14 0z" fill="#00B2A9"/>
  <path d="M7 10.5l3.5 7L14 10.5l3.5 7 3.5-7" stroke="#fff" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round" fill="none"/>
  <text x="36" y="20" fill="#fff" font-family="DM Sans, sans-serif" font-size="18" font-weight="700">Meltwater</text>
</svg>
```

## Do NOT Include

- Product screenshots, pricing, roadmap, release timelines
- Links to Meltwater help centre or docs
- SC-facing notes or internal talking points
- References to AI/Claude generation
