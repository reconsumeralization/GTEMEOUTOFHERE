#!/usr/bin/env python3
"""
COSURVIVAL FLASK APPLICATION
============================
Full-stack web application for COSURVIVAL dashboard.

Implements Week 9 (Flask) + Week 10 (Security) patterns:
- Flask routes for TRIBE/TEACHER/RECON
- Jinja templates for dashboard
- SQL integration with parameterized queries
- Security: input validation, XSS prevention, CSRF protection
- JSON APIs for dashboard data
"""

# =============================================================================
# CONFIG & IMPORTS
# =============================================================================

# Standard library imports
import os  # noqa: E402
import sys  # noqa: E402
import hashlib  # noqa: E402
from datetime import datetime  # noqa: E402

# Third-party imports
from flask import Flask, render_template, request, jsonify, redirect, url_for, g  # noqa: E402
from flask_wtf.csrf import CSRFProtect, generate_csrf  # type: ignore[import-not-found, attr-defined]  # noqa: E402

# Add current directory to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# Local imports
from database import SafeDatabase  # noqa: E402
from extractors.ingest import extract_entities, ingest_csv  # noqa: E402, F401
from extractors.recon_scores import identify_friction_points, score_providers  # noqa: E402, F401
from extractors.teacher_paths import build_role_skill_matrix, track_progressions  # noqa: E402, F401
from cosurvival.teaching.context_modes import (  # noqa: E402
    AssignmentContext,
    ContextMode,
    detect_context_mode,
)
from security import (  # noqa: E402
    access_controller,
    generate_csrf_token,  # noqa: F401
    rate_limiter,  # noqa: F401
    sanitize_input,
    secret_manager,
    security_audit_log,
    validate_company_id,  # noqa: F401
    validate_lens,
    validate_user_id,  # noqa: F401
    verify_csrf_token,  # noqa: F401
)
from ssm import log_ssm_session  # noqa: E402

# =============================================================================
# APP SETUP & SECRETS
# =============================================================================

app = Flask(__name__)

# Harden session cookies by default; override via env for special cases
app.config.update(
    SESSION_COOKIE_SECURE=True,
    SESSION_COOKIE_HTTPONLY=True,
    SESSION_COOKIE_SAMESITE="Lax",
)

def _resolve_secret_key() -> str:
    """Resolve a non-default secret key or fail fast."""
    env_key = os.environ.get("COSURVIVAL_SECRET_KEY") or os.environ.get("SECRET_KEY")
    if env_key and env_key != "dev-secret-key-change-in-production":
        return env_key
    raise RuntimeError("COSURVIVAL_SECRET_KEY is required to run the Flask app securely.")


try:
    app.secret_key = secret_manager.get_api_key("COSURVIVAL_SECRET_KEY")
except ValueError:
    app.secret_key = _resolve_secret_key()

# Enable CSRF protection (Week 10: security)
csrf = CSRFProtect(app)

# Valid lenses (Week 9: authoritative list)
VALID_LENSES = {"tribe", "teacher", "recon"}

LENS_ACCESS_DOMAINS = {
    "tribe": "education",
    "teacher": "education",
    "recon": "supplier",
}


@app.context_processor
def inject_csrf_token():
    """Expose CSRF token generator to Jinja templates."""

    return {"csrf_token": generate_csrf}


@app.after_request
def apply_security_headers(response):
    """Apply baseline security headers."""

    csp = (
        "default-src 'self'; "
        "script-src 'self'; "
        "style-src 'self' 'unsafe-inline'; "
        "img-src 'self' data:; "
        "object-src 'none'; "
        "base-uri 'self'; "
        "frame-ancestors 'none'"
    )
    permissions_policy = (
        "accelerometer=(), camera=(), microphone=(), geolocation=(), gyroscope=(), "
        "magnetometer=(), usb=(), payment=(), fullscreen=(self)"
    )
    response.headers.setdefault("Content-Security-Policy", csp)
    response.headers.setdefault("X-Frame-Options", "DENY")
    response.headers.setdefault("Referrer-Policy", "no-referrer")
    response.headers.setdefault("X-Content-Type-Options", "nosniff")
    response.headers.setdefault("Permissions-Policy", permissions_policy)
    if request.is_secure:
        response.headers.setdefault(
            "Strict-Transport-Security", "max-age=31536000; includeSubDomains"
        )
    return response


