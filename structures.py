#!/usr/bin/env python3
"""
TEACHER DATA STRUCTURES
=======================
Fair, safe, scalable data structures for TRIBE/TEACHER/RECON.

These structures encode morality:
- Queues = Fairness
- Stacks = Explainability
- Trees = Multiple paths
- Hash Tables = Scale with justice
- Tries = Humane UX
"""

"""
TEACHER DATA STRUCTURES
=======================
Fair, safe, scalable data structures for TRIBE/TEACHER/RECON.

These structures encode morality:
- Queues = Fairness
- Stacks = Explainability
- Trees = Multiple paths
- Hash Tables = Scale with justice
- Tries = Humane UX
"""

# Standard library imports
import hashlib
from collections import deque
from datetime import datetime
from typing import Dict, List, Optional, Any


# =============================================================================
# QUEUE - Fairness Pipeline
# =============================================================================


class FairnessQueue:
    """
    FIFO queue for fairness guarantees.

    Use cases:
    - Content moderation review
    - Teacher support tickets
    - Permission upgrade reviews

    Fairness guarantee: First in, first out = no favoritism
    """

    def __init__(self):
        self.queue = deque()
        self.enqueue_times = {}  # Track fairness metrics
        self.total_processed = 0

    def enqueue(self, item: Any, item_id: Optional[str] = None):
        """Add item to back of queue."""
        item_id = item_id or str(id(item))
        self.queue.append((item, item_id))
        self.enqueue_times[item_id] = datetime.now()

    def dequeue(self) -> Optional[Any]:
        """Remove item from front of queue."""
        if not self.queue:
            return None

        item, item_id = self.queue.popleft()
        self.total_processed += 1

        # Calculate wait time for fairness metrics
        wait_time = (datetime.now() - self.enqueue_times[item_id]).total_seconds()
        del self.enqueue_times[item_id]

        return item, wait_time

    def is_empty(self) -> bool:
        return len(self.queue) == 0

    def size(self) -> int:
        return len(self.queue)

    def get_fairness_metrics(self) -> Dict[str, Any]:
        """Get fairness metrics."""
        if not self.enqueue_times:
            return {"average_wait": 0, "max_wait": 0, "items_waiting": 0}

        current_time = datetime.now()
        wait_times = [
            (current_time - enqueue_time).total_seconds()
            for enqueue_time in self.enqueue_times.values()
        ]

        return {
            "average_wait": sum(wait_times) / len(wait_times) if wait_times else 0,
            "max_wait": max(wait_times) if wait_times else 0,
            "items_waiting": len(wait_times),
            "total_processed": self.total_processed,
        }


# =============================================================================
# STACK - Recovery + Explainability
# =============================================================================


class ReasoningStack:
    """
    Stack for reasoning traces and rollback.

    Use cases:
    - Session reasoning traces
    - Undo/rollback of governance actions
    - Recent-learning emphasis

    Explainability guarantee: Can always explain most recent decision
    """

    def __init__(self):
        self.stack = []

    def push(self, reasoning_step: str, context: Optional[Dict[str, Any]] = None):
        """Add reasoning step to stack."""
        self.stack.append(
            {"step": reasoning_step, "timestamp": datetime.now(), "context": context or {}}
        )

    def pop(self) -> Optional[Dict]:
        """Get most recent reasoning step."""
        if not self.stack:
            return None
        return self.stack.pop()

    def peek(self) -> Optional[Dict]:
        """View most recent step without removing."""
        if not self.stack:
            return None
        return self.stack[-1]

    def explain(self) -> str:
        """Generate explanation from stack (most recent first)."""
        if not self.stack:
            return "No reasoning steps recorded."

        lines = ["Reasoning Trace (most recent first):"]
        for i, step in enumerate(reversed(self.stack)):
            lines.append(f"  {i+1}. {step['step']}")
            if step["context"]:
                lines.append(f"     Context: {step['context']}")

        return "\n".join(lines)

    def rollback(self, steps: int = 1) -> List[Dict]:
        """Rollback last N steps."""
        rolled_back = []
        for _ in range(min(steps, len(self.stack))):
            if self.stack:
                rolled_back.append(self.stack.pop())
        return rolled_back


# =============================================================================
# LINKED LIST - Audit Streams
# =============================================================================


