#!/usr/bin/env python3
"""
TEACHER Week 1: Hello, World (Data Edition)
===========================================
The three-lens demo that shows how the same data means different things
depending on which perspective you use.

This is the "Hello, World" equivalent for COSURVIVAL.
"""

from typing import Dict, Any, List
from datetime import datetime


# =============================================================================
# THE DATA: One Activity Row
# =============================================================================

SAMPLE_ACTIVITY = {
    "Uid": "user_alice",
    "UidOpp": "user_bob",
    "Type": "document_share",
    "Date": "2024-01-15T10:30:00Z",
    "CompanyId": "org_techcorp",
    "GroupId": "team_alpha",
    "StateOld": "viewer",
    "StateNew": "editor",
    "ResourcePath": "/projects/secret/budget.xlsx",
    "ProviderId": "provider_sharepoint",
    "ErrorCode": None,
}


# =============================================================================
# LENS 1: TRIBE (Social Network)
# =============================================================================


def interpret_tribe(activity: Dict[str, Any]) -> Dict[str, Any]:
    """
    Interpret activity through the TRIBE lens.

    Focus: Who is connected to whom?
    """
    key_insights: List[str] = []
    graph_elements: Dict[str, Any] = {}

    interpretation: Dict[str, Any] = {
        "lens": "TRIBE",
        "focus": "Social connections and collaboration patterns",
        "key_insights": key_insights,
        "graph_elements": graph_elements,
    }

    # Extract relationship
    user_a = activity.get("Uid")
    user_b = activity.get("UidOpp")

    if user_a and user_b:
        key_insights.append(f"{user_a} interacted with {user_b}")
        graph_elements["edge"] = {
            "source": user_a,
            "target": user_b,
            "type": "collaboration",
            "weight": 1,
            "evidence": f"Document share on {activity.get('Date')}",
        }

    # Extract group context
    group_id = activity.get("GroupId")
    if group_id:
        key_insights.append(f"Both users are in {group_id}")
        graph_elements["group"] = group_id

    # Extract company context
    company_id = activity.get("CompanyId")
    if company_id:
        key_insights.append(f"Activity occurred within {company_id}")
        graph_elements["company"] = company_id

    return interpretation


# =============================================================================
# LENS 2: TEACHER (Learning Pathways)
# =============================================================================


def interpret_teacher(activity: Dict[str, Any]) -> Dict[str, Any]:
    """
    Interpret activity through the TEACHER lens.

    Focus: Who is growing in what ways?
    """
    key_insights: List[str] = []
    learning_signals: Dict[str, Any] = {}

    interpretation: Dict[str, Any] = {
        "lens": "TEACHER",
        "focus": "Skill growth and learning progressions",
        "key_insights": key_insights,
        "learning_signals": learning_signals,
    }

    # Extract permission change (skill growth signal)
    state_old = activity.get("StateOld")
    state_new = activity.get("StateNew")

    if state_old and state_new and state_old != state_new:
        key_insights.append(f"Permission upgrade: {state_old} -> {state_new}")
        learning_signals["progression"] = {
            "from": state_old,
            "to": state_new,
            "meaning": f"Grew from {state_old} to {state_new}",
            "skill_acquired": f"Ability to {state_new} (previously only {state_old})",
        }

    # Extract activity type as skill demonstration
    activity_type = activity.get("Type")
    if activity_type:
        key_insights.append(f"Demonstrated skill: {activity_type}")
        learning_signals["activity_skill"] = activity_type

    # Extract collaboration as learning opportunity
    user_opp = activity.get("UidOpp")
    if user_opp:
        key_insights.append(f"Learning from collaboration with {user_opp}")
        learning_signals["collaboration_learning"] = {
            "peer": user_opp,
            "type": "document_share",
            "opportunity": "Learning through shared resources",
        }

    return interpretation


# =============================================================================
# LENS 3: RECONSUMERALIZATION (Value Exchange)
# =============================================================================


def interpret_recon(activity: Dict[str, Any]) -> Dict[str, Any]:
    """
    Interpret activity through the RECONSUMERALIZATION lens.

    Focus: Who is providing value ethically?
    """
    key_insights: List[str] = []
    value_flows: Dict[str, Any] = {}

    interpretation: Dict[str, Any] = {
        "lens": "RECONSUMERALIZATION",
        "focus": "Ethical value exchange and provider quality",
        "key_insights": key_insights,
        "value_flows": value_flows,
    }

    # Extract provider
    provider_id = activity.get("ProviderId")
    if provider_id:
        key_insights.append(f"Provider {provider_id} enabled this activity")
        value_flows["provider"] = {
            "id": provider_id,
            "service": "Document sharing platform",
            "value_provided": "Enabled collaboration and permission management",
        }

    # Extract company (consumer)
    company_id = activity.get("CompanyId")
    if company_id:
        key_insights.append(f"Company {company_id} consumed this service")
        value_flows["consumer"] = {
            "id": company_id,
            "value_received": "Platform enabled capability growth (viewer -> editor)",
        }

    # Extract quality signal
    error_code = activity.get("ErrorCode")
    if error_code:
        key_insights.append(f"⚠️ Error occurred: {error_code}")
        value_flows["quality"] = {
            "error": True,
            "error_code": error_code,
            "reliability_impact": "Negative - reduces provider score",
        }
    else:
        value_flows["quality"] = {
            "error": False,
            "reliability_impact": "Positive - successful transaction",
        }

    # Extract value type
    state_change = activity.get("StateOld") != activity.get("StateNew")
    if state_change:
        key_insights.append("Value type: Capability enablement (permission upgrade)")
        value_flows["value_type"] = "capability_growth"

    return interpretation


