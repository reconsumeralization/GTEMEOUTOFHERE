#!/usr/bin/env python3
"""
TEACHER Week 3: MVP Extractors Demo
===================================
Demonstrates the three core algorithms that make TRIBE, TEACHER, and RECON work.

This shows:
1. Collaboration Strength (TRIBE)
2. Role Mastery Profile (TEACHER)
3. Provider Reliability Score (RECON)
"""

from dataclasses import dataclass
from typing import Dict, List, Optional, Set
from collections import defaultdict
from datetime import datetime


# =============================================================================
# DATA MODELS
# =============================================================================


@dataclass
class CanonicalActivity:
    """Canonical activity entity."""

    id: str
    timestamp: str
    timestamp_date: str
    activity_type: str
    user_id: str
    target_user_id: str = ""
    company_id: str = ""
    resource_id: str = ""
    state_before: str = ""
    state_after: str = ""
    error_code: str = ""
    provider_id: str = ""


@dataclass
class CanonicalPermissionChange:
    """Canonical permission change entity."""

    id: str
    timestamp: str
    user_id: str
    state_before: str
    state_after: str
    permission_type: str = ""


@dataclass
class CanonicalProvider:
    """Canonical provider entity."""

    id: str
    name: str
    reliability_score: float = 0.0


# =============================================================================
# SAMPLE DATA
# =============================================================================

SAMPLE_ACTIVITIES = [
    CanonicalActivity(
        id="act_1",
        timestamp="2024-01-15T10:00:00Z",
        timestamp_date="2024-01-15",
        activity_type="document_share",
        user_id="user_alice",
        target_user_id="user_bob",
        resource_id="doc_123",
        provider_id="provider_sharepoint",
    ),
    CanonicalActivity(
        id="act_2",
        timestamp="2024-01-15T10:30:00Z",
        timestamp_date="2024-01-15",
        activity_type="document_access",
        user_id="user_bob",
        resource_id="doc_123",
        provider_id="provider_sharepoint",
    ),
    CanonicalActivity(
        id="act_3",
        timestamp="2024-01-15T11:00:00Z",
        timestamp_date="2024-01-15",
        activity_type="permission_change",
        user_id="user_alice",
        state_before="viewer",
        state_after="editor",
        provider_id="provider_sharepoint",
    ),
    CanonicalActivity(
        id="act_4",
        timestamp="2024-01-15T12:00:00Z",
        timestamp_date="2024-01-15",
        activity_type="api_call",
        user_id="user_carol",
        provider_id="provider_google",
        error_code="ERR_500",
    ),
    CanonicalActivity(
        id="act_5",
        timestamp="2024-01-15T13:00:00Z",
        timestamp_date="2024-01-15",
        activity_type="api_call",
        user_id="user_carol",
        provider_id="provider_google",
    ),
]

SAMPLE_PERMISSION_CHANGES = [
    CanonicalPermissionChange(
        id="perm_1",
        timestamp="2024-01-15T11:00:00Z",
        user_id="user_alice",
        state_before="viewer",
        state_after="editor",
        permission_type="document_access",
    ),
    CanonicalPermissionChange(
        id="perm_2",
        timestamp="2024-01-16T09:00:00Z",
        user_id="user_alice",
        state_before="editor",
        state_after="admin",
        permission_type="document_access",
    ),
]


# =============================================================================
# EXTRACTOR 1: COLLABORATION STRENGTH (TRIBE)
# =============================================================================


