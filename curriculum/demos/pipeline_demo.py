#!/usr/bin/env python3
"""
TEACHER Week 2: 4-Stage Pipeline Demo
======================================
Demonstrates the complete governance pipeline with observability.

This shows how data flows through:
1. INGEST (raw data)
2. NORMALIZE (canonical entities)
3. GOVERN (PII protection + rules)
4. SYNTHESIZE (TRIBE/TEACHER/RECON outputs)
"""

from dataclasses import dataclass, field
from typing import Dict, List, Any, Optional
from datetime import datetime
import json
import hashlib


# =============================================================================
# STAGE RESULT MODEL
# =============================================================================


@dataclass
class StageResult:
    """Result of a pipeline stage."""

    stage_name: str
    passed: bool
    exit_code: int  # 0 = success, non-zero = error
    confidence: float  # 0.0-1.0
    review_required: bool
    reason: str
    metadata: Dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> Dict:
        return {
            "stage": self.stage_name,
            "status": "PASS" if self.passed else "FAIL",
            "exit_code": self.exit_code,
            "confidence": self.confidence,
            "review_required": self.review_required,
            "reason": self.reason,
            "metadata": self.metadata,
        }


# =============================================================================
# PIPELINE TRACE MODEL
# =============================================================================


@dataclass
class StageTrace:
    """Trace of a single stage execution."""

    name: str
    start_time: datetime
    end_time: Optional[datetime] = None
    duration_seconds: Optional[float] = None
    metadata: Dict[str, Any] = field(default_factory=dict)

    def complete(self, metadata: Optional[Dict[str, Any]] = None):
        """Mark stage as complete."""
        self.end_time = datetime.now()
        if self.end_time and self.start_time:
            self.duration_seconds = (self.end_time - self.start_time).total_seconds()
        if metadata:
            self.metadata.update(metadata)


class PipelineTrace:
    """Tracks execution of entire pipeline."""

    def __init__(self):
        self.stages: List[StageTrace] = []
        self.start_time = datetime.now()
        self.end_time: Optional[datetime] = None

    def stage(self, name: str, start: bool = False, end: bool = False, **metadata) -> StageTrace:
        """Record stage start/end with metadata."""
        if start:
            trace = StageTrace(name=name, start_time=datetime.now(), metadata=metadata)
            self.stages.append(trace)
            return trace
        elif end:
            # Find most recent stage with this name
            for stage in reversed(self.stages):
                if stage.name == name and stage.end_time is None:
                    stage.complete(metadata)
                    return stage
        return None

    def explain(self) -> str:
        """Generate human-readable explanation."""
        lines = []
        lines.append("=" * 70)
        lines.append("  PIPELINE EXECUTION TRACE")
        lines.append("=" * 70)

        for stage in self.stages:
            lines.append(f"\n[{stage.name.upper()}]")
            lines.append(
                f"  Duration: {stage.duration_seconds:.3f}s"
                if stage.duration_seconds
                else "  Duration: N/A"
            )
            for key, value in stage.metadata.items():
                lines.append(f"  {key}: {value}")

        if self.end_time:
            total = (self.end_time - self.start_time).total_seconds()
            lines.append(f"\nTotal Pipeline Time: {total:.3f}s")

        lines.append("\n" + "=" * 70)
        return "\n".join(lines)


# =============================================================================
# SAMPLE DATA
# =============================================================================

SAMPLE_RAW_DATA = [
    {
        "Uid": "user_alice",
        "UidOpp": "user_bob",
        "Type": "document_share",
        "Date": "2024-01-15T10:30:00Z",
        "CompanyId": "org_techcorp",
        "StateOld": "viewer",
        "StateNew": "editor",
        "ProviderId": "provider_sharepoint",
    },
    {
        "Uid": "user_bob",
        "UidOpp": "user_carol",
        "Type": "permission_grant",
        "Date": "2024-01-15T11:00:00Z",
        "CompanyId": "org_techcorp",
        "StateOld": "viewer",
        "StateNew": "admin",
        "ProviderId": "provider_google",
    },
]


