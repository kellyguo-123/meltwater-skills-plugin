# Meltwater Skills Plugin

Meltwater MCP skills for media intelligence reporting. Install this plugin to get Meltwater-branded report generation directly in Claude Cowork.

> **Requirement:** The Meltwater MCP must be connected in Cowork (Settings → Connections) for data retrieval to work.

## Skills included

| Skill | What it does |
|-------|-------------|
| **Brand Pulse** | Full brand health report — sentiment, top posts, risks, competitive landscape, recommendations — as a branded HTML infographic + PDF |
| **Issues & Crisis Report** | 11-section crisis brief — timeline, daily volume chart, key narratives, risk assessment, strategic recommendations — as a branded HTML infographic + PDF |
| **Campaign Impact Report** | Campaign performance reporting using Meltwater data |
| **GenAI Lens Report** | GenAI media coverage analysis — how AI topics and brands are covered across news and social |
| **GenAI Lens Framework** | Framework for applying a GenAI lens to any media intelligence analysis |
| **Klear Influencer Report** | Influencer analysis via Klear MCP — reach, engagement, brand fit, and audience breakdown |
| **Meltwater Reddit Intelligence** | Reddit-specific media intelligence — community sentiment, thread analysis, emerging narratives |
| **Meltwater Trending & Viral** | Trending and viral content tracking across news and social channels |
| **Meltwater Brand** | Brand guidelines for all Meltwater-branded outputs — colors, typography, logo assets, layout rules |

## How to trigger

**Brand Pulse:**
> "Give me a brand pulse report on [brand]"
> "Pull from Meltwater and analyze [brand]"
> "What's the media landscape for [brand]?"

**Issues & Crisis:**
> "Build a crisis report on [brand] around [topic]"
> "What's the controversy situation for [brand]?"
> "Pull from Meltwater and build an issues brief on [brand]"

**Campaign Impact:**
> "Build a campaign impact report for [campaign]"
> "How did [campaign] perform across media?"

**GenAI Lens:**
> "Give me a GenAI lens report on [brand or topic]"
> "How is [brand] being covered in the context of AI?"

**Klear Influencer:**
> "Pull a Klear influencer report for [brand]"
> "Who are the top influencers for [brand or topic]?"

**Reddit Intelligence:**
> "What's Reddit saying about [brand]?"
> "Pull Meltwater Reddit intelligence on [brand]"

**Trending & Viral:**
> "What's trending for [brand or topic]?"
> "Show me viral content for [brand] this week"

## Version history

| Version | Changes |
|---------|---------|
| 0.2.0 | Added Campaign Impact, GenAI Lens, GenAI Lens Framework, Klear Influencer, Reddit Intelligence, Trending & Viral |
| 0.1.0 | Initial release — Brand Pulse + Issues & Crisis + Meltwater brand assets |

## Adding more skills

Drop a new subdirectory with a `SKILL.md` into `skills/` and bump the version in `.claude-plugin/plugin.json`.
