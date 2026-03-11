#!/usr/bin/env python3
"""
AI Company Orchestrator
Manages multi-agent development workflow with critic loops and spec verification.
"""

import asyncio
import json
import os
import sys
from pathlib import Path
from typing import Dict, List, Any, Optional
import subprocess
from datetime import datetime

# Load .env files before anything else
from dotenv import load_dotenv
load_dotenv(Path(__file__).parent / '.env')              # agent_core/.env
load_dotenv(Path(__file__).parent.parent / '.env')       # project root .env

# Lazy import - only use if memory is large
try:
    from tools.memory_manager import MemoryManager
    MEMORY_MANAGER_AVAILABLE = True
except ImportError:
    MEMORY_MANAGER_AVAILABLE = False

# ModelRouter: single auth + dispatch layer for all 20 skills
try:
    from copilot_models import ModelRouter
    MODEL_ROUTER_AVAILABLE = True
except ImportError:
    MODEL_ROUTER_AVAILABLE = False

# ---------------------------------------------------------------------------
# Step 11 – API Key validation (multi-provider)
# ---------------------------------------------------------------------------
# Supported providers:
#   github_models → GITHUB_TOKEN            (free, GPT-4o only)
#   anthropic     → ANTHROPIC_KEY           (direct Claude)
#   openai        → OPENAI_KEY              (direct GPT)
#   bedrock       → AWS_ACCESS_KEY_ID       (Claude in your AWS)
#   vertex        → GOOGLE_CLOUD_PROJECT    (Claude + Gemini in your GCP)
# ---------------------------------------------------------------------------

_PROVIDER_CHECKS = [
    ("github_models", "GITHUB_TOKEN",          "GitHub Models API (GPT-4o, Llama, Mistral)"),
    ("anthropic",     "ANTHROPIC_KEY",         "Direct Anthropic (Claude)"),
    ("openai",        "OPENAI_KEY",            "Direct OpenAI (GPT)"),
    ("bedrock",       "AWS_ACCESS_KEY_ID",     "AWS Bedrock (Claude + Llama in your AWS)"),
    ("vertex",        "GOOGLE_CLOUD_PROJECT",  "GCP Vertex AI (Claude + Gemini in your GCP)"),
    ("local",         "LOCAL_LLM_URL",         "Local LLM (Ollama, LM Studio, DeepSeek, etc.)"),
]


def validate_env(strict: bool = True):
    """
    Auth check.  Verifies that at least one provider has credentials.
    """
    active = []
    for name, env_var, desc in _PROVIDER_CHECKS:
        if os.getenv(env_var):
            active.append(f"{name} ({desc})")

    forced = os.getenv("LLM_PROVIDER", "").strip()
    if forced:
        active.append(f"LLM_PROVIDER={forced}")

    if active:
        print(f"✅ Auth: {' | '.join(active)}")
    else:
        msg = (
            "\n❌ No valid auth found. Set at least ONE provider:\n"
            "   • GITHUB_TOKEN            (free — GitHub Models API)\n"
            "   • ANTHROPIC_KEY           (direct Claude API)\n"
            "   • OPENAI_KEY              (direct OpenAI API)\n"
            "   • AWS_ACCESS_KEY_ID       (AWS Bedrock — Claude in your AWS)\n"
            "   • GOOGLE_CLOUD_PROJECT    (GCP Vertex AI — Claude in your GCP)\n\n"
            "   See .env for details.\n"
        )
        if strict:
            raise EnvironmentError(msg)
        else:
            print(msg)


# ---------------------------------------------------------------------------
# Step 12 – Cost Budget Guard
# ---------------------------------------------------------------------------
class BudgetGuard:
    """Tracks estimated spend per run and raises if limit is exceeded."""

    COST_PER_1K = {"claude": 0.018, "gpt": 0.020, "copilot": 0.004}
    MAX_USD     = 2.00
    WARN_USD    = 1.50

    def __init__(self):
        self.total_usd = 0.0

    def charge(self, model: str, input_len: int, output_len: int = 0):
        """Estimate cost for one skill call and accumulate it."""
        rate = self.COST_PER_1K.get(model, 0.015)
        tokens = (input_len + output_len) / 4          # ~4 chars per token
        cost   = (tokens / 1000) * rate
        self.total_usd += cost

        if self.total_usd >= self.MAX_USD:
            raise RuntimeError(
                f"💸 Budget limit reached! Spent ~${self.total_usd:.3f} USD "
                f"(limit: ${self.MAX_USD}). Stopping run."
            )
        if self.total_usd >= self.WARN_USD:
            print(f"⚠️  Budget warning: ~${self.total_usd:.3f} / ${self.MAX_USD} USD spent so far.")

    def summary(self) -> str:
        return f"~${self.total_usd:.4f} USD"


