#!/usr/bin/env python3
"""
Unit tests for security.py module.

CURRICULUM: Week 10 - Security Module
Testing all security controls from SECURITY_CONTROLS_CHECKLIST.md
"""

import os
import tempfile
from pathlib import Path
from datetime import datetime, timedelta
import pytest

from security import (
    validate_content_package,
    ContentValidationResult,
    SecretManager,
    AIConnector,
    AccessController,
    generate_sbom,
    validate_dependency,
    secret_manager,
    access_controller,
)


class TestContentValidation:
    """Test content validation (no implicit execution)."""

    def test_valid_text_file(self):
        """Test validation of safe text file."""
        with tempfile.NamedTemporaryFile(mode="w", suffix=".txt", delete=False) as f:
            f.write("This is safe content.\nNo executable code here.")
            temp_path = f.name

        try:
            result = validate_content_package(temp_path)
            assert result.is_valid is True
            assert len(result.issues) == 0
            assert result.file_type == ".txt"
        finally:
            os.unlink(temp_path)

    def test_file_with_executable_pattern(self):
        """Test detection of executable patterns."""
        with tempfile.NamedTemporaryFile(mode="w", suffix=".txt", delete=False) as f:
            f.write("Normal content\n<script>alert('xss')</script>\nMore content")
            temp_path = f.name

        try:
            result = validate_content_package(temp_path)
            assert result.is_valid is False
            assert len(result.issues) > 0
            assert any("executable pattern" in issue.lower() for issue in result.issues)
            assert result.requires_sandbox is True
        finally:
            os.unlink(temp_path)

    def test_file_size_limit(self):
        """Test file size limit enforcement."""
        # Create a file larger than MAX_CONTENT_SIZE (10MB)
        with tempfile.NamedTemporaryFile(mode="wb", suffix=".txt", delete=False) as f:
            # Write 11MB of data
            f.write(b"x" * (11 * 1024 * 1024))
            temp_path = f.name

        try:
            result = validate_content_package(temp_path)
            assert result.is_valid is False
            assert any("size" in issue.lower() for issue in result.issues)
        finally:
            os.unlink(temp_path)

    def test_disallowed_file_type(self):
        """Test file type whitelist enforcement."""
        with tempfile.NamedTemporaryFile(mode="w", suffix=".exe", delete=False) as f:
            f.write("This looks like an executable")
            temp_path = f.name

        try:
            result = validate_content_package(temp_path)
            assert result.is_valid is False
            assert any("not in allowed whitelist" in issue for issue in result.issues)
            assert result.requires_sandbox is True
        finally:
            os.unlink(temp_path)

    def test_nonexistent_file(self):
        """Test handling of nonexistent file."""
        result = validate_content_package("/nonexistent/file.txt")
        assert result.is_valid is False
        assert len(result.issues) > 0


class TestSecretManager:
    """Test secret management."""

    def test_get_api_key_from_env(self, monkeypatch):
        """Test getting API key from environment variable."""
        monkeypatch.setenv("OPENAI_API_KEY", "test-key-12345")

        key = secret_manager.get_api_key("OPENAI_API_KEY")
        assert key == "test-key-12345"

    def test_get_api_key_missing(self):
        """Test error when API key not in environment."""
        # Temporarily remove if it exists
        original = os.environ.pop("OPENAI_API_KEY", None)
        try:
            with pytest.raises(ValueError) as exc_info:
                secret_manager.get_api_key("OPENAI_API_KEY")
            assert "not found in environment" in str(exc_info.value)
        finally:
            if original:
                os.environ["OPENAI_API_KEY"] = original

    def test_store_and_get_secret(self):
        """Test storing and retrieving secrets."""
        manager = SecretManager()

        manager.store_secret("test_secret", "secret_value_123")
        retrieved = manager.get_secret("test_secret")

        assert retrieved == "secret_value_123"

    def test_secret_expiration(self):
        """Test secret expiration."""
        manager = SecretManager()

        # Store secret that expires in 1 second
        expires_at = datetime.now() + timedelta(seconds=1)
        manager.store_secret("expiring_secret", "value", expires_at=expires_at)

        # Should be available immediately
        assert manager.get_secret("expiring_secret") == "value"

        # Wait for expiration
        import time

        time.sleep(2)

        # Should be None after expiration
        assert manager.get_secret("expiring_secret") is None

    def test_usage_tracking(self, monkeypatch):
        """Test usage tracking."""
        monkeypatch.setenv("TEST_KEY", "test-value")

        manager = SecretManager()
        manager.get_api_key("TEST_KEY")
        manager.get_api_key("TEST_KEY")

        stats = manager.get_usage_stats("TEST_KEY")
        assert stats["total_uses"] >= 2


