#!/usr/bin/env python3
"""
RAPID PIPELINE - Ship It in a Week
===================================
Complete Python pipeline: CSV → Three JSON Views

This is the "productivity layer" - fast, Pythonic, shippable.
The formal core (governance, models) is imported from parent.
"""

import sys
from pathlib import Path
from typing import Dict, Any, List, Optional  # noqa: F401 (Optional used in return type)
from datetime import datetime

# Add parent to path
parent_dir = Path(__file__).parent.parent
sys.path.insert(0, str(parent_dir))

from extractors.ingest import ingest_csv, extract_entities  # noqa: E402
from extractors.tribe_graph import (
    build_tribe_graph,
    extract_communities,
    find_mentors,
    find_bridges,
)  # noqa: E402
from extractors.teacher_paths import (
    build_role_skill_matrix,
    track_progressions,
    identify_org_skill_gaps,
)  # noqa: E402
from extractors.recon_scores import (
    score_providers,
    identify_friction_points,
    calculate_value_flows,
)  # noqa: E402
from extractors.export_json import export_unified_json, save_json  # noqa: E402
from governance import GovernanceGate, PIIHandler  # noqa: E402
from lens_boundary import LENS_BOUNDARIES  # noqa: E402


def ensure_no_prohibited_fields(lens: str, payload: Dict[str, Any]) -> None:
    """Ensure payload keys do not violate lens boundary prohibitions."""

    prohibited = {field.lower() for field in LENS_BOUNDARIES[lens].prohibited_fields}
    violations = set()

    def _scan(obj: Any):
        if isinstance(obj, dict):
            for key, value in obj.items():
                if key.lower() in prohibited:
                    violations.add(key)
                _scan(value)
        elif isinstance(obj, list):
            for item in obj:
                _scan(item)

    _scan(payload)

    if violations:
        raise ValueError(
            f"Lens '{lens}' payload contains prohibited fields: {', '.join(sorted(violations))}"
        )