def collaboration_strength(user_a: str, user_b: str, activities: List[CanonicalActivity]) -> float:
    """
    Calculate collaboration strength between two users.

    Factors:
    - Direct interactions (UidOpp/UidReq)
    - Co-resource access (same resource on same day)

    Efficiency: O(m) where m = activities count

    Returns: Score from 0.0 to 1.0
    """
    if user_a == user_b:
        return 0.0  # Can't collaborate with yourself

    direct_count = 0
    co_access_count = 0

    # Track resource access by date
    resource_access: Dict[str, Dict[str, Set[str]]] = defaultdict(lambda: defaultdict(set))

    for activity in activities:
        # Direct interactions
        if (activity.user_id == user_a and activity.target_user_id == user_b) or (
            activity.user_id == user_b and activity.target_user_id == user_a
        ):
            direct_count += 1

        # Track resource co-access
        if activity.resource_id and activity.timestamp_date:
            resource_access[activity.resource_id][activity.timestamp_date].add(activity.user_id)

    # Count co-access
    for resource_id, date_users in resource_access.items():
        for date, users in date_users.items():
            if user_a in users and user_b in users:
                co_access_count += 1

    # Weighted combination
    direct_score = min(direct_count / 10.0, 1.0)  # Normalize
    co_access_score = min(co_access_count / 5.0, 1.0)  # Normalize

    return (direct_score * 0.6) + (co_access_score * 0.4)


# =============================================================================
# EXTRACTOR 2: ROLE MASTERY PROFILE (TEACHER)
# =============================================================================


def is_permission_upgrade(before: str, after: str) -> bool:
    """Check if permission change represents an upgrade."""
    hierarchy = ["viewer", "commenter", "editor", "admin"]
    try:
        return hierarchy.index(after) > hierarchy.index(before)
    except ValueError:
        return False


def extract_skill_from_permission(change: CanonicalPermissionChange) -> str:
    """Extract skill name from permission change."""
    return f"{change.permission_type}_{change.state_after}"


def role_mastery_profile(user_id: str, permission_changes: List[CanonicalPermissionChange]) -> Dict:
    """
    Build mastery profile from permission history.

    Key insight: Permission upgrades = skill demonstrations

    Efficiency: O(m) where m = permission changes
    """
    skills = []
    progressions = []

    for change in permission_changes:
        if change.user_id != user_id:
            continue

        # Check if this is an upgrade
        if is_permission_upgrade(change.state_before, change.state_after):
            skill = extract_skill_from_permission(change)
            skills.append(skill)

            progressions.append(
                {
                    "from": change.state_before,
                    "to": change.state_after,
                    "timestamp": change.timestamp,
                    "skill": skill,
                }
            )

    # Calculate trajectory
    trajectory = "growing" if len(progressions) > 1 else "stable"

    return {
        "user_id": user_id,
        "skills": skills,
        "progressions": progressions,
        "trajectory": trajectory,
        "mastery_score": min(len(skills) / 10.0, 1.0),  # Normalize
    }


# =============================================================================
# EXTRACTOR 3: PROVIDER RELIABILITY SCORE (RECON)
# =============================================================================


def provider_reliability_score(provider_id: str, activities: List[CanonicalActivity]) -> Dict:
    """
    Calculate provider reliability score.

    Score = 1 - (error_rate)
    Confidence based on sample size

    Efficiency: O(m) where m = activities
    """
    provider_activities = [a for a in activities if a.provider_id == provider_id]

    if not provider_activities:
        return {
            "provider_id": provider_id,
            "reliability_score": 0.0,
            "confidence": 0.0,
            "error_rate": 1.0,
            "total_activities": 0,
            "error_count": 0,
            "grade": "F",
        }

    total = len(provider_activities)
    errors = sum(1 for a in provider_activities if a.error_code)
    error_rate = errors / total if total > 0 else 1.0
    reliability = 1.0 - error_rate

    # Confidence increases with sample size
    confidence = min(total / 100.0, 1.0)  # 100+ activities = full confidence

    # Calculate grade
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

    return {
        "provider_id": provider_id,
        "reliability_score": reliability,
        "confidence": confidence,
        "error_rate": error_rate,
        "total_activities": total,
        "error_count": errors,
        "grade": grade,
    }


# =============================================================================
# DEMO
# =============================================================================


