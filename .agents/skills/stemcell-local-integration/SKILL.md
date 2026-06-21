---
name: stemcell-local-integration
description: Integrate one or more Codex Cloud changes in an isolated local Worktree and prove Docker/kind behavior before milestone completion.
---

# Local integration

## Workflow

1. Create or use an isolated Worktree from the intended base branch.
2. Confirm a clean state and list candidate Cloud branches/PRs with dependencies.
3. Integrate one candidate at a time; resolve conflicts against specification and architecture, not by blindly choosing one side.
4. Run `bash scripts/verify-cloud.sh` after each integration.
5. For full E2E, unset external `KUBECONFIG` and run `bash scripts/verify-local.sh`; it establishes the isolated pre-creation/existing-cluster guard.
6. Before any additional direct `kubectl` command, run `bash scripts/kind-e2e-preflight.sh` against the created disposable cluster.
7. Spawn `code_reviewer`, `test_engineer`, and `security_reviewer` as appropriate.
8. Spawn `deployment_validator` only after the disposable kind context is proven.
9. Record identical image identity across roles, observed rollout/rollback state, and condition evidence.
10. Update backlog checkboxes only after mapped acceptance criteria pass.

## Failure handling

- Do not hide integration failures with repeated retries.
- Keep rejected Cloud branches intact for diagnosis.
- If a conflict changes public API or architecture, return to `architect`.
- Never point tests at production, a shared cluster, or an ambiguous context.
