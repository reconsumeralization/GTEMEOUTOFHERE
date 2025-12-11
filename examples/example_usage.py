"""
COSURVIVAL Example Usage
========================

This example demonstrates basic usage of the COSURVIVAL pipeline.
"""

import os
import sys
from pathlib import Path

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent))

from pipeline import run_pipeline


def main():
    """
    Example: Run COSURVIVAL pipeline on sample data
    """
    # Example CSV path (create your own sample data)
    sample_csv = Path(__file__).parent / "sample_activity_data.csv"
    output_dir = Path(__file__).parent.parent / "output"
    
    # Create output directory if it doesn't exist
    output_dir.mkdir(exist_ok=True)
    
    # Check if sample data exists
    if not sample_csv.exists():
        print(f"Sample data not found at {sample_csv}")
        print("\nTo use this example:")
        print("1. Create a CSV file with activity data")
        print("2. See README.md for expected column formats")
        print("3. Update the sample_csv path above")
        return
    
    print("Running COSURVIVAL pipeline...")
    print(f"Input: {sample_csv}")
    print(f"Output: {output_dir}")
    print()
    
    try:
        # Run the pipeline
        results = run_pipeline(str(sample_csv), str(output_dir))
        
        print("✓ Pipeline completed successfully!")
        print(f"\nGenerated files in {output_dir}:")
        for file in output_dir.glob("*.json"):
            print(f"  - {file.name}")
        for file in output_dir.glob("*.html"):
            print(f"  - {file.name}")
        
        print(f"\nView dashboard: {output_dir / 'dashboard.html'}")
        
    except Exception as e:
        print(f"✗ Error running pipeline: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()

