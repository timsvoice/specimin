# Implementation Tasks Quality Rubric

Evaluate the following implementation task breakdown on three dimensions using a 1-5 scale.

**IMPORTANT:** Implementation tasks should NOT contain actual code. They should describe WHAT needs to be built with clear acceptance criteria, not provide code solutions. Pseudo code is acceptable only if a concept cannot be communicated in another way. Tasks containing significant code snippets should be penalized in scoring.

## Implementation Tasks to Evaluate

```
{IMPLEMENTATION_CONTENT}
```

## Scoring Dimensions

### 1. Actionability (1-5)

Can a developer immediately start working from these tasks?

**5 - Immediately Actionable**
- Each task has clear acceptance criteria
- What to build/modify is explicit
- Success conditions are observable
- No ambiguity about what "done" means

**4 - Actionable**
- Most tasks have clear criteria
- Generally clear what to implement
- Minor interpretation needed
- Success mostly obvious

**3 - Moderately Actionable**
- Tasks need some interpretation
- Acceptance criteria are vague in places
- Some tasks lack clear completion definition
- Developer can proceed but with questions

**2 - Difficult to Act On**
- Many tasks are vague
- Acceptance criteria missing or unclear
- Significant interpretation required
- Hard to know where to start

**1 - Not Actionable**
- Tasks are too vague to implement
- No acceptance criteria
- Cannot determine what to do
- Reads like a wish list

### 2. Granularity (1-5)

Are tasks appropriately sized (not too big, not too small)?

**5 - Perfect Granularity**
- Tasks are function/method-level boundaries
- Each task is 1-4 hours of work
- Not too broad (multiple days) or too narrow (minutes)
- Consistent sizing throughout

**4 - Good Granularity**
- Most tasks are appropriately sized
- Minor variation in complexity
- Generally follows function boundaries
- Few tasks are too large or small

**3 - Acceptable Granularity**
- Mix of appropriate and inappropriate sizing
- Some tasks too broad, others too granular
- Workable but uneven
- May need re-scoping during implementation

**2 - Poor Granularity**
- Many tasks are too large or too small
- Difficult to estimate effort
- Inconsistent sizing
- Needs significant breakdown

**1 - Wrong Granularity**
- All tasks are either massive or trivial
- Cannot estimate effort
- Unusable for planning
- Complete re-breakdown needed

### 3. Dependencies (1-5)

Are task dependencies clear and correctly identified?

**5 - Dependencies Crystal Clear**
- All dependencies explicitly stated
- Dependency graph is logical
- No circular dependencies
- Enables parallel work where possible

**4 - Clear Dependencies**
- Most dependencies identified
- Logic is sound
- Minor omissions don't block work
- Generally enables good workflow

**3 - Adequate Dependencies**
- Some dependencies identified
- Some implicit dependencies not stated
- Logic is mostly sound
- May cause minor blocking

**2 - Unclear Dependencies**
- Many dependencies missing or wrong
- Potential circular dependencies
- Difficult to determine work order
- Will cause blocking issues

**1 - Dependencies Missing/Wrong**
- No dependency information
- Or dependencies are completely wrong
- Cannot determine implementation order
- Will cause major blocking

## Your Task

Provide scores for each dimension with a brief 1-sentence justification:

**Actionability:** [1-5]
*Justification:* [One sentence explaining the score]

**Granularity:** [1-5]
*Justification:* [One sentence explaining the score]

**Dependencies:** [1-5]
*Justification:* [One sentence explaining the score]
