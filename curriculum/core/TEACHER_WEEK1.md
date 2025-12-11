# TEACHER Week 1: From Visual Truth to Formal Truth

> *"The jump from Scratch to C is the jump from visual intuition to formal rigor. The jump from Scratch-for-Data to governed pipelines is the same jump — and it's where trust begins."*

---

## Module Overview

**Duration:** 5-7 hours  
**Prerequisites:** Week 0 (Concepts)  
**Next:** Week 2 (Data Structures)

This week, learners make the critical transition from:
- **Visual understanding** → **Formal specification**
- **Intuition** → **Repeatable, testable systems**
- **"I think this works"** → **"I can prove this is safe"**

Just as CS50 Week 1 introduces C after Scratch, TEACHER Week 1 introduces **governed canonical systems** after visual pipeline building.

---

## Learning Outcomes

By the end of this week, learners will be able to:

1. **Explain** why governance is the "compiler" of safe AI systems
2. **Identify** canonical entities in activity logs
3. **Understand** why types and schemas prevent real-world failures
4. **Build** or assemble a basic lens pipeline
5. **Recognize** system limits and why guardrails exist

---

## Core Concept: The Translation

### CS50's Translation

```
SOURCE CODE → COMPILER → MACHINE CODE
```

### TEACHER's Translation

```
HUMAN INTENT → GOVERNED MODEL → DEPLOYABLE OUTPUT
```

Where:
- **Human Intent** = What the user *means* (TRIBE/TEACHER/RECON lens choice)
- **Governed Model** = Policy + PII abstraction + role safety checks
- **Deployable Output** = Dashboards, graphs, scores, recommendations

**Key Insight:** The "compiler" is governance + validation. Without it, you have fast but unsafe outputs. With it, you have trustworthy intelligence.

##### Inspiration: The Foundation of Understanding

> *"Wisdom is the principal thing; therefore get wisdom: and with all thy getting get understanding."*
> 
> — Proverbs 4:7

**Connection:** Data dictionary provides understanding—the foundation of wisdom. Without clear schemas, we have confusion. With understanding, we have wisdom.

> *"The beginning is the most important part of the work."*
> 
> — Plato

**Connection:** The data dictionary is the beginning. Without clear schemas, nothing else can be built correctly. Week 1 sets the foundation for all that follows.

> *"A good decision is based on knowledge and not on numbers."*
> 
> — Plato

**Connection:** A good data dictionary is based on knowledge (understanding what fields mean), not just numbers (raw data). Understanding precedes analysis.

> *"I saw the angel in the marble and carved until I set him free."*
> 
> — Michelangelo

**Connection:** The data dictionary helps us see the "angel" (meaning) in the "marble" (raw data). We carve (analyze) until we set meaning free.

##### Alternative Perspectives: How Other Thinkers Would Build Foundations

**The Problem:** How do we create a solid foundation for data understanding? What makes a good data dictionary?

**Plato's Approach (The Beginning Matters Most):**
> *"The beginning is the most important part of the work."*
> 
> — Plato

Plato would say: The data dictionary is the beginning—it sets the foundation for all understanding. Without clear schemas, nothing else can be built correctly. Week 1 sets the foundation for all that follows. Get the beginning right, and the rest follows.

**Aristotle's Approach (Knowledge Over Numbers):**
> *"A good decision is based on knowledge and not on numbers."*
> 
> — Plato (but Aristotle would agree)

Aristotle would say: A good data dictionary is based on knowledge (understanding what fields mean), not just numbers (raw data). Understanding precedes analysis. We must know what data represents before we can use it wisely.

**Michelangelo's Approach (Revealing Hidden Meaning):**
> *"I saw the angel in the marble and carved until I set him free."*
> 
> — Michelangelo

Michelangelo would say: The meaning isn't created—it's already there, waiting to be revealed. The data dictionary helps us see the "angel" (meaning) in the "marble" (raw data). We "carve" (analyze) until we set meaning free. The foundation reveals what's hidden.

**Biblical Perspective (Wisdom and Understanding):**
> *"Wisdom is the principal thing; therefore get wisdom: and with all thy getting get understanding."*
> 
> — Proverbs 4:7

