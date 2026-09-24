# ARCHITECTURE.md — eaos — Enterprise Agent OS

## ۶. eaos — Enterprise Agent OS (Local-First)

### Purpose
Local-first enterprise agent OS: LLM, trading, voice STT/TTS, phases 13-16, kill switch, confidence threshold, max daily spend.

### Graph
```mermaid
graph TD
    User --> API[FastAPI<br/>apps/api/main.py<br/>python:3.11-slim<br/>USER appuser<br/>HEALTHCHECK /api/health]

    API --> LLM[LLM<br/>LOCAL_LLM_ENDPOINT<br/>llama3-8b<br/>or OpenAI]
    API --> DB[(SQLite eaos.db<br/>DB_PATH)]
    API --> Trading[Trading<br/>MAX_POSITION_PCT 0.10<br/>MAX_DAILY_LOSS_PCT 0.02<br/>KILL_SWITCH true]
    API --> Voice[Voice<br/>STT faster-whisper<br/>TTS]

    subgraph Config[Config via .env]
        LLMConfig[MAX_DAILY_SPEND_USD 5.0<br/>LOCAL_CONFIDENCE_THRESHOLD 0.7]
        TradingConfig[Trading limits]
        VoiceConfig[Voice STT/TTS]
    end

    Config --> API

    subgraph Docker[Docker]
        Builder[builder<br/>pip --prefix=/install]
        Runner[runner<br/>curl minimal<br/>USER appuser<br/>HEALTHCHECK curl /api/health]
        Ollama[ollama/ollama:latest<br/>for local LLM]
        Builder --> Runner
    end

    API --> Ollama
```

### Connections
- **API → LLM:** Via LOCAL_LLM_ENDPOINT or OPENAI_API_KEY, with MAX_DAILY_SPEND and CONFIDENCE_THRESHOLD
- **API → Trading:** With kill switch, max position %, max daily loss %
- **API → Voice:** STT faster-whisper, TTS
- **API → DB:** SQLite eaos.db

### Modern Standards Check
- ✅ **Local-First:** No cloud required, Ollama local, SQLite, no hardcoded secrets
- ✅ **Safety:** Kill switch, max position, max daily loss, confidence threshold, max daily spend
- ✅ **Modular:** apps/api, packages, configs — separation
- ✅ **Docker:** Multi-stage, USER appuser, HEALTHCHECK, curl minimal
- ✅ **Testing:** 42 tests, ruff 0, 0 any, 0 console.log
- ⚠️ **Product Gap:** Needs phases 13-16 real embeddings pgvector, Temporal prod, voice STT/TTS real, trading live

### Deep Issues Fixed
- **Root Docker:** Fixed to USER appuser multi-stage

---


