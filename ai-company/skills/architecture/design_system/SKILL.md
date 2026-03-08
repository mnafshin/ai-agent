# Skill: Design System

## Metadata
- **MODEL**: Claude 3.5 Sonnet
- **TEAM**: Architecture
- **ROLE**: Architect / Tech Lead

## Goal
Design a clean, modular architecture for the requested feature that integrates seamlessly with existing codebase.

## Input
- Specification from WriteSpec
- Repository analysis from AnalyzeRepo
- Memory files with existing architectural decisions

## Process Steps
1. Review existing architecture patterns
2. Identify components needed for new feature
3. Design interfaces and contracts between components
4. Map dependencies and avoid circular dependencies
5. Ensure consistency with existing patterns
6. Identify new modules/packages if needed
7. Document integration points with existing code
8. Consider scalability and extensibility

## Output Format (Markdown)
```markdown
# Architecture Design: [Feature Name]

## Component Diagram
```
[ASCII or description of component relationships]
```

## Components
### [ComponentName]
- Purpose: ...
- Responsibilities: ...
- Dependencies: ...
- Interface: ...

## Design Decisions
- Why this pattern?
- Alternative considered?
- Trade-offs?

## Integration Points
- How does this integrate with existing code?
- What existing components does it depend on?

## New Modules
- [Module name]: path, responsibilities
```

## Memory Update
**Action**: Append design to `memory/architecture.md`

## Critic Criteria
- ✓ Design follows existing patterns in repository
- ✓ Components are loosely coupled
- ✓ All requirements can be implemented
- ✓ Scalability considered
- ✓ No circular dependencies

## Quality Threshold
90/100 - Architecture impacts entire implementation

## Notes
- Prefer patterns already used in codebase
- Document your design decisions
- Consider testability from start
- Plan for future extensions
