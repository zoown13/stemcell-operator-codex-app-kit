# StemCell Operator project instructions

These rules apply to every human and Codex change in this repository.

## 1. Mission

Build a research-quality Kubernetes proof of concept in which one immutable “genome” image can express one of three bounded roles—`api`, `worker`, or `ai`—according to a `StemCell` custom resource and a deterministic expression policy.

The project demonstrates a software-engineering analogy to biological differentiation. It is not arbitrary self-modifying software.

## 2. Sources of truth

Use this precedence for repository decisions:

1. the current user task;
2. `docs/SPEC.md` for behavior and acceptance criteria;
3. `docs/ARCHITECTURE.md` for architecture invariants;
4. `docs/OPERATING_MODEL.md` for Codex execution-mode boundaries;
5. this file for engineering process;
6. existing code conventions and tests.

When they conflict, avoid scope expansion, choose the safer interpretation, and document the conflict.

## 3. Codex app execution model

The same repository is used in three Codex modes.

### Cloud

Cloud is the preferred place for bounded implementation, unit tests, refactoring, documentation, and independent review. A Cloud task runs in a separate remote environment checked out from a branch or commit. It must:

- read `AGENTS.md` and the source-of-truth documents;
- own one explicit vertical slice and a declared file set;
- run only checks supported by the configured Cloud environment;
- avoid relying on local Docker, kind, kubeconfig, VPN, registry login, or workstation files;
- end with a reviewable diff or PR and a structured handoff;
- label unexecuted Docker/kind checks as `LOCAL_REQUIRED`, never as passed.

Cloud tasks may use internet access only when required by the configured environment and must not broaden access merely for convenience. Secrets must not be written into files, logs, prompts, status, or tests.

### Worktree

Worktree is the default local mode for implementation and integration because it isolates changes from the main checkout. Use separate Worktrees for parallel tasks only when their ownership areas do not overlap.

Suggested ownership boundaries:

```text
worktree/api              api/v1alpha1 and generated CRD assets
worktree/expression       internal/expression and its tests
worktree/controller       internal/controller and envtest
worktree/runtime          cmd/runtime and internal/runtime
worktree/e2e              test/e2e, config/samples, integration docs
```

Do not let two active tasks edit the same generated files or shared API types. Integrate prerequisite branches first.

### Local

Local mode may edit the main project directory. Use it deliberately for final integration or when the user explicitly wants direct edits. Do not use it for unattended work when unrelated uncommitted changes exist.

### Codex app Automation

Automations are optional and local-machine dependent. Use a dedicated background Worktree. The computer, repository, and Codex app must remain available. Automation findings belong in the Codex app Triage inbox and in `docs/reports/` when repository evidence is needed.

Automation must never merge, push without explicit instruction, mutate the main checkout, access a production cluster, or run indefinitely. See `docs/AUTOMATIONS.md`.

## 4. Baseline stack

Use the versions documented in `docs/SPEC.md` as the tested baseline. Keep dependencies minimal and pinned through Go modules and generated manifests. Do not introduce a framework merely to reduce a small amount of code.

Target layout after scaffolding:

```text
api/v1alpha1/                     CRD Go types and validation markers
cmd/manager/                      controller manager entry point
cmd/runtime/                      universal runtime entry point
internal/controller/              StemCell reconciler
internal/expression/              pure deterministic policy engine
internal/runtime/roles/           bounded role implementations
config/                           Kubebuilder manifests, RBAC, samples
test/e2e/                         kind-based end-to-end tests
docs/                             design and runbooks
```

## 5. Design rules

### Kubernetes controller

- Reconcile desired state; never orchestrate through imperative sleeps.
- Make every reconciliation idempotent.
- Use controller references and ownership consistently.
- Set `status.observedGeneration` only after observing the current spec.
- Represent progress and failure with standard conditions and stable reason strings.
- Avoid hot loops; use watches, bounded requeues, and explicit deadlines.
- Treat transient API errors differently from permanent specification errors.
- Keep durable transition state in API/workload state, not process memory alone.
- Never store secrets or high-cardinality signal data in status.

### Expression engine

- Keep policy evaluation pure: input snapshot in, decision and explanation out.
- Deterministically order by descending priority and ascending stable rule name.
- Use an injected clock for cooldown and timeout logic.
- No network access, shell execution, dynamic code loading, or hidden global state.
- Return a machine-readable reason for every decision.
- Malformed numeric inputs are explicit input errors, not silent false results.

### Universal runtime

