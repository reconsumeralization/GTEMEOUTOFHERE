# Applying CS50 Concepts to COSURVIVAL Codebase

This document maps CS50 concepts from each week to specific improvements and enhancements for the COSURVIVAL (TRIBE/TEACHER/RECON) system.

---

## Week 0: Computational Thinking & Problem Decomposition

### Current State
- Pipeline is well-structured with clear separation of concerns
- Good use of functions and modules

### Improvements to Apply

**1. Scratch-style Visual Flow Diagrams**
```python
# Add to README.md or create visual_pipeline.py
def visualize_pipeline():
    """
    Create a visual representation of the pipeline flow.
    Like Scratch blocks, but in code comments.
    """
    # [START] User provides CSV
    #   ↓
    # [GOVERNANCE CHECK] PII detection, bias guardrails
    #   ↓ (if pass)
    # [INGEST] Load CSV, normalize schema
    #   ↓
    # [EXTRACT] Users, Companies, Providers, Activities
    #   ↓
    # [TRIBE] Build graph, find communities
    # [TEACHER] Build skill matrix, track progressions
    # [RECON] Score providers, calculate value flows
    #   ↓
    # [UNIFY] Combine all three lenses
    #   ↓
    # [EXPORT] JSON for dashboard
    # [END]
```

**2. Event-Driven Architecture (like Scratch events)**
```python
# Add to pipeline.py
class PipelineEvent:
    """Event-driven pipeline, like Scratch's 'when flag clicked'"""
    def __init__(self):
        self.listeners = []
    
    def on_governance_pass(self, callback):
        """Register callback for governance pass event"""
        self.listeners.append(callback)
    
    def trigger(self, event_type, data):
        """Trigger event, like Scratch broadcasts"""
        for listener in self.listeners:
            if listener.event_type == event_type:
                listener(data)
```

---

## Week 1: C Fundamentals - Memory, Types, Compilation

### Current State
- Python abstracts away memory management
- No explicit type checking in many places

### Improvements to Apply

