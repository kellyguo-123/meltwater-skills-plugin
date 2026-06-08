# Meltwater Skills Plugin

Meltwater MCP skills for media intelligence reporting. Install this plugin to get Meltwater-branded report generation directly in Claude Cowork.

## Skills included

| Skill | What it does |
|-------|-------------|
| **Brand Pulse** | Full brand health report — sentiment, top posts, risks, competitive landscape, recommendations — as a branded HTML infographic + PDF |
| **Issues & Crisis Report** | 11-section crisis brief — timeline, volume trends, key narratives, risk assessment, strategic recommendations — as a branded HTML infographic + PDF |
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

## Version history

| Version | Changes |
|---------|---------|
| 0.1.0 | Initial release — Brand Pulse + Issues & Crisis + brand assets |

## Adding more skills

Drop a new subdirectory with a `SKILL.md` into `skills/` and bump the version in `.claude-plugin/plugin.json`.