def run_rapid_pipeline(
    csv_path: str, output_path: str = "cosurvival_output.json"
) -> Optional[Dict[str, Any]]:
    """
    Run complete pipeline: CSV → TRIBE/TEACHER/RECON JSON.

    This is the "ship it in a week" version.

    Args:
        csv_path: Path to input CSV
        output_path: Path for output JSON

    Returns:
        Unified COSURVIVAL JSON
    """
    print("=" * 70)
    print("  RAPID PIPELINE - Python Productivity Layer")
    print("  CSV -> TRIBE/TEACHER/RECON -> Unified JSON")
    print("=" * 70)

    try:
        governance_gate = GovernanceGate(PIIHandler())

        # 1. INGEST - Fast CSV loading
        print("\n[1/5] Ingesting CSV...")
        df = ingest_csv(csv_path)
        governance_report = governance_gate.run_full_check(
            df,
            analysis_intents=[
                "tribe_network_mapping",
                "teacher_learning_paths",
                "recon_provider_scoring",
            ],
            output_types=[
                "community_detection",
                "skill_progression",
                "provider_reliability",
            ],
        )
        if not governance_report.overall_passed:
            print("\n✗ Governance gate blocked processing. Review source data and try again.")
            return None
        users, companies, providers, activities = extract_entities(df)
        print(f"   ✓ Loaded {len(activities)} activities")

        # 2. TRIBE - Network analysis
        print("\n[2/5] Extracting TRIBE network...")
        graph = build_tribe_graph(activities)
        communities = extract_communities(graph)
        mentors = find_mentors(graph, users)
        bridges = find_bridges(graph, communities)

        # Convert graph to dict if NetworkX
        if hasattr(graph, "nodes") and hasattr(graph, "edges"):
            graph_data: Dict[str, Any] = {
                "nodes": list(graph.nodes()),
                "edges": [{"source": u, "target": v} for u, v in graph.edges()],
            }
        else:
            graph_data = graph if isinstance(graph, dict) else {"nodes": [], "edges": []}

        tribe_json = {
            "lens": "tribe",
            "generated_at": datetime.now().isoformat(),
            "network": {
                "nodes": len(graph_data.get("nodes", [])),
                "edges": len(graph_data.get("edges", [])),
            },
            "communities": [
                {"id": i, "size": len(comm), "members": comm[:10]}
                for i, comm in enumerate(communities[:10])
            ],
            "mentor_candidates": mentors[:10],
            "bridge_connectors": bridges[:10],
        }
        print(f"   ✓ Found {len(communities)} communities, {len(mentors)} mentor candidates")
        ensure_no_prohibited_fields("tribe", tribe_json)

        # 3. TEACHER - Learning pathways
        print("\n[3/5] Extracting TEACHER pathways...")

        # Extract permission changes from activities
        permission_changes = [
            a
            for a in activities
            if hasattr(a, "state_before")
            and hasattr(a, "state_after")
            and a.state_before
            and a.state_after
            and a.state_before != a.state_after
        ]

        role_skills = build_role_skill_matrix(permission_changes)
        progressions = track_progressions(permission_changes)

        # Generate recommendations (simplified - would need user roles)
        recommendations: List[Dict[str, Any]] = []
        user_roles: Dict[str, str] = {}  # Would come from data

        org_gaps = identify_org_skill_gaps(users, role_skills, user_roles)

        teacher_json = {
            "lens": "teacher",
            "generated_at": datetime.now().isoformat(),
            "role_skill_matrix": {role: list(skills) for role, skills in role_skills.items()},
            "recommendations": recommendations[:20],
            "progressions": progressions[:20],
            "org_skill_gaps": org_gaps,
        }
        print(f"   ✓ Found {len(role_skills)} roles, {len(progressions)} progressions")
        ensure_no_prohibited_fields("teacher", teacher_json)

        # 4. RECON - Provider scoring
        print("\n[4/5] Scoring providers (RECON)...")
        provider_scores = score_providers(activities)
        friction_points = identify_friction_points(activities, provider_scores)
        value_flows = calculate_value_flows(activities, provider_scores)

        recon_json = {
            "lens": "recon",
            "generated_at": datetime.now().isoformat(),
            "provider_scores": provider_scores,
            "friction_points": friction_points[:10],
            "value_flows": value_flows[:10],
        }
        print(
            f"   ✓ Scored {len(provider_scores)} providers, found {len(friction_points)} friction points"
        )
        ensure_no_prohibited_fields("recon", recon_json)

        # 5. UNIFIED - Combine all three
        print("\n[5/5] Generating unified JSON...")
        unified = export_unified_json(tribe_json, teacher_json, recon_json)

        # Save to file
        save_json(unified, output_path)

        print("\n" + "=" * 70)
        print("  PIPELINE COMPLETE")
        print("=" * 70)
        print(f"\n  Output: {output_path}")
        print(f"  TRIBE: {len(communities)} communities")
        print(f"  TEACHER: {len(role_skills)} roles")
        print(f"  RECON: {len(provider_scores)} providers")
        print("\n  ✓ Ready for dashboard!")

        return unified

    except FileNotFoundError:
        print(f"✗ Error: File not found: {csv_path}")
        return None
    except Exception as e:
        print(f"✗ Error: {e}")
        import traceback

        traceback.print_exc()
        return None


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python rapid_pipeline.py <csv_path> [output_path]")
        print("\nExample: python rapid_pipeline.py brian_data.csv output.json")
        sys.exit(1)

    csv_path = sys.argv[1]
    output_path = sys.argv[2] if len(sys.argv) > 2 else "cosurvival_output.json"

    result = run_rapid_pipeline(csv_path, output_path)

    if result:
        print("\n✅ Success! Pipeline completed.")
    else:
        print("\n❌ Pipeline failed. Check errors above.")
