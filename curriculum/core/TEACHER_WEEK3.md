# TEACHER Week 3: Algorithms

> *"Week 3 is where CS50 stops teaching syntax and starts teaching problem-solving. That's exactly where TEACHER needs to be: from infrastructure → to intelligence extraction."*

---

## Module Overview

**Duration:** 7-9 hours  
**Prerequisites:** Week 2 (Data Structures)  
**Next:** Week 4+ (Domains)

This week, learners implement the **actual algorithms** that make TRIBE, TEACHER, and RECON work. Just as CS50 Week 3 introduces search, sort, and recursion, TEACHER Week 3 introduces collaboration strength, role mastery profiling, and provider reliability scoring.

---

## Learning Outcomes

By the end of this week, learners will be able to:

1. **Implement** collaboration strength algorithm
2. **Build** role mastery profiler
3. **Create** provider reliability scorer
4. **Understand** algorithm efficiency (Big O)
5. **Apply** divide-and-conquer to community detection
6. **Use** recursion for graph traversal
7. **Recognize** trade-offs (simple vs efficient)

---

## Core Concept: Algorithms Are Everywhere

### CS50's Insight

> "These algorithms are everywhere - in your phone, in Google, in Microsoft. Understanding them helps you write better code."

### TEACHER's Insight

> "These algorithms are in every organization - collaboration networks, skill progression, provider evaluation. Understanding them helps you build trustworthy intelligence."

---

## Divide and Conquer → Community Detection

### CS50's Attendance Algorithm

**Problem:** Count people in a room

**Approach:** Pair up, add numbers, one sits, repeat

**Efficiency:** O(log n) - each iteration halves the problem

### TEACHER's Community Detection

**Problem:** Find communities in a network

**Approach:** Divide graph into subgraphs, detect communities recursively

**Efficiency:** O(n log n) - similar to merge sort

### Algorithm

```python
def detect_communities(graph: Dict[str, List[str]]) -> List[List[str]]:
    """
    Detect communities using divide-and-conquer.
    
    Algorithm:
    1. If graph is small enough, return as single community
    2. Else, divide graph into two subgraphs
    3. Recursively detect communities in each subgraph
    4. Merge communities that have strong connections
    """
    # Base case: small graph
    if len(graph) <= 3:
        return [list(graph.keys())]
    
    # Divide: split graph into two parts
    left, right = divide_graph(graph)
    
    # Conquer: recursively find communities
    left_communities = detect_communities(left)
    right_communities = detect_communities(right)
    
    # Merge: combine communities with strong connections
    return merge_communities(left_communities, right_communities)
```

**Key Lesson:**
> "Divide and conquer makes complex problems manageable.  
> Community detection is just recursive graph division."

---

## Linear Search → Finding Entities

### CS50's Linear Search

**Problem:** Find a value in an unsorted array

**Algorithm:** Check each element until found

**Efficiency:** O(n) worst case, Ω(1) best case

### TEACHER's Entity Search

**Problem:** Find a user, activity, or provider

**Algorithm:** Linear search through entity collections

**Efficiency:** O(n) - acceptable for small datasets, needs optimization for large

### Algorithm

```python
def find_user_by_id(users: List[CanonicalUser], user_id: str) -> Optional[CanonicalUser]:
    """
    Linear search for user by ID.
    
    Efficiency: O(n) worst case, Ω(1) best case
    """
    for user in users:
        if user.id == user_id:
            return user
    return None

def find_activities_by_user(activities: List[CanonicalActivity], 
                           user_id: str) -> List[CanonicalActivity]:
    """
    Linear search for all activities by a user.
    
    Efficiency: O(n) - must check every activity
    """
    result = []
    for activity in activities:
        if activity.user_id == user_id:
            result.append(activity)
    return result
```

**When to Use:**
- Small datasets (< 1000 entities)
- Unsorted data
- One-time searches

**When NOT to Use:**
- Large datasets (> 10,000 entities)
- Frequent searches
- Sorted data (use binary search instead)

---

## Binary Search → Fast Entity Lookups

### CS50's Binary Search

