#!/usr/bin/env python3
"""
COSURVIVAL DATA MODELS
======================
Core data structures for the three pillars of Cosurvival:
- TRIBE: Social network and organizational relationships
- TEACHER: Learning pathways and educational content
- RECONSUMERALIZATION: Ethical value exchange tracking

These models use dataclasses for clarity and Pydantic for validation.
"""

from dataclasses import dataclass, field
from typing import Dict, List, Optional, Set, Any
from datetime import datetime
from enum import Enum
import json


# =============================================================================
# ENUMS
# =============================================================================


class EthicsGrade(Enum):
    """Ethics rating grades for providers and consumers."""

    A = "A"  # Exceptional - Leading ethical practices
    B = "B"  # Good - Meets high standards
    C = "C"  # Satisfactory - Room for improvement
    D = "D"  # Needs Improvement - Significant gaps
    F = "F"  # Failing - Major ethical concerns


class ActivityType(Enum):
    """Types of activities in the system."""

    CREATE = "create"
    READ = "read"
    UPDATE = "update"
    DELETE = "delete"
    SHARE = "share"
    PERMISSION_GRANT = "permission_grant"
    PERMISSION_REVOKE = "permission_revoke"
    LOGIN = "login"
    LOGOUT = "logout"
    COLLABORATION = "collaboration"
    OTHER = "other"


class RelationshipType(Enum):
    """Types of relationships between entities."""

    COLLABORATION = "collaboration"
    MEMBERSHIP = "membership"
    OWNERSHIP = "ownership"
    MENTORSHIP = "mentorship"
    PROVIDER_CONSUMER = "provider_consumer"
    HIERARCHICAL = "hierarchical"


class LearningStatus(Enum):
    """Status of learning progress."""

    NOT_STARTED = "not_started"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    MASTERED = "mastered"


# =============================================================================
# TRIBE MODELS - Social Network Layer
# =============================================================================


@dataclass
class TribeUser:
    """Represents a user in the TRIBE network."""

    id: str
    name: str
    email: str = ""
    company_id: str = ""
    roles: List[str] = field(default_factory=list)
    groups: List[str] = field(default_factory=list)
    connections: List[str] = field(default_factory=list)
    activity_count: int = 0
    skills: Set[str] = field(default_factory=set)
    mentors: List[str] = field(default_factory=list)
    mentees: List[str] = field(default_factory=list)
    joined_at: Optional[datetime] = None

    def to_dict(self) -> Dict[str, Any]:
        return {
            "id": self.id,
            "name": self.name,
            "email": self.email,
            "company_id": self.company_id,
            "roles": self.roles,
            "groups": self.groups,
            "connections": self.connections,
            "activity_count": self.activity_count,
            "skills": list(self.skills),
            "mentors": self.mentors,
            "mentees": self.mentees,
            "joined_at": self.joined_at.isoformat() if self.joined_at else None,
        }


@dataclass
class TribeCompany:
    """Represents a company/organization in the TRIBE network."""

    id: str
    name: str
    users: List[str] = field(default_factory=list)
    groups: List[str] = field(default_factory=list)
    providers: List[str] = field(default_factory=list)
    activity_count: int = 0
    industry: str = ""
    size: str = ""  # small, medium, large, enterprise
    collaboration_score: float = 0.0
    ethics_grade: EthicsGrade = EthicsGrade.C

    def to_dict(self) -> Dict[str, Any]:
        return {
            "id": self.id,
            "name": self.name,
            "users": self.users,
            "groups": self.groups,
            "providers": self.providers,
            "activity_count": self.activity_count,
            "industry": self.industry,
            "size": self.size,
            "collaboration_score": self.collaboration_score,
            "ethics_grade": self.ethics_grade.value,
        }


