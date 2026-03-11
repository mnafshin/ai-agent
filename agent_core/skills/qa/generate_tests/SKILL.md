# Skill: Generate Tests

## Metadata
- **MODEL**: GPT-5.4 (`gpt-5.4-2026-02-15`)
- **TEAM**: QA
- **ROLE**: QA Engineer / Test Automation Engineer

## Auth
| Priority | Key | Notes |
|----------|-----|-------|
| 1 (preferred) | `GITHUB_COPILOT_TOKEN` | Covers all models |
| 2 (override) | `OPENAI_KEY` | Direct OpenAI billing |

Auth resolved by `ModelRouter` in `copilot_models.py`.

## Goal
Generate comprehensive unit and integration tests that cover happy path, edge cases, and error conditions.

## Input
- Implementation code to test
- Acceptance criteria from task
- Repository testing framework (JUnit, pytest, etc.)
- Existing tests as reference

## Process Steps
1. Identify testable units (classes, methods)
2. Write happy path tests (normal operation)
3. Write edge case tests (boundary conditions)
4. Write error case tests (invalid inputs)
5. Write integration tests if applicable
6. Ensure tests are deterministic
7. Verify tests fail without implementation
8. Verify tests pass with implementation

## Output Format
```java
public class ProductServiceTest {
  
  @Test
  void testCreateProduct_Success() {
    // Arrange
    Product product = new Product("Widget", 9.99);
    
    // Act
    Product saved = productService.save(product);
    
    // Assert
    assertNotNull(saved.getId());
    assertEquals("Widget", saved.getName());
  }
  
  @Test
  void testCreateProduct_NullProduct_ThrowsException() {
    // Assert
    assertThrows(IllegalArgumentException.class, 
      () -> productService.save(null));
  }
  
  @Test
  void testCreateProduct_InvalidPrice_ThrowsException() {
    Product product = new Product("Widget", -5.0);
    assertThrows(IllegalArgumentException.class,
      () -> productService.save(product));
  }
}
```

## Memory Update
**Action**: Append test summary to `memory/qa.md`

## Critic Criteria
- ✓ Test coverage at least 80%
- ✓ All edge cases covered
- ✓ Error conditions tested
- ✓ Tests are deterministic (no flakiness)
- ✓ Tests follow repository conventions
- ✓ Tests are independent (can run in any order)

## Quality Threshold
85/100 - Good test coverage prevents bugs

## Notes
- Write tests AFTER seeing implementation
- Follow Arrange-Act-Assert pattern
- One assertion per test when possible
- Test behavior, not implementation details
- Use meaningful test names
- Mark slow tests as @Slow
- Use test fixtures for common setup
