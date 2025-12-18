# TEACHER Week 4: Memory of Trust

> *"Week 4 is where TEACHER proves it can touch sensitive reality without turning that reality into risk."*

---

## Module Overview

**Duration:** 7-9 hours  
**Prerequisites:** Week 3 (Algorithms)  
**Next:** Week 5+ (Domains & Integration)

This week, learners discover that data has **memory** — real storage, references, and lifecycle. Just as CS50 Week 4 reveals how computers actually store data, TEACHER Week 4 reveals how data systems must manage sensitive information safely.

---

## Learning Outcomes

By the end of this week, learners will be able to:

1. **Explain** why references can cause privacy harm
2. **Distinguish** raw, derived, and redacted data classes
3. **Understand** why governance must be enforced at the field level
4. **Connect** "buffer overflow" logic to real-world data leakage
5. **Implement** safe data copying and lifecycle management
6. **Use** Lensgrind to detect privacy leaks
7. **Design** lens boundary contracts

---

## Core Concept: Data Has Memory

### CS50's Insight

> "Strings, files, images are just bytes in memory. Understanding memory is understanding how computers actually work."

### TEACHER's Insight

> "TRIBE/TEACHER/RECON are just structured meaning laid on top of bytes. Understanding data memory is understanding how to keep that meaning safe."

##### Inspiration: Trust Requires Boundaries

> *"Trust in the Lord with all thine heart; and lean not unto thine own understanding. In all thy ways acknowledge him, and he shall direct thy paths."*
> 
> — Proverbs 3:5-6

**Connection:** Trust requires boundaries. We trust systems that have proper safeguards—just as we trust paths that are clearly marked. Data needs "secret places" and "fortresses"—proper boundaries and protection.

> *"The price of apathy towards public affairs is to be ruled by evil men."*
> 
> — Plato

**Connection:** The price of apathy towards data safety is to be ruled by unsafe systems. We must actively govern data, not passively accept leaks.

> *"The roots of education are bitter, but the fruit is sweet."*
> 
> — Aristotle

**Connection:** Learning memory safety is hard (bitter), but the result—trustworthy systems—is sweet. The governance work is difficult, but the outcome is worth it.

> *"The greater danger for most of us lies not in setting our aim too high and falling short, but in setting our aim too low and achieving our mark."*
> 
> — Michelangelo

**Connection:** Don't aim for "good enough" security. Aim for excellence. Trust requires high standards.

##### Alternative Perspectives: How Other Thinkers Would Build Trust

**The Problem:** How do we build trustworthy systems? What creates trust in data handling?

**Plato's Approach (Conquering Self First):**
> *"The first and best victory is to conquer self."*
> 
> — Plato

Plato would say: Trust begins with self-mastery. We must conquer our own vulnerabilities—proper validation, boundaries, governance. Before we can protect others, we must master ourselves. The "first victory" is building systems that resist our own mistakes.

**Aristotle's Approach (Courage as Foundation):**
> *"Courage is the first of human qualities because it is the quality which guarantees the others."*
> 
> — Aristotle

Aristotle would say: Trust requires courage—the courage to say no, to set boundaries, to enforce rules. Without courage, other virtues (privacy, integrity) cannot be guaranteed. Security systems must be built with courage—willing to reject unsafe practices, even when convenient.

**Michelangelo's Approach (Continuous Learning):**
> *"I am still learning."*
> 
> — Michelangelo

Michelangelo would say: Trust is built through continuous learning. Security is never "finished"—we keep learning, adapting, improving. Defense in depth means continuous vigilance. Each new threat teaches us, each new protection strengthens trust.

**Biblical Perspective (Trust in Boundaries):**
> *"Trust in the Lord with all thine heart; and lean not unto thine own understanding. In all thy ways acknowledge him, and he shall direct thy paths."*
> 
> — Proverbs 3:5-6

