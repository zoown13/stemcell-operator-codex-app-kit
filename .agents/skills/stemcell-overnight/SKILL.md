---
name: stemcell-overnight
description: Prepare and execute a safe overnight StemCell Operator batch using bounded Codex Cloud tasks, or an optional local Codex app Automation on an always-on machine.
---

# Overnight batch

Use this skill when the user wants work to continue unattended. Do not model the night as one unbounded six-to-eight-hour task. Split it into reviewable tasks with independent completion contracts.

## Choose the execution pattern

### Preferred: Cloud task batch

Use when the computer may sleep or turn off.

1. Read the source-of-truth documents and current backlog.
2. Select up to four independent tasks with non-overlapping file ownership.
3. Define dependencies. A task that edits API types or shared generated assets must run before dependent tasks, not in parallel.
4. Give each Cloud task:
   - one backlog item or sub-item;
   - explicit SC-* criteria;
   - owned and forbidden paths;
   - Cloud-safe verification commands;
   - `LOCAL_REQUIRED` checks;
   - required specialist agents;
   - a branch/PR or diff handoff contract.
5. Never have multiple tasks edit the same generated manifests, `go.mod`, shared API types, or backlog checkboxes.
6. The next Local Worktree session integrates tasks one at a time and runs `./scripts/verify-local.sh`.

Use `prompts/cloud/07-overnight-batch.md` as the operator prompt template.

### Optional: Codex app Automation

Use only on an always-on trusted development machine.

1. Run in a dedicated background Worktree, never the main checkout.
2. Use workspace-write rather than full access unless the user explicitly accepts the risk.
3. Select exactly one bounded unchecked backlog item.
4. Never push, merge, change branch protection, access production/shared Kubernetes, or use arbitrary credentials.
5. Write `docs/reports/latest-automation.md` with scope, diff, agents, commands, and blockers.
6. Surface findings in the Codex app Triage inbox.

Use `prompts/automation/nightly-bounded-iteration.md` as the Automation prompt.

## Specialist sequence

For each implementation task:

1. spawn `architect` for a read-only plan;
2. spawn `implementer` for the approved owned files;
3. spawn `code_reviewer` and `test_engineer` for independent verification;
4. spawn `security_reviewer` when security boundaries changed;
5. leave `deployment_validator` for the next verified Local Worktree unless the current task is already local and disposable.

## Stop conditions

Stop rather than broaden scope when:

- P0/P1 findings remain;
- the task needs local Docker/kind or private infrastructure;
- file ownership overlaps another active task;
- a required secret or production access is requested;
- generated outputs cannot be reproduced;
- the next step is a distinct backlog item.

## Required handoff

Every task reports:

```markdown
# Codex handoff
- Execution mode
- Base revision and branch/PR
- Scope and SC-* criteria
- Owned files changed
- Generated files changed
- Specialist agents used and findings
- Commands: pass / fail / skip
- LOCAL_REQUIRED validation
- Risks and recommended integration order
```
