#!/usr/bin/env python3
"""
COSURVIVAL DATA GOVERNANCE MODULE
=================================
The trust backbone of the entire system.

This module ensures:
1. PII is properly handled (hashed/pseudonymized)
2. Sensitivity classifications are enforced
3. Bias guardrails are active
4. Triple Balance review triggers work
5. Audit trails are maintained

NOTHING proceeds without passing governance checks.
"""

"""
COSURVIVAL DATA GOVERNANCE MODULE
=================================
The trust backbone of the entire system.

This module ensures:
1. PII is properly handled (hashed/pseudonymized)
2. Sensitivity classifications are enforced
3. Bias guardrails are active
4. Triple Balance review triggers work
5. Audit trails are maintained

NOTHING proceeds without passing governance checks.
"""

# Standard library imports
import hashlib  # noqa: E402
import json  # noqa: E402
import re  # noqa: E402
import secrets  # noqa: E402
from dataclasses import dataclass, field  # noqa: E402
from datetime import datetime  # noqa: E402
from enum import Enum  # noqa: E402
from typing import Dict, List, Optional, Any  # noqa: E402


# =============================================================================
# SENSITIVITY CLASSIFICATIONS
# =============================================================================


class SensitivityLevel(Enum):
    """
    Data sensitivity classification levels.

    CURRICULUM: Week 1, Activity 1.1 - Build a Data Dictionary
    Learners classify columns by sensitivity level (public/internal/confidential/restricted).
    See: TEACHER_CORE_TRACK.md, Week 1, Activity 1.1
    """

    PUBLIC = "public"  # Can be shared freely
    INTERNAL = "internal"  # Organization-internal only
    CONFIDENTIAL = "confidential"  # Need-to-know basis
    RESTRICTED = "restricted"  # PII, requires anonymization
    PROHIBITED = "prohibited"  # Must not be processed/stored


class PIIType(Enum):
    """Types of Personally Identifiable Information."""

    DIRECT_ID = "direct_identifier"  # Name, email, SSN
    QUASI_ID = "quasi_identifier"  # Job title + dept + hire date
    SENSITIVE = "sensitive_attribute"  # Health, religion, politics
    NON_PII = "non_pii"  # Aggregated, anonymized


# =============================================================================
# DATA DICTIONARY - Column Classifications
# =============================================================================


@dataclass
class ColumnDefinition:
    """
    Definition of a data column for governance purposes.

    CURRICULUM: Week 1, Activity 1.1 - Build a Data Dictionary
    This dataclass represents the structure learners create when building their
    data dictionary. Each column needs: name, meaning, type, sensitivity, PII type.
    See: TEACHER_CORE_TRACK.md, Week 1, Activity 1.1
    """

    name: str
    meaning: str
    data_type: str
    example: str
    sensitivity: SensitivityLevel
    pii_type: PIIType
    requires_hashing: bool = False
    requires_masking: bool = False
    allowed_operations: List[str] = field(default_factory=lambda: ["aggregate", "count"])
    notes: str = ""


