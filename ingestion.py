#!/usr/bin/env python3
"""
COSURVIVAL SCHEMA-FIRST INGESTION PIPELINE
==========================================
Clean, validated data ingestion that produces canonical entities.

This module:
1. Validates and normalizes raw CSV/JSON data
2. Handles missing fields, mixed types, inconsistent IDs
3. Produces canonical entities: User, Company, Group, Provider, Resource, Activity, PermissionChange
4. Outputs a unified intermediate format (Parquet or JSONL)

NOTHING reaches the analysis layer without passing through here.

CURRICULUM MAPPING:
-------------------
Week 1: Fundamentals - Canonical Entities
  - Activity 1.1: Build a Data Dictionary (column classification)
  - Introduces the seven canonical entities
  - See: TEACHER_CORE_TRACK.md, Week 1, Core Concepts #1

Week 2: Data Structures - Canonical Representations
  - Activity 2.1: Design Your Schema (User, Activity, PermissionChange)
  - Activity 2.3: Validation Rules (is_valid_user, is_valid_activity)
  - See: TEACHER_CORE_TRACK.md, Week 2, Core Concepts #1

Week 7: SQL - Database Design
  - Similar concepts: schema design, entity relationships
  - See: TEACHER_CORE_TRACK.md, Week 7 (if applicable)
"""

# Standard library imports
import hashlib
import json
from collections import defaultdict
from dataclasses import dataclass, field, asdict
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional, Any

# Third-party imports
import pandas as pd  # type: ignore[import-untyped]

# Local imports
from governance import (
    GovernanceGate,
    PIIHandler,
    GovernanceReport,
    create_data_dictionary,
)


# =============================================================================
# CANONICAL ENTITY SCHEMAS
# =============================================================================


@dataclass
class CanonicalUser:
    """
    Canonical user entity.

    CURRICULUM: Week 1, Core Concepts #1 - Canonical Entities
    One of the seven canonical entities introduced in Week 1.
    See: TEACHER_CORE_TRACK.md, Week 1, Core Concepts #1

    CURRICULUM: Week 2, Activity 2.1 - Design Your Schema
    Learners design complete schemas for User, Activity, PermissionChange.
    This is the reference implementation.
    See: TEACHER_CORE_TRACK.md, Week 2, Activity 2.1

    Key design decisions:
    - id is hashed for privacy (Week 0, Activity 0.3 - PII handling)
    - email_domain preserved for org analysis (not full email)
    - roles and groups as lists (Week 2 - data structures)
    """

    id: str  # Hashed/pseudonymized
    original_id_hash: str  # For consistency checking
    email_domain: str = ""  # Preserved for org analysis
    company_id: str = ""
    first_seen: Optional[str] = None
    last_seen: Optional[str] = None
    activity_count: int = 0
    roles: List[str] = field(default_factory=list)
    groups: List[str] = field(default_factory=list)


@dataclass
class CanonicalCompany:
    """Canonical company/organization entity."""

    id: str
    name: str = ""
    user_count: int = 0
    group_count: int = 0
    first_seen: Optional[str] = None
    last_seen: Optional[str] = None
    activity_count: int = 0
    providers: List[str] = field(default_factory=list)


@dataclass
class CanonicalGroup:
    """Canonical group/team entity."""

    id: str
    name: str = ""
    company_id: str = ""
    member_count: int = 0
    first_seen: Optional[str] = None
    last_seen: Optional[str] = None
    activity_count: int = 0


@dataclass
class CanonicalProvider:
    """Canonical provider/service entity."""

    id: str
    name: str = ""
    schemes: List[str] = field(default_factory=list)
    customer_companies: List[str] = field(default_factory=list)
    user_count: int = 0
    activity_count: int = 0
    error_count: int = 0
    first_seen: Optional[str] = None
    last_seen: Optional[str] = None


@dataclass
class CanonicalResource:
    """Canonical resource entity (file, path, etc.)."""

    id: str  # Hash of masked path
    path_pattern: str  # Masked/generalized path
    resource_type: str = ""  # file, folder, api, etc.
    access_count: int = 0
    unique_accessors: int = 0