The biblical view: Trust requires boundaries and guidance. We trust systems that have proper safeguards—just as we trust paths that are clearly marked. Data needs "secret places" and "fortresses"—proper boundaries and protection. Trust comes from knowing the boundaries are secure.

**Synthesis:** All four perspectives converge: trust requires self-mastery (Plato), courage (Aristotle), continuous learning (Michelangelo), and secure boundaries (biblical). Trust isn't given—it's earned through proper design, constant vigilance, and moral courage. Our systems must reflect all four: mastery, courage, learning, and boundaries.

---

## Pointers → Data Aliasing Threat Model

### CS50's Big Reveal

```c
string s = "hello";
string t = s;  // t points to same memory as s
```

**The bug:** `t = s` doesn't copy the string, it copies the pointer.

### TEACHER's Equivalent Risk

```python
# DANGEROUS: Shallow copy
raw_user = get_user_with_pii("user_123")
safe_view = raw_user  # Points to same object!

# Later, safe_view.email still contains PII
# This is a privacy leak waiting to happen
```

**The bug:** Copying a reference to sensitive data ≠ copying safe data.

### The Solution: Two Forms of Every Sensitive Object

```python
# Form 1: Raw (restricted, locked)
@dataclass
class RawUser:
    id: str
    email: str  # PII - RESTRICTED
    name: str   # PII - RESTRICTED
    company_id: str
    # ... other sensitive fields

# Form 2: Redacted/Derived (safe for lenses)
@dataclass
class SafeUser:
    id: str  # Hashed
    email_domain: str  # Aggregated - SAFE
    # name: NOT INCLUDED - removed
    company_id: str  # SAFE for org-level analysis
    activity_count: int  # Derived - SAFE
    # ... only safe fields
```

**The Rule:**
> "All lens outputs must be deep-copied into safe schemas.  
> No pointers to raw data."

---

## Deep Copy vs Shallow Copy → Privacy-by-Default

### CS50's Bug

```c
int *x = malloc(sizeof(int));
int *y = x;  // y points to same memory
*x = 5;
// Now *y is also 5 - they share memory!
```

### TEACHER's Bug

```python
# BUG: Shallow copy
raw_activities = load_activities_with_pii()
tribe_input = raw_activities  # Same reference!

# Later, TRIBE lens accidentally accesses:
for activity in tribe_input:
    print(activity.user_email)  # LEAK! PII exposed
```

### The Fix: Deep Copy to Safe Schema

```python
def create_safe_activities(raw_activities: List[RawActivity]) -> List[SafeActivity]:
    """Deep copy raw activities into safe schema."""
    safe = []
    for raw in raw_activities:
        safe.append(SafeActivity(
            id=hash_pii(raw.user_id),
            timestamp=raw.timestamp,
            activity_type=raw.activity_type,
            company_id=raw.company_id,  # Safe for org analysis
            # email: NOT COPIED - removed
            # name: NOT COPIED - removed
        ))
    return safe  # Completely separate objects, no shared references
```

**The Pattern:**
```
Raw Event Store (locked)
    ↓ [deep copy + transform]
Lens-safe Feature Store (PII stripped)
    ↓ [only safe fields]
Model Inputs (governed)
```

---

## Stack vs Heap → Ephemeral vs Durable Data

### CS50's Model

- **Stack:** Short life, local scope, automatic cleanup
- **Heap:** Allocated, managed, persists until freed
- **Persistent storage:** Files, databases

### TEACHER's Model

- **Stack (Session Context):** Temporary inference state, query results
- **Heap (Caches):** Feature vectors, graph snapshots, computed scores
- **Persistent Storage (Audited Logs):** Event store, governance reports

### The Architecture

