# COSURVIVAL: Connected Intelligence Network

> *Transforming activity data into the three pillars of ethical collaboration*

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.9+](https://img.shields.io/badge/python-3.9+-blue.svg)](https://www.python.org/downloads/)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)

**COSURVIVAL** is an open-source ecosystem for building ethical, governance-first intelligence networks. It transforms activity data into three interconnected systems: **TRIBE** (social networks), **TEACHER** (adaptive learning), and **RECONSUMERALIZATION** (ethical commerce).

---

## 📋 Table of Contents

- [Quick Start](#-quick-start)
- [Core Concepts](#-core-concepts)
- [Architecture](#-architecture)
- [Contributing](#-contributing)
- [Documentation](#-documentation)
- [License](#-license)

---

Quick setup and SBOM steps: see `docs/START_HERE.md`.

**Quick links**
- 🧭 Architecture: `PROJECT_STRUCTURE.md`
- 🚀 Run pipeline: `pipeline.py` (full) / `extractors/rapid_pipeline.py` (rapid)
- 🛡️ Governance: `governance.py` + `SECURITY_APPLIED.md`
- 🎯 Review system: `cosurvival/tracking/review_system.py` + `curriculum/REVIEW_SYSTEM_GUIDE.md`
- 🎓 Teaching agents: `cosurvival/teaching/` + `SHADOW_STUDENT_MODE_ARCHITECTURE.md`
- 📈 Analysis plan: `BRIAN_DATA_ANALYSIS_PLAN.md`
- 📜 Thesis & PRD map: `curriculum/vision/TEACHER_THESIS_INDEX.md` + `curriculum/guides/TEACHER_THESIS_PRD_MAP.md`
- 🗂️ Unified PRD: `PRD_UNIFIED_ECOSYSTEM.md`
- ✅ Ethics bundle: `ethics/TEACHER_ETHICAL_GUARDRAILS.md`, `ethics/ETHICAL_CHECKLIST.md`, `ethics/ETHICS_INTEGRATION_SUMMARY.md`, `ethics/MODEL_WELFARE_AND_INTERACTION_NORMS.md`, `curriculum/vision/appendices/C_MAS_CHECKLIST.md`, `curriculum/vision/appendices/A_NON_NEGOTIABLES.md`
- 📚 Case studies: `CASE_STUDIES_INDEX.md` (JLR, A-SWE) + `CASE_STUDY_INTEGRATION_PROCESS.md`

---

## Start Here (2-minute orientation)
1) **If you’re new:** Read `curriculum/vision/TEACHER_THESIS_EXEC_SUMMARY.md` (1-page)  
2) **To run the system:** `python pipeline.py sample.csv ./output` → open `output/dashboard.html`  
3) **To see code-to-curriculum:** `curriculum/guides/TEACHER_THESIS_PRD_MAP.md`  
4) **For security posture:** `SECURITY_APPLIED.md` and `governance.py`  
5) **For teaching agents (SSM):** `SHADOW_STUDENT_MODE_ARCHITECTURE.md` + `cosurvival/teaching/`

## 🌐 TRIBE | 📚 TEACHER | 💱 RECONSUMERALIZATION

This system processes activity/audit log data to build an interconnected intelligence network across three integrated systems.

**⚠️ GOVERNANCE-FIRST ARCHITECTURE**: Nothing proceeds without passing privacy, bias, and ethics checks.

---

## 📐 Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                    COSURVIVAL PIPELINE                          │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  ┌──────────────┐    ┌──────────────┐    ┌──────────────┐      │
│  │  GOVERNANCE  │───▶│  INGESTION   │───▶│     MVP      │      │
│  │    GATE      │    │   PIPELINE   │    │  EXTRACTORS  │      │
│  └──────────────┘    └──────────────┘    └──────────────┘      │
│        │                    │                    │              │
│        ▼                    ▼                    ▼              │
│  ┌──────────────┐    ┌──────────────┐    ┌──────────────┐      │
│  │ • PII Check  │    │ • Schema Map │    │ • TRIBE      │      │
│  │ • Bias Guard │    │ • Normalize  │    │ • TEACHER    │      │
│  │ • Scope Stmt │    │ • Clean Data │    │ • RECON      │      │
│  │ • Review Trg │    │ • Canonical  │    │ • Insights   │      │
│  └──────────────┘    └──────────────┘    └──────────────┘      │
│                                                                 │
│                    ┌──────────────────┐                        │
│                    │ UNIFIED OUTPUT   │                        │
│                    │ cosurvival_mvp   │                        │
│                    │     .json        │                        │
│                    └──────────────────┘                        │
│                             │                                   │
│                             ▼                                   │
│                    ┌──────────────────┐                        │
│                    │    DASHBOARD     │                        │
│                    │   (D3.js viz)    │                        │
│                    └──────────────────┘                        │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

---

## 🚀 Quick Start

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

### 1b. Configure Secret Key

All Flask sessions are now backed by the secret manager. Set `COSURVIVAL_SECRET_KEY`
before launching the app:

```bash
# macOS/Linux
export COSURVIVAL_SECRET_KEY="replace-with-strong-secret"

# Windows (PowerShell)
$env:COSURVIVAL_SECRET_KEY = "replace-with-strong-secret"
```

### 2. Run the Complete Pipeline

```bash
python pipeline.py path/to/activity_data.csv ./output
```

This runs the full governance-gated pipeline:
1. ✓ Governance checks (PII, bias, prohibited inferences)
2. ✓ Schema detection and data normalization  
3. ✓ Canonical entity extraction
4. ✓ MVP outputs for all three systems
5. ✓ Unified JSON for dashboard

> ⚠️ Legacy helpers like `csv_data_processor.py` and `extractors/rapid_pipeline.py`
> now enforce the same governance + lens-boundary audits. They will halt with
> actionable errors if a dataset cannot clear the gate.

### 3. Launch the Dashboard

```bash
cd output
python -m http.server 8000
```

Then open: **http://localhost:8000/dashboard.html**

---

## 🔒 Governance Framework

### What We Check

| Check | Purpose |
|-------|---------|
| **PII Detection** | Identifies columns requiring hashing (names, emails, UIDs) |
| **Bias Guardrails** | Ensures outputs don't misinterpret activity as performance |
| **Prohibited Inferences** | Blocks individual performance/discipline predictions |
| **Quasi-ID Combinations** | Warns when column combinations could identify individuals |
| **Data Quality** | Flags high-null columns and inconsistent data |

### What We Will NOT Infer

❌ Individual employee performance scores  
❌ Disciplinary action recommendations  
❌ Termination risk predictions  
❌ Political or religious affiliations  
❌ Psychological profiling  
❌ Surveillance-based productivity metrics  

### Bias Guardrails

| Pattern | Warning |
|---------|---------|
| High activity | ≠ high value or performance (may reflect role requirements) |
| Low activity | ≠ low contribution (may indicate deep focus work) |
| Collaboration score | Compare within role cohorts only |
| Skill gaps | Frame as growth opportunities, not deficiencies |

---

## 📊 Expected Data Format

The processor auto-detects columns matching common patterns:

### Entity Columns
| Pattern | Examples | Purpose |
|---------|----------|---------|
| `uid`, `userid` | Uid, UserId, UserIdentifier | User identifier |
| `name`, `username` | Name, DisplayName, FullName | User name |
| `email` | Email, Mail, EmailAddress | User email |
| `companyid` | CompanyId, OrgId, OrganizationId | Company identifier |
| `companyname` | CompanyName, OrgName | Company name |
| `groupid` | GroupId, TeamId | Group identifier |
| `groupname` | GroupName, TeamName | Group name |

### Provider Columns
| Pattern | Examples | Purpose |
|---------|----------|---------|
| `pid`, `providerid` | Pid, ProviderId, ServiceId | Provider identifier |
| `providername` | ProviderName, ServiceName | Provider name |
| `scheme` | Scheme, Protocol, Method | Service type |

### Activity Columns
| Pattern | Examples | Purpose |
|---------|----------|---------|
| `type`, `activitytype` | Type, ActivityType, Action | Activity type |
| `date`, `timestamp` | Date, Timestamp, DateTime | Activity time |
| `stateold` | StateOld, PreviousState | Before state |
| `statenew` | StateNew, NewState | After state |
| `codeerror` | CodeError, Error, ErrorCode | Error codes |

### Relationship Columns
| Pattern | Examples | Purpose |
|---------|----------|---------|
| `uidopp` | UidOpp, OpposingUser, TargetUser | Other user in interaction |
| `uidreq` | UidReq, RequestingUser, Initiator | Requesting user |
| `roleid` | RoleId, Role_Id | Role identifier |
| `privilege` | Privilege, Privileges, Permission | Access levels |

---

## 🔄 The Feedback Loop

```
User joins TRIBE
      ↓
Assigned role based on company/group
      ↓
TEACHER creates personalized curriculum
      ↓
User learns about providers in their tech stack
      ↓
User evaluates providers on RECONSUMERALIZATION
      ↓
Ratings influence what TRIBE adopts
      ↓
New adoptions create new learning needs
      ↓
TEACHER adapts curriculum
      ↓
    CYCLE CONTINUES
```

---

## ⚖️ Triple Balance Governance

Every decision is evaluated through three perspectives:

### 🧠 AI Logic
Data-driven analysis of patterns, metrics, and trends

### 🔟 10th Man
Mandatory dissent - challenging assumptions and identifying blind spots

### 🔮 Witch
Intuitive pattern recognition beyond what data shows

---

## 📁 File Structure

```
teacher/
├── pipeline.py              # 🚀 MAIN ENTRY POINT - runs everything
├── governance.py            # Data governance and PII handling
├── ingestion.py             # Schema-first data normalization
├── mvp_extractors.py        # TRIBE, TEACHER, RECON extractors
├── models.py                # Core data models (dataclasses)
├── csv_data_processor.py    # Legacy processor (still works)
├── dashboard.html           # Interactive visualization dashboard
├── requirements.txt         # Python dependencies
├── README.md               # This file
│
└── [Generated Files]
    ├── governance_report.json    # Safety check results
    ├── data_dictionary.md        # Column classifications
    ├── events_clean.jsonl        # Normalized activity data
    ├── cosurvival_mvp.json       # Complete MVP outputs
    ├── tribe_network.json        # D3.js network graph
    ├── dashboard_summary.json    # Dashboard-optimized data
    └── pipeline_results.json     # Pipeline execution summary
```

---

## 🎯 MVP Outputs

### TRIBE MVP (Social Network)
- **Communities**: Connected user groups with cohesion scores
- **Cross-silo bridges**: Users connecting different communities
- **Mentor candidates**: Based on network position (NOT performance)
- **Collaboration patterns**: Company and group level (aggregated)

### TEACHER MVP (Learning Pathways)  
- **Role × Privilege ladder**: Skills associated with each role
- **Skill progressions**: Common state transitions tracked
- **Learning recommendations**: "Next likely skills" from peer comparison
- **Organization gaps**: Missing skills at company level

### RECONSUMERALIZATION MVP (Value Exchange)
- **Provider scores**: Adoption × Reliability × Transparency
- **Ethics grades**: A-F ratings with methodology notes
- **Value flows**: Provider → Company volume and quality
- **Friction points**: Low-quality or low-engagement relationships

---

## 🔧 API Usage (Programmatic)

```python
from csv_data_processor import CosurvivalDataProcessor

# Initialize processor
processor = CosurvivalDataProcessor('activity_data.csv')

# Load and process all data
data = processor.process_all()

# Access specific systems
tribe_data = data['tribe']
teacher_data = data['teacher']
recon_data = data['reconsumeralization']

# Export for visualization
processor.export_json('output.json')
processor.export_network_graph('network.json')
```

---

## 🎯 Use Cases

### For Organizations
- Map collaboration patterns across teams
- Identify skill gaps and training needs
- Evaluate vendor/provider relationships
- Track ethical compliance

### For Educators
- Generate role-based curricula
- Match mentors with learners
- Track learning progressions
- Personalize recommendations

### For Ethical Commerce
- Rate provider transparency
- Track value exchange quality
- Measure sustainability scores
- Enable informed decisions

---

## 🌟 Vision

This is not just software. It's infrastructure for a new kind of economy - one where:

- **Networks are visible** (TRIBE)
- **Learning is continuous** (TEACHER)  
- **Value exchange is ethical** (RECONSUMERALIZATION)

Together, these systems create the foundation for **Cosurvival** - the realization that in a connected world, we either thrive together or fail apart.

---

## 🤝 Contributing

We welcome contributions! Please see our [Contributing Guide](CONTRIBUTING.md) for details.

- 📖 [Code of Conduct](CODE_OF_CONDUCT.md)
- 🔒 [Security Policy](SECURITY.md)
- 📝 [Contributing Guidelines](CONTRIBUTING.md)
- 📋 [Changelog](CHANGELOG.md)

### Quick Contribution Steps

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Make your changes
4. Run tests (`pytest`)
5. Commit your changes (`git commit -m 'Add amazing feature'`)
6. Push to the branch (`git push origin feature/amazing-feature`)
7. Open a Pull Request

## 📚 Documentation

- 🧭 [Project Structure](PROJECT_STRUCTURE.md)
- 🎓 [TEACHER Thesis](curriculum/vision/TEACHER_THESIS_EXEC_SUMMARY.md)
- 🛡️ [Security Applied](SECURITY_APPLIED.md)
- 📖 [Unified PRD](PRD_UNIFIED_ECOSYSTEM.md)
- 🔬 [Research Integration](RESEARCH_INTEGRATION_SUMMARY.md)

## 📜 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

**Use freely, attribute kindly, contribute openly.**

---

## 🌟 Acknowledgments

COSURVIVAL is built on the principle of **Mutually Assured Success (MAS)** - we either thrive together or fail apart. Thank you to all contributors, researchers, and community members who make this possible.

*Built with intention. Designed for impact. Ready for deployment.*

