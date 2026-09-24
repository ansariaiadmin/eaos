# AGENT_HANDOFF.md — Enterprise Agent OS (EAOS)

**Read this file completely before touching any code.** It contains everything a
fresh AI agent needs to launch, understand, and extend this repo.

---

## 1. What this project is

**Local-first Enterprise Agent OS** — a monorepo implementing phases 1–10 of a
roadmap: a deterministic double-entry finance core, a privacy-first hybrid LLM
router with a redaction engine, voice pipeline templates, Temporal workflows, a
legal RAG agent, trading guardrails, tax adapters, a React dashboard with a
React Flow DAG visualizer, and a full pytest suite.

**Locked architectural decisions (do NOT change these):**

1. **Local-first**: SQLite is the default DB (`configs/settings.yaml: db: sqlite:///eaos.db`). No cloud dependency required to run.
2. **Money is integer minor units** (scale 1e-4, `CENTS = 10_000`). **No floats ever cross a ledger boundary.** Use `to_minor` / `from_minor` from `packages/core/finance.py` exclusively.
3. **The ledger is append-only and hash-chained** (SHA-256, `prev` link, genesis = `"GENESIS"`). Every entry must balance to 0 minor units. Never mutate history; verify with `GET /ledger/verify`.
4. **Privacy-first routing**: redaction runs BEFORE any prompt leaves the process. The router (`packages/core/router.py`) prefers the local provider (Ollama `llama3-8b` at `http://localhost:11434`); the cloud provider is gated by a daily cost cap (`max_daily_spend_usd: 5.0`) and a privacy/confidence policy in `configs/prompts/router_policy.md`.
5. **Tax adapters** are US federal 2024 brackets + an *anonymized* Iran adapter. No PII is ever sent to a tax computation.
6. **Trading guardrails**: `max_position_pct: 0.10`, `max_daily_loss_pct: 0.02`, kill switch enabled. Pre-trade check must pass before any order.
7. **Python 3.11+**, FastAPI 0.111, Pydantic v2, SQLAlchemy 2, Temporal 1.6. Frontend: Vite + React + React Flow.

---

## 2. Folder tour

```
eaos/
├── AGENT_HANDOFF.md        ← you are here
├── ROADMAP.md              ← phases 1–10 done; 11–16 pending (see §5)
├── README.md, Makefile, requirements.txt, pyproject.toml
├── apps/
│   ├── api/                ← FastAPI app
│   │   ├── main.py         ← all HTTP endpoints (see §3)
│   │   ├── db.py           ← SQLite engine + migrations runner
│   │   └── migrations/001_init.sql
│   └── web/                ← Vite + React dashboard
│       ├── index.html, vite.config.js, package.json
│       └── src/{main.jsx, Dashboard.jsx, AgentDAG.jsx}
├── packages/
│   ├── core/
│   │   ├── finance.py      ← Ledger, Posting, JournalEntry, to_minor/from_minor
│   │   ├── router.py       ← hybrid LLM router (privacy + cost cap)
│   │   └── redaction.py    ← IBAN/NID/PAN/EMAIL/PHONE/SECRETS scrubber
│   ├── legal/
│   │   ├── rag_agent.py    ← lexical retrieval + cited answers (local-only)
│   │   └── kb.json         ← tiny local knowledge base
│   ├── trading/guardrails.py ← position caps, loss limit, kill switch
│   ├── tax/adapters.py     ← ADAPTERS dict: us_federal, ir_anonymized
│   ├── voice/pipeline.py   ← STT → redact → route → LLM → TTS templates
│   └── temporal_pkg/
│       ├── workflows.py    ← DailyCloseWorkflow, LegalResearchWorkflow
│       ├── activities.py   ← reconciliation, risk check, redact, tax, RAG
│       └── worker.py       ← connects to Temporal at localhost:7233
├── tests/                  ← pytest suite (5 test files)
└── configs/
    ├── settings.yaml       ← single source of runtime config
    └── prompts/router_policy.md
```

---

## 3. API surface (apps/api/main.py)

| Method | Path                | Body / notes |
|--------|---------------------|--------------|
| POST   | `/ledger/post`      | `{entry_id, postings:[{account, minor, memo}]}` — must sum to 0 |
| GET    | `/ledger/balances`  | account → decimal string |
| GET    | `/ledger/verify`    | `{chain_valid: bool}` |
| POST   | `/route`            | `{prompt, task_type}` → routed LLM decision |
| POST   | `/legal/ask`        | `{query}` → cited RAG answer |
| POST   | `/trading/check`    | `{order_value, equity, position}` → guardrail verdict |
| POST   | `/tax/compute`      | `{jurisdiction, taxable}` → tax in minor units |

App import path: `apps.api.main:app`. DB auto-migrates on startup (`db.upgrade()`).

---

## 4. Exact launch commands

```bash
# 1) Environment
cd eaos
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt

# 2) Run tests first (expect green)
pytest -q

# 3) Start the API (http://localhost:8000, docs at /docs)
uvicorn apps.api.main:app --reload --port 8000

# 4) Start the dashboard
cd apps/web && npm install && npm run dev   # http://localhost:5173

# 5) Optional: local LLM backend
ollama serve && ollama pull llama3-8b

# 6) Optional: Temporal workflows
temporal server start-dev          # listens on localhost:7233
python -m packages.temporal_pkg.worker

# Makefile shortcuts: make run-api | make run-web | make test
```

Smoke test:
```bash
curl -s localhost:8000/ledger/verify
curl -s -X POST localhost:8000/ledger/post -H 'Content-Type: application/json' \
  -d '{"entry_id":"t1","postings":[{"account":"cash","minor":10000},{"account":"revenue","minor":-10000}]}'
curl -s localhost:8000/ledger/balances
```

---

## 5. Next phases (11–16) for the next agent

11. **Multi-agent orchestration** — planner/executor/critic loop on top of `core/router.py`.
12. **Vector store + embeddings** for `legal/rag_agent.py` (keep it local: e.g. sentence-transformers + FAISS/Chroma in SQLite dir).
13. **Plugin marketplace & signed skills** — skills manifest + signature verification before load.
14. **Real broker integration** — paper trading FIRST, then live; must call `trading/guardrails.py` pre-trade check unconditionally.
15. **Local fine-tuning loop** on redacted data only.
16. **Audit evidence vault** — WORM (write-once) storage for ledger entries, RAG citations, and trading decisions.

**Working rules for the next agent:**
- Never bypass redaction before any external LLM call.
- Never store money as float; always `to_minor` on ingest, `from_minor` on display.
- Keep the ledger hash chain intact — write new code as append-only, verify after every write.
- New config goes in `configs/settings.yaml`; new tables get a numbered migration in `apps/api/migrations/`.
- Add pytest tests for every new package; keep the suite green before committing.
