# COSURVIVAL Project Structure

## Overview

This document provides a complete overview of the COSURVIVAL project structure, organized by purpose and function.

---

## Root Directory

### Core Application Files
- `advisor.py` - Base CosurvivalAdvisor (cross-domain pattern recognition)
- `teacher_advisor.py` - TEACHER-certified AI advisor
- `app.py` - Flask web application
- `database.py` - Database utilities and SQL operations
- `pipeline.py` - Complete data processing pipeline
- `test_pipeline.py` - Pipeline testing script

### Core Data & Governance
- `models.py` - Data models for TRIBE, TEACHER, RECON
- `governance.py` - Data governance, PII handling, bias guardrails
- `ingestion.py` - Schema-first data ingestion and normalization
- `mvp_extractors.py` - MVP extraction for TRIBE/TEACHER/RECON

### Security & Privacy
- `security.py` - Security utilities (hashing, validation, rate limiting)
- `lens_boundary.py` - Lens boundary contracts
- `lensgrind.py` - Privacy and scope auditor

### Learning & Tracking
- `progression_tracker.py` - CS50-inspired self-relative learning tracking
- `structures.py` - Data structures (Queue, Stack, Tree, Hash Table, Trie)

### Data Processing
- `csv_data_processor.py` - Legacy CSV processor
- `dashboard.html` - Interactive D3.js visualization dashboard
- `scratch_for_data.html` - Visual pipeline builder UI

### Documentation
- `README.md` - Project overview and usage
- `requirements.txt` - Python dependencies
- `ADVISOR_VISION.md` - AI advisor vision documentation
- `APPLIED_LESSONS.md` - Applied CS50 lessons summary
- `ORGANIZATION_SUMMARY.md` - Codebase organization summary
- `RESEARCH_INTEGRATION_SUMMARY.md` - Research integration guide
- `SECURITY_APPLIED.md` - Security implementation documentation
- `SECURITY_IMPLEMENTATION_COMPLETE.md` - Security completion status
- `STRATEGIC_CONTEXT_MUSK_INSIGHTS.md` - Strategic positioning
- `TEACHER_ADVISOR_COMPLETE.md` - TEACHER advisor documentation
- `VISION_ALIGNMENT.md` - Vision alignment documentation

### Research & Content
- `research_library_schema.py` - Research Library database schema

---

## Package Structure

### `cosurvival/` - Main Package

**Purpose:** Organized package structure for core COSURVIVAL functionality

#### `cosurvival/__init__.py`
- Main package exports
- Version information
- Re-exports from subpackages

#### `cosurvival/core/` - Core Components
**Purpose:** Foundational data models, governance, and ingestion

- `__init__.py` - Exports from root-level modules:
  - `models.py` - Data models
  - `governance.py` - Governance framework
  - `ingestion.py` - Data ingestion

**Root-level modules (imported by package):**
- `models.py` - TRIBE, TEACHER, RECON data models
- `governance.py` - PII handling, bias guardrails, Triple Balance
- `ingestion.py` - Canonical entity creation, schema validation

#### `cosurvival/advisors/` - AI Advisors
**Purpose:** AI advisor implementations

- `__init__.py` - Exports advisor classes

**Root-level modules (imported by package):**
- `advisor.py` - Base CosurvivalAdvisor
- `teacher_advisor.py` - TEACHER-certified advisor

#### `cosurvival/tracking/` - Learning Tracking
**Purpose:** Learning progression and certification tracking

- `__init__.py` - Exports tracking components
- `review_system.py` - Multi-factor review system

**Root-level modules (imported by package):**
- `progression_tracker.py` - Self-relative learning tracking

#### `cosurvival/teaching/` - Teaching Agents
**Purpose:** Shadow Student Mode agents for assignment understanding

- `__init__.py` - Exports teaching components
- `context_modes.py` - Assignment context modes (Practice/Study/Graded) with:
  - Policy enforcement (`can_perform`, `requires_time_guard`)
  - Academic integrity helpers (`register_student_attempt`, tool whitelisting)

**Future modules (to be implemented):**
- `learning_trace.py` - Learning trace data models
- `shadow_student.py` - Student-Sim Agent
- `tutor_agent.py` - Tutor Agent
- `validator_agent.py` - Validator/Assessor Agent
- `integrity_guardrails.py` - Academic integrity rules

#### `cosurvival/governance_tools/` - Governance Tools
**Purpose:** Privacy and scope enforcement tools

- `__init__.py` - Exports governance tools

**Root-level modules (imported by package):**
- `lens_boundary.py` - Lens boundary contracts
- `lensgrind.py` - Privacy auditor

---

## Extractors Package

### `extractors/` - Rapid Pipeline

**Purpose:** Fast Python-based extraction for TRIBE/TEACHER/RECON

- `__init__.py` - Package exports
- `ingest.py` - Fast CSV ingestion
- `tribe_graph.py` - TRIBE graph analysis
- `teacher_paths.py` - TEACHER learning path extraction
- `recon_scores.py` - RECON provider scoring
- `export_json.py` - JSON export utilities
- `rapid_pipeline.py` - Complete rapid pipeline orchestration

---

## Curriculum Package

### `curriculum/` - TEACHER Curriculum & Documentation

**Purpose:** Complete TEACHER curriculum, security documentation, and research

