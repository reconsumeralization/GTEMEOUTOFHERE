# TEACHER Core Track Curriculum

> *"What ultimately matters is not where you end up relative to your classmates, but where you end up relative to yourself when you began."*

> **Ethical Foundation:** *"AI that strengthens human agency, privacy, and dignity — not one that replaces them."*

> **Security Foundation:** *"Trust is a supply chain problem—of code, data, identity, and human integrity. No single tool, file, or community action can become a silent pivot into global harm."*

---

## The Learning Architecture

```
CONCEPTS → FUNDAMENTALS → STRUCTURES → ALGORITHMS → DOMAINS → CAPSTONE
   ↓           ↓             ↓            ↓           ↓          ↓
 Week 0     Week 1        Week 2       Week 3     Week 4+    Final
 Visual     Formal        Canonical    Extractors  Applied    Real
 Intuition  Primitives    Entities     + Models    Systems    World
```

This curriculum transforms any learner from "what is data?" to "I can build ethical intelligence systems."

---

# Week 0: Concepts

## Theme: "Making Data Alive"

### Learning Objectives
By the end of this week, learners will:
- Understand that the same data can mean different things in different contexts
- Recognize the three lenses: TRIBE (relationships), TEACHER (growth), RECON (value)
- Feel confident that they belong in this space

### Core Concepts

#### 1. Everything is 0s and 1s (but context creates meaning)

```
Same Row of Activity Data:
┌──────────────────────────────────────────────────────────┐
│ UserA accessed Document.pdf shared by UserB at 10:30am  │
└──────────────────────────────────────────────────────────┘
                         │
        ┌────────────────┼────────────────┐
        ▼                ▼                ▼
    TRIBE LENS      TEACHER LENS     RECON LENS
    "UserA and      "UserA is        "The document
    UserB are       learning from    platform is
    connected"      UserB"           providing value"
```

##### Inspiration: Meaning Through Perspective

> *"For now we see through a glass, darkly; but then face to face: now I know in part; but then shall I know even as also I am known."*
> 
> — 1 Corinthians 13:12

**Connection:** Just as we see truth partially now, we see data through different lenses. The same activity row means different things through TRIBE (relationships), TEACHER (growth), and RECON (value) perspectives. Understanding grows as we view from multiple angles.

> *"The same object casts different shadows depending on the light."*
> 
> — Plato's Allegory of the Cave

**Connection:** The same activity data means different things through TRIBE/TEACHER/RECON lenses. Just as prisoners in the cave see shadows and must learn to see the true forms, we see data through different perspectives to understand deeper truth.

> *"The whole is greater than the sum of its parts."*
> 
> — Aristotle

**Connection:** The three lenses together (TRIBE + TEACHER + RECON) reveal more than any single lens alone. The whole system is greater than individual insights.

> *"I saw the angel in the marble and carved until I set him free."*
> 
> — Michelangelo

**Connection:** The same raw data contains multiple meanings. We "carve" (analyze) through different lenses until we "set free" the insights hidden within.

##### Alternative Perspectives: How Other Thinkers Would View This Problem

**The Problem:** The same activity data can mean different things. How do we understand truth when context changes meaning?

**Plato's Approach (Forms & Shadows):**
> *"The same object casts different shadows depending on the light."*
> 
> — Allegory of the Cave

Plato would say: The shadows (TRIBE/TEACHER/RECON views) are not the truth itself, but they point to the Form (the underlying reality). We must move beyond the shadows to see the true Form—the complete understanding that synthesizes all three lenses.

**Aristotle's Approach (Empirical Observation):**
> *"The whole is greater than the sum of its parts."*
> 
> — Aristotle

Aristotle would say: Don't choose one lens—use all three. Observe through TRIBE, then TEACHER, then RECON. The complete truth emerges from combining all perspectives. The whole (all three lenses together) reveals more than any single lens alone.

**Michelangelo's Approach (Revealing Hidden Beauty):**
> *"I saw the angel in the marble and carved until I set him free."*
> 
> — Michelangelo

Michelangelo would say: The meaning isn't created—it's already there, waiting to be revealed. Each lens "carves away" the unnecessary to reveal a different aspect of the truth. All three carvings together reveal the complete "angel" (full understanding).

**Biblical Perspective (Progressive Revelation):**
> *"For now we see through a glass, darkly; but then face to face: now I know in part; but then shall I know even as also I am known."*
> 
> — 1 Corinthians 13:12