@dataclass
class CanonicalActivity:
    """
    Canonical activity/event record.

    CURRICULUM: Week 0, Core Concepts #1 - Everything is 0s and 1s
    The same activity row can be viewed through TRIBE/TEACHER/RECON lenses.
    This dataclass captures the raw event that gets interpreted differently.
    See: TEACHER_CORE_TRACK.md, Week 0, Core Concepts #1

    CURRICULUM: Week 2, Activity 2.1 - Design Your Schema
    Learners design schemas for Activity as part of Week 2.
    See: TEACHER_CORE_TRACK.md, Week 2, Activity 2.1

    CURRICULUM: Week 2, Activity 2.3 - Validation Rules
    Learners write is_valid_activity() function.
    This dataclass defines what a valid activity looks like.
    See: TEACHER_CORE_TRACK.md, Week 2, Activity 2.3

    Key fields:
    - target_user_id: For TRIBE lens (who interacted with whom)
    - state_before/state_after: For TEACHER lens (permission upgrades = skills)
    - provider_id: For RECON lens (value exchange)
    """

    id: str
    timestamp: str  # ISO format
    timestamp_date: str  # YYYY-MM-DD for aggregation
    activity_type: str
    user_id: str
    company_id: str = ""
    group_id: str = ""
    provider_id: str = ""
    resource_id: str = ""
    target_user_id: str = ""  # For interactions
    state_before: str = ""
    state_after: str = ""
    error_code: str = ""
    is_internal: bool = True
    metadata: Dict[str, Any] = field(default_factory=dict)


@dataclass
class CanonicalPermissionChange:
    """
    Canonical permission change record.

    CURRICULUM: Week 0, Core Concepts #3 - Privileges = Skills
    Key insight: "When someone gets permission to do something new,
    they're demonstrating readiness. Permission changes are skill
    acquisitions in disguise."
    See: TEACHER_CORE_TRACK.md, Week 0, Core Concepts #3

    Example: StateOld: "viewer" → StateNew: "editor"
    TEACHER interpretation: This person has grown from consuming
    information to creating it.

    CURRICULUM: Week 2, Activity 2.1 - Design Your Schema
    Learners design schemas for PermissionChange.
    See: TEACHER_CORE_TRACK.md, Week 2, Activity 2.1

    CURRICULUM: Week 3, Core Concepts #2 - TEACHER Algorithms
    Used in role_mastery_profile() to build skill profiles.
    See: TEACHER_CORE_TRACK.md, Week 3, Core Concepts #2
    """

    id: str
    timestamp: str
    user_id: str
    granted_by_id: str = ""
    permission_type: str = ""
    permission_action: str = ""  # grant, revoke, modify
    role_id: str = ""
    resource_id: str = ""
    state_before: str = ""
    state_after: str = ""


# =============================================================================
# SCHEMA DETECTION & MAPPING
# =============================================================================