**Problem:** Find a value in a **sorted** array

**Algorithm:** Divide in half, compare, recurse

**Efficiency:** O(log n) - much faster than linear

### TEACHER's Binary Entity Search

**Problem:** Find a user in a sorted user list

**Algorithm:** Binary search on sorted IDs

**Efficiency:** O(log n) - essential for large datasets

### Algorithm

```python
def binary_search_user(users: List[CanonicalUser], user_id: str) -> Optional[CanonicalUser]:
    """
    Binary search for user in sorted list.
    
    Requires: users list sorted by id
    Efficiency: O(log n)
    """
    left = 0
    right = len(users) - 1
    
    while left <= right:
        middle = (left + right) // 2
        
        if users[middle].id == user_id:
            return users[middle]
        elif users[middle].id < user_id:
            left = middle + 1
        else:
            right = middle - 1
    
    return None
```

**Key Lesson:**
> "Sorting enables faster searching.  
> For 1,000,000 users, linear = 1,000,000 steps, binary = ~20 steps."

---

## Selection Sort → Simple But Slow

### CS50's Selection Sort

**Algorithm:** Find smallest, swap to front, repeat

**Efficiency:** Θ(n²) - always slow, but simple

### TEACHER's Simple Provider Ranking

**Problem:** Rank providers by reliability

**Simple Algorithm:** Compare all pairs, swap

**Efficiency:** O(n²) - fine for small datasets, too slow for large

### Algorithm

```python
def simple_provider_ranking(providers: List[CanonicalProvider]) -> List[CanonicalProvider]:
    """
    Simple ranking: selection sort style.
    
    Efficiency: O(n²) - simple but slow
    Use for: Small datasets, teaching purposes
    """
    ranked = providers.copy()
    n = len(ranked)
    
    for i in range(n):
        # Find provider with highest reliability
        max_idx = i
        for j in range(i + 1, n):
            if ranked[j].reliability_score > ranked[max_idx].reliability_score:
                max_idx = j
        
        # Swap to front
        ranked[i], ranked[max_idx] = ranked[max_idx], ranked[i]
    
    return ranked
```

**When to Use:**
- Teaching algorithm concepts
- Small datasets (< 100 providers)
- Prototyping

**When NOT to Use:**
- Production systems
- Large datasets
- Real-time ranking

---

## Merge Sort → Efficient Algorithms

### CS50's Merge Sort

**Algorithm:** Divide, sort halves, merge

**Efficiency:** Θ(n log n) - much faster than selection/bubble

### TEACHER's Efficient Provider Ranking

**Problem:** Rank providers efficiently

**Algorithm:** Merge sort by reliability score

**Efficiency:** O(n log n) - production-ready

### Algorithm

```python
def merge_sort_providers(providers: List[CanonicalProvider]) -> List[CanonicalProvider]:
    """
    Efficient provider ranking using merge sort.
    
    Efficiency: O(n log n) - production-ready
    """
    if len(providers) <= 1:
        return providers
    
    # Divide
    middle = len(providers) // 2
    left = merge_sort_providers(providers[:middle])
    right = merge_sort_providers(providers[middle:])
    
    # Merge
    return merge_providers(left, right)

def merge_providers(left: List[CanonicalProvider], 
                   right: List[CanonicalProvider]) -> List[CanonicalProvider]:
    """Merge two sorted provider lists."""
    result = []
    i = j = 0
    
    while i < len(left) and j < len(right):
        if left[i].reliability_score >= right[j].reliability_score:
            result.append(left[i])
            i += 1
        else:
            result.append(right[j])
            j += 1
    
    # Add remaining
    result.extend(left[i:])
    result.extend(right[j:])
    return result
```

**Key Lesson:**
> "n log n is much better than n².  
> For 10,000 providers: selection = 100M steps, merge = 133K steps."

---

## Recursion → Graph Traversal

### CS50's Recursive Structures

- **Pyramids:** A pyramid of height n = pyramid of height (n-1) + 1 row
- **Trees:** A tree = root + left subtree + right subtree

### TEACHER's Recursive Graph Traversal

