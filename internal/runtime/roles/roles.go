package roles

import "fmt"

const (
	RoleAPI    = "api"
	RoleWorker = "worker"
	RoleAI     = "ai"
)

// Supported reports whether role is one of the bounded StemCell runtime roles.
func Supported(role string) bool {
	switch role {
	case RoleAPI, RoleWorker, RoleAI:
		return true
	default:
		return false
	}
}

// Validate returns an error for unsupported roles.
func Validate(role string) error {
	if Supported(role) {
		return nil
	}
	return fmt.Errorf("unsupported stemcell role %q", role)
}
