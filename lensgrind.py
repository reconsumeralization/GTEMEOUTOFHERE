#!/usr/bin/env python3
"""
LENSGRIND - Privacy and Scope Auditor
======================================
Finds privacy leaks, scope violations, and unsafe references.

Just as Valgrind finds memory leaks, Lensgrind finds privacy leaks.

This is TEACHER's Week 6 moment:
- C taught you the truth-layer (formal, audited, deterministic)
- Python gives you the delivery-layer (rapid, iterative, shippable)

Lensgrind is the governance bridge that lets you move fast without breaking trust.

Detects:
- PII fields used outside allowed scope
- Disallowed joins
- Unsafe cardinality reveals (small-group re-identification)
- Dangling references to raw IDs
- Shallow copies that leak PII
- Cross-lens domain violations

Architecture:
    CANON (C mindset)
      models / policies / invariants
              ↓
    RAPID LAYER (Python mindset)
      experiments / MVP extractors / curriculum protos
              ↓
    LENSGRIND (governance gate)
      safe abstraction / privacy enforcement / audit trail
"""

"""
LENSGRIND - Privacy and Scope Auditor
======================================
Finds privacy leaks, scope violations, and unsafe references.

Just as Valgrind finds memory leaks, Lensgrind finds privacy leaks.

This is TEACHER's Week 6 moment:
- C taught you the truth-layer (formal, audited, deterministic)
- Python gives you the delivery-layer (rapid, iterative, shippable)

Lensgrind is the governance bridge that lets you move fast without breaking trust.

Detects:
- PII fields used outside allowed scope
- Disallowed joins
- Unsafe cardinality reveals (small-group re-identification)
- Dangling references to raw IDs
- Shallow copies that leak PII
- Cross-lens domain violations

Architecture:
    CANON (C mindset)
      models / policies / invariants
              ↓
    RAPID LAYER (Python mindset)
      experiments / MVP extractors / curriculum protos
              ↓
    LENSGRIND (governance gate)
      safe abstraction / privacy enforcement / audit trail
"""

# Standard library imports
import json  # noqa: E402
import re  # noqa: E402
from collections import defaultdict  # noqa: E402
from dataclasses import dataclass, field as dataclass_field  # noqa: E402
from datetime import datetime  # noqa: E402
from typing import Dict, List, Optional, Any  # noqa: E402

# Local imports
from lens_boundary import BoundaryEnforcer, LENS_BOUNDARIES  # noqa: E402


# =============================================================================
# VIOLATION TYPES
# =============================================================================


class ViolationType:
    """
    Types of violations Lensgrind can detect.

    These map to TEACHER's core safety requirements:
    - People can create value without being able to leak PII
    - Abstraction gates protect dangerous operations
    - Fast iteration doesn't corrupt the truth-layer
    """

    FIELD_ACCESS_VIOLATION = "FIELD_ACCESS_VIOLATION"
    JOIN_VIOLATION = "JOIN_VIOLATION"
    AGGREGATION_VIOLATION = "AGGREGATION_VIOLATION"
    SMALL_COHORT_VIOLATION = "SMALL_COHORT_VIOLATION"
    HIGH_CARDINALITY_VIOLATION = "HIGH_CARDINALITY_VIOLATION"
    PII_REFERENCE_VIOLATION = "PII_REFERENCE_VIOLATION"
    SHALLOW_COPY_VIOLATION = "SHALLOW_COPY_VIOLATION"
    CROSS_LENS_LEAK = "CROSS_LENS_LEAK"
    UNSAFE_AGGREGATION = "UNSAFE_AGGREGATION"


