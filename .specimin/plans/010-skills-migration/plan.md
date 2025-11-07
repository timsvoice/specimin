# Implementation Plan: Refactor Specimin Plugin to Use Agent Skills

**Technical Context**
Existing: Claude Code plugin with slash commands in `.claude-plugin/commands/` | Detected: 6 command files (init, spec, plan, task, wrap, refactor), supporting shell scripts in `.specimin/`, plugin.json configuration | Decisions: Skills in `.claude-plugin/skills/` with explicit plugin.json declaration, prefixed naming (specimin-*), permissive tool permissions, gradual deprecation of old commands

**Decision Exploration**

### Decision 1: Skills Directory Location
**Options**:
- A: `.claude-plugin/skills/` - Mirrors commands structure, keeps plugin self-contained
- B: `.claude/skills/` at root - Matches project skills but not bundled
- C: Both with symlink - Complex and confusing

**Selected**: A (`.claude-plugin/skills/`)
**Rationale**: Keeps all plugin assets in one location for marketplace distribution, mirrors existing commands/ structure, self-contained and portable

### Decision 2: Plugin Configuration
**Options**:
- A: Add "skills" array to plugin.json - Explicit declaration
- B: Convention-based discovery - Automatic but unverified
- C: Check documentation - Delays work

**Selected**: A (Add "skills" array)
**Rationale**: Explicit is better than implicit, mirrors commands array pattern, provides clarity about what's bundled

### Decision 3: Skill Naming
**Options**:
- A: Simple names (spec, plan) - Concise but generic
- B: Prefixed names (specimin-spec, specimin-plan) - Unique and clear
- C: Descriptive names (feature-specification) - Self-documenting but verbose

**Selected**: B (Prefixed names)
**Rationale**: Prevents naming conflicts with other plugins, maintains clear ownership while staying concise, follows common plugin naming patterns

### Decision 4: Tool Permissions Strategy
**Options**:
- A: Conservative minimal - Safer but might break functionality
- B: Permissive comprehensive - Ensures functionality
- C: Iterative minimal-first - Balanced but requires testing

**Selected**: B (Permissive)
**Rationale**: Priority is maintaining all existing functionality without regression, each skill has clear scope making permissive acceptable, easier to restrict later than debug missing permissions

### Decision 5: Command Deprecation Approach
**Options**:
- A: Remove immediately - Clean but risky
- B: Deprecate gradually (.deprecated suffix) - Safe fallback
- C: Keep both documented - User confusion

**Selected**: B (Gradual deprecation)
**Rationale**: Provides safety net during testing, allows rollback if issues found, clearer than keeping both active, minimal directory clutter with .deprecated suffix

**Solution Architecture**

The migration follows a structural transformation pattern: each slash command becomes a skill with identical workflow logic but different invocation mechanism. Skills will be stored in `.claude-plugin/skills/` with each skill in its own subdirectory containing a SKILL.md file. The plugin.json manifest gains a "skills" array declaring the four new skills.

Each skill preserves its original command's multi-stage workflow (analyze, clarify, draft, iterate, finalize) but adapts the description to indicate explicit user intent triggering. Tool permissions are audited by analyzing each command's current tool usage: spec uses Write/Bash/AskUserQuestion, plan adds Read/Grep/Glob for codebase analysis, task uses Read/Write/Bash for file generation, wrap uses Read/Bash/AskUserQuestion for git operations.

Skills reference supporting shell scripts via `${CLAUDE_PLUGIN_ROOT}/.specimin/` paths, maintaining the existing script infrastructure without duplication. Old command files are renamed with .deprecated suffix rather than deleted, providing fallback mechanism during transition period.

The plugin remains backward compatible for init and refactor commands which stay as slash commands. Users transition from typing `/specimin:cmd.spec` to saying "create a specification", leveraging Claude's autonomous skill discovery based on intent-focused descriptions.

**Technology Decisions**
- Skills location: `.claude-plugin/skills/{skill-name}/SKILL.md`
- Skill naming: `specimin-spec`, `specimin-plan`, `specimin-task`, `specimin-wrap`
- Plugin manifest: Add `"skills": [...]` array to plugin.json
- Script references: `${CLAUDE_PLUGIN_ROOT}/.specimin/*.sh` (unchanged)
- Deprecation method: Rename to `.md.deprecated` suffix
- Tool permissions: Comprehensive per-skill audit (permissive approach)

