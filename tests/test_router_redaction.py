from packages.core.redaction import redact
from packages.core.router import Router


def test_redact_iban_email():
    out, hits = redact("pay to DE89370400440532013000 at a@b.com")
    assert "IBAN" in hits and "EMAIL" in hits and "DE8937" not in out

def test_privacy_routes_local():
    r = Router()
    res = r.route("my national id 1234567890", task_type="general")
    assert res["provider"] == "local" and res["redactions"]

def test_cost_cap_forces_local():
    r = Router()
    r.spend_today = 99.0
    res = r.route("hello generic world", task_type="general", local_confidence=0.1)
    assert res["provider"] == "local"

def test_low_risk_can_go_cloud():
    r = Router()
    res = r.route("summarize this generic marketing text", task_type="general", local_confidence=0.1)
    assert res["provider"] == "cloud"
