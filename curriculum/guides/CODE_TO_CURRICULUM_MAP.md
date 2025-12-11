# Code to Curriculum Mapping

This document maps all code files to their corresponding curriculum weeks and activities.

---

## governance.py

**Primary Curriculum Mapping:**
- **Week 0, Activity 0.3:** The Governance Gate
  - PII handling, bias guardrails, prohibited inferences
  - `PIIHandler`, `GovernanceGate`, `PROHIBITED_INFERENCES`, `BIAS_GUARDRAILS`
  
- **Week 0, Activity 0.4:** Ethical Guardrails
  - AI as advisor, not authority
  - Anti-patterns prevention
  
- **Week 1, Activity 1.1:** Build a Data Dictionary
  - `ColumnDefinition`, `SensitivityLevel`, `PIIType`
  - Column classification by sensitivity
  
- **Week 1, Activity 1.2:** Write Governance Rules
  - `PROHIBITED_INFERENCES` list
  - Rules that BLOCK analysis
  
- **Week 10:** Security Module
  - PII protection, secure data handling

**Key Classes:**
- `SensitivityLevel` - Week 1, Activity 1.1
- `ColumnDefinition` - Week 1, Activity 1.1
- `PIIHandler` - Week 0, Activity 0.3; Week 1, Activity 1.1; Week 10
- `GovernanceGate` - Week 0, Activity 0.3; Week 1, Activity 1.2

---

## ingestion.py

**Primary Curriculum Mapping:**
- **Week 1, Core Concepts #1:** Canonical Entities
  - The seven canonical entities: User, Company, Group, Provider, Resource, Activity, Permission
  
- **Week 1, Core Concepts #3:** Schema Detection
  - `ColumnMapper` - pattern matching for column names
  
- **Week 2, Activity 2.1:** Design Your Schema
  - `CanonicalUser`, `CanonicalActivity`, `CanonicalPermissionChange`
  - Complete schema design with field names, types, validation rules
  
- **Week 2, Activity 2.3:** Validation Rules
  - `is_valid_user()`, `is_valid_activity()` concepts
  - Schema validation

**Key Classes:**
- `CanonicalUser` - Week 1, Core Concepts #1; Week 2, Activity 2.1
- `CanonicalActivity` - Week 0, Core Concepts #1 (lens interpretation); Week 2, Activity 2.1
- `CanonicalPermissionChange` - Week 0, Core Concepts #3 (Privileges = Skills); Week 2, Activity 2.1; Week 3, Core Concepts #2
- `ColumnMapper` - Week 1, Core Concepts #3
- `IngestionPipeline` - Week 1 & 2 integration

---

## mvp_extractors.py

**Primary Curriculum Mapping:**
- **Week 0, Core Concepts #2:** The Three Questions
  - TRIBE: "Who is connected to whom?" → Network graph
  - TEACHER: "Who is growing in what ways?" → Learning pathways
  - RECON: "Who is providing value ethically?" → Provider scores
  
- **Week 0, Core Concepts #3:** Privileges = Skills
  - Permission upgrades = skill demonstrations
  - Used in `TeacherMVPExtractor.extract_progressions()`
  
- **Week 2, Core Concepts #2:** Graph Structures
  - TRIBE graphs: nodes, edges, weights
  - Used in `TribeMVPExtractor.build_graph()`
  
- **Week 3, Activity 3.1:** Implement Collaboration Strength
  - `TribeMVPExtractor.build_graph()` implements collaboration algorithm
  - Factors: direct interactions, co-resource access, shared groups
  
- **Week 3, Activity 3.2:** Build Role Mastery Profiler
  - `TeacherMVPExtractor` implements `role_mastery_profile()` concept
  - Builds skill profiles from permission history
  
- **Week 3, Activity 3.3:** Create Provider Scorer
  - `ReconMVPExtractor.score_providers()` implements provider scoring
  - Returns reliability, adoption, composite scores, letter grades
  
- **Week 3, Core Concepts #4:** Efficiency Matters
  - Graph building: O(n²) naive → O(n log n) optimized
  
- **Week 4+, Module 4A:** TRIBE Deep Dive
  - Community detection, bridge finder, mentor identifier
  
- **Week 4+, Module 4B:** TEACHER Deep Dive
  - Role-skill matrix, learning path generator
  
- **Week 4+, Module 4C:** RECON Deep Dive
  - Provider profiler, value flow mapper, ethics scorer

**Key Classes:**
- `TribeMVPExtractor` - Week 0, #2; Week 2, #2; Week 3, Activity 3.1; Week 4+, Module 4A
- `TeacherMVPExtractor` - Week 0, #2 & #3; Week 3, Activity 3.2; Week 4+, Module 4B
- `ReconMVPExtractor` - Week 0, #2; Week 3, Activity 3.3; Week 4+, Module 4C

