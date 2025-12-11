#!/usr/bin/env python3
"""
LENS BOUNDARY CONTRACT
======================
Defines what each lens is allowed to access.

This is the governance layer that prevents:
- TRIBE from accessing TEACHER learning gaps
- TEACHER from accessing RECON vendor disputes
- RECON from accessing private permissions

Each lens has:
- Allowed fields (whitelist)
- Prohibited fields (blacklist)
- Allowed join keys
- Minimum cohort sizes (k-anonymity)
- Maximum cardinality limits
"""

"""
LENS BOUNDARY CONTRACT
======================
Defines what each lens is allowed to access.

This is the governance layer that prevents:
- TRIBE from accessing TEACHER learning gaps
- TEACHER from accessing RECON vendor disputes
- RECON from accessing private permissions

Each lens has:
- Allowed fields (whitelist)
- Prohibited fields (blacklist)
- Allowed join keys
- Minimum cohort sizes (k-anonymity)
- Maximum cardinality limits
"""

# Standard library imports
from dataclasses import dataclass, field
from enum import Enum
from typing import Dict, Set, List, Optional, Any


class FieldSensitivity(Enum):
    """Field sensitivity classification."""

    PUBLIC = "public"  # Safe for all lenses
    INTERNAL = "internal"  # Safe for some lenses
    CONFIDENTIAL = "confidential"  # Restricted to specific lenses
    RESTRICTED = "restricted"  # PII - never in lens outputs
    PROHIBITED = "prohibited"  # Never accessible


@dataclass
class LensBoundary:
    """
    Defines the boundary contract for a lens.

    This is the "buffer" that prevents overflow into unauthorized data.
    """

    lens_name: str

    # Allowed fields (whitelist)
    allowed_fields: Set[str] = field(default_factory=set)

    # Prohibited fields (blacklist)
    prohibited_fields: Set[str] = field(default_factory=set)

    # Allowed join keys (for relationships)
    allowed_join_keys: Set[str] = field(default_factory=set)

    # Aggregation safety
    min_cohort_size: int = 5  # k-anonymity minimum
    max_cardinality: int = 1000  # Prevent high-cardinality leaks

    # Allowed aggregation functions
    allowed_aggregations: Set[str] = field(
        default_factory=lambda: {"count", "sum", "avg", "min", "max"}
    )

    # Prohibited aggregations
    prohibited_aggregations: Set[str] = field(
        default_factory=lambda: {"list", "collect", "distinct"}  # May reveal individuals
    )

    def validate_field_access(self, field: str, context: Dict[str, Any] = None) -> tuple[bool, str]:
        """
        Check if lens can access this field.

        Returns:
            (allowed: bool, reason: str)
        """
        context = context or {}

        # Check blacklist first (most restrictive)
        if field in self.prohibited_fields:
            return False, f"Field '{field}' is prohibited for lens '{self.lens_name}'"

        # Check whitelist
        if field not in self.allowed_fields:
            return False, f"Field '{field}' is not in allowed fields for lens '{self.lens_name}'"

        # Check cohort size if provided
        cohort_size = context.get("cohort_size")
        if cohort_size is not None and cohort_size < self.min_cohort_size:
            return (
                False,
                f"Cohort size {cohort_size} < minimum {self.min_cohort_size} (re-identification risk)",
            )

        # Check cardinality
        cardinality = context.get("cardinality")
        if cardinality is not None and cardinality > self.max_cardinality:
            return (
                False,
                f"Cardinality {cardinality} > maximum {self.max_cardinality} (information leakage risk)",
            )

        return True, "Access allowed"

    def validate_join(self, join_key: str) -> tuple[bool, str]:
        """Check if join is allowed."""
        if join_key not in self.allowed_join_keys:
            return False, f"Join on '{join_key}' not allowed for lens '{self.lens_name}'"
        return True, "Join allowed"

    def validate_aggregation(self, aggregation: str) -> tuple[bool, str]:
        """Check if aggregation is allowed."""
        if aggregation in self.prohibited_aggregations:
            return False, f"Aggregation '{aggregation}' is prohibited for lens '{self.lens_name}'"
        if aggregation not in self.allowed_aggregations:
            return False, f"Aggregation '{aggregation}' is not in allowed aggregations"
        return True, "Aggregation allowed"

    def to_dict(self) -> Dict[str, Any]:
        """Export boundary as dictionary."""
        return {
            "lens_name": self.lens_name,
            "allowed_fields": list(self.allowed_fields),
            "prohibited_fields": list(self.prohibited_fields),
            "allowed_join_keys": list(self.allowed_join_keys),
            "min_cohort_size": self.min_cohort_size,
            "max_cardinality": self.max_cardinality,
            "allowed_aggregations": list(self.allowed_aggregations),
            "prohibited_aggregations": list(self.prohibited_aggregations),
        }


# =============================================================================
# LENS BOUNDARY DEFINITIONS
# =============================================================================

TRIBE_BOUNDARY = LensBoundary(
    lens_name="tribe",
    allowed_fields={
        "user_id",  # Hashed
        "company_id",  # Safe for org analysis
        "group_id",  # Safe for team analysis
        "activity_type",  # Safe activity classification
        "timestamp",  # Safe temporal data
        "target_user_id",  # Hashed, for relationship analysis
    },
    prohibited_fields={
        "email",  # PII
        "name",  # PII
        "email_domain",  # May reveal individuals in small orgs
        "resource_path",  # May reveal sensitive files
        "error_code",  # May reveal internal issues
        "state_before",  # Permission details (TEACHER domain)
        "state_after",  # Permission details (TEACHER domain)
        "provider_id",  # Vendor info (RECON domain)
    },
    allowed_join_keys={"user_id", "company_id", "group_id"},
    min_cohort_size=5,  # k-anonymity
    max_cardinality=1000,
)

