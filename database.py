#!/usr/bin/env python3
"""
COSURVIVAL DATABASE MODULE
==========================
SQL database setup and utilities with security best practices.

This implements Week 7 (SQL) + Week 10 (Security) best practices:
- Parameterized queries (SQL injection prevention)
- Indexes for performance
- Transactions for atomicity
- Input validation
"""

# Standard library imports
import os
import sqlite3
import sys
from typing import Dict, List, Optional, Any, Tuple

# Add current directory to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# Local imports
from security import (
    build_safe_query,
    validate_company_id,
    validate_user_id,
)


# =============================================================================
# DATABASE SCHEMA (Week 7: Relational design)
# =============================================================================

SCHEMA_SQL = """
-- Users table
CREATE TABLE IF NOT EXISTS users (
    id TEXT PRIMARY KEY,
    company_id TEXT,
    hashed_email TEXT,
    activity_count INTEGER DEFAULT 0,
    created_at TEXT DEFAULT (datetime('now')),
    FOREIGN KEY (company_id) REFERENCES companies(id)
);

-- Companies table
CREATE TABLE IF NOT EXISTS companies (
    id TEXT PRIMARY KEY,
    name TEXT,
    activity_count INTEGER DEFAULT 0,
    created_at TEXT DEFAULT (datetime('now'))
);

-- Groups table
CREATE TABLE IF NOT EXISTS groups (
    id TEXT PRIMARY KEY,
    name TEXT,
    company_id TEXT,
    member_count INTEGER DEFAULT 0,
    created_at TEXT DEFAULT (datetime('now')),
    FOREIGN KEY (company_id) REFERENCES companies(id)
);

-- Providers table (RECON)
CREATE TABLE IF NOT EXISTS providers (
    id TEXT PRIMARY KEY,
    name TEXT,
    activity_count INTEGER DEFAULT 0,
    error_count INTEGER DEFAULT 0,
    created_at TEXT DEFAULT (datetime('now'))
);

-- Activities table (bridge table)
CREATE TABLE IF NOT EXISTS activities (
    id TEXT PRIMARY KEY,
    user_id TEXT,
    target_user_id TEXT,
    activity_type TEXT,
    timestamp TEXT,
    timestamp_date TEXT,
    company_id TEXT,
    group_id TEXT,
    provider_id TEXT,
    state_before TEXT,
    state_after TEXT,
    error_code TEXT,
    created_at TEXT DEFAULT (datetime('now')),
    FOREIGN KEY (user_id) REFERENCES users(id),
    FOREIGN KEY (target_user_id) REFERENCES users(id),
    FOREIGN KEY (company_id) REFERENCES companies(id),
    FOREIGN KEY (group_id) REFERENCES groups(id),
    FOREIGN KEY (provider_id) REFERENCES providers(id)
);

-- Permission changes table (TEACHER)
CREATE TABLE IF NOT EXISTS permission_changes (
    id TEXT PRIMARY KEY,
    user_id TEXT,
    timestamp TEXT,
    state_before TEXT,
    state_after TEXT,
    permission_type TEXT,
    role_id TEXT,
    created_at TEXT DEFAULT (datetime('now')),
    FOREIGN KEY (user_id) REFERENCES users(id)
);

-- Queries table (for audit trail)
CREATE TABLE IF NOT EXISTS queries (
    id TEXT PRIMARY KEY,
    user_id TEXT,
    lens TEXT,
    timestamp TEXT DEFAULT (datetime('now')),
    FOREIGN KEY (user_id) REFERENCES users(id)
);
"""


# =============================================================================
# INDEXES (Week 7: Performance optimization)
# =============================================================================

