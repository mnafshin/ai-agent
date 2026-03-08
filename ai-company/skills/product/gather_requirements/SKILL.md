# Skill: Gather Requirements

## Metadata
- **MODEL**: Claude 3.5 Sonnet
- **TEAM**: Product
- **ROLE**: Product Manager

## Goal
Convert a vague user request into structured product requirements with clear goals, constraints, and success metrics.

## Input
- User request text (can be informal)
- Optional: existing project context

## Process Steps
1. Identify the core problem being solved
2. Identify the target user / stakeholder
3. Extract functional requirements
4. Extract non-functional requirements (performance, security, scalability)
5. Identify constraints (tech stack, timeline, budget)
6. Define success metrics / acceptance criteria

## Output Format (JSON)
```json
{
  "problem": "Clear statement of what problem this solves",
  "target_user": "Who will use this feature",
  "functional_requirements": [
    "User can do X",
    "System should support Y"
  ],
  "non_functional_requirements": [
    "Handle 1000 requests/sec",
    "GDPR compliant data storage"
  ],
  "constraints": [
    "Must use existing Spring Boot framework",
    "3 week deadline"
  ],
  "success_metrics": [
    "API responds in <100ms",
    "99.9% uptime",
    "All unit tests pass"
  ]
}
```

## Memory Update
**Action**: Append requirements to `memory/repo_summary.md`

Update section: `# Current Request`

## Critic Criteria
- ✓ Requirements are clear and unambiguous
- ✓ Success metrics are measurable
- ✓ Constraints are realistic
- ✓ No contradictions between requirements

## Quality Threshold
90/100 - These requirements drive all downstream work

## Notes
- Ask clarifying questions if the user request is vague
- Assume reasonable defaults if not specified
- Document assumptions in the output
