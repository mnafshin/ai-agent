# Memory Management Guide

## The Problem

As your AI agent project grows, memory files become a bottleneck:

```
Month 1:  decisions.md = 20 KB   ✅ Fast
Month 6:  decisions.md = 150 KB  ⚠️ Slow
Year 1:   decisions.md = 500 KB  ❌ Very slow
Year 2:   decisions.md = 1.2 MB  ❌ Bottleneck
```

**Impact**:
- Each request loads entire memory (2-5 seconds per load)
- Agent context window wastes tokens on irrelevant history
- Search becomes slow (LLM must read entire file)
- Project scales poorly

## Solution: 4-Layer Memory Strategy

### Layer 1: Request-Scoped Memory (Fast)
**When**: Every request  
**What**: Isolated 5KB memory for current task  
**Tool**: `orchestrator.py --create-scope`

```bash
# Before: Load 500KB global memory for 1-hour task
# After: Load 5KB request memory for 1-hour task
# Savings: 100x smaller, 10x faster
```

**How it works**:
```
tasks/request_001/
├── memory/
│   ├── decisions.md       # Only decisions for this request
│   ├── debug_log.md       # Only bugs we hit
│   ├── review_log.md      # Only reviews for this request
│   └── context.md         # Reference to global context
├── 01_task.md
└── 02_task.md
```

### Layer 2: Lazy Loading (Background)
**When**: Automatic  
**What**: Load only recent entries, lazy-load history if needed  
**Tool**: `memory_manager.py` (automatic)

```python
# Before
agent_sees_all_500kb_of_decisions = load_file("decisions.md")

# After  
recent_decisions = load_recent(10)  # 2KB
if needs_historical_context:
    full_decisions = load_file("decisions.md")  # On-demand
```

**Benefit**: Most requests only see 2KB, full history available if needed.

### Layer 3: Archive Rotation (Monthly)
**When**: Once per month  
**What**: Move entries older than 90 days to archive  
**Tool**: `python tools/archive_memory.py`

```bash
# Before
decisions.md = 500 KB (2-year history)

# After
decisions.md = 50 KB (recent 3 months)
archive_decisions_2026_q1.md = 150 KB (Jan-Mar)
archive_decisions_2025_q4.md = 150 KB (Oct-Dec)
archive_decisions_2025_q3.md = 50 KB (Jul-Sep)
```

**Result**: Active memory stays small, history available but archived.

### Layer 4: Consolidation & Indexing (Weekly)
**When**: After each request completes  
**What**: 
- Merge important findings into global memory
- Build fast search index (10KB to find anything)  

**Tool**: `python tools/consolidate_memory.py request_001`

```bash
# Flow
request_001 runs     → Learns new things
request_001 ends     → python consolidate_memory.py request_001
↓
Request findings merged into global memory
↓
Index rebuilt for fast search
↓
Request memory archived for historical reference
```

## Quick Reference: What to Use When

| Situation | Action | Command |
|-----------|--------|---------|
| **Starting new feature** | Use request scope | `orchestrator.py --request feature_001 --create-scope` |
| **Feature complete** | Consolidate findings | `python tools/consolidate_memory.py feature_001` |
| **Monthly maintenance** | Archive old entries | `python tools/archive_memory.py` |
| **Need historic context** | Restore from archive | `python tools/archive_memory.py --restore archive_decisions_2026_q1.md decisions.md` |
| **Search for decision** | Use memory manager | `python tools/memory_manager.py` |
| **Memory growing too large** | Check stats | `python tools/archive_memory.py --stats` |

## Implementation Details

### Request-Scoped Memory

**Why it helps**:
- ✅ Start each request fresh (5KB context)
- ✅ No accumulated history burden
- ✅ Parallel requests don't interfere
- ✅ Project growth doesn't affect request speed

**How to use**:
```bash
# Create request with isolated memory
python orchestrator.py --request my_feature --create-scope

# This creates:
tasks/my_feature/memory/
├── decisions.md          # Empty (request populates)
├── debug_log.md          # Empty (request populates)
├── review_log.md         # Empty (request populates)
└── context.md            # Links to global context
```

**After request completes**:
```bash
# Consolidate important findings
python tools/consolidate_memory.py my_feature

# This:
# 1. Shows findings from request memory
# 2. Merges into global memory (if important)
# 3. Archives request memory for history
# 4. Cleans up
```

### Archive Rotation

**Monthly schedule**:
```bash
# 1st of each month (cron job)
0 0 1 * * cd /path/to/agent_core && python tools/archive_memory.py

# Or manual
python tools/archive_memory.py
```

