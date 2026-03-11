# CLI Agent - Usage Guide

The CLI interface makes it easy to orchestrate all 20 agents from the command line and integrate with GitHub/GitLab workflows.

## Installation

```bash
cd agent_core
pip install -e .
```

This creates an `agent` command available globally.

## Quick Start

### 1. Execute All 20 Agents on a Task

Run the entire "software company" on a single task:

```bash
# From a file
agent execute task.md

# From stdin
cat task.md | agent execute

# From clipboard (macOS)
pbpaste | agent execute
```

**Output**: JSON with results from all 20 agents
```json
{
  "status": "completed",
  "request_id": "cli_20260308_144532",
  "timestamp": "2026-03-08T14:45:32.123456",
  "agents": 20,
  "results": {
    "architect": { "analysis": "..." },
    "critic": { "review": "..." },
    ...
  }
}
```

### 2. Review Code or Diffs

Use the review agent for code analysis:

```bash
# Review a file
agent review < src/app.py

# Review from stdin
cat src/module.js | agent review

# Review a PR (GitHub)
gh pr diff | agent review

# Review an MR (GitLab)
glab mr diff | agent review

# Review with verbose output
gh pr diff | agent review --verbose
```

### 3. Analyze Code Structure

Use the architect agent for deep code analysis:

```bash
# Analyze a file
agent analyze < src/app.py

# Specify language
echo "function foo() { return 42; }" | agent analyze --language javascript

# Analyze project structure
cat src/**/*.py | agent analyze --language python
```

### 4. Check System Status

View available agents and system health:

```bash
agent status
agent status --format json
```

## Workflow Examples

### GitHub PR Review Workflow

```bash
# Review PR before merging
gh pr diff | agent review --format json | jq '.results.issues'

# Review and save report
gh pr diff | agent review > review_report.json

# Add review as comment (manual step)
gh pr comment --body "$(agent review < diff.txt | jq -r '.results.summary')"
```

### GitLab MR Workflow

```bash
# Quick MR review
glab mr diff | agent review

# Get structured feedback
glab mr diff | agent review --format json | jq '.results'

# Review specific file in MR
glab mr diff | agent review --file src/main.py
```

### Feature Task Execution

```bash
# Execute full task with all 20 agents
agent execute feature_request.md > feature_result.json

# Get specific agent output
agent execute task.md | jq '.results.architect'

# Save detailed results for team review
agent execute << EOF > task_analysis.json
Feature: Add user authentication
Requirements:
  - Support OAuth2
  - Rate limiting
  - Audit logging
EOF
```

### Code Review Pipeline

```bash
# 1. Get PR diff
gh pr diff > pr.diff

# 2. Run review agent
agent review < pr.diff > review.json

# 3. Parse issues
cat review.json | jq '.results.issues | length'

# 4. Extract summary
cat review.json | jq -r '.results.summary'
```

## Output Formats

### JSON Format (default)

```bash
agent execute task.md --format json
```

Perfect for:
- Piping to other tools (`jq`, `grep`)
- Programmatic processing
- Integration with CI/CD pipelines

### Text Format

```bash
agent execute task.md --format text
```

Perfect for:
- Human reading in terminal
- Quick status checks
- Documentation

## Request Scoping

Each CLI execution creates a scoped request with isolated memory:

```bash
# Custom request ID
agent execute task.md --request-id feature/auth

# Auto-generated request ID
agent execute task.md
# Creates: cli_20260308_144532
```

Memory is automatically consolidated after execution, so findings persist across tasks.

## Advanced: Piping with jq

```bash
# Get all issues found
gh pr diff | agent review | jq '.results.issues[]'

# Count findings by severity
agent execute task.md | jq '.results | keys[] as $agent | {($agent): .[$agent] | length}'

# Extract architect recommendations
agent analyze < code.py | jq '.results.architect.recommendations'

# Filter to critical issues only
agent execute task.md | jq '.results[] | select(.severity == "critical")'
```

## Verbose Mode

Get detailed agent logs:

```bash
agent execute task.md --verbose
agent review < code.py --verbose
```

Outputs detailed information about:
- Each agent's processing
- Memory operations
- Performance metrics
- Consolidation details

## Environment Variables

```bash
# API keys (required)
export ANTHROPIC_API_KEY="sk-ant-..."
export OPENAI_API_KEY="sk-..."

# Optional: memory config
export MEMORY_ENABLED=true
export REQUEST_SCOPE_ENABLED=true
```

## Integration Examples

### GitHub Actions

```yaml
name: AI Code Review
on: [pull_request]

jobs:
  review:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      
      - name: Install agent CLI
        run: |
          cd agent_core
          pip install -e .
      
      - name: Review PR
        run: |
          gh pr diff | agent review --format json > review.json
        env:
          GH_TOKEN: ${{ secrets.GITHUB_TOKEN }}
          ANTHROPIC_API_KEY: ${{ secrets.ANTHROPIC_API_KEY }}
      
      - name: Comment on PR
        run: |
          SUMMARY=$(jq -r '.results.summary' review.json)
          gh pr comment --body "## AI Review\n$SUMMARY"
```

### GitLab CI

```yaml
review:
  script:
    - pip install -e agent_core/
    - glab mr diff | agent review --format json > review.json
    - SUMMARY=$(jq -r '.results.summary' review.json)
    - echo "Review complete: $SUMMARY"
  artifacts:
    reports:
      annotation: review.json
```

### Local Git Hook

```bash
# .git/hooks/pre-push (executable)
#!/bin/bash
echo "Running AI review before push..."
git diff HEAD~1 | agent review --verbose

if [ $? -ne 0 ]; then
  echo "Review failed, push cancelled"
  exit 1
fi
```

## Troubleshooting

### Command not found

```bash
# Ensure installation
pip install -e agent_core/

# Check installation
which agent
agent --version
```

### No input provided

```bash
# Correct: provide input
agent execute task.md

# Correct: pipe input
cat task.md | agent execute

# Incorrect: missing input
agent execute  # Error: No task input provided
```

### API key errors

```bash
# Set required keys
export ANTHROPIC_API_KEY="your-key"
export OPENAI_API_KEY="your-key"

# Verify
agent status
```

### JSON parsing errors

```bash
# Validate JSON output
agent execute task.md | jq .

# Pretty print
agent execute task.md | jq . | less

# Extract specific field
agent execute task.md | jq '.results.architect'
```

## Performance Tips

1. **Use request scope**: Defaults to faster isolated memory
   ```bash
   agent execute --request-id feature_x task.md
   ```

2. **Limit verbosity**: Skip verbose for production
   ```bash
   agent execute task.md  # No --verbose flag
   ```

3. **Pipe to jq**: Filter output early
   ```bash
   agent execute task.md | jq '.results | keys'
   ```

4. **Cache results**: Save JSON for re-analysis
   ```bash
   agent execute task.md > task.json
   cat task.json | jq '.results.architect'
   ```

## Next Steps

- [Memory Management](MEMORY_MANAGEMENT.md) - How memory persists across requests
- [Request-Scoped Memory](REQUEST_SCOPED_MEMORY.md) - Using isolated memory contexts
- [Main Documentation](README.md) - Full system overview