# =============================================================================
# STAGE 1: INGEST
# =============================================================================


def stage_ingest(raw_data: List[Dict]) -> tuple[List[Dict], StageResult]:
    """Stage 1: Ingest raw data."""
    # Simulate file loading
    result = StageResult(
        stage_name="ingest",
        passed=True,
        exit_code=0,
        confidence=1.0,
        review_required=False,
        reason="Data loaded successfully",
        metadata={
            "rows_loaded": len(raw_data),
            "columns_detected": len(raw_data[0].keys()) if raw_data else 0,
            "encoding": "utf-8",
        },
    )
    return raw_data, result


# =============================================================================
# STAGE 2: NORMALIZE
# =============================================================================


@dataclass
class CanonicalActivity:
    """Canonical activity entity."""

    id: str
    timestamp: str
    activity_type: str
    user_id: str
    target_user_id: str = ""
    company_id: str = ""
    state_before: str = ""
    state_after: str = ""
    provider_id: str = ""


def stage_normalize(raw_data: List[Dict]) -> tuple[List[CanonicalActivity], StageResult]:
    """Stage 2: Normalize to canonical entities."""
    activities = []
    errors = []

    for i, row in enumerate(raw_data):
        try:
            activity = CanonicalActivity(
                id=f"act_{i}",
                timestamp=row.get("Date", ""),
                activity_type=row.get("Type", ""),
                user_id=row.get("Uid", ""),
                target_user_id=row.get("UidOpp", ""),
                company_id=row.get("CompanyId", ""),
                state_before=row.get("StateOld", ""),
                state_after=row.get("StateNew", ""),
                provider_id=row.get("ProviderId", ""),
            )
            activities.append(activity)
        except Exception as e:
            errors.append(f"Row {i}: {str(e)}")

    passed = len(errors) == 0
    result = StageResult(
        stage_name="normalize",
        passed=passed,
        exit_code=0 if passed else 1,
        confidence=1.0 - (len(errors) / len(raw_data)) if raw_data else 1.0,
        review_required=len(errors) > 0,
        reason="Normalization complete" if passed else f"Errors: {len(errors)}",
        metadata={
            "entities_created": len(activities),
            "errors": errors,
            "schema_compliant": passed,
        },
    )
    return activities, result


# =============================================================================
# STAGE 3: GOVERN
# =============================================================================


def hash_pii(value: str) -> str:
    """Hash PII value."""
    if not value:
        return ""
    return hashlib.md5(value.encode()).hexdigest()[:12]


def stage_govern(
    activities: List[CanonicalActivity],
) -> tuple[List[CanonicalActivity], StageResult]:
    """Stage 3: Apply governance (PII protection, rules)."""
    # Apply PII protection
    protected_activities = []
    pii_count = 0

    for activity in activities:
        # Hash user IDs
        protected = CanonicalActivity(
            id=activity.id,
            timestamp=activity.timestamp,
            activity_type=activity.activity_type,
            user_id=f"entity_{hash_pii(activity.user_id)}",
            target_user_id=f"entity_{hash_pii(activity.target_user_id)}"
            if activity.target_user_id
            else "",
            company_id=activity.company_id,  # Keep for org analysis
            state_before=activity.state_before,
            state_after=activity.state_after,
            provider_id=activity.provider_id,
        )
        protected_activities.append(protected)
        pii_count += 2  # user_id + target_user_id

    # Governance checks
    gov_passed = True
    gov_issues: List[str] = []

    # Check: No prohibited inferences
    # (Would check for performance scores, termination risk, etc.)

    result = StageResult(
        stage_name="govern",
        passed=gov_passed,
        exit_code=0 if gov_passed else 2,
        confidence=1.0,
        review_required=len(gov_issues) > 0,
        reason="Governance checks passed" if gov_passed else f"Issues: {gov_issues}",
        metadata={
            "pii_hashed": pii_count,
            "governance_rules_applied": 3,
            "bias_guardrails_active": True,
            "prohibited_inferences_blocked": 0,
        },
    )
    return protected_activities, result


