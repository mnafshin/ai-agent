# Skill: Implement Feature

## Metadata
- **SKILL_ID**: implement_feature
- **MODEL**: Claude 4 Sonnet (`claude-4-sonnet-20260201`)
- **TEAM**: Development
- **ROLE**: Senior Developer

## Auth
| Priority | Key | Notes |
|----------|-----|-------|
| 1 (preferred) | `GITHUB_COPILOT_TOKEN` | Covers all models |
| 2 (override) | `ANTHROPIC_KEY` | Direct Anthropic billing |

Auth resolved by `ModelRouter` in `copilot_models.py`.
- **MODEL**: copilot/codex (fast code generation, expert at writing production code)

## Alternative Models
- `gpt/gpt-4o` - If Codex unavailable, fallback to GPT-4o for code generation
- `claude/sonnet` - For lower latency, still good code quality

## Goal
Implement a single development task by writing clean, testable code that follows repository conventions.

## Input
- Task description (from planned task)
- Acceptance criteria
- Repository context from AnalyzeRepo
- Architecture design from DesignSystem
- Memory files with coding conventions

## Process Steps
1. Read acceptance criteria carefully
2. Review repository coding standards
3. Identify files to create/modify
4. Implement minimum code needed (no over-engineering)
5. Follow existing naming conventions
6. Add comments for complex logic
7. Ensure code compiles
8. Output git diff/patch

## Output Format
```
File: src/main/java/com/example/entity/Product.java
Action: CREATE

@Entity
@Table(name = "products")
public class Product {
  @Id
  @GeneratedValue
  private Long id;
  
  private String name;
  
  // ... rest of implementation
}

---

File: src/test/java/com/example/entity/ProductTest.java
Action: CREATE

public class ProductTest {
  @Test
  void testProductCreation() {
    // test code
  }
}
```

## Memory Update
**Action**: Optional - append to `memory/decisions.md` if approach differs from architecture

## Critic Criteria
- ✓ Code is clean and readable
- ✓ Follows repository conventions
- ✓ No compiler errors
- ✓ Implements all acceptance criteria
- ✓ Doesn't break existing tests
- ✓ Proper error handling

## Quality Threshold
85/100 for implementation (tests and review will catch more issues)

## Notes
- Ask for clarification if ambiguous
- Keep changes minimal and focused
- Don't refactor existing code (use RefactorCode skill)
- Add unit tests in same PR
- Use existing patterns from codebase
