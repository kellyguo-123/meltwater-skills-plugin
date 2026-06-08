---
name: klear-influencer-report
description: Build a brand-true, client-ready HTML influencer marketing report comparing two creator cohorts using Klear MCP campaign data. Triggers when the user asks for things like "an influencer marketing report for [brand]", "compare our two creator cohorts for [brand]", "build a Klear report on [brand campaign]", "do a [brand] influencer report", "pull our [brand] campaigns into a report", "analysis of [brand]'s creator performance", "client-ready influencer report for [brand]". Compares two Klear campaigns side-by-side and produces a single self-contained HTML file with KPIs, network/format breakdown, audience demographics, and per-cohort deep dives with real Instagram embeds. The output is one HTML file — not a slide deck, PDF, or dashboard.
---

# Klear Influencer Marketing Report

A workflow that turns two Klear campaigns into a brand-true, client-ready HTML influencer marketing report.

## What this skill does and does not do

**Does**: gathers campaign data from Klear, aggregates it into a clean shape, and gives Claude everything needed to build a single brand-true HTML report file from scratch.

**Does not**: provide a template. There is no default visual style, no default fonts, no default colour palette, no default layout. Each report's visual identity must come from the brand's own design language, discovered fresh per report. **Two reports for two different brands should not look like cousins.**

## Hard rules (apply to every report)

1. **Real data only**. Every number, every quote, every post, every creator name comes from the named Klear campaigns. Nothing else. No invented stats. No synthetic creators. No filler quotes.
2. **Say "modelled", not "estimated"**. Reach and EMV from Klear are calculated, not measured. Label them *modelled* everywhere they appear. Direct platform numbers (likes, comments) are not modelled — don't apply the label there.
3. **All links must be real and tested**. Every Instagram embed URL must come from the data. Every external link must resolve. Broken or invented links are a failure.
4. **All quotes attributed**. If you quote a creator's caption, the post URL appears alongside it.
5. **No prior-report DNA**. Do not borrow the layout structure, typography, or visual treatment of any previous report Claude has built. Each report is designed for *this brand*, not derived from a template Claude has in its head.
6. **Hands off after design approval**. Once the user approves a design direction, execute it. Don't ask follow-up styling questions mid-build.

## Workflow

### Step 1 — Gather inputs from the user

Use `ask_user_input_v0` or direct conversation to confirm:
- **Brand name** (e.g. any consumer brand the user works with — sportswear, supplements, spirits, food, tech, fashion)
- **Two cohort names** (e.g. "Strength" and "Endurance" for a fitness brand; "Mixologists" and "Travel" for a spirits brand; "Pro" and "Amateur" for a sports brand). These are the two Klear campaigns to compare.
- **Optional report title**. If the user doesn't have one, suggest 2–3 in a later step based on the brand's voice.

### Step 2 — Resolve the campaigns in Klear

Call `klear:klear_list_account_campaigns` to get the full campaign list. Fuzzy-match the user's cohort names against `campaignName`. Show the user the matches:

> "I found *\<Brand\> \<Cohort A\>* (id 12345, N creators) and *\<Brand\> \<Cohort B\>* (id 12346, M creators). Are these the right two?"

If the user wants different campaigns, list candidates by name or accept campaign IDs directly.

### Step 3 — Research the brand identity

**This is the most important step for visual quality.** The skill provides no styling defaults. Each report's design must come from the brand's actual visual language.

Use `web_fetch` on the brand's primary website. If the site is heavily JS-rendered and `web_fetch` returns little, fall back to `image_search` for `"<brand> logo"`, `"<brand> packaging"`, `"<brand> advertising campaign"`.

Collect, at minimum:
- **Logo** — capture the SVG markup if available, or note the visual treatment (wordmark, monogram, symbol)
- **Primary palette** — the brand's main colour(s). What dominates their marketing?
- **Secondary palette** — supporting colours, neutrals, accent foils
- **Typography character** — heritage serif? Geometric sans? Display-driven? Hand-written?
- **Visual treatment** — what does their marketing *look* like? Photo-led? Type-led? Illustration-led? Maximalist? Minimal?
- **Aesthetic family** — pick one and commit. Examples (non-exhaustive): heritage spirits magazine, athletic sportswear, technical/laboratory, club/nightlife, hospitality/luxury, food/kitchen, outdoor adventure, fashion editorial, scientific/clinical, retro/vintage, brutalist, organic/natural, futuristic/tech, artisan/craft, festival/colour-block. **Do not pick "modern minimal" as a default — that is a non-answer.**
- **Tone of voice** — premium? Playful? Authoritative? Casual?

Synthesise this into a one- or two-sentence design direction. The format:

> *"I'll design this as a \<aesthetic family\> — \<primary colour\> against \<secondary palette\>, \<display font\> with \<typographic treatment\>, \<layout philosophy\>. Not \<contrasting aesthetic\>, not \<contrasting layout\>."*

The design direction should describe the **aesthetic family**, the **palette in role** (which colour does what), the **typography character**, and the **layout philosophy**.

### Step 4 — User confirmation (DO NOT SKIP)

Show the user:
1. The two campaigns resolved (name + ID + creator count).
2. The design direction (one or two sentences as above).
3. Two or three suggested report titles in the brand's voice.

Use the `Visualizer` to render a small swatch panel of palette + sample type if available, otherwise describe in prose. Ask explicitly: **"Do these campaigns and this design direction look right? Reply 'yes' to proceed, or tell me what to change."**

