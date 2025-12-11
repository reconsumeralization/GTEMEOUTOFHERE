# Content Taxonomy: Medium Papers → COSURVIVAL Ecosystem

## Overview

This taxonomy maps Reconsumeralization Medium papers to COSURVIVAL's product taxonomy (TEACHER, TRIBE, RECON, Security, Supply Chain, Transparency). Each paper is tagged and linked to features, policies, and learning assets.

---

## Taxonomy Structure

### Top-Level Categories

1. **TEACHER** - Learning, education, curriculum, certification
2. **TRIBE** - Relationships, collaboration, community, mentorship
3. **RECON** - Value exchange, provider scoring, ethical commerce
4. **Security** - Privacy, governance, PII, access control
5. **Supply Chain** - Provenance, SBOM, signed artifacts, verification
6. **Transparency** - Explainability, audit trails, reasoning, governance gates

### Secondary Tags

- **AI/ML** - AI systems, machine learning, pattern recognition
- **Governance** - Rules, policies, guardrails, prohibited inferences
- **Ethics** - Fairness, bias, exploitation prevention
- **Architecture** - System design, data structures, algorithms
- **Philosophy** - Vision, principles, "Labor of Love"

---

## Mapping Table

| Paper Title | Primary Category | Secondary Tags | Feature Link | Policy Link | Learning Asset |
|------------|------------------|----------------|--------------|-------------|----------------|
| *Cross-ecosystem supply chain risk* | Supply Chain | Security, Governance | `extractors/recon_scores.py` | `governance.py` | TEACHER Week 7 + 10 |
| *Signed artifacts and SBOM* | Supply Chain | Security, Provenance | `security.py` | `governance.py` | TEACHER Week 10 |
| *AI as advisor, not authority* | TEACHER | AI/ML, Philosophy | `advisor.py` | `teacher_advisor.py` | TEACHER Week 0 |
| *The labor of love* | Philosophy | AI/ML, TEACHER | `teacher_advisor.py` | `VISION_ALIGNMENT.md` | TEACHER Week 0 |
| *Cross-generational learning* | TEACHER | Philosophy, TRIBE | `teacher_advisor.py` | `progression_tracker.py` | TEACHER Week AI |
| *TEACHER: Equal Access Codex* | TEACHER | Architecture, Philosophy | `progression_tracker.py` | `curriculum/core/TEACHER_CORE_TRACK.md` | All TEACHER Weeks |
| *CS50 for data* | TEACHER | Architecture, Algorithms | `curriculum/core/TEACHER_WEEK*.md` | `curriculum/core/TEACHER_CORE_TRACK.md` | All TEACHER Weeks |
| *Self-relative mastery* | TEACHER | Philosophy, Governance | `progression_tracker.py` | `curriculum/core/TEACHER_CORE_TRACK.md` | TEACHER Week 0 |
| *Reconsumeralization framework* | RECON | Philosophy, Ethics | `mvp_extractors.py` | `models.py` | TEACHER Week 3 |
| *Provider ethics scoring* | RECON | Ethics, Governance | `extractors/recon_scores.py` | `models.py` | TEACHER Week 3 |
| *Dispute resolution* | RECON | Governance, TRIBE | `mvp_extractors.py` | `governance.py` | TEACHER Week 5 |
| *Transparent reasoning* | Transparency | AI/ML, Governance | `advisor.py` | `governance.py` | TEACHER Week 0 |
| *Provenance as first-class* | Supply Chain | Security, Transparency | `governance.py` | `ingestion.py` | TEACHER Week 1 |
| *The governance gate* | Security | Governance, Transparency | `governance.py` | `governance.py` | TEACHER Week 0 |

---

## Detailed Mappings

### TEACHER Category

**Papers:**
- *TEACHER: Equal Access Codex*
- *CS50 for data: Teaching the three lenses*
- *Self-relative mastery: Growth over rank*
- *Cross-generational learning*
- *AI as advisor, not authority*

**Feature Modules:**
- `progression_tracker.py` - Self-relative learning tracking
- `teacher_advisor.py` - TEACHER-certified AI advisor
- `curriculum/core/TEACHER_CORE_TRACK.md` - Complete curriculum
- `curriculum/TEACHER_WEEK*.md` - Individual week modules

**Policy Documents:**
- `curriculum/TEACHER_CORE_TRACK.md` - Curriculum framework
- `curriculum/TEACHER_ETHICAL_GUARDRAILS.md` - Ethical guidelines
- `VISION_ALIGNMENT.md` - Vision alignment

**Learning Assets:**
- All TEACHER Week modules (0-10 + AI)
- Problem sets for each week
- Demo scripts and examples

---

### TRIBE Category

**Papers:**
- *The collaboration graph: Who is connected to whom*
- *Mentorship at scale: Finding bridges*
- *Community detection in organizational networks*

**Feature Modules:**
- `extractors/tribe_graph.py` - Graph building, community detection
- `mvp_extractors.py` - TribeMVPExtractor
- `models.py` - TribeUser, TribeRelationship, TribeCommunity

**Policy Documents:**
- `governance.py` - PII handling for social graphs
- `lens_boundary.py` - TRIBE lens boundaries

