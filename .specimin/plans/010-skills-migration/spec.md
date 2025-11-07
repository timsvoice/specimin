## Refactor Specimin Plugin to Use Agent Skills

### Objective
Convert core workflow commands (spec, plan, task, wrap) from slash commands to Agent Skills bundled with the plugin, while preserving init and refactor as slash commands.

### Context
The Specimin plugin currently uses slash commands for its feature development workflow. Agent Skills provide better integration with Claude Code by:
- Being bundled with plugins and automatically available when installed
- Having explicit tool restrictions for safety and clarity
- Supporting clearer invocation patterns based on explicit user intent
- Reducing the need for slash command syntax

This migration will make the plugin more aligned with Claude Code's skill-based architecture while maintaining backward compatibility for init and refactor commands.

### Assumptions
- Claude Code plugin format supports bundling skills in a `skills/` directory
- Skills bundled with plugins are automatically discovered when the plugin is installed
- The `allowed-tools` frontmatter field works correctly in Claude Code for restricting tool access
- Users will adapt to requesting skills explicitly ("create a spec") rather than using slash commands
- Supporting shell scripts (`.specimin/*.sh`) remain accessible to skills via `${CLAUDE_PLUGIN_ROOT}`
- The current workflow logic and prompts are sound and don't require rewriting

### Constraints
- Must maintain all existing functionality for spec, plan, task, and wrap workflows
- Must preserve the workflow sequence integrity (spec → plan → task → wrap)
- Tool restrictions must be carefully audited for each skill to ensure functionality isn't broken
- Init and refactor must remain as slash commands (not converted)
- Skills must have descriptions that clearly indicate when to use them based on explicit user intent
- Must follow Agent Skills best practices from Claude Code documentation
- SKILL.md files must have valid YAML frontmatter with name, description, and allowed-tools fields

### Acceptance Criteria
- Four new SKILL.md files created in plugin's `skills/` directory (spec, plan, task, wrap)
- Each skill has an appropriate `allowed-tools` list covering all tools needed for its workflow
- Each skill's description clearly states it should be used only when user explicitly requests that action
- Slash command files for converted skills (cmd.spec.md, cmd.plan.md, cmd.task.md, cmd.wrap.md) are removed
- Init and refactor remain as slash commands in `.claude-plugin/commands/`
- Skills reference shell scripts correctly using `${CLAUDE_PLUGIN_ROOT}` variable
- All workflow functionality verified working (spec creation, plan generation, task breakdown, PR wrap-up)
- No regression in existing behavior

### User Scenarios

**Scenario 1: Create Specification**
1. User says: "I need to create a specification for user authentication"
2. Claude recognizes explicit intent and invokes the spec skill
3. Skill prompts for requirements and generates spec
4. Spec saved to `.specimin/plans/{branch}/spec.md`

**Scenario 2: Generate Plan**
1. User says: "Generate an implementation plan for this feature"
2. Claude invokes the plan skill
3. Skill reads existing spec, asks clarifying questions, generates plan
4. Plan saved to `.specimin/plans/{branch}/plan.md`

**Scenario 3: Break Down Tasks**
1. User says: "Break down the plan into implementation tasks"
2. Claude invokes the task skill
3. Skill reads spec and plan, generates atomic tasks with TDD cycles
4. Tasks saved to `.specimin/plans/{branch}/implementation.md`
5. Phase files and manifest automatically generated

**Scenario 4: Wrap Up Feature**
1. User says: "Wrap this feature up and create a PR"
2. Claude invokes the wrap skill
3. Skill squashes commits, generates PR description, creates pull request
4. User receives PR URL

**Scenario 5: Initialize Project (Unchanged)**
1. User types: `/specimin:init`
2. Slash command executes, creates `.specimin/plans/` directory
3. Confirmation message displayed

**Scenario 6: Refactor Code (Unchanged)**
1. User types: `/specimin:cmd.refactor`
2. Slash command executes refactoring workflow
3. Code refactored with test verification

### Edge Cases
- User attempts old slash commands (`/specimin:cmd.spec`) → Command not found (graceful failure)
- Skill invoked before project initialization → Skill checks for `.specimin/` and provides helpful error message
- Tool restriction prevents needed operation → Skill fails with clear error (must audit tools carefully to prevent this)
- User says ambiguous phrase like "help me with this feature" → Claude asks for clarification rather than auto-invoking skill
- Multiple skills could apply → Claude asks user which action they want (spec vs plan vs task)
- Supporting scripts not accessible → Skills fail gracefully with error pointing to plugin installation issue

### Dependencies
- Claude Code plugin format must support `skills/` directory for bundled skills
- `${CLAUDE_PLUGIN_ROOT}` environment variable must be available to skills
- Shell scripts in `.specimin/` must remain accessible and functional
- Git must be installed and repository initialized for workflow to function
- `gh` CLI must be installed for wrap skill (PR creation)
- `jq` must be available for JSON parsing in shell scripts

### Out of Scope
- Modifying the underlying workflow logic or prompts beyond necessary adaptations
- Changing or rewriting the supporting shell scripts (save-spec.sh, save-plan.sh, etc.)
- Adding new features or capabilities beyond the migration
- Modifying the `.specimin/` directory structure or conventions
- Converting init or refactor commands to skills
- Creating tests or evaluation framework for the migrated skills
- Updating external documentation or README files (assume plugin metadata handles this)