The biblical view: We see partially now (through one lens), but understanding grows as we view from multiple angles. Complete knowledge comes from seeing "face to face"—integrating all three perspectives.

**Synthesis:** All four perspectives agree: truth requires multiple viewpoints. Plato seeks the Form beyond shadows, Aristotle combines observations, Michelangelo reveals hidden beauty, and the biblical view emphasizes progressive understanding. Together, they teach us that the three lenses (TRIBE/TEACHER/RECON) are not competing truths—they are complementary paths to complete understanding.

#### 2. The Three Questions

| Lens | Question | Output |
|------|----------|--------|
| **TRIBE** | Who is connected to whom? | Network graph |
| **TEACHER** | Who is growing in what ways? | Learning pathways |
| **RECON** | Who is providing value ethically? | Provider scores |

#### 3. Privileges = Skills (a key insight)

When someone gets permission to do something new, they're demonstrating readiness. Permission changes are skill acquisitions in disguise.

```
StateOld: "viewer" → StateNew: "editor"

TEACHER interpretation: This person has grown from 
consuming information to creating it.
```

### Activities

#### Activity 0.1: The Lens Toggle Simulator
**Time:** 15 minutes

Interactive exercise where learners view a single activity row and toggle between:
- 🌐 TRIBE view (highlights: who interacted with whom)
- 📚 TEACHER view (highlights: what skill was demonstrated)
- 💱 RECON view (highlights: what value was exchanged)

#### Activity 0.2: Find Yourself in the Data
**Time:** 20 minutes

Given a sample dataset:
1. Find an activity that represents learning
2. Find an activity that represents collaboration
3. Find an activity that represents value exchange

#### Activity 0.3: The Governance Gate
**Time:** 15 minutes

Discussion: "Why can't we just analyze everything?"

Concepts introduced:
- PII (Personally Identifiable Information)
- Bias guardrails ("high activity ≠ high value")
- Prohibited inferences (never predict performance)

#### Activity 0.4: Ethical Guardrails
**Time:** 20 minutes

Discussion: "AI as advisor, not authority"

Core principle: **AI that strengthens human agency, privacy, and dignity — not one that replaces them.**

Anti-patterns to avoid:
- ❌ Advisor → Authority (AI making decisions without human approval)
- ❌ Manipulation for profit (optimizing engagement over wellbeing)
- ❌ Surveillance under safety banner (tracking without consent)
- ❌ Centralized sensitive data (data leaving user control)
- ❌ Opaque decisions (no explanation or audit trail)
- ❌ Biased models (gatekeeping opportunity)
- ❌ Dependency by design (making users feel incapable)

See: `TEACHER_ETHICAL_GUARDRAILS.md` for detailed guidance

##### Inspiration: The Labor of Love

> *"And now abideth faith, hope, charity, these three; but the greatest of these is charity."*
> 
> — 1 Corinthians 13:13

**Connection:** The goal of AI isn't efficiency—it's freeing humanity for the greatest labor: love. Relationships, care, meaning. When AI handles routine tasks, we're freed for the Labor of Love.

> *"Love is a serious mental disease."*
> 
> — Plato

**Connection:** The "Labor of Love" is not rational efficiency—it's a "disease" that compels us to care, to serve, to give. AI should free us for this irrational but essential work.

> *"We are what we repeatedly do. Excellence, then, is not an act, but a habit."*
> 
> — Aristotle

**Connection:** The Labor of Love is not a single act—it's a habit, a way of life. AI should free us to make love a habit, not an exception.

> *"I saw the angel in the marble and carved until I set him free."*
> 
> — Michelangelo

**Connection:** AI should free the "angel" in humanity—our capacity for love, care, meaning. We're not creating something new, we're revealing what's already there.

##### Alternative Perspectives: How Other Thinkers Would View "The Labor of Love"

**The Problem:** What should AI free us for? What is the purpose of technology if not efficiency?

**Plato's Approach (Love as Divine Madness):**
> *"Love is a serious mental disease."*
> 
> — Plato

Plato would say: Love is not rational—it's a "disease" that compels us beyond self-interest. AI should free us for this "irrational" but essential work. Efficiency serves the rational; love serves the divine. The Labor of Love is the highest purpose because it connects us to the Forms (ultimate reality).

