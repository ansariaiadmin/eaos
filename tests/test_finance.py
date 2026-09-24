import pytest
from decimal import Decimal
from packages.core.finance import Ledger, Posting, to_minor, from_minor, LedgerError

def test_double_entry_balance():
    l = Ledger()
    l.post("e1", [Posting("cash", 1_000_000), Posting("revenue", -1_000_000)])
    assert l.verify_chain() and l.balances()["cash"] == 1_000_000

def test_unbalanced_rejected():
    with pytest.raises(LedgerError):
        Ledger().post("e2", [Posting("a", 100), Posting("b", -99)])

def test_roundtrip_minor():
    assert from_minor(to_minor(Decimal("1234.5678"))) == Decimal("1234.5678")

def test_chain_tamper_detected():
    l = Ledger()
    l.post("e1", [Posting("a", 1), Posting("b", -1)])
    l.entries[0].postings[0].minor = 999
    assert not l.verify_chain()
