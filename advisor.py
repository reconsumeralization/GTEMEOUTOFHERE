#!/usr/bin/env python3
"""
COSURVIVAL AI ADVISOR
=====================
Cross-domain pattern recognition and early-warning advisor.

Core Philosophy:
"AI should advise, not control. Support, not surveil. 
Transparent about why, so we can trust without becoming dependent."

This advisor:
- Connects dots across TRIBE, TEACHER, RECON, and life domains
- Surfaces weak signals before they become crises
- Always explains reasoning transparently
- Respects user agency (preferences, overrides)
- Uses nonjudgmental, supportive framing
"""

"""
COSURVIVAL AI ADVISOR
=====================
Cross-domain pattern recognition and early-warning advisor.

Core Philosophy:
"AI should advise, not control. Support, not surveil. 
Transparent about why, so we can trust without becoming dependent."

This advisor:
- Connects dots across TRIBE, TEACHER, RECON, and life domains
- Surfaces weak signals before they become crises
- Always explains reasoning transparently
- Respects user agency (preferences, overrides)
- Uses nonjudgmental, supportive framing
"""

# Standard library imports
from collections import defaultdict  # noqa: E402
from dataclasses import dataclass, field  # noqa: E402
from datetime import datetime  # noqa: E402
from enum import Enum  # noqa: E402
from typing import Dict, List, Optional, Any, Set  # noqa: E402


# =============================================================================
# ENUMS
# =============================================================================


class SignalStrength(Enum):
    """Strength of an early warning signal."""

    WEAK = "weak"  # Emerging pattern, worth monitoring
    MODERATE = "moderate"  # Clear pattern, action recommended
    STRONG = "strong"  # Urgent attention needed
    CRITICAL = "critical"  # Immediate action required


class Domain(Enum):
    """Life domains the advisor can connect."""

    TRIBE = "tribe"  # Relationships, community, collaboration
    TEACHER = "teacher"  # Learning, skill development, growth
    RECON = "recon"  # Value exchange, provider relationships
    FINANCIAL = "financial"  # Budget, spending patterns, resource stress
    HEALTH = "health"  # Wellbeing indicators, activity patterns
    TIME = "time"  # Time management, workload, balance
    VALUES = "values"  # Spiritual, ethical, meaning, purpose (spiritual mentor perspective)
    RELATIONAL = "relational"  # Personal relationships, family, social


class RecommendationType(Enum):
    """Types of recommendations the advisor can make."""

    EARLY_WARNING = "early_warning"
    OPPORTUNITY = "opportunity"
    CONNECTION = "connection"  # Connecting patterns across domains
    RESOURCE = "resource"  # Suggesting helpful resources
    REFLECTION = "reflection"  # Prompting self-reflection
    ACTION = "action"  # Specific action to take


# =============================================================================
# CORE DATA MODELS
# =============================================================================


@dataclass
class PatternSignal:
    """
    A detected pattern that may indicate an opportunity or risk.

    Nonjudgmental framing: patterns are observations, not evaluations.
    """

    id: str
    domain: Domain
    signal_type: str  # e.g., "declining_collaboration", "skill_gap_emerging"
    strength: SignalStrength
    description: str
    detected_at: str
    confidence: float  # 0.0-1.0

    # Supporting evidence (transparent reasoning)
    evidence: List[str] = field(default_factory=list)
    data_points: List[Dict[str, Any]] = field(default_factory=list)

    # Cross-domain connections
    related_signals: List[str] = field(default_factory=list)  # IDs of related signals

    # Nonjudgmental framing
    framing: str = ""  # How to present this without judgment

    def to_dict(self) -> Dict[str, Any]:
        return {
            "id": self.id,
            "domain": self.domain.value,
            "signal_type": self.signal_type,
            "strength": self.strength.value,
            "description": self.description,
            "detected_at": self.detected_at,
            "confidence": self.confidence,
            "evidence": self.evidence,
            "data_points": self.data_points[:5],  # Limit for display
            "related_signals": self.related_signals,
            "framing": self.framing,
        }


@dataclass
class Recommendation:
    """
    A recommendation from the advisor.

    Always includes transparent reasoning and respects user agency.
    """

    id: str
    type: RecommendationType
    title: str
    description: str
    priority: str  # low, medium, high, urgent

    # Transparent reasoning
    reasoning: Dict[str, Any] = field(default_factory=dict)
    """
    Structure:
    {
        "why_now": "Why this matters now",
        "evidence": ["Supporting data point 1", "Supporting data point 2"],
        "cross_domain_connections": ["Related pattern in TRIBE", "Related pattern in TEACHER"],
        "confidence": 0.85,
        "alternatives_considered": ["Alternative interpretation 1", "Alternative interpretation 2"]
    }
    """

    # Agency controls
    user_can_override: bool = True
    user_can_dismiss: bool = True
    user_can_customize: bool = True

    # Suggested actions (not commands!)
    suggested_actions: List[str] = field(default_factory=list)

    # Resources
    helpful_resources: List[Dict[str, str]] = field(default_factory=list)
    """
    Structure:
    [
        {"type": "article", "title": "...", "url": "..."},
        {"type": "person", "name": "...", "reason": "..."},
        {"type": "tool", "name": "...", "description": "..."}
    ]
    """

    # Nonjudgmental framing
    supportive_message: str = ""

    generated_at: str = ""

    def to_dict(self) -> Dict[str, Any]:
        return {
            "id": self.id,
            "type": self.type.value,
            "title": self.title,
            "description": self.description,
            "priority": self.priority,
            "reasoning": self.reasoning,
            "user_can_override": self.user_can_override,
            "user_can_dismiss": self.user_can_dismiss,
            "user_can_customize": self.user_can_customize,
            "suggested_actions": self.suggested_actions,
            "helpful_resources": self.helpful_resources,
            "supportive_message": self.supportive_message,
            "generated_at": self.generated_at,
        }


