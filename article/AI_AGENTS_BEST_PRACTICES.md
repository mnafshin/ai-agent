# AI Agents Best Practices: A Comprehensive Guide

## The Evolution of AI-Powered Development

Autonomous AI agents are transforming how we build software. Rather than treat AI as a simple completion tool, leading teams are designing multi-agent systems that simulate real software development teams. This article shares the best practices we discovered after analyzing production systems like Claude Code, Cursor, and emerging frameworks like LangGraph.

---

## The Three Core Problems AI Systems Face

Before designing agents, understand what breaks most systems:

1. **Context Loss** - LLMs forget what they learned or previous decisions
2. **Hallucination** - Generated solutions that look good but violate requirements or architecture
3. **Inconsistency** - Multiple agents produce conflicting decisions

Our approach solves these through three mechanisms:

- **Persistent Memory** - Architectural decisions and context stored between runs
- **Critic Loops** - Self-improvement through iterative refinement
- **Specification Verification** - Always check outputs against original requirements

---

## Architecture: From Single Agent to Software Company

### Traditional Approach (Broken)
```
User Request → LLM → Code → Done ❌
```

Problems:
- No reasoning phase
- Single model for all tasks
- No verification
- Hallucinations common

### Best Practice Approach (This Design)
```
User Request
  ↓
Product Team (requirements)
  ↓ CRITIC LOOP + SPEC VERIFICATION
Architecture Team (design)
  ↓ CRITIC LOOP + SPEC VERIFICATION
Development Team (implementation)
  ↓ CRITIC LOOP + SPEC VERIFICATION
QA Team (testing & review)
  ↓ CRITIC LOOP + SPEC VERIFICATION
DevOps Team (deployment)
  ↓ CRITIC LOOP + SPEC VERIFICATION
Documentation Team (release)
```

---

## The Software Company Model: 20 Specialized Skills

Instead of one large agent, we divide work across **20 specialized skills**, each with:
- A specific role (like team members)
- Recommended model (Claude, Copilot, GPT)
- Critic loop for quality (max 5 iterations)
- Specification verification (does it meet requirements?)
- Memory updates (shared knowledge)

### Team Structure

#### Product Team (Discovery)
- **Gather Requirements** - Convert vague user requests into structured goals
- **Write Specification** - Formal spec with functional & non-functional requirements

#### Architecture Team (Design)
- **Analyze Repository** - Understand existing code structure and conventions
- **Design System** - Architecture for the requested feature
- **Update Architecture Memory** - Persist decisions for future reference

#### Development Team (Implementation)
- **Plan Tasks** - Break architecture into atomic, independent tasks
- **Implement Feature** - Write code for a single task (uses Copilot)
- **Refactor Code** - Safely update existing code (uses Copilot)
- **Fix Bug** - Debug and fix failing tests

#### QA Team (Validation)
- **Generate Tests** - Unit and integration tests covering edge cases
- **Debug Cycle** - Fix compilation errors and test failures
- **Review Code** - Evaluate quality, correctness, performance, security

#### DevOps Team (Delivery)
- **Configure CI** - Generate CI/CD pipeline files
- **Deploy App** - Deploy to staging/production

#### Documentation Team (Communication)
- **Update Docs** - Technical documentation for new features
- **Write Release Notes** - Summary of changes and deployment info

#### Control Layer (Quality Assurance)
- **Critic** - Roasts any output to improve quality (max 5 iterations)
- **Verify Spec** - Ensures solution satisfies original requirements

---

## Key Innovation: The Critic Loop

The biggest improvement to traditional LLM workflows is the **self-correction loop**.

### How It Works

```
Generate Result
    ↓
Run Critic (Claude)
    ↓
Score < 90? → Improve Result → Loop (max 5)
    ↓
Score >= 90? → Accept and Move Forward
    ↓
Verify Against Spec
```

### Why This Works

