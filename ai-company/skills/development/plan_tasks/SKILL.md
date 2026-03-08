# Skill: Plan Tasks

## Metadata
- **MODEL**: Claude 3.5 Sonnet
- **TEAM**: Development
- **ROLE**: Tech Lead / Senior Developer

## Goal
Break the architecture into small, independent, atomic development tasks that can be implemented in sequence.

## Input
- Architecture design from DesignSystem
- Specification from WriteSpec
- Repository analysis from AnalyzeRepo

## Process Steps
1. Identify all components from architecture
2. Order components respecting dependencies
3. Break components into testable units
4. Create one task per file/class to create or modify
5. Specify files to create and modify
6. Include acceptance criteria for each task
7. Order tasks so earlier ones don't depend on later ones

## Output Format (JSON)
```json
{
  "tasks": [
    {
      "id": 1,
      "name": "Create ProductEntity",
      "description": "Define Product JPA entity",
      "files": ["src/main/java/com/example/entity/Product.java"],
      "acceptance_criteria": [
        "Entity has all fields from spec",
        "Annotations correct for database mapping",
        "Equals/hashCode/toString implemented"
      ]
    },
    {
      "id": 2,
      "name": "Create ProductRepository",
      "description": "Define ProductRepository interface",
      "files": ["src/main/java/com/example/repository/ProductRepository.java"],
      "dependencies": [1]
    }
  ]
}
```

## Memory Update
**Action**: Write individual task files `tasks/request_X/0Y_taskname.md`

## Critic Criteria
- ✓ Tasks are small and focused
- ✓ Each task is independent (no circular dependencies)
- ✓ Tasks follow correct build order
- ✓ Each task specifies files to modify
- ✓ Acceptance criteria are testable
- ✓ Covers all requirements

## Quality Threshold
90/100 - Task planning prevents forgotten work

## Notes
- Keep tasks small (1-2 hours of work each)
- Each task should produce testable code
- Minimize context switching between tasks
- Order tasks to maximize parallelizability where possible
