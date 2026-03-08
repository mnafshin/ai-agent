# 📑 Complete File Index & Navigation Guide

## Start Here (Read in This Order)

1. **SUMMARY.md** ← You are here! Overview of everything
2. **QUICKSTART.md** ← 5-minute setup (if in hurry)
3. **article/AI_AGENTS_BEST_PRACTICES.md** ← Full philosophy & guide
4. **README.md** ← Comprehensive documentation

---

## 📰 Documentation Files

### Main Articles
| File | Purpose | Length | Read Time |
|------|---------|--------|-----------|
| `article/AI_AGENTS_BEST_PRACTICES.md` | Complete guide to AI agent best practices | 4000+ words | 20 min |
| `README.md` | Full technical documentation | 3000+ words | 15 min |
| `QUICKSTART.md` | 5-minute setup and reference | 1000+ words | 5 min |
| `SUMMARY.md` | Project overview | 2000+ words | 10 min |
| `DIRECTORY_TREE.md` | Complete file structure | 1000+ words | 5 min |

### When to Read Each
- **First time?** → Start with QUICKSTART.md
- **Want to understand?** → Read AI_AGENTS_BEST_PRACTICES.md
- **Need details?** → Check README.md
- **Lost?** → Look at DIRECTORY_TREE.md
- **Quick reference?** → Use this INDEX.md

---

## 🏭 Implementation Files

### Orchestrator (Main Engine)
```
ai-company/orchestrator.py
```
- **Purpose**: Manages 20-agent workflow
- **What it does**:
  - Loads skills dynamically
  - Runs critic loops (max 5 iterations)
  - Verifies against spec
  - Updates memory files
- **How to use**: `python orchestrator.py 001`
- **Lines**: ~400

### Inspector (Validation Tool)
```
tools/inspector.py
```
- **Purpose**: Validates entire system
- **What it checks**:
  - All 20 skills present
  - SKILL.md files properly formatted
  - Memory directory initialized
  - Config files in place
- **How to use**: `python inspector.py ai-company`
- **Lines**: ~400

### Configuration
```
ai-company/config.yaml
```
- **Purpose**: System configuration
- **Contains**:
  - Critic loop settings (max 5, threshold 90)
  - Model assignments (Claude, GPT, Copilot)
  - Memory configuration
  - Execution settings

---

## 🎓 Skill Reference (20 Files)

### Product Team (2 Skills)

#### 1. Gather Requirements
```
ai-company/skills/product/gather_requirements/SKILL.md
```
- **Goal**: Extract structured requirements from user request
- **Model**: Claude
- **Input**: Vague user request
- **Output**: JSON with requirements, constraints, success metrics
- **Memory**: Updates repo_summary.md
- **Quality Threshold**: 90/100
- **Read this to**: Understand requirement extraction

#### 2. Write Specification
```
ai-company/skills/product/write_spec/SKILL.md
```
- **Goal**: Create formal implementation-ready specification
- **Model**: Claude
- **Input**: Requirements JSON
- **Output**: Detailed spec with APIs, data models, error handling
- **Memory**: Updates decisions.md
- **Critic Loop**: Yes (quality critical)
- **Quality Threshold**: 90/100
- **Read this to**: Understand spec creation

### Architecture Team (3 Skills)

#### 3. Analyze Repository
```
ai-company/skills/architecture/analyze_repo/SKILL.md
```
- **Goal**: Understand existing code structure and conventions
- **Model**: Claude
- **Input**: Repository structure
- **Output**: Analysis of tech stack, patterns, conventions
- **Memory**: Overwrites repo_summary.md
- **Quality Threshold**: 85/100
- **Read this to**: Learn how to analyze existing code

#### 4. Design System
```
ai-company/skills/architecture/design_system/SKILL.md
```
- **Goal**: Create architecture for new features
- **Model**: Claude
- **Input**: Specification + repository analysis
- **Output**: Component diagrams, interfaces, integration points
- **Memory**: Appends to architecture.md
- **Critic Loop**: Yes
- **Verify Spec**: Yes
- **Quality Threshold**: 90/100
- **Read this to**: Understand architecture design

### Development Team (4 Skills)

