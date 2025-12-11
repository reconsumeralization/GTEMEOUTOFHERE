# TEACHER Week 6: The Productivity Layer

> *"Week 6 is where Cosurvival becomes shippable: the same truth-models, now expressed in a language fast enough for real-world iteration."*

---

## Module Overview

**Duration:** 8-10 hours  
**Prerequisites:** Week 5 (Structures of Fairness)  
**Next:** Capstone (Real-World Application)

This week, learners discover that **Python is the productivity layer** that makes COSURVIVAL shippable. Just as CS50 Week 6 shows how Python lets you solve the same problems with less pain, TEACHER Week 6 shows how Python lets you ship the same truth-models with real-world speed.

---

## Learning Outcomes

By the end of this week, learners will be able to:

1. **Explain** the two-speed development doctrine (core vs edge)
2. **Build** Python MVP extractors for TRIBE/TEACHER/RECON
3. **Understand** how abstraction enables safe human building
4. **Use** Python's built-in structures for rapid development
5. **Handle** exceptions compassionately (robust UX)
6. **Ship** a complete pipeline from CSV to three JSON views

---

## Core Concept: Two-Speed Development

### CS50's Insight

> "C taught you how computers *really* work. Python lets you solve the *same problems* with less pain."

### TEACHER's Insight

> "Weeks 0-5 gave you the **truth-layer** (data models, governance, structures).  
> Week 6 gives you the **delivery-layer** (rapid pipelines, prototypes, iteration)."

---

## The Architecture: Canon + Rapid Layer

```
┌─────────────────────────────────────────────────────────┐
│                    CANON (C-Mindset)                    │
│  Formal, Audited, Deterministic Core                    │
├─────────────────────────────────────────────────────────┤
│  • models.py          (canonical schemas)               │
│  • governance.py      (trust calculations)               │
│  • lens_boundary.py   (invariant contracts)             │
│  • structures.py      (fair data structures)            │
└─────────────────────────────────────────────────────────┘
                        ↓
┌─────────────────────────────────────────────────────────┐
│              RAPID LAYER (Python-Mindset)                │
│  Fast Iteration, Experimental, Human-Buildable          │
├─────────────────────────────────────────────────────────┤
│  • ingest.py          (CSV → entities)                 │
│  • tribe_graph.py     (network analysis)                │
│  • teacher_paths.py   (learning pathways)               │
│  • recon_scores.py    (provider evaluation)             │
│  • export_json.py     (dashboard-ready outputs)         │
└─────────────────────────────────────────────────────────┘
```

**The Rule:**
> **Core must be slow, formal, audited.  
> Edge can be fast, Pythonic, experimental.**

This prevents "fast MVP" from corrupting your truth-layer.

---

## Python's Gifts to TEACHER

### 1. Abstraction is Governance Ally

Python's biggest gift isn't syntax. It's **safe abstraction**.

**In COSURVIVAL terms:**
> "People can create value without being able to leak PII."

**Example:**
```python
# High-level, safe abstraction
def extract_tribe(activities):
    """Extract TRIBE insights - PII already handled by core."""
    # User doesn't need to know about hashing, boundaries, etc.
    # They just work with safe data
    graph = build_graph(activities)
    communities = detect_communities(graph)
    return {"communities": communities, "graph": graph}
```

The dangerous gears (PII hashing, boundary enforcement) are in the core.  
The productive layer (extractors, analytics) is Python.

---

### 2. Built-in Data Structures = Acceleration

**Python gives you Week 5 for free.**

| Python Built-in | Week 5 Equivalent | TEACHER Use Case |
|-----------------|-------------------|-----------------|
| `dict` | Hash table | `role_id → required_skills` lookup |
| `list` | Dynamic array | Activity collections |
| `set` | Fast membership | Skill sets, user groups |
| `tuple` | Immutable snapshot | State transitions |

