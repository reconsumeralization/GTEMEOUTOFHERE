"""
COSURVIVAL TEACHING MODULE
==========================
Shadow Student Mode: Student-Sim + Tutor + Validator pattern

This package contains:
- context_modes: Assignment context modes (Practice/Study/Graded)
- Shadow Student Mode agents for deep assignment understanding
"""

# Import from package-local modules
from cosurvival.teaching.context_modes import (
    ContextMode,
    AssignmentContext,
    detect_context_mode,
    create_practice_context,
    create_study_context,
    create_graded_context,
)

# Note: Other modules (learning_trace, shadow_student, tutor_agent, etc.)
# will be imported here once implemented

__all__ = [
    # Context modes
    'ContextMode',
    'AssignmentContext',
    'detect_context_mode',
    'create_practice_context',
    'create_study_context',
    'create_graded_context',
]

