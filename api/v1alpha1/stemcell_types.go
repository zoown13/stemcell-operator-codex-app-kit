package v1alpha1

// StemCellSpec defines the desired state of StemCell.
type StemCellSpec struct {
	// TODO(M1): add genome, expression policy, validation markers, and defaults.
}

// StemCellStatus defines the observed state of StemCell.
type StemCellStatus struct {
	// TODO(M1): add observed generation, roles, revision, timestamps, and conditions.
}

// StemCell is the Schema for the stemcells API.
type StemCell struct {
	APIVersion string            `json:"apiVersion,omitempty"`
	Kind       string            `json:"kind,omitempty"`
	Metadata   map[string]string `json:"metadata,omitempty"`

	Spec   StemCellSpec   `json:"spec,omitempty"`
	Status StemCellStatus `json:"status,omitempty"`
}

// StemCellList contains a list of StemCell.
type StemCellList struct {
	Items []StemCell `json:"items"`
}
