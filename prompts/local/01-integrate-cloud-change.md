# Local Worktree — integrate one Cloud result

Read all repository instructions. Confirm execution mode is `Worktree` and print the current branch, worktree path, base revision, and working-tree status.

```yaml
mode: Worktree
backlog_item: <milestone>
acceptance_criteria: [<SC list>]
cloud_result: <branch/PR/commit>
deliverable: integrated branch with validation report
```

Use `$stemcell-local-integration`.

1. Refuse to proceed if unrelated uncommitted changes would be overwritten.
2. Inspect the Cloud handoff, diff, base revision, generated files, reviewer findings, and `LOCAL_REQUIRED` checklist before integrating.
3. Integrate exactly one Cloud result by merge or cherry-pick according to the repository history; do not combine unrelated changes.
4. Resolve conflicts against `docs/SPEC.md` and architecture invariants, not by mechanically choosing one side.
5. Run `bash scripts/verify-cloud.sh` after integration.
6. Explicitly spawn `code_reviewer` and `test_engineer`; add `security_reviewer` when relevant.
7. For Kubernetes-sensitive milestones, prepare the next local E2E step but do not run kubectl until `bash scripts/kind-e2e-preflight.sh` proves a disposable context.
8. Record pass/fail/skip results and update the PR handoff. Do not merge to `main` automatically.
