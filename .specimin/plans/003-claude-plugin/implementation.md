# Implementation Tasks: Convert Specimin to Claude Code Plugin

**Implementation Overview**

This implementation converts the specimin repository from a standalone tool to a distributable Claude Code plugin. Tasks are organized into 4 phases matching the plan: creating plugin structure, adapting commands to use plugin context, cleaning up legacy structure, and preparing for distribution. The approach preserves existing command functionality while enabling cross-project reusability.

---

## **Phase 1: Plugin Structure Setup**

### Task 1.1: Create plugin manifest file
**Context**: Claude Code requires a `plugin.json` manifest to recognize and load plugins with metadata and component paths.
**Acceptance Criteria**:
- File `.claude-plugin/plugin.json` exists with valid JSON structure
- Manifest contains `name`, `version` (1.0.0), `description`, and `author` fields
- `commands` array explicitly lists all 5 command file paths (init, spec, feature.plan, implement, wrap)
**Dependencies**: None

### Task 1.2: Create plugin commands directory and move command files
**Context**: Plugin commands must reside in `.claude-plugin/commands/` per Claude Code plugin specification.
**Acceptance Criteria**:
- Directory `.claude-plugin/commands/` exists
- All 4 command files (cmd.spec.md, cmd.feature.plan.md, cmd.implement.md, cmd.wrap.md) copied to `.claude-plugin/commands/`
- Original files in `.claude/commands/` remain for now (cleanup in Phase 3)
**Dependencies**: Task 1.1

### Task 1.3: Move setup script to plugin root
**Context**: Setup script must be accessible via `${CLAUDE_PLUGIN_ROOT}` but shouldn't include the entire `.specimin/plans/` directory structure.
**Acceptance Criteria**:
- Directory `.specimin/` created at plugin root (parallel to `.claude-plugin/`)
- File `setup.feature.sh` moved from old location to `.specimin/setup.feature.sh` at plugin root
- Script retains execute permissions after move
- Old `.specimin/plans/003-claude-plugin/` directory preserved (contains current feature planning files)
**Dependencies**: Task 1.1

---

## **Phase 2: Command Adaptation**

### Task 2.1: Update cmd.spec.md to use plugin script path
**Context**: Spec command must invoke setup script using plugin context variable instead of relative path.
**Acceptance Criteria**:
- All references to `./.specimin/setup.feature.sh` changed to `bash ${CLAUDE_PLUGIN_ROOT}/.specimin/setup.feature.sh`
- Command functionality unchanged (still generates spec files)
- Command includes check: if `.specimin/plans/` doesn't exist in user project, fail with "Please run /init first"
**Dependencies**: Phase 1 complete

### Task 2.2: Update cmd.feature.plan.md to use plugin script path and add init check
**Context**: Feature plan command must reference plugin script path and verify initialization.
**Acceptance Criteria**:
- Script references updated to `bash ${CLAUDE_PLUGIN_ROOT}/.specimin/setup.feature.sh`
- Includes initialization check: fail gracefully if `.specimin/plans/{branch}/` missing
- Command reads spec.md from user's project `.specimin/plans/{branch}/`, not plugin directory
**Dependencies**: Phase 1 complete