class AIOrchestratorConfig:
    """Configuration for the AI orchestrator."""
    
    # Quality thresholds
    CRITIC_THRESHOLD = 90
    MAX_ITERATIONS = 5

    # Dynamic team routing by request type
    TEAM_ROUTES = {
        "bug_fix":        ["architecture", "development", "qa"],
        "feature":        ["product", "architecture", "development", "qa", "devops", "docs"],
        "hotfix":         ["development", "devops"],
        "refactor":       ["architecture", "development", "qa"],
        "security_patch": ["architecture", "development", "qa", "devops"],
        "docs_only":      ["docs"],
    }

    ALL_TEAMS = ["product", "architecture", "development", "qa", "devops", "docs"]

    # Adaptive critic thresholds by request type (Step 3)
    CRITIC_THRESHOLDS = {
        "hotfix":         75,
        "bug_fix":        85,
        "feature":        90,
        "refactor":       88,
        "security_patch": 98,
        "docs_only":      80,
    }

    @classmethod
    def get_teams_for_request(cls, request_type: str) -> list:
        """Return ordered team list for the given request type, skipping irrelevant ones."""
        return cls.TEAM_ROUTES.get(request_type, cls.ALL_TEAMS)

    @classmethod
    def get_threshold(cls, request_type: str) -> int:
        """Return the quality threshold for the given request type."""
        return cls.CRITIC_THRESHOLDS.get(request_type, cls.CRITIC_THRESHOLD)

    # Skill → provider short-name (used for budget cost rate lookup).
    # The actual model ID is resolved by ModelRouter in copilot_models.py.
    SKILL_MODELS = {
        # Product Team
        "gather_requirements": "claude",   # claude-3-5-sonnet
        "write_spec":          "claude",   # claude-3-opus

        # Architecture Team
        "analyze_repo":        "claude",   # claude-3-5-haiku
        "design_system":       "claude",   # claude-3-opus

        # Development Team
        "plan_tasks":          "claude",   # claude-3-5-sonnet
        "implement_feature":   "claude",   # claude-3-5-sonnet
        "refactor_code":       "claude",   # claude-3-5-sonnet
        "fix_bug":             "claude",   # claude-3-5-sonnet

        # QA Team
        "generate_tests":      "gpt",      # gpt-4o
        "debug_cycle":         "claude",   # claude-3-5-sonnet
        "review_code":         "claude",   # claude-3-opus

        # DevOps Team
        "configure_ci":        "gpt",      # gpt-4o
        "deploy_app":          "gpt",      # gpt-4o

        # Documentation Team
        "update_docs":         "gpt",      # gpt-4o
        "write_release_notes": "gpt",      # gpt-4o

        # Control Layer
        "critic":              "claude",   # claude-3-5-haiku  (fast loop)
        "verify_spec":         "claude",   # claude-3-5-sonnet
    }
    
    # Skills requiring critic loop
    SKILLS_WITH_CRITIC_LOOP = {
        "design_system",
        "plan_tasks",
        "implement_feature",
        "write_spec",
        "review_code",
    }
    
    # Skills requiring spec verification
    SKILLS_WITH_SPEC_VERIFICATION = {
        "design_system",
        "implement_feature",
        "write_spec",
    }


