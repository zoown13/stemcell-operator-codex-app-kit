#!/usr/bin/env python3
"""Minimal YAML sanity check for CI/config manifests in Cloud."""
from pathlib import Path
import sys

for name in sys.argv[1:]:
    path = Path(name)
    text = path.read_text(encoding="utf-8")
    if "\t" in text:
        raise SystemExit(f"{name}: tabs are not allowed in YAML")
    if not text.strip():
        raise SystemExit(f"{name}: empty YAML file")
    if not any(line.startswith("apiVersion:") or line.startswith("name:") for line in text.splitlines()):
        raise SystemExit(f"{name}: expected apiVersion or workflow name")
