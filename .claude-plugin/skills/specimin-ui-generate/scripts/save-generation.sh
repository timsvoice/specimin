#!/bin/bash
# save-generation.sh - Saves generated UI code and commits to feature branch
# Usage: save-generation.sh <branch_name>

set -e

BRANCH_NAME="$1"

if [ -z "$BRANCH_NAME" ]; then
  # Try to get current branch if not provided
  BRANCH_NAME=$(git branch --show-current)
fi

if [ -z "$BRANCH_NAME" ]; then
  echo "Error: Could not determine branch name"
  echo "Usage: save-generation.sh <branch_name>"
  exit 1
fi

# Verify we're in a git repository
if ! git rev-parse --git-dir > /dev/null 2>&1; then
  echo "Error: Not in a git repository"
  exit 1
fi

# Verify branch exists
if ! git rev-parse --verify "$BRANCH_NAME" > /dev/null 2>&1; then
  echo "Error: Branch '$BRANCH_NAME' does not exist"
  exit 1
fi

# Verify we're on the correct branch
CURRENT_BRANCH=$(git branch --show-current)
if [ "$CURRENT_BRANCH" != "$BRANCH_NAME" ]; then
  echo "Error: Not on branch '$BRANCH_NAME' (currently on '$CURRENT_BRANCH')"
  exit 1
fi

FEATURE_DIR=".specimin/ui/$BRANCH_NAME"

# Verify feature directory exists
if [ ! -d "$FEATURE_DIR" ]; then
  echo "Error: Feature directory not found: $FEATURE_DIR"
  echo "Run specimin:ui-understand first"
  exit 1
fi

# Verify structure.md exists
STRUCTURE_PATH="$FEATURE_DIR/structure.md"
if [ ! -f "$STRUCTURE_PATH" ]; then
  echo "Error: structure.md not found at $STRUCTURE_PATH"
  echo "Run specimin:ui-structure first"
  exit 1
fi

# Check if generation report exists in /tmp
REPORT_TEMP="/tmp/ui-generation-report.md"
if [ ! -f "$REPORT_TEMP" ]; then
  echo "Error: Generation report not found at $REPORT_TEMP"
  echo "The skill should write the generation report to /tmp/ui-generation-report.md"
  exit 1
fi

# Copy generation report to feature directory
REPORT_DEST="$FEATURE_DIR/generation-report.md"
cp "$REPORT_TEMP" "$REPORT_DEST"

# Add all changes (generated code files + report)
git add -A

# Check if there are changes to commit
if git diff --cached --quiet; then
  echo "Warning: No changes to commit (generated files may already be staged)"
else
  # Commit with descriptive message
  git commit -m "Generate UI implementation

- Generated code files from structure specification
- Completed validation loops (compilation, structure, accessibility)
- See generation-report.md for details"
fi

# Output success message with JSON
echo "{\"feature_dir\": \"$FEATURE_DIR\", \"branch_name\": \"$BRANCH_NAME\", \"report_path\": \"$REPORT_DEST\"}"
