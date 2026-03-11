"""
Tests for spec verification logic inside AIOrchestrator.
"""
import sys
from pathlib import Path
import pytest

sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from orchestrator import AIOrchestrator


class TestSpecVerification:
    def setup_method(self):
        base = Path(__file__).parent.parent
        self.orchestrator = AIOrchestrator(str(base))

    def test_verify_spec_returns_dict(self):
        result = self.orchestrator.verify_spec("some solution", "some spec")
        assert isinstance(result, dict)

    def test_verify_spec_has_required_keys(self):
        result = self.orchestrator.verify_spec("solution", "specification")
        assert "valid" in result
        assert "compliance_score" in result
        assert "issues" in result

    def test_compliance_score_in_range(self):
        result = self.orchestrator.verify_spec("solution", "specification")
        assert 0 <= result["compliance_score"] <= 100

    def test_issues_is_list(self):
        result = self.orchestrator.verify_spec("solution", "specification")
        assert isinstance(result["issues"], list)

