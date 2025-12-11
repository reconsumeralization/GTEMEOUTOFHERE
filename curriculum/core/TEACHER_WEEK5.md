# TEACHER Week 5: Structures of Fairness

> *"Week 5 is where TEACHER's morality becomes architecture: fairness, speed, and safety are encoded into the structures themselves."*

---

## Module Overview

**Duration:** 8-10 hours  
**Prerequisites:** Week 4 (Memory of Trust)  
**Next:** Week 6+ (Domains & Integration)

This week, learners discover that **data structures are moral choices**. Just as CS50 Week 5 teaches how to choose the right structure for time/space trade-offs, TEACHER Week 5 teaches how to choose the right structure for fairness, privacy, learning quality, and network resilience.

---

## Learning Outcomes

By the end of this week, learners will be able to:

1. **Explain** why systems become unfair when structure is sloppy
2. **Identify** which data structure best matches an educational goal
3. **Understand** that personalization requires safe indexing
4. **Connect** "hash collisions" to real-world bias risks
5. **Design** fair, scalable data structures for TRIBE/TEACHER/RECON
6. **Implement** queues for fairness, stacks for rollback, trees for pathways

---

## Core Concept: Structures Encode Morality

### CS50's Insight

> "Choose the right structure for time/space trade-offs. The structure you pick determines what's fast, what's slow, and what's possible."

### TEACHER's Insight

> "Choose the right structure for fairness/privacy/quality trade-offs. The structure you pick determines what's fair, what's safe, and what's scalable."

##### Inspiration: Structures Encode Justice

> *"He hath shewed thee, O man, what is good; and what doth the Lord require of thee, but to do justly, and to love mercy, and to walk humbly with thy God?"*
> 
> — Micah 6:8

**Connection:** Structures should encode justice. Queues ensure fairness (FIFO = no favoritism). Hash functions must be just. Balanced trees ensure equity. The structures we choose encode our values—justice, mercy, humility.

> *"Justice in the life and conduct of the State is possible only as first it resides in the hearts and souls of the citizens."*
> 
> — Plato

**Connection:** Justice in data structures is possible only as it first resides in the hearts of the builders. Fairness must be intentional, not accidental.

> *"The worst form of inequality is to try to make unequal things equal."*
> 
> — Aristotle

**Connection:** Fairness doesn't mean treating everyone the same—it means treating each according to their needs. Balanced trees allow different paths, not forced uniformity.

> *"Every block of stone has a statue inside it and it is the task of the sculptor to discover it."*
> 
> — Michelangelo

**Connection:** Every dataset has fair structures inside it. Our task is to discover them—queues for fairness, trees for pathways, hash tables for justice.

##### Alternative Perspectives: How Other Thinkers Would Design Fair Structures

**The Problem:** How do we encode fairness and justice into data structures? What makes a structure "just"?

**Plato's Approach (Justice in the Soul):**
> *"Justice in the life and conduct of the State is possible only as first it resides in the hearts and souls of the citizens."*
> 
> — Plato

Plato would say: Justice in data structures is possible only as it first resides in the hearts of the builders. Fairness must be intentional, not accidental. We must design with justice in mind—queues for fairness (FIFO prevents favoritism), balanced trees for equity (no single path dominates). The structure reflects the builder's soul.

**Aristotle's Approach (Distributive Justice):**
> *"The worst form of inequality is to try to make unequal things equal."*
> 
> — Aristotle

Aristotle would say: Fairness doesn't mean treating everyone the same—it means treating each according to their needs. Balanced trees allow different paths (different learners need different routes). Hash tables must distribute fairly (no collisions that favor some over others). Justice is proportional, not uniform.

**Michelangelo's Approach (Discovering the Form):**
> *"Every block of stone has a statue inside it and it is the task of the sculptor to discover it."*
> 
> — Michelangelo

Michelangelo would say: The fair structure is already there—we must discover it. Don't force fairness—reveal it. Queues naturally ensure fairness (FIFO is inherent). Trees naturally allow multiple paths. Our job is to "carve away" the unfair parts to reveal the just structure within.

**Biblical Perspective (Do Justly, Love Mercy):**
> *"He hath shewed thee, O man, what is good; and what doth the Lord require of thee, but to do justly, and to love mercy, and to walk humbly with thy God?"*
> 
> — Micah 6:8

The biblical view: Structures should encode justice, mercy, and humility. Queues ensure justice (fair order). Trees allow mercy (multiple paths for those who struggle). Hash functions require humility (no assumption that one approach fits all).

