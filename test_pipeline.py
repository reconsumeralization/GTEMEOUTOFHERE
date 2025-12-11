#!/usr/bin/env python3
"""Quick test of rapid pipeline module."""
try:
    from extractors.rapid_pipeline import run_rapid_pipeline  # noqa: F401

    print("[OK] Pipeline module loaded successfully")
    print("[OK] Ready to process CSV files")
    print("\nUsage: python extractors/rapid_pipeline.py <csv_path> [output.json]")
except ImportError as e:
    print(f"[ERROR] Import error: {e}")
except Exception as e:
    print(f"[ERROR] Error: {e}")
