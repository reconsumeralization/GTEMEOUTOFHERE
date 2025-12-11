#!/usr/bin/env python3
"""
RESEARCH LIBRARY SCHEMA
=======================
Lightweight schema for in-app Research Library.

This module provides:
1. Database schema for storing Medium papers
2. API endpoints for accessing papers
3. Auto-tagging logic
4. Integration with features, policies, and learning assets
"""

# Standard library imports
import json
from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from pathlib import Path
from typing import Any, Dict, List, Optional, Set

# Third-party imports (if using RSS parsing)
# import feedparser  # For RSS feed parsing


# =============================================================================
# ENUMS
# =============================================================================


class PaperCategory(Enum):
    """Primary categories for papers."""

    TEACHER = "teacher"
    TRIBE = "tribe"
    RECON = "recon"
    SECURITY = "security"
    SUPPLY_CHAIN = "supply_chain"
    TRANSPARENCY = "transparency"
    PHILOSOPHY = "philosophy"


class SecondaryTag(Enum):
    """Secondary tags for papers."""

    AI_ML = "ai_ml"
    GOVERNANCE = "governance"
    ETHICS = "ethics"
    ARCHITECTURE = "architecture"
    ALGORITHMS = "algorithms"
    DATA_STRUCTURES = "data_structures"
    SECURITY = "security"
    PRIVACY = "privacy"
    PROVENANCE = "provenance"
    EXPLAINABILITY = "explainability"


# =============================================================================
# DATA MODELS
# =============================================================================


