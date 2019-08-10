#!/usr/bin/env bash
set -euo pipefail

smart_bot_sessid="dfe5cd552bf72b356a1d5c173405dd94b9f48a4153b522548ee7870ad0eda085"
export SERVICE_SESSIONS="$(printf '{"%s": "smart_bot"}' "${smart_bot_sessid}")"
export SERVICE_SMART_BOT_SESSION_ID="${smart_bot_sessid}"
export MOZ_HEADLESS=1
export SMART_BOT_URL='http://web-ebanking-smart-bot:6666'

exec python3 main.py