#### Core Curriculum
- `TEACHER_CORE_TRACK.md` - Complete curriculum structure
- `TEACHER_WEEK0.md` through `TEACHER_WEEK10.md` - Individual week modules
- `TEACHER_WEEK_AI.md` - AI module
- `week1_problem_sets.md` through `week10_problem_sets.md` - Problem sets
- `week_ai_problem_sets.md` - AI problem sets

#### Security Documentation
- `SECURITY_CONTROLS_CHECKLIST.md` - Security checklist
- `SECURITY_IMPLEMENTATION_STATUS.md` - Implementation status
- `SECURITY_INTEGRATION_SUMMARY.md` - Security integration guide
- `SECURITY_TRUST_FABRIC.md` - Trust fabric documentation
- `SECURITY_VULNERABILITY_RESPONSE.md` - Vulnerability response plan
- `API_KEY_SECURITY_CRITICAL.md` - API key security guide

#### Ethics & Vision
- `TEACHER_ETHICAL_GUARDRAILS.md` - Ethical guidelines
- `TEACHER_FAMILY_AI_VISION.md` - Family AI vision
- `TEACHER_VISION_COMPLETE.md` - Complete vision
- `TEACHER_VISION_INTEGRATION.md` - Vision integration
- `ETHICAL_CHECKLIST.md` - Ethics checklist
- `ETHICS_INTEGRATION_SUMMARY.md` - Ethics integration

#### Research & Content
- `RESEARCH_BACKBONE_PRD.md` - PRD research section
- `CONTENT_TAXONOMY.md` - Content taxonomy mapping
- `SYNDICATION_PLAN.md` - Medium paper syndication plan

#### Implementation Guides
- `CODE_TO_CURRICULUM_MAP.md` - Code-to-curriculum mapping
- `CS50_CONCEPTS_APPLIED.md` - CS50 concepts applied
- `FAMILY_COSURVIVAL_IMPLEMENTATION.md` - Family implementation
- `AI_VISION_INTEGRATION_SUMMARY.md` - AI vision integration

#### Demos & Scripts
- `hello_world_demo.py` - Three-lens interpretation demo
- `pipeline_demo.py` - 4-stage governance pipeline demo
- `extractors_demo.py` - MVP extractors demo
- `INVESTOR_DEMO_SCRIPT.md` - Investor demo script

---

## Tests Directory

### `tests/` - Test Suite

- `test_security.py` - Security module tests
- `test_governance_severity.py` - Governance severity tests
- `test_integration_security.py` - Security integration tests

---

## Cache Directories (Generated)

- `__pycache__/` - Python bytecode cache
- `.mypy_cache/` - MyPy type checking cache
- `cosurvival/__pycache__/` - Package bytecode cache
- `cosurvival/*/__pycache__/` - Subpackage caches
- `extractors/__pycache__/` - Extractors cache

**Note:** These should be in `.gitignore`

---

## File Organization Principles

### 1. Root-Level Core Modules
Core functionality remains at root for backward compatibility:
- `models.py`, `governance.py`, `ingestion.py`
- `advisor.py`, `teacher_advisor.py`
- `progression_tracker.py`
- `security.py`, `structures.py`

### 2. Package Structure
Organized packages for clean imports:
- `cosurvival/` - Main package with subpackages
- `extractors/` - Rapid pipeline extractors
- `curriculum/` - All curriculum and documentation

### 3. Documentation
Comprehensive documentation at multiple levels:
- Root-level: Vision, strategy, implementation guides
- Curriculum: Week-by-week modules, problem sets, security docs
- Code-level: Inline documentation and curriculum mappings

### 4. Tests
Separate test directory with focused test files

---

## Import Patterns

### From Root-Level Modules
```python
from models import TribeUser, TeacherSkill
from governance import PIIHandler, GovernanceGate
from advisor import CosurvivalAdvisor
```

### From Packages
```python
from cosurvival.core import TribeUser, PIIHandler
from cosurvival.advisors import CosurvivalAdvisor, TEACHERAdvisor
from extractors import ingest_csv, build_tribe_graph
```

### Both Work (Backward Compatible)
The package structure re-exports from root-level modules, so both import styles work.

---

## Key Directories Summary

| Directory | Purpose | Key Files |
|-----------|---------|-----------|
| **Root** | Core application | `advisor.py`, `governance.py`, `pipeline.py` |
| **cosurvival/** | Organized package | `__init__.py`, subpackages |
| **extractors/** | Rapid pipeline | `ingest.py`, `rapid_pipeline.py` |
| **curriculum/** | TEACHER curriculum | Week modules, problem sets, security docs |
| **tests/** | Test suite | Security, governance, integration tests |

---

## Development Workflow

### Adding New Features
1. **Core functionality** → Root-level module (e.g., `new_feature.py`)
2. **Package integration** → Add to appropriate `cosurvival/*/__init__.py`
3. **Documentation** → Add to `curriculum/` if curriculum-related
4. **Tests** → Add to `tests/`

### Adding New Curriculum
1. **Week module** → `curriculum/core/TEACHER_WEEK*.md`
2. **Problem sets** → `curriculum/core/week*_problem_sets.md`
3. **Code mapping** → Update `curriculum/guides/CODE_TO_CURRICULUM_MAP.md`

### Adding Research Papers
1. **Schema** → Use `research_library_schema.py`
2. **Taxonomy** → Update `curriculum/CONTENT_TAXONOMY.md`
3. **PRD** → Update `curriculum/RESEARCH_BACKBONE_PRD.md`

---

*This structure supports both rapid development (extractors/) and formal core (cosurvival/), maintaining backward compatibility while enabling clean organization.*

