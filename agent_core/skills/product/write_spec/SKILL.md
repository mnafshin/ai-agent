# Skill: Write Specification

## Metadata
- **MODEL**: Claude 4.6 Opus (`claude-4.6-opus-20260301`)
- **TEAM**: Product
- **ROLE**: Product Manager / Tech Lead

## Auth
| Priority | Key | Notes |
|----------|-----|-------|
| 1 (preferred) | `GITHUB_COPILOT_TOKEN` | Covers all models |
| 2 (override) | `ANTHROPIC_KEY` | Direct Anthropic billing |

Auth resolved by `ModelRouter` in `copilot_models.py`.

## Goal
Create a formal specification document that translates requirements into implementation-ready specs with clear acceptance criteria.

## Input
- Requirements JSON from GatherRequirements skill
- Optional: existing architecture context

## Process Steps
1. Define functional specifications with examples
2. Define non-functional specifications (latency, throughput, etc.)
3. Map each requirement to acceptance criteria
4. Identify API contracts or interfaces needed
5. Define data models or schemas required
6. Document edge cases and error handling
7. Create acceptance test scenarios

## Output Format (Markdown)
```markdown
# Specification: [Feature Name]

## Functional Specifications

### Use Case 1: [Description]
- Prerequisites: ...
- Steps: ...
- Expected Result: ...

### Use Case 2: ...

## Non-Functional Specifications
- Latency: <100ms
- Throughput: 1000 req/sec
- Concurrency: 100 concurrent users
- Data Retention: 1 year

## API Contract
```

## Memory Update
**Action**: Overwrite `memory/decisions.md` with specification summary

## Critic Criteria
- ✓ Specification is implementation-ready (not abstract)
- ✓ All functional requirements covered
- ✓ Non-functional specs are measurable
- ✓ Edge cases documented
- ✓ No ambiguous terms

## Quality Threshold
90/100 - Specification quality directly impacts code quality

## Notes
- Write for developers, not stakeholders
- Include examples and counter-examples
- Cover both happy path and error cases
- Reference requirements by ID
