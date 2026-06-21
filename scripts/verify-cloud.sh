#!/usr/bin/env bash
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "${ROOT}"

python3 scripts/check-codex-kit.py

if [[ ! -f Makefile || ! -f go.mod ]]; then
  echo "Cloud verification: kit-only repository; Go/Kubebuilder project has not been scaffolded yet."
  exit 0
fi

has_target() {
  make -qp 2>/dev/null | awk -F: -v target="$1" '$1 == target { found=1 } END { exit !found }'
}

run_target() {
  local target="$1"
  if has_target "${target}"; then
    echo "> make ${target}"
    make "${target}"
  else
    echo "SKIP: make ${target} (target not defined)"
  fi
}

run_target fmt
run_target vet
run_target test

snapshot() {
  git status --porcelain=v1 --untracked-files=all
  git diff --binary --no-ext-diff HEAD -- .
}

if has_target manifests || has_target generate; then
  before="$(mktemp)"
  after="$(mktemp)"
  trap 'rm -f "${before:-}" "${after:-}"' EXIT
  snapshot > "${before}"
  run_target manifests
  run_target generate
  snapshot > "${after}"
  if ! cmp -s "${before}" "${after}"; then
    echo "error: manifest/code generation changed the working tree." >&2
    echo "Review and keep the generated files, then rerun verification until generation is idempotent." >&2
    diff -u "${before}" "${after}" || true
    exit 1
  fi
fi

run_target test-race

echo "Cloud-safe verification passed. Docker/kind integration remains LOCAL_REQUIRED when mapped criteria need it."
