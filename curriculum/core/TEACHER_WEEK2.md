# TEACHER Week 2: Data Has Physics

> *"Week 2 is where CS50 stops feeling like 'learning syntax' and starts feeling like 'I now understand what the machine is actually doing.' That's exactly the moment TEACHER needs: from conceptual lenses → to trustworthy infrastructure."*

---

## Module Overview

**Duration:** 6-8 hours  
**Prerequisites:** Week 1 (Fundamentals)  
**Next:** Week 3 (Algorithms)

This week, learners discover that data has **physics** — real constraints, boundaries, and failure modes. Just as CS50 Week 2 reveals how computers actually work, TEACHER Week 2 reveals how data systems actually work.

---

## Learning Outcomes

By the end of this week, learners will be able to:

1. **Explain** why schemas + metadata are non-negotiable
2. **Understand** how text and identity are stored, bounded, and misused
3. **Recognize** system failure modes early
4. **Use** the lens model responsibly
5. **Understand** why security and education are inseparable

---

## Core Concept: The 4-Step Pipeline

### CS50's 4-Step Compilation

```
SOURCE CODE → PREPROCESS → COMPILE → ASSEMBLE → LINK → EXECUTABLE
```

### TEACHER's 4-Step Governance Pipeline

```
RAW DATA → INGEST → NORMALIZE → GOVERN → SYNTHESIZE → TRUSTED OUTPUT
```

**Key Insight:** We don't *trust* outputs unless we can name the stage where integrity was enforced.

---

### Stage 1: INGEST

**What it does:** Load raw data (CSV, audit logs, streams)

**Integrity check:** File format validation, encoding detection

**Failure mode:** Corrupted data, wrong format, missing files

**Example:**
```python
def ingest(csv_path: str) -> pd.DataFrame:
    """Stage 1: Load raw data."""
    df = pd.read_csv(csv_path, encoding='utf-8')
    validate_file_format(df)  # Integrity check
    return df
```

---

### Stage 2: NORMALIZE

**What it does:** Convert to canonical schema & types

**Integrity check:** Schema validation, type coercion, missing value handling

**Failure mode:** Type mismatches, missing required fields, inconsistent formats

**Example:**
```python
def normalize(df: pd.DataFrame) -> List[CanonicalActivity]:
    """Stage 2: Convert to canonical entities."""
    activities = []
    for row in df.itertuples():
        activity = CanonicalActivity(
            id=normalize_id(row.Uid),
            timestamp=normalize_timestamp(row.Date),
            activity_type=normalize_string(row.Type),
            # ... strict typing enforced
        )
        validate_activity(activity)  # Integrity check
        activities.append(activity)
    return activities
```

---

### Stage 3: GOVERN

**What it does:** Apply PII abstraction + role gates + bias checks

**Integrity check:** PII hashing, governance rules, prohibited inference checks

**Failure mode:** Privacy leakage, bias amplification, unauthorized access

**Example:**
```python
def govern(activities: List[CanonicalActivity]) -> List[CanonicalActivity]:
    """Stage 3: Apply governance."""
    # PII protection
    safe_activities = apply_pii_protection(activities)
    
    # Governance checks
    gov_report = governance_gate.run_full_check(safe_activities)
    if not gov_report.overall_passed:
        raise GovernanceError("Governance check failed")
    
    return safe_activities
```

---

### Stage 4: SYNTHESIZE

**What it does:** Generate TRIBE/TEACHER/RECON outputs

**Integrity check:** Output validation, confidence scores, review flags

**Failure mode:** Hallucinated structures, invalid recommendations, unsafe inferences

**Example:**
```python
def synthesize(activities: List[CanonicalActivity], lens: str) -> Dict:
    """Stage 4: Generate outputs."""
    if lens == "tribe":
        return extract_tribe(activities)
    elif lens == "teacher":
        return extract_teacher(activities)
    elif lens == "recon":
        return extract_recon(activities)
    else:
        raise ValueError(f"Unknown lens: {lens}")
```

---

## Arrays → Canonical Entity Collections

Arrays are the first time students feel: **"I can handle a lot of data cleanly."**

### The Parallel

