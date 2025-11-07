# Specification Quality Rubric

Evaluate the following specification on three dimensions using a 1-5 scale.

## Specification to Evaluate

```
{SPEC_CONTENT}
```

## Scoring Dimensions

### 1. Completeness (1-5)

Does the specification include all necessary information to implement the feature?

**5 - Comprehensive**
- All required elements present: objective, context, constraints, acceptance criteria
- Edge cases and error conditions documented
- Dependencies and out-of-scope items clearly stated
- No ambiguity about what needs to be built

**4 - Mostly Complete**
- Most required elements present
- Minor gaps that don't significantly impact implementation
- Edge cases mostly covered
- Dependencies mentioned

**3 - Adequate**
- Core elements present (objective, acceptance criteria)
- Some gaps in edge cases or constraints
- Implementation possible but may require assumptions
- Some ambiguity exists

**2 - Incomplete**
- Missing key elements (e.g., acceptance criteria or constraints)
- Significant gaps that would block implementation
- Edge cases not addressed
- Unclear scope boundaries

**1 - Severely Incomplete**
- Minimal information provided
- Cannot implement without major clarification
- Most required elements missing
- Fundamentally unclear what to build

### 2. Clarity (1-5)

Is the specification understandable and unambiguous?

**5 - Crystal Clear**
- Precise, concrete language throughout
- No ambiguous terms or vague requirements
- Examples provided where helpful
- Easy to understand intent

**4 - Clear**
- Generally clear and specific
- Minor ambiguities that don't significantly impact understanding
- Intent is obvious
- Minimal interpretation needed

**3 - Moderately Clear**
- Understandable with some effort
- Some ambiguous language or vague requirements
- May require re-reading to grasp intent
- Some interpretation needed

**2 - Unclear**
- Confusing or contradictory statements
- Significant ambiguity
- Difficult to understand intent
- Extensive interpretation required

**1 - Very Unclear**
- Incomprehensible or highly contradictory
- Cannot determine intent
- Filled with jargon or undefined terms
- Impossible to act on

### 3. Testability (1-5)

Can the specification be verified through testing?

**5 - Highly Testable**
- All acceptance criteria are measurable and observable
- Clear success/failure conditions
- Specific, verifiable requirements
- Test scenarios are obvious from the spec

**4 - Testable**
- Most criteria are measurable
- Success conditions generally clear
- Requirements can be verified with minor interpretation
- Test approach is clear

**3 - Moderately Testable**
- Some criteria are measurable
- Mix of concrete and subjective requirements
- Testing possible but requires assumptions
- Some verification methods unclear

**2 - Difficult to Test**
- Many subjective or unmeasurable criteria
- Unclear how to verify success
- Vague requirements dominate
- Testing approach unclear

**1 - Untestable**
- No measurable criteria
- Cannot determine success/failure
- All requirements are subjective
- Verification impossible

## Your Task

Provide scores for each dimension with a brief 1-sentence justification:

**Completeness:** [1-5]
*Justification:* [One sentence explaining the score]

**Clarity:** [1-5]
*Justification:* [One sentence explaining the score]

**Testability:** [1-5]
*Justification:* [One sentence explaining the score]