TEACHER_BOUNDARY = LensBoundary(
    lens_name="teacher",
    allowed_fields={
        "user_id",  # Hashed
        "role_id",  # Safe role identifier
        "state_before",  # Permission state (for progression)
        "state_after",  # Permission state (for progression)
        "permission_type",  # Safe permission classification
        "timestamp",  # Safe temporal data
    },
    prohibited_fields={
        "email",  # PII
        "name",  # PII
        "company_id",  # May reveal org structure
        "group_id",  # May reveal team composition
        "resource_path",  # May reveal sensitive files
        "provider_id",  # Vendor info (RECON domain)
        "error_code",  # Quality info (RECON domain)
        "target_user_id",  # Relationship info (TRIBE domain)
    },
    allowed_join_keys={"user_id", "role_id"},
    min_cohort_size=3,  # Smaller for role-based analysis
    max_cardinality=500,
)

RECON_BOUNDARY = LensBoundary(
    lens_name="recon",
    allowed_fields={
        "provider_id",  # Safe provider identifier
        "company_id",  # Safe for org-level analysis
        "activity_count",  # Aggregated metric
        "error_count",  # Aggregated metric
        "scheme",  # Safe service type
        "timestamp",  # Safe temporal data
    },
    prohibited_fields={
        "user_id",  # Individual-level data
        "target_user_id",  # Individual relationships
        "email",  # PII
        "name",  # PII
        "email_domain",  # May reveal individuals
        "role_id",  # Role info (TEACHER domain)
        "state_before",  # Permission details (TEACHER domain)
        "state_after",  # Permission details (TEACHER domain)
        "resource_path",  # May reveal sensitive resources
    },
    allowed_join_keys={"provider_id", "company_id"},
    min_cohort_size=5,
    max_cardinality=100,
)

# Registry of all boundaries
LENS_BOUNDARIES = {"tribe": TRIBE_BOUNDARY, "teacher": TEACHER_BOUNDARY, "recon": RECON_BOUNDARY}


# =============================================================================
# BOUNDARY ENFORCEMENT
# =============================================================================


class BoundaryEnforcer:
    """
    Enforces lens boundaries at runtime.

    This is the "firewall" that prevents lens overflow.
    """

    def __init__(self):
        self.boundaries = LENS_BOUNDARIES.copy()
        self.violations: List[Dict[str, Any]] = []

    def check_field_access(self, lens: str, field: str, context: Dict[str, Any] = None) -> bool:
        """Check if field access is allowed, log violations."""
        if lens not in self.boundaries:
            self.violations.append(
                {
                    "type": "UNKNOWN_LENS",
                    "lens": lens,
                    "field": field,
                    "reason": f"Unknown lens: {lens}",
                }
            )
            return False

        boundary = self.boundaries[lens]
        allowed, reason = boundary.validate_field_access(field, context or {})

        if not allowed:
            self.violations.append(
                {"type": "FIELD_ACCESS_VIOLATION", "lens": lens, "field": field, "reason": reason}
            )

        return allowed

    def check_join(self, lens: str, join_key: str) -> bool:
        """Check if join is allowed, log violations."""
        if lens not in self.boundaries:
            return False

        boundary = self.boundaries[lens]
        allowed, reason = boundary.validate_join(join_key)

        if not allowed:
            self.violations.append(
                {"type": "JOIN_VIOLATION", "lens": lens, "field": join_key, "reason": reason}
            )

        return allowed

    def check_aggregation(self, lens: str, aggregation: str) -> bool:
        """Check if aggregation is allowed, log violations."""
        if lens not in self.boundaries:
            return False

        boundary = self.boundaries[lens]
        allowed, reason = boundary.validate_aggregation(aggregation)

        if not allowed:
            self.violations.append(
                {
                    "type": "AGGREGATION_VIOLATION",
                    "lens": lens,
                    "field": aggregation,
                    "reason": reason,
                }
            )

        return allowed

    def get_violations(self) -> List[Dict[str, Any]]:
        """Get all violations detected."""
        return self.violations.copy()

    def clear_violations(self):
        """Clear violation log."""
        self.violations = []

    def has_violations(self) -> bool:
        """Check if any violations were detected."""
        return len(self.violations) > 0


# =============================================================================
# USAGE EXAMPLE
# =============================================================================


def example_usage():
    """Example of using lens boundaries."""
    enforcer = BoundaryEnforcer()

    # TRIBE lens accessing allowed field
    assert enforcer.check_field_access("tribe", "user_id") == True

    # TRIBE lens accessing prohibited field
    assert enforcer.check_field_access("tribe", "email") == False

    # TEACHER lens accessing its domain
    assert enforcer.check_field_access("teacher", "state_before") == True

    # TEACHER lens accessing TRIBE domain
    assert enforcer.check_field_access("teacher", "target_user_id") == False

    # RECON lens accessing its domain
    assert enforcer.check_field_access("recon", "provider_id") == True

    # RECON lens accessing individual data
    assert enforcer.check_field_access("recon", "user_id") == False

    # Check violations
    violations = enforcer.get_violations()
    print(f"Detected {len(violations)} violations")

    for v in violations:
        print(f"  - {v['type']}: {v['reason']}")


if __name__ == "__main__":
    example_usage()
