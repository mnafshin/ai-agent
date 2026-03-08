# AI Agents Best Practices - Complete Implementation

This directory contains a complete, production-ready implementation of the AI agent best practices from the ChatGPT conversation on building autonomous AI development systems.

## Overview

This system implements a **20-skill multi-agent architecture** that simulates a complete software development team:

- **Product Team** - Requirements gathering and specification
- **Architecture Team** - System design and planning
- **Development Team** - Implementation and refactoring
- **QA Team** - Testing and code review
- **DevOps Team** - CI/CD and deployment
- **Documentation Team** - Technical docs and release notes
- **Control Layer** - Critic loops and specification verification

## Key Innovations

### 1. Critic Loops (Self-Improvement)
Each important skill runs a feedback loop:
```
Generate → Critique → Score → Improve (if < 90) → Repeat (max 5)
```

### 2. Specification Verification
Every implementation is verified against requirements:
```
Output → Verify Against Spec → Approved/Rejected
```

### 3. Persistent Memory
Architectural decisions and context stored across runs:
```
memory/
  ├── architecture.md      # Design decisions
  ├── decisions.md         # Critical choices
  ├── debug_log.md         # Issues and fixes
  └── review_log.md        # Code quality tracking
```

### 4. Task Ordering
Work organized in numbered, sequential files:
```
tasks/request_001/
  ├── 01_gather_requirements.md
  ├── 02_write_spec.md
  ├── 03_design_architecture.md
  └── ...
```

## Directory Structure

```
ai-agent/
  ├── article/
  │   └── AI_AGENTS_BEST_PRACTICES.md       # Main article
  │
  ├── ai-company/                            # Complete implementation
  │   ├── skills/                            # 20 SKILL.md files
  │   │   ├── product/
  │   │   │   ├── gather_requirements/SKILL.md
  │   │   │   └── write_spec/SKILL.md
  │   │   ├── architecture/
  │   │   ├── development/
  │   │   ├── qa/
  │   │   ├── devops/
  │   │   ├── docs/
  │   │   └── control/
  │   │
  │   ├── memory/                            # Persistent context
  │   │   ├── repo_summary.md
  │   │   ├── architecture.md
  │   │   ├── decisions.md
  │   │   ├── debug_log.md
  │   │   ├── review_log.md
  │   │   ├── verification.md
  │   │   ├── qa.md
  │   │   ├── devops.md
  │   │   ├── docs.md
  │   │   └── release_notes.md
  │   │
  │   ├── tasks/                             # Development tasks
  │   │   ├── EXAMPLE_REQUEST.md
  │   │   └── request_001/                   # Example request
  │   │       ├── 01_task.md
  │   │       ├── 02_task.md
  │   │       └── ...
  │   │
  │   ├── orchestrator.py                    # Main executor
  │   └── config.yaml                        # Configuration
  │
  └── tools/
      └── inspector.py                       # Validation tool
```

## Quick Start

### 1. Install Prerequisites
```bash
# Python 3.11+
python --version

# Install dependencies (optional)
pip install anthropic openai
```

### 2. Set Environment Variables
```bash
export ANTHROPIC_KEY="sk-ant-..."
export OPENAI_KEY="sk-..."
export GITHUB_COPILOT_TOKEN="..."
```

### 3. Validate Configuration
```bash
cd ai-company
python ../tools/inspector.py .
```

Expected output:
```
✅ INSPECTION PASSED - System is ready to use!
```

### 4. Run Orchestrator
```bash
# Run with a request ID
python orchestrator.py 001

# Output shows:
# 🚀 Running gather_requirements (model: claude)...
# 🔄 Critic Loop for write_spec
# 🏗️  STAGE 2: Architecture Design
# ... and so on
```

### 5. Check Memory Updates
```bash
# View updated memory files
cat memory/architecture.md
cat memory/decisions.md
cat memory/debug_log.md
```

## Using the System

### Creating a New Request

1. Create a request folder:
```bash
mkdir -p tasks/request_001
```

2. Create numbered task files:
```bash
# 01_gather_requirements.md
# 02_write_spec.md
# 03_analyze_repository.md
# ... etc
```

See [tasks/EXAMPLE_REQUEST.md](ai-company/tasks/EXAMPLE_REQUEST.md) for task format.

