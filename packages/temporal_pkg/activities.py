import json
import pathlib

from packages.core.redaction import redact


def run_reconciliation(business_date):
    return {"date": business_date, "matched": 0, "unmatched": [], "status": "ok"}

def check_trading_risk(business_date):
    return {"date": business_date, "daily_loss_pct": 0.0, "breach": False}

def redact_snapshot(payload):
    safe, hits = redact(json.dumps(payload))
    return json.loads(safe) if not hits else {"redacted": safe, "hits": hits}

def run_tax_snapshot(business_date):
    return {"date": business_date, "jurisdictions": ["us_federal"], "filings": []}

def legal_rag(query):
    kb = json.loads(pathlib.Path("packages/legal/kb.json").read_text())
    hits = [d for d in kb["docs"] if any(t in d["text"].lower() for t in query.lower().split())]
    return {"query": query, "citations": hits[:5], "method": "lexical"}