- One compiled binary and one OCI image support all roles.
- Select the role only from validated controller-supplied configuration.
- Start exactly one role per process.
- Provide `/healthz`, `/readyz`, and `/role` for every role.
- `ai` is a deterministic local stub in the MVP and downloads no model.
- Handle `SIGTERM`, stop accepting work, and exit within the grace period.

### Role transitions

- A transition updates the pod template role and expression revision.
- Kubernetes performs a normal rollout; never mutate the active process in place.
- `status.expressedRole` changes only after the new workload is Ready.
- On rollout timeout, restore the last known-good role and surface a degraded condition.
- Cooldown and failed-decision backoff prevent oscillation and retry storms.
- Controller restart during transition must preserve correct behavior.

### Security

- Run as non-root with a read-only root filesystem where feasible.
- Drop Linux capabilities, use seccomp, and disable privilege escalation.
- Do not use `hostPath`, host PID/network, privileged mode, or writable service-account tokens without explicit reviewed need.
- The CRD must not expose arbitrary commands, arguments, source code, plugin URLs, model URLs, executable paths, or role-specific images.
- Limit controller RBAC to resources it reconciles.
- Never print credentials, tokens, full environment dumps, or secret values.
- Do not copy kubeconfig, registry credentials, SSH keys, or workstation secrets into Cloud environment setup.

## 6. Coding rules

- Write idiomatic Go and run `gofmt`.
- Accept `context.Context` at I/O boundaries and honor cancellation.
- Wrap errors with operation and resource context while preserving causes.
- Avoid package globals for mutable state.
- Inject clocks, readers, and clients where determinism or testing requires it.
- Prefer table-driven tests and small interfaces owned by consumers.
- Avoid fixed sleeps in tests; use bounded polling and observed conditions.
- Generated code and manifests must be regenerated by repository targets, not manually edited.
- Public API changes require validation, compatibility analysis, generated assets, samples, and tests in the same change.

## 7. Testing rules

Map every behavior change to `SC-*` criteria and the narrowest test layer that proves it.

### Cloud-safe validation

Typical Cloud checks:

```bash
./scripts/verify-cloud.sh
```

Once the Makefile exists, this should cover formatting, vet, unit tests, envtest where available, generation cleanliness, and race tests as appropriate. A Cloud environment blocker is a documented blocker, not a pass.

### Local integration validation

For the full E2E path, refuse external kubeconfig state and let the helper establish an isolated pre-creation/existing-cluster guard:

```bash
unset KUBECONFIG
./scripts/verify-local.sh
```

Before any additional direct `kubectl` operation against the created cluster, run:

```bash
./scripts/kind-e2e-preflight.sh
```

A test passes only when it observes the intended behavior, including Ready conditions, role endpoint, rollout/rollback state, and identical image digest where relevant.

## 8. Git and PR rules

- One task maps to one branch/Worktree/Cloud thread.
- Branch names should be descriptive, for example `codex/m1-crd-api` or `codex/m2-expression-engine`.
- Keep commits reviewable and avoid unrelated formatting churn.
- Cloud output must include base commit, changed files, generated files, and local-only checks required.
- Do not auto-merge. Human review and Local validation remain required for milestones involving Kubernetes behavior.
- Request GitHub Codex review with `@codex review` or use repository auto-review settings; do not reproduce this by storing an API key in the repository.

## 9. Custom agent responsibilities

- `architect`: read-only plan, invariants, API/state-machine implications.
- `implementer`: one approved bounded vertical slice.
- `code_reviewer`: read-only correctness and maintainability review.
- `test_engineer`: coverage design and permitted test changes.
- `security_reviewer`: read-only API/RBAC/runtime/supply-chain/agent-boundary review.
- `deployment_validator`: disposable local kind validation only.

Subagents inherit the parent task's sandbox and execution environment. A specialized name does not grant Docker, network, or cluster capabilities.

## 10. Stop conditions

Stop expanding the task and return a handoff when any of these occurs:

- unresolved P0/P1 correctness or security finding;
- ambiguous or non-disposable Kubernetes context;
- required secret or production access;
- a task would cross into another Worktree's owned files;
- generated changes cannot be reproduced;
- specification and architecture conflict;
- the remaining work is a distinct backlog item;
- Cloud needs a local-only acceptance test.

## 11. Definition of done

A change is complete only when:

1. scope and acceptance criteria are explicit;
2. implementation and tests are present;
3. generated artifacts are reproducible;
4. required independent agents have reported and P0/P1 findings are resolved;
5. available checks pass and unavailable checks are marked with a concrete handoff;
6. docs and backlog claims match actual evidence;
7. no architecture or security invariant was weakened.
