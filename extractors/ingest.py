#!/usr/bin/env python3
"""
RAPID CSV INGESTION
===================
Fast CSV processing using Pandas.

This is the Python productivity layer - what took 200 lines in C
takes 20 lines here.
"""

"""
RAPID CSV INGESTION
===================
Fast CSV processing using Pandas.

This is the Python productivity layer - what took 200 lines in C
takes 20 lines here.
"""

# Standard library imports
import os  # noqa: E402
import sys  # noqa: E402
from copy import deepcopy  # noqa: E402
from dataclasses import dataclass  # noqa: E402
from typing import Dict, List, Tuple, Any, Optional  # noqa: E402

# Third-party imports
import pandas as pd  # type: ignore[import-untyped]  # noqa: E402

# Add parent directory to path for core imports
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Local imports
from governance import PIIHandler  # noqa: E402
from security import sanitize_input, validate_company_id, validate_user_id  # noqa: E402


# Simple data classes for rapid extraction
@dataclass
class CanonicalActivity:
    id: str
    timestamp: str
    timestamp_date: str = ""
    activity_type: str = ""
    user_id: str = ""
    target_user_id: str = ""
    company_id: str = ""
    resource_id: str = ""
    state_before: str = ""
    state_after: str = ""
    error_code: str = ""
    provider_id: str = ""


@dataclass
class CanonicalUser:
    id: str
    company_id: str = ""
    activity_count: int = 0


@dataclass
class CanonicalCompany:
    id: str
    name: str = ""
    activity_count: int = 0


@dataclass
class CanonicalProvider:
    id: str
    name: str = ""
    activity_count: int = 0
    error_count: int = 0


def ingest_csv(filepath: str, encoding: Optional[str] = None) -> pd.DataFrame:
    """
    Load CSV - Python makes this trivial.

    Args:
        filepath: Path to CSV file
        encoding: Optional encoding (auto-detected if None)

    Returns:
        DataFrame with raw data
    """
    encodings = [encoding] if encoding else ["utf-8", "latin-1", "cp1252", "iso-8859-1"]

    for enc in encodings:
        try:
            df = pd.read_csv(filepath, encoding=enc, low_memory=False)
            print(f"✓ Loaded {len(df):,} rows with {len(df.columns)} columns (encoding: {enc})")
            return df
        except UnicodeDecodeError:
            continue
        except Exception as e:
            print(f"✗ Error with {enc}: {e}")
            continue

    raise ValueError(f"Could not load CSV from {filepath}")


def hash_pii(value: Any) -> str:
    """Quick PII hashing - uses governance handler."""
    if pd.isna(value) or not value:
        return ""

    handler = PIIHandler()
    return handler.hash_value(str(value), "uid")


def extract_entities(
    df: pd.DataFrame, pii_handler: Optional[PIIHandler] = None
) -> Tuple[Dict, Dict, Dict, List]:
    """
    Extract entities - fast Python iteration.

    Returns:
        (users, companies, providers, activities)
    """
    if pii_handler is None:
        pii_handler = PIIHandler()

    users = {}
    companies = {}
    providers = {}
    activities = []

    # Fast iteration with iterrows
    for idx, row in df.iterrows():
        try:
            # Extract user (with validation and deep copy)
            uid_raw = row.get("Uid") or row.get("uid") or row.get("UserID")
            if pd.notna(uid_raw):
                # Sanitize input (Week 10: XSS prevention)
                uid_raw = sanitize_input(uid_raw)
                user_id = hash_pii(uid_raw)

                # Validate user_id format (Week 10: input validation)
                is_valid, error = validate_user_id(user_id)
                if not is_valid:
                    print(f"⚠️  Invalid user_id format: {error}")
                    continue

                if user_id and user_id not in users:
                    # Deep copy to safe schema (Week 4: memory safety)
                    company_id_raw = str(row.get("CompanyId", row.get("companyid", "")))
                    company_id = sanitize_input(company_id_raw) if company_id_raw != "nan" else ""

                    # Create new object (no shared references)
                    users[user_id] = CanonicalUser(
                        id=user_id, company_id=company_id, activity_count=0
                    )
                if user_id:
                    users[user_id].activity_count += 1

            # Extract company (with validation)
            company_id_raw = str(row.get("CompanyId", row.get("companyid", "")))
            if company_id_raw and company_id_raw != "nan":
                company_id = sanitize_input(company_id_raw)

                # Validate company_id (Week 10: input validation)
                is_valid, error = validate_company_id(company_id)
                if not is_valid:
                    print(f"⚠️  Invalid company_id format: {error}")
                    continue

                if company_id not in companies:
                    # Deep copy to safe schema (Week 4: memory safety)
                    company_name = sanitize_input(
                        str(row.get("CompanyName", row.get("companyname", "")))
                    )
                    companies[company_id] = CanonicalCompany(
                        id=company_id, name=company_name, activity_count=0
                    )
                companies[company_id].activity_count += 1

            # Extract provider
            provider_id = str(row.get("Pid", row.get("pid", row.get("ProviderId", ""))))
            if provider_id and provider_id != "nan" and provider_id not in providers:
                providers[provider_id] = CanonicalProvider(
                    id=provider_id,
                    name=str(row.get("ProviderName", row.get("providername", ""))),
                    activity_count=0,
                    error_count=0,
                )
            if provider_id and provider_id != "nan":
                providers[provider_id].activity_count += 1
                if pd.notna(row.get("CodeError", row.get("codeerror"))):
                    providers[provider_id].error_count += 1

            # Extract activity
            activity_type = str(row.get("Type", row.get("type", "")))
            timestamp = str(row.get("Date", row.get("date", row.get("Timestamp", ""))))

            if activity_type and activity_type != "nan":
                # Deep copy to safe schema (Week 4: memory safety)
                # All fields sanitized (Week 10: XSS prevention)
                safe_activity = CanonicalActivity(
                    id=f"act_{idx}",
                    timestamp=sanitize_input(timestamp),
                    timestamp_date=sanitize_input(timestamp[:10] if len(timestamp) >= 10 else ""),
                    activity_type=sanitize_input(activity_type),
                    user_id=user_id if "user_id" in locals() else "",
                    target_user_id=hash_pii(row.get("UidOpp", row.get("uidopp")))
                    if pd.notna(row.get("UidOpp", row.get("uidopp")))
                    else "",
                    company_id=company_id if company_id != "nan" else "",
                    provider_id=provider_id if provider_id != "nan" else "",
                    state_before=sanitize_input(str(row.get("StateOld", row.get("stateold", "")))),
                    state_after=sanitize_input(str(row.get("StateNew", row.get("statenew", "")))),
                    error_code=sanitize_input(str(row.get("CodeError", row.get("codeerror", ""))))
                    if pd.notna(row.get("CodeError", row.get("codeerror")))
                    else "",
                )
                # Append deep copy (not reference)
                activities.append(deepcopy(safe_activity))

        except Exception as e:
            # Graceful failure - log but continue
            print(f"⚠️  Row {idx} error: {e}")
            continue

    print(
        f"✓ Extracted: {len(users)} users, {len(companies)} companies, "
        f"{len(providers)} providers, {len(activities)} activities"
    )

    return users, companies, providers, activities


if __name__ == "__main__":
    # Quick test
    if len(sys.argv) > 1:
        df = ingest_csv(sys.argv[1])
        users, companies, providers, activities = extract_entities(df)
        print(f"\n✓ Ingested {len(activities)} activities")
