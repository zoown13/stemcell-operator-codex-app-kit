# Cloud task — M1 CRD contract and validation

Read the repository instructions and confirm M0 is integrated before editing.

```yaml
mode: Cloud
backlog_item: M1
acceptance_criteria: [SC-08, SC-11]
owned_paths:
  - api/v1alpha1/**
  - config/crd/**
  - config/samples/**
  - docs/**crd**
forbidden_paths:
  - internal/controller/**
  - internal/expression/**
  - cmd/runtime/**
  - internal/runtime/**
  - .agents/**
  - .codex/**
deliverable: reviewable diff or draft PR
```

Use `$stemcell-crd` and `$stemcell-cloud-task`.

1. Record base revision, owned paths, and the exact M1 contract from `docs/SPEC.md`.
2. Spawn `architect` to review API compatibility, defaults, status shape, validation, and generated assets.
3. Spawn `implementer` for the approved CRD slice only.
4. Implement bounded enums, fields, defaults, status subresource, printer columns, schema/CEL validation where appropriate, and Manual/Policy samples.
5. Do not add arbitrary command, source, executable URL, per-role image, plugin, model-download, or template execution fields.
6. Add serialization/defaulting/validation tests, including invalid roles, modes, operators, duplicate rule names, unsafe fields, and bounds.
7. Run generation plus `bash scripts/verify-cloud.sh`.
8. Spawn `code_reviewer`, `test_engineer`, and `security_reviewer`; resolve P0/P1 findings.
9. Return a Cloud handoff with generated files and any admission behavior that still needs Local proof.
