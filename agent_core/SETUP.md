# Setup: Adding agent_core to a Project

The `agent_core/` folder is a **self-contained, opt-in agent system** that can be added to any existing project without interference.

## Quick Integration (3 steps)

### 1. Copy the Folder
```bash
# Copy agent_core/ into project root
cp -r agent_core/ /path/to/project/
```

### 2. Set API Keys
```bash
export ANTHROPIC_API_KEY="your-anthropic-key"
export OPENAI_API_KEY="your-openai-key"
```

### 3. Create First Request
```bash
cd project/agent_core
python orchestrator.py --request 001
```

## What Gets Added

```
project/
├── agent_core/              ← Everything is here (self-contained)
│   ├── docs/                ← Documentation
│   ├── skills/              ← 20 agent skills
│   ├── memory/              ← Persistent context
│   ├── tasks/               ← Workflow requests
│   ├── tools/               ← Inspector + utilities
│   ├── orchestrator.py      ← Main execution engine
│   ├── config.yaml          ← Configuration
│   ├── SETUP.md             ← This file
│   └── .gitignore           ← Excludes artifacts
├── src/                     ← Existing code (untouched)
├── tests/                   ← Existing tests (untouched)
└── README.md                ← Existing docs (untouched)
```

**Nothing in the project root changes.** ✅

## Start Using It

### Option A: Simple Request
```bash
cd agent_core
python orchestrator.py --request 001
```

### Option B: Validate Setup
```bash
cd agent_core
python tools/inspector.py --validate
```

### Option C: Read Documentation
```bash
# Start here
cat docs/QUICKSTART.md    # 5-minute overview

# Then read
cat docs/README.md        # Full technical docs

# Then deep dive  
cat docs/INDEX.md         # Navigation guide
```

## Creating a Task

Create a task file:

```bash
mkdir -p agent_core/tasks/request_001
```

File: `agent_core/tasks/request_001/spec.md`
```markdown
# Request: Build User Authentication

## Goal
Implement JWT-based authentication for the API

## Requirements
- JWT token generation and validation
- Refresh token support  
- Password hashing with bcrypt
- Rate limiting on login attempts

## Success Criteria
- All unit tests passing
- Integration tests verify token flow
- No hardcoded secrets
```

Then run:
```bash
cd agent_core
python orchestrator.py --request 001
```

## Integration with Development Workflow

### Pre-commit
```bash
# In project root .git/hooks/pre-commit
cd agent_core && python tools/inspector.py --validate
```

### CI/CD Pipeline
```yaml
# In .github/workflows/ai-review.yml
- name: Run AI Code Review
  run: |
    cd agent_core
    python orchestrator.py --request ${{ github.run_number }}
```

### Local Development
```bash
# When AI assistance is needed on a feature
cd agent_core
python orchestrator.py --request my_feature_001
```

## Customization

### Add Custom Skills
Create: `agent_core/skills/{team}/{skill}/SKILL.md`

Example:
```markdown
# Skill: SecurityAudit

MODEL: Claude
TEAM: Security
ROLE: Security Reviewer

## Goal
Identify security vulnerabilities in code

## Input
Source code to audit

## Output
JSON with vulnerabilities and remediation

## Process
1. Analyze code for OWASP top 10
2. Check dependencies for CVEs
3. Review authentication/authorization
4. Score and report

## Memory Update
→ security_audit.md
```

### Modify Configuration
Edit: `agent_core/config.yaml`

```yaml
critic_loop:
  max_iterations: 5      # Change if needed
  quality_threshold: 90  # Lower to accept earlier

spec_verification:
  compliance_threshold: 90  # Stricter/looser verification
```

## Memory Management (Preventing Bottlenecks)

As a project grows, memory files can become a bottleneck. The system provides efficient tools to prevent this.

### 1. Request-Scoped Memory (Recommended)

**Problem**: Loading a project's entire memory (500KB+) for a single 1-hour task wastes tokens and time.

**Solution**: Each request has its own isolated memory containing only relevant context.

```bash
# Create request with isolated memory (5KB instead of 500KB)
python orchestrator.py --request 001 --create-scope

# This automatically:
# - Creates tasks/request_001/memory/
# - Pulls only relevant global context
# - Keeps request isolated from other tasks
```

