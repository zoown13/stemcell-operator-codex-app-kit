# Architecture

## 1. Concept mapping

| Biology analogy | Software element |
|---|---|
| Genome | Immutable universal OCI image |
| Gene expression | Validated role selection plus pod-template configuration |
| Cell differentiation | Kubernetes rollout to a pod expressing one role |
| Regulatory signal | ConfigMap values observed by the controller |
| Homeostasis | Cooldown, readiness gates, status conditions, rollback |
| Cell lineage memory | Last known-good role and expression revision persisted in API state |

The analogy is intentionally bounded. Software does not reproduce, mutate, or execute arbitrary latent genes.

## 2. Components

```text
                        +-----------------------+
User / GitOps --------> | StemCell custom       |
                        | resource              |
                        +-----------+-----------+
                                    |
                                    v
+-------------------+    +----------+-----------+     +-------------------+
| Signal ConfigMap  | -> | StemCell controller  | --> | Deployment/Service|
+-------------------+    +----------+-----------+     +---------+---------+
                                    |                           |
                                    v                           v
                        +-----------+-----------+     +---------+---------+
                        | Expression engine     |     | Universal runtime |
                        | pure deterministic    |     | api|worker|ai     |
                        +-----------------------+     +-------------------+
```

### Controller

The controller owns Kubernetes state transitions. It reads the resource and signal snapshot, invokes the expression engine, creates or updates owned resources, observes rollout state, and writes status.

### Expression engine

A pure Go package accepts a typed policy, signal map, currently expressed role, last transition time, and evaluation time. It returns a typed decision and explanation. It never calls Kubernetes APIs.

Suggested interface:

```go
type Input struct {
    Policy            Policy
    Signals           map[string]string
    ExpressedRole     Role
    LastTransitionAt  *time.Time
    Now               time.Time
}

type Decision struct {
    DesiredRole       Role
    Action            Action // Hold, Transition, Invalid
    MatchedRule       string
    Reason            string
    CooldownRemaining time.Duration
}

func Evaluate(input Input) Decision
```

### Universal runtime

One binary dispatches to one compile-time role implementation after validating `STEMCELL_ROLE`. Each role implements a narrow lifecycle contract:

```go
type Role interface {
    Name() string
    Run(context.Context, Config) error
    Ready() bool
}
```

The binary should not use reflection-based plugin loading or subprocess dispatch.

## 3. Reconciliation state machine

```text
                 invalid spec/signal
          +------------------------------+
          |                              v
Unknown -> Evaluating -> Stable -> Transitioning -> Stable
                 |          ^            |
                 |          |            | timeout
                 |          +--Rollback--+
                 v
              Degraded
```

Suggested phases:

- `Pending`: no available workload yet;
- `Ready`: desired and expressed roles match and Deployment is available;
- `Transitioning`: a new revision is rolling out;
- `Degraded`: invalid expression or failed rollout requiring user/input change.

### Reconcile outline

1. Fetch `StemCell`; ignore NotFound.
2. Handle deletion/finalization only if a real external resource later requires it; the MVP likely needs no finalizer.
3. Validate or normalize defaults already enforced by the API server.
4. Read the referenced ConfigMap once for a consistent snapshot.
5. Evaluate policy.
6. If invalid, update conditions and stop with an event-driven requeue.
7. If holding due to cooldown, update status and requeue at the cooldown boundary.
8. Build the desired Deployment/Service from pure helper functions.
9. Create/patch owned resources.
10. Observe Deployment generation and availability.
11. Mark transition complete only when the new revision is available.
12. On timeout, reconcile rollback revision and conditions.
13. Patch status only when it materially changes.

## 4. Revision and transition persistence

The controller must not rely only on in-memory timers. Persist enough state to resume after restart:

- `status.expressionRevision`;
- `status.expressedRole`;
- `status.previousRole`;
- `status.lastTransitionTime`;
- a condition carrying the transition start time;
- Deployment annotations for role and revision.

A resource generation change or signal ConfigMap resource-version change provides input identity. The exact failed-decision suppression mechanism should be documented and tested before M4 is closed.

## 5. Same-image proof

End-to-end tests must obtain the image ID/digest from pods for each role and assert equality. Merely comparing a mutable tag is insufficient for SC-01. For a local kind load, record the built image ID and assert every role pod references that exact local image artifact.

## 6. Security model

The controller is trusted to choose among a fixed enum of role identifiers. It is not trusted to execute user-supplied code. The runtime image contains bounded implementations whose attack surface is known at build time.

Threats explicitly addressed:

- command injection through CRD values;
- role-specific image substitution;
- unbounded ConfigMap/rule input;
- privilege escalation in runtime pods;
- controller over-permission;
- denial of service through reconcile flapping;
- secret leakage in logs/status.

## 7. Failure handling

| Failure | Expected behavior |
|---|---|
| ConfigMap absent | `ExpressionValid=False`, watch/requeue on ConfigMap creation |
| Signal absent | invalid decision with stable reason; no silent zero value |
| Numeric parse error | `ExpressionValid=False`; no transition |
| Deployment create conflict | retry through normal controller error handling |
| Target never ready | timeout, condition, rollback |
| Controller restart | derive state from CR/status/Deployment and continue |
| Unsupported role at runtime | fail fast, unready, non-zero exit |
| Rapid signal oscillation | deterministic selection plus cooldown/hysteresis |

## 8. Future extensions, not MVP

Potential research after `v0.1.0`:

- weighted or multi-signal conditions;
- explicit hysteresis thresholds;
- signed WebAssembly modules under a separate threat model;
- role capability manifests and SBOM-aware expression;
- node/edge placement signals;
- formal state-machine verification;
- comparison against separate-image microservices for latency, storage, vulnerability surface, and rollback behavior.