@dataclass
class UserPreferences:
    """
    User preferences for advisor behavior.

    This is how users maintain agency - they control what the advisor sees,
    how it communicates, and what it focuses on.
    """

    user_id: str

    # Communication preferences
    communication_style: str = "supportive"  # supportive, direct, detailed, minimal
    notification_frequency: str = "moderate"  # minimal, moderate, frequent
    preferred_domains: List[Domain] = field(default_factory=list)  # Empty = all domains

    # Privacy boundaries
    domains_to_exclude: List[Domain] = field(default_factory=list)
    sensitive_topics: List[str] = field(default_factory=list)

    # Recommendation preferences
    min_confidence_threshold: float = 0.6  # Only show recommendations above this
    max_recommendations_per_day: int = 5

    # Overrides (user has said "don't show me X")
    dismissed_patterns: Set[str] = field(default_factory=set)
    dismissed_recommendations: Set[str] = field(default_factory=set)

    # Customization
    custom_framing: Dict[str, str] = field(default_factory=dict)
    """
    Structure:
    {
        "skill_gap": "I prefer to think of these as 'exploration opportunities'",
        "declining_activity": "I want to know about this, but frame it as 'shifting focus'"
    }
    """

    # Values and goals (for personalization)
    stated_values: List[str] = field(default_factory=list)
    current_goals: List[str] = field(default_factory=list)

    def to_dict(self) -> Dict[str, Any]:
        return {
            "user_id": self.user_id,
            "communication_style": self.communication_style,
            "notification_frequency": self.notification_frequency,
            "preferred_domains": [d.value for d in self.preferred_domains],
            "domains_to_exclude": [d.value for d in self.domains_to_exclude],
            "sensitive_topics": self.sensitive_topics,
            "min_confidence_threshold": self.min_confidence_threshold,
            "max_recommendations_per_day": self.max_recommendations_per_day,
            "dismissed_patterns": list(self.dismissed_patterns),
            "dismissed_recommendations": list(self.dismissed_recommendations),
            "custom_framing": self.custom_framing,
            "stated_values": self.stated_values,
            "current_goals": self.current_goals,
        }


@dataclass
class CrossDomainInsight:
    """
    An insight that connects patterns across multiple domains.

    This is the advisor's superpower: seeing connections humans might miss.
    """

    id: str
    title: str
    description: str

    # Which domains are connected
    domains_involved: List[Domain]

    # The connection
    connection_explanation: str

    # Why this matters
    significance: str

    # Supporting evidence
    evidence: Dict[Domain, List[str]] = field(default_factory=dict)
    """
    Structure:
    {
        Domain.TRIBE: ["Evidence from TRIBE domain"],
        Domain.TEACHER: ["Evidence from TEACHER domain"]
    }
    """

    # Suggested reflection or action
    reflection_prompt: str = ""
    suggested_action: str = ""

    confidence: float = 0.0
    detected_at: str = ""

    def to_dict(self) -> Dict[str, Any]:
        return {
            "id": self.id,
            "title": self.title,
            "description": self.description,
            "domains_involved": [d.value for d in self.domains_involved],
            "connection_explanation": self.connection_explanation,
            "evidence": {k.value: v for k, v in self.evidence.items()},
            "significance": self.significance,
            "reflection_prompt": self.reflection_prompt,
            "suggested_action": self.suggested_action,
            "confidence": self.confidence,
            "detected_at": self.detected_at,
        }


# =============================================================================
# AI ADVISOR SERVICE
# =============================================================================