- **Communities:** A community = connected subgraph + recursive detection
- **Skill Trees:** A skill = prerequisites + recursive dependencies

### Algorithm: Recursive Community Detection

```python
def find_connected_component(graph: Dict[str, List[str]], 
                            start: str, 
                            visited: Set[str] = None) -> Set[str]:
    """
    Recursively find all nodes connected to start.
    
    Base case: No unvisited neighbors
    Recursive case: Visit neighbor, recurse
    """
    if visited is None:
        visited = set()
    
    # Base case: already visited
    if start in visited:
        return visited
    
    # Mark as visited
    visited.add(start)
    
    # Recursive case: visit all neighbors
    for neighbor in graph.get(start, []):
        find_connected_component(graph, neighbor, visited)
    
    return visited
```

### Algorithm: Recursive Skill Prerequisites

```python
def get_skill_prerequisites(skill_id: str, 
                           skill_graph: Dict[str, List[str]],
                           visited: Set[str] = None) -> List[str]:
    """
    Recursively find all prerequisites for a skill.
    
    Base case: Skill has no prerequisites
    Recursive case: Get prerequisites of prerequisites
    """
    if visited is None:
        visited = set()
    
    if skill_id in visited:
        return []  # Avoid cycles
    
    visited.add(skill_id)
    prerequisites = skill_graph.get(skill_id, [])
    
    # Recursive case: get prerequisites of prerequisites
    all_prereqs = prerequisites.copy()
    for prereq in prerequisites:
        all_prereqs.extend(get_skill_prerequisites(prereq, skill_graph, visited))
    
    return all_prereqs
```

**Key Lesson:**
> "Recursion simplifies complex problems.  
> Graph traversal is naturally recursive."

---

## The Three MVP Extractors

This is where the magic happens. These are the algorithms that make TRIBE, TEACHER, and RECON real.

---

### Extractor 1: Collaboration Strength (TRIBE)

**Problem:** Measure how strongly two users collaborate

**Algorithm:** Weighted combination of factors

**Efficiency:** O(m) where m = number of activities

```python
def collaboration_strength(user_a: str, 
                          user_b: str,
                          activities: List[CanonicalActivity]) -> float:
    """
    Calculate collaboration strength between two users.
    
    Factors:
    - Direct interactions (UidOpp/UidReq)
    - Co-resource access (same resource on same day)
    - Shared group membership
    
    Efficiency: O(m) where m = activities count
    """
    direct_count = 0
    co_access_count = 0
    
    # Track resource access by date
    resource_access: Dict[str, Dict[str, Set[str]]] = defaultdict(lambda: defaultdict(set))
    
    for activity in activities:
        # Direct interactions
        if (activity.user_id == user_a and activity.target_user_id == user_b) or \
           (activity.user_id == user_b and activity.target_user_id == user_a):
            direct_count += 1
        
        # Track resource co-access
        if activity.resource_id and activity.timestamp_date:
            resource_access[activity.resource_id][activity.timestamp_date].add(activity.user_id)
    
    # Count co-access
    for resource_id, date_users in resource_access.items():
        for date, users in date_users.items():
            if user_a in users and user_b in users:
                co_access_count += 1
    
    # Weighted combination
    direct_score = min(direct_count / 10.0, 1.0)  # Normalize
    co_access_score = min(co_access_count / 5.0, 1.0)  # Normalize
    
    return (direct_score * 0.6) + (co_access_score * 0.4)
```

**Efficiency Analysis:**
- **Time:** O(m) - must check all activities
- **Space:** O(r) where r = unique resources
- **Optimization:** Could use hash maps for O(1) lookups

---

### Extractor 2: Role Mastery Profile (TEACHER)

**Problem:** Build a skill profile from permission history

**Algorithm:** Track state transitions as skill acquisitions

**Efficiency:** O(m) where m = permission changes

