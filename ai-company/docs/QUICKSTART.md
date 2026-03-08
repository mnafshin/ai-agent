# Quick Start Guide

## What is This?

A complete, production-ready **multi-agent AI development system** with:
- ✅ 20 specialized skills (product, architecture, dev, qa, devops, docs)
- ✅ Critic loops for iterative quality improvement
- ✅ Specification verification to catch hallucinations
- ✅ Persistent memory system
- ✅ Task ordering and tracking
- ✅ Built-in inspection and validation

## 5-Minute Setup

### 1. Check Files Exist
```bash
cd ai-agent
ls -la article/
ls -la ai-company/
ls -la tools/
```

✅ You should see:
- `article/AI_AGENTS_BEST_PRACTICES.md`
- `ai-company/skills/*/SKILL.md` (20 files)
- `ai-company/memory/*.md` (10 files)
- `ai-company/orchestrator.py`
- `tools/inspector.py`

### 2. Run Inspector
```bash
cd ai-agent
python tools/inspector.py ai-company --validate
```

✅ Expected output:
```
🔍 STARTING AI COMPANY INSPECTION
✅ INSPECTION PASSED - System is ready to use!
```

### 3. Try Orchestrator
```bash
cd ai-company
python orchestrator.py 001
```

✅ Expected output:
```
🎯 Starting AI Development Workflow: Request 001
📦 STAGE 1: Product Discovery
[... workflow runs ...]
✨ Workflow Summary
```

### 4. Review Memory
```bash
cat memory/architecture.md
cat memory/decisions.md
```

✅ Memory files are now populated with run results.

## What Does It Do?

The orchestrator runs a complete **20-agent software development workflow**:

```
Requirements → Specification → Design → Plan Tasks
    ↓              ↓              ↓          ↓
  Score 92    CRITIC LOOP      CRITIC    Verify Spec
            → 87→91→94 ✓       LOOP

Implement → Test → Debug → Review → Docs → Release
   ↓          ↓      ↓       ↓       ↓       ↓
 CRITIC     GPT    Claude  Claude   GPT    GPT
  LOOP

All decisions saved to memory/ folder
```

## Key Concepts

### 1. 20 Skills
| Team | Skills |
|------|--------|
| Product | Gather Requirements, Write Spec |
| Architecture | Analyze Repo, Design System |
| Development | Plan Tasks, Implement, Refactor, Fix Bug |
| QA | Generate Tests, Debug, Review Code |
| DevOps | Configure CI, Deploy App |
| Docs | Update Docs, Write Release Notes |
| Control | Critic, Verify Spec |

### 2. Critic Loops
Quality improvement through iteration:
```
Result → Critic Scores → Score < 90? → Improve → Loop (max 5)
```

### 3. Spec Verification
Ensures solutions actually solve the problem:
```
Implementation → Verify Against Spec → Approved/Rejected
```

### 4. Memory System
Persistent context between runs:
```
memory/
  ├── architecture.md (design decisions)
  ├── decisions.md (critical choices)
  ├── debug_log.md (issues & fixes)
  └── review_log.md (quality scores)
```

## Creating Your First Request

### 1. Create Task Folder
```bash
mkdir -p ai-company/tasks/request_001
cd ai-company/tasks/request_001
```

### 2. Create Task Files
Create numbered markdown files describing what to build. See detailed template at `ai-company/tasks/EXAMPLE_REQUEST.md`

Quick example:
```bash
cat > 01_gather_requirements.md << 'EOF'
# Task 1: Gather Requirements

## Goal
Understand user request for a REST API.

## Input
Build a REST API for managing products with create, read, update, delete operations.

## Success Criteria
Requirements documented in JSON format.
EOF
```

### 3. Run Orchestrator
```bash
python orchestrator.py 001
```

### 4. Check Results
```bash
ls memory/
cat memory/architecture.md
cat memory/debug_log.md
```

## Most Important Files

1. **Article**: `article/AI_AGENTS_BEST_PRACTICES.md`
   - Read this first to understand the philosophy

