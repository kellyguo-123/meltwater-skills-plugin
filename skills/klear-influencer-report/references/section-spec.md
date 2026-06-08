# Section spec

The report has ten required sections. Their order, layout, and visual treatment are flexible — adapt them to the brand. Their **data content** is fixed: every section listed below must appear, with the data shown.

The aggregated data file `report-data.json` is the source. Here is the shape — refer to it when wiring sections.

```jsonc
{
  "brand_name": "...",
  "report_title": "...",
  "period": {
    "start": "YYYY-MM-DD",
    "end": "YYYY-MM-DD"
  },
  "combined": {
    "total_mentions": int,
    "total_reach": float,
    "total_engagements": int,
    "total_emv": float,
    "creators": int
  },
  "cohort_a": {
    "name": "...",
    "descriptor": "...",          // e.g. "bartenders and cocktail creators"
    "campaign_id": int,
    "creators_count": int,
    "mentioning_users": int,
    "total_mentions": int,
    "total_reach": float,
    "total_engagements": int,
    "total_impressions": int,
    "engagement_rate": float,     // already in percent (0.74 = 0.74%)
    "emv": float,
    "networks": {                 // network → mentions count
      "insta": int, "insta_stories": int, "twitter": int,
      "facebook": int, "youtube": int, "tiktok": int
    },
    "content_types": {            // type → count
      "image": int, "video": int, "text": int
    },
    "top_posts_by_engagement": [  // creator-diversified, max 3
      {
        "author_name": "...", "author_handle": "...",
        "author_ig_followers": int,
        "link": "https://www.instagram.com/p/...",
        "ig_shortcode": "...",    // null for non-IG posts
        "network": "instagram|tiktok|youtube|twitter|facebook",
        "content_type": "image|video|text|story",
        "caption": "...",         // truncated to ~160 chars
        "engagements": int, "likes": int, "comments": int,
        "created_at": "YYYY-MM-DD"
      }
    ],
    "top_posts_by_reach": [...],  // same shape, creator-diversified
    "demographics": {             // or null if endpoint was down
      "avg_age": float | null,
      "male_pct": float | null,
      "female_pct": float | null,
      "age_18_24": float | null,
      "age_25_34": float | null,
      "age_35_49": float | null,
      "us_pct": float | null,
      "top_countries": [{"country": "...", "pct": float}, ...]
    }
  },
  "cohort_b": { /* same shape */ }
}
```

## The ten sections

### 1. Opening / hero

**Must show**: report title, period (`period.start` → `period.end`), brand name, source attribution ("Klear MCP, 2 campaigns"), framing context — what the reader is about to see.

**Notes**: do not default to a giant centred headline. Many brands suit asymmetric, sidebar, or magazine-masthead approaches. The opening should *feel* like the brand's own.

### 2. Headline KPIs

**Must show**: `combined.total_mentions`, `combined.total_reach` (label as *modelled*), `combined.total_engagements`, `combined.total_emv` (label as *modelled*).

**Notes**: format reach and EMV with their currency/magnitude markers (1.7M, $4.9M). The grid-of-four KPI strip is one option; an inline "by the numbers" sidebar is another; a single hero number with three supporting figures is a third. Pick what serves the brand.

### 3. Two-cohort comparison

**Must show**, per cohort: name, descriptor, creators_count, mentioning_users, total_mentions, total_reach (modelled), total_engagements, engagement_rate, emv (modelled).

**Notes**: side-by-side "tasting cards" is one option. Running prose with stats embedded inline is another. Two-column editorial spread is another. Stat tables in alternating brand colours is another.

### 4. Network distribution

**Must show**: per cohort, mention counts across `insta`, `insta_stories`, `twitter`, `facebook`, `youtube`, `tiktok`. A short narrative interpretation is welcome (e.g. "Instagram dominates both; Stories matter only for cohort B").

**Notes**: bar chart is the obvious choice but not the only one. A radial chart, a dot plot, or even a simple table can work. Match the brand's visual sophistication.

### 5. Content format breakdown

**Must show**: per cohort, counts across `image`, `video`, `text`.

**Notes**: don't over-engineer this. Six numbers and a short narrative is usually enough.

### 6. Audience demographics

**If `demographics` data exists for both cohorts**: show age distribution, gender split, top countries.

**If demographics is `null` or empty**: render an explicit, brand-styled *"data temporarily unavailable"* panel. Explain that Klear's `profileDemographics` endpoint was unresponsive during the build. Don't leave empty cells. Don't fake or estimate. Be honest.

### 7. Cohort A deep dive

**Must show**: a short narrative paragraph about the cohort (its character, what it sells, the headline number), `cohort_a.creators_count`, `cohort_a.mentioning_users`, `cohort_a.total_mentions`, `cohort_a.emv`, then **top 3 posts by engagement** and **top 3 posts by modelled reach**, each with author name, handle, Instagram embed (or non-IG placeholder), caption, headline stats.

**Notes**: the "creator portrait gallery" approach is one option; a "post showcase" with magazine-style stat callouts is another; a feature article with embedded post cards is another. The deep dive should feel like an editorial profile of the cohort, not a roster page.

### 8. Cohort B deep dive

**Must show**: same shape as Cohort A.

**Notes**: visually distinguish from Cohort A — different background tone, different layout rhythm, or different framing. The two cohorts should feel like two separate features, not duplicates of one another.

### 9. Methodology / colophon

**Must show**:
- Source: "All content metrics from Klear MCP, drawn from [campaign A name + id] and [campaign B name + id]."
- Sample disclaimer: "These are curated samples maintained inside Klear, not the totality of either community."
- Time window: `period.start` → `period.end`.
- "Modelled" definition: Klear calculates reach and EMV from audience size, network norms, and post type — they are not direct platform measurements.
- Demographics caveat if applicable: "Klear's `profileDemographics` endpoint was unresponsive during the build window for this issue."
- Embed disclaimer: "Top posts use Instagram's official embed URLs. If a post is later deleted or set private, the card may go blank."

**Notes**: this section can be small-type and corner-tucked, or a full magazine-style "colophon" page. It is required, but its emphasis can be low.

### 10. Footer

**Must show**: report title, volume/issue/date, trademark disclaimer ("[Brand] is a registered trademark of its respective owner. This report is not affiliated with, endorsed by, or sponsored by [Brand].").

**Notes**: an echo of the opening masthead works well — it gives the report a finished, bookended feel.

## Field formatting conventions

- **Numbers ≥1,000,000**: format as `1.7M`, `23.8M`. Use one decimal place unless the value rounds cleanly to an integer.
- **Numbers 10,000 – 999,999**: format as `131,897` or `367K` depending on context. Use the comma version in tables/stats; use the K version in tight cards.
- **Numbers <10,000**: use the full integer with commas.
- **Engagement rate**: `0.74%` (already in percent in the data, just append `%`).
- **EMV**: `$4.9M`, `$472K`. Always prefix `$` (or the brand's currency if applicable).
- **The word "modelled"** appears wherever reach or EMV is shown. Direct platform numbers (likes, comments, follower counts) are not modelled.
