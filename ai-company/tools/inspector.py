#!/usr/bin/env python3
"""
AI Company Inspector Tool
Validates agent configuration, SKILL.md files, memory structure, and task ordering.
"""

import json
import sys
from pathlib import Path
from typing import Dict, List, Tuple


class InspectorReport:
    """Collects inspection results."""
    
    def __init__(self):
        self.errors = []
        self.warnings = []
        self.info = []
        self.checks_passed = 0
        self.checks_failed = 0
    
    def error(self, message: str):
        self.errors.append(message)
        self.checks_failed += 1
    
    def warning(self, message: str):
        self.warnings.append(message)
    
    def info(self, message: str):
        self.info.append(message)
    
    def pass_check(self):
        self.checks_passed += 1
    
    def print_report(self):
        """Print the inspection report."""
        print("\n" + "="*70)
        print("🔍 AI COMPANY INSPECTOR REPORT")
        print("="*70 + "\n")
        
        # Summary
        total = self.checks_passed + self.checks_failed
        print(f"📊 Summary:")
        print(f"   ✓ Checks Passed: {self.checks_passed}")
        print(f"   ✗ Checks Failed: {self.checks_failed}")
        print(f"   ⚠️  Warnings: {len(self.warnings)}")
        print(f"   ℹ️  Info: {len(self.info)}")
        
        # Errors
        if self.errors:
            print(f"\n❌ ERRORS ({len(self.errors)}):")
            for err in self.errors:
                print(f"   • {err}")
        
        # Warnings
        if self.warnings:
            print(f"\n⚠️  WARNINGS ({len(self.warnings)}):")
            for warn in self.warnings:
                print(f"   • {warn}")
        
        # Info
        if self.info:
            print(f"\nℹ️  INFO:")
            for inf in self.info:
                print(f"   • {inf}")
        
        # Status
        print("\n" + "="*70)
        if self.checks_failed == 0:
            print("✅ INSPECTION PASSED - System is ready to use!")
        else:
            print("❌ INSPECTION FAILED - Please fix errors above")
        print("="*70 + "\n")
        
        return self.checks_failed == 0