# =============================================================================
# INPUT VALIDATION
# =============================================================================


def _normalize_identifier(raw_value):
    """Normalize and validate incoming identifiers."""

    if raw_value is None:
        return ""
    value = str(raw_value).strip()
    if len(value) > 100:
        raise ValueError("Input too long")
    if value and not all(ch.isalnum() or ch in {"_", "-"} for ch in value):
        raise ValueError("Invalid characters")
    return value


def _scan_for_abuse(content: str) -> dict:
    """
    Very light stub for abuse/CSAM/grooming detection.
    In production, replace with dedicated classifiers and escalation.
    """
    lowered = content.lower()
    indicators = []
    for token in ["csam", "child abuse", "grooming", "sex tourism"]:
        if token in lowered:
            indicators.append(token)
    return {"hit": bool(indicators), "indicators": indicators}


# =============================================================================
# ACCESS CONTROL & CONTEXT HELPERS
# =============================================================================
def _get_request_identity() -> tuple[str, str]:
    """Derive sanitized user identity and role from the request context."""

    raw_user = request.args.get("user_id") or request.form.get("user_id") or "anonymous"
    raw_role = request.args.get("user_role") or request.form.get("user_role") or "consumer"

    return sanitize_input(raw_user), sanitize_input(raw_role)


def enforce_access_control(
    lens: str, action: str, resource: str, response_format: str = "html"
):
    """Enforce blast-radius controls for a lens/resource combination."""

    user_id, user_role = _get_request_identity()
    domain = LENS_ACCESS_DOMAINS.get(lens, "consumer")
    allowed, reason = access_controller.check_access(
        user_id=user_id,
        user_role=user_role,
        resource=resource,
        action=action,
        domain=domain,
    )

    if allowed:
        return None, user_id, user_role

    security_audit_log.log_event(
        "access_denied",
        {
            "lens": lens,
            "user_id": user_id,
            "user_role": user_role,
            "resource": resource,
            "reason": reason,
            "ip": request.remote_addr,
        },
    )

    if response_format == "json":
        return (jsonify({"error": reason}), 403), user_id, user_role

    return (render_template("error.html", message=reason), 403), user_id, user_role


def _build_assignment_context() -> AssignmentContext:
    """
    Build an assignment context from request data for policy enforcement.
    
    Inputs supported:
    - context_mode: "practice" | "study" | "graded" (defaults to study)
    - assignment_title / assignment_description: optional metadata
    - student_attempt: if provided, counts as submitted attempt
    
    This is used to ensure TEACHER responses respect academic integrity:
    - Graded mode requires student attempt before detailed help.
    - Practice/Study modes allow broader assistance.
    """
    mode_raw = (
        request.form.get("context_mode")
        or request.args.get("context_mode")
        or "study"
    ).lower()
    title = request.form.get("assignment_title") or "Inline Request"
    description = request.form.get("assignment_description") or ""
    student_attempt = request.form.get("student_attempt") or ""
    tools_raw = request.form.get("tools_allowed") or ""

    try:
        mode = ContextMode(mode_raw)
    except ValueError:
        # Fall back to heuristic detection if explicit mode is unknown
        mode = detect_context_mode(title, description)

    ctx = AssignmentContext(
        assignment_id=request.form.get("assignment_id") or "inline",
        mode=mode,
        title=title,
        description=description,
    )

    if student_attempt.strip():
        ctx.register_student_attempt()

    if tools_raw:
        for tool in tools_raw.split(","):
            tool = tool.strip()
            if tool:
                ctx.add_tool(tool)

    return ctx


@app.before_request
def apply_rate_limiting():
    """Apply request-level rate limiting before any handler executes."""

    endpoint = request.endpoint or "unknown"
    key = f"{request.remote_addr or 'unknown'}:{endpoint}:{request.method}"
    allowed, message, retry_after = rate_limiter.check_rate_limit(key)

    if allowed:
        return None

    security_audit_log.log_event(
        "rate_limit_triggered",
        {"endpoint": endpoint, "ip": request.remote_addr, "message": message},
    )

    response = jsonify({"error": "rate_limit", "message": message})
    response.status_code = 429
    if retry_after:
        delta = int((retry_after - datetime.now()).total_seconds())
        response.headers["Retry-After"] = max(delta, 0)
    return response


