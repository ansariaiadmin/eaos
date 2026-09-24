from sqlalchemy import create_engine, text
import os
URL = os.environ.get("EAOS_DB", "sqlite:///eaos.db")
engine = create_engine(URL, future=True)
MIGRATIONS = [
    "CREATE TABLE IF NOT EXISTS ledger_entries (id TEXT PRIMARY KEY, ts TEXT, hash TEXT, prev_hash TEXT)",
    "CREATE TABLE IF NOT EXISTS ledger_postings (entry_id TEXT, account TEXT, minor INTEGER, memo TEXT)",
    "CREATE TABLE IF NOT EXISTS audit_log (id INTEGER PRIMARY KEY AUTOINCREMENT, ts TEXT, actor TEXT, action TEXT, payload TEXT)",
    "CREATE TABLE IF NOT EXISTS llm_routes (id INTEGER PRIMARY KEY AUTOINCREMENT, ts TEXT, provider TEXT, reason TEXT, redactions TEXT)",
]

def upgrade():
    with engine.begin() as c:
        for m in MIGRATIONS:
            c.execute(text(m))
