# TEACHER Week 7: SQL for COSURVIVAL

> *"SQL is better for asking questions of data at scale. Different tools for different jobs: CSV for portability, Python for glue, SQL for powerful queries."*

---

## Module Overview

**Duration:** 8-10 hours  
**Prerequisites:** Week 6 (Python Productivity Layer)  
**Next:** Capstone (Real-World Deployment)

This week, learners discover how **SQL enables powerful queries** across TRIBE, TEACHER, and RECON. Just as CS50 Week 7 shows SQL is better for asking questions at scale, TEACHER Week 7 shows SQL enables cross-lens queries, relationship analysis, and scalable insights.

---

## Learning Outcomes

By the end of this week, learners will be able to:

1. **Explain** why SQL is better than CSV for complex queries
2. **Design** relational schemas for TRIBE/TEACHER/RECON
3. **Write** SQL queries for cross-lens analysis
4. **Use** joins to connect relationships
5. **Create** indexes for performance
6. **Prevent** SQL injection and race conditions
7. **Query** COSURVIVAL data at scale

---

## Core Concept: Different Tools for Different Jobs

### CS50's Insight

> "CSV/flat files are simple and portable. Python is great for glue + quick analysis. **SQL is better for asking questions of data at scale** with fewer lines and often better performance."

### TEACHER's Insight

> "CSV is great for initial ingestion. Python is great for extractors and transformations. **SQL is better for asking complex questions across TRIBE/TEACHER/RECON** with relationships, joins, and scale."

---

## From CSV to SQL: The COSURVIVAL Schema

### CSV: Simple but Limited

**What we've been using:**
```python
# CSV structure (flat)
Uid, UidOpp, Type, Date, CompanyId, GroupId, StateOld, StateNew, ...
user_1, user_2, document_share, 2024-01-15, org_1, team_alpha, viewer, editor, ...
```

**Limitations:**
- Hard to query relationships
- Redundant data (company names repeated)
- No enforced structure
- Slow for complex questions

### SQL: Structured and Powerful

**COSURVIVAL schema:**
```sql
-- Core entities
CREATE TABLE users (
    id TEXT PRIMARY KEY,
    company_id TEXT,
    hashed_email TEXT,
    activity_count INTEGER DEFAULT 0,
    FOREIGN KEY (company_id) REFERENCES companies(id)
);

CREATE TABLE companies (
    id TEXT PRIMARY KEY,
    name TEXT,
    activity_count INTEGER DEFAULT 0
);

CREATE TABLE groups (
    id TEXT PRIMARY KEY,
    company_id TEXT,
    name TEXT,
    FOREIGN KEY (company_id) REFERENCES companies(id)
);

-- Activities (bridge between users)
CREATE TABLE activities (
    id TEXT PRIMARY KEY,
    user_id TEXT,
    target_user_id TEXT,
    activity_type TEXT,
    timestamp TEXT,
    company_id TEXT,
    group_id TEXT,
    provider_id TEXT,
    state_before TEXT,
    state_after TEXT,
    error_code TEXT,
    FOREIGN KEY (user_id) REFERENCES users(id),
    FOREIGN KEY (target_user_id) REFERENCES users(id),
    FOREIGN KEY (company_id) REFERENCES companies(id),
    FOREIGN KEY (group_id) REFERENCES groups(id),
    FOREIGN KEY (provider_id) REFERENCES providers(id)
);

-- Providers (RECON)
CREATE TABLE providers (
    id TEXT PRIMARY KEY,
    name TEXT,
    activity_count INTEGER DEFAULT 0,
    error_count INTEGER DEFAULT 0
);

-- Permission changes (TEACHER)
CREATE TABLE permission_changes (
    id TEXT PRIMARY KEY,
    user_id TEXT,
    timestamp TEXT,
    state_before TEXT,
    state_after TEXT,
    permission_type TEXT,
    FOREIGN KEY (user_id) REFERENCES users(id)
);
```

