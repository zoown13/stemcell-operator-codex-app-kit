# Codex app and Cloud setup

This repository uses Codex product features, not the Codex API.

## 1. Repository preparation

```bash
git init
git add .
git commit -m "chore: initialize StemCell Operator Codex app kit"
git branch -M main
git remote add origin <repository-url>
git push -u origin main
```

Replace module-path placeholders only as part of M0.

## 2. Connect Codex Cloud

In Codex settings:

1. connect the GitHub account and authorize the target repository;
2. enable Codex Cloud for the repository;
3. create a Cloud environment for this project;
4. pin the intended Go version when package-version controls are available;
5. use the following setup script:

```bash
./scripts/codex-cloud-setup.sh
```

The setup script is idempotent. It installs Kubebuilder into a repository-local `.tools/bin` when absent, adds that directory to the shell path for the task, and downloads Go modules after M0 creates `go.mod`.

### Cloud environment variables

Normally none are required for the project kit. Optional values:

```text
KUBEBUILDER_VERSION=4.15.0
KUBEBUILDER_SHA256=<release-artifact-sha256>
STEMCELL_MODULE=github.com/OWNER/stemcell-operator
```

`KUBEBUILDER_SHA256` is optional in the helper but recommended when the Cloud environment supports pinning it from the official release asset. `STEMCELL_MODULE` is consumed by task prompts/scaffolding, not by the kit validator.

Do not add kubeconfig, registry credentials, SSH private keys, production tokens, or a general-purpose cloud credential merely to make tests pass.

### Internet access

Keep agent internet access off unless a task needs official documentation or dependency access during the agent phase. Setup scripts have their own installation phase. Prefer narrow allowlists over unrestricted access.

## 3. Open the local project in Codex app

Add the repository as a Codex app project. Start a new thread from the repository root so Codex discovers root `AGENTS.md` and `.agents/skills`.

Use Worktree mode for normal implementation and integration. Use Local mode only when direct edits to the main checkout are intentional.

The tracked `.worktreeinclude` is intentionally empty except for comments. Do not add kubeconfig, `.env` secrets, registry credentials, SSH keys, or tokens merely to make a managed Worktree behave like the Local checkout.

## 4. Configure Local environment

In the Codex app project settings, configure the Worktree setup script as:

```bash
./scripts/codex-worktree-setup.sh
```

Recommended project actions:

| Action | Script |
|---|---|
| Kit check | `./scripts/check-codex-kit.py` |
| Cloud-safe verify | `./scripts/verify-cloud.sh` |
| Local verify | `./scripts/verify-local.sh` |
| kind safety preflight | `./scripts/kind-e2e-preflight.sh` |

Codex app may generate local-environment configuration under `.codex`. Review the generated file before committing it, especially any machine-specific paths or secrets.

## 5. Configure GitHub review

In Codex settings, enable code review for the repository. Reviews can then be requested on a PR with:

```text
@codex review
```

The root `AGENTS.md` contains repository review guidelines. Automatic review is optional. Human review and local integration remain required.

## 6. Notifications

Codex app Automation results appear in the app's Triage inbox. Cloud tasks and PR activity are visible in Codex/GitHub.

For email completion signals, use GitHub's notification settings for PR activity and ensure Cloud tasks create a draft PR or update an assigned PR. This kit does not store SMTP credentials and does not claim a built-in Codex email notification path.

## 7. Smoke test

Run a Cloud thread with:

```text
Read AGENTS.md and docs/OPERATING_MODEL.md. State the execution mode,
list the instruction files and project skills you discovered, and run
./scripts/check-codex-kit.py. Do not edit files.
```

Run a local Worktree thread with the same prompt, then verify the project action buttons execute in the Worktree directory.
