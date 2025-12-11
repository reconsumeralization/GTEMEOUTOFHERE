# TEACHER Week 1: Problem Sets

> *"Practice is where intuition becomes skill."*

---

## Problem Set 1: Type Safety

### Problem 1.1: The Broken Pipeline

You're given this code:

```python
def process_user(row):
    user_id = row["Uid"]
    company_id = row["CompanyId"]
    
    if user_id == 123:
        print("Processing user 123")
    
    if company_id == "org_1":
        print("User is in org_1")
```

**Question:** Why might this code fail? What types of errors could occur?

**Hint:** What if `Uid` is the string `"123"` instead of the integer `123`? What if `CompanyId` is sometimes `1` and sometimes `"org_1"`?

**Your Task:**
1. Identify 3 potential type-related bugs
2. Rewrite the function using canonical entities
3. Explain why your version is safer

---

### Problem 1.2: Schema Validation

You're given this activity data:

```json
{
  "Uid": 12345,
  "UidOpp": "user_678",
  "Type": "document_share",
  "Date": "2024-01-15",
  "CompanyId": null,
  "StateOld": "viewer",
  "StateNew": "editor"
}
```

**Question:** What validation errors would you catch?

**Your Task:**
1. List all validation issues
2. Write a validation function that catches them
3. Show what the cleaned/canonical version would look like

---

## Problem Set 2: Function Implementation

### Problem 2.1: Collaboration Strength

**Task:** Implement `collaboration_strength(user_a, user_b, activities)`

**Requirements:**
- Returns a float from 0.0 to 1.0
- Considers:
  - Direct interactions (UidOpp/UidReq matches)
  - Co-resource access (same resource on same day)
  - Shared group membership
- Handles edge cases (empty lists, same user, etc.)

**Starter Code:**
```python
def collaboration_strength(user_a: str, user_b: str, 
                          activities: List[CanonicalActivity]) -> float:
    """
    Calculate collaboration strength between two users.
    
    Args:
        user_a: First user ID
        user_b: Second user ID
        activities: List of activity records
    
    Returns:
        float: Score from 0.0 (no collaboration) to 1.0 (strong collaboration)
    """
    # TODO: Implement
    pass
```

**Test Cases:**
```python
# Test 1: No interactions
assert collaboration_strength("user_1", "user_2", []) == 0.0

# Test 2: One direct interaction
activities = [
    CanonicalActivity(
        user_id="user_1",
        target_user_id="user_2",
        activity_type="document_share"
    )
]
result = collaboration_strength("user_1", "user_2", activities)
assert 0.0 < result <= 1.0

# Test 3: Multiple interactions (should increase score)
# TODO: Write this test
```

**Your Task:**
1. Implement the function
2. Write at least 3 test cases
3. Explain your algorithm

---

### Problem 2.2: Permission Upgrade Detector

**Task:** Write a function that detects permission upgrades from activities.

**Requirements:**
- Takes a list of activities
- Returns a list of permission changes where `state_after` represents higher privilege than `state_before`
- Handles unknown states gracefully

**Starter Code:**
```python
def detect_permission_upgrades(activities: List[CanonicalActivity]) -> List[Dict]:
    """
    Detect permission upgrades from activities.
    
    Returns:
        List of permission changes that represent upgrades
    """
    # TODO: Implement
    pass
```

**Hint:** Permission hierarchy might be:
- `viewer` < `commenter` < `editor` < `admin`

**Your Task:**
1. Implement the function
2. Define your permission hierarchy
3. Write test cases

---

## Problem Set 3: Governance Rules

### Problem 3.1: High Activity Interpretation

**Scenario:** A user has 1,000 activities in one week.

**Question:** What are 5 possible interpretations of this?

**Your Task:**
1. List 5 interpretations
2. For each, explain what additional context you'd need to confirm it
3. Write a governance rule that prevents misinterpreting high activity