@dataclass
class TribeGroup:
    """Represents a group/team in the TRIBE network."""

    id: str
    name: str
    company_id: str = ""
    members: List[str] = field(default_factory=list)
    activity_count: int = 0
    purpose: str = ""
    skills: Set[str] = field(default_factory=set)

    def to_dict(self) -> Dict[str, Any]:
        return {
            "id": self.id,
            "name": self.name,
            "company_id": self.company_id,
            "members": self.members,
            "activity_count": self.activity_count,
            "purpose": self.purpose,
            "skills": list(self.skills),
        }


@dataclass
class TribeRelationship:
    """Represents a relationship between entities in TRIBE."""

    source_id: str
    target_id: str
    relationship_type: RelationshipType
    weight: float = 1.0
    created_at: Optional[datetime] = None
    metadata: Dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        return {
            "source": self.source_id,
            "target": self.target_id,
            "type": self.relationship_type.value,
            "weight": self.weight,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "metadata": self.metadata,
        }


@dataclass
class TribeCommunity:
    """Represents a detected community in the TRIBE network."""

    id: int
    members: List[str] = field(default_factory=list)
    name: str = ""
    cohesion_score: float = 0.0
    key_connectors: List[str] = field(default_factory=list)
    common_skills: Set[str] = field(default_factory=set)

    def to_dict(self) -> Dict[str, Any]:
        return {
            "id": self.id,
            "members": self.members,
            "name": self.name,
            "cohesion_score": self.cohesion_score,
            "key_connectors": self.key_connectors,
            "common_skills": list(self.common_skills),
        }


# =============================================================================
# TEACHER MODELS - Learning Pathway Layer
# =============================================================================


@dataclass
class TeacherSkill:
    """Represents a skill that can be learned."""

    id: str
    name: str
    category: str = ""
    description: str = ""
    prerequisites: List[str] = field(default_factory=list)
    related_providers: List[str] = field(default_factory=list)
    difficulty_level: int = 1  # 1-5
    estimated_hours: float = 0.0

    def to_dict(self) -> Dict[str, Any]:
        return {
            "id": self.id,
            "name": self.name,
            "category": self.category,
            "description": self.description,
            "prerequisites": self.prerequisites,
            "related_providers": self.related_providers,
            "difficulty_level": self.difficulty_level,
            "estimated_hours": self.estimated_hours,
        }


@dataclass
class TeacherRole:
    """Represents a role with associated learning requirements."""

    id: str
    name: str
    required_skills: List[str] = field(default_factory=list)
    technology_stack: List[str] = field(default_factory=list)
    typical_activities: Dict[str, int] = field(default_factory=dict)
    user_count: int = 0
    career_paths: List[str] = field(default_factory=list)  # IDs of next roles

    def to_dict(self) -> Dict[str, Any]:
        return {
            "id": self.id,
            "name": self.name,
            "required_skills": self.required_skills,
            "technology_stack": self.technology_stack,
            "typical_activities": self.typical_activities,
            "user_count": self.user_count,
            "career_paths": self.career_paths,
        }


@dataclass
class TeacherProgression:
    """Represents a learning progression/state transition."""

    from_state: str
    to_state: str
    frequency: int = 0
    average_duration_days: float = 0.0
    success_rate: float = 0.0
    recommended_resources: List[str] = field(default_factory=list)

    def to_dict(self) -> Dict[str, Any]:
        return {
            "from": self.from_state,
            "to": self.to_state,
            "frequency": self.frequency,
            "average_duration_days": self.average_duration_days,
            "success_rate": self.success_rate,
            "recommended_resources": self.recommended_resources,
        }


@dataclass
class TeacherLearningPath:
    """Represents a complete learning path for a role."""

    id: str
    name: str
    target_role_id: str
    modules: List["TeacherModule"] = field(default_factory=list)
    estimated_duration_days: int = 0
    difficulty: str = "intermediate"  # beginner, intermediate, advanced
    completion_rate: float = 0.0

    def to_dict(self) -> Dict[str, Any]:
        return {
            "id": self.id,
            "name": self.name,
            "target_role_id": self.target_role_id,
            "modules": [m.to_dict() for m in self.modules],
            "estimated_duration_days": self.estimated_duration_days,
            "difficulty": self.difficulty,
            "completion_rate": self.completion_rate,
        }


