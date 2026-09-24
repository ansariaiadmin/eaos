# Local-First Enterprise Agent OS (Phases 1-10)
Deterministic finance core, hybrid LLM router with redaction, voice pipeline
templates, Temporal workflows, legal RAG, trading guardrails, tax adapters,
full tests, and a React dashboard with a React Flow DAG visualizer.

## Quickstart
```bash
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
pytest -q
uvicorn apps.api.main:app --reload --port 8000
cd apps/web && npm i && npm run dev
```
Local-first: SQLite default DB, no cloud dependency. See AGENT_HANDOFF.md.