def main():
    """Run the extractors demo."""
    print("=" * 70)
    print("  TEACHER WEEK 3: MVP EXTRACTORS DEMO")
    print("  The Algorithms That Make COSURVIVAL Work")
    print("=" * 70)

    # ========================================================================
    # EXTRACTOR 1: COLLABORATION STRENGTH
    # ========================================================================
    print("\n[EXTRACTOR 1] COLLABORATION STRENGTH (TRIBE)")
    print("-" * 70)

    strength = collaboration_strength("user_alice", "user_bob", SAMPLE_ACTIVITIES)
    print(f"  Collaboration strength (alice <-> bob): {strength:.3f}")
    print(f"  Algorithm: Weighted combination of direct interactions + co-resource access")
    print(f"  Efficiency: O(m) where m = {len(SAMPLE_ACTIVITIES)} activities")

    # ========================================================================
    # EXTRACTOR 2: ROLE MASTERY PROFILE
    # ========================================================================
    print("\n[EXTRACTOR 2] ROLE MASTERY PROFILE (TEACHER)")
    print("-" * 70)

    profile = role_mastery_profile("user_alice", SAMPLE_PERMISSION_CHANGES)
    print(f"  User: {profile['user_id']}")
    print(f"  Skills acquired: {len(profile['skills'])}")
    print(f"  Progressions: {len(profile['progressions'])}")
    print(f"  Trajectory: {profile['trajectory']}")
    print(f"  Mastery score: {profile['mastery_score']:.3f}")
    print(f"  Algorithm: Track permission upgrades as skill demonstrations")
    print(f"  Efficiency: O(m) where m = {len(SAMPLE_PERMISSION_CHANGES)} permission changes")

    if profile["progressions"]:
        print(f"\n  Progressions:")
        for prog in profile["progressions"]:
            print(f"    {prog['from']} -> {prog['to']} ({prog['skill']})")

    # ========================================================================
    # EXTRACTOR 3: PROVIDER RELIABILITY SCORE
    # ========================================================================
    print("\n[EXTRACTOR 3] PROVIDER RELIABILITY SCORE (RECON)")
    print("-" * 70)

    # Score provider_sharepoint
    sharepoint_score = provider_reliability_score("provider_sharepoint", SAMPLE_ACTIVITIES)
    print(f"  Provider: {sharepoint_score['provider_id']}")
    print(f"  Reliability: {sharepoint_score['reliability_score']:.3f}")
    print(f"  Error rate: {sharepoint_score['error_rate']:.3f}")
    print(f"  Grade: {sharepoint_score['grade']}")
    print(f"  Confidence: {sharepoint_score['confidence']:.3f}")
    print(f"  Total activities: {sharepoint_score['total_activities']}")

    # Score provider_google
    google_score = provider_reliability_score("provider_google", SAMPLE_ACTIVITIES)
    print(f"\n  Provider: {google_score['provider_id']}")
    print(f"  Reliability: {google_score['reliability_score']:.3f}")
    print(f"  Error rate: {google_score['error_rate']:.3f}")
    print(f"  Grade: {google_score['grade']}")
    print(f"  Confidence: {google_score['confidence']:.3f}")
    print(f"  Total activities: {google_score['total_activities']}")

    print(f"\n  Algorithm: Error rate calculation with confidence intervals")
    print(f"  Efficiency: O(m) where m = {len(SAMPLE_ACTIVITIES)} activities")

    # ========================================================================
    # EFFICIENCY ANALYSIS
    # ========================================================================
    print("\n" + "=" * 70)
    print("  EFFICIENCY ANALYSIS")
    print("=" * 70)

    print("\n  All three extractors are O(m) - linear time:")
    print("    - Must examine each activity/permission change")
    print("    - Acceptable for most use cases")
    print("    - Can optimize with indexing for O(1) lookups")

    print("\n  At scale (1,000,000 activities):")
    print("    - Linear scan: ~1 second")
    print("    - With indexing: ~0.1 seconds")
    print("    - Difference matters in production")

    # ========================================================================
    # KEY TAKEAWAYS
    # ========================================================================
    print("\n" + "=" * 70)
    print("  KEY TAKEAWAYS")
    print("=" * 70)
    print("  1. Algorithms are real, working code")
    print("  2. Efficiency matters at scale")
    print("  3. The three extractors enable TRIBE/TEACHER/RECON")
    print("  4. Simple algorithms can be powerful")
    print("  5. Optimization comes when needed")
    print("\n" + "=" * 70)
    print("  This is where intelligence extraction happens.")
    print("=" * 70 + "\n")


if __name__ == "__main__":
    main()
