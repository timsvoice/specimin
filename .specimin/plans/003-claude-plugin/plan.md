## **Technical Context**

**Existing**: Standalone repository with `.claude/commands/` (4 slash commands), `.specimin/setup.feature.sh` (bash script), `.specimin/plans/` (feature state storage)

**Detected**: Git repository, bash shell scripting, markdown-based commands, JSON processing (jq), GitHub CLI integration

**Unknowns Resolved**:
- Plugin root via `${CLAUDE_PLUGIN_ROOT}` for script access
- Dual distribution (marketplace stable + git cutting-edge)
- Separate `/init` initialization command
- Pure `.claude-plugin/` structure (no `.claude/` in final)
- Manual versioning with git tags

---

## **Decision Exploration**

### Decision 1: Script Location Strategy

**Options Explored**:
- A: Keep script in plugin with `${CLAUDE_PLUGIN_ROOT}` reference
- B: Copy script to user project on first use
- C: Inline script logic into commands

**Selected**: Option A

**Rationale**: Maintains single source of truth for setup logic, enables centralized updates via plugin versioning, aligns with standard plugin patterns where reusable utilities live in plugin directory. Commands can reference script using environment variable without duplicating logic.

### Decision 2: Distribution Strategy

**Options Explored**:
- A: Claude marketplace only (broad reach, gated)
- B: Git repository as plugin source (immediate, flexible)
- C: Both channels (marketplace + git development)

**Selected**: Option C

**Rationale**: Enables rapid iteration on git main branch while providing stable, versioned releases via marketplace. Users can choose between bleeding-edge (git) or stable (marketplace). Supports both development workflow and production usage.

### Decision 3: Directory Auto-Creation

**Options Explored**:
- A: Each command auto-creates directories (fully automatic)
- B: Setup script handles detection (fail gracefully)
- C: Separate `/init` command (explicit initialization)

**Selected**: Option C

**Rationale**: Provides clear project setup boundary, makes directory creation explicit and intentional, avoids surprise modifications to user's repository. Aligns with "convention over surprise" principle - users understand what's happening to their project structure.

### Decision 4: Repository Structure

**Options Explored**:
- A: Dual structure (`.claude/` + `.claude-plugin/` coexist)
- B: Pure `.claude-plugin/` structure (plugin-only)
- C: Build process generates plugin from dev structure

**Selected**: Option B

**Rationale**: Clean separation eliminates duplicate maintenance, forces authentic "use as plugin" testing during development, simplifies repository structure. Developer experience uses plugin installation workflow, ensuring what's tested matches what's distributed.

### Decision 5: Version Management

**Options Explored**:
- A: Manual versioning + git tags (simple, explicit)
- B: Automated versioning + changelog tooling (professional)
- C: Git SHA versioning (no management)

**Selected**: Option A

**Rationale**: Appropriate for initial release cadence, low tooling overhead, explicit control over version bumps. Manual updates to `plugin.json` version field combined with git tags provide traceability without automation complexity.

---

## **Solution Architecture**

The plugin architecture transforms the current standalone repository into a distributable Claude Code plugin while maintaining the repository as the development source. The core transformation involves restructuring from `.claude/commands/` to `.claude-plugin/` directory layout, creating a plugin manifest, and adding an initialization command.

Commands will reference the setup script using `${CLAUDE_PLUGIN_ROOT}/.specimin/setup.feature.sh` to execute branch/directory creation logic. The script itself remains unchanged but is invoked from the plugin context. When users run commands in their projects, the setup script creates `.specimin/plans/` directories in the user's working directory (not the plugin directory), enabling per-project feature state management.

The initialization flow requires users to run `/init` once per project to create the `.specimin/` structure. Subsequent commands (`/spec`, `/feature.plan`, `/implement`, `/wrap`) assume this structure exists and fail gracefully with helpful error messages if missing. This explicit initialization prevents surprise directory creation and gives users control over when their project is "specimin-enabled."

Distribution follows a dual-channel model: stable releases published to Claude marketplace with semantic versions (e.g., 1.0.0, 1.1.0), and continuous git main branch for development/preview. Users choose their desired stability level by installation method. The repository functions exclusively as a plugin - local testing requires adding the repo as a plugin source in Claude Code settings.

---

## **Technology Decisions**

- Plugin manifest format: JSON (`.claude-plugin/plugin.json`)
- Semantic versioning: MAJOR.MINOR.PATCH (starting at 1.0.0)
- Script invocation: Bash with `${CLAUDE_PLUGIN_ROOT}` environment variable
- Directory structure: `.specimin/plans/{branch}/` in user projects
- Error handling: Graceful failures with actionable error messages
- Git operations: Use existing git commands (no additional tooling)

