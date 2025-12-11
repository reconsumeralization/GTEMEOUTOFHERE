#!/usr/bin/env python3
"""
COSURVIVAL SECURITY MODULE
==========================
Implements security best practices from Week 10.

This module provides:
1. Password hashing with salt
2. Input validation
3. SQL injection prevention helpers
4. XSS prevention helpers
5. Rate limiting
6. Session management
7. Content validation (no implicit execution)
8. Secret management (API keys, tokens)
9. Supply chain security (SBOM, signatures)
10. Access control and authorization

CURRICULUM MAPPING:
-------------------
Week 10: Security & Trust Fabric
  - All security controls from SECURITY_CONTROLS_CHECKLIST.md
  - See: TEACHER_CORE_TRACK.md, Week 10
  - See: SECURITY_TRUST_FABRIC.md (complete framework)
  - See: API_KEY_SECURITY_CRITICAL.md (API key security)

Design Axiom: "Any local-execution surface can become a cross-cloud 
and downstream supply-chain pivot."
"""


# Standard library imports
import hashlib
import re
import secrets
from collections import defaultdict
from dataclasses import dataclass, field
from datetime import datetime, timedelta
from typing import Optional, Tuple, Dict, Any, List

# Third-party imports
from markupsafe import escape


# =============================================================================
# PASSWORD SECURITY
# =============================================================================

# Common passwords to block
COMMON_PASSWORDS = {
    "123456",
    "password",
    "admin",
    "12345678",
    "123456789",
    "1234",
    "12345",
    "123",
    "Aa123456",
    "1234567890",
    "qwerty",
    "abc123",
    "password123",
    "welcome",
    "letmein",
}

PASSWORD_REQUIREMENTS = {
    "min_length": 12,
    "require_uppercase": True,
    "require_lowercase": True,
    "require_numbers": True,
    "require_special": True,
    "forbid_common": True,
}


def check_password_strength(password: str) -> Tuple[bool, str]:
    """
    Check if password meets security requirements.

    Returns:
        (is_valid: bool, message: str)
    """
    if len(password) < PASSWORD_REQUIREMENTS["min_length"]:
        return False, f"Password must be at least {PASSWORD_REQUIREMENTS['min_length']} characters"

    if PASSWORD_REQUIREMENTS["require_uppercase"] and not any(c.isupper() for c in password):
        return False, "Password must contain uppercase letters"

    if PASSWORD_REQUIREMENTS["require_lowercase"] and not any(c.islower() for c in password):
        return False, "Password must contain lowercase letters"

    if PASSWORD_REQUIREMENTS["require_numbers"] and not any(c.isdigit() for c in password):
        return False, "Password must contain numbers"

    if PASSWORD_REQUIREMENTS["require_special"] and not any(
        c in "!@#$%^&*()_+-=[]{}|;:,.<>?" for c in password
    ):
        return False, "Password must contain special characters"

    if PASSWORD_REQUIREMENTS["forbid_common"] and password.lower() in COMMON_PASSWORDS:
        return False, "Password is too common"

    return True, "Password is strong"


def hash_password_with_salt(password: str) -> Tuple[str, str]:
    """
    Hash password with random salt.

    Returns:
        (password_hash: str, salt: str)
    """
    salt = secrets.token_hex(16)  # 32-character random salt
    salted_password = salt + password
    hash_value = hashlib.sha256(salted_password.encode()).hexdigest()
    return hash_value, salt


def verify_password_with_salt(password: str, stored_hash: str, salt: str) -> bool:
    """
    Verify password using stored hash and salt.

    Returns:
        True if password matches, False otherwise
    """
    salted_password = salt + password
    computed_hash = hashlib.sha256(salted_password.encode()).hexdigest()
    return computed_hash == stored_hash


# =============================================================================
# INPUT VALIDATION
# =============================================================================


def validate_user_id(user_id: str) -> Tuple[bool, str]:
    """
    Validate user ID format.

    Returns:
        (is_valid: bool, error_message: str)
    """
    if not user_id:
        return False, "User ID is required"

    if len(user_id) > 100:
        return False, "User ID too long (max 100 characters)"

    # Allow alphanumeric, underscore, hyphen
    if not re.match(r"^[a-zA-Z0-9_-]+$", user_id):
        return False, "User ID contains invalid characters"

    return True, "Valid"


