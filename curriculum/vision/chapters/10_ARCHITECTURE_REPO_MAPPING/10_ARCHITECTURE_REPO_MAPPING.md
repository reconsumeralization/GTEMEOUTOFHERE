# Chapter 10 — System Architecture and Repo Mapping

This thesis aligns directly with the existing code and curriculum structure—and every component carries the same throughlines: advisor-not-executor (assist, don’t auto-act), trust fabric (provenance, consent, verification), reconsumeralization (ethical use by design), the cell model (small, auditable, least-privilege), and MAS (raising the floor for safety, capability, belonging, meaning).

High-level components:

- **Core Engine**: `cosurvival/*`, `app.py`, `models.py`  
- **Advisors Layer**: `cosurvival/advisors`, `teacher_advisor.py`  
- **Governance**: `governance.py`, `cosurvival/governance_tools`  
- **Tracking & Reviews**: `cosurvival/tracking/review_system.py`  
- **Curriculum**: `curriculum/core`, `curriculum/vision`, `curriculum/security`, `curriculum/ethics`  
- **Security Fabric**: `security.py`, `curriculum/security/*`  
- **Content Integrity Service**: integrity toolkit endpoint for synthetic/forgery detection across text/image/audio uploads and chat, with explainable flags and audit logs.  
- **Pipelines & Extractors**: `pipeline.py`, `extractors/*`  
- **Frontend**: `frontend/src/sections/*`

Conceptual mapping:

- **SSM** ↔ `SHADOW_STUDENT_MODE_ARCHITECTURE.md`
- **Tribes** ↔ `extractors/tribe_graph.py`, `frontend/src/sections/Tribe.tsx`
- **Security** ↔ `SECURITY_TRUST_FABRIC.md`, `SECURITY_IMPLEMENTATION_*`
- **Research Backbone** ↔ `RESEARCH_BACKBONE_PRD.md`

This chapter is the bridge between philosophical spec and working system. Keep the throughlines in view: services advise, humans decide; provenance is tracked and signed; components stay small and auditable; markets reward aligned conduct; and every layer is built to raise the floor for all.

### Field Note (The Analyst)
In one audit, a single poisoned config auto-ran on clone and pivoted across clouds. Architecture isn’t just a map of components—it’s a chain of custody. One weak link (auto-exec, unpinned deps, hardcoded creds) and the blast radius jumps vendors and clouds.

### Threat Model
- Auto-exec configs/CLIs; hardcoded creds; unpinned dependencies/actions.
- CI/CD leakage of secrets; unsigned artifacts; missing SBOM/provenance.
- Cross-cloud credential sprawl enabling chained pivots; downstream vendor compromise.
- Integrity endpoint overload or tampering: spam scans creating DoS; insider modification of detection logic to whitelist synthetics.

### Mitigation Checklist
- Enforce “advisor, not executor”: display-only, confirm-before-run; sandbox helpers; allowlists for binaries/args/env; block chaining/metacharacters.
- Pin deps/actions; SBOM + signature verification; secrets scanning; least-privilege CI tokens; MFA everywhere; keystore/HSM for signing keys.
- Map blast radius: assume one weak link can pivot across clouds/vendors; test with red-team drills and lockdowns.
- Content-integrity service hardening: rate limits and CAPTCHA on public edges, signed detector modules, immutable event logs, graceful degrade to human review if the service is unavailable.

---

**Prev:** [Chapter 9 — Spirituality](09_SPIRITUALITY_MEANING.md)  
**Next:** [Chapter 11 — Governance & Lenses](11_GOVERNANCE_LENSES.md)  
**Index:** [TEACHER Thesis Index](../TEACHER_THESIS_INDEX.md)
# Chapter 10  System Architecture and Repo Mapping

This thesis aligns directly with the existing code and curriculum structure.

High-level components:
- Core Engine: `cosurvival/*`, `app.py`, `models.py`
- Advisors Layer: `cosurvival/advisors`, `teacher_advisor.py`
- Governance: `governance.py`, `cosurvival/governance_tools`
- Tracking and Reviews: `cosurvival/tracking/review_system.py`
- Curriculum: `curriculum/core`, `curriculum/vision`, `curriculum/security`, `curriculum/ethics`
- Security Fabric: `security.py`, `curriculum/security/*`
- Pipelines and Extractors: `pipeline.py`, `extractors/*`
- Frontend: `frontend/src/sections/*`

Conceptual mapping:
- SSM: `SHADOW_STUDENT_MODE_ARCHITECTURE.md`
- Tribes: `extractors/tribe_graph.py`, `frontend/src/sections/Tribe.tsx`
- Security: `SECURITY_TRUST_FABRIC.md`, `SECURITY_IMPLEMENTATION_*`
- Research Backbone: `RESEARCH_BACKBONE_PRD.md`

Partnered inspirations and friend-of-the-program contributions:
- Bill (security reviewer) pushes MFA/least-privilege/continuous monitoring as default posture for every surface we ship ([bill.com](https://www.bill.com/product/security?utm_source=openai)).
- Dr. Mousa Bahrami informs our future-proof track with quantum-grade encryption and secure deletion concepts (Q-Trash/Q-Vault) for data at rest and in transit ([b2match.com](https://www.b2match.com/e/virtual-cybersecurity-b2b-2025/participants/2946359?utm_source=openai)).
- Andy Jenkinson’s “Whitethorn Shield” DNS/PKI/TLS misconfiguration sweeps guide our trust fabric hardening and feed the security pipeline with OSINT findings for remediation.
- Andrew Hopkins’ safety culture frame keeps “learn-from-incidents” and proactive hazard surfacing baked into governance and release gates ([investors.exscientia.ai](https://investors.exscientia.ai/press-releases/press-release-details/2023/Professor-Andrew-L.-Hopkins-elected-Fellow-of-the-Royal-Society/default.aspx?utm_source=openai)).

Active pipeline (friend/partner-led):
- FCA whistleblower path on late-fixed cloud vulns (90-day clock breached) with Gregory Krakauer as legal lead; target outcome: compel custodianship/mandate of remediation work as a trusted arm.
- “Whitethorn Shield” integrations: automated ingestion of DNS/PKI/TLS findings into our Security Fabric and dashboards.
- FileFlex AI integration: David leading applied AI security assist; prospective credit-union customer-in-the-loop.
- “Linked Open” graph utility to surface aligned professional contacts; “Buy the Breach” risk intelligence/short signals; “Privacy Chain” (Hopkins) applicability for media/government modernization.
- CLE training track (Andy, David, Bill) to translate practice into accredited education.

This chapter is the bridge between philosophical spec and working system.

---

**Prev:** [Chapter 9  Spirituality](09_SPIRITUALITY_MEANING.md)  
**Next:** [Chapter 11  Governance and Lenses](11_GOVERNANCE_LENSES.md)  
**Index:** [TEACHER Thesis Index](../TEACHER_THESIS_INDEX.md)