**Example Governance Rule:**
```python
def check_high_activity(user_id: str, activity_count: int, 
                       role_baseline: int) -> Dict[str, Any]:
    """
    Check if high activity is within expected range for role.
    
    Returns:
        {
            "flagged": bool,
            "reason": str,
            "recommendation": str
        }
    """
    if activity_count > role_baseline * 2:
        return {
            "flagged": True,
            "reason": "Activity significantly above role baseline",
            "recommendation": "Review for: burnout, automation, or role mismatch"
        }
    return {"flagged": False}
```

---

### Problem 3.2: Bias Guardrail

**Scenario:** You're building a "top performers" list based on activity count.

**Question:** Why is this dangerous?

**Your Task:**
1. Explain 3 ways this could be biased
2. Write a governance rule that blocks this
3. Suggest an alternative approach

**Example:**
```python
def check_performance_ranking(ranking_type: str) -> bool:
    """
    Check if a ranking type is prohibited.
    
    Returns:
        True if prohibited, False if allowed
    """
    PROHIBITED = [
        "individual_performance",
        "employee_ranking",
        "termination_risk"
    ]
    return ranking_type in PROHIBITED
```

---

## Problem Set 4: Three-Lens Interpretation

### Problem 4.1: Interpret This Activity

Given this activity:

```json
{
  "Uid": "user_carol",
  "UidOpp": "user_dave",
  "Type": "permission_grant",
  "Date": "2024-01-20T14:00:00Z",
  "CompanyId": "org_education",
  "StateOld": "viewer",
  "StateNew": "admin",
  "ProviderId": "provider_google_workspace",
  "ErrorCode": null
}
```

**Your Task:**
1. Write TRIBE interpretation
2. Write TEACHER interpretation
3. Write RECON interpretation
4. Explain how they're different but complementary

---

### Problem 4.2: Build a Mini Pipeline

**Task:** Assemble a pipeline that:
1. Takes a CSV with activity data
2. Applies PII protection
3. Extracts users and companies
4. Builds a simple collaboration graph
5. Finds one mentor candidate

**Deliverable:**
- Code (or visual pipeline)
- Documentation explaining each step
- Output showing the results

---

## Problem Set 5: System Limits

### Problem 5.1: Identify the Limit

For each scenario, identify the system limit and suggest a guardrail:

**Scenario A:** A provider has 99.9% reliability, but all errors occur with one specific company.

**Question:** What limit does this reveal? What guardrail would you add?

**Scenario B:** A user's activity count doubles after a role change, but their collaboration score drops.

**Question:** What limit does this reveal? What guardrail would you add?

**Scenario C:** Three quasi-identifiers (role + department + hire_date) uniquely identify 5 employees in a dataset of 1,000.

**Question:** What limit does this reveal? What guardrail would you add?

---

### Problem 5.2: Design for Limits

**Task:** Design a system that:
- Tracks skill progressions
- Never ranks individuals against each other
- Always compares to personal baseline
- Flags anomalies for human review

**Your Task:**
1. Write pseudocode for the system
2. List 3 limits you're designing for
3. Explain how your design addresses each limit

---

## Submission Guidelines

### For Each Problem Set

1. **Code:** Working implementation (or pseudocode if visual)
2. **Explanation:** Why your solution works
3. **Tests:** At least 2 test cases
4. **Reflection:** What you learned

### Self-Assessment

After completing all problem sets, answer:

1. What was the hardest concept?
2. What surprised you?
3. What would you do differently next time?

**Remember:** Growth over position. Compare to your Week 0 baseline, not to others.

---

## Solutions (For Instructors)

Solutions are available in `week1_solutions.py` for instructors.

**Key Learning Points:**
- Type safety prevents runtime errors
- Governance rules are code, not just policy
- Three lenses reveal different truths
- System limits require guardrails

---

*"Practice makes permanent. Perfect practice makes perfect permanent."*