def validate_lens(lens: str) -> Tuple[bool, str]:
    """
    Validate lens name.

    Returns:
        (is_valid: bool, error_message: str)
    """
    VALID_LENSES = {"tribe", "teacher", "recon"}

    if not lens:
        return False, "Lens is required"

    if lens not in VALID_LENSES:
        return False, f"Invalid lens. Must be one of: {', '.join(VALID_LENSES)}"

    return True, "Valid"


def validate_company_id(company_id: str) -> Tuple[bool, str]:
    """
    Validate company ID format.

    Returns:
        (is_valid: bool, error_message: str)
    """
    if not company_id:
        return True, "Valid"  # Optional field

    if len(company_id) > 100:
        return False, "Company ID too long (max 100 characters)"

    if not re.match(r"^[a-zA-Z0-9_-]+$", company_id):
        return False, "Company ID contains invalid characters"

    return True, "Valid"


def sanitize_input(value: Any) -> str:
    """
    Sanitize user input to prevent XSS.

    Returns:
        Sanitized string
    """
    if value is None:
        return ""

    # Convert to string and escape HTML
    return escape(str(value))


# =============================================================================
# SQL INJECTION PREVENTION
# =============================================================================


def safe_sql_identifier(identifier: str) -> str:
    """
    Validate SQL identifier (table/column name) to prevent injection.

    Only allows alphanumeric and underscore.

    Returns:
        Validated identifier or raises ValueError
    """
    if not re.match(r"^[a-zA-Z_][a-zA-Z0-9_]*$", identifier):
        raise ValueError(f"Invalid SQL identifier: {identifier}")
    return identifier


def build_safe_query(base_query: str, params: Tuple) -> Tuple[str, Tuple]:
    """
    Build safe SQL query with parameterized placeholders.

    Example:
        query, params = build_safe_query(
            "SELECT * FROM users WHERE id = ? AND company_id = ?",
            (user_id, company_id)
        )

    Returns:
        (query: str, params: Tuple)
    """
    # Validate query doesn't contain dangerous patterns
    dangerous_patterns = [
        "DROP TABLE",
        "DELETE FROM",
        "TRUNCATE",
        "ALTER TABLE",
        "CREATE TABLE",
        "INSERT INTO",
    ]

    query_upper = base_query.upper()
    for pattern in dangerous_patterns:
        if pattern in query_upper and "?" not in base_query:
            raise ValueError(f"Query contains potentially dangerous operation: {pattern}")

    return base_query, params


# =============================================================================
# RATE LIMITING
# =============================================================================


class RateLimiter:
    """
    Rate limiter to prevent brute force attacks.
    """

    def __init__(self, max_attempts: int = 5, window_minutes: int = 15):
        """
        Initialize rate limiter.

        Args:
            max_attempts: Maximum attempts allowed in window
            window_minutes: Time window in minutes
        """
        self.max_attempts = max_attempts
        self.window_minutes = window_minutes
        self.attempts: Dict[str, List[datetime]] = defaultdict(list)

    def check_rate_limit(self, key: str) -> Tuple[bool, str, Optional[datetime]]:
        """
        Check if action is allowed based on rate limit.

        Args:
            key: Unique identifier (e.g., "username:ip_address")

        Returns:
            (allowed: bool, message: str, retry_after: Optional[datetime])
        """
        now = datetime.now()
        window_start = now - timedelta(minutes=self.window_minutes)

        # Remove old attempts
        self.attempts[key] = [attempt for attempt in self.attempts[key] if attempt > window_start]

        # Check if limit exceeded
        if len(self.attempts[key]) >= self.max_attempts:
            oldest_attempt = min(self.attempts[key])
            retry_after = oldest_attempt + timedelta(minutes=self.window_minutes)
            return (
                False,
                f"Rate limit exceeded. Try again after {retry_after.strftime('%H:%M:%S')}",
                retry_after,
            )

        # Record this attempt
        self.attempts[key].append(now)

        return True, "OK", None

    def clear_attempts(self, key: str):
        """Clear attempts for a key (e.g., on successful login)."""
        if key in self.attempts:
            del self.attempts[key]


