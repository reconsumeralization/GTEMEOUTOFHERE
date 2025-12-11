#!/usr/bin/env python3
"""Security header tests for Flask app."""

import importlib
import os


def test_csp_and_frame_headers():
    os.environ.setdefault("COSURVIVAL_SECRET_KEY", "test-secret-key")
    app_module = importlib.import_module("app")
    client = app_module.app.test_client()
    resp = client.get("/")
    assert resp.status_code in (200, 302)  # allow redirect if auth enforced later
    headers = resp.headers
    assert "Content-Security-Policy" in headers
    assert headers["X-Frame-Options"] == "DENY"
    assert headers["Referrer-Policy"] == "no-referrer"
    assert headers["X-Content-Type-Options"] == "nosniff"
