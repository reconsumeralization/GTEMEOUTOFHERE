#!/usr/bin/env python3
"""
Unit tests for enhanced severity scoring in governance.py.

CURRICULUM: Week 0, Activity 0.3 - Governance Gate
CURRICULUM: Week 10 - Security Module
Testing chain impact severity scoring from vulnerability report 440782380
"""

import pytest
from datetime import datetime

from governance import (
    GovernanceGate,
    SeverityScore,
    PIIHandler,
)


class TestSeverityScoring:
    """Test enhanced severity scoring with chain impact."""

    def test_severity_score_creation(self):
        """Test SeverityScore dataclass creation."""
        score = SeverityScore(entry_point=5, chain_impact=7, blast_radius=3, final=7)

        assert score.entry_point == 5
        assert score.chain_impact == 7
        assert score.blast_radius == 3
        assert score.final == 7  # max(5, 7, 3)

    def test_final_severity_is_max(self):
        """Test that final severity is maximum of all three."""
        score = SeverityScore(entry_point=3, chain_impact=8, blast_radius=5, final=8)

        assert score.final == max(3, 8, 5)

    def test_requires_architecture_mitigation(self):
        """Test architecture mitigation trigger."""
        # High chain impact
        score1 = SeverityScore(entry_point=3, chain_impact=7, blast_radius=2, final=7)  # >= 7
        assert score1.requires_architecture_mitigation() is True

        # High blast radius
        score2 = SeverityScore(entry_point=3, chain_impact=2, blast_radius=7, final=7)  # >= 7
        assert score2.requires_architecture_mitigation() is True

        # Both low
        score3 = SeverityScore(entry_point=3, chain_impact=5, blast_radius=4, final=5)
        assert score3.requires_architecture_mitigation() is False

    def test_requires_ecosystem_review(self):
        """Test ecosystem review trigger."""
        # High blast radius
        score = SeverityScore(entry_point=3, chain_impact=2, blast_radius=5, final=5)  # >= 5
        assert score.requires_ecosystem_review() is True

        # Low blast radius
        score2 = SeverityScore(entry_point=3, chain_impact=2, blast_radius=3, final=3)  # < 5
        assert score2.requires_ecosystem_review() is False


class TestVulnerabilityAssessment:
    """Test vulnerability assessment with chain impact."""

    def setup_method(self):
        """Set up test fixtures."""
        self.gate = GovernanceGate()

    def test_assess_entry_point_severity(self):
        """Test entry point severity assessment."""
        vulnerability = {"impact": "critical", "complexity": "low", "auth_required": False}

        severity = self.gate._assess_entry_point(vulnerability)

        # Critical + low complexity + no auth = high score
        assert severity >= 7

    def test_assess_chain_impact(self):
        """Test chain impact assessment."""
        vulnerability = {
            "can_pivot_products": True,
            "can_pivot_domains": True,
            "local_execution_surface": True,
            "supply_chain_impact": True,
        }

        severity = self.gate._assess_chain_impact(vulnerability)

        # Multiple pivot points = high chain impact
        assert severity >= 7

    def test_assess_blast_radius(self):
        """Test blast radius assessment."""
        vulnerability = {
            "affected_products": ["teacher", "tribes", "courses"],
            "affected_domains": ["consumer", "supplier"],
        }

        severity = self.gate._assess_blast_radius(vulnerability)

        # 3 products + 2 domains = high blast radius
        assert severity >= 5

    def test_complete_severity_assessment(self):
        """Test complete severity assessment."""
        vulnerability = {
            "id": "test_001",
            "impact": "high",
            "complexity": "medium",
            "auth_required": False,
            "can_pivot_products": True,
            "can_pivot_domains": True,
            "local_execution_surface": True,
            "affected_products": ["teacher", "tribes"],
            "affected_domains": ["consumer", "supplier"],
        }

        severity = self.gate.assess_severity(vulnerability)

        assert isinstance(severity, SeverityScore)
        assert severity.entry_point > 0
        assert severity.chain_impact > 0
        assert severity.blast_radius > 0
        assert severity.final == max(
            severity.entry_point, severity.chain_impact, severity.blast_radius
        )

    def test_vulnerability_assessment_with_recommendations(self):
        """Test complete vulnerability assessment."""
        vulnerability = {
            "id": "test_002",
            "impact": "high",
            "complexity": "low",
            "auth_required": False,
            "can_pivot_products": True,
            "can_pivot_domains": True,
            "local_execution_surface": True,
            "affected_products": ["teacher", "tribes", "courses"],
            "affected_domains": ["consumer", "supplier", "education"],
        }

        assessment = self.gate.assess_vulnerability(vulnerability)

        assert assessment["vulnerability_id"] == "test_002"
        assert "severity_score" in assessment
        assert "requires_architecture_mitigation" in assessment
        assert "requires_ecosystem_review" in assessment
        assert "recommendations" in assessment

        # Should have recommendations for high chain impact
        assert len(assessment["recommendations"]) > 0

    def test_duplicate_entry_point_high_chain_impact(self):
        """
        Test that duplicate entry point with high chain impact triggers mitigation.

        This tests the key insight from 440782380:
        "Entry-point bugs can be duplicate, but the impact chain is novel."
        """
        vulnerability = {
            "id": "duplicate_entry_but_novel_chain",
            "impact": "low",  # Low entry point severity
            "complexity": "high",
            "auth_required": True,
            "can_pivot_products": True,  # But high chain impact!
            "can_pivot_domains": True,
            "local_execution_surface": True,
            "affected_products": ["teacher", "tribes", "courses", "reconsumeralization"],
            "affected_domains": ["consumer", "supplier", "education", "admin"],
        }

        assessment = self.gate.assess_vulnerability(vulnerability)

        # Even with low entry point, high chain impact should trigger mitigation
        if assessment["severity_score"]["chain_impact"] >= 7:
            assert assessment["requires_architecture_mitigation"] is True

        if assessment["severity_score"]["blast_radius"] >= 5:
            assert assessment["requires_ecosystem_review"] is True


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
