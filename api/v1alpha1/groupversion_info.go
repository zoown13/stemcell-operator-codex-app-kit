// Package v1alpha1 contains API schema definitions for the genome v1alpha1 API group.
//
// This M0 scaffold intentionally keeps the package dependency-light. Later milestones
// will replace these placeholders with Kubebuilder-generated Kubernetes runtime
// registration once the CRD contract is implemented.
package v1alpha1

const (
	// Group is the Kubernetes API group for StemCell resources.
	Group = "genome.stemcell.io"

	// Version is the Kubernetes API version for StemCell resources.
	Version = "v1alpha1"
)

// GroupVersion identifies the StemCell API group and version.
var GroupVersion = struct {
	Group   string
	Version string
}{Group: Group, Version: Version}
