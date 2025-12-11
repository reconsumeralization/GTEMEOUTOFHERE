"""
COSURVIVAL CORE MODULE
======================
Core data models, governance, and ingestion.

This package contains the foundational components:
- models: Data structures for TRIBE, TEACHER, RECON
- governance: PII handling, bias guardrails, Triple Balance
- ingestion: Schema-first data normalization
"""

# Import from root-level modules (maintaining backward compatibility)
import sys
from pathlib import Path

# Add parent directory to path for imports
_parent_dir = Path(__file__).parent.parent.parent
if str(_parent_dir) not in sys.path:
    sys.path.insert(0, str(_parent_dir))

# Re-export core components
from models import (
    EthicsGrade,
    ActivityType,
    RelationshipType,
    LearningStatus,
    TribeUser,
    TribeCompany,
    TribeGroup,
    TribeRelationship,
    TribeCommunity,
    TeacherSkill,
    TeacherRole,
    TeacherProgression,
    TeacherLearningPath,
    TeacherModule,
    TeacherRecommendation,
    ReconProvider,
    ReconConsumer,
    ReconValueFlow,
    ReconEthicsScore,
    IntegrationInsight,
    TripleBalanceDecision,
    TribeData,
    TeacherData,
    ReconsumeralizationData,
    CosurvivalData,
)

from governance import (
    SensitivityLevel,
    PIIType,
    ColumnDefinition,
    PIIHandler,
    GovernanceGate,
    GovernanceReport,
    create_data_dictionary,
    STANDARD_COLUMN_CLASSIFICATIONS,
    PROHIBITED_INFERENCES,
    BIAS_GUARDRAILS,
)

from ingestion import (
    CanonicalUser,
    CanonicalCompany,
    CanonicalGroup,
    CanonicalProvider,
    CanonicalResource,
    CanonicalActivity,
    CanonicalPermissionChange,
    IngestionPipeline,
    ingest_csv,
)

__all__ = [
    # Models
    "EthicsGrade",
    "ActivityType",
    "RelationshipType",
    "LearningStatus",
    "TribeUser",
    "TribeCompany",
    "TribeGroup",
    "TribeRelationship",
    "TribeCommunity",
    "TeacherSkill",
    "TeacherRole",
    "TeacherProgression",
    "TeacherLearningPath",
    "TeacherModule",
    "TeacherRecommendation",
    "ReconProvider",
    "ReconConsumer",
    "ReconValueFlow",
    "ReconEthicsScore",
    "IntegrationInsight",
    "TripleBalanceDecision",
    "TribeData",
    "TeacherData",
    "ReconsumeralizationData",
    "CosurvivalData",
    # Governance
    "SensitivityLevel",
    "PIIType",
    "ColumnDefinition",
    "PIIHandler",
    "GovernanceGate",
    "GovernanceReport",
    "create_data_dictionary",
    "STANDARD_COLUMN_CLASSIFICATIONS",
    "PROHIBITED_INFERENCES",
    "BIAS_GUARDRAILS",
    # Ingestion
    "CanonicalUser",
    "CanonicalCompany",
    "CanonicalGroup",
    "CanonicalProvider",
    "CanonicalResource",
    "CanonicalActivity",
    "CanonicalPermissionChange",
    "IngestionPipeline",
    "ingest_csv",
]
