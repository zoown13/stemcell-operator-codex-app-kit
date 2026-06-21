package controller

import (
	"context"
	"fmt"
)

// StemCellReconciler is the M0 controller skeleton.
//
// Later milestones will wire this type to controller-runtime and implement declarative
// Deployment and Service reconciliation. M0 keeps the type compileable without adding
// M1 CRD fields or transition behavior.
type StemCellReconciler struct{}

// Reconcile validates that the skeleton can be called with a context.
func (r *StemCellReconciler) Reconcile(ctx context.Context, namespace, name string) error {
	if err := ctx.Err(); err != nil {
		return fmt.Errorf("reconcile stemcell %s/%s: %w", namespace, name, err)
	}
	return nil
}
