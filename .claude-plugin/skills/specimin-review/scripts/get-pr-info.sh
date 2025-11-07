#!/bin/bash
# get-pr-info.sh - Fetches PR information for the current branch
# Usage: get-pr-info.sh [branch_name]
# Output: JSON with PR details

set -e

BRANCH_NAME="${1:-$(git rev-parse --abbrev-ref HEAD)}"

# Check if gh CLI is installed
if ! command -v gh &> /dev/null; then
  echo '{"error": "GitHub CLI (gh) not installed. Install: https://cli.github.com/"}' | jq
  exit 1
fi

# Check if authenticated
if ! gh auth status &> /dev/null; then
  echo '{"error": "Not authenticated with GitHub CLI. Run: gh auth login"}' | jq
  exit 1
fi

# Get PR for current branch
PR_DATA=$(gh pr view "$BRANCH_NAME" --json number,title,body,url,state,isDraft,additions,deletions,changedFiles 2>/dev/null || echo '{"error": "No PR found for branch: '"$BRANCH_NAME"'"}')

# Check if error in PR_DATA
if echo "$PR_DATA" | jq -e '.error' &> /dev/null; then
  echo "$PR_DATA"
  exit 1
fi

# Add branch name to output
echo "$PR_DATA" | jq --arg branch "$BRANCH_NAME" '. + {branch: $branch}'
