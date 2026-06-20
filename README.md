# StemCell Operator — Codex App Project Kit

This repository kit prepares the **Codex app** to implement a Kubernetes proof of concept inspired by biological gene expression: one immutable runtime image can express one bounded role (`api`, `worker`, or `ai`) under the control of a Kubernetes operator.

The kit is the engineering control plane for the project. It contains the product specification, repository instructions, reusable skills, custom subagents, Cloud task prompts, Local/Worktree validation scripts, and an operating model for overnight work.

It does **not** call the Codex API and it contains no Codex GitHub Action. Codex authentication, Cloud tasks, Worktrees, Automations, and GitHub review are configured through the Codex app/web product.

## Recommended operating model

> Cloud proposes implementation; Local Worktree proves Kubernetes behavior.

| Work | Recommended mode |
|---|---|
| Scaffolding, bounded feature implementation, unit tests, docs | Cloud |
| Parallel alternative implementations or independent review | Cloud |
| Normal interactive edits with isolation | Worktree |
| Docker image builds, kind, Helm, webhooks, RBAC, rollout tests | Local Worktree |
| Final integration and release evidence | Local Worktree |
| Scheduled unattended checks on an always-on machine | Codex app Automation in a dedicated Worktree |

Cloud tasks must not claim success for Docker/kind behavior unless the configured Cloud environment actually provides and validates those capabilities. Local validation is the final gate for Kubernetes acceptance criteria.

## Start here

1. Put this kit in an empty Git repository and commit it.
2. Connect the repository to Codex Cloud through Codex settings.
3. Open the same repository as a project in the Codex app.
4. Read `docs/CODEX_APP_SETUP.md` and configure:
   - a Cloud environment using `scripts/codex-cloud-setup.sh`;
   - a Local environment setup action using `scripts/codex-worktree-setup.sh`;
   - project actions for Cloud-safe and Local validation.
5. Start the first Cloud thread with `prompts/cloud/01-m0-scaffold.md`.
6. Integrate the resulting branch or PR in a Local Worktree using `prompts/local/01-integrate-cloud-change.md`.

## First Codex prompt

```text
Read AGENTS.md, Instructions.md, docs/SPEC.md, docs/ARCHITECTURE.md,
docs/BACKLOG.md, and docs/OPERATING_MODEL.md.

Use $stemcell-scaffold to complete milestone M0 only.
Explicitly spawn architect for planning, implementer for the approved slice,
and code_reviewer plus test_engineer for independent verification.
Do not perform Docker, kind, or production-cluster operations in Cloud mode.
Do not start M1 until M0 acceptance checks pass.
```

## Repository map

```text
AGENTS.md                         Codex auto-discovery entry point
Instructions.md                  Detailed engineering and mode rules
.codex/config.toml               Project-scoped subagent limits
.codex/agents/*.toml             Specialized custom agents
.agents/skills/*/SKILL.md        Reusable project workflows
docs/SPEC.md                     Product and acceptance specification
docs/ARCHITECTURE.md             Architecture and invariants
docs/BACKLOG.md                  Ordered implementation milestones
docs/OPERATING_MODEL.md          Cloud/Worktree/Local decision rules
docs/CODEX_APP_SETUP.md          Codex app and Cloud setup
docs/CLOUD_PLAYBOOK.md           Cloud task decomposition and handoff
docs/LOCAL_VALIDATION.md         Docker/kind integration runbook
docs/AUTOMATIONS.md              Optional local background automation
docs/GITHUB_INTEGRATION.md       PR and Codex review workflow
docs/REFERENCES.md               Official product/tool references
prompts/cloud/                    Ready-to-paste Cloud task prompts
prompts/local/                    Ready-to-paste Local/Worktree prompts
prompts/automation/               Ready-to-paste app Automation prompt
scripts/                          Setup, validation, and safety helpers
.worktreeinclude                   Empty-by-default ignored-file copy policy
```

## Overnight work

For a machine-independent overnight batch, launch several bounded **Cloud** tasks before leaving. Each task must own disjoint files or milestones and end with a diff or draft PR. The next Local Worktree session integrates them and runs Docker/kind tests.

Codex app Automations are a separate option. They run on the local machine and therefore require the computer and app to remain available. Automation findings appear in the app's Triage inbox. See `docs/AUTOMATIONS.md`.

This kit intentionally does not promise that one agent will work continuously for six to eight hours. It converts that time window into multiple bounded tasks with explicit completion contracts, which is safer and easier to review.

## Safety defaults

- no production-cluster credentials;
- no automatic merge or force-push;
- no arbitrary command/plugin/model execution from the CRD;
- no runtime executable downloads;
- no privileged pods, host paths, or ambiguous Kubernetes contexts;
- one bounded backlog item per implementation task;
- independent code, test, security, and deployment validation roles;
- every completion claim includes commands actually run and skipped checks.

## Validate the kit

```bash
./scripts/check-codex-kit.py
./scripts/validate-repo.sh
```

## License

Choose and add a license before publishing. Apache-2.0 is common for Kubernetes operators, but the repository owner should decide explicitly.
