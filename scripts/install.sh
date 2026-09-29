#!/usr/bin/env bash
set -euo pipefail

if ! python3 -c 'import venv' >/dev/null 2>&1; then
  sudo DEBIAN_FRONTEND=noninteractive apt-get update -qq
  sudo DEBIAN_FRONTEND=noninteractive apt-get install -y -qq python3-venv
fi

python3 -m venv .venv
.venv/bin/pip install -r requirements.txt
