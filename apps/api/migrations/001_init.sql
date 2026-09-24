CREATE TABLE ledger_entries (id TEXT PRIMARY KEY, ts TEXT, hash TEXT, prev_hash TEXT);
CREATE TABLE ledger_postings (entry_id TEXT, account TEXT, minor INTEGER, memo TEXT);
CREATE TABLE audit_log (id INTEGER PRIMARY KEY AUTOINCREMENT, ts TEXT, actor TEXT, action TEXT, payload TEXT);
CREATE TABLE llm_routes (id INTEGER PRIMARY KEY AUTOINCREMENT, ts TEXT, provider TEXT, reason TEXT, redactions TEXT);
