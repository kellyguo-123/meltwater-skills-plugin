# Klear MCP cheatsheet

Behaviour notes for each Klear tool, captured from real usage building reports against this MCP. Read before fetching campaign data so you don't get surprised.

## `klear:accountCampaigns`

- Takes no arguments. Returns every campaign on the account.
- The `numberOfInfluencersInCampaign` is the right number to read — note that the API also calls this `total_users` elsewhere, and the two should match.
- `campaignMode` is `ACTIVE` or `ARCHIVE`. Prefer `ACTIVE` when fuzzy-matching, unless the user has explicitly named an archived one.
- `campaignEndDate` is null for ongoing campaigns. Don't rely on it.

When fuzzy-matching by brand + cohort, the convention in this account is `<Brand> <Cohort>` and `<Brand> <Cohort> 2` — usually the `2`-suffixed campaign is the newer, refreshed version. Prefer the higher-numbered ACTIVE campaign unless the user says otherwise.

## `klear:campaignKpis`

- **Authoritative** for headline metrics. Don't recompute these from `campaignMeasure` rollups — the totals won't match because `campaignKpis` includes deduplication and weighting that `campaignMeasure` doesn't expose.
- Returns: `total_users`, `mentioning_users`, `total_mentions`, `impressions`, `reach`, `engagements`, `engagement_rate`, `ROI` (this is EMV in USD), `post_averages`, `currency`, plus per-network and per-content-type rollups.
- `ROI` here means "Earned Media Value" — Klear's modelled $ figure based on `$0.43` CPE and `$7.29` CPM defaults. Label it as **modelled EMV** in the report.
- Per-network keys: `twitter`, `insta`, `facebook`, `youtube`, `insta_stories`, `facebook_stories`, `tiktok`, `pinterest`, `blog`, `twitch`.
- Content media types: `image`, `video`, `text` (sometimes also `reel`, `album`).

## `klear:campaignMembers`

- Returns the creator list with handles, follower counts per platform, totalReach, and Klear Influence Score.
- Use this to identify the top N members to drill into for `profileContent` (fallback path) and `profileDemographics`.
- The data is well-bounded — typically < 100KB even for 100-creator campaigns — so this is always safe to call.

## `klear:campaignMeasure`

- Returns post-level data with engagement metrics. This is the workhorse for top-post rankings.
- **Critical wrapping**: the result is `[{type: "text", text: "<JSON string>"}]`. Unwrap with `json.loads(result[0]['text'])`. Inside that, you'll find `{users: [{... postsInCampaign: [...]}]}`.
- **1MB limit**: for campaigns with thousands of posts (e.g. anything > ~1500 posts in total), the response exceeds the 1MB tool limit and returns a sentinel error. Don't retry — switch to the fallback path:
  1. From `campaignMembers`, sort by `totalReach` and take the top 10.
  2. For each top member, call `klear:profileContent(handle, network='instagram', limit=50)`.
  3. Filter for brand-relevant keywords on `contentText`.
  4. Filter to the time window.
  5. Combine into a single flat list and treat it as if it came from `campaignMeasure`.
- **postReach is mostly null** for Instagram posts (the platform doesn't expose it for non-business accounts). Model it from author followers × content-type factor (see `aggregate_klear.py`).

## `klear:profileContent`

- Returns recent posts for a single creator on a single network. Most reliable for Instagram.
- The brand-keyword filter has to be applied client-side — this tool returns all the creator's posts, not just those mentioning the brand.
- `postReach`, `impressions`, `shares`, `reactions`, `replies` are typically null for Instagram personal accounts.

## `klear:profileDemographics`

- Returns modelled audience demographics: ages, genders, countries, states, cities, top brands, hashtags, skills.
- **Has been known to time out repeatedly.** When it times out, skip the creator and continue with what's left. The report's demographics section needs at least 2 valid responses per cohort to be meaningful.
- The `brands` field shows which brands the audience over-indexes on. The campaign's own brand will typically appear here with a percentage like `9.1` — that means "9.1% of this audience's brand affinity is for that brand".

## `klear:campaignContentInstagramPostsComments`

- Returns `{"postsWithComments": []}` for most campaigns we've used. Don't rely on it for content discovery.

## `klear:campaignDeliverables`, `klear:campaignPayments`, `klear:campaignSales`, `klear:campaignGifting`

- All exist; none are needed for this report skill. Useful for finance/ops reporting, not influencer marketing reports.

## Discovery tools (not used by this skill but worth knowing)

- `klear:discoveryByTopic`, `klear:discoveryByKeyword`, `klear:discoveryByText`, `klear:discoveryByVisualPrompt` — for finding new creators outside an existing campaign. Useful for the "who else should we onboard?" question, not for reporting on an existing roster.
