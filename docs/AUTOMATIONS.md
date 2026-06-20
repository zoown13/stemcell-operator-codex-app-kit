# Codex app Automations

## 1. Positioning

Codex app Automations are optional local background jobs. They are not the remote Cloud execution path.

Use them only when:

- the development machine remains powered on and awake;
- Codex app remains available;
- the repository remains accessible at the configured path;
- the task is safe to run without interactive approval;
- a dedicated Worktree isolates changes.

Automation runs and findings appear in the Codex app Triage inbox.

## 2. Recommended automation

Create a standalone/project Automation in the Codex app using:

- Project: this repository
- Workspace: dedicated background Worktree
- Sandbox: workspace-write
- Prompt: `prompts/automation/nightly-bounded-iteration.md`
- Schedule: the user's chosen local schedule

Test the prompt manually in a normal Worktree thread before scheduling it.

## 3. Boundaries

The Automation must:

- select exactly one bounded backlog item or audit task;
- preserve unrelated changes;
- never access a production/shared Kubernetes context;
- never push, merge, force-push, or modify branch protection;
- never request or expose secrets;
- stop on unresolved P0/P1 issues;
- write `docs/reports/latest-automation.md` when it changes files;
- report local-only blockers rather than bypassing them.

Do not use full-access sandbox merely to avoid command failures. Prefer workspace-write and allowlist only commands that are clearly required.

## 4. App availability caveat

Because Automation executes locally, laptop sleep, shutdown, app termination, unavailable mounts, or expired local credentials may interrupt the run. For machine-independent overnight work, launch bounded Cloud tasks instead.

## 5. Notification model

Primary result locations:

- Codex app Triage inbox;
- changed Worktree/diff;
- optional `docs/reports/latest-automation.md`.

For email, rely on an explicit GitHub PR/mention workflow after human review or on the user's normal repository notification settings. This kit does not embed email credentials.

## 6. Cleanup

Frequent Worktree Automations can leave many Worktrees. Archive unneeded runs in Codex app and periodically inspect:

```bash
git worktree list
git worktree prune --dry-run
```

Only prune after confirming no useful uncommitted changes remain.
