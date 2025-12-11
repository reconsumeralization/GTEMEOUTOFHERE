"""
COSURVIVAL - Core Package
==========================
The Cosurvival system for TRIBE, TEACHER, and RECONSUMERALIZATION.

This package provides:
- Core data models and governance
- AI advisors (certified and standard)
- Learning progression tracking
- Security and privacy tools
- Data structures for fairness and trust
"""

__version__ = "1.0.0"

# Core exports - import from subpackage __init__.py files
from cosurvival.core import (  # type: ignore[import-untyped]
    # Models
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
    # Governance
    SensitivityLevel,
    PIIType,
    PIIHandler,
    GovernanceGate,
    GovernanceReport,
    create_data_dictionary,
    # Ingestion
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

# Advisors - import from subpackage __init__.py files
from cosurvival.advisors import (  # type: ignore[import-untyped]
    Domain,
    SignalStrength,
    RecommendationType,
    PatternSignal,
    Recommendation,
    UserPreferences,
    CrossDomainInsight,
    CosurvivalAdvisor,
    CertificationLevel,
    LearningSource,
    TrustMetric,
    TEACHERCertification,
    CrossGenerationalLearning,
    LaborOfLoveMetrics,
    TEACHERAdvisor,
)

# Tracking - import from subpackage __init__.py files
from cosurvival.tracking import (  # type: ignore[import-untyped]
    ModuleStatus,
    Trajectory,
    CheckpointResult,
    Skill,
    Module,
    Activity,
    Checkpoint,
    LearnerProfile,
    CompetencySnapshot,
    CheckpointAttempt,
    MasteryDelta,
    ProgressionTracker,
    # Review system
    ReviewSystem,
    Review,
    ReviewSummary,
    ReviewStage,
    ReviewTarget,
    ReviewFactor,
    FactorRating,
    create_week_review,
    create_feature_review,
    create_course_review,
)

# Teaching - import from subpackage __init__.py files
from cosurvival.teaching import (  # type: ignore[import-untyped]
    ContextMode,
    AssignmentContext,
    detect_context_mode,
    create_practice_context,
    create_study_context,
    create_graded_context,
)

__all__ = [
    # Core models
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
    "PIIHandler",
    "GovernanceGate",
    "GovernanceReport",
    "create_data_dictionary",
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
    # Advisors
    "Domain",
    "SignalStrength",
    "RecommendationType",
    "PatternSignal",
    "Recommendation",
    "UserPreferences",
    "CrossDomainInsight",
    "CosurvivalAdvisor",
    # TEACHER Advisor
    "CertificationLevel",
    "LearningSource",
    "TrustMetric",
    "TEACHERCertification",
    "CrossGenerationalLearning",
    "LaborOfLoveMetrics",
    "TEACHERAdvisor",
    # Tracking
    "ModuleStatus",
    "Trajectory",
    "CheckpointResult",
    "Skill",
    "Module",
    "Activity",
    "Checkpoint",
    "LearnerProfile",
    "CompetencySnapshot",
    "CheckpointAttempt",
    "MasteryDelta",
    "ProgressionTracker",
    # Review system
    "ReviewSystem",
    "Review",
    "ReviewSummary",
    "ReviewStage",
    "ReviewTarget",
    "ReviewFactor",
    "FactorRating",
    "create_week_review",
    "create_feature_review",
    "create_course_review",
    # Teaching
    "ContextMode",
    "AssignmentContext",
    "detect_context_mode",
    "create_practice_context",
    "create_study_context",
    "create_graded_context",
]
