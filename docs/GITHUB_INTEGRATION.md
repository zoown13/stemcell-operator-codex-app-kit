# GitHub integration

## 1. Cloud output

Codex Cloud can create a PR from its work after the repository is connected. Prefer a draft PR until Cloud-safe checks and Local integration are complete.

Suggested PR title:

```text
feat(<scope>): implement <bounded behavior>
```

The PR body should use `.github/pull_request_template.md` and clearly separate Cloud evidence from `LOCAL_REQUIRED` evidence.

## 2. Codex code review

Request a review in a PR comment:

```text
@codex review
```

For a focused review:

```text
@codex review for reconciliation restart safety, status conditions, and same-image invariants
```

Repository-specific review rules come from `AGENTS.md`. Automatic review may be enabled in Codex settings.

## 3. Fixing findings

Apply findings in the same feature branch only after confirming they are valid and in scope. A review agent should not silently redesign the API or broaden the milestone.

After fixes:

1. rerun Cloud-safe checks;
2. request a fresh review when behavior changed materially;
3. perform Local Worktree integration for Docker/kind criteria;
4. update the PR with local evidence;
5. merge only after human approval.

## 4. Notification contract

For overnight Cloud work, define “completion” as one of:

- a draft PR created;
- an existing PR updated;
- a Cloud task result ready for review.

Use GitHub repository/PR notification settings for email alerts. No `OPENAI_API_KEY`, SMTP secret, or Codex Action is needed in this repository.
