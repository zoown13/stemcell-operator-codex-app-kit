# Product and engineering specification

**Project:** StemCell Operator  
**Status:** MVP specification  
**Primary implementation language:** Go  
**Target platform:** Kubernetes  
**API maturity:** `v1alpha1`

## 1. Who uses it

### Primary user: platform engineer / SRE

A platform engineer wants to deploy one audited runtime artifact and declaratively choose or change its operational role without maintaining a separate image for each role. They use Kubernetes manifests, inspect status/conditions, and observe a controlled rollout.

### Secondary user: software architecture researcher

A researcher wants a concrete, measurable prototype for “genome plus expression” architecture: invariant code payload, externally controlled role expression, deterministic differentiation, and reversible transitions.

### Maintainer

A Go/Kubernetes contributor extends expression rules, controller behavior, tests, and documentation without weakening reproducibility or security boundaries.

## 2. Problem statement

Typical services produce a distinct artifact for each role. That is efficient, but it does not test whether a single immutable artifact can safely and predictably express multiple bounded behaviors under declarative policy.

The MVP must answer this question:

> Can one immutable OCI image act as a small set of predefined roles while a Kubernetes operator deterministically controls differentiation, rollout, observation, and rollback?

## 3. Product behavior

A user creates a `StemCell` custom resource. The operator evaluates either a manual target or named signals from a ConfigMap, chooses one allowed role, and reconciles a Deployment. The Deployment always references the same genome image. Differentiation is represented by a validated role value and expression revision in the pod template, causing a normal rollout.

Supported roles:

- `api`: exposes a small HTTP API and health endpoints;
- `worker`: processes deterministic demo jobs from an in-memory or local test source and exposes health/status endpoints;
- `ai`: exposes a deterministic local `/infer` stub plus health endpoints; it downloads no model.

The role implementations are demonstrations, not production application frameworks.

## 4. Scope

### MVP capabilities

1. `StemCell` CRD in `genome.stemcell.io/v1alpha1`.
2. Manual expression mode.
3. Policy expression mode using values from one referenced ConfigMap.
4. Deterministic rule priority and tie-breaking.
5. Cooldown between successful role transitions.
6. Reconciliation of a Deployment and a Service when the role exposes HTTP.
7. Status with desired role, expressed role, previous role, revision, transition timestamps, and conditions.
8. Rollout timeout and rollback to the last known-good role.
9. One universal runtime binary/image for all roles.
10. Unit, controller, and kind end-to-end tests.
11. Metrics, structured logs, health/readiness endpoints, and sample manifests.

### Explicit non-goals

- arbitrary code, commands, WebAssembly, or plugin loading;
- downloading role packages or models at runtime;
- mutating a running container into another role;
- expressing multiple roles in one pod;
- production autoscaling or cost optimization;
- multi-cluster scheduling;
- service mesh integration;
- a general policy language such as CEL/Rego in the MVP;
- production AI inference.

## 5. Baseline toolchain

The initial implementation should target:

- Go `1.26.x`;
- Kubebuilder `v4.15.x` with the Go v4 plugin;
- `controller-runtime v0.24.x`;
- a Kubernetes version supported by that controller-runtime release;
- `kind` for end-to-end testing.

The generated `go.mod` and CI matrix are the final executable record of exact versions.

## 6. API contract

Illustrative resource:

```yaml
apiVersion: genome.stemcell.io/v1alpha1
kind: StemCell
metadata:
  name: demo
spec:
  genome:
    image: ghcr.io/example/stemcell-runtime:v0.1.0
    imagePullPolicy: IfNotPresent
  replicas: 1
  expression:
    mode: Policy
    defaultRole: api
    cooldown: 60s
    rolloutTimeout: 120s
    evaluationInterval: 10s
    signalConfigMapRef:
      name: stemcell-signals
    rules:
      - name: ai-requested
        priority: 200
        when:
          signal: aiRequested
          operator: Eq
          value: "true"
        express: ai
      - name: queue-backed-up
        priority: 100
        when:
          signal: queueDepth
          operator: Gte
          value: "100"
        express: worker
```

Manual mode uses `spec.expression.targetRole` and ignores policy rules:

```yaml
expression:
  mode: Manual
  targetRole: api
  cooldown: 30s
  rolloutTimeout: 120s
```

### Allowed values

- roles: `api`, `worker`, `ai`;
- modes: `Manual`, `Policy`;
- operators: `Eq`, `NotEq`, `Gt`, `Gte`, `Lt`, `Lte`;
- durations must be positive and bounded by validation markers;
- rule names must be unique within a resource;
- signal and rule counts must have conservative maximums.

### Policy semantics

