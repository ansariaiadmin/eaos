# Roadmap Phases 1-10 (implemented)
1. Deterministic finance core (integer minor units, hash-chained double-entry ledger)
2. Config-driven settings + SQL migrations
3. Hybrid LLM router (privacy-first, cost cap, confidence gate)
4. Redaction engine (IBAN/NID/PAN/EMAIL/PHONE/SECRETS)
5. Voice pipeline templates (STT -> redact -> route -> LLM -> TTS)
6. Temporal workflows (DailyClose, LegalResearch)
7. Legal RAG agent (lexical retrieval + citations, local-only)
8. Trading guardrails (position caps, loss limit, kill switch)
9. Tax integration adapters (US federal 2024 brackets + anonymized IR)
10. Frontend dashboard + React Flow DAG visualizer + full pytest suite

## Next phases (11-16) - see AGENT_HANDOFF.md
11. Multi-agent orchestration (planner/executor/critic)
12. Vector store + embeddings for legal RAG
13. Plugin marketplace & signed skills
14. Real broker integration (paper trading first)
15. Local fine-tuning loop
16. Audit evidence vault (WORM storage)
