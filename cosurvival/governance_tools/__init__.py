"""
COSURVIVAL GOVERNANCE TOOLS MODULE
===================================
Tools for enforcing privacy, scope, and lens boundaries.

This package contains:
- lens_boundary: Lens boundary contracts and enforcement
- lensgrind: Privacy and scope auditor (like Valgrind for memory)
"""

import sys
from pathlib import Path

# Add parent directory to path for imports
_parent_dir = Path(__file__).parent.parent.parent
if str(_parent_dir) not in sys.path:
    sys.path.insert(0, str(_parent_dir))

from lens_boundary import (
    LensType,
    BoundaryRule,
    BoundaryEnforcer,
    LENS_BOUNDARIES,
)

from lensgrind import (
    Violation,
    Lensgrind,
)

__all__ = [
    "LensType",
    "BoundaryRule",
    "BoundaryEnforcer",
    "LENS_BOUNDARIES",
    "Violation",
    "Lensgrind",
]