| CS50 Concept | TEACHER Equivalent | Why It Matters |
|--------------|-------------------|----------------|
| **Array declaration** | Entity collection initialization | Explicit structure |
| **Contiguity** | Consistent schema | Predictable access |
| **Indexing** | Stable identity keys | Reliable lookups |
| **Length must be passed** | Metadata must be explicit | Prevent structural lies |
| **Bounds checking** | Schema validation | Catch errors early |

### Example: Activity Array

```python
# CS50-style thinking
activities: List[CanonicalActivity] = []  # Array declaration
for row in data:
    activity = create_activity(row)      # Type-safe creation
    activities.append(activity)          # Bounds-checked append

# Length is explicit (not hidden)
activity_count = len(activities)         # Metadata is explicit

# Safe iteration
for i in range(len(activities)):         # Bounds-checked access
    process(activities[i])
```

**Key Lesson:** 
> "If you don't track length in C, you crash.  
> If you don't track metadata in AI, you hallucinate structure."

---

## Strings → Identity, PII, and "The Hidden Byte"

The **NUL terminator** (`\0`) is the perfect metaphor for privacy boundaries.

### The Hidden Boundary

A string looks simple, but it has:
- **A hidden boundary marker** (`\0`)
- **A required rule for safe interpretation**

So TEACHER teaches:

> "Human identity data *also* has invisible boundaries.  
> You must mark what can be exposed, redacted, or aggregated."

### PII Sentinel Rules

```python
# Raw identity (unsafe)
user_name = "John Smith"  # No boundary marker

# Redacted identity (safe)
user_id = hash_pii("John Smith")  # Boundary: hashed
user_id = "entity_abc123"         # Boundary: pseudonymized

# Aggregated identity (safe for analysis)
user_domain = "smith@company.com".split('@')[1]  # Boundary: domain only
```

### Privacy-by-Schema

```python
@dataclass
class CanonicalUser:
    id: str                    # REQUIRED: Hashed boundary
    email_domain: str          # SAFE: Aggregated boundary
    # name: str                # PROHIBITED: No boundary protection
    # email: str               # PROHIBITED: Direct PII
```

**Key Lesson:**
> "Just as C requires `\0` to safely read strings,  
> TEACHER requires PII boundaries to safely process identity."

---

## Debugging → Observability & Auditability

### CS50's Debugging Evolution

**printf debugging** → Ad hoc inspection  
**debug50** → Structured stepping with state visibility

### TEACHER's Observability Evolution

**Quick logs** → Ad hoc inspection  
**Full observable pipeline** → Structured tracing with state visibility

### Pipeline Observability

```python
class ObservablePipeline:
    """Pipeline with full observability."""
    
    def run(self, data, lens):
        trace = PipelineTrace()
        
        # Stage 1: INGEST
        trace.stage("ingest", start=True)
        raw_data = self.ingest(data)
        trace.stage("ingest", end=True, output_size=len(raw_data))
        
        # Stage 2: NORMALIZE
        trace.stage("normalize", start=True)
        normalized = self.normalize(raw_data)
        trace.stage("normalize", end=True, 
                   entities_created=len(normalized),
                   validation_errors=self.validation_errors)
        
        # Stage 3: GOVERN
        trace.stage("govern", start=True)
        governed = self.govern(normalized)
        trace.stage("govern", end=True,
                   pii_hashed=self.pii_count,
                   governance_passed=self.gov_check_passed)
        
        # Stage 4: SYNTHESIZE
        trace.stage("synthesize", start=True, lens=lens)
        output = self.synthesize(governed, lens)
        trace.stage("synthesize", end=True,
                   output_confidence=output['confidence'],
                   review_required=output['review_required'])
        
        return output, trace
```

### Lens Diff (Why Was This Generated?)

```python
def explain_recommendation(user_id: str, recommendation: Dict) -> Dict:
    """Explain why a recommendation was generated."""
    return {
        "user_id": user_id,
        "recommendation": recommendation,
        "reasoning": {
            "baseline_skills": get_baseline_skills(user_id),
            "peer_comparison": compare_to_peers(user_id),
            "role_requirements": get_role_requirements(user_id),
            "gap_identified": identify_gap(user_id),
            "confidence": calculate_confidence(user_id, recommendation)
        },
        "governance": {
            "bias_guardrails_applied": True,
            "no_performance_inference": True,
            "self_relative_only": True
        }
    }
```

