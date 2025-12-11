#!/usr/bin/env python3
"""
COSURVIVAL MVP EXTRACTORS
=========================
Small, undeniable wins for each system layer.

These extractors produce the minimum viable outputs that prove:
- TRIBE: Social network is real and measurable
- TEACHER: Learning pathways can be derived from activity
- RECONSUMERALIZATION: Value flows and ethics can be scored

Each MVP is designed to be:
- Independently valuable
- Verifiable against raw data
- Free of prohibited inferences
- Compliant with bias guardrails

CURRICULUM MAPPING:
-------------------
Week 3: Algorithms - MVP Extractors
  - Activity 3.1: Implement Collaboration Strength
  - Activity 3.2: Build Role Mastery Profiler
  - Activity 3.3: Create Provider Scorer
  - See: TEACHER_CORE_TRACK.md, Week 3, Theme: "MVP Extractors"

Week 4+: Domains - Applied Systems
  - Module 4A: TRIBE Deep Dive (community detection, bridges, mentors)
  - Module 4B: TEACHER Deep Dive (role-skill matrix, learning paths)
  - Module 4C: RECON Deep Dive (provider profiler, value flows)
  - See: TEACHER_CORE_TRACK.md, Week 4+, Domains
"""

"""
COSURVIVAL MVP EXTRACTORS
=========================
Small, undeniable wins for each system layer.

These extractors produce the minimum viable outputs that prove:
- TRIBE: Social network is real and measurable
- TEACHER: Learning pathways can be derived from activity
- RECONSUMERALIZATION: Value flows and ethics can be scored

Each MVP is designed to be:
- Independently valuable
- Verifiable against raw data
- Free of prohibited inferences
- Compliant with bias guardrails
"""

# Standard library imports
import hashlib
import json
from collections import defaultdict
from dataclasses import dataclass, field, asdict
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional, Any, Tuple, Set

# Local imports
from ingestion import (
    CanonicalUser,
    CanonicalCompany,
    CanonicalGroup,
    CanonicalProvider,
    CanonicalActivity,
    CanonicalPermissionChange,
)


# =============================================================================
# TRIBE MVP - Social Network Analysis
# =============================================================================


@dataclass
class TribeCommunity:
    """A detected community in the network."""

    id: str
    members: List[str]
    size: int
    cohesion_score: float  # 0-1, based on internal edge density
    label: str = ""  # Auto-generated or manual label


@dataclass
class TribeBridge:
    """A cross-silo bridge connector."""

    user_id: str
    communities_connected: List[str]
    bridge_score: float  # How important for cross-community flow
    unique_connections: int


@dataclass
class TribeMentorCandidate:
    """A potential mentor based on network position and activity."""

    user_id: str
    company_id: str
    roles: List[str]
    activity_count: int
    connection_count: int
    mentorship_score: float
    strengths: List[str]
    # Bias guardrail: explicitly NOT a performance rating
    note: str = "Score reflects network position and tenure, not performance"


@dataclass
class TribeMVPOutput:
    """Complete TRIBE MVP output."""

    generated_at: str

    # Network statistics
    total_users: int
    total_companies: int
    total_groups: int
    total_edges: int
    network_density: float

    # Communities
    communities: List[TribeCommunity]
    largest_community_size: int
    isolated_users: int

    # Bridges
    cross_silo_bridges: List[TribeBridge]

    # Mentor candidates
    mentor_candidates: List[TribeMentorCandidate]

    # Collaboration patterns (aggregated, not individual)
    top_collaborating_companies: List[Dict[str, Any]]
    top_collaborating_groups: List[Dict[str, Any]]

    # Metadata
    methodology_notes: List[str] = field(default_factory=list)
    bias_guardrails_applied: List[str] = field(default_factory=list)


