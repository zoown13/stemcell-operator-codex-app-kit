package main

import (
	"context"
	"fmt"
	"os"

	"github.com/stemcell/stemcell-operator/internal/controller"
)

func main() {
	reconciler := &controller.StemCellReconciler{}
	if err := reconciler.Reconcile(context.Background(), "", ""); err != nil {
		fmt.Fprintln(os.Stderr, err)
		os.Exit(1)
	}
	fmt.Println("stemcell manager scaffold")
}