**Aristotle's Approach (Happiness as Ultimate Purpose):**
> *"Happiness is the meaning and the purpose of life, the whole aim and end of human existence."*
> 
> — Aristotle

Aristotle would say: But happiness isn't pleasure—it's eudaimonia (flourishing). The Labor of Love is what makes us flourish. AI should free us for activities that develop virtue, build relationships, and create meaning. This is true happiness.

**Michelangelo's Approach (Love in God's Light):**
> *"I live and love in God's peculiar light."*
> 
> — Michelangelo

Michelangelo would say: The Labor of Love is done in a "peculiar light"—not the light of efficiency, but the light of divine purpose. AI should free us to work in this light—creating beauty, serving others, expressing love.

**Biblical Perspective (Charity as Greatest):**
> *"And now abideth faith, hope, charity, these three; but the greatest of these is charity."*
> 
> — 1 Corinthians 13:13

The biblical view: All technical achievement means nothing without love (charity). The Labor of Love is the greatest because it's eternal—relationships, care, meaning outlast all technology.

**Synthesis:** All four perspectives converge: AI's purpose is to free us for love. Plato calls it divine madness, Aristotle calls it eudaimonia, Michelangelo calls it God's light, and the biblical view calls it charity. They all point to the same truth: the Labor of Love is the highest purpose technology can serve.

**Reflection:** What would you do with time freed by AI? How would you use it to love others?

### Checkpoint 0
**Artifact:** Reflection document

Answer these questions:
1. Which fields in an activity log define identity?
2. Which fields imply skill growth?
3. Which fields signal supplier quality?
4. Why is governance necessary?

### Mastery Indicators
- [ ] Can explain the three lenses
- [ ] Can identify PII in a dataset
- [ ] Understands context-dependent interpretation
- [ ] Feels confident to proceed

---

# Week 1: Fundamentals

## Theme: "The Policy-First Mindset"

### Learning Objectives
- Understand canonical data types
- Apply governance checks before analysis
- Write pseudocode for data transformation

### Core Concepts

#### 1. Canonical Entities

```python
# The Seven Canonical Entities
User        # A person in the system
Company     # An organization
Group       # A team within an organization  
Provider    # A service/tool supplier
Resource    # A file, API, or digital asset
Activity    # An event that happened
Permission  # A change in access rights
```

#### 2. The Governance Gate (Non-Negotiable)

```
RAW DATA → [GOVERNANCE GATE] → CLEAN DATA → ANALYSIS
              │
              ├── PII Check (hash names, emails)
              ├── Bias Check (no performance inference)
              ├── Scope Check (no prohibited outputs)
              └── Review Trigger (human approval needed?)
```

#### 3. Schema Detection

```
"Uid" → user_id
"CompanyName" → company_name  
"StateOld → StateNew" → permission_change
```

Patterns matter more than exact column names.

### Activities

#### Activity 1.1: Build a Data Dictionary
**Time:** 30 minutes

Given a CSV with 20 columns, create a data dictionary:
- Column name
- Meaning
- Data type
- Sensitivity level (public/internal/confidential/restricted)
- Requires hashing? (yes/no)

#### Activity 1.2: Write Governance Rules
**Time:** 25 minutes

Create 5 rules that should BLOCK analysis:
1. Example: "If the analysis attempts to rank individual performance..."

#### Activity 1.3: Pseudocode Practice
**Time:** 30 minutes

Write pseudocode for:
1. Detecting a user-to-user interaction
2. Detecting a permission upgrade
3. Detecting a provider error

### Checkpoint 1
**Artifact:** governance_rules.md

A document containing:
- Your data dictionary for a sample dataset
- 5 governance rules you would enforce
- Pseudocode for one detection algorithm

### Mastery Indicators
- [ ] Can classify columns by sensitivity
- [ ] Can identify PII requiring hashing
- [ ] Can write governance rules
- [ ] Can translate logic to pseudocode

---

# Week 2: Data Structures

## Theme: "Canonical Representations"

### Learning Objectives
- Design schemas for the seven canonical entities
- Understand graph structures for relationships
- Validate data against schemas

### Core Concepts

#### 1. Entity Schemas

```python
@dataclass
class CanonicalUser:
    id: str                    # Hashed for privacy
    email_domain: str          # Preserved for org analysis
    company_id: str
    roles: List[str]
    groups: List[str]
    activity_count: int
    first_seen: datetime
    last_seen: datetime
```

