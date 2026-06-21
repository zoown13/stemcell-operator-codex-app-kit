package main

import (
	"fmt"
	"os"

	"github.com/stemcell/stemcell-operator/internal/runtime/roles"
)

func main() {
	role := os.Getenv("STEMCELL_ROLE")
	if err := roles.Validate(role); err != nil {
		fmt.Fprintln(os.Stderr, err)
		os.Exit(1)
	}
	fmt.Printf("stemcell runtime scaffold role=%s\n", role)
}