**1. Type Hints (Python's equivalent of C types)**
```python
# Improve extractors/ingest.py
from typing import Dict, List, Tuple, Optional, Any

def extract_entities(df: pd.DataFrame, 
                     pii_handler: Optional[PIIHandler] = None) -> Tuple[Dict[str, CanonicalUser], 
                                                                         Dict[str, CanonicalCompany],
                                                                         Dict[str, CanonicalProvider],
                                                                         List[CanonicalActivity]]:
    """
    Explicit return types - like C function signatures.
    Makes code self-documenting and catchable by type checkers.
    """
    # ... existing code ...
```

**2. Constants (like C's #define)**
```python
# Add to governance.py or create constants.py
# Week 1 concept: Use constants instead of magic numbers/strings

# Column name patterns (like C macros)
UID_PATTERNS = ["uid", "userid", "user_id", "UserId", "UserID"]
EMAIL_PATTERNS = ["email", "mail", "Email", "EmailAddress"]
COMPANY_PATTERNS = ["companyid", "CompanyId", "orgid", "OrganizationId"]

# Thresholds (like C constants)
MIN_COMMUNITY_SIZE = 3  # Minimum users for valid community
MAX_PII_LENGTH = 256    # Maximum PII field length before truncation
HASH_SALT_LENGTH = 32   # Salt length for hashing

# Use in code:
def is_uid_column(col_name: str) -> bool:
    """Check if column matches UID pattern"""
    return any(pattern.lower() in col_name.lower() for pattern in UID_PATTERNS)
```

**3. Error Handling (like C's error codes)**
```python
# Add to pipeline.py
class PipelineErrorCode:
    """Error codes - like C's exit status"""
    SUCCESS = 0
    FILE_NOT_FOUND = 1
    GOVERNANCE_FAIL = 2
    INVALID_SCHEMA = 3
    MEMORY_ERROR = 4
    UNKNOWN_ERROR = 5

def run_pipeline(csv_path: str) -> int:
    """Returns error code, like C main()"""
    try:
        # ... pipeline code ...
        return PipelineErrorCode.SUCCESS
    except FileNotFoundError:
        return PipelineErrorCode.FILE_NOT_FOUND
    except GovernanceViolation:
        return PipelineErrorCode.GOVERNANCE_FAIL
    # ... etc
```

**4. Memory Efficiency (Python equivalents)**
```python
# Improve extractors/ingest.py - use generators for large files
def ingest_csv_streaming(filepath: str):
    """
    Week 1 concept: Process data in chunks to avoid memory overflow.
    Like C's careful memory management, but Pythonic.
    """
    chunk_size = 10000  # Process 10k rows at a time
    for chunk in pd.read_csv(filepath, chunksize=chunk_size):
        yield chunk  # Generator - memory efficient
```

---

## Week 2: Arrays, Strings, Command-Line Arguments

### Current State
- Uses pandas DataFrames (like 2D arrays)
- Command-line args in rapid_pipeline.py

### Improvements to Apply

**1. Array-like Operations (Week 2 concepts)**
```python
# Add to extractors/tribe_graph.py
def find_most_connected_users(graph: Dict, top_n: int = 10) -> List[Tuple[str, int]]:
    """
    Week 2: Array operations - find top N users by connections.
    Like C's array sorting/searching.
    """
    # Count connections (like iterating through array)
    connection_counts = []
    for node in graph.get("nodes", []):
        count = sum(1 for edge in graph.get("edges", [])
                   if edge["source"] == node or edge["target"] == node)
        connection_counts.append((node, count))
    
    # Sort (like C's qsort)
    connection_counts.sort(key=lambda x: x[1], reverse=True)
    
    # Return top N (like array slicing)
    return connection_counts[:top_n]
```

**2. String Manipulation (Week 2 concepts)**
```python
# Improve governance.py - better string handling
def normalize_column_name(name: str) -> str:
    """
    Week 2: String manipulation - normalize column names.
    Like C's string functions (strcmp, strcpy, etc.)
    """
    # Remove whitespace, convert to lowercase
    normalized = name.strip().lower()
    
    # Replace common variations (like string replacement)
    replacements = {
        "userid": "uid",
        "user_id": "uid",
        "companyid": "company_id",
        "providerid": "provider_id"
    }
    
    for old, new in replacements.items():
        if old in normalized:
            normalized = normalized.replace(old, new)
    
    return normalized
```

**3. Command-Line Arguments (Week 2 concepts)**
```python
# Improve rapid_pipeline.py - use argparse (better than sys.argv)
import argparse

def main():
    """
    Week 2: Proper command-line argument handling.
    Like C's argc/argv, but more robust.
    """
    parser = argparse.ArgumentParser(
        description="COSURVIVAL Rapid Pipeline - Process CSV to TRIBE/TEACHER/RECON JSON"
    )
    parser.add_argument("csv_path", help="Path to input CSV file")
    parser.add_argument("-o", "--output", default="cosurvival_output.json",
                       help="Output JSON file path")
    parser.add_argument("-v", "--verbose", action="store_true",
                       help="Enable verbose output")
    parser.add_argument("--skip-governance", action="store_true",
                       help="Skip governance checks (NOT RECOMMENDED)")
    
    args = parser.parse_args()
    
    if args.verbose:
        print(f"Processing: {args.csv_path}")
        print(f"Output: {args.output}")
    
    # ... rest of pipeline ...
```

**4. Parallel Arrays Pattern (Week 2 concept)**
```python
# Add to extractors/teacher_paths.py
def build_role_skill_parallel_arrays(activities: List) -> Tuple[List[str], List[List[str]]]:
    """
    Week 2: Parallel arrays pattern.
    Instead of dict, use two arrays that correspond by index.
    """
    roles = []      # Array 1: Role names
    skills = []     # Array 2: Skills for each role (parallel)
    
    for activity in activities:
        role = getattr(activity, 'role', '')
        skill = getattr(activity, 'skill', '')
        
        if role in roles:
            idx = roles.index(role)
            if skill not in skills[idx]:
                skills[idx].append(skill)
        else:
            roles.append(role)
            skills.append([skill])
    
    return roles, skills  # Parallel arrays
```

---

## Week 3: Algorithms, Big O, Search & Sort

### Current State
- Uses NetworkX for graph algorithms
- Some inefficient iterations

### Improvements to Apply

**1. Algorithm Analysis (Week 3 concepts)**
```python
# Add algorithm complexity comments throughout
def extract_communities(graph: Dict) -> List[List[str]]:
    """
    Week 3: Algorithm analysis.
    
    Time Complexity: O(V + E) where V = vertices, E = edges
    Space Complexity: O(V) for visited set
    
    Uses depth-first search (DFS) for connected components.
    """
    # ... implementation ...
```

**2. Binary Search (Week 3 concept)**
```python
# Add to extractors/recon_scores.py
def find_provider_by_score(providers: List[Dict], target_score: float) -> Optional[Dict]:
    """
    Week 3: Binary search for sorted provider list.
    O(log n) instead of O(n) linear search.
    """
    # Sort providers by score first (O(n log n))
    sorted_providers = sorted(providers, key=lambda p: p.get('score', 0))
    
    # Binary search (O(log n))
    left, right = 0, len(sorted_providers) - 1
    
    while left <= right:
        mid = (left + right) // 2
        mid_score = sorted_providers[mid].get('score', 0)
        
        if mid_score == target_score:
            return sorted_providers[mid]
        elif mid_score < target_score:
            left = mid + 1
        else:
            right = mid - 1
    
    return None
```

**3. Merge Sort Pattern (Week 3 concept)**
```python
# Add to extractors/export_json.py
def merge_tribe_teacher_recon(tribe: Dict, teacher: Dict, recon: Dict) -> Dict:
    """
    Week 3: Merge pattern (like merge sort).
    Combine three sorted/structured datasets efficiently.
    """
    # Divide: Three separate datasets
    # Conquer: Merge into unified structure
    
    unified = {
        "metadata": {
            "generated_at": datetime.now().isoformat(),
            "version": "1.0"
        },
        "tribe": tribe,
        "teacher": teacher,
        "recon": recon,
        "cross_lens_insights": merge_cross_lens_data(tribe, teacher, recon)
    }
    
    return unified

def merge_cross_lens_data(tribe: Dict, teacher: Dict, recon: Dict) -> Dict:
    """Merge insights that span multiple lenses"""
    # Like merge sort's merge step
    insights = []
    
    # Merge user data from all three lenses
    tribe_users = set(tribe.get("users", []))
    teacher_users = set(teacher.get("users", []))
    recon_users = set(recon.get("users", []))
    
    # Find intersection (users in all three)
    common_users = tribe_users & teacher_users & recon_users
    
    return {"users_in_all_lenses": list(common_users)}
```

**4. Selection Sort Pattern (Week 3 concept)**
```python
# Add to extractors/tribe_graph.py
def find_top_mentors_simple(graph: Dict, n: int = 10) -> List[str]:
    """
    Week 3: Selection sort pattern - find top N without full sort.
    More efficient than sorting entire list if n << total.
    """
    # Like selection sort: find max, remove, repeat
    mentors = []
    connections = count_connections(graph)
    
    for _ in range(min(n, len(connections))):
        # Find user with most connections (like finding max)
        max_user = max(connections.items(), key=lambda x: x[1])
        mentors.append(max_user[0])
        del connections[max_user[0]]  # Remove from consideration
    
    return mentors
```

---

## Week 4: Memory, Pointers, File I/O

### Current State
- Uses pandas for file I/O
- No explicit memory management

### Improvements to Apply

**1. File I/O Patterns (Week 4 concepts)**
```python
# Add to extractors/ingest.py - explicit file handling
def ingest_csv_safe(filepath: str) -> pd.DataFrame:
    """
    Week 4: Proper file I/O with error handling.
    Like C's fopen/fread/fclose pattern.
    """
    file_handle = None
    try:
        # fopen equivalent
        file_handle = open(filepath, 'r', encoding='utf-8')
        
        # Check file size (like fseek/ftell)
        file_handle.seek(0, 2)  # Seek to end
        file_size = file_handle.tell()
        file_handle.seek(0)      # Reset to beginning
        
        if file_size > 100 * 1024 * 1024:  # 100MB limit
            raise ValueError("File too large for safe processing")
        
        # fread equivalent (pandas handles this)
        df = pd.read_csv(file_handle)
        return df
        
    except FileNotFoundError:
        print(f"Error: File not found: {filepath}")
        raise
    except PermissionError:
        print(f"Error: Permission denied: {filepath}")
        raise
    finally:
        # fclose equivalent
        if file_handle:
            file_handle.close()
```

**2. Memory Management Patterns (Week 4 concepts)**
```python
# Add to pipeline.py - explicit resource management
from contextlib import contextmanager

@contextmanager
def managed_pipeline_resources():
    """
    Week 4: Memory management pattern.
    Like C's malloc/free, but Pythonic with context managers.
    """
    resources = {
        'dataframes': [],
        'graphs': [],
        'large_dicts': []
    }
    
    try:
        yield resources
    finally:
        # Free resources (like C's free())
        for df in resources['dataframes']:
            del df
        for graph in resources['graphs']:
            del graph
        for d in resources['large_dicts']:
            d.clear()
        
        import gc
        gc.collect()  # Force garbage collection
```

**3. Pointer-like References (Week 4 concepts)**
```python
# Add to models.py - use references efficiently
from typing import Optional

@dataclass
class ActivityNode:
    """
    Week 4: Pointer-like structure.
    Like C's struct with pointers to other nodes.
    """
    activity: CanonicalActivity
    user_ref: Optional['UserNode'] = None  # "Pointer" to user
    provider_ref: Optional['ProviderNode'] = None  # "Pointer" to provider
    
    def link_user(self, user: 'UserNode'):
        """Like setting a pointer in C"""
        self.user_ref = user
    
    def follow_user(self) -> Optional['UserNode']:
        """Like dereferencing a pointer in C"""
        return self.user_ref
```

**4. Buffer Management (Week 4 concepts)**
```python
# Add to extractors/ingest.py
def process_csv_in_chunks(filepath: str, chunk_size: int = 10000):
    """
    Week 4: Buffer management pattern.
    Process data in fixed-size chunks to avoid buffer overflow.
    """
    buffer = []  # Like C's buffer array
    buffer_size = 0
    
    for chunk in pd.read_csv(filepath, chunksize=chunk_size):
        # Process chunk (like filling buffer)
        buffer.append(chunk)
        buffer_size += len(chunk)
        
        # Flush buffer when full (like writing buffer to file)
        if buffer_size >= chunk_size * 10:  # 10 chunks
            yield pd.concat(buffer, ignore_index=True)
            buffer = []
            buffer_size = 0
    
    # Flush remaining
    if buffer:
        yield pd.concat(buffer, ignore_index=True)
```

---

## Week 5: Data Structures - Linked Lists, Trees, Hash Tables, Tries

### Current State
- Uses NetworkX graphs (like trees)
- Uses Python dicts (hash tables)

### Improvements to Apply

**1. Linked List Pattern (Week 5 concept)**
```python
# Add to models.py
@dataclass
class ActivityNode:
    """
    Week 5: Linked list node structure.
    Like C's struct with next pointer.
    """
    activity: CanonicalActivity
    next: Optional['ActivityNode'] = None
    
    def append(self, activity: CanonicalActivity):
        """Append to end of list"""
        current = self
        while current.next:
            current = current.next
        current.next = ActivityNode(activity)
    
    def find(self, activity_id: str) -> Optional['ActivityNode']:
        """Search linked list"""
        current = self
        while current:
            if current.activity.id == activity_id:
                return current
            current = current.next
        return None
```

**2. Binary Search Tree (Week 5 concept)**
```python
# Add to extractors/teacher_paths.py
@dataclass
class SkillTreeNode:
    """
    Week 5: Binary search tree for skills.
    Enables O(log n) skill lookups.
    """
    skill: str
    role: str
    left: Optional['SkillTreeNode'] = None
    right: Optional['SkillTreeNode'] = None
    
    def insert(self, skill: str, role: str):
        """Insert into BST"""
        if skill < self.skill:
            if self.left:
                self.left.insert(skill, role)
            else:
                self.left = SkillTreeNode(skill, role)
        elif skill > self.skill:
            if self.right:
                self.right.insert(skill, role)
            else:
                self.right = SkillTreeNode(skill, role)
    
    def search(self, skill: str) -> Optional['SkillTreeNode']:
        """Search BST - O(log n)"""
        if skill == self.skill:
            return self
        elif skill < self.skill and self.left:
            return self.left.search(skill)
        elif skill > self.skill and self.right:
            return self.right.search(skill)
        return None
```

**3. Hash Table Implementation (Week 5 concept)**
```python
# Add to extractors/tribe_graph.py
class SimpleHashTable:
    """
    Week 5: Custom hash table implementation.
    Understand how Python dicts work under the hood.
    """
    def __init__(self, size: int = 1000):
        self.size = size
        self.buckets = [[] for _ in range(size)]  # Array of linked lists
    
    def _hash(self, key: str) -> int:
        """Hash function - like CS50's hash function"""
        hash_value = 0
        for char in key:
            hash_value = (hash_value * 31 + ord(char)) % self.size
        return hash_value
    
    def insert(self, key: str, value: Any):
        """Insert with collision handling (chaining)"""
        bucket_idx = self._hash(key)
        bucket = self.buckets[bucket_idx]
        
        # Check if key already exists
        for i, (k, v) in enumerate(bucket):
            if k == key:
                bucket[i] = (key, value)  # Update
                return
        
        # Append to bucket (chaining)
        bucket.append((key, value))
    
    def lookup(self, key: str) -> Optional[Any]:
        """Lookup - O(1) average case"""
        bucket_idx = self._hash(key)
        bucket = self.buckets[bucket_idx]
        
        for k, v in bucket:
            if k == key:
                return v
        return None
```

**4. Trie for Prefix Matching (Week 5 concept)**
```python
# Add to extractors/teacher_paths.py
class SkillTrie:
    """
    Week 5: Trie data structure for skill prefix matching.
    Useful for autocomplete in TEACHER system.
    """
    def __init__(self):
        self.children = {}  # Dict of char -> TrieNode
        self.is_end = False
        self.skills = []  # Skills ending at this node
    
    def insert(self, skill: str):
        """Insert skill into trie"""
        node = self
        for char in skill.lower():
            if char not in node.children:
                node.children[char] = SkillTrie()
            node = node.children[char]
        node.is_end = True
        node.skills.append(skill)
    
    def search_prefix(self, prefix: str) -> List[str]:
        """Find all skills with given prefix - O(m) where m = prefix length"""
        node = self
        for char in prefix.lower():
            if char not in node.children:
                return []
            node = node.children[char]
        
        # Collect all skills from this subtree
        results = []
        self._collect_all(node, results)
        return results
    
    def _collect_all(self, node: 'SkillTrie', results: List[str]):
        """DFS to collect all skills"""
        if node.is_end:
            results.extend(node.skills)
        for child in node.children.values():
            self._collect_all(child, results)
```

---

## Week 6: Python - High-Level Abstractions

### Current State
- Already using Python extensively
- Good use of dataclasses, type hints

### Improvements to Apply

**1. Pythonic Patterns (Week 6 concepts)**
```python
# Improve extractors/ingest.py - more Pythonic
def extract_entities_pythonic(df: pd.DataFrame) -> Tuple[Dict, Dict, Dict, List]:
    """
    Week 6: Pythonic code - list comprehensions, dict comprehensions.
    """
    # List comprehension instead of loop
    activities = [
        CanonicalActivity(
            id=f"act_{idx}",
            timestamp=str(row.get('Date', '')),
            activity_type=str(row.get('Type', '')),
            user_id=hash_pii(row.get('Uid', ''))
        )
        for idx, row in df.iterrows()
        if pd.notna(row.get('Type'))
    ]
    
    # Dict comprehension for users
    users = {
        hash_pii(uid): CanonicalUser(id=hash_pii(uid))
        for uid in df['Uid'].dropna().unique()
        if hash_pii(uid)
    }
    
    # Set operations (Python sets)
    active_users = {a.user_id for a in activities if a.user_id}
    
    return users, companies, providers, activities
```

**2. Exception Handling (Week 6 concepts)**
```python
# Improve rapid_pipeline.py - better exception handling
def run_rapid_pipeline(csv_path: str, output_path: str = "cosurvival_output.json"):
    """
    Week 6: Python exception handling - try/except.
    """
    try:
        df = ingest_csv(csv_path)
    except FileNotFoundError:
        print(f"Error: File not found: {csv_path}")
        return None
    except pd.errors.EmptyDataError:
        print("Error: CSV file is empty")
        return None
    except pd.errors.ParserError as e:
        print(f"Error: Could not parse CSV: {e}")
        return None
    except Exception as e:
        print(f"Unexpected error: {e}")
        import traceback
        traceback.print_exc()
        return None
```

**3. Python Libraries (Week 6 concepts)**
```python
# Add to requirements.txt and use in code
# collections.Counter for frequency counting
from collections import Counter

def count_activity_types(activities: List[CanonicalActivity]) -> Dict[str, int]:
    """
    Week 6: Use Python's Counter instead of manual counting.
    """
    types = [a.activity_type for a in activities]
    return dict(Counter(types))

# Use itertools for efficient iteration
from itertools import groupby

def group_activities_by_user(activities: List[CanonicalActivity]) -> Dict[str, List]:
    """
    Week 6: Use itertools.groupby for grouping.
    """
    sorted_activities = sorted(activities, key=lambda a: a.user_id)
    return {
        user_id: list(group)
        for user_id, group in groupby(sorted_activities, key=lambda a: a.user_id)
    }
```

**4. F-strings and String Formatting (Week 6 concepts)**
```python
# Improve all print statements - use f-strings
def print_pipeline_summary(tribe: Dict, teacher: Dict, recon: Dict):
    """
    Week 6: Use f-strings for string formatting.
    """
    print(f"""
    Pipeline Summary:
    =================
    TRIBE:    {len(tribe.get('communities', []))} communities
    TEACHER:  {len(teacher.get('role_skill_matrix', {}))} roles
    RECON:    {len(recon.get('provider_scores', {}))} providers
    
    Generated at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
    """)
```

---

## Week 7: SQL - Databases and Relational Data

### Current State
- Processes CSV files (flat-file database)
- No SQL database integration

### Improvements to Apply

**1. SQLite Integration (Week 7 concepts)**
```python
# Add database.py
import sqlite3
from cs50 import SQL

def create_cosurvival_db(db_path: str = "cosurvival.db"):
    """
    Week 7: Create SQLite database for COSURVIVAL data.
    """
    db = SQL(f"sqlite:///{db_path}")
    
    # Create tables
    db.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id TEXT PRIMARY KEY,
            company_id TEXT,
            activity_count INTEGER DEFAULT 0,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (company_id) REFERENCES companies(id)
        )
    """)
    
    db.execute("""
        CREATE TABLE IF NOT EXISTS companies (
            id TEXT PRIMARY KEY,
            name TEXT,
            activity_count INTEGER DEFAULT 0
        )
    """)
    
    db.execute("""
        CREATE TABLE IF NOT EXISTS activities (
            id TEXT PRIMARY KEY,
            user_id TEXT,
            company_id TEXT,
            provider_id TEXT,
            activity_type TEXT,
            timestamp TEXT,
            state_before TEXT,
            state_after TEXT,
            FOREIGN KEY (user_id) REFERENCES users(id),
            FOREIGN KEY (company_id) REFERENCES companies(id),
            FOREIGN KEY (provider_id) REFERENCES providers(id)
        )
    """)
    
    db.execute("""
        CREATE TABLE IF NOT EXISTS providers (
            id TEXT PRIMARY KEY,
            name TEXT,
            activity_count INTEGER DEFAULT 0,
            error_count INTEGER DEFAULT 0
        )
    """)
    
    # Create indexes for performance (Week 7 concept)
    db.execute("CREATE INDEX IF NOT EXISTS idx_activities_user ON activities(user_id)")
    db.execute("CREATE INDEX IF NOT EXISTS idx_activities_company ON activities(company_id)")
    db.execute("CREATE INDEX IF NOT EXISTS idx_activities_provider ON activities(provider_id)")
    db.execute("CREATE INDEX IF NOT EXISTS idx_activities_timestamp ON activities(timestamp)")
    
    return db
```

**2. SQL Queries for Analysis (Week 7 concepts)**
```python
# Add to extractors/tribe_graph.py
def build_tribe_graph_from_db(db: SQL) -> Dict:
    """
    Week 7: Use SQL JOINs to build graph efficiently.
    """
    # Week 7: JOIN to get user interactions
    edges = db.execute("""
        SELECT 
            a1.user_id AS user1,
            a2.user_id AS user2,
            COUNT(*) AS interaction_count
        FROM activities a1
        JOIN activities a2 ON a1.provider_id = a2.provider_id
        WHERE a1.user_id < a2.user_id  -- Avoid duplicates
          AND a1.timestamp = a2.timestamp  -- Same time = interaction
        GROUP BY a1.user_id, a2.user_id
        HAVING interaction_count > 0
    """)
    
    return {
        "nodes": db.execute("SELECT DISTINCT id FROM users"),
        "edges": edges
    }
```

**3. Parameterized Queries (Week 7 security)**
```python
# Add to database.py - prevent SQL injection
def get_user_activities(db: SQL, user_id: str) -> List[Dict]:
    """
    Week 7: Always use parameterized queries (placeholders).
    Prevents SQL injection attacks.
    """
    # CORRECT: Use ? placeholder
    return db.execute(
        "SELECT * FROM activities WHERE user_id = ?",
        user_id
    )
    
    # WRONG: String concatenation (vulnerable to SQL injection)
    # return db.execute(f"SELECT * FROM activities WHERE user_id = '{user_id}'")
```

**4. Aggregation Queries (Week 7 concepts)**
```python
# Add to extractors/recon_scores.py
def score_providers_from_db(db: SQL) -> List[Dict]:
    """
    Week 7: Use SQL aggregation functions (COUNT, AVG, SUM).
    """
    scores = db.execute("""
        SELECT 
            p.id,
            p.name,
            COUNT(a.id) AS activity_count,
            SUM(CASE WHEN a.error_code != '' THEN 1 ELSE 0 END) AS error_count,
            CAST(SUM(CASE WHEN a.error_code != '' THEN 1 ELSE 0 END) AS FLOAT) / COUNT(a.id) AS error_rate
        FROM providers p
        LEFT JOIN activities a ON p.id = a.provider_id
        GROUP BY p.id, p.name
        HAVING activity_count > 0
        ORDER BY error_rate ASC, activity_count DESC
    """)
    
    return scores
```

---

## Week 8: HTML, CSS, JavaScript - Web Development

### Current State
- Has dashboard.html with D3.js
- Good use of modern web technologies

### Improvements to Apply

**1. Semantic HTML (Week 8 concepts)**
```html
<!-- Improve dashboard.html -->
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>COSURVIVAL Dashboard</title>
</head>
<body>
    <!-- Week 8: Semantic HTML tags -->
    <header>
        <h1>COSURVIVAL Intelligence Network</h1>
        <nav>
            <a href="#tribe">TRIBE</a>
            <a href="#teacher">TEACHER</a>
            <a href="#recon">RECON</a>
        </nav>
    </header>
    
    <main>
        <section id="tribe">
            <h2>TRIBE Network</h2>
            <!-- Network visualization -->
        </section>
        
        <section id="teacher">
            <h2>TEACHER Pathways</h2>
            <!-- Learning pathways -->
        </section>
        
        <section id="recon">
            <h2>RECON Scores</h2>
            <!-- Provider scores -->
        </section>
    </main>
    
    <footer>
        <p>&copy; 2024 COSURVIVAL. Built with intention.</p>
    </footer>
</body>
</html>
```

**2. CSS Best Practices (Week 8 concepts)**
```css
/* Add to dashboard.html <style> section */
/* Week 8: Use CSS classes, avoid inline styles */

.lens-card {
    background: var(--bg-card);
    border: 1px solid var(--border);
    border-radius: 8px;
    padding: 1.5rem;
    margin: 1rem 0;
}

.lens-card.tribe {
    border-left: 4px solid var(--tribe-primary);
}

.lens-card.teacher {
    border-left: 4px solid var(--teacher-primary);
}

.lens-card.recon {
    border-left: 4px solid var(--recon-primary);
}

/* Week 8: Responsive design with media queries */
@media (max-width: 768px) {
    .lens-card {
        padding: 1rem;
        margin: 0.5rem 0;
    }
}
```

**3. JavaScript Event Handling (Week 8 concepts)**
```javascript
// Add to dashboard.html <script> section
// Week 8: Proper event handling with addEventListener

document.addEventListener('DOMContentLoaded', function() {
    // Week 8: Query selectors
    const tribeSection = document.querySelector('#tribe');
    const teacherSection = document.querySelector('#teacher');
    const reconSection = document.querySelector('#recon');
    
    // Week 8: Event listeners
    document.querySelectorAll('nav a').forEach(link => {
        link.addEventListener('click', function(event) {
            event.preventDefault(); // Week 8: Prevent default behavior
            
            const targetId = this.getAttribute('href').substring(1);
            const targetSection = document.querySelector(`#${targetId}`);
            
            // Smooth scroll
            targetSection.scrollIntoView({ behavior: 'smooth' });
        });
    });
    
    // Week 8: Fetch API for loading data
    fetch('cosurvival_mvp.json')
        .then(response => response.json())
        .then(data => {
            renderTribe(data.tribe);
            renderTeacher(data.teacher);
            renderRecon(data.recon);
        })
        .catch(error => {
            console.error('Error loading data:', error);
        });
});
```

**4. Form Handling (Week 8 concepts)**
```html
<!-- Add to dashboard.html - filter/search form -->
<form id="filter-form">
    <label for="company-filter">Filter by Company:</label>
    <select id="company-filter" name="company">
        <option value="">All Companies</option>
        <!-- Options populated by JavaScript -->
    </select>
    
    <label for="date-range">Date Range:</label>
    <input type="date" id="date-start" name="date_start">
    <input type="date" id="date-end" name="date_end">
    
    <button type="submit">Apply Filters</button>