```python
def role_mastery_profile(user_id: str,
                        permission_changes: List[CanonicalPermissionChange]) -> Dict:
    """
    Build mastery profile from permission history.
    
    Key insight: Permission upgrades = skill demonstrations
    
    Efficiency: O(m) where m = permission changes
    """
    skills = []
    progressions = []
    
    for change in permission_changes:
        if change.user_id != user_id:
            continue
        
        # Check if this is an upgrade
        if is_permission_upgrade(change.state_before, change.state_after):
            skill = extract_skill_from_permission(change)
            skills.append(skill)
            
            progressions.append({
                "from": change.state_before,
                "to": change.state_after,
                "timestamp": change.timestamp,
                "skill": skill
            })
    
    # Calculate trajectory
    trajectory = "growing" if len(progressions) > 3 else "stable"
    
    return {
        "user_id": user_id,
        "skills": skills,
        "progressions": progressions,
        "trajectory": trajectory,
        "mastery_score": len(skills) / 10.0  # Normalize
    }

def is_permission_upgrade(before: str, after: str) -> bool:
    """Check if permission change represents an upgrade."""
    hierarchy = ["viewer", "commenter", "editor", "admin"]
    try:
        return hierarchy.index(after) > hierarchy.index(before)
    except ValueError:
        return False
```

**Efficiency Analysis:**
- **Time:** O(m) - linear scan
- **Space:** O(s) where s = skills acquired
- **Optimization:** Could pre-sort by timestamp for chronological analysis

---

### Extractor 3: Provider Reliability Score (RECON)

**Problem:** Score provider reliability from activity data

**Algorithm:** Error rate calculation with confidence intervals

**Efficiency:** O(m) where m = activities

```python
def provider_reliability_score(provider_id: str,
                              activities: List[CanonicalActivity]) -> Dict:
    """
    Calculate provider reliability score.
    
    Score = 1 - (error_rate)
    Confidence based on sample size
    
    Efficiency: O(m) where m = activities
    """
    provider_activities = [a for a in activities if a.provider_id == provider_id]
    
    if not provider_activities:
        return {
            "provider_id": provider_id,
            "reliability_score": 0.0,
            "confidence": 0.0,
            "error_rate": 1.0,
            "total_activities": 0
        }
    
    total = len(provider_activities)
    errors = sum(1 for a in provider_activities if a.error_code)
    error_rate = errors / total if total > 0 else 1.0
    reliability = 1.0 - error_rate
    
    # Confidence increases with sample size
    confidence = min(total / 100.0, 1.0)  # 100+ activities = full confidence
    
    # Calculate grade
    if reliability >= 0.99:
        grade = "A"
    elif reliability >= 0.95:
        grade = "B"
    elif reliability >= 0.90:
        grade = "C"
    elif reliability >= 0.80:
        grade = "D"
    else:
        grade = "F"
    
    return {
        "provider_id": provider_id,
        "reliability_score": reliability,
        "confidence": confidence,
        "error_rate": error_rate,
        "total_activities": total,
        "error_count": errors,
        "grade": grade
    }
```

**Efficiency Analysis:**
- **Time:** O(m) - linear scan
- **Space:** O(1) - constant space
- **Optimization:** Could use streaming for real-time updates

---

## Big O Notation → Why Efficiency Matters

### CS50's Big O

| Notation | Name | Example |
|----------|------|---------|
| O(1) | Constant | Array lookup |
| O(log n) | Logarithmic | Binary search |
| O(n) | Linear | Linear search |
| O(n log n) | Linearithmic | Merge sort |
| O(n²) | Quadratic | Selection sort |

### TEACHER's Efficiency Reality

**Scenario:** 1,000,000 activities, 10,000 users

| Algorithm | Efficiency | Steps | Time (est.) |
|-----------|-----------|-------|-------------|
| Linear search user | O(n) | 10,000 | 10ms |
| Binary search user | O(log n) | ~13 | 0.01ms |
| Collaboration strength | O(m) | 1,000,000 | 1s |
| Simple provider ranking | O(n²) | 100,000,000 | 100s |
| Merge sort providers | O(n log n) | 133,000 | 0.13s |

**Key Lesson:**
> "Efficiency isn't academic. At scale, O(n²) vs O(n log n) is the difference between 100 seconds and 0.13 seconds."

