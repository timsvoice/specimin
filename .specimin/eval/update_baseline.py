#!/usr/bin/env python3
"""
Baseline management for Specimin evaluation framework.
Appends evaluation results to historical baseline and detects regressions.
"""

import sys
import json
from pathlib import Path
from datetime import datetime


def load_baselines():
    """
    Load existing baseline data or create empty baseline.

    Returns:
        list: List of baseline entries
    """
    eval_dir = Path(__file__).parent
    baseline_file = eval_dir / "baselines.json"

    if not baseline_file.exists():
        return []

    try:
        with open(baseline_file, 'r') as f:
            return json.load(f)
    except json.JSONDecodeError:
        print("Warning: Corrupted baselines.json, starting fresh", file=sys.stderr)
        return []


def save_baselines(baselines):
    """
    Save baselines to file.

    Args:
        baselines (list): List of baseline entries
    """
    eval_dir = Path(__file__).parent
    baseline_file = eval_dir / "baselines.json"

    with open(baseline_file, 'w') as f:
        json.dump(baselines, f, indent=2)


def create_baseline_entry(report):
    """
    Create a baseline entry from a report.

    Args:
        report (dict): Report data

    Returns:
        dict: Baseline entry
    """
    stats = report['statistics']

    entry = {
        "timestamp": report['timestamp'],
        "run_directory": report['run_directory'],
        "total_tests": stats['total_tests'],
        "passed": stats['passed'],
        "failed": stats['failed'],
        "pass_rate": stats['pass_rate'],
        "average_scores": stats['average_scores']
    }

    return entry


def detect_regression(current, previous):
    """
    Detect if current run represents a regression from previous.

    Args:
        current (dict): Current baseline entry
        previous (dict): Previous baseline entry

    Returns:
        dict: Regression analysis with keys:
            - has_regression (bool)
            - pass_rate_change (float)
            - message (str)
    """
    if not previous:
        return {
            "has_regression": False,
            "pass_rate_change": 0.0,
            "message": "First baseline - no comparison available"
        }

    current_rate = current['pass_rate']
    previous_rate = previous['pass_rate']
    change = current_rate - previous_rate

    # Regression if pass rate drops by more than 5%
    has_regression = change < -5.0

    if has_regression:
        message = f"⚠️  REGRESSION DETECTED: Pass rate dropped {abs(change):.1f}% ({previous_rate}% → {current_rate}%)"
    elif change > 0:
        message = f"✅ Improvement: Pass rate increased {change:.1f}% ({previous_rate}% → {current_rate}%)"
    else:
        message = f"Stable: Pass rate changed {change:.1f}% ({previous_rate}% → {current_rate}%)"

    return {
        "has_regression": has_regression,
        "pass_rate_change": change,
        "message": message
    }


def update_baseline_with_report(report_path):
    """
    Update baseline file with new report and check for regressions.

    Args:
        report_path (str): Path to report.json file

    Returns:
        dict: Regression analysis result
    """
    # Load report
    with open(report_path, 'r') as f:
        report = json.load(f)

    # Load existing baselines
    baselines = load_baselines()

    # Get previous baseline (most recent)
    previous = baselines[-1] if baselines else None

    # Create new baseline entry
    current = create_baseline_entry(report)

    # Detect regression
    regression_analysis = detect_regression(current, previous)

    # Append to baselines
    baselines.append(current)

    # Save updated baselines
    save_baselines(baselines)

    return regression_analysis


def main():
    """Main entry point when run as script."""
    if len(sys.argv) != 2:
        print("Usage: update_baseline.py <report_json_path>", file=sys.stderr)
        sys.exit(1)

    report_path = sys.argv[1]

    if not Path(report_path).exists():
        print(f"Error: Report file not found: {report_path}", file=sys.stderr)
        sys.exit(1)

    try:
        regression = update_baseline_with_report(report_path)

        # Print regression analysis
        print(json.dumps(regression, indent=2))

    except Exception as e:
        print(f"Error updating baseline: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
