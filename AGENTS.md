# Codex repository entry point

Before changing anything, read these files in order:

1. `Instructions.md`
2. `docs/SPEC.md`
3. `docs/ARCHITECTURE.md`
4. `docs/BACKLOG.md`
5. `docs/OPERATING_MODEL.md`

Treat them as the repository source of truth. Do not infer a broader product than they define.

## Establish execution mode

At the beginning of every task, state which mode you are in:

- **Cloud**: remote Codex environment; use Cloud-safe checks only unless a capability is explicitly proven.
- **Worktree**: isolated checkout on the user's machine.
- **Local**: main local project directory.

Never assume Cloud can access the user's Docker daemon, kind cluster, private registry, VPN, kubeconfig, or local credentials. Never assume Local/Worktree may use an arbitrary Kubernetes context.

## Mandatory workflow

- Select one bounded backlog item unless the user explicitly scopes the task differently.
- Map the task to one or more `SC-*` acceptance criteria before editing.
- Use the relevant skill under `.agents/skills/`.
- For cross-layer changes, explicitly spawn `architect` before implementation.
- Spawn `implementer` only after the plan and file ownership are concrete.
- Before completion, explicitly spawn `code_reviewer` and `test_engineer`.
- Spawn `security_reviewer` for CRD, RBAC, runtime, container, supply-chain, Cloud environment, or automation changes.
- Spawn `deployment_validator` only in a verified disposable local Kubernetes environment.
- The parent agent owns integration and must verify delegated claims from diffs, files, or command output.

Codex spawns custom agents only when explicitly asked. Do not merely mention that an agent “would be useful”; actually delegate when the workflow requires it.

## Mode boundaries

### Cloud

Allowed by default:

- source and documentation edits;
- code generation and refactoring;
- unit tests, envtest, static analysis, formatting, and manifest generation when dependencies exist;
- opening a PR or returning a diff;
- independent read-only reviews.

Not a completion gate in Cloud unless explicitly available and demonstrated:

- Docker image build or runtime execution;
- kind/minikube cluster tests;
- private registry, VPN, or enterprise cluster access;
- production or shared cluster operations.

Use `./scripts/verify-cloud.sh` and report skipped local-only checks.

### Local or Worktree

Use a Worktree for isolated implementation, integration, and background Automation. Use Local only when intentional edits to the main checkout are desired.

For the full E2E path, unset external kubeconfig state and use `./scripts/verify-local.sh`; it establishes an isolated safe pre-creation/existing-cluster guard. Before any additional direct `kubectl` command, run:

```bash
./scripts/kind-e2e-preflight.sh
```

Never use a production, shared, or ambiguous context.

## Non-negotiable architecture invariants

- The same immutable runtime image digest serves every supported role.
- A pod expresses exactly one role at a time.
- Role changes use declarative reconciliation and rollout, never in-place process mutation.
- CRD fields cannot carry arbitrary shell commands, source code, image references per role, executable URLs, or plugin/model download locations.
- Expression evaluation is deterministic and testable as a pure function.
- Reconciliation is idempotent; durable transition state is derivable after controller restart.
- Status updates use Kubernetes conditions and accurately distinguish desired, transitioning, ready, invalid, and degraded states.
- Do not mark backlog work complete until mapped acceptance checks pass.
- Never merge, force-push, change branch protection, expose secrets, or deploy to production.

## Verification order

After scaffolding, prefer repository targets in this order:

```bash
make fmt
make vet
make test
make manifests generate
git diff --exit-code
make test-race
make verify
```

Run `make test-e2e` only when Docker, kind, and a disposable context are available. Record every command as passed, failed, or skipped with reason.

## Review guidelines

Treat the following as high-priority defects:

- role-specific image substitution or runtime executable download;
- nondeterministic expression decisions;
- reconcile hot loops, lost transitions after restart, or incorrect status;
- unsafe Kubernetes context handling;
- overly broad RBAC or privileged workload configuration;
- tests that claim integration success without observing workload readiness and image identity;
- Cloud tasks claiming local-only validation they did not perform.

## Completion response

Report:

1. execution mode and scoped backlog item;
2. acceptance criteria addressed;
3. files changed;
4. specialist agents actually used and their material findings;
5. commands actually run with pass/fail/skip results;
6. unresolved risks, handoff requirements, and next unchecked backlog item.
