# Local Worktree — final milestone acceptance review

Use after Cloud implementation has been integrated and all mapped local checks have run.

1. State milestone, base/head revisions, and every claimed SC criterion.
2. Collect Cloud handoffs, local validation reports, generated-file evidence, and open review findings.
3. Spawn `code_reviewer`, `test_engineer`, and `security_reviewer`; spawn `deployment_validator` when Kubernetes behavior is in scope.
4. Re-run the smallest decisive checks for any disputed claim.
5. Reject completion when a mandatory criterion is failed, skipped without an approved deferral, or supported only by assertions rather than observations.
6. Update `docs/BACKLOG.md` only for items whose acceptance evidence is present and reproducible.
7. Produce a final table: criterion, evidence, command/report, result, residual risk.
8. Do not merge, tag, or release without explicit human instruction.
