#!/usr/bin/env python3
"""
This script runs all the examples in this repository.

Author: Muhammad Mohsin Khan
Date: October 16, 2026
License: MIT
Repository: https://github.com/mkhan138/calculix-fea-examples
"""

from pathlib import Path
import subprocess
import sys

# Root directory: the directory containing this script
ROOT_DIR = Path(__file__).resolve().parent

for physical_domain in sorted(ROOT_DIR.iterdir()):
    if not physical_domain.is_dir() or physical_domain.name.startswith("."):
        continue

    print(f"\n{'=' * 60}")
    print(f"Physical domain: {physical_domain.name}")
    print(f"{'=' * 60}")

    # Iterate through analysis type folders
    for analysis_type in sorted(physical_domain.iterdir()):
        if not analysis_type.is_dir() or analysis_type.name.startswith("."):
            continue

        print(f"\nAnalysis type: {analysis_type.name}")

        # Iterate through example folders
        for example in sorted(analysis_type.iterdir()):
            if not example.is_dir() or example.name.startswith("."):
                continue

            run_file = example / "run.py"

            if not run_file.is_file():
                print(f"SKIP: No run.py in {example.relative_to(ROOT_DIR)}")
                continue

            print(f"\nRunning: {example.relative_to(ROOT_DIR)}")

            try:
                # Run from the example directory
                subprocess.run(
                    [sys.executable, str(run_file)],
                    cwd=example,
                    check=True,
                )
                print(f"SUCCESS: {example.name}")

            except subprocess.CalledProcessError as error:
                print(f"FAILED: {example.name} (exit code {error.returncode})")

print("\nAll examples processed.")