@dataclass
class TeacherModule:
    """Represents a learning module within a path."""

    id: str
    title: str
    description: str = ""
    skills_taught: List[str] = field(default_factory=list)
    provider_id: Optional[str] = None
    content_type: str = "interactive"  # video, interactive, reading, practice
    duration_minutes: int = 30
    order: int = 0

    def to_dict(self) -> Dict[str, Any]:
        return {
            "id": self.id,
            "title": self.title,
            "description": self.description,
            "skills_taught": self.skills_taught,
            "provider_id": self.provider_id,
            "content_type": self.content_type,
            "duration_minutes": self.duration_minutes,
            "order": self.order,
        }


@dataclass
class TeacherRecommendation:
    """Represents a personalized learning recommendation."""

    user_id: str
    recommended_skills: List[str] = field(default_factory=list)
    recommended_modules: List[str] = field(default_factory=list)
    recommended_mentors: List[str] = field(default_factory=list)
    reason: str = ""
    priority: str = "medium"  # low, medium, high, critical
    generated_at: datetime = field(default_factory=datetime.now)

    def to_dict(self) -> Dict[str, Any]:
        return {
            "user_id": self.user_id,
            "recommended_skills": self.recommended_skills,
            "recommended_modules": self.recommended_modules,
            "recommended_mentors": self.recommended_mentors,
            "reason": self.reason,
            "priority": self.priority,
            "generated_at": self.generated_at.isoformat(),
        }


# =============================================================================
# RECONSUMERALIZATION MODELS - Value Exchange Layer
# =============================================================================


@dataclass
class ReconProvider:
    """Represents a provider/supplier in the value exchange network."""

    id: str
    name: str
    services: List[str] = field(default_factory=list)
    customer_count: int = 0
    user_count: int = 0
    activity_volume: int = 0
    error_rate: float = 0.0
    reliability_score: float = 1.0
    transparency_score: float = 1.0
    ethics_grade: EthicsGrade = EthicsGrade.C
    pricing_model: str = ""
    data_practices: str = ""
    sustainability_score: float = 0.0

    def to_dict(self) -> Dict[str, Any]:
        return {
            "id": self.id,
            "name": self.name,
            "services": self.services,
            "customer_count": self.customer_count,
            "user_count": self.user_count,
            "activity_volume": self.activity_volume,
            "error_rate": self.error_rate,
            "reliability_score": self.reliability_score,
            "transparency_score": self.transparency_score,
            "ethics_grade": self.ethics_grade.value,
            "pricing_model": self.pricing_model,
            "data_practices": self.data_practices,
            "sustainability_score": self.sustainability_score,
        }


@dataclass
class ReconConsumer:
    """Represents a consumer (company/user) in the value exchange network."""

    id: str
    name: str
    entity_type: str = "company"  # company, individual, group
    providers_used: List[str] = field(default_factory=list)
    total_users: int = 0
    activity_volume: int = 0
    technology_adoption_score: float = 0.0
    collaboration_score: float = 0.0
    transparency_score: float = 0.0
    ethics_grade: EthicsGrade = EthicsGrade.C
    values: List[str] = field(default_factory=list)

    def to_dict(self) -> Dict[str, Any]:
        return {
            "id": self.id,
            "name": self.name,
            "entity_type": self.entity_type,
            "providers_used": self.providers_used,
            "total_users": self.total_users,
            "activity_volume": self.activity_volume,
            "technology_adoption_score": self.technology_adoption_score,
            "collaboration_score": self.collaboration_score,
            "transparency_score": self.transparency_score,
            "ethics_grade": self.ethics_grade.value,
            "values": self.values,
        }