class ColumnMapper:
    """
    Maps raw column names to canonical field names.
    Uses fuzzy matching and pattern recognition.

    CURRICULUM: Week 1, Core Concepts #3 - Schema Detection
    "Patterns matter more than exact column names."
    Examples: "Uid" → user_id, "CompanyName" → company_name
    See: TEACHER_CORE_TRACK.md, Week 1, Core Concepts #3

    This class implements the schema detection logic that allows
    the system to work with different CSV formats without manual mapping.
    """

    # Canonical field -> possible raw column patterns
    FIELD_PATTERNS = {
        # User identifiers
        "user_id": ["uid", "userid", "user_id", "useridentifier", "actor", "actorid"],
        "user_name": ["name", "username", "displayname", "fullname", "user_name"],
        "user_email": ["email", "mail", "emailaddress", "useremail"],
        # Target user (for interactions)
        "target_user_id": ["uidopp", "uid_opp", "targetuser", "targetuserid", "opposinguser"],
        "requesting_user_id": ["uidreq", "uid_req", "requestinguser", "initiator", "requester"],
        # Organization
        "company_id": ["companyid", "company_id", "orgid", "organizationid", "tenantid"],
        "company_name": ["companyname", "company_name", "orgname", "organization", "tenant"],
        "group_id": ["groupid", "group_id", "teamid", "team_id", "departmentid"],
        "group_name": ["groupname", "group_name", "teamname", "team_name", "department"],
        # Provider
        "provider_id": ["pid", "providerid", "provider_id", "serviceid", "service_id"],
        "provider_name": ["providername", "provider_name", "servicename", "service_name"],
        "scheme": ["scheme", "protocol", "method", "authscheme"],
        # Role/Permission
        "role_id": ["roleid", "role_id", "role"],
        "role_name": ["rolename", "role_name"],
        "privilege": ["privilege", "privileges", "permission", "permissions", "access", "rights"],
        "privilege_action": ["privilegeactions", "privilege_actions", "permissionaction"],
        # Activity
        "activity_type": [
            "type",
            "activitytype",
            "activity_type",
            "action",
            "eventtype",
            "event_type",
        ],
        "timestamp": ["date", "timestamp", "datetime", "created", "createdat", "time", "eventtime"],
        # State
        "state_before": ["stateold", "state_old", "previousstate", "oldstate", "before"],
        "state_after": ["statenew", "state_new", "newstate", "currentstate", "after"],
        # Resource
        "resource_path": ["path", "filepath", "resource", "listpathactual", "resourcepath", "file"],
        "resource_path_virtual": ["listpathvirtual", "virtualpath", "displaypath"],
        # Error
        "error_code": [
            "codeerror",
            "code_error",
            "error",
            "errorcode",
            "error_code",
            "errormessage",
        ],
        # Flags
        "is_internal": ["internal", "isinternal", "is_internal", "internaluser"],
    }

    def __init__(self) -> None:
        self.mappings: Dict[str, str] = {}  # raw_col -> canonical_field
        self.reverse_mappings: Dict[str, str] = {}  # canonical_field -> raw_col
        self.unmapped: List[str] = []

    def detect_mappings(self, columns: List[str]) -> Dict[str, str]:
        """
        Detect mappings from raw columns to canonical fields.

        Returns:
            Dict mapping raw column names to canonical field names
        """
        self.mappings = {}
        self.reverse_mappings = {}
        self.unmapped = []

        # Normalize column names for matching
        normalized = {col: col.lower().strip().replace(" ", "").replace("_", "") for col in columns}

        for col, norm_col in normalized.items():
            matched = False

            for canonical_field, patterns in self.FIELD_PATTERNS.items():
                for pattern in patterns:
                    pattern_norm = pattern.lower().replace("_", "")

                    # Exact match
                    if norm_col == pattern_norm:
                        self.mappings[col] = canonical_field
                        self.reverse_mappings[canonical_field] = col
                        matched = True
                        break

                    # Substring match (careful with short patterns)
                    if len(pattern_norm) >= 4 and pattern_norm in norm_col:
                        if canonical_field not in self.reverse_mappings:
                            self.mappings[col] = canonical_field
                            self.reverse_mappings[canonical_field] = col
                            matched = True
                            break

                if matched:
                    break

            if not matched:
                self.unmapped.append(col)

        return self.mappings

    def get_canonical_field(self, raw_col: str) -> Optional[str]:
        """Get canonical field name for a raw column."""
        return self.mappings.get(raw_col)

    def get_raw_column(self, canonical_field: str) -> Optional[str]:
        """Get raw column name for a canonical field."""
        return self.reverse_mappings.get(canonical_field)

    def get_mapping_report(self) -> Dict[str, Any]:
        """Generate a report of the mapping results."""
        return {
            "total_columns": len(self.mappings) + len(self.unmapped),
            "mapped_columns": len(self.mappings),
            "unmapped_columns": len(self.unmapped),
            "mappings": self.mappings,
            "unmapped": self.unmapped,
            "coverage": len(self.mappings) / (len(self.mappings) + len(self.unmapped))
            if (len(self.mappings) + len(self.unmapped)) > 0
            else 0,
        }


# =============================================================================
# DATA NORMALIZERS
# =============================================================================


class DataNormalizer:
    """Handles data type normalization and cleaning."""

    @staticmethod
    def normalize_timestamp(value: Any) -> Optional[str]:
        """Normalize timestamp to ISO format."""
        if pd.isna(value) or value is None:
            return None

        # Already a datetime
        if isinstance(value, datetime):
            return value.isoformat()

        str_value = str(value).strip()
        if not str_value or str_value.lower() in ["nan", "nat", "none", ""]:
            return None

        # Try common formats
        formats = [
            "%Y-%m-%dT%H:%M:%S.%fZ",
            "%Y-%m-%dT%H:%M:%SZ",
            "%Y-%m-%dT%H:%M:%S",
            "%Y-%m-%d %H:%M:%S.%f",
            "%Y-%m-%d %H:%M:%S",
            "%Y-%m-%d",
            "%m/%d/%Y %H:%M:%S",
            "%m/%d/%Y",
            "%d/%m/%Y %H:%M:%S",
            "%d/%m/%Y",
        ]

        for fmt in formats:
            try:
                dt = datetime.strptime(str_value, fmt)
                return dt.isoformat()
            except ValueError:
                continue

        # Try pandas parser as fallback
        try:
            dt = pd.to_datetime(str_value)
            if pd.notna(dt):
                return dt.isoformat()
        except (ValueError, TypeError):
            pass

        return None

    @staticmethod
    def normalize_boolean(value: Any) -> Optional[bool]:
        """Normalize to boolean."""
        if pd.isna(value) or value is None:
            return None

        if isinstance(value, bool):
            return value

        str_value = str(value).strip().lower()

        if str_value in ["true", "1", "yes", "y", "t"]:
            return True
        if str_value in ["false", "0", "no", "n", "f"]:
            return False

        return None

    @staticmethod
    def normalize_id(value: Any) -> str:
        """Normalize ID to string, handling various formats."""
        if pd.isna(value) or value is None:
            return ""

        str_value = str(value).strip()

        # Handle float IDs (e.g., 12345.0)
        if "." in str_value:
            try:
                float_val = float(str_value)
                if float_val == int(float_val):
                    return str(int(float_val))
            except (ValueError, TypeError):
                pass

        return str_value

    @staticmethod
    def normalize_string(value: Any) -> str:
        """Normalize string value."""
        if pd.isna(value) or value is None:
            return ""
        return str(value).strip()

    @staticmethod
    def extract_date(timestamp: Optional[str]) -> Optional[str]:
        """Extract date (YYYY-MM-DD) from ISO timestamp."""
        if not timestamp:
            return None
        try:
            return timestamp[:10]
        except (TypeError, IndexError):
            return None


