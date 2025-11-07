# Specimin

A structured workflow for feature development with Claude Code.

## Why Specimin?

- **Systematic workflow**: Break features into spec → plan → tasks → PR → review
- **Context-aware**: Reviews compare against your spec's acceptance criteria
- **Token efficient**: Scripts handle data gathering, AI focuses on analysis
- **Research-backed**: Optimized using core prompt engineering primciples
- **Organized**: All artifacts in `.specimin/plans/{branch}/` directory

## Philosophy

Specimin separates **what** from **how**:

- **Specification** defines requirements and success criteria (product thinking)
- **Planning** explores implementation approaches (architectural thinking)
- **Implementation** breaks work into atomic tasks (execution)
- **Review & Refactor** maintains code quality (craftsmanship)

Each phase has clear boundaries and artifacts, enabling deliberate decision-making rather than ad-hoc development.

## Getting Started

### Installation

This is a Claude Code plugin. Install it via the marketplace or clone this repository into your Claude plugins directory.

### Initialize in Your Project

First time setup:
```bash
/specimin:init
```

This creates the `.specimin/` directory structure for managing feature specifications and plans.

### Basic Workflow

Specimin works through natural conversation with Claude Code. Just describe what you want:

1. **Specify** - Define what you're building and why

   "Create a specimin-spec for user authentication"

   Claude will guide you through clarifying questions and generate a product specification focused on requirements, not implementation.

2. **Plan** - Explore how to build it

   "Generate an implementation specimen-plan for this feature"

   Uses Tree-of-Thought exploration to evaluate multiple approaches and recommend the best strategy.

3. **Implement** - Break down into tasks

   "Break this plan down into implementation specimin-task"

   Converts high-level plans into atomic, actionable work items for step-by-step execution.

4. **Wrap** - Complete the feature

   "specimin-wrap up this feature and create a PR"

   Squashes commits and creates a pull request with context from your specification.

### Additional Capabilities

- **Review** - "specimin-review this code against the specification"
- **Refactor** - "specimin-refactor extract  this logic into a separate function"

## Requirements

- Git repository
- Claude Code