# =============================================================================
# DATABASE CONNECTION (Week 7: SQL integration)
# =============================================================================


def get_db():
    """
    Get database connection with proper lifecycle management.

    Uses Flask's g object for request-scoped connections.
    """
    if "db" not in g:
        g.db = SafeDatabase()
    return g.db


@app.teardown_appcontext
def close_db(error):
    """Close database connection at end of request."""
    db = g.pop("db", None)
    if db is not None:
        db.close()


# =============================================================================
# ROUTES - Dashboard Pages (Week 9: Flask routes)
# =============================================================================


@app.route("/")
def index():
    """Dashboard home page."""
    return render_template("index.html")


@app.route("/tribe")
def tribe():
    """
    TRIBE network visualization page.

    Week 9: Template rendering
    Week 10: Input validation
    """
    denial, _, _ = enforce_access_control("tribe", "read", "tribe_dashboard")
    if denial:
        return denial
    # Get optional filters (Week 9: query parameters)
    company_id = request.args.get("company_id")
    if company_id:
        try:
            company_id = _normalize_identifier(company_id)
        except ValueError as exc:
            return render_template("error.html", message=str(exc)), 400

    # Query database (Week 7: SQL)
    db = get_db()

    # Use parameterized query (Week 10: SQL injection prevention)
    if company_id:
        query = """
            SELECT COUNT(*) as user_count, COUNT(DISTINCT group_id) as group_count
            FROM users
            WHERE company_id = ?
        """
        stats = db.execute_one_safe(query, (company_id,))
    else:
        query = (
            "SELECT COUNT(*) as user_count, COUNT(DISTINCT company_id) as company_count FROM users"
        )
        stats = db.execute_one_safe(query)

    return render_template("tribe.html", company_id=company_id, stats=dict(stats) if stats else {})


@app.route("/teacher")
def teacher():
    """
    TEACHER learning pathways page.

    Week 9: Template rendering
    Week 10: Input validation
    """
    denial, _, _ = enforce_access_control("teacher", "read", "teacher_dashboard")
    if denial:
        return denial

    user_id = request.args.get("user_id")

    if user_id:
        # Validate input (Week 10: security)
        try:
            user_id = _normalize_identifier(user_id)
        except ValueError as exc:
            return render_template("error.html", message=str(exc)), 400

        # Log SSM session for traceability (hash to avoid PII)
        hashed_user = hashlib.sha256(user_id.encode()).hexdigest()[:16]
        attempts = [
            {"step": 1, "input": "validate_user_id", "hint": "id format check", "complete": True}
        ]
        try:
            log_ssm_session(
                task_id=f"teacher_{hashed_user}",
                attempts=attempts,
                mode="guided",
            )
        except Exception:
            # Do not block page render on SSM logging failure
            pass

        # Query database (Week 7: SQL with parameterized query)
        db = get_db()
        query = """
            SELECT COUNT(*) as progression_count
            FROM permission_changes
            WHERE user_id = ?
        """
        stats = db.execute_one_safe(query, (user_id,))
    else:
        stats = None

    return render_template("teacher.html", user_id=user_id, stats=dict(stats) if stats else {})


@app.route("/recon")
def recon():
    """
    RECON provider scores page.

    Week 9: Template rendering
    Week 10: Input validation
    """
    denial, _, _ = enforce_access_control("recon", "read", "recon_dashboard")
    if denial:
        return denial

    company_id = request.args.get("company_id")

    if company_id:
        # Validate input (Week 10: security)
        try:
            company_id = _normalize_identifier(company_id)
        except ValueError as exc:
            return render_template("error.html", message=str(exc)), 400

    # Query database (Week 7: SQL with parameterized query)
    db = get_db()
    if company_id:
        query = """
            SELECT COUNT(DISTINCT provider_id) as provider_count,
                   SUM(CASE WHEN error_code IS NOT NULL THEN 1 ELSE 0 END) as error_count
            FROM activities
            WHERE company_id = ?
        """
        stats = db.execute_one_safe(query, (company_id,))
    else:
        query = """
            SELECT COUNT(DISTINCT provider_id) as provider_count,
                   SUM(CASE WHEN error_code IS NOT NULL THEN 1 ELSE 0 END) as error_count
            FROM activities
        """
        stats = db.execute_one_safe(query)

    return render_template("recon.html", company_id=company_id, stats=dict(stats) if stats else {})