**Synthesis:** All four perspectives teach us: fairness is both intentional (Plato) and discovered (Michelangelo), both proportional (Aristotle) and merciful (biblical). The structures we choose—queues, trees, hash tables—must reflect these values. Justice isn't added to structures—it's encoded in their design.

---

## Abstract Data Types (ADTs) → Lens-Level Objects

### CS50's ADTs

Define the **interface** before the **implementation**:
- What operations are allowed?
- What are the constraints?
- What's the contract?

### TEACHER's ADTs

Define the **lens-level objects** before storage:

#### 1. Identity Graph (TRIBE)

**Abstract Interface:**
```python
class IdentityGraph:
    """
    Abstract: Social network graph for TRIBE analysis.
    
    Operations:
    - add_connection(user_a, user_b, weight)
    - get_connections(user_id) -> List[User]
    - find_communities() -> List[Community]
    - find_bridges() -> List[User]
    
    Constraints:
    - No PII in nodes
    - All edges weighted
    - Communities have minimum size
    """
    pass
```

**Implementation Choices:**
- Adjacency list (sparse graphs)
- Adjacency matrix (dense graphs)
- Graph database (production scale)

---

#### 2. Learning State (TEACHER)

**Abstract Interface:**
```python
class LearningState:
    """
    Abstract: Learning progression state for TEACHER.
    
    Operations:
    - record_progression(user_id, from_state, to_state)
    - get_current_state(user_id) -> State
    - get_pathway(user_id) -> List[State]
    - recommend_next(user_id) -> List[State]
    
    Constraints:
    - Self-relative only (no peer comparison)
    - States are skill-based, not performance-based
    - Pathways are trees, not linear
    """
    pass
```

**Implementation Choices:**
- State machine (simple)
- Tree structure (pathways)
- Graph structure (prerequisites)

---

#### 3. Permission/Trust State (Governance)

**Abstract Interface:**
```python
class PermissionState:
    """
    Abstract: Permission and trust state tracking.
    
    Operations:
    - grant_permission(user_id, permission)
    - revoke_permission(user_id, permission)
    - get_permissions(user_id) -> Set[Permission]
    - audit_trail(user_id) -> List[PermissionChange]
    
    Constraints:
    - Append-only audit log
    - Immutable history
    - Rollback capability
    """
    pass
```

**Implementation Choices:**
- Linked list (audit trail)
- Stack (rollback)
- Hash table (fast lookup)

---

#### 4. Provider Value Ledger (RECON)

**Abstract Interface:**
```python
class ProviderValueLedger:
    """
    Abstract: Value exchange ledger for RECON.
    
    Operations:
    - record_exchange(provider_id, company_id, value, quality)
    - get_provider_score(provider_id) -> Score
    - get_company_consumption(company_id) -> List[Exchange]
    - calculate_ethics_grade(provider_id) -> Grade
    
    Constraints:
    - Immutable records
    - Aggregated only (no individual data)
    - Minimum cohort sizes
    """
    pass
```

**Implementation Choices:**
- Hash table (fast provider lookup)
- Linked list (immutable ledger)
- Tree (hierarchical aggregation)

---

## Queues (FIFO) → Fairness + Risk Moderation

### CS50's Queue

**First In, First Out** - the order matters.

### TEACHER's Fairness Queues

Queues are **built-in equity mechanisms**.

**Why FIFO matters:**
> "FIFO is a built-in anti-corruption mechanism.  
> It reduces 'influence-based priority' drift."

### Use Cases

#### 1. Content Moderation Review Queue

```python
class ModerationQueue:
    """
    FIFO queue for content moderation.
    
    Ensures:
    - No favoritism
    - Fair review order
    - Timely processing
    """
    def __init__(self):
        self.queue = []  # Simple list as queue
    
    def enqueue(self, item):
        """Add item to back of queue."""
        self.queue.append(item)
    
    def dequeue(self):
        """Remove item from front of queue."""
        if not self.queue:
            return None
        return self.queue.pop(0)
    
    def is_empty(self):
        return len(self.queue) == 0
```

**Fairness guarantee:** First flagged content is first reviewed.

---

#### 2. Teacher Support Ticket Queue

```python
class SupportQueue:
    """
    FIFO queue for teacher support requests.
    
    Ensures:
    - No VIP treatment
    - Fair response time
    - Equal access to help
    """
    pass
```

**Fairness guarantee:** All teachers get support in order of need.

---

#### 3. Permission Upgrade Review Queue

```python
class PermissionReviewQueue:
    """
    FIFO queue for permission upgrade reviews.
    
    Ensures:
    - No influence-based priority
    - Consistent review process
    - Audit trail of review order
    """
    pass
```

