---
name: stemcell-runtime-role
description: Add or change a bounded role in the universal StemCell runtime while preserving one binary/image, common lifecycle endpoints, graceful shutdown, and security constraints.
---

# Universal runtime role workflow

Use for `cmd/runtime` and `internal/runtime/roles` changes.

## Workflow

1. Confirm the role is one of the specification's fixed enums.
2. Define behavior through the shared role lifecycle interface.
3. Dispatch from one binary using validated `STEMCELL_ROLE`; never spawn downloaded or user-selected executables.
4. Provide common `/healthz`, `/readyz`, and `/role` behavior.
5. Make readiness represent actual role initialization.
6. Honor context cancellation and `SIGTERM`; bound shutdown.
7. Keep the MVP deterministic and self-contained. The `ai` role is a local stub with no model download.
8. Add role contract tests, invalid-role tests, graceful-shutdown tests, and race checks.
9. Review the container image for non-root execution, minimal writable paths, and no role-specific image stages.
10. Ask `security_reviewer` and `test_engineer` for independent checks.

## Prohibited designs

- Go plugins, `dlopen`, shell dispatch, embedded interpreters for user input;
- runtime package/model downloads;
- multiple simultaneously active roles in one process;
- role-specific image references or mutable tags selected by the CRD.
