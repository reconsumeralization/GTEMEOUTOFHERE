# COSURVIVAL Frontend Plan

## Purpose

Deliver a transparent, governance-first web experience that surfaces COSURVIVAL's three lenses (TRIBE, TEACHER, RECON), pipeline state, and AI advisor insights without exposing disallowed inferences. This document organizes the scope, architecture, and implementation phases for a modern frontend that consumes the existing Flask APIs and generated artifacts.

---

## Guiding Objectives

1. **Center Governance:** Highlight pipeline stages, governances scores, auditability, and provenance for every data point.
2. **Preserve Agency:** Provide preference controls (notification cadence, domains, framing) aligned with `UserPreferences` in `advisor.py`.
3. **Explainable Insights:** Pair all advisor outputs with "why now", evidence, and alternatives; clearly show derived data vs. source artifacts.
4. **Safe Aggregations:** Keep all views at aggregated/network levels, never rendering individual performance metrics or raw PII.
5. **Responsive & Accessible:** Mirror the cosmic-dark aesthetic established in `dashboard.html` while ensuring WCAG AA compliance across device sizes, including mobile-first layouts and touch interactions.

---

## Data Sources & Contracts

| Source | Format | Purpose | Notes |
| --- | --- | --- | --- |
| `/api/v1/tribe/graph` | JSON | Graph nodes/edges for TRIBE visualizations | Requires optional `company_id` filter.
| `/api/v1/teacher/recommendations` | JSON | Top permission-based recommendations | Needs `user_id`; inherits ACL + validation.
| `/api/v1/recon/providers` | JSON | Provider reliability stats | Optional company scope; includes calculated grades.
| Database counts | SQL via `SafeDatabase` | Stats for headers/cards | Already used in Flask templates; expose via new API if SPA.
| Pipeline artifacts (`cosurvival_mvp.json`, `dashboard_summary.json`) | JSON | Aggregated KPIs, communities, mentor lists | Produced by `pipeline.py` runs.
| Governance outputs (`governance_report.json`, `data_dictionary.md`) | JSON / MD | Risk flags, severity, classifications | Must stay downloadable for auditors.
| Advisor signals (future `/api/v1/advisor/signals`) | JSON | Weak/moderate/strong alerts + reasoning | Align with `CosurvivalAdvisor`.
| Security audit log excerpts | JSONL / DB | Rate limiting, access denials | Expose filtered API for UI timeline.
| Reviews API (`/api/v1/reviews`) | JSON | Peer/community reflections with governance prompts | Requires moderation + audit logging.
| Certificates store (`/api/v1/certificates`) | JSON / PDF | Issued certificates metadata + download links | Include verification hashes.

All client requests must include CSRF tokens emitted by Flask templates (`generate_csrf_token`) and honor `Retry-After` headers from the shared rate limiter.

---

## Recommended Libraries & Tools (2025)

### Core Framework & Build
- **React 18 + TypeScript:** Mature ecosystem, Suspense readiness, and tight typing support for the detailed data contracts in this plan.
- **Vite 5:** Fast dev server, modern bundling, and Vitest integration; works well for SPAs served via Flask.
- **pnpm** (or npm workspaces): Efficient monorepo-friendly package manager with deterministic lockfiles.

### State & Data Layer
- **Zustand** (with middleware/devtools): Lightweight global store for session, pipeline, advisor, review, and achievement slices without boilerplate.
- **TanStack Query v5:** Declarative fetching/caching, background refresh, retry/backoff—ideal for rate-limited Flask APIs.
- **Zod**: Runtime validation + TS inference, ensuring payloads from governance/advisor/review endpoints remain trustworthy.
- **idb-keyval**: Minimal IndexedDB helper for offline caching of review drafts and recently fetched artifacts.

### UI, Styling, and Accessibility
- **Tailwind CSS 3.4/4 + CSS variables:** Rapid mobile-first styling aligned with the cosmic palette; easy responsive breakpoints.
- **Radix UI Primitives:** Accessible dialogs, tabs, dropdowns to compose shells, review drawers, and preference panels.
- **Framer Motion 11:** High-performance animation library with `useReducedMotion` support for micro-interactions and celebratory sequences.
- **canvas-confetti** or **tsParticles:** Triggerable confetti/particle overlays for milestones, with configurable density for accessibility.
- **lottie-react:** Render Lottie JSON for certificate seals or subtle onboarding animations.
- **react-hook-form 7 + @hookform/resolvers/zod:** Performant, type-safe forms for reviews, settings, and query flows.

