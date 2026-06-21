# Cloud task — M3 universal runtime

Read the repository instructions and preserve the one-image/one-role invariants.

```yaml
mode: Cloud
backlog_item: M3
acceptance_criteria: [SC-01, SC-10, SC-11]
owned_paths:
  - cmd/runtime/**
  - internal/runtime/**
  - Dockerfile
  - .dockerignore
  - build/**
forbidden_paths:
  - api/v1alpha1/**
  - internal/controller/**
  - internal/expression/**
  - config/crd/**
deliverable: reviewable diff or draft PR
```

Use `$stemcell-runtime-role` and `$stemcell-cloud-task`.

1. Record base revision and runtime contract.
2. Spawn `architect` to define the shared lifecycle, role selection, probes, metadata, cancellation, and image constraints.
3. Spawn `implementer` for one binary supporting only `api`, `worker`, and deterministic `ai` stub roles selected by validated `STEMCELL_ROLE`.
4. Implement common `/healthz`, `/readyz`, and `/role`, bounded graceful shutdown, and no runtime executable/model downloads.
5. Add role contract, invalid-role, readiness, shutdown, and race tests.
6. Add one multi-stage non-root image definition without role-specific final images.
7. Run Cloud-safe builds/tests and `bash scripts/verify-cloud.sh`; do not claim Docker runtime behavior unless the Cloud environment actually proves it.
8. Spawn `code_reviewer`, `test_engineer`, and `security_reviewer`; resolve P0/P1 findings.
9. Return exact Docker/kind checks as `LOCAL_REQUIRED`, including proof that one digest runs all roles.
