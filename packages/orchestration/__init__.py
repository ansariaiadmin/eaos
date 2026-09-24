"""Orchestration package — planner, executor, critic."""
from .critic import Critic
from .executor import Executor
from .planner import Planner


class Orchestrator:
    """Full orchestration: planner -> executor -> critic with one retry."""
    def __init__(self):
        self.planner = Planner()
        self.executor = Executor()
        self.critic = Critic()

    def run(self, query: str) -> dict:
        tasks = self.planner.decompose(query)
        result = self.executor.execute(tasks, query)
        critique = self.critic.evaluate(result, query)
        if not critique["ok"] and critique.get("retry"):
            # One retry
            tasks_retry = self.planner.decompose(query, retry=True)
            result_retry = self.executor.execute(tasks_retry, query)
            critique_retry = self.critic.evaluate(result_retry, query)
            return {
                "query": query,
                "tasks": tasks_retry,
                "result": result_retry,
                "critique": critique_retry,
                "retried": True,
                "first_critique": critique,
            }
        return {
            "query": query,
            "tasks": tasks,
            "result": result,
            "critique": critique,
            "retried": False,
        }
