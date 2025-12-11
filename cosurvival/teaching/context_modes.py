"""
Assignment Context Modes
=======================
Defines Practice, Study, and Graded modes with different permission levels.
"""

# =============================================================================
# IMPORTS
# =============================================================================

from dataclasses import dataclass, field
from enum import Enum
from typing import List, Optional, Set
from datetime import datetime


class ContextMode(Enum):
    """Assignment context mode - determines what help is allowed."""
    PRACTICE = "practice"      # Full support allowed
    STUDY = "study"            # Strong guidance, not full answers
    GRADED = "graded"          # Restricted - hints only, no answers


@dataclass
class AssignmentContext:
    """
    Context for an assignment - determines what TEACHER can provide.
    
    This is the key to preventing TEACHER from becoming a cheating engine.
    """
    assignment_id: str
    mode: ContextMode
    
    # Assignment metadata
    title: str
    description: str
    rubric: Optional[str] = None
    
    # Constraints
    tools_allowed: Set[str] = field(default_factory=set)  # calculator, internet, notes, etc.
    time_limit: Optional[float] = None  # minutes
    collaboration_allowed: bool = False
    
    # Student work requirements
    requires_student_attempt: bool = False  # Must see student work first
    student_attempt_provided: bool = False
    
    # Metadata
    created_at: datetime = field(default_factory=datetime.now)
    course_id: Optional[str] = None
    week_number: Optional[int] = None
    
    def __post_init__(self):
        # Auto-set requirements based on mode
        if self.mode == ContextMode.GRADED:
            self.requires_student_attempt = True
    
    def allows_full_solution(self) -> bool:
        """Can we show the full solution?"""
        return self.mode == ContextMode.PRACTICE
    
    def allows_worked_example(self) -> bool:
        """Can we show a worked example?"""
        return self.mode in [ContextMode.PRACTICE, ContextMode.STUDY]
    
    def allows_hints(self) -> bool:
        """Can we provide hints?"""
        return True  # Always allowed
    
    def allows_parallel_example(self) -> bool:
        """Can we show a parallel (different) example?"""
        return True  # Always allowed, even in graded mode
    
    def requires_attempt_first(self) -> bool:
        """Must student provide attempt before detailed help?"""
        return (
            self.mode == ContextMode.GRADED
            and not self.student_attempt_provided
        )
    
    def can_show_steps(self) -> bool:
        """Can we show step-by-step solution?"""
        if self.mode == ContextMode.PRACTICE:
            return True
        if self.mode == ContextMode.STUDY:
            return True  # But not the final answer
        return False  # Graded mode - no steps
    
    def can_explain_mistake(self) -> bool:
        """Can we explain what's wrong with student's attempt?"""
        return True  # Always allowed if student provides attempt

    def register_student_attempt(self):
        """Mark that the student has provided an attempt."""
        self.student_attempt_provided = True

    def add_tool(self, tool: str):
        """Allow a tool for this context (e.g., calculator, notes)."""
        self.tools_allowed.add(tool.lower())

    def requires_time_guard(self) -> bool:
        """Whether the session should enforce timing (security/academic integrity)."""
        return self.mode == ContextMode.GRADED and self.time_limit is not None

    def can_perform(self, action: str) -> tuple[bool, str]:
        """
        Policy enforcement helper.
        
        Supported actions:
        - "full_solution"
        - "worked_example"
        - "hints"
        - "steps"
        - "parallel_example"
        - "mistake_explanation"
        
        Returns:
            (allowed: bool, reason: str)
        """
        action = action.lower().strip()
        if action == "full_solution":
            if self.allows_full_solution():
                return True, "Full solution allowed in practice mode."
            return False, "Full solutions are only allowed in practice mode."
        
        if action == "worked_example":
            if self.allows_worked_example():
                return True, "Worked example allowed in practice/study."
            return False, "Worked examples not allowed in graded mode."
        
        if action == "hints":
            return True, "Hints always allowed."
        
        if action == "steps":
            if self.can_show_steps():
                return True, "Step-by-step is allowed."
            return False, "Step-by-step not allowed in graded mode."
        
        if action == "parallel_example":
            if self.allows_parallel_example():
                return True, "Parallel examples are allowed."
            return False, "Parallel examples not allowed."
        
        if action == "mistake_explanation":
            if self.student_attempt_provided or not self.requires_student_attempt:
                return True, "Mistake explanations allowed after attempt."
            return False, "Need student attempt before explaining mistakes."
        
        return False, f"Unknown action '{action}'."
    
    def to_dict(self) -> dict:
        """Convert to dictionary."""
        return {
            'assignment_id': self.assignment_id,
            'mode': self.mode.value,
            'title': self.title,
            'description': self.description,
            'rubric': self.rubric,
            'tools_allowed': list(self.tools_allowed),
            'time_limit': self.time_limit,
            'collaboration_allowed': self.collaboration_allowed,
            'requires_student_attempt': self.requires_student_attempt,
            'student_attempt_provided': self.student_attempt_provided,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'course_id': self.course_id,
            'week_number': self.week_number,
        }


