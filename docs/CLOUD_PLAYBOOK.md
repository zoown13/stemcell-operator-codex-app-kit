# Codex Cloud playbook

## 1. What belongs in Cloud

Use Cloud for work that can be validated from a clean repository checkout:

- Kubebuilder/Go scaffolding after environment setup;
- CRD types and validation;
- pure expression engine and tests;
- controller logic with fake client or envtest;
- universal runtime and contract tests;
- docs, examples, refactoring, static analysis;
- independent code, test, and security review.

Do not assume access to local Docker, kind, private registries, corporate VPN, or workstation credentials.

## 2. Task sizing

One Cloud task should have one primary deliverable and normally modify fewer than three architectural layers. Split broad work by backlog milestone or stable interface boundary.

Good:

```text
Implement M2 pure expression engine under internal/expression and its tests.
Do not edit controller or CRD types. Use existing API contracts.
```

Too broad:

```text
Build the entire operator, deploy it, fix everything, and make it production ready.
```

## 3. Cloud task template

```text
Read AGENTS.md, Instructions.md, docs/SPEC.md, docs/ARCHITECTURE.md,
docs/BACKLOG.md, and docs/OPERATING_MODEL.md.

Execution mode: Cloud.
Base revision: <SHA/branch>.
Backlog item: <item>.
Acceptance criteria: <SC list>.
Owned paths: <paths>.
Forbidden paths: <paths>.

Use $stemcell-cloud-task and the relevant domain skill.
Explicitly spawn architect before cross-layer changes.
Spawn implementer for the approved slice, then code_reviewer and test_engineer.
Spawn security_reviewer if the API, RBAC, runtime, image, Cloud setup, or automation boundary changes.

Run bash scripts/verify-cloud.sh and targeted tests. Do not run or claim local Docker/kind tests.
Return a branch/PR or reviewable diff with the required Cloud handoff and LOCAL_REQUIRED checks.
```

## 4. Recommended M0–M4 sequence

1. **M0 scaffold** — sequential; owns project root, module, generated scaffold.
2. **M1 CRD contract** — sequential; owns API and generated CRD assets.
3. After M1 stabilizes, parallelize carefully:
   - M2 expression engine;
   - M3 universal runtime.
4. M4 controller depends on M1 and M2; integrate those before starting.
5. Reviews may run in parallel against a stable branch, but fixes must be integrated serially.
6. kind E2E and deployment validation are Local Worktree tasks.

## 5. Overnight batch example

Launch independent tasks such as:

```text
Task A: M2 expression engine implementation; owns internal/expression/**.
Task B: runtime contract tests; owns internal/runtime/** and cmd/runtime/**.
Task C: read-only review of current M1 branch; no edits.
Task D: documentation/samples for already-merged behavior; owns docs/examples only.
```

Do not launch A and B together if both need to modify shared enums or `go.mod` before those interfaces are stable.

## 6. Cloud completion checklist

- [ ] Base revision recorded
- [ ] Scope and owned paths respected
- [ ] SC-* criteria mapped
- [ ] Required subagents actually spawned
- [ ] Cloud-safe checks run
- [ ] Generated-file cleanliness checked where applicable
- [ ] P0/P1 findings resolved
- [ ] Local-only tests explicitly listed
- [ ] Diff/branch/PR is reviewable
- [ ] No secret or production access introduced