# =============================================================================
# UNIFIED INTERPRETATION
# =============================================================================


def interpret_unified(activity: Dict[str, Any]) -> Dict[str, Any]:
    """
    Interpret the same activity through all three lenses.

    This demonstrates the core COSURVIVAL principle:
    Same data, three perspectives, one unified system.
    """
    return {
        "activity": activity,
        "interpreted_at": datetime.now().isoformat(),
        "tribe": interpret_tribe(activity),
        "teacher": interpret_teacher(activity),
        "recon": interpret_recon(activity),
        "insight": "The same activity reveals different truths depending on the lens. Together, they form a complete picture.",
    }


# =============================================================================
# PRETTY PRINTING
# =============================================================================


def print_interpretation(interpretation: Dict[str, Any]):
    """Print a formatted interpretation."""
    print("=" * 70)
    print(f"  ACTIVITY: {interpretation['activity'].get('Type', 'Unknown')}")
    print(f"  Date: {interpretation['activity'].get('Date', 'Unknown')}")
    print("=" * 70)

    # TRIBE
    tribe = interpretation["tribe"]
    print(f"\n[TRIBE] LENS: {tribe['focus']}")
    print("-" * 70)
    for insight in tribe["key_insights"]:
        print(f"  * {insight}")
    if tribe.get("graph_elements"):
        print("  Graph Elements:")
        for key, value in tribe["graph_elements"].items():
            if isinstance(value, dict):
                print(f"    {key}: {value.get('source', '')} -> {value.get('target', '')}")
            else:
                print(f"    {key}: {value}")

    # TEACHER
    teacher = interpretation["teacher"]
    print(f"\n[TEACHER] LENS: {teacher['focus']}")
    print("-" * 70)
    for insight in teacher["key_insights"]:
        print(f"  * {insight}")
    if teacher.get("learning_signals"):
        print("  Learning Signals:")
        for key, value in teacher["learning_signals"].items():
            if isinstance(value, dict):
                if "from" in value and "to" in value:
                    print(f"    {key}: {value['from']} -> {value['to']}")
                else:
                    print(f"    {key}: {value}")
            else:
                print(f"    {key}: {value}")

    # RECON
    recon = interpretation["recon"]
    print(f"\n[RECON] LENS: {recon['focus']}")
    print("-" * 70)
    for insight in recon["key_insights"]:
        print(f"  * {insight}")
    if recon.get("value_flows"):
        print("  Value Flows:")
        for key, value in recon["value_flows"].items():
            if isinstance(value, dict):
                if "id" in value:
                    print(f"    {key}: {value['id']}")
                elif "error" in value:
                    status = "[ERROR]" if value["error"] else "[SUCCESS]"
                    print(f"    {key}: {status}")
                else:
                    print(f"    {key}: {value}")
            else:
                print(f"    {key}: {value}")

    print("\n" + "=" * 70)
    print(f"  {interpretation['insight']}")
    print("=" * 70)


# =============================================================================
# MAIN: The Demo
# =============================================================================


def main():
    """Run the Hello, World demo."""
    print("\n" + "=" * 70)
    print("  TEACHER Week 1: Hello, World (Data Edition)")
    print("  Same Data -> Three Lenses -> Unified Intelligence")
    print("=" * 70)

    print("\nINPUT DATA:")
    print("-" * 70)
    for key, value in SAMPLE_ACTIVITY.items():
        print(f"  {key}: {value}")

    print("\n\nINTERPRETING THROUGH THREE LENSES...")
    print("-" * 70)

    # Generate unified interpretation
    unified = interpret_unified(SAMPLE_ACTIVITY)

    # Print formatted output
    print_interpretation(unified)

    # Summary
    print("\n\nSUMMARY:")
    print("-" * 70)
    print("  TRIBE:   Found 1 collaboration edge (user_alice -> user_bob)")
    print("  TEACHER: Detected 1 skill progression (viewer -> editor)")
    print("  RECON:   Identified 1 value flow (provider_sharepoint -> org_techcorp)")
    print("\n  [OK] Same data. Three perspectives. One unified system.")
    print("\n" + "=" * 70)
    print("  This is COSURVIVAL.")
    print("=" * 70 + "\n")


if __name__ == "__main__":
    main()
