package v1alpha1

import "testing"

func TestGroupVersion(t *testing.T) {
	if GroupVersion.Group != "genome.stemcell.io" {
		t.Fatalf("GroupVersion.Group = %q, want genome.stemcell.io", GroupVersion.Group)
	}
	if GroupVersion.Version != "v1alpha1" {
		t.Fatalf("GroupVersion.Version = %q, want v1alpha1", GroupVersion.Version)
	}
}