**Fairness guarantee:** Permission requests processed in order received.

---

## Stacks (LIFO) → Recovery + Explainability

### CS50's Stack

**Last In, First Out** - recent context first.

### TEACHER's Recovery Stacks

Stacks are **inherently about recent context**.

**Why LIFO matters:**
> "When TEACHER makes a mistake,  
> LIFO gives you clean rollback and narrative clarity."

### Use Cases

#### 1. Session Reasoning Traces

```python
class ReasoningStack:
    """
    Stack for tracking reasoning steps.
    
    Enables:
    - "Why did TEACHER recommend this?"
    - Step-by-step explanation
    - Recent context emphasis
    """
    def __init__(self):
        self.stack = []
    
    def push(self, reasoning_step):
        """Add reasoning step."""
        self.stack.append({
            "step": reasoning_step,
            "timestamp": datetime.now(),
            "context": self._capture_context()
        })
    
    def pop(self):
        """Get most recent reasoning step."""
        if not self.stack:
            return None
        return self.stack.pop()
    
    def explain(self) -> str:
        """Generate explanation from stack."""
        return "\n".join([
            f"Step {i+1}: {step['step']}"
            for i, step in enumerate(reversed(self.stack))
        ])
```

**Explainability guarantee:** Can always explain the most recent decision.

---

#### 2. Undo/Rollback of Governance Actions

```python
class GovernanceRollbackStack:
    """
    Stack for rolling back governance actions.
    
    Enables:
    - Undo bad permission grants
    - Rollback policy changes
    - Restore previous state
    """
    def __init__(self):
        self.action_stack = []
    
    def push_action(self, action):
        """Record governance action."""
        self.action_stack.append({
            "action": action,
            "state_before": self._capture_state(),
            "timestamp": datetime.now()
        })
    
    def rollback(self):
        """Rollback most recent action."""
        if not self.action_stack:
            return None
        
        last_action = self.action_stack.pop()
        self._restore_state(last_action["state_before"])
        return last_action
```

**Safety guarantee:** Can always undo the most recent mistake.

---

## Linked Lists → Audit Streams + Append-Only Truth

### CS50's Linked List

**Sequential access** - perfect for history.

### TEACHER's Audit Lists

Linked lists are **perfect for sequential history**.

**Why linked lists matter:**
> "You get human-legible lineage  
> without pretending you need random access."

### Use Cases

#### 1. Event Log Stream

```python
class AuditLog:
    """
    Append-only audit log using linked list.
    
    Properties:
    - Immutable (append-only)
    - Sequential access
    - Human-legible
    - Tamper-evident
    """
    class LogNode:
        def __init__(self, event, prev=None):
            self.event = event
            self.prev = prev
            self.next = None
            self.hash = self._compute_hash()
    
    def __init__(self):
        self.head = None
        self.tail = None
        self.length = 0
    
    def append(self, event):
        """Append event to log (immutable)."""
        new_node = self.LogNode(event, self.tail)
        
        if self.tail:
            self.tail.next = new_node
        else:
            self.head = new_node
        
        self.tail = new_node
        self.length += 1
    
    def verify_integrity(self) -> bool:
        """Verify log hasn't been tampered."""
        current = self.head
        while current:
            if current.hash != current._compute_hash():
                return False
            current = current.next
        return True
```

**Trust guarantee:** Complete, unalterable history.

---

#### 2. State Transition Narrative

```python
class StateTransitionChain:
    """
    Linked list of state transitions.
    
    Tracks:
    - StateOld → StateNew
    - Complete progression history
    - Narrative of growth
    """
    pass
```

**Learning guarantee:** Can always see the full journey.

---

## Trees (Balanced) → Learning Pathways + Org Structure

### CS50's Trees

**Hierarchical structure** - natural for dependencies.

### TEACHER's Learning Trees

Trees are **natural structure for learning**.

**Why balance matters:**
> "An unbalanced curriculum becomes a 'linked list of burnout.'"

### Use Cases

#### 1. Curriculum Progression Tree