INDEXES_SQL = """
-- User lookups (most common)
CREATE INDEX IF NOT EXISTS idx_activities_user_id ON activities(user_id);
CREATE INDEX IF NOT EXISTS idx_activities_target_user_id ON activities(target_user_id);

-- Company/group queries
CREATE INDEX IF NOT EXISTS idx_activities_company_id ON activities(company_id);
CREATE INDEX IF NOT EXISTS idx_activities_group_id ON activities(group_id);

-- Provider queries (RECON)
CREATE INDEX IF NOT EXISTS idx_activities_provider_id ON activities(provider_id);

-- Time-based queries
CREATE INDEX IF NOT EXISTS idx_activities_timestamp ON activities(timestamp);
CREATE INDEX IF NOT EXISTS idx_activities_timestamp_date ON activities(timestamp_date);

-- Permission changes (TEACHER)
CREATE INDEX IF NOT EXISTS idx_permission_changes_user_id ON permission_changes(user_id);
CREATE INDEX IF NOT EXISTS idx_permission_changes_timestamp ON permission_changes(timestamp);
CREATE INDEX IF NOT EXISTS idx_permission_changes_role_id ON permission_changes(role_id);

-- Companies
CREATE INDEX IF NOT EXISTS idx_users_company_id ON users(company_id);
"""


# =============================================================================
# DATABASE INITIALIZATION
# =============================================================================


def init_database(db_path: str = "cosurvival.db") -> sqlite3.Connection:
    """
    Initialize database with schema and indexes.

    Week 7: SQL schema creation
    Week 10: Safe database setup

    Returns:
        Database connection
    """
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row

    # Create schema
    conn.executescript(SCHEMA_SQL)

    # Create indexes
    conn.executescript(INDEXES_SQL)

    conn.commit()
    return conn


# =============================================================================
# SAFE QUERY HELPERS (Week 10: SQL injection prevention)
# =============================================================================


