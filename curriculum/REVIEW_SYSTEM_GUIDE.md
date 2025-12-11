# Review System Guide

## Overview

The TEACHER review system allows learners to provide multi-factor feedback on specific features and the overall course at different stages (before, during, after). It aligns with TEACHER's philosophy: self-relative, growth-focused, and non-judgmental.

---

## Philosophy

### Self-Relative
- Reviews are about the learner's individual experience
- No comparison to other learners
- Focus on personal growth and trajectory

### Growth-Focused
- Emphasis on "what helped most" and "growth observed"
- "What could improve" framed as opportunities, not deficiencies
- Trajectory over position

### Multi-Factor
- Not just one rating—multiple dimensions
- Clarity, engagement, usefulness, inspiration, etc.
- Allows nuanced feedback

### Time-Aware
- Before: Expectations and initial impressions
- During: Real-time feedback as learning happens
- After: Reflection on completed experience

---

## Review Factors

### Clarity & Understanding
- **Clarity** - How clear was the content?
- **Explanation Quality** - Quality of explanations
- **Examples Helpful** - Were examples helpful?

### Engagement & Motivation
- **Engagement** - How engaging was it?
- **Motivation** - Did it motivate you?
- **Interest Level** - How interesting was it?

### Practical Value
- **Usefulness** - How useful was it?
- **Applicability** - Can you apply this?
- **Relevance** - How relevant to your goals?

### Difficulty & Challenge
- **Difficulty Level** - How difficult was it?
- **Challenge Appropriate** - Was challenge appropriate?
- **Pace** - Was the pace right?

### Support & Resources
- **Support Quality** - Quality of support/resources
- **Resources Helpful** - Were resources helpful?
- **Community Helpful** - Was community helpful?

### Inspiration & Values
- **Inspiration** - Did quotes/inspiration help?
- **Values Alignment** - Did it align with your values?
- **Meaningful** - Was it meaningful to you?

### Technical Quality
- **Code Quality** - Quality of code examples
- **Documentation** - Quality of documentation
- **Tools Effective** - Were tools effective?

---

## Review Targets

### Course Overall
Review the entire TEACHER Core Track experience.

**When to review:**
- **Before:** After reading overview, before starting
- **During:** Mid-course check-in
- **After:** Upon completion

**Example factors:**
- Overall clarity, engagement, usefulness
- Values alignment, meaningfulness
- Support quality, community helpfulness

### Week Module
Review a specific week (e.g., Week 1, Week 4).

**When to review:**
- **Before:** After reading week overview
- **During:** While working through activities
- **After:** Upon completing the week

**Example factors:**
- Clarity, explanation quality, examples
- Difficulty level, pace, challenge
- Inspiration, values alignment

### Activity
Review a specific activity (e.g., Activity 0.1, Activity 3.2).

**When to review:**
- **During:** While doing the activity
- **After:** Upon completing the activity

**Example factors:**
- Clarity, examples helpful
- Engagement, interest level
- Applicability, usefulness

### Feature
Review a specific feature (e.g., progression tracker, lens toggle).

**When to review:**
- **Before:** Initial impression
- **During:** While using the feature
- **After:** After extended use

**Example factors:**
- Clarity, documentation
- Tools effective, code quality
- Usefulness, applicability

### Resource
Review a specific resource (e.g., problem set, demo script).

**When to review:**
- **During:** While using the resource
- **After:** Upon completing the resource

**Example factors:**
- Clarity, examples helpful
- Resources helpful, support quality
- Usefulness, relevance

### Inspiration
Review the inspirational content (quotes, passages).

**When to review:**
- **During:** While reading/viewing inspiration
- **After:** After reflecting on inspiration

**Example factors:**
- Inspiration, values alignment
- Meaningful, engagement
- Clarity, explanation quality

---

## Review Stages

### Before
**Purpose:** Capture expectations and initial impressions.

**Questions to consider:**
- What are your expectations?
- What do you hope to learn?
- How does this align with your goals?
- What concerns do you have?

**Example:**
```python
review = create_week_review(
    learner_id="learner_123",
    week_number=1,
    stage=ReviewStage.BEFORE,
    factor_ratings=[
        FactorRating(ReviewFactor.CLARITY, 4, "Overview was clear"),
        FactorRating(ReviewFactor.RELEVANCE, 5, "Very relevant to my goals"),
    ],
    overall_rating=4,
    free_text="Excited to start! The foundation concepts make sense.",
)
```