#### 2. Graph Structures

```
TRIBE Graph:
- Nodes: Users, Groups, Companies
- Edges: Collaboration, Membership, Hierarchy
- Weights: Interaction frequency

Example:
User_A ──[collaborated 15x]──> User_B
   │                             │
   └──[member of]──> Group_X <──┘
```

#### 3. Event Stores

```json
{
  "id": "evt_001",
  "timestamp": "2024-01-15T10:30:00Z",
  "type": "document_access",
  "user_id": "entity_abc123",
  "resource_id": "doc_xyz789",
  "target_user_id": "entity_def456",
  "state_before": "viewer",
  "state_after": "editor"
}
```

### Activities

#### Activity 2.1: Design Your Schema
**Time:** 45 minutes

Design complete schemas for:
- User
- Activity
- PermissionChange

Include: field names, types, validation rules, example values

#### Activity 2.2: Build a Mini Graph
**Time:** 30 minutes

Given 10 activity records, manually construct:
- Node list
- Edge list with weights
- Visualization (hand-drawn or tool)

#### Activity 2.3: Validation Rules
**Time:** 25 minutes

Write validation functions:
- `is_valid_user(user_dict) -> bool`
- `is_valid_activity(activity_dict) -> bool`

### Checkpoint 2
**Artifact:** schema_design.json

A JSON file containing:
- Complete schemas for 3 entities
- Example valid instances
- Example invalid instances with explanation

### Mastery Indicators
- [ ] Can design entity schemas
- [ ] Can construct graph representations
- [ ] Can write validation rules
- [ ] Understands schema-first development

---

# Week 3: Algorithms

## Theme: "MVP Extractors"

### Learning Objectives
- Implement collaboration strength algorithm
- Implement role mastery profiler
- Implement provider reliability scorer
- Understand Big O basics

### Core Concepts

#### 1. TRIBE Algorithms

```python
def collaboration_strength(user_a, user_b, activities):
    """
    Measures how strongly two users collaborate.
    
    Factors:
    - Direct interactions (UidOpp/UidReq)
    - Co-resource access (same file on same day)
    - Shared group membership
    """
    direct = count_direct_interactions(user_a, user_b, activities)
    co_access = count_co_resource_access(user_a, user_b, activities)
    shared_groups = count_shared_groups(user_a, user_b)
    
    return (direct * 0.5) + (co_access * 0.3) + (shared_groups * 0.2)
```

#### 2. TEACHER Algorithms

```python
def role_mastery_profile(user, permission_changes):
    """
    Builds a skill profile from permission history.
    
    Key insight: Permission upgrades = skill demonstrations
    """
    skills = []
    for change in permission_changes:
        if change.user_id == user.id:
            if is_upgrade(change.state_before, change.state_after):
                skills.append(extract_skill(change))
    
    return MasteryProfile(
        user_id=user.id,
        skills=skills,
        trajectory="growing" if len(skills) > baseline else "stable"
    )
```

#### 3. RECON Algorithms

```python
def provider_reliability_score(provider, activities):
    """
    Scores provider reliability.
    
    Score = 1 - (errors / total_activities)
    """
    total = count_activities(provider, activities)
    errors = count_errors(provider, activities)
    
    return 1 - (errors / total) if total > 0 else 0
```

#### 4. Efficiency Matters

| Algorithm | Naive | Optimized | Why It Matters |
|-----------|-------|-----------|----------------|
| Find user | O(n) | O(1) hash | 1M users = 1M vs 1 lookup |
| Build graph | O(n²) | O(n log n) | 10K users = 100M vs 130K ops |
| Community detection | O(n³) | O(n log n) | Makes it possible at all |

### Activities

#### Activity 3.1: Implement Collaboration Strength
**Time:** 45 minutes

Write working code that:
- Takes two user IDs and a list of activities
- Returns a collaboration strength score (0-1)
- Includes at least two factors

#### Activity 3.2: Build Role Mastery Profiler
**Time:** 45 minutes

Write working code that:
- Takes a user and their permission changes
- Returns a mastery profile with skills list
- Categorizes trajectory (growing/stable/declining)

#### Activity 3.3: Create Provider Scorer
**Time:** 30 minutes

Write working code that:
- Takes a provider ID and activities
- Returns reliability, adoption, and composite scores
- Assigns a letter grade (A-F)

