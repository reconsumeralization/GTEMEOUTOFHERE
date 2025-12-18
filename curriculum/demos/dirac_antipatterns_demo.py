#!/usr/bin/env python3
"""
Dirac Anti-Patterns Demo
========================

Demonstrates the Dirac-inspired anti-pattern detection system.

Like Dirac's negative energy solutions revealing antiparticles,
we find insights in gaps, absences, and inverse relationships.

CURRICULUM: Week 0, Activity 0.5 - Negative Patterns Are Not Nonsense
Week 1, Activity 1.3 - Multi-Component Wave Functions
See: curriculum/vision/chapters/DIrac_ANTIPATTERNS_APPLICATION.md
"""

import sys
from pathlib import Path

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from advisor import CosurvivalAdvisor, UserPreferences, Domain, SignalStrength
from models import PatternSignal


def main():
    """Demonstrate anti-pattern detection."""
    print("=" * 70)
    print("  DIRAC ANTI-PATTERNS DEMO")
    print("  Like Dirac's negative energy → antiparticles,")
    print("  we find insights in gaps, absences, and inverses")
    print("=" * 70)

    advisor = CosurvivalAdvisor()

    # Set up user preferences
    print("\n1. Setting user preferences...")
    prefs = UserPreferences(
        user_id="demo_user_001",
        communication_style="supportive",
        min_confidence_threshold=0.5,
    )
    advisor.set_user_preferences("demo_user_001", prefs)
    print("   [OK] User preferences set")

    # Create sample positive patterns
    print("\n2. Creating sample positive patterns...")
    positive_patterns = [
        PatternSignal(
            id="pattern_tribe_001",
            domain=Domain.TRIBE,
            signal_type="high_collaboration",
            strength=SignalStrength.MODERATE,
            description="User collaborates frequently with Team X",
            detected_at="2024-01-15T10:00:00",
            confidence=0.75,
            evidence=["45 interactions in last 30 days", "Active in Team X channels"],
            framing="Strong collaboration with Team X",
        ),
        PatternSignal(
            id="pattern_teacher_001",
            domain=Domain.TEACHER,
            signal_type="skill_progression",
            strength=SignalStrength.STRONG,
            description="User is progressing in data governance skills",
            detected_at="2024-01-15T10:00:00",
            confidence=0.85,
            evidence=["Completed 3 modules", "Passed 2 checkpoints"],
            framing="Excellent progress in data governance",
        ),
        PatternSignal(
            id="pattern_recon_001",
            domain=Domain.RECON,
            signal_type="provider_adoption",
            strength=SignalStrength.MODERATE,
            description="User actively uses Provider Y for analytics",
            detected_at="2024-01-15T10:00:00",
            confidence=0.70,
            evidence=["High usage of Provider Y", "Positive feedback"],
            framing="Effective use of Provider Y",
        ),
    ]
    print(f"   [OK] Created {len(positive_patterns)} positive patterns")

    # Detect anti-patterns
    print("\n3. Detecting complementary anti-patterns...")
    demo_data = {
        "tribe": {"collaboration_trend": {"direction": "declining", "rate": 0.3}},
        "teacher": {"skill_gaps": ["security_literacy"]},
        "recon": {"friction_points": [{"provider": "tool_c", "issue": "not_adopted"}]},
    }

    anti_patterns = advisor.detect_anti_patterns("demo_user_001", demo_data, positive_patterns)
    print(f"   [OK] Detected {len(anti_patterns)} anti-patterns")

    # Display anti-patterns
    print("\n4. Anti-Pattern Analysis:")
    for i, anti_pattern in enumerate(anti_patterns, 1):
        print(f"\n   [{i}] {anti_pattern.anti_pattern_type.upper()}")
        print(f"       Domain: {anti_pattern.domain}")
        print(f"       Description: {anti_pattern.description}")
        print(f"       Gap: {anti_pattern.gap_description}")
        print(f"       Framing: {anti_pattern.framing}")
        if anti_pattern.complementary_to:
            print(f"       Complementary to: {anti_pattern.complementary_to}")

    # Analyze pattern-anti-pattern annihilation
    print("\n5. Pattern-Anti-Pattern Annihilation:")
    if positive_patterns and anti_patterns:
        # Match first pattern with first anti-pattern
        pattern = positive_patterns[0]
        anti_pattern = anti_patterns[0] if anti_patterns else None

        if anti_pattern and anti_pattern.complementary_to == pattern.id:
            annihilation = advisor.analyze_pattern_annihilation(pattern, anti_pattern)
            print(f"\n   Pattern: {pattern.description}")
            print(f"   Anti-Pattern: {anti_pattern.description}")
            print(f"\n   Annihilation Insight:")
            print(f"   {annihilation['insight']}")
            print(f"\n   Revealed Truth:")
            print(f"   {annihilation['revealed_truth']}")
            if annihilation.get("recommendation"):
                print(f"\n   Recommendation:")
                print(f"   {annihilation['recommendation']}")

    # Temporal inversion example
    print("\n6. Temporal Inversion Analysis:")
    print("   Working backwards from outcomes to find causes...")
    temporal_result = advisor.analyze_temporal_inversion(
        demo_data, "sensitive_data_access"
    )
    print(f"   Outcome: {temporal_result['outcome']}")
    print(f"   Root Causes: {temporal_result.get('root_causes', [])}")
    print(f"   Insight: {temporal_result.get('insight', '')}")

    print("\n" + "=" * 70)
    print("  DEMO COMPLETE")
    print("=" * 70)
    print("\nKey Takeaways:")
    print("  • Negative patterns (gaps, absences) are valid insights")
    print("  • Every pattern has a complementary anti-pattern")
    print("  • Pattern-anti-pattern pairs reveal complete truth")
    print("  • Temporal inversion works both forwards and backwards")
    print("\nSee: curriculum/vision/chapters/DIrac_ANTIPATTERNS_APPLICATION.md")


if __name__ == "__main__":
    main()
