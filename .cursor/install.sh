#!/usr/bin/env bash
# Idempotent Cloud Agent install for the AI Dev Tools Zoomcamp homework.
# Installs uv (if missing), syncs the Django project dependencies (including
# the pinned CPython 3.14 toolchain), and applies database migrations.
set -euo pipefail

export PATH="$HOME/.local/bin:$PATH"

if ! command -v uv >/dev/null 2>&1; then
  curl -LsSf https://astral.sh/uv/install.sh | sh
fi
export PATH="$HOME/.local/bin:$PATH"

cd "$(dirname "$0")/../01-ai-native-workflow"

uv sync
uv run python manage.py migrate
