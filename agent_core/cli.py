#!/usr/bin/env python3
"""
Agent CLI - Command interface for orchestrating AI agents.

Supports piping from gh/glab CLIs for seamless MR/PR integration.
Usage:
  agent execute task.md          # Run all 20 agents on task
  agent review < diff.txt        # Review piped diff
  gh pr diff | agent review      # Review PR directly
"""

import click
import json
import sys
from pathlib import Path
from typing import Dict, Any
from datetime import datetime

# Load .env files before anything else
from dotenv import load_dotenv
load_dotenv(Path(__file__).parent / '.env')              # agent_core/.env
load_dotenv(Path(__file__).parent.parent / '.env')       # project root .env

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent))

from orchestrator import AIOrchestrator
from tools.memory_manager import MemoryManager

__version__ = "1.0.0"


class AgentCLI:
    """Main CLI handler for agent orchestration."""

    def __init__(self):
        self.orchestrator = None
        self.memory_manager = None
        self._init_managers()

    def _init_managers(self):
        """Initialize orchestrator and memory manager."""
        # base_path = agent_core/ directory (where orchestrator.py lives)
        base_path = Path(__file__).parent
        memory_path = base_path / "memory"

        try:
            self.memory_manager = MemoryManager(memory_path)
        except Exception as e:
            click.echo(f"Warning: Memory manager unavailable: {e}", err=True)

        self.orchestrator = AIOrchestrator(str(base_path), use_request_scope=True)

    def format_output(self, data: Dict[str, Any], format_type: str = "json") -> str:
        """Format output for piping."""
        if format_type == "json":
            return json.dumps(data, indent=2)
        elif format_type == "text":
            return self._format_text(data)
        else:
            return json.dumps(data, indent=2)

    @staticmethod
    def _format_text(data: Dict[str, Any]) -> str:
        """Format data as human-readable text."""
        output = []
        if "status" in data:
            output.append(f"Status: {data['status']}")
        if "results" in data:
            output.append("\n=== Results ===")
            for key, value in data["results"].items():
                output.append(f"\n{key}:")
                if isinstance(value, dict):
                    for k, v in value.items():
                        output.append(f"  {k}: {v}")
                else:
                    output.append(f"  {value}")
        if "errors" in data and data["errors"]:
            output.append("\n=== Errors ===")
            for error in data["errors"]:
                output.append(f"  - {error}")
        return "\n".join(output)


@click.group()
@click.version_option(version=__version__)
def cli():
    """Agent CLI - Orchestrate AI agents for code tasks."""
    pass


@cli.command()
@click.argument("task", type=click.File("r"), default="-", required=False)
@click.option(
    "--format",
    "output_format",
    type=click.Choice(["json", "text"]),
    default="json",
    help="Output format (json or text).",
)
@click.option(
    "--request-id",
    default=None,
    help="Request ID for scoped memory (auto-generated if not provided).",
)
@click.option(
    "--verbose",
    is_flag=True,
    help="Verbose output with detailed agent logs.",
)
def execute(task, output_format: str, request_id: str, verbose: bool):
    """
    Execute all 20 agents on a task.

    TASK can be a file path or piped input.
    
    Examples:
        agent execute task.md
        cat task.md | agent execute
        agent execute -  # Read from stdin
    """
    try:
        cli_handler = AgentCLI()
        
        # Read task input
        if task is None or task == sys.stdin:
            task_input = sys.stdin.read()
        else:
            tsk_content = task.read()
            task_input = tsk_content

        if not task_input.strip():
            raise click.UsageError("No task input provided")

        # Generate request ID if not provided
        if not request_id:
            request_id = f"cli_{datetime.now().strftime('%Y%m%d_%H%M%S')}"

        click.echo(f"Executing task with all 20 agents...", err=True)
        if verbose:
            click.echo(f"Request ID: {request_id}", err=True)

        # Orchestrate execution with all agents
        results = {
            "status": "executing",
            "request_id": request_id,
            "timestamp": datetime.now().isoformat(),
            "task_preview": task_input[:200] + "..." if len(task_input) > 200 else task_input,
            "agents": 20,
            "results": {},
            "errors": [],
        }

        # Run orchestrator (all 20 agents)
        try:
            # Run workflow with all skills
            workflow_result = cli_handler.orchestrator.run_workflow(request_id)
            
            # Collect results from workflow execution
            results["results"] = {
                "workflow": "executed",
                "request_id": request_id,
                "status": "completed"
            }
            results["status"] = "completed"
            
            # Optionally consolidate findings into global memory
            if cli_handler.memory_manager:
                try:
                    cli_handler.memory_manager.consolidate_request(request_id)
                except Exception as e:
                    results["warnings"] = [f"Memory consolidation failed: {e}"]

        except Exception as e:
            results["status"] = "failed"
            results["errors"].append(str(e))
            if verbose:
                click.echo(f"Error during orchestration: {e}", err=True)

        # Output results
        output = cli_handler.format_output(results, output_format)
        click.echo(output)

    except Exception as e:
        error_output = {
            "status": "error",
            "error": str(e),
            "timestamp": datetime.now().isoformat(),
        }
        click.echo(cli_handler.format_output(error_output, output_format))
        sys.exit(1)