# Standard column classifications for activity/audit data
STANDARD_COLUMN_CLASSIFICATIONS: Dict[str, ColumnDefinition] = {
    # Direct Identifiers - MUST be hashed
    "uid": ColumnDefinition(
        name="uid",
        meaning="Unique user identifier",
        data_type="string",
        example="user_12345",
        sensitivity=SensitivityLevel.RESTRICTED,
        pii_type=PIIType.DIRECT_ID,
        requires_hashing=True,
        allowed_operations=["aggregate", "count", "graph_edges"],
        notes="Hash before any analysis. Maintain reversible mapping only with explicit permission.",
    ),
    "name": ColumnDefinition(
        name="name",
        meaning="User's display name",
        data_type="string",
        example="John Smith",
        sensitivity=SensitivityLevel.RESTRICTED,
        pii_type=PIIType.DIRECT_ID,
        requires_hashing=True,
        allowed_operations=["none"],
        notes="Remove or hash. Never display in outputs.",
    ),
    "email": ColumnDefinition(
        name="email",
        meaning="User's email address",
        data_type="string",
        example="john@company.com",
        sensitivity=SensitivityLevel.RESTRICTED,
        pii_type=PIIType.DIRECT_ID,
        requires_hashing=True,
        allowed_operations=["none"],
        notes="Remove or hash. Domain may be preserved for org analysis.",
    ),
    "uidopp": ColumnDefinition(
        name="uidopp",
        meaning="Opposing/target user in interaction",
        data_type="string",
        example="user_67890",
        sensitivity=SensitivityLevel.RESTRICTED,
        pii_type=PIIType.DIRECT_ID,
        requires_hashing=True,
        allowed_operations=["aggregate", "count", "graph_edges"],
        notes="Hash consistently with uid for relationship analysis.",
    ),
    "uidreq": ColumnDefinition(
        name="uidreq",
        meaning="Requesting user in interaction",
        data_type="string",
        example="user_11111",
        sensitivity=SensitivityLevel.RESTRICTED,
        pii_type=PIIType.DIRECT_ID,
        requires_hashing=True,
        allowed_operations=["aggregate", "count", "graph_edges"],
        notes="Hash consistently with uid for relationship analysis.",
    ),
    # Quasi-Identifiers - Handle with care
    "companyid": ColumnDefinition(
        name="companyid",
        meaning="Company/organization identifier",
        data_type="string",
        example="org_abc",
        sensitivity=SensitivityLevel.CONFIDENTIAL,
        pii_type=PIIType.QUASI_ID,
        requires_hashing=False,  # Usually OK to keep for org-level analysis
        allowed_operations=["aggregate", "count", "graph_edges", "group_by"],
        notes="May be kept for organizational analysis. Consider hashing for external reports.",
    ),
    "groupid": ColumnDefinition(
        name="groupid",
        meaning="Group/team identifier",
        data_type="string",
        example="team_123",
        sensitivity=SensitivityLevel.CONFIDENTIAL,
        pii_type=PIIType.QUASI_ID,
        requires_hashing=False,
        allowed_operations=["aggregate", "count", "graph_edges", "group_by"],
        notes="May reveal organizational structure. Hash for external reports.",
    ),
    "roleid": ColumnDefinition(
        name="roleid",
        meaning="User's role identifier",
        data_type="string",
        example="role_admin",
        sensitivity=SensitivityLevel.INTERNAL,
        pii_type=PIIType.QUASI_ID,
        allowed_operations=["aggregate", "count", "group_by", "compare"],
        notes="Key for TEACHER analysis. OK for internal use.",
    ),
    # Activity Data - Generally safe
    "type": ColumnDefinition(
        name="type",
        meaning="Activity/event type",
        data_type="string",
        example="file_access",
        sensitivity=SensitivityLevel.INTERNAL,
        pii_type=PIIType.NON_PII,
        allowed_operations=["all"],
        notes="Safe for analysis.",
    ),
    "date": ColumnDefinition(
        name="date",
        meaning="Timestamp of activity",
        data_type="datetime",
        example="2024-01-15T10:30:00Z",
        sensitivity=SensitivityLevel.INTERNAL,
        pii_type=PIIType.NON_PII,
        allowed_operations=["all"],
        notes="May be coarsened (day-level) for external reports.",
    ),
    # Resource Data - Check paths carefully
    "path": ColumnDefinition(
        name="path",
        meaning="Resource path accessed",
        data_type="string",
        example="/projects/secret/doc.pdf",
        sensitivity=SensitivityLevel.CONFIDENTIAL,
        pii_type=PIIType.QUASI_ID,
        requires_masking=True,
        allowed_operations=["aggregate", "count"],
        notes="Path contents may reveal sensitive info. Mask specific filenames.",
    ),
    # Provider Data - Business sensitive
    "providerid": ColumnDefinition(
        name="providerid",
        meaning="Service provider identifier",
        data_type="string",
        example="provider_aws",
        sensitivity=SensitivityLevel.INTERNAL,
        pii_type=PIIType.NON_PII,
        allowed_operations=["all"],
        notes="Key for RECONSUMERALIZATION analysis.",
    ),
    # Permission Data - Sensitive
    "privilege": ColumnDefinition(
        name="privilege",
        meaning="Permission/privilege granted",
        data_type="string",
        example="read_write",
        sensitivity=SensitivityLevel.CONFIDENTIAL,
        pii_type=PIIType.QUASI_ID,
        allowed_operations=["aggregate", "count", "compare"],
        notes="Key for TEACHER skill gap analysis. Don't expose individual permissions.",
    ),
    "stateold": ColumnDefinition(
        name="stateold",
        meaning="Previous state before change",
        data_type="string",
        example="pending",
        sensitivity=SensitivityLevel.INTERNAL,
        pii_type=PIIType.NON_PII,
        allowed_operations=["all"],
        notes="Key for progression tracking.",
    ),
    "statenew": ColumnDefinition(
        name="statenew",
        meaning="New state after change",
        data_type="string",
        example="active",
        sensitivity=SensitivityLevel.INTERNAL,
        pii_type=PIIType.NON_PII,
        allowed_operations=["all"],
        notes="Key for progression tracking.",
    ),
    # Error/Quality Data
    "codeerror": ColumnDefinition(
        name="codeerror",
        meaning="Error code if any",
        data_type="string",
        example="ERR_401",
        sensitivity=SensitivityLevel.INTERNAL,
        pii_type=PIIType.NON_PII,
        allowed_operations=["all"],
        notes="Key for reliability scoring.",
    ),
}


# =============================================================================
# SCOPE STATEMENT - What We Will NOT Infer
# =============================================================================

PROHIBITED_INFERENCES = [
    """
    Prohibited inferences that the system will NEVER make.
    
    CURRICULUM: Week 0, Activity 0.3 - The Governance Gate
    These are the "never predict performance" rules introduced in Week 0.
    Learners understand why we can't analyze everything.
    See: TEACHER_CORE_TRACK.md, Week 0, Activity 0.3
    
    CURRICULUM: Week 1, Activity 1.2 - Write Governance Rules
    Learners create their own 5 rules that should BLOCK analysis.
    This list serves as the reference implementation.
    See: TEACHER_CORE_TRACK.md, Week 1, Activity 1.2
    """
    "Individual employee performance scores",
    "Disciplinary action recommendations",
    "Termination risk predictions",
    "Political or religious affiliations",
    "Health status or conditions",
    "Personal relationship assessments",
    "Psychological profiling",
    "Surveillance-based productivity metrics",
    "Individual compliance scores (only aggregate)",
    "Predictive hiring/firing recommendations",
]

