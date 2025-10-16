#!/usr/bin/env bash
set -euo pipefail

# Example: rebuild a static feed/site, clear caches, etc.
# Do NOT run docker build/run here when using Compose.
APP_DIR="/app"

echo "[$(date -Is)] Rebuild step start"

# Put your actual rebuild operations here. Examples:
# /usr/bin/env python3 "${APP_DIR}/generate_feeds.py"
# /usr/bin/env python3 "${APP_DIR}/reindex.py"

echo "[$(date -Is)] Rebuild step done"