**Example:**
```python
# Fast, built-in hash table
role_skills = {
    "data_engineer": {"Python", "SQL", "ETL", "Cloud"},
    "product_manager": {"Strategy", "Agile", "Analytics"},
    "full_stack": {"React", "Node.js", "TypeScript"}
}

# Fast lookup - O(1)
skills_needed = role_skills.get("data_engineer", set())

# Fast set operations
user_skills = {"Python", "SQL"}
missing = skills_needed - user_skills  # Set difference
```

**No custom hash table needed. Just use `dict`.**

---

### 3. Exceptions = Compassionate Design

**C:** You check error codes  
**Python:** You handle exceptions explicitly

**TEACHER meaning:**
You can formalize:
- "We expect failure"
- "We recover safely"
- "We don't punish users for bad input"

**Example:**
```python
def generate_recommendation(user_id: str) -> Dict:
    """Generate learning recommendation with graceful failure."""
    try:
        user = get_user(user_id)
        if not user:
            return {"error": "User not found", "recommendations": []}
        
        skills = get_user_skills(user_id)
        role = get_user_role(user_id)
        required = get_role_requirements(role)
        
        missing = required - skills
        return {
            "user_id": user_id,
            "recommendations": list(missing)[:3],
            "reason": "Skill gap analysis"
        }
    
    except KeyError as e:
        # Missing data - not user's fault
        return {"error": "Incomplete profile", "recommendations": []}
    
    except Exception as e:
        # Unexpected error - log but don't crash
        log_error(f"Recommendation failed for {user_id}: {e}")
        return {"error": "Unable to generate", "recommendations": []}
```

**Compassionate UX:** System doesn't crash on bad input. It recovers gracefully.

---

### 4. Libraries = Ecosystem Integration

Python's library ecosystem enables:
- **Pandas:** CSV processing
- **NetworkX:** Graph analysis
- **JSON:** Data serialization
- **FastAPI:** API layer (future)

**Example:**
```python
import pandas as pd
import networkx as nx

# Pandas: CSV → DataFrame (one line)
df = pd.read_csv("activity_log.csv")

# NetworkX: Build graph (one line)
G = nx.Graph()
G.add_edges_from([(u, v) for u, v in zip(df['user_id'], df['target_user_id'])])

# Detect communities (one line)
communities = nx.community.greedy_modularity_communities(G)
```

**Productivity:** What took 1000 lines in C takes 10 lines in Python.

---

## The Python MVP Extractor Pack

This is where Week 6 becomes **real shipping code**.

### Module Structure

```
teacher/
├── core/                    # Canon (formal, audited)
│   ├── models.py
│   ├── governance.py
│   ├── lens_boundary.py
│   └── structures.py
│
└── extractors/              # Rapid Layer (Python, fast)
    ├── ingest.py           # CSV → entities
    ├── normalize.py        # Clean data
    ├── tribe_graph.py      # Network analysis
    ├── teacher_paths.py    # Learning pathways
    ├── recon_scores.py     # Provider evaluation
    └── export_json.py      # Dashboard outputs
```

---

### 1. `ingest.py` - CSV to Entities

```python
"""
Rapid CSV ingestion using Pandas.
"""
import pandas as pd
from core.models import CanonicalActivity, CanonicalUser

def ingest_csv(filepath: str) -> pd.DataFrame:
    """Load CSV - Python makes this trivial."""
    return pd.read_csv(filepath, encoding='utf-8')

def extract_entities(df: pd.DataFrame):
    """Extract entities - fast Python iteration."""
    activities = []
    users = {}
    
    for _, row in df.iterrows():
        # Fast dict operations
        user_id = hash_pii(row.get('Uid', ''))
        if user_id not in users:
            users[user_id] = CanonicalUser(
                id=user_id,
                company_id=row.get('CompanyId', '')
            )
        
        activities.append(CanonicalActivity(
            id=f"act_{len(activities)}",
            user_id=user_id,
            activity_type=row.get('Type', ''),
            timestamp=row.get('Date', '')
        ))
    
    return users, activities
```

**Productivity:** 20 lines vs 200 lines in C.

---

### 2. `tribe_graph.py` - Network Analysis