@dataclass
class ResearchPaper:
    """
    Represents a Medium paper in the Research Library.

    This is the core data model for integrating research into the product.
    """

    # Identity (required fields first)
    id: str  # Unique identifier (e.g., "paper_supply_chain_risk")
    title: str
    medium_url: str  # Original Medium article URL
    abstract: str  # 2-3 line summary

    # Optional fields (with defaults)
    canonical_url: Optional[str] = None  # If syndicated to own domain
    full_text: Optional[str] = None  # If syndicated
    estimated_read_time: int = 0  # Minutes
    publish_date: datetime = field(default_factory=datetime.now)
    last_updated: Optional[datetime] = None
    author: str = "Reconsumeralization"

    # Taxonomy
    primary_category: PaperCategory = PaperCategory.PHILOSOPHY
    secondary_tags: Set[SecondaryTag] = field(default_factory=set)

    # Integration
    feature_links: List[str] = field(default_factory=list)
    """
    List of feature/module paths that this paper informs.
    Example: ["extractors/recon_scores.py", "governance.py"]
    """

    policy_links: List[str] = field(default_factory=list)
    """
    List of policy documents or governance rules.
    Example: ["governance.py", "curriculum/ethics/TEACHER_ETHICAL_GUARDRAILS.md"]
    """

    learning_asset_links: List[str] = field(default_factory=list)
    """
    List of TEACHER curriculum modules or problem sets.
    Example: ["curriculum/core/TEACHER_WEEK0.md", "curriculum/core/week1_problem_sets.md"]
    """

    # Takeaways
    one_sentence_takeaway: str = ""
    why_it_matters: str = ""

    # Media
    hero_image_url: Optional[str] = None
    excerpt: str = ""  # First paragraph or selected excerpt

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for JSON serialization."""
        return {
            "id": self.id,
            "title": self.title,
            "medium_url": self.medium_url,
            "canonical_url": self.canonical_url,
            "abstract": self.abstract,
            "full_text": self.full_text,
            "estimated_read_time": self.estimated_read_time,
            "publish_date": self.publish_date.isoformat(),
            "last_updated": self.last_updated.isoformat() if self.last_updated else None,
            "author": self.author,
            "primary_category": self.primary_category.value,
            "secondary_tags": [tag.value for tag in self.secondary_tags],
            "feature_links": self.feature_links,
            "policy_links": self.policy_links,
            "learning_asset_links": self.learning_asset_links,
            "one_sentence_takeaway": self.one_sentence_takeaway,
            "why_it_matters": self.why_it_matters,
            "hero_image_url": self.hero_image_url,
            "excerpt": self.excerpt,
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "ResearchPaper":
        """Create from dictionary."""
        return cls(
            id=data["id"],
            title=data["title"],
            medium_url=data["medium_url"],
            canonical_url=data.get("canonical_url"),
            abstract=data["abstract"],
            full_text=data.get("full_text"),
            estimated_read_time=data.get("estimated_read_time", 0),
            publish_date=datetime.fromisoformat(data["publish_date"]),
            last_updated=datetime.fromisoformat(data["last_updated"])
            if data.get("last_updated")
            else None,
            author=data.get("author", "Reconsumeralization"),
            primary_category=PaperCategory(data["primary_category"]),
            secondary_tags={SecondaryTag(tag) for tag in data.get("secondary_tags", [])},
            feature_links=data.get("feature_links", []),
            policy_links=data.get("policy_links", []),
            learning_asset_links=data.get("learning_asset_links", []),
            one_sentence_takeaway=data.get("one_sentence_takeaway", ""),
            why_it_matters=data.get("why_it_matters", ""),
            hero_image_url=data.get("hero_image_url"),
            excerpt=data.get("excerpt", ""),
        )


# =============================================================================
# AUTO-TAGGING LOGIC
# =============================================================================


def auto_tag_paper(
    title: str, abstract: str, content: Optional[str] = None
) -> tuple[PaperCategory, Set[SecondaryTag]]:
    """
    Auto-tag a paper based on title and content.

    Returns:
        (primary_category, secondary_tags)
    """
    text = (title + " " + abstract + " " + (content or "")).lower()

    # Determine primary category
    primary = PaperCategory.PHILOSOPHY  # Default

    if any(term in text for term in ["supply chain", "sbom", "provenance", "signed artifact"]):
        primary = PaperCategory.SUPPLY_CHAIN
    elif any(
        term in text for term in ["teacher", "learning", "education", "curriculum", "mastery"]
    ):
        primary = PaperCategory.TEACHER
    elif any(
        term in text for term in ["tribe", "collaboration", "community", "mentorship", "network"]
    ):
        primary = PaperCategory.TRIBE
    elif any(
        term in text
        for term in ["recon", "reconsumeralization", "value exchange", "provider", "consumer"]
    ):
        primary = PaperCategory.RECON
    elif any(
        term in text for term in ["security", "privacy", "pii", "access control", "authentication"]
    ):
        primary = PaperCategory.SECURITY
    elif any(term in text for term in ["transparent", "explain", "reasoning", "governance gate"]):
        primary = PaperCategory.TRANSPARENCY

    # Determine secondary tags
    tags = set()

    if any(term in text for term in ["ai", "ml", "machine learning", "advisor", "authority"]):
        tags.add(SecondaryTag.AI_ML)

    if any(term in text for term in ["governance", "policy", "rule", "guardrail", "prohibited"]):
        tags.add(SecondaryTag.GOVERNANCE)

    if any(term in text for term in ["ethics", "fairness", "bias", "exploitation", "ethical"]):
        tags.add(SecondaryTag.ETHICS)

    if any(term in text for term in ["architecture", "design", "system", "structure"]):
        tags.add(SecondaryTag.ARCHITECTURE)

    if any(term in text for term in ["algorithm", "sort", "search", "graph", "tree"]):
        tags.add(SecondaryTag.ALGORITHMS)

    if any(term in text for term in ["data structure", "queue", "stack", "hash", "trie"]):
        tags.add(SecondaryTag.DATA_STRUCTURES)

    if any(term in text for term in ["security", "encryption", "hashing", "authentication"]):
        tags.add(SecondaryTag.SECURITY)

    if any(term in text for term in ["privacy", "pii", "anonymize", "redact"]):
        tags.add(SecondaryTag.PRIVACY)

    if any(term in text for term in ["provenance", "sbom", "signed", "artifact"]):
        tags.add(SecondaryTag.PROVENANCE)

    if any(term in text for term in ["explain", "transparent", "reasoning", "why"]):
        tags.add(SecondaryTag.EXPLAINABILITY)

    return primary, tags


# =============================================================================
# RESEARCH LIBRARY SERVICE
# =============================================================================


class ResearchLibrary:
    """
    Service for managing the Research Library.

    This handles:
    - Storing papers
    - Auto-tagging
    - Filtering and search
    - Integration with features, policies, learning assets
    """

    def __init__(self, storage_path: Optional[str] = None):
        """
        Initialize Research Library.

        Args:
            storage_path: Path to JSON file for storage (or None for in-memory)
        """
        self.storage_path = storage_path
        self.papers: Dict[str, ResearchPaper] = {}

        if storage_path and Path(storage_path).exists():
            self.load()

    def add_paper(self, paper: ResearchPaper, auto_tag: bool = True):
        """Add a paper to the library."""
        if auto_tag:
            primary, tags = auto_tag_paper(paper.title, paper.abstract, paper.full_text)
            paper.primary_category = primary
            paper.secondary_tags.update(tags)

        self.papers[paper.id] = paper
        self.save()

    def get_paper(self, paper_id: str) -> Optional[ResearchPaper]:
        """Get a paper by ID."""
        return self.papers.get(paper_id)

    def list_papers(
        self,
        category: Optional[PaperCategory] = None,
        tags: Optional[Set[SecondaryTag]] = None,
        feature_link: Optional[str] = None,
        policy_link: Optional[str] = None,
        learning_asset_link: Optional[str] = None,
    ) -> List[ResearchPaper]:
        """
        List papers with optional filters.

        Args:
            category: Filter by primary category
            tags: Filter by secondary tags (any match)
            feature_link: Filter by feature link
            policy_link: Filter by policy link
            learning_asset_link: Filter by learning asset link
        """
        results = list(self.papers.values())

        if category:
            results = [p for p in results if p.primary_category == category]

        if tags:
            results = [p for p in results if p.secondary_tags & tags]

        if feature_link:
            results = [p for p in results if feature_link in p.feature_links]

        if policy_link:
            results = [p for p in results if policy_link in p.policy_links]

        if learning_asset_link:
            results = [p for p in results if learning_asset_link in p.learning_asset_links]

        # Sort by publish date (newest first)
        results.sort(key=lambda p: p.publish_date, reverse=True)

        return results

    def get_papers_for_feature(self, feature_path: str) -> List[ResearchPaper]:
        """Get all papers that inform a specific feature."""
        return self.list_papers(feature_link=feature_path)

    def get_papers_for_policy(self, policy_path: str) -> List[ResearchPaper]:
        """Get all papers that inform a specific policy."""
        return self.list_papers(policy_link=policy_path)

    def get_papers_for_learning_asset(self, asset_path: str) -> List[ResearchPaper]:
        """Get all papers for a specific learning asset."""
        return self.list_papers(learning_asset_link=asset_path)

    def save(self):
        """Save papers to storage."""
        if not self.storage_path:
            return

        data = {
            "papers": [paper.to_dict() for paper in self.papers.values()],
            "updated_at": datetime.now().isoformat(),
        }

        with open(self.storage_path, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2, default=str)

    def load(self):
        """Load papers from storage."""
        if not self.storage_path or not Path(self.storage_path).exists():
            return

        with open(self.storage_path, "r", encoding="utf-8") as f:
            data = json.load(f)

        for paper_data in data.get("papers", []):
            paper = ResearchPaper.from_dict(paper_data)
            self.papers[paper.id] = paper


# =============================================================================
# RSS FEED PARSER (Optional)
# =============================================================================


def parse_medium_rss(rss_url: str) -> List[Dict[str, Any]]:
    """
    Parse Medium RSS feed and extract paper metadata.

    This would use feedparser or similar library.

    Returns:
        List of paper dictionaries with title, link, summary, etc.
    """
    # Example implementation (requires feedparser):
    # import feedparser
    # feed = feedparser.parse(rss_url)
    # papers = []
    # for entry in feed.entries:
    #     papers.append({
    #         'title': entry.title,
    #         'medium_url': entry.link,
    #         'abstract': entry.summary,
    #         'publish_date': datetime(*entry.published_parsed[:6]),
    #         'author': entry.author,
    #     })
    # return papers

    # Placeholder
    return []


# =============================================================================
# EXAMPLE USAGE
# =============================================================================


def main():
    """Example usage of Research Library."""
    library = ResearchLibrary(storage_path="research_library.json")

    # Example paper
    paper = ResearchPaper(
        id="paper_supply_chain_risk",
        title="Cross-ecosystem supply chain risk: Why provenance matters",
        medium_url="https://medium.com/@reconsumeralization/...",
        abstract="Supply chain attacks succeed because we don't verify provenance. Signed artifacts and SBOMs create auditable trust chains.",
        estimated_read_time=8,
        one_sentence_takeaway="Supply chain attacks succeed because we don't verify provenance; signed artifacts and SBOMs create auditable trust chains.",
        why_it_matters="Informs our provider scoring system and provenance tracking requirements.",
        feature_links=["extractors/recon_scores.py", "governance.py"],
        policy_links=["governance.py"],
        learning_asset_links=[
            "curriculum/core/TEACHER_WEEK7.md",
            "curriculum/core/TEACHER_WEEK10.md",
        ],
    )

    library.add_paper(paper, auto_tag=True)

    # Query examples
    print("Papers for supply chain category:")
    for p in library.list_papers(category=PaperCategory.SUPPLY_CHAIN):
        print(f"  - {p.title}")

    print("\nPapers that inform governance.py:")
    for p in library.get_papers_for_policy("governance.py"):
        print(f"  - {p.title}: {p.one_sentence_takeaway}")


if __name__ == "__main__":
    main()
