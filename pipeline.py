#!/usr/bin/env python3
"""
COSURVIVAL COMPLETE PIPELINE
============================
The single entry point that orchestrates:
1. Governance gate (safety checks)
2. Schema-first ingestion (data normalization)
3. MVP extraction (proof of concept outputs)
4. Unified JSON generation (dashboard-ready)

Usage:
    python pipeline.py <csv_path> [output_dir]
    
Example:
    python pipeline.py brian_activity_data.csv ./output

CURRICULUM MAPPING:
-------------------
Week 4+: Domains - Applied Systems
  - Integrates all three lenses: TRIBE, TEACHER, RECON
  - Builds complete end-to-end pipelines
  - See: TEACHER_CORE_TRACK.md, Week 4+, Theme: "Applied Systems"

Capstone: Real World Application
  - Theme: "Prove It Works"
  - Runs complete pipeline on real dataset
  - Produces: Governance Report, TRIBE Output, TEACHER Output, RECON Output
  - See: TEACHER_CORE_TRACK.md, Capstone section

This pipeline demonstrates:
- Week 0: Governance gate (PII, bias, prohibited inferences)
- Week 1: Schema detection and canonical entities
- Week 2: Data structure validation
- Week 3: Algorithm implementation (TRIBE/TEACHER/RECON extractors)
- Week 4+: Complete system integration
"""

# =============================================================================
# IMPORTS
# =============================================================================

# =============================================================================
# IMPORTS
# =============================================================================
# Standard library imports
import json
import sys
from datetime import datetime
from pathlib import Path
from typing import Dict, Any

# Local imports
from governance import create_data_dictionary
from ingestion import IngestionPipeline
from mvp_extractors import run_mvp_extraction