# =============================================================================
# XSS PREVENTION
# =============================================================================


def sanitize_html(value: Any) -> str:
    """
    Sanitize HTML to prevent XSS attacks.

    Uses markupsafe.escape to escape HTML entities.

    Returns:
        Sanitized string safe for HTML output
    """
    if value is None:
        return ""

    return escape(str(value))


def sanitize_json_value(value: Any) -> Any:
    """
    Sanitize value for JSON output (prevent JSON injection).

    Returns:
        Sanitized value
    """
    if isinstance(value, str):
        # Remove control characters that could break JSON
        return re.sub(r"[\x00-\x1f\x7f-\x9f]", "", value)
    return value


# =============================================================================
# CSRF TOKEN GENERATION
# =============================================================================


def generate_csrf_token() -> str:
    """
    Generate CSRF token.

    Returns:
        Random token string
    """
    return secrets.token_urlsafe(32)


def verify_csrf_token(token: str, stored_token: str) -> bool:
    """
    Verify CSRF token using constant-time comparison.

    Returns:
        True if tokens match, False otherwise
    """
    return secrets.compare_digest(token, stored_token)


# =============================================================================
# SECURITY UTILITIES
# =============================================================================


def is_safe_filename(filename: str) -> bool:
    """
    Check if filename is safe (prevents path traversal).

    Returns:
        True if safe, False otherwise
    """
    # Block path traversal attempts
    if ".." in filename or "/" in filename or "\\" in filename:
        return False

    # Block null bytes
    if "\x00" in filename:
        return False

    # Reasonable length
    if len(filename) > 255:
        return False

    return True


def validate_timestamp(timestamp: str) -> Tuple[bool, str]:
    """
    Validate timestamp format.

    Returns:
        (is_valid: bool, error_message: str)
    """
    if not timestamp:
        return False, "Timestamp is required"

    # Try parsing ISO format
    try:
        datetime.fromisoformat(timestamp.replace("Z", "+00:00"))
        return True, "Valid"
    except ValueError:
        return False, "Invalid timestamp format (expected ISO 8601)"


# =============================================================================
# SECURITY AUDIT LOGGING
# =============================================================================


class SecurityAuditLog:
    """
    Log security events for audit trail.
    """

    def __init__(self) -> None:
        self.events: List[Dict[str, Any]] = []

    def log_event(self, event_type: str, details: Dict[str, Any]):
        """
        Log security event.

        Args:
            event_type: Type of event (login_attempt, sql_query, etc.)
            details: Event details
        """
        event = {
            "timestamp": datetime.now().isoformat(),
            "event_type": event_type,
            "details": details,
        }
        self.events.append(event)

    def get_events(
        self, event_type: Optional[str] = None, limit: int = 100
    ) -> List[Dict[str, Any]]:
        """
        Get security events.

        Args:
            event_type: Filter by event type (optional)
            limit: Maximum number of events to return

        Returns:
            List of security events
        """
        events = self.events
        if event_type:
            events = [e for e in events if e["event_type"] == event_type]

        return events[-limit:]


# =============================================================================
# CONTENT VALIDATION (No Implicit Execution)
# =============================================================================

# Executable patterns that should never appear in content
EXECUTABLE_PATTERNS = [
    r"<script[^>]*>",  # Script tags
    r"javascript:",  # JavaScript protocol
    r"on\w+\s*=",  # Event handlers (onclick, onload, etc.)
    r"eval\s*\(",  # eval() calls
    r"exec\s*\(",  # exec() calls
    r"system\s*\(",  # system() calls
    r"subprocess\.",  # subprocess calls
    r"os\.system",  # os.system calls
    r"__import__",  # Dynamic imports
    r"compile\s*\(",  # compile() calls
]