class AuditLogNode:
    """Node in append-only audit log."""

    def __init__(self, event: Dict[str, Any], prev=None):
        self.event = event
        self.prev = prev
        self.next = None
        self.timestamp = datetime.now()
        self.hash = self._compute_hash()

    def _compute_hash(self) -> str:
        """Compute integrity hash."""
        data = f"{self.event}{self.timestamp.isoformat()}"
        if self.prev:
            data += self.prev.hash
        return hashlib.sha256(data.encode()).hexdigest()[:16]


class AuditLog:
    """
    Append-only audit log using linked list.

    Properties:
    - Immutable (append-only)
    - Sequential access
    - Human-legible
    - Tamper-evident
    """

    def __init__(self):
        self.head = None
        self.tail = None
        self.length = 0

    def append(self, event: Dict[str, Any]):
        """Append event to log (immutable)."""
        new_node = AuditLogNode(event, self.tail)

        if self.tail:
            self.tail.next = new_node
        else:
            self.head = new_node

        self.tail = new_node
        self.length += 1

    def verify_integrity(self) -> bool:
        """Verify log hasn't been tampered."""
        current = self.head
        prev_hash = None

        while current:
            # Recompute hash
            data = f"{current.event}{current.timestamp.isoformat()}"
            if prev_hash:
                data += prev_hash
            expected_hash = hashlib.sha256(data.encode()).hexdigest()[:16]

            if current.hash != expected_hash:
                return False

            prev_hash = current.hash
            current = current.next

        return True

    def get_history(self, limit: Optional[int] = None) -> List[Dict]:
        """Get audit history (sequential access)."""
        history = []
        current = self.head
        count = 0

        while current and (limit is None or count < limit):
            history.append(
                {
                    "event": current.event,
                    "timestamp": current.timestamp.isoformat(),
                    "hash": current.hash,
                }
            )
            current = current.next
            count += 1

        return history


# =============================================================================
# TREE - Learning Pathways
# =============================================================================


class CurriculumTreeNode:
    """Node in curriculum tree."""

    def __init__(self, skill_id: str, skill_name: str):
        self.skill_id = skill_id
        self.skill_name = skill_name
        self.prerequisites: List["CurriculumTreeNode"] = []  # Children (must complete these first)
        self.unlocks: List["CurriculumTreeNode"] = []  # Parents (this unlocks these)
        self.difficulty = 1
        self.estimated_hours = 0

    def add_prerequisite(self, prereq_node):
        """Add prerequisite relationship."""
        if prereq_node not in self.prerequisites:
            self.prerequisites.append(prereq_node)
        if self not in prereq_node.unlocks:
            prereq_node.unlocks.append(self)


class CurriculumTree:
    """
    Balanced tree for learning pathways.

    Properties:
    - Multiple paths to mastery
    - Prerequisite relationships
    - Balanced branching
    - No single point of failure
    """

    def __init__(self):
        self.root = None
        self.nodes: Dict[str, CurriculumTreeNode] = {}

    def add_skill(self, skill_id: str, skill_name: str, prerequisites: Optional[List[str]] = None):
        """Add skill to tree."""
        if skill_id in self.nodes:
            return self.nodes[skill_id]

        node = CurriculumTreeNode(skill_id, skill_name)
        self.nodes[skill_id] = node

        if prerequisites:
            for prereq_id in prerequisites:
                if prereq_id in self.nodes:
                    prereq_node = self.nodes[prereq_id]
                    node.add_prerequisite(prereq_node)

        if not self.root:
            self.root = node

        return node

    def get_pathway(self, target_skill_id: str) -> List[List[str]]:
        """Get all learning pathways to target skill."""
        if target_skill_id not in self.nodes:
            return []

        target = self.nodes[target_skill_id]
        pathways = []

        def traverse(node: CurriculumTreeNode, path: List[str]):
            """Recursively find all paths."""
            current_path = path + [node.skill_id]

            if not node.prerequisites:
                # Leaf node - complete pathway
                pathways.append(current_path)
                return

            # Multiple prerequisites = multiple paths
            for prereq in node.prerequisites:
                traverse(prereq, current_path)

        traverse(target, [])
        return pathways

    def ensure_balance(self):
        """Ensure tree is balanced (multiple paths exist)."""
        unbalanced = []

        for skill_id, node in self.nodes.items():
            # Check if node has only one path (unbalanced)
            if len(node.prerequisites) == 1 and len(node.unlocks) == 0:
                # This is a linear path - suggest alternatives
                unbalanced.append(skill_id)

        return unbalanced

    def get_alternate_paths(self, skill_id: str) -> List[List[str]]:
        """Get alternate pathways to a skill."""
        pathways = self.get_pathway(skill_id)

        if len(pathways) > 1:
            return pathways
        else:
            # Only one path - suggest adding alternatives
            return []