- **Claude as Critic** - Different reasoning pass avoids reinforcing mistakes
- **Deterministic Quality** - Never ship code that didn't meet threshold
- **Traceable Improvement** - Every iteration logged for transparency
- **Prevents Hallucination** - Spec verification catches missing requirements

### Example: Architecture Design Loop

```
Iteration 1: Score 62 - Missing validation layer
Iteration 2: Score 85 - Inconsistent naming conventions
Iteration 3: Score 94 - ACCEPTED ✓
```

---

## Model Selection: Right Tool for Each Task

Different models excel at different tasks:

| Task | Model | Reason |
|------|-------|--------|
| Reasoning / Planning | Claude 3.5 | Best reasoning, large context |
| Code Generation | Copilot/GPT-4 | Fastest deterministic code |
| Review / Critique | Claude 3.5 | Exceptional at evaluation |
| Testing | GPT-4 | Good test generation |
| Bug Fixing | Claude 3.5 | Strong debugging reasoning |
| Documentation | GPT-4 | Excellent summarization |

**Key Insight**: Reasoning tasks → Claude. Code generation → Copilot/GPT.

---

## Memory System: Preventing Context Loss

Agents forget easily. We solve this with persistent memory:

```
memory/
  ├── repo_summary.md        # Project structure & tech stack
  ├── architecture.md         # System design decisions
  ├── decisions.md            # Important decisions & rationale
  ├── tech_stack.md           # Technologies in use
  ├── coding_rules.md         # Project conventions
  ├── debug_log.md            # Issues found & fixed
  └── review_log.md           # Code review outcomes
```

### How Memory Works

1. **Agent reads** `memory/` before acting
2. **Agent executes** task with full context
3. **Agent updates** memory if decisions made
4. **Loop** - Next agent starts with fresh context

### Example Update

```markdown
# decisions.md
## 2026-03-07: Plugin Architecture Decision

**Chosen**: Plugin-based request processing
**Reason**: Enables external integrations
**Pattern**: Strategy pattern for plugin loading
**Impact**: Core module, affects deployment
```

---

## Task Files: Never Forget Work

Tasks are stored as individual markdown files with sequential numbering:

```
tasks/request_001/
  ├── 01_analyze_requirements.md
  ├── 02_design_architecture.md
  ├── 03_plan_implementation.md
  ├── 04_create_service.md
  ├── 05_create_controller.md
  ├── 06_write_tests.md
  ├── 07_integration_tests.md
  └── 08_document_changes.md
```

### Why This Works

- **Deterministic ordering** - Files processed sequentially
- **Prevents hallucination** - LLM can't "forget" tasks
- **Transparent progress** - Users see exactly what's being done
- **Resumable** - Crash? Just restart from last completed task

### Task File Format

```markdown
# Task 04: Create ProductService

## Goal
Implement the ProductService class with CRUD operations.

## Requirements
- CRUD methods (create, read, update, delete)
- Input validation
- Transaction management
- Logging

## Files to Create/Modify
- src/main/java/com/example/service/ProductService.java
- src/test/java/com/example/service/ProductServiceTest.java

## Success Criteria
- All CRUD methods implemented
- Unit tests written and passing
- Validation catches invalid inputs
```

---

## Orchestration: Putting It All Together

The orchestrator is the conductor that:

1. **Loads** task files in order
2. **Invokes** appropriate skill (with right model)
3. **Runs critic loop** for quality gates
4. **Verifies spec** before accepting
5. **Updates memory** with decisions
6. **Tracks** progress and errors

### Orchestrator Pseudocode

```python
specification = refine("write_spec", user_request)
architecture = refine("design_system", specification)
verify_spec(architecture, specification)

tasks = refine("plan_tasks", architecture)
write_task_files(tasks)

results = []
for task in tasks:
    code = refine("implement_feature", task)
    verify_spec(code, specification)
    
    tests = run_skill("generate_tests", code)
    debug = run_skill("debug_cycle", tests)
    
    review = refine("review_code", code)
    results.append(review)

update_memory("decisions", architecture)
update_memory("debug_log", debug)
```