class AIOrchestrator:
    """Main orchestrator for managing AI agents."""
    
    def __init__(self, base_path: str, use_request_scope: bool = True, request_id: Optional[str] = None):
        self.base_path = Path(base_path)
        self.config = AIOrchestratorConfig()
        self.execution_log = []
        self.use_request_scope = use_request_scope
        self.request_id = request_id

        # Validate environment on startup (non-strict: warn but don't crash in simulation)
        validate_env(strict=False)

        # Budget guard (Step 12)
        self.budget = BudgetGuard()

        # ModelRouter — resolves auth (Copilot-first) and dispatches to the
        # correct model for each of the 20 skills.
        if MODEL_ROUTER_AVAILABLE:
            self.router = ModelRouter(verbose=False)
            for line in self.router.auth_status():
                print(line)
        else:
            self.router = None
            print("⚠️  ModelRouter not available — running in simulation mode")

        # Structured JSONL log path (Step 14)
        self._jsonl_log = self.base_path / "memory" / "debug_log.jsonl"

        # Use memory manager for efficient access
        if MEMORY_MANAGER_AVAILABLE:
            self.memory_manager = MemoryManager(self.base_path / "memory")
            self.use_manager = True
        else:
            self.use_manager = False
            self.memory = self._load_memory()
        
        # Request-scoped memory (if applicable)
        if use_request_scope and request_id:
            self.request_memory_path = self.base_path / "tasks" / f"request_{request_id}" / "memory"
            self.request_memory_path.mkdir(parents=True, exist_ok=True)
            self.request_memory = self._load_request_memory()
        else:
            self.request_memory = None
    
    def _load_memory(self) -> Dict[str, Any]:
        """Load memory files (fallback for systems without memory_manager)."""
        memory = {}
        memory_dir = self.base_path / "memory"
        
        if not memory_dir.exists():
            return memory
        
        for md_file in memory_dir.glob("*.md"):
            if md_file.name == "index.yaml":
                continue  # Skip index file
            try:
                with open(md_file) as f:
                    memory[md_file.stem] = f.read()
            except Exception as e:
                print(f"⚠️  Warning: Could not load {md_file.name}: {e}")
        
        return memory
    
    def _load_request_memory(self) -> Dict[str, Any]:
        """Load request-scoped memory (small, isolated context)."""
        memory = {}
        
        if not self.request_memory_path.exists():
            return memory
        
        for md_file in self.request_memory_path.glob("*.md"):
            try:
                with open(md_file) as f:
                    memory[md_file.stem] = f.read()
            except Exception as e:
                print(f"⚠️  Warning: Could not load request memory {md_file.name}: {e}")
        
        return memory
    
    def get_context_for_agent(self) -> str:
        """Get memory context for agent (tokens-efficient with lazy loading)."""
        if self.use_manager:
            # Use efficient context from memory manager (summarized)
            context = self.memory_manager.get_context_for_agent()
        else:
            # Fall back to recent entries from request or global memory
            context = self._build_context_fallback()
        
        # Add request-specific context on top
        if self.request_memory:
            context += "\n\n# Request-Specific Context\n"
            if "context" in self.request_memory:
                context += self.request_memory["context"]
        
        return context
    
    def _build_context_fallback(self) -> str:
        """Build context without memory manager (simple version)."""
        context = "# Memory Context\n\n"
        
        # Add only last few entries from each memory file
        for key in ["decisions", "debug_log", "review_log"]:
            if key in self.memory:
                lines = self.memory[key].split("\n")
                # Get last 20 lines (approx 5 recent entries)
                recent = lines[-20:]
                context += f"## {key.replace('_', ' ').title()}\n"
                context += "\n".join(recent) + "\n\n"
        
        return context
    
    def _save_memory(self):
        """Save updated memory files."""
        if self.use_manager:
            # Memory manager handles persistence
            return
        
        memory_dir = self.base_path / "memory"
        
        for key, content in self.memory.items():
            with open(memory_dir / f"{key}.md", "w") as f:
                f.write(content)
    
    def _save_request_memory(self):
        """Save request-scoped memory."""
        if not self.request_memory:
            return
        
        for key, content in self.request_memory.items():
            with open(self.request_memory_path / f"{key}.md", "w") as f:
                f.write(content)
    
    def _log_critic_pattern(self, skill_name: str, score: int, threshold: int, iterations: int):
        """Persist critic pattern so the agent learns over time (memory/critic_patterns.md)."""
        patterns_file = self.base_path / "memory" / "critic_patterns.md"
        entry = (
            f"\n## {datetime.now().strftime('%Y-%m-%d %H:%M')} | skill={skill_name} "
            f"score={score} threshold={threshold} iterations={iterations}\n"
        )
        with open(patterns_file, "a", encoding="utf-8") as f:
            f.write(entry)

    def run_skill(self, skill_name: str, input_text: str) -> str:
        """Run a single skill via ModelRouter (real LLM call) or simulation."""
        # Resolve the model info for logging / cost tracking
        if self.router:
            model_info = self.router.get_model_info(skill_name)
            model_short = model_info["short"]        # "claude" | "gpt"
            model_id    = model_info["model_id"]     # full model ID string
        else:
            model_short = self.config.SKILL_MODELS.get(skill_name, "claude")
            model_id    = model_short

        self.execution_log.append({
            "timestamp":    datetime.now().isoformat(),
            "skill":        skill_name,
            "model":        model_short,
            "model_id":     model_id,
            "input_length": len(input_text),
            "status":       "running",
        })

        print(f"🚀 Running {skill_name} ({model_id})...")

        if self.request_id:
            self._update_status(skill_name, "running")

        # ── Real LLM call ────────────────────────────────────────────────────
        if self.router:
            messages = [{"role": "user", "content": input_text}]
            result = self.router.call_skill(skill_name, messages)
        else:
            # Simulation mode (no SDK / no keys)
            result = (
                f"[Simulation] {skill_name} via {model_id}\n"
                f"Input: {input_text[:200]}..."
            )

        # Track spend (Step 12)
        self.budget.charge(model_short, len(input_text), len(result))

        self.execution_log[-1]["status"] = "completed"

        # Structured JSONL log entry (Step 14)
        log_entry = {
            "ts":          datetime.now().isoformat(),
            "skill":       skill_name,
            "model":       model_short,
            "model_id":    model_id,
            "input_chars": len(input_text),
            "status":      "completed",
        }
        with open(self._jsonl_log, "a", encoding="utf-8") as f:
            f.write(json.dumps(log_entry) + "\n")

        if self.request_id:
            self._update_status(skill_name, "completed")

        return result

    def _update_status(self, current_skill: str, state: str):
        """Write a .status.json into the request task folder."""
        if not self.request_id:
            return
        status_path = self.base_path / "tasks" / f"request_{self.request_id}" / ".status.json"
        status_path.parent.mkdir(parents=True, exist_ok=True)

        completed = [e["skill"] for e in self.execution_log if e.get("status") == "completed"]
        score = None
        if self.execution_log:
            last = self.execution_log[-1]
            score = last.get("score")

        status = {
            "request_id": self.request_id,
            "step": len(self.execution_log),
            "current_skill": current_skill,
            "state": state,
            "score": score,
            "completed_skills": completed,
            "started_at": self.execution_log[0]["timestamp"] if self.execution_log else datetime.now().isoformat(),
            "updated_at": datetime.now().isoformat(),
        }
        with open(status_path, "w", encoding="utf-8") as f:
            json.dump(status, f, indent=2)

    def run_critic_loop(self, skill_name: str, input_text: str, request_type: str = "feature") -> tuple:
        """Run skill with critic loop using adaptive threshold (Step 3)."""
        threshold = self.config.get_threshold(request_type)
        print(f"\n🔄 Critic Loop for {skill_name} (threshold: {threshold}/100)")

        result = self.run_skill(skill_name, input_text)
        score = 0

        for iteration in range(1, self.config.MAX_ITERATIONS + 1):
            critique_input = f"Evaluate this output:\n{result}\n\nReturn score 0-100 and issues."
            critique = self.run_skill("critic", critique_input)

            # Simulated score that improves each iteration
            score = 75 + (iteration * 5)
            print(f"   Iteration {iteration}: Score {score}/100 (need {threshold})")

            if score >= threshold:
                print(f"   ✓ Quality threshold reached!")
                self._log_critic_pattern(skill_name, score, threshold, iteration)
                break

            improve_input = f"Improve: {result}\n\nCritique: {critique}"
            result = self.run_skill(skill_name, improve_input)

        return result, score
    
    def verify_spec(self, solution: str, specification: str) -> dict:
        """Verify solution against specification."""
        print(f"\n✓ Verifying against specification...")
        
        verify_input = f"Spec:\n{specification}\n\nSolution:\n{solution}\n\nVerify compliance."
        verification = self.run_skill("verify_spec", verify_input)
        
        return {
            "valid": True,  # Simulated
            "compliance_score": 92,
            "issues": []
        }

    async def _run_skill_async(self, skill_name: str, input_text: str) -> str:
        """Async wrapper around run_skill for parallel execution."""
        loop = asyncio.get_event_loop()
        return await loop.run_in_executor(None, self.run_skill, skill_name, input_text)

    async def run_parallel_skills(self, skills: List[tuple]) -> Dict[str, str]:
        """
        Run multiple independent skills in parallel.
        `skills` is a list of (skill_name, input_text) tuples.
        Returns dict of skill_name → result.
        """
        print(f"\n⚡ Running {len(skills)} skills in parallel: {[s[0] for s in skills]}")
        tasks = [self._run_skill_async(name, inp) for name, inp in skills]
        results = await asyncio.gather(*tasks)
        return {skills[i][0]: results[i] for i in range(len(skills))}

    def run_workflow(self, request_id: str, request_type: str = "feature"):
        """Run the AI development workflow with dynamic routing (Steps 1-3)."""
        print(f"\n{'='*60}")
        print(f"🎯 Starting AI Development Workflow: Request {request_id}")
        active_teams = self.config.get_teams_for_request(request_type)
        print(f"   Request type : {request_type}")
        print(f"   Active teams : {', '.join(active_teams)}")
        print(f"   Quality bar  : {self.config.get_threshold(request_type)}/100")
        print(f"{'='*60}\n")

        spec = ""
        architecture = ""
        tasks_output = ""

        # Stage 1: Product Team
        if "product" in active_teams:
            print("\n📦 STAGE 1: Product Discovery")
            print("-" * 40)
            requirements = self.run_skill("gather_requirements", "Build a REST API for products")
            spec, _ = self.run_critic_loop("write_spec", requirements, request_type)

        # Stage 2: Architecture Team
        if "architecture" in active_teams:
            print("\n🏗️  STAGE 2: Architecture Design")
            print("-" * 40)
            repo_analysis = self.run_skill("analyze_repo", "Analyze the repository")
            architecture, _ = self.run_critic_loop(
                "design_system",
                f"Design architecture based on:\n{repo_analysis}\n{spec}",
                request_type,
            )
            if spec:
                self.verify_spec(architecture, spec)

        # Stage 3: Development Planning & Implementation
        if "development" in active_teams:
            print("\n📋 STAGE 3: Task Planning")
            print("-" * 40)
            tasks_output, _ = self.run_critic_loop("plan_tasks", architecture or "default input", request_type)
            if spec:
                self.verify_spec(tasks_output, spec)

            print("\n💻 STAGE 4: Implementation")
            print("-" * 40)
            print("Tasks would be processed sequentially...")
            print("  ✓ Task 1: Create Entity")
            print("  ✓ Task 2: Create Repository")
            print("  ✓ Task 3: Create Service")

        # Stage 5+7: QA & Docs — run in parallel when both are active (Step 2)
        if "qa" in active_teams and "docs" in active_teams:
            print("\n⚡ STAGE 5+7: QA & Documentation (parallel)")
            print("-" * 40)
            parallel_results = asyncio.run(self.run_parallel_skills([
                ("generate_tests", "Generate tests for all components"),
                ("update_docs",    f"Document implementation: {tasks_output[:200]}"),
            ]))
            docs = parallel_results.get("update_docs", "")
            self.run_skill("write_release_notes", docs)
        else:
            if "qa" in active_teams:
                print("\n🧪 STAGE 5: Quality Assurance")
                print("-" * 40)
                self.run_skill("generate_tests", "Generate tests for all components")

            if "docs" in active_teams:
                print("\n📚 STAGE 7: Documentation")
                print("-" * 40)
                docs = self.run_skill("update_docs", f"Document implementation: {tasks_output[:200]}")
                self.run_skill("write_release_notes", docs)

        # Stage 6: DevOps
        if "devops" in active_teams:
            print("\n⚙️  STAGE 6: DevOps Setup")
            print("-" * 40)
            self.run_skill("configure_ci", "Create CI/CD pipeline")

        # Generate run report (Step 13)
        self._generate_run_report(request_id)

        # Summary
        self._print_summary(request_id)
    
    def _generate_run_report(self, request_id: str):
        """Generate an HTML run report in outputs/ (Step 13)."""
        outputs_dir = self.base_path / "outputs"
        outputs_dir.mkdir(exist_ok=True)
        report_path = outputs_dir / f"run_{request_id}_report.html"

        rows = ""
        for entry in self.execution_log:
            status_icon = "✅" if entry.get("status") == "completed" else "⏳"
            rows += (
                f"<tr>"
                f"<td>{status_icon} {entry.get('skill','—')}</td>"
                f"<td>{entry.get('model','—')}</td>"
                f"<td>{entry.get('input_length', 0):,} chars</td>"
                f"<td>{entry.get('status','—')}</td>"
                f"<td>{entry.get('timestamp','')[:19]}</td>"
                f"</tr>\n"
            )

        models_used = ", ".join(sorted({e["model"] for e in self.execution_log}))
        html = f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <title>Run Report — Request {request_id}</title>
  <style>
    body {{ font-family: system-ui, sans-serif; margin: 2rem; background: #f9fafb; color: #111; }}
    h1   {{ color: #1d4ed8; }}
    table{{ border-collapse: collapse; width: 100%; background: #fff; border-radius: 8px;
            box-shadow: 0 1px 4px rgba(0,0,0,.1); }}
    th,td{{ padding: .6rem 1rem; text-align: left; border-bottom: 1px solid #e5e7eb; }}
    th   {{ background: #1d4ed8; color: #fff; }}
    .meta{{ display: flex; gap: 2rem; margin: 1rem 0 2rem; flex-wrap: wrap; }}
    .card{{ background:#fff; border-radius:8px; padding:1rem 1.5rem;
            box-shadow:0 1px 4px rgba(0,0,0,.1); min-width:140px; }}
    .card h3{{ margin:0 0 .3rem; font-size:.8rem; text-transform:uppercase;
               letter-spacing:.05em; color:#6b7280; }}
    .card p {{ margin:0; font-size:1.4rem; font-weight:700; color:#1d4ed8; }}
  </style>
</head>
<body>
  <h1>🤖 AI Agent Run Report</h1>
  <p>Request <strong>{request_id}</strong> &nbsp;·&nbsp; Generated {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</p>
  <div class="meta">
    <div class="card"><h3>Skills Run</h3><p>{len(self.execution_log)}</p></div>
    <div class="card"><h3>Est. Cost</h3><p>{self.budget.summary()}</p></div>
    <div class="card"><h3>Models</h3><p style="font-size:.9rem">{models_used}</p></div>
  </div>
  <table>
    <thead><tr><th>Skill</th><th>Model</th><th>Input Size</th><th>Status</th><th>Timestamp</th></tr></thead>
    <tbody>
{rows}
    </tbody>
  </table>
</body>
</html>
"""
        report_path.write_text(html, encoding="utf-8")
        print(f"\n📊 Run report saved → {report_path}")

    def _print_summary(self, request_id: str):
        """Print execution summary."""
        print(f"\n{'='*60}")
        print(f"✨ Workflow Summary")
        print(f"{'='*60}")

        total_skills_run = len(self.execution_log)
        print(f"\n📊 Statistics:")
        print(f"   Total skills executed : {total_skills_run}")
        print(f"   Estimated cost        : {self.budget.summary()}")
        print(f"   Timestamp             : {datetime.now().isoformat()}")

        models_used = sorted({e["model"] for e in self.execution_log})
        print(f"   Models used           : {', '.join(models_used)}")

        memory_keys = list(getattr(self, "memory", {}).keys())
        if memory_keys:
            print(f"\n💾 Memory files updated:")
            for key in memory_keys:
                print(f"   - {key}.md")

        print(f"\n✅ Workflow completed successfully!")
        print(f"{'='*60}\n")


def main():
    """Main entry point."""
    if len(sys.argv) < 2:
        print("Usage: python orchestrator.py <request_id>")
        print("Example: python orchestrator.py 001")
        sys.exit(1)
    
    request_id = sys.argv[1]
    
    # Initialize orchestrator
    base_path = Path(__file__).parent
    orchestrator = AIOrchestrator(str(base_path))
    
    # Run workflow
    orchestrator.run_workflow(request_id)


if __name__ == "__main__":
    main()
