# Cloud orchestration — bounded overnight batch

Use this document to create several independent Cloud tasks. Do not paste it as one “work for eight hours” task.

## Preparation

1. Choose a stable base revision and one current milestone.
2. Decompose work into three to five tasks with non-overlapping owned paths.
3. Avoid parallel tasks that both edit API types, generated manifests, `go.mod`, or backlog checkboxes.
4. Give each task a stop condition and a reviewable deliverable.

## Example batch after M1 is integrated

- Task A: run `03-m2-expression-engine.md`; owns `internal/expression/**`.
- Task B: run `04-m3-universal-runtime.md`; owns runtime paths and image files.
- Task C: run `06-independent-review.md` against the stable M1 branch; read-only.
- Task D: improve already-valid contributor documentation only; owns explicitly named docs.

## Completion contract

Each task must leave a reviewable diff/branch/draft PR, exact commands, unresolved findings, and a `LOCAL_REQUIRED` list. The next-day Local Worktree integrates tasks sequentially and runs `prompts/local/01-integrate-cloud-change.md` followed by the applicable local validation prompt.