```python
"""
TRIBE network analysis using NetworkX.
"""
import networkx as nx
from collections import defaultdict

def build_tribe_graph(activities: List[CanonicalActivity]) -> nx.Graph:
    """Build collaboration graph - Python makes this easy."""
    G = nx.Graph()
    edge_weights = defaultdict(int)
    
    # Fast iteration
    for activity in activities:
        if activity.target_user_id:
            u1, u2 = activity.user_id, activity.target_user_id
            edge_weights[(u1, u2)] += 1
    
    # Add edges with weights
    for (u1, u2), weight in edge_weights.items():
        G.add_edge(u1, u2, weight=weight)
    
    return G

def extract_communities(graph: nx.Graph) -> List[List[str]]:
    """Detect communities - one library call."""
    communities = nx.community.greedy_modularity_communities(graph)
    return [list(comm) for comm in communities]

def find_mentors(graph: nx.Graph, users: Dict) -> List[Dict]:
    """Find mentor candidates - fast Python operations."""
    # Fast centrality calculation
    centrality = nx.degree_centrality(graph)
    
    # Sort by centrality (Python built-in)
    candidates = sorted(
        centrality.items(),
        key=lambda x: x[1],
        reverse=True
    )[:10]
    
    return [
        {
            "user_id": user_id,
            "centrality": score,
            "connections": graph.degree(user_id)
        }
        for user_id, score in candidates
    ]
```

**Productivity:** Library does the hard work. You focus on insights.

---

### 3. `teacher_paths.py` - Learning Pathways

```python
"""
TEACHER learning pathway generation.
"""
from collections import defaultdict

def build_role_skill_matrix(permission_changes: List) -> Dict[str, Set[str]]:
    """Build role → skills mapping - fast dict operations."""
    role_skills = defaultdict(set)
    
    for change in permission_changes:
        role = change.role_id
        skill = change.permission_type
        if role and skill:
            role_skills[role].add(skill)
    
    return dict(role_skills)

def generate_recommendations(user_id: str, 
                           user_skills: Set[str],
                           role_skills: Dict[str, Set[str]],
                           user_role: str) -> List[str]:
    """Generate recommendations - set operations."""
    required = role_skills.get(user_role, set())
    missing = required - user_skills
    return list(missing)[:3]  # Top 3

def track_progressions(permission_changes: List) -> List[Dict]:
    """Track skill progressions - list comprehensions."""
    progressions = []
    
    for change in permission_changes:
        if change.state_before != change.state_after:
            progressions.append({
                "from": change.state_before,
                "to": change.state_after,
                "user": change.user_id,
                "timestamp": change.timestamp
            })
    
    return progressions
```

**Productivity:** Set operations, list comprehensions = readable, fast code.

---

### 4. `recon_scores.py` - Provider Evaluation

```python
"""
RECON provider scoring and evaluation.
"""
from collections import defaultdict

def score_providers(activities: List[CanonicalActivity]) -> Dict[str, Dict]:
    """Score all providers - fast aggregation."""
    provider_stats = defaultdict(lambda: {"total": 0, "errors": 0})
    
    # Fast aggregation
    for activity in activities:
        if activity.provider_id:
            provider_stats[activity.provider_id]["total"] += 1
            if activity.error_code:
                provider_stats[activity.provider_id]["errors"] += 1
    
    # Calculate scores
    scores = {}
    for provider_id, stats in provider_stats.items():
        reliability = 1 - (stats["errors"] / stats["total"]) if stats["total"] > 0 else 0
        
        if reliability >= 0.99:
            grade = "A"
        elif reliability >= 0.95:
            grade = "B"
        elif reliability >= 0.90:
            grade = "C"
        else:
            grade = "F"
        
        scores[provider_id] = {
            "reliability": reliability,
            "grade": grade,
            "total_activities": stats["total"],
            "error_count": stats["errors"]
        }
    
    return scores

def identify_friction_points(activities: List[CanonicalActivity],
                            provider_scores: Dict) -> List[Dict]:
    """Identify friction points - list comprehension."""
    return [
        {
            "provider_id": pid,
            "reason": "High error rate" if score["reliability"] < 0.9 else "Low volume",
            "score": score
        }
        for pid, score in provider_scores.items()
        if score["reliability"] < 0.9 or score["total_activities"] < 10
    ]
```

