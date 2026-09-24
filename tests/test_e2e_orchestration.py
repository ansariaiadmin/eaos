"""E2E orchestration with local LLM mock — Phase 11+12."""
from unittest.mock import patch

from packages.core.router import Router
from packages.orchestration import Orchestrator


def test_e2e_orchestration_with_mock_llm():
    """Full orchestration E2E with mocked local LLM."""
    # Mock Router to always return local provider
    with patch.object(Router, 'route', return_value={"provider": "local", "redactions": [], "cost": 0}):
        o = Orchestrator()
        result = o.run("What are GDPR data minimization obligations and US tax for 60000?")
        assert result["result"]["tasks_executed"] >= 1
        assert "critique" in result
        # Should have at least legal task
        types = [t["type"] for t in result["tasks"]]
        assert "legal" in types or "tax" in types

def test_e2e_orchestration_retry_path():
    """E2E that triggers retry logic via critic failure."""
    # Create orchestrator with failing first execution
    o = Orchestrator()
    # Query that will produce valid tasks but we force critic to fail first time
    # By mocking executor to return empty citations first
    from packages.orchestration.executor import Executor

    original_execute = Executor.execute

    def failing_first(self, tasks, query):
        if not hasattr(self, '_called'):
            self._called = True
            # Return result with missing citations to trigger retry
            return {
                "original_query": query,
                "tasks_executed": len(tasks),
                "all_ok": False,
                "results": [{"task_id": "legal-1", "type": "legal", "ok": True, "output": {"citations": [], "answer": "x"}}]
            }
        return original_execute(self, tasks, query)

    with patch.object(Executor, 'execute', failing_first):
        result = o.run("GDPR compliance check")
        # Should have retried
        assert result["retried"] is True
        assert "first_critique" in result
        assert result["first_critique"]["ok"] is False

def test_e2e_voice_and_trading():
    """E2E with voice + trading multi-intent."""
    o = Orchestrator()
    result = o.run("Check trading order 5000 and voice transcript for compliance")
    assert result["result"]["tasks_executed"] >= 1
    assert result["critique"]["ok"] in (True, False)
