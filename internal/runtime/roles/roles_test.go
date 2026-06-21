package roles

import "testing"

func TestValidate(t *testing.T) {
	for _, role := range []string{RoleAPI, RoleWorker, RoleAI} {
		if err := Validate(role); err != nil {
			t.Fatalf("Validate(%q) error = %v", role, err)
		}
	}
	if err := Validate("shell"); err == nil {
		t.Fatal("Validate(unsupported) expected error")
	}
}
