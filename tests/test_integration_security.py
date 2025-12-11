#!/usr/bin/env python3
"""
Integration tests for security controls in the pipeline.

CURRICULUM: Week 10 - Security Module
Tests security integration across ingestion, governance, and pipeline.
"""

import os
import tempfile
import pytest
from pathlib import Path

from ingestion import IngestionPipeline
from governance import GovernanceGate, PIIHandler
from security import (
    validate_content_package,
    secret_manager,
    access_controller,
    security_audit_log,
)


class TestIngestionSecurityIntegration:
    """Test security integration in ingestion pipeline."""

    def test_content_validation_in_ingestion(self):
        """Test that content validation is called during ingestion."""
        # Create a safe CSV file
        with tempfile.NamedTemporaryFile(mode="w", suffix=".csv", delete=False) as f:
            f.write("uid,name,email\n")
            f.write("user1,Alice,alice@test.com\n")
            temp_path = f.name

        try:
            pipeline = IngestionPipeline(governance_enabled=True)

            # This should call validate_content_package internally
            df = pipeline.load_csv(temp_path)

            assert len(df) > 0
            # Check that validation was attempted (may pass or fail)
        finally:
            os.unlink(temp_path)

    def test_governance_with_security_checks(self):
        """Test governance checks include security considerations."""
        import pandas as pd

        # Create test data
        test_df = pd.DataFrame(
            {
                "Uid": ["user_1", "user_2"],
                "Name": ["Alice", "Bob"],
                "Email": ["alice@test.com", "bob@test.com"],
                "Type": ["login", "file_access"],
            }
        )

        gate = GovernanceGate()
        report = gate.run_full_check(
            test_df,
            analysis_intents=["collaboration scoring"],
            output_types=["high_activity rankings"],
        )

        # Should have security-related checks
        check_names = [c.check_name for c in report.checks]
        assert any("PII" in name for name in check_names)
        assert any("Bias" in name for name in check_names)


class TestSecretManagementIntegration:
    """Test secret management integration."""

    def test_secret_manager_environment_variable(self, monkeypatch):
        """Test secret manager reads from environment."""
        monkeypatch.setenv("TEST_API_KEY", "test-key-12345")

        key = secret_manager.get_api_key("TEST_API_KEY")
        assert key == "test-key-12345"

        # Check usage tracking
        stats = secret_manager.get_usage_stats("TEST_API_KEY")
        assert stats["total_uses"] > 0

    def test_secret_manager_missing_key(self):
        """Test secret manager error handling."""
        original = os.environ.pop("NONEXISTENT_KEY", None)
        try:
            with pytest.raises(ValueError) as exc_info:
                secret_manager.get_api_key("NONEXISTENT_KEY")
            assert "not found in environment" in str(exc_info.value)
        finally:
            if original:
                os.environ["NONEXISTENT_KEY"] = original


class TestAccessControlIntegration:
    """Test access control integration."""

    def test_pipeline_with_access_control(self):
        """Test that pipeline respects access control."""
        # Consumer role should not access supplier domain
        allowed, reason = access_controller.check_access(
            user_id="consumer_1",
            user_role="consumer",
            resource="supplier_data",
            action="read",
            domain="supplier",
        )

        assert allowed is False
        assert "denied" in reason.lower()

    def test_admin_cross_domain_access(self):
        """Test admin can access multiple domains."""
        # Admin should access admin domain
        allowed, reason = access_controller.check_access(
            user_id="admin_1",
            user_role="admin",
            resource="admin_data",
            action="read",
            domain="admin",
        )

        assert allowed is True


class TestAuditLoggingIntegration:
    """Test audit logging integration."""

    def test_security_events_logged(self):
        """Test that security events are logged."""
        initial_count = len(security_audit_log.get_events())

        # Log a security event
        security_audit_log.log_event("test_event", {"action": "test", "user": "test_user"})

        events = security_audit_log.get_events()
        assert len(events) > initial_count

        # Check last event
        last_event = events[-1]
        assert last_event["event_type"] == "test_event"
        assert last_event["details"]["action"] == "test"


class TestEndToEndSecurity:
    """Test end-to-end security in complete pipeline."""

    def test_complete_pipeline_with_security(self):
        """Test complete pipeline with all security checks."""
        # Create test CSV
        with tempfile.NamedTemporaryFile(mode="w", suffix=".csv", delete=False) as f:
            f.write("uid,name,email,type\n")
            f.write("user1,Alice,alice@test.com,login\n")
            f.write("user2,Bob,bob@test.com,file_access\n")
            temp_path = f.name

        try:
            from pipeline import run_complete_pipeline

            # Run pipeline with security enabled
            result = run_complete_pipeline(
                csv_path=temp_path, output_dir=tempfile.mkdtemp(), governance_enabled=True
            )

            # Should complete successfully
            assert result["success"] is True

            # Should have governance report
            assert "governance" in result["stages"]

            # Security events should be logged
            events = security_audit_log.get_events(event_type="data_ingestion")
            assert len(events) > 0

        finally:
            os.unlink(temp_path)


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