```python
class CurriculumTree:
    """
    Balanced tree for learning pathways.
    
    Properties:
    - Multiple paths to mastery
    - Prerequisite relationships
    - Balanced branching
    - No single point of failure
    """
    class TreeNode:
        def __init__(self, skill_id, skill_name):
            self.skill_id = skill_id
            self.skill_name = skill_name
            self.prerequisites = []  # Children
            self.unlocks = []  # Parents
            self.difficulty = 1
            self.estimated_hours = 0
    
    def __init__(self):
        self.root = None
        self.nodes = {}
    
    def add_skill(self, skill_id, skill_name, prerequisites=None):
        """Add skill to tree."""
        node = self.TreeNode(skill_id, skill_name)
        self.nodes[skill_id] = node
        
        if prerequisites:
            for prereq_id in prerequisites:
                if prereq_id in self.nodes:
                    prereq_node = self.nodes[prereq_id]
                    prereq_node.unlocks.append(node)
                    node.prerequisites.append(prereq_node)
        
        if not self.root:
            self.root = node
    
    def get_pathway(self, target_skill_id) -> List[str]:
        """Get learning pathway to target skill."""
        if target_skill_id not in self.nodes:
            return []
        
        target = self.nodes[target_skill_id]
        pathway = []
        
        def traverse(node, path):
            if not node.prerequisites:
                pathway.append([s.skill_id for s in path + [node]])
                return
            
            for prereq in node.prerequisites:
                traverse(prereq, path + [node])
        
        traverse(target, [])
        return pathway[0] if pathway else []
    
    def ensure_balance(self):
        """Ensure tree is balanced (multiple paths)."""
        # Check for nodes with only one path
        # Add alternative routes
        pass
```

**Fairness guarantee:** Multiple valid paths to mastery.

---

#### 2. Organizational Hierarchy Tree

```python
class OrgHierarchyTree:
    """
    Tree for company/group hierarchies.
    
    Enables:
    - Org structure analysis
    - Permission inheritance
    - Group-based learning
    """
    pass
```

---

## Hash Tables → The Engine of Viable Scale

### CS50's Hash Tables

**Fast lookups** - O(1) average case.

### TEACHER's Identity Hash Tables

Hash tables are the **"daily driver structure"**.

**Use cases:**
- User safe IDs → feature profiles
- RoleId → required competencies
- ProviderId → reliability metrics
- ResourcePath → classification labels

### Implementation

```python
class SafeHashTable:
    """
    Hash table with governance-aware collision handling.
    
    Prevents:
    - Misclassification of roles
    - Merging similar users incorrectly
    - Flattening minority patterns
    """
    def __init__(self, size=1000):
        self.size = size
        self.buckets = [[] for _ in range(size)]
        self.collision_count = 0
    
    def _hash(self, key: str) -> int:
        """Hash function with good distribution."""
        # Use consistent hashing to prevent bias
        hash_value = 0
        for char in key:
            hash_value = (hash_value * 31 + ord(char)) % self.size
        return hash_value
    
    def put(self, key: str, value: Any):
        """Insert key-value pair."""
        index = self._hash(key)
        bucket = self.buckets[index]
        
        # Check for collision
        for i, (k, v) in enumerate(bucket):
            if k == key:
                bucket[i] = (key, value)  # Update existing
                return
        
        # Collision detected
        if bucket:
            self.collision_count += 1
            # Log collision for governance review
            self._log_collision(key, bucket[0][0])
        
        bucket.append((key, value))
    
    def get(self, key: str) -> Optional[Any]:
        """Get value by key."""
        index = self._hash(key)
        bucket = self.buckets[index]
        
        for k, v in bucket:
            if k == key:
                return v
        
        return None
    
    def _log_collision(self, key1: str, key2: str):
        """Log hash collision for governance review."""
        # Collisions might indicate:
        # - Similar users being merged incorrectly
        # - Role misclassification
        # - Bias in hash function
        pass
```

**Governance consideration:**
> "A good hash function here is a justice tool,  
> not just a speed hack."

---

## Tries → Prefix Intelligence

### CS50's Tries

**Prefix matching** - fast autocomplete.

### TEACHER's Concept Tries

Tries enable **magical UX at scale**.

**Use cases:**
- Autocomplete for learning
- Concept search
- Policy search
- Safe content routing

### Implementation

```python
class ConceptTrie:
    """
    Trie for concept/learning autocomplete.
    
    Hybrid approach:
    - Trie front-end (fast prefix matching)
    - Hash-backed storage (efficient memory)
    """
    class TrieNode:
        def __init__(self):
            self.children = {}
            self.is_end = False
            self.concept_id = None
            self.hash_ref = None  # Reference to hash table
    
    def __init__(self):
        self.root = self.TrieNode()
        self.concept_store = {}  # Hash table for full data
    
    def insert(self, concept_name: str, concept_id: str, concept_data: Dict):
        """Insert concept into trie."""
        node = self.root
        
        for char in concept_name.lower():
            if char not in node.children:
                node.children[char] = self.TrieNode()
            node = node.children[char]
        
        node.is_end = True
        node.concept_id = concept_id
        node.hash_ref = concept_id
        
        # Store full data in hash table
        self.concept_store[concept_id] = concept_data
    
    def search_prefix(self, prefix: str) -> List[Dict]:
        """Find all concepts matching prefix."""
        node = self.root
        
        # Navigate to prefix
        for char in prefix.lower():
            if char not in node.children:
                return []
            node = node.children[char]
        
        # Collect all matches
        results = []
        self._collect_matches(node, prefix, results)
        return results
    
    def _collect_matches(self, node, prefix, results):
        """Recursively collect matching concepts."""
        if node.is_end and node.hash_ref:
            results.append(self.concept_store[node.hash_ref])
        
        for char, child in node.children.items():
            self._collect_matches(child, prefix + char, results)
```