**Component Modifications**
1. plugin.json (.claude-plugin/): Add "skills" array with paths to four skill directories
2. cmd.spec.md (.claude-plugin/commands/): Rename to cmd.spec.md.deprecated
3. cmd.plan.md (.claude-plugin/commands/): Rename to cmd.plan.md.deprecated  
4. cmd.task.md (.claude-plugin/commands/): Rename to cmd.task.md.deprecated
5. cmd.wrap.md (.claude-plugin/commands/): Rename to cmd.wrap.md.deprecated

**New Components**
1. specimin-spec skill (.claude-plugin/skills/specimin-spec/): Specification generation workflow
2. specimin-plan skill (.claude-plugin/skills/specimin-plan/): Implementation planning workflow
3. specimin-task skill (.claude-plugin/skills/specimin-task/): Task breakdown workflow
4. specimin-wrap skill (.claude-plugin/skills/specimin-wrap/): Feature wrap-up and PR creation workflow

**Task Sequence**

**Phase 1: Foundation Setup**
1. Create skills directory structure
2. Audit tool requirements for each command
3. Create SKILL.md template following Claude Code best practices
Dependencies: None

**Phase 2: Skill Migration (Core Workflows)**
4. Create specimin-spec skill with permissive tool list
5. Create specimin-plan skill with permissive tool list
6. Create specimin-task skill with permissive tool list
7. Create specimin-wrap skill with permissive tool list
Dependencies: Phase 1 complete

**Phase 3: Plugin Configuration**
8. Update plugin.json with skills array
9. Deprecate old command files (.md.deprecated suffix)
Dependencies: Phase 2 complete

**Phase 4: Verification**
10. Test spec skill workflow (create specification)
11. Test plan skill workflow (generate plan)
12. Test task skill workflow (break down tasks)
13. Test wrap skill workflow (squash and PR)
14. Verify init and refactor commands still work
Dependencies: Phase 3 complete

**Integration Points**
- Shell scripts (.specimin/): Skills call save-spec.sh, save-plan.sh via Bash tool using `${CLAUDE_PLUGIN_ROOT}` environment variable
- Git: Skills use Bash tool for git commands (branch detection, commit operations)
- GitHub CLI: wrap skill uses gh CLI via Bash for PR creation
- File system: Skills write to .specimin/plans/{branch}/ directories, read spec/plan/implementation files
- Plugin system: Claude Code discovers skills via plugin.json "skills" array, loads SKILL.md files on demand

**Testing Strategy**
Unit: Verify each SKILL.md has valid YAML frontmatter (name, description, allowed-tools) | Integration: Test each skill end-to-end (spec creation → plan generation → task breakdown → wrap PR) on test feature branch | E2E: Complete workflow test from "/specimin:init" through skill-based spec/plan/task/wrap to merged PR | Edge: Test missing .specimin/ directory (error message), test without git repo (graceful failure), test script path resolution with CLAUDE_PLUGIN_ROOT, test deprecated commands still accessible if needed

**Risks & Mitigation**
- **Risk**: Skills directory not auto-discovered by Claude Code
  - Mitigation: Explicit "skills" array in plugin.json, verify with test installation
  
- **Risk**: `${CLAUDE_PLUGIN_ROOT}` not available in skill context
  - Mitigation: Test early in Phase 4, fallback to relative paths if needed
  
- **Risk**: Tool restrictions break existing functionality
  - Mitigation: Permissive tool lists audited from current commands, comprehensive testing in Phase 4
  
- **Risk**: Skill descriptions don't trigger on user intent
  - Mitigation: Clear "Use only when user explicitly requests" language in descriptions, test with various phrasings
  
- **Risk**: Users attempt old slash commands and get confused
  - Mitigation: Keep .deprecated files as fallback, consider adding deprecation notice in descriptions
  
- **Risk**: Skills not bundled correctly with plugin distribution
  - Mitigation: Verify plugin.json includes skills in manifest, test via marketplace installation
