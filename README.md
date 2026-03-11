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
├── agent_core/         ← The actual agent system (copy to projects)
│   ├── docs/           ← Full documentation
│   ├── skills/         ← 20 specialized agent skills
│   ├── memory/         ← Persistent context between runs
│   ├── tasks/          ← Workflow requests
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
Add to an existing project:
```bash
cp -r agent_core/ /path/to/project/
```

### 3. Integrate (5 minutes)
See: `agent_core/SETUP.md`

### 4. Use It (ongoing)
Create tasks and run workflows:
```bash
cd agent_core
python orchestrator.py --request 001
```

## Documentation

All documentation is in `agent_core/docs/`:

- **`QUICKSTART.md`** — 5-minute setup guide
- **`README.md`** — Complete technical documentation
- **`SETUP.md`** — Integration with existing projects
- **`INDEX.md`** — Navigation guide for all files
- **`DIRECTORY_TREE.md`** — Complete file structure

Start here:
```bash
cat agent_core/docs/QUICKSTART.md
```

## Key Features

### 1. Critic Loops with Adaptive Thresholds
Self-improving outputs — threshold adjusts by request type:
```
hotfix → 75/100   |   feature → 90/100   |   security_patch → 98/100
Generate → Evaluate → Score < threshold? → Improve & Loop
```

### 2. Dynamic Team Routing
Skips irrelevant teams automatically:
```
bug_fix   → architecture → development → qa
hotfix    → development → devops
feature   → all 6 teams
```

### 3. Parallel Execution
QA + Documentation run concurrently after development:
```
development → [QA ║ Docs] (parallel) → devops
```

### 4. Specification Verification
Every output verified against original requirements:
```
Implementation → Verify Against Spec → Missing Requirements? → Send Back
```

### 5. Persistent Memory + Auto-Pruning
Architectural decisions stored between runs, auto-pruned at 10 KB:
```
memory/
  ├── architecture.md     → System design
  ├── decisions.md        → Why decisions were made
  ├── debug_log.jsonl     → Structured per-skill log
  ├── critic_patterns.md  → What caused low scores (learns over time)
  └── archive/            → Auto-archived old entries
```

### 6. Budget Guard
Hard spending limit per run — configurable in `config.yaml`:
```yaml
budget:
  max_usd_per_run: 2.00
  warn_at_usd:     1.50
```

### 7. Run Dashboard
HTML report generated after every run in `outputs/`:
```
outputs/run_001_report.html  ← skills, models, cost, timestamps
```

### 8. 20 Specialized Skills + Task Templates
Organized into 7 teams. Start from templates:
```
tasks/_templates/
  ├── bug_fix.md
  ├── new_feature.md
  └── refactor.md
```

### 9. Task Status Tracking
Live `.status.json` written for every running request:
```json
{"step": 3, "current_skill": "review_code", "state": "running", "score": 87}
```

### 10. Expanded Inspector CLI
```bash
python inspector.py . --validate            # full validation
python inspector.py . --dry-run 001         # simulate without API calls
python inspector.py . --cost-estimate 001   # estimate spend before running
python inspector.py . --diff 001            # show memory changes after run
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
# Add to a project
cp -r agent_core/ /path/to/project/

# Project structure stays intact
project/
  ├── agent_core/   ← Only this is new
  ├── src/          ← Untouched
  ├── tests/        ← Untouched
  └── README.md     ← Untouched
```

**Nothing to remove if you decide not to use it** — just delete the `agent_core/` folder.

## Getting Started

### Prerequisites

**Auth: You need ONE of these setups:**

**Option A (recommended):** GitHub Copilot token only
```bash
export GITHUB_COPILOT_TOKEN=gho_your-token-here   # covers Claude + GPT
```

**Option B (direct APIs):** Separate provider keys
```bash
export ANTHROPIC_KEY=sk-ant-xxx   # Claude only
export OPENAI_KEY=sk-xxx           # GPT only
```

**Option C (hybrid):** Mix both — provider keys override Copilot per-provider
```bash
export GITHUB_COPILOT_TOKEN=gho_xxx   # fallback for both
export ANTHROPIC_KEY=sk-ant-xxx       # overrides Copilot for Claude
# OPENAI_KEY not set → uses Copilot for GPT
```

### One-Command Setup

Setup scripts detect existing keys and prompt for Copilot token if needed:

```bash
# Linux / macOS
bash setup.sh

# Windows PowerShell
.\setup.ps1
```

Both scripts:
1. Create Python venv
2. Install dependencies from `requirements.txt`
3. Detect `GITHUB_COPILOT_TOKEN` / `ANTHROPIC_KEY` / `OPENAI_KEY` from environment
4. Prompt for Copilot token if nothing is set
5. Write `.env` with detected keys
6. Validate setup

### Manual Setup

If you prefer manual setup:
```bash
python -m venv .venv
source .venv/bin/activate          # Linux/macOS
# or: .\.venv\Scripts\Activate.ps1  # Windows

pip install -r requirements.txt
cp .env.example .env
# Edit .env with your GITHUB_COPILOT_TOKEN
```

### First Step
```bash
cd agent_core
cat docs/QUICKSTART.md
```

## File Contents

- **`agent_core/`** — The complete multi-agent system (copy this to any project)
- **`article/`** — Comprehensive article explaining the 20-skill architecture
- **`README.md`** — This file

## Next Steps

1. Run `bash setup.sh` (Linux/macOS) or `.\setup.ps1` (Windows) — sets up venv + deps
2. Edit `.env` with your API keys
3. Read `agent_core/docs/QUICKSTART.md` (5 min)
4. Run `python agent_core/tools/inspector.py agent_core --validate` — verify setup
5. Pick a template from `agent_core/tasks/_templates/` and create `tasks/request_001/`
6. Execute: `python agent_core/orchestrator.py 001`
7. Open `outputs/run_001_report.html` to review the run dashboard

---

**Questions?** See `agent_core/docs/INDEX.md` for navigation.

**Ready?** See `agent_core/SETUP.md` for integration instructions.
