#!/usr/bin/env python3
"""
TEACHER PROGRESSION TRACKER
===========================
CS50-inspired self-relative mastery tracking.

Core Philosophy:
"What ultimately matters is not where you end up relative to your classmates,
but where you end up relative to yourself when you began."

This tracker:
- Never compares learners to each other
- Never labels gaps as deficiencies
- Always frames progress as growth opportunities
- Measures trajectory, not position
"""

"""
TEACHER PROGRESSION TRACKER
===========================
CS50-inspired self-relative mastery tracking.

Core Philosophy:
"What ultimately matters is not where you end up relative to your classmates,
but where you end up relative to yourself when you began."

This tracker:
- Never compares learners to each other
- Never labels gaps as deficiencies
- Always frames progress as growth opportunities
- Measures trajectory, not position
"""

# Standard library imports
import hashlib
import json
from dataclasses import dataclass, field, asdict
from datetime import datetime
from enum import Enum
from pathlib import Path
from typing import Dict, List, Optional, Any, Set


# =============================================================================
# ENUMS
# =============================================================================


class ModuleStatus(Enum):
    """Status of a learning module for a learner."""

    NOT_STARTED = "not_started"
    IN_PROGRESS = "in_progress"
    CHECKPOINT_READY = "checkpoint_ready"
    COMPLETED = "completed"
    MASTERED = "mastered"  # Completed + demonstrated in practice


class Trajectory(Enum):
    """Learning trajectory direction."""

    ACCELERATING = "accelerating"  # Gaining skills faster over time
    STEADY = "steady"  # Consistent progress
    PLATEAUED = "plateaued"  # Progress slowed (not bad! might be deepening)
    EXPLORING = "exploring"  # Trying new areas


class CheckpointResult(Enum):
    """Result of a checkpoint attempt."""

    PASSED = "passed"
    NEEDS_REVIEW = "needs_review"
    RESUBMIT = "resubmit"


# =============================================================================
# CORE DATA MODELS
# =============================================================================


@dataclass
class Skill:
    """A skill that can be learned."""

    id: str
    name: str
    category: str  # concepts, fundamentals, structures, algorithms, domains
    description: str = ""
    prerequisites: List[str] = field(default_factory=list)
    indicators: List[str] = field(default_factory=list)  # How mastery is demonstrated

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)


@dataclass
class Module:
    """A learning module in the curriculum."""

    id: str
    week: int
    name: str
    theme: str
    learning_objectives: List[str]
    skills_taught: List[str]  # Skill IDs
    activities: List["Activity"]
    checkpoint: "Checkpoint"
    estimated_hours: float = 5.0

    def to_dict(self) -> Dict[str, Any]:
        return {
            "id": self.id,
            "week": self.week,
            "name": self.name,
            "theme": self.theme,
            "learning_objectives": self.learning_objectives,
            "skills_taught": self.skills_taught,
            "activities": [a.to_dict() for a in self.activities],
            "checkpoint": self.checkpoint.to_dict(),
            "estimated_hours": self.estimated_hours,
        }


@dataclass
class Activity:
    """An activity within a module."""

    id: str
    name: str
    description: str
    duration_minutes: int
    activity_type: str  # interactive, reading, coding, reflection, discussion

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)


@dataclass
class Checkpoint:
    """A checkpoint (like a CS50 problem set) that demonstrates learning."""

    id: str
    name: str
    description: str
    artifact_type: str  # code, document, reflection, project
    rubric: List[str]  # What we look for (not scored numerically)
    mastery_indicators: List[str]  # Checklist of understanding

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)


@dataclass
class LearnerProfile:
    """
    A learner's profile - the foundation for self-relative tracking.

    CRITICAL: This profile is for growth tracking, NOT evaluation.
    """

    id: str
    created_at: str

    # Starting snapshot (captured at enrollment)
    baseline_snapshot: "CompetencySnapshot"

    # Current state
    current_snapshot: "CompetencySnapshot"

    # Module progress
    module_progress: Dict[str, ModuleStatus] = field(default_factory=dict)

    # Checkpoint history
    checkpoint_attempts: List["CheckpointAttempt"] = field(default_factory=list)

    # Trajectory
    trajectory: Trajectory = Trajectory.STEADY

    # Personal notes (learner's own reflections)
    reflections: List[str] = field(default_factory=list)

    # Context (role, organization - for personalization, not comparison)
    role_context: str = ""
    org_context: str = ""

    def to_dict(self) -> Dict[str, Any]:
        return {
            "id": self.id,
            "created_at": self.created_at,
            "baseline_snapshot": self.baseline_snapshot.to_dict(),
            "current_snapshot": self.current_snapshot.to_dict(),
            "module_progress": {k: v.value for k, v in self.module_progress.items()},
            "checkpoint_attempts": [a.to_dict() for a in self.checkpoint_attempts],
            "trajectory": self.trajectory.value,
            "reflections": self.reflections,
            "role_context": self.role_context,
            "org_context": self.org_context,
        }


