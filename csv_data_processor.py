#!/usr/bin/env python3
"""
COSURVIVAL DATA PROCESSOR
=========================
Transforms activity/audit log data into the three interconnected systems:
- TRIBE: Social network mapping
- TEACHER: Educational pathway extraction  
- RECONSUMERALIZATION: Value exchange tracking

Author: Cosurvival Initiative
"""

import pandas as pd
import numpy as np
import json
from collections import defaultdict
from datetime import datetime
from pathlib import Path
import networkx as nx
from typing import Dict, List, Any, Optional, Tuple
import warnings

from governance import GovernanceGate, PIIHandler

warnings.filterwarnings("ignore")


class CosurvivalDataProcessor:
    """
    Main processor that transforms raw activity data into
    the three pillars of the Cosurvival system.
    """

    def __init__(self, csv_path: str):
        """Initialize with path to Brian's activity CSV."""
        self.csv_path = Path(csv_path)
        self.df = None
        self.tribe_graph = nx.Graph()
        self.tribe_data = {}
        self.teacher_data = {}
        self.recon_data = {}
        self.governance_gate = GovernanceGate(PIIHandler())
        self.governance_report = None

    def load_data(self) -> pd.DataFrame:
        """Load and preprocess the CSV data."""
        print(f"📁 Loading data from {self.csv_path}...")

        # Try multiple encodings
        for encoding in ["utf-8", "latin-1", "cp1252", "iso-8859-1"]:
            try:
                self.df = pd.read_csv(self.csv_path, encoding=encoding, low_memory=False)
                print(
                    f"   ✓ Loaded {len(self.df):,} activities with {len(self.df.columns)} columns"
                )
                break
            except UnicodeDecodeError:
                continue
            except Exception as e:
                print(f"   ✗ Error with {encoding}: {e}")

        if self.df is None:
            raise ValueError(f"Could not load CSV from {self.csv_path}")

        # Standardize column names (handle variations)
        self.df.columns = self.df.columns.str.strip()

        # Print detected columns for mapping
        print(f"\n📊 Detected Columns:\n   {list(self.df.columns)[:20]}...")

        self._run_governance_check()

        return self.df

    def _run_governance_check(self) -> None:
        """Run governance gate to ensure data meets safety requirements."""

        if self.df is None:
            return

        analysis_intents = [
            "tribe_network_mapping",
            "teacher_learning_paths",
            "recon_provider_scoring",
        ]
        output_types = [
            "community_detection",
            "skill_progression",
            "provider_reliability",
        ]

        report = self.governance_gate.run_full_check(
            self.df,
            analysis_intents=analysis_intents,
            output_types=output_types,
        )
        self.governance_report = report.to_dict()

        if not report.overall_passed:
            raise RuntimeError(
                "Governance gate blocked processing. Review governance_report for remediation."
            )

    def _find_column(self, patterns: List[str]) -> Optional[str]:
        """Find a column matching any of the given patterns (case-insensitive)."""
        for pattern in patterns:
            for col in self.df.columns:
                if pattern.lower() in col.lower():
                    return col
        return None

    def _get_column_mapping(self) -> Dict[str, str]:
        """Auto-detect column mappings based on common patterns."""
        mappings = {
            "uid": self._find_column(["uid", "userid", "user_id", "useridentifier"]),
            "name": self._find_column(["name", "username", "displayname", "fullname"]),
            "email": self._find_column(["email", "mail", "emailaddress"]),
            "company_id": self._find_column(["companyid", "company_id", "orgid", "organizationid"]),
            "company_name": self._find_column(
                ["companyname", "company_name", "orgname", "organization"]
            ),
            "group_id": self._find_column(["groupid", "group_id", "teamid"]),
            "group_name": self._find_column(["groupname", "group_name", "teamname"]),
            "provider_id": self._find_column(["pid", "providerid", "provider_id", "serviceid"]),
            "provider_name": self._find_column(["providername", "provider_name", "servicename"]),
            "role_id": self._find_column(["roleid", "role_id"]),
            "role_name": self._find_column(["rolename", "role_name", "role"]),
            "privilege": self._find_column(["privilege", "privileges", "permission", "access"]),
            "activity_type": self._find_column(["type", "activitytype", "action", "eventtype"]),
            "date": self._find_column(["date", "timestamp", "datetime", "created", "time"]),
            "state_old": self._find_column(["stateold", "state_old", "previousstate", "oldstate"]),
            "state_new": self._find_column(["statenew", "state_new", "newstate", "currentstate"]),
            "uid_opp": self._find_column(["uidopp", "uid_opp", "opposinguser", "targetuser"]),
            "uid_req": self._find_column(["uidreq", "uid_req", "requestinguser", "initiator"]),
            "path": self._find_column(["path", "filepath", "resource", "listpathactual"]),
            "scheme": self._find_column(["scheme", "protocol", "method"]),
            "error_code": self._find_column(["codeerror", "error", "errorcode", "error_code"]),
            "internal": self._find_column(["internal", "isinternal", "is_internal"]),
        }

        # Filter out None values and report
        found = {k: v for k, v in mappings.items() if v is not None}
        print(f"\n🔗 Auto-detected {len(found)}/{len(mappings)} column mappings:")
        for key, col in found.items():
            print(f"   {key}: {col}")

        return mappings

    # =========================================================================
    # TRIBE PROCESSING - Social Network Analysis
    # =========================================================================

    def process_tribe(self) -> Dict[str, Any]:
        """
        Extract TRIBE data: social network, organizational structure,
        and relationship patterns.
        """
        print("\n🌐 Processing TRIBE (Social Network)...")
        cols = self._get_column_mapping()

        # Initialize tribe structure
        self.tribe_data = {
            "users": {},
            "companies": {},
            "groups": {},
            "relationships": [],
            "communities": [],
            "stats": {},
        }

        # Extract unique users
        if cols["uid"]:
            users = (
                self.df.groupby(cols["uid"])
                .agg(
                    {
                        col: "first"
                        for col in [
                            cols["name"],
                            cols["email"],
                            cols["company_id"],
                            cols["role_id"],
                        ]
                        if col is not None
                    }
                )
                .reset_index()
            )

            for _, row in users.iterrows():
                uid = str(row[cols["uid"]])
                self.tribe_data["users"][uid] = {
                    "id": uid,
                    "name": row.get(cols["name"], "Unknown") if cols["name"] else "Unknown",
                    "email": row.get(cols["email"], "") if cols["email"] else "",
                    "company_id": str(row.get(cols["company_id"], ""))
                    if cols["company_id"]
                    else "",
                    "connections": [],
                    "activity_count": len(self.df[self.df[cols["uid"]] == row[cols["uid"]]]),
                    "roles": [],
                    "groups": [],
                }
                self.tribe_graph.add_node(uid, type="user")

            print(f"   ✓ Extracted {len(self.tribe_data['users']):,} unique users")

        # Extract companies/organizations
        if cols["company_id"] and cols["company_name"]:
            companies = (
                self.df.groupby(cols["company_id"])
                .agg({cols["company_name"]: "first"})
                .reset_index()
            )

            for _, row in companies.iterrows():
                cid = str(row[cols["company_id"]])
                if pd.notna(cid) and cid != "nan":
                    self.tribe_data["companies"][cid] = {
                        "id": cid,
                        "name": str(row[cols["company_name"]]),
                        "users": [],
                        "groups": [],
                        "activity_count": len(
                            self.df[self.df[cols["company_id"]] == row[cols["company_id"]]]
                        ),
                    }
                    self.tribe_graph.add_node(f"company_{cid}", type="company")

            print(f"   ✓ Extracted {len(self.tribe_data['companies']):,} companies")

        # Extract groups
        if cols["group_id"] and cols["group_name"]:
            groups = (
                self.df.groupby(cols["group_id"])
                .agg(
                    {
                        cols["group_name"]: "first",
                        cols["company_id"]: "first" if cols["company_id"] else None,
                    }.items()
                )
                .reset_index()
                if cols["company_id"]
                else self.df.groupby(cols["group_id"])
                .agg({cols["group_name"]: "first"})
                .reset_index()
            )

            for _, row in groups.iterrows():
                gid = str(row[cols["group_id"]])
                if pd.notna(gid) and gid != "nan":
                    self.tribe_data["groups"][gid] = {
                        "id": gid,
                        "name": str(row[cols["group_name"]]),
                        "company_id": str(row.get(cols["company_id"], ""))
                        if cols["company_id"]
                        else "",
                        "members": [],
                        "activity_count": 0,
                    }

            print(f"   ✓ Extracted {len(self.tribe_data['groups']):,} groups")

        # Build relationship edges from interactions
        if cols["uid"] and cols["uid_opp"]:
            interactions = self.df[[cols["uid"], cols["uid_opp"]]].dropna()
            edge_weights = defaultdict(int)

            for _, row in interactions.iterrows():
                u1, u2 = str(row[cols["uid"]]), str(row[cols["uid_opp"]])
                if u1 != u2:
                    edge_key = tuple(sorted([u1, u2]))
                    edge_weights[edge_key] += 1

            for (u1, u2), weight in edge_weights.items():
                self.tribe_graph.add_edge(u1, u2, weight=weight, type="collaboration")
                self.tribe_data["relationships"].append(
                    {"source": u1, "target": u2, "weight": weight, "type": "collaboration"}
                )

            print(
                f"   ✓ Found {len(self.tribe_data['relationships']):,} collaboration relationships"
            )

        # Detect communities using Louvain algorithm if available
        try:
            from networkx.algorithms import community

            if len(self.tribe_graph.nodes()) > 2:
                communities = community.greedy_modularity_communities(self.tribe_graph)
                for i, comm in enumerate(communities):
                    self.tribe_data["communities"].append(
                        {"id": i, "members": list(comm), "size": len(comm)}
                    )
                print(f"   ✓ Detected {len(self.tribe_data['communities'])} communities")
        except Exception as e:
            print(f"   ⚠ Community detection skipped: {e}")

        # Calculate network statistics
        if len(self.tribe_graph.nodes()) > 0:
            self.tribe_data["stats"] = {
                "total_nodes": self.tribe_graph.number_of_nodes(),
                "total_edges": self.tribe_graph.number_of_edges(),
                "density": nx.density(self.tribe_graph) if len(self.tribe_graph.nodes()) > 1 else 0,
                "avg_clustering": nx.average_clustering(self.tribe_graph)
                if len(self.tribe_graph.nodes()) > 2
                else 0,
                "connected_components": nx.number_connected_components(self.tribe_graph),
            }
            print(
                f"   ✓ Network: {self.tribe_data['stats']['total_nodes']} nodes, "
                f"{self.tribe_data['stats']['total_edges']} edges, "
                f"density={self.tribe_data['stats']['density']:.4f}"
            )

        return self.tribe_data

    # =========================================================================
    # TEACHER PROCESSING - Learning Pathway Extraction
    # =========================================================================

    def process_teacher(self) -> Dict[str, Any]:
        """
        Extract TEACHER data: learning pathways, skill progressions,
        and educational recommendations.
        """
        print("\n📚 Processing TEACHER (Learning Pathways)...")
        cols = self._get_column_mapping()

        self.teacher_data = {
            "roles": {},
            "skills": {},
            "progressions": [],
            "learning_paths": {},
            "recommendations": [],
            "technology_curriculum": {},
            "stats": {},
        }

        # Extract roles and their skill requirements
        if cols["role_id"] and cols["role_name"]:
            roles = self.df.groupby(cols["role_id"]).agg({cols["role_name"]: "first"}).reset_index()

            for _, row in roles.iterrows():
                rid = str(row[cols["role_id"]])
                if pd.notna(rid) and rid != "nan":
                    role_activities = self.df[self.df[cols["role_id"]] == row[cols["role_id"]]]

                    # Get privileges/skills for this role
                    privileges = []
                    if cols["privilege"]:
                        privileges = role_activities[cols["privilege"]].dropna().unique().tolist()

                    # Get providers used by this role
                    providers = []
                    if cols["provider_name"]:
                        providers = (
                            role_activities[cols["provider_name"]].dropna().unique().tolist()
                        )

                    self.teacher_data["roles"][rid] = {
                        "id": rid,
                        "name": str(row[cols["role_name"]]),
                        "required_skills": privileges[:10],  # Top 10
                        "technology_stack": providers[:10],  # Top 10
                        "user_count": role_activities[cols["uid"]].nunique() if cols["uid"] else 0,
                        "activity_types": role_activities[cols["activity_type"]]
                        .value_counts()
                        .head(5)
                        .to_dict()
                        if cols["activity_type"]
                        else {},
                    }

            print(f"   ✓ Extracted {len(self.teacher_data['roles'])} role-based learning tracks")

        # Extract skill progressions (state transitions)
        if cols["state_old"] and cols["state_new"] and cols["uid"]:
            transitions = self.df[[cols["uid"], cols["state_old"], cols["state_new"]]].dropna()

            progression_counts = defaultdict(int)
            user_progressions = defaultdict(list)

            for _, row in transitions.iterrows():
                uid = str(row[cols["uid"]])
                old_state = str(row[cols["state_old"]])
                new_state = str(row[cols["state_new"]])

                if old_state != new_state:
                    key = f"{old_state} → {new_state}"
                    progression_counts[key] += 1
                    user_progressions[uid].append({"from": old_state, "to": new_state})

            # Top progressions as learning pathways
            for progression, count in sorted(
                progression_counts.items(), key=lambda x: x[1], reverse=True
            )[:20]:
                self.teacher_data["progressions"].append(
                    {
                        "transition": progression,
                        "count": count,
                        "significance": "high"
                        if count > 100
                        else "medium"
                        if count > 10
                        else "low",
                    }
                )

            print(
                f"   ✓ Identified {len(progression_counts)} state transitions (learning milestones)"
            )

        # Build technology curriculum from provider usage
        if cols["provider_name"] and cols["role_id"]:
            provider_by_role = (
                self.df.groupby([cols["role_id"], cols["provider_name"]])
                .size()
                .reset_index(name="usage_count")
            )

            for rid in self.teacher_data["roles"].keys():
                role_providers = provider_by_role[
                    provider_by_role[cols["role_id"]].astype(str) == rid
                ].nlargest(5, "usage_count")

                self.teacher_data["technology_curriculum"][rid] = [
                    {
                        "provider": row[cols["provider_name"]],
                        "priority": i + 1,
                        "usage": row["usage_count"],
                    }
                    for i, (_, row) in enumerate(role_providers.iterrows())
                ]

            print(
                f"   ✓ Generated technology curriculum for {len(self.teacher_data['technology_curriculum'])} roles"
            )

        # Generate learning recommendations based on peer comparison
        if cols["uid"] and cols["role_id"] and cols["privilege"]:
            user_skills = (
                self.df.groupby(cols["uid"])[cols["privilege"]]
                .apply(lambda x: set(x.dropna()))
                .to_dict()
            )

            role_skills = (
                self.df.groupby(cols["role_id"])[cols["privilege"]]
                .apply(lambda x: set(x.dropna()))
                .to_dict()
            )

            # For each user, find skill gaps compared to role peers
            sample_users = list(user_skills.keys())[:100]  # Sample for performance

            for uid in sample_users:
                user_role = (
                    self.df[self.df[cols["uid"]] == uid][cols["role_id"]].iloc[0]
                    if len(self.df[self.df[cols["uid"]] == uid]) > 0
                    else None
                )

                if user_role and user_role in role_skills:
                    missing_skills = role_skills[user_role] - user_skills.get(uid, set())
                    if missing_skills:
                        self.teacher_data["recommendations"].append(
                            {
                                "user_id": str(uid),
                                "recommended_skills": list(missing_skills)[:5],
                                "reason": "Skill gap compared to role peers",
                                "priority": "high" if len(missing_skills) > 3 else "medium",
                            }
                        )

            print(
                f"   ✓ Generated {len(self.teacher_data['recommendations'])} personalized recommendations"
            )

        # Calculate teaching statistics
        self.teacher_data["stats"] = {
            "total_roles": len(self.teacher_data["roles"]),
            "total_progressions": len(self.teacher_data["progressions"]),
            "users_with_recommendations": len(self.teacher_data["recommendations"]),
            "technology_modules": sum(
                len(v) for v in self.teacher_data["technology_curriculum"].values()
            ),
        }

        return self.teacher_data

    # =========================================================================
    # RECONSUMERALIZATION PROCESSING - Value Exchange Tracking
    # =========================================================================

    def process_reconsumeralization(self) -> Dict[str, Any]:
        """
        Extract RECONSUMERALIZATION data: provider profiles, consumer patterns,
        value flows, and ethics metrics.
        """
        print("\n💱 Processing RECONSUMERALIZATION (Value Exchange)...")
        cols = self._get_column_mapping()

        self.recon_data = {
            "providers": {},
            "consumers": {},
            "value_flows": [],
            "ethics_scores": {},
            "quality_metrics": {},
            "stats": {},
        }

        # Extract provider profiles
        if cols["provider_id"] and cols["provider_name"]:
            providers = (
                self.df.groupby(cols["provider_id"])
                .agg({cols["provider_name"]: "first"})
                .reset_index()
            )

            for _, row in providers.iterrows():
                pid = str(row[cols["provider_id"]])
                if pd.notna(pid) and pid != "nan":
                    provider_activities = self.df[
                        self.df[cols["provider_id"]] == row[cols["provider_id"]]
                    ]

                    # Calculate quality metrics
                    total_activities = len(provider_activities)
                    error_count = 0
                    if cols["error_code"]:
                        error_count = provider_activities[cols["error_code"]].notna().sum()

                    # Get schemes/services offered
                    schemes = []
                    if cols["scheme"]:
                        schemes = provider_activities[cols["scheme"]].dropna().unique().tolist()

                    # Get customer companies
                    customers = []
                    if cols["company_id"]:
                        customers = (
                            provider_activities[cols["company_id"]].dropna().unique().tolist()
                        )

                    # Get user count
                    user_count = 0
                    if cols["uid"]:
                        user_count = provider_activities[cols["uid"]].nunique()

                    self.recon_data["providers"][pid] = {
                        "id": pid,
                        "name": str(row[cols["provider_name"]]),
                        "services": schemes[:10],
                        "customer_count": len(customers),
                        "user_count": user_count,
                        "activity_volume": total_activities,
                        "error_rate": error_count / total_activities if total_activities > 0 else 0,
                        "reliability_score": 1 - (error_count / total_activities)
                        if total_activities > 0
                        else 1,
                        "transparency_score": 0.85,  # Placeholder - would be calculated from audit completeness
                        "ethics_rating": "A",  # Placeholder - would be calculated from multiple factors
                    }

            print(f"   ✓ Profiled {len(self.recon_data['providers'])} providers/suppliers")

        # Extract consumer (company) profiles
        if cols["company_id"] and cols["company_name"]:
            companies = (
                self.df.groupby(cols["company_id"])
                .agg({cols["company_name"]: "first"})
                .reset_index()
            )

            for _, row in companies.iterrows():
                cid = str(row[cols["company_id"]])
                if pd.notna(cid) and cid != "nan":
                    company_activities = self.df[
                        self.df[cols["company_id"]] == row[cols["company_id"]]
                    ]

                    # Get providers used
                    providers_used = []
                    if cols["provider_name"]:
                        providers_used = (
                            company_activities[cols["provider_name"]].dropna().unique().tolist()
                        )

                    # Get user count
                    user_count = 0
                    if cols["uid"]:
                        user_count = company_activities[cols["uid"]].nunique()

                    # Get group count
                    group_count = 0
                    if cols["group_id"]:
                        group_count = company_activities[cols["group_id"]].nunique()

                    self.recon_data["consumers"][cid] = {
                        "id": cid,
                        "name": str(row[cols["company_name"]]),
                        "providers_used": providers_used[:15],
                        "total_users": user_count,
                        "total_groups": group_count,
                        "activity_volume": len(company_activities),
                        "technology_adoption_score": len(providers_used) / 10,  # Normalized
                        "collaboration_score": 0.75,  # Placeholder
                        "transparency_score": 0.80,  # Placeholder
                    }

            print(f"   ✓ Profiled {len(self.recon_data['consumers'])} consumers/companies")

        # Calculate value flows
        if cols["provider_id"] and cols["company_id"]:
            flows = (
                self.df.groupby([cols["provider_id"], cols["company_id"]])
                .size()
                .reset_index(name="volume")
            )

            for _, row in flows.iterrows():
                pid = str(row[cols["provider_id"]])
                cid = str(row[cols["company_id"]])

                if pd.notna(pid) and pd.notna(cid) and pid != "nan" and cid != "nan":
                    # Get error rate for this specific flow
                    flow_data = self.df[
                        (self.df[cols["provider_id"]] == row[cols["provider_id"]])
                        & (self.df[cols["company_id"]] == row[cols["company_id"]])
                    ]

                    error_rate = 0
                    if cols["error_code"]:
                        error_rate = flow_data[cols["error_code"]].notna().sum() / len(flow_data)

                    self.recon_data["value_flows"].append(
                        {
                            "from_provider": pid,
                            "to_company": cid,
                            "volume": int(row["volume"]),
                            "quality": 1 - error_rate,
                            "value_score": int(row["volume"]) * (1 - error_rate),
                        }
                    )

            print(f"   ✓ Mapped {len(self.recon_data['value_flows'])} value flows")

        # Calculate aggregate ethics scores
        for pid, provider in self.recon_data["providers"].items():
            # Composite ethics score
            reliability = provider["reliability_score"]
            transparency = provider["transparency_score"]

            # Calculate ethics grade
            composite = (reliability * 0.4) + (transparency * 0.4) + 0.2  # Base score
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

            self.recon_data["ethics_scores"][pid] = {
                "provider_id": pid,
                "reliability": reliability,
                "transparency": transparency,
                "composite": composite,
                "grade": grade,
            }

        print(
            f"   ✓ Calculated ethics scores for {len(self.recon_data['ethics_scores'])} providers"
        )

        # Statistics
        self.recon_data["stats"] = {
            "total_providers": len(self.recon_data["providers"]),
            "total_consumers": len(self.recon_data["consumers"]),
            "total_value_flows": len(self.recon_data["value_flows"]),
            "total_value_exchanged": sum(f["volume"] for f in self.recon_data["value_flows"]),
            "avg_provider_reliability": np.mean(
                [p["reliability_score"] for p in self.recon_data["providers"].values()]
            )
            if self.recon_data["providers"]
            else 0,
            "ethics_grades": {
                grade: len(
                    [s for s in self.recon_data["ethics_scores"].values() if s["grade"] == grade]
                )
                for grade in ["A", "B", "C", "D", "F"]
            },
        }

        return self.recon_data

    # =========================================================================
    # INTEGRATION & OUTPUT
    # =========================================================================

    def process_all(self) -> Dict[str, Any]:
        """Process all three systems and return integrated data."""
        self.load_data()

        tribe = self.process_tribe()
        teacher = self.process_teacher()
        recon = self.process_reconsumeralization()

        # Generate integration insights
        insights = self._generate_integration_insights()

        return {
            "tribe": tribe,
            "teacher": teacher,
            "reconsumeralization": recon,
            "integration": insights,
            "metadata": {
                "source_file": str(self.csv_path),
                "total_activities": len(self.df),
                "total_columns": len(self.df.columns),
                "processed_at": datetime.now().isoformat(),
            },
        }

    def _generate_integration_insights(self) -> Dict[str, Any]:
        """Generate insights from the integration of all three systems."""
        insights = {"feedback_loops": [], "cross_system_connections": [], "recommendations": []}

        # Find users who could be mentors (high activity + diverse skills)
        mentor_candidates = []
        for uid, user in self.tribe_data.get("users", {}).items():
            if user["activity_count"] > 100:  # High activity
                mentor_candidates.append(
                    {
                        "user_id": uid,
                        "activity_count": user["activity_count"],
                        "reason": "High activity user - potential mentor",
                    }
                )

        if mentor_candidates:
            insights["recommendations"].append(
                {
                    "type": "mentorship",
                    "candidates": mentor_candidates[:10],
                    "description": "Users with high activity who could mentor others",
                }
            )

        # Find providers that need attention (low reliability)
        for pid, provider in self.recon_data.get("providers", {}).items():
            if provider["reliability_score"] < 0.9:
                insights["recommendations"].append(
                    {
                        "type": "provider_attention",
                        "provider_id": pid,
                        "provider_name": provider["name"],
                        "reliability": provider["reliability_score"],
                        "description": f"Provider {provider['name']} has {provider['reliability_score']:.1%} reliability",
                    }
                )

        # Identify learning opportunities from progressions
        for progression in self.teacher_data.get("progressions", [])[:5]:
            insights["feedback_loops"].append(
                {
                    "type": "skill_progression",
                    "transition": progression["transition"],
                    "frequency": progression["count"],
                    "description": f"Common skill progression: {progression['transition']}",
                }
            )

        return insights

    def export_json(self, output_path: str = "cosurvival_data.json"):
        """Export processed data to JSON for visualization."""
        data = self.process_all()

        # Convert sets to lists for JSON serialization
        def convert_sets(obj):
            if isinstance(obj, set):
                return list(obj)
            elif isinstance(obj, dict):
                return {k: convert_sets(v) for k, v in obj.items()}
            elif isinstance(obj, list):
                return [convert_sets(item) for item in obj]
            return obj

        data = convert_sets(data)

        with open(output_path, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2, default=str)

        print(f"\n✅ Exported data to {output_path}")
        return output_path

    def export_network_graph(self, output_path: str = "tribe_network.json"):
        """Export network graph in format suitable for D3.js visualization."""
        nodes = []
        links = []

        # Add user nodes
        for uid, user in self.tribe_data.get("users", {}).items():
            nodes.append(
                {
                    "id": uid,
                    "name": user["name"],
                    "type": "user",
                    "size": min(user["activity_count"] / 10, 50),  # Normalize size
                    "company": user.get("company_id", ""),
                }
            )

        # Add company nodes
        for cid, company in self.tribe_data.get("companies", {}).items():
            nodes.append(
                {"id": f"company_{cid}", "name": company["name"], "type": "company", "size": 30}
            )

        # Add relationship links
        for rel in self.tribe_data.get("relationships", []):
            links.append(
                {
                    "source": rel["source"],
                    "target": rel["target"],
                    "weight": rel["weight"],
                    "type": rel["type"],
                }
            )

        graph_data = {"nodes": nodes, "links": links}

        with open(output_path, "w", encoding="utf-8") as f:
            json.dump(graph_data, f, indent=2)

        print(f"✅ Exported network graph to {output_path}")
        return output_path


def main():
    """Main entry point."""
    import sys

    if len(sys.argv) < 2:
        print("Usage: python csv_data_processor.py <path_to_csv>")
        print("\nExample: python csv_data_processor.py brian_activity_data.csv")
        print("\nThis will process the CSV and generate:")
        print("  - cosurvival_data.json (complete processed data)")
        print("  - tribe_network.json (network graph for visualization)")
        sys.exit(1)

    csv_path = sys.argv[1]

    print("=" * 60)
    print("  COSURVIVAL DATA PROCESSOR")
    print("  Transforming Activity Data into Connected Intelligence")
    print("=" * 60)

    processor = CosurvivalDataProcessor(csv_path)

    # Process and export
    processor.export_json("cosurvival_data.json")
    processor.export_network_graph("tribe_network.json")

    print("\n" + "=" * 60)
    print("  PROCESSING COMPLETE")
    print("=" * 60)
    print("\nNext steps:")
    print("1. Open the dashboard: python -m http.server 8000")
    print("2. Navigate to http://localhost:8000/dashboard.html")
    print("3. Load the generated JSON files")


if __name__ == "__main__":
    main()