**Before**: Load 500KB memory per request  
**After**: Load 5KB memory per request  
**Savings**: 100x smaller context, faster execution, fewer token waste

See: `docs/REQUEST_SCOPED_MEMORY.md` for details.

### 2. Archive Old Entries (Monthly)

**Problem**: `decisions.md`, `debug_log.md` grow unbounded.

**Solution**: Archive entries older than 90 days to keep working memory lean.

```bash
# Run monthly to archive old entries
python tools/archive_memory.py

# View archive stats
python tools/archive_memory.py --stats

# Restore from archive if needed
python tools/archive_memory.py --restore archive_decisions_2026_q1.md decisions.md
```

**Result**: Active memory files stay <50KB, archives available for historical reference.

### 3. Consolidate Request Findings (After Tasks)

**Problem**: Each request learns new things that might be useful globally.

**Solution**: Consolidate important findings from request memory into global memory.

```bash
# After request_001 completes, consolidate findings
python tools/consolidate_memory.py request_001

# Or interactively review what to consolidate
python tools/consolidate_memory.py request_001 --review

# Findings merged into global memory, request archived
```

**Flow**:
1. Request runs with isolated memory (5KB)
2. Request learns new architecture decisions
3. Run consolidate → findings merged into global decisions.md
4. Request memory archived for historical reference

### 4. Memory Manager (Automatic Optimization)

If installed (`pip install pyyaml`), the system automatically optimizes memory access:

```bash
# View memory statistics
python tools/memory_manager.py

# Generate efficient context for agent
# (does this automatically, summarized instead of full history)
```

**What it does**:
- ✓ Lazy loads only needed entries
- ✓ Caches frequently accessed files
- ✓ Generates summaries instead of full history
- ✓ Ready for SQLite backend (for 10,000+ entries)

### Memory Scaling Diagram

```
Entries              Archive         Approach
-------------------
    < 1,000         (Recent)        → Request-scoped memory
                                    → Lazy loading
                                    → Memory manager
    
    1,000-5,000     (Recent)        → Archive rotation (90 days)
                    (Old)           → Consolidate requests
    
    5,000+          (Recent)        → Memory index
                    (Archived)      → SQLite backend (optional)
                    (Historical)    → Full-text search
```

## Troubleshooting

### Memory growing too fast
1. Run `python tools/archive_memory.py` monthly
2. Check if consolidate is running after requests
3. Run `python tools/memory_manager.py` to rebuild index

### "Context too large" errors
1. Use request-scoped memory: `--create-scope`
2. Run consolidation and archival
3. Check memory stats: `python tools/memory_manager.py`

### "Module not found" for pyyaml
1. Optional: `pip install pyyaml`
   - Without it, system works but memory_manager unavailable
2. Archive and consolidation tools still work



### "API key not found"
```bash
export ANTHROPIC_API_KEY="sk-..."
export OPENAI_API_KEY="sk-..."
```

### "Module not found"
```bash
pip install anthropic openai langchain   # Install dependencies
```

### Inspector validation fails
```bash
cd agent_core
python tools/inspector.py --verbose  # See detailed errors
```

### Task doesn't execute
1. Check task file format: `tasks/request_001/spec.md`
2. Verify API keys are set
3. Run inspector: `python tools/inspector.py --validate`

## Next Steps

1. **Read** `docs/QUICKSTART.md` (5 minutes)
2. **Understand** `docs/README.md` (30 minutes)  
3. **Create** a task in `tasks/request_001/`
4. **Run** `python orchestrator.py --request 001`
5. **Iterate** based on results

## Important Notes

- ✅ **Non-invasive**: Only `agent_core/` folder added to the project
- ✅ **Optional**: If you don't use it, delete the folder—no cleanup needed
- ✅ **Portable**: Copy to other projects as-is
- ✅ **Isolated**: Source code stays untouched
- ✅ **Gitignore**: Artifacts stored in `.gitignore` patterns

---

**Ready to start?** 

```bash
cd agent_core
cat docs/QUICKSTART.md
```