BIAS_GUARDRAILS = {
    """
    Bias guardrails to prevent harmful interpretations.
    
    CURRICULUM: Week 0, Activity 0.3 - The Governance Gate
    Introduces the key insight: "high activity ≠ high value"
    This is one of the first governance concepts learners encounter.
    See: TEACHER_CORE_TRACK.md, Week 0, Activity 0.3
    
    CURRICULUM: Week 0, Activity 0.4 - Ethical Guardrails
    These guardrails prevent the "biased models" anti-pattern.
    See: TEACHER_CORE_TRACK.md, Week 0, Activity 0.4
    See: TEACHER_ETHICAL_GUARDRAILS.md for detailed anti-pattern documentation
    """
    "high_activity": {
        "warning": "High activity ≠ high value or performance",
        "context": "Activity volume may reflect role requirements, not individual merit",
        "required_action": "Always present with role/context normalization",
    },
    "low_activity": {
        "warning": "Low activity ≠ low contribution",
        "context": "Strategic work, deep focus, or leadership roles may show lower activity",
        "required_action": "Never flag individuals based on activity alone",
    },
    "collaboration_score": {
        "warning": "High collaboration ≠ better employee",
        "context": "Individual contributors and collaborative roles have different patterns",
        "required_action": "Compare within role cohorts only",
    },
    "skill_gaps": {
        "warning": "Skill gaps are opportunities, not deficiencies",
        "context": "Present as growth paths, never as shortcomings",
        "required_action": "Frame positively in all outputs",
    },
    "provider_rankings": {
        "warning": "Rankings reflect fit, not absolute quality",
        "context": "A provider may rank low for one use case but excel in another",
        "required_action": "Always include context and use-case specificity",
    },
}


# =============================================================================
# PII HANDLING
# =============================================================================


class PIIHandler:
    """
    Handles PII hashing, pseudonymization, and reversible mappings.

    CURRICULUM: Week 0, Activity 0.3 - The Governance Gate
    Introduces PII (Personally Identifiable Information) concept.
    Learners understand why we hash names and emails.
    See: TEACHER_CORE_TRACK.md, Week 0, Activity 0.3

    CURRICULUM: Week 1, Activity 1.1 - Build a Data Dictionary
    Learners identify which columns require hashing (requires_hashing: yes/no).
    This class implements the actual hashing logic.
    See: TEACHER_CORE_TRACK.md, Week 1, Activity 1.1

    CURRICULUM: Week 10 - Security Module
    PII protection is a critical security practice.
    See: TEACHER_WEEK10.md, API_KEY_SECURITY_CRITICAL.md
    """

    def __init__(self, salt: Optional[str] = None, allow_reversal: bool = False):
        """
        Initialize PII handler.

        Args:
            salt: Salt for hashing. If None, generates secure random salt.
            allow_reversal: If True, maintains reverse mapping (requires permission).
        """
        self.salt = salt or secrets.token_hex(32)
        self.allow_reversal = allow_reversal
        self._forward_map: Dict[str, str] = {}  # original -> hashed
        self._reverse_map: Dict[str, str] = {}  # hashed -> original (only if allowed)
        self._hash_counter = 0

    def hash_value(self, value: Any, column_name: str = "") -> str:
        """
        Hash a PII value consistently.

        Args:
            value: The value to hash
            column_name: Column name for consistent cross-column hashing

        Returns:
            Hashed value (deterministic for same input)
        """
        if value is None or (isinstance(value, float) and str(value) == "nan"):
            return "REDACTED_NULL"

        str_value = str(value).strip()
        if not str_value:
            return "REDACTED_EMPTY"

        # Check if already hashed
        if str_value in self._forward_map:
            return self._forward_map[str_value]

        # Create deterministic hash
        hash_input = f"{self.salt}:{str_value}".encode("utf-8")
        hashed = hashlib.sha256(hash_input).hexdigest()[:16]

        # Create human-readable pseudonym
        self._hash_counter += 1
        pseudonym = f"entity_{hashed}"

        # Store mappings
        self._forward_map[str_value] = pseudonym
        if self.allow_reversal:
            self._reverse_map[pseudonym] = str_value

        return pseudonym

    def hash_email_preserve_domain(self, email: str) -> str:
        """Hash email but preserve domain for organizational analysis."""
        if not email or "@" not in str(email):
            return self.hash_value(email, "email")

        local, domain = str(email).rsplit("@", 1)
        hashed_local = self.hash_value(local, "email_local")
        return f"{hashed_local}@{domain}"

    def mask_path(self, path: str) -> str:
        """Mask sensitive parts of file paths."""
        if not path:
            return "REDACTED_PATH"

        # Keep structure, mask specific names
        parts = str(path).replace("\\", "/").split("/")
        masked_parts = []

        for part in parts:
            # Keep common structural elements
            if part.lower() in ["", "home", "users", "documents", "projects", "shared"]:
                masked_parts.append(part)
            # Mask anything that looks like a username or specific file
            elif re.match(r"^[a-zA-Z0-9._-]+\.[a-zA-Z]+$", part):  # Filename with extension
                ext = part.rsplit(".", 1)[1] if "." in part else ""
                masked_parts.append(
                    f"FILE_{len(masked_parts)}.{ext}" if ext else f"FILE_{len(masked_parts)}"
                )
            else:
                masked_parts.append(f"DIR_{len(masked_parts)}")

        return "/".join(masked_parts)

    def reverse_lookup(self, hashed_value: str) -> Optional[str]:
        """Reverse lookup (only if reversal is allowed and value exists)."""
        if not self.allow_reversal:
            raise PermissionError(
                "Reverse lookup not permitted. Initialize with allow_reversal=True"
            )
        return self._reverse_map.get(hashed_value)

    def export_mapping(self, filepath: str) -> str:
        """Export the mapping for secure storage (only if reversal allowed)."""
        if not self.allow_reversal:
            raise PermissionError("Cannot export mapping when reversal is not allowed")

        mapping = {
            "created_at": datetime.now().isoformat(),
            "salt_hash": hashlib.sha256(self.salt.encode()).hexdigest()[
                :8
            ],  # Don't expose actual salt
            "forward_map": self._forward_map,
            "total_entities": len(self._forward_map),
        }

        with open(filepath, "w") as f:
            json.dump(mapping, f, indent=2)

        return filepath

    def get_stats(self) -> Dict[str, Any]:
        """Get statistics about PII handling."""
        return {
            "total_hashed": len(self._forward_map),
            "reversal_enabled": self.allow_reversal,
            "reverse_map_size": len(self._reverse_map) if self.allow_reversal else "N/A",
        }