class CosurvivalAdvisor:
    """
    Cross-domain AI advisor that connects patterns and provides early warnings.

    Key principles:
    1. Advise, don't control
    2. Support, don't surveil
    3. Transparent reasoning always
    4. Respect user agency
    5. Nonjudgmental framing
    """

    def __init__(self) -> None:
        self.user_preferences: Dict[str, UserPreferences] = {}
        self.active_signals: Dict[str, PatternSignal] = {}
        self.recommendations_history: Dict[str, List[Recommendation]] = defaultdict(list)
        self.cross_domain_insights: List[CrossDomainInsight] = []

        # Data sources (would be connected to actual systems)
        self.tribe_data: Optional[Dict[str, Any]] = None
        self.teacher_data: Optional[Dict[str, Any]] = None
        self.recon_data: Optional[Dict[str, Any]] = None

    # =========================================================================
    # USER PREFERENCES & AGENCY
    # =========================================================================

    def set_user_preferences(self, user_id: str, preferences: UserPreferences):
        """Set user preferences - this is how users maintain agency."""
        self.user_preferences[user_id] = preferences

    def get_user_preferences(self, user_id: str) -> Optional[UserPreferences]:
        """Get user preferences."""
        return self.user_preferences.get(user_id)

    def user_dismisses_recommendation(self, user_id: str, recommendation_id: str):
        """User dismisses a recommendation - respect their choice."""
        if user_id in self.user_preferences:
            self.user_preferences[user_id].dismissed_recommendations.add(recommendation_id)

    def user_overrides_recommendation(
        self, user_id: str, recommendation_id: str, override_reason: str
    ):
        """User overrides a recommendation - learn from their choice."""
        if user_id in self.user_preferences:
            self.user_preferences[user_id].dismissed_recommendations.add(recommendation_id)
            # In a real system, we'd learn from this override

    # =========================================================================
    # PATTERN DETECTION (Early Warning System)
    # =========================================================================

    def detect_early_warning_signals(
        self, user_id: str, data: Dict[str, Any]
    ) -> List[PatternSignal]:
        """
        Detect weak signals before they become crises.

        This is the advisor's early-warning capability.
        """
        signals = []
        prefs = self.get_user_preferences(user_id)

        # Check TRIBE domain
        if not prefs or Domain.TRIBE not in prefs.domains_to_exclude:
            tribe_signals = self._detect_tribe_signals(user_id, data)
            signals.extend(tribe_signals)

        # Check TEACHER domain
        if not prefs or Domain.TEACHER not in prefs.domains_to_exclude:
            teacher_signals = self._detect_teacher_signals(user_id, data)
            signals.extend(teacher_signals)

        # Check RECON domain
        if not prefs or Domain.RECON not in prefs.domains_to_exclude:
            recon_signals = self._detect_recon_signals(user_id, data)
            signals.extend(recon_signals)

        # Check FINANCIAL domain
        if not prefs or Domain.FINANCIAL not in prefs.domains_to_exclude:
            financial_signals = self._detect_financial_signals(user_id, data)
            signals.extend(financial_signals)

        # Check HEALTH domain
        if not prefs or Domain.HEALTH not in prefs.domains_to_exclude:
            health_signals = self._detect_health_signals(user_id, data)
            signals.extend(health_signals)

        # Check VALUES domain
        if not prefs or Domain.VALUES not in prefs.domains_to_exclude:
            values_signals = self._detect_values_signals(user_id, data)
            signals.extend(values_signals)

        # Filter by user preferences
        if prefs:
            signals = [s for s in signals if s.signal_type not in prefs.dismissed_patterns]
            signals = [s for s in signals if s.confidence >= prefs.min_confidence_threshold]

        # Store active signals
        for signal in signals:
            self.active_signals[signal.id] = signal

        return signals

    def _detect_tribe_signals(self, user_id: str, data: Dict[str, Any]) -> List[PatternSignal]:
        """Detect patterns in TRIBE domain."""
        signals = []

        # Example: Declining collaboration
        if "tribe" in data and "collaboration_trend" in data["tribe"]:
            trend = data["tribe"]["collaboration_trend"]
            if trend.get("direction") == "declining" and trend.get("rate") > 0.2:
                signal = PatternSignal(
                    id=f"tribe_signal_{datetime.now().strftime('%Y%m%d%H%M%S')}",
                    domain=Domain.TRIBE,
                    signal_type="declining_collaboration",
                    strength=SignalStrength.MODERATE
                    if trend.get("rate") < 0.4
                    else SignalStrength.STRONG,
                    description="Collaboration activity has been declining",
                    detected_at=datetime.now().isoformat(),
                    confidence=0.75,
                    evidence=[
                        f"Collaboration score decreased by {trend.get('rate', 0):.1%}",
                        f"Fewer connections in last {trend.get('period', 'period')}",
                    ],
                    framing="This might indicate shifting priorities or changing work patterns. Not necessarily a problem - worth checking in.",
                )
                signals.append(signal)

        return signals

    def _detect_teacher_signals(self, user_id: str, data: Dict[str, Any]) -> List[PatternSignal]:
        """Detect patterns in TEACHER domain."""
        signals = []

        # Example: Skill gap emerging
        if "teacher" in data and "skill_gaps" in data["teacher"]:
            gaps = data["teacher"]["skill_gaps"]
            if len(gaps) > 3:  # Multiple gaps
                signal = PatternSignal(
                    id=f"teacher_signal_{datetime.now().strftime('%Y%m%d%H%M%S')}",
                    domain=Domain.TEACHER,
                    signal_type="skill_gaps_emerging",
                    strength=SignalStrength.WEAK,
                    description="Several skill growth opportunities identified",
                    detected_at=datetime.now().isoformat(),
                    confidence=0.65,
                    evidence=[
                        f"{len(gaps)} skills commonly held by peers in your role",
                        "These are opportunities, not deficiencies",
                    ],
                    framing="These are exciting growth opportunities! Your peers have found these skills valuable.",
                )
                signals.append(signal)

        return signals

    def _detect_recon_signals(self, user_id: str, data: Dict[str, Any]) -> List[PatternSignal]:
        """Detect patterns in RECON domain."""
        signals = []

        # Example: Provider friction
        if "recon" in data and "friction_points" in data["recon"]:
            friction = data["recon"]["friction_points"]
            if len(friction) > 0:
                signal = PatternSignal(
                    id=f"recon_signal_{datetime.now().strftime('%Y%m%d%H%M%S')}",
                    domain=Domain.RECON,
                    signal_type="provider_friction",
                    strength=SignalStrength.MODERATE,
                    description="Friction points detected with providers",
                    detected_at=datetime.now().isoformat(),
                    confidence=0.70,
                    evidence=[
                        f"{len(friction)} friction points identified",
                        "These may indicate opportunities for better tool fit",
                    ],
                    framing="These friction points might indicate it's time to explore alternatives or optimize workflows.",
                )
                signals.append(signal)

        return signals

    def _detect_financial_signals(self, user_id: str, data: Dict[str, Any]) -> List[PatternSignal]:
        """
        Detect patterns in FINANCIAL domain.

        A financial planner sees budget and spending, but won't see learning patterns.
        AI can connect these.
        """
        signals = []

        # Budget stress detection
        if "financial" in data:
            financial = data["financial"]

            # High spending relative to income
            if "spending_stress" in financial:
                stress = financial["spending_stress"]
                if stress.get("level") in ["high", "critical"]:
                    signal = PatternSignal(
                        id=f"financial_signal_{datetime.now().strftime('%Y%m%d%H%M%S')}",
                        domain=Domain.FINANCIAL,
                        signal_type="budget_stress",
                        strength=SignalStrength.STRONG
                        if stress.get("level") == "critical"
                        else SignalStrength.MODERATE,
                        description="Budget stress detected - spending patterns may be causing strain",
                        detected_at=datetime.now().isoformat(),
                        confidence=0.75,
                        evidence=[
                            f"Spending {stress.get('percentage', 0):.0f}% of income",
                            f"Budget status: {stress.get('status', 'unknown')}",
                        ],
                        framing="Financial stress can affect many areas of life. This is an observation, not a judgment about your choices.",
                    )
                    signals.append(signal)

            # Unusual spending patterns
            if "unusual_spending" in financial:
                unusual = financial["unusual_spending"]
                if unusual.get("detected"):
                    signal = PatternSignal(
                        id=f"financial_signal_unusual_{datetime.now().strftime('%Y%m%d%H%M%S')}",
                        domain=Domain.FINANCIAL,
                        signal_type="unusual_spending",
                        strength=SignalStrength.WEAK,
                        description="Unusual spending pattern detected",
                        detected_at=datetime.now().isoformat(),
                        confidence=0.60,
                        evidence=[unusual.get("description", "Unusual pattern")],
                        framing="This might be intentional or might be worth reviewing.",
                    )
                    signals.append(signal)

        return signals

    def _detect_health_signals(self, user_id: str, data: Dict[str, Any]) -> List[PatternSignal]:
        """
        Detect patterns in HEALTH domain.

        A doctor sees health indicators, but won't track household budget stress.
        AI can connect these.
        """
        signals = []

        if "health" in data:
            health = data["health"]

            # Activity decline (could indicate stress, fatigue, health issue)
            if "activity_decline" in health:
                decline = health["activity_decline"]
                if decline.get("rate", 0) > 0.2:
                    signal = PatternSignal(
                        id=f"health_signal_{datetime.now().strftime('%Y%m%d%H%M%S')}",
                        domain=Domain.HEALTH,
                        signal_type="activity_decline",
                        strength=SignalStrength.MODERATE
                        if decline.get("rate", 0) > 0.3
                        else SignalStrength.WEAK,
                        description="Physical activity has been declining",
                        detected_at=datetime.now().isoformat(),
                        confidence=0.70,
                        evidence=[
                            f"Activity decreased by {decline.get('rate', 0):.0%}",
                            f"Period: {decline.get('period', 'recent')}",
                        ],
                        framing="Activity patterns can reflect many things - stress, schedule changes, or health. Worth paying attention to.",
                    )
                    signals.append(signal)

            # Sleep pattern changes
            if "sleep_changes" in health:
                sleep = health["sleep_changes"]
                if sleep.get("detected"):
                    signal = PatternSignal(
                        id=f"health_signal_sleep_{datetime.now().strftime('%Y%m%d%H%M%S')}",
                        domain=Domain.HEALTH,
                        signal_type="sleep_pattern_change",
                        strength=SignalStrength.WEAK,
                        description="Sleep patterns have changed",
                        detected_at=datetime.now().isoformat(),
                        confidence=0.65,
                        evidence=[sleep.get("description", "Sleep pattern change")],
                        framing="Sleep changes can affect many areas of life. This is worth monitoring.",
                    )
                    signals.append(signal)

        return signals

    def _detect_values_signals(self, user_id: str, data: Dict[str, Any]) -> List[PatternSignal]:
        """
        Detect patterns in VALUES/SPIRITUAL domain.

        A spiritual mentor sees values and meaning, but may not have data context
        to spot early practical risks. AI can bridge these.
        """
        signals = []

        if "values" in data:
            values = data["values"]

            # Values-goal misalignment
            if "values_alignment" in values:
                alignment = values["values_alignment"]
                if alignment.get("score", 1.0) < 0.7:
                    signal = PatternSignal(
                        id=f"values_signal_{datetime.now().strftime('%Y%m%d%H%M%S')}",
                        domain=Domain.VALUES,
                        signal_type="values_misalignment",
                        strength=SignalStrength.MODERATE,
                        description="Actions may not be fully aligned with stated values",
                        detected_at=datetime.now().isoformat(),
                        confidence=0.65,
                        evidence=[
                            f"Alignment score: {alignment.get('score', 0):.0%}",
                            alignment.get("description", "Potential misalignment detected"),
                        ],
                        framing="This might indicate a need for reflection or adjustment. Values evolve, and that's okay.",
                    )
                    signals.append(signal)

            # Purpose/meaning questions
            if "purpose_questions" in values:
                questions = values["purpose_questions"]
                if questions.get("detected"):
                    signal = PatternSignal(
                        id=f"values_signal_purpose_{datetime.now().strftime('%Y%m%d%H%M%S')}",
                        domain=Domain.VALUES,
                        signal_type="purpose_reflection_opportunity",
                        strength=SignalStrength.WEAK,
                        description="Opportunity for reflection on purpose and meaning",
                        detected_at=datetime.now().isoformat(),
                        confidence=0.60,
                        evidence=[questions.get("description", "Purpose reflection opportunity")],
                        framing="Reflection on purpose and meaning is valuable. This might be a good time for it.",
                    )
                    signals.append(signal)

        return signals

    # =========================================================================
    # CROSS-DOMAIN PATTERN CONNECTION
    # =========================================================================

    def connect_cross_domain_patterns(
        self, user_id: str, signals: List[PatternSignal]
    ) -> List[CrossDomainInsight]:
        """
        Connect patterns across domains - the advisor's superpower.

        This is where AI excels: seeing connections humans might miss.
        """
        insights = []

        # Group signals by domain
        by_domain: Dict[Domain, List[PatternSignal]] = defaultdict(list)
        for signal in signals:
            by_domain[signal.domain].append(signal)

        # Look for cross-domain connections
        # This is where AI excels: connecting what financial planners, doctors,
        # and spiritual mentors each see separately

        # Connection 1: Financial stress → Learning patterns
        # (Financial planner won't see learning patterns)
        if Domain.FINANCIAL in by_domain and Domain.TEACHER in by_domain:
            financial_signals = [
                s for s in by_domain[Domain.FINANCIAL] if s.signal_type == "budget_stress"
            ]
            teacher_signals = [
                s for s in by_domain[Domain.TEACHER] if s.signal_type == "skill_gaps_emerging"
            ]

            if financial_signals and teacher_signals:
                insight = CrossDomainInsight(
                    id=f"insight_financial_teacher_{datetime.now().strftime('%Y%m%d%H%M%S')}",
                    title="Connection: Financial Stress & Learning Opportunities",
                    description="I notice a connection between financial patterns and learning opportunities",
                    domains_involved=[Domain.FINANCIAL, Domain.TEACHER],
                    connection_explanation=(
                        "Your budget shows stress while learning opportunities have emerged. "
                        "A financial planner would see the budget stress but not the learning patterns. "
                        "These might be related - financial stress can limit learning investments, "
                        "or learning opportunities might require financial resources. "
                        "Sometimes free or low-cost learning paths can address both."
                    ),
                    evidence={
                        Domain.FINANCIAL: [s.description for s in financial_signals],
                        Domain.TEACHER: [s.description for s in teacher_signals],
                    },
                    significance=(
                        "This connection might reveal opportunities: free learning resources, "
                        "community-based learning, or learning that could improve financial outcomes."
                    ),
                    reflection_prompt=(
                        "Does financial stress affect your ability to pursue learning? "
                        "Are there free or low-cost ways to address the learning opportunities?"
                    ),
                    suggested_action=(
                        "Consider exploring free learning resources (community courses, online tutorials, "
                        "peer learning) that could address both the learning opportunities and "
                        "financial constraints."
                    ),
                    confidence=0.70,
                    detected_at=datetime.now().isoformat(),
                )
                insights.append(insight)

        # Connection 2: Health patterns → Collaboration
        # (Doctor won't track household budget stress or collaboration patterns)
        if Domain.HEALTH in by_domain and Domain.TRIBE in by_domain:
            health_signals = [
                s for s in by_domain[Domain.HEALTH] if s.signal_type == "activity_decline"
            ]
            tribe_signals = [
                s for s in by_domain[Domain.TRIBE] if s.signal_type == "declining_collaboration"
            ]

            if health_signals and tribe_signals:
                insight = CrossDomainInsight(
                    id=f"insight_health_tribe_{datetime.now().strftime('%Y%m%d%H%M%S')}",
                    title="Connection: Health Patterns & Collaboration",
                    description="I notice a connection between health patterns and collaboration",
                    domains_involved=[Domain.HEALTH, Domain.TRIBE],
                    connection_explanation=(
                        "Your physical activity has been declining while collaboration has also decreased. "
                        "A doctor would see the activity decline but not the collaboration patterns. "
                        "These might be related - fatigue or health issues can affect our ability to engage, "
                        "or reduced collaboration might be contributing to lower activity levels."
                    ),
                    evidence={
                        Domain.HEALTH: [s.description for s in health_signals],
                        Domain.TRIBE: [s.description for s in tribe_signals],
                    },
                    significance=(
                        "This connection might indicate that addressing one could help the other. "
                        "Collaborative activities (walking meetings, group exercise) could address both."
                    ),
                    reflection_prompt=(
                        "Is fatigue or health affecting your collaboration? "
                        "Could collaborative activities help with both health and connection?"
                    ),
                    suggested_action=(
                        "Consider collaborative activities that combine movement and connection "
                        "(walking meetings, group exercise, active social time)."
                    ),
                    confidence=0.65,
                    detected_at=datetime.now().isoformat(),
                )
                insights.append(insight)

        # Connection 3: Values → Provider choices (RECON)
        # (Spiritual mentor may not have data context to spot practical risks)
        if Domain.VALUES in by_domain and Domain.RECON in by_domain:
            values_signals = [
                s for s in by_domain[Domain.VALUES] if s.signal_type == "values_misalignment"
            ]
            recon_signals = [
                s for s in by_domain[Domain.RECON] if s.signal_type == "provider_friction"
            ]

            if values_signals and recon_signals:
                insight = CrossDomainInsight(
                    id=f"insight_values_recon_{datetime.now().strftime('%Y%m%d%H%M%S')}",
                    title="Connection: Values & Provider Choices",
                    description="I notice a connection between your values and provider relationships",
                    domains_involved=[Domain.VALUES, Domain.RECON],
                    connection_explanation=(
                        "There's potential misalignment with your values while provider friction has been detected. "
                        "A spiritual mentor would see the values but may not have data context to spot "
                        "practical risks with providers. These might be related - using providers that don't "
                        "align with your values can create friction, and friction can make it harder to live "
                        "according to your values."
                    ),
                    evidence={
                        Domain.VALUES: [s.description for s in values_signals],
                        Domain.RECON: [s.description for s in recon_signals],
                    },
                    significance=(
                        "This connection might reveal an opportunity: finding providers that better align "
                        "with your values could reduce friction and improve alignment."
                    ),
                    reflection_prompt=(
                        "Do your provider choices align with your values? "
                        "Could switching providers improve both alignment and reduce friction?"
                    ),
                    suggested_action=(
                        "Consider reviewing your providers for values alignment. "
                        "Providers that match your values might reduce friction and improve satisfaction."
                    ),
                    confidence=0.70,
                    detected_at=datetime.now().isoformat(),
                )
                insights.append(insight)

        # Connection 4: Financial stress → Health
        # (Financial planner won't see health, doctor won't see budget stress)
        if Domain.FINANCIAL in by_domain and Domain.HEALTH in by_domain:
            financial_signals = [
                s for s in by_domain[Domain.FINANCIAL] if s.signal_type == "budget_stress"
            ]
            health_signals = [
                s
                for s in by_domain[Domain.HEALTH]
                if s.signal_type in ["activity_decline", "sleep_pattern_change"]
            ]

            if financial_signals and health_signals:
                insight = CrossDomainInsight(
                    id=f"insight_financial_health_{datetime.now().strftime('%Y%m%d%H%M%S')}",
                    title="Connection: Budget Stress & Health Patterns",
                    description="I notice a connection between financial stress and health patterns",
                    domains_involved=[Domain.FINANCIAL, Domain.HEALTH],
                    connection_explanation=(
                        "Budget stress is present while health patterns have changed. "
                        "A financial planner would see the budget stress but not health patterns. "
                        "A doctor would see health patterns but not budget stress. "
                        "Financial stress can affect health (sleep, activity, stress levels), "
                        "and health issues can create financial stress."
                    ),
                    evidence={
                        Domain.FINANCIAL: [s.description for s in financial_signals],
                        Domain.HEALTH: [s.description for s in health_signals],
                    },
                    significance=(
                        "This connection might indicate that addressing financial stress could improve health, "
                        "or that health improvements could reduce financial stress (fewer medical costs, "
                        "better work capacity)."
                    ),
                    reflection_prompt=(
                        "Is financial stress affecting your health? "
                        "Could addressing one help with the other?"
                    ),
                    suggested_action=(
                        "Consider low-cost health activities (walking, free exercise resources) "
                        "and financial stress reduction strategies (budget review, free financial counseling)."
                    ),
                    confidence=0.75,
                    detected_at=datetime.now().isoformat(),
                )
                insights.append(insight)

        # Original connection: Declining collaboration + skill gaps
        if Domain.TRIBE in by_domain and Domain.TEACHER in by_domain:
            tribe_signals = [
                s for s in by_domain[Domain.TRIBE] if s.signal_type == "declining_collaboration"
            ]
            teacher_signals = [
                s for s in by_domain[Domain.TEACHER] if s.signal_type == "skill_gaps_emerging"
            ]

            if tribe_signals and teacher_signals:
                insight = CrossDomainInsight(
                    id=f"insight_{datetime.now().strftime('%Y%m%d%H%M%S')}",
                    title="Connection: Collaboration & Learning",
                    description="I notice a pattern connecting your collaboration patterns and learning opportunities",
                    domains_involved=[Domain.TRIBE, Domain.TEACHER],
                    connection_explanation=(
                        "Your collaboration activity has been declining while several skill growth "
                        "opportunities have emerged. These might be related - sometimes learning "
                        "new skills happens through collaboration, and sometimes collaboration "
                        "happens when we're learning together."
                    ),
                    evidence={
                        Domain.TRIBE: [s.description for s in tribe_signals],
                        Domain.TEACHER: [s.description for s in teacher_signals],
                    },
                    significance=(
                        "This connection might indicate an opportunity: engaging with peers "
                        "who have these skills could both address the skill opportunities "
                        "and rebuild collaboration connections."
                    ),
                    reflection_prompt=(
                        "Does this connection resonate? Have you been focusing more on "
                        "individual work lately? Is there a way to combine learning with collaboration?"
                    ),
                    suggested_action=(
                        "Consider reaching out to peers who have the skills you're exploring. "
                        "This could be a natural way to both learn and reconnect."
                    ),
                    confidence=0.70,
                    detected_at=datetime.now().isoformat(),
                )
                insights.append(insight)

        self.cross_domain_insights.extend(insights)
        return insights

    # =========================================================================
    # RECOMMENDATION GENERATION
    # =========================================================================

    def generate_recommendations(
        self, user_id: str, signals: List[PatternSignal], insights: List[CrossDomainInsight]
    ) -> List[Recommendation]:
        """
        Generate recommendations with transparent reasoning.

        Always explains why, always respects agency.
        """
        prefs = self.get_user_preferences(user_id)
        recommendations = []

        # Generate from signals
        for signal in signals:
            if prefs and signal.id in prefs.dismissed_recommendations:
                continue

            rec = self._signal_to_recommendation(user_id, signal, prefs)
            if rec:
                recommendations.append(rec)

        # Generate from cross-domain insights
        for insight in insights:
            rec = self._insight_to_recommendation(user_id, insight, prefs)
            if rec:
                recommendations.append(rec)

        # Apply user preferences
        if prefs:
            # Filter by confidence
            recommendations = [
                r
                for r in recommendations
                if r.reasoning.get("confidence", 0) >= prefs.min_confidence_threshold
            ]

            # Limit count
            recommendations = recommendations[: prefs.max_recommendations_per_day]

            # Apply custom framing
            for rec in recommendations:
                if rec.type.value in prefs.custom_framing:
                    rec.supportive_message = prefs.custom_framing[rec.type.value]

        # Store in history
        self.recommendations_history[user_id].extend(recommendations)

        return recommendations

    def _signal_to_recommendation(
        self, user_id: str, signal: PatternSignal, prefs: Optional[UserPreferences]
    ) -> Optional[Recommendation]:
        """Convert a signal to a recommendation."""

        # Determine recommendation type
        if signal.strength in [SignalStrength.STRONG, SignalStrength.CRITICAL]:
            rec_type = RecommendationType.EARLY_WARNING
            priority = "high" if signal.strength == SignalStrength.STRONG else "urgent"
        else:
            rec_type = RecommendationType.OPPORTUNITY
            priority = "medium" if signal.strength == SignalStrength.MODERATE else "low"

        # Generate supportive message
        if signal.framing:
            supportive_msg = signal.framing
        else:
            supportive_msg = (
                "This is an observation, not a judgment. You're in control of how to respond."
            )

        rec = Recommendation(
            id=f"rec_{signal.id}",
            type=rec_type,
            title=f"Pattern in {signal.domain.value.title()}: {signal.signal_type.replace('_', ' ').title()}",
            description=signal.description,
            priority=priority,
            reasoning={
                "why_now": f"This pattern has {signal.strength.value} strength",
                "evidence": signal.evidence,
                "confidence": signal.confidence,
                "alternatives_considered": [
                    "This could be a temporary fluctuation",
                    "This might reflect intentional choices",
                    "This could indicate a shift in priorities",
                ],
            },
            user_can_override=True,
            user_can_dismiss=True,
            user_can_customize=True,
            suggested_actions=self._generate_actions_for_signal(signal),
            supportive_message=supportive_msg,
            generated_at=datetime.now().isoformat(),
        )

        return rec

    def _insight_to_recommendation(
        self, user_id: str, insight: CrossDomainInsight, prefs: Optional[UserPreferences]
    ) -> Optional[Recommendation]:
        """Convert a cross-domain insight to a recommendation."""

        rec = Recommendation(
            id=f"rec_{insight.id}",
            type=RecommendationType.CONNECTION,
            title=insight.title,
            description=insight.description,
            priority="medium",
            reasoning={
                "why_now": "I noticed a connection across domains that might be worth exploring",
                "evidence": {
                    domain.value: evidence for domain, evidence in insight.evidence.items()
                },
                "cross_domain_connections": insight.connection_explanation,
                "confidence": insight.confidence,
                "alternatives_considered": [
                    "These patterns might be coincidental",
                    "The connection might not be meaningful for you",
                ],
            },
            user_can_override=True,
            user_can_dismiss=True,
            user_can_customize=True,
            suggested_actions=[insight.suggested_action] if insight.suggested_action else [],
            helpful_resources=[
                {
                    "type": "reflection",
                    "title": "Reflection Prompt",
                    "description": insight.reflection_prompt,
                }
            ],
            supportive_message=(
                "I'm sharing this connection because it might be helpful. "
                "You know your situation best - take what resonates, leave what doesn't."
            ),
            generated_at=datetime.now().isoformat(),
        )

        return rec

    def _generate_actions_for_signal(self, signal: PatternSignal) -> List[str]:
        """Generate suggested actions for a signal."""
        actions = []

        if signal.domain == Domain.TRIBE:
            if signal.signal_type == "declining_collaboration":
                actions = [
                    "Check in with a few key collaborators",
                    "Review your collaboration goals - are they still aligned?",
                    "Consider if this reflects intentional focus on deep work",
                ]

        elif signal.domain == Domain.TEACHER:
            if signal.signal_type == "skill_gaps_emerging":
                actions = [
                    "Explore one skill that interests you most",
                    "Connect with peers who have these skills",
                    "Consider if any of these align with your current goals",
                ]

        elif signal.domain == Domain.RECON:
            if signal.signal_type == "provider_friction":
                actions = [
                    "Review which friction points matter most to you",
                    "Explore alternatives for the highest-friction tools",
                    "Consider if workflow optimization could reduce friction",
                ]

        return actions

    # =========================================================================
    # EXPLAINABILITY (Transparent Reasoning)
    # =========================================================================

    def explain_recommendation(self, recommendation_id: str, user_id: str) -> Dict[str, Any]:
        """
        Provide full explanation of why a recommendation was generated.

        This is how we build trust through transparency.
        """
        # Find recommendation
        rec = None
        for rec_list in self.recommendations_history.values():
            for r in rec_list:
                if r.id == recommendation_id:
                    rec = r
                    break
            if rec:
                break

        if not rec:
            return {"error": "Recommendation not found"}

        # Build full explanation
        explanation = {
            "recommendation": rec.to_dict(),
            "reasoning_breakdown": {
                "why_this_matters": rec.reasoning.get("why_now", ""),
                "evidence": rec.reasoning.get("evidence", []),
                "confidence": rec.reasoning.get("confidence", 0.0),
                "what_i_considered": rec.reasoning.get("alternatives_considered", []),
                "cross_domain_connections": rec.reasoning.get("cross_domain_connections", ""),
            },
            "your_control": {
                "can_override": rec.user_can_override,
                "can_dismiss": rec.user_can_dismiss,
                "can_customize": rec.user_can_customize,
                "message": "This is a suggestion, not a command. You're in control.",
            },
            "how_to_respond": {
                "if_this_resonates": "Consider the suggested actions",
                "if_this_doesnt_fit": "Feel free to dismiss or override",
                "if_you_want_more_info": "Ask me to explain any part in more detail",
            },
        }

        return explanation

    # =========================================================================
    # SUMMARY & EXPORT
    # =========================================================================

    def get_advisor_summary(self, user_id: str) -> Dict[str, Any]:
        """Get a summary of advisor activity for a user."""
        prefs = self.get_user_preferences(user_id)
        recent_recs = self.recommendations_history.get(user_id, [])[-10:]
        active_signals = [
            s
            for s in self.active_signals.values()
            if s.id not in (prefs.dismissed_patterns if prefs else set())
        ]
        recent_insights = self.cross_domain_insights[-5:]

        return {
            "user_id": user_id,
            "preferences": prefs.to_dict() if prefs else None,
            "active_signals": len(active_signals),
            "recent_recommendations": len(recent_recs),
            "cross_domain_insights": len(recent_insights),
            "advisor_philosophy": {
                "advise_not_control": True,
                "support_not_surveil": True,
                "transparent_reasoning": True,
                "respect_agency": True,
                "nonjudgmental": True,
            },
            "recent_activity": {
                "signals": [s.to_dict() for s in active_signals[:5]],
                "recommendations": [r.to_dict() for r in recent_recs[:5]],
                "insights": [i.to_dict() for i in recent_insights],
            },
        }