class AICompanyInspector:
    """Inspects AI Company configuration and structure."""
    
    REQUIRED_TEAMS = [
        "product",
        "architecture",
        "development",
        "qa",
        "devops",
        "docs",
        "control",
    ]
    
    REQUIRED_SKILLS = {
        "product": ["gather_requirements", "write_spec"],
        "architecture": ["analyze_repo", "design_system"],
        "development": ["plan_tasks", "implement_feature", "refactor_code", "fix_bug"],
        "qa": ["generate_tests", "debug_cycle", "review_code"],
        "devops": ["configure_ci", "deploy_app"],
        "docs": ["update_docs", "write_release_notes"],
        "control": ["critic", "verify_spec"],
    }
    
    REQUIRED_MEMORY_FILES = [
        "repo_summary.md",
        "architecture.md",
        "decisions.md",
        "debug_log.md",
        "review_log.md",
        "verification.md",
        "qa.md",
        "devops.md",
        "docs.md",
        "release_notes.md",
    ]
    
    REQUIRED_SKILL_SECTIONS = [
        "Metadata",
        "Goal",
        "Input",
        "Output Format",
        "Memory Update",
        "Critic Criteria"
    ]
    
    def __init__(self, base_path: str):
        self.base_path = Path(base_path)
        self.report = InspectorReport()
    
    def inspect_structure(self):
        """Check folder structure."""
        print("🏗️  Checking folder structure...")
        
        # Check required directories
        required_dirs = ["skills", "memory", "tasks"]
        for dir_name in required_dirs:
            dir_path = self.base_path / dir_name
            if dir_path.exists():
                self.report.info(f"✓ {dir_name}/ directory exists")
                self.report.pass_check()
            else:
                self.report.error(f"Missing {dir_name}/ directory")
    
    def inspect_teams_and_skills(self):
        """Check all teams and their skills."""
        print("\n👥 Checking teams and skills...")
        
        skills_dir = self.base_path / "skills"
        
        for team in self.REQUIRED_TEAMS:
            team_path = skills_dir / team
            if team_path.exists():
                self.report.info(f"✓ Team '{team}' directory exists")
                self.report.pass_check()
                
                # Check required skills for this team
                required_skills = self.REQUIRED_SKILLS.get(team, [])
                for skill in required_skills:
                    skill_path = team_path / skill / "SKILL.md"
                    if skill_path.exists():
                        self.report.info(f"  ✓ Skill '{skill}' found")
                        self.report.pass_check()
                        self._inspect_skill_file(skill_path)
                    else:
                        self.report.error(f"  Missing skill '{skill}' in team '{team}'")
            else:
                self.report.error(f"Missing team directory: {team_path}")
    
    def _inspect_skill_file(self, skill_path: Path):
        """Inspect a single SKILL.md file."""
        with open(skill_path) as f:
            content = f.read()
        
        skill_name = skill_path.parent.name
        missing_sections = []
        
        for section in self.REQUIRED_SKILL_SECTIONS:
            if f"## {section}" not in content and f"# {section}" not in content:
                missing_sections.append(section)
        
        if missing_sections:
            self.report.warning(f"    Skill '{skill_name}' missing sections: {', '.join(missing_sections)}")
        else:
            self.report.pass_check()
    
    def inspect_memory_system(self):
        """Check memory files."""
        print("\n💾 Checking memory system...")
        
        memory_dir = self.base_path / "memory"
        
        if not memory_dir.exists():
            self.report.error("Memory directory does not exist")
            return
        
        self.report.info("✓ Memory directory exists")
        self.report.pass_check()
        
        for mem_file in self.REQUIRED_MEMORY_FILES:
            mem_path = memory_dir / mem_file
            if mem_path.exists():
                self.report.info(f"  ✓ {mem_file}")
                self.report.pass_check()
            else:
                self.report.error(f"  Missing memory file: {mem_file}")
    
    def inspect_tasks(self):
        """Check task structure."""
        print("\n📋 Checking task structure...")
        
        tasks_dir = self.base_path / "tasks"
        
        if not tasks_dir.exists():
            self.report.info("⚠️  No tasks directory yet (will be created on first run)")
            return
        
        request_dirs = list(tasks_dir.glob("request_*"))
        
        if request_dirs:
            self.report.info(f"✓ Found {len(request_dirs)} request(s)")
            self.report.pass_check()
            
            for req_dir in request_dirs[:3]:  # Check first 3
                task_files = sorted(req_dir.glob("*.md"))
                if task_files:
                    self.report.info(f"  ✓ {req_dir.name}: {len(task_files)} tasks")
                    self.report.pass_check()
                else:
                    self.report.warning(f"  {req_dir.name}: No task files found")
        else:
            self.report.info("⚠️  No task requests created yet")
    
    def inspect_orchestrator(self):
        """Check orchestrator file."""
        print("\n🎯 Checking orchestrator...")
        
        orchestrator_path = self.base_path / "orchestrator.py"
        
        if orchestrator_path.exists():
            self.report.info("✓ orchestrator.py exists")
            self.report.pass_check()
            
            with open(orchestrator_path) as f:
                content = f.read()
            
            required_classes = [
                "AIOrchestratorConfig",
                "AIOrchestrator",
            ]
            
            for cls in required_classes:
                if f"class {cls}" in content:
                    self.report.pass_check()
                else:
                    self.report.error(f"  Missing class: {cls}")
        else:
            self.report.error("orchestrator.py not found")
    
    def inspect_configuration(self):
        """Check configuration."""
        print("\n⚙️  Checking configuration...")
        
        # Check for API key environment variables
        required_keys = [
            "ANTHROPIC_KEY",
            "OPENAI_KEY",
            "GITHUB_COPILOT_TOKEN",
        ]
        
        import os
        for key in required_keys:
            if os.getenv(key):
                self.report.info(f"✓ {key} is set")
                self.report.pass_check()
            else:
                self.report.warning(f"  {key} not set in environment")
    
    def run_all_checks(self) -> bool:
        """Run all inspection checks."""
        print("\n" + "="*70)
        print("🔍 STARTING AI COMPANY INSPECTION")
        print("="*70)
        
        self.inspect_structure()
        self.inspect_teams_and_skills()
        self.inspect_memory_system()
        self.inspect_tasks()
        self.inspect_orchestrator()
        self.inspect_configuration()
        
        return self.report.print_report()


def main():
    """Main entry point."""
    if len(sys.argv) < 2:
        print("Usage: python inspector.py <path> [--validate]")
        print("Example: python inspector.py . --validate")
        sys.exit(1)
    
    base_path = sys.argv[1]
    
    if not Path(base_path).exists():
        print(f"Error: Path does not exist: {base_path}")
        sys.exit(1)
    
    # Run inspection
    inspector = AICompanyInspector(base_path)
    success = inspector.run_all_checks()
    
    sys.exit(0 if success else 1)


if __name__ == "__main__":
    main()
