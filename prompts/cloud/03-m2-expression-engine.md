# Cloud task — M2 pure expression engine

Read the repository instructions and use the integrated M1 API types as the contract.

```yaml
mode: Cloud
backlog_item: M2
acceptance_criteria: [SC-03, SC-04, SC-11]
owned_paths:
  - internal/expression/**
forbidden_paths:
  - api/v1alpha1/**
  - internal/controller/**
  - cmd/runtime/**
  - internal/runtime/**
  - config/**
deliverable: reviewable diff or draft PR
```

Use `$stemcell-expression-engine` and `$stemcell-cloud-task`.

1. Record base revision and exact decision semantics from `docs/SPEC.md` and `docs/ARCHITECTURE.md`.
2. Spawn `architect` to define the pure input/output contract, deterministic ordering, injected clock boundary, and invalid-decision reasons.
3. Spawn `implementer` to implement only `internal/expression` and its tests.
4. Support specified string/numeric comparisons, priority ordering, rule-name tie-break, default role, and cooldown decision semantics without I/O or global state.
5. Add table-driven, boundary, malformed-input, tie, absent-signal, and fuzz tests.
6. Run targeted tests, race checks when applicable, and `./scripts/verify-cloud.sh`.
7. Spawn `code_reviewer`, `test_engineer`, and `security_reviewer`; resolve P0/P1 findings.
8. Return the deterministic contract and controller-integration assumptions. Mark kind no-flapping observation `LOCAL_REQUIRED`.
