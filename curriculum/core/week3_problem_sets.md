# TEACHER Week 3: Problem Sets

> *"Algorithms are everywhere. Understanding them helps you build trustworthy intelligence."*

---

## Problem Set 1: Search Algorithms

### Problem 1.1: Linear Search for Activities

**Task:** Implement linear search to find activities by user

```python
def find_activities_linear(activities: List[CanonicalActivity], 
                          user_id: str) -> List[CanonicalActivity]:
    """
    Linear search for all activities by a user.
    
    Efficiency: O(n)
    """
    # TODO: Implement
    pass
```

**Requirements:**
1. Return all activities where `user_id` matches
2. Handle empty lists
3. Return empty list if no matches

**Test Cases:**
```python
activities = [
    CanonicalActivity(user_id="user_1", activity_type="login"),
    CanonicalActivity(user_id="user_2", activity_type="logout"),
    CanonicalActivity(user_id="user_1", activity_type="file_access")
]

result = find_activities_linear(activities, "user_1")
assert len(result) == 2
assert all(a.user_id == "user_1" for a in result)
```

---

### Problem 1.2: Binary Search for Users

**Task:** Implement binary search for users in sorted list

```python
def binary_search_user(users: List[CanonicalUser], user_id: str) -> Optional[CanonicalUser]:
    """
    Binary search for user in sorted list.
    
    Requires: users sorted by id
    Efficiency: O(log n)
    """
    # TODO: Implement
    pass
```

**Requirements:**
1. Assume users list is sorted by `id`
2. Return user if found, None otherwise
3. Handle edge cases (empty list, not found)

**Test Cases:**
```python
users = [
    CanonicalUser(id="user_1", company_id="org_a"),
    CanonicalUser(id="user_2", company_id="org_a"),
    CanonicalUser(id="user_3", company_id="org_b")
]

result = binary_search_user(users, "user_2")
assert result is not None
assert result.id == "user_2"

result = binary_search_user(users, "user_999")
assert result is None
```

---

### Problem 1.3: Efficiency Comparison

**Task:** Compare linear vs binary search performance

**Requirements:**
1. Generate sorted list of 10,000 users
2. Time linear search for 100 random IDs
3. Time binary search for same 100 IDs
4. Graph results and explain difference

---

## Problem Set 2: Sorting Algorithms

### Problem 2.1: Simple Provider Ranking (Selection Sort Style)

**Task:** Implement simple ranking using selection sort approach

```python
def simple_provider_ranking(providers: List[CanonicalProvider]) -> List[CanonicalProvider]:
    """
    Rank providers by reliability (selection sort style).
    
    Efficiency: O(n²)
    """
    # TODO: Implement
    pass
```

**Requirements:**
1. Sort by `reliability_score` (highest first)
2. Use selection sort algorithm
3. Return sorted list

---

### Problem 2.2: Efficient Provider Ranking (Merge Sort)

**Task:** Implement efficient ranking using merge sort

```python
def merge_sort_providers(providers: List[CanonicalProvider]) -> List[CanonicalProvider]:
    """
    Rank providers efficiently using merge sort.
    
    Efficiency: O(n log n)
    """
    # TODO: Implement
    pass
```

**Requirements:**
1. Sort by `reliability_score` (highest first)
2. Use merge sort algorithm
3. Include merge helper function

---

### Problem 2.3: Performance Comparison

**Task:** Compare simple vs efficient ranking

**Requirements:**
1. Generate list of 1,000 providers
2. Time simple ranking
3. Time efficient ranking
4. Explain the difference

---

## Problem Set 3: The Three MVP Extractors

### Problem 3.1: Collaboration Strength

**Task:** Implement `collaboration_strength()`

**Requirements:**
1. Consider direct interactions
2. Consider co-resource access
3. Return score 0.0-1.0
4. Handle edge cases (no interactions, same user)

**Starter Code:**
```python
def collaboration_strength(user_a: str, 
                          user_b: str,
                          activities: List[CanonicalActivity]) -> float:
    """
    Calculate collaboration strength.
    
    Returns: Score from 0.0 to 1.0
    """
    # TODO: Implement
    pass
```

**Test Cases:**
```python
# No interactions
assert collaboration_strength("user_1", "user_2", []) == 0.0

# One interaction
activities = [
    CanonicalActivity(user_id="user_1", target_user_id="user_2")
]
result = collaboration_strength("user_1", "user_2", activities)
assert 0.0 < result <= 1.0
```

---