### During
**Purpose:** Real-time feedback as learning happens.

**Questions to consider:**
- How is it going so far?
- What's helping you learn?
- What's challenging?
- What would help right now?

**Example:**
```python
review = create_week_review(
    learner_id="learner_123",
    week_number=1,
    stage=ReviewStage.DURING,
    factor_ratings=[
        FactorRating(ReviewFactor.CLARITY, 3, "Some concepts are unclear"),
        FactorRating(ReviewFactor.PACE, 4, "Pace is good"),
        FactorRating(ReviewFactor.EXAMPLES_HELPFUL, 5, "Examples really help"),
    ],
    overall_rating=4,
    what_helped="The examples and code snippets are very helpful",
    what_improve="Could use more explanation on data dictionary",
)
```

### After
**Purpose:** Reflection on completed experience.

**Questions to consider:**
- What helped you most?
- What growth did you observe?
- What could improve?
- How will you apply this?

**Example:**
```python
review = create_week_review(
    learner_id="learner_123",
    week_number=1,
    stage=ReviewStage.AFTER,
    factor_ratings=[
        FactorRating(ReviewFactor.CLARITY, 4),
        FactorRating(ReviewFactor.USEFULNESS, 5),
        FactorRating(ReviewFactor.INSPIRATION, 5, "Quotes really resonated"),
        FactorRating(ReviewFactor.APPLICABILITY, 4),
    ],
    overall_rating=5,
    what_helped="The data dictionary concept and the inspirational quotes",
    what_improve="Could use more practice problems",
    growth="I now understand how to build foundations for data systems",
)
```

---

## Growth-Focused Questions

### What Helped Most?
Focus on positive experiences and effective elements.

**Examples:**
- "The examples really clarified the concepts"
- "The inspirational quotes connected the technical to deeper meaning"
- "The progression tracker helped me see my growth"

### What Could Improve?
Framed as opportunities, not deficiencies.

**Examples:**
- "More examples would help" (not "examples were insufficient")
- "Could use more practice problems" (not "practice problems were lacking")
- "Slower pace for Week 4" (not "Week 4 was too fast")

### Growth Observed
Self-relative reflection on personal growth.

**Examples:**
- "I now understand how data structures encode morality"
- "I can see how the three lenses reveal different truths"
- "I feel more confident building governed systems"

---

## Usage Examples

### Review a Week Module

```python
from cosurvival.tracking.review_system import (
    ReviewSystem, ReviewStage, ReviewTarget, ReviewFactor,
    FactorRating, create_week_review
)

# Create review system
review_system = ReviewSystem()

# Create a review
review = create_week_review(
    learner_id="learner_123",
    week_number=5,
    stage=ReviewStage.AFTER,
    factor_ratings=[
        FactorRating(ReviewFactor.CLARITY, 5),
        FactorRating(ReviewFactor.ENGAGEMENT, 4),
        FactorRating(ReviewFactor.USEFULNESS, 5),
        FactorRating(ReviewFactor.INSPIRATION, 5, "The justice quotes really resonated"),
        FactorRating(ReviewFactor.APPLICABILITY, 4),
    ],
    overall_rating=5,
    what_helped="The alternative perspectives section showed how different thinkers approach fairness",
    what_improve="Could use more code examples for balanced trees",
    growth="I now understand how data structures encode morality",
)

# Submit review
review_id = review_system.submit_review(review)
```

### Review a Feature

```python
from cosurvival.tracking.review_system import (
    ReviewSystem, ReviewStage, ReviewTarget, ReviewFactor,
    FactorRating, create_feature_review
)

review_system = ReviewSystem()

review = create_feature_review(
    learner_id="learner_123",
    feature_name="Progression Tracker",
    stage=ReviewStage.DURING,
    factor_ratings=[
        FactorRating(ReviewFactor.CLARITY, 4),
        FactorRating(ReviewFactor.USEFULNESS, 5),
        FactorRating(ReviewFactor.TOOLS_EFFECTIVE, 4),
    ],
    overall_rating=5,
    free_text="Love seeing my growth trajectory! The self-relative approach is perfect.",
)

review_id = review_system.submit_review(review)
```

### Review the Course

