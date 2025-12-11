#!/usr/bin/env python3
"""Unit tests for cosurvival.teaching.context_modes."""

import pytest  # type: ignore[import-not-found]

from cosurvival.teaching.context_modes import (
    ContextMode,
    AssignmentContext,
    detect_context_mode,
    create_practice_context,
    create_study_context,
    create_graded_context,
)


class TestDetectContextMode:
    def test_detects_graded_by_keywords(self):
        mode = detect_context_mode("Midterm Exam", "Closed book assessment")
        assert mode is ContextMode.GRADED

    def test_detects_practice_by_keywords(self):
        mode = detect_context_mode("Homework 3", "Practice set")
        assert mode is ContextMode.PRACTICE

    def test_defaults_to_study(self):
        mode = detect_context_mode("Reading", "General review")
        assert mode is ContextMode.STUDY

    def test_metadata_override(self):
        mode = detect_context_mode("Project", "", metadata={"is_practice": True})
        assert mode is ContextMode.PRACTICE


class TestAssignmentContextPolicies:
    def test_requires_attempt_in_graded(self):
        ctx = create_graded_context("a1", "Exam", "Final exam")
        assert ctx.requires_student_attempt is True
        assert ctx.requires_attempt_first() is True

        ctx.register_student_attempt()
        assert ctx.student_attempt_provided is True
        assert ctx.requires_attempt_first() is False

    def test_can_perform_actions(self):
        ctx_practice = create_practice_context("p1", "Practice", "")
        allowed, _ = ctx_practice.can_perform("full_solution")
        assert allowed is True

        ctx_graded = create_graded_context("g1", "Exam", "")
        allowed, reason = ctx_graded.can_perform("full_solution")
        assert allowed is False
        assert "practice" in reason.lower()

    def test_time_guard_flag(self):
        ctx = create_graded_context("g2", "Exam", "", time_limit=60)
        assert ctx.requires_time_guard() is True

    def test_tools_are_lowercased_and_set_based(self):
        ctx = create_study_context("s1", "Study", "")
        ctx.add_tool("Calculator")
        ctx.add_tool("NOTES")
        assert ctx.tools_allowed == {"calculator", "notes"}

    def test_unknown_action(self):
        ctx = create_practice_context("p2", "Practice", "")
        allowed, reason = ctx.can_perform("unknown_action")
        assert allowed is False
        assert "unknown" in reason.lower()

    def test_assignment_context_to_dict(self):
        ctx = create_practice_context("p3", "Practice", "Desc")
        assert isinstance(ctx, AssignmentContext)
        ctx_dict = ctx.to_dict()
        assert ctx_dict["mode"] == ContextMode.PRACTICE.value
        assert ctx_dict["assignment_id"] == "p3"


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
