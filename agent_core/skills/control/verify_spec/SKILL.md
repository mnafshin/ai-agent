# Skill: Verify Spec

## Metadata
- **MODEL**: Claude 4 Sonnet (`claude-4-sonnet-20260201`)
- **TEAM**: Control Layer
- **ROLE**: Requirements Verification

## Auth
| Priority | Key | Notes |
|----------|-----|-------|
| 1 (preferred) | `GITHUB_COPILOT_TOKEN` | Covers all models |
| 2 (override) | `ANTHROPIC_KEY` | Direct Anthropic billing |

Auth resolved by `ModelRouter` in `copilot_models.py`.

## Goal
Verify that a generated solution actually satisfies the original specification and requirements.

## Input
- Original specification document
- Generated solution/implementation
- Acceptance criteria from task
- Architecture design (if applicable)

## Process Steps
1. Carefully re-read original specification
2. Review generated solution
3. Check each requirement against implementation
4. Identify missing functionality
5. Verify edge cases are handled
6. Ensure error cases handled
7. Check performance requirements if specified
8. Generate verification report

## Output Format
```json
{
  "valid": false,
  "compliance_score": 85,
  "missing_requirements": [
    {
      "requirement": "API must return 404 for non-existent products",
      "status": "NOT IMPLEMENTED",
      "severity": "CRITICAL",
      "impact": "API violates REST conventions"
    },
    {
      "requirement": "Bulk delete operation for multiple products",
      "status": "NOT IMPLEMENTED",
      "severity": "MAJOR",
      "impact": "Missing feature from spec"
    }
  ],
  "implemented_requirements": [
    "Create product endpoint with validation",
    "Retrieve product by ID",
    "Update product details",
    "List all products with pagination"
  ],
  "discrepancies": [
    "Response format uses 'product_id' but spec requires 'id'",
    "API response time target was 100ms, implementation takes 200ms for bulk operations"
  ],
  "verdict": "REJECTED - Must implement missing error handling and API corrections"
}
```

## Memory Update
**Action**: Append to `memory/verification.md`

## Verification Levels
- **APPROVED**: 95%+ requirements met, minor issues only
- **ACCEPTED_WITH_ISSUES**: 85-95% requirements met, issues documented
- **REJECTED**: <85% requirements met, must fix and resubmit

## Notes
- Spec verification is the final quality gate
- Don't accept "close enough" - be strict
- Document every missing requirement
- Note performance/quality issues
- Clarify ambiguities by referencing spec section
- Explain what needs to be fixed for approval
- This is the most important quality control

## Critical Points
⚠️ This is where most "works but doesn't solve the problem" issues are caught
⚠️ Never skip spec verification 
⚠️ Be extremely thorough and specific about what's missing
