# COSURVIVAL - Start Here

## Quick Setup
- `python -m venv .venv && .\.venv\Scripts\activate` (PowerShell) or `source .venv/bin/activate` (Unix)
- `pip install -r requirements.txt`
- Set a strong secret key before running Flask: `set COSURVIVAL_SECRET_KEY=replace-me` (or export on Unix).
- Run the full pipeline on your CSV: `python pipeline.py path/to/activity.csv ./output`
- Serve the dashboard artifacts: `cd output && python -m http.server 8000` (opens `dashboard.html`).
- Launch the Flask app for lens pages: `python app.py` (uses templates under `templates/`).

## Where to Look
- **Pipeline entry:** `pipeline.py` (writes governance + MVP JSON to `./output`).
- **Flask app:** `app.py` + Jinja templates in `templates/` (Tribe/Teacher/Recon/Query).
- **MVP logic:** `ingestion.py`, `mvp_extractors.py`, `governance.py`.
- **Dashboard (static):** `dashboard.html` expects `cosurvival_mvp.json`, `tribe_network.json`, `dashboard_summary.json`.

## Security & Provenance
- Secret key is mandatory; the app refuses to start without `COSURVIVAL_SECRET_KEY`.
- CSRF is enforced via Flask-WTF; forms include `csrf_token()`.
- Generate a local SBOM after dependency changes: `python scripts/generate_sbom.py` → `sbom.json`.

## Tests
- Smoke tests (including Flask template render) run with `pytest`.
- Add data-focused tests beside their modules (e.g., `tests/` for governance/ingestion).
