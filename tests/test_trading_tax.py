from packages.trading.guardrails import TradingGuardrails
from packages.tax.adapters import ADAPTERS
from packages.core.finance import from_minor

def test_position_cap():
    g = TradingGuardrails()
    assert not g.pre_trade_check(20_000, 100_000, 0)["ok"]

def test_position_within_cap():
    g = TradingGuardrails()
    assert g.pre_trade_check(5_000, 100_000, 0)["ok"]

def test_kill_switch():
    g = TradingGuardrails(); g.trigger_kill_switch()
    assert not g.pre_trade_check(1, 1_000_000, 0)["ok"]

def test_daily_loss_breach_triggers_kill():
    g = TradingGuardrails()
    g.mark_to_market(-2_500, equity=100_000)  # > 2% loss
    assert g.killed

def test_us_tax_bracket():
    r = ADAPTERS["us_federal"].compute(500_000_000)  # 50,000.0000
    assert r["tax_minor"] == 57_680_000  # 11600*0.10 + 38400*0.12

def test_tax_roundtrip():
    v = ADAPTERS["us_federal"].compute(100_000_000)["tax_minor"]
    assert from_minor(v) > 0

def test_ir_adapter():
    assert ADAPTERS["ir_anonymized"].compute(10_000_000)["tax_minor"] == 1_500_000
