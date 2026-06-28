---
name: stemcell-deploy-validate
description: Run a reproducible StemCell Operator validation in an ephemeral kind cluster, proving role expression, same-image identity, status, cooldown, rollback, and security context.
---

# Ephemeral deployment validation

## Safety preflight

1. Verify Docker, kind, and kubectl availability.
2. Choose a disposable name through `STEMCELL_KIND_CLUSTER`; the project E2E target must honor it.
3. Unset any external `KUBECONFIG` and run `bash scripts/verify-local.sh`. The helper creates an isolated repository-local kubeconfig and proves a safe existing-or-missing-cluster state before invoking E2E tooling.
4. Before every additional direct `kubectl` command, run `bash scripts/kind-e2e-preflight.sh`; abort unless context and loopback API server match the disposable kind cluster.
5. Never reuse the user's default kubeconfig or any production/shared context.

## Validation sequence

1. Build one universal runtime image and record its immutable image ID/digest.
2. Load that image into kind.
3. Install CRDs and deploy the controller.
4. Express `api`; verify probes, endpoint, status, security context, and image identity.
5. Transition manually to `worker`; verify rollout, revision, and old pod replacement.
6. Exercise policy default, queue-based worker, and AI-requested precedence.
7. Oscillate inputs within cooldown and prove no repeated rollout/hot loop.
8. Trigger a deliberately unready role configuration supported only by test hooks; verify timeout and rollback.
9. Restart the controller during a transition and verify recovery.
10. Save concise events, conditions, pod image IDs, and command results.
11. Delete the temporary cluster and kubeconfig even on failure.

## Output

Write a report under `docs/reports/` or return equivalent evidence. Do not mark success based only on logs or desired state.
