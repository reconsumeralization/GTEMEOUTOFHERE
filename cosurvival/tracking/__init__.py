"""
COSURVIVAL TRACKING MODULE
==========================
Learning progression tracking and self-relative assessment.

This package contains:
- progression_tracker: CS50-inspired self-relative learning tracking
- review_system: Multi-factor review system for features and course
"""

import sys
from pathlib import Path

# Add parent directory to path for imports
_parent_dir = Path(__file__).parent.parent.parent
if str(_parent_dir) not in sys.path:
    sys.path.insert(0, str(_parent_dir))

from progression_tracker import (
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
)

from cosurvival.tracking.review_system import (
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

__all__ = [
    # Progression tracking
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
]