The biblical view: Data dictionary provides understanding—the foundation of wisdom. Without clear schemas, we have confusion. With understanding, we have wisdom. The foundation enables wisdom.

**Synthesis:** All four perspectives agree: the foundation (data dictionary) is crucial. Plato emphasizes getting the beginning right, Aristotle emphasizes knowledge over numbers, Michelangelo emphasizes revealing hidden meaning, and the biblical view emphasizes wisdom through understanding. Together, they teach us that Week 1's foundation enables all that follows.

---

## The Three Commands

Just as CS50 has `code`, `make`, `./`, TEACHER has:

### 1. `define models`

**What it does:** Define canonical entities with strict schemas

**Example:**
```python
@dataclass
class CanonicalUser:
    id: str                    # Hashed for privacy
    company_id: str
    roles: List[str]
    activity_count: int
```

**Why it matters:** Without formal models, "user" might mean different things in different contexts. With models, we have shared truth.

### 2. `build pipeline`

**What it does:** Assemble validation → PII gate → Entity mapping → Graph building → Extractors

**Example:**
```
CSV Upload → PII Redaction → Normalize → Map Entities → Build Graph → Extract Insights
```

**Why it matters:** Pipelines are repeatable. One person's pipeline works for everyone.

### 3. `run lens`

**What it does:** Generate TRIBE, TEACHER, or RECON outputs from the same data

**Example:**
```bash
run lens --tribe    # Network analysis
run lens --teacher  # Learning pathways
run lens --recon     # Value exchange
```

**Why it matters:** Same data, three perspectives, one unified system.

---

## CS50 Concepts → TEACHER Primitives

| CS50 Week 1 Concept | TEACHER Equivalent | What It Enables |
|---------------------|-------------------|-----------------|
| **Source vs Machine Code** | Intent vs Governed Output | Trustable AI decisions |
| **Compiler** | Governance Gate + Validation | Safe deployment |
| **Data Types** | Canonical entities + strict schemas | Less ambiguity, fewer errors |
| **Functions** | Extractors (`mentor_finder()`, `silo_detector()`) | Modular, reusable logic |
| **Loops** | Batch + streaming analytics | Enterprise-ready processing |
| **Conditionals** | Policy decisions (`if external_user then restrict`) | Security-native logic |
| **Scope** | Least privilege boundaries | Perfect security analogy |
| **Overflow/Imprecision** | Bias/Drift/Metric traps | Long-term safety |

---

## The Seven Canonical Entities

Just as C has fundamental types (`int`, `char`, `float`), TEACHER has seven canonical entities:

### 1. **User**
A person in the system (hashed for privacy)

```python
CanonicalUser(
    id="entity_abc123",      # Hashed UID
    company_id="org_xyz",
    roles=["data_analyst"],
    activity_count=450
)
```

### 2. **Company**
An organization

```python
CanonicalCompany(
    id="org_xyz",
    name="TechCorp Inc",
    user_count=150,
    activity_count=5000
)
```

### 3. **Group**
A team within an organization

```python
CanonicalGroup(
    id="team_alpha",
    company_id="org_xyz",
    member_count=12
)
```

### 4. **Provider**
A service/tool supplier

```python
CanonicalProvider(
    id="provider_aws",
    name="Amazon Web Services",
    reliability_score=0.998,
    customer_count=45
)
```

### 5. **Resource**
A file, API, or digital asset

```python
CanonicalResource(
    id="doc_xyz789",
    path_pattern="/projects/DIR_1/FILE_2.pdf",  # Masked
    access_count=23
)
```

### 6. **Activity**
An event that happened

```python
CanonicalActivity(
    timestamp="2024-01-15T10:30:00Z",
    activity_type="document_access",
    user_id="entity_abc123",
    resource_id="doc_xyz789"
)
```

### 7. **PermissionChange**
A change in access rights

```python
CanonicalPermissionChange(
    user_id="entity_abc123",
    state_before="viewer",
    state_after="editor",
    timestamp="2024-01-15T10:30:00Z"
)
```

**Key Insight:** These seven entities can represent any activity log. They're the "alphabet" of our system.