class TribeMVPExtractor:
    """
    Extracts TRIBE MVP outputs from canonical data.

    Graph Structure:
    - Nodes: Users, Groups, Companies
    - Edges:
      - UidOpp/UidReq interactions
      - Shared group membership
      - Shared company membership
      - Co-resource access (same resource within time window)

    CURRICULUM: Week 0, Core Concepts #2 - The Three Questions
    TRIBE Lens Question: "Who is connected to whom?"
    Output: Network graph
    See: TEACHER_CORE_TRACK.md, Week 0, Core Concepts #2

    CURRICULUM: Week 2, Core Concepts #2 - Graph Structures
    Learners understand TRIBE graphs: nodes (users/groups/companies),
    edges (collaboration/membership), weights (interaction frequency).
    See: TEACHER_CORE_TRACK.md, Week 2, Core Concepts #2

    CURRICULUM: Week 3, Activity 3.1 - Implement Collaboration Strength
    This extractor implements the collaboration_strength algorithm.
    See: TEACHER_CORE_TRACK.md, Week 3, Activity 3.1

    CURRICULUM: Week 4+, Module 4A - TRIBE Deep Dive
    Community detection, bridge finder, mentor identifier.
    See: TEACHER_CORE_TRACK.md, Week 4+, Module 4A
    """

    def __init__(self):
        self.users: Dict[str, CanonicalUser] = {}
        self.companies: Dict[str, CanonicalCompany] = {}
        self.groups: Dict[str, CanonicalGroup] = {}
        self.activities: List[CanonicalActivity] = []

        # Graph structures
        self.user_edges: Dict[str, Dict[str, int]] = defaultdict(lambda: defaultdict(int))
        self.company_edges: Dict[str, Dict[str, int]] = defaultdict(lambda: defaultdict(int))
        self.group_edges: Dict[str, Dict[str, int]] = defaultdict(lambda: defaultdict(int))

    def load_data(
        self,
        users: Dict[str, CanonicalUser],
        companies: Dict[str, CanonicalCompany],
        groups: Dict[str, CanonicalGroup],
        activities: List[CanonicalActivity],
    ):
        """Load canonical data."""
        self.users = users
        self.companies = companies
        self.groups = groups
        self.activities = activities

    def build_graph(self):
        """
        Build the collaboration graph from activities.

        CURRICULUM: Week 3, Core Concepts #1 - TRIBE Algorithms
        Implements the collaboration_strength algorithm factors:
        - Direct interactions (UidOpp/UidReq)
        - Co-resource access (same file on same day)
        - Shared group membership
        See: TEACHER_CORE_TRACK.md, Week 3, Core Concepts #1

        CURRICULUM: Week 3, Core Concepts #4 - Efficiency Matters
        Graph building: O(n²) naive → O(n log n) optimized
        See: TEACHER_CORE_TRACK.md, Week 3, Core Concepts #4
        """
        print("   Building collaboration graph...")

        # Track resource co-access (users accessing same resource on same day)
        resource_access: Dict[str, Dict[str, Set[str]]] = defaultdict(lambda: defaultdict(set))

        for activity in self.activities:
            # Direct interactions (UidOpp/UidReq)
            if activity.target_user_id and activity.user_id != activity.target_user_id:
                u1, u2 = sorted([activity.user_id, activity.target_user_id])
                self.user_edges[u1][u2] += 1

            # Track resource access
            if activity.resource_id and activity.timestamp_date:
                resource_access[activity.resource_id][activity.timestamp_date].add(activity.user_id)

        # Add co-access edges
        for resource_id, date_users in resource_access.items():
            for date, users in date_users.items():
                users_list = list(users)
                for i in range(len(users_list)):
                    for j in range(i + 1, len(users_list)):
                        u1, u2 = sorted([users_list[i], users_list[j]])
                        self.user_edges[u1][u2] += 1

        # Build company edges from user connections
        for u1, connections in self.user_edges.items():
            c1 = self.users.get(u1, {})
            c1_id = c1.company_id if hasattr(c1, "company_id") else ""

            for u2, weight in connections.items():
                c2 = self.users.get(u2, {})
                c2_id = c2.company_id if hasattr(c2, "company_id") else ""

                if c1_id and c2_id and c1_id != c2_id:
                    self.company_edges[c1_id][c2_id] += weight

        total_edges = sum(len(v) for v in self.user_edges.values())
        print(f"   ✓ Built graph with {len(self.user_edges)} nodes, {total_edges} edges")

    def detect_communities(self, min_size: int = 3) -> List[TribeCommunity]:
        """
        Detect communities using simple connected components.
        (For production, use Louvain or similar.)
        """
        print("   Detecting communities...")

        # Simple connected components approach
        visited = set()
        communities = []

        def bfs(start: str) -> Set[str]:
            component = set()
            queue = [start]
            while queue:
                node = queue.pop(0)
                if node in visited:
                    continue
                visited.add(node)
                component.add(node)
                for neighbor in self.user_edges.get(node, {}).keys():
                    if neighbor not in visited:
                        queue.append(neighbor)
            return component

        for user_id in self.users.keys():
            if user_id not in visited:
                component = bfs(user_id)
                if len(component) >= min_size:
                    # Calculate cohesion (internal edges / possible edges)
                    internal_edges = (
                        sum(
                            1
                            for u1 in component
                            for u2 in self.user_edges.get(u1, {})
                            if u2 in component
                        )
                        // 2
                    )
                    possible_edges = len(component) * (len(component) - 1) // 2
                    cohesion = internal_edges / possible_edges if possible_edges > 0 else 0

                    communities.append(
                        TribeCommunity(
                            id=f"comm_{len(communities)}",
                            members=list(component),
                            size=len(component),
                            cohesion_score=cohesion,
                        )
                    )

        print(f"   ✓ Found {len(communities)} communities")
        return sorted(communities, key=lambda c: c.size, reverse=True)

    def find_bridges(self, communities: List[TribeCommunity]) -> List[TribeBridge]:
        """Find users who bridge multiple communities."""
        print("   Finding cross-silo bridges...")

        # Map users to their communities
        user_communities: Dict[str, List[str]] = defaultdict(list)
        for comm in communities:
            for member in comm.members:
                user_communities[member].append(comm.id)

        bridges = []
        for user_id, comms in user_communities.items():
            if len(comms) > 1:
                # Calculate bridge score
                unique_connections = len(self.user_edges.get(user_id, {}))
                bridge_score = len(comms) * unique_connections / 100  # Normalize

                bridges.append(
                    TribeBridge(
                        user_id=user_id,
                        communities_connected=comms,
                        bridge_score=min(bridge_score, 1.0),
                        unique_connections=unique_connections,
                    )
                )

        # Also find users who connect different companies
        for user_id in self.users.keys():
            connections = self.user_edges.get(user_id, {})
            connected_companies = set()
            for conn_id in connections.keys():
                if conn_id in self.users:
                    conn_company = self.users[conn_id].company_id
                    if conn_company:
                        connected_companies.add(conn_company)

            user_company = self.users[user_id].company_id
            external_companies = connected_companies - {user_company}

            if len(external_companies) >= 2:
                # This user bridges multiple external companies
                existing = next((b for b in bridges if b.user_id == user_id), None)
                if not existing:
                    bridges.append(
                        TribeBridge(
                            user_id=user_id,
                            communities_connected=[f"company_{c}" for c in external_companies],
                            bridge_score=len(external_companies) / 10,
                            unique_connections=len(connections),
                        )
                    )

        print(f"   ✓ Found {len(bridges)} bridge connectors")
        return sorted(bridges, key=lambda b: b.bridge_score, reverse=True)[:20]

    def find_mentor_candidates(self) -> List[TribeMentorCandidate]:
        """
        Find mentor candidates based on network position and tenure.

        BIAS GUARDRAIL: This is NOT a performance rating.
        High activity/connections may indicate:
        - Role requirements
        - Tenure
        - Network position
        NOT individual merit or contribution quality.
        """
        print("   Identifying mentor candidates...")

        candidates = []

        for user_id, user in self.users.items():
            connections = self.user_edges.get(user_id, {})
            connection_count = len(connections)

            # Simple mentorship score based on network position
            # (connection diversity + activity + tenure proxy)
            connection_score = min(connection_count / 10, 1.0)
            activity_score = min(user.activity_count / 500, 1.0)
            role_diversity = len(user.roles) / 5 if user.roles else 0

            mentorship_score = connection_score * 0.4 + activity_score * 0.3 + role_diversity * 0.3

            if mentorship_score > 0.3:  # Threshold
                # Determine strengths (from roles and connections)
                strengths = []
                if connection_count > 10:
                    strengths.append("Well-connected")
                if len(user.roles) > 1:
                    strengths.append("Multi-role experience")
                if user.activity_count > 200:
                    strengths.append("Active contributor")
                if len(user.groups) > 2:
                    strengths.append("Cross-team exposure")

                candidates.append(
                    TribeMentorCandidate(
                        user_id=user_id,
                        company_id=user.company_id,
                        roles=user.roles,
                        activity_count=user.activity_count,
                        connection_count=connection_count,
                        mentorship_score=mentorship_score,
                        strengths=strengths[:4],
                    )
                )

        print(f"   ✓ Found {len(candidates)} mentor candidates")
        return sorted(candidates, key=lambda c: c.mentorship_score, reverse=True)[:20]

    def extract(self) -> TribeMVPOutput:
        """Extract complete TRIBE MVP output."""
        print("\n🌐 Extracting TRIBE MVP...")

        self.build_graph()
        communities = self.detect_communities()
        bridges = self.find_bridges(communities)
        mentor_candidates = self.find_mentor_candidates()

        # Calculate network stats
        total_edges = sum(len(v) for v in self.user_edges.values())
        max_possible_edges = len(self.users) * (len(self.users) - 1) // 2
        density = total_edges / max_possible_edges if max_possible_edges > 0 else 0

        # Find isolated users (not in any community)
        community_members = set()
        for comm in communities:
            community_members.update(comm.members)
        isolated = len(self.users) - len(community_members)

        # Top collaborating companies
        company_collab = []
        for c1, connections in self.company_edges.items():
            for c2, weight in connections.items():
                company_collab.append(
                    {"company_1": c1, "company_2": c2, "collaboration_strength": weight}
                )
        company_collab.sort(key=lambda x: x["collaboration_strength"], reverse=True)

        # Top collaborating groups
        # (simplified - would need group edge building)
        group_collab = []

        return TribeMVPOutput(
            generated_at=datetime.now().isoformat(),
            total_users=len(self.users),
            total_companies=len(self.companies),
            total_groups=len(self.groups),
            total_edges=total_edges,
            network_density=density,
            communities=communities[:10],
            largest_community_size=communities[0].size if communities else 0,
            isolated_users=isolated,
            cross_silo_bridges=bridges,
            mentor_candidates=mentor_candidates,
            top_collaborating_companies=company_collab[:10],
            top_collaborating_groups=group_collab[:10],
            methodology_notes=[
                "Communities detected via connected components",
                "Bridge score = communities_connected × connections / 100",
                "Mentorship score = 0.4×connections + 0.3×activity + 0.3×role_diversity",
                "Collaboration edges from: direct interactions + resource co-access",
            ],
            bias_guardrails_applied=[
                "Mentor candidates are NOT performance ratings",
                "High activity reflects role requirements, not individual merit",
                "Isolated users may be deep-focus individual contributors",
            ],
        )