---

## Specification Verification: The Missing Piece

Most systems fail here. We explicitly verify:

**Verifier checks**:
1. ✓ Does implementation match spec?
2. ✓ Are all requirements satisfied?
3. ✓ Any missing edge cases?
4. ✓ Consistent with architectural decisions?

If invalid → **Send back to generator** with specific feedback

### Example Verification Output

```json
{
  "valid": false,
  "missing_requirements": [
    "Bulk delete operation not implemented",
    "Audit logging missing from update operation"
  ],
  "notes": [
    "API validation covers happy path but not error cases"
  ]
}
```

---

## Best Practices Summary

### ✅ DO

1. **Separate concerns** - Planner ≠ Coder ≠ Reviewer
2. **Use critic loops** - Refine everything important (threshold: 90 score)
3. **Verify specs** - Always check against requirements
4. **Persist memory** - Store architectural decisions
5. **Order tasks** - Sequential file naming prevents forgetting
6. **Match models** - Use Claude for reasoning, Copilot for coding
7. **Log everything** - Critic iterations, reviews, decisions
8. **Reuse tokens** - Use Copilot for IDE integration where possible

### ❌ DON'T

1. ~~Use same model for all tasks~~ → Use specialized models
2. ~~Trust LLM hallucinations~~ → Verify with specs and tests
3. ~~Keep context in LLM~~ → Persist to memory files
4. ~~Run one big agent~~ → Divide into specialized skills
5. ~~Ship first output~~ → Always run critic loop
6. ~~Ignore architecture~~ → Analyze repo first, design before coding
7. ~~Forget requirements~~ → Verify every implementation step

---

## Workflow Example: Building a REST API

User says: "Build a REST API for managing products"

### Step 1: Product Team
```
GatherRequirements → WriteSpec → CRITIC LOOP → VERIFY
Output: Formal spec with functional requirements
```

### Step 2: Architecture Team
```
AnalyzeRepo → DesignSystem → CRITIC LOOP → VERIFY
Output: Architecture design with modules, APIs, dependencies
```

### Step 3: Development Team
```
PlanTasks → CRITIC LOOP → VERIFY
Output: 5-8 ordered task files (entity, service, controller, tests, docs)
```

### Step 4: For Each Task
```
ImplementFeature (Copilot) → CRITIC LOOP → VERIFY
GenerateTests (GPT) → DebugCycle → ReviewCode (Claude)
```

### Step 5: Final Steps
```
UpdateDocs → WriteReleaseNotes
```

### Step 6: Memory Updated
```
architecture.md    ← API design pattern
decisions.md       ← Why REST over GraphQL
debug_log.md       ← Issues found and fixed
review_log.md      ← Code quality scores
```

---

## Advanced Pattern: Multi-Critic Evaluation

For critical systems, use multiple reviewers:

```
Implementation
    ↓
    ├─→ Security Critic
    ├─→ Performance Critic
    └─→ Architecture Critic
    ↓
Merge Critiques
    ↓
Improve Result
```

This catches issues single reviewer would miss.

---

## Tools Included in This Design

### 1. Inspector Tool (`inspector.py`)
Analyzes your agent configuration:
- ✓ Validates all SKILL.md files
- ✓ Checks task ordering
- ✓ Verifies memory structure
- ✓ Reports missing skills
- ✓ Tests orchestrator config

### 2. Orchestrator (`orchestrator.py`)
Implementation framework:
- Loads skills dynamically
- Manages critic loops (max 5 iterations)
- Runs spec verification
- Updates memory
- Handles multi-model execution

### 3. SKILL.md Templates
20 ready-to-use skill definitions with:
- Goals and instructions
- Input/output formats
- Model recommendations
- Memory update hints

---