```python
class DataLifecycle:
    """
    Explicit lifecycle management for sensitive data.
    """
    
    # Stack: Session data (ephemeral)
    session_context: Dict[str, Any]  # Cleared after request
    
    # Heap: Caches (managed)
    feature_cache: Dict[str, SafeFeatures]  # TTL-based expiration
    
    # Persistent: Audit logs (durable)
    event_store: EventStore  # Immutable, append-only
    
    def process_request(self, raw_data: RawData):
        # 1. Create safe copy (stack)
        safe_data = self.create_safe_copy(raw_data)
        
        # 2. Cache features if needed (heap)
        cache_key = self.get_cache_key(safe_data)
        if cache_key not in self.feature_cache:
            self.feature_cache[cache_key] = self.extract_features(safe_data)
        
        # 3. Log to event store (persistent)
        self.event_store.append(AuditEvent(
            timestamp=datetime.now(),
            action="lens_query",
            data_hash=hash_data(safe_data),  # Not the data itself
            lens_used="tribe"
        ))
        
        # 4. Return result (stack - will be garbage collected)
        return self.run_lens(safe_data, "tribe")
```

**The Promise:**
> "We do not persist what you didn't intend to persist."

---

## Buffer Overflow → Lens Boundary Breach

### CS50's Overflow

```c
char buffer[10];
strcpy(buffer, "This string is too long!");  // OVERFLOW!
// Writes past allocated memory - undefined behavior
```

### TEACHER's Overflow

**The risk:** A lens accessing data beyond its allowed scope.

**Examples:**
- TRIBE insight that leaks TEACHER learning gaps
- TEACHER pathway that reveals RECON vendor disputes
- RECON score that exposes private internal permissions

### The Solution: Lens Boundary Contract

```python
@dataclass
class LensBoundary:
    """Defines what a lens is allowed to access."""
    lens_name: str
    
    # Allowed fields (whitelist)
    allowed_fields: Set[str]
    
    # Allowed join keys (for relationships)
    allowed_join_keys: Set[str]
    
    # Allowed aggregation levels
    min_cohort_size: int  # Prevent small-n re-identification
    max_cardinality: int  # Prevent high-cardinality leaks
    
    # Prohibited fields (blacklist)
    prohibited_fields: Set[str]
    
    def validate_access(self, field: str, context: Dict) -> bool:
        """Check if lens can access this field."""
        # Check whitelist
        if field not in self.allowed_fields:
            return False
        
        # Check blacklist
        if field in self.prohibited_fields:
            return False
        
        # Check cohort size
        cohort_size = context.get('cohort_size', 0)
        if cohort_size < self.min_cohort_size:
            return False  # Too small - re-identification risk
        
        return True
```

### Example Boundaries

```python
TRIBE_BOUNDARY = LensBoundary(
    lens_name="tribe",
    allowed_fields={
        "user_id",  # Hashed
        "company_id",
        "group_id",
        "activity_type",
        "timestamp"
    },
    prohibited_fields={
        "email",
        "name",
        "path",  # May reveal sensitive resources
        "error_code"  # May reveal internal issues
    },
    allowed_join_keys={"user_id", "company_id", "group_id"},
    min_cohort_size=5,  # k-anonymity
    max_cardinality=1000
)

TEACHER_BOUNDARY = LensBoundary(
    lens_name="teacher",
    allowed_fields={
        "user_id",  # Hashed
        "role_id",
        "state_before",
        "state_after",
        "permission_type"
    },
    prohibited_fields={
        "email",
        "name",
        "company_id",  # May reveal org structure
        "resource_path"  # May reveal sensitive files
    },
    allowed_join_keys={"user_id", "role_id"},
    min_cohort_size=3,  # Smaller for role-based analysis
    max_cardinality=500
)

RECON_BOUNDARY = LensBoundary(
    lens_name="recon",
    allowed_fields={
        "provider_id",
        "company_id",
        "activity_count",
        "error_count",
        "scheme"
    },
    prohibited_fields={
        "user_id",  # Individual-level data
        "email",
        "name",
        "resource_path"
    },
    allowed_join_keys={"provider_id", "company_id"},
    min_cohort_size=5,
    max_cardinality=100
)
```