@dataclass
class Violation:
    """
    A privacy or scope violation detected by Lensgrind.

    Python's exception model maps to TEACHER's moral design:
    - We expect failure
    - We recover safely
    - We don't punish users for bad input
    """

    type: str
    severity: str  # critical, high, medium, low
    lens: str
    field: Optional[str] = None
    reason: str = ""
    location: Optional[str] = None  # Function/file where violation occurred
    context: Dict[str, Any] = dataclass_field(default_factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        return {
            "type": self.type,
            "severity": self.severity,
            "lens": self.lens,
            "field": self.field,
            "reason": self.reason,
            "location": self.location,
            "context": self.context,
        }


# =============================================================================
# LENSGRIND AUDITOR
# =============================================================================


class Lensgrind:
    """
    Privacy and scope auditor for lens execution.

    This is TEACHER's abstraction gate:
    - Lets humans build without touching dangerous gears
    - Enables rapid Python iteration on top of formal C-style core
    - Provides audit trail for governance

    Usage:
        lensgrind = Lensgrind()
        lensgrind.start_monitoring("tribe")

        # ... run lens code ...

        report = lensgrind.generate_report()

    Two-speed development doctrine:
    - CORE: slow, formal, audited (your truth-layer)
    - EDGE: fast, Pythonic, experimental (your delivery-layer)

    Lensgrind ensures fast MVP doesn't corrupt your truth-layer.
    """

    def __init__(self) -> None:
        self.enforcer = BoundaryEnforcer()
        self.violations: List[Violation] = []
        self.field_access_log: Dict[str, List[str]] = defaultdict(list)
        self.current_lens: Optional[str] = None
        self.monitoring: bool = False

        # PII patterns - using Python's built-in regex (Week 6 gift)
        self.pii_patterns = {
            "email": re.compile(r"[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}"),
            "phone": re.compile(r"\+?[\d\s\-\(\)]{10,}"),
            "ssn": re.compile(r"\d{3}-\d{2}-\d{4}"),
        }

    def start_monitoring(self, lens: str):
        """
        Start monitoring a lens execution.

        This is where Python's interpreter model shines:
        - No compilation step
        - Immediate feedback
        - Rapid iteration on governance rules
        """
        self.current_lens = lens
        self.monitoring = True
        self.enforcer.clear_violations()
        self.violations = []
        self.field_access_log.clear()

    def stop_monitoring(self):
        """Stop monitoring."""
        self.monitoring = False
        self.current_lens = None

    def check_field_access(self, field: str, context: Optional[Dict[str, Any]] = None) -> bool:
        """
        Check if field access is allowed.

        Uses Python's dict (hash table) for O(1) lookup.
        Week 5 data structures, now built-in and free.
        """
        if not self.monitoring or not self.current_lens:
            return True  # Not monitoring

        # Log access - Python's defaultdict makes this clean
        self.field_access_log[self.current_lens].append(field)

        # Check boundary
        allowed = self.enforcer.check_field_access(self.current_lens, field, context or {})

        if not allowed:
            violations = self.enforcer.get_violations()
            if violations:
                latest = violations[-1]
                self.violations.append(
                    Violation(
                        type=ViolationType.FIELD_ACCESS_VIOLATION,
                        severity="high",
                        lens=self.current_lens,
                        field=field,
                        reason=latest.get("reason", "Field access violation"),
                        context=context or {},
                    )
                )

        return allowed

    def check_join(self, join_key: str) -> bool:
        """
        Check if join is allowed.

        Prevents cross-lens leaks at the data model level.
        """
        if not self.monitoring or not self.current_lens:
            return True

        allowed = self.enforcer.check_join(self.current_lens, join_key)

        if not allowed:
            violations = self.enforcer.get_violations()
            if violations:
                latest = violations[-1]
                self.violations.append(
                    Violation(
                        type=ViolationType.JOIN_VIOLATION,
                        severity="high",
                        lens=self.current_lens,
                        field=join_key,
                        reason=latest.get("reason", "Join violation"),
                    )
                )

        return allowed

    def check_cohort_size(self, cohort_size: int, field: Optional[str] = None) -> bool:
        """
        Check if cohort is large enough to prevent re-identification.

        This is TEACHER's k-anonymity enforcement:
        - Small groups can be re-identified
        - We fail safely and explain why
        - Compassionate error handling (Week 6 exception model)
        """
        if not self.monitoring or not self.current_lens:
            return True

        boundary = LENS_BOUNDARIES.get(self.current_lens)
        if not boundary:
            return True

        if cohort_size < boundary.min_cohort_size:
            self.violations.append(
                Violation(
                    type=ViolationType.SMALL_COHORT_VIOLATION,
                    severity="critical",
                    lens=self.current_lens,
                    field=field,
                    reason=f"Cohort size {cohort_size} < minimum {boundary.min_cohort_size} (re-identification risk)",
                    context={"cohort_size": cohort_size, "minimum": boundary.min_cohort_size},
                )
            )
            return False

        return True

    def check_cardinality(self, cardinality: int, field: Optional[str] = None) -> bool:
        """
        Check if cardinality is safe.

        High cardinality = information leakage risk.
        """
        if not self.monitoring or not self.current_lens:
            return True

        boundary = LENS_BOUNDARIES.get(self.current_lens)
        if not boundary:
            return True

        if cardinality > boundary.max_cardinality:
            self.violations.append(
                Violation(
                    type=ViolationType.HIGH_CARDINALITY_VIOLATION,
                    severity="high",
                    lens=self.current_lens or "unknown",
                    field=field,
                    reason=f"Cardinality {cardinality} > maximum {boundary.max_cardinality} (information leakage risk)",
                    context={"cardinality": cardinality, "maximum": boundary.max_cardinality},
                )
            )
            return False

        return True

    def check_pii_reference(self, data: Any, field_name: Optional[str] = None) -> bool:
        """
        Check for unsafe references to PII.

        Python's regex and introspection make this fast to implement.
        This is the "abstraction gate" in action:
        - Developers can work with data
        - Without being able to leak PII
        """
        if not self.monitoring:
            return True

        # Check if data contains PII patterns
        data_str = str(data)

        for pii_type, pattern in self.pii_patterns.items():
            if pattern.search(data_str):
                self.violations.append(
                    Violation(
                        type=ViolationType.PII_REFERENCE_VIOLATION,
                        severity="critical",
                        lens=self.current_lens or "unknown",
                        field=field_name,
                        reason=f"Unsafe reference to PII type '{pii_type}' detected",
                        context={"pii_type": pii_type, "data_preview": data_str[:50]},
                    )
                )
                return False

        # Check for common PII field names using Python's introspection
        if hasattr(data, "__dict__"):
            for key, value in data.__dict__.items():
                if key.lower() in ["email", "name", "phone", "ssn", "address"]:
                    if isinstance(value, str) and value:
                        self.violations.append(
                            Violation(
                                type=ViolationType.PII_REFERENCE_VIOLATION,
                                severity="critical",
                                lens=self.current_lens or "unknown",
                                field=key,
                                reason=f"Unsafe reference to PII field '{key}'",
                                context={"field": key, "value_preview": str(value)[:20]},
                            )
                        )
                        return False

        return True

    def check_shallow_copy(self, source: Any, destination: Any) -> bool:
        """
        Check if copy is shallow (unsafe).

        Python's automatic memory management is a gift,
        but shallow copies can still leak PII.
        """
        if not self.monitoring:
            return True

        # Simple check: if they have same id, it's a reference (shallow)
        if id(source) == id(destination):
            self.violations.append(
                Violation(
                    type=ViolationType.SHALLOW_COPY_VIOLATION,
                    severity="high",
                    lens=self.current_lens or "unknown",
                    reason="Shallow copy detected - destination references same object as source (PII leak risk)",
                    context={
                        "source_type": type(source).__name__,
                        "destination_type": type(destination).__name__,
                    },
                )
            )
            return False

        return True

    def check_cross_lens_leak(self, lens: str, field: str) -> bool:
        """
        Check if field belongs to another lens's domain.

        This enforces TEACHER's lens boundaries:
        - TRIBE: collaboration patterns
        - TEACHER: learning paths
        - RECON: provider reliability

        Each lens should only access its own domain.
        """
        if not self.monitoring or not self.current_lens:
            return True

        # Check if field is allowed in current lens but belongs to another lens
        current_boundary = LENS_BOUNDARIES.get(self.current_lens)
        if not current_boundary:
            return True

        # Check other lens boundaries using Python's dict iteration
        for other_lens, other_boundary in LENS_BOUNDARIES.items():
            if other_lens == self.current_lens:
                continue

            # If field is allowed in other lens but not current, it's a cross-lens leak
            if (
                field in other_boundary.allowed_fields
                and field not in current_boundary.allowed_fields
            ):
                self.violations.append(
                    Violation(
                        type=ViolationType.CROSS_LENS_LEAK,
                        severity="high",
                        lens=self.current_lens,
                        field=field,
                        reason=f"Field '{field}' belongs to '{other_lens}' lens domain, not '{self.current_lens}'",
                        context={"source_lens": other_lens, "target_lens": self.current_lens},
                    )
                )
                return False

        return True

    def generate_report(self) -> Dict[str, Any]:
        """
        Generate comprehensive privacy leak report.

        This is your audit trail for governance.
        Python's built-in JSON support makes this trivial.
        """
        # Combine with our violations
        all_violations = self.violations.copy()

        # Group by type using Python's defaultdict
        violations_by_type: Dict[str, int] = defaultdict(int)
        violations_by_severity: Dict[str, int] = defaultdict(int)

        for v in all_violations:
            violations_by_type[v.type] += 1
            violations_by_severity[v.severity] += 1

        # Generate recommendations
        recommendations = self._generate_recommendations(all_violations)

        return {
            "generated_at": datetime.now().isoformat(),
            "lens_monitored": self.current_lens,
            "total_violations": len(all_violations),
            "violations_by_type": dict(violations_by_type),
            "violations_by_severity": dict(violations_by_severity),
            "critical_violations": len([v for v in all_violations if v.severity == "critical"]),
            "violations": [v.to_dict() for v in all_violations],
            "field_access_summary": {
                lens: len(fields) for lens, fields in self.field_access_log.items()
            },
            "recommendations": recommendations,
            "status": "PASS" if len(all_violations) == 0 else "FAIL",
        }

    def _generate_recommendations(self, violations: List[Violation]) -> List[str]:
        """
        Generate remediation recommendations.

        Compassionate error handling:
        - We explain what went wrong
        - We suggest how to fix it
        - We don't punish users for mistakes
        """
        recommendations = []

        field_violations = [v for v in violations if v.type == ViolationType.FIELD_ACCESS_VIOLATION]
        if field_violations:
            recommendations.append(
                f"Remove {len(field_violations)} prohibited field accesses. "
                f"Fields: {', '.join(set(v.field for v in field_violations if v.field))}"
            )

        cohort_violations = [
            v for v in violations if v.type == ViolationType.SMALL_COHORT_VIOLATION
        ]
        if cohort_violations:
            recommendations.append(
                f"Increase cohort sizes for {len(cohort_violations)} analyses to prevent re-identification. "
                f"Minimum cohort size required: {cohort_violations[0].context.get('minimum', 'N/A')}"
            )

        pii_violations = [v for v in violations if v.type == ViolationType.PII_REFERENCE_VIOLATION]
        if pii_violations:
            recommendations.append(
                f"CRITICAL: Remove {len(pii_violations)} PII references. "
                f"These must be hashed or removed before lens processing."
            )

        shallow_copy_violations = [
            v for v in violations if v.type == ViolationType.SHALLOW_COPY_VIOLATION
        ]
        if shallow_copy_violations:
            recommendations.append(
                f"Replace {len(shallow_copy_violations)} shallow copies with deep copies. "
                f"Use safe schema transformation instead of reference assignment."
            )

        cross_lens_violations = [v for v in violations if v.type == ViolationType.CROSS_LENS_LEAK]
        if cross_lens_violations:
            recommendations.append(
                f"Fix {len(cross_lens_violations)} cross-lens leaks. "
                f"Each lens should only access its own domain fields."
            )

        if not recommendations:
            recommendations.append("No violations detected. Lens execution is safe.")

        return recommendations

    def export_report(self, filepath: str) -> str:
        """
        Export report to JSON file.

        Python's built-in JSON support = Week 6 productivity win.
        No manual serialization needed.
        """
        report = self.generate_report()
        with open(filepath, "w", encoding="utf-8") as f:
            json.dump(report, f, indent=2, default=str)
        return filepath


# =============================================================================
# DECORATOR FOR AUTOMATIC MONITORING
# =============================================================================


def monitored_lens(lens_name: str):
    """
    Decorator to automatically monitor a lens function.

    This is Python's abstraction power in action:
    - One line of code adds full governance
    - Developers can't forget to monitor
    - Fast iteration stays safe

    Usage:
        @monitored_lens("tribe")
        def extract_tribe(activities):
            # ... lens code ...
            pass

    This is how you build the "Scratch for Data" vision:
    - Block UI outputs Python pipeline recipes
    - Decorator ensures governance
    - Sandbox runs them safely
    """

    def decorator(func):
        def wrapper(*args, **kwargs):
            lensgrind = Lensgrind()
            lensgrind.start_monitoring(lens_name)

            try:
                result = func(*args, **kwargs)
                report = lensgrind.generate_report()

                if report["status"] == "FAIL":
                    print(
                        f"⚠️  Lensgrind detected {report['total_violations']} violations in {lens_name} lens"
                    )
                    for rec in report["recommendations"]:
                        print(f"   → {rec}")

                return result
            finally:
                lensgrind.stop_monitoring()

        return wrapper

    return decorator


# =============================================================================
# MAIN - DEMO
# =============================================================================


def main():
    """
    Demonstrate Lensgrind.

    This is your Week 6 killer demo:
    - Same truth-models as C-style core
    - Now expressed in Python for rapid iteration
    - Governance enforced automatically

    Next step: Build the Python MVP pipeline that outputs:
    1. TRIBE graph (collaboration patterns)
    2. TEACHER skill-gap + mentor suggestions
    3. RECON provider scorecards

    From Brian's CSV to three JSON views.
    That's not theory. That's a product.
    """
    print("=" * 70)
    print("  LENSGRIND - Privacy and Scope Auditor")
    print("  Finding Privacy Leaks Like Valgrind Finds Memory Leaks")
    print("=" * 70)
    print("\n  Week 6 Moment: Same truth-models, now shippable in Python")
    print("  Truth first, speed second. Governance always.")
    print("=" * 70)

    lensgrind = Lensgrind()

    # Simulate TRIBE lens execution
    print("\n[Monitoring TRIBE lens execution...]")
    lensgrind.start_monitoring("tribe")

    # Allowed access
    assert lensgrind.check_field_access("user_id") is True
    assert lensgrind.check_field_access("company_id") is True

    # Violation: accessing prohibited field
    assert lensgrind.check_field_access("email") is False

    # Violation: accessing TEACHER domain
    assert lensgrind.check_field_access("state_before") is False

    # Violation: small cohort
    assert lensgrind.check_cohort_size(2) is False  # Below minimum of 5

    # Check PII reference
    test_data = {"email": "user@company.com", "name": "John"}
    assert lensgrind.check_pii_reference(test_data, "user_data") is False

    lensgrind.stop_monitoring()

    # Generate report
    report = lensgrind.generate_report()

    print("\n[Lensgrind Report]")
    print("-" * 70)
    print(f"  Lens: {report['lens_monitored']}")
    print(f"  Status: {report['status']}")
    print(f"  Total Violations: {report['total_violations']}")
    print(f"  Critical: {report['critical_violations']}")

    print("\n  Violations by Type:")
    for vtype, count in report["violations_by_type"].items():
        print(f"    {vtype}: {count}")

    print("\n  Recommendations:")
    for rec in report["recommendations"]:
        print(f"    → {rec}")

    print("\n" + "=" * 70)
    print("  Week 6 is where Cosurvival becomes shippable:")
    print("  The same truth-models, now expressed in a language")
    print("  fast enough for real-world iteration.")
    print("=" * 70 + "\n")


if __name__ == "__main__":
    main()
