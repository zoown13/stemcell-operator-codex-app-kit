# Codex app Automation — one bounded local iteration

Execution mode: Worktree created for this Automation.

Read `AGENTS.md`, `Instructions.md`, `docs/SPEC.md`, `docs/ARCHITECTURE.md`, `docs/BACKLOG.md`, `docs/OPERATING_MODEL.md`, and `docs/AUTOMATIONS.md`.

Use `$stemcell-overnight`.

1. Inspect the worktree and select exactly one small unchecked backlog item or one read-only audit that does not require user input.
2. State owned paths, forbidden paths, mapped SC criteria, and stop conditions before editing.
3. Never use a production/shared cluster, external kubeconfig, private credential, unrestricted network access, push, merge, force-push, or branch-protection change.
4. Spawn the required specialist agents. Keep parallel ownership disjoint.
5. Run Cloud-safe checks. Run local Docker/kind checks only when the repository's safety preflight proves a disposable environment and the task explicitly needs them.
6. Stop on P0/P1 findings, ambiguous context, unreproducible generation, scope collision, or need for a secret.
7. Write or update `docs/reports/latest-automation.md` with scope, changed files, agents used, commands, findings, blockers, and next action.
8. Leave a reviewable Worktree diff for the Triage inbox. Do not mark a milestone complete without all required evidence.
