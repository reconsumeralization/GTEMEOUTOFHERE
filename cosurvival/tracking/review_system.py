"""
Review System for TEACHER Curriculum
====================================
Allows multi-factor feedback on features and course at before/during/after stages.
Philosophy: Self-relative, growth-focused, non-judgmental.
"""

# =============================================================================
# IMPORTS
# =============================================================================

from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from typing import Dict, List, Optional, Set
from uuid import uuid4


# =============================================================================
# ENUMS
# =============================================================================

class ReviewStage(Enum):
    """When the review is given relative to the course."""
    BEFORE = "before"      # Before starting the course/module
    DURING = "during"      # While actively learning
    AFTER = "after"        # After completing the course/module


class ReviewFactor(Enum):
    """Factors learners can rate."""
    # Clarity & Understanding
    CLARITY = "clarity"                    # How clear was the content?
    EXPLANATION_QUALITY = "explanation"    # Quality of explanations
    EXAMPLES_HELPFUL = "examples"         # Were examples helpful?
    
    # Engagement & Motivation
    ENGAGEMENT = "engagement"              # How engaging was it?
    MOTIVATION = "motivation"              # Did it motivate you?
    INTEREST_LEVEL = "interest"            # How interesting was it?
    
    # Practical Value
    USEFULNESS = "usefulness"              # How useful was it?
    APPLICABILITY = "applicability"        # Can you apply this?
    RELEVANCE = "relevance"                # How relevant to your goals?
    
    # Difficulty & Challenge
    DIFFICULTY_LEVEL = "difficulty"        # How difficult was it?
    CHALLENGE_APPROPRIATE = "challenge"    # Was challenge appropriate?
    PACE = "pace"                          # Was the pace right?
    
    # Support & Resources
    SUPPORT_QUALITY = "support"            # Quality of support/resources
    RESOURCES_HELPFUL = "resources"        # Were resources helpful?
    COMMUNITY_HELPFUL = "community"        # Was community helpful?
    
    # Inspiration & Values
    INSPIRATION = "inspiration"            # Did quotes/inspiration help?
    VALUES_ALIGNMENT = "values"            # Did it align with your values?
    MEANINGFUL = "meaningful"              # Was it meaningful to you?
    
    # Technical Quality
    CODE_QUALITY = "code_quality"          # Quality of code examples
    DOCUMENTATION = "documentation"        # Quality of documentation
    TOOLS_EFFECTIVE = "tools"              # Were tools effective?



# =============================================================================
# DATA TARGETS
# =============================================================================
class ReviewTarget(Enum):
    """What is being reviewed."""
    COURSE_OVERALL = "course"              # Entire course
    WEEK_MODULE = "week"                   # Specific week (e.g., Week 1)
    ACTIVITY = "activity"                   # Specific activity
    FEATURE = "feature"                    # Specific feature (e.g., progression tracker)
    RESOURCE = "resource"                  # Specific resource (e.g., problem set)
    INSPIRATION = "inspiration"            # Quotes/inspiration content



# =============================================================================
# DATA CLASSES
# =============================================================================
@dataclass
class FactorRating:
    """Rating for a specific factor."""
    factor: ReviewFactor
    rating: int  # 1-5 scale
    comment: Optional[str] = None  # Optional explanation
    
    def __post_init__(self):
        if not 1 <= self.rating <= 5:
            raise ValueError(f"Rating must be 1-5, got {self.rating}")


@dataclass
class Review:
    """
    A review from a learner.
    
    Philosophy: Self-relative, growth-focused
    - Reviews are about the learner's experience, not comparison to others
    - Focus on growth and improvement, not deficiencies
    - Multiple factors allow nuanced feedback
    """
    learner_id: str  # Who gave the review
    target_type: ReviewTarget  # What is being reviewed
    target_id: str  # Specific ID (e.g., "week1", "progression_tracker")
    stage: ReviewStage  # When the review was given
    
    # Required fields first, then optional
    id: str = field(default_factory=lambda: str(uuid4()))
    
    # Ratings for different factors
    factor_ratings: List[FactorRating] = field(default_factory=list)
    
    # Overall feedback
    overall_rating: Optional[int] = None  # 1-5 overall
    free_text_feedback: Optional[str] = None  # Open-ended feedback
    
    # Growth-focused questions
    what_helped_most: Optional[str] = None  # What helped you most?
    what_could_improve: Optional[str] = None  # What could improve?
    growth_observed: Optional[str] = None  # What growth did you observe?
    
    # Context
    timestamp: datetime = field(default_factory=datetime.now)
    week_number: Optional[int] = None  # If reviewing a week
    module_name: Optional[str] = None  # Human-readable name
    
    # Metadata
    anonymous: bool = False  # Whether to show learner_id publicly
    helpful_count: int = 0  # How many found this review helpful
    
    def to_dict(self) -> Dict:
        """Convert to dictionary for storage/API."""
        return {
            'id': self.id,
            'learner_id': self.learner_id,
            'target_type': self.target_type.value,
            'target_id': self.target_id,
            'stage': self.stage.value,
            'factor_ratings': [
                {
                    'factor': fr.factor.value,
                    'rating': fr.rating,
                    'comment': fr.comment
                }
                for fr in self.factor_ratings
            ],
            'overall_rating': self.overall_rating,
            'free_text_feedback': self.free_text_feedback,
            'what_helped_most': self.what_helped_most,
            'what_could_improve': self.what_could_improve,
            'growth_observed': self.growth_observed,
            'timestamp': self.timestamp.isoformat(),
            'week_number': self.week_number,
            'module_name': self.module_name,
            'anonymous': self.anonymous,
            'helpful_count': self.helpful_count,
        }


