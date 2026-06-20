---
name: stemcell-plan
description: Plan one bounded StemCell Operator change by mapping specification criteria, architecture invariants, files, tests, risks, and specialist-agent work.
---

# StemCell change planning

Use this skill before any change that touches more than one architectural layer or more than three files.

## Inputs

- current user task;
- highest-priority relevant item in `docs/BACKLOG.md`;
- current diff and repository state;
- `docs/SPEC.md` success criteria.

## Workflow

1. Read `AGENTS.md`, `Instructions.md`, `docs/SPEC.md`, `docs/ARCHITECTURE.md`, and the relevant code/tests.
2. State the selected backlog item and exact success criteria.
3. Explicitly delegate a read-only plan to the `architect` agent.
4. Independently verify the architect's assumptions against the repository.
5. Produce a dependency-ordered plan containing:
   - behavior and API changes;
   - files expected to change;
   - generated artifacts;
   - tests to write before or with code;
   - security and rollback effects;
   - exact verification commands;
   - stop conditions.
6. Keep the plan to one vertical slice. Move unrelated ideas to follow-up notes.

## Required invariants

- same immutable image for all roles;
- exactly one expressed role per pod;
- declarative rollout, not in-process mutation;
- no arbitrary execution or runtime download surface;
- deterministic expression;
- restart-safe transition state.

## Output

Return a concise implementation plan and acceptance matrix. Do not edit code while using this skill unless the parent task explicitly combines planning and implementation.