# =============================================================================
# GOVERNANCE GATE
# =============================================================================


@dataclass
class SeverityScore:
    """
    Enhanced severity scoring with chain impact assessment.

    CURRICULUM: Week 0, Activity 0.3 - Governance Gate
    CURRICULUM: Week 10 - Security Module

    New Approach (from vulnerability report 440782380):
    - Entry Point Severity: Traditional CVE-style scoring (1-10)
    - Chain Impact Severity: Cross-domain pivot potential (1-10)
    - Blast Radius: How many products/domains affected (1-10)
    - Final Severity: Maximum of all three

    Key Insight: "Entry-point bugs can be duplicate, but the impact
    chain is novel. Severity must score chain impact and cross-domain
    pivot potential."

    See: SECURITY_VULNERABILITY_RESPONSE.md, Severity & Governance Rubric Update
    See: SECURITY_TRUST_FABRIC.md, Severity & Governance Rubric
    """

    entry_point: int  # 1-10, traditional CVE-style
    chain_impact: int  # 1-10, cross-domain pivot potential
    blast_radius: int  # 1-10, products/domains affected
    final: int  # max(entry_point, chain_impact, blast_radius)

    def requires_architecture_mitigation(self) -> bool:
        """
        Architecture-level mitigation if chain impact or blast radius is high.

        CURRICULUM: Week 0, Activity 0.3 - Governance Gate
        Even "duplicate" entry points can trigger architecture changes if
        chain impact or blast radius is high.
        """
        return self.chain_impact >= 7 or self.blast_radius >= 7

    def requires_ecosystem_review(self) -> bool:
        """Ecosystem risk review if multiple products affected."""
        return self.blast_radius >= 5

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary."""
        return {
            "entry_point": self.entry_point,
            "chain_impact": self.chain_impact,
            "blast_radius": self.blast_radius,
            "final": self.final,
            "requires_architecture_mitigation": self.requires_architecture_mitigation(),
            "requires_ecosystem_review": self.requires_ecosystem_review(),
        }


@dataclass
class GovernanceCheckResult:
    """
    Result of a governance check.

    Enhanced with severity scoring for chain impact assessment.
    """

    passed: bool
    check_name: str
    severity: str  # info, warning, error, critical
    message: str
    details: Dict[str, Any] = field(default_factory=dict)
    remediation: str = ""
    severity_score: Optional[SeverityScore] = None  # Enhanced severity scoring


@dataclass
class GovernanceReport:
    """Complete governance report for a dataset."""

    dataset_id: str
    checked_at: datetime
    overall_passed: bool
    checks: List[GovernanceCheckResult]
    risk_flags: List[str]
    review_required: bool
    review_reasons: List[str]
    recommendations: List[str]
    pii_stats: Dict[str, Any]
    column_classifications: Dict[str, str]

    def to_dict(self) -> Dict[str, Any]:
        return {
            "dataset_id": self.dataset_id,
            "checked_at": self.checked_at.isoformat(),
            "overall_passed": self.overall_passed,
            "checks": [
                {
                    "passed": c.passed,
                    "name": c.check_name,
                    "severity": c.severity,
                    "message": c.message,
                    "details": c.details,
                    "remediation": c.remediation,
                }
                for c in self.checks
            ],
            "risk_flags": self.risk_flags,
            "review_required": self.review_required,
            "review_reasons": self.review_reasons,
            "recommendations": self.recommendations,
            "pii_stats": self.pii_stats,
            "column_classifications": self.column_classifications,
        }


class GovernanceGate:
    """
    The governance gate that ALL data must pass through.

    This is the trust backbone of Cosurvival.

    CURRICULUM: Week 0, Activity 0.3 - The Governance Gate
    This is the core concept: "Why can't we just analyze everything?"
    The GovernanceGate enforces PII checks, bias checks, scope checks.
    See: TEACHER_CORE_TRACK.md, Week 0, Activity 0.3

    CURRICULUM: Week 1, Activity 1.2 - Write Governance Rules
    Learners write rules that should BLOCK analysis.
    This class implements those rules programmatically.
    See: TEACHER_CORE_TRACK.md, Week 1, Activity 1.2

    CURRICULUM: Week 10 - Security Module
    Enhanced with chain impact severity scoring.
    See: SECURITY_VULNERABILITY_RESPONSE.md, Finding 1

    The flow: RAW DATA → [GOVERNANCE GATE] → CLEAN DATA → ANALYSIS
    """

    def __init__(self, pii_handler: Optional[PIIHandler] = None):
        self.pii_handler = pii_handler or PIIHandler()
        self.column_defs = STANDARD_COLUMN_CLASSIFICATIONS.copy()
        self.checks_performed: List[GovernanceCheckResult] = []

    def assess_severity(self, vulnerability: Dict[str, Any]) -> SeverityScore:
        """
        Assess severity including chain impact.

        CURRICULUM: Week 0, Activity 0.3 - Governance Gate
        CURRICULUM: Week 10 - Security Module

        Enhanced severity scoring from vulnerability report 440782380:
        - Entry point severity (traditional CVE-style)
        - Chain impact severity (cross-domain pivot potential)
        - Blast radius (products/domains affected)
        - Final = max(all three)

        Key Insight: "Entry-point bugs can be duplicate, but the
        impact chain is novel."

        See: SECURITY_VULNERABILITY_RESPONSE.md, Finding 1
        See: SECURITY_TRUST_FABRIC.md, Severity & Governance Rubric
        """
        entry_severity = self._assess_entry_point(vulnerability)
        chain_severity = self._assess_chain_impact(vulnerability)
        blast_radius = self._assess_blast_radius(vulnerability)

        final = max(entry_severity, chain_severity, blast_radius)

        return SeverityScore(
            entry_point=entry_severity,
            chain_impact=chain_severity,
            blast_radius=blast_radius,
            final=final,
        )

    def _assess_entry_point(self, vulnerability: Dict[str, Any]) -> int:
        """
        Assess traditional entry point severity (1-10).

        Based on:
        - CVSS-style scoring
        - Attack complexity
        - Authentication requirements
        - Impact on confidentiality/integrity/availability
        """
        # Simplified scoring - in production would use CVSS
        impact = vulnerability.get("impact", "low")
        complexity = vulnerability.get("complexity", "high")
        auth_required = vulnerability.get("auth_required", True)

        score = 5  # Base score

        # Impact adjustment
        if impact == "critical":
            score += 3
        elif impact == "high":
            score += 2
        elif impact == "medium":
            score += 1

        # Complexity adjustment (easier = higher score)
        if complexity == "low":
            score += 2
        elif complexity == "medium":
            score += 1

        # Auth adjustment (no auth = higher score)
        if not auth_required:
            score += 1

        return min(score, 10)  # Cap at 10

    def _assess_chain_impact(self, vulnerability: Dict[str, Any]) -> int:
        """
        Assess chain impact severity (cross-domain pivot potential).

        CURRICULUM: Week 10 - Security Module
        This is the NEW assessment from vulnerability report 440782380.

        Assesses:
        - Can this pivot to other products?
        - Can this pivot to other domains?
        - Can this create downstream supply-chain issues?
        """
        can_pivot_products = vulnerability.get("can_pivot_products", False)
        can_pivot_domains = vulnerability.get("can_pivot_domains", False)
        supply_chain_impact = vulnerability.get("supply_chain_impact", False)
        local_execution = vulnerability.get("local_execution_surface", False)

        score = 1  # Base score

        # Local execution surfaces create global risk
        if local_execution:
            score += 3

        # Cross-product pivot
        if can_pivot_products:
            score += 3

        # Cross-domain pivot
        if can_pivot_domains:
            score += 2

        # Supply chain impact
        if supply_chain_impact:
            score += 2

        return min(score, 10)  # Cap at 10

    def _assess_blast_radius(self, vulnerability: Dict[str, Any]) -> int:
        """
        Assess blast radius (how many products/domains affected).

        CURRICULUM: Week 10 - Security Module
        Assesses ecosystem-wide impact.
        """
        affected_products = vulnerability.get("affected_products", [])
        affected_domains = vulnerability.get("affected_domains", [])

        product_count = len(affected_products) if isinstance(affected_products, list) else 0
        domain_count = len(affected_domains) if isinstance(affected_domains, list) else 0

        # Score based on number of products/domains
        score = min(product_count, 5) + min(domain_count, 5)

        return min(score, 10)  # Cap at 10

    def add_column_definition(self, column_def: ColumnDefinition):
        """Add or override a column definition."""
        self.column_defs[column_def.name.lower()] = column_def

    def classify_columns(self, columns: List[str]) -> Dict[str, ColumnDefinition]:
        """
        Classify columns in a dataset.

        Returns mapping of column name to its classification.
        """
        classifications = {}

        for col in columns:
            col_lower = col.lower().strip()

            # Direct match
            if col_lower in self.column_defs:
                classifications[col] = self.column_defs[col_lower]
                continue

            # Pattern matching
            matched = False
            for pattern, definition in self.column_defs.items():
                if pattern in col_lower or col_lower in pattern:
                    classifications[col] = definition
                    matched = True
                    break

            # Unknown column - default to confidential
            if not matched:
                classifications[col] = ColumnDefinition(
                    name=col,
                    meaning="Unknown - requires manual classification",
                    data_type="unknown",
                    example="",
                    sensitivity=SensitivityLevel.CONFIDENTIAL,
                    pii_type=PIIType.QUASI_ID,
                    notes="AUTO-CLASSIFIED: Review and update classification",
                )

        return classifications

    def check_pii_columns(
        self, df, classifications: Dict[str, ColumnDefinition]
    ) -> GovernanceCheckResult:
        """
        Check for PII columns that need handling.

        CURRICULUM: Week 1, Activity 1.1 - Build a Data Dictionary
        Learners identify PII columns and their hashing requirements.
        This check ensures all PII columns are properly classified.
        See: TEACHER_CORE_TRACK.md, Week 1, Activity 1.1
        """
        pii_columns = []
        unhandled_pii = []

        for col, defn in classifications.items():
            if defn.pii_type in [PIIType.DIRECT_ID, PIIType.SENSITIVE]:
                pii_columns.append(col)
                if col in df.columns and not defn.requires_hashing:
                    unhandled_pii.append(col)

        if unhandled_pii:
            return GovernanceCheckResult(
                passed=False,
                check_name="PII Column Check",
                severity="critical",
                message=f"Found {len(unhandled_pii)} PII columns without hashing requirement",
                details={"unhandled_columns": unhandled_pii},
                remediation="Update column definitions to require hashing for PII columns",
            )

        return GovernanceCheckResult(
            passed=True,
            check_name="PII Column Check",
            severity="info",
            message=f"Found {len(pii_columns)} PII columns, all properly classified",
            details={"pii_columns": pii_columns},
        )

    def check_prohibited_inferences(self, analysis_intent: List[str]) -> GovernanceCheckResult:
        """Check that analysis doesn't attempt prohibited inferences."""
        violations = []

        for intent in analysis_intent:
            for prohibited in PROHIBITED_INFERENCES:
                if any(word in intent.lower() for word in prohibited.lower().split()):
                    violations.append({"intent": intent, "prohibition": prohibited})

        if violations:
            return GovernanceCheckResult(
                passed=False,
                check_name="Prohibited Inference Check",
                severity="critical",
                message=f"Analysis intent violates {len(violations)} prohibited inference rules",
                details={"violations": violations},
                remediation="Remove or reframe analysis to avoid prohibited inferences",
            )

        return GovernanceCheckResult(
            passed=True,
            check_name="Prohibited Inference Check",
            severity="info",
            message="No prohibited inference violations detected",
        )

    def check_bias_guardrails(self, output_type: str) -> GovernanceCheckResult:
        """Check that output type has appropriate bias guardrails."""
        warnings = []

        for bias_type, guardrail in BIAS_GUARDRAILS.items():
            if bias_type in output_type.lower():
                warnings.append(
                    {
                        "type": bias_type,
                        "warning": guardrail["warning"],
                        "required_action": guardrail["required_action"],
                    }
                )

        if warnings:
            return GovernanceCheckResult(
                passed=True,  # Pass but with warnings
                check_name="Bias Guardrail Check",
                severity="warning",
                message=f"Output type requires {len(warnings)} bias guardrails",
                details={"guardrails": warnings},
                remediation="Ensure all required actions are implemented in output",
            )

        return GovernanceCheckResult(
            passed=True,
            check_name="Bias Guardrail Check",
            severity="info",
            message="No specific bias guardrails triggered",
        )

    def run_full_check(
        self,
        df,
        analysis_intents: Optional[List[str]] = None,
        output_types: Optional[List[str]] = None,
    ) -> GovernanceReport:
        """
        Run complete governance check on a dataset.

        Args:
            df: Pandas DataFrame to check
            analysis_intents: List of intended analyses (e.g., ["collaboration scoring", "skill gaps"])
            output_types: List of output types (e.g., ["high_activity ranking", "provider_rankings"])

        Returns:
            GovernanceReport with all results
        """
        import pandas as pd  # type: ignore[import-untyped]  # noqa: F401

        analysis_intents = analysis_intents or []
        output_types = output_types or []

        checks = []
        risk_flags = []
        review_reasons = []
        recommendations = []

        # 1. Classify all columns
        classifications = self.classify_columns(list(df.columns))

        # 2. Check for unknown columns
        unknown_cols = [col for col, defn in classifications.items() if "Unknown" in defn.meaning]
        if unknown_cols:
            checks.append(
                GovernanceCheckResult(
                    passed=True,
                    check_name="Unknown Column Check",
                    severity="warning",
                    message=f"Found {len(unknown_cols)} unclassified columns",
                    details={"columns": unknown_cols},
                    remediation="Review and classify these columns manually",
                )
            )
            risk_flags.append(f"UNCLASSIFIED_COLUMNS:{len(unknown_cols)}")
            recommendations.append("Review and classify unknown columns before production use")

        # 3. Check PII handling
        pii_check = self.check_pii_columns(df, classifications)
        checks.append(pii_check)
        if not pii_check.passed:
            risk_flags.append("PII_HANDLING_REQUIRED")
            review_reasons.append("PII columns require proper handling before analysis")

        # 4. Check prohibited inferences
        if analysis_intents:
            inference_check = self.check_prohibited_inferences(analysis_intents)
            checks.append(inference_check)
            if not inference_check.passed:
                risk_flags.append("PROHIBITED_INFERENCE_ATTEMPT")
                review_reasons.append("Analysis intent includes prohibited inferences")

        # 5. Check bias guardrails
        for output_type in output_types:
            bias_check = self.check_bias_guardrails(output_type)
            checks.append(bias_check)
            if bias_check.severity == "warning":
                risk_flags.append(f"BIAS_GUARDRAIL:{output_type}")

        # 6. Check for sensitive combinations (k-anonymity proxy)
        quasi_id_cols = [
            col
            for col, defn in classifications.items()
            if defn.pii_type == PIIType.QUASI_ID and col in df.columns
        ]
        if len(quasi_id_cols) >= 3:
            # Check if combinations could identify individuals
            checks.append(
                GovernanceCheckResult(
                    passed=True,
                    check_name="Quasi-Identifier Combination Check",
                    severity="warning",
                    message=f"Dataset has {len(quasi_id_cols)} quasi-identifiers that could combine to identify individuals",
                    details={"quasi_identifiers": quasi_id_cols},
                    remediation="Consider k-anonymity or l-diversity before releasing aggregated data",
                )
            )
            recommendations.append("Apply k-anonymity (k≥5) before any external data sharing")

        # 7. Data quality check
        null_percentages = {}
        for col in df.columns:
            null_pct = df[col].isna().sum() / len(df) * 100
            if null_pct > 50:
                null_percentages[col] = null_pct

        if null_percentages:
            checks.append(
                GovernanceCheckResult(
                    passed=True,
                    check_name="Data Quality Check",
                    severity="warning",
                    message=f"Found {len(null_percentages)} columns with >50% null values",
                    details={"high_null_columns": null_percentages},
                    remediation="Review data completeness before analysis",
                )
            )

        # Determine overall status
        critical_failures = [c for c in checks if not c.passed and c.severity == "critical"]
        overall_passed = len(critical_failures) == 0
        review_required = len(review_reasons) > 0 or len(risk_flags) > 3

        # Enhanced severity assessment for any vulnerabilities found
        # (This would be called when processing security reports)
        if risk_flags:
            # Example: assess severity if this were a vulnerability report
            # In practice, this would be called separately for actual vulnerabilities
            pass

        if review_required and "Human review triggered" not in review_reasons:
            review_reasons.append("Human review triggered by Triple Balance rule")

        # Build report
        report = GovernanceReport(
            dataset_id=f"dataset_{datetime.now().strftime('%Y%m%d_%H%M%S')}",
            checked_at=datetime.now(),
            overall_passed=overall_passed,
            checks=checks,
            risk_flags=risk_flags,
            review_required=review_required,
            review_reasons=review_reasons,
            recommendations=recommendations,
            pii_stats=self.pii_handler.get_stats(),
            column_classifications={
                col: defn.sensitivity.value for col, defn in classifications.items()
            },
        )

        return report

    def apply_pii_protection(self, df, classifications: Dict[str, ColumnDefinition]):
        """
        Apply PII protection to a DataFrame.

        Returns a new DataFrame with PII hashed/masked.
        """
        import pandas as pd  # type: ignore[import-untyped]  # noqa: F401

        df_protected = df.copy()

        for col, defn in classifications.items():
            if col not in df_protected.columns:
                continue

            if defn.requires_hashing:
                if "email" in col.lower():
                    df_protected[col] = df_protected[col].apply(
                        lambda x: self.pii_handler.hash_email_preserve_domain(x)
                        if pd.notna(x)
                        else x
                    )
                else:
                    df_protected[col] = df_protected[col].apply(
                        lambda x: self.pii_handler.hash_value(x, col) if pd.notna(x) else x
                    )

            if defn.requires_masking:
                df_protected[col] = df_protected[col].apply(
                    lambda x: self.pii_handler.mask_path(x) if pd.notna(x) else x
                )

        return df_protected

    def assess_vulnerability(self, vulnerability_report: Dict[str, Any]) -> Dict[str, Any]:
        """
        Assess vulnerability with enhanced severity scoring.

        CURRICULUM: Week 0, Activity 0.3 - Governance Gate
        CURRICULUM: Week 10 - Security Module

        This method implements the enhanced severity scoring from vulnerability
        report 440782380, which includes chain impact and blast radius assessment.

        Key Rule: "A report can be 'duplicate entry point' but still trigger:
        - Architecture-level mitigation
        - Ecosystem risk review
        - Cross-product policy changes"

        See: SECURITY_VULNERABILITY_RESPONSE.md, Severity & Governance Rubric Update
        """
        severity_score = self.assess_severity(vulnerability_report)

        result = {
            "vulnerability_id": vulnerability_report.get("id", "unknown"),
            "severity_score": severity_score.to_dict(),
            "requires_architecture_mitigation": severity_score.requires_architecture_mitigation(),
            "requires_ecosystem_review": severity_score.requires_ecosystem_review(),
            "recommendations": [],
        }

        # Generate recommendations based on severity
        if severity_score.chain_impact >= 7:
            result["recommendations"].append(
                "High chain impact detected - implement cross-domain access controls"
            )

        if severity_score.blast_radius >= 7:
            result["recommendations"].append(
                "High blast radius - review all affected products and domains"
            )

        if severity_score.requires_architecture_mitigation():
            result["recommendations"].append(
                "Architecture-level mitigation required - not just a patch"
            )

        if severity_score.requires_ecosystem_review():
            result["recommendations"].append(
                "Ecosystem risk review required - assess cross-product impact"
            )

        return result