---

## Trade-offs: Simple vs Efficient

### CS50's Trade-offs

- **Time vs. Space:** Merge sort uses more memory but is faster
- **Simplicity vs. Efficiency:** Selection sort is simple but slow

### TEACHER's Trade-offs

| Algorithm | Simple? | Efficient? | When to Use |
|-----------|---------|-----------|-------------|
| Linear search | ✅ Yes | ❌ O(n) | Small datasets, prototyping |
| Binary search | ⚠️ Medium | ✅ O(log n) | Large datasets, production |
| Simple ranking | ✅ Yes | ❌ O(n²) | Teaching, < 100 items |
| Merge sort ranking | ⚠️ Medium | ✅ O(n log n) | Production, any size |
| Recursive traversal | ⚠️ Medium | ✅ O(n) | Graph algorithms |

**Key Lesson:**
> "Start simple. Optimize when needed.  
> But know when simple becomes too slow."

---

## Micro-Labs (CS50-Style)

### Lab 1: Implement Collaboration Strength

**Task:** Write `collaboration_strength()` function

**Requirements:**
- Takes two user IDs and activities list
- Returns score 0.0-1.0
- Considers at least 2 factors
- Handles edge cases

**Test Cases:**
```python
# No interactions
assert collaboration_strength("user_1", "user_2", []) == 0.0

# One direct interaction
activities = [CanonicalActivity(user_id="user_1", target_user_id="user_2")]
result = collaboration_strength("user_1", "user_2", activities)
assert 0.0 < result <= 1.0

# Multiple interactions (should increase score)
# TODO: Write test
```

---

### Lab 2: Build Role Mastery Profiler

**Task:** Implement `role_mastery_profile()`

**Requirements:**
- Tracks permission upgrades
- Identifies skills acquired
- Calculates trajectory
- Returns mastery score

---

### Lab 3: Create Provider Scorer

**Task:** Implement `provider_reliability_score()`

**Requirements:**
- Calculates error rate
- Assigns letter grade
- Includes confidence score
- Handles zero-activity providers

---

### Lab 4: Recursive Community Detection

**Task:** Implement recursive community finder

**Requirements:**
- Base case: small graph
- Recursive case: divide and conquer
- Merge communities with strong connections

---

### Lab 5: Algorithm Efficiency Analysis

**Task:** Compare algorithm performance

**Requirements:**
- Implement linear and binary search
- Time both on sorted data
- Graph results (n vs time)
- Explain the difference

---

## Assessment: Self-Relative Growth

### Baseline (Before Week 3)

**Question:** "Can you write a function that finds a user?"

**Expected Response:**
- May use simple linear search
- May not consider efficiency
- May not handle edge cases

### After Week 3

**Question:** "Can you implement collaboration strength with efficiency analysis?"

**Expected Response:**
- Can implement the algorithm
- Can analyze efficiency (Big O)
- Can explain trade-offs
- Can optimize when needed

---

## Key Takeaways

1. **Algorithms are everywhere.** In every organization, in every system.

2. **Efficiency matters at scale.** O(n²) vs O(n log n) is real-world impact.

3. **Divide and conquer is powerful.** Community detection, graph algorithms.

4. **Recursion simplifies complex problems.** Graph traversal, skill trees.

5. **Trade-offs are real.** Simple vs efficient, time vs space.

6. **The three extractors are real algorithms.** Collaboration strength, role mastery, provider scoring.

---

## Next Steps

**Week 4+:** Domains
- Complete TRIBE pipeline
- Complete TEACHER pipeline
- Complete RECON pipeline
- Integration and real-world application

**For Now:** Practice the algorithms:
- `collaboration_strength()`
- `role_mastery_profile()`
- `provider_reliability_score()`

---

## Resources

- **mvp_extractors.py:** See the extractors in action
- **pipeline.py:** See how extractors fit into the pipeline
- **governance.py:** See how algorithms respect governance

---

*"Week 1 was 'We can build this.' Week 2 was 'We can make this safe.' Week 3 is 'We can extract intelligence.' Welcome to algorithms."*