</form>

<script>
// Week 8: Form submission handling
document.querySelector('#filter-form').addEventListener('submit', function(event) {
    event.preventDefault();
    
    const formData = new FormData(this);
    const filters = {
        company: formData.get('company'),
        date_start: formData.get('date_start'),
        date_end: formData.get('date_end')
    };
    
    // Apply filters to visualization
    applyFilters(filters);
});
</script>
```

---

## Week 9: Flask - Web Applications

### Current State
- Static HTML dashboard
- No web server/API

### Improvements to Apply

**1. Flask Web Application (Week 9 concepts)**
```python
# Add app.py - Flask web application
from flask import Flask, render_template, request, jsonify, redirect, url_for
from flask_session import Session
from cs50 import SQL

app = Flask(__name__)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Week 9: Database connection
db = SQL("sqlite:///cosurvival.db")

@app.route("/")
def index():
    """Week 9: Home page route"""
    return render_template("dashboard.html")

@app.route("/api/tribe")
def api_tribe():
    """Week 9: API endpoint for TRIBE data"""
    # Week 9: Query database
    communities = db.execute("""
        SELECT community_id, COUNT(*) as size
        FROM user_communities
        GROUP BY community_id
        ORDER BY size DESC
        LIMIT 10
    """)
    
    return jsonify({
        "communities": communities,
        "status": "success"
    })