**Benefits:**
- Enforced relationships
- No redundancy
- Fast queries
- Complex questions in one query

---

## SQL Essentials for COSURVIVAL

### 1. Count Activities

**Question:** How many activities in total?

```sql
SELECT COUNT(*) AS total_activities
FROM activities;
```

**COSURVIVAL query:**
```sql
-- Count activities by type
SELECT activity_type, COUNT(*) AS n
FROM activities
GROUP BY activity_type
ORDER BY n DESC;
```

---

### 2. Find Active Users

**Question:** Which users have the most collaborations?

```sql
SELECT 
    u.id AS user_id,
    COUNT(DISTINCT a.target_user_id) AS collaboration_count
FROM users u
JOIN activities a ON u.id = a.user_id
WHERE a.target_user_id IS NOT NULL
GROUP BY u.id
ORDER BY collaboration_count DESC
LIMIT 10;
```

---

### 3. Find Communities (TRIBE)

**Question:** Which users collaborate most with each other?

```sql
-- Find strong collaboration pairs
SELECT 
    a1.user_id AS user_a,
    a1.target_user_id AS user_b,
    COUNT(*) AS collaboration_count
FROM activities a1
JOIN activities a2 
    ON a1.user_id = a2.target_user_id 
    AND a1.target_user_id = a2.user_id
WHERE a1.user_id < a1.target_user_id  -- Avoid duplicates
GROUP BY a1.user_id, a1.target_user_id
HAVING collaboration_count >= 5
ORDER BY collaboration_count DESC;
```

---

### 4. Track Skill Progressions (TEACHER)

**Question:** Which users are progressing fastest?

```sql
-- Count permission upgrades per user
SELECT 
    u.id AS user_id,
    COUNT(*) AS progression_count,
    MAX(pc.timestamp) AS latest_progression
FROM users u
JOIN permission_changes pc ON u.id = pc.user_id
WHERE pc.state_after > pc.state_before  -- Upgrade only
GROUP BY u.id
ORDER BY progression_count DESC
LIMIT 10;
```

---

### 5. Score Providers (RECON)

**Question:** Which providers are most reliable?

```sql
-- Calculate provider reliability
SELECT 
    p.id AS provider_id,
    p.name,
    COUNT(a.id) AS total_activities,
    SUM(CASE WHEN a.error_code IS NOT NULL THEN 1 ELSE 0 END) AS error_count,
    ROUND(
        1.0 - (SUM(CASE WHEN a.error_code IS NOT NULL THEN 1 ELSE 0 END) * 1.0 / COUNT(a.id)),
        3
    ) AS reliability_score
FROM providers p
JOIN activities a ON p.id = a.provider_id
GROUP BY p.id, p.name
HAVING total_activities >= 10  -- Minimum sample size
ORDER BY reliability_score DESC;
```

---

## Relational Design: TRIBE/TEACHER/RECON Relationships

### The Problem: Flat CSV

**CSV has redundancy:**
```
user_1, org_techcorp, team_alpha, provider_aws, ...
user_2, org_techcorp, team_alpha, provider_aws, ...
user_3, org_techcorp, team_beta, provider_google, ...
```

**Issues:**
- Company name repeated
- Group name repeated
- Provider name repeated
- Hard to update (change company name = update all rows)

### The Solution: Normalized Tables

**Separate entities:**
```sql
-- Companies (one row per company)
CREATE TABLE companies (
    id TEXT PRIMARY KEY,
    name TEXT NOT NULL
);

-- Groups (one row per group)
CREATE TABLE groups (
    id TEXT PRIMARY KEY,
    company_id TEXT,
    name TEXT,
    FOREIGN KEY (company_id) REFERENCES companies(id)
);

-- Users (one row per user)
CREATE TABLE users (
    id TEXT PRIMARY KEY,
    company_id TEXT,
    FOREIGN KEY (company_id) REFERENCES companies(id)
);

-- Activities (references other tables)
CREATE TABLE activities (
    id TEXT PRIMARY KEY,
    user_id TEXT,
    company_id TEXT,
    group_id TEXT,
    provider_id TEXT,
    FOREIGN KEY (user_id) REFERENCES users(id),
    FOREIGN KEY (company_id) REFERENCES companies(id),
    FOREIGN KEY (group_id) REFERENCES groups(id),
    FOREIGN KEY (provider_id) REFERENCES providers(id)
);
```