class SafeDatabase:
    """
    Database wrapper with security best practices.

    Week 7: SQL integration
    Week 10: Security (parameterized queries, input validation)
    """

    def __init__(self, db_path: str = "cosurvival.db"):
        """Initialize database connection."""
        self.conn = init_database(db_path)
        self.conn.row_factory = sqlite3.Row

    def execute_safe(self, query: str, params: Tuple = ()) -> List[sqlite3.Row]:
        """
        Execute parameterized query safely.

        Week 10: SQL injection prevention

        Args:
            query: SQL query with ? placeholders
            params: Parameters tuple

        Returns:
            List of rows
        """
        # Validate query (Week 10: security)
        query, params = build_safe_query(query, params)

        return self.conn.execute(query, params).fetchall()

    def execute_write_safe(self, query: str, params: Tuple = ()) -> None:
        """Execute a mutating query safely and commit the transaction."""

        query, params = build_safe_query(query, params)
        self.conn.execute(query, params)
        self.conn.commit()

    def execute_one_safe(self, query: str, params: Tuple = ()) -> Optional[sqlite3.Row]:
        """
        Execute parameterized query and return one row.

        Week 10: SQL injection prevention
        """
        rows = self.execute_safe(query, params)
        return rows[0] if rows else None

    def insert_user(self, user_id: str, company_id: str = "") -> bool:
        """
        Insert user safely.

        Week 10: Input validation + parameterized query
        """
        # Validate input
        is_valid, error = validate_user_id(user_id)
        if not is_valid:
            raise ValueError(f"Invalid user_id: {error}")

        if company_id:
            is_valid, error = validate_company_id(company_id)
            if not is_valid:
                raise ValueError(f"Invalid company_id: {error}")

        # Use parameterized query
        try:
            self.conn.execute(
                """
                INSERT INTO users (id, company_id)
                VALUES (?, ?)
            """,
                (user_id, company_id),
            )
            self.conn.commit()
            return True
        except sqlite3.IntegrityError:
            return False  # User already exists

    def get_user_activities(self, user_id: str, limit: int = 100) -> List[Dict[str, Any]]:
        """
        Get activities for user safely.

        Week 7: SQL query
        Week 10: Parameterized query, input validation
        """
        # Validate input
        is_valid, error = validate_user_id(user_id)
        if not is_valid:
            raise ValueError(f"Invalid user_id: {error}")

        # Parameterized query
        query = """
            SELECT a.*, c.name AS company_name
            FROM activities a
            LEFT JOIN companies c ON a.company_id = c.id
            WHERE a.user_id = ?
            ORDER BY a.timestamp DESC
            LIMIT ?
        """
        rows = self.execute_safe(query, (user_id, limit))

        return [dict(row) for row in rows]

    def get_tribe_graph(self, company_id: Optional[str] = None) -> Dict[str, Any]:
        """
        Get TRIBE graph data safely.

        Week 7: SQL query with joins
        Week 10: Parameterized query
        """
        if company_id:
            # Validate input
            is_valid, error = validate_company_id(company_id)
            if not is_valid:
                raise ValueError(f"Invalid company_id: {error}")

            # Parameterized query
            query = """
                SELECT 
                    a1.user_id AS user_a,
                    a1.target_user_id AS user_b,
                    COUNT(*) AS collaboration_count
                FROM activities a1
                JOIN activities a2 
                    ON a1.user_id = a2.target_user_id 
                    AND a1.target_user_id = a2.user_id
                WHERE a1.user_id < a1.target_user_id
                    AND a1.company_id = ?
                GROUP BY a1.user_id, a1.target_user_id
                HAVING collaboration_count >= 5
            """
            rows = self.execute_safe(query, (company_id,))
        else:
            query = """
                SELECT 
                    a1.user_id AS user_a,
                    a1.target_user_id AS user_b,
                    COUNT(*) AS collaboration_count
                FROM activities a1
                JOIN activities a2 
                    ON a1.user_id = a2.target_user_id 
                    AND a1.target_user_id = a2.user_id
                WHERE a1.user_id < a1.target_user_id
                GROUP BY a1.user_id, a1.target_user_id
                HAVING collaboration_count >= 5
            """
            rows = self.execute_safe(query)

        nodes = set()
        edges = []

        for row in rows:
            nodes.add(row["user_a"])
            nodes.add(row["user_b"])
            edges.append(
                {
                    "source": row["user_a"],
                    "target": row["user_b"],
                    "weight": row["collaboration_count"],
                }
            )

        return {"nodes": list(nodes), "edges": edges}

    def get_provider_scores(self, company_id: Optional[str] = None) -> List[Dict[str, Any]]:
        """
        Get provider reliability scores safely.

        Week 7: SQL aggregation
        Week 10: Parameterized query
        """
        if company_id:
            # Validate input
            is_valid, error = validate_company_id(company_id)
            if not is_valid:
                raise ValueError(f"Invalid company_id: {error}")

            # Parameterized query
            query = """
                SELECT 
                    p.id AS provider_id,
                    p.name AS provider_name,
                    COUNT(a.id) AS total_activities,
                    SUM(CASE WHEN a.error_code IS NOT NULL THEN 1 ELSE 0 END) AS error_count,
                    ROUND(
                        1.0 - (SUM(CASE WHEN a.error_code IS NOT NULL THEN 1 ELSE 0 END) * 1.0 / COUNT(a.id)),
                        3
                    ) AS reliability_score
                FROM providers p
                JOIN activities a ON p.id = a.provider_id
                WHERE a.company_id = ?
                GROUP BY p.id, p.name
                HAVING total_activities >= 10
                ORDER BY reliability_score DESC
            """
            rows = self.execute_safe(query, (company_id,))
        else:
            query = """
                SELECT 
                    p.id AS provider_id,
                    p.name AS provider_name,
                    COUNT(a.id) AS total_activities,
                    SUM(CASE WHEN a.error_code IS NOT NULL THEN 1 ELSE 0 END) AS error_count,
                    ROUND(
                        1.0 - (SUM(CASE WHEN a.error_code IS NOT NULL THEN 1 ELSE 0 END) * 1.0 / COUNT(a.id)),
                        3
                    ) AS reliability_score
                FROM providers p
                JOIN activities a ON p.id = a.provider_id
                GROUP BY p.id, p.name
                HAVING total_activities >= 10
                ORDER BY reliability_score DESC
            """
            rows = self.execute_safe(query)

        providers = []
        for row in rows:
            reliability = row["reliability_score"]
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

            providers.append(
                {
                    "provider_id": row["provider_id"],
                    "provider_name": row["provider_name"],
                    "reliability": reliability,
                    "grade": grade,
                    "total_activities": row["total_activities"],
                    "error_count": row["error_count"],
                }
            )

        return providers

    def close(self):
        """Close database connection."""
        if self.conn:
            self.conn.close()


# =============================================================================
# MAIN
# =============================================================================

if __name__ == "__main__":
    # Initialize database
    print("Initializing COSURVIVAL database...")
    db = SafeDatabase()
    print("✓ Database initialized with schema and indexes")
    db.close()
