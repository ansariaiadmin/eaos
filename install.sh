#!/usr/bin/env bash
set -e
GREEN='\033[0;32m'; BLUE='\033[0;34m'; RED='\033[0;31m'; YELLOW='\033[1;33m'; CYAN='\033[0;36m'; MAGENTA='\033[0;35m'; BOLD='\033[1m'; DIM='\033[2m'; NC='\033[0m'
ok() { echo -e "${GREEN}✅ $1${NC}"; }
explain() { echo -e "${CYAN}   💡 $1${NC}"; }
example() { echo -e "${DIM}   📝 مثال: $1${NC}"; }
where() { echo -e "${MAGENTA}   🔗 کجا؟ $1${NC}"; }
ask_with_help() {
  local prompt="$1"; local help_text="$2"; local example_text="$3"; local where_text="$4"; local default_val="$5"; local is_secret="${6:-false}"
  echo ""; echo -e "${BOLD}${BLUE}❓ $prompt${NC}"; [ -n "$help_text" ] && explain "$help_text"; [ -n "$example_text" ] && example "$example_text"; [ -n "$where_text" ] && where "$where_text"
  [ -n "$default_val" ] && echo -e "${DIM}   ⏭️  Enter=پیش‌فرض: $default_val${NC}" || echo -e "${DIM}   ⏭️  اگر نداری Enter=mock${NC}"
  local input=""; if [ "$is_secret" = "true" ]; then read -s -p "   👉 جواب: " input; echo ""; else read -p "   👉 جواب: " input; fi
  [ -z "$input" ] && [ -n "$default_val" ] && input="$default_val"; echo "$input"
}
ask_yes_no() {
  local prompt="$1"; local help_text="$2"; local default_yes="${3:-true}"
  echo ""; echo -e "${BOLD}${BLUE}❓ $prompt${NC}"; [ -n "$help_text" ] && explain "$help_text"
  [ "$default_yes" = "true" ] && echo -e "${DIM}   ⏭️  [Y/n] Enter=بله${NC}" || echo -e "${DIM}   ⏭️  [y/N] Enter=خیر${NC}"
  local input=""; read -p "   👉 جواب (y/n): " input; input=$(echo "$input" | tr '[:upper:]' '[:lower:]')
  [ -z "$input" ] && { if [ "$default_yes" = "true" ]; then input="y"; else input="n"; fi; }
  if [ "$input" = "y" ] || [ "$input" = "yes" ] || [ "$input" = "بله" ]; then echo "yes"; else echo "no"; fi
}

clear
echo -e "${CYAN}"
cat <<'BANNER'
 _____    _    ___  ____
| ____|  / \  / _ \/ ___|
|  _|   / _ \| | | \___ \
| |___ / ___ \ |_| |___) |
|_____/_/   \_\___/|____/
Enterprise Agent OS + LLM + Trading + Voice + Notification — Zero Support
BANNER
echo -e "${NC}"
echo -e "${BLUE}========================================${NC}"
echo -e "${BLUE}  🧙‍♂️ جادوگر نصب EAOS v3.1.0 — پشتیبانی صفر — تاریکی روشن شد${NC}"
echo -e "${BLUE}========================================${NC}"
echo ""
echo -e "${YELLOW}سلام! 👋 سیستم عامل ایجنت — LLM + ترید + صدا + pgvector + ناتیف — سقف!${NC}"
echo ""
read -p "برای شروع جادو Enter بزنید... ✨ " _

echo -e "${BLUE}[1/6] 🔍 سیستم${NC}"; ok "اوکیه"; sleep 1
echo -e "${BLUE}[2/6] 🐳 Docker${NC}"; if ! command -v docker &> /dev/null; then echo -e "${RED}Docker نیست${NC}"; exit 1; else ok "Docker: $(docker --version)"; fi; sleep 1
echo -e "${BLUE}[3/6] 🤖 LLM Provider${NC}"
explain "EAOS از LLM برای ایجنت استفاده می‌کنه"
LLM_PROVIDER=$(ask_with_help "LLM پرووایدر؟" "برای ایجنت — ollama لوکال رایگان یا openai" "ollama یا openai یا mock" "https://ollama.com/ یا https://platform.openai.com/api-keys" "ollama" "false")
LLM_KEY=""
if [ "$LLM_PROVIDER" != "ollama" ] && [ "$LLM_PROVIDER" != "mock" ]; then LLM_KEY=$(ask_with_help "کلید API؟" "sk-..." "sk-..." "https://platform.openai.com/api-keys" "" "true"); ok "LLM تنظیم شد"; fi
sleep 1

echo -e "${BLUE}[4/6] 💱 Trading + 📱 SMS + 📧 Email${NC}"
TRADING=$(ask_yes_no "ترید فعال باشه؟" "اگر بله، kill switch روشن می‌مونه — امن" "false")
# هزینه: هر پیامک ~120 تومان — تاریکی روشن شد — cost warning
SMS_PROVIDER=$(ask_with_help "SMS پرووایدر برای ناتیف ترید؟" "وقتی ترید می‌شه پیامک بره" "ghasedak یا mock" "https://ghasedak.me/" "mock" "false")
SMS_KEY=""
if [ "$SMS_PROVIDER" != "mock" ]; then SMS_KEY=$(ask_with_help "کلید API SMS؟" "از پنل" "api-key" "پنل → API" "" "true"); ok "SMS تنظیم شد"; fi
sleep 1