### Task 2.3: Update cmd.implement.md to add initialization check
**Context**: Implement command reads plan.md and spec.md from user project, must verify structure exists.
**Acceptance Criteria**:
- Includes check for `.specimin/plans/{branch}/plan.md` existence
- Fails with helpful message "Please run /init and /feature.plan first" if files missing
- No script path updates needed (this command doesn't invoke setup script directly)
**Dependencies**: Phase 1 complete

### Task 2.4: Update cmd.wrap.md to add initialization check
**Context**: Wrap command reads feature files from user project, must verify structure exists.
**Acceptance Criteria**:
- Includes check for `.specimin/plans/{branch}/` directory existence
- Fails with message "Please run /init first" if directory missing
- Command continues to read spec.md, plan.md, implementation.md from user's `.specimin/plans/{branch}/`
**Dependencies**: Phase 1 complete

### Task 2.5: Create init.md command for project initialization
**Context**: New command to explicitly bootstrap `.specimin/` structure in user projects.
**Acceptance Criteria**:
- File `.claude-plugin/commands/init.md` created with command description
- Command checks if current directory is a git repository (fail if not)
- Command creates `.specimin/plans/` directory structure in user's working directory
- Command displays success message: "Specimin initialized. You can now use /spec, /feature.plan, /implement, and /wrap commands."
- Command is idempotent (safe to run multiple times, doesn't error if `.specimin/` exists)
**Dependencies**: Phase 1 complete

---

## **Phase 3: Backward Compatibility Cleanup**

### Task 3.1: Remove legacy .claude directory
**Context**: Repository converts to pure plugin structure, `.claude/` directory no longer needed.
**Acceptance Criteria**:
- Directory `.claude/` and all contents deleted
- Git tracks the deletion
- No remaining references to `.claude/` paths in any files
**Dependencies**: Phase 2 complete

### Task 3.2: Test plugin installation locally
**Context**: Verify plugin works when installed via Claude Code before finalizing.
**Acceptance Criteria**:
- Plugin added to Claude Code via local path configuration
- All 5 commands (`/init`, `/spec`, `/feature.plan`, `/implement`, `/wrap`) appear in command palette
- Test in fresh directory: `/init` creates structure, `/spec` generates spec file
- Commands correctly reference `${CLAUDE_PLUGIN_ROOT}` and find setup script
**Dependencies**: Task 3.1

### Task 3.3: Update plugin.json with corrected command paths
**Context**: After testing, ensure all command references are accurate and plugin.json reflects final structure.
**Acceptance Criteria**:
- Command paths in plugin.json match actual file locations
- Manifest includes complete metadata (homepage, repository URL if applicable)
- JSON validates against Claude Code plugin schema
**Dependencies**: Task 3.2

---

## **Phase 4: Distribution Preparation**

### Task 4.1: Create README documentation for plugin
**Context**: Users need installation and usage instructions for both distribution channels.
**Acceptance Criteria**:
- File `README.md` created at repository root
- Documents installation via git URL: instructions for adding plugin to Claude Code
- Documents expected marketplace installation process
- Includes quick start: run `/init`, then `/spec` workflow example
- Lists all 5 commands with brief descriptions
**Dependencies**: Phase 3 complete

### Task 4.2: Create git tag for v1.0.0 release
**Context**: Establishes first official plugin version for distribution tracking.
**Acceptance Criteria**:
- Git tag `v1.0.0` created on current commit
- Tag annotation includes release notes summarizing plugin functionality
- Tag pushed to remote repository (if applicable)
**Dependencies**: Task 4.1

### Task 4.3: Test git-based plugin installation
**Context**: Verify users can install plugin directly from git repository URL.
**Acceptance Criteria**:
- Plugin successfully installs via git URL in clean Claude Code environment
- All commands functional after git-based installation
- `${CLAUDE_PLUGIN_ROOT}` correctly resolves to cloned plugin location
- Setup script accessible and executable
**Dependencies**: Task 4.2

---

## **Cross-Phase Dependencies**

- Phase 2 requires Phase 1 complete (commands need plugin structure to exist)
- Phase 3 requires Phase 2 complete (must verify adapted commands work before removing legacy)
- Phase 4 requires Phase 3 complete (documentation describes final structure, not intermediate)

---

## **Integration Notes**

Commands create `.specimin/plans/` in the user's working directory, not in the plugin directory. The plugin itself contains only the setup script (`.specimin/setup.feature.sh`) and command definitions (`.claude-plugin/commands/`). Each user project maintains independent feature planning state. The setup script remains unchanged functionally but is invoked via `${CLAUDE_PLUGIN_ROOT}` environment variable. Git operations (branch creation, commits, PR generation) continue working as-is since they operate on the user's repository.
