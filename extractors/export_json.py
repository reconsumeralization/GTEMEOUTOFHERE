#!/usr/bin/env python3
"""
EXPORT TO DASHBOARD-READY JSON
==============================
Fast JSON serialization for dashboard consumption.

Python's built-in JSON = one function call.
"""

"""
EXPORT TO DASHBOARD-READY JSON
==============================
Fast JSON serialization for dashboard consumption.

Python's built-in JSON = one function call.
"""

# Standard library imports
import json  # noqa: E402
import os  # noqa: E402
from copy import deepcopy  # noqa: E402
from datetime import datetime  # noqa: E402
from typing import Dict, List, Optional  # noqa: E402

# Local imports
from security import sanitize_json_value  # noqa: E402


def export_tribe_json(
    graph_data: Dict,
    communities: List[List[str]],
    mentors: List[Dict],
    bridges: Optional[List[Dict]] = None,
) -> Dict:
    """
    Export TRIBE data to JSON.

    Week 4: Deep copy to safe schema (no shared references)
    Week 10: Sanitize JSON values (prevent JSON injection)

    Args:
        graph_data: Graph structure (nodes, edges)
        communities: List of community member lists
        mentors: List of mentor candidates
        bridges: List of bridge connectors

    Returns:
        TRIBE JSON structure (safe, sanitized)
    """
    # Deep copy to avoid shared references (Week 4)
    safe_communities = [deepcopy(comm) for comm in communities]
    safe_mentors = [deepcopy(mentor) for mentor in mentors]
    safe_bridges = [deepcopy(bridge) for bridge in (bridges or [])]

    # Sanitize all values (Week 10: JSON injection prevention)
    def sanitize_dict(d: Dict) -> Dict:
        return {k: sanitize_json_value(v) for k, v in d.items()}

    safe_mentors = [sanitize_dict(m) for m in safe_mentors]
    safe_bridges = [sanitize_dict(b) for b in safe_bridges]

    return {
        "lens": "tribe",
        "generated_at": datetime.now().isoformat(),
        "network": {
            "nodes": len(graph_data.get("nodes", []))
            if isinstance(graph_data, dict)
            else graph_data.number_of_nodes()
            if hasattr(graph_data, "number_of_nodes")
            else 0,
            "edges": len(graph_data.get("edges", []))
            if isinstance(graph_data, dict)
            else graph_data.number_of_edges()
            if hasattr(graph_data, "number_of_edges")
            else 0,
        },
        "communities": [
            {
                "id": i,
                "size": len(comm),
                "members": [sanitize_json_value(m) for m in comm[:10]],  # Sample, sanitized
            }
            for i, comm in enumerate(safe_communities[:10])  # Top 10
        ],
        "mentor_candidates": safe_mentors[:10],
        "bridge_connectors": safe_bridges[:10],
    }


def export_teacher_json(
    role_skills: Dict[str, List[str]],
    recommendations: List[Dict],
    progressions: List[Dict],
    org_gaps: Optional[Dict[str, List[str]]] = None,
) -> Dict:
    """
    Export TEACHER data to JSON.

    Args:
        role_skills: Dict mapping role_id to set of skills
        recommendations: List of learning recommendations
        progressions: List of skill progressions
        org_gaps: Dict mapping company_id to missing skills

    Returns:
        TEACHER JSON structure
    """
    return {
        "lens": "teacher",
        "generated_at": datetime.now().isoformat(),
        "role_skill_matrix": {role: list(skills) for role, skills in role_skills.items()},
        "recommendations": recommendations[:20],
        "progressions": progressions[:20],
        "org_skill_gaps": org_gaps or {},
    }


def export_recon_json(
    provider_scores: Dict, friction_points: List[Dict], value_flows: Optional[List[Dict]] = None
) -> Dict:
    """
    Export RECON data to JSON.

    Args:
        provider_scores: Dict mapping provider_id to score
        friction_points: List of friction points
        value_flows: List of value flow records

    Returns:
        RECON JSON structure
    """
    # Sort providers by reliability
    top_providers = sorted(
        provider_scores.items(), key=lambda x: x[1].get("reliability", 0), reverse=True
    )[:5]

    # Count grades
    grade_counts: Dict[str, int] = {}
    for score in provider_scores.values():
        grade = score.get("grade", "F")
        grade_counts[grade] = grade_counts.get(grade, 0) + 1

    return {
        "lens": "recon",
        "generated_at": datetime.now().isoformat(),
        "provider_scores": provider_scores,
        "top_providers": [pid for pid, _ in top_providers],
        "friction_points": friction_points[:10],
        "value_flows": (value_flows or [])[:10],
        "grade_distribution": grade_counts,
    }


def generate_cross_system_insights(tribe: Dict, teacher: Dict, recon: Dict) -> List[Dict]:
    """
    Generate cross-system integration insights.

    Returns:
        List of integration insights
    """
    insights = []

    # Insight: Mentors who could teach missing skills
    if tribe.get("mentor_candidates") and teacher.get("org_skill_gaps"):
        mentors = tribe.get("mentor_candidates", [])
        gaps = teacher.get("org_skill_gaps", {})

        if mentors and gaps:
            insights.append(
                {
                    "type": "mentorship_opportunity",
                    "description": f"{len(mentors)} mentor candidates could help address skill gaps",
                    "priority": "medium",
                }
            )

    # Insight: Friction points affecting communities
    if tribe.get("communities") and recon.get("friction_points"):
        communities = tribe.get("communities", [])
        friction = recon.get("friction_points", [])

        if communities and friction:
            insights.append(
                {
                    "type": "friction_community_impact",
                    "description": f"{len(friction)} provider friction points may affect {len(communities)} communities",
                    "priority": "high",
                }
            )

    return insights


def export_unified_json(tribe: Dict, teacher: Dict, recon: Dict) -> Dict:
    """
    Export unified COSURVIVAL JSON.

    This is the "ship it" output - three lenses, one file.
    """
    return {
        "version": "1.0.0",
        "generated_at": datetime.now().isoformat(),
        "tribe": tribe,
        "teacher": teacher,
        "reconsumeralization": recon,
        "integration": {"insights": generate_cross_system_insights(tribe, teacher, recon)},
    }


def save_json(data: Dict, filepath: str) -> str:
    """
    Save JSON to file - Python makes this trivial.

    Week 10: Validate filename (prevent path traversal)
    Week 10: Sanitize data before saving

    Args:
        data: Dictionary to serialize
        filepath: Output file path

    Returns:
        Path to saved file
    """
    # Validate filename (Week 10: security)
    from security import is_safe_filename

    filename = os.path.basename(filepath)
    if not is_safe_filename(filename):
        raise ValueError(f"Unsafe filename: {filename}")

    # Deep copy and sanitize data (Week 4: memory safety, Week 10: security)
    safe_data = deepcopy(data)

    def sanitize_recursive(obj):
        """Recursively sanitize JSON values."""
        if isinstance(obj, dict):
            return {k: sanitize_recursive(v) for k, v in obj.items()}
        elif isinstance(obj, list):
            return [sanitize_recursive(item) for item in obj]
        elif isinstance(obj, str):
            return sanitize_json_value(obj)
        else:
            return obj

    safe_data = sanitize_recursive(safe_data)

    with open(filepath, "w", encoding="utf-8") as f:
        json.dump(safe_data, f, indent=2, default=str)

    print(f"✓ Saved JSON to {filepath}")
    return filepath


if __name__ == "__main__":
    print("JSON Exporter - Ready")
    print(
        "Use export_tribe_json(), export_teacher_json(), export_recon_json(), export_unified_json()"
    )
