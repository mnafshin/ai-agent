# Request-Scoped Memory Template

## About Request Memory

Instead of loading the project's entire memory (which grows over time), each request has its own **isolated memory** containing only relevant context for that specific task.

This prevents:
- ❌ Loading 500KB of history for a 1-hour task
- ❌ Token waste on irrelevant context
- ❌ Performance degradation as project grows

## Structure

```
tasks/request_001/
├── memory/              ← Isolated to this request only
│   ├── decisions.md     # Decisions within this request scope
│   ├── debug_log.md     # Issues we hit on this request
│   ├── review_log.md    # Code review scores for this request
│   └── context.md       # Relevant global context (auto-populated)
├── 01_analyze.md
├── 02_design.md
└── 03_implement.md
```

## Usage

### Option 1: Automatic (Recommended)

```bash
# Create request with auto-populated request-scoped memory
python orchestrator.py --request 001 --create-scope
```

This automatically:
- Creates `tasks/request_001/memory/` 
- Pulls relevant context from global memory
- Isolates decisions to just this request
- Adds reference to global memory if needed

### Option 2: Manual

Create `tasks/request_001/memory/context.md`:

```markdown
# Context for Request 001: Add Payment Processing

## Related Global Decisions
- 2026-03-01: PostgreSQL chosen as primary database (see /agent_core/memory/decisions.md#L42)
- 2026-02-15: Authentication via OAuth 2.0 (see /agent_core/memory/decisions.md#L28)

## Key Architecture
- Service layer pattern used throughout
- All external calls wrapped with retry logic
- Transaction management via Spring @Transactional

## Recent Related Issues
- 2026-03-05: Fixed N+1 query problem in UserRepository
- 2026-02-28: Resolved JWT refresh token timing issue
```

## Lifecycle

### During Request
```
Agent reads request memory (small, fast)
  ↓
Agent learns new things, updates request memory
  ↓
Request memory stays isolated
```

### After Request (Manual)
```
If findings are generalizable:
  Run: python tools/consolidate_memory.py request_001
  
This merges important findings into global memory:
  ✓ New architectural decisions → decisions.md
  ✓ Bugs found → debug_log.md
  ✓ Code quality issues → review_log.md
  ✓ Everything else archived for request history
```

## Benefits

| Aspect | Before | After |
|--------|--------|-------|
| Memory loaded per request | 500KB | 5KB (100x smaller) |
| Token waste on old context | High | None |
| Time to load context | Slow | Fast |
| Scalability | O(n) - grows with history | O(1) - stays small |
| Request isolation | Mixed contexts | Pure isolation |

## Implementation in Orchestrator

```python
class RequestScopedMemory:
    def __init__(self, request_path, global_memory_path):
        self.request_memory = request_path / "memory"
        self.global_memory = global_memory_path
        self.request_memory.mkdir(parents=True, exist_ok=True)
        
        # Load only this request's context
        self.context = self._load_request_context()
    
    def _load_request_context(self):
        """Load only relevant context for this request"""
        # Load decisions.md from request (small file)
        # Don't load global decisions.md (could be 100KB+)
        # Reference global if needed via link in context.md
        pass
    
    def get_context_for_agent(self):
        """Return minimal context needed for this request"""
        return self.context  # 5KB instead of 500KB
```

## When to Use

**Always use request-scoped memory for:**
- New feature development
- Bug fixes
- Any isolated task

**Use global memory reference only:**
- When you need historical decisions
- When learning from past issues
- Via `consolidate_memory.py` after task completion

## Example Workflow

```bash
# 1. Create new request with isolated memory
mkdir -p tasks/request_feature_oauth/memory
cat agent_core/memory/context_template.md > tasks/request_feature_oauth/memory/context.md

# 2. Add relevant global context (manually or via tool)
echo "See /agent_core/memory/decisions.md for full architecture" >> ...

# 3. Create task files - they use request memory
python orchestrator.py --request feature_oauth

# 4. After success, consolidate important findings
python tools/consolidate_memory.py feature_oauth

# 5. Next request starts fresh with small isolated memory
```

## Files

- `memory_manager.py` — Handles lazy loading from global memory
- `archive_memory.py` — Moves old entries to archives
- `consolidate_memory.py` — Merges request findings into global memory

See `/agent_core/tools/` for implementation.
