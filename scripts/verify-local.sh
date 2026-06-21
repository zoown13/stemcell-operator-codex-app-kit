#!/usr/bin/env bash
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "${ROOT}"

./scripts/verify-cloud.sh

if [[ ! -f Makefile || ! -f go.mod ]]; then
  echo "Local verification: operator scaffold is not present yet; no Docker/kind checks to run."
  exit 0
fi

has_target() {
  make -qp 2>/dev/null | awk -F: -v target="$1" '$1 == target { found=1 } END { exit !found }'
}

if ! has_target test-e2e; then
  echo "SKIP: make test-e2e (target not defined yet)."
  exit 0
fi

for cmd in docker kind kubectl; do
  if ! command -v "${cmd}" >/dev/null 2>&1; then
    echo "error: local E2E target exists but '${cmd}' is unavailable." >&2
    exit 1
  fi
done

docker info >/dev/null

mkdir -p "${ROOT}/.tmp"
cluster="${STEMCELL_KIND_CLUSTER:-stemcell-e2e}"
isolated_kubeconfig="${ROOT}/.tmp/kubeconfig-${cluster}"

if [[ -n "${KUBECONFIG:-}" && "${KUBECONFIG}" != "${isolated_kubeconfig}" ]]; then
  echo "error: refusing E2E while an external KUBECONFIG is selected: '${KUBECONFIG}'." >&2
  echo "Unset KUBECONFIG and rerun; this script will use an isolated repository-local kubeconfig." >&2
  exit 2
fi

export KUBECONFIG="${isolated_kubeconfig}"
export STEMCELL_KIND_CLUSTER="${cluster}"

if kind get clusters 2>/dev/null | grep -Fxq "${cluster}"; then
  kind export kubeconfig --name "${cluster}" --kubeconfig "${KUBECONFIG}" >/dev/null
  ./scripts/kind-e2e-preflight.sh
else
  rm -f "${KUBECONFIG}"
  ./scripts/kind-e2e-preflight.sh --allow-missing
fi

echo "> make test-e2e"
make test-e2e

if kind get clusters 2>/dev/null | grep -Fxq "${cluster}"; then
  kind export kubeconfig --name "${cluster}" --kubeconfig "${KUBECONFIG}" >/dev/null
  ./scripts/kind-e2e-preflight.sh
  echo "Local validation completed; disposable cluster '${cluster}' remains for evidence collection or explicit cleanup."
else
  echo "Local validation completed; E2E target removed disposable cluster '${cluster}'."
fi
