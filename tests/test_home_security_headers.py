#!/usr/bin/env python3
"""Home route security header test."""

import importlib
import os


def test_home_csp_hsts():
    os.environ.setdefault("COSURVIVAL_SECRET_KEY", "test-secret-key")
    app_module = importlib.import_module("app")
    client = app_module.app.test_client()
    resp = client.get("/", environ_overrides={"wsgi.url_scheme": "https"})
    assert resp.headers.get("Content-Security-Policy")
    assert resp.headers.get("X-Frame-Options") == "DENY"
    assert resp.headers.get("Strict-Transport-Security")