# =============================================================================
# TRIPLE BALANCE REVIEW TRIGGER
# =============================================================================


@dataclass
class TripleBalanceReview:
    """
    Tracks when Triple Balance review is needed.

    Reviews are triggered when:
    - Risk flags exceed threshold
    - Governance checks fail
    - High-impact decisions are made
    - Anomalous patterns detected
    """

    trigger_reason: str
    triggered_at: datetime
    logic_assessment: str = ""
    dissent_points: List[str] = field(default_factory=list)
    intuition_flags: List[str] = field(default_factory=list)
    resolved: bool = False
    resolution: str = ""

    def to_dict(self) -> Dict[str, Any]:
        return {
            "trigger_reason": self.trigger_reason,
            "triggered_at": self.triggered_at.isoformat(),
            "logic_assessment": self.logic_assessment,
            "dissent_points": self.dissent_points,
            "intuition_flags": self.intuition_flags,
            "resolved": self.resolved,
            "resolution": self.resolution,
        }


def create_data_dictionary(classifications: Dict[str, ColumnDefinition]) -> str:
    """Generate a markdown data dictionary from classifications."""
    lines = [
        "# Data Dictionary",
        "",
        "| Column | Meaning | Type | Sensitivity | PII Type | Requires Hashing | Notes |",
        "|--------|---------|------|-------------|----------|------------------|-------|",
    ]

    for col, defn in sorted(classifications.items()):
        lines.append(
            f"| {defn.name} | {defn.meaning} | {defn.data_type} | "
            f"{defn.sensitivity.value} | {defn.pii_type.value} | "
            f"{'Yes' if defn.requires_hashing else 'No'} | {defn.notes} |"
        )

    lines.extend(["", "## Prohibited Inferences", ""])
    for prohibition in PROHIBITED_INFERENCES:
        lines.append(f"- ❌ {prohibition}")

    lines.extend(["", "## Bias Guardrails", ""])
    for bias_type, guardrail in BIAS_GUARDRAILS.items():
        lines.append(f"### {bias_type}")
        lines.append(f"- ⚠️ **Warning:** {guardrail['warning']}")
        lines.append(f"- 📝 **Context:** {guardrail['context']}")
        lines.append(f"- ✅ **Required:** {guardrail['required_action']}")
        lines.append("")

    return "\n".join(lines)