@dataclass
class CompetencySnapshot:
    """
    A snapshot of a learner's competencies at a point in time.

    Used for self-comparison, NEVER for peer comparison.
    """

    captured_at: str
    skills_demonstrated: Set[str] = field(default_factory=set)
    concepts_understood: Set[str] = field(default_factory=set)
    modules_completed: Set[str] = field(default_factory=set)
    checkpoints_passed: Set[str] = field(default_factory=set)

    # Qualitative self-assessment (not scored)
    confidence_areas: List[str] = field(default_factory=list)
    growth_areas: List[str] = field(default_factory=list)  # NOT "weaknesses"

    def to_dict(self) -> Dict[str, Any]:
        return {
            "captured_at": self.captured_at,
            "skills_demonstrated": list(self.skills_demonstrated),
            "concepts_understood": list(self.concepts_understood),
            "modules_completed": list(self.modules_completed),
            "checkpoints_passed": list(self.checkpoints_passed),
            "confidence_areas": self.confidence_areas,
            "growth_areas": self.growth_areas,
        }


@dataclass
class CheckpointAttempt:
    """A checkpoint submission and its review."""

    id: str
    checkpoint_id: str
    submitted_at: str
    artifact_reference: str  # Link/path to submitted work

    # Review (not a grade!)
    result: CheckpointResult = CheckpointResult.NEEDS_REVIEW
    feedback: str = ""
    mastery_indicators_met: List[str] = field(default_factory=list)

    # Learner reflection
    learner_reflection: str = ""

    def to_dict(self) -> Dict[str, Any]:
        return {
            "id": self.id,
            "checkpoint_id": self.checkpoint_id,
            "submitted_at": self.submitted_at,
            "artifact_reference": self.artifact_reference,
            "result": self.result.value,
            "feedback": self.feedback,
            "mastery_indicators_met": self.mastery_indicators_met,
            "learner_reflection": self.learner_reflection,
        }


@dataclass
class MasteryDelta:
    """
    The growth between two snapshots.

    This is what we celebrate - not position, but movement.
    """

    from_snapshot: str  # timestamp
    to_snapshot: str  # timestamp

    # Gains (always framed positively)
    new_skills: List[str] = field(default_factory=list)
    new_concepts: List[str] = field(default_factory=list)
    new_modules: List[str] = field(default_factory=list)
    new_checkpoints: List[str] = field(default_factory=list)

    # Summary message (human-friendly)
    summary_message: str = ""

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)


# =============================================================================
# PROGRESSION TRACKER SERVICE
# =============================================================================


