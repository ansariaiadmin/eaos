"""Deterministic finance core. Money stored as integer minor units (1e-4).
No floats cross a ledger boundary."""
from __future__ import annotations

import datetime
import hashlib
import json
from dataclasses import dataclass
from decimal import ROUND_HALF_UP, Decimal, getcontext

getcontext().prec = 28
CENTS = 10_000

def to_minor(amount) -> int:
    d = Decimal(str(amount)).scaleb(4)
    assert d == d.to_integral_value(), f"more than 4 dp: {amount}"
    return int(d)

def from_minor(m: int) -> Decimal:
    return (Decimal(m) / Decimal(CENTS)).quantize(Decimal("0.0001"), rounding=ROUND_HALF_UP)

class LedgerError(Exception):
    pass

@dataclass
class Posting:
    account: str
    minor: int
    memo: str = ""

@dataclass
class JournalEntry:
    id: str
    ts: str
    postings: list
    _hash: str = ""

    def hash(self, prev: str) -> str:
        payload = json.dumps({"id": self.id, "ts": self.ts, "prev": prev,
                              "postings": [[p.account, p.minor, p.memo] for p in self.postings]},
                             sort_keys=True, separators=(",", ":"))
        return hashlib.sha256(payload.encode()).hexdigest()

class Ledger:
    """Append-only double-entry ledger with SHA-256 hash chaining."""
    def __init__(self):
        self.entries = []
        self._prev = "GENESIS"

    def post(self, eid, postings, ts=None):
        if sum(p.minor for p in postings) != 0:
            raise LedgerError("entry not balanced: sum != 0")
        if any(e.id == eid for e in self.entries):
            raise LedgerError("duplicate entry id")
        e = JournalEntry(id=eid, ts=ts or datetime.datetime.now(datetime.UTC).isoformat().replace("+00:00", "Z"),
                         postings=list(postings))
        e._hash = e.hash(self._prev)
        self.entries.append(e)
        self._prev = e._hash
        return e

    def verify_chain(self) -> bool:
        prev = "GENESIS"
        for e in self.entries:
            if e.hash(prev) != e._hash:
                return False
            prev = e._hash
        return True

    def balances(self) -> dict:
        out = {}
        for e in self.entries:
            for p in e.postings:
                out[p.account] = out.get(p.account, 0) + p.minor
        return out