### Checkpoint 3
**Artifact:** extractors.py

A Python module containing:
- `collaboration_strength()` function
- `role_mastery_profile()` function
- `provider_reliability_score()` function
- Unit tests for each

### Mastery Indicators
- [ ] Can implement graph algorithms
- [ ] Can implement scoring algorithms
- [ ] Understands algorithmic efficiency
- [ ] Can write testable code

---

# Week 4+: Domains

## Theme: "Applied Systems"

### Learning Objectives
- Build complete TRIBE analysis pipeline
- Build complete TEACHER pathway generator
- Build complete RECON scoring system
- Integrate all three into unified output

### Module 4A: TRIBE Deep Dive

#### Deliverables
1. Community detection algorithm
2. Cross-silo bridge finder
3. Mentor candidate identifier
4. Network visualization

#### Capstone Output
```json
{
  "tribe_analysis": {
    "communities": [...],
    "bridges": [...],
    "mentors": [...],
    "network_stats": {...}
  }
}
```

### Module 4B: TEACHER Deep Dive

#### Deliverables
1. Role-skill matrix builder
2. Peer comparison engine (non-competitive)
3. Learning path generator
4. Progression tracker

#### Capstone Output
```json
{
  "teacher_analysis": {
    "role_skill_matrix": {...},
    "user_recommendations": [...],
    "org_gap_reports": [...],
    "progression_metrics": {...}
  }
}
```

### Module 4C: RECON Deep Dive

#### Deliverables
1. Provider profiler
2. Value flow mapper
3. Ethics scorer
4. Friction point detector

#### Capstone Output
```json
{
  "recon_analysis": {
    "provider_scores": [...],
    "value_flows": [...],
    "friction_points": [...],
    "ethics_grades": {...}
  }
}
```

### Mastery Indicators
- [ ] Can build end-to-end TRIBE pipeline
- [ ] Can build end-to-end TEACHER pipeline
- [ ] Can build end-to-end RECON pipeline
- [ ] Can integrate outputs into unified JSON

---

# Capstone: Real World Application

## Theme: "Prove It Works"

### Requirements

Run your complete pipeline on a real organizational dataset and produce:

1. **Governance Report**
   - PII handling documentation
   - Bias guardrail verification
   - Scope statement compliance

2. **TRIBE Output**
   - Network visualization
   - Top 5 communities
   - Top 5 bridge connectors
   - Mentor recommendations

3. **TEACHER Output**
   - Role-skill matrix
   - 10 personalized learning recommendations
   - Organization skill gaps

4. **RECON Output**
   - Provider rankings with ethics grades
   - Top 5 value flows
   - Top 5 friction points

5. **Integration Insights**
   - Cross-system connections
   - Actionable recommendations

### Evaluation Criteria

**Not evaluated:**
- Speed relative to peers
- "Correctness" of interpretations
- Complexity of implementation

**Evaluated:**
- Growth from Week 0 baseline
- Governance compliance
- Bias guardrail adherence
- Quality of documentation
- Ability to explain decisions

### Final Reflection

Answer:
1. What do you understand now that you didn't in Week 0?
2. What would you do differently next time?
3. How might you apply this in your context?

---

# Appendix: Mastery Tracking Philosophy

## The Self-Relative Principle

```
NEVER:
- Rank learners against each other
- Label skill gaps as "deficiencies"
- Use activity volume as quality proxy

ALWAYS:
- Compare learner to their own baseline
- Frame gaps as "growth opportunities"
- Celebrate trajectory over position
```

## Progress Display

```
Instead of:  "You are at level 3 (class average: 4.2)"

Display:     "Since you started:
              ✓ +2 new capabilities unlocked
              ✓ 3 concepts mastered
              ✓ On track for Week 3 checkpoint"
```

## The Growth Mindset in Code

```python
def display_progress(learner):
    baseline = learner.starting_snapshot
    current = learner.current_snapshot
    
    gains = current.skills - baseline.skills
    
    return {
        "message": f"You've unlocked {len(gains)} new capabilities since you began.",
        "gains": list(gains),
        "trajectory": calculate_trajectory(learner),
        # NEVER include: rank, percentile, comparison to others
    }
```

---

*This curriculum is designed to be completed at your own pace. There is no deadline. There is no ranking. There is only your growth.*