**Benefits:**
- Update company name once
- Enforce relationships
- Query efficiently
- No redundancy

---

## Joins: Connecting TRIBE/TEACHER/RECON

### 1. User → Company → Activities

**Question:** Which companies have the most active users?

```sql
SELECT 
    c.name AS company_name,
    COUNT(DISTINCT u.id) AS user_count,
    COUNT(a.id) AS activity_count
FROM companies c
JOIN users u ON c.id = u.company_id
JOIN activities a ON u.id = a.user_id
GROUP BY c.id, c.name
ORDER BY activity_count DESC;
```

---

### 2. User → Skills → Role Requirements

**Question:** Which users are missing skills for their role?

```sql
-- This would require a skills table
SELECT 
    u.id AS user_id,
    r.name AS role_name,
    rs.skill_name AS required_skill,
    CASE 
        WHEN us.skill_name IS NULL THEN 'Missing'
        ELSE 'Has'
    END AS status
FROM users u
JOIN roles r ON u.role_id = r.id
JOIN role_skills rs ON r.id = rs.role_id
LEFT JOIN user_skills us ON u.id = us.user_id AND rs.skill_name = us.skill_name
WHERE us.skill_name IS NULL  -- Missing skills only
ORDER BY u.id, rs.skill_name;
```

---

### 3. Provider → Activities → Companies

**Question:** Which providers serve which companies?

```sql
SELECT 
    p.name AS provider_name,
    c.name AS company_name,
    COUNT(a.id) AS activity_count,
    ROUND(
        1.0 - (SUM(CASE WHEN a.error_code IS NOT NULL THEN 1 ELSE 0 END) * 1.0 / COUNT(a.id)),
        3
    ) AS quality_score
FROM providers p
JOIN activities a ON p.id = a.provider_id
JOIN companies c ON a.company_id = c.id
GROUP BY p.id, p.name, c.id, c.name
ORDER BY activity_count DESC;
```

---

## Indexes: Performance at Scale

### Why Indexes Matter

**Without index:**
- Query scans entire table
- Slow for large datasets
- O(n) complexity

**With index:**
- Query uses index structure (B-tree)
- Fast lookups
- O(log n) complexity

### COSURVIVAL Indexes

```sql
-- User lookups (most common)
CREATE INDEX idx_activities_user_id ON activities(user_id);
CREATE INDEX idx_activities_target_user_id ON activities(target_user_id);

-- Company/group queries
CREATE INDEX idx_activities_company_id ON activities(company_id);
CREATE INDEX idx_activities_group_id ON activities(group_id);

-- Provider queries (RECON)
CREATE INDEX idx_activities_provider_id ON activities(provider_id);

-- Time-based queries
CREATE INDEX idx_activities_timestamp ON activities(timestamp);

-- Permission changes (TEACHER)
CREATE INDEX idx_permission_changes_user_id ON permission_changes(user_id);
CREATE INDEX idx_permission_changes_timestamp ON permission_changes(timestamp);
```

**Tradeoff:**
- Faster queries
- More storage
- Slower inserts/updates/deletes

**Rule of thumb:** Index columns you query frequently.

---

## Python + SQL Together

### Instead of CSV Scanning

**Old way (CSV):**
```python
import csv
from collections import Counter

counts = Counter()
with open("activities.csv", "r") as file:
    reader = csv.DictReader(file)
    for row in reader:
        counts[row["activity_type"]] += 1

for activity_type, count in counts.most_common():
    print(activity_type, count)
```