# =============================================================================
# TEACHER MVP - Learning Pathway Extraction
# =============================================================================


@dataclass
class TeacherSkillProgression:
    """A skill progression from state transitions."""

    from_state: str
    to_state: str
    frequency: int
    avg_time_days: Optional[float]
    common_in_roles: List[str]


@dataclass
class TeacherLearningRecommendation:
    """Personalized learning recommendation."""

    user_id: str
    current_skills: List[str]  # From roles/privileges
    recommended_skills: List[str]
    reason: str
    priority: str  # low, medium, high
    peer_reference: str  # "Based on peers in role X"
    # Bias guardrail
    note: str = "Skill gaps are growth opportunities, not deficiencies"


@dataclass
class TeacherRoleTransition:
    """Role transition probability."""

    from_role: str
    to_role: str
    frequency: int
    typical_time_days: Optional[float]
    prerequisite_skills: List[str]


@dataclass
class TeacherMVPOutput:
    """Complete TEACHER MVP output."""

    generated_at: str

    # Role analysis
    total_roles: int
    roles_with_users: Dict[str, int]  # role_id -> user_count

    # Skill progressions
    skill_progressions: List[TeacherSkillProgression]
    most_common_progression: Optional[TeacherSkillProgression]

    # Role transitions
    role_transitions: List[TeacherRoleTransition]

    # Personalized recommendations (sample)
    sample_recommendations: List[TeacherLearningRecommendation]
    total_recommendations_generated: int

    # Organization-level gaps
    org_skill_gaps: Dict[str, List[str]]  # company_id -> missing skills

    # Methodology
    methodology_notes: List[str] = field(default_factory=list)
    bias_guardrails_applied: List[str] = field(default_factory=list)


