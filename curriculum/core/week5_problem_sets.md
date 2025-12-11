# TEACHER Week 5: Problem Sets

> *"Structures of Fairness - Every promise is a data-structure decision."*

---

## Problem Set 1: Abstract Data Types (ADTs)

### Problem 1.1: Design Identity Graph ADT

**Task:** Design the ADT for TRIBE's identity graph

**Requirements:**
1. Define operations (add_connection, get_connections, find_communities)
2. Define constraints (no PII, weighted edges, minimum community size)
3. Write interface (no implementation yet)
4. Explain why each operation/constraint matters

**Starter:**
```python
class IdentityGraph:
    """
    Abstract: Social network graph for TRIBE analysis.
    
    Operations:
    - TODO: Define operations
    
    Constraints:
    - TODO: Define constraints
    """
    pass
```

---

### Problem 1.2: Design Learning State ADT

**Task:** Design the ADT for TEACHER's learning state

**Requirements:**
1. Define operations (record_progression, get_current_state, recommend_next)
2. Define constraints (self-relative, skill-based, tree pathways)
3. Write interface
4. Explain fairness guarantees

---

## Problem Set 2: Queues for Fairness

### Problem 2.1: Implement Moderation Queue

**Task:** Build FIFO queue for content moderation

**Requirements:**
1. Implement enqueue/dequeue
2. Ensure FIFO order
3. Add fairness metrics (average wait time, max wait time)
4. Prove no favoritism

**Starter:**
```python
class ModerationQueue:
    def __init__(self):
        self.queue = []
        self.enqueue_times = {}  # Track fairness
    
    def enqueue(self, item):
        # TODO: Implement
        pass
    
    def dequeue(self):
        # TODO: Implement
        pass
```

---

### Problem 2.2: Fairness Analysis

**Task:** Analyze queue fairness

**Requirements:**
1. Simulate 100 items in queue
2. Measure wait times
3. Prove FIFO = fair (variance in wait times)
4. Compare to priority queue (show unfairness)

---

## Problem Set 3: Stacks for Recovery

### Problem 3.1: Implement Reasoning Stack

**Task:** Build stack for reasoning traces

**Requirements:**
1. Implement push/pop
2. Generate explanations
3. Show recent context emphasis
4. Demonstrate rollback capability

---

### Problem 3.2: Governance Rollback

**Task:** Implement rollback stack for governance actions

**Requirements:**
1. Record actions with state snapshots
2. Implement rollback function
3. Show audit chain
4. Prove immutability

---

## Problem Set 4: Linked Lists for Audit

### Problem 4.1: Implement Audit Log

**Task:** Build append-only audit log using linked list

**Requirements:**
1. Append-only (immutable)
2. Sequential access
3. Integrity verification
4. Human-legible format

---

### Problem 4.2: State Transition Chain

**Task:** Build linked list of state transitions

**Requirements:**
1. Track StateOld → StateNew
2. Generate progression narrative
3. Show complete journey
4. Enable "how did I get here?" queries

---

## Problem Set 5: Trees for Pathways

### Problem 5.1: Build Curriculum Tree

**Task:** Implement balanced curriculum tree

**Requirements:**
1. Add skills with prerequisites
2. Find pathways to target skill
3. Ensure balance (multiple paths)
4. Detect and fix unbalanced trees

**Starter:**
```python
class CurriculumTree:
    class TreeNode:
        def __init__(self, skill_id, skill_name):
            self.skill_id = skill_id
            self.skill_name = skill_name
            self.prerequisites = []
            self.unlocks = []
    
    def add_skill(self, skill_id, prerequisites=None):
        # TODO: Implement
        pass
    
    def get_pathway(self, target_skill_id):
        # TODO: Implement
        pass
```

---

### Problem 5.2: Balance Enforcement

**Task:** Ensure curriculum tree is balanced

**Requirements:**
1. Detect unbalanced nodes (only one path)
2. Add alternative routes
3. Prove multiple valid paths exist
4. Explain why balance = fairness

---

## Problem Set 6: Hash Tables for Scale

### Problem 6.1: Implement Safe Hash Table

**Task:** Build hash table with collision guardrails

**Requirements:**
1. Implement hash function
2. Handle collisions
3. Log collisions for governance review
4. Prevent bias (misclassification)

**Starter:**
```python
class SafeHashTable:
    def __init__(self, size=1000):
        self.size = size
        self.buckets = [[] for _ in range(size)]
        self.collision_log = []
    
    def _hash(self, key: str) -> int:
        # TODO: Implement good hash function
        pass
    
    def put(self, key: str, value: Any):
        # TODO: Implement with collision detection
        pass
    
    def get(self, key: str) -> Optional[Any]:
        # TODO: Implement
        pass
```

---

### Problem 6.2: Collision Analysis

**Task:** Analyze hash collisions for bias

**Requirements:**
1. Load 10,000 user IDs
2. Hash them
3. Detect collisions
4. Analyze if collisions indicate bias (similar users merged?)

---

## Problem Set 7: Tries for UX

### Problem 7.1: Implement Concept Trie

**Task:** Build trie for concept autocomplete

**Requirements:**
1. Insert concepts
2. Search by prefix
3. Hybrid approach (trie + hash table)
4. Memory-efficient

---

### Problem 7.2: Autocomplete Integration

**Task:** Integrate trie into learning interface

**Requirements:**
1. Build concept trie from curriculum
2. Implement autocomplete function
3. Show top 5 matches
4. Measure performance

---

## Problem Set 8: Integration Challenge

### Problem 8.1: Build Complete TRIBE Structure

**Task:** Combine structures for TRIBE pipeline

**Requirements:**
1. Hash table for user lookup
2. Graph structure for relationships
3. Queue for mentor matching fairness
4. Tree for org hierarchy

---

### Problem 8.2: Build Complete TEACHER Structure

**Task:** Combine structures for TEACHER pipeline

**Requirements:**
1. Tree for curriculum pathways
2. Hash table for role → skills lookup
3. Stack for reasoning traces
4. Linked list for progression history

---

### Problem 8.3: Build Complete RECON Structure

**Task:** Combine structures for RECON pipeline

**Requirements:**
1. Hash table for provider lookup
2. Linked list for value ledger
3. Queue for provider review fairness
4. Tree for provider hierarchy

---

## Submission Guidelines

### For Each Problem Set

1. **Code:** Working implementation
2. **Tests:** At least 2 test cases
3. **Fairness Analysis:** Explain how structure ensures fairness
4. **Performance Analysis:** Big O notation

### Self-Assessment

After completing all problem sets, answer:

1. Can you explain why structure choice = fairness choice?
2. Can you identify bias risks in structures?
3. Can you design fair structures?
4. What was the hardest concept?

**Remember:** Growth over position. Compare to your Week 4 baseline.

---

## Solutions (For Instructors)

Solutions are available in `week5_solutions.py` for instructors.

**Key Learning Points:**
- Structures encode morality
- Queue = fairness, Stack = explainability, Tree = multiple paths
- Hash collisions = bias risk
- Balance prevents burnout
- Every promise is a structure decision

---

*"Week 5 is where TEACHER's morality becomes architecture."*

