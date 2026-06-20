# Codex app operating model

## 1. Principle

The project uses a hybrid workflow:

> **Cloud proposes implementation; Local Worktree proves Kubernetes behavior.**

This is not a fallback arrangement. It intentionally separates scalable code work from environment-sensitive evidence.

## 2. Mode selection

| Task | Cloud | Worktree | Local main checkout |
|---|---:|---:|---:|
| Read/specify/plan | Preferred | Good | Good |
| Bounded Go implementation | Preferred | Preferred | Allowed |
| Unit tests and static analysis | Preferred | Preferred | Allowed |
| Independent review | Preferred | Good | Allowed |
| Parallel alternatives | Preferred | Preferred with disjoint paths | Avoid |
| Docker image build | Only if environment proves Docker | Preferred | Allowed |
| kind/minikube E2E | Not an assumed capability | Required | Allowed |
| VPN/private registry/company cluster | No by default | Required when approved | Required when approved |
| Final milestone evidence | Insufficient alone | Preferred | Allowed |
| Scheduled background work | Cloud tasks for remote execution | App Automation on always-on machine | Avoid main checkout |

## 3. Work units

Each Codex task must define:

```yaml
base_revision: <commit SHA or branch>
mode: Cloud | Worktree | Local
backlog_item: M0/M1/...
acceptance_criteria: [SC-xx]
owned_paths: []
forbidden_paths: []
deliverable: diff | branch | draft PR | review report
cloud_safe_checks: []
local_required_checks: []
stop_conditions: []
```

A task should fit one reviewable vertical slice. Do not use time spent as the definition of completion.

## 4. Parallelism rules

Parallelize only when file ownership is non-overlapping.

Safe examples:

- expression-engine implementation and README improvements;
- runtime role contract tests and read-only architecture review;
- security review and test coverage analysis.

Unsafe examples:

- two tasks changing `api/v1alpha1/*`;
- two tasks running Kubebuilder generation from different API versions;
- controller and API tasks both editing generated RBAC/CRD files;
- multiple tasks changing `go.mod` or backlog checkboxes;
- implementation and “fix all findings” tasks running against a moving base.

When dependencies exist, run tasks sequentially or branch dependent work from the prerequisite branch.

## 5. Branch conventions

Suggested names:

```text
codex/m0-scaffold
codex/m1-crd-contract
codex/m2-expression-engine
codex/m3-runtime-roles
codex/m4-controller-rollout
codex/review-m4
codex/local-e2e-m4
```

A Cloud task should create or expose a branch/PR only after its Cloud-safe checks are complete. It must not merge.

## 6. Handoff contract

Every Cloud result must contain:

- exact base revision;
- scope and SC-* mapping;
- files changed and generated;
- agent roles actually used;
- commands actually run;
- skipped checks and `LOCAL_REQUIRED` list;
- known risks and dependency order;
- suggested Local integration commands.

Every Local integration result must add:

- Docker/kind versions and cluster name;
- proven kube context;
- image IDs/digests observed for all roles;
- rollout/rollback observations and conditions;
- cleanup result;
- final milestone/backlog decision.

## 7. Review separation

Implementation and approval are separate roles.

- `architect` validates the plan before broad edits.
- `implementer` owns the bounded change.
- `code_reviewer` looks for correctness and regression risk without editing.
- `test_engineer` maps proof to acceptance criteria.
- `security_reviewer` checks attack surfaces and agent/environment boundaries.
- `deployment_validator` operates only on a disposable local cluster.

The parent Codex thread integrates reports and independently checks the evidence.

## 8. Overnight model

### Remote overnight batch

Launch three to five bounded Cloud tasks. Prefer this when the local computer may sleep.

Recommended sequence:

1. prerequisite implementation task;
2. independent test/review tasks based on a stable branch;
3. documentation or samples task with disjoint ownership;
4. next-day Local Worktree integration and kind E2E.

Do not ask one task to “keep working for eight hours.” A task ends when its acceptance contract is met or a stop condition is reached.

### Local Automation

Use only when the machine remains on with Codex app available. Run in a dedicated Worktree and use the prompt under `prompts/automation/`. The output goes to the Codex Triage inbox and optionally `docs/reports/latest-automation.md`.

## 9. Completion rule

Cloud completion means **implementation handoff ready**. It does not mean the Kubernetes milestone is accepted when the success criterion requires Docker/kind evidence.
