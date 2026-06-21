#!/usr/bin/env bash
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
TOOLS_DIR="${ROOT}/.tools/bin"
mkdir -p "${TOOLS_DIR}" "${ROOT}/.cache" "${ROOT}/.tmp"
export PATH="${TOOLS_DIR}:${PATH}"

cd "${ROOT}"
if command -v go >/dev/null 2>&1 && [[ -f go.mod ]]; then
  go mod download
fi

if [[ -x scripts/check-codex-kit.py ]]; then
  scripts/check-codex-kit.py
fi

cat <<MSG
Worktree setup complete.
Repository: ${ROOT}
Local tools are not installed automatically except through the configured Cloud setup.
Before Kubernetes operations, use scripts/kind-e2e-preflight.sh or scripts/verify-local.sh.
MSG