---

## Valgrind → Lensgrind

### CS50's Valgrind

**Purpose:** Find memory leaks, use-after-free, buffer overflows

**How it works:** Instruments code to track memory access

### TEACHER's Lensgrind

**Purpose:** Find privacy leaks, scope violations, unsafe references

**How it works:** Instruments lens execution to track data access

### Lensgrind Implementation

```python
class Lensgrind:
    """
    Privacy and scope auditor for lens execution.
    
    Detects:
    - PII fields used outside allowed scope
    - Disallowed joins
    - Unsafe cardinality reveals
    - Dangling references to raw IDs
    """
    
    def __init__(self):
        self.violations: List[Violation] = []
        self.field_access_log: Dict[str, List[str]] = defaultdict(list)
    
    def check_field_access(self, lens: str, field: str, boundary: LensBoundary):
        """Check if field access is allowed."""
        if not boundary.validate_access(field, {}):
            self.violations.append(Violation(
                type="FIELD_ACCESS_VIOLATION",
                lens=lens,
                field=field,
                reason=f"Field '{field}' not allowed for lens '{lens}'"
            ))
            return False
        return True
    
    def check_join(self, lens: str, join_key: str, boundary: LensBoundary):
        """Check if join is allowed."""
        if join_key not in boundary.allowed_join_keys:
            self.violations.append(Violation(
                type="JOIN_VIOLATION",
                lens=lens,
                field=join_key,
                reason=f"Join on '{join_key}' not allowed for lens '{lens}'"
            ))
            return False
        return True
    
    def check_cohort_size(self, lens: str, cohort_size: int, boundary: LensBoundary):
        """Check if cohort is large enough."""
        if cohort_size < boundary.min_cohort_size:
            self.violations.append(Violation(
                type="SMALL_COHORT_VIOLATION",
                lens=lens,
                field="cohort_size",
                reason=f"Cohort size {cohort_size} < minimum {boundary.min_cohort_size} (re-identification risk)"
            ))
            return False
        return True
    
    def check_reference_safety(self, data: Any):
        """Check for unsafe references to raw data."""
        # Check if data contains PII fields
        if hasattr(data, '__dict__'):
            for key, value in data.__dict__.items():
                if key in ['email', 'name', 'phone']:
                    if isinstance(value, str) and '@' in str(value):
                        self.violations.append(Violation(
                            type="PII_REFERENCE_VIOLATION",
                            lens="unknown",
                            field=key,
                            reason=f"Unsafe reference to PII field '{key}'"
                        ))
                        return False
        return True
    
    def generate_report(self) -> Dict:
        """Generate privacy leak report."""
        return {
            "total_violations": len(self.violations),
            "violations_by_type": self._group_by_type(),
            "violations": [v.to_dict() for v in self.violations],
            "recommendations": self._generate_recommendations()
        }
    
    def _group_by_type(self) -> Dict[str, int]:
        """Group violations by type."""
        counts = defaultdict(int)
        for v in self.violations:
            counts[v.type] += 1
        return dict(counts)
    
    def _generate_recommendations(self) -> List[str]:
        """Generate remediation recommendations."""
        recommendations = []
        
        field_violations = [v for v in self.violations if v.type == "FIELD_ACCESS_VIOLATION"]
        if field_violations:
            recommendations.append(
                f"Remove {len(field_violations)} prohibited field accesses"
            )
        
        cohort_violations = [v for v in self.violations if v.type == "SMALL_COHORT_VIOLATION"]
        if cohort_violations:
            recommendations.append(
                f"Increase cohort sizes for {len(cohort_violations)} analyses to prevent re-identification"
            )
        
        return recommendations


@dataclass
class Violation:
    """A privacy or scope violation detected by Lensgrind."""
    type: str
    lens: str
    field: str
    reason: str
    
    def to_dict(self) -> Dict:
        return {
            "type": self.type,
            "lens": self.lens,
            "field": self.field,
            "reason": self.reason
        }
```