#### 5. Plan Tasks
```
ai-company/skills/development/plan_tasks/SKILL.md
```
- **Goal**: Break architecture into atomic development tasks
- **Model**: Claude
- **Input**: Architecture design
- **Output**: JSON list of ordered, independent tasks
- **Critic Loop**: Yes
- **Memory**: Writes individual task files
- **Quality Threshold**: 90/100
- **Read this to**: Understand task planning

#### 6. Implement Feature
```
ai-company/skills/development/implement_feature/SKILL.md
```
- **Goal**: Write code for a single development task
- **Model**: Copilot (reuse your token!)
- **Input**: Task description, acceptance criteria
- **Output**: Git diff or code patch
- **Critic Loop**: Yes
- **Verify Spec**: Yes
- **Quality Threshold**: 85/100
- **Read this to**: Understand code generation

#### 7. Refactor Code
```
ai-company/skills/development/refactor_code/SKILL.md
```
- **Goal**: Safely refactor existing code
- **Model**: Copilot
- **Input**: Code and refactoring task
- **Output**: Git diff preserving behavior
- **Quality Threshold**: 85/100
- **Read this to**: Understand safe refactoring

#### 8. Fix Bug
```
ai-company/skills/development/fix_bug/SKILL.md
```
- **Goal**: Debug and fix compilation/runtime errors
- **Model**: Claude (reasoning from errors)
- **Input**: Error message, stack trace
- **Output**: Root cause analysis + fix
- **Memory**: Appends to debug_log.md
- **Quality Threshold**: 90/100
- **Read this to**: Understand debugging approach

### QA Team (3 Skills)

#### 9. Generate Tests
```
ai-company/skills/qa/generate_tests/SKILL.md
```
- **Goal**: Create unit and integration tests
- **Model**: GPT-4 (excellent at test generation)
- **Input**: Implementation code
- **Output**: Test files with happy path + edge cases
- **Memory**: Appends to qa.md
- **Quality Threshold**: 85/100
- **Read this to**: Understand test generation

#### 10. Debug Cycle
```
ai-company/skills/qa/debug_cycle/SKILL.md
```
- **Goal**: Fix build failures and test failures
- **Model**: Claude
- **Input**: Build logs, error messages
- **Output**: Fixed code, log analysis
- **Memory**: Appends to debug_log.md
- **Quality Threshold**: 95/100 (build must succeed)
- **Read this to**: Understand failure recovery

#### 11. Review Code
```
ai-company/skills/qa/review_code/SKILL.md
```
- **Goal**: Evaluate code quality, security, performance
- **Model**: Claude
- **Input**: Implementation code or diff
- **Output**: Score 0-100 with specific issues
- **Critic Loop**: Yes
- **Memory**: Appends to review_log.md
- **Quality Threshold**: 80/100
- **Read this to**: Understand code review criteria

### DevOps Team (2 Skills)

#### 12. Configure CI
```
ai-company/skills/devops/configure_ci/SKILL.md
```
- **Goal**: Generate CI/CD pipeline configuration
- **Model**: GPT-4 (good at YAML)
- **Input**: Build system, testing framework
- **Output**: GitHub Actions/GitLab CI config
- **Memory**: Appends to devops.md
- **Quality Threshold**: 85/100
- **Read this to**: Understand CI/CD setup

#### 13. Deploy App
```
ai-company/skills/devops/deploy_app/SKILL.md
```
- **Goal**: Create deployment scripts and procedures
- **Model**: GPT-4
- **Input**: Build artifacts, deployment target
- **Output**: Deployment script with health checks
- **Memory**: Appends to deployments.md
- **Quality Threshold**: 85/100
- **Read this to**: Understand deployment automation

### Documentation Team (2 Skills)

#### 14. Update Docs
```
ai-company/skills/docs/update_docs/SKILL.md
```
- **Goal**: Update technical documentation
- **Model**: GPT-4 (excellent at clarity)
- **Input**: Implementation details, APIs
- **Output**: Updated markdown docs with examples
- **Memory**: Appends to docs.md
- **Quality Threshold**: 80/100
- **Read this to**: Understand technical writing

