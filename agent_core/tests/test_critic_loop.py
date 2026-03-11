"""
Tests for the critic loop logic inside AIOrchestrator.
"""
import sys
from pathlib import Path
import pytest

# Make sure agent_core is importable
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from orchestrator import AIOrchestrator, AIOrchestratorConfig


class TestAdaptiveThresholds:
    def test_feature_threshold(self):
        assert AIOrchestratorConfig.get_threshold("feature") == 90

    def test_hotfix_threshold_is_lower(self):
        assert AIOrchestratorConfig.get_threshold("hotfix") < AIOrchestratorConfig.get_threshold("feature")

    def test_security_patch_threshold_is_highest(self):
        assert AIOrchestratorConfig.get_threshold("security_patch") >= 98

    def test_unknown_type_returns_default(self):
        assert AIOrchestratorConfig.get_threshold("unknown_type") == AIOrchestratorConfig.CRITIC_THRESHOLD


class TestTeamRouting:
    def test_hotfix_skips_product_team(self):
        teams = AIOrchestratorConfig.get_teams_for_request("hotfix")
        assert "product" not in teams

    def test_feature_includes_all_teams(self):
        teams = AIOrchestratorConfig.get_teams_for_request("feature")
        assert "product" in teams
        assert "qa" in teams
        assert "docs" in teams

    def test_unknown_request_returns_all_teams(self):
        teams = AIOrchestratorConfig.get_teams_for_request("unknown")
        assert teams == AIOrchestratorConfig.ALL_TEAMS


class TestCriticLoop:
    def setup_method(self):
        base = Path(__file__).parent.parent
        self.orchestrator = AIOrchestrator(str(base))

    def test_critic_loop_returns_tuple(self):
        result, score = self.orchestrator.run_critic_loop("write_spec", "sample input", "feature")
        assert isinstance(result, str)
        assert isinstance(score, (int, float))

    def test_critic_loop_score_above_threshold(self):
        """Score should reach threshold within MAX_ITERATIONS."""
        threshold = AIOrchestratorConfig.get_threshold("feature")
        _, score = self.orchestrator.run_critic_loop("write_spec", "sample", "feature")
        assert score >= threshold