---

## Files + Images → Pipeline Reality Check

### CS50's Insight

> "Files are just bytes. Images are structured bytes. Understanding this is understanding how to work with data."

### TEACHER's Insight

> "A CSV is just a memory object with risk until proven safe. So ingestion must be: classify → sanitize → map → extract → store safely → only then model."

### The Safe Ingestion Pipeline

```python
def safe_ingestion_pipeline(csv_path: str) -> SafeDataStore:
    """
    Safe ingestion with explicit stages.
    
    Stage 1: Classify (identify risk)
    Stage 2: Sanitize (remove/transform PII)
    Stage 3: Map (to canonical schema)
    Stage 4: Extract (entities)
    Stage 5: Store safely (in safe schema)
    Stage 6: Model (only then can we analyze)
    """
    
    # Stage 1: Classify
    raw_df = pd.read_csv(csv_path)
    classifications = classify_columns(raw_df)
    
    # Stage 2: Sanitize
    sanitized_df = sanitize_pii(raw_df, classifications)
    
    # Stage 3: Map
    canonical_entities = map_to_canonical(sanitized_df)
    
    # Stage 4: Extract
    users, companies, activities = extract_entities(canonical_entities)
    
    # Stage 5: Store safely (deep copy to safe schema)
    safe_store = SafeDataStore()
    safe_store.users = [create_safe_user(u) for u in users]
    safe_store.companies = companies  # Already safe
    safe_store.activities = [create_safe_activity(a) for a in activities]
    
    # Stage 6: Model (now safe to analyze)
    return safe_store
```

---

## Micro-Labs (CS50-Style)

### Lab 1: TRIBE Lab - "Safe Identity Graph"

**Objective:** Build a social graph without storing emails

**Task:**
1. Load user data with emails
2. Create safe user nodes (hashed IDs only)
3. Build graph edges (user_id → user_id, both hashed)
4. Prove no reverse map exists in the graph store

**Success Criteria:**
- [ ] Graph contains only hashed IDs
- [ ] No email fields in graph nodes
- [ ] Can demonstrate graph structure without PII
- [ ] Can prove reverse lookup is impossible

---

### Lab 2: TEACHER Lab - "Learning Profile Deep Copy"

**Objective:** Generate a learner profile without leaking raw fields

**Task:**
1. Create raw learning profile (with PII)
2. Show the bug version (shallow copy, leaks email)
3. Show safe version (deep copy, feature-only)
4. Demonstrate the difference

**Success Criteria:**
- [ ] Can identify the bug in shallow copy
- [ ] Can implement safe deep copy
- [ ] Safe profile contains only safe fields
- [ ] Can prove no shared references

---

### Lab 3: RECON Lab - "Provider Score Without Re-identification"

**Objective:** Score providers while preventing small-n re-identification

**Task:**
1. Calculate provider scores
2. Check cohort sizes
3. Block scoring if cohort < minimum
4. Aggregate to safe levels

**Success Criteria:**
- [ ] Enforces minimum cohort size
- [ ] Blocks unsafe aggregations
- [ ] Provides safe aggregated scores
- [ ] Can explain why small-n is dangerous

---

### Lab 4: Governance Lab - "Lensgrind"

**Objective:** Run automated privacy leak detection

**Task:**
1. Implement Lensgrind checker
2. Run on sample lens code
3. Detect violations
4. Generate remediation report

**Success Criteria:**
- [ ] Detects field access violations
- [ ] Detects join violations
- [ ] Detects small cohort violations
- [ ] Generates actionable recommendations

---

## Assessment: Self-Relative Growth

### Baseline (Before Week 4)

**Question:** "Can you explain how data is stored in your system?"

**Expected Response:**
- May not distinguish raw vs safe
- May not understand reference risks
- May not see lifecycle implications

### After Week 4