@cli.command()
@click.argument("code_input", type=click.File("r"), default="-", required=False)
@click.option(
    "--format",
    "output_format",
    type=click.Choice(["json", "text"]),
    default="json",
    help="Output format.",
)
@click.option(
    "--file",
    "file_path",
    default=None,
    help="File path being reviewed (for context).",
)
@click.option(
    "--verbose",
    is_flag=True,
    help="Verbose review with detailed findings.",
)
def review(code_input, output_format: str, file_path: str, verbose: bool):
    """
    Review code using the review agent.

    Accepts piped input (diff, PR, or code).

    Examples:
        gh pr diff | agent review
        glab mr diff | agent review
        agent review < src/app.py
        agent review --file src/app.py < code_snippet.txt
    """
    try:
        cli_handler = AgentCLI()

        # Read review input
        if code_input is None or code_input == sys.stdin:
            review_input = sys.stdin.read()
        else:
            review_input = code_input.read()

        if not review_input.strip():
            raise click.UsageError("No code input provided")

        click.echo(f"Running review agent...", err=True)

        results = {
            "status": "reviewing",
            "timestamp": datetime.now().isoformat(),
            "input_preview": review_input[:100] + "..." if len(review_input) > 100 else review_input,
            "file": file_path,
            "results": {},
            "errors": [],
        }

        # Run review agent
        try:
            review_result = cli_handler.orchestrator.run_skill(
                skill_name="review_code",
                input_text=review_input,
            )
            
            results["results"] = {
                "review": review_result,
                "status": "completed"
            }
            results["status"] = "completed"

        except Exception as e:
            results["status"] = "failed"
            results["errors"].append(str(e))
            if verbose:
                click.echo(f"Error during review: {e}", err=True)

        # Output results
        output = cli_handler.format_output(results, output_format)
        click.echo(output)

    except Exception as e:
        error_output = {
            "status": "error",
            "error": str(e),
            "timestamp": datetime.now().isoformat(),
        }
        click.echo(json.dumps(error_output, indent=2))
        sys.exit(1)


@cli.command()
@click.argument("code", type=click.File("r"), default="-", required=False)
@click.option(
    "--format",
    "output_format",
    type=click.Choice(["json", "text"]),
    default="json",
    help="Output format.",
)
@click.option(
    "--language",
    default=None,
    help="Programming language (auto-detect if not provided).",
)
def analyze(code, output_format: str, language: str):
    """
    Analyze code using the architect agent.

    Examples:
        agent analyze < src/app.py
        cat src/module.js | agent analyze --language javascript
    """
    try:
        cli_handler = AgentCLI()

        # Read code input
        if code is None or code == sys.stdin:
            code_input = sys.stdin.read()
        else:
            code_input = code.read()

        if not code_input.strip():
            raise click.UsageError("No code input provided")

        click.echo(f"Analyzing code...", err=True)

        results = {
            "status": "analyzing",
            "timestamp": datetime.now().isoformat(),
            "language": language,
            "input_size": len(code_input),
            "results": {},
            "errors": [],
        }

        # Run analysis
        try:
            analysis_result = cli_handler.orchestrator.run_skill(
                skill_name="analyze_repo",
                input_text=code_input,
            )
            
            results["results"] = {
                "analysis": analysis_result,
                "status": "completed"
            }
            results["status"] = "completed"

        except Exception as e:
            results["status"] = "failed"
            results["errors"].append(str(e))

        # Output results
        output = cli_handler.format_output(results, output_format)
        click.echo(output)

    except Exception as e:
        error_output = {
            "status": "error",
            "error": str(e),
            "timestamp": datetime.now().isoformat(),
        }
        click.echo(json.dumps(error_output, indent=2))
        sys.exit(1)


@cli.command()
@click.option(
    "--format",
    "output_format",
    type=click.Choice(["json", "text"]),
    default="text",
    help="Output format.",
)
def status(output_format: str):
    """
    Show agent system status and available agents.

    Examples:
        agent status
        agent status --format json
    """
    try:
        cli_handler = AgentCLI()

        status_data = {
            "system": "Agent CLI",
            "version": __version__,
            "timestamp": datetime.now().isoformat(),
            "orchestrator": "ready",
            "memory_manager": "ready" if cli_handler.memory_manager else "unavailable",
            "agents_available": 20,
            "agents": [
                "architect", "critic", "planner", "coder", "tester",
                "reviewer", "documenter", "security", "performance", "accessibility",
                "devops", "quality", "refactor", "debug", "mentor",
                "researcher", "validator", "optimizer", "integrator", "lead",
            ],
        }

        output = cli_handler.format_output(status_data, output_format)
        click.echo(output)

    except Exception as e:
        click.echo(json.dumps({"status": "error", "error": str(e)}))
        sys.exit(1)


if __name__ == "__main__":
    cli()
