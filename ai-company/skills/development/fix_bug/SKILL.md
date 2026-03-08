# Skill: Fix Bug

## Metadata
- **MODEL**: Claude 3.5 Sonnet (debugging reasoning)
- **TEAM**: Development
- **ROLE**: Senior Developer / Debug Expert

## Goal
Debug and fix compilation errors, runtime errors, or failing tests with root cause analysis.

## Input
- Error message or failing test
- Stack trace or logs
- Relevant source code
- Test case that demonstrates the bug

## Process Steps
1. Read error message and stack trace carefully
2. Identify root cause (not just symptom)
3. Trace execution flow to understand issue
4. Propose minimal fix (don't refactor while fixing)
5. Apply patch
6. Run tests to verify fix
7. Check for related issues
8. Document what went wrong and why

## Output Format
```
## Root Cause Analysis
The issue is in ProductService.save() - it's passing null to the repository method.

## Error Stack
java.lang.NullPointerException at ProductRepository.save(ProductRepository.java:45)

## Fix
Add null check in ProductService.save():
```

## Example Output
```java
// Before
public Product save(Product product) {
  return productRepository.save(product);
}

// After - add validation
public Product save(Product product) {
  if (product == null) {
    throw new IllegalArgumentException("Product cannot be null");
  }
  return productRepository.save(product);
}
```

## Memory Update
**Action**: Append to `memory/debug_log.md`

Format:
```
## Bug Fix [Date]
**Issue**: [what was wrong]
**Root Cause**: [why it happened]
**Fix**: [what changed]
**Tests**: [which tests were failing, now passing]
```

## Critic Criteria
- ✓ Root cause identified (not just symptom treated)
- ✓ Fix is minimal and focused
- ✓ Doesn't introduce new issues
- ✓ Failing test now passes
- ✓ Related tests still pass

## Quality Threshold
90/100 - Fixes must be correct

## Notes
- Debug methodically - trace code execution
- Fix the cause, not the symptom
- Add unit tests for edge cases
- Don't refactor while debugging
- Document the learning for future reference
