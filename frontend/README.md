# COSURVIVAL Frontend

React + Vite + TypeScript application implementing the COSURVIVAL dashboard with governance-first UX, multi-lens navigation, advisor feed, and celebratory review workflows.

## Quick Start

```bash
cd frontend
npm install
npm run dev
```

Set `VITE_API_BASE_URL` in a `.env.local` file if the Flask backend is running on a different origin. The application expects Flask to emit bootstrap data (`__COSURVIVAL_BOOTSTRAP__`) with CSRF tokens, user ID, and role.

## Scripts

- `npm run dev` – Start Vite dev server.
- `npm run build` – Type-check and build for production.
- `npm run preview` – Preview production bundle.
- `npm run lint` – ESLint over `src`.
- `npm run test` – Vitest test runner (placeholder; add suites alongside components).

## Features

- Global navigation across Overview, Governance, TRIBE, TEACHER, RECON, Advisor, Reviews, and Settings panels.
- Zustand store + TanStack Query for state/fetching, with Zod validation and offline-friendly persistence.
- Responsive, accessibility-aware layout with Tailwind CSS and Framer Motion micro-interactions.
- Review submission workflow (React Hook Form + Zod) triggering confetti celebrations and populating the recognition feed.
- Placeholder API client ready to integrate with Flask endpoints (`/api/v1/tribe/graph`, `/api/v1/teacher/recommendations`, `/api/v1/recon/providers`, forthcoming advisor/reviews APIs).

Refer to `FRONTEND_PLAN.md` for detailed architecture, responsive strategy, and roadmap.