**What it does**:
1. Find entries older than 90 days
2. Move to archive files (by quarter)
3. Keep active memory lean
4. Update index with archive info

**View archives**:
```bash
python tools/archive_memory.py --stats

# Output:
# Active decisions.md: 45 entries
# Active debug_log.md: 28 entries
# Active review_log.md: 52 entries
#
# Archives:
#   archive_decisions_2026_q1.md: 180 entries (450 KB)
#   archive_debug_log_2026_q1.md: 120 entries (300 KB)
#   archive_review_log_2026_q1.md: 200 entries (400 KB)
```

**Restore if needed**:
```bash
# Bring back decisions from Q1 2026
python tools/archive_memory.py --restore archive_decisions_2026_q1.md decisions.md

# Decisions will re-appear in active memory
```

### Consolidation Process

**Interactive consolidation**:
```bash
python tools/consolidate_memory.py feature_001 --review

# Shows:
# 1. All decisions made during request
# 2. All bugs hit and fixed
# 3. All code quality findings
#
# Asks: Keep these in global memory? (y/n)
```

**Auto consolidation**:
```bash
python tools/consolidate_memory.py feature_001

# Auto-merges everything into global memory
```

**Result**:
```
Global memory before:
  decisions.md (50 entries)
  debug_log.md (35 entries)

Global memory after consolidation:
  decisions.md (55 entries) ← +5 new from request
  debug_log.md (40 entries) ← +5 new from request
  
Archived:
  archived_requests/request_feature_001_memory/
    ├── decisions.md
    ├── debug_log.md
    └── review_log.md
    (Kept for full request history if audit needed)
```

### Memory Manager (Automatic)

**Optional: Install for automatic optimization**:
```bash
pip install pyyaml
python tools/memory_manager.py

# Output:
# 🧠 Memory Manager
# 
# ## Decisions
# - 2026-03-01: PostgreSQL chosen over MongoDB
# - 2026-02-28: OAuth 2.0 for auth
# 
# ## Recent Issues Fixed
# - 2026-03-05: N+1 query in ProductService
# - 2026-03-02: JWT refresh token timeout
#
# 📊 Stats:
# Total decisions: 45
# Total bugs fixed: 28
# Total reviews: 52
# Cache size: 3 items
```

**Without manual installation**: System still works, just less optimized.

## Scaling Timeline

| Scale | Active Memory | Strategy |
|-------|--------------|----------|
| < 1 month | 50 KB | Request scope only |
| 1-3 months | 100 KB | Request scope + lazy load |
| 3-6 months | 150 KB | Add archive rotation |
| 6-12 months | 200 KB | Add consolidation |
| 1-2 years | 300 KB | Add memory manager index |
| 2+ years | 500 KB → 100 KB+ | Use SQLite backend (optional) |

## Preventing Common Problems

### Problem: Memory keeps growing
**Solution**: 
1. Run `archive_memory.py --stats` to check size
2. If >200 KB, run `python tools/archive_memory.py`
3. Automate monthly: `0 0 1 * * cd /agent_core && python tools/archive_memory.py`

### Problem: Can't find old decisions
**Solution**:
1. Check archives: `python tools/archive_memory.py --stats`
2. Restore if needed: `python tools/archive_memory.py --restore archive_decisions_2026_q1.md decisions.md`
3. Search restored content with memory_manager

### Problem: Requests are slow
**Solution**:
1. Use request scope: `--create-scope` flag
2. Check memory size: `python tools/memory_manager.py`
3. If >300 KB, consolidate older requests
4. Run cleanup: `python tools/archive_memory.py`

### Problem: Too many archived files
**Solution**:
1. Consolidate archives annually
2. Keep current year + 1 previous year
3. Move older archives to cold storage if needed

## SQL Backend (Future-Proof)

When memory reaches 10,000+ entries (won't happen for years), switch to SQLite:

```python
# In future releases
manager = MemoryManager(memory_path, use_sqlite=True)

# Automatically queries only needed entries
decisions = manager.get_recent_decisions(10)  # Returns 10 rows
bugs = manager.search("performance")           # Full-text search
```

No migration needed - system auto-detects and switches.

## Summary

The 4-layer strategy ensures your memory system **never becomes a bottleneck**:

1. **Request scope** (100x smaller per task)
2. **Lazy loading** (load only what's needed)
3. **Archive rotation** (keep active memory lean)
4. **Consolidation** (merge important findings)

**Result**: Year 1 = same speed as Month 1 ✅

See `docs/REQUEST_SCOPED_MEMORY.md` for detailed usage examples.
