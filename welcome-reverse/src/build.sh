#!/usr/bin/env bash
set -xeuo pipefail
meson --wipe build
ninja -C build
ln -svf src/build/authorize ..
strip build/authorize
if ! grep build/authorize -Fe 'LKLCTF{'; then
    echo 'Fatal error: executable file does not contain the flag'
    exit 1
fi
