#!/bin/bash
# save-review.sh - Saves PR review to feature directory
# Usage: save-review.sh <branch_name> <review_file_path>

set -e

BRANCH_NAME="$1"
REVIEW_FILE_PATH="$2"

if [ -z "$BRANCH_NAME" ] || [ -z "$REVIEW_FILE_PATH" ]; then
  echo "Error: Missing required arguments"
  echo "Usage: save-review.sh <branch_name> <review_file_path>"
  exit 1
fi

# Verify feature directory exists
FEATURE_DIR=".specimin/plans/$BRANCH_NAME"
if [ ! -d "$FEATURE_DIR" ]; then
  echo "Error: Feature directory not found: $FEATURE_DIR"
  echo "This PR was not created through the spec/plan/implement flow."
  exit 1
fi

# Verify review file exists
if [ ! -f "$REVIEW_FILE_PATH" ]; then
  echo "Error: Review file not found: $REVIEW_FILE_PATH"
  exit 1
fi

# Create reviews directory if it doesn't exist
REVIEWS_DIR="$FEATURE_DIR/reviews"
mkdir -p "$REVIEWS_DIR"

# Find the next review number
NEXT_NUM=1
if [ -d "$REVIEWS_DIR" ]; then
  # Find highest existing review number
  HIGHEST=$(find "$REVIEWS_DIR" -name "review_*.md" -type f 2>/dev/null | \
    sed 's/.*review_\([0-9]*\)\.md/\1/' | \
    sort -n | \
    tail -1)

  if [ -n "$HIGHEST" ]; then
    NEXT_NUM=$((HIGHEST + 1))
  fi
fi

# Copy review file to reviews directory with incremental number
REVIEW_DEST="$REVIEWS_DIR/review_$NEXT_NUM.md"
cp "$REVIEW_FILE_PATH" "$REVIEW_DEST"

# Output success message with JSON
echo "{\"feature_dir\": \"$FEATURE_DIR\", \"branch_name\": \"$BRANCH_NAME\", \"review_path\": \"$REVIEW_DEST\", \"review_number\": $NEXT_NUM}"
