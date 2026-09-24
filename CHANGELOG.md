## [v0.9.1] - 2026-09-24 - Non-Technical Auto Install + Auto Update Edition

### Added - نصب خودکار برای افراد غیر فنی
- **install.sh**: نصب خودکار تمیز - چک Docker, ساخت .env با رمز تصادفی openssl, docker compose up --build -d, صبر 30s, سلامت چک, نمایش آدرس و رمز ورود
- **update.sh**: آپدیت خودکار - بکاپ به backups/YYYYMMDD-HHMMSS/, git pull origin main, docker compose pull + up --build -d, health check, rollback hint
- **start.sh, stop.sh, status.sh, logs.sh, backup.sh**: دستورات ساده روزانه
- **install.bat, start.bat, stop.bat, status.bat, logs.bat, update.bat, backup.bat**: نسخه ویندوز برای افراد غیر فنی
- **INSTALL.md**: راهنمای کامل فارسی نصب در 3 قدم (<5 دقیقه)
- **docs/USER_GUIDE_FA.md**: آموزش کامل تمام بخش‌ها - داشبورد, تنظیمات .env, Docker چیست, بکاپ, عیب‌یابی, امنیت, ورژن‌ها
- **docs/USER_GUIDE_EN.md**: Full English guide for non-technical
- **README**: بخش جدید "برای افراد غیر فنی / For Non-Technical Users — نصب در 1 دقیقه!" با one-liner

### Fixed
- Clean presentation: حذف cache artifacts, .env فقط .env.example
- Non-technical UX: پیام‌های فارسی + انگلیسی، رنگی، راهنمای قدم به قدم

### Docs
- README badge+mermaid+quickstart+sample output + non-technical section
- INSTALL.md + docs/USER_GUIDE_FA.md + docs/USER_GUIDE_EN.md

# Changelog — EAOS

All notable changes to this project will be documented in this file.

## [0.9.0] — 2026-09-24 — Fleet to 10/10 Final

### Added
- Orchestration package: planner, executor, critic, Orchestrator with 1 retry (Phase 11)
- Vector store lite: hash embeddings 64-dim + cosine, fallback lexical (Phase 12)
- E2E orchestration tests with local LLM mock (3 tests)
- AGENTS.md, CHANGELOG.md, .env.example, CI workflow
- ROADMAP updated with honest Done vs v2 split

### Fixed
- `test_us_tax_bracket` corrected to 60,530,000 (2024 brackets include 22% third bracket)
- `finance.py` utcnow deprecation → datetime.now(timezone.utc)
- Linter 0 errors, deprecation 0

### Tests
- 42 passed, 0 failed (was 18 with 1 failing)

## [0.8.0] — 2026-09-24 — Phase 11+12 Lite (REPORT #7)

- Added orchestration planner/executor/critic
- Added vector store lite
- 39 tests

## [0.7.0] — Earlier — Phases 1-10

- Finance core, router, redaction, voice, Temporal, legal RAG lexical, trading guardrails, tax adapters, frontend