### Data Visualization
- **D3 v7/8:** Core engine for TRIBE force-directed graphs and bespoke network effects.
- **Visx 3.x:** React-friendly primitives for timelines, heatmaps, and KPI charts in TEACHER/RECON views.
- **Nivo 0.85 or Apache ECharts 5:** High-level components for chord/sankey diagrams to show RECON value flows when time-to-build is tight.

### Review, Recognition, Certificates
- **TipTap (ProseMirror) v2:** Structured rich-text editor with custom extensions enforcing governance-safe prompts for reviews.
- **pdf-lib / @react-pdf/renderer:** Client-side certificate generation with embedded verification hashes + QR codes.
- **html-to-image / dom-to-image-more:** Export shareable PNGs of badges/certificates without server rendering.
- **dayjs** (or date-fns): Lightweight date formatting for review timelines and certificate issuance records.

### Quality, Testing, Tooling
- **Vitest + React Testing Library:** Component/unit coverage consistent with workspace guidance.
- **Storybook 8 (Chromatic optional):** Visual regression + responsive testing for components (including motion states).
- **axe-core / @axe-core/react:** Automated accessibility checks across celebratory experiences.
- **Playwright:** E2E validation of review submissions, certificate downloads, and mobile nav flows with device emulation.

These tools reflect the current (2025) ecosystem and align with COSURVIVAL's requirements around governance, responsiveness, explainability, and celebratory UX.

---

## Getting Started Workflow

1. **Scaffold the React app (Vite + TypeScript):**
   ```bash
   npm create vite@latest cosurvival-frontend -- --template react-ts
   cd cosurvival-frontend
   npm install
   ```
   (Replace `npm` with `pnpm` or `yarn` if preferred.) Vite 5 ships with the most up-to-date React tooling and supports the fast dev cycle we need.

2. **Install core dependencies:**
   ```bash
   npm install zustand @tanstack/react-query zod react-hook-form @hookform/resolvers
   npm install -D tailwindcss postcss autoprefixer
   npx tailwindcss init -p
   ```
   Then configure Tailwind with the cosmic palette + Radix colors in `tailwind.config.ts`.

3. **Add visualization & animation libs as needed:**
   ```bash
   npm install d3 @visx/visx framer-motion canvas-confetti lottie-react
   npm install @tiptap/react @tiptap/starter-kit pdf-lib dom-to-image-more dayjs
   ```

4. **Set up linting/testing:**
   ```bash
   npm install -D eslint @typescript-eslint/parser @typescript-eslint/eslint-plugin
   npm install -D vitest @vitest/ui @testing-library/react @testing-library/jest-dom
   ```
   Configure Vitest in `vite.config.ts` and mirror repo lint rules.

5. **Connect to Flask backend:**
   - Use a `.env.local` file to store `VITE_API_BASE_URL` pointing at the Flask server (respecting governance guidelines).
   - Create an API client module that injects CSRF tokens from server-rendered bootstrap data before each fetch.

6. **Run locally:**
   ```bash
   npm run dev
   ```
   For production builds served by Flask, run `npm run build` and have Flask serve the `dist/` assets (or proxy via `vite build --watch` during development).

This workflow reflects the latest React/Vite tooling in 2025 and aligns with COSURVIVAL's architecture needs.

---

## Information Architecture

1. **Global Shell** – Fixed header, lens tabs (TRIBE/TEACHER/RECON), pipeline status indicator, user menu (identity, preferences, logout).
2. **Overview** – KPI tiles (users, companies, providers, governance grade), timeline of latest pipeline runs, quick links to artifacts.
3. **Governance & Pipeline** – Stage timeline (governance → ingestion → extraction → unified output), risk flag accordions, download buttons.
4. **TRIBE Lens** – Network canvas (D3), community cards, bridge + mentor spotlights, collaboration heatmaps.
5. **TEACHER Lens** – Role x privilege ladder, skill progression timeline, recommendation stack derived from permission changes.
6. **RECON Lens** – Provider reliability table, value-flow chords/bars, friction alerts with methodology notes.
7. **Advisor Feed** – Signal stack grouped by severity, reasoning drawer, dismissal/override controls tied to `UserPreferences`.
8. **Query Lab & Audit** – Enhanced UI for `/query`/`/results` plus searchable security + rate limit logs.
9. **Review & Recognition** – Space for peer/community reviews, milestone reflections, and certificate downloads with celebratory animations.
10. **Settings** – Agency controls (domains, notification cadence, framing text), API key management, accessibility toggles.

