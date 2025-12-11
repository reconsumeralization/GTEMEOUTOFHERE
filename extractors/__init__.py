"""
COSURVIVAL EXTRACTORS - Rapid Pipeline
=======================================
Python productivity layer for TRIBE/TEACHER/RECON extraction.

This is the "ship it in a week" code - fast, Pythonic, experimental.
The formal core (governance, models, boundaries) is in the root-level modules.

Two-speed development doctrine:
- CORE: slow, formal, audited (governance, models, ingestion)
- RAPID: fast, Pythonic, experimental (this package)
"""

# Core extraction functions
from extractors.ingest import (
    CanonicalActivity,
    CanonicalUser,
    CanonicalCompany,
    CanonicalProvider,
    ingest_csv,
    extract_entities,
    hash_pii,
)

from extractors.tribe_graph import (
    build_tribe_graph,
    extract_communities,
    find_mentors,
    find_bridges,
)

from extractors.teacher_paths import (
    build_role_skill_matrix,
    generate_recommendations,
    track_progressions,
    identify_org_skill_gaps,
)

from extractors.recon_scores import (
    score_providers,
    identify_friction_points,
    calculate_value_flows,
)

from extractors.export_json import (
    export_tribe_json,
    export_teacher_json,
    export_recon_json,
    export_unified_json,
    save_json,
)

from extractors.rapid_pipeline import (
    run_rapid_pipeline,
)

__all__ = [
    # Ingest
    "CanonicalActivity",
    "CanonicalUser",
    "CanonicalCompany",
    "CanonicalProvider",
    "ingest_csv",
    "extract_entities",
    "hash_pii",
    # TRIBE
    "build_tribe_graph",
    "extract_communities",
    "find_mentors",
    "find_bridges",
    # TEACHER
    "build_role_skill_matrix",
    "generate_recommendations",
    "track_progressions",
    "identify_org_skill_gaps",
    # RECON
    "score_providers",
    "identify_friction_points",
    "calculate_value_flows",
    # Export
    "export_tribe_json",
    "export_teacher_json",
    "export_recon_json",
    "export_unified_json",
    "save_json",
    # Pipeline
    "run_rapid_pipeline",
]