**New way (SQL):**
```python
import sqlite3

db = sqlite3.connect("cosurvival.db")
db.row_factory = sqlite3.Row  # Access by column name

rows = db.execute("""
    SELECT activity_type, COUNT(*) AS n
    FROM activities
    GROUP BY activity_type
    ORDER BY n DESC
""").fetchall()

for row in rows:
    print(row["activity_type"], row["n"])
```

**Benefits:**
- Faster (indexed)
- Less code
- More powerful queries

---

## Security: SQL Injection Prevention

### The Danger

**Unsafe (SQL injection risk):**
```python
user_input = "'; DROP TABLE activities; --"
query = f"SELECT * FROM users WHERE id = '{user_input}'"
# This would execute: SELECT * FROM users WHERE id = ''; DROP TABLE activities; --'
```

**Safe (placeholders):**
```python
user_input = "'; DROP TABLE activities; --"
query = "SELECT * FROM users WHERE id = ?"
rows = db.execute(query, (user_input,)).fetchall()
# This safely treats user_input as a literal value
```

### COSURVIVAL Best Practice

**Always use placeholders:**
```python
def get_user_activities(user_id: str):
    """Get activities for user - safe from SQL injection."""
    query = """
        SELECT a.*, c.name AS company_name
        FROM activities a
        JOIN companies c ON a.company_id = c.id
        WHERE a.user_id = ?
        ORDER BY a.timestamp DESC
        LIMIT 100
    """
    return db.execute(query, (user_id,)).fetchall()
```

---

## Race Conditions: Concurrent Access

### The Problem

**Naive counter update:**
```python
# User 1 and User 2 both read count = 100
count = db.execute("SELECT activity_count FROM users WHERE id = ?", (user_id,)).fetchone()[0]
# User 1: count = 100, writes 101
# User 2: count = 100, writes 101 (should be 102!)
db.execute("UPDATE users SET activity_count = ? WHERE id = ?", (count + 1, user_id))
```

**Result:** Lost update (should be 102, got 101)

### The Solution: Transactions

**Atomic update:**
```python
def increment_activity_count(user_id: str):
    """Increment count atomically - safe from race conditions."""
    db.execute("""
        UPDATE users 
        SET activity_count = activity_count + 1
        WHERE id = ?
    """, (user_id,))
    db.commit()  # Atomic operation
```

**Or use transactions:**
```python
def update_with_transaction():
    """Use transaction for multiple operations."""
    db.execute("BEGIN TRANSACTION")
    try:
        db.execute("UPDATE users SET activity_count = activity_count + 1 WHERE id = ?", (user_id,))
        db.execute("INSERT INTO activities (...) VALUES (...)")
        db.commit()  # All or nothing
    except:
        db.rollback()  # Undo on error
        raise
```

---

## COSURVIVAL Query Patterns

### Pattern 1: Cross-Lens Analysis

**Question:** Which users are both active collaborators (TRIBE) and fast learners (TEACHER)?

```sql
SELECT 
    u.id AS user_id,
    -- TRIBE metric
    COUNT(DISTINCT a1.target_user_id) AS collaboration_count,
    -- TEACHER metric
    COUNT(DISTINCT pc.id) AS progression_count
FROM users u
LEFT JOIN activities a1 ON u.id = a1.user_id AND a1.target_user_id IS NOT NULL
LEFT JOIN permission_changes pc ON u.id = pc.user_id AND pc.state_after > pc.state_before
GROUP BY u.id
HAVING collaboration_count >= 5 AND progression_count >= 3
ORDER BY collaboration_count DESC, progression_count DESC;
```

---

### Pattern 2: Provider Quality by Company

**Question:** Which providers have the best quality scores per company?

```sql
SELECT 
    c.name AS company_name,
    p.name AS provider_name,
    COUNT(a.id) AS activity_count,
    ROUND(
        1.0 - (SUM(CASE WHEN a.error_code IS NOT NULL THEN 1 ELSE 0 END) * 1.0 / COUNT(a.id)),
        3
    ) AS quality_score
FROM companies c
JOIN activities a ON c.id = a.company_id
JOIN providers p ON a.provider_id = p.id
GROUP BY c.id, c.name, p.id, p.name
HAVING activity_count >= 10  -- Minimum sample
ORDER BY c.name, quality_score DESC;
```