Common adjustments:
- Wrong colour → user names a specific hex.
- Different aesthetic family → user redirects (e.g. "actually go more nightclub than heritage").
- Title doesn't work → user picks one of the suggestions or proposes their own.

Iterate until the user approves.

### Step 5 — Fetch the Klear data

For each cohort, call the following Klear tools. See `references/klear-mcp-cheatsheet.md` for known quirks.

- `klear:klear_get_campaign_kpis` — authoritative lifetime KPIs
- `klear:klear_list_campaign_members` — full creator list with follower counts (`_select` to keep it small)
- `klear:klear_get_campaign_measure` — every post in the campaign. May return >1MB; if it does, the response is auto-stashed to a file path. Both paths work for the aggregator.
- `klear:klear_get_profile_demographics` — for the top 3–5 highest-reach creators per cohort. This endpoint is known to time out for long periods. If it fails repeatedly, **stop retrying after two attempts** and let the demographics section render an explicit *"unavailable"* state. Don't burn the user's time on a known-broken endpoint.

Save each response under `/tmp/klear-raw/` with predictable filenames the aggregator expects:
```
cohort-a-kpis.json
cohort-a-members.json
cohort-a-measure.json
cohort-a-demos-<handle>.json   (one per sampled handle, can be empty `{}` if unavailable)
cohort-b-kpis.json
cohort-b-members.json
cohort-b-measure.json
cohort-b-demos-<handle>.json
```

### Step 6 — Aggregate

Run `scripts/aggregate_klear.py` from inside the skill directory:

```bash
python3 scripts/aggregate_klear.py --brand "<brand name>" --keywords <kw1> <kw2> ...
```

The `--brand` flag is used to extract audience brand-affinity from the demographics data. The `--keywords` flag is only used in the fallback path when `campaignMeasure` exceeds the 1MB limit; pass keywords relevant to the brand (e.g. for a spirits brand: the brand name + any signature product names).

This produces `/home/claude/report-data.json` — a clean, brand-agnostic data shape with:
- Period (start/end dates)
- Per-cohort: creator count, mentioning users, total mentions, modelled reach, engagements, impressions, engagement rate, modelled EMV
- Per-cohort network breakdown (Instagram/Stories/Twitter/Facebook/YouTube/TikTok counts)
- Per-cohort content type breakdown (image/video/text counts)
- Top posts by engagement (creator-diversified — no creator appears twice in the same list)
- Top posts by modelled reach (also creator-diversified)
- Aggregated demographics (or `None` values if the endpoint was down)

See `references/section-spec.md` for the full data shape and which fields drive which section.

### Step 7 — Build the HTML from scratch

**This is the critical step.** There is no template. You build the report's HTML directly, using:
- The aggregated data (`report-data.json`)
- The brand design direction agreed in Step 4
- The required sections list (`references/section-spec.md`)

**Do not borrow layout structure from previous reports.** Do not default to a centred-hero-then-KPI-strip-then-comparison-cards structure unless that is genuinely right for *this brand*. Heritage brands might want asymmetric editorial spreads with drop caps and pull quotes. Tech brands might want grid-heavy data visualisations. Outdoor brands might want full-bleed photographic backgrounds. Each report's structure should serve the brand.

The required sections (any order, any visual treatment that fits the brand):
1. **Opening / hero** — title, period, source attribution, headline framing
2. **Headline KPIs** — combined totals: mentions, modelled reach, engagements, modelled EMV
3. **Two-cohort comparison** — side-by-side per-cohort stats
4. **Network distribution** — where each cohort posts (Instagram, Stories, Twitter, etc.)
5. **Content format breakdown** — image / video / text per cohort
6. **Audience demographics** — or graceful "unavailable" state if the data is missing
7. **Cohort A deep dive** — short cohort narrative + top 3 posts by engagement + top 3 by modelled reach (Instagram embeds where the post is on Instagram)
8. **Cohort B deep dive** — same shape, different visual treatment if it suits the brand
9. **Methodology / colophon** — source attribution, "modelled" definition, time window, demographics caveat
10. **Footer** — title echo, volume/date, trademark disclaimer

For Instagram embeds, the URL pattern is `https://www.instagram.com/p/<SHORTCODE>/embed/`. Extract the shortcode from the post link returned by `campaignMeasure`. If a top creator's strongest post is on TikTok or YouTube, render a clean "non-IG placeholder" card rather than a broken embed.

See `references/section-spec.md` for what each section must contain. Visual treatment is up to you.

### Step 8 — Save and present

Save the HTML to `/mnt/user-data/outputs/<slugified-title>.html`. Validate:
- No unfilled placeholders (search for `{{` or `[BRAND]` etc.)
- Every Instagram embed URL is a real shortcode from the data
- Every external link resolves
- Every quoted creator has a name and handle alongside

Use `present_files` to surface the output. Briefly summarise the headline finding in chat (one or two sentences), but the report itself does the talking.

## References

- `references/klear-mcp-cheatsheet.md` — Klear MCP tool quirks (response wrapping, timeouts, the 1MB limit)
- `references/section-spec.md` — what each section must contain and which data fields drive it
- `references/brand-research.md` — how to extract a brand's visual identity from the web
- `references/design-guidance.md` — neutral guidance on translating brand identity into design choices

## Scripts

- `scripts/aggregate_klear.py` — turns the per-tool Klear responses into a single clean `report-data.json`. Brand-agnostic. Do not edit per-brand.
