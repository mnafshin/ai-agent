# Model Versioning Guide

## Overview

The system supports specifying exact model versions for each SKILL, enabling:

- **Precise Control**: Choose the exact model version (Opus 4.5 vs 4.6, GPT-5.4 vs 5.5)
- **Cost Optimization**: Select cheaper models for simple tasks
- **Fallback Strategy**: Automatic fallback to alternate models if preferred one unavailable
- **Future-Proof**: Easy to update model versions as new releases become available

## Model Namespace

All models follow the format: `provider/model-version`

### Claude Models
```yaml
claude/haiku           # Claude 3.5 Haiku - Fast for simple tasks
claude/sonnet          # Claude 3.5 Sonnet - Balanced speed/reasoning
claude/opus            # Claude Opus 4.5 - Best reasoning
claude/opus-4-6        # Claude Opus 4.6 - Future/experimental
```

**Best For**:
- `haiku` - Simple formatting, preprocessing
- `sonnet` - Balanced tasks, code review prep
- `opus` - Complex reasoning, architecture, debugging
- `opus-4-6` - Hardest problems when available

### GPT Models
```yaml
gpt/gpt-4o             # GPT-4o - Vision capable, general purpose
gpt/gpt-4-turbo        # GPT-4 Turbo - Higher reasoning than 4o
gpt/gpt-5              # GPT-5.4 - Next generation (future)
```

**Best For**:
- `gpt-4o` - Test generation, documentation, vision tasks
- `gpt-4-turbo` - Complex test cases, detailed reviews
- `gpt-5` - Experimental, best performance when available

### Copilot Models
```yaml
copilot/codex          # Copilot Codex 5.3 - Specialized code gen
copilot/latest         # Latest Copilot release
```

**Best For**:
- `codex` - Production code generation, refactoring
- `latest` - When you want newest features

## Using Model Versions in SKILL Files

### Basic Specification

```markdown
## Metadata
- **MODEL**: claude/opus-4-6 (best reasoning for architecture)
```

### With Fallback Options

```markdown
## Metadata
- **MODEL**: claude/opus-4-6 (if available)
- **FALLBACK**: claude/opus → claude/sonnet
```

### Task-Specific Models

```markdown
## Model Selection

This skill uses different models for different sub-tasks:

- **Phase 1 (Design)**: claude/opus-4-6 (complex reasoning)
- **Phase 2 (Implementation)**: copilot/codex (code generation)
- **Phase 3 (Verification)**: claude/opus (quality check)
```

### With Cost Notes

```markdown
## Metadata
- **MODEL**: claude/sonnet (balanced: $3/1M input, $15/1M output)
```

## Programmatic Usage

### Using the Model Manager

```python
from tools.model_manager import ModelManager, SkillModelResolver

# Initialize manager
manager = ModelManager()

# Get API model ID for API calls
model_id = manager.get_model_id("claude/opus-4-6")
# Returns: "claude-opus-4-1-20250805"

# Get model details
version = manager.get_model_version("gpt/gpt-5")
# Returns: "5.4"

description = manager.get_description("copilot/codex")
# Returns: "Code generation specialist"

# Estimate cost
cost = manager.estimate_cost("claude/opus", input_tokens=1000, output_tokens=500)
# Returns: 0.020 (20 cents)
```

### Parsing SKILL Specifications

```python
from tools.model_manager import SkillModelResolver

resolver = SkillModelResolver()

# Parse various formats
model_id = resolver.parse_model_spec("claude/opus-4-6")        # → full API ID
model_id = resolver.parse_model_spec("opus-4-6")               # → infers claude/
model_id = resolver.parse_model_spec("gpt/gpt-5 (best)")       # → removes comment
```

### Integration with Orchestrator

Update orchestrator.py to use ModelManager:

```python
from tools.model_manager import ModelManager, SkillModelResolver

class AIOrchestrator:
    def __init__(self):
        self.model_manager = ModelManager()
        self.skill_resolver = SkillModelResolver(self.model_manager)
    
    def run_skill(self, skill_name, input_text, skill_config):
        # Parse model from SKILL metadata
        model_spec = skill_config.get("MODEL", "claude/opus")
        model_id = self.skill_resolver.parse_model_spec(model_spec)
        
        # Get max tokens for this model
        max_tokens = self.model_manager.get_max_tokens(model_spec)
        
        # Call API
        response = call_api(model_id, input_text, max_tokens=max_tokens)
        
        # Log cost estimate
        cost = self.model_manager.estimate_cost(
            model_spec, 
            response.usage.prompt_tokens,
            response.usage.completion_tokens
        )
        print(f"Cost: ${cost:.4f}")
```

