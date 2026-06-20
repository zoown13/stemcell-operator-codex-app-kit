# Local Worktree validation runbook

## 1. Purpose

Local validation proves environment-sensitive success criteria that a normal Cloud task cannot establish: image construction, disposable Kubernetes behavior, rollout/rollback, RBAC, probes, security context, and identical image identity across roles.

## 2. Prerequisites

Expected tools after implementation reaches the relevant milestone:

```text
git
go
make
docker
kubectl
kind
```

Optional tools may include Helm, kustomize, and vulnerability/SBOM scanners when the backlog requires them.

## 3. Create an integration Worktree

```bash
git fetch --all --prune
git worktree add ../stemcell-integration -b codex/local-integration origin/main
cd ../stemcell-integration
./scripts/codex-worktree-setup.sh
```

Integrate Cloud branches one at a time and run Cloud-safe checks after each merge/cherry-pick.

## 4. Safety preflight

For an existing disposable cluster, run before every direct `kubectl` operation:

```bash
export STEMCELL_KIND_CLUSTER=stemcell-e2e
./scripts/kind-e2e-preflight.sh
```

For the normal full E2E path, use `verify-local.sh`. It refuses an externally selected `KUBECONFIG`, creates a repository-local isolated kubeconfig, proves either the expected kind context or a safe no-context pre-creation state, and only then invokes the reviewed `make test-e2e` target.

```bash
unset KUBECONFIG
export STEMCELL_KIND_CLUSTER=stemcell-e2e
./scripts/verify-local.sh
```

`--allow-missing` is an internal pre-creation guard for reviewed E2E tooling. Do not use it with a populated or external kubeconfig. Never bypass the preflight for a production, shared, or ambiguous context.

## 5. Validation sequence

```bash
./scripts/verify-cloud.sh
unset KUBECONFIG
./scripts/verify-local.sh
```

The exact Make targets evolve with the implementation. The local aggregate should include:

1. formatting, vet, unit/envtest, generation cleanliness, and race tests;
2. controller and universal runtime image builds;
3. ephemeral kind cluster creation;
4. CRD/controller installation;
5. manual `api -> worker` transition;
6. policy default/worker/ai selection;
7. cooldown/no-flapping behavior;
8. deliberately failed readiness and rollback;
9. controller restart during transition;
10. status/condition checks;
11. identical runtime image ID/digest across roles;
12. restricted pod security and RBAC checks;
13. diagnostics and cluster cleanup.

## 6. Evidence record

Create `docs/reports/local-validation-<date>.md` containing:

```markdown
# Local validation report
- Base and integrated branches/PRs
- Tool versions
- Worktree path
- kind cluster and proven context
- SC-* criteria tested
- Commands with pass/fail/skip
- Role transition observations
- Image IDs/digests per role
- Status/condition excerpts
- Security/RBAC observations
- Failure diagnostics
- Cleanup result
- Acceptance decision and remaining risks
```

Do not include tokens, full kubeconfig, registry credentials, or sensitive environment dumps.

## 7. Failure handling

- Capture controller logs, Deployment/Pod status, events, and resource YAML with secrets excluded.
- Use bounded retries and deadlines; do not replace failures with arbitrary sleeps.
- Keep the failing branch and report reproducible commands.
- Do not mark a milestone complete when a required local criterion failed or was skipped.