---

## System Limits: Why Guardrails Exist

CS50 teaches that computers have limits:
- **Overflow:** Numbers too large
- **Truncation:** Precision loss
- **Imprecision:** Floating-point errors

TEACHER teaches that data systems have limits:
- **Bias Amplification:** Small biases become large over time
- **Missing Context:** Data doesn't tell the whole story
- **Metric Gaming:** People optimize for what's measured
- **Data Drift:** Patterns change over time
- **Privacy Leakage:** Quasi-identifiers combine to reveal individuals

**The Solution:** Design for limits from the start.

---

## Micro-Labs (CS50-Style Problem Sets)

### Lab 1: Hello, World (Data Edition)

**Objective:** Interpret a single activity row through three lenses

**Input:**
```json
{
  "Uid": "user_123",
  "UidOpp": "user_456",
  "Type": "document_share",
  "Date": "2024-01-15T10:30:00Z",
  "CompanyId": "org_abc",
  "StateOld": "viewer",
  "StateNew": "editor"
}
```

**Task:** Write three interpretations:

1. **TRIBE interpretation:**
   ```
   "User user_123 shared a document with user_456. 
   This creates a collaboration edge between them."
   ```

2. **TEACHER interpretation:**
   ```
   "User user_123 upgraded from 'viewer' to 'editor' permissions.
   This represents skill growth: consuming → creating."
   ```

3. **RECON interpretation:**
   ```
   "A permission change occurred within org_abc.
   This is a value exchange: the platform enabled capability growth."
   ```

**Success Criteria:**
- [ ] Can identify which fields matter for each lens
- [ ] Understands that same data = different meanings
- [ ] Can explain why context matters

---

### Lab 2: Type Safety Lab

**Objective:** Show how sloppy typing breaks analytics

**Scenario 1: The Broken Pipeline**

```python
# BAD: Everything is a string
user_id = row["Uid"]  # Could be "123", "user_123", or 123
company_id = row["CompanyId"]  # Could be "org_1" or 1

# This breaks:
if user_id == 123:  # Never matches if it's a string!
    process_user()
```

**Scenario 2: The Fixed Pipeline**

```python
# GOOD: Canonical types
@dataclass
class CanonicalUser:
    id: str  # Always a string, always hashed
    company_id: str  # Always a string, always normalized

# This works:
user = CanonicalUser(id=hash_value("123"), company_id="org_1")
if user.company_id == "org_1":
    process_user()
```

**Task:** 
1. Identify 3 type-related bugs in a sample pipeline
2. Fix them using canonical entities
3. Explain why strict types prevent errors

**Success Criteria:**
- [ ] Can identify type mismatches
- [ ] Can apply canonical entity schemas
- [ ] Understands why "everything is a string" is dangerous

---

### Lab 3: Function Lab

**Objective:** Implement a single extractor function

**Task:** Write `collaboration_strength(user_a, user_b, activities)`

**Requirements:**
- Takes two user IDs and a list of activities
- Returns a score from 0.0 to 1.0
- Considers:
  - Direct interactions (UidOpp/UidReq)
  - Co-resource access (same file on same day)
  - Shared group membership

**Starter Code:**
```python
def collaboration_strength(user_a: str, user_b: str, 
                          activities: List[CanonicalActivity]) -> float:
    """
    Calculate collaboration strength between two users.
    
    Returns:
        float: Score from 0.0 (no collaboration) to 1.0 (strong collaboration)
    """
    # TODO: Implement
    return 0.0
```

**Test Cases:**
```python
# Test 1: No interactions
assert collaboration_strength("user_1", "user_2", []) == 0.0

# Test 2: One direct interaction
activities = [CanonicalActivity(
    user_id="user_1",
    target_user_id="user_2",
    activity_type="document_share"
)]
assert collaboration_strength("user_1", "user_2", activities) > 0.0

# Test 3: Multiple interactions
# (Add more test cases)
```

**Success Criteria:**
- [ ] Function compiles/runs without errors
- [ ] Returns scores in valid range (0.0-1.0)
- [ ] Handles edge cases (empty lists, same user, etc.)
- [ ] Can explain the algorithm

---

