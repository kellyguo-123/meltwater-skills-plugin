#!/usr/bin/env python3
"""
Aggregate raw Klear campaign data into a single report-data.json that the
template renderer consumes.

Input:
  /home/claude/klear-raw/
    cohort-a-kpis.json           # full klear:campaignKpis response
    cohort-a-members.json        # full klear:campaignMembers response
    cohort-a-measure.json        # raw klear:campaignMeasure response (wrapped in {type:text,...}[])
                                 # OR cohort-a-posts.json — a flat list of posts from the profileContent
                                 # fallback path. Either one works; this script handles both.
    cohort-a-demos-<handle>.json # one file per profileDemographics call (any number)
    cohort-b-...                 # same set for cohort B

Output:
  /home/claude/report-data.json

Usage:
  python aggregate_klear.py [--raw-dir /home/claude/klear-raw] [--out /home/claude/report-data.json] [--period-days 365]

The renderer expects fields documented in references/template-tokens.md.
"""

import argparse
import datetime
import json
import os
import re
import sys
from collections import Counter
from pathlib import Path

# Keywords used to identify brand-relevant posts when filtering profileContent output
# (only used in the fallback path when campaignMeasure exceeds the 1MB limit).
# Pass per-run via --keywords. No defaults — must be supplied at runtime.

# Reach-modelling factors when postReach is null. These mirror what Klear itself uses.
REACH_FACTOR = {
    "image": 0.10,    # ~10% of follower count
    "video": 0.15,
    "reel": 0.15,
    "album": 0.10,
    "text": 0.04,
    "link": 0.04,
}


def fmt_num(n):
    """Format a number in human-readable form: 1.2K, 3.4M, 5.6B"""
    if n is None:
        return "—"
    try:
        n = float(n)
    except (TypeError, ValueError):
        return str(n)
    if n >= 1e9:
        return f"{n/1e9:.1f}B"
    if n >= 1e6:
        return f"{n/1e6:.1f}M"
    if n >= 1e3:
        return f"{n/1e3:.1f}K"
    if n >= 100:
        return f"{n:.0f}"
    return f"{n:.1f}".rstrip("0").rstrip(".")


def fmt_pct(p, decimals=2):
    """Format a percentage. Handles ratios already in %."""
    if p is None:
        return "—"
    return f"{p:.{decimals}f}%"


def fmt_money(n):
    if n is None:
        return "—"
    if n >= 1e6:
        return f"${n/1e6:.1f}M"
    if n >= 1e3:
        return f"${n/1e3:.1f}K"
    return f"${n:.0f}"


def unwrap_measure(raw):
    """
    klear:campaignMeasure wraps the data in [{type: "text", text: "<JSON string>"}].
    Parse and return the inner data, or return raw if already flat.
    """
    if isinstance(raw, list) and raw and isinstance(raw[0], dict) and "text" in raw[0]:
        return json.loads(raw[0]["text"])
    return raw


def load_json(path):
    if not os.path.exists(path):
        return None
    with open(path) as f:
        return json.load(f)


def normalize_posts(raw_measure):
    """Take a parsed campaignMeasure payload and return a flat list of posts with author metadata."""
    if not raw_measure:
        return []
    users = raw_measure.get("users", [])
    out = []
    for u in users:
        handles = u.get("socialMediaHandles", {}) or {}
        followers = u.get("numberOfFollowers", {}) or {}
        for p in u.get("postsInCampaign", []) or []:
            out.append({
                **p,
                "author_name": u.get("name", ""),
                "author_handle": handles.get("instagram", ""),
                "author_ig_followers": followers.get("instagram", 0) or 0,
                "author_klear_score": u.get("klearInfluenceScore", 0),
            })
    return out


def model_reach(post):
    """If postReach is null, model it from author followers × content-type factor."""
    if post.get("postReach"):
        return post["postReach"]
    ctype = (post.get("contentType") or "image").lower()
    factor = REACH_FACTOR.get(ctype, 0.10)
    return (post.get("author_ig_followers", 0) or 0) * factor


def extract_shortcode(link):
    """Pull an Instagram shortcode from a URL. Return None if not Instagram."""
    if not link:
        return None
    m = re.search(r"instagram\.com/(?:p|reel|reels|tv)/([A-Za-z0-9_-]+)", link)
    return m.group(1) if m else None