3. Run orchestrator:
```bash
python orchestrator.py 001
```

### Understanding SKILL.md Files

Each skill is defined in a SKILL.md file with:

```markdown
# Skill: [Name]

## Metadata
- MODEL: Claude / GPT / Copilot
- TEAM: Product / Architecture / etc
- ROLE: Specific role

## Goal
Clear, single-sentence goal

## Input
What inputs the skill expects

## Process Steps
1. Step 1
2. Step 2
...

## Output Format
Expected output structure

## Memory Update
How memory files are updated

## Critic Criteria
Quality evaluation criteria

## Notes
Additional guidance
```

### Memory System

Memory files are persistent across runs. Agents read from them before acting:

- **repo_summary.md** - Project structure, tech stack, conventions
- **architecture.md** - System design and components
- **decisions.md** - Critical architectural choices
- **debug_log.md** - Issues found and fixed
- **review_log.md** - Code quality scores and reviews
- **verification.md** - Spec compliance checks
- **qa.md** - Test coverage and QA tracking
- **devops.md** - Infrastructure and deployments
- **docs.md** - Documentation updates
- **release_notes.md** - Release history

### Critic Loops

For quality-critical skills, the system runs iterative improvement:

```python
for iteration in range(MAX_ITERATIONS):
    result = generate()
    critique = critic(result)
    score = extract_score(critique)
    
    if score >= THRESHOLD:
        return result
    
    result = improve(result, critique)
```

Applies to:
- `write_spec` - High quality spec is critical
- `design_system` - Architecture impacts all code
- `plan_tasks` - Task quality affects implementation
- `implement_feature` - Code quality matters
- `review_code` - Reviews catch issues

### Specification Verification

Every implementation verified against spec:

```python
verification = verify_spec(solution, specification)

if not verification["valid"]:
    improvements = verification["missing_requirements"]
    solution = refine(solution, improvements)
```

## Inspector Tool

Validate your system configuration:

```bash
# Full validation
python inspector.py . --validate

# Checks:
# ✓ All directories exist
# ✓ All 20 skills present
# ✓ All SKILL.md files have required sections
# ✓ Memory files initialized
# ✓ Environment variables set
# ✓ Orchestrator functional
```

## Configuration

Edit `config.yaml` to customize:

```yaml
# Max iterations before accepting lower quality
critic_loop:
  max_iterations: 5
  quality_threshold: 90

# Which skills use critic loop
spec_verification:
  apply_to:
    - write_spec
    - design_system
    - implement_feature

# API keys and models
models:
  claude: claude-3-5-sonnet
  gpt: gpt-4-turbo
  copilot: github-copilot
```

## The 20 Skills

### Product Team (2 skills)
1. **Gather Requirements** - Parse user requests into structured requirements
2. **Write Specification** - Create formal specification with acceptance criteria

### Architecture Team (3 skills)
3. **Analyze Repository** - Understand existing code structure and conventions
4. **Design System** - Create architecture design for new features
5. **Update Architecture Memory** - Persist architectural decisions

### Development Team (4 skills)
6. **Plan Tasks** - Break architecture into atomic development tasks
7. **Implement Feature** - Write code for a task (uses Copilot)
8. **Refactor Code** - Safely refactor existing code
9. **Fix Bug** - Debug and fix issues

### QA Team (3 skills)
10. **Generate Tests** - Create unit and integration tests
11. **Debug Cycle** - Fix build failures and test issues
12. **Review Code** - Evaluate code quality and security

### DevOps Team (2 skills)
13. **Configure CI** - Generate CI/CD pipeline
14. **Deploy App** - Create deployment scripts

### Documentation Team (2 skills)
15. **Update Docs** - Update technical documentation
16. **Write Release Notes** - Create release notes

### Control Layer (2 skills)
17. **Critic** - Evaluate and improve quality of any output
18. **Verify Spec** - Verify implementation meets specification

## Workflow Example