def run_complete_pipeline(
    csv_path: str,
    output_dir: str = ".",
    governance_enabled: bool = True,
    pii_reversal: bool = False,
    export_parquet: bool = True,
) -> Dict[str, Any]:
    """
    Run the complete Cosurvival pipeline.

    This function orchestrates the entire curriculum journey:
    1. Governance (Week 0, Activity 0.3 & 0.4)
    2. Ingestion (Week 1 & 2)
    3. Extraction (Week 3)
    4. Integration (Week 4+)

    CURRICULUM: Capstone - Real World Application
    This is the complete pipeline learners build for their capstone project.
    See: TEACHER_CORE_TRACK.md, Capstone section

    Args:
        csv_path: Path to input CSV file
        output_dir: Directory for output files
        governance_enabled: Whether to run governance checks (Week 0)
        pii_reversal: Whether to allow PII reverse lookup (Week 10 - Security)
        export_parquet: Whether to export Parquet files

    Returns:
        Dictionary with pipeline results
    """
    print("=" * 70)
    print("  COSURVIVAL COMPLETE PIPELINE")
    print("  Governance → Ingestion → MVP Extraction → Unified Output")
    print("=" * 70)

    output_path = Path(output_dir)
    output_path.mkdir(parents=True, exist_ok=True)

    stages: Dict[str, Any] = {}
    results: Dict[str, Any] = {
        "started_at": datetime.now().isoformat(),
        "input_file": csv_path,
        "output_dir": str(output_path),
        "stages": stages,
    }

    # ==========================================================================
    # STAGE 1: GOVERNANCE + INGESTION
    # ==========================================================================
    print("\n" + "=" * 70)
    print("  STAGE 1: GOVERNANCE + INGESTION")
    print("=" * 70)

    pipeline = IngestionPipeline(governance_enabled=governance_enabled, pii_reversal=pii_reversal)

    # Load data (with content validation)
    try:
        df = pipeline.load_csv(csv_path)

        # Log security event
        try:
            from security import security_audit_log

            security_audit_log.log_event(
                "data_ingestion",
                {
                    "file": csv_path,
                    "rows": len(df),
                    "columns": len(df.columns),
                    "governance_enabled": governance_enabled,
                },
            )
        except ImportError:
            pass  # Security module optional
    except Exception as e:
        results["success"] = False
        results["error"] = f"Failed to load CSV: {e}"
        return results

    # Run governance checks (with enhanced severity scoring)
    if governance_enabled:
        gov_report = pipeline.run_governance_check(df)
        stages["governance"] = gov_report.to_dict()

        # Enhanced severity assessment if any vulnerabilities found
        # (This would be called when processing security reports)
        if gov_report.risk_flags:
            try:
                from security import security_audit_log

                security_audit_log.log_event(
                    "governance_risk_flags",
                    {
                        "risk_flags": gov_report.risk_flags,
                        "review_required": gov_report.review_required,
                    },
                )
            except ImportError:
                pass

        # Export governance report
        gov_path = output_path / "governance_report.json"
        with open(gov_path, "w") as f:
            json.dump(gov_report.to_dict(), f, indent=2)

        # Export data dictionary
        if pipeline.governance_gate is not None:
            classifications = pipeline.governance_gate.classify_columns(list(df.columns))
            data_dict = create_data_dictionary(classifications)
            dict_path = output_path / "data_dictionary.md"
            with open(dict_path, "w", encoding="utf-8") as f:
                f.write(data_dict)

        if not gov_report.overall_passed:
            print("\n⚠️  GOVERNANCE CHECK FAILED")
            print("   Cannot proceed without addressing critical issues.")
            print(f"   Review report at: {gov_path}")

            results["success"] = False
            results["error"] = "Governance check failed"
            return results

    # Detect schema
    schema_report = pipeline.detect_schema(df)
    stages["schema"] = schema_report

    # Extract entities
    entity_counts = pipeline.extract_entities(df)
    stages["ingestion"] = {
        "raw_rows": pipeline.raw_row_count,
        "processed_rows": pipeline.processed_row_count,
        "error_rows": len(pipeline.error_rows),
        "entities": entity_counts,
    }

    # Export clean data
    if export_parquet:
        try:
            parquet_files = pipeline.export_parquet(str(output_path))
            stages["ingestion"]["parquet_files"] = parquet_files
        except Exception as e:
            print(f"⚠️  Parquet export failed: {e}")

    jsonl_path = output_path / "events_clean.jsonl"
    pipeline.export_jsonl(str(jsonl_path))

    print(
        f"\n✓ Ingestion complete: {entity_counts['users']} users, "
        f"{entity_counts['companies']} companies, "
        f"{entity_counts['activities']} activities"
    )

    # ==========================================================================
    # STAGE 2: MVP EXTRACTION
    # ==========================================================================
    print("\n" + "=" * 70)
    print("  STAGE 2: MVP EXTRACTION")
    print("=" * 70)

    # Get canonical entities
    users = pipeline.users
    companies = pipeline.companies
    groups = pipeline.groups
    providers = pipeline.providers
    activities = pipeline.activities
    permission_changes = pipeline.permission_changes

    # Run MVP extraction
    cosurvival_json = run_mvp_extraction(
        users=users,
        companies=companies,
        groups=groups,
        providers=providers,
        activities=activities,
        permission_changes=permission_changes,
        output_path=str(output_path / "cosurvival_mvp.json"),
        governance_report=results["stages"].get("governance"),
    )

    stages["mvp"] = {
        "tribe": {
            "users": cosurvival_json["entities"]["users"],
            "communities": len(cosurvival_json["tribe"]["communities"]),
            "bridges": len(cosurvival_json["tribe"]["cross_silo_bridges"]),
            "mentor_candidates": len(cosurvival_json["tribe"]["mentor_candidates"]),
        },
        "teacher": {
            "roles": cosurvival_json["teacher"]["total_roles"],
            "progressions": len(cosurvival_json["teacher"]["skill_progressions"]),
            "recommendations": cosurvival_json["teacher"]["total_recommendations_generated"],
        },
        "reconsumeralization": {
            "providers": len(cosurvival_json["reconsumeralization"]["provider_scores"]),
            "value_flows": len(cosurvival_json["reconsumeralization"]["top_value_flows"]),
            "friction_points": len(cosurvival_json["reconsumeralization"]["friction_points"]),
        },
    }

    # ==========================================================================
    # STAGE 3: DASHBOARD-READY OUTPUT
    # ==========================================================================
    print("\n" + "=" * 70)
    print("  STAGE 3: DASHBOARD-READY OUTPUT")
    print("=" * 70)

    # Generate network graph for D3
    generate_network_json(users, companies, groups, activities, output_path)

    # Generate summary for dashboard
    generate_dashboard_summary(cosurvival_json, output_path)

    stages["dashboard"] = {
        "network_file": str(output_path / "tribe_network.json"),
        "summary_file": str(output_path / "dashboard_summary.json"),
    }

    # ==========================================================================
    # FINAL SUMMARY
    # ==========================================================================
    print("\n" + "=" * 70)
    print("  PIPELINE COMPLETE")
    print("=" * 70)

    results["success"] = True
    results["completed_at"] = datetime.now().isoformat()
    results["output_files"] = {
        "governance_report": str(output_path / "governance_report.json"),
        "data_dictionary": str(output_path / "data_dictionary.md"),
        "events_clean": str(jsonl_path),
        "cosurvival_mvp": str(output_path / "cosurvival_mvp.json"),
        "tribe_network": str(output_path / "tribe_network.json"),
        "dashboard_summary": str(output_path / "dashboard_summary.json"),
    }

    # Export results
    results_path = output_path / "pipeline_results.json"
    with open(results_path, "w") as f:
        json.dump(results, f, indent=2, default=str)

    print(f"\n  📁 Output directory: {output_path}")
    print("\n  Generated files:")
    for name, path in results["output_files"].items():
        print(f"     • {name}: {Path(path).name}")

    print("\n  🚀 Ready for dashboard!")
    print("     Run: python -m http.server 8000")
    print("     Open: http://localhost:8000/dashboard.html")

    return results