class TeacherMVPExtractor:
    """
    Extracts TEACHER MVP outputs from canonical data.

    Key analyses:
    - Role × Privilege ladder
    - "Next likely skills" from peer deltas
    - Personalized 3-step learning recommendations
    - Role transition likelihood
    """

    def __init__(self):
        self.users: Dict[str, CanonicalUser] = {}
        self.activities: List[CanonicalActivity] = []
        self.permission_changes: List[CanonicalPermissionChange] = []

        # Derived structures
        self.role_privileges: Dict[str, Set[str]] = defaultdict(set)
        self.user_privileges: Dict[str, Set[str]] = defaultdict(set)

    def load_data(
        self,
        users: Dict[str, CanonicalUser],
        activities: List[CanonicalActivity],
        permission_changes: List[CanonicalPermissionChange],
    ):
        """Load canonical data."""
        self.users = users
        self.activities = activities
        self.permission_changes = permission_changes

    def build_skill_maps(self):
        """Build role -> skills and user -> skills maps."""
        print("   Building skill maps...")

        # From permission changes
        for change in self.permission_changes:
            if change.permission_type:
                self.user_privileges[change.user_id].add(change.permission_type)
                if change.role_id:
                    self.role_privileges[change.role_id].add(change.permission_type)

        # From activities (activity types as proxy for skills)
        for activity in self.activities:
            if activity.activity_type:
                self.user_privileges[activity.user_id].add(f"activity:{activity.activity_type}")

        print(
            f"   ✓ Mapped skills for {len(self.user_privileges)} users across {len(self.role_privileges)} roles"
        )

    def extract_progressions(self) -> List[TeacherSkillProgression]:
        """
        Extract skill progressions from state transitions.

        CURRICULUM: Week 0, Core Concepts #3 - Privileges = Skills
        State transitions (state_before → state_after) represent
        skill acquisitions. Example: "viewer" → "editor" = growth.
        See: TEACHER_CORE_TRACK.md, Week 0, Core Concepts #3

        CURRICULUM: Week 3, Core Concepts #2 - TEACHER Algorithms
        Builds skill profile from permission history.
        See: TEACHER_CORE_TRACK.md, Week 3, Core Concepts #2
        """
        print("   Extracting skill progressions...")

        progression_counts: Dict[Tuple[str, str], int] = defaultdict(int)
        progression_roles: Dict[Tuple[str, str], Set[str]] = defaultdict(set)

        for change in self.permission_changes:
            if (
                change.state_before
                and change.state_after
                and change.state_before != change.state_after
            ):
                key = (change.state_before, change.state_after)
                progression_counts[key] += 1
                if change.role_id:
                    progression_roles[key].add(change.role_id)

        # Also from activities
        for activity in self.activities:
            if (
                activity.state_before
                and activity.state_after
                and activity.state_before != activity.state_after
            ):
                key = (activity.state_before, activity.state_after)
                progression_counts[key] += 1

        progressions = [
            TeacherSkillProgression(
                from_state=from_state,
                to_state=to_state,
                frequency=count,
                avg_time_days=None,  # Would need timestamp analysis
                common_in_roles=list(progression_roles.get((from_state, to_state), set()))[:5],
            )
            for (from_state, to_state), count in progression_counts.items()
        ]

        print(f"   ✓ Found {len(progressions)} skill progressions")
        return sorted(progressions, key=lambda p: p.frequency, reverse=True)

    def generate_recommendations(self) -> Tuple[List[TeacherLearningRecommendation], int]:
        """Generate personalized learning recommendations."""
        print("   Generating learning recommendations...")

        recommendations = []

        for user_id, user in self.users.items():
            user_skills = self.user_privileges.get(user_id, set())

            for role_id in user.roles:
                role_skills = self.role_privileges.get(role_id, set())
                missing = role_skills - user_skills

                if missing:
                    recommendations.append(
                        TeacherLearningRecommendation(
                            user_id=user_id,
                            current_skills=list(user_skills)[:5],
                            recommended_skills=list(missing)[:3],
                            reason=f"Commonly held by peers in role {role_id}",
                            priority="high" if len(missing) > 3 else "medium",
                            peer_reference=f"Based on {len([u for u in self.users.values() if role_id in u.roles])} peers in role {role_id}",
                        )
                    )

        print(f"   ✓ Generated {len(recommendations)} recommendations")
        return recommendations[:20], len(recommendations)

    def analyze_role_transitions(self) -> List[TeacherRoleTransition]:
        """Analyze role transition patterns."""
        print("   Analyzing role transitions...")

        # Track users with multiple roles (proxy for transitions)
        multi_role_users = [u for u in self.users.values() if len(u.roles) > 1]

        transition_counts: Dict[Tuple[str, str], int] = defaultdict(int)

        for user in multi_role_users:
            # Assume roles are in order of acquisition (simplification)
            for i in range(len(user.roles) - 1):
                key = (user.roles[i], user.roles[i + 1])
                transition_counts[key] += 1

        transitions = [
            TeacherRoleTransition(
                from_role=from_role,
                to_role=to_role,
                frequency=count,
                typical_time_days=None,
                prerequisite_skills=list(self.role_privileges.get(from_role, set()))[:5],
            )
            for (from_role, to_role), count in transition_counts.items()
        ]

        print(f"   ✓ Found {len(transitions)} role transitions")
        return sorted(transitions, key=lambda t: t.frequency, reverse=True)

    def identify_org_gaps(self) -> Dict[str, List[str]]:
        """Identify organization-level skill gaps."""
        print("   Identifying organization skill gaps...")

        company_skills: Dict[str, Set[str]] = defaultdict(set)

        for user_id, user in self.users.items():
            if user.company_id:
                company_skills[user.company_id].update(self.user_privileges.get(user_id, set()))

        # Find skills that are sparse relative to roles present
        all_skills = set()
        for skills in self.role_privileges.values():
            all_skills.update(skills)

        org_gaps = {}
        for company_id, skills in company_skills.items():
            missing = all_skills - skills
            if missing:
                org_gaps[company_id] = list(missing)[:10]

        print(f"   ✓ Identified gaps for {len(org_gaps)} organizations")
        return org_gaps

    def extract(self) -> TeacherMVPOutput:
        """Extract complete TEACHER MVP output."""
        print("\n📚 Extracting TEACHER MVP...")

        self.build_skill_maps()
        progressions = self.extract_progressions()
        recommendations, total_recs = self.generate_recommendations()
        transitions = self.analyze_role_transitions()
        org_gaps = self.identify_org_gaps()

        # Role user counts
        roles_with_users = defaultdict(int)
        for user in self.users.values():
            for role in user.roles:
                roles_with_users[role] += 1

        return TeacherMVPOutput(
            generated_at=datetime.now().isoformat(),
            total_roles=len(self.role_privileges),
            roles_with_users=dict(roles_with_users),
            skill_progressions=progressions[:20],
            most_common_progression=progressions[0] if progressions else None,
            role_transitions=transitions[:15],
            sample_recommendations=recommendations,
            total_recommendations_generated=total_recs,
            org_skill_gaps=org_gaps,
            methodology_notes=[
                "Skills derived from: permissions + activity types",
                "Recommendations based on peer skill comparison within role",
                "Role transitions inferred from multi-role users",
                "Org gaps = skills present in roles but missing in company",
            ],
            bias_guardrails_applied=[
                "Skill gaps framed as growth opportunities, not deficiencies",
                "Recommendations are suggestions, not requirements",
                "No individual performance implications",
            ],
        )


