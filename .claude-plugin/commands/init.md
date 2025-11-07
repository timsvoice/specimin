---
description: Initialize Specimin in the current project by creating the required directory structure.
---

# Specimin Initialization Command

## Purpose

This command bootstraps the Specimin directory structure in your project, enabling the use of `/spec`, `/feature.plan`, `/implement`, and `/wrap` commands for feature development workflow.

## Workflow

### Step 1: Validate Git Repository

First, verify the current directory is a git repository:

```bash
git rev-parse --git-dir
```

If the command fails (exit code != 0), display error and exit:
```
Error: Current directory is not a git repository.
Specimin requires git for version control and branch management.

Initialize git first:
  git init
```

### Step 2: Check Existing Installation

Check if Specimin is already initialized:

```bash
if [ -d ".specimin/plans/" ]; then
  echo "Specimin is already initialized in this project."
  exit 0
fi
```

### Step 3: Create Directory Structure

Create the required directory structure:

```bash
mkdir -p .specimin/plans
```

### Step 4: Confirm Success

Display success message:
```
✓ Specimin initialized successfully!

Created directory structure:
  .specimin/plans/

You can now use:
  /spec         - Create feature specifications
  /feature.plan - Generate implementation plans
  /implement    - Break down plans into tasks
  /wrap         - Squash commits and create PR

Get started:
  Run /spec to create your first feature specification
```

## Notes

- This command is **idempotent** - safe to run multiple times
- Creates only the `.specimin/plans/` directory structure
- Does not modify any existing files or git configuration
- The `.specimin/plans/` directory will contain feature-specific subdirectories (one per branch)
- Each feature branch will have its own directory at `.specimin/plans/{branch-name}/`

## Error Handling

**Not a git repository**: Must be run in a directory with `.git/` folder

**Permission denied**: Ensure write permissions in the current directory

## Future Enhancements

Consider adding:
- `.gitignore` entry for temporary plan files (if needed)
- Configuration file (`.specimin/config.json`) for user preferences
- Template files for spec/plan structure
