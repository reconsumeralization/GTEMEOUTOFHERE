#!/usr/bin/env python3
"""
RECON PROVIDER SCORING
======================
Fast provider evaluation using Python aggregation.

Dictionary comprehensions, fast aggregation = clean, readable code.
"""

from typing import Dict, List
from collections import defaultdict
from copy import deepcopy


def score_providers(activities: List) -> Dict[str, Dict]:
    """
    Score all providers - fast aggregation.

    Week 4: Deep copy activities to avoid shared references
    Week 5: Use defaultdict for efficient aggregation

    Returns:
        Dict mapping provider_id to score dict (safe, deep copied)
    """
    provider_stats = defaultdict(
        lambda: {"total": 0, "errors": 0, "companies": set(), "users": set()}
    )

    # Fast aggregation with deep copies (Week 4: memory safety)
    for activity in activities:
        # Deep copy to avoid shared references
        activity_copy = deepcopy(activity) if hasattr(activity, "__dict__") else activity
        provider_id = None

        if hasattr(activity, "provider_id"):
            provider_id = activity.provider_id
        elif isinstance(activity, dict):
            provider_id = activity.get("provider_id")

        if not provider_id or provider_id == "":
            continue

        provider_stats[provider_id]["total"] += 1

        # Track companies and users
        company_id = (
            activity.company_id
            if hasattr(activity, "company_id")
            else activity.get("company_id", "")
        )
        user_id = activity.user_id if hasattr(activity, "user_id") else activity.get("user_id", "")

        if company_id:
            provider_stats[provider_id]["companies"].add(company_id)
        if user_id:
            provider_stats[provider_id]["users"].add(user_id)

        # Count errors
        error_code = (
            activity.error_code
            if hasattr(activity, "error_code")
            else activity.get("error_code", "")
        )
        if error_code:
            provider_stats[provider_id]["errors"] += 1

    # Calculate scores
    scores = {}
    for provider_id, stats in provider_stats.items():
        reliability = 1 - (stats["errors"] / stats["total"]) if stats["total"] > 0 else 0

        # Grade assignment
        if reliability >= 0.99:
            grade = "A"
        elif reliability >= 0.95:
            grade = "B"
        elif reliability >= 0.90:
            grade = "C"
        elif reliability >= 0.80:
            grade = "D"
        else:
            grade = "F"

        scores[provider_id] = {
            "reliability": reliability,
            "grade": grade,
            "total_activities": stats["total"],
            "error_count": stats["errors"],
            "error_rate": stats["errors"] / stats["total"] if stats["total"] > 0 else 0,
            "customer_count": len(stats["companies"]),
            "user_count": len(stats["users"]),
        }

    return scores


def identify_friction_points(activities: List, provider_scores: Dict) -> List[Dict]:
    """
    Identify friction points - list comprehension.

    Returns:
        List of friction points with reasons
    """
    friction_points = []

    for provider_id, score in provider_scores.items():
        reasons = []

        if score["reliability"] < 0.9:
            reasons.append("High error rate")

        if score["total_activities"] < 10:
            reasons.append("Low engagement")

        if score["customer_count"] < 2:
            reasons.append("Limited adoption")

        if reasons:
            friction_points.append(
                {
                    "provider_id": provider_id,
                    "reasons": reasons,
                    "reliability": score["reliability"],
                    "grade": score["grade"],
                    "total_activities": score["total_activities"],
                }
            )

    return sorted(friction_points, key=lambda x: len(x["reasons"]), reverse=True)


def calculate_value_flows(activities: List, provider_scores: Dict) -> List[Dict]:
    """
    Calculate value flows between providers and companies.

    Returns:
        List of value flow records
    """
    flows = defaultdict(lambda: {"volume": 0, "errors": 0})

    for activity in activities:
        provider_id = (
            activity.provider_id
            if hasattr(activity, "provider_id")
            else activity.get("provider_id", "")
        )
        company_id = (
            activity.company_id
            if hasattr(activity, "company_id")
            else activity.get("company_id", "")
        )

        if provider_id and company_id:
            key = (provider_id, company_id)
            flows[key]["volume"] += 1

            error_code = (
                activity.error_code
                if hasattr(activity, "error_code")
                else activity.get("error_code", "")
            )
            if error_code:
                flows[key]["errors"] += 1

    # Convert to list with quality scores
    value_flows = []
    for (provider_id, company_id), stats in flows.items():
        quality = 1 - (stats["errors"] / stats["volume"]) if stats["volume"] > 0 else 0
        value_score = stats["volume"] * quality

        value_flows.append(
            {
                "provider_id": provider_id,
                "company_id": company_id,
                "volume": stats["volume"],
                "quality": quality,
                "value_score": value_score,
            }
        )

    return sorted(value_flows, key=lambda x: x["value_score"], reverse=True)


if __name__ == "__main__":
    print("RECON Provider Scorer - Ready")
    print("Use score_providers(), identify_friction_points(), calculate_value_flows()")
