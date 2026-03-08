# Skill: Refactor Code

## Metadata
- **MODEL**: Copilot / GPT-4
- **TEAM**: Development
- **ROLE**: Senior Developer

## Goal
Safely refactor existing code to improve quality, readability, or performance while preserving all behavior.

## Input
- Refactoring task description
- Code files to refactor
- Repository coding standards
- Existing tests that must pass

## Process Steps
1. Understand current code behavior
2. Identify refactoring target (simplify, extract, rename, etc.)
3. Run existing tests - ensure they all pass
4. Apply refactoring incrementally
5. Run tests after each change
6. Verify behavior unchanged
7. Output git diff/patch

## Output Format
```
File: src/main/java/com/example/service/ProductService.java
Action: MODIFY

// Before:
public List<Product> search(String query) {
  List<Product> results = new ArrayList<>();
  for (Product p : products) {
    if (p.getName().contains(query)) {
      results.add(p);
    }
  }
  return results;
}

// After:
public List<Product> search(String query) {
  return products.stream()
    .filter(p -> p.getName().contains(query))
    .collect(Collectors.toList());
}
```

## Memory Update
**Action**: Optional - append to `memory/decisions.md` if approach affects design

## Critic Criteria
- ✓ All existing tests still pass
- ✓ Code is more readable/maintainable
- ✓ No behavioral changes
- ✓ Performance improved or maintained
- ✓ Follows repository style after refactoring

## Quality Threshold
85/100 - Refactoring must preserve behavior

## Notes
- Never refactor and add features simultaneously
- Always run tests before and after
- Keep refactoring focused (one goal per task)
- Document why refactoring is needed
- Avoid over-engineering / premature optimization
