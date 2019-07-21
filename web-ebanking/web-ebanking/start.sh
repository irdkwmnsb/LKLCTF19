#!/usr/bin/env bash
set -euo pipefail

smart_bot_sessid="$(python3 -c 'import secrets; print(secrets.token_hex())')"
export SERVICE_SESSIONS="$(printf '{"%s": "smart_bot"}' "${smart_bot_sessid}")"
export SERVICE_SMART_BOT_SESSION_ID="${smart_bot_sessid}"
export MOZ_HEADLESS=1

exec python3 main.py