---

## Component System

| Component | Description | Data |
| --- | --- | --- |
| `PipelineStatusCard` | Visualizes stage completion, timestamps, links to raw files | `pipeline_results.json`
| `GovernanceChecklist` | Shows pass/fail items, severity, remediation guidance | `governance_report.json`
| `ArtifactList` | Downloadable artifacts with provenance badges | Files in `/output`
| `NetworkCanvas` | Force-directed graph with filters | `/api/v1/tribe/graph`
| `CommunityList` | Ranked communities with cohesion metrics | `TribeMVPOutput.communities`
| `BridgeSpotlight` | Highlights cross-silo connectors | `TribeMVPOutput.cross_silo_bridges`
| `MentorCard` | Mentor candidates with note on methodology | `TribeMVPOutput.mentor_candidates`
| `SkillProgressionTimeline` | Chronological privilege changes | `permission_changes`
| `RolePrivilegeMatrix` | Matrix of role vs. privilege adoption | Derived from canonical TEACHER data
| `RecommendationStack` | "Next skills" cards with peer context | `/api/v1/teacher/recommendations`
| `ProviderReliabilityTable` | Sortable table with filters and grade badges | `/api/v1/recon/providers`
| `ValueFlowChart` | Visualization of provider ↔ company volume | `ReconMVPExtractor` outputs
| `AdvisorSignalStack` | Cards grouped by severity + reasoning modals | Future advisor API
| `PreferenceDrawer` | Interacts with `UserPreferences` to adjust agency settings | `advisor.py`
| `AuditLogTable` | Paginated security events (rate limits, access denials) | `security_audit_log`
| `ReviewPanel` | Collects structured peer/mentor reviews with prompts + safeguards | New `/api/v1/reviews` (Flask + DB)
| `ReviewTimeline` | Chronological view of submitted reviews with filters and export | Same reviews endpoint
| `ConfettiOverlay` | Reusable celebration animation triggered on milestones/completions | Client-side animation config
| `AchievementBadge` | Displays unlocked milestones with micro-animations | Derived from review + pipeline events
| `CertificateGenerator` | Generates downloadable/shareable certificates (PDF/PNG) with verification hashes | Pipeline outputs + `certificates` store

Every visualization includes a "Data Source" tooltip linking to the originating artifact or API endpoint for traceability.

---

## Review & Celebration Experience

- **Review System:** Provide guided prompts (e.g., "What collaboration pattern did you observe?"), enforce governance-safe language templates, and store structured data via a new `/api/v1/reviews` endpoint backed by `SafeDatabase`. Include moderation hooks plus export to governance reviews.
- **Animations & Motion:** Use subtle micro-interactions (hover glows, tab transitions) plus event-based celebrations—when a user completes a learning milestone, publishes a review, or receives a certification, trigger the `ConfettiOverlay` with adjustable particle counts respecting reduced-motion preferences.
- **Achievements & Badges:** Map pipeline milestones (governance pass, TRIBE network goals, TEACHER progression) and advisor acknowledgments to unlockable badges displayed in `AchievementBadge` carousels. Each badge references underlying data and timestamps for auditability.
- **Certificates:** Offer customizable templates (organization seal, signatures) rendered client-side (HTML -> canvas/PDF) with embedded verification hashes. Certificates are downloadable/shareable and logged in audit history.
- **Accessibility:** All animations respect `prefers-reduced-motion`; provide alternative textual confirmations ("Goal unlocked!" toasts). Confetti and certificates must include ARIA announcements and keyboard-accessible controls.

---

## Responsive & Mobile Strategy

- **Breakpoints:** Adopt mobile-first CSS with key breakpoints at 480px (phones), 768px (tablets), 1024px (small desktops), 1440px (wide). Use CSS variables and utility mixins to keep spacing/typography consistent.
- **Navigation:** Collapse global lens tabs into a sticky bottom nav or off-canvas drawer on small screens; keep pipeline status + alerts accessible via compact banner.
- **Layouts:** Replace multi-column grids with stacked cards on mobile; ensure charts degrade gracefully (sparkline summaries, swipeable carousels for tables/graphs).
- **Interactions:** Provide touch targets ≥44px, enable pinch/zoom for D3 views, and add tap-to-focus tooltips rather than hover-only cues.
- **Performance:** Lazy-load heavy visualizations outside the viewport, leverage IntersectionObserver for infinite lists, and reuse data caches to avoid large re-fetches over cellular networks.
- **Testing:** Include responsive snapshots (Storybook or Percy) and manual audits using Chrome DevTools device emulation each sprint.

