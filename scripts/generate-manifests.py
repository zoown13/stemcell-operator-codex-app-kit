#!/usr/bin/env python3
"""Write stable M0 scaffold manifests without requiring network-installed generators."""
from pathlib import Path

FILES = {
    "config/crd/bases/genome.stemcell.io_stemcells.yaml": """apiVersion: apiextensions.k8s.io/v1
kind: CustomResourceDefinition
metadata:
  name: stemcells.genome.stemcell.io
spec:
  group: genome.stemcell.io
  names:
    kind: StemCell
    listKind: StemCellList
    plural: stemcells
    singular: stemcell
  scope: Namespaced
  versions:
    - name: v1alpha1
      served: true
      storage: true
      subresources:
        status: {}
      schema:
        openAPIV3Schema:
          type: object
          description: StemCell is the Schema for the stemcells API.
          properties:
            apiVersion:
              type: string
            kind:
              type: string
            metadata:
              type: object
            spec:
              type: object
            status:
              type: object
""",
    "config/rbac/role.yaml": """apiVersion: rbac.authorization.k8s.io/v1
kind: ClusterRole
metadata:
  name: stemcell-manager-role
rules:
  - apiGroups: [\"genome.stemcell.io\"]
    resources: [\"stemcells\"]
    verbs: [\"get\", \"list\", \"watch\"]
""",
}

for relative, content in FILES.items():
    path = Path(relative)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8")
