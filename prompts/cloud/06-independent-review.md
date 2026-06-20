# Cloud task — independent milestone review

This is a read-first review task. Do not implement fixes unless the user explicitly changes the scope.

```yaml
mode: Cloud
backlog_item: <M0-M7 or PR>
acceptance_criteria: [<SC list>]
owned_paths: []
forbidden_paths: ["**"]
deliverable: review report
```

Use `$stemcell-review`.

1. Record base/head revisions and the claimed acceptance criteria.
2. Explicitly spawn `code_reviewer` and `test_engineer` in parallel.
3. Spawn `security_reviewer` when API, RBAC, controller, runtime, image, supply chain, Cloud setup, or Automation is in scope.
4. Do not spawn `deployment_validator` in Cloud; list deployment evidence as `LOCAL_REQUIRED`.
5. Independently reconcile duplicate or conflicting findings against the source and tests.
6. Report P0-P3 findings with evidence, impact, affected SC criterion, and concrete remediation.
7. Separate observed defects, missing evidence, and optional improvements.
8. State commands actually run. Never infer local Docker/kind success from manifests or unit tests.
