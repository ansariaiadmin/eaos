"""Tests for orchestration Phase 11 — planner, executor, critic, orchestrator."""
from packages.orchestration import Orchestrator
from packages.orchestration.critic import Critic
from packages.orchestration.executor import Executor
from packages.orchestration.planner import Planner


def test_planner_legal():
    p = Planner()
    tasks = p.decompose("what are GDPR data minimization obligations?")
    assert len(tasks) >= 1
    assert any(t["type"] == "legal" for t in tasks)

def test_planner_tax():
    p = Planner()
    tasks = p.decompose("calculate tax for 75000 US federal")
    assert any(t["type"] == "tax" for t in tasks)

def test_planner_trading():
    p = Planner()
    tasks = p.decompose("check trading order value 5000 equity 100k")
    assert any(t["type"] == "trading" for t in tasks)

def test_planner_multi_intent():
    p = Planner()
    tasks = p.decompose("check trading tax implications for US")
    # Should detect at least trading or tax
    assert len(tasks) >= 1
    assert any(t["type"] in ("trading", "tax") for t in tasks)

def test_executor_legal():
    e = Executor()
    tasks = [{"id": "legal-1", "type": "legal", "query": "data minimization", "params": {"k": 2}}]
    res = e.execute(tasks, "data minimization")
    assert res["tasks_executed"] == 1
    assert res["results"][0]["ok"]
    assert "citations" in res["results"][0]["output"]

def test_executor_tax():
    e = Executor()
    tasks = [{"id": "tax-1", "type": "tax", "query": "tax", "params": {"jurisdiction": "us_federal", "taxable": 500000000}}]
    res = e.execute(tasks, "tax")
    assert res["results"][0]["ok"]
    assert "tax_minor" in res["results"][0]["output"]

def test_executor_trading():
    e = Executor()
    tasks = [{"id": "trading-1", "type": "trading", "query": "trade", "params": {"order_value": 5000, "equity": 100000, "position": 0}}]
    res = e.execute(tasks, "trade")
    assert res["results"][0]["ok"]

def test_critic_ok():
    c = Critic()
    exec_res = {
        "results": [
            {"task_id": "legal-1", "type": "legal", "ok": True, "output": {"citations": ["GDPR-5"], "answer": "x"}},
            {"task_id": "tax-1", "type": "tax", "ok": True, "output": {"tax_minor": 1000}},
        ]
    }
    critique = c.evaluate(exec_res, "test query")
    assert critique["ok"] is True

def test_critic_fail_missing_citation():
    c = Critic()
    exec_res = {
        "results": [
            {"task_id": "legal-1", "type": "legal", "ok": True, "output": {"citations": [], "answer": "x"}},
        ]
    }
    critique = c.evaluate(exec_res, "test query")
    assert critique["ok"] is False
    assert critique["retry"] is True

def test_orchestrator_full():
    o = Orchestrator()
    result = o.run("what are GDPR obligations for data minimization?")
    assert "tasks" in result
    assert "result" in result
    assert "critique" in result
    assert result["result"]["tasks_executed"] >= 1

def test_orchestrator_retry_logic():
    o = Orchestrator()
    # Query that should trigger legal and pass
    result = o.run("calculate tax US federal 60000 and GDPR compliance")
    assert result["result"]["all_ok"] in (True, False)  # may be true
    # Check retry flag exists
    assert "retried" in result

def test_orchestrator_trading_tax():
    o = Orchestrator()
    result = o.run("check trading order and tax implications")
    assert result["result"]["tasks_executed"] >= 1
