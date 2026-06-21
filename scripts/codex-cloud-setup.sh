#!/usr/bin/env bash
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
TOOLS_DIR="${ROOT}/.tools/bin"
mkdir -p "${TOOLS_DIR}" "${ROOT}/.cache"

# Codex Cloud setup and agent phases may use separate shells. Persist only the
# repository-local tool path; never persist credentials here.
PATH_LINE="export PATH=\"${TOOLS_DIR}:\$PATH\""
if ! grep -Fqx "${PATH_LINE}" "${HOME}/.bashrc" 2>/dev/null; then
  printf '\n%s\n' "${PATH_LINE}" >> "${HOME}/.bashrc"
fi
export PATH="${TOOLS_DIR}:${PATH}"

if ! command -v go >/dev/null 2>&1; then
  echo "error: Go is required. Pin/install the version from docs/SPEC.md in the Codex Cloud environment." >&2
  exit 1
fi

echo "Go: $(go version)"

if ! command -v kubebuilder >/dev/null 2>&1; then
  version="${KUBEBUILDER_VERSION:-4.15.0}"
  version="${version#v}"
  os="$(go env GOOS)"
  arch="$(go env GOARCH)"
  url="${KUBEBUILDER_URL:-https://github.com/kubernetes-sigs/kubebuilder/releases/download/v${version}/kubebuilder_${os}_${arch}}"
  tmp="${TOOLS_DIR}/kubebuilder.tmp"

  if [[ -z "${KUBEBUILDER_SHA256:-}" ]]; then
    echo "error: KUBEBUILDER_SHA256 is required before downloading Kubebuilder in Cloud." >&2
    echo "Provide the checksum for ${url}, or preinstall kubebuilder in the Cloud image." >&2
    exit 1
  fi

  echo "Installing Kubebuilder ${version} into ${TOOLS_DIR}"
  echo "Source: ${url}"
  curl --fail --location --silent --show-error --output "${tmp}" "${url}"
  printf '%s  %s\n' "${KUBEBUILDER_SHA256}" "${tmp}" | sha256sum --check --status

  chmod +x "${tmp}"
  mv "${tmp}" "${TOOLS_DIR}/kubebuilder"
fi

echo "Kubebuilder: $(kubebuilder version 2>/dev/null || kubebuilder --version 2>/dev/null || echo installed)"

cd "${ROOT}"
if [[ -f go.mod ]]; then
  go mod download
fi

if [[ -x scripts/check-codex-kit.py ]]; then
  scripts/check-codex-kit.py
fi

echo "Cloud setup complete. Docker, kind, kubeconfig, registry, VPN, and production credentials were not configured."