**Productivity:** Dictionary comprehensions, fast aggregation = clean code.

---

### 5. `export_json.py` - Dashboard Outputs

```python
"""
Export to dashboard-ready JSON.
"""
import json
from datetime import datetime

def export_tribe_json(graph_data: Dict, communities: List, mentors: List) -> Dict:
    """Export TRIBE data to JSON."""
    return {
        "lens": "tribe",
        "generated_at": datetime.now().isoformat(),
        "network": {
            "nodes": len(graph_data.get("nodes", [])),
            "edges": len(graph_data.get("edges", []))
        },
        "communities": [
            {"id": i, "size": len(comm), "members": comm[:5]}  # Sample
            for i, comm in enumerate(communities)
        ],
        "mentor_candidates": mentors[:10]
    }

def export_teacher_json(role_skills: Dict, 
                       recommendations: List,
                       progressions: List) -> Dict:
    """Export TEACHER data to JSON."""
    return {
        "lens": "teacher",
        "generated_at": datetime.now().isoformat(),
        "role_skill_matrix": {
            role: list(skills) for role, skills in role_skills.items()
        },
        "recommendations": recommendations[:20],
        "progressions": progressions[:20]
    }

def export_recon_json(provider_scores: Dict,
                     friction_points: List) -> Dict:
    """Export RECON data to JSON."""
    return {
        "lens": "recon",
        "generated_at": datetime.now().isoformat(),
        "provider_scores": provider_scores,
        "friction_points": friction_points,
        "top_providers": sorted(
            provider_scores.items(),
            key=lambda x: x[1]["reliability"],
            reverse=True
        )[:5]
    }

def export_unified_json(tribe: Dict, teacher: Dict, recon: Dict) -> Dict:
    """Export unified COSURVIVAL JSON."""
    return {
        "version": "1.0.0",
        "generated_at": datetime.now().isoformat(),
        "tribe": tribe,
        "teacher": teacher,
        "reconsumeralization": recon,
        "integration": {
            "insights": generate_cross_system_insights(tribe, teacher, recon)
        }
    }
```

**Productivity:** JSON serialization is built-in. One function call.

---

## The Complete Pipeline

```python
"""
Complete Python pipeline: CSV → Three JSON Views
"""
from extractors.ingest import ingest_csv, extract_entities
from extractors.tribe_graph import build_tribe_graph, extract_communities, find_mentors
from extractors.teacher_paths import build_role_skill_matrix, generate_recommendations
from extractors.recon_scores import score_providers, identify_friction_points
from extractors.export_json import export_unified_json

def run_complete_pipeline(csv_path: str) -> Dict:
    """
    Run complete pipeline: CSV → TRIBE/TEACHER/RECON JSON.
    
    This is the "ship it in a week" version.
    """
    # 1. Ingest
    df = ingest_csv(csv_path)
    users, activities = extract_entities(df)
    
    # 2. TRIBE
    graph = build_tribe_graph(activities)
    communities = extract_communities(graph)
    mentors = find_mentors(graph, users)
    tribe_json = export_tribe_json(
        {"nodes": list(graph.nodes()), "edges": list(graph.edges())},
        communities,
        mentors
    )
    
    # 3. TEACHER
    # (Would need permission_changes - simplified here)
    role_skills = build_role_skill_matrix([])  # Simplified
    teacher_json = export_teacher_json(role_skills, [], [])
    
    # 4. RECON
    provider_scores = score_providers(activities)
    friction_points = identify_friction_points(activities, provider_scores)
    recon_json = export_recon_json(provider_scores, friction_points)
    
    # 5. Unified
    unified = export_unified_json(tribe_json, teacher_json, recon_json)
    
    return unified
```

**Productivity:** 50 lines of Python = complete pipeline.

---

## Scratch-for-Data → Python Pipeline Recipes

### The Vision

**Block UI** → **Python Pipeline Recipes** → **Sandbox Execution**