class ProgressionTracker:
    """
    Service that tracks learner progress using CS50's philosophy.

    Key principles:
    1. Self-relative comparison only
    2. Growth opportunities, not deficiencies
    3. Trajectory over position
    4. Celebration of gains
    """

    def __init__(self):
        self.learners: Dict[str, LearnerProfile] = {}
        self.curriculum: Dict[str, Module] = {}
        self.skills: Dict[str, Skill] = {}

    # =========================================================================
    # CURRICULUM MANAGEMENT
    # =========================================================================

    def register_skill(self, skill: Skill):
        """Register a skill in the curriculum."""
        self.skills[skill.id] = skill

    def register_module(self, module: Module):
        """Register a module in the curriculum."""
        self.curriculum[module.id] = module

    def load_core_curriculum(self):
        """Load the TEACHER Core Track curriculum."""

        # Week 0 Skills
        self.register_skill(
            Skill(
                id="skill_three_lenses",
                name="Understanding the Three Lenses",
                category="concepts",
                description="Ability to view data through TRIBE, TEACHER, and RECON perspectives",
                indicators=[
                    "Can explain each lens",
                    "Can identify which lens applies to a scenario",
                ],
            )
        )

        self.register_skill(
            Skill(
                id="skill_pii_identification",
                name="PII Identification",
                category="concepts",
                description="Ability to identify personally identifiable information",
                indicators=["Can classify columns by sensitivity", "Can explain why PII matters"],
            )
        )

        self.register_skill(
            Skill(
                id="skill_context_interpretation",
                name="Context-Dependent Interpretation",
                category="concepts",
                description="Understanding that same data means different things in different contexts",
                indicators=["Can give examples", "Can explain the Malan quote application"],
            )
        )

        # Week 1 Skills
        self.register_skill(
            Skill(
                id="skill_data_dictionary",
                name="Data Dictionary Creation",
                category="fundamentals",
                description="Ability to document column meanings and sensitivity",
                prerequisites=["skill_pii_identification"],
                indicators=[
                    "Can create complete data dictionary",
                    "Includes sensitivity classification",
                ],
            )
        )

        self.register_skill(
            Skill(
                id="skill_governance_rules",
                name="Governance Rule Writing",
                category="fundamentals",
                description="Ability to write rules that protect privacy and prevent bias",
                prerequisites=["skill_pii_identification"],
                indicators=["Can write blocking rules", "Understands prohibited inferences"],
            )
        )

        # Week 2 Skills
        self.register_skill(
            Skill(
                id="skill_schema_design",
                name="Schema Design",
                category="structures",
                description="Ability to design data schemas for canonical entities",
                prerequisites=["skill_data_dictionary"],
                indicators=["Can design entity schemas", "Includes validation rules"],
            )
        )

        self.register_skill(
            Skill(
                id="skill_graph_construction",
                name="Graph Construction",
                category="structures",
                description="Ability to construct graph representations from activity data",
                indicators=["Can identify nodes and edges", "Can assign edge weights"],
            )
        )

        # Week 3 Skills
        self.register_skill(
            Skill(
                id="skill_algorithm_implementation",
                name="Algorithm Implementation",
                category="algorithms",
                description="Ability to implement scoring and analysis algorithms",
                prerequisites=["skill_schema_design"],
                indicators=[
                    "Can implement collaboration strength",
                    "Can implement provider scoring",
                ],
            )
        )

        # Week 4+ Skills (Domain-specific)
        self.register_skill(
            Skill(
                id="skill_tribe_pipeline",
                name="TRIBE Pipeline Building",
                category="domains",
                description="Ability to build complete TRIBE analysis",
                prerequisites=["skill_graph_construction", "skill_algorithm_implementation"],
                indicators=["Can detect communities", "Can identify bridges and mentors"],
            )
        )

        self.register_skill(
            Skill(
                id="skill_teacher_pipeline",
                name="TEACHER Pipeline Building",
                category="domains",
                description="Ability to build complete TEACHER analysis",
                prerequisites=["skill_algorithm_implementation"],
                indicators=["Can build role-skill matrix", "Can generate recommendations"],
            )
        )

        self.register_skill(
            Skill(
                id="skill_recon_pipeline",
                name="RECON Pipeline Building",
                category="domains",
                description="Ability to build complete RECONSUMERALIZATION analysis",
                prerequisites=["skill_algorithm_implementation"],
                indicators=["Can score providers", "Can identify friction points"],
            )
        )

        print(f"[OK] Loaded {len(self.skills)} skills into curriculum")

    # =========================================================================
    # LEARNER MANAGEMENT
    # =========================================================================

    def enroll_learner(
        self, learner_id: str, role_context: str = "", org_context: str = ""
    ) -> LearnerProfile:
        """
        Enroll a new learner and capture their baseline.

        This baseline is ONLY for self-comparison.
        """
        now = datetime.now().isoformat()

        # Create baseline snapshot (empty for new learners)
        baseline = CompetencySnapshot(
            captured_at=now,
            skills_demonstrated=set(),
            concepts_understood=set(),
            modules_completed=set(),
            checkpoints_passed=set(),
            confidence_areas=[],
            growth_areas=["Everything is a growth area - and that's exciting!"],
        )

        profile = LearnerProfile(
            id=learner_id,
            created_at=now,
            baseline_snapshot=baseline,
            current_snapshot=CompetencySnapshot(captured_at=now),
            module_progress={},
            checkpoint_attempts=[],
            trajectory=Trajectory.STEADY,
            role_context=role_context,
            org_context=org_context,
        )

        self.learners[learner_id] = profile
        return profile

    def start_module(self, learner_id: str, module_id: str) -> Dict[str, Any]:
        """Start a module for a learner."""
        if learner_id not in self.learners:
            raise ValueError(f"Learner {learner_id} not found")

        learner = self.learners[learner_id]
        learner.module_progress[module_id] = ModuleStatus.IN_PROGRESS

        # Get module info
        module = self.curriculum.get(module_id, None)

        return {
            "message": f"Started module: {module.name if module else module_id}",
            "status": "in_progress",
            "encouragement": "Remember: focus on your own growth, not speed.",
        }

    def complete_activity(
        self, learner_id: str, module_id: str, activity_id: str
    ) -> Dict[str, Any]:
        """Record activity completion."""
        if learner_id not in self.learners:
            raise ValueError(f"Learner {learner_id} not found")

        learner = self.learners[learner_id]

        return {
            "message": "Activity completed!",
            "encouragement": "Every step forward is progress.",
        }

    def submit_checkpoint(
        self, learner_id: str, checkpoint_id: str, artifact_reference: str, reflection: str = ""
    ) -> CheckpointAttempt:
        """Submit a checkpoint for review."""
        if learner_id not in self.learners:
            raise ValueError(f"Learner {learner_id} not found")

        attempt = CheckpointAttempt(
            id=f"attempt_{checkpoint_id}_{datetime.now().strftime('%Y%m%d%H%M%S')}",
            checkpoint_id=checkpoint_id,
            submitted_at=datetime.now().isoformat(),
            artifact_reference=artifact_reference,
            result=CheckpointResult.NEEDS_REVIEW,
            learner_reflection=reflection,
        )

        learner = self.learners[learner_id]
        learner.checkpoint_attempts.append(attempt)

        return attempt

    def record_skill_demonstration(self, learner_id: str, skill_id: str):
        """Record that a learner has demonstrated a skill."""
        if learner_id not in self.learners:
            raise ValueError(f"Learner {learner_id} not found")

        learner = self.learners[learner_id]
        learner.current_snapshot.skills_demonstrated.add(skill_id)
        learner.current_snapshot.captured_at = datetime.now().isoformat()

    # =========================================================================
    # PROGRESS CALCULATION (Self-Relative Only!)
    # =========================================================================

    def calculate_mastery_delta(self, learner_id: str) -> MasteryDelta:
        """
        Calculate the learner's growth since baseline.

        This is THE key output - celebrating progress, not position.
        """
        if learner_id not in self.learners:
            raise ValueError(f"Learner {learner_id} not found")

        learner = self.learners[learner_id]
        baseline = learner.baseline_snapshot
        current = learner.current_snapshot

        # Calculate gains
        new_skills = list(current.skills_demonstrated - baseline.skills_demonstrated)
        new_concepts = list(current.concepts_understood - baseline.concepts_understood)
        new_modules = list(current.modules_completed - baseline.modules_completed)
        new_checkpoints = list(current.checkpoints_passed - baseline.checkpoints_passed)

        # Generate celebratory message
        total_gains = len(new_skills) + len(new_concepts) + len(new_modules)

        if total_gains == 0:
            message = "You're at the beginning of your journey. Every expert was once a beginner!"
        elif total_gains < 3:
            message = f"You've made your first steps! {total_gains} new capability unlocked."
        elif total_gains < 10:
            message = (
                f"Solid progress! You've unlocked {total_gains} new capabilities since you began."
            )
        else:
            message = (
                f"Impressive growth! {total_gains} new capabilities since your starting point."
            )

        return MasteryDelta(
            from_snapshot=baseline.captured_at,
            to_snapshot=current.captured_at,
            new_skills=new_skills,
            new_concepts=new_concepts,
            new_modules=new_modules,
            new_checkpoints=new_checkpoints,
            summary_message=message,
        )

    def calculate_trajectory(self, learner_id: str) -> Trajectory:
        """
        Determine the learner's trajectory.

        Trajectory is about direction and pace, not comparison.
        """
        if learner_id not in self.learners:
            raise ValueError(f"Learner {learner_id} not found")

        learner = self.learners[learner_id]

        # Simple trajectory calculation based on checkpoint frequency
        recent_attempts = [
            a for a in learner.checkpoint_attempts if a.result == CheckpointResult.PASSED
        ]

        if len(recent_attempts) == 0:
            return Trajectory.EXPLORING
        elif len(recent_attempts) > 3:
            return Trajectory.ACCELERATING
        else:
            return Trajectory.STEADY

    def get_growth_opportunities(self, learner_id: str) -> List[Dict[str, Any]]:
        """
        Identify growth opportunities (NOT deficiencies).

        Framing matters: these are exciting possibilities, not failures.
        """
        if learner_id not in self.learners:
            raise ValueError(f"Learner {learner_id} not found")

        learner = self.learners[learner_id]
        current_skills = learner.current_snapshot.skills_demonstrated

        opportunities = []

        for skill_id, skill in self.skills.items():
            if skill_id not in current_skills:
                # Check if prerequisites are met
                prereqs_met = all(p in current_skills for p in skill.prerequisites)

                if prereqs_met or len(skill.prerequisites) == 0:
                    opportunities.append(
                        {
                            "skill_id": skill_id,
                            "skill_name": skill.name,
                            "category": skill.category,
                            "message": f"Ready to explore: {skill.name}",
                            "why_now": "You have the foundation for this!"
                            if prereqs_met
                            else "Great starting point",
                        }
                    )

        return opportunities[:5]  # Top 5 opportunities

    # =========================================================================
    # DISPLAY / EXPORT
    # =========================================================================

    def get_progress_display(self, learner_id: str) -> Dict[str, Any]:
        """
        Generate a learner-facing progress display.

        CRITICAL: Never includes comparisons to others.
        """
        if learner_id not in self.learners:
            raise ValueError(f"Learner {learner_id} not found")

        learner = self.learners[learner_id]
        delta = self.calculate_mastery_delta(learner_id)
        trajectory = self.calculate_trajectory(learner_id)
        opportunities = self.get_growth_opportunities(learner_id)

        # Count completed modules
        completed_modules = sum(
            1
            for status in learner.module_progress.values()
            if status in [ModuleStatus.COMPLETED, ModuleStatus.MASTERED]
        )

        return {
            "learner_id": learner_id,
            "headline": delta.summary_message,
            "stats": {
                "skills_unlocked": len(learner.current_snapshot.skills_demonstrated),
                "modules_completed": completed_modules,
                "checkpoints_passed": len(learner.current_snapshot.checkpoints_passed),
                "trajectory": trajectory.value,
            },
            "recent_gains": {
                "new_skills": [self.skills[s].name for s in delta.new_skills if s in self.skills],
                "new_modules": delta.new_modules,
            },
            "growth_opportunities": opportunities,
            "encouragement": self._get_encouragement(trajectory),
            # Explicitly NOT included:
            # - Rank
            # - Percentile
            # - Comparison to others
            # - "Deficiencies" or "weaknesses"
        }

    def _get_encouragement(self, trajectory: Trajectory) -> str:
        """Generate trajectory-appropriate encouragement."""
        messages = {
            Trajectory.ACCELERATING: "You're on fire! Keep the momentum going.",
            Trajectory.STEADY: "Consistent progress is powerful progress.",
            Trajectory.PLATEAUED: "Plateaus are often where deep learning happens. Keep exploring.",
            Trajectory.EXPLORING: "Exploration is the first step to mastery. Enjoy the journey!",
        }
        return messages.get(trajectory, "Keep going!")

    def export_learner_profile(self, learner_id: str, filepath: str) -> str:
        """Export a learner's profile to JSON."""
        if learner_id not in self.learners:
            raise ValueError(f"Learner {learner_id} not found")

        profile = self.learners[learner_id]
        display = self.get_progress_display(learner_id)

        export_data = {
            "profile": profile.to_dict(),
            "display": display,
            "exported_at": datetime.now().isoformat(),
        }

        with open(filepath, "w", encoding="utf-8") as f:
            json.dump(export_data, f, indent=2, default=str)

        return filepath