# =============================================================================
# QUERY ROUTE (Week 9: Forms + POST)
# =============================================================================


@app.route("/query", methods=["GET", "POST"])
def query():
    """
    Query interface - handles both GET (show form) and POST (process query).

    Week 9: GET + POST consolidation
    Week 10: Server-side validation, CSRF protection
    """
    denial, _, _ = enforce_access_control("teacher", "write", "lens_query")
    if denial:
        return denial

    if request.method == "POST":
        # Build academic-integrity-aware context (Shadow Student guardrail)
        assignment_ctx = _build_assignment_context()

        # Get form data
        user_id = request.form.get("user_id")
        lens = request.form.get("lens")

        # Server-side validation (Week 10: never trust client)
        if not user_id:
            return render_template("error.html", message="User ID is required"), 400

        # Validate user_id (Week 10: input validation)
        try:
            user_id = _normalize_identifier(user_id)
        except ValueError as exc:
            return render_template("error.html", message=str(exc)), 400

        # Validate lens (Week 10: whitelist validation)
        is_valid, error = validate_lens(lens)
        if not is_valid:
            return render_template("error.html", message=error), 400

        # Sanitize input (Week 10: XSS prevention)
        user_id = sanitize_input(user_id)
        lens = sanitize_input(lens)

        denial_by_lens, _, _ = enforce_access_control(lens, "write", f"{lens}_query")
        if denial_by_lens:
            return denial_by_lens

        # Enforce context policy: graded mode requires student attempt before detailed help
        # For now we gate on "full_solution" to keep TEACHER from over-assisting.
        allowed, reason = assignment_ctx.can_perform("full_solution")
        if not allowed:
            return render_template("error.html", message=reason), 403

        # Log security event (Week 10: audit trail)
        security_audit_log.log_event(
            "query_submission",
            {
                "user_id": user_id,
                "lens": lens,
                "ip": request.remote_addr,
                "context_mode": assignment_ctx.mode.value,
                "requires_attempt": assignment_ctx.requires_student_attempt,
                "student_attempt_provided": assignment_ctx.student_attempt_provided,
            },
        )

        # Process query
        query_id = save_query(user_id, lens)

        # Redirect to results (Week 9: Post-Redirect-Get pattern)
        return redirect(url_for("results", query_id=query_id))

    # GET: Show query form
    return render_template("query.html")


@app.route("/results/<query_id>")
def results(query_id):
    """
    Display query results.

    Week 10: Input validation for query_id
    """
    denial, _, _ = enforce_access_control("teacher", "read", "query_results")
    if denial:
        return denial

    # Validate query_id (Week 10: security)
    try:
        query_id = _normalize_identifier(query_id)
    except ValueError as exc:
        return render_template("error.html", message=str(exc)), 400

    # Get results from database (Week 7: SQL with parameterized query)
    db = get_db()
    query = "SELECT * FROM queries WHERE id = ?"
    result = db.execute_one_safe(query, (query_id,))

    if not result:
        return render_template("error.html", message="Query not found"), 404

    return render_template("results.html", result=dict(result))


# =============================================================================
# API ENDPOINTS (Week 9: JSON APIs)
# =============================================================================