def filter_brand_relevant(posts, keywords):
    """Filter posts whose contentText mentions any brand-relevant keyword."""
    lo_kw = [k.lower() for k in keywords]
    def relevant(p):
        t = (p.get("contentText") or "").lower()
        return any(k in t for k in lo_kw)
    return [p for p in posts if relevant(p)]


def filter_recent(posts, cutoff_ts):
    return [p for p in posts if (p.get("createdAt") or 0) >= cutoff_ts]


def aggregate_demographics(demo_files, brand_name=None):
    """Take a list of (handle, demo_json, follower_count) and produce weighted averages.
    If brand_name is supplied, also extract the audience's affinity for that brand from
    the demographics 'brands' field."""
    fields = ["avg_age", "male_pct", "us_pct", "age_18_24", "age_25_34", "age_35_49",
              "brand_affinity_pct"]
    sums = {k: 0.0 for k in fields}
    weights = {k: 0.0 for k in fields}
    handles_used = []

    brand_match = (brand_name or "").strip().lower() or None

    for handle, demo, followers in demo_files:
        if not demo:
            continue
        d = demo.get("demographics", {})
        per = {}

        # average ages
        avgs = d.get("averageAges") or []
        if avgs and avgs[0].get("values"):
            per["avg_age"] = avgs[0]["values"][0].get("value")

        # gender
        for g in d.get("genders") or []:
            if g.get("label", "").lower() in ("men", "male"):
                v = g.get("values", [{}])[0].get("value")
                if v is not None:
                    per["male_pct"] = v

        # countries
        for c in d.get("countries") or []:
            if c.get("label") == "United States":
                v = c.get("values", [{}])[0].get("value")
                if v is not None:
                    per["us_pct"] = v
                break

        # ages
        for a in d.get("ages") or []:
            label = a.get("label", "")
            v = a.get("values", [{}])[0].get("value")
            if v is None:
                continue
            if label in ("18 - 24", "18-24"):
                per["age_18_24"] = v
            elif label in ("25 - 34", "25-34"):
                per["age_25_34"] = v
            elif label in ("35 - 49", "35-49"):
                per["age_35_49"] = v

        # brand affinity — only if the caller named a brand to look up
        if brand_match:
            brands = d.get("brands") or []
            for b in brands:
                if b.get("label", "").lower() == brand_match:
                    v = b.get("values", [{}])[0].get("value")
                    if v is not None:
                        per["brand_affinity_pct"] = v
                    break

        # accumulate weighted
        handles_used.append(handle)
        for k, v in per.items():
            if v is not None:
                sums[k] += v * followers
                weights[k] += followers

    out = {}
    for k in fields:
        out[k] = (sums[k] / weights[k]) if weights[k] > 0 else None
    out["sample_creators"] = handles_used
    return out


