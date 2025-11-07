#!/usr/bin/env python3
"""
Report generation module for Specimin evaluation framework.
Aggregates test results and artifact scores into structured reports.
"""

import sys
import json
from pathlib import Path
from datetime import datetime


def load_test_results(run_dir):
    """
    Load all test results from the run directory.

    Args:
        run_dir (str): Directory containing test case subdirectories

    Returns:
        list: List of test result dicts
    """
    run_dir = Path(run_dir)
    results = []

    # Iterate through test case directories
    for test_case_dir in run_dir.iterdir():
        if not test_case_dir.is_dir():
            continue

        results_file = test_case_dir / "results.json"
        if results_file.exists():
            with open(results_file, 'r') as f:
                results.append(json.load(f))

    return results


def calculate_statistics(results):
    """
    Calculate aggregate statistics from test results.

    Args:
        results (list): List of test result dicts

    Returns:
        dict: Statistics including pass rate, average scores, etc.
    """
    total = len(results)
    passed = sum(1 for r in results if r.get('test_passed', False))
    failed = total - passed

    pass_rate = (passed / total * 100) if total > 0 else 0

    # Calculate average rubric scores
    def avg_score(dimension):
        scores = [r.get('rubric_scores', {}).get('spec', {}).get(dimension, {}).get('score')
                  for r in results]
        scores = [s for s in scores if s is not None]
        return sum(scores) / len(scores) if scores else None

    stats = {
        "total_tests": total,
        "passed": passed,
        "failed": failed,
        "pass_rate": round(pass_rate, 2),
        "average_scores": {
            "spec": {
                "completeness": avg_score('Completeness'),
                "clarity": avg_score('Clarity'),
                "testability": avg_score('Testability')
            }
        }
    }

    return stats


def generate_json_report(run_dir):
    """
    Generate JSON report from test results.

    Args:
        run_dir (str): Directory containing test results

    Returns:
        dict: Complete report data
    """
    run_dir = Path(run_dir)
    results = load_test_results(run_dir)
    stats = calculate_statistics(results)

    report = {
        "timestamp": datetime.now().isoformat(),
        "run_directory": str(run_dir),
        "statistics": stats,
        "test_results": results
    }

    return report


def generate_markdown_report(report):
    """
    Generate formatted markdown report from report data.

    Args:
        report (dict): Report data from generate_json_report

    Returns:
        str: Formatted markdown report
    """
    stats = report['statistics']

    md = f"""# Specimin Evaluation Report

**Date:** {report['timestamp']}
**Run Directory:** {report['run_directory']}

---

## Summary

- **Total Tests:** {stats['total_tests']}
- **Passed:** {stats['passed']} ✓
- **Failed:** {stats['failed']} ✗
- **Pass Rate:** {stats['pass_rate']}%

"""

    # Add pass/fail indicator
    if stats['pass_rate'] >= 80:
        md += "**Status:** ✅ PASSING (≥80% threshold)\n\n"
    else:
        md += f"**Status:** ❌ FAILING (<80% threshold, {80 - stats['pass_rate']:.1f}% below)\n\n"

    md += "---\n\n## Test Results\n\n"

    # List each test case
    for result in report['test_results']:
        test_id = result.get('test_id', 'unknown')
        test_name = result.get('test_name', test_id)
        passed = result.get('test_passed', False)
        status = "✓ PASS" if passed else "✗ FAIL"

        md += f"### {test_name} ({test_id})\n\n"
        md += f"**Status:** {status}\n\n"

        if not passed:
            error = result.get('test_error', {})
            md += f"**Error Type:** {error.get('error_type', 'unknown')}\n"
            md += f"**Error:** {error.get('error_message', 'No details')}\n\n"

        # Add rubric scores if available
        rubrics = result.get('rubric_scores', {})
        if rubrics:
            md += "**Artifact Scores:**\n\n"
            for artifact_type, scores in rubrics.items():
                md += f"- **{artifact_type.capitalize()}:**\n"
                for dimension, data in scores.items():
                    score = data.get('score', 'N/A')
                    md += f"  - {dimension}: {score}/5\n"
            md += "\n"

        md += "---\n\n"

    # Add average scores summary
    md += "## Average Artifact Quality Scores\n\n"
    avg_scores = stats['average_scores']
    for artifact_type, dimensions in avg_scores.items():
        md += f"### {artifact_type.capitalize()}\n\n"
        for dimension, score in dimensions.items():
            if score is not None:
                md += f"- **{dimension.capitalize()}:** {score:.2f}/5\n"
        md += "\n"

    return md


def save_reports(run_dir, json_report, md_report):
    """
    Save JSON and markdown reports to run directory.

    Args:
        run_dir (str): Directory to save reports
        json_report (dict): JSON report data
        md_report (str): Markdown report content
    """
    run_dir = Path(run_dir)

    # Save JSON report
    json_file = run_dir / "report.json"
    with open(json_file, 'w') as f:
        json.dump(json_report, f, indent=2)

    # Save markdown report
    md_file = run_dir / "report.md"
    with open(md_file, 'w') as f:
        f.write(md_report)


def main():
    """Main entry point when run as script."""
    if len(sys.argv) != 2:
        print("Usage: reporter.py <run_directory>", file=sys.stderr)
        sys.exit(1)

    run_dir = sys.argv[1]

    try:
        json_report = generate_json_report(run_dir)
        md_report = generate_markdown_report(json_report)
        save_reports(run_dir, json_report, md_report)

        print(f"Reports generated:")
        print(f"  - {run_dir}/report.json")
        print(f"  - {run_dir}/report.md")

    except Exception as e:
        print(f"Error generating report: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