## Getting Started

### Prerequisites
```bash
export ANTHROPIC_KEY="your-claude-key"
export OPENAI_KEY="your-gpt-key"
export GITHUB_COPILOT_TOKEN="your-copilot-token"
```

### Project Structure
```
ai-company/
  ├── skills/
  │   ├── product/
  │   ├── architecture/
  │   ├── development/
  │   ├── qa/
  │   ├── devops/
  │   ├── docs/
  │   └── control/
  ├── memory/
  ├── tasks/
  ├── orchestrator.py
  └── config.yaml
```

### Run Your First Request
```bash
# 1. Create a request in tasks/request_001/
# 2. Run orchestrator
python orchestrator.py --request 001

# 3. Inspector validates configuration
python inspector.py --validate
```

---

## Common Patterns

### Pattern 1: Emergency Bug Fix
```
User: "We have a critical bug in production"
    ↓
RunDebugCycle → FixBug → Tests → Verify → Critic Loop → Deploy
```

### Pattern 2: Feature Refactor
```
User: "Refactor authentication to use OAuth"
    ↓
DesignSystem (new OAuth architecture)
    ↓
RefactorCode (rewrite auth module, using Copilot)
    ↓
GenerateTests → Debug → Review → Verify
```

### Pattern 3: Parallel Work
```
Task 1: API endpoint     |  Task 2: Database migration
    ↓                    |      ↓
Implement (Copilot)      |  Implement (Copilot)
  ↓                      |      ↓
Test (GPT)               |  Test (GPT)
  ↓                      |      ↓
Review (Claude)          |  Review (Claude)
    └─────────┬──────────┘
              ↓
          Integration Test
```

---

## Why This Works: The Science

### Reduces Hallucination
- **Reasoning Phase** - Separate from implementation
- **Verification** - Check against specs
- **Critic Passes** - Catch obvious mistakes early

### Improves Code Quality
- **Testing** - Dedicated QA team
- **Code Review** - Always happens
- **Architecture Review** - Before coding starts

### Prevents Context Loss
- **Memory Files** - Persistent context
- **Task Files** - Ordered, indexed work
- **Agent Logs** - What each agent thought

### Enables Debugging
- **Trace** - Every iteration logged
- **Verify** - Clear spec validation
- **Review** - Score and issues documented

---

## Extending the System

### Add New Skills
1. Create `skills/{team}/{skill}/SKILL.md`
2. Define goal, inputs, outputs
3. Specify recommended model
4. Add to orchestrator config

Example:
```markdown
# Skill: SecurityAudit
MODEL: Claude
GOAL: Identify security vulnerabilities
```

### Add New Workflows
Create orchestration sequences in `config.yaml`:
```yaml
workflows:
  bug_fix:
    - analyze_bug
    - debug_cycle
    - implement_fix
    - generate_tests
    - verify_spec
    - review_code
```

### Custom Critics
Create specialized critics for your domain:
```markdown
# Skill: PerformanceCritic
MODEL: Claude
GOAL: Evaluate implementation performance
```

---

## Conclusion

The shift from single agents to multi-agent systems is the key innovation in AI-powered development. By:

1. ✓ **Separating roles** (Product, Architecture, Dev, QA, DevOps, Docs)
2. ✓ **Running critic loops** (max 5 iterations, score threshold 90)
3. ✓ **Verifying specs** (always validate requirements)
4. ✓ **Persisting memory** (architectural decisions & context)
5. ✓ **Ordering tasks** (sequential files prevent forgetting)
6. ✓ **Matching models** (Claude reasoning, Copilot coding)

...we create self-improving systems that produce production-ready code while maintaining architectural consistency and handling edge cases.

This is how tools like Claude Code, Cursor, and emerging autonomous dev systems actually work under the hood.

---

## Alternatives: Claude Code vs Cursor vs LangGraph vs In-House System

