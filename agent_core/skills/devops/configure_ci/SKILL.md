# Skill: Configure CI

## Metadata
- **MODEL**: GPT-5.4 (`gpt-5.4-2026-02-15`)
- **TEAM**: DevOps
- **ROLE**: DevOps Engineer

## Auth
| Priority | Key | Notes |
|----------|-----|-------|
| 1 (preferred) | `GITHUB_COPILOT_TOKEN` | Covers all models |
| 2 (override) | `OPENAI_KEY` | Direct OpenAI billing |

Auth resolved by `ModelRouter` in `copilot_models.py`.

## Goal
Generate CI/CD pipeline configuration files for automated building, testing, and deployment.

## Input
- Repository structure from AnalyzeRepo
- Build system (Maven, Gradle, npm, etc.)
- Testing framework
- Deployment targets
- Memory/decisions on architecture

## Process Steps
1. Detect build system and programming language
2. Create build step (compile, install dependencies)
3. Create test step (run unit + integration tests)
4. Create code quality checks (lint, coverage)
5. Create artifact building step
6. Create deployment step (staging/production)
7. Configure notifications/alerts
8. Generate appropriate YAML (GitHub Actions, GitLab CI, etc.)

## Output Format
```yaml
name: CI/CD Pipeline

on:
  push:
    branches: [main, develop]
  pull_request:
    branches: [main]

jobs:
  build:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - name: Set up JDK 17
        uses: actions/setup-java@v3
        with:
          java-version: '17'
      
      - name: Build with Maven
        run: mvn clean package
      
      - name: Run Tests
        run: mvn test
      
      - name: Upload Coverage
        run: bash <(curl -s https://codecov.io/bash)
```

## Memory Update
**Action**: Append to `memory/devops.md`

## Critic Criteria
- ✓ Pipeline builds successfully
- ✓ Tests run and results captured
- ✓ Coverage reported
- ✓ Artifacts generated
- ✓ Deployment steps correct
- ✓ Proper error handling

## Quality Threshold
85/100 - Pipeline should be reliable

## Notes
- Use latest GitHub Actions/GitLab versions
- Cache dependencies for speed
- Parallelize steps where possible
- Include deployment gates (only deploy if tests pass)
- Document deployment process
- Include rollback procedures