@dataclass
class ReconValueFlow:
    """Represents a value exchange between provider and consumer."""

    id: str
    from_provider_id: str
    to_consumer_id: str
    volume: int = 0
    quality_score: float = 1.0
    value_score: float = 0.0
    reciprocity: bool = False  # Is there mutual value exchange?
    ethical_compliance: float = 1.0
    period_start: Optional[datetime] = None
    period_end: Optional[datetime] = None

    def to_dict(self) -> Dict[str, Any]:
        return {
            "id": self.id,
            "from_provider": self.from_provider_id,
            "to_consumer": self.to_consumer_id,
            "volume": self.volume,
            "quality": self.quality_score,
            "value_score": self.value_score,
            "reciprocity": self.reciprocity,
            "ethical_compliance": self.ethical_compliance,
            "period_start": self.period_start.isoformat() if self.period_start else None,
            "period_end": self.period_end.isoformat() if self.period_end else None,
        }


@dataclass
class ReconEthicsScore:
    """Comprehensive ethics score for an entity."""

    entity_id: str
    entity_type: str  # provider, consumer
    reliability: float = 0.0
    transparency: float = 0.0
    sustainability: float = 0.0
    fairness: float = 0.0
    data_ethics: float = 0.0
    composite_score: float = 0.0
    grade: EthicsGrade = EthicsGrade.C
    calculated_at: datetime = field(default_factory=datetime.now)
    factors: Dict[str, float] = field(default_factory=dict)

    def calculate_grade(self) -> EthicsGrade:
        """Calculate ethics grade from composite score."""
        if self.composite_score >= 0.9:
            return EthicsGrade.A
        elif self.composite_score >= 0.8:
            return EthicsGrade.B
        elif self.composite_score >= 0.7:
            return EthicsGrade.C
        elif self.composite_score >= 0.6:
            return EthicsGrade.D
        return EthicsGrade.F

    def to_dict(self) -> Dict[str, Any]:
        return {
            "entity_id": self.entity_id,
            "entity_type": self.entity_type,
            "reliability": self.reliability,
            "transparency": self.transparency,
            "sustainability": self.sustainability,
            "fairness": self.fairness,
            "data_ethics": self.data_ethics,
            "composite_score": self.composite_score,
            "grade": self.grade.value,
            "calculated_at": self.calculated_at.isoformat(),
            "factors": self.factors,
        }


# =============================================================================
# INTEGRATION MODELS - Cross-System Connections
# =============================================================================


@dataclass
class IntegrationInsight:
    """Represents an insight derived from cross-system analysis."""

    id: str
    insight_type: str  # mentorship, skill_gap, ethics_concern, opportunity
    title: str
    description: str
    affected_entities: List[str] = field(default_factory=list)
    recommended_actions: List[str] = field(default_factory=list)
    priority: str = "medium"
    confidence: float = 0.0
    source_systems: List[str] = field(default_factory=list)  # tribe, teacher, recon

    def to_dict(self) -> Dict[str, Any]:
        return {
            "id": self.id,
            "type": self.insight_type,
            "title": self.title,
            "description": self.description,
            "affected_entities": self.affected_entities,
            "recommended_actions": self.recommended_actions,
            "priority": self.priority,
            "confidence": self.confidence,
            "source_systems": self.source_systems,
        }