# =============================================================================
# RECONSUMERALIZATION MVP - Value Exchange Scoring
# =============================================================================


@dataclass
class ReconProviderScore:
    """Provider score v0."""

    provider_id: str
    provider_name: str
    adoption_score: float  # % of companies using
    reliability_score: float  # 1 - error_rate
    transparency_score: float  # Proxy from activity logging
    composite_score: float
    grade: str  # A-F
    customer_count: int
    user_count: int
    activity_volume: int
    error_rate: float
    strengths: List[str]
    concerns: List[str]


@dataclass
class ReconValueFlow:
    """A value flow between provider and consumer."""

    provider_id: str
    consumer_id: str  # company
    volume: int
    quality_score: float
    value_score: float
    is_friction_point: bool
    friction_reason: Optional[str]


@dataclass
class ReconMVPOutput:
    """Complete RECONSUMERALIZATION MVP output."""

    generated_at: str

    # Provider scores
    provider_scores: List[ReconProviderScore]
    top_providers: List[str]
    providers_needing_attention: List[str]

    # Value flows
    top_value_flows: List[ReconValueFlow]
    friction_points: List[ReconValueFlow]
    total_value_exchanged: int

    # Consumer profiles (aggregated)
    consumer_diversity_scores: Dict[str, float]  # company -> # providers / norm

    # Methodology
    methodology_notes: List[str] = field(default_factory=list)
    bias_guardrails_applied: List[str] = field(default_factory=list)