# =============================================================================
# HASH TABLE - Scale with Justice
# =============================================================================


class SafeHashTable:
    """
    Hash table with governance-aware collision handling.

    Prevents:
    - Misclassification of roles
    - Merging similar users incorrectly
    - Flattening minority patterns
    """

    def __init__(self, size: int = 1000):
        self.size = size
        self.buckets: List[List[tuple[str, Any]]] = [[] for _ in range(size)]
        self.collision_count = 0
        self.collision_log: List[Dict[str, Any]] = []

    def _hash(self, key: str) -> int:
        """Hash function with good distribution."""
        # Consistent hashing to prevent bias
        hash_value = 0
        for char in key:
            hash_value = (hash_value * 31 + ord(char)) % self.size
        return hash_value

    def put(self, key: str, value: Any):
        """Insert key-value pair."""
        index = self._hash(key)
        bucket = self.buckets[index]

        # Check for existing key
        for i, (k, v) in enumerate(bucket):
            if k == key:
                bucket[i] = (key, value)  # Update existing
                return

        # Collision detected (bucket not empty)
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
        self.collision_log.append(
            {
                "key1": key1,
                "key2": key2,
                "timestamp": datetime.now().isoformat(),
                "note": "Collision may indicate: similar users merged, role misclassification, or bias in hash function",
            }
        )

    def get_collision_report(self) -> Dict[str, Any]:
        """Get collision analysis report."""
        return {
            "total_collisions": self.collision_count,
            "collision_rate": self.collision_count / max(self.size, 1),
            "collisions": self.collision_log[:10],  # Top 10
            "recommendation": "Review collisions for potential bias or misclassification",
        }


# =============================================================================
# TRIE - Prefix Intelligence
# =============================================================================


class ConceptTrieNode:
    """Node in concept trie."""

    def __init__(self):
        self.children = {}
        self.is_end = False
        self.concept_id = None
        self.hash_ref = None  # Reference to hash table


class ConceptTrie:
    """
    Trie for concept/learning autocomplete.

    Hybrid approach:
    - Trie front-end (fast prefix matching)
    - Hash-backed storage (efficient memory)
    """

    def __init__(self):
        self.root = ConceptTrieNode()
        self.concept_store = {}  # Hash table for full data

    def insert(self, concept_name: str, concept_id: str, concept_data: Dict):
        """Insert concept into trie."""
        node = self.root

        for char in concept_name.lower():
            if char not in node.children:
                node.children[char] = ConceptTrieNode()
            node = node.children[char]

        node.is_end = True
        node.concept_id = concept_id
        node.hash_ref = concept_id

        # Store full data in hash table
        self.concept_store[concept_id] = concept_data

    def search_prefix(self, prefix: str, limit: int = 5) -> List[Dict]:
        """Find all concepts matching prefix."""
        node = self.root

        # Navigate to prefix
        for char in prefix.lower():
            if char not in node.children:
                return []
            node = node.children[char]

        # Collect all matches
        results: List[Dict[str, Any]] = []
        self._collect_matches(node, prefix.lower(), results, limit)
        return results

    def _collect_matches(self, node: ConceptTrieNode, prefix: str, results: List[Dict], limit: int):
        """Recursively collect matching concepts."""
        if len(results) >= limit:
            return

        if node.is_end and node.hash_ref:
            if node.hash_ref in self.concept_store:
                results.append(self.concept_store[node.hash_ref])

        for char, child in node.children.items():
            if len(results) < limit:
                self._collect_matches(child, prefix + char, results, limit)


# =============================================================================
# DEMO
# =============================================================================