@app.route("/api/teacher")
def api_teacher():
    """Week 9: API endpoint for TEACHER data"""
    role = request.args.get("role", "")  # Week 9: GET parameters
    
    if role:
        skills = db.execute("""
            SELECT skill, proficiency_level
            FROM role_skills
            WHERE role = ?
        """, role)
    else:
        skills = db.execute("SELECT * FROM role_skills")
    
    return jsonify({
        "skills": skills,
        "status": "success"
    })

@app.route("/api/recon", methods=["GET", "POST"])
def api_recon():
    """Week 9: Support both GET and POST"""
    if request.method == "POST":
        # Week 9: POST data from form
        provider_id = request.form.get("provider_id")
        score = request.form.get("score")
        
        # Update database
        db.execute("""
            UPDATE providers
            SET user_score = ?
            WHERE id = ?
        """, score, provider_id)
        
        return redirect(url_for("index"))
    else:
        # Week 9: GET request
        providers = db.execute("""
            SELECT * FROM providers
            ORDER BY overall_score DESC
        """)
        return jsonify({"providers": providers})
```

**2. Template Inheritance (Week 9 concepts)**
```html
<!-- templates/layout.html -->
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>{% block title %}COSURVIVAL{% endblock %}</title>
    <link rel="stylesheet" href="{{ url_for('static', filename='style.css') }}">
