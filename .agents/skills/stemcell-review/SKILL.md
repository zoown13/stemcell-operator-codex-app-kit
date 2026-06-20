---
name: stemcell-review
description: Orchestrate independent correctness, test, and security reviews of a StemCell Operator diff and consolidate only actionable, evidence-backed findings.
---

# Review a StemCell change

## Workflow

1. Identify the base/head diff and mapped acceptance criteria.
2. In parallel, explicitly delegate:
   - correctness/state-machine review to `code_reviewer`;
   - test adequacy to `test_engineer` in analysis/review mode;
   - security review to `security_reviewer` when API, RBAC, runtime, image, or workflow files changed;
   - deployment review to `deployment_validator` when manifests/controller transitions changed and kind is available.
3. Independently inspect high-risk claims and remove duplicates.
4. Rank findings P0-P3.
5. Require each finding to contain file/line or symbol evidence, user/operational impact, affected `SC-*`, and remediation.
6. Separate defects from optional improvements and residual validation gaps.
7. Resolve P0/P1 before completion. Resolve P2 when low risk or explicitly track it.

## Review checklist

- same image and one role invariants;
- idempotent reconciliation and restart safety;
- rollout timeout and rollback correctness;
- deterministic expression and cooldown;
- status condition conventions;
- validation/RBAC/pod security;
- tests that prove behavior rather than implementation details;
- generated files and docs consistency;
- no exaggerated completion claims.