#### 15. Write Release Notes
```
ai-company/skills/docs/write_release_notes/SKILL.md
```
- **Goal**: Create comprehensive release notes
- **Model**: GPT-4 (excellent summarization)
- **Input**: All completed tasks, changes, bugs fixed
- **Output**: Formatted release notes with examples
- **Memory**: Appends to release_notes.md
- **Quality Threshold**: 80/100
- **Read this to**: Understand release documentation

### Control Layer (2 Skills)

#### 16. Critic
```
ai-company/skills/control/critic/SKILL.md
```
- **Purpose**: Quality improvement through criticism
- **Model**: Claude 3.5 Sonnet (expert evaluator)
- **How it works**:
  1. Receives any output from another skill
  2. Identifies weaknesses and gaps
  3. Assigns score 0-100
  4. Lists specific improvements
- **Auto-applied to**: write_spec, design_system, plan_tasks, implement_feature, review_code
- **Max iterations**: 5
- **Quality threshold**: 90/100 minimum to accept
- **Read this to**: Understand quality evaluation

#### 17. Verify Spec
```
ai-company/skills/control/verify_spec/SKILL.md
```
- **Purpose**: Ensure implementation meets requirements
- **Model**: Claude 3.5 Sonnet
- **How it works**:
  1. Compares implementation against spec
  2. Checks all requirements covered
  3. Identifies missing features
  4. Reports compliance percentage
- **Auto-applied to**: write_spec, design_system, implement_feature
- **Compliance levels**:
  - 95-100%: APPROVED
  - 85-95%: ACCEPTED_WITH_ISSUES
  - <85%: REJECTED (send back for fixes)
- **Read this to**: Understand spec verification

---

## 💾 Memory Files (10 Total)

### repo_summary.md
- **Updated by**: analyze_repo
- **Contains**: Project structure, tech stack, frameworks, conventions
- **Used by**: All skills for context
- **How often**: Once per project
- **Example**: Java 17, Spring Boot 3.1, PostgreSQL

### architecture.md
- **Updated by**: design_system
- **Contains**: Component diagrams, interfaces, patterns
- **Used by**: Implementation skills
- **How often**: Updated when architecture changes
- **Purpose**: Prevents architectural drift

### decisions.md
- **Updated by**: All skills
- **Contains**: Why decisions were made, alternatives considered
- **Used by**: Verify consistency with past decisions
- **How often**: Updated throughout development
- **Purpose**: Learn from previous choices

### debug_log.md
- **Updated by**: fix_bug, debug_cycle
- **Contains**: Issues found, root causes, fixes applied
- **Used by**: Prevent recurring bugs
- **How often**: Updated when bugs fixed
- **Purpose**: Build institutional knowledge

### review_log.md
- **Updated by**: review_code
- **Contains**: Code quality scores, issues found, improvements
- **Used by**: Track quality trends
- **How often**: Updated after each code review
- **Purpose**: Monitor code quality over time

### verification.md
- **Updated by**: verify_spec
- **Contains**: Spec compliance checks, missing requirements
- **Used by**: Ensure completeness
- **How often**: Updated when verifying implementations
- **Purpose**: Catch incomplete solutions

### qa.md
- **Updated by**: generate_tests
- **Contains**: Test coverage percentages, edge cases tested
- **Used by**: QA team for context
- **How often**: Updated as tests written
- **Purpose**: Track test coverage

### devops.md
- **Updated by**: configure_ci, deploy_app
- **Contains**: Infrastructure setup, deployment procedures, CI/CD config
- **Used by**: DevOps team
- **How often**: Updated when infrastructure changes
- **Purpose**: Document deployment procedures

### docs.md
- **Updated by**: update_docs
- **Contains**: Documentation changes, what was updated
- **Used by**: Track documentation updates
- **How often**: Updated as docs written
- **Purpose**: Version control for documentation

### release_notes.md
- **Updated by**: write_release_notes
- **Contains**: All releases, features, fixes, breaking changes
- **Used by**: Version history
- **How often**: Updated at each release
- **Purpose**: Track all releases

---

## 📋 Task Files

### EXAMPLE_REQUEST.md
```
ai-company/tasks/EXAMPLE_REQUEST.md
```
- **Purpose**: Template for how to create task files
- **Shows**: Format, naming convention, task structure
- **Example**: Building a Product REST API  
- **Read this to**: Learn how to create tasks