**Learning Assets:**
- TEACHER Week 2 (Data Structures) - Graph structures
- TEACHER Week 3 (Algorithms) - Community detection
- TEACHER Week 5 (Data Structures) - Hash tables for scale

---

### RECON Category

**Papers:**
- *Reconsumeralization: From passive consumption to active value exchange*
- *Provider ethics scoring: Reliability × Transparency × Fairness*
- *Dispute resolution in the value graph*
- *Value flows: Measuring reciprocity*

**Feature Modules:**
- `extractors/recon_scores.py` - Provider scoring
- `mvp_extractors.py` - ReconMVPExtractor
- `models.py` - ReconProvider, ReconValueFlow, ReconEthicsScore

**Policy Documents:**
- `governance.py` - Bias guardrails for provider rankings
- `models.py` - EthicsGrade enum, ethics scoring

**Learning Assets:**
- TEACHER Week 3 (Algorithms) - Provider scoring algorithm
- TEACHER Week 5 (Data Structures) - Value flow graphs
- TEACHER Week 7 (SQL) - Provider database design

---

### Security Category

**Papers:**
- *Signed artifacts and SBOM: Building trust from the ground up*
- *The governance gate: What we will and won't infer*
- *PII handling: Privacy by design*

**Feature Modules:**
- `security.py` - Password hashing, input validation, XSS prevention
- `governance.py` - PIIHandler, GovernanceGate
- `lens_boundary.py` - Lens boundary contracts
- `lensgrind.py` - Privacy auditor

**Policy Documents:**
- `governance.py` - PII handling, prohibited inferences
- `security.py` - Security best practices
- `curriculum/SECURITY_CONTROLS_CHECKLIST.md` - Security checklist

**Learning Assets:**
- TEACHER Week 0 (Concepts) - Governance gate
- TEACHER Week 1 (Fundamentals) - PII handling
- TEACHER Week 10 (Security) - Complete security module

---

### Supply Chain Category

**Papers:**
- *Cross-ecosystem supply chain risk: Why provenance matters*
- *Signed artifacts and SBOM: Building trust from the ground up*
- *The supply chain as a trust graph*

**Feature Modules:**
- `security.py` - Signed artifact verification
- `governance.py` - Provenance tracking
- `extractors/recon_scores.py` - Provider verification

**Policy Documents:**
- `governance.py` - Provenance requirements
- `security.py` - SBOM validation

**Learning Assets:**
- TEACHER Week 7 (SQL) - Supply chain database design
- TEACHER Week 10 (Security) - Supply chain security

---

### Transparency Category

**Papers:**
- *Transparent reasoning: Why AI must explain itself*
- *Provenance as a first-class concern*
- *The governance gate: What we will and won't infer*

**Feature Modules:**
- `advisor.py` - Transparent reasoning in recommendations
- `governance.py` - GovernanceGate, explainable decisions
- `lensgrind.py` - Privacy audit reports

**Policy Documents:**
- `governance.py` - Transparency requirements
- `advisor.py` - Reasoning transparency

**Learning Assets:**
- TEACHER Week 0 (Concepts) - Governance gate, explainability
- TEACHER Week 1 (Fundamentals) - Data dictionary
- TEACHER Week AI (Making it Intelligent) - Explainable AI

---

## Auto-Tagging Rules

### Rule-Based Tagging

```python
# Example tagging logic
if "supply chain" in title.lower() or "sbom" in title.lower() or "provenance" in title.lower():
    tags.add("Supply Chain")
    tags.add("Security")

if "teacher" in title.lower() or "learning" in title.lower() or "education" in title.lower():
    tags.add("TEACHER")

if "tribe" in title.lower() or "collaboration" in title.lower() or "community" in title.lower():
    tags.add("TRIBE")

if "recon" in title.lower() or "value exchange" in title.lower() or "provider" in title.lower():
    tags.add("RECON")

if "transparent" in title.lower() or "explain" in title.lower() or "reasoning" in title.lower():
    tags.add("Transparency")

if "ai" in title.lower() or "advisor" in title.lower() or "authority" in title.lower():
    tags.add("AI/ML")
    tags.add("TEACHER")
```

---

## Usage in Product

### Research Library UI

Filter by:
- Category (TEACHER, TRIBE, RECON, Security, Supply Chain, Transparency)
- Secondary tags (AI/ML, Governance, Ethics, etc.)
- Feature link (show papers that inform a specific module)
- Policy link (show papers that inform governance rules)
- Learning asset (show papers for a specific TEACHER week)

### Feature Context

When viewing a feature/module, show:
- "Research Foundation" section
- List of papers that inform this feature
- 1-sentence takeaways
- Links to full papers

### Policy Context

When viewing governance rules, show:
- "Policy Rationale" section
- Papers that establish the principles
- Why this rule exists
- How it connects to the vision

### Learning Context

In TEACHER curriculum, show:
- "Further Reading" section
- Papers relevant to this week's concepts
- How research connects to practice
- Links to full papers

---

*This taxonomy makes research a first-class citizen in the COSURVIVAL ecosystem.*