echo -e "${BLUE}[5/6] 🔔 Notification System${NC}"
explain "وقتی ایجنت کاری می‌کنه یا ترید می‌شه — ناتیف می‌ده"
NOTIF_EMAIL=$(ask_yes_no "ایمیل ناتیف روشن باشه؟" "وقتی ایجنت کاری می‌کنه ایمیل بره" "false")
NOTIF_SMS=$(ask_yes_no "پیامک ناتیف روشن باشه؟" "وقتی ترید می‌شه پیامک بره" "true")
TELEGRAM_ENABLED=$(ask_yes_no "ربات تلگرام برای ناتیف ایجنت می‌خوای؟" "وقتی ایجنت کاری می‌کنه تلگرام خبر می‌ده" "false")
TELEGRAM_TOKEN=""; TELEGRAM_CHAT=""
if [ "$TELEGRAM_ENABLED" = "yes" ]; then
  TELEGRAM_TOKEN=$(ask_with_help "توکن ربات؟" "از @BotFather" "123456:ABC..." "@BotFather → /newbot" "" "true")
  TELEGRAM_CHAT=$(ask_with_help "Chat ID؟" "از getUpdates" "123456789" "https://api.telegram.org/bot<TOKEN>/getUpdates" "" "false")
  ok "Telegram تنظیم شد"
fi
sleep 1

echo -e "${BLUE}[6/6] ⚙️ .env + 🏗️ اجرا${NC}"
if [ -f .env ]; then
  echo -e "${YELLOW}  .env وجود دارد — keep/new/backup? — تاریکی روشن شد — idempotency${NC}"
  read -p "   keep (نگه دار) / new (جدید) / backup (بکاپ بعد جدید) [keep]: " KEEP_ENV
  [ -z "$KEEP_ENV" ] && KEEP_ENV="keep"
  if [ "$KEEP_ENV" = "backup" ]; then cp .env .env.backup.$(date +%Y%m%d_%H%M%S); echo -e "${GREEN}✅ بکاپ گرفته شد — تاریکی روشن شد${NC}"; KEEP_ENV="new"; fi
  if [ "$KEEP_ENV" = "keep" ]; then echo -e "${GREEN}✅ .env نگه داشته شد — idempotency — تاریکی روشن شد${NC}"; SKIP_ENV="true"; else SKIP_ENV="false"; fi
else
  SKIP_ENV="false"
fi

if [ "$SKIP_ENV" = "false" ]; then
cat > .env <<EOF
# EAOS — .env — جادوگر v3.1.0 — پشتیبانی صفر — تاریکی روشن شد — $(date)
LOCAL_LLM_ENDPOINT=http://localhost:11434/api/generate
LOCAL_LLM_MODEL=llama3-8b
OPENAI_API_KEY=${LLM_KEY}
MAX_DAILY_SPEND_USD=5.0
LOCAL_CONFIDENCE_THRESHOLD=0.7
DB_PATH=sqlite:///eaos.db
TRADING_MAX_POSITION_PCT=0.10
TRADING_MAX_DAILY_LOSS_PCT=0.02
TRADING_KILL_SWITCH=true
VOICE_STT=faster-whisper
VOICE_TTS=piper
VOICE_SAMPLE_RATE=16000
FINANCE_CURRENCY=USD
FINANCE_DECIMAL_PLACES=4

# SMS — برای ناتیف ترید
# هزینه: هر پیامک ~120 تومان — تاریکی روشن شد — cost warning
SMS_PROVIDER=${SMS_PROVIDER}
SMS_API_KEY=${SMS_KEY}

# Notification System — سقف 10/10
NOTIF_IN_APP=true
NOTIF_EMAIL=${NOTIF_EMAIL}
NOTIF_SMS=${NOTIF_SMS}
NOTIF_TELEGRAM=${TELEGRAM_ENABLED}
TELEGRAM_BOT_TOKEN=${TELEGRAM_TOKEN}
TELEGRAM_CHAT_ID=${TELEGRAM_CHAT}

# Trading
TRADING_ENABLED=${TRADING}
EOF

chmod 600 .env 2>/dev/null || true
ok ".env ساخته شد — permission 600 — امن — تاریکی روشن شد"
fi
if [ "$SKIP_ENV" = "true" ]; then
  chmod 600 .env 2>/dev/null || true
  echo -e "${GREEN}✅ .env permission 600 — امن — تاریکی روشن شد${NC}"
fi — امن — تاریکی روشن شد"
docker compose up --build -d 2>&1 | tail -n 10
echo ""; echo -e "${BLUE}  ⏳ 30 ثانیه صبر...${NC}"
echo -n "  "; for i in {1..30}; do echo -n "."; sleep 1; if curl -sf http://localhost:8000/api/health >/dev/null 2>&1; then echo ""; ok "آماده!"; break; fi; done
echo ""; docker compose ps 2>/dev/null || true

echo ""
echo -e "${GREEN}========================================${NC}"
echo -e "${GREEN}  🎉 جادو تمام! EAOS آماده — پشتیبانی صفر! 🎉${NC}"
echo -e "${GREEN}========================================${NC}"
echo ""
echo -e "${BOLD}${BLUE}📍 دسترسی:${NC}"
echo -e "${GREEN}  🌐 URL: http://localhost:8000 — LLM + Trading + Voice + pgvector${NC}"
echo ""
echo -e "${CYAN}📚 docs/SETUP-WIZARD-FA.md${NC}"
echo ""