def load_cohort(raw_dir, cohort_key, keywords, cutoff_ts, brand_name=None):
    """Load all files for a cohort and produce its slice of the report data."""
    base = Path(raw_dir)

    kpis = load_json(base / f"{cohort_key}-kpis.json") or {}
    kpi = kpis.get("campaignKpi") or kpis  # accept either wrapped or unwrapped
    members = load_json(base / f"{cohort_key}-members.json") or {}

    # posts: try measure first, fall back to posts.json (profileContent flat list)
    measure_raw = load_json(base / f"{cohort_key}-measure.json")
    if measure_raw is not None:
        measure = unwrap_measure(measure_raw)
        posts_all = normalize_posts(measure)
    else:
        posts_all = load_json(base / f"{cohort_key}-posts.json") or []
        # In fallback mode, filter for brand relevance — campaignMeasure already filters by keyword
        posts_all = filter_brand_relevant(posts_all, keywords)

    posts_recent = filter_recent(posts_all, cutoff_ts)

    # rank by engagement
    by_eng = sorted(
        [p for p in posts_recent if (p.get("postEngagements") or 0) > 0],
        key=lambda p: p.get("postEngagements") or 0,
        reverse=True,
    )
    # rank by modelled reach
    by_reach = sorted(
        posts_recent,
        key=lambda p: model_reach(p),
        reverse=True,
    )

    # demographics
    demo_files = []
    members_list = members.get("users", []) if isinstance(members, dict) else members
    for fpath in base.glob(f"{cohort_key}-demos-*.json"):
        handle = fpath.stem.replace(f"{cohort_key}-demos-", "")
        demo = load_json(fpath)
        # find this creator's follower count
        followers = 0
        for u in members_list:
            if (u.get("socialMediaHandles", {}) or {}).get("instagram") == handle:
                followers = (u.get("numberOfFollowers", {}) or {}).get("instagram", 0) or 0
                break
        demo_files.append((handle, demo, followers))

    demos = aggregate_demographics(demo_files, brand_name=brand_name)

    # network breakdown from kpi.networks
    networks_raw = kpi.get("networks", {})
    networks = {}
    for k, v in networks_raw.items():
        networks[k] = {
            "mentions": v.get("mentions", 0),
            "reach": v.get("reach", 0),
            "engagements": v.get("engagements", 0),
            "engagement_rate": v.get("engagement_rate", 0),
        }

    content_mix_raw = kpi.get("content_media_types", {})
    content_mix = {}
    for k, v in content_mix_raw.items():
        content_mix[k] = {
            "mentions": v.get("mentions", 0),
            "reach": v.get("reach", 0),
            "engagements": v.get("engagements", 0),
            "engagement_rate": v.get("engagement_rate", 0),
        }

    return {
        "campaign_id": kpis.get("campaignId") or kpi.get("campaign_id"),  # may be absent; renderer fills it
        "creators_count": kpi.get("total_users", 0),
        "mentioning_users": kpi.get("mentioning_users", 0),
        "total_mentions": kpi.get("total_mentions", 0),
        "total_reach": kpi.get("reach", 0),
        "total_engagements": kpi.get("engagements", 0),
        "total_impressions": kpi.get("impressions", 0),
        "engagement_rate": kpi.get("engagement_rate", 0),
        "emv": kpi.get("ROI", 0),
        "post_averages": kpi.get("post_averages", {}),
        "networks": networks,
        "content_mix": content_mix,
        "demographics": demos,
        "top_posts_by_engagement": by_eng[:3],
        "top_posts_by_reach": by_reach[:3],
        "recent_post_count": len(posts_recent),
        "all_time_post_count": len(posts_all),
    }


def main():
    p = argparse.ArgumentParser()
    p.add_argument("--raw-dir", default="/home/claude/klear-raw")
    p.add_argument("--out", default="/home/claude/report-data.json")
    p.add_argument("--period-days", type=int, default=365)
    p.add_argument("--keywords", nargs="*", default=[],
                   help="Brand-relevant keywords for filtering profileContent fallback (only used when campaignMeasure exceeds the 1MB limit)")
    p.add_argument("--brand", default=None,
                   help="Brand name (used for audience brand-affinity lookup in demographics)")
    args = p.parse_args()

    cutoff_ts = (datetime.datetime.now() - datetime.timedelta(days=args.period_days)).timestamp()

    cohort_a = load_cohort(args.raw_dir, "cohort-a", args.keywords, cutoff_ts, brand_name=args.brand)
    cohort_b = load_cohort(args.raw_dir, "cohort-b", args.keywords, cutoff_ts, brand_name=args.brand)

    out = {
        "period": {
            "start": datetime.datetime.fromtimestamp(cutoff_ts).date().isoformat(),
            "end": datetime.datetime.now().date().isoformat(),
            "days": args.period_days,
        },
        "cohort_a": cohort_a,
        "cohort_b": cohort_b,
    }

    with open(args.out, "w") as f:
        json.dump(out, f, indent=2, default=str)
    print(f"Wrote {args.out}")
    print(f"  cohort A: {cohort_a['creators_count']} creators, "
          f"{cohort_a['total_mentions']} mentions, "
          f"{cohort_a['recent_post_count']} recent posts")
    print(f"  cohort B: {cohort_b['creators_count']} creators, "
          f"{cohort_b['total_mentions']} mentions, "
          f"{cohort_b['recent_post_count']} recent posts")


if __name__ == "__main__":
    main()