### Problem 3.2: Role Mastery Profile

**Task:** Implement `role_mastery_profile()`

**Requirements:**
1. Track permission upgrades
2. Extract skills from upgrades
3. Calculate trajectory
4. Return mastery score

**Starter Code:**
```python
def role_mastery_profile(user_id: str,
                        permission_changes: List[CanonicalPermissionChange]) -> Dict:
    """
    Build mastery profile from permission history.
    """
    # TODO: Implement
    pass
```

---

### Problem 3.3: Provider Reliability Score

**Task:** Implement `provider_reliability_score()`

**Requirements:**
1. Calculate error rate
2. Assign letter grade (A-F)
3. Include confidence score
4. Handle zero-activity case

**Starter Code:**
```python
def provider_reliability_score(provider_id: str,
                              activities: List[CanonicalActivity]) -> Dict:
    """
    Calculate provider reliability.
    """
    # TODO: Implement
    pass
```

---

## Problem Set 4: Recursion

### Problem 4.1: Recursive Community Detection

**Task:** Implement recursive community finder

```python
def find_connected_component(graph: Dict[str, List[str]], 
                            start: str, 
                            visited: Set[str] = None) -> Set[str]:
    """
    Recursively find all nodes connected to start.
    
    Base case: No unvisited neighbors
    Recursive case: Visit neighbor, recurse
    """
    # TODO: Implement
    pass
```

**Requirements:**
1. Base case: already visited or no neighbors
2. Recursive case: visit all neighbors
3. Return set of all connected nodes

---

### Problem 4.2: Recursive Skill Prerequisites

**Task:** Find all prerequisites for a skill recursively

```python
def get_skill_prerequisites(skill_id: str, 
                           skill_graph: Dict[str, List[str]],
                           visited: Set[str] = None) -> List[str]:
    """
    Recursively find all prerequisites.
    """
    # TODO: Implement
    pass
```

**Requirements:**
1. Base case: no prerequisites
2. Recursive case: get prerequisites of prerequisites
3. Avoid cycles (use visited set)

---

## Problem Set 5: Algorithm Efficiency Analysis

### Problem 5.1: Big O Analysis

**Task:** Analyze efficiency of your extractors

For each extractor:
1. Count operations in terms of input size
2. Determine Big O notation
3. Explain why

**Extractors to analyze:**
- `collaboration_strength()`
- `role_mastery_profile()`
- `provider_reliability_score()`

---

### Problem 5.2: Optimization Challenge

**Task:** Optimize one of your extractors

**Requirements:**
1. Identify bottleneck
2. Implement optimization
3. Measure improvement
4. Explain trade-offs

**Example:** Optimize `collaboration_strength()` by:
- Pre-indexing activities by user
- Using hash maps for O(1) lookups
- Reducing redundant scans

---

## Problem Set 6: Integration Challenge

### Problem 6.1: Build Complete TRIBE Extractor

**Task:** Build end-to-end TRIBE extractor

**Requirements:**
1. Load activities
2. Build collaboration graph
3. Detect communities (recursive)
4. Find mentor candidates
5. Return complete TRIBE output

---

### Problem 6.2: Build Complete TEACHER Extractor

**Task:** Build end-to-end TEACHER extractor

**Requirements:**
1. Load permission changes
2. Build role mastery profiles
3. Generate recommendations
4. Track progressions
5. Return complete TEACHER output

---

### Problem 6.3: Build Complete RECON Extractor

**Task:** Build end-to-end RECON extractor

**Requirements:**
1. Load activities
2. Score all providers
3. Rank providers (efficiently)
4. Identify friction points
5. Return complete RECON output

---

## Submission Guidelines

### For Each Problem Set

1. **Code:** Working implementation
2. **Tests:** At least 2 test cases per function
3. **Efficiency Analysis:** Big O notation
4. **Explanation:** Why your algorithm works

### Self-Assessment

After completing all problem sets, answer:

1. Which algorithm was hardest to implement?
2. What surprised you about efficiency?
3. How would you optimize further?
4. What would you do differently?

**Remember:** Growth over position. Compare to your Week 2 baseline.

---

## Solutions (For Instructors)

Solutions are available in `week3_solutions.py` for instructors.

**Key Learning Points:**
- Algorithms are everywhere in organizations
- Efficiency matters at scale
- Divide and conquer is powerful
- Recursion simplifies complex problems
- The three extractors are real, working algorithms

---

*"Understanding algorithms helps you build trustworthy intelligence at scale."*

