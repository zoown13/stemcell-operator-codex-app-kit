#!/usr/bin/env bash
set -euo pipefail
ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "${ROOT}"

python3 scripts/check-codex-kit.py

python3 - <<'PY'
from pathlib import Path
source = Path('scripts/check-codex-kit.py').read_text(encoding='utf-8')
compile(source, 'scripts/check-codex-kit.py', 'exec')
print('Python syntax parsing passed')
PY

while IFS= read -r -d '' script; do
  bash -n "${script}"
done < <(find scripts -maxdepth 1 -type f -name '*.sh' -print0)
echo "Shell syntax parsing passed"

python3 - <<'PY'
from pathlib import Path
import tomllib
root = Path('.')
for path in [root / '.codex/config.toml', *sorted((root / '.codex/agents').glob('*.toml'))]:
    tomllib.loads(path.read_text(encoding='utf-8'))
print('TOML parsing passed')
PY

if find . -type d -name __pycache__ -o -type f -name '*.pyc' | grep -q .; then
  echo "error: validation generated or found Python cache files" >&2
  exit 1
fi

echo "Repository kit validation passed."
