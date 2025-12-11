"""
COSURVIVAL ADVISORS MODULE
==========================
AI advisors for cross-domain pattern recognition and early warnings.

This package contains:
- advisor: Base CosurvivalAdvisor with cross-domain pattern recognition
- teacher_advisor: TEACHER-certified advisor with cross-generational learning
"""

import sys
from pathlib import Path

# Add parent directory to path for imports
_parent_dir = Path(__file__).parent.parent.parent
if str(_parent_dir) not in sys.path:
    sys.path.insert(0, str(_parent_dir))

from advisor import (
    Domain,
    SignalStrength,
    RecommendationType,
    PatternSignal,
    Recommendation,
    UserPreferences,
    CrossDomainInsight,
    CosurvivalAdvisor,
)

from teacher_advisor import (
    CertificationLevel,
    LearningSource,
    TrustMetric,
    TEACHERCertification,
    CrossGenerationalLearning,
    LaborOfLoveMetrics,
    TEACHERAdvisor,
)

__all__ = [
    "Domain",
    "SignalStrength",
    "RecommendationType",
    "PatternSignal",
    "Recommendation",
    "UserPreferences",
    "CrossDomainInsight",
    "CosurvivalAdvisor",
    "CertificationLevel",
    "LearningSource",
    "TrustMetric",
    "TEACHERCertification",
    "CrossGenerationalLearning",
    "LaborOfLoveMetrics",
    "TEACHERAdvisor",
]