</head>
<body>
    <header>
        <h1>COSURVIVAL</h1>
        <nav>
            <a href="{{ url_for('index') }}">Home</a>
            <a href="{{ url_for('tribe') }}">TRIBE</a>
            <a href="{{ url_for('teacher') }}">TEACHER</a>
            <a href="{{ url_for('recon') }}">RECON</a>
        </nav>
    </header>
    
    <main>
        {% block body %}{% endblock %}
    </main>
    
    <footer>
        <p>&copy; 2024 COSURVIVAL</p>
    </footer>
</body>
</html>

<!-- templates/dashboard.html -->
{% extends "layout.html" %}

{% block title %}Dashboard - COSURVIVAL{% endblock %}

{% block body %}
    <section id="tribe">
        <h2>TRIBE Network</h2>
        <div id="tribe-viz"></div>
    </section>
    
    <section id="teacher">
        <h2>TEACHER Pathways</h2>
        <div id="teacher-viz"></div>
    </section>
    
    <section id="recon">
        <h2>RECON Scores</h2>
        <div id="recon-viz"></div>
    </section>
{% endblock %}
```

**3. Session Management (Week 9 concepts)**
```python
# Add to app.py - user sessions
@app.route("/login", methods=["GET", "POST"])
def login():
    """Week 9: Login with session management"""
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")
        
        # Week 9: Check credentials (with hashing!)
        user = db.execute("""
            SELECT id, username, password_hash
            FROM users
            WHERE username = ?
        """, username)
        
        if user and verify_password(password, user[0]["password_hash"]):
            # Week 9: Store in session
            session["user_id"] = user[0]["id"]
            session["username"] = username
            return redirect(url_for("index"))
        else:
            return render_template("login.html", error="Invalid credentials")
    
    return render_template("login.html")

