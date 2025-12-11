#!/usr/bin/env python3
"""Agent-as-Student demo endpoint tests."""

import importlib
import os
from pathlib import Path

import pytest
from flask.testing import FlaskClient


@pytest.fixture()
def client(monkeypatch: pytest.MonkeyPatch, tmp_path: Path):
    os.environ.setdefault("COSURVIVAL_SECRET_KEY", "test-secret-key")
    os.environ["SSM_LOG_DIR"] = str(tmp_path)
    app_module = importlib.import_module("app")
    # Bypass access control for tests
    monkeypatch.setattr(app_module, "enforce_access_control", lambda *args, **kwargs: (None, "u", "role"))
    return app_module.app.test_client()


def test_agent_student_demo_success(client: FlaskClient):
    resp = client.post(
        "/api/v1/teacher/agent_student_demo",
        json={"assignment": "Write a short summary", "constraint": "concise"},
    )
    assert resp.status_code == 200
    data = resp.get_json()
    for key in ["worked_solution", "steps", "common_mistakes", "rubric_map", "show_me"]:
        assert key in data
    assert isinstance(data["steps"], list)
    assert isinstance(data["common_mistakes"], list)
    assert isinstance(data["rubric_map"], list)


def test_agent_student_demo_validation(client: FlaskClient):
    resp = client.post("/api/v1/teacher/agent_student_demo", json={"assignment": ""})
    assert resp.status_code == 400


def test_catalog_why_this(client: FlaskClient):
    resp = client.post(
        "/api/v1/catalog/why_this",
        json={"product_ids": ["sku1", "sku2"]},
    )
    assert resp.status_code == 200
    data = resp.get_json()
    assert "explanations" in data
    assert len(data["explanations"]) == 2


def test_assessment_sample(client: FlaskClient):
    resp = client.post(
        "/api/v1/teacher/assessment_sample",
        json={"prompt": "Summarize the benefits", "rubric_note": "concise"},
    )
    assert resp.status_code == 200
    data = resp.get_json()
    for key in ["worked_solution", "steps", "common_mistakes", "rubric_map", "show_me"]:
        assert key in data
