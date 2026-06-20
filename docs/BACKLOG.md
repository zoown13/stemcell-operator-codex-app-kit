# Ordered implementation backlog

Codex must select the highest-priority unchecked milestone that fits one bounded run. A checkbox may be marked complete only after its acceptance checks pass.

## M0 — Repository and Kubebuilder scaffold

- [ ] Initialize the Go module and Kubebuilder v4 project.
- [ ] Create the `StemCell` API/controller skeleton in `genome.stemcell.io/v1alpha1`.
- [ ] Preserve this kit's `AGENTS.md`, `Instructions.md`, skills, agents, and docs.
- [ ] Add `make verify` and placeholders for `make test-e2e`.
- [ ] Add baseline CI for formatting, vet, tests, generated-manifest cleanliness, and race tests.

**Acceptance:** project builds; `make manifests generate` is clean and repeatable; `go test ./...` passes; CI YAML parses.

## M1 — CRD model and validation

- [ ] Implement genome, expression, rules, status, role/mode/operator enums, and defaults.
- [ ] Add schema bounds, CEL markers where appropriate, printer columns, and status subresource.
- [ ] Add sample Manual and Policy resources.
- [ ] Test valid and invalid serialization/validation behavior.

**Acceptance:** SC-08 plus generated CRD review.

## M2 — Pure expression engine

- [ ] Implement deterministic string and numeric comparisons.
- [ ] Implement priority and rule-name tie-breaking.
- [ ] Implement default role and explicit invalid-decision reasons.
- [ ] Implement cooldown decision semantics without I/O.
- [ ] Add comprehensive table-driven and fuzz tests.

**Acceptance:** SC-03 and the pure portion of SC-04.

## M3 — Universal runtime

- [ ] Implement one binary with `api`, `worker`, and deterministic `ai` stub roles.
- [ ] Implement common health, readiness, role metadata, signal handling, and graceful shutdown.
- [ ] Add a multi-stage, non-root OCI image and SBOM/provenance hooks.
- [ ] Add role contract tests.

**Acceptance:** role unit/integration tests and groundwork for SC-01/SC-10/SC-11.

## M4 — Controller steady state and transitions

- [ ] Reconcile Deployment, Service, labels, probes, security context, owner references, and RBAC.
- [ ] Watch referenced ConfigMaps.
- [ ] Implement expression revision and normal role rollout.
- [ ] Implement status phases and conditions.
- [ ] Avoid no-op writes and hot loops.

**Acceptance:** SC-02, SC-04, SC-05, SC-10, and SC-11 in controller tests.

## M5 — Timeout, rollback, and restart recovery

- [ ] Persist transition state in CR status/workload annotations.
- [ ] Detect rollout timeout and restore last known-good role.
- [ ] Suppress unsafe repeated retries of an unchanged failed decision.
- [ ] Add controller-restart-during-transition tests.

**Acceptance:** SC-06 and SC-07.

## M6 — End-to-end environment and observability

- [ ] Build/load one image into kind and express all roles.
- [ ] Assert the same image ID/digest across role transitions.
- [ ] Add transition, rollback, status, and security-context e2e tests.
- [ ] Add custom metrics and structured logging checks.

**Acceptance:** SC-01, SC-02, SC-03, SC-06, SC-09, and SC-10 in kind/CI.

## M7 — Documentation and v0.1.0 readiness

- [ ] Write user quickstart, architecture decision record, troubleshooting, and demo script.
- [ ] Document threat model, image provenance, SBOM, and known limitations.
- [ ] Run independent code, test, security, and deployment reviews.
- [ ] Close or explicitly defer all release-gate findings.

**Acceptance:** SC-12 and the release exit gate in `docs/SPEC.md`.
