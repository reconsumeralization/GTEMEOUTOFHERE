#!/usr/bin/env python3
"""Input validation and security header tests."""

import importlib
import os

import pytest


@pytest.fixture(scope="module")
def app_module():
    os.environ.setdefault("COSURVIVAL_SECRET_KEY", "test-secret-key")
    return importlib.import_module("app")


@pytest.fixture()
def app_client(app_module, monkeypatch):
    # Bypass access control for these tests
    monkeypatch.setattr(app_module, "enforce_access_control", lambda *args, **kwargs: (None, "u", "role"))
    return app_module.app.test_client()


@pytest.mark.parametrize(
    "path,param",
    [
        ("/tribe?company_id=" + "a" * 101, None),
        ("/tribe?company_id=bad!id", None),
        ("/teacher?user_id=" + "b" * 101, None),
        ("/teacher?user_id=bad$id", None),
        ("/recon?company_id=" + "c" * 101, None),
        ("/recon?company_id=bad$id", None),
    ],
)
def test_invalid_identifiers_blocked(app_client, path, param):
    resp = app_client.get(path)
    assert resp.status_code == 400


def test_query_post_requires_valid_id(app_client):
    resp = app_client.post("/query", data={"user_id": "bad$id", "lens": "teacher"})
    assert resp.status_code == 400


def test_hsts_when_https(app_client):
    resp = app_client.get("/", environ_overrides={"wsgi.url_scheme": "https"})
    assert resp.headers.get("Strict-Transport-Security")
