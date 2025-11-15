# UI Workflow Guide (Streamlined v1.3.0)

## Overview

Specimin's UI workflow has been **streamlined** to reduce documentation overhead by **76-92%**.

Now there's just **one skill** to use: `specimin:ui-generate`

## Quick Start

### For 90% of UI Changes (Simple)

Just use `specimin:ui-generate` directly:

```bash
# Provide sketch, mockup, or description
# Agent explores codebase
# Agent generates code
# Agent validates
# Result: Working code + ~75 line report
```

**Example use cases**:
- Add charts/visualizations
- Modify existing components
- Layout adjustments
- Add standard components

**Documentation created**: ~75 lines (generation report only)

### For 10% of UI Changes (Complex)

Use `specimin:ui-generate` with optional design context:

```bash
# Agent asks if simple or complex
# If complex: Agent creates lightweight design context first (80-150 lines)
# Agent generates code
# Agent validates
# Result: Working code + design context + report (~220 lines total)
```

**Example use cases**:
- Multi-component features with ambiguities
- New design patterns not in codebase
- Significant responsive/interactive complexity

**Documentation created**: ~220 lines (design context + report)

## What Changed from v1.2.0

### Before (3 separate skills)

1. `specimin:ui-understand` - Analyze design (243 lines)
2. `specimin:ui-structure` - Define structure (485 lines)
3. `specimin:ui-generate` - Generate code (178 lines)

**Total**: 906 lines, 3 phases, ~30 minutes

### After (1 streamlined skill)

1. `specimin:ui-generate` - Does everything

**For simple changes**:
- ~75 lines, 1 phase, ~8 minutes
- **92% less documentation, 75% faster**

**For complex features**:
- ~220 lines, 1 phase, ~20 minutes
- **76% less documentation, 60% faster**

## How It Works

### Stage 1: Assess Complexity

Agent asks: "Is this simple or complex?"

- **Simple**: Proceed directly to generation
- **Complex**: Create lightweight design context first

### Stage 2: Explore Codebase Inline

Agent automatically:
- Detects framework (Phoenix/React/Vue/Next.js)
- Finds similar components in your codebase
- Discovers styling patterns (Tailwind usage)
- Loads design system (if available)

Time-boxed to 2-3 minutes.

### Stage 3: Make Decisions Inline

Agent decides automatically:
- Which design system patterns to use
- Component structure
- File locations
- Responsive approach
- Styling patterns

Only asks user for:
- Real ambiguities (multiple valid approaches)
- Business logic (what happens on click?)
- Data requirements (where does data come from?)

### Stage 4: Generate Code

Agent generates:
- ✅ Complete implementations (no placeholders)
- ✅ Semantic HTML
- ✅ Tailwind utilities only
- ✅ Realistic content
- ✅ Proper imports

### Stage 5: Validate (Max 3 Iterations)

Agent checks:
- **Compilation**: Does code compile?
- **Structure**: Responsive, semantic HTML, design system patterns?
- **Accessibility**: Semantic elements, ARIA, keyboard nav?

Fixes issues and regenerates up to 3 times.

### Stage 6: Create Concise Report

Agent creates brief report (50-100 lines):
- Files created/modified
- Validation results
- Issues resolved
- Next steps

## Real Example: Benchmark Charts

### Task
Replace text statistics with horizontal bar charts

### Old Workflow (v1.2.0)

**Phase 1 - ui-understand**: 243 lines
- Analyzed entire page
- Documented all components
- Listed style specifications
- Captured responsive behaviors

**Phase 2 - ui-structure**: 485 lines
- Loaded framework context
- Mapped design system patterns
- Defined HTML structure with pseudo-code
- Specified responsive strategy with examples
- Documented interactivity with code snippets

**Phase 3 - ui-generate**: 178 lines
- Generated code (2 iterations)
- Documented validation results
- Listed issues resolved

**Total**: 906 lines, 3 phases, ~30 minutes

### New Workflow (v1.3.0)

**Single Phase - ui-generate**: 75 lines
- Explored codebase for chart patterns
- Decided on ApexCharts + Phoenix hook
- Generated code (2 iterations)
- Validated compilation, structure, accessibility
- Fixed missing ID attributes
- Created concise report

**Total**: 75 lines, 1 phase, ~8 minutes

**Improvement**: 92% less documentation, 75% faster

## Key Improvements

### 1. No More Redundant Phases

**Before**: `understanding.md` and `structure.md` had massive overlap
- Same components documented twice
- Same styling patterns repeated
- Same responsive behaviors listed twice

**After**: Single generation process, optional lightweight design context only for complex features

### 2. Inline Exploration

**Before**: Separate analysis phase tried to document everything upfront

**After**: Agent explores during generation
- Finds actual patterns in your code
- Makes decisions based on real conventions
- Only documents what was actually built

### 3. Tiered Complexity

**Before**: Always 3-phase workflow, even for trivial changes

**After**: Match process to complexity
- Simple (90%): Direct generation, ~75 lines
- Complex (10%): Optional design context, ~220 lines

### 4. Lazy Documentation

**Before**: Documented everything that might be built
- Exact Tailwind classes specified upfront
- Helper functions pre-defined
- Performance notes written
- Future enhancements listed

**After**: Document what was actually built
- Real changes made
- Validation results
- Practical next steps only

## Best Practices

### Do

- ✅ Provide clear sketches or descriptions
- ✅ Let agent explore and decide for simple changes
- ✅ Answer questions about business logic
- ✅ Review generation reports for accuracy
- ✅ Trust the agent to find patterns in your codebase

### Don't

- ❌ Over-specify implementation details
- ❌ Try to document everything upfront
- ❌ Assume agent knows your business requirements
- ❌ Ignore validation warnings
- ❌ Skip testing after generation

## Metrics

### Documentation Volume
- **Simple changes**: 75 lines (92% reduction from 906)
- **Complex features**: 220 lines (76% reduction from 906)

### Time to Completion
- **Simple changes**: ~8 min (75% faster than 30 min)
- **Complex features**: ~20 min (60% faster than 50 min)

### Quality Maintained
- **Compilation success**: Same (80%+ after validation)
- **Accessibility**: Same (basic checks passed)
- **Code completeness**: Improved (fewer placeholders)

## Troubleshooting

**"Agent is making wrong decisions"**
→ Tell agent it's a complex feature so it creates design context first

**"Need more detailed documentation"**
→ Request agent document specific decisions in design context

**"Agent asked something obvious"**
→ Provide more context in initial description

**"Code doesn't match codebase patterns"**
→ Check if similar patterns exist; agent explores during generation

## Migration from v1.2.0

If you have existing projects with old 3-phase documentation:

**Option 1: Keep old docs** (recommended)
- Old docs still valid as reference
- Use new workflow for new features

**Option 2: Clean up old docs**
- Archive old `understanding.md` and `structure.md`
- Keep `generation-report.md` for reference
- Use new workflow going forward

## What's Next

Future improvements planned:
- Visual diff tool for comparing generated vs expected
- Automated screenshot testing integration
- Design system auto-discovery
- Cost estimation based on complexity

## Feedback

This streamlined workflow is based on research and real-world testing. Please provide feedback on what works and what doesn't!

---

**TL;DR**: Just use `specimin:ui-generate` for everything. For 90% of changes it'll explore your codebase, generate code, validate, and create a brief report (~75 lines). For complex features, it'll optionally create lightweight design context first (~220 lines total). Either way, you get 76-92% less documentation than before.
