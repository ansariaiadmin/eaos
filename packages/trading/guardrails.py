"""Trading guardrails: position caps, loss limit, kill switch. Fail-closed."""
from __future__ import annotations
import yaml, pathlib

class TradingGuardrails:
    def __init__(self, cfg_path="configs/settings.yaml"):
        self.cfg = yaml.safe_load(pathlib.Path(cfg_path).read_text())["trading"]
        self.daily_pnl = 0.0
        self.killed = False

    def pre_trade_check(self, order_value, equity, proposed_position):
        if self.killed:
            return {"ok": False, "reason": "kill-switch-active"}
        max_pos = equity * self.cfg["max_position_pct"]
        if proposed_position + order_value > max_pos:
            return {"ok": False, "reason": "position-cap %.2f" % max_pos}
        return {"ok": True, "reason": "within-limits"}

    def mark_to_market(self, pnl_delta, equity=None):
        self.daily_pnl += pnl_delta
        breach = False
        if equity and self.daily_pnl < 0:
            breach = -self.daily_pnl > equity * self.cfg["max_daily_loss_pct"]
            if breach and self.cfg["kill_switch"]:
                self.killed = True
        return {"daily_pnl": self.daily_pnl, "breach": breach}

    def trigger_kill_switch(self):
        self.killed = True
        return {"kill_switch": True}
