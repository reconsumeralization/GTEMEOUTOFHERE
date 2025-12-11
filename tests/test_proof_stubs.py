#!/usr/bin/env python3
"""
Proof scaffolds for thesis alignment. These use lightweight fixtures to verify
data structures for SSM attempts, security controls presence, and recon scoring
provenance. Now includes fixtures for dashboard KPIs and API route checks.
"""

import json
from pathlib import Path
from typing import Any, Dict, List

import pytest

from ssm import log_ssm_session


FIXTURES_DIR = Path(__file__).parent / "fixtures"


def load_json_fixture(relative_path: str) -> Dict[str, Any]:
    path = FIXTURES_DIR / relative_path
    with path.open("r", encoding="utf-8") as f:
        return json.load(f)


def test_ssm_fixture_structure():
    """Validate SSM attempt/hint structure."""
    data = load_json_fixture("ssm/sample_ssm.json")
    assert data["task_id"]
    assert data["mode"] in ["guided", "reveal"]
    assert isinstance(data["attempts"], list) and data["attempts"]
    for attempt in data["attempts"]:
        assert attempt["step"] > 0
        assert attempt["input"]
        assert attempt["hint"]
        assert isinstance(attempt["complete"], bool)
    # Ensure reveal mode is explicit when present
    if data["mode"] == "reveal":
        assert data.get("reveal_reason")


def test_ssm_log_writer(tmp_path: Path):
    """Ensure SSM logs can be written and reloaded."""
    attempts = [
        {"step": 1, "input": "find pattern", "hint": "look at states", "complete": False},
        {"step": 2, "input": "map to skill", "hint": "viewer->editor", "complete": True},
    ]
    log_path = log_ssm_session("task_demo", attempts, output_dir=str(tmp_path))
    assert Path(log_path).exists()
    data = json.loads(Path(log_path).read_text())
    assert data["task_id"] == "task_demo"
    assert len(data["attempts"]) == 2
    assert data["attempts"][-1]["complete"] is True


def test_ssm_log_created_via_teacher_route(tmp_path: Path, monkeypatch: pytest.MonkeyPatch):
    """GET /teacher with user_id should create a hashed SSM log entry."""
    import importlib
    import os

    class _StubDB:
        def execute_one_safe(self, *args, **kwargs):
            return {"progression_count": 0}

    os.environ.setdefault("COSURVIVAL_SECRET_KEY", "test-secret-key")
    os.environ["SSM_LOG_DIR"] = str(tmp_path)
    app_module = importlib.import_module("app")
    monkeypatch.setattr(app_module, "get_db", lambda: _StubDB())
    monkeypatch.setattr(app_module, "enforce_access_control", lambda *args, **kwargs: (None, "u", "role"))
    client = app_module.app.test_client()
    resp = client.get("/teacher?user_id=testuser")
    assert resp.status_code in (200, 302)
    logs = list(tmp_path.glob("teacher_*.json"))
    assert logs, "Expected an SSM log file"


def test_security_controls_presence():
    """Ensure security controls are declared in app and CSRF is configured."""
    import os

    os.environ.setdefault("COSURVIVAL_SECRET_KEY", "test-secret-key")
    import importlib

    app_module = importlib.import_module("app")

    assert hasattr(app_module, "csrf"), "CSRFProtect should be attached"
    assert app_module.app.secret_key, "Secret key required for CSRF/session"


def test_query_post_requires_csrf():
    """POST /query without CSRF token should be rejected."""
    import os
    import importlib

    os.environ.setdefault("COSURVIVAL_SECRET_KEY", "test-secret-key")
    app_module = importlib.import_module("app")
    client = app_module.app.test_client()

    resp = client.post("/query", data={"user_id": "user1", "lens": "teacher"})
    assert resp.status_code in (400, 403)


def test_recon_fixture_provenance():
    """Validate recon provider scoring and friction point structure."""
    data = load_json_fixture("recon/sample_recon.json")
    providers = data["providers"]
    assert providers
    for p in providers:
        assert p["provider_id"]
        assert 0 <= p["reliability"] <= 1
        assert p["grade"] in ["A", "B", "C", "D", "F"]
        assert p["total_activities"] >= p["error_count"] >= 0
    friction = data["friction_points"]
    for f in friction:
        assert f["provider_id"]
        assert f["consumer_id"]
        assert f["friction_reason"]


def test_dashboard_summary_kpis():
    """Validate dashboard summary fixture contains KPI domains."""
    summary = load_json_fixture("pipeline/dashboard_summary.json")
    assert summary["overview"]["users"] >= 0
    assert summary["overview"]["companies"] >= 0
    assert summary["tribe_highlights"]["communities"] >= 0
    assert summary["teacher_highlights"]["roles"] >= 0
    assert summary["recon_highlights"]["providers_scored"] >= 0
    assert "governance" in summary and "passed" in summary["governance"]


class _ReconStubDB:
    """Stub DB for recon route testing."""

    def execute_safe(self, *_args, **_kwargs) -> List[Dict[str, Any]]:
        return [
            {
                "provider_id": "provider_a",
                "total_activities": 50,
                "error_count": 1,
                "reliability_score": 0.98,
            },
            {
                "provider_id": "provider_b",
                "total_activities": 20,
                "error_count": 3,
                "reliability_score": 0.85,
            },
        ]

    def execute_one_safe(self, *_args, **_kwargs):
        return None


def test_recon_api_with_stub_db(monkeypatch: pytest.MonkeyPatch):
    """Exercise recon API with stubbed DB to verify grading and payload shape."""
    import os
    import importlib

    os.environ.setdefault("COSURVIVAL_SECRET_KEY", "test-secret-key")
    app_module = importlib.import_module("app")

    # Bypass access control for this test
    monkeypatch.setattr(app_module, "enforce_access_control", lambda *args, **kwargs: (None, "user", "role"))
    monkeypatch.setattr(app_module, "get_db", lambda: _ReconStubDB())

    client = app_module.app.test_client()
    resp = client.get("/api/v1/recon/providers")
    assert resp.status_code == 200
    payload = resp.get_json()
    assert "providers" in payload
    grades = {p["provider_id"]: p["grade"] for p in payload["providers"]}
    assert grades["provider_a"] in ["A", "B"]
    assert grades["provider_b"] in ["C", "D", "F"]