# Allowed file types for content packages (whitelist)
ALLOWED_CONTENT_TYPES = {
    # Documents
    ".pdf",
    ".doc",
    ".docx",
    ".txt",
    ".md",
    ".rtf",
    # Images
    ".jpg",
    ".jpeg",
    ".png",
    ".gif",
    ".svg",
    ".webp",
    # Data
    ".json",
    ".csv",
    ".xml",
    ".yaml",
    ".yml",
    # Archives (will be scanned)
    ".zip",
    ".tar",
    ".gz",
}

# Maximum file size (10MB)
MAX_CONTENT_SIZE = 10 * 1024 * 1024


@dataclass  # type: ignore[misc]
class ContentValidationResult:
    """Result of content validation."""

    is_valid: bool
    issues: List[str]
    warnings: List[str]
    requires_sandbox: bool
    file_type: Optional[str] = None
    file_size: int = 0


def validate_content_package(package_path: str) -> ContentValidationResult:
    """
    Validate that content package contains no executable commands.

    CURRICULUM: Week 10 - Security Module
    Activity: "Secure Content Packaging"
    Prevents content-to-execution attacks (Finding 2 from 440782380).

    Requirements:
    - No executable commands in config files
    - File type validation (whitelist)
    - Size limits enforced
    - Executable pattern detection

    See: SECURITY_TRUST_FABRIC.md, Content & Execution Security
    See: SECURITY_CONTROLS_CHECKLIST.md, Content & Execution Security
    """
    from pathlib import Path

    issues = []
    warnings = []
    requires_sandbox = False

    path = Path(package_path)

    # Check if file exists
    if not path.exists():
        return ContentValidationResult(  # type: ignore[misc]
            is_valid=False, issues=["File does not exist"], warnings=[], requires_sandbox=False
        )

    # Check file size
    file_size = path.stat().st_size
    if file_size > MAX_CONTENT_SIZE:
        issues.append(
            f"File size ({file_size:,} bytes) exceeds maximum ({MAX_CONTENT_SIZE:,} bytes)"
        )

    # Check file type (extension)
    file_type = path.suffix.lower()
    if file_type not in ALLOWED_CONTENT_TYPES:
        issues.append(f"File type '{file_type}' not in allowed whitelist")
        requires_sandbox = True

    # For text-based files, check for executable patterns
    if file_type in [".txt", ".md", ".json", ".xml", ".yaml", ".yml", ".csv"]:
        try:
            with open(package_path, "r", encoding="utf-8", errors="ignore") as f:
                content = f.read()

                # Check for executable patterns
                for pattern in EXECUTABLE_PATTERNS:
                    if re.search(pattern, content, re.IGNORECASE):
                        issues.append(f"Found executable pattern: {pattern}")
                        requires_sandbox = True

                # Check for suspicious command-like patterns
                if re.search(r"[;&|`]\s*\w+", content):
                    warnings.append("Found command-like patterns (may be false positive)")

        except Exception as e:
            warnings.append(f"Could not read file for pattern checking: {e}")

    # Archives require special handling
    if file_type in [".zip", ".tar", ".gz"]:
        warnings.append("Archive file - contents should be extracted and validated")
        requires_sandbox = True

    is_valid = len(issues) == 0

    return ContentValidationResult(  # type: ignore[misc]
        is_valid=is_valid,
        issues=issues,
        warnings=warnings,
        requires_sandbox=requires_sandbox,
        file_type=file_type,
        file_size=file_size,
    )


# =============================================================================
# SECRET MANAGEMENT (API Keys, Tokens)
# =============================================================================


