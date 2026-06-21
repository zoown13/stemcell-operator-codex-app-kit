# Migration from the API/GitHub Actions kit

This package replaces the earlier Codex API-oriented automation with a Codex app hybrid workflow.

## Removed

- Codex API invocation scripts;
- `openai/codex-action` workflows;
- repository `OPENAI_API_KEY` requirements;
- scheduled GitHub Actions intended to drive Codex work;
- SMTP notification scripts or secrets;
- assumptions that a single unattended agent should consume a fixed six-to-eight-hour window.

## Added

- explicit Cloud, Worktree, and Local execution boundaries;
- Cloud setup and bounded task prompts;
- Local Worktree integration and safe kind validation runbooks;
- Codex app Automation prompt for an always-on local machine;
- six project-scoped custom agents;
- reusable Cloud/local integration skills;
- PR template separating Cloud evidence from `LOCAL_REQUIRED` evidence;
- kit validator that rejects legacy API automation assets.

## Operational change

Cloud tasks produce a diff, branch, or draft PR. Local Worktree integration proves Docker/Kubernetes behavior. App Automations are optional local jobs whose machine and app must remain available. GitHub PR notifications—not embedded SMTP credentials—provide an optional email completion signal.

## Existing repository migration

When applying this kit to a repository created from the previous package:

1. create a migration branch;
2. remove only the old Codex API workflows/scripts, preserving normal build/test CI;
3. copy the new `AGENTS.md`, `Instructions.md`, `.agents/`, `.codex/`, `docs/`, `prompts/`, and helper scripts after reviewing project-specific differences;
4. run `python3 scripts/check-codex-kit.py` and `bash scripts/validate-repo.sh`;
5. configure Codex Cloud and Codex app using `docs/CODEX_APP_SETUP.md`;
6. test one read-only Cloud task and one read-only Worktree task before implementation.