@app.route("/logout")
def logout():
    """Week 9: Logout and clear session"""
    session.clear()
    return redirect(url_for("index"))

@app.route("/dashboard")
def dashboard():
    """Week 9: Protected route - requires login"""
    if "user_id" not in session:
        return redirect(url_for("login"))
    
    user_id = session["user_id"]
    # Load user-specific data
    return render_template("dashboard.html", user_id=user_id)
```

**4. AJAX with Flask (Week 9 concepts)**
```javascript
// Add to dashboard.html - AJAX requests
// Week 9: Fetch data without page reload

async function loadTribeData() {
    try {
        const response = await fetch('/api/tribe');
        const data = await response.json();
        renderTribeVisualization(data.communities);
    } catch (error) {
        console.error('Error loading TRIBE data:', error);
    }
}

async function loadTeacherData(role = '') {
    const url = role ? `/api/teacher?role=${role}` : '/api/teacher';
    const response = await fetch(url);
    const data = await response.json();
    renderTeacherVisualization(data.skills);
}

// Week 9: Real-time updates
setInterval(loadTribeData, 30000); // Update every 30 seconds
```

---

## Week 10: Cybersecurity - Security Best Practices

### Current State
- Has governance.py with PII handling
- Uses hashing for PII

### Improvements to Apply

**1. Password Hashing (Week 10 concepts)**
```python
# Improve governance.py - proper password hashing
import hashlib
import secrets

