# TEACHER Thesis → Product Requirements Mapping

This document maps thesis chapters to product epics and illustrative user stories. It is designed to sit alongside the thesis, the core curriculum, and the implementation tracks.

## How to use this guide
- Start from the chapter you’re implementing.
- Align with the epic(s) below.
- Use the user stories as acceptance scaffolds; refine per sprint.
- Link your tickets back to this map to keep narrative → execution traceable.

---

## Part I — Context & Purpose

### Ch1: Crisis of Acceleration → Epic: Adaptive Capacity
- **User Story:** As a learner, I want content that stays current with AI/tools so I don’t fall behind when platforms change.
- **User Story:** As a curriculum maintainer, I want a change-diff pipeline that flags outdated modules when core APIs or security practices change.
- **Acceptance:** Content freshness checks; version tagging; visible “last updated” in UI.

### Ch2: Mutually Assured Success (MAS) → Epic: MAS Baseline & Equity
- **User Story:** As an admin, I want MAS baseline metrics (safety, capability, belonging, meaning) tracked per cohort so I can see if the floor is rising.
- **User Story:** As a learner, I want an onboarding that sets my initial safety and capability baseline without shaming or ranking.
- **Acceptance:** MAS KPI dashboard; non-comparative baselines; equity segment views.

---

## Part II — The TEACHER System

### Ch3: Definition & Core Hypotheses → Epic: Advisor-Not-Authority UX
- **User Story:** As a learner, I want guidance that is explainable and challengeable so I remain in control.
- **User Story:** As a guardian, I want visibility into how advice was generated without exposing private student work to third parties.
- **Acceptance:** Explainability panel; “challenge/appeal” affordance; guardian-safe summaries.

### Ch4: Shadow Student Mode (SSM) → Epic: Proof-of-Understanding Engine
- **User Story:** As a student, I want hints derived from real solution attempts, not generic tips, so help feels targeted.
- **User Story:** As a reviewer, I want SSM runs logged with reasoning steps and “solution reveal” events clearly labeled.
- **Acceptance:** SSM trace artifacts; hint quality tied to traces; reveal-mode logging; graded-mode guardrails.

### Ch5: Courses & World Grade → Epic: World-Grade Curriculum
- **User Story:** As a learner, I want a holistic progress map (skills, security, ethics, meaning) so I can navigate growth, not just grades.
- **User Story:** As a curriculum designer, I want modular skills and micro-skills linked to projects and assessments.
- **Acceptance:** World Grade view (navigation, not ranking); modular skill graph; transfer tasks across domains.

### Ch6: Tribes → Epic: Belonging & Mentorship
- **User Story:** As a learner, I want an opt-in tribe aligned to my values and goals so I’m not learning alone.
- **User Story:** As a mentor, I want safe, scoped channels to support mentees without overexposing personal data.
- **Acceptance:** Tribe enrollment with consent; mentorship matching; community milestones; moderation & safety cues.

### Ch7: Security → Epic: Trust Fabric
- **User Story:** As a learner, I want built-in security literacy (phishing, consent, manipulation detection) embedded in my path.
- **User Story:** As a platform owner, I want hard boundaries (rate limits, ACLs, audit logs) and lens-based access controls.
- **Acceptance:** Security lessons as first-class modules; platform controls active (CSRF, RBAC/ACL, logging); governance reports generated.

### Ch8: Reconsumeralization → Epic: Ethical Marketplace Layer
- **User Story:** As a student, I want to see transparent supplier profiles and friction points so I can practice ethical consumption.
- **User Story:** As an org leader, I want provider scores (adoption, reliability, transparency) with evidence, not just grades.
- **Acceptance:** Provider scorecards with methodology notes; value-flow views; dispute/feedback channels; transparency metrics beyond placeholders.

### Ch9: Spirituality & Meaning → Epic: Meaning-Safe UX
- **User Story:** As a learner, I want reflective prompts and value-alignment tools without AI claiming moral or spiritual authority.
- **User Story:** As a guardian, I want assurance that spiritual content is respectful, optional, and non-coercive.
- **Acceptance:** Opt-in reflection modules; guardrails prohibiting AI “authority” claims; clear boundaries in UX copy.

---

## Part III — Architecture, Governance, Evaluation

### Ch10: Architecture & Repo Mapping → Epic: Traceable Architecture
- **User Story:** As an engineer, I want a clear map from thesis concepts to code paths so I can extend features without breaking alignment.
- **User Story:** As a PM, I want implementation status per component (core, advisors, governance, tracking, frontend).
- **Acceptance:** Up-to-date architecture map; component status; links to outputs (cosurvival_mvp.json, dashboard_summary.json).

### Ch11: Governance & Lenses → Epic: Multi-Lens Governance
- **User Story:** As a learner/parent/mentor/security reviewer, I want lens-specific views with appropriate data minimization.
- **User Story:** As a compliance reviewer, I want audit logs and challenge flows for significant decisions.
- **Acceptance:** Lens configs enforced (lens_boundary/lensgrind); auditability of decisions; challenge/review pathways.

### Ch12: Evaluation & World Grade → Epic: Evaluation System
- **User Story:** As a learner, I want feedback that guides effort, not labels my identity.
- **User Story:** As an analyst, I want quantitative (time-to-competence, incidents) and qualitative (belonging, confidence) signals together.
- **Acceptance:** Non-comparative feedback; World Grade signals; mixed-methods dashboards.

### Ch13: Risks & Safeguards → Epic: Safety & Integrity
- **User Story:** As a risk officer, I want enumerated failure modes (overreach, data exploitation, dependency, cultural flattening, spiritual misuse) with mitigations and alerts.
- **User Story:** As an admin, I want explicit advisor-not-authority enforcement across flows.
- **Acceptance:** Risk register with mitigations; policy checks in high-stakes flows; red-team/audit hooks.

### Ch14: Roadmap → Epic: Deployment Phases
- **User Story:** As a program lead, I want clear phase gates (prototype, family pilot, tribes+recon, institutional, MAS coalition) with success criteria.
- **Acceptance:** Phase gate checklist; pilot success metrics; rollout plan per segment.

---

## Close & Conclusion

### Conclusion — Labor of Love → Epic: Narrative Integrity
- **User Story:** As a communicator, I want the product story to reinforce “advisor-not-authority,” dignity, and the Labor of Love.
- **Acceptance:** Consistent messaging in docs, UI copy, and demos; no dark patterns; respect for user agency throughout.

---

## Appendices

### Appendix A — Non-Negotiables → Epic: Guardrail Enforcement
- **User Story:** As a platform owner, I want system-wide enforcement of non-negotiables (advisor-not-authority, privacy=dignity, security-first, ability to say no, SSM required, spirituality respected, explainability/challengeability, no dependency growth hacks).
- **Acceptance:** Guardrail checklist integrated into design reviews; automated tests where applicable.

### Appendix B — SSM Policy → Epic: SSM Compliance
- **User Story:** As a QA lead, I want SSM runs logged and reveal events labeled; as a PM, I want graded-mode protections.
- **Acceptance:** Logging of SSM traces; reveal-mode labels; graded-mode blocks; test coverage for constraints.

### Appendix C — MAS Checklist → Epic: MAS Compliance
- **User Story:** As a release manager, I want a MAS checklist run before shipping features.
- **Acceptance:** MAS checklist gating; documentation of decisions when exceptions occur.

### Appendix D — Repo Layout → Epic: Doc/Code Coherence
- **User Story:** As a newcomer, I want the repo structure to mirror the thesis map so I can find code and docs fast.
- **Acceptance:** READMEs and indexes updated; cross-links to code and outputs; consistent naming.