# =============================================================================
# INGESTION PIPELINE
# =============================================================================


class IngestionPipeline:
    """
    Main ingestion pipeline that transforms raw data into canonical entities.
    """

    def __init__(self, governance_enabled: bool = True, pii_reversal: bool = False):
        """
        Initialize ingestion pipeline.

        Args:
            governance_enabled: Whether to run governance checks
            pii_reversal: Whether to allow PII reverse lookup (requires explicit permission)
        """
        self.governance_enabled = governance_enabled
        self.pii_handler = PIIHandler(allow_reversal=pii_reversal)
        self.governance_gate = GovernanceGate(self.pii_handler) if governance_enabled else None
        self.column_mapper = ColumnMapper()
        self.normalizer = DataNormalizer()

        # Extracted entities
        self.users: Dict[str, CanonicalUser] = {}
        self.companies: Dict[str, CanonicalCompany] = {}
        self.groups: Dict[str, CanonicalGroup] = {}
        self.providers: Dict[str, CanonicalProvider] = {}
        self.resources: Dict[str, CanonicalResource] = {}
        self.activities: List[CanonicalActivity] = []
        self.permission_changes: List[CanonicalPermissionChange] = []

        # Tracking
        self.raw_row_count = 0
        self.processed_row_count = 0
        self.error_rows: List[Dict[str, Any]] = []
        self.governance_report: Optional[GovernanceReport] = None

    def load_csv(self, filepath: str, encoding: Optional[str] = None) -> pd.DataFrame:
        """
        Load CSV file with auto-encoding detection.

        CURRICULUM: Week 10 - Security Module
        Now includes content validation before loading.
        See: SECURITY_TRUST_FABRIC.md, Content & Execution Security
        """
        # Validate content before loading (security check)
        try:
            from security import validate_content_package

            validation_result = validate_content_package(filepath)
            if not validation_result.is_valid:
                raise ValueError(
                    f"Content validation failed: {', '.join(validation_result.issues)}. "
                    f"See: SECURITY_CONTROLS_CHECKLIST.md, Content & Execution Security"
                )

            if validation_result.warnings:
                print(f"⚠ Content validation warnings: {', '.join(validation_result.warnings)}")

            if validation_result.requires_sandbox:
                print("⚠ Content requires sandbox execution - proceed with caution")
        except ImportError:
            # Security module not available - skip validation (not recommended)
            print("⚠ Security module not available - skipping content validation")
        except Exception as e:
            # Don't fail on validation errors, but log them
            print(f"⚠ Content validation error: {e}")

        encodings = [encoding] if encoding else ["utf-8", "latin-1", "cp1252", "iso-8859-1"]

        for enc in encodings:
            try:
                df = pd.read_csv(filepath, encoding=enc, low_memory=False)
                print(f"✓ Loaded {len(df):,} rows with {len(df.columns)} columns (encoding: {enc})")
                self.raw_row_count = len(df)
                return df
            except UnicodeDecodeError:
                continue
            except Exception as e:
                print(f"✗ Error loading with {enc}: {e}")
                continue

        raise ValueError(f"Could not load CSV from {filepath}")

    def run_governance_check(self, df: pd.DataFrame) -> GovernanceReport:
        """Run governance checks on the raw data."""
        if not self.governance_gate:
            raise ValueError("Governance not enabled")

        print("\n🔒 Running Governance Checks...")

        self.governance_report = self.governance_gate.run_full_check(
            df,
            analysis_intents=[
                "collaboration network analysis",
                "skill gap identification",
                "learning pathway recommendation",
                "provider reliability scoring",
                "value flow mapping",
            ],
            output_types=[
                "high_activity rankings",
                "collaboration_score",
                "provider_rankings",
                "skill_gaps",
            ],
        )

        # Print summary
        status = "✓ PASSED" if self.governance_report.overall_passed else "✗ FAILED"
        print(f"\n   Governance Check: {status}")
        print(f"   Risk Flags: {len(self.governance_report.risk_flags)}")
        print(f"   Review Required: {self.governance_report.review_required}")

        for check in self.governance_report.checks:
            icon = "✓" if check.passed else "✗"
            print(f"   {icon} [{check.severity}] {check.check_name}")

        if self.governance_report.recommendations:
            print("\n   Recommendations:")
            for rec in self.governance_report.recommendations:
                print(f"   → {rec}")

        return self.governance_report

    def detect_schema(self, df: pd.DataFrame) -> Dict[str, Any]:
        """Detect and map the schema."""
        print("\n📋 Detecting Schema...")

        self.column_mapper.detect_mappings(list(df.columns))
        report = self.column_mapper.get_mapping_report()

        print(
            f"   Mapped: {report['mapped_columns']}/{report['total_columns']} columns ({report['coverage']:.1%})"
        )

        if report["unmapped"]:
            print(
                f"   Unmapped columns: {report['unmapped'][:10]}{'...' if len(report['unmapped']) > 10 else ''}"
            )

        return report

    def _get_value(self, row: pd.Series, canonical_field: str, default: Any = "") -> Any:
        """Get value from row using canonical field mapping."""
        raw_col = self.column_mapper.get_raw_column(canonical_field)
        if raw_col and raw_col in row.index:
            return row[raw_col]
        return default

    def _hash_id(self, value: Any, field_type: str = "") -> str:
        """Hash an ID value for privacy."""
        normalized = self.normalizer.normalize_id(value)
        if not normalized:
            return ""
        return self.pii_handler.hash_value(normalized, field_type)

    def extract_entities(self, df: pd.DataFrame) -> Dict[str, Any]:
        """Extract all canonical entities from the data."""
        print("\n🔄 Extracting Canonical Entities...")

        # Apply PII protection first
        if self.governance_gate:
            classifications = self.governance_gate.classify_columns(list(df.columns))
            df_protected = self.governance_gate.apply_pii_protection(df, classifications)
        else:
            df_protected = df

        # Track first/last seen
        user_times: Dict[str, List[str]] = defaultdict(list)
        company_times: Dict[str, List[str]] = defaultdict(list)
        group_times: Dict[str, List[str]] = defaultdict(list)
        provider_times: Dict[str, List[str]] = defaultdict(list)

        # Process each row
        for idx, row in df_protected.iterrows():
            try:
                # Extract timestamp
                timestamp = self.normalizer.normalize_timestamp(self._get_value(row, "timestamp"))
                timestamp_date = self.normalizer.extract_date(timestamp)

                # Extract user
                user_id = self.normalizer.normalize_id(self._get_value(row, "user_id"))
                if user_id:
                    if user_id not in self.users:
                        email = self._get_value(row, "user_email", "")
                        email_domain = email.split("@")[1] if "@" in str(email) else ""

                        self.users[user_id] = CanonicalUser(
                            id=user_id,
                            original_id_hash=hashlib.md5(user_id.encode()).hexdigest()[:8],
                            email_domain=email_domain,
                            company_id=self.normalizer.normalize_id(
                                self._get_value(row, "company_id")
                            ),
                        )

                    self.users[user_id].activity_count += 1
                    if timestamp:
                        user_times[user_id].append(timestamp)

                    # Track roles
                    role_id = self.normalizer.normalize_id(self._get_value(row, "role_id"))
                    if role_id and role_id not in self.users[user_id].roles:
                        self.users[user_id].roles.append(role_id)

                    # Track groups
                    group_id = self.normalizer.normalize_id(self._get_value(row, "group_id"))
                    if group_id and group_id not in self.users[user_id].groups:
                        self.users[user_id].groups.append(group_id)

                # Extract company
                company_id = self.normalizer.normalize_id(self._get_value(row, "company_id"))
                if company_id:
                    if company_id not in self.companies:
                        self.companies[company_id] = CanonicalCompany(
                            id=company_id,
                            name=self.normalizer.normalize_string(
                                self._get_value(row, "company_name")
                            ),
                        )

                    self.companies[company_id].activity_count += 1
                    if timestamp:
                        company_times[company_id].append(timestamp)

                # Extract group
                group_id = self.normalizer.normalize_id(self._get_value(row, "group_id"))
                if group_id:
                    if group_id not in self.groups:
                        self.groups[group_id] = CanonicalGroup(
                            id=group_id,
                            name=self.normalizer.normalize_string(
                                self._get_value(row, "group_name")
                            ),
                            company_id=company_id,
                        )

                    self.groups[group_id].activity_count += 1
                    if timestamp:
                        group_times[group_id].append(timestamp)

                # Extract provider
                provider_id = self.normalizer.normalize_id(self._get_value(row, "provider_id"))
                if provider_id:
                    if provider_id not in self.providers:
                        self.providers[provider_id] = CanonicalProvider(
                            id=provider_id,
                            name=self.normalizer.normalize_string(
                                self._get_value(row, "provider_name")
                            ),
                        )

                    self.providers[provider_id].activity_count += 1
                    if timestamp:
                        provider_times[provider_id].append(timestamp)

                    # Track scheme
                    scheme = self.normalizer.normalize_string(self._get_value(row, "scheme"))
                    if scheme and scheme not in self.providers[provider_id].schemes:
                        self.providers[provider_id].schemes.append(scheme)

                    # Track customer
                    if (
                        company_id
                        and company_id not in self.providers[provider_id].customer_companies
                    ):
                        self.providers[provider_id].customer_companies.append(company_id)

                    # Track errors
                    error_code = self.normalizer.normalize_string(
                        self._get_value(row, "error_code")
                    )
                    if error_code:
                        self.providers[provider_id].error_count += 1

                # Extract resource
                resource_path = self.normalizer.normalize_string(
                    self._get_value(row, "resource_path")
                )
                if resource_path:
                    # Hash the path for ID
                    resource_id = hashlib.md5(resource_path.encode()).hexdigest()[:12]

                    if resource_id not in self.resources:
                        self.resources[resource_id] = CanonicalResource(
                            id=resource_id,
                            path_pattern=resource_path,
                            resource_type=self._infer_resource_type(resource_path),
                        )

                    self.resources[resource_id].access_count += 1

                # Create activity record
                activity_type = self.normalizer.normalize_string(
                    self._get_value(row, "activity_type")
                )
                if activity_type:
                    activity = CanonicalActivity(
                        id=f"act_{idx}",
                        timestamp=timestamp or "",
                        timestamp_date=timestamp_date or "",
                        activity_type=activity_type,
                        user_id=user_id,
                        company_id=company_id,
                        group_id=group_id,
                        provider_id=provider_id,
                        resource_id=resource_id if resource_path else "",
                        target_user_id=self.normalizer.normalize_id(
                            self._get_value(row, "target_user_id")
                        ),
                        state_before=self.normalizer.normalize_string(
                            self._get_value(row, "state_before")
                        ),
                        state_after=self.normalizer.normalize_string(
                            self._get_value(row, "state_after")
                        ),
                        error_code=self.normalizer.normalize_string(
                            self._get_value(row, "error_code")
                        ),
                        is_internal=self.normalizer.normalize_boolean(
                            self._get_value(row, "is_internal")
                        )
                        or True,
                    )
                    self.activities.append(activity)

                # Check for permission change
                state_before = self.normalizer.normalize_string(
                    self._get_value(row, "state_before")
                )
                state_after = self.normalizer.normalize_string(self._get_value(row, "state_after"))
                privilege = self.normalizer.normalize_string(self._get_value(row, "privilege"))

                if state_before and state_after and state_before != state_after:
                    perm_change = CanonicalPermissionChange(
                        id=f"perm_{idx}",
                        timestamp=timestamp or "",
                        user_id=user_id,
                        granted_by_id=self.normalizer.normalize_id(
                            self._get_value(row, "requesting_user_id")
                        ),
                        permission_type=privilege,
                        permission_action="change",
                        role_id=self.normalizer.normalize_id(self._get_value(row, "role_id")),
                        state_before=state_before,
                        state_after=state_after,
                    )
                    self.permission_changes.append(perm_change)

                self.processed_row_count += 1

            except Exception as e:
                self.error_rows.append({"row_index": idx, "error": str(e)})

        # Set first/last seen times
        for uid, times in user_times.items():
            if times:
                self.users[uid].first_seen = min(times)
                self.users[uid].last_seen = max(times)

        for cid, times in company_times.items():
            if times:
                self.companies[cid].first_seen = min(times)
                self.companies[cid].last_seen = max(times)

        for gid, times in group_times.items():
            if times:
                self.groups[gid].first_seen = min(times)
                self.groups[gid].last_seen = max(times)

        for pid, times in provider_times.items():
            if times:
                self.providers[pid].first_seen = min(times)
                self.providers[pid].last_seen = max(times)

        # Calculate derived counts
        for company in self.companies.values():
            company.user_count = len([u for u in self.users.values() if u.company_id == company.id])
            company.group_count = len(
                [g for g in self.groups.values() if g.company_id == company.id]
            )

        for group in self.groups.values():
            group.member_count = len([u for u in self.users.values() if group.id in u.groups])

        for provider in self.providers.values():
            provider.user_count = len(
                set(a.user_id for a in self.activities if a.provider_id == provider.id)
            )

        # Print summary
        print(f"   ✓ Users: {len(self.users):,}")
        print(f"   ✓ Companies: {len(self.companies):,}")
        print(f"   ✓ Groups: {len(self.groups):,}")
        print(f"   ✓ Providers: {len(self.providers):,}")
        print(f"   ✓ Resources: {len(self.resources):,}")
        print(f"   ✓ Activities: {len(self.activities):,}")
        print(f"   ✓ Permission Changes: {len(self.permission_changes):,}")

        if self.error_rows:
            print(f"   ⚠ Errors: {len(self.error_rows)} rows")

        return {
            "users": len(self.users),
            "companies": len(self.companies),
            "groups": len(self.groups),
            "providers": len(self.providers),
            "resources": len(self.resources),
            "activities": len(self.activities),
            "permission_changes": len(self.permission_changes),
            "errors": len(self.error_rows),
        }

    def _infer_resource_type(self, path: str) -> str:
        """Infer resource type from path."""
        path_lower = path.lower()

        if any(ext in path_lower for ext in [".pdf", ".doc", ".xls", ".ppt", ".txt"]):
            return "document"
        if any(ext in path_lower for ext in [".jpg", ".png", ".gif", ".svg"]):
            return "image"
        if any(ext in path_lower for ext in [".py", ".js", ".java", ".ts", ".go"]):
            return "code"
        if "/api/" in path_lower or path_lower.startswith("http"):
            return "api"
        if path_lower.endswith("/") or "." not in path_lower.split("/")[-1]:
            return "folder"

        return "file"

    def export_parquet(self, output_dir: str = ".") -> Dict[str, str]:
        """Export entities to Parquet files."""
        output_path = Path(output_dir)
        output_path.mkdir(parents=True, exist_ok=True)

        files = {}

        # Export each entity type
        if self.activities:
            activities_df = pd.DataFrame([asdict(a) for a in self.activities])
            path = output_path / "events_clean.parquet"
            activities_df.to_parquet(path, index=False)
            files["activities"] = str(path)

        if self.users:
            users_df = pd.DataFrame([asdict(u) for u in self.users.values()])
            path = output_path / "users_clean.parquet"
            users_df.to_parquet(path, index=False)
            files["users"] = str(path)

        if self.companies:
            companies_df = pd.DataFrame([asdict(c) for c in self.companies.values()])
            path = output_path / "companies_clean.parquet"
            companies_df.to_parquet(path, index=False)
            files["companies"] = str(path)

        if self.providers:
            providers_df = pd.DataFrame([asdict(p) for p in self.providers.values()])
            path = output_path / "providers_clean.parquet"
            providers_df.to_parquet(path, index=False)
            files["providers"] = str(path)

        print(f"\n✓ Exported {len(files)} Parquet files to {output_dir}")
        return files

    def export_jsonl(self, output_path: str = "events_clean.jsonl") -> str:
        """Export activities to JSONL format."""
        with open(output_path, "w", encoding="utf-8") as f:
            for activity in self.activities:
                f.write(json.dumps(asdict(activity), default=str) + "\n")

        print(f"✓ Exported {len(self.activities):,} activities to {output_path}")
        return output_path

    def get_summary(self) -> Dict[str, Any]:
        """Get ingestion summary."""
        return {
            "raw_rows": self.raw_row_count,
            "processed_rows": self.processed_row_count,
            "error_rows": len(self.error_rows),
            "entities": {
                "users": len(self.users),
                "companies": len(self.companies),
                "groups": len(self.groups),
                "providers": len(self.providers),
                "resources": len(self.resources),
                "activities": len(self.activities),
                "permission_changes": len(self.permission_changes),
            },
            "governance": {
                "passed": self.governance_report.overall_passed if self.governance_report else None,
                "risk_flags": self.governance_report.risk_flags if self.governance_report else [],
                "review_required": self.governance_report.review_required
                if self.governance_report
                else None,
            },
            "pii_stats": self.pii_handler.get_stats(),
        }


