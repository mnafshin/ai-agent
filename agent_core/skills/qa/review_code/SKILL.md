# Skill: Review Code

## Metadata
- **MODEL**: Claude 4.6 Opus (`claude-4.6-opus-20260301`)
- **TEAM**: QA
- **ROLE**: Code Reviewer / Architect

## Auth
| Priority | Key | Notes |
|----------|-----|-------|
| 1 (preferred) | `GITHUB_COPILOT_TOKEN` | Covers all models |
| 2 (override) | `ANTHROPIC_KEY` | Direct Anthropic billing |

Auth resolved by `ModelRouter` in `copilot_models.py`.

## Goal
Perform comprehensive code review evaluating correctness, quality, performance, and security.

## Input
- Implementation code or git diff
- Specification from WriteSpec
- Repository coding standards from AnalyzeRepo
- Acceptance criteria from task

## Process Steps
1. Review code for correctness against spec
2. Check adherence to coding standards
3. Evaluate code quality (readability, maintainability)
4. Identify performance issues
5. Check for security vulnerabilities
6. Verify test coverage
7. Generate score and recommendations
8. Identify blocking vs. non-blocking issues

## Output Format
```json
{
  "score": 87,
  "summary": "Good implementation with proper error handling. Consider performance optimization.",
  "blocking_issues": [
    {
      "severity": "CRITICAL",
      "issue": "SQL injection vulnerability in query",
      "location": "ProductRepository.java:25",
      "suggestion": "Use parameterized queries"
    }
  ],
  "non_blocking_issues": [
    {
      "severity": "MINOR",
      "issue": "Unused import",
      "location": "ProductService.java:3",
      "suggestion": "Remove unused import"
    }
  ],
  "recommendations": [
    "Add caching for frequently accessed products",
    "Add pagination for large result sets"
  ]
}
```

## Memory Update
**Action**: Append to `memory/review_log.md`

## Critic Criteria
- ✓ Review covers all dimensions (correctness, security, performance)
- ✓ Issues are specific with line numbers
- ✓ Blocking vs. non-blocking clearly marked
- ✓ Score is calibrated (90+ is excellent, 70- needs work)
- ✓ Recommendations are actionable

## Quality Threshold
80/100 - Review quality doesn't need to be perfect (feedback will improve code)

## Notes
- Be constructive - explain WHY, not just WHAT
- Follow repository code review culture
- Score 90+ = ready to merge
- Score 70-89 = needs improvements
- Score <70 = send back for revision
- Consider author intent, not just style