**Key Lesson:**
> "A black box mentor is not safe.  
> A guided, explainable mentor can be trusted."

---

## Command-Line Arguments → Lens Selection API

### CS50's Model

```c
int main(int argc, string argv[])
```

### TEACHER's Model

A clean mental model:
- The user passes the **lens**
- The system returns the **interpretation**

### Conceptual CLI

```bash
# Single lens
teacher run --lens tribe
teacher run --lens teacher
teacher run --lens recon

# Multiple lenses
teacher run --lens tribe --lens teacher --lens recon

# With options
teacher run --lens tribe --output json --verbose
```

### Python API

```python
from teacher import Pipeline

pipeline = Pipeline()

# Run single lens
tribe_output = pipeline.run(data, lens="tribe")

# Run all lenses
all_outputs = pipeline.run(data, lens=["tribe", "teacher", "recon"])

# With observability
output, trace = pipeline.run_observable(data, lens="teacher")
print(trace.explain())
```

**Key Lesson:**
> "Same data, different truth-views.  
> The lens is the argument. The output is the interpretation."

---

## Exit Status → Quality Gates

### CS50's Model

- `0` = success
- Non-zero = error

### TEACHER's Model

Every stage returns:
- **Pass/fail** + reason
- **Confidence band** (0.0-1.0)
- **Required human review flag**

```python
@dataclass
class StageResult:
    """Result of a pipeline stage."""
    stage_name: str
    passed: bool
    exit_code: int  # 0 = success, non-zero = error
    confidence: float  # 0.0-1.0
    review_required: bool
    reason: str
    metadata: Dict[str, Any]
    
    def to_dict(self) -> Dict:
        return {
            "stage": self.stage_name,
            "status": "PASS" if self.passed else "FAIL",
            "exit_code": self.exit_code,
            "confidence": self.confidence,
            "review_required": self.review_required,
            "reason": self.reason,
            "metadata": self.metadata
        }
```

### Quality Gate Example

```python
def check_quality(output: Dict, lens: str) -> StageResult:
    """Quality gate for synthesized output."""
    
    # Check confidence
    confidence = output.get('confidence', 0.0)
    if confidence < 0.7:
        return StageResult(
            stage_name="quality_gate",
            passed=False,
            exit_code=1,
            confidence=confidence,
            review_required=True,
            reason="Low confidence output requires human review"
        )
    
    # Check for prohibited inferences
    if 'performance_score' in output:
        return StageResult(
            stage_name="quality_gate",
            passed=False,
            exit_code=2,
            confidence=0.0,
            review_required=True,
            reason="Prohibited inference detected: performance_score"
        )
    
    # Pass
    return StageResult(
        stage_name="quality_gate",
        passed=True,
        exit_code=0,
        confidence=confidence,
        review_required=False,
        reason="All quality checks passed"
    )
```

**Key Lesson:**
> "No silent failure in high-stakes education.  
> Every stage must declare its status explicitly."

---

## Cryptography → Provenance & Tamper-Evident Logs

Week 2's crypto isn't just "cool." It's your **trust infrastructure** for TEACHER.

### The Big Idea

> "Meaning + key + mechanism = protected truth."

### Applications

1. **Signed Learning Events**
   ```python
   def sign_learning_event(event: Dict, private_key: str) -> str:
       """Sign a learning event for tamper detection."""
       event_hash = hash_event(event)
       signature = sign_with_key(event_hash, private_key)
       return signature
   ```

2. **Tamper-Evident Mentorship Logs**
   ```python
   def verify_mentorship_log(log_entry: Dict, signature: str, public_key: str) -> bool:
       """Verify mentorship log hasn't been tampered."""
       event_hash = hash_event(log_entry)
       return verify_signature(event_hash, signature, public_key)
   ```

3. **Privacy-Preserving Analytics**
   ```python
   def aggregate_with_privacy(user_data: List[Dict]) -> Dict:
       """Aggregate data while preserving privacy."""
       # Differential privacy, homomorphic encryption, etc.
       pass
   ```