@dataclass
class TripleBalanceDecision:
    """
    Represents a decision evaluated through Triple Balance governance:
    - AI Logic: Data-driven analysis
    - 10th Man: Dissent and alternative viewpoints
    - Witch: Intuition and pattern recognition beyond data
    """

    id: str
    decision_context: str

    # AI Logic perspective
    ai_analysis: str = ""
    ai_confidence: float = 0.0
    ai_recommendation: str = ""

    # 10th Man perspective
    dissent_raised: str = ""
    alternative_interpretation: str = ""
    blind_spots_identified: List[str] = field(default_factory=list)

    # Witch perspective
    intuitive_concerns: str = ""
    pattern_insights: str = ""
    emotional_intelligence: str = ""

    # Final synthesis
    synthesized_decision: str = ""
    action_items: List[str] = field(default_factory=list)
    created_at: datetime = field(default_factory=datetime.now)

    def to_dict(self) -> Dict[str, Any]:
        return {
            "id": self.id,
            "context": self.decision_context,
            "ai": {
                "analysis": self.ai_analysis,
                "confidence": self.ai_confidence,
                "recommendation": self.ai_recommendation,
            },
            "tenth_man": {
                "dissent": self.dissent_raised,
                "alternative": self.alternative_interpretation,
                "blind_spots": self.blind_spots_identified,
            },
            "witch": {
                "concerns": self.intuitive_concerns,
                "patterns": self.pattern_insights,
                "emotional": self.emotional_intelligence,
            },
            "synthesis": {"decision": self.synthesized_decision, "actions": self.action_items},
            "created_at": self.created_at.isoformat(),
        }


# =============================================================================
# AGGREGATE CONTAINERS
# =============================================================================


@dataclass
class TribeData:
    """Container for all TRIBE system data."""

    users: Dict[str, TribeUser] = field(default_factory=dict)
    companies: Dict[str, TribeCompany] = field(default_factory=dict)
    groups: Dict[str, TribeGroup] = field(default_factory=dict)
    relationships: List[TribeRelationship] = field(default_factory=list)
    communities: List[TribeCommunity] = field(default_factory=list)

    def to_dict(self) -> Dict[str, Any]:
        return {
            "users": {k: v.to_dict() for k, v in self.users.items()},
            "companies": {k: v.to_dict() for k, v in self.companies.items()},
            "groups": {k: v.to_dict() for k, v in self.groups.items()},
            "relationships": [r.to_dict() for r in self.relationships],
            "communities": [c.to_dict() for c in self.communities],
        }


@dataclass
class TeacherData:
    """Container for all TEACHER system data."""

    roles: Dict[str, TeacherRole] = field(default_factory=dict)
    skills: Dict[str, TeacherSkill] = field(default_factory=dict)
    progressions: List[TeacherProgression] = field(default_factory=list)
    learning_paths: Dict[str, TeacherLearningPath] = field(default_factory=dict)
    recommendations: List[TeacherRecommendation] = field(default_factory=list)

    def to_dict(self) -> Dict[str, Any]:
        return {
            "roles": {k: v.to_dict() for k, v in self.roles.items()},
            "skills": {k: v.to_dict() for k, v in self.skills.items()},
            "progressions": [p.to_dict() for p in self.progressions],
            "learning_paths": {k: v.to_dict() for k, v in self.learning_paths.items()},
            "recommendations": [r.to_dict() for r in self.recommendations],
        }


