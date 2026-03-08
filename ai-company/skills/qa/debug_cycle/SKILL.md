# Skill: Debug Cycle

## Metadata
- **MODEL**: Claude 3.5 Sonnet (reasoning from error logs)
- **TEAM**: QA
- **ROLE**: QA Engineer / DevOps

## Goal
Fix failing builds or test failures during the automated execution pipeline.

## Input
- Build logs or test failure output
- Stack traces
- Error messages
- Relevant source code

## Process Steps
1. Parse build or test failure
2. Identify root cause from logs
3. Categorize error (compilation, runtime, assertion, etc.)
4. Generate suggested fix with explanation
5. Apply patch to source code
6. Re-run tests to verify fix
7. Repeat until all tests pass
8. Document what fixed the issue

## Output Format
```
## Build Failure Analysis

**Error Type**: Compilation error
**Location**: src/main/java/com/example/service/ProductService.java:42

**Error Message**: 
error: cannot find symbol: variable productId

**Root Cause**:
Method parameter name is 'id' but code references 'productId'

**Fix Applied**:
Changed reference from productId to id on line 42

**Result**: ✓ BUILD SUCCESSFUL
```

## Memory Update
**Action**: Append to `memory/debug_log.md`

## Critic Criteria
- ✓ Root cause identified
- ✓ Fix is correct
- ✓ Build now succeeds
- ✓ Tests pass
- ✓ No new warnings introduced

## Quality Threshold
95/100 - Build must succeed

## Notes
- Read entire error stack, not just first line
- Check for multiple errors (fix one at a time)
- Verify fix doesn't break other tests
- Document error patterns for future prevention
- Keep build log for analysis