# =============================================================================
# EXAMPLE JSON STRUCTURES
# =============================================================================

EXAMPLE_LEARNER_PROFILE = {
    "id": "learner_abc123",
    "created_at": "2024-01-15T10:00:00",
    "baseline_snapshot": {
        "captured_at": "2024-01-15T10:00:00",
        "skills_demonstrated": [],
        "concepts_understood": [],
        "modules_completed": [],
        "checkpoints_passed": [],
        "confidence_areas": [],
        "growth_areas": ["Everything is a growth area - and that's exciting!"],
    },
    "current_snapshot": {
        "captured_at": "2024-02-20T15:30:00",
        "skills_demonstrated": [
            "skill_three_lenses",
            "skill_pii_identification",
            "skill_data_dictionary",
        ],
        "concepts_understood": ["context_matters", "governance_first", "self_relative_growth"],
        "modules_completed": ["week_0_concepts", "week_1_fundamentals"],
        "checkpoints_passed": ["checkpoint_0", "checkpoint_1"],
        "confidence_areas": ["Understanding the three lenses", "Creating data dictionaries"],
        "growth_areas": ["Algorithm implementation", "Graph construction"],
    },
    "module_progress": {
        "week_0_concepts": "completed",
        "week_1_fundamentals": "completed",
        "week_2_structures": "in_progress",
        "week_3_algorithms": "not_started",
    },
    "trajectory": "steady",
    "role_context": "data_analyst",
    "org_context": "education_nonprofit",
}

