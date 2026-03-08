# AI Agent Best Practices System

This repository contains a **production-ready multi-agent system** designed to automate software development workflows using specialized AI models.

## What Is This?

A comprehensive guide and implementation package for building autonomous AI agents that:
- ✅ Separate concerns (Product, Architecture, Dev, QA, DevOps, Docs teams)
- ✅ Use critic loops for self-improvement (max 5 iterations, 90/100 threshold)
- ✅ Verify outputs against specifications
- ✅ Maintain persistent memory across runs
- ✅ Handle complex multi-step workflows deterministically

## Structure

```
├── ai-company/          ← The actual agent system (copy this to your projects)
│   ├── docs/           ← Full documentation
│   ├── skills/         ← 20 specialized agent skills
│   ├── memory/         ← Persistent context between runs
│   ├── tasks/          ← Your workflow requests
│   ├── tools/          ← Inspector validation tool
│   ├── orchestrator.py ← Main execution engine
│   ├── config.yaml     ← Configuration
│   ├── SETUP.md        ← Integration instructions
│   └── .gitignore      ← Git exclusions
├── article/            ← Deep-dive article explaining the system
└── README.md           ← This file
```

## Quick Start

### 1. Read the Article (10 minutes)
Understand the philosophy and design:
```bash
cat article/AI_AGENTS_BEST_PRACTICES.md
```

### 2. Copy the System (1 minute)
Add to your existing project:
```bash
cp -r ai-company/ /path/to/your/project/
```

### 3. Integrate (5 minutes)
See: `ai-company/SETUP.md`

### 4. Use It (ongoing)
Create tasks and run workflows:
```bash
cd ai-company
python orchestrator.py --request 001
```

## Documentation

All documentation is in `ai-company/docs/`:

- **`QUICKSTART.md`** — 5-minute setup guide
- **`README.md`** — Complete technical documentation
- **`SETUP.md`** — Integration with existing projects
- **`INDEX.md`** — Navigation guide for all files
- **`DIRECTORY_TREE.md`** — Complete file structure

Start here:
```bash
cat ai-company/docs/QUICKSTART.md
```

## Key Features

### 1. Critic Loops
Self-improving outputs through iterative refinement:
```
Generate → Evaluate (score 0-100) → Score < 90? → Improve & Loop
```

### 2. Specification Verification
Every output verified against original requirements:
```
Implementation → Verify Against Spec → Missing Requirements? → Send Back
```

### 3. Persistent Memory
Architectural decisions stored between runs:
```
memory/
  ├── architecture.md    → System design
  ├── decisions.md       → Why decisions were made
  ├── debug_log.md       → Issues found & fixed
  └── ... (10 total)
```

### 4. 20 Specialized Skills
Organized into 7 teams:
- **Product Team** (2 skills): Requirements gathering, spec writing
- **Architecture Team** (2 skills): Code analysis, system design
- **Development Team** (4 skills): Task planning, implementation, refactoring, debugging
- **QA Team** (3 skills): Test generation, debugging, code review
- **DevOps Team** (2 skills): CI/CD configuration, deployment
- **Documentation Team** (2 skills): Technical docs, release notes
- **Control Layer** (2 skills): Critic loops, spec verification

### 5. Deterministic Task Ordering
Tasks processed sequentially (no forgetting):
```
tasks/request_001/
  ├── 01_analyze_requirements.md
  ├── 02_design_architecture.md
  ├── 03_implement_feature.md
  └── 04_generate_tests.md
```

## System Architecture

```
User Request
    ↓
Product Team → Requirements + Specification (with CRITIC LOOP)
    ↓
Architecture Team → System Design (with CRITIC LOOP + SPEC VERIFICATION)
    ↓
Development Team → Implementation (with CRITIC LOOP + SPEC VERIFICATION)
    ↓
QA Team → Tests + Review (with CRITIC LOOP)
    ↓
DevOps Team → CI/CD + Deployment
    ↓
Documentation Team → Docs + Release Notes
    ↓
Persistent Memory Updated (decisions, debug logs, review scores)
```

## When to Use This System

### ✅ Perfect For
- Production systems needing reproducible quality
- Complex workflows with multiple teams
- Projects you build repeatedly
- Systems requiring audit trails
- High-stakes code that needs verification

### ⏩ Not Ideal For
- One-off quick prototypes (use Claude Code)
- Interactive human-guided development (use Cursor)
- Simple automation (use LangGraph)

See `article/` for complete comparison of alternatives.

## Use as Opt-In Addition

This system is designed to be added to existing projects without interference:

```bash
# Add to your project
cp -r ai-company/ /path/to/your/project/

# Your project structure stays intact
your-project/
  ├── ai-company/   ← Only this is new
  ├── src/          ← Untouched
  ├── tests/        ← Untouched
  └── README.md     ← Untouched
```

**Nothing to remove if you decide not to use it** — just delete the `ai-company/` folder.

## Getting Started

### Prerequisites
```bash
export ANTHROPIC_API_KEY="your-key"
export OPENAI_API_KEY="your-key"
```

### First Step
```bash
cd ai-company
cat docs/QUICKSTART.md
```

## File Contents

- **`ai-company/`** — The complete multi-agent system (copy this to any project)
- **`article/`** — Comprehensive article explaining the 20-skill architecture
- **`README.md`** — This file

## Next Steps

1. Read `ai-company/docs/QUICKSTART.md` (5 min)
2. Read `article/AI_AGENTS_BEST_PRACTICES.md` (15 min)
3. Run `python ai-company/tools/inspector.py --validate` (verify setup)
4. Create your first task in `ai-company/tasks/request_001/`
5. Execute: `python ai-company/orchestrator.py --request 001`

---

**Questions?** See `ai-company/docs/INDEX.md` for navigation.

**Ready?** See `ai-company/SETUP.md` for integration instructions.