You might ask: "Why build an in-house system when Claude Code, Cursor, and LangGraph already exist?"

Good question. The honest answer: **it depends on your goals, and these aren't mutually exclusive**—they address different problems at different scales.

### Feature Comparison

| Factor | Claude Code | Cursor | LangGraph | In-House |
|--------|---|---|---|---|
| **Learning curve** | Minimal (just prompt) | Minimal (IDE plugin) | Moderate (framework) | Steep (requires design) |
| **Flexibility** | High (unrestricted) | High (IDE-based) | High (extensible) | Very high (custom) |
| **Control** | Low (black box) | Low (black box) | Medium (defined patterns) | Complete |
| **Reproducibility** | Medium (non-deterministic) | Medium | High (state-managed) | Very high (deterministic) |
| **Quality gates** | None | None | Basic (retry/fallback) | Explicit (critic, verification) |
| **Memory persistence** | Limited (context window) | Limited | Moderate (state dict) | Deep (10 specialized files) |
| **Cost** | Pay-per-call (high) | Subscription | Self-hosted | Self-hosted |
| **Production readiness** | Quick prototype | Interactive dev | Good platform | Enterprise-grade |
| **Audit trail** | Minimal | Minimal | Good (logs) | Comprehensive |
| **Multi-model support** | Single model | Single model | Yes | Specialized assignment |

### When to Use Each

#### Claude Code (Best for: Quick Prototypes)
**Use when:**
- You want the fastest path to working code
- You're okay with occasional hallucinations
- Quality doesn't need to be reproducible
- You don't need persistent state
- One-off projects with tight deadlines
- Cost isn't a constraint

**Example**: "Build me a Next.js dashboard real quick"

**Advantages**:
- Minimal setup (just authorize)
- Fastest iteration speed
- No infrastructure to maintain

**Disadvantages**:
- No quality gates
- Can't reuse learned context
- Not reproducible (same prompt gets different results)
- Expensive at scale

#### Cursor (Best for: Interactive Development)
**Use when:**
- You're actively coding alongside the agent
- You catch and approve changes before they ship
- You need IDE-level control
- You want real-time feedback
- Building complex applications where you maintain oversight

**Example**: "I'll guide the AI while building my app"

**Advantages**:
- Real-time human-in-the-loop
- IDE integration (context from your files)
- You maintain editorial control
- Good for learning and mentoring

**Disadvantages**:
- Requires active user presence (not autonomous)
- No built-in quality gates
- Hard to scale to teams
- Context still limited to window size

#### LangGraph (Best for: Structured Orchestration)
**Use when:**
- You need agent orchestration framework
- You want explicit state management
- You're building production autonomous systems
- You prefer open-source + flexibility
- You want to ship in weeks (not months)
- You're okay with learning a framework

**Example**: "Research → analyze → generate report" workflow

**Advantages**:
- Structured agent patterns (no reinventing wheels)
- State graphs prevent hallucinations
- Good developer experience
- Active community
- Moderate implementation time (2-3 weeks)

**Disadvantages**:
- Still framework-level (you write agents)
- Quality gates are simple (retries, not critic loops)
- No built-in specification verification
- Memory is state dict (not persistent files)
- Learning curve before productivity

#### In-House System (Best for: Repeated Production Workflows)
**Use when:**
- You build similar systems repeatedly (amortize learning cost)
- Quality and reproducibility are non-negotiable
- You need audit trails and compliance
- You require specialized models per task
- You're automating complex workflows
- You want deep customization

**Example**: "Every client project uses this same 20-skill architecture"

**Advantages**:
- Purpose-built for your domain
- Critic loops + spec verification (catches hallucinations others miss)
- Persistent memory (context survives crashes)
- Deterministic task ordering (nothing forgotten)
- Deep customization (adapt to your needs)
- No third-party lock-in

**Disadvantages**:
- High initial investment (2-4 weeks design + implementation)
- Steep learning curve (your team must understand the system)
- Requires maintenance
- Only profitable after 3+ similar projects