def detect_context_mode(
    assignment_title: str,
    assignment_description: str,
    tags: Optional[List[str]] = None,
    metadata: Optional[dict] = None,
) -> ContextMode:
    """
    Detect context mode from assignment metadata.
    
    Heuristics:
    - "exam", "test", "quiz", "graded" → GRADED
    - "practice", "homework", "exercise" → PRACTICE
    - "study", "review", "preparation" → STUDY
    - Default: STUDY (safest)
    """
    text = (assignment_title + " " + assignment_description).lower()
    tags_lower = [t.lower() for t in (tags or [])]
    
    # Graded indicators
    graded_keywords = ["exam", "test", "quiz", "graded", "assessment", "final", "midterm"]
    if any(kw in text for kw in graded_keywords) or any(kw in tags_lower for kw in graded_keywords):
        return ContextMode.GRADED
    
    # Practice indicators
    practice_keywords = ["practice", "homework", "exercise", "drill", "worksheet"]
    if any(kw in text for kw in practice_keywords) or any(kw in tags_lower for kw in practice_keywords):
        return ContextMode.PRACTICE
    
    # Study indicators
    study_keywords = ["study", "review", "preparation", "prep"]
    if any(kw in text for kw in study_keywords) or any(kw in tags_lower for kw in study_keywords):
        return ContextMode.STUDY
    
    # Check metadata
    if metadata:
        if metadata.get("is_graded", False):
            return ContextMode.GRADED
        if metadata.get("is_practice", False):
            return ContextMode.PRACTICE
    
    # Default: STUDY (safest - allows guidance but not full answers)
    return ContextMode.STUDY


def create_practice_context(
    assignment_id: str,
    title: str,
    description: str,
    tools_allowed: Optional[Set[str]] = None,
) -> AssignmentContext:
    """Create a practice mode context."""
    return AssignmentContext(
        assignment_id=assignment_id,
        mode=ContextMode.PRACTICE,
        title=title,
        description=description,
        tools_allowed=tools_allowed or set(),
        requires_student_attempt=False,
    )


def create_study_context(
    assignment_id: str,
    title: str,
    description: str,
    tools_allowed: Optional[Set[str]] = None,
) -> AssignmentContext:
    """Create a study mode context."""
    return AssignmentContext(
        assignment_id=assignment_id,
        mode=ContextMode.STUDY,
        title=title,
        description=description,
        tools_allowed=tools_allowed or set(),
        requires_student_attempt=False,
    )


def create_graded_context(
    assignment_id: str,
    title: str,
    description: str,
    tools_allowed: Optional[Set[str]] = None,
    time_limit: Optional[float] = None,
) -> AssignmentContext:
    """Create a graded mode context."""
    return AssignmentContext(
        assignment_id=assignment_id,
        mode=ContextMode.GRADED,
        title=title,
        description=description,
        tools_allowed=tools_allowed or set(),
        time_limit=time_limit,
        requires_student_attempt=True,
    )

