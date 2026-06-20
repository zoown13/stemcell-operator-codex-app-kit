---
name: stemcell-scaffold
description: Create or repair the initial Go and Kubebuilder scaffold for StemCell Operator in Codex Cloud or Worktree while preserving the app kit and reproducible checks.
---

# Scaffold the operator

Use for backlog milestone M0 only.

## Preconditions

- repository URL/module path is known or a placeholder is explicitly accepted;
- execution mode is stated;
- the working tree is understood;
- Go and Kubebuilder versions are checked against `docs/SPEC.md`;
- this Codex app kit is committed or backed up.

## Workflow

1. Use `$stemcell-plan` and spawn `architect`.
2. Initialize a Kubebuilder Go v4 project without overwriting repository instructions or Codex configuration.
3. Create the `StemCell` API/controller skeleton for group `genome`, version `v1alpha1`, kind `StemCell`.
4. Establish the package layout from `Instructions.md`.
5. Add or normalize Make targets:
   - `fmt`, `vet`, `test`;
   - `generate`, `manifests`;
   - `test-race`;
   - `verify` as the local aggregate;
   - `test-e2e` as an explicit environment-gated target.
6. Add normal repository CI only when requested; do not add Codex API or Codex GitHub Action workflows.
7. Add only skeletal runtime packages; do not implement later milestones.
8. Run formatting, generation, tests, and YAML/TOML parsing supported by the current mode.
9. Spawn `code_reviewer` and `test_engineer` for independent checks.

## Preserve

Never delete or replace `AGENTS.md`, `Instructions.md`, `.agents/`, `.codex/`, `docs/`, `prompts/`, or app setup scripts unless the task explicitly updates them.

## Mode-specific completion

- Cloud: run `./scripts/verify-cloud.sh`; mark Docker/kind work `LOCAL_REQUIRED`.
- Worktree/Local: run `./scripts/verify-local.sh` when Docker/kind are available and safe.

M0 may be checked complete only when the project builds, generation is repeatable, tests pass, and required Local validation has either passed or is explicitly not part of M0.
