---
name: stemcell-crd
description: Implement or review StemCell CRD fields, validation, defaults, status, generated manifests, samples, and API tests from the project specification.
---

# Implement a StemCell CRD change

Use for changes to `api/v1alpha1`, CRD manifests, samples, or public API semantics.

## Workflow

1. Map every requested field to a behavior in `docs/SPEC.md`.
2. Identify whether the change is additive, breaking, defaulting, status-only, or validation-only.
3. Define typed enums and bounded structures; avoid generic maps except the external ConfigMap snapshot.
4. Add Kubebuilder validation/defaulting markers and status subresource markers.
5. Prevent unsafe values:
   - no arbitrary commands, args, scripts, plugin URLs, templates, or per-role images;
   - conservative length and item bounds;
   - unique rule names;
   - enum and duration constraints.
6. Update deepcopy/generated code and CRD manifests only through generation targets.
7. Update sample YAML and printer columns when useful.
8. Add API/envtest coverage for valid, invalid, defaulted, and round-trip cases.
9. Ask `code_reviewer` to check compatibility and `security_reviewer` to check execution/injection surfaces.

## Required evidence

- generated diff reviewed;
- `make manifests generate` is idempotent;
- focused tests and full API tests pass;
- affected success criteria are named.