## Recommended Model Assignments

| Task | Model | Reasoning |
|------|-------|-----------|
| **Requirements Gathering** | `claude/opus` | Complex clarification |
| **Architecture Design** | `claude/opus-4-6` | Hardest reasoning problem |
| **Code Implementation** | `copilot/codex` | Fastest code generation |
| **Code Refactoring** | `copilot/codex` | Understands existing code |
| **Bug Fixing** | `claude/opus` | Deep debugging reasoning |
| **Code Review** | `claude/opus` | Catching subtle issues |
| **Test Generation** | `gpt/gpt-4o` | Good for test coverage |
| **Documentation** | `gpt/gpt-4o` | Clear writing and examples |
| **Simple Formatting** | `claude/haiku` | Fast and cheap |

## Cost Optimization Strategies

### Strategy 1: Tiered Models
Use cheaper models for initial passes, expensive for final:

```markdown
## Model Strategy
1. Write spec: `claude/sonnet` ($3 input, $15 output)
2. Review spec: `claude/opus` ($15 input, $75 output)
```

### Strategy 2: Task-Appropriate Selection
Match model capability to task complexity:

```markdown
- Simple validation: `claude/haiku` (saves 80%)
- Medium tasks: `claude/sonnet` (balanced)
- Complex reasoning: `claude/opus-4-6` (best)
```

### Strategy 3: Fallback Chain
Specify fallback models for cost optimization:

```python
# In config/models.yaml
fallback:
  level1: "claude/opus-4-6"    # Best option
  level2: "claude/opus"        # Good alternative
  level3: "gpt/gpt-4o"         # Acceptable fallback
```

## Future Models

The system is designed to support future model releases:

```yaml
# Future updates just require adding to config/models.yaml
claude/opus-5:
  version: "5"
  id: "claude-opus-5-20261231"
  cost: { input: 25, output: 100 }

gpt/gpt-6:
  version: "6"
  id: "gpt-6-2026-12-01"
  cost: { input: 20, output: 60 }
```

## Managing Model Versions

### Updating Available Models

Edit `config/models.yaml`:

```yaml
models:
  claude:
    new-model:
      version: "X.Y"
      id: "claude-new-model-id"
      cost: { input: 10, output: 50 }
      description: "Description"
      max_tokens: 200000
```

### Deprecating Old Models

Comment out or remove from `config/models.yaml` and update SKILL files to new recommendations.

### Environment Setup

No additional setup needed—ModelManager loads from `config/models.yaml` automatically.

## Troubleshooting

### Model Not Found

**Error**: `ValueError: Model not found: claude/opus-5`

**Solution**: Check if model is in `config/models.yaml`. If new model, add it:

```yaml
# Add to config/models.yaml
claude:
  opus-5:
    version: "5"
    id: "claude-opus-5-..."
```

### API Key Missing

**Error**: `ValueError: API key not found for claude`

**Solution**: Set environment variables:

```bash
export ANTHROPIC_API_KEY="sk-ant-..."
export OPENAI_API_KEY="sk-..."
export GITHUB_COPILOT_TOKEN="ghp_..."
```

### Getting Available Models

```python
manager = ModelManager()

# List all models
all_models = manager.list_models()

# List Claude models only
claude_models = manager.list_models("claude")
```

## Example: Complete SKILL with Versioning

```markdown
# Skill: Design System Architecture

## Metadata
- **SKILL_ID**: design_system
- **TEAM**: Architecture
- **ROLE**: Architect
- **MODEL**: claude/opus-4-6 (best reasoning)
- **FALLBACK_MODELS**: 
  - claude/opus (if 4.6 unavailable)
  - gpt/gpt-4-turbo (last resort)

## Alternative Models by Task

- **If budget is critical**: Use `claude/sonnet` (saves 80%)
- **If speed matters**: Use `claude/haiku` for validation phase
- **For experimental**: Try `claude/opus-4-6` for better results

## Cost Estimate
- Expected input: ~5,000 tokens
- Expected output: ~3,000 tokens
- Cost @ claude/opus: ~$0.12
- Cost @ claude/sonnet: ~$0.04
```

---

See `tools/model_manager.py` for full API documentation.