```python
"""
Scratch-for-Data generates Python pipeline code.
"""
def generate_pipeline_code(blocks: List[Block]) -> str:
    """
    Convert visual blocks to Python code.
    
    Blocks:
    - CSV Upload → pd.read_csv()
    - PII Redaction → apply_pii_protection()
    - Build Graph → build_tribe_graph()
    - Extract Insights → extract_communities()
    """
    code_lines = []
    
    for block in blocks:
        if block.type == "csv_upload":
            code_lines.append(f"df = pd.read_csv('{block.filepath}')")
        
        elif block.type == "pii_redaction":
            code_lines.append("df = apply_pii_protection(df)")
        
        elif block.type == "build_graph":
            code_lines.append("graph = build_tribe_graph(activities)")
        
        elif block.type == "extract_communities":
            code_lines.append("communities = extract_communities(graph)")
    
    return "\n".join(code_lines)
```

**The Flow:**
1. User drags blocks in Scratch-for-Data
2. System generates Python code
3. Code runs in sandbox with governance
4. Results displayed in dashboard

**Productivity:** Visual → Code → Results in minutes.

---

## Micro-Labs (CS50-Style)

### Lab 1: Build Your First Extractor

**Task:** Write a Python function that extracts one insight

**Example:**
```python
def extract_top_collaborators(activities: List[CanonicalActivity], 
                             top_n: int = 5) -> List[Dict]:
    """Extract top collaborators - Python makes this easy."""
    from collections import Counter
    
    # Fast aggregation
    pairs = [
        (a.user_id, a.target_user_id)
        for a in activities
        if a.target_user_id
    ]
    
    # Count occurrences
    counter = Counter(pairs)
    
    # Get top N
    top = counter.most_common(top_n)
    
    return [
        {"user_1": u1, "user_2": u2, "collaborations": count}
        for (u1, u2), count in top
    ]
```

**Success Criteria:**
- [ ] Function works
- [ ] Uses Python built-ins
- [ ] Handles edge cases
- [ ] Returns clean JSON

---

### Lab 2: Exception Handling

**Task:** Write robust extractor with exception handling

**Requirements:**
1. Handle missing data gracefully
2. Don't crash on bad input
3. Return helpful error messages
4. Log errors for debugging

---

### Lab 3: Build Complete Pipeline

**Task:** Assemble all extractors into one pipeline

**Requirements:**
1. CSV → entities
2. TRIBE extraction
3. TEACHER extraction
4. RECON extraction
5. Unified JSON output

---

## Assessment: Self-Relative Growth

### Baseline (Before Week 6)

**Question:** "Can you build a working pipeline?"

**Expected Response:**
- May understand concepts
- May not be able to implement quickly
- May struggle with syntax

### After Week 6

**Question:** "Can you ship a complete pipeline from CSV to JSON in a day?"

**Expected Response:**
- Can use Python built-ins effectively
- Can handle exceptions gracefully
- Can assemble extractors into pipeline
- Can export to JSON

---

## Key Takeaways

1. **Python is the productivity layer.** Same truth-models, faster shipping.

2. **Two-speed development.** Core = formal, Edge = fast.

3. **Abstraction enables safety.** People can build without touching dangerous gears.

4. **Built-ins accelerate.** Dict, list, set = Week 5 for free.

5. **Exceptions = compassionate UX.** System recovers gracefully.

6. **Libraries = ecosystem.** Pandas, NetworkX = instant capabilities.

---

## Next Steps

**Capstone:** Real-World Application
- Run pipeline on Brian's CSV
- Generate three JSON views
- Deploy to dashboard
- Present to stakeholders

**For Now:** Practice Python productivity:
- Build extractors
- Handle exceptions
- Export JSON
- Ship pipelines

---

## Resources

- **extractors/:** See Python MVP extractors
- **pipeline.py:** See complete pipeline
- **structures.py:** See how Python uses built-ins

---

*"Week 6 is where Cosurvival becomes shippable: the same truth-models, now expressed in a language fast enough for real-world iteration."*