4. **Provider Integrity Scoring**
   ```python
   def score_provider_integrity(provider: Provider) -> float:
       """Score provider based on cryptographic proofs of service."""
       # Verify service claims cryptographically
       pass
   ```

### Simple Example: Hash-Based Integrity

```python
import hashlib

def create_integrity_hash(data: Dict) -> str:
    """Create integrity hash for data."""
    data_str = json.dumps(data, sort_keys=True)
    return hashlib.sha256(data_str.encode()).hexdigest()

def verify_integrity(data: Dict, expected_hash: str) -> bool:
    """Verify data integrity."""
    actual_hash = create_integrity_hash(data)
    return actual_hash == expected_hash

# Usage
activity = {"user_id": "entity_123", "type": "document_share"}
hash_value = create_integrity_hash(activity)

# Later, verify it hasn't changed
if verify_integrity(activity, hash_value):
    print("Data integrity verified")
else:
    print("WARNING: Data may have been tampered")
```

**Key Lesson:**
> "Cryptography enables long-term trust.  
> Without it, you can't prove what happened or who said what."

---

## Micro-Labs (CS50-Style)

### Lab 1: Reading Level → Org Clarity Index

**Objective:** Convert CS50's reading level demo into policy clarity scoring

**CS50 Version:**
```c
// Calculate reading level of text
int calculate_reading_level(string text);
```

**TEACHER Version:**
```python
def calculate_policy_clarity(policy_text: str) -> Dict[str, Any]:
    """
    Calculate clarity index for organizational policies.
    
    Returns:
        {
            "clarity_score": float,  # 0-100
            "reading_level": str,     # "accessible", "moderate", "complex"
            "recommendations": List[str]
        }
    """
    # Count sentences, words, syllables
    # Calculate readability metrics
    # Return clarity assessment
    pass
```

**Task:**
1. Implement `calculate_policy_clarity()`
2. Test on sample policy documents
3. Generate recommendations for improvement

---

### Lab 2: Array Lab → Activity Buckets

**Objective:** Group activities by provider, role, and company

**CS50 Thinking:**
```c
// Count occurrences in array
int count_occurrences(int array[], int length, int value);
```

**TEACHER Thinking:**
```python
def bucket_activities(activities: List[CanonicalActivity], 
                     bucket_by: str) -> Dict[str, List[CanonicalActivity]]:
    """
    Group activities into buckets.
    
    Args:
        activities: List of activities
        bucket_by: "provider", "role", or "company"
    
    Returns:
        Dictionary mapping bucket key to list of activities
    """
    buckets = {}
    
    for activity in activities:
        if bucket_by == "provider":
            key = activity.provider_id
        elif bucket_by == "role":
            key = activity.user_role  # Would need to look up
        elif bucket_by == "company":
            key = activity.company_id
        else:
            raise ValueError(f"Unknown bucket: {bucket_by}")
        
        if key not in buckets:
            buckets[key] = []
        buckets[key].append(activity)
    
    return buckets
```

**Task:**
1. Implement `bucket_activities()`
2. Write tests for each bucket type
3. Calculate statistics per bucket (count, average, etc.)

---

### Lab 3: String Lab → PII Rules

**Objective:** Show raw identity → redacted identity → aggregated identity

**CS50 Thinking:**
```c
// String manipulation
string capitalize(string word);
string redact(string text, int start, int length);
```

**TEACHER Thinking:**
```python
def demonstrate_pii_levels(name: str, email: str) -> Dict[str, str]:
    """
    Show identity at different privacy levels.
    
    Returns:
        {
            "raw": "John Smith <john@company.com>",
            "redacted": "entity_abc123 <entity_abc123@company.com>",
            "aggregated": "User in company.com domain"
        }
    """
    return {
        "raw": f"{name} <{email}>",
        "redacted": f"{hash_pii(name)} <{hash_pii(email.split('@')[0])}@{email.split('@')[1]}>",
        "aggregated": f"User in {email.split('@')[1]} domain"
    }
```

**Task:**
1. Implement PII transformation functions
2. Show all three levels for sample data
3. Explain when each level is appropriate

---

### Lab 4: Debug Lab → Lens Diff

**Objective:** Same user, same dataset → three different outputs

**CS50 Thinking:**
```c
// Debug by comparing outputs
void compare_outputs(int result1, int result2);
```