### The Hybrid Approach (Recommended)

The best strategy combines all four:

```
Day-to-day work
    ↓
Use Claude Code (interactive prototypes)
    ↓
Successful pattern found?
    ├─→ NO → Keep using Claude Code
    └─→ YES → Does it need production stability?
                ├─→ NO → Use Cursor (human-in-the-loop)
                └─→ YES → Repeatability needed?
                            ├─→ NO → Use LangGraph (quick framework)
                            └─→ YES → Use in-house (long-term asset)
```

### Decision Tree

**Question 1: Speed vs Quality?**
- Speed (prototype in 1 hour) → Claude Code
- Quality (reproducible production) → In-house System

**Question 2: Human in the loop?**
- Yes (I'm actively coding) → Cursor
- No (autonomous system) → LangGraph or In-House

**Question 3: Will you build this again?**
- Once → LangGraph (don't over-engineer)
- 3+ times → In-House (amortize investment)

**Question 4: Need production guarantees?**
- No (internal tool) → LangGraph
- Yes (customer-facing) → In-House

### The Real Competitive Advantage

Here's what your in-house system has that the others don't provide out-of-box:

1. **Specification Verification** — Not just "does code work?" but "does it meet original requirements?"
   - Claude Code: No
   - Cursor: No
   - LangGraph: Optional (you must implement)
   - In-House: ✅ Built-in, enforced

2. **Critic Loops** — Sophisticated self-improvement (max 5 iterations, 90/100 threshold)
   - Claude Code: No (generates once)
   - Cursor: No (you review manually)
   - LangGraph: Basic retry (success/failure only)
   - In-House: ✅ Iterative refinement, scoring

3. **Deterministic Task Ordering** — Nothing gets forgotten
   - Claude Code: Relies on agent memory (fragile)
   - Cursor: File-based (but unordered)
   - LangGraph: Task graphs (good, but needs manual setup)
   - In-House: ✅ `01_`, `02_` sequential files (foolproof)

4. **Role-Specific Models** — Right tool for each job
   - Claude Code: Single model
   - Cursor: Your model of choice (one)
   - LangGraph: Multi-model support (you build it)
   - In-House: ✅ Claude for reasoning, Copilot for coding, GPT for generation

### Quick ROI Calculation

| System | Setup Time | Per-Project Time | Best After |
|--------|---|---|---|
| Claude Code | 0 hours | 1-2 hours | First project |
| Cursor | 0.5 hours | 2-4 hours | Second project |
| LangGraph | 40 hours | 4-8 hours | Third project |
| In-House | 80 hours | 6-12 hours | Fourth project |

**The in-house system pays for itself by project #4**. After that, every project is faster and higher quality than competitors.

### Final Recommendation

1. **Start with LangGraph** for your first autonomous system
   - Get familiar with agent patterns
   - 2-3 week implementation
   - All your key needs met

2. **If you find yourself rebuilding the same pattern**, invest in in-house
   - Migration from LangGraph to in-house is ~40% of original implementation time
   - Your knowledge of "what works" transfers directly
   - Now you own the system completely

3. **Use Claude Code as your daily driver** for exploration
   - 5-minute prototypes
   - Discovery and learning
   - Then migrate successful patterns upward

This way, you don't over-engineer (avoiding in-house complexity for one-off projects) while still building competitive advantages as you identify repeatable patterns.

---

## References

- [Anthropic: Building Effective Agents](https://www.anthropic.com/research/building-effective-agents)
- [Claude Code Documentation](https://docs.anthropic.com/en/docs/claude-code/sub-agents)
- [LangGraph Agent Framework](https://langchain-ai.github.io/langgraph/)
- [CrewAI Multi-Agent System](https://crew.ai)

---

**Version**: 1.0  
**Date**: March 2026  
**Authors**: Afshin Amini + Copilot
