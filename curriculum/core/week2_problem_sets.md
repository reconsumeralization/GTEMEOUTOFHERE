# TEACHER Week 2: Problem Sets

> *"Data has physics. Understanding the constraints is understanding the system."*

---

## Problem Set 1: The 4-Stage Pipeline

### Problem 1.1: Trace the Pipeline

Given this code:

```python
def process_data(csv_path: str, lens: str):
    df = pd.read_csv(csv_path)
    activities = []
    for row in df.itertuples():
        activities.append(CanonicalActivity(
            id=row.Uid,
            timestamp=row.Date,
            activity_type=row.Type
        ))
    if lens == "tribe":
        return build_graph(activities)
    elif lens == "teacher":
        return extract_skills(activities)
    elif lens == "recon":
        return score_providers(activities)
```

**Question:** Which stages are missing? What integrity checks are absent?

**Your Task:**
1. Identify which of the 4 stages are present
2. Identify which stages are missing
3. Rewrite to include all 4 stages with integrity checks
4. Add observability/tracing

---

### Problem 1.2: Stage Result Design

**Task:** Design a `StageResult` class that captures:
- Stage name
- Pass/fail status
- Exit code (0 = success, non-zero = error)
- Confidence score (0.0-1.0)
- Review required flag
- Reason/message
- Metadata

**Requirements:**
1. Implement the class
2. Write a function that creates results for each stage
3. Write a function that aggregates results into a pipeline report

---

## Problem Set 2: Arrays → Entity Collections

### Problem 2.1: Activity Bucketing

**Task:** Implement `bucket_activities()` that groups activities by:
- Provider
- Role (requires user lookup)
- Company
- Time period (day, week, month)

**Requirements:**
1. Handle empty lists gracefully
2. Return statistics per bucket (count, average, etc.)
3. Validate that bucket keys are valid

**Starter Code:**
```python
def bucket_activities(activities: List[CanonicalActivity], 
                     bucket_by: str) -> Dict[str, List[CanonicalActivity]]:
    """
    Group activities into buckets.
    
    Args:
        activities: List of activities
        bucket_by: "provider", "role", "company", or "time_period"
    
    Returns:
        Dictionary mapping bucket key to list of activities
    """
    # TODO: Implement
    pass
```

---

### Problem 2.2: Safe Array Operations

**Task:** Implement safe operations on activity arrays:

1. **Safe indexing:** `get_activity(activities, index)` that handles out-of-bounds
2. **Safe filtering:** `filter_by_type(activities, activity_type)` with validation
3. **Safe aggregation:** `count_by_provider(activities)` with error handling

**Requirements:**
- Never crash on invalid input
- Return meaningful error messages
- Log warnings for suspicious patterns

---

## Problem Set 3: Strings → PII Boundaries

### Problem 3.1: PII Transformation Levels

**Task:** Implement three levels of PII transformation:

```python
def transform_pii(name: str, email: str, level: str) -> Dict[str, str]:
    """
    Transform PII at different privacy levels.
    
    Args:
        name: Full name
        email: Email address
        level: "raw", "redacted", or "aggregated"
    
    Returns:
        Dictionary with transformed identity
    """
    # TODO: Implement
    pass
```

**Test Cases:**
```python
# Raw (unsafe for analysis)
result = transform_pii("John Smith", "john@company.com", "raw")
assert result["name"] == "John Smith"
assert result["email"] == "john@company.com"

# Redacted (safe for analysis)
result = transform_pii("John Smith", "john@company.com", "redacted")
assert result["name"] != "John Smith"  # Hashed
assert "@company.com" in result["email"]  # Domain preserved

# Aggregated (safe for statistics)
result = transform_pii("John Smith", "john@company.com", "aggregated")
assert "company.com" in result["domain"]
assert "name" not in result  # No individual identity
```

---

### Problem 3.2: Privacy Boundary Detection

**Task:** Write a function that detects if data contains PII boundaries:

```python
def detect_pii_boundaries(data: Dict) -> Dict[str, bool]:
    """
    Detect which fields have proper PII boundaries.
    
    Returns:
        {
            "user_id": True,      # Hashed (has boundary)
            "email": False,       # Raw (no boundary)
            "email_domain": True  # Aggregated (has boundary)
        }
    """
    # TODO: Implement
    pass
```

**Requirements:**
- Identify hashed fields (start with "entity_" or are hex strings)
- Identify aggregated fields (domains, counts, etc.)
- Flag raw PII (names, emails, etc.)

---

## Problem Set 4: Observability & Debugging

### Problem 4.1: Pipeline Tracing

**Task:** Implement a `PipelineTrace` class that tracks:

```python
class PipelineTrace:
    def __init__(self):
        self.stages = []
        self.start_time = None
        self.end_time = None
    
    def stage(self, name: str, start: bool = False, end: bool = False, **metadata):
        """Record stage start/end with metadata."""
        # TODO: Implement
        pass
    
    def explain(self) -> str:
        """Generate human-readable explanation of pipeline execution."""
        # TODO: Implement
        pass
```

