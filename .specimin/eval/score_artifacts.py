#!/usr/bin/env python3
"""
Artifact scoring helper for Specimin evaluation framework.
Generates prompts for LLM-as-judge evaluation of specs, plans, and implementations.
"""

import sys
import json
from pathlib import Path


def load_rubric(artifact_type):
    """
    Load the rubric template for the given artifact type.

    Args:
        artifact_type (str): One of 'spec', 'plan', 'implementation'

    Returns:
        str: Rubric template content
    """
    eval_dir = Path(__file__).parent
    rubric_file = eval_dir / "rubrics" / f"{artifact_type}_rubric.md"

    if not rubric_file.exists():
        raise FileNotFoundError(f"Rubric file not found: {rubric_file}")

    with open(rubric_file, 'r') as f:
        return f.read()


def load_artifact(test_dir, artifact_type):
    """
    Load the artifact file from the test directory.

    Args:
        test_dir (str): Directory containing the artifact
        artifact_type (str): One of 'spec', 'plan', 'implementation'

    Returns:
        str: Artifact content
    """
    test_dir = Path(test_dir)
    artifact_file = test_dir / f"{artifact_type}.md"

    if not artifact_file.exists():
        raise FileNotFoundError(f"Artifact file not found: {artifact_file}")

    with open(artifact_file, 'r') as f:
        return f.read()


def generate_evaluation_prompt(test_dir, artifact_type):
    """
    Generate the full evaluation prompt by combining rubric and artifact.

    Args:
        test_dir (str): Directory containing the artifact
        artifact_type (str): One of 'spec', 'plan', 'implementation'

    Returns:
        str: Complete evaluation prompt
    """
    rubric = load_rubric(artifact_type)
    artifact = load_artifact(test_dir, artifact_type)

    # Replace placeholder with actual content
    prompt = rubric.replace(f"{{{artifact_type.upper()}_CONTENT}}", artifact)

    return prompt


def parse_scores(evaluation_response):
    """
    Parse scores from LLM evaluation response.

    Expected format:
    **Dimension1:** [1-5]
    *Justification:* [text]

    Args:
        evaluation_response (str): Raw LLM response

    Returns:
        dict: Parsed scores and justifications
    """
    import re

    scores = {}
    lines = evaluation_response.split('\n')

    current_dimension = None
    for line in lines:
        # Match score line: **Dimension:** [score]
        score_match = re.match(r'\*\*(.+?):\*\*\s*(\d+)', line)
        if score_match:
            dimension = score_match.group(1).strip()
            score = int(score_match.group(2))
            current_dimension = dimension
            scores[dimension] = {"score": score, "justification": ""}

        # Match justification line
        just_match = re.match(r'\*Justification:\*\s*(.+)', line)
        if just_match and current_dimension:
            scores[current_dimension]["justification"] = just_match.group(1).strip()

    return scores


def main():
    """Main entry point when run as script."""
    if len(sys.argv) != 3:
        print("Usage: score_artifacts.py <test_directory> <artifact_type>", file=sys.stderr)
        print("  artifact_type: spec, plan, or implementation", file=sys.stderr)
        sys.exit(1)

    test_dir = sys.argv[1]
    artifact_type = sys.argv[2]

    if artifact_type not in ['spec', 'plan', 'implementation']:
        print(f"Invalid artifact type: {artifact_type}", file=sys.stderr)
        print("  Must be one of: spec, plan, implementation", file=sys.stderr)
        sys.exit(1)

    try:
        prompt = generate_evaluation_prompt(test_dir, artifact_type)
        print(prompt)
    except FileNotFoundError as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print(f"Unexpected error: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
