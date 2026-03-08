# Skill: Analyze Repository

## Metadata
- **MODEL**: Claude 3.5 Sonnet
- **TEAM**: Architecture
- **ROLE**: Architect

## Goal
Understand the existing repository structure, modules, conventions, and tech stack before designing new features.

## Input
- Local repository path
- Optional: README and key configuration files

## Process Steps
1. Map folder structure and identify modules
2. Detect framework (Spring Boot, Django, FastAPI, etc.)
3. Identify tech stack (Java 17, Spring 3.1, PostgreSQL, etc.)
4. Find coding standards and conventions
5. Identify design patterns in use
6. Note dependencies and their purposes
7. Check for existing test framework and coverage approach

## Output Format (Markdown)
```markdown
# Repository Analysis

## Project Structure
- Backend: Spring Boot 3.1
- Frontend: Angular 17
- Database: PostgreSQL 15

## Tech Stack
- Language: Java 17
- Framework: Spring Boot
- Build: Maven
- Testing: JUnit 5, Mockito

## Design Patterns
- MVC for web controllers
- Service/Repository pattern for data access
- Dependency injection via Spring

## Coding Standards
- Package naming: com.company.domain.*
- Class naming: PascalCase
- Method naming: camelCase

## Testing Approach
- Unit tests in src/test
- Integration tests use TestContainers
- Test coverage target: 80%

## Key Dependencies
- [dependency]: purpose
```

## Memory Update
**Action**: Overwrite `memory/repo_summary.md` with analysis

## Critic Criteria
- ✓ Accurately represents current structure
- ✓ Tech stack versions are correct
- ✓ Design patterns identified correctly
- ✓ Coding conventions documented

## Quality Threshold
85/100 - This becomes reference for all future work

## Notes
- If source code large, focus on key modules
- Look for README, architecture docs
- Check for existing architectural decisions