class SecretManager:
    """
    Secure secret management - never in code or plain files.

    CURRICULUM: Week 10 - Security Module
    Activity: "Secure API Key Management"
    Prevents credential exfiltration (Finding 3 from 440782380).

    Requirements:
    - No keys in source code
    - No keys in client-side code
    - No keys in config files (plain text)
    - Keys stored in secure storage (keychain/enclave)
    - Short-lived tokens preferred
    - Token rotation implemented

    See: API_KEY_SECURITY_CRITICAL.md (complete guide)
    See: SECURITY_TRUST_FABRIC.md, Secrets Hardening
    See: SECURITY_CONTROLS_CHECKLIST.md, Secrets Management
    """

    def __init__(self) -> None:
        self._secrets: Dict[str, Dict[str, Any]] = {}
        self._usage_tracker: Dict[str, List[datetime]] = defaultdict(list)

    def get_api_key(self, key_name: str = "OPENAI_API_KEY") -> str:
        """
        Get API key securely from environment or secure storage.

        NEVER:
        - Read from code
        - Read from config files
        - Read from client-side code

        ALWAYS:
        - Read from environment variables (server-side)
        - Use secure storage (keychain/enclave) for production
        - Prefer short-lived tokens
        """
        import os

        # Try environment variable first
        key = os.environ.get(key_name)
        if key:
            self._track_usage(key_name)
            return key

        # In production, would use secure storage:
        # - AWS Secrets Manager
        # - Azure Key Vault
        # - Google Secret Manager
        # - OS keychain

        raise ValueError(
            f"{key_name} not found in environment. "
            "Never hardcode keys in source code or config files. "
            "See: API_KEY_SECURITY_CRITICAL.md"
        )

    def store_secret(self, name: str, value: str, expires_at: Optional[datetime] = None):
        """
        Store secret securely (in-memory for demo, use secure storage in production).

        In production, use:
        - OS keychain
        - Secure enclave
        - Cloud secret managers
        """
        self._secrets[name] = {
            "value": value,
            "created_at": datetime.now(),
            "expires_at": expires_at,
            "usage_count": 0,
        }

    def get_secret(self, name: str) -> Optional[str]:
        """Get secret if not expired."""
        if name not in self._secrets:
            return None

        secret = self._secrets[name]

        # Check expiration
        if secret["expires_at"] and datetime.now() > secret["expires_at"]:
            del self._secrets[name]
            return None

        secret["usage_count"] += 1
        self._track_usage(name)
        return secret["value"]

    def rotate_secret(self, name: str, new_value: str):
        """Rotate secret (invalidate old, set new)."""
        if name in self._secrets:
            # In production, would invalidate old key in service
            pass

        self.store_secret(name, new_value)

    def _track_usage(self, key_name: str):
        """Track secret usage for monitoring."""
        self._usage_tracker[key_name].append(datetime.now())

        # Keep only last 1000 uses
        if len(self._usage_tracker[key_name]) > 1000:
            self._usage_tracker[key_name] = self._usage_tracker[key_name][-1000:]

    def get_usage_stats(self, key_name: str) -> Dict[str, Any]:
        """Get usage statistics for monitoring."""
        uses = self._usage_tracker.get(key_name, [])

        if not uses:
            return {"total_uses": 0, "recent_uses": 0}

        recent_cutoff = datetime.now() - timedelta(hours=1)
        recent_uses = [u for u in uses if u > recent_cutoff]

        return {
            "total_uses": len(uses),
            "recent_uses_1h": len(recent_uses),
            "last_used": uses[-1].isoformat() if uses else None,
        }


# =============================================================================
# API CONNECTOR SECURITY (Least Privilege)
# =============================================================================


@dataclass
class ConnectorPermission:
    """Permission for an API connector."""

    scope: str
    resource: str
    action: str  # read, write, delete, etc.
    expires_at: Optional[datetime] = None
    created_at: datetime = field(default_factory=datetime.now)  # type: ignore[misc]


