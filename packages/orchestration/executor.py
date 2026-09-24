"""Executor — dispatch to specialists: legal/tax/trading/voice."""
from __future__ import annotations

from packages.core.router import Router
from packages.legal.rag_agent import LegalRAGAgent
from packages.tax.adapters import ADAPTERS
from packages.trading.guardrails import TradingGuardrails
from packages.voice.pipeline import VoiceConfig, VoicePipeline


class Executor:
    """Dispatches tasks to specialist agents."""

    def __init__(self):
        self.rag = LegalRAGAgent()
        self.guard = TradingGuardrails()
        self.router = Router()

    def execute(self, tasks: list[dict], original_query: str) -> dict:
        """Execute tasks and return aggregated results."""
        results = []
        for task in tasks:
            t_type = task.get("type", "legal")
            params = task.get("params", {})
            try:
                if t_type == "legal":
                    out = self.rag.answer(task.get("query", original_query))
                    results.append({"task_id": task["id"], "type": t_type, "ok": True, "output": out})
                elif t_type == "tax":
                    jurisdiction = params.get("jurisdiction", "us_federal")
                    taxable = params.get("taxable", 500_000_000)
                    adapter = ADAPTERS.get(jurisdiction, ADAPTERS["us_federal"])
                    out = adapter.compute(taxable)
                    results.append({"task_id": task["id"], "type": t_type, "ok": True, "output": out})
                elif t_type == "trading":
                    out = self.guard.pre_trade_check(
                        params.get("order_value", 5000.0),
                        params.get("equity", 100000.0),
                        params.get("position", 0.0),
                    )
                    results.append({"task_id": task["id"], "type": t_type, "ok": out.get("ok", False), "output": out})
                elif t_type == "voice":
                    vp = VoicePipeline(VoiceConfig(), self.router)
                    audio = params.get("audio", original_query.encode("utf-8"))
                    out = vp.handle(audio if isinstance(audio, bytes) else str(audio).encode("utf-8"))
                    results.append({"task_id": task["id"], "type": t_type, "ok": True, "output": out})
                else:
                    results.append({"task_id": task["id"], "type": t_type, "ok": False, "error": f"unknown specialist {t_type}"})
            except Exception as e:  # noqa: BLE001 - executor must catch all specialist errors
                results.append({"task_id": task["id"], "type": t_type, "ok": False, "error": str(e)})

        # Aggregate
        all_ok = all(r.get("ok") for r in results) if results else False
        return {
            "original_query": original_query,
            "tasks_executed": len(results),
            "all_ok": all_ok,
            "results": results,
        }