class ReconMVPExtractor:
    """
    Extracts RECONSUMERALIZATION MVP outputs from canonical data.

    Key analyses:
    - Provider score v0: Adoption × Reliability × Transparency proxy
    - Top 5 strongest value flows
    - Top 5 friction points
    """

    def __init__(self):
        self.providers: Dict[str, CanonicalProvider] = {}
        self.companies: Dict[str, CanonicalCompany] = {}
        self.activities: List[CanonicalActivity] = []

        # Derived
        self.provider_company_flows: Dict[str, Dict[str, int]] = defaultdict(
            lambda: defaultdict(int)
        )
        self.provider_company_errors: Dict[str, Dict[str, int]] = defaultdict(
            lambda: defaultdict(int)
        )

    def load_data(
        self,
        providers: Dict[str, CanonicalProvider],
        companies: Dict[str, CanonicalCompany],
        activities: List[CanonicalActivity],
    ):
        """Load canonical data."""
        self.providers = providers
        self.companies = companies
        self.activities = activities

    def build_flow_matrix(self):
        """Build provider -> company flow matrix."""
        print("   Building value flow matrix...")

        for activity in self.activities:
            if activity.provider_id and activity.company_id:
                self.provider_company_flows[activity.provider_id][activity.company_id] += 1

                if activity.error_code:
                    self.provider_company_errors[activity.provider_id][activity.company_id] += 1

        total_flows = sum(
            sum(companies.values()) for companies in self.provider_company_flows.values()
        )
        print(f"   ✓ Built flow matrix with {total_flows:,} total flows")

    def score_providers(self) -> List[ReconProviderScore]:
        """
        Calculate provider scores.

        CURRICULUM: Week 3, Core Concepts #3 - RECON Algorithms
        Score = 1 - (errors / total_activities)
        See: TEACHER_CORE_TRACK.md, Week 3, Core Concepts #3

        CURRICULUM: Week 3, Activity 3.3 - Create Provider Scorer
        Returns reliability, adoption, and composite scores.
        Assigns letter grade (A-F).
        See: TEACHER_CORE_TRACK.md, Week 3, Activity 3.3

        BIAS GUARDRAIL: Provider rankings reflect fit, not absolute quality.
        A provider may rank low for one use case but excel in another.
        See: governance.py, BIAS_GUARDRAILS["provider_rankings"]
        """
        print("   Scoring providers...")

        total_companies = len(self.companies)
        scores = []

        for provider_id, provider in self.providers.items():
            # Adoption score
            customer_count = len(provider.customer_companies)
            adoption = customer_count / total_companies if total_companies > 0 else 0

            # Reliability score
            reliability = (
                1 - (provider.error_count / provider.activity_count)
                if provider.activity_count > 0
                else 1
            )

            # Transparency proxy (activities logged / expected)
            # Simplified: assume all activities should be logged
            transparency = 0.85  # Placeholder - would need audit completeness metric

            # Composite score
            composite = adoption * 0.3 + reliability * 0.5 + transparency * 0.2

            # Grade
            if composite >= 0.9:
                grade = "A"
            elif composite >= 0.8:
                grade = "B"
            elif composite >= 0.7:
                grade = "C"
            elif composite >= 0.6:
                grade = "D"
            else:
                grade = "F"

            # Strengths and concerns
            strengths = []
            concerns = []

            if reliability > 0.99:
                strengths.append("Excellent reliability")
            elif reliability < 0.95:
                concerns.append("Reliability below 95%")

            if adoption > 0.5:
                strengths.append("Widely adopted")
            elif adoption < 0.1:
                concerns.append("Limited adoption")

            if len(provider.schemes) > 3:
                strengths.append("Diverse service offerings")

            scores.append(
                ReconProviderScore(
                    provider_id=provider_id,
                    provider_name=provider.name,
                    adoption_score=adoption,
                    reliability_score=reliability,
                    transparency_score=transparency,
                    composite_score=composite,
                    grade=grade,
                    customer_count=customer_count,
                    user_count=provider.user_count,
                    activity_volume=provider.activity_count,
                    error_rate=1 - reliability,
                    strengths=strengths,
                    concerns=concerns,
                )
            )

        print(f"   ✓ Scored {len(scores)} providers")
        return sorted(scores, key=lambda s: s.composite_score, reverse=True)

    def extract_value_flows(self) -> Tuple[List[ReconValueFlow], List[ReconValueFlow]]:
        """Extract value flows and identify friction points."""
        print("   Extracting value flows...")

        flows = []

        for provider_id, companies in self.provider_company_flows.items():
            for company_id, volume in companies.items():
                errors = self.provider_company_errors.get(provider_id, {}).get(company_id, 0)
                quality = 1 - (errors / volume) if volume > 0 else 1

                is_friction = quality < 0.9 or volume < 10  # Low quality or low volume

                flows.append(
                    ReconValueFlow(
                        provider_id=provider_id,
                        consumer_id=company_id,
                        volume=volume,
                        quality_score=quality,
                        value_score=volume * quality,
                        is_friction_point=is_friction,
                        friction_reason="High error rate"
                        if quality < 0.9
                        else "Low engagement"
                        if volume < 10
                        else None,
                    )
                )

        top_flows = sorted(flows, key=lambda f: f.value_score, reverse=True)[:5]
        friction_points = [f for f in flows if f.is_friction_point][:5]

        print(f"   ✓ Extracted {len(flows)} flows, {len(friction_points)} friction points")
        return top_flows, friction_points

    def calculate_consumer_diversity(self) -> Dict[str, float]:
        """Calculate consumer (company) provider diversity scores."""
        print("   Calculating consumer diversity...")

        diversity = {}
        max_providers = len(self.providers)

        for company_id, company in self.companies.items():
            provider_count = len(company.providers)
            diversity[company_id] = provider_count / max_providers if max_providers > 0 else 0

        return diversity

    def extract(self) -> ReconMVPOutput:
        """Extract complete RECONSUMERALIZATION MVP output."""
        print("\n💱 Extracting RECONSUMERALIZATION MVP...")

        self.build_flow_matrix()
        provider_scores = self.score_providers()
        top_flows, friction_points = self.extract_value_flows()
        consumer_diversity = self.calculate_consumer_diversity()

        total_value = sum(
            sum(companies.values()) for companies in self.provider_company_flows.values()
        )

        return ReconMVPOutput(
            generated_at=datetime.now().isoformat(),
            provider_scores=provider_scores,
            top_providers=[s.provider_id for s in provider_scores[:5]],
            providers_needing_attention=[
                s.provider_id for s in provider_scores if s.grade in ["D", "F"]
            ],
            top_value_flows=top_flows,
            friction_points=friction_points,
            total_value_exchanged=total_value,
            consumer_diversity_scores=consumer_diversity,
            methodology_notes=[
                "Adoption score = customers / total_companies",
                "Reliability score = 1 - (errors / activities)",
                "Transparency score = placeholder (0.85) pending audit completeness",
                "Composite = 0.3×adoption + 0.5×reliability + 0.2×transparency",
                "Friction point = quality < 90% OR volume < 10",
            ],
            bias_guardrails_applied=[
                "Provider rankings reflect fit, not absolute quality",
                "Low scores may indicate niche providers with specific use cases",
                "Context and use-case specificity required for interpretation",
            ],
        )