1. Read a snapshot of the referenced ConfigMap.
2. Evaluate all valid rules against that same snapshot.
3. Select matching rule with greatest numeric priority.
4. Break equal-priority ties by lexicographically ascending rule name.
5. If none match, select `defaultRole`.
6. If the selected role equals the expressed role, do nothing.
7. If cooldown has not elapsed, retain the expressed role and surface the pending decision in status.
8. Otherwise begin a rollout to the selected role.

Numeric operators parse base-10 decimal values. Parse failures are permanent input errors until the ConfigMap or spec changes; they must not silently evaluate to false.

## 7. Status contract

Illustrative status:

```yaml
status:
  observedGeneration: 4
  phase: Ready
  desiredRole: worker
  expressedRole: worker
  previousRole: api
  expressionRevision: "7"
  lastEvaluationTime: "2026-06-20T15:00:00Z"
  lastTransitionTime: "2026-06-20T15:00:08Z"
  conditions:
    - type: Ready
      status: "True"
      reason: WorkloadReady
      message: Deployment is available in role worker
    - type: ExpressionValid
      status: "True"
      reason: RuleSelected
      message: Rule queue-backed-up selected role worker
    - type: Transitioning
      status: "False"
      reason: RolloutComplete
```

Required condition types:

- `Ready`;
- `ExpressionValid`;
- `Transitioning`;
- `Degraded`.

Use Kubernetes condition conventions and stable reason strings.

## 8. Workload contract

The reconciled Deployment must:

- reference exactly `spec.genome.image` for every role;
- set `STEMCELL_ROLE` to the selected role;
- set a pod-template annotation `genome.stemcell.io/expression-revision`;
- have an owner reference to the `StemCell` resource;
- apply secure container defaults;
- expose named health/readiness ports and probes;
- use a rolling update with bounded unavailability;
- carry labels that identify the resource and expressed role.

A Service is reconciled for roles that expose HTTP. Removing/recreating a Service during a role transition is allowed for the MVP only if behavior is deterministic and covered by tests; a stable Service is preferred.

## 9. Rollback behavior

When a new Deployment revision fails to become available before `rolloutTimeout`:

1. set `Degraded=True` and `Transitioning=False` with reason `RolloutTimedOut`;
2. restore the last known-good role in the pod template;
3. increment the expression revision;
4. wait for the rollback rollout;
5. keep the failed desired role visible in status for diagnosis;
6. avoid retrying the same failed decision until input changes or an explicit bounded backoff expires.

The controller must survive restarts by deriving transition state from the resource and owned workload, not process memory alone.

## 10. Observability

Controller metrics should include:

- `stemcell_expression_transitions_total{from_role,to_role,result}`;
- `stemcell_expression_evaluations_total{result}`;
- `stemcell_rollbacks_total{failed_role}`;
- normal controller-runtime reconciliation metrics.

Logs must include resource namespace/name, generation, desired role, expressed role, decision reason, and revision. Do not put signal values in logs by default if they may be sensitive.

Every runtime role must expose:

- `GET /healthz` — process liveness;
- `GET /readyz` — role readiness;
- `GET /role` — JSON containing role, build version, and expression revision.

## 11. Success criteria

The MVP succeeds only when all criteria below are demonstrated in automated tests or a documented reproducible validation:

| ID | Criterion |
|---|---|
| SC-01 | A single OCI image digest starts successfully as `api`, `worker`, and `ai`. |
| SC-02 | Changing manual target from `api` to `worker` completes a controlled rollout within 120 seconds in the reference kind environment. |
| SC-03 | ConfigMap signals deterministically select `ai`, `worker`, or the default `api` according to priority and tie-breaking. |
| SC-04 | Cooldown prevents repeated transitions and does not create a reconcile hot loop. |
| SC-05 | `status.observedGeneration`, roles, revision, timestamps, and conditions accurately reflect steady, transitioning, invalid, and degraded states. |
| SC-06 | A deliberately unready target role triggers timeout and rollback to the last known-good role. |
| SC-07 | Controller restart during a transition does not lose or corrupt transition state. |
| SC-08 | CRD validation rejects unsupported roles/modes/operators, duplicate rule names, unsafe fields, and invalid duration/rule bounds. |
| SC-09 | Unit, controller, race, manifest-generation, and kind end-to-end checks pass in CI. |
| SC-10 | Runtime and controller containers use the documented restricted security context and require no production-grade cluster privileges. |
| SC-11 | No CRD field enables arbitrary command execution, executable download, per-role image substitution, or in-place process mutation. |
| SC-12 | README and samples allow a new contributor to reproduce the three role expressions and one rollback scenario. |

## 12. Release exit gate

A `v0.1.0` tag is permitted only after SC-01 through SC-12 pass, the API is clearly marked experimental, image provenance is documented, and no unresolved P0/P1 review finding remains.