---

### Pattern 3: Learning Pathway Analysis

**Question:** What's the most common skill progression path?

```sql
SELECT 
    pc1.state_after AS from_skill,
    pc2.state_after AS to_skill,
    COUNT(*) AS frequency
FROM permission_changes pc1
JOIN permission_changes pc2 
    ON pc1.user_id = pc2.user_id 
    AND pc2.timestamp > pc1.timestamp
    AND pc2.timestamp <= datetime(pc1.timestamp, '+30 days')  -- Within 30 days
WHERE pc1.state_after != pc2.state_after
GROUP BY pc1.state_after, pc2.state_after
ORDER BY frequency DESC
LIMIT 10;
```

---

## Micro-Labs (CS50-Style)

### Lab 1: Import CSV to SQLite

**Task:** Import activity CSV into SQLite database

**Requirements:**
1. Create schema (users, companies, activities, providers)
2. Import CSV data
3. Verify import (count rows)
4. Check relationships

---

### Lab 2: Write COSURVIVAL Queries

**Task:** Write SQL queries for common questions

**Questions:**
1. Top 10 most active users
2. Companies with most activities
3. Providers with best reliability scores
4. Users with most skill progressions

---

### Lab 3: Cross-Lens Joins

**Task:** Write queries that join TRIBE/TEACHER/RECON data

**Requirements:**
1. Join users → activities → companies
2. Join users → permission_changes → skills
3. Join providers → activities → companies
4. Combine all three lenses in one query

---

### Lab 4: Create Indexes

**Task:** Add indexes for performance

**Requirements:**
1. Identify slow queries
2. Create appropriate indexes
3. Measure performance improvement
4. Explain tradeoffs

---

### Lab 5: Prevent SQL Injection

**Task:** Rewrite unsafe queries with placeholders

**Requirements:**
1. Identify unsafe string formatting
2. Rewrite with placeholders
3. Test with malicious input
4. Verify safety

---

### Lab 6: Handle Race Conditions

**Task:** Implement atomic updates

**Requirements:**
1. Identify race condition risks
2. Use transactions for atomicity
3. Test concurrent access
4. Verify correctness

---

## Assessment: Self-Relative Growth

### Baseline (Before Week 7)

**Question:** "Can you query COSURVIVAL data efficiently?"

**Expected Response:**
- May use CSV scanning
- May not understand relationships
- May not optimize queries

### After Week 7

**Question:** "Can you write SQL queries for cross-lens analysis?"

**Expected Response:**
- Can design relational schemas
- Can write complex joins
- Can optimize with indexes
- Can prevent security issues

---

## Key Takeaways

1. **SQL is better for complex queries.** CSV is simple, SQL is powerful.

2. **Normalize data across tables.** Avoid redundancy, enforce relationships.

3. **Use joins to reassemble meaning.** Connect TRIBE/TEACHER/RECON data.

4. **Add indexes for performance.** Trade storage for speed.

5. **Use placeholders to prevent SQL injection.** Never format SQL with user input.

6. **Use transactions for atomicity.** Prevent race conditions.

7. **Different tools for different jobs.** CSV for portability, Python for glue, SQL for queries.

---

## Next Steps

**Capstone:** Real-World Deployment
- Design production schema
- Optimize queries with indexes
- Secure against injection
- Handle concurrent access

**For Now:** Practice SQL:
- Write COSURVIVAL queries
- Design schemas
- Optimize performance
- Secure queries

---

## Resources

- **extractors/:** See Python productivity layer
- **models.py:** See data models
- **pipeline.py:** See data flow

---

*"SQL is better for asking questions of data at scale. Different tools for different jobs: CSV for portability, Python for glue, SQL for powerful queries."*
