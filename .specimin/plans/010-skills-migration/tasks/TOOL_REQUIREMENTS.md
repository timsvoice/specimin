# Tool Requirements Audit

## cmd.spec.md (specimin-spec)
**Required Tools:**
- `run_terminal_cmd` - Execute bash script (save-spec.sh)
- `write` - Write spec draft to temporary file
- `read_file` - Read existing files if needed

**Scripts Used:**
- `${CLAUDE_PLUGIN_ROOT}/.specimin/save-spec.sh`
- `${CLAUDE_PLUGIN_ROOT}/.specimin/setup.feature.sh` (called by save-spec.sh)

## cmd.plan.md (specimin-plan)
**Required Tools:**
- `run_terminal_cmd` - Execute bash script (save-plan.sh)
- `write` - Write plan draft to temporary file
- `read_file` - Read spec.md and analyze codebase

**Scripts Used:**
- `${CLAUDE_PLUGIN_ROOT}/.specimin/save-plan.sh`

## cmd.task.md (specimin-task)
**Required Tools:**
- `run_terminal_cmd` - Execute git commands (git rev-parse)
- `write` - Write implementation.md and phase files
- `read_file` - Read plan.md and spec.md

**Scripts Used:**
- None (pure file operations)

## cmd.wrap.md (specimin-wrap)
**Required Tools:**
- `run_terminal_cmd` - Execute git commands and gh CLI
- `read_file` - Read spec.md, plan.md, implementation.md

**Scripts Used:**
- None (direct git/gh commands)

---

# SKILL.md Structure

## YAML Frontmatter Format

```yaml
---
name: "skill-name"
description: "Clear description of when to use this skill. Only invoke when user explicitly requests [action]."
allowed-tools:
  - tool1
  - tool2
  - tool3
---
```

## Field Requirements

- **name**: Kebab-case identifier (e.g., "specimin-spec")
- **description**: Must clearly state skill should only be used when user explicitly requests the action
- **allowed-tools**: Array of tool names that the skill is permitted to use

## Script References

When referencing scripts, use:
- `${CLAUDE_PLUGIN_ROOT}/.specimin/script.sh` for scripts in .specimin/
- `${CLAUDE_PLUGIN_ROOT}/.claude-plugin/skills/{skill-name}/scripts/script.sh` for skill-specific scripts