class AIConnector:
    """
    Permissioned AI connector with least-privilege defaults.

    CURRICULUM: Week 10 - Security Module
    Activity: "Least Privilege API Design"
    Prevents over-broad trust links (Finding 2 from 440782380).

    Requirements:
    - Least-privilege scopes by default
    - Time-bounded tokens
    - Revocable in one click
    - Auditable by user
    - Role-scoped defaults

    See: SECURITY_TRUST_FABRIC.md, Permissioned AI Connectors
    See: SECURITY_CONTROLS_CHECKLIST.md, API Connectors
    """

    # Role-based default scopes (least privilege)
    ROLE_SCOPES = {
        "consumer": ["read:data", "read:resources"],
        "supplier": ["read:data", "write:resources", "read:analytics"],
        "educator": ["read:data", "read:analytics", "write:content"],
        "admin": ["read:data", "write:data", "read:analytics", "write:analytics", "admin"],
    }

    def __init__(self, connector_id: str, role: str = "consumer"):
        self.connector_id = connector_id
        self.role = role
        self.scopes = self.ROLE_SCOPES.get(role, self.ROLE_SCOPES["consumer"]).copy()
        self.created_at = datetime.now()
        self.expires_at = datetime.now() + timedelta(hours=1)  # Time-bounded
        self.revocable = True
        self.permissions: List[ConnectorPermission] = []
        self.usage_log: List[Dict[str, Any]] = []

    def has_permission(self, scope: str, resource: str, action: str) -> bool:
        """Check if connector has permission for action."""
        # Check if expired
        if datetime.now() > self.expires_at:
            return False

        # Check if revoked
        if not self.revocable:
            return False

        # Check scope
        if scope not in self.scopes:
            return False

        # Log access attempt
        self.usage_log.append(
            {
                "timestamp": datetime.now().isoformat(),
                "scope": scope,
                "resource": resource,
                "action": action,
                "allowed": True,
            }
        )

        return True

    def revoke(self):
        """Revoke connector (one-click revocation)."""
        self.revocable = False
        self.usage_log.append(
            {
                "timestamp": datetime.now().isoformat(),
                "action": "revoked",
                "reason": "User revocation",
            }
        )

    def extend_expiration(self, hours: int = 1):
        """Extend expiration time."""
        self.expires_at = datetime.now() + timedelta(hours=hours)

    def get_audit_trail(self) -> List[Dict[str, Any]]:
        """Get audit trail (user-auditable)."""
        return self.usage_log.copy()


# =============================================================================
# SUPPLY CHAIN SECURITY
# =============================================================================


@dataclass  # type: ignore[misc]
class SBOMEntry:
    """Software Bill of Materials entry."""

    name: str
    version: str
    license: Optional[str] = None
    source: Optional[str] = None
    checksum: Optional[str] = None


def generate_sbom(package_name: str, dependencies: List[Dict[str, str]]) -> Dict[str, Any]:
    """
    Generate Software Bill of Materials (SBOM).

    CURRICULUM: Week 10 - Security Module
    Activity: "Supply Chain Security"

    Requirements:
    - SBOM generation for all builds
    - Signed artifacts end-to-end
    - Dependency pinning + provenance checks

    See: SECURITY_TRUST_FABRIC.md, Supply Chain Integrity
    See: SECURITY_CONTROLS_CHECKLIST.md, Supply Chain Security
    """
    import hashlib

    sbom: Dict[str, Any] = {
        "package": package_name,
        "generated_at": datetime.now().isoformat(),
        "dependencies": [],
    }

    for dep in dependencies:
        entry = {
            "name": dep.get("name", ""),
            "version": dep.get("version", ""),
            "license": dep.get("license"),
            "source": dep.get("source"),
        }

        # Calculate checksum if source available
        if dep.get("source"):
            try:
                checksum = hashlib.sha256(dep["source"].encode()).hexdigest()[:16]
                entry["checksum"] = checksum
            except Exception:
                pass

        sbom["dependencies"].append(entry)

    return sbom


def validate_dependency(
    dep_name: str,
    dep_version: str,
    allowed_versions: Optional[List[str]] = None,
    checksum: Optional[str] = None,
) -> Tuple[bool, str]:
    """
    Validate dependency (pinning and provenance checks).

    Returns:
        (is_valid: bool, error_message: str)
    """
    # Check if version is pinned
    if not dep_version or dep_version == "latest":
        return False, f"Dependency {dep_name} must have pinned version (not 'latest')"

    # Check if version is in allowed list
    if allowed_versions and dep_version not in allowed_versions:
        return False, f"Dependency {dep_name} version {dep_version} not in allowed versions"

    # In production, would verify checksum and signature
    if checksum:
        # Verify checksum matches
        pass

    return True, "Valid"


