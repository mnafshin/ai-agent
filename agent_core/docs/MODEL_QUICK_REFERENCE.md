# Model Versioning Quick Reference

## Quick Model Specs

### Use in SKILL Files

```markdown
## Metadata
- **MODEL**: claude/opus-4-6  # Best reasoning
- **MODEL**: gpt/gpt-5       # Latest GPT
- **MODEL**: copilot/codex   # Code specialist
```

## Available Models (as of March 2026)

| Model | ID | Input $ | Output $ | Best For |
|-------|---------|---------|----------|----------|
| `claude/haiku` | claude-3-5-haiku | 0.8 | 4 | Simple tasks, fast |
| `claude/sonnet` | claude-3-5-sonnet | 3 | 15 | Balanced tasks |
| `claude/opus` | claude-opus-4-1 | 15 | 75 | Complex reasoning |
| `claude/opus-4-6` | claude-opus-4-6 | 20 | 100 | Best reasoning (future) |
| `gpt/gpt-4o` | gpt-4o-2024-11 | 10 | 20 | General purpose |
| `gpt/gpt-4-turbo` | gpt-4-turbo-2024 | 10 | 30 | High reasoning |
| `gpt/gpt-5` | gpt-5-2025-06 | 15 | 45 | Next gen (future) |
| `copilot/codex` | copilot-codex-5-3 | 8 | 40 | Code generation |
| `copilot/latest` | copilot-latest | 10 | 50 | Latest features |

## Recommended Models by Task

```
Reasoning/Planning      → claude/opus-4-6
Code Generation        → copilot/codex
Code Review            → claude/opus
Testing                → gpt/gpt-4o
Bug Fixing             → claude/opus
Documentation          → gpt/gpt-4o
Simple Tasks           → claude/haiku
```

## Fallback Chain

If specified model unavailable:
1. Try: `claude/opus-4-6`
2. Fall back to: `claude/opus`
3. Last resort: `gpt/gpt-4o`

## Usage Examples

### Python Code

```python
from tools.model_manager import ModelManager

manager = ModelManager()

# Get API ID (for API calls)
model_id = manager.get_model_id("claude/opus-4-6")

# Get version
version = manager.get_model_version("gpt/gpt-5")

# Estimate cost
cost = manager.estimate_cost("claude/opus", 1000, 500)

# List models
all_models = manager.list_models()
```

### In SKILL Files

```markdown
## Metadata
- **MODEL**: claude/opus-4-6 (best reasoning, $20/$100 per 1M tokens)
- **FALLBACK**: claude/opus → gpt/gpt-4o
```

## Adding New Models

Edit `config/models.yaml`:

```yaml
models:
  claude:
    opus-5:                    # Model name
      version: "5"             # Version string
      id: "claude-opus-5-..."  # API ID
      cost: { input: 25, output: 100 }
      description: "Next gen"
      max_tokens: 200000
```

## Cost Examples

For a typical 1,000 input / 500 output token task:

| Model | Cost |
|-------|------|
| `claude/haiku` | $0.002 |
| `claude/sonnet` | $0.006 |
| `claude/opus` | $0.020 |
| `claude/opus-4-6` | $0.030 |
| `gpt/gpt-4o` | $0.015 |
| `gpt/gpt-5` | $0.022 |
| `copilot/codex` | $0.008 |

---

**Full docs**: See `MODEL_VERSIONING.md`  
**Config**: `config/models.yaml`  
**Manager**: `tools/model_manager.py`