def generate_network_json(users, companies, groups, activities, output_path) -> Dict[str, Any]:
    """Generate D3-compatible network JSON."""
    print("   Generating network graph JSON...")

    nodes = []
    links = []

    # Add user nodes (limit for performance)
    user_list = list(users.values())[:200]
    for user in user_list:
        nodes.append(
            {
                "id": user.id,
                "name": f"User {user.id[:8]}...",
                "type": "user",
                "size": min(5 + user.activity_count / 50, 30),
                "company": user.company_id,
            }
        )

    # Add company nodes
    for company_id, company in companies.items():
        nodes.append(
            {
                "id": f"company_{company_id}",
                "name": company.name or f"Company {company_id[:8]}",
                "type": "company",
                "size": 20 + min(company.user_count, 30),
            }
        )

    # Build edges from activities
    edge_weights: Dict[tuple[str, str], int] = {}
    for activity in activities:
        if activity.target_user_id and activity.user_id != activity.target_user_id:
            if activity.user_id in [u.id for u in user_list] and activity.target_user_id in [
                u.id for u in user_list
            ]:
                key = tuple(sorted([activity.user_id, activity.target_user_id]))
                edge_weights[key] = edge_weights.get(key, 0) + 1

    for (u1, u2), weight in list(edge_weights.items())[:500]:
        links.append({"source": u1, "target": u2, "weight": weight, "type": "collaboration"})

    network_data = {"nodes": nodes, "links": links}

    network_path = output_path / "tribe_network.json"
    with open(network_path, "w") as f:
        json.dump(network_data, f, indent=2)

    print(f"   ✓ Network graph: {len(nodes)} nodes, {len(links)} links")
    return network_data