# =============================================================================
# MAIN - Demo/Test
# =============================================================================

if __name__ == "__main__":
    print("=" * 60)
    print("  COSURVIVAL GOVERNANCE MODULE - Self Test")
    print("=" * 60)

    # Test PII handler
    print("\n1. Testing PII Handler...")
    handler = PIIHandler(allow_reversal=True)

    test_values = [
        ("john.smith@company.com", "email"),
        ("Jane Doe", "name"),
        ("user_12345", "uid"),
    ]

    for value, col in test_values:
        hashed = handler.hash_value(value, col)
        print(f"   {col}: '{value}' → '{hashed}'")

    # Test email domain preservation
    email_hashed = handler.hash_email_preserve_domain("jane@techcorp.com")
    print(f"   Email (domain preserved): 'jane@techcorp.com' → '{email_hashed}'")

    # Test path masking
    path_masked = handler.mask_path("/home/john/documents/secret_project/budget.xlsx")
    print(f"   Path masked: '/home/john/documents/secret_project/budget.xlsx' → '{path_masked}'")

    print(f"\n   PII Stats: {handler.get_stats()}")

    # Test governance gate
    print("\n2. Testing Governance Gate...")
    gate = GovernanceGate(handler)

    # Simulate a dataset
    import pandas as pd  # type: ignore[import-untyped]

    test_df = pd.DataFrame(
        {
            "Uid": ["user_1", "user_2", "user_3"],
            "Name": ["Alice", "Bob", "Carol"],
            "Email": ["alice@co.com", "bob@co.com", "carol@co.com"],
            "CompanyId": ["c1", "c1", "c2"],
            "Type": ["login", "file_access", "permission_change"],
            "UnknownColumn": ["x", "y", "z"],
        }
    )

    report = gate.run_full_check(
        test_df,
        analysis_intents=["collaboration scoring", "skill gap analysis"],
        output_types=["high_activity rankings", "provider_rankings"],
    )

    print(f"   Overall Passed: {report.overall_passed}")
    print(f"   Risk Flags: {report.risk_flags}")
    print(f"   Review Required: {report.review_required}")
    print(f"   Review Reasons: {report.review_reasons}")

    for check in report.checks:
        status = "✓" if check.passed else "✗"
        print(f"   {status} [{check.severity}] {check.check_name}: {check.message}")

    # Generate data dictionary
    print("\n3. Generating Data Dictionary...")
    classifications = gate.classify_columns(list(test_df.columns))
    data_dict = create_data_dictionary(classifications)
    print("   Generated data dictionary (preview):")
    print("   " + "\n   ".join(data_dict.split("\n")[:10]))

    print("\n" + "=" * 60)
    print("  GOVERNANCE MODULE READY")
    print("=" * 60)