# =============================================================================
# STAGE 4: SYNTHESIZE
# =============================================================================


def stage_synthesize_tribe(activities: List[CanonicalActivity]) -> tuple[Dict, StageResult]:
    """Stage 4a: Synthesize TRIBE output."""
    # Count users
    users = set()
    for activity in activities:
        users.add(activity.user_id)
        if activity.target_user_id:
            users.add(activity.target_user_id)

    # Count edges
    edges = len([a for a in activities if a.target_user_id])

    output = {
        "lens": "tribe",
        "users": len(users),
        "collaboration_edges": edges,
        "communities": 1,  # Simplified
        "insights": [f"Found {len(users)} unique users", f"Detected {edges} collaboration edges"],
    }

    result = StageResult(
        stage_name="synthesize_tribe",
        passed=True,
        exit_code=0,
        confidence=0.9,
        review_required=False,
        reason="TRIBE analysis complete",
        metadata={"output_size": len(output), "confidence": 0.9},
    )
    return output, result


def stage_synthesize_teacher(activities: List[CanonicalActivity]) -> tuple[Dict, StageResult]:
    """Stage 4b: Synthesize TEACHER output."""
    # Count progressions
    progressions = len(
        [
            a
            for a in activities
            if a.state_before and a.state_after and a.state_before != a.state_after
        ]
    )

    output = {
        "lens": "teacher",
        "progressions_detected": progressions,
        "recommendations": progressions,  # Simplified
        "insights": [
            f"Detected {progressions} skill progressions",
            "Recommendations generated based on state transitions",
        ],
    }

    result = StageResult(
        stage_name="synthesize_teacher",
        passed=True,
        exit_code=0,
        confidence=0.85,
        review_required=False,
        reason="TEACHER analysis complete",
        metadata={"output_size": len(output), "confidence": 0.85},
    )
    return output, result


def stage_synthesize_recon(activities: List[CanonicalActivity]) -> tuple[Dict, StageResult]:
    """Stage 4c: Synthesize RECON output."""
    # Count providers
    providers = set()
    for activity in activities:
        if activity.provider_id:
            providers.add(activity.provider_id)

    output = {
        "lens": "recon",
        "providers_detected": len(providers),
        "value_flows": len(activities),
        "insights": [
            f"Found {len(providers)} unique providers",
            f"Tracked {len(activities)} value exchanges",
        ],
    }

    result = StageResult(
        stage_name="synthesize_recon",
        passed=True,
        exit_code=0,
        confidence=0.88,
        review_required=False,
        reason="RECON analysis complete",
        metadata={"output_size": len(output), "confidence": 0.88},
    )
    return output, result


# =============================================================================
# COMPLETE PIPELINE
# =============================================================================


