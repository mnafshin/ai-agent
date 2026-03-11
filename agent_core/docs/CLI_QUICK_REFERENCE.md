# Agent CLI - Quick Reference

## Command Overview

```
agent execute [TASK]         # Run all 20 agents
agent review [CODE_INPUT]    # Review code/diffs
agent analyze [CODE]         # Analyze code structure
agent status                 # System status
```

## Installation

```bash
cd agent_core
pip install -e .
```

## Usage Examples

### Execute All Agents
```bash
# From file
agent execute task.md

# From stdin
cat task.md | agent execute

# Piped from clipboard
pbpaste | agent execute
```

### Review Code
```bash
# From file
agent review < src/app.py

# GitHub PR
gh pr diff | agent review

# GitLab MR
glab mr diff | agent review

# With verbose output
gh pr diff | agent review --verbose
```

### Analyze Code
```bash
# From file
agent analyze < code.py

# Specify language
echo "function foo() {}" | agent analyze --language javascript
```

### Output Formats
```bash
# JSON (default, for piping)
agent execute task.md --format json

# Text (default, human readable)
agent execute task.md --format text

# Parse with jq
agent execute task.md | jq '.results.architect'
```

## CI/CD Integration

### GitHub Actions
```yaml
- name: Review PR
  run: |
    gh pr diff | agent review > review.json
    SUMMARY=$(jq -r '.results.summary' review.json)
    gh pr comment --body "$SUMMARY"
```

### GitLab CI
```yaml
review:
  script:
    - glab mr diff | agent review --format json
```

### Git Pre-Push Hook
```bash
#!/bin/bash
git diff HEAD~1 | agent review --verbose || exit 1
```

## Advanced Features

### Request Scoping
```bash
# Each execution gets isolated memory
agent execute --request-id feature/auth task.md
```

### Verbose Logging
```bash
agent execute task.md --verbose
```

### Memory Consolidation
Results are automatically consolidated into global memory after execution.

## Output Structure

```json
{
  "status": "completed",
  "request_id": "cli_20260308_144532",
  "timestamp": "2026-03-08T14:45:32",
  "agents": 20,
  "results": {
    "architect": { ... },
    "critic": { ... },
    ...
  }
}
```

## Common Workflows

### Review PR and Comment
```bash
gh pr diff | agent review --format json | jq -r '.results.summary' | \
  gh pr comment --body "$(cat)"
```

### Analyze Multiple Files
```bash
for file in src/**/*.py; do
  echo "Analyzing $file..."
  agent analyze < "$file" | jq -r '.results.architecture'
done
```

### Save Task Results
```bash
agent execute task.md > results_$(date +%s).json
```

### Extract Specific Agent Output
```bash
agent execute task.md | jq '.results.architect.recommendations'
```

## Troubleshooting

| Issue | Solution |
|-------|----------|
| `command not found: agent` | Run `pip install -e .` in agent_core directory |
| No input provided | Use `agent execute task.md` or `cat input \| agent execute` |
| API key errors | Set `ANTHROPIC_API_KEY` and `OPENAI_API_KEY` env vars |
| JSON parse errors | Use `jq .` to validate output |

## Full Documentation

See [CLI_USAGE.md](CLI_USAGE.md) for complete guide with workflows, examples, and advanced usage.