```
User: "Build a REST API for products"
  ↓
[Product Team]
  GatherRequirements → score 92
  WriteSpec → CRITIC LOOP → score 87→91→94 ✓
  VerifySpec → PASSED ✓
  ↓
[Architecture Team]
  AnalyzeRepo → score 88
  DesignSystem → CRITIC LOOP → score 84→89→92 ✓
  VerifySpec → PASSED ✓
  ↓
[Development Team]
  PlanTasks → CRITIC LOOP → score 89
  VerifySpec → PASSED ✓
  ↓
[For each task]
  ImplementFeature → CRITIC LOOP → score 85
  VerifySpec → PASSED ✓
  GenerateTests → score 88
  DebugCycle → score 95 ✓
  ReviewCode → score 91
  ↓
[Documentation Team]
  UpdateDocs → score 86
  WriteReleaseNotes → score 89
  ↓
[Memory Updated]
  ✓ architecture.md
  ✓ decisions.md
  ✓ review_log.md
  ↓
✨ Complete and ready for deployment!
```

## Best Practices

### ✅ DO

1. **Run inspector before first use** - Validate configuration
2. **Keep memory files updated** - Critical for consistency
3. **Order tasks sequentially** - Prevents forgotten work
4. **Use critic loops on important skills** - Architecture, specs, implementation
5. **Always verify against spec** - Catch hallucinations early
6. **Log everything** - Helps with debugging and learning
7. **Review critic feedback** - Learn from improvements

### ❌ DON'T

1. ~~Skip spec verification~~ → Always verify against requirements
2. ~~Use same model for all skills~~ → Match models to tasks
3. ~~Skip critic loops~~ → Use on important quality gates
4. ~~Ignore memory~~ → Update persistently
5. ~~Create unordered tasks~~ → Use sequential numbering
6. ~~Trust first output~~ → Iterate until threshold met

## Extending the System

### Add a New Skill

1. Create folder structure:
```bash
mkdir -p skills/team/new_skill
```

2. Create SKILL.md:
```bash
# Copy from existing skill and customize
cp skills/product/gather_requirements/SKILL.md skills/team/new_skill/SKILL.md
```

3. Update orchestrator.py to register skill

4. Run inspector to validate

### Add New Workflow

Edit `config.yaml`:
```yaml
workflows:
  new_workflow:
    - skill_1
    - skill_2
    - skill_3
```

## Troubleshooting

### Orchestrator fails to start
```bash
# Check Python version
python --version  # Need 3.11+

# Check environment variables
echo $ANTHROPIC_KEY
echo $OPENAI_KEY
```

### Inspector shows errors
```bash
# Run inspector for details
python inspector.py . --validate

# Check specific team
ls -la skills/product/
ls -la skills/product/gather_requirements/
```

### Memory files not updating
Check orchestrator output for errors:
```bash
python orchestrator.py 001 2>&1 | tee orchestrator.log
grep -i error orchestrator.log
```

## Files Reference

| File | Purpose |
|------|---------|
| `article/AI_AGENTS_BEST_PRACTICES.md` | Main article explaining best practices |
| `ai-company/skills/*/SKILL.md` | 20 skill definitions |
| `ai-company/memory/*.md` | Persistent context files |
| `ai-company/orchestrator.py` | Main execution engine |
| `ai-company/config.yaml` | Configuration |
| `ai-company/tasks/*/` | Development tasks |
| `tools/inspector.py` | Validation tool |

## Performance Tips

1. **Cache repository analysis** - Reuse from memory
2. **Parallelize independent tasks** - Generate tests + review code together
3. **Minimize context in each LLM call** - Reference memory instead of pasting large docs
4. **Reuse Copilot token** - Cheaper than calling APIs directly

## Next Steps

1. ✅ Read the article: [AI_AGENTS_BEST_PRACTICES.md](article/AI_AGENTS_BEST_PRACTICES.md)
2. ✅ Run inspector: `python tools/inspector.py ai-company`
3. ✅ Try orchestrator: `python ai-company/orchestrator.py 001`
4. ✅ Create your first request in `ai-company/tasks/request_001/`
5. ✅ Monitor progress in `ai-company/memory/`

## Resources

- [Original ChatGPT Conversation](https://chatgpt.com/share/69ad3a56-5db8-8000-a1d4-1343483328fd)
- [Anthropic: Building Effective Agents](https://www.anthropic.com/research/building-effective-agents)
- [Claude API Docs](https://docs.anthropic.com/en/docs/claude-code/sub-agents)
- [LangGraph Framework](https://langchain-ai.github.io/langgraph/)

## License

Open source - feel free to use and modify for your projects.

---

**Last Updated**: March 2026  
**Version**: 1.0.0