@app.route("/api/v1/tribe/graph")
def api_tribe_graph():
    """
    TRIBE graph data API endpoint.

    Week 9: JSON API
    Week 10: Input validation, SQL injection prevention
    """
    denial, _, _ = enforce_access_control(
        "tribe", "read", "tribe_graph", response_format="json"
    )
    if denial:
        return denial

    company_id = request.args.get("company_id")

    # Validate input (Week 10: security)
    if company_id:
        try:
            company_id = _normalize_identifier(company_id)
        except ValueError as exc:
            return jsonify({"error": str(exc)}), 400

    # Query database (Week 7: SQL with parameterized query)
    db = get_db()

    if company_id:
        query = """
            SELECT u1.id AS user_a, u2.id AS user_b, COUNT(*) AS collaboration_count
            FROM activities a1
            JOIN activities a2 ON a1.user_id = a2.target_user_id
            JOIN users u1 ON a1.user_id = u1.id
            JOIN users u2 ON a2.user_id = u2.id
            WHERE u1.company_id = ? AND u2.company_id = ?
            GROUP BY u1.id, u2.id
            HAVING collaboration_count >= 5
        """
        rows = db.execute_safe(query, (company_id, company_id))
    else:
        query = """
            SELECT u1.id AS user_a, u2.id AS user_b, COUNT(*) AS collaboration_count
            FROM activities a1
            JOIN activities a2 ON a1.user_id = a2.target_user_id
            JOIN users u1 ON a1.user_id = u1.id
            JOIN users u2 ON a2.user_id = u2.id
            GROUP BY u1.id, u2.id
            HAVING collaboration_count >= 5
        """
        rows = db.execute_safe(query)

    graph_data = {
        "nodes": list(set([row["user_a"] for row in rows] + [row["user_b"] for row in rows])),
        "edges": [
            {"source": row["user_a"], "target": row["user_b"], "weight": row["collaboration_count"]}
            for row in rows
        ],
    }

    return jsonify(graph_data)


@app.route("/api/v1/teacher/recommendations")
def api_teacher_recommendations():
    """
    TEACHER recommendations API endpoint.

    Week 9: JSON API
    Week 10: Input validation
    """
    denial, _, _ = enforce_access_control(
        "teacher", "read", "teacher_recommendations", response_format="json"
    )
    if denial:
        return denial

    user_id = request.args.get("user_id")

    # Validate input (Week 10: security)
    if not user_id:
        return jsonify({"error": "user_id required"}), 400

    try:
        user_id = _normalize_identifier(user_id)
    except ValueError as exc:
        return jsonify({"error": str(exc)}), 400

    # Query database (Week 7: SQL with parameterized query)
    db = get_db()
    query = """
        SELECT permission_type, COUNT(*) as frequency
        FROM permission_changes
        WHERE user_id = ?
        GROUP BY permission_type
        ORDER BY frequency DESC
        LIMIT 5
    """
    rows = db.execute_safe(query, (user_id,))

    recommendations = [
        {"skill": row["permission_type"], "frequency": row["frequency"]} for row in rows
    ]

    return jsonify({"recommendations": recommendations})


@app.route("/api/v1/recon/providers")
def api_recon_providers():
    """
    RECON provider scores API endpoint.

    Week 9: JSON API
    Week 10: Input validation
    """
    denial, _, _ = enforce_access_control(
        "recon", "read", "recon_providers", response_format="json"
    )
    if denial:
        return denial

    company_id = request.args.get("company_id")

    # Validate input (Week 10: security)
    if company_id:
        try:
            company_id = _normalize_identifier(company_id)
        except ValueError as exc:
            return jsonify({"error": str(exc)}), 400

    # Query database (Week 7: SQL with parameterized query)
    db = get_db()

    if company_id:
        query = """
            SELECT 
                p.id AS provider_id,
                COUNT(a.id) AS total_activities,
                SUM(CASE WHEN a.error_code IS NOT NULL THEN 1 ELSE 0 END) AS error_count,
                ROUND(1.0 - (SUM(CASE WHEN a.error_code IS NOT NULL THEN 1 ELSE 0 END) * 1.0 / COUNT(a.id)), 3) AS reliability_score
            FROM providers p
            JOIN activities a ON p.id = a.provider_id
            WHERE a.company_id = ?
            GROUP BY p.id
            HAVING total_activities >= 10
            ORDER BY reliability_score DESC
        """
        rows = db.execute_safe(query, (company_id,))
    else:
        query = """
            SELECT 
                p.id AS provider_id,
                COUNT(a.id) AS total_activities,
                SUM(CASE WHEN a.error_code IS NOT NULL THEN 1 ELSE 0 END) AS error_count,
                ROUND(1.0 - (SUM(CASE WHEN a.error_code IS NOT NULL THEN 1 ELSE 0 END) * 1.0 / COUNT(a.id)), 3) AS reliability_score
            FROM providers p
            JOIN activities a ON p.id = a.provider_id
            GROUP BY p.id
            HAVING total_activities >= 10
            ORDER BY reliability_score DESC
        """
        rows = db.execute_safe(query)

    providers = [
        {
            "provider_id": row["provider_id"],
            "reliability": row["reliability_score"],
            "total_activities": row["total_activities"],
            "error_count": row["error_count"],
            "grade": "A"
            if row["reliability_score"] >= 0.99
            else "B"
            if row["reliability_score"] >= 0.95
            else "C"
            if row["reliability_score"] >= 0.90
            else "F",
        }
        for row in rows
    ]

    return jsonify({"providers": providers})


