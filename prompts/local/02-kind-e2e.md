# Local Worktree — kind end-to-end proof

Run only in a dedicated Worktree with Docker, kind, kubectl, and a disposable cluster. Never run against a production, shared, or ambiguous Kubernetes context.

Use `$stemcell-deploy-validate`, `$stemcell-test`, and explicitly spawn `deployment_validator`.

1. Record base revision, branch, tool versions, cluster name, and mapped SC criteria.
2. Set `STEMCELL_KIND_CLUSTER=stemcell-e2e` unless the reviewed project target specifies another disposable name.
3. Refuse an external kubeconfig: `unset KUBECONFIG`, then run `./scripts/verify-local.sh`. This script establishes an isolated kubeconfig and performs the safe existing-or-missing-cluster preflight before the reviewed E2E target creates or uses the cluster.
4. Before any additional direct `kubectl` command, run `./scripts/kind-e2e-preflight.sh` and preserve its context evidence.
5. Observe—not merely infer—controller readiness, role endpoint, rollout, cooldown/no-flapping, failure/rollback, restart recovery, conditions, owner references, RBAC, and restricted security context as applicable.
6. Record the runtime image ID/digest for `api`, `worker`, and `ai` and prove they are identical when SC-01 is in scope.
7. Collect bounded diagnostics on failure and clean up the cluster.
8. Write `docs/reports/local-validation-<YYYY-MM-DD>.md` using `docs/LOCAL_VALIDATION.md`.
9. Spawn `code_reviewer`, `test_engineer`, and `security_reviewer` for the final evidence review. Do not claim acceptance for skipped mandatory checks.