def hash_password(password: str) -> Tuple[str, str]:
    """
    Week 10: Hash passwords with salt.
    Never store plaintext passwords!
    """
    # Generate random salt
    salt = secrets.token_hex(32)
    
    # Hash password + salt
    password_hash = hashlib.pbkdf2_hmac(
        'sha256',
        password.encode('utf-8'),
        salt.encode('utf-8'),
        100000  # 100k iterations
    )
    
    return password_hash.hex(), salt

def verify_password(password: str, stored_hash: str, salt: str) -> bool:
    """Week 10: Verify password against stored hash"""
    password_hash = hashlib.pbkdf2_hmac(
        'sha256',
        password.encode('utf-8'),
        salt.encode('utf-8'),
        100000
    )
    return password_hash.hex() == stored_hash
```

**2. SQL Injection Prevention (Week 10 concepts)**
```python
# Already using parameterized queries, but add validation
def safe_query(db: SQL, query: str, *params):
    """
    Week 10: Always use parameterized queries.
    Validate inputs before querying.
    """
    # Validate inputs
    for param in params:
        if isinstance(param, str) and (';' in param or '--' in param or 'DROP' in param.upper()):
            raise ValueError("Potentially malicious input detected")
    
    # Week 10: Use parameterized query (already doing this)
    return db.execute(query, *params)