# =============================================================================
# MAIN - Demo
# =============================================================================


def main():
    """Demonstrate the Cosurvival Advisor."""
    print("=" * 70)
    print("  COSURVIVAL AI ADVISOR - Demo")
    print("=" * 70)

    advisor = CosurvivalAdvisor()

    # Set up user preferences (user maintains agency)
    print("\n1. Setting user preferences...")
    prefs = UserPreferences(
        user_id="demo_user_001",
        communication_style="supportive",
        notification_frequency="moderate",
        min_confidence_threshold=0.6,
        max_recommendations_per_day=5,
        stated_values=["learning", "collaboration", "balance"],
        current_goals=["Build stronger team connections", "Learn data analysis skills"],
    )
    advisor.set_user_preferences("demo_user_001", prefs)
    print("   [OK] User preferences set")

    # Simulate data from TRIBE, TEACHER, RECON, FINANCIAL, HEALTH, VALUES
    print("\n2. Simulating cross-domain data...")
    demo_data = {
        "tribe": {
            "collaboration_trend": {"direction": "declining", "rate": 0.3, "period": "last 30 days"}
        },
        "teacher": {
            "skill_gaps": [
                "data_analysis",
                "python_programming",
                "sql_queries",
                "data_visualization",
            ]
        },
        "recon": {
            "friction_points": [
                {"provider": "tool_a", "issue": "slow_load_times"},
                {"provider": "tool_b", "issue": "complex_ui"},
            ]
        },
        "financial": {
            "spending_stress": {"level": "high", "percentage": 85, "status": "over_budget"}
        },
        "health": {"activity_decline": {"rate": 0.25, "period": "last 30 days"}},
        "values": {
            "values_alignment": {
                "score": 0.65,
                "description": "Some actions may not fully align with stated values",
            }
        },
    }
    print("   [OK] Data loaded (TRIBE, TEACHER, RECON, FINANCIAL, HEALTH, VALUES)")

    # Detect early warning signals
    print("\n3. Detecting early warning signals...")
    signals = advisor.detect_early_warning_signals("demo_user_001", demo_data)
    print(f"   [OK] Detected {len(signals)} signals")
    for signal in signals:
        print(f"      - {signal.domain.value}: {signal.signal_type} ({signal.strength.value})")

    # Connect cross-domain patterns
    print("\n4. Connecting cross-domain patterns...")
    insights = advisor.connect_cross_domain_patterns("demo_user_001", signals)
    print(f"   [OK] Found {len(insights)} cross-domain insights")
    for insight in insights:
        print(f"      - {insight.title}")
        print(f"        Domains: {', '.join([d.value for d in insight.domains_involved])}")

    # Generate recommendations
    print("\n5. Generating recommendations...")
    recommendations = advisor.generate_recommendations("demo_user_001", signals, insights)
    print(f"   [OK] Generated {len(recommendations)} recommendations")

    for rec in recommendations:
        print(f"\n   [REC] {rec.title}")
        print(f"      Type: {rec.type.value}")
        print(f"      Priority: {rec.priority}")
        print(f"      {rec.description}")
        print(f"      Supportive message: {rec.supportive_message}")
        confidence = rec.reasoning.get("confidence", 0)
        print(f"      Reasoning confidence: {confidence:.1%}")

        # Show cross-domain connections if this is a connection recommendation
        if (
            rec.type == RecommendationType.CONNECTION
            and "cross_domain_connections" in rec.reasoning
        ):
            print(
                f"      Cross-domain insight: {rec.reasoning['cross_domain_connections'][:150]}..."
            )

        if rec.suggested_actions:
            print("      Suggested actions:")
            for action in rec.suggested_actions:
                print(f"        - {action}")

    # Explain a recommendation
    if recommendations:
        print("\n6. Explaining recommendation reasoning...")
        explanation = advisor.explain_recommendation(recommendations[0].id, "demo_user_001")
        print("   [OK] Full explanation generated")
        print(f"      Why this matters: {explanation['reasoning_breakdown']['why_this_matters']}")
        print(f"      Confidence: {explanation['reasoning_breakdown']['confidence']:.1%}")
        print(f"      Your control: {explanation['your_control']['message']}")

    # Get summary
    print("\n7. Generating advisor summary...")
    summary = advisor.get_advisor_summary("demo_user_001")
    print("   [OK] Summary generated")
    print(f"      Active signals: {summary['active_signals']}")
    print(f"      Recent recommendations: {summary['recent_recommendations']}")
    print(f"      Cross-domain insights: {summary['cross_domain_insights']}")

    print("\n" + "=" * 70)
    print("  Advisor Philosophy:")
    print("  - Advise, don't control")
    print("  - Support, don't surveil")
    print("  - Transparent reasoning always")
    print("  - Respect user agency")
    print("  - Nonjudgmental framing")
    print("=" * 70)


if __name__ == "__main__":
    main()
