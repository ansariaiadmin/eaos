"""Critic — evaluates output + one retry if fails."""
from __future__ import annotations


class Critic:
    """Evaluates executor output and decides if retry needed."""

    def evaluate(self, execution_result: dict, original_query: str) -> dict:
        """Evaluate execution result."""
        results = execution_result.get("results", [])
        if not results:
            return {"ok": False, "reason": "no results", "retry": True}

        # Check each result has required fields
        issues = []
        for r in results:
            if not r.get("ok"):
                issues.append(f"task {r.get('task_id')} failed: {r.get('error', r.get('output', {}).get('reason', 'unknown'))}")
            else:
                out = r.get("output", {})
                # Type-specific validation — flattened to avoid SIM102
                if r["type"] == "legal" and not out.get("citations"):
                    issues.append(f"legal task {r['task_id']} missing citations")
                elif r["type"] == "tax" and "tax_minor" not in out:
                    issues.append(f"tax task {r['task_id']} missing tax_minor")
                elif r["type"] == "trading" and "ok" not in out:
                    issues.append(f"trading task {r['task_id']} missing ok field")
                elif r["type"] == "voice" and "transcript" not in out:
                    issues.append(f"voice task {r['task_id']} missing transcript")

        if issues:
            return {
                "ok": False,
                "reason": "; ".join(issues),
                "issues": issues,
                "retry": True,
            }

        return {
            "ok": True,
            "reason": "all tasks passed validation",
            "retry": False,
        }