# =============================================================================
# UNIFIED COSURVIVAL JSON OUTPUT
# =============================================================================


@dataclass
class CosurvivalMVPOutput:
    """Unified output combining all three MVPs."""

    version: str = "1.0.0"
    generated_at: str = ""

    # Governance
    governance_passed: bool = True
    risk_flags: List[str] = field(default_factory=list)
    review_required: bool = False

    # Entity counts
    entities: Dict[str, int] = field(default_factory=dict)

    # MVP outputs
    tribe: Optional[TribeMVPOutput] = None
    teacher: Optional[TeacherMVPOutput] = None
    reconsumeralization: Optional[ReconMVPOutput] = None

    # Cross-system insights
    integration_insights: List[Dict[str, Any]] = field(default_factory=list)


def generate_cosurvival_json(
    tribe_output: TribeMVPOutput,
    teacher_output: TeacherMVPOutput,
    recon_output: ReconMVPOutput,
    governance_report: Optional[Dict[str, Any]] = None,
) -> Dict[str, Any]:
    """
    Generate the unified Cosurvival JSON structure.
    """

    # Cross-system insights
    insights = []

    # Insight: Mentor candidates who could teach missing skills
    if tribe_output.mentor_candidates and teacher_output.org_skill_gaps:
        for mentor in tribe_output.mentor_candidates[:5]:
            mentor_skills = set()  # Would need skill lookup
            for company_id, gaps in teacher_output.org_skill_gaps.items():
                if mentor.company_id == company_id:
                    insights.append(
                        {
                            "type": "mentorship_opportunity",
                            "description": f"User {mentor.user_id[:8]}... could help address {len(gaps)} skill gaps in their organization",
                            "priority": "medium",
                        }
                    )

    # Insight: Friction points affecting specific communities
    if tribe_output.communities and recon_output.friction_points:
        insights.append(
            {
                "type": "friction_community_impact",
                "description": f"{len(recon_output.friction_points)} provider friction points may affect {len(tribe_output.communities)} communities",
                "priority": "high",
            }
        )

    return {
        "version": "1.0.0",
        "generated_at": datetime.now().isoformat(),
        "governance": {
            "passed": governance_report.get("overall_passed", True) if governance_report else True,
            "risk_flags": governance_report.get("risk_flags", []) if governance_report else [],
            "review_required": governance_report.get("review_required", False)
            if governance_report
            else False,
        },
        "entities": {
            "users": tribe_output.total_users,
            "companies": tribe_output.total_companies,
            "groups": tribe_output.total_groups,
            "providers": len(recon_output.provider_scores),
        },
        "tribe": asdict(tribe_output),
        "teacher": asdict(teacher_output),
        "reconsumeralization": asdict(recon_output),
        "integration_insights": insights,
    }


