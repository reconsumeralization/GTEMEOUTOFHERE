# MCP Docker Management

On-demand Docker orchestration for the backend (Flask) and frontend (Vite) MCP services.

## Prereqs
- Docker Desktop (with WSL2 backend on Windows).
- Repo root: `C:\Users\recon\teacher`

## Files
- `docker-compose.mcp.yml` – services and ports.
- `Dockerfile.mcp.backend` – Python/Flask on port 5000.
- `frontend/Dockerfile.mcp.frontend` – Vite dev server on port 5173.
- `mcp.ps1` – helper script for compose actions.
- `scan_mcp.py` – discovers candidate services (already run; produced `mcp_candidates.json`).

## Tested
- `docker compose -f docker-compose.mcp.yml config` ✅
- `docker compose -f docker-compose.mcp.yml build` ✅ (frontend uses `npm install`; no lockfile present).

## Usage (PowerShell, from repo root)
- Build images: `./mcp.ps1 build`
- Start all: `./mcp.ps1 up`
- Start one: `./mcp.ps1 up backend` or `./mcp.ps1 up frontend`
- Logs: `./mcp.ps1 logs backend` (or frontend)
- Stop one: `./mcp.ps1 stop backend`
- Stop/remove all: `./mcp.ps1 down`

## Direct compose (if you prefer)
```
docker compose -f docker-compose.mcp.yml up mcp-backend
docker compose -f docker-compose.mcp.yml up mcp-frontend
docker compose -f docker-compose.mcp.yml stop mcp-backend
docker compose -f docker-compose.mcp.yml down
```

## Hot reload
- Volumes are mounted (`.:/app`, `./frontend:/app`), so code edits on host reflect in containers.
- Frontend runs `npm run dev -- --host --port 5173`.
- Backend runs `python app.py` on port 5000.

## Ports
- Backend: host `5000` → container `5000`
- Frontend: host `5173` → container `5173`

## Notes
- Frontend build uses `npm install` (no package-lock present). If you add a lockfile, switch to `npm ci` in `frontend/Dockerfile.mcp.frontend`.
- `npm install` reported a few moderate advisories; run `npm audit fix --force` if you want to address them (may change deps).