EXAMPLE_PROGRESS_DISPLAY = {
    "learner_id": "learner_abc123",
    "headline": "Solid progress! You've unlocked 6 new capabilities since you began.",
    "stats": {
        "skills_unlocked": 3,
        "modules_completed": 2,
        "checkpoints_passed": 2,
        "trajectory": "steady",
    },
    "recent_gains": {
        "new_skills": [
            "Understanding the Three Lenses",
            "PII Identification",
            "Data Dictionary Creation",
        ],
        "new_modules": ["week_0_concepts", "week_1_fundamentals"],
    },
    "growth_opportunities": [
        {
            "skill_id": "skill_schema_design",
            "skill_name": "Schema Design",
            "category": "structures",
            "message": "Ready to explore: Schema Design",
            "why_now": "You have the foundation for this!",
        },
        {
            "skill_id": "skill_governance_rules",
            "skill_name": "Governance Rule Writing",
            "category": "fundamentals",
            "message": "Ready to explore: Governance Rule Writing",
            "why_now": "You have the foundation for this!",
        },
    ],
    "encouragement": "Consistent progress is powerful progress.",
}


# =============================================================================
# MAIN - Demo
# =============================================================================


def main():
    """Demonstrate the Progression Tracker."""
    print("=" * 60)
    print("  TEACHER PROGRESSION TRACKER - Demo")
    print("=" * 60)

    # Initialize tracker
    tracker = ProgressionTracker()
    tracker.load_core_curriculum()

    # Enroll a learner
    print("\n1. Enrolling new learner...")
    profile = tracker.enroll_learner(
        learner_id="demo_learner_001", role_context="teacher", org_context="middle_school"
    )
    print(f"   ✓ Enrolled: {profile.id}")

    # Simulate progress
    print("\n2. Simulating progress...")
    tracker.record_skill_demonstration("demo_learner_001", "skill_three_lenses")
    tracker.record_skill_demonstration("demo_learner_001", "skill_pii_identification")
    print("   ✓ Recorded 2 skill demonstrations")

    # Get progress display
    print("\n3. Getting progress display...")
    display = tracker.get_progress_display("demo_learner_001")

    print(f"\n   📊 PROGRESS REPORT")
    print(f"   {'='*40}")
    print(f"   {display['headline']}")
    print(f"\n   Stats:")
    print(f"   • Skills unlocked: {display['stats']['skills_unlocked']}")
    print(f"   • Trajectory: {display['stats']['trajectory']}")

    print(f"\n   Growth Opportunities:")
    for opp in display["growth_opportunities"][:3]:
        print(f"   • {opp['message']}")

    print(f"\n   💪 {display['encouragement']}")

    # Export example JSON
    print("\n4. Exporting example structures...")

    output_dir = Path("curriculum")
    output_dir.mkdir(exist_ok=True)

    with open(output_dir / "example_learner_profile.json", "w") as f:
        json.dump(EXAMPLE_LEARNER_PROFILE, f, indent=2)

    with open(output_dir / "example_progress_display.json", "w") as f:
        json.dump(EXAMPLE_PROGRESS_DISPLAY, f, indent=2)

    print("   ✓ Exported to curriculum/example_*.json")

    print("\n" + "=" * 60)
    print("  Remember: Growth is measured against yourself, not others.")
    print("=" * 60)


if __name__ == "__main__":
    main()