# =============================================================================
# MAIN ENTRY POINT
# =============================================================================


def run_mvp_extraction(
    users: Dict[str, CanonicalUser],
    companies: Dict[str, CanonicalCompany],
    groups: Dict[str, CanonicalGroup],
    providers: Dict[str, CanonicalProvider],
    activities: List[CanonicalActivity],
    permission_changes: List[CanonicalPermissionChange],
    output_path: str = "cosurvival_mvp.json",
    governance_report: Optional[Dict[str, Any]] = None,
) -> Dict[str, Any]:
    """
    Run all MVP extractions and generate unified output.
    """
    print("\n" + "=" * 60)
    print("  COSURVIVAL MVP EXTRACTION")
    print("  Small wins that prove the system works")
    print("=" * 60)

    # TRIBE MVP
    tribe_extractor = TribeMVPExtractor()
    tribe_extractor.load_data(users, companies, groups, activities)
    tribe_output = tribe_extractor.extract()

    # TEACHER MVP
    teacher_extractor = TeacherMVPExtractor()
    teacher_extractor.load_data(users, activities, permission_changes)
    teacher_output = teacher_extractor.extract()

    # RECON MVP
    recon_extractor = ReconMVPExtractor()
    recon_extractor.load_data(providers, companies, activities)
    recon_output = recon_extractor.extract()

    # Generate unified output
    print("\n📦 Generating unified Cosurvival JSON...")
    cosurvival_json = generate_cosurvival_json(
        tribe_output, teacher_output, recon_output, governance_report
    )

    # Save to file
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(cosurvival_json, f, indent=2, default=str)

    print(f"✓ Saved to {output_path}")

    # Print summary
    print("\n" + "=" * 60)
    print("  MVP EXTRACTION COMPLETE")
    print("=" * 60)
    print(f"\n  TRIBE MVP:")
    print(f"    • {tribe_output.total_users} users in {len(tribe_output.communities)} communities")
    print(f"    • {len(tribe_output.cross_silo_bridges)} bridge connectors")
    print(f"    • {len(tribe_output.mentor_candidates)} mentor candidates")

    print(f"\n  TEACHER MVP:")
    print(
        f"    • {len(tribe_output.communities)} roles with {teacher_output.total_recommendations_generated} recommendations"
    )
    print(f"    • {len(teacher_output.skill_progressions)} skill progressions tracked")
    print(f"    • {len(teacher_output.org_skill_gaps)} organizations with identified gaps")

    print(f"\n  RECONSUMERALIZATION MVP:")
    print(f"    • {len(recon_output.provider_scores)} providers scored")
    print(f"    • Top providers: {', '.join(recon_output.top_providers[:3])}")
    print(f"    • {len(recon_output.friction_points)} friction points identified")

    print(f"\n  Integration insights: {len(cosurvival_json['integration_insights'])}")

    return cosurvival_json


if __name__ == "__main__":
    print("MVP Extractors module loaded.")
    print("Use run_mvp_extraction() with canonical data from ingestion pipeline.")
