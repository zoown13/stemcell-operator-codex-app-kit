# Cloud task — M0 repository and Kubebuilder scaffold

Read `AGENTS.md`, `Instructions.md`, `docs/SPEC.md`, `docs/ARCHITECTURE.md`, `docs/BACKLOG.md`, and `docs/OPERATING_MODEL.md` before editing.

```yaml
mode: Cloud
backlog_item: M0
acceptance_criteria: [SC-09, SC-11]
owned_paths:
  - go.mod
  - go.sum
  - Makefile
  - PROJECT
  - api/**
  - cmd/**
  - internal/**
  - config/**
  - hack/**
  - test/**
  - Dockerfile
  - .dockerignore
forbidden_paths:
  - AGENTS.md
  - Instructions.md
  - docs/SPEC.md
  - docs/ARCHITECTURE.md
  - .agents/**
  - .codex/**
  - prompts/**
deliverable: reviewable diff or draft PR
```

Use `$stemcell-scaffold` and `$stemcell-cloud-task`.

1. State the exact base revision and verify that M0 is still unchecked.
2. Explicitly spawn `architect` for a read-only scaffold plan. Preserve all existing kit files.
3. Spawn `implementer` to initialize a Kubebuilder Go v4 project with group `genome.stemcell.io`, version `v1alpha1`, kind `StemCell`.
4. Add only the M0 API/controller skeleton and package layout. Do not implement M1+ behavior.
5. Normalize Make targets required by the repository instructions. Normal CI may be added, but do not add a Codex API action or Codex API key.
6. Run `bash scripts/verify-cloud.sh` and targeted build/generation checks supported by the environment.
7. Explicitly spawn `code_reviewer`, `test_engineer`, and `security_reviewer`; resolve P0/P1 findings.
8. Return the Cloud handoff. Mark Docker image execution and kind checks `LOCAL_REQUIRED` rather than claiming they passed.

Do not merge, deploy, or modify unrelated backlog checkboxes.
