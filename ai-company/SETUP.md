# Setup: Adding ai-company to Your Project

The `ai-company/` folder is a **self-contained, opt-in agent system** that can be added to any existing project. It doesn't interfere with your project structure.

## Quick Integration (3 steps)

### 1. Copy the Folder
```bash
# Copy ai-company/ into your project root
cp -r ai-company/ /path/to/your/project/
```

### 2. Set API Keys
```bash
export ANTHROPIC_API_KEY="your-anthropic-key"
export OPENAI_API_KEY="your-openai-key"
```

### 3. Create Your First Request
```bash
cd your-project/ai-company
python orchestrator.py --request 001
```

## What Gets Added

```
your-project/
├── ai-company/              ← Everything is here (self-contained)
│   ├── docs/                ← Documentation
│   ├── skills/              ← 20 agent skills
│   ├── memory/              ← Persistent context
│   ├── tasks/               ← Your requests
│   ├── tools/               ← Inspector + utilities
│   ├── orchestrator.py      ← Main execution engine
│   ├── config.yaml          ← Configuration
│   ├── SETUP.md             ← This file
│   └── .gitignore           ← Excludes artifacts
├── src/                     ← Your existing code (untouched)
├── tests/                   ← Your existing tests (untouched)
└── README.md                ← Your existing docs (untouched)
```

**Nothing in your project root changes.** ✅

## Start Using It

### Option A: Simple Request
```bash
cd ai-company
python orchestrator.py --request 001
```

### Option B: Validate Setup
```bash
cd ai-company
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

## Creating Your First Task

Create a task file:

```bash
mkdir -p ai-company/tasks/request_001
```

File: `ai-company/tasks/request_001/spec.md`
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
cd ai-company
python orchestrator.py --request 001
```

## Integration with Your Workflow

### Pre-commit
```bash
# In your project root .git/hooks/pre-commit
cd ai-company && python tools/inspector.py --validate
```

### CI/CD Pipeline
```yaml
# In your .github/workflows/ai-review.yml
- name: Run AI Code Review
  run: |
    cd ai-company
    python orchestrator.py --request ${{ github.run_number }}
```

### Local Development
```bash
# When you want AI assistance on a feature
cd ai-company
python orchestrator.py --request my_feature_001
```

## Customization

### Add Your Own Skill
Create: `ai-company/skills/{team}/{skill}/SKILL.md`

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
Edit: `ai-company/config.yaml`

```yaml
critic_loop:
  max_iterations: 5      # Change if needed
  quality_threshold: 90  # Lower to accept earlier

spec_verification:
  compliance_threshold: 90  # Stricter/looser verification
```

## Troubleshooting

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
cd ai-company
python tools/inspector.py --verbose  # See detailed errors
```

### Task doesn't execute
1. Check task file format: `tasks/request_001/spec.md`
2. Verify API keys are set
3. Run inspector: `python tools/inspector.py --validate`

## Next Steps

1. **Read** `docs/QUICKSTART.md` (5 minutes)
2. **Understand** `docs/README.md` (30 minutes)  
3. **Create** your first task in `tasks/request_001/`
4. **Run** `python orchestrator.py --request 001`
5. **Iterate** based on results

## Important Notes

- ✅ **Non-invasive**: Only `ai-company/` folder added to your project
- ✅ **Optional**: If you don't use it, delete the folder—no cleanup needed
- ✅ **Portable**: Copy to other projects as-is
- ✅ **Isolated**: Your source code stays untouched
- ✅ **Gitignore**: Artifacts stored in `.gitignore` patterns

---

**Ready to start?** 

```bash
cd ai-company
cat docs/QUICKSTART.md
```
