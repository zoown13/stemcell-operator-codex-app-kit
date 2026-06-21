---
name: stemcell-cloud-task
description: Execute one bounded StemCell Operator task in Codex Cloud with explicit file ownership, Cloud-safe checks, and a Local integration handoff.
---

# Cloud task

## Contract

1. State base revision, backlog item, SC-* criteria, owned paths, and forbidden paths.
2. Read the repository instructions and relevant code.
3. Spawn `architect` for cross-layer work.
4. Implement only the approved slice; do not edit another active task's owned files.
5. Spawn `code_reviewer` and `test_engineer`; add `security_reviewer` when applicable.
6. Run `bash scripts/verify-cloud.sh` plus targeted checks.
7. Do not claim Docker, kind, private registry, VPN, or local-cluster validation.
8. Return a branch/PR or diff and a `LOCAL_REQUIRED` checklist.

## Cloud-safe output

```markdown
# Cloud task handoff
- Base revision
- Backlog item / SC-* criteria
- Changed and generated files
- Checks actually run
- Skipped local-only checks
- Reviewer findings and resolutions
- Integration prerequisites
- Recommended Local command sequence
```