**Requirements:**
1. Track all 4 stages
2. Record timing for each stage
3. Store metadata (input size, output size, errors, etc.)
4. Generate readable explanation

---

### Problem 4.2: Lens Diff

**Task:** Implement `lens_diff()` that compares outputs from all three lenses:

```python
def lens_diff(user_id: str, activities: List[CanonicalActivity]) -> Dict:
    """
    Compare how same data is interpreted by different lenses.
    
    Returns:
        {
            "user_id": user_id,
            "tribe": {...},
            "teacher": {...},
            "recon": {...},
            "differences": {
                "key_insights": [...],
                "conflicts": [...],
                "complementary": [...]
            }
        }
    """
    # TODO: Implement
    pass
```

**Requirements:**
1. Run same data through all three lenses
2. Identify where interpretations differ
3. Explain why differences are expected
4. Highlight complementary insights

---

## Problem Set 5: Quality Gates & Exit Status

### Problem 5.1: Quality Gate Implementation

**Task:** Implement quality gates for each stage:

```python
def quality_gate_ingest(df: pd.DataFrame) -> StageResult:
    """Quality gate for ingest stage."""
    # Check: file format, encoding, basic structure
    # Return: StageResult with pass/fail
    pass

def quality_gate_normalize(activities: List[CanonicalActivity]) -> StageResult:
    """Quality gate for normalize stage."""
    # Check: schema compliance, type correctness
    # Return: StageResult with pass/fail
    pass

def quality_gate_govern(activities: List[CanonicalActivity]) -> StageResult:
    """Quality gate for govern stage."""
    # Check: PII protection, governance compliance
    # Return: StageResult with pass/fail
    pass

def quality_gate_synthesize(output: Dict, lens: str) -> StageResult:
    """Quality gate for synthesize stage."""
    # Check: output validity, confidence, prohibited inferences
    # Return: StageResult with pass/fail
    pass
```

**Requirements:**
1. Each gate returns `StageResult` with exit code
2. Exit code 0 = pass, non-zero = fail
3. Include confidence scores
4. Flag when human review is required

---

### Problem 5.2: Pipeline Status Aggregation

**Task:** Write a function that aggregates all stage results:

```python
def aggregate_pipeline_status(stage_results: List[StageResult]) -> Dict:
    """
    Aggregate results from all pipeline stages.
    
    Returns:
        {
            "overall_status": "PASS" | "FAIL" | "REVIEW_REQUIRED",
            "exit_code": int,  # 0 if all pass, non-zero if any fail
            "stages": [...],
            "summary": "..."
        }
    """
    # TODO: Implement
    pass
```

**Requirements:**
1. Determine overall status from individual stages
2. Calculate aggregate exit code
3. Identify which stages need review
4. Generate human-readable summary

---

## Problem Set 6: Cryptography & Trust

### Problem 6.1: Integrity Hashing

**Task:** Implement simple integrity checking:

```python
def create_integrity_hash(data: Dict) -> str:
    """Create hash for data integrity verification."""
    # TODO: Implement
    pass

def verify_integrity(data: Dict, expected_hash: str) -> bool:
    """Verify data hasn't been tampered."""
    # TODO: Implement
    pass
```

**Test:**
```python
activity = {"user_id": "entity_123", "type": "document_share"}
hash1 = create_integrity_hash(activity)

# Verify unchanged
assert verify_integrity(activity, hash1) == True

# Verify changed
activity["type"] = "document_delete"
assert verify_integrity(activity, hash1) == False
```

---

### Problem 6.2: Trust Log Entry

**Task:** Create tamper-evident log entries:

```python
def create_trust_log_entry(event: Dict, secret_key: str) -> Dict:
    """
    Create a tamper-evident log entry.
    
    Returns:
        {
            "event": event,
            "timestamp": "...",
            "integrity_hash": "...",
            "signature": "..."  # Conceptual - use proper crypto in production
        }
    """
    # TODO: Implement
    pass

def verify_trust_log_entry(entry: Dict, public_key: str) -> bool:
    """Verify log entry hasn't been tampered."""
    # TODO: Implement
    pass
```

**Note:** For this problem set, use simple hashing. In production, use proper cryptographic signatures.

---

## Submission Guidelines

### For Each Problem Set

1. **Code:** Working implementation
2. **Tests:** At least 2 test cases per function
3. **Explanation:** Why your solution works
4. **Observability:** Show how you'd trace/debug your code

### Self-Assessment

After completing all problem sets, answer:

1. Can you trace data through all 4 stages?
2. Can you identify where integrity is enforced?
3. Can you explain why each stage matters?
4. What was the hardest concept?

**Remember:** Growth over position. Compare to your Week 1 baseline, not to others.

---

## Solutions (For Instructors)

Solutions are available in `week2_solutions.py` for instructors.

**Key Learning Points:**
- The 4-stage pipeline is non-negotiable
- Arrays teach scale and structure
- Strings teach boundaries and privacy
- Observability enables trust
- Quality gates prevent silent failures
- Cryptography enables long-term trust

---

*"Understanding the physics of data is understanding how to build trustworthy systems."*