### request_001/ (When Created)
```
ai-company/tasks/request_001/
├── 01_gather_requirements.md
├── 02_write_spec.md
├── 03_analyze_repo.md
├── ...
└── 10_write_tests.md
```
- **Purpose**: Specific development request
- **Files**: Numbered sequentially (01_*, 02_*, etc.)
- **Processing**: Orchestrator runs in order
- **Result**: Memory files updated with progress

---

## 🎯 Quick Navigation by Goal

### "I want to understand the system"
1. Read: QUICKSTART.md (5 min)
2. Read: article/AI_AGENTS_BEST_PRACTICES.md (20 min)
3. Read: README.md for details (15 min)

### "I want to validate the system works"
1. Run: `python tools/inspector.py ai-company`
2. Should see: ✅ INSPECTION PASSED

### "I want to see it in action"
1. Run: `cd ai-company && python orchestrator.py 001`
2. Check: `cat memory/architecture.md` to see results

### "I want to understand a specific skill"
1. Find: `ai-company/skills/{team}/{skill}/SKILL.md`
2. Read: Goal, Input, Output, Process Steps
3. Check: Memory Update, Critic Criteria

### "I want to customize the system"
1. Edit: `ai-company/config.yaml`
2. Adjust: Thresholds, model assignments, skill applications
3. Test: `python tools/inspector.py ai-company`

### "I want to create my own request"
1. Reference: `ai-company/tasks/EXAMPLE_REQUEST.md`
2. Create: `mkdir -p ai-company/tasks/request_001`
3. Create: `01_*.md`, `02_*.md` files
4. Run: `python orchestrator.py 001`
5. Check: `cat memory/` for results

### "I'm looking for specific information"
- **How to run it?** → QUICKSTART.md
- **Why this architecture?** → article/AI_AGENTS_BEST_PRACTICES.md
- **What does each file do?** → This INDEX.md
- **How to structure tasks?** → tasks/EXAMPLE_REQUEST.md
- **Configuration options?** → config.yaml & README.md
- **Specific skill details?** → skills/{team}/{skill}/SKILL.md

---

## 📊 System Overview

```
User Request
    ↓
[20 Skills Operating in Sequence]
    ├─ Critic Loop (max 5 iterations)
    ├─ Spec Verification (90%+ compliance)
    └─ Memory Updates
    ↓
[10 Memory Files Updated]
    ├─ architecture.md
    ├─ decisions.md
    ├─ debug_log.md
    ├─ review_log.md
    └─ ... (6 more)
    ↓
✅ Complete & Verified
```

---

## ✅ Checklist to Get Started

- [ ] Read QUICKSTART.md
- [ ] Run `python tools/inspector.py ai-company`
- [ ] Run `python orchestrator.py 001` in ai-company/
- [ ] Read AI_AGENTS_BEST_PRACTICES.md
- [ ] Check memory/ folder for results
- [ ] Read specific SKILL.md files of interest
- [ ] Create your own request in tasks/

---

## 📞 Finding Help

| Need | File | Time |
|------|------|------|
| Quick start | QUICKSTART.md | 5 min |
| Full intro | article/AI_AGENTS_BEST_PRACTICES.md | 20 min |
| Complete docs | README.md | 15 min |
| File explanation | This INDEX.md | 10 min |
| Skill details | skills/{team}/{skill}/SKILL.md | 5 min |
| Task format | tasks/EXAMPLE_REQUEST.md | 5 min |
| Directory structure | DIRECTORY_TREE.md | 5 min |

---

## 🎉 Final Summary

**You have a complete, production-ready AI agent system with:**

✅ 20 specialized skills  
✅ Critic loops for quality  
✅ Spec verification  
✅ Persistent memory  
✅ Task tracking  
✅ Full documentation  
✅ Built-in validation  
✅ Ready to use immediately  

**Start with**: QUICKSTART.md

**Then read**: article/AI_AGENTS_BEST_PRACTICES.md

**Questions?** Check this INDEX.md or relevant SKILL.md file.

---

**Last updated**: March 2026  
**Version**: 1.0.0  
**Status**: ✅ Complete and ready to use