# =============================================================================
# HELPER FUNCTIONS
# =============================================================================


def save_query(user_id: str, lens: str) -> str:
    """
    Save query to database.

    Week 7: SQL integration
    Week 10: Parameterized queries
    """
    db = get_db()
    query_id = f"query_{datetime.now().timestamp()}"

    # Use parameterized query (Week 10: SQL injection prevention)
    db.execute_write_safe(
        """
        INSERT INTO queries (id, user_id, lens, timestamp)
        VALUES (?, ?, ?, datetime('now'))
    """,
        (query_id, user_id, lens),
    )

    return query_id


# =============================================================================
# ERROR HANDLERS
# =============================================================================


@app.errorhandler(404)
def not_found(error):
    """Handle 404 errors."""
    return render_template("error.html", message="Page not found"), 404


@app.errorhandler(500)
def internal_error(error):
    """Handle 500 errors."""
    # Log error (Week 10: security audit)
    security_audit_log.log_event("server_error", {"error": str(error), "ip": request.remote_addr})
    return render_template("error.html", message="Internal server error"), 500


# =============================================================================
# API - Agent-as-Student Demo (TEACHER)
# =============================================================================


@csrf.exempt
@app.route("/api/v1/teacher/agent_student_demo", methods=["POST"])
def api_agent_student_demo():
    """
    Agent-as-Student demo endpoint.

    Returns a worked solution, step-by-step explanation, common mistakes,
    rubric mapping, and a "show me" mode for a sample assignment.
    """
    denial, _, _ = enforce_access_control(
        "teacher", "read", "agent_student_demo", response_format="json"
    )
    if denial:
        return denial

    payload = request.get_json(silent=True) or {}
    assignment = payload.get("assignment", "").strip()
    constraint = payload.get("constraint", "concise")

    if not assignment:
        return jsonify({"error": "assignment required"}), 400
    if len(assignment) > 500:
        return jsonify({"error": "assignment too long"}), 400
    if len(constraint) > 50:
        return jsonify({"error": "constraint too long"}), 400

    abuse = _scan_for_abuse(assignment)
    if abuse["hit"]:
        security_audit_log.log_event(
            "abuse_flag",
            {"type": "content", "indicators": abuse["indicators"], "ip": request.remote_addr},
        )
        return jsonify({"error": "content rejected"}), 400

    worked_solution = "Sample solution: outline key points and conclude with one actionable next step."
    steps = [
        "Restate the assignment in your own words.",
        "List 3-4 key points relevant to the prompt.",
        f"Apply constraint: {constraint}.",
        "Conclude with a clear next action.",
    ]
    common_mistakes = [
        "Overly long responses.",
        "Missing a conclusion or next step.",
        "Ignoring the stated constraint.",
    ]
    rubric_map = [
        {"criterion": "Clarity", "weight": 0.3, "expectation": "Plain, direct language."},
        {"criterion": "Relevance", "weight": 0.4, "expectation": "Addresses prompt and constraint."},
        {"criterion": "Actionability", "weight": 0.3, "expectation": "Ends with a next step."},
    ]
    show_me = (
        "Here’s how to do it: write 3 bullets covering the prompt, "
        "keep sentences short, and end with one suggested action."
    )

    try:
        digest = hashlib.sha256(assignment.encode()).hexdigest()[:16]
        attempts = [
            {"step": 1, "input": "parse_assignment", "hint": "strip/length check", "complete": True},
            {"step": 2, "input": "generate_outline", "hint": "steps/common mistakes/rubric/show_me", "complete": True},
        ]
        log_ssm_session(
            task_id=f"agent_demo_{digest}",
            attempts=attempts,
            mode="guided",
        )
    except Exception:
        pass

    return jsonify(
        {
            "worked_solution": worked_solution,
            "steps": steps,
            "common_mistakes": common_mistakes,
            "rubric_map": rubric_map,
            "show_me": show_me,
        }
    )


