---
name: stemcell-expression-engine
description: Implement deterministic, pure StemCell policy evaluation including signal parsing, priority, tie-breaking, defaults, cooldown decisions, and decision reasons.
---

# Expression engine workflow

Use for `internal/expression` or any behavior that converts policy and signal snapshots into a role decision.

## Contract

The engine performs no Kubernetes API calls, filesystem access, network access, subprocess execution, or hidden global mutation. Given the same typed input and clock value, it returns the same decision.

## Workflow

1. Write a table-driven failing test for the requested behavior.
2. Model typed inputs and outputs; include a stable machine-readable reason.
3. Parse numeric values explicitly as base-10 decimal and return input errors rather than false matches.
4. Evaluate every rule against one immutable signal snapshot.
5. Select highest priority, then lexicographically ascending rule name.
6. Fall back to `defaultRole` when no rule matches.
7. Return `Hold` when desired equals expressed or cooldown remains.
8. Keep transition persistence and Kubernetes side effects outside this package.
9. Add boundary cases, malformed input cases, deterministic permutation tests, and fuzz tests where useful.
10. Run unit tests with `-race` and ask `code_reviewer` to inspect nondeterminism/time semantics.

## Minimum cases

- all operators;
- negative, zero, decimal, and large numeric values;
- missing and malformed signals;
- equal-priority ties;
- zero matches/default role;
- already-expressed role;
- exact cooldown boundary and clock skew handling;
- rule-order permutations.