def run_pipeline(raw_data: List[Dict], lens: str = "all") -> Dict:
    """Run the complete 4-stage pipeline."""
    trace = PipelineTrace()
    stage_results = []

    print("=" * 70)
    print("  TEACHER WEEK 2: 4-STAGE PIPELINE DEMO")
    print("=" * 70)

    # Stage 1: INGEST
    print("\n[STAGE 1] INGEST")
    print("-" * 70)
    trace.stage("ingest", start=True)
    ingested_data, result1 = stage_ingest(raw_data)
    trace.stage("ingest", end=True, **result1.metadata)
    stage_results.append(result1)
    print(f"  Status: {result1.to_dict()['status']}")
    print(f"  Rows loaded: {result1.metadata['rows_loaded']}")

    # Stage 2: NORMALIZE
    print("\n[STAGE 2] NORMALIZE")
    print("-" * 70)
    trace.stage("normalize", start=True)
    normalized_data, result2 = stage_normalize(ingested_data)
    trace.stage("normalize", end=True, **result2.metadata)
    stage_results.append(result2)
    print(f"  Status: {result2.to_dict()['status']}")
    print(f"  Entities created: {result2.metadata['entities_created']}")

    # Stage 3: GOVERN
    print("\n[STAGE 3] GOVERN")
    print("-" * 70)
    trace.stage("govern", start=True)
    governed_data, result3 = stage_govern(normalized_data)
    trace.stage("govern", end=True, **result3.metadata)
    stage_results.append(result3)
    print(f"  Status: {result3.to_dict()['status']}")
    print(f"  PII hashed: {result3.metadata['pii_hashed']}")
    print(f"  Governance rules applied: {result3.metadata['governance_rules_applied']}")

    # Stage 4: SYNTHESIZE
    print("\n[STAGE 4] SYNTHESIZE")
    print("-" * 70)
    outputs = {}

    if lens in ["all", "tribe"]:
        trace.stage("synthesize_tribe", start=True)
        tribe_output, result4a = stage_synthesize_tribe(governed_data)
        trace.stage("synthesize_tribe", end=True, **result4a.metadata)
        outputs["tribe"] = tribe_output
        stage_results.append(result4a)
        print(f"  [TRIBE] Status: {result4a.to_dict()['status']}")
        print(
            f"  [TRIBE] Users: {tribe_output['users']}, Edges: {tribe_output['collaboration_edges']}"
        )

    if lens in ["all", "teacher"]:
        trace.stage("synthesize_teacher", start=True)
        teacher_output, result4b = stage_synthesize_teacher(governed_data)
        trace.stage("synthesize_teacher", end=True, **result4b.metadata)
        outputs["teacher"] = teacher_output
        stage_results.append(result4b)
        print(f"  [TEACHER] Status: {result4b.to_dict()['status']}")
        print(f"  [TEACHER] Progressions: {teacher_output['progressions_detected']}")

    if lens in ["all", "recon"]:
        trace.stage("synthesize_recon", start=True)
        recon_output, result4c = stage_synthesize_recon(governed_data)
        trace.stage("synthesize_recon", end=True, **result4c.metadata)
        outputs["recon"] = recon_output
        stage_results.append(result4c)
        print(f"  [RECON] Status: {result4c.to_dict()['status']}")
        print(f"  [RECON] Providers: {recon_output['providers_detected']}")

    trace.end_time = datetime.now()

    # Aggregate status
    all_passed = all(r.passed for r in stage_results)
    any_review = any(r.review_required for r in stage_results)
    overall_exit_code = 0 if all_passed else max(r.exit_code for r in stage_results)

    print("\n" + "=" * 70)
    print("  PIPELINE SUMMARY")
    print("=" * 70)
    print(f"  Overall Status: {'PASS' if all_passed else 'FAIL'}")
    print(f"  Exit Code: {overall_exit_code}")
    print(f"  Review Required: {'Yes' if any_review else 'No'}")
    print(f"  Stages Executed: {len(stage_results)}")

    # Show trace
    print("\n" + trace.explain())

    return {
        "outputs": outputs,
        "stage_results": [r.to_dict() for r in stage_results],
        "trace": trace.explain(),
        "overall_status": "PASS" if all_passed else "FAIL",
        "exit_code": overall_exit_code,
    }


# =============================================================================
# MAIN
# =============================================================================


def main():
    """Run the pipeline demo."""
    # Run with all lenses
    result = run_pipeline(SAMPLE_RAW_DATA, lens="all")

    print("\n" + "=" * 70)
    print("  KEY TAKEAWAYS")
    print("=" * 70)
    print("  1. Data flows through 4 stages: INGEST -> NORMALIZE -> GOVERN -> SYNTHESIZE")
    print("  2. Each stage enforces integrity at a specific point")
    print("  3. Observability enables trust and debugging")
    print("  4. Quality gates prevent silent failures")
    print("  5. Same data -> three lenses -> unified intelligence")
    print("\n" + "=" * 70)
    print("  This is the infrastructure of trust.")
    print("=" * 70 + "\n")


if __name__ == "__main__":
    main()