---

## State Management & Data Flow

- **Framework:** React + TypeScript (Vite), component library tailored to cosmic-dark theme. Use a predictable store (Zustand or Redux Toolkit) with slices: `session`, `pipeline`, `tribe`, `teacher`, `recon`, `advisor`, `governance`, `auditLogs`, `reviews`, `achievements`.
- **Bootstrap Data:** Server-rendered HTML injects `window.__COSURVIVAL_BOOTSTRAP__` containing CSRF token, current user, and minimal stats to avoid blank initial render.
- **Fetch Layer:** Centralized API client adds CSRF header, handles retries based on rate limiter hints, and surfaces access denials with guidance from `security_audit_log`.
- **Caching:** Keep latest successful payloads in memory + IndexedDB/localStorage (encrypted if storing sensitive metadata). Stale-while-revalidate pattern for lens data; cache review drafts offline so reflections can be composed without connectivity.
- **Derived Selectors:** Compute cross-lens overlaps (e.g., mentors flagged in advisor feed) and aggregate stats, plus correlations between review sentiments, achievements, and advisor recommendations without duplicating heavy computations inside components.

---

## Security & Compliance Considerations

1. Reuse Flask CSRF tokens and session cookies; SPA routes should remain behind `enforce_access_control` via server-side checks.
2. Guard every fetch with lens-specific ACL awareness—hide tabs or show "request access" placeholders when the API returns 403.
3. Enforce input validation client-side (mirroring `security.py`) but rely on server-side validation as the source of truth.
4. Keep all personally identifiable values hashed or omitted; display aggregated/restated metrics only.
5. Surface provenance: each insight card lists `Generated from: <file or endpoint> at <timestamp>` to maintain auditability.
6. Log significant client interactions (preference changes, dismissed recommendations, review submissions, certificate downloads) through secure POSTs so audit trails stay centralized.
7. Introduce moderation + approval workflows for community reviews, ensuring language is governance-compliant before becoming visible.

---

## Implementation Roadmap

1. **Phase 0 – Enablement**
   - Document API schemas and add Swagger/contract tests.
   - Expose pipeline + governance artifacts via lightweight JSON endpoints.
   - Stub `/api/v1/advisor/signals` returning sample payloads from `advisor.py` logic.

2. **Phase 1 – Foundation**
   - Scaffold React/Vite app with routing, theming, state store, and shared fetch client.
   - Implement global shell + Overview dashboard using `dashboard_summary.json`.
   - Integrate pipeline/governance panels with download links.

3. **Phase 2 – Lens Experiences**
   - TRIBE: Port D3 graph into reusable `NetworkCanvas`, add community + mentor components.
   - TEACHER: Build progression timeline, recommendation list, and role matrix.
   - RECON: Implement provider table, value flow visualization, friction alerts.

4. **Phase 3 – Advisor & Preferences**
   - Connect to advisor signals, implement reasoning drawers and preference management tied to `UserPreferences` endpoints.
   - Add dismissal/override flows with audit logging.

5. **Phase 4 – Query Lab & Audit Tools**
   - Modernize `/query` form into wizard with validation feedback and PRG still enforced via API.
   - Build audit log explorer with filters for event type, lens, severity.
   - Finalize accessibility, responsive stress tests, and Vitest coverage for critical components.

6. **Phase 5 – Reviews, Celebrations, Certificates**
   - Ship the review submission workflow (forms, moderation queue, timeline view) and wire to new backend endpoints.
   - Implement `ConfettiOverlay`, badge animations, and reduced-motion fallbacks tied to achievements + advisor milestones.
   - Build certificate generation + verification (download/share) and persist issuance records for auditability.

---

## Deliverables & Next Steps

- Align with stakeholders on advisor API contract and governance artifact hosting.
- Prepare wireframes for each lens panel + advisor feed before sprinting on UI.
- Decide whether the frontend ships as a pure SPA (served by Flask) or a hybrid (Flask-rendered shells + islands).
- Once agreed, spin up tasks per roadmap phases and track progress alongside pipeline enhancements.

This plan can evolve as new requirements emerge (e.g., additional domains like financial/health), but it provides the organized baseline for building COSURVIVAL's front-end experience.
