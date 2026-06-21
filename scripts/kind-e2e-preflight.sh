#!/usr/bin/env bash
set -euo pipefail

usage() {
  cat <<'USAGE'
Usage: kind-e2e-preflight.sh [--allow-missing]

Verifies that Kubernetes operations target the expected disposable kind cluster.
--allow-missing is intended only before a reviewed E2E target creates that cluster;
it still requires an isolated/empty kubeconfig selected by the caller.
USAGE
}

allow_missing=0
case "${1:-}" in
  "") ;;
  --allow-missing) allow_missing=1 ;;
  -h|--help) usage; exit 0 ;;
  *) usage >&2; exit 64 ;;
esac

cluster="${STEMCELL_KIND_CLUSTER:-stemcell-e2e}"
expected_context="kind-${cluster}"

if [[ ! "${cluster}" =~ ^[a-z0-9]([-a-z0-9]*[a-z0-9])?$ ]]; then
  echo "error: invalid kind cluster name '${cluster}'." >&2
  exit 64
fi

for cmd in kubectl kind; do
  if ! command -v "${cmd}" >/dev/null 2>&1; then
    echo "error: ${cmd} is required for kind validation." >&2
    exit 1
  fi
done

if ! kind get clusters 2>/dev/null | grep -Fxq "${cluster}"; then
  if [[ "${allow_missing}" == "1" ]]; then
    current="$(kubectl config current-context 2>/dev/null || true)"
    if [[ -n "${current}" ]]; then
      echo "error: expected cluster is missing but kubeconfig already selects '${current}'." >&2
      echo "Use an isolated empty KUBECONFIG before allowing cluster creation." >&2
      exit 2
    fi
    echo "Verified pre-creation state: disposable kind cluster '${cluster}' is absent and no context is selected."
    exit 0
  fi

  echo "error: disposable kind cluster '${cluster}' does not exist." >&2
  echo "Create it through the reviewed project E2E target using an isolated kubeconfig, then rerun this preflight." >&2
  exit 2
fi

current="$(kubectl config current-context 2>/dev/null || true)"
echo "Current context: ${current:-<none>}"
echo "Expected context: ${expected_context}"

if [[ "${current}" != "${expected_context}" ]]; then
  echo "error: refusing Kubernetes operations because the current context is not the expected disposable kind context." >&2
  exit 3
fi

server="$(kubectl config view --minify -o jsonpath='{.clusters[0].cluster.server}' 2>/dev/null || true)"
case "${server}" in
  https://127.0.0.1:*|https://localhost:*|http://127.0.0.1:*|http://localhost:*) ;;
  *)
    echo "error: kind context resolves to unexpected API server '${server:-<unknown>}'." >&2
    exit 4
    ;;
esac

kubectl cluster-info >/dev/null
printf "Verified disposable kind context '%s' at %s\n" "${current}" "${server}"