@dataclass
class ReviewSummary:
    """Aggregated summary of reviews for a target."""
    target_type: ReviewTarget
    target_id: str
    
    # Overall stats
    total_reviews: int = 0
    average_overall_rating: Optional[float] = None
    
    # Factor averages
    factor_averages: Dict[ReviewFactor, float] = field(default_factory=dict)
    
    # Stage distribution
    before_count: int = 0
    during_count: int = 0
    after_count: int = 0
    
    # Growth insights
    common_what_helped: List[str] = field(default_factory=list)
    common_improvements: List[str] = field(default_factory=list)
    common_growth: List[str] = field(default_factory=list)
    
    # Trends
    rating_trend: Optional[str] = None  # "improving", "declining", "stable"
    
    def to_dict(self) -> Dict:
        """Convert to dictionary for API."""
        return {
            'target_type': self.target_type.value,
            'target_id': self.target_id,
            'total_reviews': self.total_reviews,
            'average_overall_rating': self.average_overall_rating,
            'factor_averages': {
                factor.value: avg
                for factor, avg in self.factor_averages.items()
            },
            'stage_distribution': {
                'before': self.before_count,
                'during': self.during_count,
                'after': self.after_count,
            },
            'common_what_helped': self.common_what_helped,
            'common_improvements': self.common_improvements,
            'common_growth': self.common_growth,
            'rating_trend': self.rating_trend,
        }


