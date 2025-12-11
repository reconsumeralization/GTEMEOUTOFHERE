#!/usr/bin/env python3
"""Smoke tests for Flask routes and template rendering."""

import importlib
import os
from typing import Any

import pytest


os.environ.setdefault("COSURVIVAL_SECRET_KEY", "test-secret-key")


class DummyDB:
    """Minimal stub to satisfy route queries without hitting SQLite."""

    def execute_one_safe(self, *args: Any, **kwargs: Any):
        return {"user_count": 0, "company_count": 0, "group_count": 0}

    def execute_safe(self, *args: Any, **kwargs: Any):
        return []

    def execute_write_safe(self, *args: Any, **kwargs: Any):
        return None

    def close(self) -> None:
        return None


@pytest.fixture(scope="function")
def client(monkeypatch: pytest.MonkeyPatch):
    app_module = importlib.import_module("app")
    dummy_db = DummyDB()

    monkeypatch.setattr(app_module, "get_db", lambda: dummy_db)
    # Bypass access control during smoke tests.
    monkeypatch.setattr(app_module, "enforce_access_control", lambda *_, **__: (None, "test", "role"))
    app_module.app.config["TESTING"] = True

    return app_module.app.test_client()


def test_index_renders(client):
    resp = client.get("/")
    assert resp.status_code == 200
    assert b"COSURVIVAL" in resp.data


def test_lens_pages_render(client):
    for path in ["/tribe", "/teacher", "/recon"]:
        resp = client.get(path)
        assert resp.status_code == 200
        assert b"Lens" in resp.data or b"Tribe" in resp.data