class TestAIConnector:
    """Test API connector security (least privilege)."""

    def test_consumer_role_scopes(self):
        """Test consumer role has minimal scopes."""
        connector = AIConnector("conn_1", role="consumer")

        assert "read:data" in connector.scopes
        assert "read:resources" in connector.scopes
        assert "write:data" not in connector.scopes
        assert "admin" not in connector.scopes

    def test_admin_role_scopes(self):
        """Test admin role has broader scopes."""
        connector = AIConnector("conn_2", role="admin")

        assert "read:data" in connector.scopes
        assert "write:data" in connector.scopes
        assert "admin" in connector.scopes

    def test_time_bounded_tokens(self):
        """Test token expiration."""
        connector = AIConnector("conn_3", role="consumer")

        # Should be valid initially
        assert datetime.now() < connector.expires_at

        # Should expire after 1 hour
        assert (connector.expires_at - datetime.now()).total_seconds() <= 3600

    def test_permission_check(self):
        """Test permission checking."""
        connector = AIConnector("conn_4", role="consumer")

        # Has permission for read
        assert connector.has_permission("read:data", "resource_1", "read") is True

        # No permission for write
        assert connector.has_permission("write:data", "resource_1", "write") is False

    def test_revocation(self):
        """Test one-click revocation."""
        connector = AIConnector("conn_5", role="consumer")

        # Should work initially
        assert connector.has_permission("read:data", "resource_1", "read") is True

        # Revoke
        connector.revoke()

        # Should not work after revocation
        assert connector.has_permission("read:data", "resource_1", "read") is False

    def test_audit_trail(self):
        """Test audit trail generation."""
        connector = AIConnector("conn_6", role="consumer")

        connector.has_permission("read:data", "resource_1", "read")
        connector.has_permission("read:resources", "resource_2", "read")

        audit = connector.get_audit_trail()
        assert len(audit) >= 2
        assert audit[0]["scope"] == "read:data"
        assert audit[0]["resource"] == "resource_1"


class TestAccessController:
    """Test access control (blast radius)."""

    def test_deny_by_default(self):
        """Test deny-by-default policy."""
        # Consumer trying to access supplier domain
        allowed, reason = access_controller.check_access(
            user_id="user_1",
            user_role="consumer",
            resource="supplier_data",
            action="read",
            domain="supplier",
        )

        assert allowed is False
        assert "denied" in reason.lower()

    def test_domain_boundary(self):
        """Test domain boundary enforcement."""
        # Consumer accessing consumer domain (should work)
        allowed, reason = access_controller.check_access(
            user_id="user_2",
            user_role="consumer",
            resource="consumer_data",
            action="read",
            domain="consumer",
        )

        assert allowed is True

    def test_high_risk_action_dual_control(self):
        """Test dual-control requirement for high-risk actions."""
        # High-risk action requires dual-control
        allowed, reason = access_controller.check_access(
            user_id="user_3",
            user_role="admin",
            resource="all_data",
            action="delete_all",
            domain="admin",
        )

        assert allowed is False
        assert "dual-control" in reason.lower()

    def test_dual_control_workflow(self):
        """Test dual-control approval workflow."""
        # Request dual-control
        token = access_controller.request_dual_control(
            user_id="user_4", resource="all_data", action="delete_all", approver_id="admin_1"
        )

        assert token is not None

        # Approve
        approved = access_controller.approve_dual_control(token, "admin_1")
        assert approved is True

        # Now should have access (within 5 minutes)
        allowed, reason = access_controller.check_access(
            user_id="user_4",
            user_role="admin",
            resource="all_data",
            action="delete_all",
            domain="admin",
        )

        assert allowed is True


class TestSupplyChainSecurity:
    """Test supply chain security."""

    def test_generate_sbom(self):
        """Test SBOM generation."""
        dependencies = [
            {"name": "pandas", "version": "2.0.0", "license": "BSD-3", "source": "pypi"},
            {"name": "numpy", "version": "1.24.0", "license": "BSD", "source": "pypi"},
        ]

        sbom = generate_sbom("cosurvival", dependencies)

        assert sbom["package"] == "cosurvival"
        assert len(sbom["dependencies"]) == 2
        assert sbom["dependencies"][0]["name"] == "pandas"
        assert "checksum" in sbom["dependencies"][0]

    def test_validate_dependency_pinned(self):
        """Test dependency validation with pinned version."""
        is_valid, message = validate_dependency(
            "pandas", "2.0.0", allowed_versions=["2.0.0", "2.0.1"]
        )

        assert is_valid is True
        assert message == "Valid"

    def test_validate_dependency_unpinned(self):
        """Test dependency validation rejects unpinned versions."""
        is_valid, message = validate_dependency("pandas", "latest")

        assert is_valid is False
        assert "pinned" in message.lower()

    def test_validate_dependency_not_allowed(self):
        """Test dependency validation rejects non-allowed versions."""
        is_valid, message = validate_dependency(
            "pandas", "1.0.0", allowed_versions=["2.0.0", "2.0.1"]
        )

        assert is_valid is False
        assert "not in allowed" in message.lower()


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
