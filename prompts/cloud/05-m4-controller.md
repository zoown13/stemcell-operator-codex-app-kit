# Cloud task — M4 controller steady state and transitions

Start only from a revision where M1 and M2 are integrated and their contracts are stable.

```yaml
mode: Cloud
backlog_item: M4
acceptance_criteria: [SC-02, SC-04, SC-05, SC-10, SC-11]
owned_paths:
  - internal/controller/**
  - cmd/manager/**
  - config/rbac/**
  - config/manager/**
  - config/default/**
  - test/**controller**
forbidden_paths:
  - api/v1alpha1/**
  - internal/expression/**
  - cmd/runtime/**
  - internal/runtime/**
deliverable: reviewable diff or draft PR
```

Use `$stemcell-plan`, `$stemcell-cloud-task`, and the controller rules in `Instructions.md`.

1. Spawn `architect` to specify steady-state reconciliation, watches, ownership, rollout observations, status conditions, revision semantics, no-op behavior, and restart-safe persisted state boundaries.
2. Spawn `implementer` for the approved M4 slice; do not implement M5 rollback unless required by a stable interface seam.
3. Reconcile Deployment, Service, labels, probes, security context, owner references, ConfigMap watches, and least-privilege RBAC.
4. Keep expression evaluation pure and preserve the same image across roles.
5. Add fake-client/envtest coverage for create/update/no-op, Manual and Policy decisions, cooldown, status, invalid inputs, ownership, and hot-loop prevention.
6. Run generation, targeted tests, and `bash scripts/verify-cloud.sh`.
7. Spawn `code_reviewer`, `test_engineer`, and `security_reviewer`; resolve P0/P1 findings.
8. Return rollout, RBAC, probe, and kind transition checks as `LOCAL_REQUIRED`.