# =============================================================================
# MAIN ENTRY POINT
# =============================================================================


def ingest_csv(
    filepath: str, output_dir: str = ".", governance: bool = True, export_format: str = "both"
) -> Dict[str, Any]:
    """
    Main entry point for CSV ingestion.

    Args:
        filepath: Path to input CSV
        output_dir: Directory for output files
        governance: Whether to run governance checks
        export_format: "parquet", "jsonl", or "both"

    Returns:
        Dictionary with ingestion results
    """
    print("=" * 60)
    print("  COSURVIVAL INGESTION PIPELINE")
    print("  Schema-First • Governance-Gated • Privacy-Safe")
    print("=" * 60)

    # Initialize pipeline
    pipeline = IngestionPipeline(governance_enabled=governance)

    # Load data
    df = pipeline.load_csv(filepath)

    # Run governance checks
    if governance:
        gov_report = pipeline.run_governance_check(df)

        if not gov_report.overall_passed:
            print("\n⚠️  GOVERNANCE CHECK FAILED")
            print("   Review and address issues before proceeding.")

            # Export governance report
            report_path = Path(output_dir) / "governance_report.json"
            with open(report_path, "w") as f:
                json.dump(gov_report.to_dict(), f, indent=2)
            print(f"   Report saved to: {report_path}")

            return {
                "success": False,
                "governance_report": gov_report.to_dict(),
                "message": "Governance check failed. Review report and address issues.",
            }

    # Detect schema
    schema_report = pipeline.detect_schema(df)

    # Extract entities
    pipeline.extract_entities(df)

    # Export
    exported_files = {}

    if export_format in ["parquet", "both"]:
        try:
            exported_files.update(pipeline.export_parquet(output_dir))
        except Exception as e:
            print(f"⚠️  Parquet export failed: {e}")

    if export_format in ["jsonl", "both"]:
        jsonl_path = Path(output_dir) / "events_clean.jsonl"
        exported_files["jsonl"] = pipeline.export_jsonl(str(jsonl_path))

    # Export governance report
    if governance and pipeline.governance_report:
        report_path = Path(output_dir) / "governance_report.json"
        with open(report_path, "w") as f:
            json.dump(pipeline.governance_report.to_dict(), f, indent=2)
        exported_files["governance_report"] = str(report_path)

    # Export data dictionary
    if governance and pipeline.governance_gate:
        classifications = pipeline.governance_gate.classify_columns(list(df.columns))
        data_dict = create_data_dictionary(classifications)
        dict_path = Path(output_dir) / "data_dictionary.md"
        with open(dict_path, "w", encoding="utf-8") as f:
            f.write(data_dict)
        exported_files["data_dictionary"] = str(dict_path)

    # Summary
    summary = pipeline.get_summary()
    summary["exported_files"] = exported_files
    summary["schema_report"] = schema_report

    # Export summary
    summary_path = Path(output_dir) / "ingestion_summary.json"
    with open(summary_path, "w") as f:
        json.dump(summary, f, indent=2, default=str)

    print("\n" + "=" * 60)
    print("  INGESTION COMPLETE")
    print("=" * 60)
    print(f"\n  Processed: {summary['processed_rows']:,} / {summary['raw_rows']:,} rows")
    print(f"  Entities extracted: {sum(summary['entities'].values()):,}")
    print(f"  Files exported: {len(exported_files)}")
    print(f"  Governance: {'PASSED' if summary['governance']['passed'] else 'REVIEW REQUIRED'}")

    return {"success": True, "summary": summary}


if __name__ == "__main__":
    import sys

    if len(sys.argv) < 2:
        print("Usage: python ingestion.py <csv_path> [output_dir]")
        print("\nExample: python ingestion.py brian_data.csv ./output")
        sys.exit(1)

    csv_path = sys.argv[1]
    output_dir = sys.argv[2] if len(sys.argv) > 2 else "."

    result = ingest_csv(csv_path, output_dir)

    if result["success"]:
        print("\n✅ Ready for MVP analysis!")
    else:
        print("\n❌ Address governance issues first.")