---

## **Component Modifications**

1. **Setup Script** (`.specimin/setup.feature.sh`): No functional changes, relocate to plugin root context
2. **Command Files** (all 4 commands): Update to reference `${CLAUDE_PLUGIN_ROOT}` for script paths, add initialization checks

---

## **New Components**

1. **Plugin Manifest** (`.claude-plugin/plugin.json`): Metadata file defining plugin identity, version, and component locations
2. **Initialization Command** (`.claude-plugin/commands/init.md`): New command to bootstrap `.specimin/` structure in user projects
3. **Commands Directory** (`.claude-plugin/commands/`): Relocated command definitions from `.claude/commands/`
4. **README for Plugin** (optional): User-facing documentation for plugin installation and usage

---

## **Task Sequence**

**Phase 1: Plugin Structure Setup**
1. Create `.claude-plugin/` directory and `plugin.json` manifest with required metadata
2. Move existing commands from `.claude/commands/` to `.claude-plugin/commands/`
3. Relocate `.specimin/` directory to plugin root (parallel to `.claude-plugin/`)

**Dependencies**: None

**Phase 2: Command Adaptation**
4. Update all 4 commands to use `${CLAUDE_PLUGIN_ROOT}/.specimin/setup.feature.sh` for script references
5. Create new `/init` command that checks for git repo and creates `.specimin/plans/` structure
6. Add initialization detection to existing commands (fail with helpful message if `.specimin/` missing)

**Dependencies**: Phase 1 complete (plugin structure must exist)

**Phase 3: Backward Compatibility Cleanup**
7. Remove `.claude/` directory (old command structure)
8. Update any internal references or documentation pointing to old structure
9. Test plugin installation and command execution locally

**Dependencies**: Phase 2 complete (commands must be functional before removing old structure)

**Phase 4: Distribution Preparation**
10. Create git tag for v1.0.0 release
11. Document installation instructions for both marketplace and git-based installation
12. Test dual installation methods (git URL and marketplace submission preparation)

**Dependencies**: Phase 3 complete (plugin must be fully functional)

---

## **Integration Points**

- **Claude Code Plugin System**: Plugin loaded via `.claude-plugin/plugin.json` manifest, commands registered with slash command handler
- **User Projects**: Commands create/modify `.specimin/plans/` directories in user's working directory
- **Git Repository**: Existing git operations unchanged (branch creation, commits, PR generation)
- **GitHub CLI**: `/wrap` command continues using `gh pr create` as-is
- **Bash Shell**: Setup script execution via plugin environment variable

---

## **Testing Strategy**

**Unit**: Verify `plugin.json` schema validity, check command markdown frontmatter, validate setup script path references

**Integration**: Test `/init` creates correct directory structure, verify commands locate setup script via `${CLAUDE_PLUGIN_ROOT}`, confirm error messages when `.specimin/` missing

**E2E**: Full workflow test: Install plugin → run `/init` → run `/spec` → run `/feature.plan` → run `/implement` → run `/wrap`, verify all phases work across fresh project

**Edge Cases**: Plugin installed but `/init` not run (graceful failure), `.specimin/` exists with wrong structure (detect and repair or error), non-git repository (detect and fail early), conflicting plugin with same command names

---

## **Risk Assessment & Mitigation**

**Risk**: Users forget to run `/init` and get cryptic errors
→ **Mitigations**: Clear error messages with `/init` instruction, document initialization in README, consider adding auto-detection note in first-run messages

**Risk**: `${CLAUDE_PLUGIN_ROOT}` not available in command execution context
→ **Mitigations**: Test environment variable availability early, add fallback detection, document Claude Code version requirements if variable is new

**Risk**: Breaking changes to existing users if they have `.claude/` structure
→ **Mitigations**: This is a new plugin, no existing users yet. Repository becomes plugin-first from v1.0.0 onward

**Risk**: Marketplace submission rejected or delayed
→ **Mitigations**: Git installation works immediately as fallback, marketplace becomes additive distribution channel not blocking

**Risk**: Setup script loses execute permissions in plugin distribution
→ **Mitigations**: Verify permissions in packaging, document troubleshooting, consider inline bash invocation (`bash ${CLAUDE_PLUGIN_ROOT}/.specimin/setup.feature.sh`)

**Risk**: Path handling differences between local development and installed plugin
→ **Mitigations**: Consistent use of `${CLAUDE_PLUGIN_ROOT}`, test both installation methods, avoid relative path assumptions
