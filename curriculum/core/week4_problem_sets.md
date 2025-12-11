# TEACHER Week 4: Problem Sets

> *"Memory of Trust - Understanding data lifecycle prevents privacy leaks."*

---

## Problem Set 1: Deep Copy vs Shallow Copy

### Problem 1.1: Identify the Bug

**Given this code:**

```python
raw_user = RawUser(
    id="user_123",
    email="john@company.com",
    name="John Smith",
    company_id="org_abc"
)

# BUG: Shallow copy
safe_user = raw_user  # Points to same object!

# Later, safe_user.email still contains PII
print(safe_user.email)  # LEAK!
```

**Task:**
1. Identify why this is a privacy leak
2. Fix it using deep copy to safe schema
3. Prove the fix works (show safe_user has no PII)

---

### Problem 1.2: Implement Safe Copy Function

**Task:** Write a function that safely copies raw data to safe schema

```python
def create_safe_user(raw_user: RawUser) -> SafeUser:
    """
    Deep copy raw user to safe schema.
    
    Requirements:
    - Hash PII fields
    - Remove prohibited fields
    - Create new object (no shared references)
    """
    # TODO: Implement
    pass
```

**Test Cases:**
```python
raw = RawUser(id="user_123", email="john@company.com", name="John")
safe = create_safe_user(raw)

# Should not share references
assert id(raw) != id(safe)

# Should not contain PII
assert not hasattr(safe, 'email')
assert not hasattr(safe, 'name')

# Should contain safe fields
assert safe.id != "user_123"  # Hashed
assert safe.email_domain == "company.com"  # Aggregated
```

---

## Problem Set 2: Lens Boundary Contracts

### Problem 2.1: Design a Lens Boundary

**Task:** Design a boundary for a new lens: "SECURITY" (security event analysis)

**Requirements:**
1. Define allowed fields
2. Define prohibited fields
3. Set minimum cohort size
4. Explain why each field is allowed/prohibited

**Starter:**
```python
SECURITY_BOUNDARY = LensBoundary(
    lens_name="security",
    allowed_fields={...},
    prohibited_fields={...},
    min_cohort_size=...,
    # TODO: Complete
)
```

---

### Problem 2.2: Validate Field Access

**Task:** Implement boundary validation

```python
def validate_lens_access(lens: str, field: str, context: Dict) -> bool:
    """
    Validate if lens can access field.
    
    Requirements:
    - Check boundary rules
    - Check cohort size
    - Check cardinality
    - Return True/False with reason
    """
    # TODO: Implement
    pass
```

---

## Problem Set 3: Lensgrind Implementation

### Problem 3.1: Detect PII References

**Task:** Write a function that detects PII in data structures

```python
def detect_pii(data: Any) -> List[Dict[str, str]]:
    """
    Detect PII patterns in data.
    
    Returns:
        List of detected PII with type and location
    """
    # TODO: Implement
    pass
```

**Test Cases:**
```python
# Should detect email
data = {"user": "john@company.com"}
assert len(detect_pii(data)) > 0

# Should detect phone
data = {"contact": "+1-555-123-4567"}
assert len(detect_pii(data)) > 0

# Should not detect safe data
data = {"user_id": "entity_abc123"}
assert len(detect_pii(data)) == 0
```

---

### Problem 3.2: Detect Shallow Copies

**Task:** Write a function that detects shallow copies

```python
def is_shallow_copy(source: Any, destination: Any) -> bool:
    """
    Check if destination is a shallow copy of source.
    
    Returns:
        True if shallow copy (unsafe), False if deep copy (safe)
    """
    # TODO: Implement
    pass
```

---

## Problem Set 4: Data Lifecycle Management

### Problem 4.1: Design Lifecycle for Session Data

**Task:** Design lifecycle management for temporary session data

**Requirements:**
1. Define what goes on stack (ephemeral)
2. Define what goes on heap (cached)
3. Define what goes to persistent storage (audited)
4. Implement cleanup functions

---

### Problem 4.2: Implement Safe Data Store

**Task:** Implement a data store that enforces safe schemas

```python
class SafeDataStore:
    """
    Data store that only accepts safe schemas.
    
    Requirements:
    - Reject raw data with PII
    - Only accept safe schemas
    - Track data lineage
    - Enforce TTL for cached data
    """
    # TODO: Implement
    pass
```

---

## Problem Set 5: Buffer Overflow → Lens Boundary Breach

### Problem 5.1: Identify Boundary Breaches

**Given these scenarios, identify the boundary breach:**

**Scenario A:**
```python
# TRIBE lens code
def extract_tribe(activities):
    for activity in activities:
        # Accessing TEACHER domain
        if activity.state_before != activity.state_after:
            # This is a TEACHER domain field!
            process_permission_change(activity)
```

**Question:** What boundary is breached? How would you fix it?

---

**Scenario B:**
```python
# TEACHER lens code
def extract_teacher(activities):
    # Accessing RECON domain
    providers = group_by(activities, "provider_id")
    # This is RECON domain!
    score_providers(providers)
```

**Question:** What boundary is breached? How would you fix it?

---

### Problem 5.2: Implement Boundary Enforcement

**Task:** Write a decorator that enforces lens boundaries

```python
def enforce_boundary(lens_name: str):
    """
    Decorator that enforces lens boundary.
    
    Requirements:
    - Check all field accesses
    - Block prohibited fields
    - Log violations
    - Raise exception on critical violations
    """
    # TODO: Implement
    pass
```

---

## Problem Set 6: Integration Challenge

### Problem 6.1: Build Safe TRIBE Extractor

**Task:** Build TRIBE extractor with full safety checks

**Requirements:**
1. Use safe data store (no raw data)
2. Enforce TRIBE boundary
3. Use Lensgrind monitoring
4. Deep copy all outputs
5. Prove no PII in outputs

---

### Problem 6.2: Build Safe TEACHER Extractor

**Task:** Build TEACHER extractor with full safety checks

**Requirements:**
1. Use safe data store
2. Enforce TEACHER boundary
3. Use Lensgrind monitoring
4. Deep copy all outputs
5. Prove no cross-lens leaks

---

### Problem 6.3: Build Safe RECON Extractor

**Task:** Build RECON extractor with full safety checks

**Requirements:**
1. Use safe data store
2. Enforce RECON boundary
3. Use Lensgrind monitoring
4. Enforce minimum cohort sizes
5. Prove no individual-level data

---

## Submission Guidelines

### For Each Problem Set

1. **Code:** Working implementation
2. **Tests:** At least 2 test cases
3. **Safety Proof:** Demonstrate no PII leaks
4. **Lensgrind Report:** Show clean report

### Self-Assessment

After completing all problem sets, answer:

1. Can you explain why shallow copy is dangerous?
2. Can you prove your lens outputs are safe?
3. Can you use Lensgrind to verify safety?
4. What was the hardest concept?

**Remember:** Growth over position. Compare to your Week 3 baseline.

---

## Solutions (For Instructors)

Solutions are available in `week4_solutions.py` for instructors.

**Key Learning Points:**
- Shallow copy = privacy leak
- Lens boundaries prevent cross-domain leaks
- Lensgrind finds privacy violations
- Data lifecycle matters for trust
- Deep copy to safe schemas is non-negotiable

---

*"Week 4 is where we prove we can touch sensitive reality without creating risk."*