```python
from cosurvival.tracking.review_system import (
    ReviewSystem, ReviewStage, ReviewTarget, ReviewFactor,
    FactorRating, create_course_review
)

review_system = ReviewSystem()

review = create_course_review(
    learner_id="learner_123",
    stage=ReviewStage.AFTER,
    factor_ratings=[
        FactorRating(ReviewFactor.CLARITY, 5),
        FactorRating(ReviewFactor.ENGAGEMENT, 5),
        FactorRating(ReviewFactor.USEFULNESS, 5),
        FactorRating(ReviewFactor.INSPIRATION, 5),
        FactorRating(ReviewFactor.VALUES_ALIGNMENT, 5),
        FactorRating(ReviewFactor.MEANINGFUL, 5),
    ],
    overall_rating=5,
    what_helped="The combination of technical rigor and inspirational content",
    what_improve="Could use more interactive demos",
    growth="I've grown from 'what is data?' to 'I can build ethical intelligence systems'",
)

review_id = review_system.submit_review(review)
```

### Get Review Summary

```python
# Get summary for Week 5
summary = review_system.get_review_summary(
    ReviewTarget.WEEK_MODULE,
    "week5"
)

print(f"Total reviews: {summary.total_reviews}")
print(f"Average rating: {summary.average_overall_rating}")
print(f"Clarity average: {summary.factor_averages.get(ReviewFactor.CLARITY)}")
print(f"Rating trend: {summary.rating_trend}")
```

### Get Learner Trajectory

```python
# Get a learner's review trajectory
trajectory = review_system.get_learner_review_trajectory("learner_123")

print(f"Total reviews: {trajectory['total_reviews']}")
for entry in trajectory['trajectory']:
    print(f"{entry['target']} ({entry['stage']}): {entry['overall_rating']}")
```

---

## Integration with Progression Tracker

The review system integrates with the progression tracker to provide context:

```python
from cosurvival.tracking.progression_tracker import ProgressionTracker
from cosurvival.tracking.review_system import ReviewSystem, ReviewStage

# Get learner's current progress
tracker = ProgressionTracker()
progress = tracker.get_learner_progress("learner_123")

# Create review with context
review_system = ReviewSystem()

# If learner just completed Week 5
if progress.current_week == 5:
    review = create_week_review(
        learner_id="learner_123",
        week_number=5,
        stage=ReviewStage.AFTER,
        # ... factor ratings ...
    )
    review_system.submit_review(review)
```

---

## Best Practices

### For Learners
1. **Be honest** - Your feedback helps improve the course
2. **Be specific** - "Examples helped" is better than "good"
3. **Focus on growth** - What helped you grow?
4. **Frame improvements positively** - "Could use more X" not "X was lacking"

### For Course Designers
1. **Review summaries regularly** - Look for patterns
2. **Pay attention to trends** - Is rating improving or declining?
3. **Focus on growth feedback** - What's helping learners grow?
4. **Address common improvements** - If multiple learners mention the same thing

### For System
1. **Respect anonymity** - If learner chooses anonymous
2. **Show helpful reviews** - Community can mark reviews as helpful
3. **Track trajectories** - Show learners their growth over time
4. **Aggregate wisely** - Summaries should respect self-relative philosophy

---

## API Integration

The review system can be integrated into the Flask app:

```python
from flask import Flask, request, jsonify
from cosurvival.tracking.review_system import ReviewSystem, ReviewStage, ReviewTarget

app = Flask(__name__)
review_system = ReviewSystem()

@app.route('/api/reviews', methods=['POST'])
def submit_review():
    """Submit a new review."""
    data = request.json
    # ... create review from data ...
    review_id = review_system.submit_review(review)
    return jsonify({'review_id': review_id})

@app.route('/api/reviews/<target_type>/<target_id>', methods=['GET'])
def get_reviews(target_type, target_id):
    """Get reviews for a target."""
    reviews = review_system.get_reviews_for_target(
        ReviewTarget[target_type.upper()],
        target_id
    )
    return jsonify([r.to_dict() for r in reviews])

@app.route('/api/reviews/<target_type>/<target_id>/summary', methods=['GET'])
def get_summary(target_type, target_id):
    """Get review summary for a target."""
    summary = review_system.get_review_summary(
        ReviewTarget[target_type.upper()],
        target_id
    )
    return jsonify(summary.to_dict())
```

---

*"Reviews are about growth, not judgment. They help us improve together."*