**Question:** "Can you prove your lens outputs are safe from privacy leaks?"

**Expected Response:**
- Can explain raw vs safe data classes
- Can demonstrate deep copy safety
- Can use Lensgrind to verify
- Can explain lens boundaries

---

## Key Takeaways

1. **Data has memory.** References, copies, and lifecycle matter.

2. **Shallow copy = privacy leak.** Always deep copy to safe schemas.

3. **Lens boundaries are non-negotiable.** Each lens has strict access rules.

4. **Lensgrind finds privacy leaks.** Just as Valgrind finds memory leaks.

5. **Stack vs heap vs persistent.** Different storage for different trust levels.

6. **Buffer overflow = lens boundary breach.** Same concept, different domain.

---

## Activity 4.3: Background States and Excitations (Dirac Sea Concept)

**Time:** 35 minutes

**Learning Objective:** Understand the "sea" of potential patterns vs. actual observations (like Dirac's sea of negative energy states)

**Context:** Just as Dirac theorized a "sea" of electrons in negative energy states (with holes = positrons), we have a "sea" of potential patterns (with gaps = anti-patterns).

**Activity Steps:**

1. **Map the "background state":** All possible patterns that COULD exist
   - All possible collaborations (every user pair)
   - All possible skill combinations (every role × skill)
   - All possible provider adoptions (every company × provider)

2. **Identify "excitations":** Patterns that DO exist (actual observations)
   - Actual collaborations (from activity data)
   - Actual skills demonstrated (from permission changes)
   - Actual providers used (from activity data)

3. **Identify "holes":** Patterns that SHOULD exist but don't (gaps)
   - Missing collaborations (users who should collaborate but don't)
   - Missing skills (skills that should be present but aren't)
   - Missing provider adoptions (providers that should be used but aren't)

4. **Explain the relationship:**
   - Background state = All potential
   - Excitations = What's actual
   - Holes = What's missing (anti-patterns)

**Example:**
```
Background State: "All possible skill combinations for role X"
Actual Excitations: "Skills that users in role X actually have"
Holes: "Skills that users in role X should have but don't"
Insight: "The holes reveal skill gaps and learning opportunities"
```

**Implementation:**
```python
# Map background state
all_possible_collaborations = [
    (u1.id, u2.id) 
    for u1 in users 
    for u2 in users 
    if u1.id != u2.id and u1.company_id == u2.company_id
]

# Find actual excitations
actual_collaborations = [
    (a.user_id, a.target_user_id)
    for a in activities
    if a.activity_type == "collaboration"
]

# Find holes (anti-patterns)
collaboration_holes = [
    pair for pair in all_possible_collaborations
    if pair not in actual_collaborations
    and should_collaborate(pair[0], pair[1])  # Same role, similar work
]
```

**Key Insight:** The "Dirac sea" of potential patterns helps us identify what's missing (holes) as clearly as what's present (excitations).

**CURRICULUM REFERENCE:**
- See: `curriculum/vision/chapters/DIrac_ANTIPATTERNS_APPLICATION.md`
- Builds on: Activity 0.5, 1.4

**Success Criteria:**
- [ ] Can map background state (all possible patterns)
- [ ] Can identify actual excitations (what exists)
- [ ] Can identify holes (what's missing)
- [ ] Can explain how holes reveal opportunities

---

## Next Steps

**Week 5+:** Domains & Integration
- Complete TRIBE pipeline with safe graph
- Complete TEACHER pipeline with safe profiles
- Complete RECON pipeline with safe scores
- Integration and real-world deployment

**For Now:** Practice safe data handling:
- Deep copy patterns
- Lens boundary contracts
- Lensgrind validation

---

## Resources

- **governance.py:** See lens boundaries in code
- **ingestion.py:** See safe ingestion pipeline
- **mvp_extractors.py:** See extractors with safety checks

---

*"Week 4 is where TEACHER proves it can touch sensitive reality without turning that reality into risk."*