---

## pipeline.py

**Primary Curriculum Mapping:**
- **Week 4+:** Domains - Applied Systems
  - Integrates all three lenses: TRIBE, TEACHER, RECON
  - Complete end-to-end pipeline
  
- **Capstone:** Real World Application
  - Theme: "Prove It Works"
  - Runs complete pipeline on real dataset
  - Produces all required outputs:
    - Governance Report
    - TRIBE Output (network, communities, bridges, mentors)
    - TEACHER Output (role-skill matrix, recommendations, gaps)
    - RECON Output (provider scores, value flows, friction points)

**Key Functions:**
- `run_complete_pipeline()` - Capstone implementation
- `generate_network_json()` - Week 4+, Module 4A (network visualization)
- `generate_dashboard_summary()` - Week 9 (Flask dashboard integration)

---

## Complete Learning Journey

### Week 0: Concepts
- **governance.py:** `PIIHandler`, `GovernanceGate`, `PROHIBITED_INFERENCES`, `BIAS_GUARDRAILS`
- **ingestion.py:** `CanonicalActivity` (lens interpretation concept)

### Week 1: Fundamentals
- **governance.py:** `ColumnDefinition`, `SensitivityLevel` (data dictionary)
- **ingestion.py:** `CanonicalUser`, `CanonicalCompany`, etc. (canonical entities)
- **ingestion.py:** `ColumnMapper` (schema detection)

### Week 2: Data Structures
- **ingestion.py:** All `Canonical*` dataclasses (schema design)
- **mvp_extractors.py:** Graph structure concepts (TRIBE graphs)

### Week 3: Algorithms
- **mvp_extractors.py:** `TribeMVPExtractor.build_graph()` (collaboration strength)
- **mvp_extractors.py:** `TeacherMVPExtractor.extract_progressions()` (role mastery)
- **mvp_extractors.py:** `ReconMVPExtractor.score_providers()` (provider scoring)

### Week 4+: Domains
- **mvp_extractors.py:** Complete extractors (TRIBE/TEACHER/RECON deep dives)
- **pipeline.py:** System integration

### Capstone
- **pipeline.py:** `run_complete_pipeline()` - complete system

---

## How to Use This Map

1. **When learning a concept:** Find the curriculum week/activity, then look at the corresponding code
2. **When reading code:** Check the inline documentation for curriculum references
3. **When building projects:** Use the code as reference implementations for curriculum activities

---

## Quick Reference

| Curriculum Week | Key Code Files | Key Concepts |
|----------------|----------------|--------------|
| Week 0 | `governance.py` | PII, bias guardrails, ethical principles |
| Week 1 | `governance.py`, `ingestion.py` | Data dictionary, canonical entities, schema detection |
| Week 2 | `ingestion.py` | Schema design, validation, graph structures |
| Week 3 | `mvp_extractors.py` | Algorithms: collaboration, mastery, scoring |
| Week 4+ | `mvp_extractors.py`, `pipeline.py` | Complete systems, integration |
| Capstone | `pipeline.py` | End-to-end pipeline |

---

## security.py

**Primary Curriculum Mapping:**
- **Week 10: Security & Trust Fabric**
  - Content validation (no implicit execution)
  - Secret management (API keys, tokens)
  - Supply chain security (SBOM, signatures)
  - Access control (blast radius controls)
  - API connector security (least privilege)

**Key Classes:**
- `ContentValidationResult` - Week 10, Content Validation
- `SecretManager` - Week 10, Secure API Key Management
- `AIConnector` - Week 10, Least Privilege API Design
- `AccessController` - Week 0, Activity 0.3; Week 10, Blast Radius Controls
- `SBOMEntry` - Week 10, Supply Chain Security

**Key Functions:**
- `validate_content_package()` - Week 10, Prevents content-to-execution (Finding 2, 440782380)
- `generate_sbom()` - Week 10, Supply chain integrity
- `validate_dependency()` - Week 10, Dependency security

**Security Requirements Addressed:**
- ✅ No implicit execution from content (Finding 2, 440782380)
- ✅ Secrets hardening (Finding 3, 440782380)
- ✅ Permissioned AI connectors (Finding 2, 440782380)
- ✅ Supply chain integrity
- ✅ Blast radius controls (Finding 1, 440782380)

**See:** `SECURITY_IMPLEMENTATION_STATUS.md` for complete implementation details

---

*This mapping ensures learners can connect theoretical concepts from the curriculum with practical code implementations.*
