#!/usr/bin/env python3
"""
TEACHER LEARNING PATHWAY EXTRACTION
===================================
Fast Python operations for learning analysis.

Set operations, dict lookups, list comprehensions = readable, fast code.
"""

from typing import Dict, List, Set
from collections import defaultdict


def build_role_skill_matrix(permission_changes: List) -> Dict[str, Set[str]]:
    """
    Build role → skills mapping - fast dict operations.

    Returns:
        Dict mapping role_id to set of skills
    """
    role_skills = defaultdict(set)

    for change in permission_changes:
        role = None
        skill = None

        if hasattr(change, "role_id"):
            role = change.role_id
        elif isinstance(change, dict):
            role = change.get("role_id")

        if hasattr(change, "permission_type"):
            skill = change.permission_type
        elif isinstance(change, dict):
            skill = change.get("permission_type")

        if role and skill:
            role_skills[role].add(skill)

    return dict(role_skills)


def generate_recommendations(
    user_id: str, user_skills: Set[str], role_skills: Dict[str, Set[str]], user_role: str
) -> List[Dict]:
    """
    Generate recommendations - set operations.

    Returns:
        List of recommended skills with reasons
    """
    required = role_skills.get(user_role, set())
    missing = required - user_skills

    recommendations = []
    for skill in list(missing)[:5]:  # Top 5
        recommendations.append(
            {
                "user_id": user_id,
                "recommended_skill": skill,
                "reason": f"Commonly held by peers in role {user_role}",
                "priority": "high" if len(missing) > 3 else "medium",
            }
        )

    return recommendations


def track_progressions(permission_changes: List) -> List[Dict]:
    """
    Track skill progressions - list comprehensions.

    Returns:
        List of state transitions
    """
    progressions = []

    for change in permission_changes:
        state_before = None
        state_after = None

        if hasattr(change, "state_before"):
            state_before = change.state_before
        elif isinstance(change, dict):
            state_before = change.get("state_before")

        if hasattr(change, "state_after"):
            state_after = change.state_after
        elif isinstance(change, dict):
            state_after = change.get("state_after")

        if state_before and state_after and state_before != state_after:
            progressions.append(
                {
                    "from": state_before,
                    "to": state_after,
                    "user_id": change.user_id
                    if hasattr(change, "user_id")
                    else change.get("user_id", ""),
                    "timestamp": change.timestamp
                    if hasattr(change, "timestamp")
                    else change.get("timestamp", ""),
                }
            )

    # Count frequencies
    progression_counts = defaultdict(int)
    for prog in progressions:
        key = f"{prog['from']} -> {prog['to']}"
        progression_counts[key] += 1

    # Add frequency to each progression
    for prog in progressions:
        key = f"{prog['from']} -> {prog['to']}"
        prog["frequency"] = progression_counts[key]

    return sorted(progressions, key=lambda x: x["frequency"], reverse=True)


def identify_org_skill_gaps(
    users: Dict, role_skills: Dict[str, Set[str]], user_roles: Dict[str, str]
) -> Dict[str, List[str]]:
    """
    Identify organization-level skill gaps.

    Returns:
        Dict mapping company_id to list of missing skills
    """
    company_skills = defaultdict(set)
    company_users = defaultdict(list)

    # Aggregate skills by company
    for user_id, user in users.items():
        company_id = user.company_id if hasattr(user, "company_id") else user.get("company_id", "")
        if company_id:
            company_users[company_id].append(user_id)

            # Get user's role
            user_role = user_roles.get(user_id, "")
            if user_role:
                # Add role skills to company
                company_skills[company_id].update(role_skills.get(user_role, set()))

    # Find gaps
    all_skills = set()
    for skills in role_skills.values():
        all_skills.update(skills)

    org_gaps = {}
    for company_id, skills in company_skills.items():
        missing = all_skills - skills
        if missing:
            org_gaps[company_id] = list(missing)[:10]  # Top 10

    return org_gaps


if __name__ == "__main__":
    print("TEACHER Pathway Extractor - Ready")
    print("Use build_role_skill_matrix(), generate_recommendations(), track_progressions()")