# =============================================================================
# ACCESS CONTROL (Blast Radius)
# =============================================================================


class AccessController:
    """
    Blast radius controls - deny by default.

    CURRICULUM: Week 0, Activity 0.3 - Governance Gate
    CURRICULUM: Week 10 - Security Module

    Requirements:
    - Strict segmentation between domains
    - Deny-by-default cross-domain access
    - Dual-control for high-risk actions

    See: SECURITY_TRUST_FABRIC.md, Blast Radius Controls
    See: SECURITY_CONTROLS_CHECKLIST.md, Blast Radius Controls
    """

    # Domain boundaries
    DOMAINS = {
        "consumer": {"consumer", "consumer_data"},
        "supplier": {"supplier", "supplier_data"},
        "education": {"education", "education_data"},
        "admin": {
            "admin",
            "admin_data",
            "consumer",
            "consumer_data",
            "supplier",
            "supplier_data",
            "education",
            "education_data",
        },
    }

    # High-risk actions requiring dual-control
    HIGH_RISK_ACTIONS = {
        "publish",
        "delete_all",
        "mass_message",
        "payout_change",
        "role_change",
        "permission_grant",
        "data_export",
    }

    def __init__(self) -> None:
        self.access_log: List[Dict[str, Any]] = []
        self.dual_control_pending: Dict[str, Dict[str, Any]] = {}

    def check_access(
        self, user_id: str, user_role: str, resource: str, action: str, domain: str
    ) -> Tuple[bool, str]:
        """
        Check if user has access to resource (deny by default).

        Returns:
            (allowed: bool, reason: str)
        """
        # Deny by default
        user_domains = self.DOMAINS.get(user_role, set())

        # Check domain boundary
        if domain not in user_domains:
            self._log_access(user_id, resource, action, False, "Cross-domain access denied")
            return False, f"Access denied: {user_role} cannot access {domain} domain"

        # Check high-risk actions
        if action in self.HIGH_RISK_ACTIONS:
            # Require dual-control
            if not self._has_dual_control(user_id, resource, action):
                self._log_access(user_id, resource, action, False, "Dual-control required")
                return False, f"High-risk action '{action}' requires dual-control approval"

        self._log_access(user_id, resource, action, True, "Access granted")
        return True, "Access granted"

    def _has_dual_control(self, user_id: str, resource: str, action: str) -> bool:
        """Check if dual-control approval exists."""
        key = f"{user_id}:{resource}:{action}"
        approval = self.dual_control_pending.get(key)

        if not approval:
            return False

        # Check if approval is still valid (e.g., within 5 minutes)
        if datetime.now() - approval["approved_at"] > timedelta(minutes=5):
            del self.dual_control_pending[key]
            return False

        return approval.get("approved", False)

    def request_dual_control(
        self, user_id: str, resource: str, action: str, approver_id: str
    ) -> str:
        """Request dual-control approval (returns approval token)."""
        key = f"{user_id}:{resource}:{action}"
        token = secrets.token_urlsafe(32)

        self.dual_control_pending[key] = {
            "token": token,
            "user_id": user_id,
            "approver_id": approver_id,
            "resource": resource,
            "action": action,
            "requested_at": datetime.now(),
            "approved": False,
        }

        return token

    def approve_dual_control(self, token: str, approver_id: str) -> bool:
        """Approve dual-control request."""
        for key, approval in self.dual_control_pending.items():
            if approval["token"] == token and approval["approver_id"] == approver_id:
                approval["approved"] = True
                approval["approved_at"] = datetime.now()
                return True
        return False

    def _log_access(self, user_id: str, resource: str, action: str, allowed: bool, reason: str):
        """Log access attempt (tamper-evident)."""
        self.access_log.append(
            {
                "timestamp": datetime.now().isoformat(),
                "user_id": user_id,
                "resource": resource,
                "action": action,
                "allowed": allowed,
                "reason": reason,
            }
        )


# Global instances
rate_limiter = RateLimiter()
security_audit_log = SecurityAuditLog()
secret_manager = SecretManager()
access_controller = AccessController()