@dataclass
class ReconsumeralizationData:
    """Container for all RECONSUMERALIZATION system data."""

    providers: Dict[str, ReconProvider] = field(default_factory=dict)
    consumers: Dict[str, ReconConsumer] = field(default_factory=dict)
    value_flows: List[ReconValueFlow] = field(default_factory=list)
    ethics_scores: Dict[str, ReconEthicsScore] = field(default_factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        return {
            "providers": {k: v.to_dict() for k, v in self.providers.items()},
            "consumers": {k: v.to_dict() for k, v in self.consumers.items()},
            "value_flows": [f.to_dict() for f in self.value_flows],
            "ethics_scores": {k: v.to_dict() for k, v in self.ethics_scores.items()},
        }


@dataclass
class AntiPatternSignal:
    """
    A complementary pattern that reveals what's NOT happening.
    
    Like Dirac's antiparticles, these reveal the "negative energy" side
    of our analysis - gaps, absences, inverse relationships.
    
    CURRICULUM: Week 0, Activity 0.5 - Negative Patterns Are Not Nonsense
    Week 1, Activity 1.3 - Multi-Component Wave Functions
    See: curriculum/vision/chapters/DIrac_ANTIPATTERNS_APPLICATION.md
    """

    id: str
    domain: str  # TRIBE, TEACHER, RECON, etc.
    anti_pattern_type: str  # e.g., "collaboration_gap", "skill_absence"
    complementary_to: str  # ID of the pattern this complements
    strength: str  # weak, moderate, strong, critical
    description: str
    detected_at: str
    confidence: float  # 0.0-1.0

    # What's missing or inverse
    gap_description: str
    absence_evidence: List[str] = field(default_factory=list)
    inverse_relationship: Optional[Dict[str, Any]] = None

    # Temporal direction
    temporal_direction: str = "forwards"  # "forwards" (predictive) or "backwards" (retrospective)

    # Connection to "positive" pattern
    pattern_anti_pattern_annihilation: Optional[Dict[str, Any]] = None
    # When pattern and anti-pattern meet, what truth is revealed?

    # Supporting evidence
    evidence: List[str] = field(default_factory=list)
    data_points: List[Dict[str, Any]] = field(default_factory=list)

    # Nonjudgmental framing
    framing: str = ""  # How to present this as opportunity, not deficiency

    def to_dict(self) -> Dict[str, Any]:
        return {
            "id": self.id,
            "domain": self.domain,
            "anti_pattern_type": self.anti_pattern_type,
            "complementary_to": self.complementary_to,
            "strength": self.strength,
            "description": self.description,
            "detected_at": self.detected_at,
            "confidence": self.confidence,
            "gap_description": self.gap_description,
            "absence_evidence": self.absence_evidence,
            "inverse_relationship": self.inverse_relationship,
            "temporal_direction": self.temporal_direction,
            "pattern_anti_pattern_annihilation": self.pattern_anti_pattern_annihilation,
            "evidence": self.evidence,
            "data_points": self.data_points[:5],  # Limit for display
            "framing": self.framing,
        }


@dataclass
class PatternAnnihilation:
    """
    Insight revealed when pattern and anti-pattern meet.
    
    Like particle-antiparticle annihilation producing energy,
    pattern-anti-pattern annihilation produces insight.
    
    CURRICULUM: Week 1, Activity 1.3 - Multi-Component Wave Functions
    See: curriculum/vision/chapters/DIrac_ANTIPATTERNS_APPLICATION.md
    """

    id: str
    pattern_id: str
    anti_pattern_id: str
    insight: str
    revealed_truth: str
    recommendation: Optional[str] = None
    confidence: float = 0.0
    detected_at: str = ""

    def to_dict(self) -> Dict[str, Any]:
        return {
            "id": self.id,
            "pattern_id": self.pattern_id,
            "anti_pattern_id": self.anti_pattern_id,
            "insight": self.insight,
            "revealed_truth": self.revealed_truth,
            "recommendation": self.recommendation,
            "confidence": self.confidence,
            "detected_at": self.detected_at,
        }


@dataclass
class CosurvivalData:
    """Complete Cosurvival system data container."""

    tribe: TribeData = field(default_factory=TribeData)
    teacher: TeacherData = field(default_factory=TeacherData)
    reconsumeralization: ReconsumeralizationData = field(default_factory=ReconsumeralizationData)
    insights: List[IntegrationInsight] = field(default_factory=list)
    decisions: List[TripleBalanceDecision] = field(default_factory=list)
    metadata: Dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        return {
            "tribe": self.tribe.to_dict(),
            "teacher": self.teacher.to_dict(),
            "reconsumeralization": self.reconsumeralization.to_dict(),
            "insights": [i.to_dict() for i in self.insights],
            "decisions": [d.to_dict() for d in self.decisions],
            "metadata": self.metadata,
        }

    def to_json(self, filepath: str) -> str:
        """Export to JSON file."""
        with open(filepath, "w", encoding="utf-8") as f:
            json.dump(self.to_dict(), f, indent=2, default=str)
        return filepath