@csrf.exempt
@app.route("/api/v1/teacher/assessment_sample", methods=["POST"])
def api_assessment_sample():
    """
    Agent-as-Student sample for a course assessment.

    Returns solution, steps, mistakes, rubric map, show-me; logs SSM.
    """
    denial, _, _ = enforce_access_control(
        "teacher", "read", "assessment_sample", response_format="json"
    )
    if denial:
        return denial

    payload = request.get_json(silent=True) or {}
    prompt = payload.get("prompt", "").strip()
    rubric_note = payload.get("rubric_note", "concise and factual")

    if not prompt:
        return jsonify({"error": "prompt required"}), 400
    if len(prompt) > 500:
        return jsonify({"error": "prompt too long"}), 400
    if len(rubric_note) > 100:
        return jsonify({"error": "rubric_note too long"}), 400

    abuse = _scan_for_abuse(prompt)
    if abuse["hit"]:
        security_audit_log.log_event(
            "abuse_flag",
            {"type": "content", "indicators": abuse["indicators"], "ip": request.remote_addr},
        )
        return jsonify({"error": "content rejected"}), 400

    worked_solution = "Answer the prompt with 3 bullet points and cite one source."
    steps = [
        "Identify the main question in the prompt.",
        "Draft 3 concise bullets that address it directly.",
        f"Apply rubric note: {rubric_note}.",
        "Cite one credible source.",
    ]
    common_mistakes = [
        "Ignoring the rubric note.",
        "Excessive length.",
        "Missing a source.",
    ]
    rubric_map = [
        {"criterion": "Relevance", "weight": 0.4, "expectation": "Directly answers the prompt."},
        {"criterion": "Clarity", "weight": 0.3, "expectation": "Concise bullets."},
        {"criterion": "Evidence", "weight": 0.3, "expectation": "At least one credible source."},
    ]
    show_me = "Write 3 bullets, each tied to the prompt, and include (Source: ...)."

    try:
        digest = hashlib.sha256(prompt.encode()).hexdigest()[:16]
        attempts = [
            {"step": 1, "input": "parse_prompt", "hint": "strip/length check", "complete": True},
            {"step": 2, "input": "generate_assessment_outline", "hint": "steps/mistakes/rubric/show_me", "complete": True},
        ]
        log_ssm_session(
            task_id=f"assessment_{digest}",
            attempts=attempts,
            mode="guided",
        )
    except Exception:
        pass

    return jsonify(
        {
            "worked_solution": worked_solution,
            "steps": steps,
            "common_mistakes": common_mistakes,
            "rubric_map": rubric_map,
            "show_me": show_me,
        }
    )


# =============================================================================
# API - Catalog Explainability (Why This)
# =============================================================================


@csrf.exempt
@app.route("/api/v1/catalog/why_this", methods=["POST"])
def api_catalog_why_this():
    """
    Provide a simple explainability payload for a list of product IDs.

    Factors: safety > quality > sustainability > personalization (opt-in).
    """
    denial, _, _ = enforce_access_control(
        "tribe", "read", "catalog_explain", response_format="json"
    )
    if denial:
        return denial

    payload = request.get_json(silent=True) or {}
    product_ids = payload.get("product_ids", [])
    if not isinstance(product_ids, list) or not product_ids:
        return jsonify({"error": "product_ids list required"}), 400
    if len(product_ids) > 50:
        return jsonify({"error": "too many product_ids"}), 400

    explanations = []
    for pid in product_ids:
        pid_norm = str(pid)
        if len(pid_norm) > 100:
            continue
        factors = [
            {"factor": "safety", "weight": 0.4, "reason": "Trusted supplier, no recent flags."},
            {"factor": "quality", "weight": 0.3, "reason": "High review integrity, low defect rate."},
            {"factor": "sustainability", "weight": 0.2, "reason": "Supplier disclosed footprint and audits."},
            {"factor": "personalization", "weight": 0.1, "reason": "Based on opted-in preferences."},
        ]
        explanations.append({"product_id": pid_norm, "factors": factors})

    return jsonify({"explanations": explanations})


# =============================================================================
# MAIN
# =============================================================================

if __name__ == "__main__":
    # Week 10: Security reminder
    if app.secret_key == "dev-secret-key-change-in-production":
        print("⚠️  WARNING: Using default secret key. Change in production!")

    app.run(debug=True, host="0.0.0.0", port=5000)