**Memory optimization:**
> "Trie front-end + hash-backed storage  
> so you don't burn the planet on pointer forests."

---

## The Big Architectural Takeaway

**Week 5's core insight:**

> **"Every promise TEACHER makes (fairness, safety, personalization)  
> is secretly a data-structure decision."**

### Structure → Promise Mapping

| Structure | Promise | How It Works |
|-----------|---------|--------------|
| **Queue** | Fairness | FIFO = no favoritism |
| **Stack** | Explainability | LIFO = recent context |
| **Linked List** | Trust | Append-only = immutable history |
| **Tree** | Multiple paths | Balanced = no single route |
| **Hash Table** | Scale | Fast lookup = real-world latency |
| **Trie** | UX | Prefix matching = humane interface |

---

## Micro-Labs (CS50-Style)

### Lab 1: TRIBE Lab - "Mentorship Matching at Scale"

**Objective:** Build mentorship matching using hash + tree

**Task:**
1. Build hash index of skills (skill_id → users with skill)
2. Build tree of role progressions
3. For each learner, find 3 mentor candidates
4. Generate explainability note

**Deliverable:**
- Hash table implementation
- Tree traversal algorithm
- Matching function
- Explanation generator

---

### Lab 2: TEACHER Lab - "Curriculum as Balanced Tree"

**Objective:** Show linear vs branching pathways

**Task:**
1. Create linear path version (bad - single route)
2. Create branching pathway version (good - multiple routes)
3. Demonstrate why branching is fairer
4. Implement tree balance check

**Deliverable:**
- Linear curriculum (linked list)
- Branching curriculum (tree)
- Comparison analysis
- Balance enforcement

---

### Lab 3: RECON Lab - "Provider Score Lookup"

**Objective:** Fast provider lookup with collision guardrails

**Task:**
1. Implement hash table for ProviderId → metrics
2. Add collision detection
3. Add fairness checks (prevent misclassification)
4. Implement collision resolution

**Deliverable:**
- Hash table implementation
- Collision handling
- Fairness validation
- Performance analysis

---

### Lab 4: Governance Lab - "Undo the Harm"

**Objective:** Use stack logic for rollback

**Task:**
1. Implement permission grant stack
2. Show rollback of bad permission grant
3. Display audit chain
4. Prove immutability

**Deliverable:**
- Stack implementation
- Rollback function
- Audit chain display
- Safety proof

---

## Assessment: Self-Relative Growth

### Baseline (Before Week 5)

**Question:** "Can you explain how data is organized in your system?"

**Expected Response:**
- May not see structure choices
- May not connect structure to fairness
- May not understand trade-offs

### After Week 5

**Question:** "Can you explain why your structure choices ensure fairness?"

**Expected Response:**
- Can explain structure → fairness mapping
- Can justify structure choices
- Can identify bias risks in structures
- Can design fair structures

---

## Key Takeaways

1. **Structures encode morality.** Queue = fairness, Stack = explainability, Tree = multiple paths.

2. **ADTs define contracts.** Define lens-level objects before implementation.

3. **Hash collisions = bias risk.** Good hash functions are justice tools.

4. **Balance prevents burnout.** Unbalanced trees become linked lists of exhaustion.

5. **Every promise is a structure.** Fairness, safety, personalization all depend on structure choice.

---

## Next Steps

**Week 6+:** Domains & Integration
- Complete TRIBE pipeline with fair structures
- Complete TEACHER pipeline with balanced trees
- Complete RECON pipeline with hash-backed lookups
- Real-world deployment

**For Now:** Practice structure design:
- Queue for fairness
- Stack for rollback
- Tree for pathways
- Hash table for scale

---

## Resources

- **lens_boundary.py:** See structure constraints
- **mvp_extractors.py:** See structure usage
- **pipeline.py:** See structure lifecycle

---

*"Week 5 is where TEACHER's morality becomes architecture: fairness, speed, and safety are encoded into the structures themselves."*