def generate_dashboard_summary(cosurvival_json, output_path) -> Dict[str, Any]:
    """Generate summary data optimized for dashboard display."""
    print("   Generating dashboard summary...")

    summary = {
        "generated_at": datetime.now().isoformat(),
        "overview": {
            "users": cosurvival_json["entities"]["users"],
            "companies": cosurvival_json["entities"]["companies"],
            "groups": cosurvival_json["entities"]["groups"],
            "providers": cosurvival_json["entities"]["providers"],
        },
        "tribe_highlights": {
            "communities": len(cosurvival_json["tribe"]["communities"]),
            "network_density": cosurvival_json["tribe"]["network_density"],
            "bridge_connectors": len(cosurvival_json["tribe"]["cross_silo_bridges"]),
            "mentor_candidates": len(cosurvival_json["tribe"]["mentor_candidates"]),
            "top_collaborations": cosurvival_json["tribe"]["top_collaborating_companies"][:5],
        },
        "teacher_highlights": {
            "roles": cosurvival_json["teacher"]["total_roles"],
            "progressions": len(cosurvival_json["teacher"]["skill_progressions"]),
            "recommendations": cosurvival_json["teacher"]["total_recommendations_generated"],
            "top_progression": cosurvival_json["teacher"]["most_common_progression"],
            "orgs_with_gaps": len(cosurvival_json["teacher"]["org_skill_gaps"]),
        },
        "recon_highlights": {
            "providers_scored": len(cosurvival_json["reconsumeralization"]["provider_scores"]),
            "top_providers": cosurvival_json["reconsumeralization"]["top_providers"],
            "needing_attention": cosurvival_json["reconsumeralization"][
                "providers_needing_attention"
            ],
            "friction_points": len(cosurvival_json["reconsumeralization"]["friction_points"]),
            "total_value": cosurvival_json["reconsumeralization"]["total_value_exchanged"],
        },
        "governance": {
            "passed": cosurvival_json["governance"]["passed"],
            "risk_flags": cosurvival_json["governance"]["risk_flags"][:5],
            "review_required": cosurvival_json["governance"]["review_required"],
        },
        "insights": cosurvival_json["integration_insights"][:10],
    }

    summary_path = output_path / "dashboard_summary.json"
    with open(summary_path, "w") as f:
        json.dump(summary, f, indent=2)

    print("   ✓ Dashboard summary generated")
    return summary


# =============================================================================
# CLI ENTRY POINT
# =============================================================================


def main():
    """Main entry point for CLI."""
    if len(sys.argv) < 2:
        print(
            """
COSURVIVAL PIPELINE
===================

Usage:
    python pipeline.py <csv_path> [output_dir] [options]

Arguments:
    csv_path    Path to input CSV file (required)
    output_dir  Output directory (default: current directory)

Options:
    --no-governance    Skip governance checks (not recommended)
    --allow-reversal   Allow PII reverse lookup (requires permission)
    --no-parquet       Skip Parquet export

Example:
    python pipeline.py brian_activity_data.csv ./output

This pipeline will:
1. ✓ Run governance checks (PII, bias, prohibited inferences)
2. ✓ Normalize and clean the data
3. ✓ Extract TRIBE network (communities, bridges, mentors)
4. ✓ Extract TEACHER pathways (skills, progressions, recommendations)
5. ✓ Extract RECONSUMERALIZATION scores (providers, flows, friction)
6. ✓ Generate unified JSON for the dashboard
        """
        )
        sys.exit(1)

    csv_path = sys.argv[1]
    output_dir = sys.argv[2] if len(sys.argv) > 2 and not sys.argv[2].startswith("--") else "."

    # Parse options
    governance_enabled = "--no-governance" not in sys.argv
    pii_reversal = "--allow-reversal" in sys.argv
    export_parquet = "--no-parquet" not in sys.argv

    if not governance_enabled:
        print("⚠️  WARNING: Running without governance checks is not recommended!")

    if pii_reversal:
        print("⚠️  WARNING: PII reverse lookup enabled - ensure you have proper authorization!")

    result = run_complete_pipeline(
        csv_path=csv_path,
        output_dir=output_dir,
        governance_enabled=governance_enabled,
        pii_reversal=pii_reversal,
        export_parquet=export_parquet,
    )

    if result["success"]:
        print("\n✅ Pipeline completed successfully!")
        sys.exit(0)
    else:
        print(f"\n❌ Pipeline failed: {result.get('error', 'Unknown error')}")
        sys.exit(1)


if __name__ == "__main__":
    main()
