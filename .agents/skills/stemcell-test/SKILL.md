---
name: stemcell-test
description: Build and execute a success-criteria-driven test plan for StemCell Operator, from unit and envtest through race and isolated kind validation.
---

# Test a StemCell change

## Workflow

1. List the changed behavior and map it to `SC-*` criteria.
2. Ask `test_engineer` for an independent coverage matrix.
3. Run fast checks first:

```bash
make fmt
make vet
make test
```

4. Run generation cleanliness:

```bash
make manifests generate
git diff --exit-code
```

5. Run race tests when Go code changed:

```bash
make test-race
```

6. Run `make test-e2e` only when Docker, kind, and an unambiguous disposable context are available.
7. On failure, capture the narrowest useful diagnostics; do not hide failures with retries.
8. Check for fixed sleeps, shared global state, order dependence, mutable tags, and false-positive readiness.
9. Report each command as passed, failed, or skipped with reason.

## Completion rule

A skipped mandatory success criterion blocks completion. Environmental inability to run e2e is a documented blocker, not a passing result.
