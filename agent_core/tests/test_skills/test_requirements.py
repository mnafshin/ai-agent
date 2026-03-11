"""
Tests for the gather_requirements skill (SKILL.md presence & format).
"""
import sys
from pathlib import Path
import pytest

sys.path.insert(0, str(Path(__file__).parent.parent.parent.parent))

SKILLS_ROOT = Path(__file__).parent.parent.parent / "skills"
REQUIRED_SECTIONS = ["## Metadata", "## Goal", "## Input", "## Output Format", "## Memory Update", "## Critic Criteria"]


def _read_skill(team: str, skill: str) -> str:
    skill_file = SKILLS_ROOT / team / skill / "SKILL.md"
    assert skill_file.exists(), f"SKILL.md missing: {skill_file}"
    return skill_file.read_text(encoding="utf-8")


class TestGatherRequirementsSkill:
    def test_skill_file_exists(self):
        assert (SKILLS_ROOT / "product" / "gather_requirements" / "SKILL.md").exists()

    @pytest.mark.parametrize("section", REQUIRED_SECTIONS)
    def test_has_required_section(self, section):
        content = _read_skill("product", "gather_requirements")
        assert section in content, f"Missing section '{section}'"


class TestWriteSpecSkill:
    def test_skill_file_exists(self):
        assert (SKILLS_ROOT / "product" / "write_spec" / "SKILL.md").exists()

    @pytest.mark.parametrize("section", REQUIRED_SECTIONS)
    def test_has_required_section(self, section):
        content = _read_skill("product", "write_spec")
        assert section in content, f"Missing section '{section}'"

