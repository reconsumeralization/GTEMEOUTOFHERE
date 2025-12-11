#!/usr/bin/env python3
"""Trust scan endpoint tests."""

import importlib
import os

import pytest
from flask.testing import FlaskClient


@pytest.fixture()
def client(monkeypatch: pytest.MonkeyPatch):
    os.environ.setdefault("COSURVIVAL_SECRET_KEY", "test-secret-key")
    app_module = importlib.import_module("app")
    monkeypatch.setattr(app_module, "enforce_access_control", lambda *args, **kwargs: (None, "u", "role"))
    return app_module.app.test_client()


def test_trust_scan_blocks_abuse(client: FlaskClient):
    resp = client.post("/api/v1/teacher/agent_student_demo", json={"assignment": "This mentions csam", "constraint": "concise"})
    assert resp.status_code == 400
    resp2 = client.post("/api/v1/teacher/agent_student_demo", json={"assignment": "Normal task", "constraint": "concise"})
    assert resp2.status_code == 200
