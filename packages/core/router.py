"""Hybrid LLM router: privacy-first, cost-aware."""
from __future__ import annotations
import yaml, datetime, pathlib
from .redaction import redact

class Router:
    def __init__(self, cfg_path="configs/settings.yaml"):
        self.cfg = yaml.safe_load(pathlib.Path(cfg_path).read_text())
        self.spend_today = 0.0
        self._day = datetime.date.today()

    def _reset(self):
        if self._day != datetime.date.today():
            self._day, self.spend_today = datetime.date.today(), 0.0

    def route(self, prompt, *, task_type="general", local_confidence=0.5):
        self._reset()
        safe, hits = redact(prompt)
        cap = self.cfg["llm"]["max_daily_spend_usd"]
        privacy_sensitive = bool(hits) or task_type in ("finance", "tax", "legal", "voice")
        if privacy_sensitive or self.spend_today >= cap or local_confidence >= 0.6:
            return {"provider": "local", "prompt": safe, "redactions": hits, "reason": "privacy-first"}
        cloud = next(p for p in self.cfg["llm"]["providers"] if p["name"] == "cloud")
        est = cloud["cost_per_1k_tokens"] * len(prompt)
        if self.spend_today + est > cap:
            return {"provider": "local", "prompt": safe, "redactions": hits, "reason": "spend-cap"}
        self.spend_today += est
        return {"provider": cloud["name"], "prompt": safe, "redactions": hits, "reason": "low-cost-ok"}