### Lab 4: Limits Lab

**Objective:** Understand when high activity might mean burnout, not engagement

**Scenario:** A user has 1,000 activities in one week.

**Question 1: What could this mean?**

**Possible Interpretations:**
- ✅ High engagement (they're very active)
- ⚠️ Role requirement (their job requires high activity)
- ⚠️ Burnout indicator (they're working too much)
- ⚠️ Automation (a bot, not a person)
- ⚠️ Error logging (system errors, not real activity)

**Question 2: How do we know which it is?**

**Answer:** We need context:
- Compare to role baseline (is this normal for their role?)
- Check activity types (are they all errors?)
- Look at time patterns (are they working 24/7?)
- Check for automation signatures

**Question 3: What's the governance rule?**

**Answer:** 
```
NEVER infer individual performance from activity volume alone.
ALWAYS compare to role/context baselines.
ALWAYS flag anomalies for human review (10th Man check).
```

**Task:**
1. Write a governance rule that prevents misinterpreting high activity
2. Explain why this rule exists
3. Give an example of when the rule would trigger

**Success Criteria:**
- [ ] Can identify multiple interpretations of the same metric
- [ ] Understands why context matters
- [ ] Can write a governance rule to prevent misinterpretation
---

### Lab 5: Noise vs. Signal (AI Triage Edition)

**Objective:** Separate useful findings from AI-generated noise.

**Scenario:** An auto-triage system floods your queue with 200 “critical” alerts in one hour.

**Tasks:**
1. Write a quick filter that:
   - Drops duplicates by hash of summary.
   - Buckets by component/path.
   - Flags items lacking minimal evidence.
2. Set a rule: when to escalate to human review vs. auto-close.
3. Add one guardrail to reduce future noise (rate limit, auth, provenance tagging).

**Success Criteria:**
- [ ] Clear filter logic
- [ ] Human-review threshold set
- [ ] Preventive guardrail added

---

### Lab 6: Passive Recon & Responsible Disclosure (OSINT-Only)

**Objective:** Practice ethical, passive reconnaissance and turn it into a defender brief without touching live targets beyond public pages.

**Scenario:** You are given a sanitized list of public login URLs/domains (no credentials, no testing permission). You must stay passive and prepare a defender-ready summary.

**Tasks:**
1. Normalize and dedupe the list (lowercase, `sort -u`), prefer `https://` in outputs.
2. Passive-only data collection (allowed): fetch headers, `robots.txt`, and page titles with a polite user agent and rate limits. Disallowed: form posts, fuzzing, auth attempts, “dork” probes against production targets.
3. Extract for each host: `host`, HTTP status, final redirect (if any), HSTS present?, `robots.txt` present?, page title.
4. Tag each host: sector (finance/edu/gov), auth surface (login present, OAuth redirect), TLS posture (http/https, HSTS yes/no), typosquat/suspect (e.g., infintty.com vs. infinity.com).
5. Write a 1-page defender brief: likely attacker goals, top mitigations (MFA, rate limits, WAF rules for POST /login, bot detection), and a detection rule sketch for unusual POST volume to `/login`.
6. Draft a responsible disclosure email template for a hypothetical finding (passive only) with scope, evidence, and a stop-on-request clause.

**Success Criteria:**
- [ ] Stayed within passive rules; no active testing attempted
- [ ] CSV/summary includes required fields (host, status, redirect, HSTS, robots, title)
- [ ] Clear tags for sector/auth/TLS/typosquat
- [ ] Defender brief lists attacker goals + concrete mitigations + a detection rule
- [ ] Disclosure draft is respectful, scoped, and non-threatening

**Story riff (optional reflection, 10–15 min):** Imagine a tiny, three-person “cell” that only shares what is necessary. One teammate pulls public signals (headers/titles), one tags risks, one drafts the disclosure. None of them touches forms or credentials. Each keeps a narrow view to reduce blast radius—and all roads lead to a single, transparent defender brief. What did compartmentalization buy you? Where did it slow you down? How would you keep it ethical and passive if the list doubled in size?

---

### Challenge: Attribution Chain

**Objective:** Ensure credit and traceability for fixes.

**Tasks:**
1. Given a finding ID and a patch PR, draft the minimal audit log entry linking:
   - Finding ID
   - Patch commit
   - Reporter/credit
   - Triage decision (accepted/rejected) with timestamp
2. Explain why this prevents AI-washing and IP disputes. (This is the single source of truth that Chapter 11 references.)

**Success Criteria:**
- [ ] Complete linkage fields
- [ ] Clear rationale on IP/attribution

---

## The Three-Lens "Hello, World" Demo

This is your **investor demo** and **student onboarding** moment.

### Demo Script

**Step 1: Show the Data**
```json
{
  "Uid": "user_alice",
  "UidOpp": "user_bob",
  "Type": "document_share",
  "Date": "2024-01-15T10:30:00Z",
  "CompanyId": "org_techcorp",
  "StateOld": "viewer",
  "StateNew": "editor"
}
```

**Step 2: Run Through Three Lenses**

**🌐 TRIBE Lens:**
> "Alice shared a document with Bob. This creates a collaboration edge. If we see this pattern repeated, we know Alice and Bob work together. We can build a network graph showing who collaborates with whom."

**📚 TEACHER Lens:**
> "Alice's permission changed from 'viewer' to 'editor'. This is skill growth. She went from consuming information to creating it. If we track these state transitions, we can build learning pathways."

**💱 RECON Lens:**
> "A permission change occurred. The platform enabled this capability. If we track these changes across many users, we can score providers: which platforms enable growth? Which have friction?"

**Step 3: The Punchline**
> "Same data. Three perspectives. One unified system. That's COSURVIVAL."

---

## Assessment: Self-Relative Growth

### Baseline (Before Week 1)

**Question:** "Can you interpret a single activity row?"

**Expected Response:** 
- Can identify basic fields (user, timestamp, type)
- May not see multiple interpretations
- May not understand governance implications

### After Week 1

**Question:** "Can you explain why your interpretation is safe?"

**Expected Response:**
- Can identify which lens applies
- Can explain governance rules that protect privacy
- Can recognize when interpretation might be biased
- Can write a simple extractor function

### Evaluation Criteria

**NOT evaluated:**
- Speed relative to peers
- "Correctness" of interpretation
- Complexity of code

**Evaluated:**
- Growth from baseline
- Understanding of governance principles
- Ability to explain decisions
- Recognition of system limits

---

## Mini Capstone: Build Your First Pipeline

**Objective:** Assemble a complete pipeline from scratch

**Requirements:**
1. Define at least 3 canonical entities
2. Write one extractor function
3. Apply at least one governance rule
4. Generate outputs for at least one lens

**Deliverable:**
- Code (or visual pipeline in Scratch-for-Data)
- Documentation explaining:
  - What your pipeline does
  - Why it's safe (governance)
  - What it outputs (which lens)

**Example Output:**
```python
# Define entities
users = extract_users(activities)
companies = extract_companies(activities)

# Apply governance
safe_users = apply_pii_protection(users)

# Build graph
graph = build_tribe_graph(safe_users, activities)

# Extract insights
mentors = find_mentor_candidates(graph)

# Output
print(f"Found {len(mentors)} mentor candidates")
```

---

## Key Takeaways

1. **Governance is the compiler.** Without it, you have fast but unsafe outputs.

2. **Canonical entities are the primitives.** Just as C has `int` and `char`, TEACHER has `User` and `Activity`.

3. **Types prevent errors.** Strict schemas catch bugs before they become problems.

4. **System limits are real.** Design for bias, drift, and privacy leakage from the start.

5. **Same data, three lenses.** TRIBE, TEACHER, and RECON are perspectives, not separate systems.

---

## Next Steps

**Week 2:** Data Structures
- Event stores
- Graph representations
- Schema validation

**For Now:** Practice the three commands:
- `define models`
- `build pipeline`
- `run lens`

---

## Resources

- **Scratch-for-Data:** Visual pipeline builder
- **governance.py:** See governance rules in code
- **models.py:** See canonical entities
- **mvp_extractors.py:** See extractor functions

---

*"The jump from visual to formal is where trust begins. Welcome to Week 1."*

