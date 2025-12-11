# TEACHER Week 7: Problem Sets

> *"SQL for COSURVIVAL - Different tools for different jobs."*

---

## Problem Set 1: CSV to SQL

### Problem 1.1: Design COSURVIVAL Schema

**Task:** Design relational schema for TRIBE/TEACHER/RECON

**Requirements:**
1. Tables: users, companies, groups, activities, providers, permission_changes
2. Define primary keys
3. Define foreign keys
4. Add constraints (NOT NULL, UNIQUE where appropriate)

**Starter:**
```sql
CREATE TABLE users (
    id TEXT PRIMARY KEY,
    company_id TEXT,
    -- TODO: Add more columns
    FOREIGN KEY (company_id) REFERENCES companies(id)
);
```

---

### Problem 1.2: Import CSV to SQLite

**Task:** Import activity CSV into SQLite

**Requirements:**
1. Create schema
2. Import CSV data
3. Verify import (count rows, check relationships)
4. Handle errors gracefully

---

## Problem Set 2: Basic SQL Queries

### Problem 2.1: Count Activities

**Task:** Write queries to count activities

**Questions:**
1. Total activities
2. Activities by type
3. Activities per user
4. Activities per company

---

### Problem 2.2: Find Top Users

**Task:** Write queries to find most active users

**Requirements:**
1. Top 10 users by activity count
2. Users with most collaborations
3. Users with most skill progressions
4. Combine metrics (activity + progressions)

---

## Problem Set 3: Joins

### Problem 3.1: User → Company → Activities

**Task:** Write joins to connect users, companies, and activities

**Requirements:**
1. List users with their company names
2. Count activities per company
3. Find companies with most active users
4. List users who collaborate across companies

---

### Problem 3.2: Cross-Lens Joins

**Task:** Join TRIBE/TEACHER/RECON data

**Requirements:**
1. Users with both high collaboration (TRIBE) and fast learning (TEACHER)
2. Providers used by companies with high activity (RECON + TRIBE)
3. Users missing skills for their role (TEACHER)
4. Companies with best provider quality scores (RECON)

---

## Problem Set 4: Aggregations

### Problem 4.1: Group and Aggregate

**Task:** Write GROUP BY queries

**Requirements:**
1. Activities by type and company
2. Average activity count per user by company
3. Provider reliability scores by company
4. Skill progression rates by role

---

### Problem 4.2: Complex Aggregations

**Task:** Write multi-level aggregations

**Requirements:**
1. Companies ranked by total user activity
2. Providers ranked by quality across all companies
3. Users ranked by combined TRIBE/TEACHER metrics
4. Time-based trends (activities per month)

---

## Problem Set 5: Indexes

### Problem 5.1: Identify Slow Queries

**Task:** Find queries that need indexes

**Requirements:**
1. Run queries without indexes (time them)
2. Identify columns used in WHERE/JOIN/ORDER BY
3. Create appropriate indexes
4. Re-run queries and measure improvement

---

### Problem 5.2: Index Tradeoffs

**Task:** Analyze index costs and benefits

**Requirements:**
1. Create indexes on frequently queried columns
2. Measure query speed improvement
3. Measure insert/update slowdown
4. Explain when to use indexes

---

## Problem Set 6: Security

### Problem 6.1: Prevent SQL Injection

**Task:** Rewrite unsafe queries

**Requirements:**
1. Identify unsafe string formatting
2. Rewrite with placeholders
3. Test with malicious input (e.g., `'; DROP TABLE users; --`)
4. Verify queries are safe

**Unsafe example:**
```python
query = f"SELECT * FROM users WHERE id = '{user_id}'"
```

**Safe example:**
```python
query = "SELECT * FROM users WHERE id = ?"
db.execute(query, (user_id,))
```

---

### Problem 6.2: Validate Input

**Task:** Add input validation

**Requirements:**
1. Validate user IDs (format, length)
2. Validate timestamps (format, range)
3. Sanitize text inputs
4. Return errors for invalid input

---

## Problem Set 7: Race Conditions

### Problem 7.1: Identify Race Conditions

**Task:** Find code with race condition risks

**Requirements:**
1. Find read-then-write patterns
2. Identify concurrent update risks
3. Explain what could go wrong
4. Propose solutions

---

### Problem 7.2: Implement Atomic Updates

**Task:** Use transactions for atomicity

**Requirements:**
1. Rewrite counter updates atomically
2. Use transactions for multi-step operations
3. Test concurrent access
4. Verify correctness

---

## Problem Set 8: COSURVIVAL Queries

### Problem 8.1: TRIBE Queries

**Task:** Write TRIBE-specific queries

**Questions:**
1. Find strongest collaboration pairs
2. Identify bridge connectors (users in multiple communities)
3. Find mentor candidates (high centrality, high activity)
4. Detect silos (groups with no cross-group collaboration)

---

### Problem 8.2: TEACHER Queries

**Task:** Write TEACHER-specific queries

**Questions:**
1. Find users with fastest skill progression
2. Identify most common skill pathways
3. Find users missing critical skills for their role
4. Calculate learning velocity (skills per month)

---

### Problem 8.3: RECON Queries

**Task:** Write RECON-specific queries

**Questions:**
1. Calculate provider reliability scores
2. Identify friction points (high error rates)
3. Find value flows (provider → company relationships)
4. Rank providers by adoption and quality

---

### Problem 8.4: Cross-Lens Queries

**Task:** Write queries combining all three lenses

**Questions:**
1. Users who are both active collaborators and fast learners
2. Companies with best provider quality and high collaboration
3. Providers used by companies with high learning velocity
4. Complete COSURVIVAL dashboard query (all metrics)

---

## Submission Guidelines

### For Each Problem Set

1. **SQL:** Working queries
2. **Tests:** Test with sample data
3. **Performance:** Measure query time (with/without indexes)
4. **Security:** Verify SQL injection prevention

### Self-Assessment

After completing all problem sets, answer:

1. Can you design relational schemas?
2. Can you write complex joins?
3. Can you optimize queries with indexes?
4. Can you prevent SQL injection and race conditions?

**Remember:** Growth over position. Compare to your Week 6 baseline.

---

## Solutions (For Instructors)

Solutions are available in `week7_solutions.sql` for instructors.

**Key Learning Points:**
- SQL is better for complex queries
- Normalize data across tables
- Use joins to reassemble meaning
- Add indexes for performance
- Use placeholders to prevent injection
- Use transactions for atomicity

---

*"Different tools for different jobs: CSV for portability, Python for glue, SQL for powerful queries."*