2. **Skills**: `ai-company/skills/*/SKILL.md`
   - Each skill is self-documented
   - Describes goals, inputs, outputs, quality criteria

3. **Memory**: `ai-company/memory/*.md`
   - Views architectural decisions and context
   - Updated by orchestrator runs

4. **Orchestrator**: `ai-company/orchestrator.py`
   - Main execution engine
   - Runs skills, critic loops, spec verification

5. **Inspector**: `tools/inspector.py`
   - Validates system configuration
   - Checks all skills are present

## Common Commands

```bash
# Navigate to project
cd ai-agent

# Validate system
python tools/inspector.py ai-company

# Run workflow
cd ai-company
python orchestrator.py 001

# View architecture decisions
cat memory/architecture.md

# View code reviews
cat memory/review_log.md

# View spec verification results
cat memory/verification.md

# Make orchestrator executable
chmod +x orchestrator.py
chmod +x ../tools/inspector.py
```

## Understanding the Output

When you run `python orchestrator.py 001`, you'll see:

```
🎯 Starting AI Development Workflow: Request 001
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

📦 STAGE 1: Product Discovery
────────────────────────────────
🚀 Running gather_requirements (model: claude)...
🔄 Critic Loop for write_spec
   Iteration 1: Score 87/100
   Iteration 2: Score 91/100
   ✓ Quality threshold reached!
✓ Verifying against specification...

[... more stages ...]

✨ Workflow Summary
━━━━━━━━━━━━━━━━━━
📊 Statistics:
   Total skills executed: 15
   Models used: claude, gpt, copilot
💾 Memory files updated:
   - architecture.md
   - decisions.md
   - debug_log.md
```

## Next Steps

1. **Read the Article**
   ```bash
   cat article/AI_AGENTS_BEST_PRACTICES.md
   ```
   This explains the entire architecture and philosophy.

2. **Understand Each Skill**
   ```bash
   cat ai-company/skills/product/gather_requirements/SKILL.md
   cat ai-company/skills/architecture/design_system/SKILL.md
   # ... explore all skills
   ```

3. **Create Your Own Request**
   ```bash
   mkdir -p ai-company/tasks/request_002
   # Create task files based on EXAMPLE_REQUEST.md
   python orchestrator.py 002
   ```

4. **Customize for Your Needs**
   - Add your own skills
   - Adjust critic thresholds
   - Extend verification logic

## Architecture Overview

```
┌─────────────────────────────────────────┐
│         User Request                    │
└──────────────┬──────────────────────────┘
               │
       ┌───────▼────────┐
       │  Orchestrator  │  (orchestrator.py)
       └───────┬────────┘
               │
      ┌────────┼────────┐
      │        │        │
   ┌──▼──┐  ┌─▼─┐  ┌──▼───┐
   │Load │  │Run│  │Update│
   │Skills│  │Loop│  │Memory│
   └──┬──┘  └─┬─┘  └──┬───┘
      │       │       │
   Skills  Critic  Memory
   /        Loop   /
  (20       (max   (persist
   files)   5x)    context)

      │
      ▼
┌─────────────────────┐
│  Memory Updated     │
│  - architecture.md  │
│  - decisions.md     │
│  - review_log.md    │
└─────────────────────┘
```

## Troubleshooting

**Inspector shows errors:**
```bash
python tools/inspector.py ai-company --validate
# Check output for missing files or folders
```

**Orchestrator fails:**
```bash
# Check environment variables
echo $ANTHROPIC_KEY
echo $OPENAI_KEY
echo $GITHUB_COPILOT_TOKEN

# Should all be set to your API keys
```

**Memory not updating:**
```bash
# Check if memory folder exists
ls -la ai-company/memory/

# Should show 10 .md files
```

## Need Help?

1. **Read the main article**: `article/AI_AGENTS_BEST_PRACTICES.md`
2. **Check SKILL.md files**: Each skill documents itself
3. **Review example tasks**: `ai-company/tasks/EXAMPLE_REQUEST.md`
4. **Check full README**: `README.md`

---

**Version**: 1.0.0  
**Status**: ✅ Ready to use  
**Last Updated**: March 2026
