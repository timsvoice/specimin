#!/bin/bash
# get-pr-diff.sh - Gets the diff for a PR
# Usage: get-pr-diff.sh <branch_name> [main_branch]
# Output: Diff text with stats

set -e

BRANCH_NAME="$1"
MAIN_BRANCH="${2:-main}"

if [ -z "$BRANCH_NAME" ]; then
  echo "Error: Branch name required"
  echo "Usage: get-pr-diff.sh <branch_name> [main_branch]"
  exit 1
fi

# Verify main branch exists, fallback to master
if ! git show-ref --verify --quiet "refs/heads/$MAIN_BRANCH"; then
  if git show-ref --verify --quiet refs/heads/master; then
    MAIN_BRANCH="master"
  else
    echo "Error: Could not find main or master branch"
    exit 1
  fi
fi

# Get diff stats
echo "=== DIFF STATS ==="
git diff "$MAIN_BRANCH...$BRANCH_NAME" --stat

echo ""
echo "=== FILES CHANGED ==="
git diff "$MAIN_BRANCH...$BRANCH_NAME" --name-status

echo ""
echo "=== FULL DIFF ==="
git diff "$MAIN_BRANCH...$BRANCH_NAME"