**TEACHER Thinking:**
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
                "recommendations": [...]
            }
        }
    """
    tribe_output = extract_tribe(user_id, activities)
    teacher_output = extract_teacher(user_id, activities)
    recon_output = extract_recon(user_id, activities)
    
    return {
        "user_id": user_id,
        "tribe": tribe_output,
        "teacher": teacher_output,
        "recon": recon_output,
        "differences": analyze_differences(tribe_output, teacher_output, recon_output)
    }
```

**Task:**
1. Run same data through all three lenses
2. Identify where interpretations diverge
3. Explain why divergence is expected and valuable

---

### Lab 5: Crypto Lab → Trust Log

**Objective:** Introduce simple signatures conceptually

**CS50 Thinking:**
```c
// Simple Caesar cipher
string encrypt(string plaintext, int key);
```

**TEACHER Thinking:**
```python
def create_trust_log_entry(event: Dict, secret_key: str) -> Dict:
    """
    Create a tamper-evident log entry.
    
    Returns:
        {
            "event": event,
            "timestamp": "...",
            "integrity_hash": "...",
            "signature": "..."
        }
    """
    entry = {
        "event": event,
        "timestamp": datetime.now().isoformat(),
        "integrity_hash": hash_event(event)
    }
    
    # Simple signature (conceptual - use proper crypto in production)
    entry["signature"] = sign_event(entry, secret_key)
    
    return entry

def verify_trust_log_entry(entry: Dict, public_key: str) -> bool:
    """Verify log entry hasn't been tampered."""
    return verify_signature(entry, public_key)
```

**Task:**
1. Implement simple hash-based integrity checking
2. Create and verify trust log entries
3. Demonstrate tamper detection

---

## Assessment: Self-Relative Growth

### Baseline (Before Week 2)

**Question:** "Can you explain what happens to data in a pipeline?"

**Expected Response:**
- Basic understanding of input → output
- May not see intermediate stages
- May not understand governance requirements

### After Week 2

**Question:** "Can you trace data through all four stages and explain where integrity is enforced?"

**Expected Response:**
- Can name all four stages
- Can explain what happens at each stage
- Can identify where governance is applied
- Can explain why each stage matters

### Evaluation Criteria

**NOT evaluated:**
- Speed of implementation
- Complexity of code
- Comparison to peers

**Evaluated:**
- Growth from baseline
- Understanding of pipeline stages
- Ability to explain integrity enforcement
- Recognition of failure modes

---

## Mini Capstone: Build an Observable Pipeline

**Objective:** Build a complete 4-stage pipeline with full observability

**Requirements:**
1. Implement all 4 stages (Ingest, Normalize, Govern, Synthesize)
2. Add observability/tracing to each stage
3. Implement quality gates with exit codes
4. Generate lens diff for sample data
5. Document where integrity is enforced

**Deliverable:**
- Working pipeline code
- Trace output showing all stages
- Quality gate results
- Documentation explaining integrity enforcement points

---

## Key Takeaways

1. **Data has physics.** Real constraints, boundaries, and failure modes.

2. **The 4-stage pipeline is non-negotiable.** Each stage enforces integrity.

3. **Arrays teach scale.** Canonical entity collections enable clean data handling.

4. **Strings teach boundaries.** PII requires explicit privacy boundaries.

5. **Debugging teaches trust.** Observability enables explainable AI.

6. **Exit status teaches safety.** Quality gates prevent silent failures.

7. **Cryptography teaches provenance.** Long-term trust requires tamper-evident logs.

---

## Next Steps

**Week 3:** Algorithms
- Collaboration strength algorithms
- Role mastery profiling
- Provider reliability scoring
- The first real MVP extractors

**For Now:** Practice the 4-stage pipeline:
- `ingest` → `normalize` → `govern` → `synthesize`

---

## Resources

- **pipeline.py:** See the 4-stage pipeline in action
- **governance.py:** See governance rules as code
- **ingestion.py:** See normalization in detail
- **mvp_extractors.py:** See synthesis (preview of Week 3)

---

*"Week 1 was 'We can build this.' Week 2 is 'We can make this safe, explainable, and scalable.' Welcome to infrastructure."*