class ReviewSystem:
    """
    Manages reviews and feedback for TEACHER curriculum.
    
    Philosophy:
    - Self-relative: Reviews are about individual experience
    - Growth-focused: Emphasis on what helped and growth observed
    - Multi-factor: Multiple dimensions, not just one rating
    - Time-aware: Before, during, after tracking
    """
    
    def __init__(self):
        self.reviews: Dict[str, Review] = {}  # review_id -> Review
        self.reviews_by_target: Dict[str, List[str]] = {}  # target -> review_ids
        self.reviews_by_learner: Dict[str, List[str]] = {}  # learner_id -> review_ids
    
    def submit_review(self, review: Review) -> str:
        """
        Submit a new review.
        
        Returns review ID.
        """
        # Store review
        self.reviews[review.id] = review
        
        # Index by target
        target_key = f"{review.target_type.value}:{review.target_id}"
        if target_key not in self.reviews_by_target:
            self.reviews_by_target[target_key] = []
        self.reviews_by_target[target_key].append(review.id)
        
        # Index by learner
        if review.learner_id not in self.reviews_by_learner:
            self.reviews_by_learner[review.learner_id] = []
        self.reviews_by_learner[review.learner_id].append(review.id)
        
        return review.id
    
    def get_reviews_for_target(
        self,
        target_type: ReviewTarget,
        target_id: str,
        stage: Optional[ReviewStage] = None
    ) -> List[Review]:
        """Get all reviews for a specific target."""
        target_key = f"{target_type.value}:{target_id}"
        review_ids = self.reviews_by_target.get(target_key, [])
        
        reviews = [self.reviews[rid] for rid in review_ids]
        
        if stage:
            reviews = [r for r in reviews if r.stage == stage]
        
        return sorted(reviews, key=lambda r: r.timestamp, reverse=True)
    
    def get_reviews_for_learner(
        self,
        learner_id: str,
        stage: Optional[ReviewStage] = None
    ) -> List[Review]:
        """Get all reviews from a specific learner."""
        review_ids = self.reviews_by_learner.get(learner_id, [])
        
        reviews = [self.reviews[rid] for rid in review_ids]
        
        if stage:
            reviews = [r for r in reviews if r.stage == stage]
        
        return sorted(reviews, key=lambda r: r.timestamp, reverse=True)
    
    def get_review_summary(
        self,
        target_type: ReviewTarget,
        target_id: str
    ) -> ReviewSummary:
        """Get aggregated summary of reviews for a target."""
        reviews = self.get_reviews_for_target(target_type, target_id)
        
        if not reviews:
            return ReviewSummary(target_type=target_type, target_id=target_id)
        
        # Overall rating average
        overall_ratings = [r.overall_rating for r in reviews if r.overall_rating]
        avg_overall = sum(overall_ratings) / len(overall_ratings) if overall_ratings else None
        
        # Factor averages
        factor_totals: Dict[ReviewFactor, List[int]] = {}
        for review in reviews:
            for fr in review.factor_ratings:
                if fr.factor not in factor_totals:
                    factor_totals[fr.factor] = []
                factor_totals[fr.factor].append(fr.rating)
        
        factor_averages = {
            factor: sum(ratings) / len(ratings)
            for factor, ratings in factor_totals.items()
        }
        
        # Stage distribution
        before_count = sum(1 for r in reviews if r.stage == ReviewStage.BEFORE)
        during_count = sum(1 for r in reviews if r.stage == ReviewStage.DURING)
        after_count = sum(1 for r in reviews if r.stage == ReviewStage.AFTER)
        
        # Common themes (simplified - would use NLP in production)
        what_helped = [r.what_helped_most for r in reviews if r.what_helped_most]
        improvements = [r.what_could_improve for r in reviews if r.what_could_improve]
        growth = [r.growth_observed for r in reviews if r.growth_observed]
        
        # Rating trend (simplified - compare early vs late reviews)
        if len(reviews) >= 4:
            early_avg = sum(r.overall_rating or 0 for r in reviews[:len(reviews)//2] if r.overall_rating) / (len(reviews)//2)
            late_avg = sum(r.overall_rating or 0 for r in reviews[len(reviews)//2:] if r.overall_rating) / (len(reviews) - len(reviews)//2)
            if late_avg > early_avg + 0.2:
                trend = "improving"
            elif late_avg < early_avg - 0.2:
                trend = "declining"
            else:
                trend = "stable"
        else:
            trend = None
        
        return ReviewSummary(
            target_type=target_type,
            target_id=target_id,
            total_reviews=len(reviews),
            average_overall_rating=avg_overall,
            factor_averages=factor_averages,
            before_count=before_count,
            during_count=during_count,
            after_count=after_count,
            common_what_helped=what_helped[:5],  # Top 5
            common_improvements=improvements[:5],
            common_growth=growth[:5],
            rating_trend=trend,
        )
    
    def get_learner_review_trajectory(self, learner_id: str) -> Dict:
        """
        Get a learner's review trajectory over time.
        
        Shows how their experience evolved (self-relative growth).
        """
        reviews = self.get_reviews_for_learner(learner_id)
        
        if not reviews:
            return {
                'learner_id': learner_id,
                'total_reviews': 0,
                'trajectory': [],
            }
        
        # Group by target and stage
        trajectory = []
        for review in sorted(reviews, key=lambda r: r.timestamp):
            trajectory.append({
                'target': f"{review.target_type.value}:{review.target_id}",
                'stage': review.stage.value,
                'overall_rating': review.overall_rating,
                'timestamp': review.timestamp.isoformat(),
                'factors': {
                    fr.factor.value: fr.rating
                    for fr in review.factor_ratings
                },
            })
        
        return {
            'learner_id': learner_id,
            'total_reviews': len(reviews),
            'trajectory': trajectory,
        }
    
    def mark_review_helpful(self, review_id: str) -> None:
        """Mark a review as helpful (for community feedback)."""
        if review_id in self.reviews:
            self.reviews[review_id].helpful_count += 1


# =============================================================================
# EXAMPLE HELPERS
# =============================================================================

def create_week_review(
    learner_id: str,
    week_number: int,
    stage: ReviewStage,
    factor_ratings: List[FactorRating],
    overall_rating: Optional[int] = None,
    free_text: Optional[str] = None,
    what_helped: Optional[str] = None,
    what_improve: Optional[str] = None,
    growth: Optional[str] = None,
) -> Review:
    """Helper to create a week review."""
    return Review(
        learner_id=learner_id,
        target_type=ReviewTarget.WEEK_MODULE,
        target_id=f"week{week_number}",
        stage=stage,
        factor_ratings=factor_ratings,
        overall_rating=overall_rating,
        free_text_feedback=free_text,
        what_helped_most=what_helped,
        what_could_improve=what_improve,
        growth_observed=growth,
        week_number=week_number,
        module_name=f"Week {week_number}",
    )


def create_feature_review(
    learner_id: str,
    feature_name: str,
    stage: ReviewStage,
    factor_ratings: List[FactorRating],
    overall_rating: Optional[int] = None,
    free_text: Optional[str] = None,
) -> Review:
    """Helper to create a feature review."""
    return Review(
        learner_id=learner_id,
        target_type=ReviewTarget.FEATURE,
        target_id=feature_name.lower().replace(" ", "_"),
        stage=stage,
        factor_ratings=factor_ratings,
        overall_rating=overall_rating,
        free_text_feedback=free_text,
        module_name=feature_name,
    )


def create_course_review(
    learner_id: str,
    stage: ReviewStage,
    factor_ratings: List[FactorRating],
    overall_rating: Optional[int] = None,
    free_text: Optional[str] = None,
    what_helped: Optional[str] = None,
    what_improve: Optional[str] = None,
    growth: Optional[str] = None,
) -> Review:
    """Helper to create a course-wide review."""
    return Review(
        learner_id=learner_id,
        target_type=ReviewTarget.COURSE_OVERALL,
        target_id="teacher_core_track",
        stage=stage,
        factor_ratings=factor_ratings,
        overall_rating=overall_rating,
        free_text_feedback=free_text,
        what_helped_most=what_helped,
        what_could_improve=what_improve,
        growth_observed=growth,
        module_name="TEACHER Core Track",
    )

