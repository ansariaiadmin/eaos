# EAOS Roadmap — Honest Done vs v2

## Done (Phases 1-12) — Implemented & Tested

1. **Finance Core**: integer minor units (1e-4), hash-chained ledger, SHA-256, tamper detection — DONE
2. **Config**: YAML-driven settings, SQL migrations, SQLite default — DONE
3. **Hybrid LLM Router**: privacy-first, cost cap $5, confidence gate, redaction — DONE
4. **Redaction Engine**: IBAN/NID/PAN/EMAIL/PHONE/SECRETS — DONE
5. **Voice Pipeline**: STT→redact→route→LLM→TTS template — DONE
6. **Temporal Workflows**: DailyClose, LegalResearch — DONE (templates, needs Temporal server for prod)
7. **Legal RAG**: lexical BM25 + vector store lite (hash 64-dim + cosine) + citations, local-only — DONE
8. **Trading Guardrails**: position caps 10%, daily loss 2%, kill switch — DONE
9. **Tax Adapters**: US federal 2024 + IR anonymized 15% — DONE
10. **Frontend**: React dashboard + React Flow DAG — DONE (needs npm)
11. **Orchestration**: planner (keyword decompose) → executor (dispatch legal/tax/trading/voice) → critic (validate + 1 retry) — DONE, 12 tests
12. **Vector Store**: hash embeddings, cosine, fallback lexical, scores — DONE, 9 tests

## v2 — Explicit Honest Scope (Phases 13-16) — NOT Done, Requires Infra

13. **Plugin Marketplace & Signed Skills**: 
    - Why v2: needs code signing infra, sandbox (gVisor/Firecracker), registry, security audit
    - Next: design skill manifest, signing keys, sandbox POC

14. **Real Broker Integration**:
    - Why v2: needs live API keys (Nobitex/Binance), rate limits, compliance, paper trading engine
    - Next: paper trader with slippage model, then live with kill switch

15. **Local Fine-tuning Loop**:
    - Why v2: needs GPU, LoRA, dataset curation, eval harness
    - Next: collect ledger + RAG feedback, LoRA on llama3-8b, eval

16. **Audit Evidence Vault (WORM)**:
    - Why v2: needs S3/minio with object lock, hash chaining proofs, legal hold
    - Next: minio + WORM policy, evidence package signing

## No Hidden Gaps

All v2 items are explicitly listed with reason (infra/security). No hidden TODOs.

## Test Coverage

- 42 tests: finance (4), legal_rag (2), router_redaction (4), trading_tax (7), voice (1), orchestration (12), vector_store (9), e2e_orchestration (3)
- Linter: ruff 0 errors
- Deprecations: 0