```

**3. Rate Limiting (Week 10 concepts)**
```python
# Add to app.py - rate limiting
from functools import wraps
from time import time
from collections import defaultdict

# Week 10: Rate limiting to prevent brute force
request_times = defaultdict(list)
MAX_REQUESTS = 100
TIME_WINDOW = 60  # 1 minute

def rate_limit(f):
    """Week 10: Decorator for rate limiting"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        client_ip = request.remote_addr
        now = time()
        
        # Remove old requests
        request_times[client_ip] = [
            t for t in request_times[client_ip]
            if now - t < TIME_WINDOW
        ]
        
        # Check limit
        if len(request_times[client_ip]) >= MAX_REQUESTS:
            return jsonify({"error": "Rate limit exceeded"}), 429
        
        # Record request
        request_times[client_ip].append(now)
        
        return f(*args, **kwargs)
    return decorated_function

@app.route("/api/tribe")
@rate_limit
def api_tribe():
    # ... existing code ...
```

**4. Input Validation (Week 10 concepts)**
```python
# Add to governance.py - input validation
import re

def validate_user_input(input_str: str, input_type: str) -> bool:
    """
    Week 10: Validate all user inputs.
    Never trust user input!
    """
    if input_type == "email":
        pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        return bool(re.match(pattern, input_str))
    
    elif input_type == "uid":
        # UID should be alphanumeric, no special chars
        pattern = r'^[a-zA-Z0-9_-]+$'
        return bool(re.match(pattern, input_str)) and len(input_str) <= 256
    
    elif input_type == "filename":
        # Prevent path traversal
        if '..' in input_str or '/' in input_str or '\\' in input_str:
            return False
        return len(input_str) <= 255
    
    return False
```

**5. HTTPS/Encryption (Week 10 concepts)**
```python
# Add to app.py - enforce HTTPS in production
@app.before_request
def force_https():
    """Week 10: Force HTTPS in production"""
    if not request.is_secure and not app.debug:
        if request.headers.get('X-Forwarded-Proto') != 'https':
            return redirect(request.url.replace('http://', 'https://'), code=301)
```

---

## Summary: CS50 Concepts Applied

### Week 0: Problem Decomposition
- ✅ Clear pipeline structure
- ✅ Modular design
- ➕ Add visual flow diagrams

### Week 1: C Fundamentals
- ➕ Add explicit type hints
- ➕ Add constants file
- ➕ Add error codes
- ➕ Add memory-efficient streaming

### Week 2: Arrays & Strings
- ✅ Uses DataFrames (2D arrays)
- ➕ Add array-like operations
- ➕ Improve string normalization
- ➕ Use argparse for CLI

### Week 3: Algorithms
- ✅ Uses NetworkX algorithms
- ➕ Add complexity analysis comments
- ➕ Add binary search
- ➕ Add merge/selection sort patterns

### Week 4: Memory & File I/O
- ➕ Add explicit file handling
- ➕ Add resource management
- ➕ Add buffer management
- ➕ Add pointer-like references

### Week 5: Data Structures
- ✅ Uses dicts (hash tables)
- ➕ Add linked list implementation
- ➕ Add BST for skills
- ➕ Add Trie for autocomplete

### Week 6: Python
- ✅ Good Python usage
- ➕ More Pythonic patterns
- ➕ Better exception handling
- ➕ Use more standard library

### Week 7: SQL
- ➕ Add SQLite database
- ➕ Add SQL queries
- ➕ Add indexes for performance
- ➕ Use parameterized queries

### Week 8: Web Development
- ✅ Has HTML/CSS/JS
- ➕ Improve semantic HTML
- ➕ Better CSS organization
- ➕ Add form handling

### Week 9: Flask
- ➕ Add Flask web application
- ➕ Add API endpoints
- ➕ Add session management
- ➕ Add template inheritance

### Week 10: Cybersecurity
- ✅ Has PII handling
- ➕ Improve password hashing
- ➕ Add rate limiting
- ➕ Add input validation
- ➕ Add HTTPS enforcement

---

## Implementation Priority

1. **High Priority** (Security & Functionality):
   - Week 10: Password hashing, input validation
   - Week 7: SQLite database integration
   - Week 9: Flask web application

2. **Medium Priority** (Performance & Maintainability):
   - Week 3: Algorithm optimization
   - Week 5: Custom data structures
   - Week 1: Type hints and constants

3. **Low Priority** (Nice to Have):
   - Week 0: Visual diagrams
   - Week 4: Explicit memory management
   - Week 8: Enhanced web UI

---

*This document provides a roadmap for applying CS50 concepts to enhance the COSURVIVAL codebase. Each improvement maintains the existing architecture while adding educational value and real-world best practices.*
