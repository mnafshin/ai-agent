# Stop Prompting. Start Deploying an AI Development Team.

*How a multi-agent stack can 10x developer efficiency — without burning your token budget.*

---

Most developers use AI the same broken way:

> Open chat → paste code → get output → hope for the best.

No memory. No verification. No quality gate. Just vibes.

Here's a better way.

---

## The Idea: A Software Company, Not a Chatbot

Instead of one giant prompt, model a real engineering org — **20 specialized agents in 7 teams**, each doing one job well:

| Team | What It Does |
|------|-------------|
| **Product** | Turns vague requests into precise specs |
| **Architecture** | Analyzes your codebase, designs the solution |
| **Development** | Plans, implements, refactors, fixes bugs |
| **QA** | Writes tests, runs debug cycles, reviews code |
| **DevOps** | Configures CI/CD, handles deployment |
| **Docs** | Writes release notes, updates documentation |
| **Control** | Critic loop + spec verification (the quality gate) |

Each agent is small, focused, and uses the **right model for its job**. That last part matters a lot.

---

## Token Efficiency: The Right Model for the Right Job

Running every task through GPT-4o or Claude Opus is expensive and slow. The trick is **tier-matching**:

| Tier | Model | Used For |
|------|-------|----------|
| **Fast** | Claude 3.5 Haiku / GPT-4o-mini | Critic loops, quick scans, repo analysis |
| **Balanced** | Claude 3.5 Sonnet / GPT-4o | Implementation, test generation, CI config |
| **Powerful** | Claude 3 Opus / Llama 405B | Spec writing, system design, deep code review |

The system auto-routes each skill to its minimum-required tier. A critic loop running 5 iterations uses the **fast** model — not Opus. That alone cuts costs by 10–20x on high-frequency tasks.

> **Rule of thumb:** Powerful models for high-stakes decisions. Fast models for repetitive quality checks.

---

## The Critic Loop: Never Ship Below 90/100

Every agent output goes through a self-correction loop before moving on:

```
Generate → Critic scores it → Below 90? → Improve → Repeat (max 5×)
                                                ↓
                                        Above 90? → Verify against spec → Ship
```

Real example on an architecture task:
- Iteration 1: **62** — missing validation layer
- Iteration 2: **85** — inconsistent naming
- Iteration 3: **94** — ✅ accepted

The critic uses a *different reasoning pass* — it doesn't just re-read its own work. This catches hallucinations that self-review misses. And because it runs on a **fast/cheap model**, the cost is minimal.

---

## Memory: The Feature Most AI Tools Skip

LLMs forget everything between calls. This system doesn't.

```
memory/
  ├── decisions.md      ← why we chose PostgreSQL over MongoDB
  ├── architecture.md   ← the system design that all agents share
  ├── debug_log.md      ← every bug found and how it was fixed
  └── review_log.md     ← code quality trends over time
```

Every agent **reads memory before acting** and **writes findings after**. The next agent picks up exactly where the last one left off — even across days or separate runs. No repeated context, no forgotten constraints, no contradicting earlier decisions.

Tasks are numbered sequentially (`01_spec.md`, `02_design.md`, …) so agents can never skip or forget a step.

---

## One Config File. Six Backends. Full Data Control.

This is the part that matters for teams working with real company code.

```env
# Free tier — GitHub PAT, GPT-4o via GitHub Models API
GITHUB_TOKEN=ghp_...

# Real Claude — stays in YOUR AWS account (enterprise-safe)
AWS_ACCESS_KEY_ID=AKIA...
AWS_REGION=eu-west-1

# 100% offline — DeepSeek, Llama, Mistral on your own machine
LOCAL_LLM_URL=http://localhost:11434/v1

# Force one provider for all skills:
# LLM_PROVIDER=local
```

The **ProviderRegistry** auto-discovers what's set and routes each skill to the best available backend. Priority: `anthropic → bedrock → vertex → openai → local → github_models`.

| Provider | Data Location | Claude? | Cost |
|----------|--------------|---------|------|
| `github_models` | Microsoft | ❌ (GPT fallback) | Free |
| `anthropic` | Anthropic servers | ✅ | Pay-per-token |
| `bedrock` | **Your AWS** | ✅ | Pay-per-token |
| `vertex` | **Your GCP** | ✅ + Gemini | Pay-per-token |
| `local` | **Your machine** | Whatever you run | Free |

**Switching providers requires zero code changes.** Change one line in `.env`.

### The Data Privacy Rule

> If you're sending internal code or documents to an AI API, check who owns that data.
> - **GitHub Copilot Enterprise** → covered by your Microsoft agreement ✅
> - **Direct `ANTHROPIC_KEY`** → goes to Anthropic's servers, needs a DPA ⚠️
> - **AWS Bedrock** → Claude runs in your AWS account, no data leaves your infra ✅
> - **Local LLM** → never touches the internet ✅

---

## Local LLMs Are Production-Ready

Running [Ollama](https://ollama.ai) with DeepSeek takes 2 minutes:

```bash
ollama pull deepseek-coder-v2:latest
ollama serve
```

```env
LOCAL_LLM_URL=http://localhost:11434/v1
```

That's it. The agent auto-discovers models, guesses tier from the name (`70b` → powerful, `3b` → fast), and routes accordingly. **Zero external API calls. Zero data exposure.**

Best local models for code tasks: DeepSeek Coder V2, Qwen 2.5 Coder 32B, Codestral, Llama 3.1 70B.

---

## Get Running in 3 Steps

```bash
# 1. Install
.\setup.ps1          # Windows
bash setup.sh        # Linux/macOS

# 2. Set one provider key in .env
GITHUB_TOKEN=ghp_...   # free, works immediately

# 3. Run
agent execute task.md
gh pr diff | agent review
git diff HEAD~1 | agent review || exit 1   # blocks bad pushes
```

The `agent status` command shows exactly which providers are active, which models are loaded, and how each skill will be routed.

---

## The Payoff

| Without agents | With agents |
|----------------|------------|
| One LLM, one shot | 20 specialists, right model per task |
| No quality gate | Critic loop: nothing ships below 90/100 |
| Context lost between sessions | Persistent memory across all runs |
| Code goes to random APIs | Full control over data location |
| Expensive Opus for everything | Tier-matched: cheap models for cheap tasks |

For teams doing repeated workflows — feature builds, PR reviews, release cycles — the investment pays for itself fast. Start with a free GitHub PAT, swap to Bedrock when you need compliance.

---

*Full source: `agent_core/` · Config: `agent_core/config/models.yaml` · Docs: `agent_core/docs/`*

**Version 3.0 · March 2026**
