from decimal import Decimal

from fastapi import FastAPI
from pydantic import BaseModel

from apps.api import db
from packages.core.finance import Ledger, Posting, from_minor, to_minor
from packages.core.router import Router
from packages.legal.rag_agent import LegalRAGAgent
from packages.tax.adapters import ADAPTERS
from packages.trading.guardrails import TradingGuardrails

app = FastAPI(title="Enterprise Agent OS", version="1.0.0")
db.upgrade()
ledger, router, rag, guard = Ledger(), Router(), LegalRAGAgent(), TradingGuardrails()

class PostRequest(BaseModel):
    entry_id: str
    postings: list[dict]

@app.post("/ledger/post")
def post_entry(req: PostRequest):
    e = ledger.post(req.entry_id, [Posting(**p) for p in req.postings])
    return {"id": e.entry_id, "hash": e._hash}

@app.get("/ledger/balances")
def balances():
    return {k: str(from_minor(v)) for k, v in ledger.balances().items()}

@app.get("/ledger/verify")
def verify():
    return {"chain_valid": ledger.verify_chain()}

@app.post("/route")
def route(body: dict):
    return router.route(body.get("prompt", ""), task_type=body.get("task_type", "general"))

@app.post("/legal/ask")
def legal(body: dict):
    return rag.answer(body["query"])

@app.post("/trading/check")
def trading(body: dict):
    return guard.pre_trade_check(float(body["order_value"]), float(body["equity"]), float(body["position"]))

@app.post("/tax/compute")
def tax(body: dict):
    return ADAPTERS[body["jurisdiction"]].compute(to_minor(Decimal(str(body["taxable"]))))