def main():
    """Demonstrate TEACHER data structures."""
    print("=" * 70)
    print("  TEACHER WEEK 5: STRUCTURES OF FAIRNESS")
    print("  Where Morality Becomes Architecture")
    print("=" * 70)

    # ========================================================================
    # QUEUE - Fairness
    # ========================================================================
    print("\n[QUEUE] Fairness Pipeline")
    print("-" * 70)

    moderation_queue = FairnessQueue()
    moderation_queue.enqueue("Content A", "content_1")
    moderation_queue.enqueue("Content B", "content_2")
    moderation_queue.enqueue("Content C", "content_3")

    item1, wait1 = moderation_queue.dequeue()
    item2, wait2 = moderation_queue.dequeue()

    print(f"  Processed: {item1} (waited {wait1:.3f}s)")
    print(f"  Processed: {item2} (waited {wait2:.3f}s)")
    print("  Fairness: FIFO order ensures no favoritism")

    metrics = moderation_queue.get_fairness_metrics()
    print(f"  Metrics: {metrics}")

    # ========================================================================
    # STACK - Explainability
    # ========================================================================
    print("\n[STACK] Reasoning Trace")
    print("-" * 70)

    reasoning = ReasoningStack()
    reasoning.push("User has high activity count")
    reasoning.push("Compared to role baseline")
    reasoning.push("Activity pattern suggests collaboration")
    reasoning.push("Recommendation: Potential mentor")

    explanation = reasoning.explain()
    print(explanation)

    # ========================================================================
    # LINKED LIST - Audit Log
    # ========================================================================
    print("\n[LINKED LIST] Append-Only Audit Log")
    print("-" * 70)

    audit_log = AuditLog()
    audit_log.append({"action": "permission_grant", "user": "entity_123"})
    audit_log.append({"action": "permission_revoke", "user": "entity_456"})

    history = audit_log.get_history()
    print(f"  Log entries: {len(history)}")
    for entry in history:
        print(f"    {entry['timestamp']}: {entry['event']}")

    integrity = audit_log.verify_integrity()
    print(f"  Integrity verified: {integrity}")

    # ========================================================================
    # TREE - Learning Pathways
    # ========================================================================
    print("\n[TREE] Curriculum Pathways")
    print("-" * 70)

    curriculum = CurriculumTree()
    curriculum.add_skill("basics", "Basics")
    curriculum.add_skill("intermediate", "Intermediate", ["basics"])
    curriculum.add_skill("advanced", "Advanced", ["intermediate"])
    curriculum.add_skill("expert", "Expert", ["advanced"])

    pathways = curriculum.get_pathway("expert")
    print(f"  Pathways to 'expert': {len(pathways)}")
    for i, path in enumerate(pathways):
        print(f"    Path {i+1}: {' -> '.join(path)}")

    # ========================================================================
    # HASH TABLE - Scale
    # ========================================================================
    print("\n[HASH TABLE] Fast Lookups with Justice")
    print("-" * 70)

    provider_table = SafeHashTable(size=100)
    provider_table.put("provider_aws", {"reliability": 0.998, "grade": "A"})
    provider_table.put("provider_google", {"reliability": 0.995, "grade": "A"})
    provider_table.put("provider_azure", {"reliability": 0.992, "grade": "B"})

    aws_score = provider_table.get("provider_aws")
    print(f"  AWS score: {aws_score}")

    collision_report = provider_table.get_collision_report()
    print(f"  Collisions: {collision_report['total_collisions']}")

    # ========================================================================
    # TRIE - Autocomplete
    # ========================================================================
    print("\n[TRIE] Concept Autocomplete")
    print("-" * 70)

    concept_trie = ConceptTrie()
    concept_trie.insert("collaboration", "skill_1", {"name": "Collaboration", "category": "social"})
    concept_trie.insert("communication", "skill_2", {"name": "Communication", "category": "social"})
    concept_trie.insert("coding", "skill_3", {"name": "Coding", "category": "technical"})

    matches = concept_trie.search_prefix("co")
    print(f"  Matches for 'co': {len(matches)}")
    for match in matches:
        print(f"    - {match['name']}")

    # ========================================================================
    # SUMMARY
    # ========================================================================
    print("\n" + "=" * 70)
    print("  KEY TAKEAWAYS")
    print("=" * 70)
    print("  1. Queue = Fairness (FIFO = no favoritism)")
    print("  2. Stack = Explainability (LIFO = recent context)")
    print("  3. Linked List = Trust (append-only = immutable)")
    print("  4. Tree = Multiple Paths (balanced = fair)")
    print("  5. Hash Table = Scale (fast lookup = real-world latency)")
    print("  6. Trie = UX (prefix matching = humane interface)")
    print("\n  Every promise TEACHER makes is a data-structure decision.")
    print("=" * 70 + "\n")


if __name__ == "__main__":
    main()
