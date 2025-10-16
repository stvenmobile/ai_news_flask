#!/usr/bin/env bash
set -Eeuo pipefail

APP_DIR="/home/steve/stack/ai_news_flask"
VENV_PY="${APP_DIR}/.venv/bin/python"
LOG="${APP_DIR}/cron.log"

{
  echo "[$(date -Is)] START refresh"
  "${VENV_PY}" "${APP_DIR}/ai_signal_fetcher.py"
  if [[ -x "${APP_DIR}/rebuild.sh" ]]; then
    /bin/bash "${APP_DIR}/rebuild.sh"
  fi
  echo "[$(date -Is)] DONE refresh"
} >>"$LOG" 2>&1
